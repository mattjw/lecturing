import csv
import re

inMarkFileName = "gc_1314-CM1103_fullgc_2014-02-04-13-46-39.csv" # csv with marks downloaded from Learning Central
simsFileName = "10008116_2013_4_SEM1_CM1103_13A_002_SAS.CSV" # csv exported from SIMS mark entry 
outFileName = "temp.csv"  # Output file to be uploaded to SIMS

ID_COL = 3 # Column in inMarkFileName containing the student id (without initial "c")
SIMS_ID_COL = 6 # Column in simsFileName containing the student id
OUT_MARK_COL = 9 # Column to place the marks in

# Should be the only change needed 
IN_MARK_COL = 17 # Column containing marks to upload

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
            row[OUT_MARK_COL] = int(marks[number])
        else:
            print "No mark for " + number + " " + row[7]
    out.writerow(row)
