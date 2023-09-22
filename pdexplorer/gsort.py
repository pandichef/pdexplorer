# from ._search import search_iterable
from ._dataset import current
from ._print import _print


def gsort(varlist) -> None:
    """Implements Stata's gsort command
    Note Stata's different interpretation of the minus sign here
    Hence search_iterable isn't used

    >>> gsort('origfico -origltv')
    """
    df = current.df  # originally written as a function
    if type(varlist) == str:
        varlist = varlist.split()
    ascending_list = []
    new_varlist = []
    for x in varlist:
        if x[:1] == "-":
            new_varlist.append(x[1:])
            ascending_list.append(False)
        elif x[:1] == "+":
            new_varlist.append(x[1:])
            ascending_list.append(True)
        else:
            new_varlist.append(x)
            ascending_list.append(True)
    df.sort_values(new_varlist, ascending=ascending_list, inplace=True)
    _print(current.df)
