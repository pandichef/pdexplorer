from .dataset import current
from .search import search_iterable
from ._print import _print


def sort(varlist, ascending=True):
    """See also gsort"""
    sort_list = search_iterable(current.df.columns, varlist)
    current.df.sort_values(sort_list, ascending=ascending, inplace=True)
    _print(current.df)
