from ._dataset import current
from ._search import search_iterable


def _patsify(varlist: str) -> str:
    # df = current.df
    varlist = varlist.replace(" i.", " ")  # todo: use C() #
    patsy_formula = " + ".join(search_iterable(current.df.columns, varlist))
    patsy_formula = patsy_formula.replace(" + ", " ~ ", 1)
    return patsy_formula
