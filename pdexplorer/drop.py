from .search import search_iterable
from .dataset import current
from .commandarg import parse_commandarg
from .dropif import dropif
from .dropin import dropin
from ._print import _print


def drop(commandarg: str) -> None:
    parsed_commandarg = parse_commandarg(commandarg)

    if parsed_commandarg["anything"]:
        assert (
            parsed_commandarg["in"] is None and parsed_commandarg["if"] is None
        ), "drop takes either a varlist or in/if, but not both"
        varlist = search_iterable(current._df.columns, parsed_commandarg["anything"])
        current._df.drop(labels=varlist, axis=1, inplace=True)
    elif parsed_commandarg["in"] or parsed_commandarg["if"]:
        assert (
            parsed_commandarg["anything"] is None
        ), "drop takes either a varlist or in/if, but not both"
        if parsed_commandarg["in"]:
            dropin(parsed_commandarg["in"])
        if parsed_commandarg["if"]:
            print("YES")
            dropif(parsed_commandarg["if"])
    else:
        raise Exception("drop: Missing Arguments")

    current._df.reset_index(inplace=True, drop=True)
    _print(current._df)
