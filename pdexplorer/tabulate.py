import warnings
from .search import search_iterable
from .dataset import current
import pandas as pd
from ._print import _print


def tabulate(varname):
    df = current.df
    frequency_table = df.groupby(varname).size().reset_index(name="Freq")
    total_count = frequency_table["Freq"].sum()
    frequency_table["Percentage"] = (frequency_table["Freq"] / total_count) * 100
    # frequency_table = frequency_table.set_index(varname)
    frequency_table["Cum"] = frequency_table["Percentage"].cumsum()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        pd.set_option("display.max_rows", None)
        print(frequency_table)
        pd.reset_option("all")
    _print(f"*** Total Freq: {frequency_table['Freq'].sum()} ***")
