import re
import sys
import os
import collections
from textwrap import wrap


import pandas as pd
import matplotlib as mpl
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def clear_axes_contents(ax):
    # clear the main canvas of the axes
    # leave axes labels intact
    #
    # cannot use ax.clear() because it clears labels

    keep_types = [matplotlib.axis.XAxis,
                  matplotlib.axis.YAxis,
                  matplotlib.spines.Spine]
    #
    # matplotlib.collections.PathCollection
    # matplotlib.spines.Spine
    # matplotlib.axis.XAxis
    # matplotlib.axis.YAxis
    # matplotlib.patches.Rectangle
    # matplotlib.text.Text
    #
    # Whether they can be removed or not depends on the context in which
    # they're stored

    children = ax.get_children()  # children artists
    for child in children:
        ty = type(child)
        if ty not in keep_types:
            try:
                child.remove()
            except NotImplementedError:
                pass


def scatter_correlation_matrix(dataframe, onlycols=None, ignorecols=None,
                               diagonal='kde', ranges={},
                               annotate_correlation=True, 
                               colour_correlation=True):
    """
    Plot a scatter matrix from a `pandas` DataFrame.

    The matrix is composed of the following:
    * Upper triangle: A joint scatter plot for each pair of columns.
    * Lower triangle: The Pearson correlation coefficient of each pair of
      columns.
    * Diagonal: Distribution of each column.

    By default, all numeric columns present in `dataframe` will be included
    in the scatter matrix. Non-numeric columns are ignored.

    Args:
        dataframe (DataFrame):
        Data to be plotted on the scatter matrix.

        onlycols (list of str, optional), ignorecols (list of str, optional):
        Control the columns that are included in the scatter matrix by either
        providing a prescriptive list (`onlycol`) or an ignore list
        (`ignorecols`). Do not use both. Non-numeric columns will always be
        ignored.

        ranges (dict, optional): The ranges of columns. Used to set the
        limits of plots. Dictionary shold contain column names and their
        range. Range should be described as two-tuple: (min,max).

        annotate_correlation (bool, optional): Annotate the correlation 
        coefficient heatmap with its value.

        colour_correlation (bool, optional): Display the coloured heatmap or 
        not. If True, then squares the lower triangle will be coloured by the 
        strength of the correlation.
    Returns:
        A Figure.

    Correlation coefficient heatmaps will only be included if there are two or 
    more rows.

    Kernel density estimator (KDE) univariate curves will only be plotted if
    there are two or more rows of data.
    """
    #
    # Arg validation
    if (onlycols is not None) and (ignorecols is not None):
        raise ValueError('onlycols and ignorecols should not be combined')

    if diagonal not in ['hist', 'kde']:
        raise ValueError("%s not a valid distribution plot type" % diagonal)

    #
    # Filter columns by user requirements
    orig_cols = frozenset(dataframe.columns)
    if ignorecols is not None:
        drop_cols = orig_cols & frozenset(ignorecols)
    elif onlycols is not None:
        drop_cols = orig_cols - frozenset(only_cols)
    else:
        drop_cols = frozenset()

    dataframe = dataframe.drop(drop_cols, axis=1)

    #
    # Filter non-numeric columns
    # Empty columns will also be dropped.
    numeric_colnames = []
    for colname in dataframe.columns:
        col = dataframe[colname].dropna()
        if (len(col) > 0) and (col.dtype == 'float64'):
            numeric_colnames.append(colname)
    
    dframe = dataframe.reindex(columns=numeric_colnames)
    num_cols = len(dframe.columns)
    num_rows = len(dframe)

    #
    # Plot
    actual_diag = diagonal
    if num_rows < 2:
        actual_diag = 'hist'
    ax_mat = pd.tools.plotting.scatter_matrix(dframe, alpha=0.3,
                                              figsize=(12, 12),
                                              diagonal=actual_diag)


    #
    # Handle the case where there are too few rows for KDE
    if diagonal == "kde" and num_rows < 2:
        for i in xrange(num_cols):
            ax = ax_mat[i,i]

            clear_axes_contents(ax)

            s = "n/a"
            txt = mpl.text.Text(text=s,
                x=0.5, y=0.5,
                transform=ax.transAxes,  # axes coords (not data coords)
                horizontalalignment='center',
                verticalalignment='center',
                #fontsize='x-large',
                fontweight='roman')
            ax.add_artist(txt)

    #
    # If using 'hist' mode, override the default histogram behaviour
    # with better plots
    if diagonal == "hist":
        for i in xrange(num_cols):
            ax = ax_mat[i,i]

            clear_axes_contents(ax)

            # better histogram
            vals = dframe.iloc[:,i]

            rnge = ranges.get(dframe.columns[i], None)
            ax.hist(vals, range=rnge, bins = 20, color='b', edgecolor='b')

    #
    # Normalise axes limits
    for indx, colname in enumerate(dframe.columns):
        if colname not in ranges:
            # not every column has to be given a range
            continue

        l, r = ranges[colname]
        
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
        fsize = ax_bott.get_xticklabels()[0].get_fontsize()
        
        # top:
        ax_top = ax_mat[0,indx]
        
        ax_top.xaxis.tick_top()
        xticks = ax_top.get_xticklabels()
        for xtick in xticks:
            xtick.set_rotation('vertical')
            xtick.set_verticalalignment('bottom')
            xtick.set_horizontalalignment('left')
            xtick.set_fontsize(fsize)
        
        ax_top.xaxis.set_label_position('top')
        ax_top.set_xlabel(lab, rotation='vertical', verticalalignment='bottom')
        
        ax_top.xaxis.set_visible(True)
    
    #
    # Wrap axes labels

    # top:
    for i in xrange(num_cols):
        ax = ax_mat[0,i]
        txt = ax.get_xlabel()
        wrapped = '\n'.join(wrap(txt, 34))
        ax.set_xlabel(wrapped)

    # left:
    for i in xrange(num_cols):
        ax = ax_mat[i,0]
        txt = ax.get_ylabel()
        wrapped = '\n'.join(wrap(txt, 34))
        ax.set_ylabel(wrapped)

    #
    # Fix the top-left-most plot. Y axis incorrectly set to probability distro
    # (Dirty hack follows. May not be correct to scale, but close.)
    ax = ax_mat[0,0]

    if dframe.columns[0] in ranges:
        mn, mx = ranges[dframe.columns[0]]
    else:
        mn, mx = ax.get_ylim()

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
    # Set lower triangle to visualisation of correlation coefficients

    # Compute coefficients...
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

    # Visualise coefficients -- colour and text
    cmap = mpl.cm.get_cmap('PuBu')  # PuBu, Reds    
    for row_indx, rname in enumerate(dframe.columns):
        for col_indx, cname in enumerate(dframe.columns):
            if row_indx <= col_indx:
                # skip upper triangle and diagonal
                continue
            
            ax = ax_mat[row_indx,col_indx]
            clear_axes_contents(ax)

            corr = np.abs(coefs[row_indx,col_indx])  # in range [0,1]
            col = cmap(corr)

            if colour_correlation:
                # http://matplotlib.org/1.3.1/users/recipes.html#placing-text-boxes

                # rectangle
                rect = mpl.patches.Rectangle( [0, 0], 1, 1,
                    transform=ax.transAxes,  # axes coords (not data coords)
                    color=col, linewidth=0, fill=True)
                ax.add_patch(rect)
            
            # text
            if annotate_correlation:
                if np.isnan(corr):
                    s = 'n/a'
                else:
                    s = "r=%.2f" % corr
                txt = mpl.text.Text(text=s,
                    x=0.5, y=0.5,
                    transform=ax.transAxes,  # axes coords (not data coords)
                    horizontalalignment='center',
                    verticalalignment='center',
                    #fontsize='x-large',
                    fontweight='roman')
                ax.add_artist(txt)
    
    return plt.gcf()
