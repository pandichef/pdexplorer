from .dataset import current
from ._print import _print


def rename(oldnew: str) -> None:
    def _change_chase(string_method):
        column_mapping = {}
        for col in current.df.columns:
            if isinstance(col, str):  # type error without this
                column_mapping[col] = string_method(col)
            else:
                column_mapping[col] = col
        current.df.rename(columns=column_mapping, inplace=True)

    # todo: handle any set of variable names
    if oldnew.replace(" ", "") == "*,lower":
        _change_chase(str.lower)
    elif oldnew.replace(" ", "") == "*,upper":
        _change_chase(str.upper)
    elif oldnew.replace(" ", "") == "*,proper":
        _change_chase(str.title)
    else:
        df = current.df
        oldnew_split = oldnew.strip().split(" ")
        assert (
            len(oldnew_split) == 2
        ), "Function parameter must be the old variable name followed by the new variable name."
        df.rename(columns={oldnew_split[0]: oldnew_split[1]}, inplace=True)
    _print(current.df)
