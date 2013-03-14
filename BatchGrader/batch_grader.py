#!/usr/bin/python

"""
Author:  Matt J Williams
Date:    Wed 6 Mar 2013 21:00


## USAGE ## 
usage: batch_grader.py [-h] [--autograder AUTOGRADER]
                       unittest_class_file 
                       submissions_directory
                       spreadsheet_file

AUTOGRADER:
Java class file for the autograder application. If in a package, use the
standard Java dot-separated format.

unittest_class_file:
The class file for the unit tests. This should be compatible with the
autograder.

submissions_directory:
The directory containing student submissions. Each submission is itself
a directory.

spreadsheet_file:
A CSV file into which the final grades will be inserted. The input file
should be downloaded from GradeCentre. Note this file WILL BE OVERWRITTEN
with the new grades.


## EXAMPLES ##
    batch_grader.py  --autograder=autograding.CSIJUnitGrader  ./Assignment1UnitTests.class  ./CM1203+CM1207-A1/  ./test.csv 
    batch_grader.py  ./Assignment1UnitTests.class  ./CM1203+CM1207-A1/  ./test.csv 


## PREPARATION ##
The unit tests file should be compiled to produce its class file. 


## SUBMISSIONS DIRECTORY ##
The submissions directory shoulld contain multiple subdirectories. Each 
subdir represents a single student's submission. The directory should 
be named as their username, e.g. c0000000.


## SPREADSHEET ##
Espected as a CSV file.

Instructions:
    Grade Centre -> Work offline -> Download
    Select Data to Download = Selected Column
        (Choose the column for this assessment. User info us automatically 
        included.)
    Delimiter Type = Comma
    Include Hidden Information = No

Expected fields...
    1 Last Name
    2 First Name
    3 Username
    4 Student ID
    5 Last Access
    6 Availability
    7 XXX|XXX                    (this 7th field should be the grade)

This script will pad the spreadsheet to eight columns. Extra column(s) are:
* Notes on the autograding attempt. E.g., if compilation failed.


## REQUIRES ##
java
javac


## POSSIBLE VULNERABILITIES ##
A submission that prints out integers as the last thing it does? Without 
a newline at the end. This would concatenate with the mark printed by the 
Java autograder.
"""

import os.path
import os
import re
import shutil
import subprocess
import csv
import sys
import argparse

DEFAULT_AUTOGRADER_JAVA_APP = "autograding.CSIJUnitGrader"
    # default java application that does grading

SPREADSHEET_STUDNUM_COL = 3  # index from 0
    # index of the student number column

SPREADSHEET_GRADES_COL = 6  # index from 0
    # index of the grades column

SPREADSHEET_COMMENTS_COL = 7
    # index of the column with extra comments

SPREADSHEET_TARGET_NUMCOLS = 8
    # pad the spreadsheet to this many columns

DEFAULT_JVM_SANBOX_SECURITY_POLICY_FNAME = "gradersandbox.policy"
    # assumed to be located in the same directory as this script
    # see: get_default_java_sandbox_policy_abspath()


#
#
# Util methods
#

def get_default_java_sandbox_policy_abspath():
    """
    Assuming there is a "gradersandbox.policy" located in the same directory
    as this script file, this method will get the absolute path to
    "gradersandbox.policy" and return it.

    Note: the abspath method depends on the current working directory, but
    __file__ does not.
    So if we change workind dir before running this method, the 
    abspath will be out of sync.
    So this method should be called BEFORE any working dir changes.
    """
    script_fullpath = os.path.abspath( __file__ )
    (head,tail) = os.path.split( script_fullpath )
    #   head = path to directory containing this script
    #   does not have / at end
    policy_fpath = head + "/" + DEFAULT_JVM_SANBOX_SECURITY_POLICY_FNAME

    return policy_fpath


