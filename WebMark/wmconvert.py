#!/usr/bin/python

# Example:
#     wmconvert.py gc_1314-CM1103_fullgc_2014-02-04-13-46-39.csv 17 10008116_2013_4_SEM1_CM1103_13A_002_SAS.CSV temp.csv
# Try
# wmconvert.py --help
# for help

# WebMark export instructions:
# SIMS -> Assessment Management -> Assessment Mark Entry (School) -> Retrieve the relevant module
# Select single assessment via checkbox
# Display all students
# Export marks
# Generate assessment only

# GradeCentre export instructions:
# Full Grade Centre
# Work Offline -> Download
# Selected Column: Chose relevant mark
# Delimiter Type: Comma

# WebMark import instructions:
# SIMS -> Assessment Management -> Assessment Mark Entry (School) -> Retrieve the relevant module
# Select assessment via checkbox
# Import Marks
# Initial Assessments

# Verify upload:
# SIMS -> Assessment Management -> Assessment Mark Entry (School) -> Retrieve the relevant module
# Select assessment via checkbox
# View Module Results

import csv
import re
import argparse
import os

#
# Parse args
parser = argparse.ArgumentParser(description="SIMS Web Mark Converter. Converts from a file exported from Learning Central GradeCentre to Web Mark Entry. Columns are indexed from 1.")

# Optional (keyword) args...
parser.add_argument('--gc_sid_column', action='store', type=int,
                    default=4,
                    help="Column number in the GradeCentre file containing the student id (without initial 'c')" )
parser.add_argument('--wm_sid_column', action='store', type=int,
                    default=7,
                    help="Column number in the WebMark file containing the student id" )
parser.add_argument('--wm_mark_column', action='store', type=int,
                    default=10,
                    help="""Column number in the web mark file into which marks will be inserted (should be the "Mark" column)""" )


# Manadtory (positional) args...
parser.add_argument('gc_file', action='store', type=str,
                     help='GradeCentre file -- the CSV file with marks downloaded from Learning Central GradeCentre')
parser.add_argument('gc_mark_col', action='store', type=int,
                     help='Column in the GraceCentre file containing marks to upload (indexed from 1)')
parser.add_argument('wm_file', action='store', type=str,
                     help='WebMark file -- CSV file with exported from SIMS Web Mark Entry')
parser.add_argument('outfile', action='store', type=str,
                     help='Output file -- this will be a copy of the original WebMark file with marks inserted')

args = parser.parse_args()

#
# Grab args
inMarkFileName = args.gc_file  # inMarkFileName = "gc_1314-CM1103_fullgc_2014-02-04-13-46-39.csv" # csv with marks downloaded from Learning Central
simsFileName = args.wm_file  # simsFileName = "10008116_2013_4_SEM1_CM1103_13A_002_SAS.CSV" # csv exported from SIMS mark entry 
outFileName = args.outfile  # outFileName = "temp.csv"  # Output file to be uploaded to SIMS

ID_COL = args.gc_sid_column  #ID_COL = 3 # Column in inMarkFileName containing the student id (without initial "c")
SIMS_ID_COL = args.wm_sid_column  # SIMS_ID_COL = 6 # Column in simsFileName containing the student id
OUT_MARK_COL = args.wm_mark_column  # OUT_MARK_COL = 9  # Column to place the marks in

IN_MARK_COL = args.gc_mark_col #  IN_MARK_COL = 17 # Column containing marks to upload

#
# Echo back
print
print "Input GradeCentre file: ", inMarkFileName
print " ...with student numbers in column: ", ID_COL
print " ...and marks in column:            ", IN_MARK_COL
print "Input WebMark file: ", simsFileName
print " ...with student numbers in column: ", SIMS_ID_COL
print "Output file: ", outFileName
print " ...with marks to be inserted in column: ", OUT_MARK_COL
print

#
# Re-index columns from 0
ID_COL -= 1
SIMS_ID_COL -= 1

IN_MARK_COL -= 1
OUT_MARK_COL -= 1

#
# Validation
for fpath in [inMarkFileName, simsFileName]:
    if not os.path.exists(fpath):
        print "Failed!\nFile '%s' not found" % (fpath)
        exit(1)
    if not os.path.isfile(fpath):
        print "Failed!\n'%s' is not a file" % (fpath)
        exit(1)

#
# Process
rdr = csv.reader(open(inMarkFileName, "rU"))

marks = {}

for row in rdr:
    marks[row[ID_COL]] = row[IN_MARK_COL]

rdr = csv.reader(open(simsFileName, "rU"))
out = csv.writer(open(outFileName, "w"))

for row in rdr:
    no = re.match("#([\d]+)/", row[SIMS_ID_COL])
    if no:
        number = no.groups()[0]
        if number in marks:
            gc_mark = float(marks[number])
            as_int = int(round(gc_mark))
            row[OUT_MARK_COL] = as_int
        else:
            print "No mark for " + number + " " + row[7]
    out.writerow(row)
