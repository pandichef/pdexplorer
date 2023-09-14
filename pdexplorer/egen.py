# under construction: additional egen functions must be added over time
import numpy as np
from .dataset import current
from ._print import _print


def egen(assignment, by=None):
    """
    Generates a new function variable given input of the form:
    egen("newvar = fnc(arguments)")

    see https://www.stata.com/manuals/degen.pdf
    """
    assignment_list = assignment.split()
    assert assignment_list[1] == "=", 'egen assignment must contain "=".'
    newvar = assignment_list[0]
    fnc_and_args = "".join(assignment_list[2:])
    fnc_and_args_list = fnc_and_args.split("(")
    egen_fnc = fnc_and_args_list[0]
    assert len(fnc_and_args_list) == 2, "Invalid expression."
    arguments = fnc_and_args_list[1][:-1]

    if not by:
        current.df["by"] = "_all"
        by = "by"

    if egen_fnc == "rank":
        current.df[newvar] = current.df.groupby(by)[arguments].rank(method="average")
    else:
        # mean, count, median, min, max
        current.df[newvar] = current.df.groupby(by)[arguments].transform(egen_fnc)

    if by == "by":
        del current.df["by"]

    _print(current.df)