#
#
# A class for handling the CSV spreasdheet.
#
class Spreadsheet(object):
    """
    Instance variables:
        spreadsheet
        spreadsheet_fpath
        target_num_cols
    """

    def __init__( self, spreadsheet_fpath, target_num_cols ):
        """
        Load a given spreadsheet file into memory and set up the object.
        """
        # Load spreadsheet
        f = open(spreadsheet_fpath, 'U')
        rdr = csv.reader( f )
        spreadsheet = [l for l in rdr]
        f.close()

        # Pad columns
        for row in spreadsheet:
            num_cols_needed = SPREADSHEET_TARGET_NUMCOLS - len( row )
            assert num_cols_needed >= 0  # if negative, then the spreadsheet has too many cols
            row.extend( ['']*num_cols_needed )

        # ivars
        self.spreadsheet = spreadsheet
        self.spreadsheet_fpath = spreadsheet_fpath
        self.target_num_cols = target_num_cols


    def save( self ):
        f = open(self.spreadsheet_fpath, 'w')
        writer = csv.writer( f )
        writer.writerows(self.spreadsheet)
        f.close()


    def set_grade_for_studno( self, find_studno, gradeval ):
        """
        Find the row corresponding to the given student number and add the 
        grade to that row.

        If no matching student number found, add a new row to the spreadsheet.

        spreadsheet should be a list of lists. First row assumed to be headers.
        Indexed as follows:
            spreadsheet[row][col]
        """
        nrows = len( self.spreadsheet )
        ncols = len( self.spreadsheet[0] )

        #
        # Find row and insert grade
        for row_index, row in enumerate( self.spreadsheet ):
            if row_index == 0:
                continue

            studno = row[SPREADSHEET_STUDNUM_COL]
            if studno == find_studno:
                row[SPREADSHEET_GRADES_COL] = gradeval
                return

        #
        # No matching row found; add a new one...
        row = ['']*ncols
        row[SPREADSHEET_STUDNUM_COL] = find_studno
        row[SPREADSHEET_GRADES_COL] = gradeval
        self.spreadsheet.append( row )

    def add_comment_for_studno( self, find_studno, comment ):
        """
        Append to the existing comments for the given student. 
        The row for the given student SHOULD EXIST ALREADY.
        """
        nrows = len( self.spreadsheet )
        ncols = len( self.spreadsheet[0] )

        #
        # Find row, append to column
        for row_index, row in enumerate( self.spreadsheet ):
            if row_index == 0:
                continue

            studno = row[SPREADSHEET_STUDNUM_COL]
            if studno == find_studno:
                current_comment = row[SPREADSHEET_COMMENTS_COL]
                current_comment += comment
                row[SPREADSHEET_COMMENTS_COL] = current_comment
                return

        assert False  # should not reach here


#
#
# HANDLING SUBMISSIONS
#

def get_studnum_from_submission_dir( submission_dir ):
    """
    Get the student's student number from the path-to-submission-directory.
    The directory should be named after the newstyle username, from which we can 
    get student number:
        c0000000 -> 0000000
    It's possible that old school usernames were used:
        scm0xxx
    In this case, it will return the username (e.g., scm0xxx).
    If no username style can be matched, the directory name is returned.
    """
    if submission_dir[-1] == "/":
        submission_dir = submission_dir.rstrip('/')

    (head,tail) = os.path.split( submission_dir )
    dirname = tail.strip('/')

    # example newstyle: c1109712
    newstyle_match = re.match( r"^([a-zA-Z])(\d{7})$", dirname )
    if newstyle_match:
        # String matches the old style
        studnum = newstyle_match.group(2)  # 0 = entire match. 1 = first group. 2 = second group.
        return studnum
    else:
        # maybe it's not the newstyle student username?
        if re.match( r"^[a-zA-Z]{3}\d[a-zA-Z]{3}$", dirname ):
            return dirname

    return submission_dir.strip( '/' )

    #raise RuntimeError( "Unexpected username for conversion to student number " + dirname )


