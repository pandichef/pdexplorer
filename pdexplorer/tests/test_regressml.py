from math import isclose
import pytest
from ..webuse import webuse
from .._dataset import current
from .._quietly import quietly

from ..regress import regress
from ..ml.regressml import regressml
from ..returnlist import _e


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
