# UNDER CONSTRUCTION
# BC35 calculator: price -> yield
# https://github.com/pandichef/magicpandas/blob/master/magicpandas/frame.py#L496
# https://github.com/pandichef/pandicake/blob/master/pandicake/pdmonkey/yieldgen.py
import pandas as pd
from ..._dataset import current
from .mtgprice import _bc35_price
from ..._print import _print


def _bc35_yield(
    price,
    coupon,
    cpr,
    age,
    origfixedterm,
    origterm,
    dayofmonth=1,
    delay=47,
    servicing_fee=0,
):

    from scipy import optimize

    # 47 is the market standard according to Goldman Sachs' loan trader
    result = optimize.root(
        _bc35_price,
        coupon,
        args=(
            coupon,
            cpr,
            age,
            origfixedterm,
            origterm,
            dayofmonth,
            delay,
            servicing_fee,
            price,
        ),
        method="df-sane",
    )

    try:
        # if result.x is a scalar
        # if result.x is np.array or pd.Series, then float returns a TypeError
        return float(result.x)
    except TypeError:
        return result.x


def mtgyield(
    # self,
    price="price",
    coupon="coupon",
    cpr="cpr",
    age="age",
    origfixedterm="origfixedterm",
    origterm="origterm",
    dayofmonth=1,
    delay=47,
    servicing_fee="servicing_fee",
    beyield="beyield",
):
    self = current._df

    beyield_array = _bc35_yield(
        price=self[price],
        coupon=self[coupon],
        cpr=self[cpr],
        age=self[age],
        origfixedterm=self[origfixedterm],
        origterm=self[origterm],
        dayofmonth=dayofmonth,
        delay=delay,
        servicing_fee=self[servicing_fee],  # type: ignore
    )
    # df = self.copy()
    self[beyield] = pd.Series(beyield_array)
    # return df
    _print(current.df)


# from .mtgprice import yieldgen as mtgyield

# mtgyield = None

# from .mtgprice import _bc35_price


# def _bc35_yield(
#     price,
#     coupon,
#     cpr,
#     age,
#     origfixedterm,
#     origterm,
#     dayofmonth=1,
#     delay=47,
#     servicing_fee=0,
# ):
#     from scipy import optimize

#     # 47 is the market standard according to Goldman Sachs' loan trader
#     result = optimize.root(
#         _bc35_price,
#         coupon,
#         args=(
#             coupon,
#             cpr,
#             age,
#             origfixedterm,
#             origterm,
#             dayofmonth,
#             delay,
#             servicing_fee,
#             price,
#         ),
#         method="df-sane",
#     )

#     try:
#         # if result.x is a scalar
#         # if result.x is np.array or pd.Series, then float returns a TypeError
#         return float(result.x)
#     except TypeError:
#         return result.x


# def bc35_yield_gen(
#     self,
#     price="price",
#     coupon="coupon",
#     cpr="cpr",
#     age="age",
#     origfixedterm="origfixedterm",
#     origterm="origterm",
#     dayofmonth=1,
#     delay=47,
#     servicing_fee="servicing_fee",
#     beyield="beyield",
# ):
#     self = current._df

#     beyield_array = _bc35_yield(
#         price=self[price],
#         coupon=self[coupon],
#         cpr=self[cpr],
#         age=self[age],
#         origfixedterm=self[origfixedterm],
#         origterm=self[origterm],
#         dayofmonth=dayofmonth,
#         delay=delay,
#         servicing_fee=self[servicing_fee],
#     )
#     # df = self.copy()
#     self[beyield] = pd.Series(beyield_array)
#     # return df
