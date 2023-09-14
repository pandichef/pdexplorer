from pprint import pprint
import statsmodels.api as sm
import numpy as np
import pandas as pd
from pandas import CategoricalDtype
from .search import search_iterable
from .dataset import current
from ._get_custom_attributes import _get_custom_attributes
import statsmodels.formula.api as smf
from ._patsify import _patsify
from ._print import _print


def logit(varlist: str):
    df = current.df
    patsy_formula = _patsify(varlist)
    model = smf.logit(patsy_formula, data=df)
    results = model.fit()
    _print(results.summary())
    current.methods, current.properties = _get_custom_attributes(results)
    return results
