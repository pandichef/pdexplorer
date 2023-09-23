from ._search import search_iterable
from ._dataset import current
from ._commandarg import parse
from ._print import _print
from ._dataset import current
from ._search import search_iterable
from ._print import _print
from ._stata_slice import _stata_slice
from ._dataset import current
from ._print import _print


def dropin(range: str) -> None:
    range = _stata_slice(range)
    current.df = eval(f"current.df.drop(current.df.index[{range}])")
    _print(current.df)


def dropif(condition: str) -> None:
    current.df.query("~(" + condition + ")", inplace=True)
    _print(current.df)


def drop(commandarg: str) -> None:
    _ = parse(commandarg)

    if _["anything"]:
        assert (
            _["in"] is None and _["if"] is None
        ), "drop takes either a varlist or in/if, but not both"
        varlist = search_iterable(current._df.columns, _["anything"])
        current._df.drop(labels=varlist, axis=1, inplace=True)
    elif _["in"] or _["if"]:
        assert (
            _["anything"] is None
        ), "drop takes either a varlist or in/if, but not both"
        if _["in"]:
            dropin(_["in"])
        if _["if"]:
            print("YES")
            dropif(_["if"])
    else:
        raise Exception("drop: Missing Arguments")

    current._df.reset_index(inplace=True, drop=True)
    _print(current._df)
