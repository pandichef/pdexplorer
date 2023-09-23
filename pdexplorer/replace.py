# TODO: add in_/if_
from ._dataset import current
from ._print import _print
from ._commandarg import parse


def replace(commandarg: str) -> None:

    _ = parse(commandarg)

    assignment = _["anything"] + "=" + _["="]

    new_column_name = assignment.split("=")[0].strip()
    assert (
        new_column_name in current.df.columns
    ), 'Column already exists.  See "generate" command.'
    if _["if"]:
        current.df.loc[current.df.query(_["if"]).index, _["anything"],] = _["="]
    else:
        current.df.eval(assignment, inplace=True)
    _print(current.df)