def grade_submission_and_insert( dir_fpath, unittest_classname, autograder_java_app,
                          java_security_policy_abspath,
                          spreadsheet_obj, studno ):
    """
    Run the autograder in the given directory and obtain the grade.
    The grade will then be inserted into the spreadsheet represented by
    `spreadsheet_obj`.

    If for some reason the mark could not be obtained the method will write
    set the cell to be empty.

    This will temporarily switch the working directory to the given dir.

    If a grade was successfully obtained, this method will return the mark.
    Otherwise, None is returned.

    Comments will also be added to the spreadsheet for the following:
    * failure to obtain a mark
    * submission prints to standard out
    """
    #
    # Switch CWD
    old_cwd = os.getcwd()
    os.chdir( dir_fpath )

    #
    # Handle security policy
    #   http://docs.oracle.com/javase/6/docs/technotes/guides/security/PolicyFiles.html
    assert os.path.isfile( java_security_policy_abspath ), java_security_policy_abspath

    #
    # Compile
    
    cmd = ("java",
           "-Djava.security.manager",
           "-Djava.security.policy==%s" % (java_security_policy_abspath),
           autograder_java_app,
           "-m", unittest_classname)
    cmd = reduce( lambda x,y: "%s %s" % (x,y), cmd )
    # if no security policy:
    #cmd = ("java", autograder_java_app, "-m", unittest_classname)
    #cmd = reduce( lambda x,y: "%s %s" % (x,y), cmd )

    mark = None
    try:
        success_output = subprocess.check_output( cmd, shell=True )
            # using shell so that environment variables are available
            # i.e., .bashrc (or whatever) gets done before running cmd
        success_output = success_output.strip("\n")  # cull the newline that follows the mark

        # Need to deal with submissions that print to command line (doh!)...
        output = success_output.split("\n")
        if len( output ) > 1:
            spreadsheet_obj.add_comment_for_studno( studno, "Print statements found. " )
        
        # Get the mark...
        mark_str = output[-1]
        mark = float( mark_str )
        spreadsheet_obj.set_grade_for_studno( studno, mark )

    except subprocess.CalledProcessError, e:
        fail_cmd = e.cmd
        fail_code = e.returncode
        fail_output = e.output
        print "\t[java autograder failed: %s]" % dir_fpath 
        print "\t\t[fail cmd %s]" % str(fail_cmd)
        print "\t\t[fail code %s]" % fail_code
        spreadsheet_obj.add_comment_for_studno( studno, "Autograder failed. " )
        # print "\t\t%s" % fail_output          # check_output doesn't get stderr?

    except ValueError, e:
        # failed to convert string to float?
        raise e

    #
    # Revert CWD
    os.chdir( old_cwd )

    return mark


def compile_submission( dir_fpath ):
    """
    Compile all .java files in a given directory.
    This will temporarily switch the working directory to the given dir.

    Returns True if compilation was successful, False otherwise.
    """
    # Switch CWD
    old_cwd = os.getcwd()
    os.chdir( dir_fpath )

    # Compile
    success = None
    cmd = "javac *.java"
    try:
        success_output = subprocess.check_output( cmd, shell=True )
            # using shell so that environment variables are available
            # i.e., .bashrc (or whatever) gets done before running cmd
        success = True
    except subprocess.CalledProcessError, e:
        fail_cmd = e.cmd
        fail_code = e.returncode
        fail_output = e.output 
        print "\t[javac failed: %s]" % dir_fpath 
        print "\t\t[fail cmd %s]" % str(fail_cmd)
        print "\t\t[fail code %s]" % fail_code

        success = False

        # print "\t\t%s" % fail_output          # check_output doesn't get stderr?

    # Revert CWD
    os.chdir( old_cwd )

    return success


def process_submissions( unittest_classname, unittest_class_path, 
                         submissions_dir, spreadsheet_fpath, autograder_java_app,
                         java_security_policy_abspath ):
    """
    Iterate through the submissions in a given directory. Run the autograder on
    each, obtain the grade, and insert the grade into the spreadsheet/CSV file.
    """
    if submissions_dir[-1] != "/":
        submissions_dir = submissions_dir + "/"

    #
    # Prep
    submission_dirs = os.listdir( submissions_dir )  # just the filenames; no path

    # Open spreadshseet & pad columns if necessary
    spreadsheet = Spreadsheet( spreadsheet_fpath, SPREADSHEET_TARGET_NUMCOLS )

    #
    # Process submissions
    for subm_dir in submission_dirs:
        #
        # Get info
        submission_fpath = submissions_dir + subm_dir  # full path to a specific student's submission dir

        if not os.path.isdir(submission_fpath):
            # Skip over non-directories (e.g., .DS_Store)
            print "SKIP:" + submission_fpath
            print os.getcwd()
            continue

        if submission_fpath[-1] != "/":
            submission_fpath = submission_fpath + "/"
        assert os.path.isdir(submission_fpath), submission_fpath

        studnum = get_studnum_from_submission_dir( subm_dir )

        print
        print
        print
        print "**** %s ****" % studnum
        print "\tstud num:             " + studnum
        print "\tsubmission dir fpath: " + submission_fpath

        # Clear the grade for the student
        # This will also create a new row for that student if they're not
        # already in the file 
        spreadsheet.set_grade_for_studno( studnum, "" ) 

        #
        # Clean the submission dir before compilation/exec
        assert submission_fpath[-1] == "/"
        for fname in os.listdir( submission_fpath ):
            fullpath = submission_fpath + fname

            if fname.endswith( '.class' ):
                # remove class files
                os.remove(fullpath)
                print "\t\tdeleted " + fullpath
            elif unittest_classname in fname:
                # remove the test grader test file (if the student uploaded it)
                os.remove(fullpath)
                print "\t\tdeleted " + fullpath

        #
        # Copy the unit test class file in to the submission dir
        #   unittest_class_path = ./Assignment1UnitTest
        #   submission_fpath = ./CM1203+CM1207-A1/c1115684/
        class_fname = unittest_classname + ".class"  # e.g., Assignment1UnitTests.class
        class_fpath = unittest_class_path + ".class"  # e.g., /Users/matt/Desktop/Java/AutoGrading-Testing/Assignment1UnitTests.class
        shutil.copyfile( class_fpath, submission_fpath + class_fname )

        #
        # Compile
        compile_was_successful = compile_submission( submission_fpath )

        #
        # Run grader to get mark
        mark = grade_submission_and_insert( submission_fpath, unittest_classname, 
            autograder_java_app, java_security_policy_abspath,
            spreadsheet, studnum )
        print "\tmark: %s" % mark 

        #
        # Add other comments for this student 
        if not compile_was_successful:
            spreadsheet.add_comment_for_studno( studnum, "Compilation failed. " )

    #
    # Finish up...
    spreadsheet.save()


