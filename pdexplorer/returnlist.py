from typing import Literal
from .dataset import current
from pprint import pprint

###############################################
# r-class
def returnlist(return_type: Literal["r", "e", "s", "n", "c"] = "r") -> None:
    # dct = current.stored_results["e"]
    print()
    for values_type, values_dict in current.stored_results[return_type].items():
        print(values_type + ":")
        for k, v in values_dict.items():
            v_as_str = str(k)
            shift = " " * (16 - len(v_as_str))
            print(shift + "_e('" + k + "') =  " + str(v))


def _r(name, return_type: Literal["r", "e", "s", "n", "c"] = "r"):
    flattened_dict = {}
    for key, value in current.stored_results["e"].items():
        flattened_dict.update(value)
    return flattened_dict[name]


###############################################
# e-class
def ereturnlist() -> None:
    returnlist("e")


def _e(name):
    return _r(name, "e")


###############################################
# s-class
def sreturnlist() -> None:
    returnlist("s")


def _s(name):
    return _r(name, "s")


###############################################
# n-class
def nreturnlist() -> None:
    returnlist("n")


def _n(name):
    return _r(name, "n")


###############################################
# c-class
def creturnlist() -> None:
    returnlist("c")


def _c(name):
    return _r(name, "c")
