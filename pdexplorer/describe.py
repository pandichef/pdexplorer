from ._search import search_iterable
from ._dataset import current
from ._print import _print


def describe(varlist=None):
    df = current.df
    if varlist:
        labels = search_iterable(df.columns, varlist)
        inverted_labels = [x for x in df.columns if x not in labels]
        df = df.drop(labels=inverted_labels, axis=1, inplace=False)
    _print(df.info())
