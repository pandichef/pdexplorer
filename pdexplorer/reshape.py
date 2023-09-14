# under construction
import numpy as np
from .search import search_iterable
from .dataset import current
from ._print import _print
import pandas as pd

"""
pandas has several reshaping functions, including df.unstack('level') for going to wide, 
df.stack('column_level') for going to long, pd.melt, and df.pivot.

See https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html
See https://www.stata.com/manuals/dreshape.pdf

pandas "record format" = stata "wide format"
pandas "stacked format" = stata "long format"
"""


def reshapewide(stub, i, j):
    current.df[j] = stub + current.df[j].astype(str)
    current.df = current.df.pivot(index=i, columns=j, values=stub)
    current.df = current.df.reset_index()
    current.df.index.name = None
    current.df.columns.name = None
    _print(current.df)


def reshapelong(stub, i, j):
    # varlist = search_iterable(singleton.df.columns, stub + "*")
    # singleton.df.melt(id_vars=varlist, var_name=j, value_name=stub)
    current.df = pd.wide_to_long(current.df, [stub], i=i, j=j)
    current.df.sort_values(by=[i, j], inplace=True)
    current.df.reset_index(inplace=True)
    _print(current.df)
