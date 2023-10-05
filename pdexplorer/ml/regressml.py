from .._search import search_iterable
from .._dataset import current
from .._get_custom_attributes import _get_custom_attributes
from .._patsify import _patsify
from .._print import _print
from .._commandarg import parse

# from statsmodels.regression.linear_model import RegressionResultsWrapper
from typing import Union


def regressml(commandarg: str):
    """
    Stata docs: https://www.stata.com/manuals/rregress.pdf
    Returns: https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html
    """
    from sklearn.linear_model import LinearRegression

    _ = parse(commandarg, "varlist")

    varlist_as_list = _["varlist"].split()
    yvar = varlist_as_list[0]
    xvars = varlist_as_list[1:]
    # xvars = search_iterable(current.df.columns, " ".join(xvars))
    X = current.df.dropna()[xvars].values
    y = current.df.dropna()[yvar].values
    reg = LinearRegression().fit(X, y)
    return reg
