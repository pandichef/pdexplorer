import warnings
from .search import search_iterable
from .dataset import current
import pandas as pd
from ._print import _print


def tabulate(varlist):
    _varlist = varlist.split()
    if len(_varlist) == 1:
        varname = varlist
        df = current.df
        frequency_table = df.groupby(varname).size().reset_index(name="Freq")
        total_count = frequency_table["Freq"].sum()
        frequency_table["Percentage"] = (frequency_table["Freq"] / total_count) * 100
        # frequency_table = frequency_table.set_index(varname)
        frequency_table["Cum"] = frequency_table["Percentage"].cumsum()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pd.set_option("display.max_rows", None)
            _print(frequency_table)
            pd.reset_option("all")
        _print(f"*** Total Freq: {frequency_table['Freq'].sum()} ***")
    elif len(_varlist) == 2:
        twoway = pd.crosstab(current.df[_varlist[0]], current.df[_varlist[1]])  # type: ignore
        # twoway = pd.DataFrame(twoway.to_dict())  # hack to clean indexes
        twoway["Total"] = twoway.sum(axis=1).astype(int)
        _print(twoway)
    else:
        raise Exception("tabulate can only accept a varlist with two variables.")
