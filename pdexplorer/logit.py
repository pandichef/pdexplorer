from .dataset import current
from ._get_custom_attributes import _get_custom_attributes
from ._patsify import _patsify
from ._print import _print


def logit(varlist: str):
    import statsmodels.formula.api as smf

    df = current.df
    patsy_formula = _patsify(varlist)
    model = smf.logit(patsy_formula, data=df)
    results = model.fit()
    _print(results.summary())
    current.methods, current.properties = _get_custom_attributes(results)
    return results
