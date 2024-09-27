from ..._search import search_iterable
from ..._dataset import current
from ..._get_custom_attributes import _get_custom_attributes
from ..._patsify import _patsify
from ..._print import _print
from ..._commandarg import parse

# from statsmodels.regression.linear_model import RegressionResultsWrapper
from typing import Union
import pandas as pd


def regressml(commandarg: str):
    """
    Stata docs: https://www.stata.com/manuals/rregress.pdf

    
    """
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score

    _ = parse(commandarg, "varlist")

    varlist_as_list = _["varlist"].split()
    df_dropna = current.df[varlist_as_list].dropna()

    yvar = varlist_as_list[0]
    xvars = varlist_as_list[1:]
    # xvars = search_iterable(current.df.columns, " ".join(xvars))
    X = df_dropna[xvars].values
    y = df_dropna[yvar].values
    # regr = LinearRegression()
    # regr.fit(X, y)
    results = LinearRegression().fit(X, y)

    # print(regr.coef_)
    # print(reg.coef_)
    LinearRegression.__call__ = lambda self: self.__dict__  # type: ignore
    predicted = results.predict(X)

    # results and predict command
    current.stored_results["e"] = {
        "scalars": {
            # "N": int(results.nobs),
            "df_m": results()["n_features_in_"],  # type: ignore
            # "df_r": int(results.df_resid),
            # "F": results.fvalue,
            "r2": r2_score(y, predicted),
            # "mss": mean_squared_error(predicted, y),
            # "r2_a": results.rsquared_adj,
            # "ll": results.llf,
        }
    }

    def predict_fnc(newvar: str) -> None:
        X = current.df[_["varlist"].split()[1:]]
        predictions_narray = results.predict(X)
        current.df[newvar] = pd.Series(predictions_narray)

    current.predict_fnc = predict_fnc

    return results
