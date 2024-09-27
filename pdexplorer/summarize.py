from ._search import search_iterable
from ._dataset import current
from ._print import _print
from ._commandarg import parse
from copy import copy

# byable = copy(byable)

from ._by import byable

# def byable2(*args, **kwargs):
#     import inspect
#     from ._by import byable

#     exec(inspect.getsource(byable))

#     return byable(*args, **kwargs)


@byable
def summarize(commandarg="") -> None:
    # _supports_byvar()
    # if current.within_by_context_manager:
    #     raise WithinByContextManager

    parsed = parse(commandarg)
    # print(parsed)
    anything = parsed["anything"]
    assert not parsed["weight"], "Full commandarg not yet supported"

    # print(anything)

    varlist = search_iterable(current.df.columns, anything)

    df = current.df.copy()
    if varlist:
        # labels = search_iterable(df.columns, varlist)
        inverted_labels = [x for x in df.columns if x not in varlist]
        df = df.drop(labels=inverted_labels, axis=1, inplace=False)
    _print(df.describe(include="all").transpose())


# summarize = byable(summarize)
