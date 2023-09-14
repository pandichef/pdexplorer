from .dataset import current
from ._print import _print


def keepif(condition: str) -> None:
    # print(condition)
    current.df.query(condition, inplace=True)
    _print(current.df)
