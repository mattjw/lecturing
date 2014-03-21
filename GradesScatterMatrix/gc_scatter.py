"""
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
import matplotlib.pyplot as plt
import numpy as np


def gradematrix_plot(raw_dataframe, diagonal='kde'):
    if diagonal not in ['hist', 'kde']:
        raise ValueError("%s not valid diagonal chart type" % diagonal)
    
    #
    # Extract numeric columns (presumed to be marks)
    # Empty columns are ignored
    numeric_colnames = []
    for colname in raw_dataframe.columns:
        col = dat[colname].dropna()
        if (len(col) > 0) and (col.dtype == 'float64'):
            numeric_colnames.append(colname)
    
    dframe = raw_dataframe.reindex(columns=numeric_colnames)
    
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
    # Plot
    ax_mat = pd.tools.plotting.scatter_matrix(dframe, alpha=0.3, figsize=(12, 12), diagonal=diagonal)
    
    #
    # Normalise axes limits
    num_cols = len(grade_ranges)
    for indx, colname in enumerate(dframe.columns):
        # set in column
        l,r = grade_ranges[indx]
        
        # set widths, including diagonals
        for row_indx in xrange(num_cols):
            ax = ax_mat[row_indx,indx]
            ax.set_xlim(left=l, right=r)
        
        # set heights, excluding diagonals
        for col_indx in xrange(num_cols):
            if col_indx == indx:
                continue
            ax = ax_mat[indx,col_indx]
            ax.set_ylim(bottom=l, top=r)
    
    #
    # Set axes label orientations
    
    # Each cell in left column:
    for indx in xrange(num_cols):
        ax = ax_mat[indx,0]
        lab = ax.get_ylabel()
        ax.set_ylabel(lab, rotation='horizontal', horizontalalignment='right')
        
    # Move bottom xaxes to above:
    for indx in xrange(num_cols):
        # bottom label:
        ax_bott = ax_mat[-1,indx]
        ax_bott.xaxis.set_visible(False)
        lab = ax_bott.get_xlabel()
        
        # top:
        ax_top = ax_mat[0,indx]
        
        ax_top.xaxis.tick_top()
        xticks = ax_top.get_xticklabels()
        for xtick in xticks:
            xtick.set_rotation('vertical')
            xtick.set_verticalalignment('bottom')
            xtick.set_horizontalalignment('left')
        
        ax_top.xaxis.set_label_position('top')
        ax_top.set_xlabel(lab, rotation='vertical', verticalalignment='bottom')
        
        ax_top.xaxis.set_visible(True)
    
    #
    # Fix the top-left-most plot. Y axis incorrectly set to probability distro
    # (Dirty hack follows. May not be correct to scale, but potentially close.)
    ax = ax_mat[0,0]
    mn, mx = grade_ranges[0]
    nlabels = len(ax.get_yticklabels())
    labels = map( int, np.linspace(mn, mx, nlabels) )
    ax.set_yticklabels(labels)
    
    #
    # Hide overlapping tick labels
    for indx in xrange(num_cols):
        # top cell; x axis
        ax = ax_mat[0,indx]
        ax.get_xticklabels()[-1].set_visible(False)
        ax.get_xticklabels()[0].set_visible(False)
        
        # left cell; y axis
        ax = ax_mat[indx,0]
        ax.get_yticklabels()[-1].set_visible(False)
        ax.get_yticklabels()[0].set_visible(False)
    
    #
    # Add border around visualisation to highlight correlation coefficient
    coefs = np.zeros(ax_mat.shape)
    for row_indx, rname in enumerate(dframe.columns):
        for col_indx, cname in enumerate(dframe.columns):
            if row_indx == col_indx:
                continue
            a1 = dframe[rname]
            a2 = dframe[cname]

            x = np.matrix([a1, a2]).transpose()
    
            # filter out a row that has a nan on it
            keepers = (~( np.isnan(a1) | np.isnan(a2) )).nonzero()[0]
            x = x[keepers,:]
            x = x.transpose()
                
            coe_mat = np.corrcoef(x)
            c = coe_mat[0,1]
            coefs[row_indx,col_indx] = c

    cmap = mpl.cm.get_cmap('PuBu')  # PuBu, Reds
    
    for row_indx, rname in enumerate(dframe.columns):
        for col_indx, cname in enumerate(dframe.columns):
            if row_indx == col_indx:
                continue
            ax = ax_mat[row_indx,col_indx]
            x_range = ax.get_xlim()
            y_range = ax.get_ylim()

            lowleft = (x_range[0], y_range[0])
            w = x_range[1]
            h = y_range[1]
            
            corr = np.abs(coefs[row_indx,col_indx])  # in range [0,1]
            col = cmap(corr)
                       
            rect = mpl.patches.Rectangle(lowleft, w, h, color=col, linewidth=12, fill=False)
            ax.add_patch(rect)
    
    return plt.gcf()


if __name__ == "__main__":
    fin = sys.argv[1]
    
    dat = pd.read_csv(fin)
    f = gradematrix_plot(dat)
    
    head, tail = os.path.split(fin)
    fout = os.path.splitext(tail)[0] + '.pdf'
    f.savefig(fout, bbox_inches='tight')
    
    
    
    