from .dataset import current
from .search import search_iterable
import pandas as pd
import warnings
from ._print import _print
from ._stata_slice import _stata_slice


def keepin(range: str) -> None:
    range = _stata_slice(range)

    current.df = eval(f"current.df[{range}]")
    _print(current.df)
