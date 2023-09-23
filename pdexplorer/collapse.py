import numpy as np
from ._dataset import current
from ._print import _print
from ._commandarg import parse, parse_options


def collapse(commandarg: str) -> None:
    _ = parse(commandarg)

    weight = _["weight"]
    weight = weight.split("=")[1] if weight else None

    by = _["by"] if _["by"] else None

    # if _["options"]:
    #     parsed_options = parse_options(_["options"])
    #     if parsed_options["by"]:
    #         by = parsed_options["by"]
    #     else:
    #         by = None
    # else:
    #     by = None

    clist = _["anything"]

    clist_as_list = clist.split()
    # print(clist_as_list)
    # assert len(clist_as_list) == len(
    #     set(clist_as_list)
    # ), "Duplicate names found.  Create appropriately named columns first before collapsing."

    # df = current.df
    if not weight:
        current._df["weight"] = 1
        weight = "weight"
    if not by:
        current._df["by"] = "_all"
        by = "by"

    fnc = {
        # "mean": lambda x: (x * df[weight]).sum() / (df[weight]).sum(), # Denominator didn't work here
        "mean": lambda x: (x * current._df.loc[x.index, weight]).sum()  #  From ChatGPT
        / (current._df.loc[x.index, weight]).sum(),  # type:ignore
        "median": lambda x: x.median(),
        "sum": lambda x: (x * current._df[weight]).sum(),
        "rawsum": lambda x: x.sum(),
        "count": lambda x: x.count(),
        "max": lambda x: x.max(),
        "min": lambda x: x.min(),
    }

    # parse clist
    agg_functions = {}
    stat = ""
    for item in clist_as_list:
        if item[0] == "(" and item[-1] == ")":
            stat = item[1:-1]
        else:
            agg_functions[item] = fnc[stat]
        # print(stat)

    if not weight:
        del current._df["weight"]

    current.df = current._df.groupby(by).agg(agg_functions).reset_index()

    _print(current._df)
