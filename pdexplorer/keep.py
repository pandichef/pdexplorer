from ._search import search_iterable
from ._dataset import current
from ._print import _print
import pandas as pd
from ._commandarg import parse

# from .keepif import keepif
# from .keepin import keepin
from ._quietly import quietly
from ._dataset import current
from ._search import search_iterable
import pandas as pd
from ._print import _print
from ._stata_slice import _stata_slice
from ._dataset import current
from ._print import _print


def keepin(range: str) -> None:
    range = _stata_slice(range)

    current.df = eval(f"current.df[{range}]")
    _print(current.df)


def keepif(condition: str) -> None:
    current.df.query(condition, inplace=True)
    _print(current.df)


def _keep(df: pd.DataFrame, columns_to_keep: list) -> pd.DataFrame:
    columns_to_drop = [x for x in df.columns if x not in columns_to_keep]
    return df.drop(labels=columns_to_drop, axis=1, inplace=False)


# def keepold(varlist: str) -> None:
#     columns_to_keep = search_iterable(current.df.columns, varlist)
#     current.df = _keep(current.df, columns_to_keep)
#     _print(current.df)


def keep(commandarg: str) -> None:
    _ = parse(commandarg)

    if _["anything"]:
        assert (
            _["in"] is None and _["if"] is None
        ), "drop takes either a varlist or in/if, but not both"
        varlist = search_iterable(current.df.columns, _["anything"])
        current.df = _keep(current._df, varlist)
    elif _["in"] or _["if"]:
        assert (
            _["anything"] is None
        ), "drop takes either a varlist or in/if, but not both"
        with quietly():
            if _["in"]:
                keepin(_["in"])
            if _["if"]:
                keepif(_["if"])
    else:
        raise Exception("drop: Missing Arguments")

    current._df.reset_index(inplace=True, drop=True)
    _print(current._df)
