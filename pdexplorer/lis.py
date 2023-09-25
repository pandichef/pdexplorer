from ._dataset import current
from ._search import search_iterable
import pandas as pd
import warnings
from ._print import _print
from ._stata_slice import _stata_slice

# def list(varlist: str, rows=10):
def lis(varlist=None, if_=None, in_=None):
    """The Stata equivalent is list.  However, lis was used here since list is a 
    built-in type in Python.
    """
    # if isinstance(in_, str) and in_.find("/") > -1:  # Stata's slicing syntax
    #     in_ = in_.replace("/", ":")
    #     _in_list = in_.split(":")
    #     in_ = str(int(_in_list[0]) - 1) + ":" + _in_list[1]
    in_ = _stata_slice(in_)

    df = current.df
    if varlist:
        labels = search_iterable(df.columns, varlist)
        inverted_labels = [x for x in df.columns if x not in labels]
        df_to_display = df.drop(labels=inverted_labels, axis=1, inplace=False)
    else:
        df_to_display = df

    # Note "in_" must come first
    if in_:
        df_to_display = eval(f"df_to_display[{in_}]")

    if if_:
        df_to_display = df_to_display.query(if_, inplace=False)

    if in_:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pd.set_option("display.max_rows", None)
            # pd.set_option("display.min_rows", None)
            _print(df_to_display)
            pd.reset_option("all")
    else:
        _print(df_to_display)
