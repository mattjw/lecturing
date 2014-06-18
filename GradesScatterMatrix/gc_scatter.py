"""
Generate a scatter-correlation matrix for all courseworks in a single
GradeCentre module.

GradeCentre export options:
    * Data To Download: Full Grade Centre
    * Delimiter Type: Comma
    * Include Hidden Information: No
"""


import re
import sys
import os
import collections


import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


from scatter_correlation_matrix import scatter_correlation_matrix


def gc_scatter_correlation_matrix(raw_dataframe, diagonal='kde',
                                  annotate_correlation=False):
    #
    # Filter non-numeric columns
    # Empty columns will also be dropped.
    numeric_colnames = []
    for colname in raw_dataframe.columns:
        col = dat[colname].dropna()
        if (len(col) > 0) and (col.dtype == 'float64'):
            numeric_colnames.append(colname)
    
    dframe = raw_dataframe.reindex(columns=numeric_colnames)
    colnames = dframe.columns
    num_cols = len(colnames)
    
    #
    # Find grade ranges (0 to max mark)
    grade_ranges = []
    for colname in dframe.columns:
        max_grade = re.match("^.*\[Total Pts:( up to)? (\d+).*$", colname).group(2)
        max_grade = float(max_grade)
        grade_ranges.append((0,max_grade))

    #
    # Rename to filter out GradeCentre chaff
    def transform(s):
        return re.match("^(.*?)( \[.*$)", s).group(1)
    
    dframe = dframe.rename(columns=transform)

    #
    # Rename columns with same names
    cnts = collections.Counter(dframe.columns)
    dupes = {k:v for k,v in cnts.iteritems() if v>=2}
    for name, _ in dupes.iteritems():
        dupe_indxs = dframe.columns.get_loc(name).nonzero()[0]  # indexes of duplicates
        i = 0
        for indx in dupe_indxs:
            i +=1
            prev_cols = list(dframe.columns)
            prev_cols[indx] = "%s (%d)" % (name, i)
            dframe.columns = prev_cols

    #
    # Create grade range dictionary
    ranges_dict = {}
    for indx, colname in enumerate(dframe.columns):
        ranges_dict = grade_ranges[indx]

    fig = scatter_correlation_matrix(dframe, diagonal=diagonal,
                                     annotate_correlation=annotate_correlation,
                                     ranges=ranges_dict)
    return fig


if __name__ == "__main__":
    fin = sys.argv[1]
    
    dat = pd.read_csv(fin)
    f = gc_scatter_correlation_matrix(dat, diagonal='hist',
                                      annotate_correlation=True)
    
    head, tail = os.path.split(fin)
    fout = os.path.splitext(tail)[0] + '.pdf'
    f.savefig(fout, bbox_inches='tight')



