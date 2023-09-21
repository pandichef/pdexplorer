from math import isclose
from ..webuse import webuse
from ..dataset import current
from ..quietly import quietly
from ..regress import regress
from ..returnlist import _e


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


def test_regress_smf_vs_sklearn():
    # compare smf and sklearn
    with quietly():
        webuse("Duncan__carData", "rdatasets", use_local=True)
    with quietly():
        results = regress("income education")
    with quietly():
        results2 = regress("income education", library="sklearn")
    assert isclose(results.params["Intercept"], results2.intercept_)  # type:ignore
    assert isclose(results.params["education"], results2.coef_[0])  # type:ignore


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


def test_regress_smf_vs_pytorch_Rprop_2_covariates():
    with quietly():
        webuse("Duncan__carData", "rdatasets", use_local=True)
    with quietly():
        results = regress("income education prestige")
    with quietly():
        model = regress("income education prestige", library="pytorch", epochs=100)
    abs_tol = 0.5
    # print(list(model.parameters()))
    assert isclose(
        results.params["Intercept"],  # type:ignore
        float(list(model.parameters())[1]),  # type:ignore
        abs_tol=abs_tol,  # type:ignore
    )
    # print(list(model.parameters())[0][0][0])
    assert isclose(
        results.params["education"],  # type:ignore
        float(list(model.parameters())[0][0][0]),  # type:ignore
        abs_tol=abs_tol,  # type:ignore
    )
    assert isclose(
        results.params["prestige"],  # type:ignore
        float(list(model.parameters())[0][0][1]),  # type:ignore
        abs_tol=abs_tol,  # type:ignore
    )


def test_ereturn_list():
    webuse("auto", use_local=True)
    res = regress("price mpg")
    assert type(res.nobs) == float  # type: ignore
    assert type(_e("N")) == int
    assert int(res.nobs) == _e("N")  # type: ignore
