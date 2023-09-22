# TODO: add in_/if_
from ._dataset import current
from ._print import _print
from ._commandarg import parse_commandarg


def generate(commandarg: str) -> None:
    parsed_commandarg = parse_commandarg(commandarg)
    # print(parsed_commandarg)
    assignment = parsed_commandarg["anything"] + "=" + parsed_commandarg["="]

    new_column_name = assignment.split("=")[0].strip()
    assert (
        new_column_name not in current.df.columns
    ), 'Column already exists.  See "replace" command.'
    # current.df.eval(assignment, inplace=True)

    if parsed_commandarg["if"]:
        current.df.loc[
            current.df.query(parsed_commandarg["if"]).index,
            parsed_commandarg["anything"],
        ] = parsed_commandarg["="]
    else:
        current.df.eval(assignment, inplace=True)

    _print(current.df)
