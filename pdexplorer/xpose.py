from ._dataset import current
from ._print import _print


def xpose() -> None:
    current.df = current.df.transpose()
    _print(current.df)
