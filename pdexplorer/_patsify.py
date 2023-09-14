from .dataset import current
from .search import search_iterable


def _patsify(varlist: str) -> str:
    df = current.df
    patsy_formula = " + ".join(search_iterable(df.columns, varlist))
    patsy_formula = patsy_formula.replace(" + ", " ~ ", 1)
    return patsy_formula