#
#
# MAIN
#
def main():
    #
    # Arg parse
    args = sys.argv
    parser = argparse.ArgumentParser(description="Batch Grader")

    # optional...
    parser.add_argument( '--autograder', action='store', type=str,
                         help='Dot-separated specifier for the autograder class',
                         default=DEFAULT_AUTOGRADER_JAVA_APP,  # default val. thus optional
                         dest='autograder' )  # the ivar used in ArgumentParser results

    # non-optional...
    parser.add_argument( 'unittest_class_file', action='store', type=str,
                         help="Path to unit test class file" )
    parser.add_argument( 'submissions_directory', action='store', type=str,
                         help="Path to directory containing submissions to be graded" )
    parser.add_argument( 'spreadsheet_file', action='store', type=str,
                         help="Path to spreadsheet file" )

    # Grab args...
    results = parser.parse_args()
    SUBMISSIONS_DIR = results.submissions_directory
    UNITTEST_CLASS_FPATH = results.unittest_class_file
    SPREADSHEET_FPATH = results.spreadsheet_file
    AUTOGRADER_JAVA_APP = results.autograder

    #SUBMISSIONS_DIR = "./CM1203+CM1207-A1/"
    #UNITTEST_CLASS_FPATH = "./Assignment1UnitTests.class"
    #SPREADSHEET_FPATH = "./test.csv"
    #AUTOGRADER_JAVA_APP = "autograding.CSIJUnitGrader"
    # Example:
    #   batch_grader.py  --autograder=autograding.CSIJUnitGrader  ./Assignment1UnitTests.class  ./CM1203+CM1207-A1/  ./test.csv 
    #   batch_grader.py  ./Assignment1UnitTests.class  ./CM1203+CM1207-A1/  ./test.csv 

    #
    # Arg proc
    SUBMISSIONS_DIR = os.path.abspath( SUBMISSIONS_DIR )
    UNITTEST_CLASS_FPATH = os.path.abspath( UNITTEST_CLASS_FPATH )
    SPREADSHEET_FPATH = os.path.abspath( SPREADSHEET_FPATH )


    assert os.path.isfile( UNITTEST_CLASS_FPATH ), "No class file found: " + UNITTEST_CLASS_FPATH
    (head,tail) = os.path.split( UNITTEST_CLASS_FPATH )
    #   head -- does not have a / at the end
    #   tail -- does not have a / at the start
    head = head + "/"
    assert ".class" in tail
    
    unittest_classname = tail.replace(".class","").strip('/')  # e.g., Assignment1UnitTest
    unittest_class_path = head + unittest_classname  # e.g., ./Assignment1UnitTest. Doesn't include the extension

    assert os.path.isdir( SUBMISSIONS_DIR )
    assert os.path.isfile( SPREADSHEET_FPATH ), SPREADSHEET_FPATH

    java_security_policy_abspath = get_default_java_sandbox_policy_abspath()

    #
    # Begin
    process_submissions( unittest_classname, unittest_class_path, 
                         SUBMISSIONS_DIR, SPREADSHEET_FPATH, 
                         AUTOGRADER_JAVA_APP,
                         java_security_policy_abspath )


if __name__ == "__main__":
    main()




