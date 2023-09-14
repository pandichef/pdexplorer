from .search import search_iterable
from .dataset import current
from ._print import _print
import pandas as pd
from .commandarg import parse_commandarg
from .keepif import keepif
from .keepin import keepin


def _keep(df: pd.DataFrame, columns_to_keep: list) -> pd.DataFrame:
    columns_to_drop = [x for x in df.columns if x not in columns_to_keep]
    return df.drop(labels=columns_to_drop, axis=1, inplace=False)


# def keepold(varlist: str) -> None:
#     columns_to_keep = search_iterable(current.df.columns, varlist)
#     current.df = _keep(current.df, columns_to_keep)
#     _print(current.df)


def keep(commandarg: str) -> None:
    parsed_commandarg = parse_commandarg(commandarg)
    # print(parsed_commandarg["in"])
    # print(parsed_commandarg["in"])
    # print(parsed_commandarg["in"])
    # print(parsed_commandarg)

    if parsed_commandarg["anything"]:
        assert (
            parsed_commandarg["in"] is None and parsed_commandarg["if"] is None
        ), "drop takes either a varlist or in/if, but not both"
        varlist = search_iterable(current.df.columns, parsed_commandarg["anything"])
        current.df = _keep(current.df, varlist)
    elif parsed_commandarg["in"] or parsed_commandarg["if"]:
        assert (
            parsed_commandarg["anything"] is None
        ), "drop takes either a varlist or in/if, but not both"
        if parsed_commandarg["in"]:
            keepin(parsed_commandarg["in"])
        if parsed_commandarg["if"]:
            keepif(parsed_commandarg["if"])
    else:
        raise Exception("drop: Missing Arguments")

    current.df.reset_index(inplace=True, drop=True)
    _print(current.df)
