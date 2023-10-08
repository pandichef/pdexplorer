from math import isclose
import pandas as pd
import pytest
from ..webuse import webuse
from .._dataset import current
from .._quietly import quietly
from ..regress import regress
from ..returnlist import _e
from ..predict import predict


def test_regress_smf_vs_sm():
    # https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html
    # compare sm and smf
    import statsmodels.api as sm

    with quietly():
        webuse("Duncan__carData", "rdatasets", use_local=True)
    Y = current.df["income"]
    X = current.df["education"]
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    results = model.fit()
    with quietly():
        results2 = regress("income education")

    assert isclose(results.params["const"], results2.params["Intercept"])  # type:ignore
    assert isclose(
        results.params["education"], results2.params["education"]  # type: ignore
    )


def test_ereturn_list():
    webuse("auto", use_local=True)
    res = regress("price mpg")
    assert type(res.nobs) == float  # type: ignore
    assert type(_e("N")) == int
    assert int(res.nobs) == _e("N")  # type: ignore


def test_predict():
    webuse("auto", use_local=True)
    current.df = current.df[:10]  # use first 10 observations #
    regress("price mpg weight")
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


# def test_value_labels():
#     webuse("auto", use_local=False)
#     assert False, current.df


def test_predict_with_if():
    webuse("auto", use_local=True)
    # assert False, current.df
    regress('price mpg weight if foreign=="Foreign"')
    predict("newvar")
    s = current.df["newvar"]
    s2 = pd.Series(  # results from Stata #
        [
            9605.675,
            11870.015,
            8110.481,
            11295.099,
            15673.335,
            13500.108,
            5917.476,
            11449.774,
            14622.389,
            12088.253,
            16982.073,
            14765.061,
            16637.398,
            5239.443,
            13642.779,
            10894.635,
            11100.869,
            8638.069,
            12242.928,
            5271.224,
            13139.199,
            13178.753,
            13880.794,
            3660.909,
            8181.816,
            19651.107,
            19032.406,
            14404.152,
            7801.13,
            15589.995,
            13817.232,
            11953.355,
            15950.904,
            9129.645,
            15451.554,
            11624.227,
            11572.669,
            13603.224,
            11933.578,
            8534.952,
            15395.765,
            11188.439,
            3542.245,
            5782.578,
            7412.67,
            11747.121,
            13654.783,
            12468.939,
            11108.643,
            11057.084,
            12191.37,
            8328.718,
            9188.977,
            5151.873,
            8102.707,
            6698.626,
            4656.753,
            6214.823,
            8697.401,
            5500.778,
            5988.812,
            3454.675,
            4549.406,
            12290.256,
            3855.139,
            4811.428,
            7003.746,
            5663.914,
            8344.265,
            5615.899,
            4641.205,
            4390.501,
            4699.851,
            10941.964,
        ]
    )
    assert (abs(s2 - s) < 0.001).all()


# def test_regress_smf_vs_sklearn():
#     # compare smf and sklearn
#     with quietly():
#         webuse("Duncan__carData", "rdatasets", use_local=True)
#     with quietly():
#         results = regress("income education")
#     with quietly():
#         results2 = regress("income education", library="sklearn")
#     assert isclose(results.params["Intercept"], results2.intercept_)  # type:ignore
#     assert isclose(results.params["education"], results2.coef_[0])  # type:ignore


# def test_regress_smf_vs_pytorch_Rprop():
#     with quietly():
#         webuse("Duncan__carData", "rdatasets", use_local=True)
#     with quietly():
#         results = regress("income education")
#     with quietly():
#         model = regress("income education", library="pytorch", epochs=50)
#     rel_tol = 1  # high tolerance for speed
#     assert isclose(
#         results.params["Intercept"],
#         float(list(model.parameters())[1]),
#         rel_tol=rel_tol,  # type:ignore
#     )
#     assert isclose(
#         results.params["education"],
#         float(list(model.parameters())[0]),
#         rel_tol=rel_tol,  # type:ignore
#     )


# @pytest.mark.slow
# def test_regress_smf_vs_pytorch_Rprop_2_covariates():
#     with quietly():
#         webuse("Duncan__carData", "rdatasets", use_local=True)
#     with quietly():
#         results = regress("income education prestige")
#     with quietly():
#         model = regress("income education prestige", library="pytorch", epochs=100)
#     abs_tol = 0.5
#     # print(list(model.parameters()))
#     assert isclose(
#         results.params["Intercept"],  # type:ignore
#         float(list(model.parameters())[1]),  # type:ignore
#         abs_tol=abs_tol,  # type:ignore
#     )
#     # print(list(model.parameters())[0][0][0])
#     assert isclose(
#         results.params["education"],  # type:ignore
#         float(list(model.parameters())[0][0][0]),  # type:ignore
#         abs_tol=abs_tol,  # type:ignore
#     )
#     assert isclose(
#         results.params["prestige"],  # type:ignore
#         float(list(model.parameters())[0][0][1]),  # type:ignore
#         abs_tol=abs_tol,  # type:ignore
#     )

