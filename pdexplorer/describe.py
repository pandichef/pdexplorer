import pandas as pd
from ._search import search_iterable
from ._dataset import current
from ._print import _print


def describe(
    varlist: str | None = None, return_describe_table: bool = False
) -> pd.DataFrame | None:
    df = current.df
    if varlist:
        labels = search_iterable(df.columns, varlist)
        inverted_labels = [x for x in df.columns if x not in labels]
        df = df.drop(labels=inverted_labels, axis=1, inplace=False)
    describe_table = pd.DataFrame()
    describe_table["FIELD"] = pd.Series(list(df.columns))
    describe_table["LABEL"] = describe_table["FIELD"].map(
        lambda varname: current.metadata["variable_labels"].get(varname, varname)
    )
    describe_table["TYPE"] = pd.Series(df.dtypes.astype(str).tolist())
    describe_table.set_index("FIELD", inplace=True)
    describe_table.index.name = None
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        # print(df)  # This will print the entire DataFrame without truncation
        _print(describe_table)
    # _print(df.info(100))
    if return_describe_table:
        return describe_table
