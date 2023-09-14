from .dataset import current
from ._print import _print


def dropif(condition: str) -> None:
    current.df.query("~(" + condition + ")", inplace=True)
    _print(current.df)
