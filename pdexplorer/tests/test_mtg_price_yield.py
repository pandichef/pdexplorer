from math import isclose
import pandas as pd
from ..finance.mtgprice import mtgprice
from ..finance.mtgyield import mtgyield
from ..use import use
from .._quietly import quietly
from .._dataset import current
from ..drop import drop

loan_df = {
    "beyield": {0: 6, 1: 7},
    "coupon": {0: 5, 1: 5},
    "cpr": {0: 15, 1: 15},
    "age": {0: 0, 1: 0},
    "origfixedterm": {0: 360, 1: 360},
    "origterm": {0: 360, 1: 360},
    "servicing_fee": {0: 0, 1: 0},
}


def test_mtg_price_yield():
    with quietly():
        use(pd.DataFrame(loan_df))
        yield_series = current.df.beyield.copy()
        mtgprice()
        drop("beyield")
        assert "beyield" not in current.df.columns
        mtgyield()
        yield_series2 = current.df.beyield.copy()
        assert isclose(yield_series[0], yield_series2[0], abs_tol=0.000001)
        assert isclose(yield_series[1], yield_series2[1], abs_tol=0.000001)
