from ._search import search_iterable
from ._dataset import current
from ._by import byable
from ._print import _print


@byable
def summarize(varlist=None) -> None:
    # _supports_byvar()
    # if current.within_by_context_manager:
    #     raise WithinByContextManager

    df = current.df
    if varlist:
        labels = search_iterable(df.columns, varlist)
        inverted_labels = [x for x in df.columns if x not in labels]
        df = df.drop(labels=inverted_labels, axis=1, inplace=False)
    _print(df.describe(include="all").transpose())
