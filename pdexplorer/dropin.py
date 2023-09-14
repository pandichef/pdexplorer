from .dataset import current
from .search import search_iterable
import pandas as pd
from ._print import _print
from ._stata_slice import _stata_slice


def dropin(range: str) -> None:
    range = _stata_slice(range)
    current.df = eval(f"current.df.drop(current.df.index[{range}])")
    _print(current.df)
