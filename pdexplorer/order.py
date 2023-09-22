from ._search import search_iterable
from ._dataset import current
from ._print import _print


def order(varlist, refvar=None, after=True, last=False) -> None:
    """
    For whatever reason, it isn't that simple to order columns in pandas.
    This method corrects that.  Note: This currently only supports column
    ordering.

    Parameters
    ----------
    varlist : single label or list-like or magicpandas search string
        The columns to order.
    refvar str, default None
        A reference column e.g., to order after or before refvar
    after : bool, default True
        If True, order after the refvar
    last : bool, default False
        If True, place ordered columns at the end of the dataframe

    Returns
    -------
    MagicDataFrame
        DataFrame with ordered columns.
    """
    df = current.df
    # if type(varlist) == str:
    #     varlist = varlist.split()
    # varlist = df._parse_varlist(varlist)
    varlist = search_iterable(df.columns, varlist)

    assert type(after) == bool
    assert type(last) == bool
    assert (
        last is False or refvar is None
    ), "last and refvar options cannot be use simultaneously"

    therest = [x for x in list(df.columns) if x not in varlist]

    if refvar is None:
        if len(therest) != 0:
            refvar = therest[0]
        after = False

    if last is True:
        after = True
        refvar = therest[-1]

    if len(therest) != 0:
        colnum = list(therest).index(refvar)  # type: ignore
    else:
        colnum = 0

    if after is False:
        head = therest[:colnum]
        tail = therest[colnum:]
    else:
        head = therest[: colnum + 1]
        tail = therest[colnum + 1 :]

    newlist = head
    newlist.extend(varlist)
    newlist.extend(tail)
    df = df[newlist]
    # return df
    current.df = df
    _print(current.df)
