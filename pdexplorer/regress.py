# raw_syntax = """[anything] [if] [in] [aw fw iw pw] [,		///
raw_syntax = """varlist [if] [in] [aw fw iw pw] [,		///
	VCE(passthru) Robust CLuster(passthru)		///
	HC2 HC3						///
	beta						///
	EForm(passthru)					///
	noHEader					///
	noTABle						///
	plus						///
	dfci DFPValues					///
	*						///
]"""
# https://www.stata.com/manuals13/psyntax.pdf

import pandas as pd
from ._search import search_iterable
from ._dataset import current
from ._get_custom_attributes import _get_custom_attributes
from ._patsify import _patsify
from ._print import _print
from ._commandarg import parse

# from statsmodels.regression.linear_model import RegressionResultsWrapper
from typing import Union


def regress(commandarg: str):
    """
    Stata docs: https://www.stata.com/manuals/rregress.pdf
    Returns: https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html
    """
    # assert False, current.df
    syntax = " ".join(raw_syntax.replace("///", "").split())
    _ = parse(commandarg, syntax)
    varlist = _["varlist"]

    import statsmodels.formula.api as smf
    import statsmodels.api as sm

    # df = current.df
    patsy_formula = _patsify(varlist)
    if _["if"]:
        model = smf.ols(patsy_formula, data=current.df.query(_["if"]), missing="drop")
    else:
        model = smf.ols(patsy_formula, data=current.df, missing="drop")
    results = model.fit()
    _print(results.summary2())
    current.methods, current.properties = _get_custom_attributes(results)  # deprecated

    # results and predict command
    # current.stored_results["e"] = {}
    current.stored_results["e"] = {
        "scalars": {
            "N": int(results.nobs),
            "df_m": int(results.df_model),
            "df_r": int(results.df_resid),
            "F": results.fvalue,
            "r2": results.rsquared,
            "mss": results.mse_model,
            "r2_a": results.rsquared_adj,
            "ll": results.llf,
        }
    }

    def predict_fnc(newvar: str) -> None:
        X = current.df[_["varlist"].split()[1:]]
        predictions_narray = results.predict(sm.add_constant(X))
        current.df[newvar] = pd.Series(predictions_narray)

    current.predict_fnc = predict_fnc

    # def to_dict(self):
    #     attr_dict = {
    #         attr_name: getattr(self, attr_name)
    #         for attr_name in dir(self)
    #         if not callable(getattr(self, attr_name))
    #     }
    #     return attr_dict

    results.__class__.__call__ = lambda self: self.__dict__["_results"].__dict__  # type: ignore
    return results
