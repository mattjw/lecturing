"""
Generate a scatter-correlation matrices for multiple modudules.
A single Excel file is expected. Each worksheet in the Excel file should
correspond to a particular module.
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


def scm_for_worksheet(df_raw, diagonal='kde', annotate_correlation=True,
                      colour_correlation=True):
    """
    df_raw: dataframe representing worksheet for a particular module.
    """

    cols = df_raw.columns
    ncols = len(cols)

    # Obtain subset of cols
    indxs = [2] + range(4, ncols)
        # 2 = module marks (weighted total)
        # range(4,ncols) = individual courseworks
    df = df_raw.iloc[:,indxs]  #iloc: = 0, n-1

    # Drop first row ("Mark", ...)
    #df = df.drop([0])
    df = df.iloc[1:,:]
    df = df.reset_index()

    # Drop mystical 'index' col
    df = df.drop('index', 1)

    # Change dtypes
    for cname in df.columns:
        df[cname] = df[cname].astype(float)


    # Set grade ranges for each coursework
    # (Assume all webmark grades are always 0 to 100)
    ranges_dict = {}
    for cname in df.columns:
        ranges_dict[cname] = (0.0, 100.0)

    # Plot
    fig = scatter_correlation_matrix(df, diagonal=diagonal,
                                     annotate_correlation=annotate_correlation,
                                     colour_correlation=colour_correlation,
                                     ranges=ranges_dict)
    return fig


def handle_file(fpath, diagonal='kde', annotate_correlation=True,
                colour_correlation=True):
    """
    Take an Excel file (`fpath`) and process each worksheet contained within 
    it.
    """
    exc = pd.ExcelFile(fpath)  # excel file
    sheet_names = exc.sheet_names
    for sheet_name in sheet_names:
        # Parse frame for this sheet:
        dframe = exc.parse(sheet_name)

        # Obtain SCM
        fig = scm_for_worksheet(dframe, diagonal=diagonal, 
                                annotate_correlation=annotate_correlation,
                                colour_correlation=colour_correlation)

        # Output graphic
        fout = sheet_name + '.pdf'
        fig.savefig(fout, bbox_inches='tight')

if __name__ == "__main__":
    fin = sys.argv[1]
    handle_file(fin, diagonal='hist', colour_correlation=False,
                annotate_correlation=True)

