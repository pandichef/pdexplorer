from math import isclose
import pytest
from ..webuse import webuse
from .._dataset import current
from .._quietly import quietly

from ..regress import regress
from ..ml.regressml import regressml
from ..predict import predict
import pandas as pd


def test_regress_smf_vs_sklearn():
    # compare smf and sklearn
    with quietly():
        webuse("Duncan__carData", "rdatasets", use_local=True)
    with quietly():
        results = regress("income education")
    with quietly():
        results2 = regressml("income education")  # , library="sklearn")
    assert isclose(results.params["Intercept"], results2.intercept_)  # type:ignore
    assert isclose(results.params["education"], results2.coef_[0])  # type:ignore


def test_regress_smf_vs_sklearn_2():
    # compare smf and sklearn
    with quietly():
        webuse("auto", use_local=True)
    with quietly():
        results = regress("price mpg weight")
    with quietly():
        results2 = regressml("price mpg weight")  # , library="sklearn")
    assert isclose(results.params["Intercept"], results2.intercept_)  # type:ignore
    assert isclose(results.params["mpg"], results2.coef_[0])  # type:ignore
    assert isclose(results.params["weight"], results2.coef_[1])  # type:ignore


def test_predict():
    webuse("auto", use_local=True)
    current.df = current.df[:10]  # use first 10 observations #
    regressml("price mpg weight")
    predict("newvar")
    s = current.df["newvar"]
    s2 = pd.Series(  # results from Stata #
        [
            4717.105,
            5382.828,
            3682.33,
            5525.76,
            7654.441,
            6691.233,
            2885.706,
            5632.806,
            7107.386,
            5894.405,
        ]
    )
    assert (abs(s2 - s) < 0.001).all()
