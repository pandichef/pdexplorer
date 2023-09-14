import re
import pandas as pd
from typing import Iterable, Union, List, Any


def _search_lazily(list_to_search: Iterable, search_string: str) -> list:
    """
    Matches columns starting with a string if it's unique in the set of column names.
    For example, 'firstn' would match 'firstname'.  However, if 'firstname' and
    'firstnumber' are two columns, then a NameError is raised.

    :param list_to_search: pandas.DataFrame
    :param search_string: Stata-style list i.e., string with column names separated by a space
    :return: match list

    Example:
    >>> match_list = _search_lazily(list_to_search, 'origfix origfic')
    >>> assert match_list = ['origfixedterm', 'origfico']
    """
    collist = list(
        list_to_search
    )  # valid inputs: pandas.DataFrame, pandas.core.indexes.base.Index, ordinary Python list
    # if type(search_string) == str:
    search_list = search_string.split()

    matchlist = []
    for var in search_list:
        try:
            collist.index(var)  # produces a ValueError if not found
            matchlist.append(var)
        except ValueError:
            matches = [x for x in collist if x.startswith(var)]
            if len(matches) == 1:
                matchlist.append(matches[0])
            elif len(matches) == 0:
                raise NameError("variable " + var + " not found")
            else:
                raise NameError(var + " ambiguous abbreviation")

    return matchlist


def _search_by_range(list_to_search: Iterable, search_string: str) -> list:
    """
    Matches columns based on a range, as specified by the syntax "startvar - endvar"

    :param list_to_search: pandas.DataFrame
    :param search_string: Column range, specified by the syntax "startvar - endvar"
    :return: match list

    Example:
    >>> match_list = _search_by_range(list_to_search, 'origfixedterm-origfico')
    >>> assert match_list = ['origfixedterm', 'origltv', 'origfico']
    """
    collist = list(
        list_to_search
    )  # valid inputs: pandas.DataFrame, pandas.core.indexes.base.Index, ordinary Python list
    # if type(search_string) == str:
    search_list = search_string.split()

    search_string = "".join(search_list)
    search_list = search_string.split("-")

    pos0 = collist.index(search_list[0])
    pos1 = collist.index(search_list[1])
    matchlist = collist[pos0 : pos1 + 1]

    return matchlist


def _search_by_ranges(list_to_search: Iterable, search_string: str) -> list:
    """Handle the case where more than one range is specified"""
    collist = list(
        list_to_search
    )  # valid inputs: pandas.DataFrame, pandas.core.indexes.base.Index, ordinary Python list
    # if type(search_string) == str:
    search_list = search_string.split()

    matchlist = []
    for subsearch_string in search_list:
        thismatchlist = _search_by_range(collist, subsearch_string)
        matchlist.extend(thismatchlist)

    return matchlist


def _search_by_wildcard(list_to_search: Iterable, search_string: str) -> list:
    """
    Matches columns based on * wildcards e.g., "orig*"

    :param list_to_search: pandas.DataFrame
    :param search_string: String containing variables specified by wildcards
    :return: match list
    """
    collist = list(
        list_to_search
    )  # valid inputs: pandas.DataFrame, pandas.core.indexes.base.Index, ordinary Python list

    # if type(search_string) == str:
    search_list = search_string.split()

    relist = []
    for x in search_list:
        x = x.replace("*", ".*")
        relist.append(x)
    restr = "^" + "$|^".join(relist) + "$"
    matchlist = [x for x in collist if re.match(restr, x)]
    return matchlist


def search_iterable(
    list_to_search: Iterable, search_string: str, subtract: bool = False
) -> list:
    """Search any iterable by wildcard, by range, or "lazily"
    """
    collist = list(list_to_search)  # recast iterable as an ordinary list
    # if type(search_string) == str:
    search_list = search_string.split()

    typelist = []
    for x in search_list:
        if x.find("*") > -1:
            typelist.append("w")  # wildcard
        elif x.find("-") > -1:
            typelist.append("r")  # range
        else:
            typelist.append("l")  # lazy

    if len(set(typelist)) == 1 and typelist[0] == "w":
        matchlist = _search_by_wildcard(list_to_search, search_string)
    elif len(set(typelist)) == 1 and typelist[0] == "r":
        matchlist = _search_by_ranges(list_to_search, search_string)
    elif len(set(typelist)) == 1 and typelist[0] == "l":
        matchlist = _search_lazily(list_to_search, search_string)
    else:  # handle mixed search_string (note: this apparently isn't any slower than a 'pure' search_string)
        matchlist = []
        for x in search_list:
            if x.find("*") > -1:
                matchlist.extend(_search_by_wildcard(list_to_search, x))
            elif x.find("-") > -1:
                matchlist.extend(_search_by_ranges(list_to_search, x))
            else:
                matchlist.extend(_search_lazily(list_to_search, x))
    if subtract:
        matchlist = [x for x in collist if x not in matchlist]
    return matchlist
