from ._search import search_iterable
from ._dataset import current
from ._by import byable
from ._print import _print
from ._commandarg import parse


@byable
def summarize(commandarg="") -> None:
    # _supports_byvar()
    # if current.within_by_context_manager:
    #     raise WithinByContextManager

    parsed = parse(commandarg)
    # print(parsed)
    varlist = parsed["anything"]
    assert not parsed["weight"], "Full commandarg not yet supported"

    df = current.df
    if varlist:
        # labels = search_iterable(df.columns, varlist)
        inverted_labels = [x for x in df.columns if x not in varlist]
        df = df.drop(labels=inverted_labels, axis=1, inplace=False)
    _print(df.describe(include="all").transpose())
