#!/usr/bin/env python

##!/usr/bin/python2.7

"""
Some lecturers provide the coursework grades and feedback to students through
Learning Central's GradeCentre. This scripts converts GradeCentre feedback to
HTML or PDF reports. A report is generated for each student.

The motivating use case for this script is to generate reports that can be
distributed to external moderators.

Input format:
* Learning Central -> Full Grade Centre
* Select submenu for chosen coursework -> View Grade History
* Show Entries from Past: "All"
  By default, this should be sorted in reverse chronological order (most-recent
  first). Check that this is the case.
* "Download"
* Delimiter Type: Comma; Include Comments: yes
* Submit and download.

By default, reports are generated as HTML. For PDF reports, please select the
PDF output option and install the following dependences:
* Python -- xhtml2pdf
"""

# MattJW
# 1.0.0


import csv
import os.path
import cStringIO
import argparse
import xhtml2pdf.pisa as pisa


if __name__ == "__main__":
    #
    # Args
    parser = argparse.ArgumentParser(description="Generate coursework feedback reports from GradeCentre.""")

    # Optionals
    parser.add_argument('--type', action='store', type=str,
                        default="html",
                        choices=['pdf', 'html'],
                        help="Type of report file. Reports can be generated as HTML or PDF." )

    # Mandatories
    parser.add_argument('gc_file', action='store', type=str,
                        help='GradeCentre file -- the CSV file containing coursework grades and feedback.')

    parser.add_argument('out_dir', action='store', type=str,
                        help='Path to the directory to which reports will be saved. Directory will be created if not found.')

    # Extract
    args = parser.parse_args()

    in_path = args.gc_file
    outdir_path = args.out_dir

    report_type = args.type

    if report_type == "pdf":
        import xhtml2pdf.pisa as pisa

    #
    # Reader
    fin = open(in_path, 'r')
    rdr = csv.DictReader(fin)

    #
    # Output dir
    if not os.path.exists(outdir_path):
        os.mkdir(outdir_path)

    if not os.path.isdir(outdir_path):
        print "Directory does not exist or could not be created"
        print outdir_path
        exit(1)

    #
    # Generate reports
    students = {}

    for row in rdr:
        stdname = row['User']
        if stdname not in students:
            dct = {}
            dct['FullName'] = row['User']
            dct['Grade'] = row['Value']
            dct['GCFeedback'] = row['Feedback to User']
            dct['CWName'] = row['Column']
            dct['GradedBy'] = row['Last Edited by: Name']

            if row['User'] == row['Last Edited by: Name']:
                # This indicates that the row corresponds to the student's
                # original submission, not the grade by the instructor
                # This probably means the student's submission hasn't been
                # graded for some reason
                dct['Grade'] = 'n/a'
                dct['GradedBy'] = 'n/a'
                dct['GCFeedback'] = 'n/a'

            students[stdname] = dct

    for _, dct in students.iteritems():
        html_out = "<!DOCTYPE HTML>\n<html>"
        html_out += "<hr>\n"
        html_out += "<h3>Grade Info:</h3>\n"
        html_out += "<b>Student:</b> %s <br>\n" % dct['FullName']
        html_out += "<b>Grade:</b> %s <br>\n" % dct['Grade']
        html_out += "<b>Coursework:</b> %s <br>\n" % dct['CWName']
        html_out += "<b>Grader:</b> %s <br>\n" % dct['GradedBy']
        html_out += "<hr>\n<h3>Feedback:</h3>\n"
        html_out += dct['GCFeedback']
        html_out += "<hr>\n"
        html_out += "</body></html>"

        if report_type == "html":
            fname = dct['FullName'].replace(' ', '') + ".html"
            out_path = os.path.join(outdir_path, fname)

            print out_path

            fout = open(out_path, 'w')
            fout.write(html_out)
            fout.close()
        elif report_type == "pdf":
            fname = dct['FullName'].replace(' ', '') + ".pdf"
            out_path = os.path.join(outdir_path, fname)

            print out_path

            #pdfkit.from_string(html_out, out_path)

            strIO = cStringIO.StringIO(html_out)
            fout = open(out_path, 'w')
            pdf = pisa.CreatePDF(strIO, fout)
            fout.close()
        else:
            assert False

    #
    # Fin.
    fin.close()
