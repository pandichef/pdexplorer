from math import isclose
import pytest
from ..webuse import webuse
from .._dataset import current
from .._quietly import quietly

from ..regress import regress
from ..nn.regressnn import regressnn
from ..returnlist import _e

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


# @pytest.mark.skip
@pytest.mark.slow
def test_regress_smf_vs_pytorch_Rprop_2_covariates():
    with quietly():
        webuse("Duncan__carData", "rdatasets", use_local=True)
    # with quietly():
    results = regress("income education prestige")
    with quietly():
        model = regressnn(
            "income education prestige", use_dataloader=True,
        )  # , library="pytorch", epochs=100)
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
