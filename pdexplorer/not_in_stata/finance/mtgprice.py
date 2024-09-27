# UNDER CONSTRUCTION
# BC35 calculator: yield -> price
# https://github.com/pandichef/magicpandas/blob/master/magicpandas/frame.py#L479
# https://github.com/pandichef/pandicake/blob/master/pandicake/pdmonkey/pricegen.py
import pandas as pd
from copy import copy, deepcopy

# import numpy as np
from ..._dataset import current
from ..._print import _print


def _bc35_price(
    beyield,
    coupon,
    cpr,
    age,
    origfixedterm,
    origterm,
    dayofmonth=1,
    delay=47,
    servicing_fee=0,
    root=None,
):  # 47 is market standard according to Goldmach Sachs
    """This implements BC35 in core Python (vs columnwise in a pandas.DataFrame)
    """
    epsilon = servicing_fee / 1200

    r = coupon / 1200
    y = (1 + beyield / 200) ** (1 / 6) - 1
    s = 1 - (1 - cpr / 100) ** (1 / 12)

    m = origfixedterm - age
    n = origterm - age

    qn = 1 - 1 / (1 + r) ** n
    l1 = (r * (1 - s) - epsilon + s * (1 + r)) / qn  # lambda 1
    l2 = (s * (1 + r) - epsilon) * (1 - 1 / qn)  # lambda 2
    l3 = (1 - 1 / qn) * ((1 + r) * (1 - s)) ** m + (1 / qn) * (1 - s) ** m  # lambda 3

    pvl1 = (l1 / (y + s)) * (1 - ((1 - s) / (1 + y)) ** m)  # PV of lamda 1 term
    pvl2 = (l2 / (y - (1 + r) * (1 - s) + 1)) * (
        1 - ((1 + r) * (1 - s) / (1 + y)) ** m
    )  # PV of lamda 2 term
    pvb = l3 / (1 + y) ** m  # PV of the balloon term
    price = 100 * (pvl1 + pvl2 + pvb)

    # Mod Durn
    dvl1 = (l1 / (y + s)) * ((m / (1 + y)) * ((1 - s) / (1 + y)) ** m) - (
        l1 / (y + s) ** 2
    ) * (1 - ((1 - s) / (1 + y)) ** m)
    dvl2 = (l2 / (y - (1 + r) * (1 - s) + 1)) * (
        (m / (1 + y)) * ((1 + r) * (1 - s) / (1 + y)) ** m
    ) - (l2 / (y - (1 + r) * (1 - s) + 1) ** 2) * (
        1 - ((1 + r) * (1 - s) / (1 + y)) ** m
    )
    dvb = -m * l3 / (1 + y) ** (m + 1)
    adjfactor = 12 * (1 + beyield / 200) ** (5 / 6)
    staticdv01 = -(dvl1 + dvl2 + dvb) / adjfactor  # adjustment factor to reflect
    # derivative based on bond equivalent yield (using the chain rule)
    moddurn = staticdv01 / (price / 100)

    # WAL
    l1 = (r * (1 - s) + s * (1 + r)) / qn  # HACK: lambda 1 assuming no servicing fee;
    # price/moddurn fine withou the servicing fee adjustment, but the WAL math breaks
    l2 = (s * (1 + r)) * (1 - 1 / qn)  # HACK: lambda 2 assuming no servicing fee;
    # price/moddurn fine withou the servicing fee adjustment, but the WAL math breaks
    multl1 = l1 - r / qn
    wall1 = (
        (1 - ((1 - s)) ** (m + 1)) / (1 - ((1 - s))) - (m + 1) * ((1 - s)) ** m
    ) / (1 - ((1 - s)))
    multl2 = l2 + (r / qn) / (1 + r) ** n
    wall2 = (
        (1 - ((1 - s) * (1 + r)) ** (m + 1)) / (1 - ((1 - s) * (1 + r)))
        - (m + 1) * ((1 - s) * (1 + r)) ** m
    ) / (1 - ((1 - s) * (1 + r)))

    qnlessm = 1 - 1 / (1 + r) ** (n - m)
    walb = m * qnlessm / qn * (1 - s) ** (m)

    wal = (multl1 * wall1 + multl2 * wall2 + walb) / 12  # wal1+wal2+walb

    # day and delay adjustments
    forwardprice = price * (1 + y) ** ((dayofmonth - 1 + 30 - delay) / 30)
    cleanprice = forwardprice - coupon * (dayofmonth - 1) / 360

    waladjustment = (dayofmonth - 1 + 30 - delay) / 360
    adjwal = wal - waladjustment
    adjmoddurn = moddurn - waladjustment / (1 + beyield / 200)

    if root is None:
        return (cleanprice, adjmoddurn, adjwal)
    else:
        return cleanprice - root


# def bc35_price_gen(self, beyield='beyield', coupon='coupon', cpr='cpr',
def mtgprice(
    # self,
    beyield="beyield",
    coupon="coupon",
    cpr="cpr",
    age="age",
    origfixedterm="origfixedterm",
    origterm="origterm",
    dayofmonth=1,
    delay=47,
    servicing_fee="servicing_fee",
    price="price",
    moodurn="moddurn",
    wal="wal",
    price_only=True,
):
    self = current._df

    cleanprice, adjmoddurn, adjwal = _bc35_price(
        beyield=self[beyield],
        coupon=self[coupon],
        cpr=self[cpr],
        age=self[age],
        origfixedterm=self[origfixedterm],
        origterm=self[origterm],
        dayofmonth=dayofmonth,
        delay=delay,
        servicing_fee=self[servicing_fee],
    )
    # df = self.copy()
    self[price] = pd.Series(cleanprice)
    if not price_only:
        self[moodurn] = pd.Series(adjmoddurn)
        self[wal] = pd.Series(adjwal)
    # return df
    _print(current.df)


'''
def _pdbc35(
    _yield, dayofmonth=1, delay=47, forsolver=True
):  # 47 day delay is mkt standard per JPM & GS
    """
    This implements BC35 for a pandas DataFrame on a loan level basis

    expects to find rate, origfixedterm, age, servicing_fee,
    """
    # epsilon = tmp.servicing_fee/1200

    tmp["r"] = tmp.rate / 1200
    tmp["y"] = (1 + _yield / 200) ** (1 / 6) - 1
    tmp["s"] = 1 - (1 - tmp._cpr / 100) ** (1 / 12)

    tmp["m"] = tmp.origfixedterm - tmp.age
    tmp["n"] = tmp.origterm - tmp.age

    tmp["qn"] = 1 - 1 / (1 + tmp.r) ** tmp.n
    tmp["l1"] = (
        tmp.r * (1 - tmp.s) - tmp.servicing_fee / 1200 + tmp.s * (1 + tmp.r)
    ) / tmp.qn  # lambda 1
    tmp["l2"] = (tmp.s * (1 + tmp.r) - tmp.servicing_fee / 1200) * (
        1 - 1 / tmp.qn
    )  # lambda 2
    tmp["l3"] = (
        (1 - 1 / tmp.qn) * ((1 + tmp.r) * (1 - tmp.s)) ** tmp.m
        + (1 / tmp.qn) * (1 - tmp.s) ** tmp.m
    )  # lambda 3

    tmp["pvl1"] = (tmp.l1 / (tmp.y + tmp.s)) * (
        1 - ((1 - tmp.s) / (1 + tmp.y)) ** tmp.m
    )  # PV of lamda 1 term
    tmp["pvl2"] = (tmp.l2 / (tmp.y - (1 + tmp.r) * (1 - tmp.s) + 1)) * (
        1 - ((1 + tmp.r) * (1 - tmp.s) / (1 + tmp.y)) ** tmp.m
    )  # PV of lamda 2 term
    tmp["pvb"] = tmp.l3 / (1 + tmp.y) ** tmp.m  # PV of the balloon term
    tmp["price"] = 100 * (tmp.pvl1 + tmp.pvl2 + tmp.pvb)

    tmp["forwardprice"] = tmp.price * (1 + tmp.y) ** (
        (dayofmonth - 1 + 30 - delay) / 30
    )
    tmp["cleanprice"] = tmp.forwardprice - tmp.rate * (dayofmonth - 1) / 360

    if forsolver == True:
        return (
            tmp["cleanprice"] - tmp["_price"]
        )  # (round(cleanprice,6), round(adjmoddurn,2), round(adjwal,2))
    else:
        # Mod Durn
        tmp["dvl1"] = (tmp.l1 / (tmp.y + tmp.s)) * (
            (tmp.m / (1 + tmp.y)) * ((1 - tmp.s) / (1 + tmp.y)) ** tmp.m
        ) - (tmp.l1 / (tmp.y + tmp.s) ** 2) * (1 - ((1 - tmp.s) / (1 + tmp.y)) ** tmp.m)
        tmp["dvl2"] = (tmp.l2 / (tmp.y - (1 + tmp.r) * (1 - tmp.s) + 1)) * (
            (tmp.m / (1 + tmp.y)) * ((1 + tmp.r) * (1 - tmp.s) / (1 + tmp.y)) ** tmp.m
        ) - (tmp.l2 / (tmp.y - (1 + tmp.r) * (1 - tmp.s) + 1) ** 2) * (
            1 - ((1 + tmp.r) * (1 - tmp.s) / (1 + tmp.y)) ** tmp.m
        )
        tmp["dvb"] = -tmp.m * tmp.l3 / (1 + tmp.y) ** (tmp.m + 1)
        tmp["adjfactor"] = 12 * (1 + _yield / 200) ** (5 / 6)
        tmp["staticdv01"] = (
            -(tmp.dvl1 + tmp.dvl2 + tmp.dvb) / tmp.adjfactor
        )  # adjustment factor to reflect derivative based on bond equivalent yield (using the chain rule)
        tmp["moddurn"] = tmp.staticdv01 / (tmp.price / 100)

        # WAL
        tmp["l1"] = (
            tmp.r * (1 - tmp.s) + tmp.s * (1 + tmp.r)
        ) / tmp.qn  # HACK: lambda 1 assuming no servicing fee; price/moddurn fine withou the servicing fee adjustment, but the WAL math breaks
        tmp["l2"] = (tmp.s * (1 + tmp.r)) * (
            1 - 1 / tmp.qn
        )  # HACK: lambda 2 assuming no servicing fee; price/moddurn fine withou the servicing fee adjustment, but the WAL math breaks
        tmp["multl1"] = tmp.l1 - tmp.r / tmp.qn
        tmp["wall1"] = (
            (1 - ((1 - tmp.s)) ** (tmp.m + 1)) / (1 - ((1 - tmp.s)))
            - (tmp.m + 1) * ((1 - tmp.s)) ** tmp.m
        ) / (1 - ((1 - tmp.s)))
        tmp["multl2"] = tmp.l2 + (tmp.r / tmp.qn) / (1 + tmp.r) ** tmp.n
        tmp["wall2"] = (
            (1 - ((1 - tmp.s) * (1 + tmp.r)) ** (tmp.m + 1))
            / (1 - ((1 - tmp.s) * (1 + tmp.r)))
            - (tmp.m + 1) * ((1 - tmp.s) * (1 + tmp.r)) ** tmp.m
        ) / (1 - ((1 - tmp.s) * (1 + tmp.r)))

        tmp["qnlessm"] = 1 - 1 / (1 + tmp.r) ** (tmp.n - tmp.m)
        tmp["walb"] = tmp.m * tmp.qnlessm / tmp.qn * (1 - tmp.s) ** (tmp.m)

        tmp["wal"] = (
            tmp.multl1 * tmp.wall1 + tmp.multl2 * tmp.wall2 + tmp.walb
        ) / 12  # wal1+wal2+walb

        tmp["waladjustment"] = (dayofmonth - 1 + 30 - delay) / 360
        tmp["_wal"] = tmp.wal - tmp.waladjustment
        tmp["_moddurn"] = tmp.moddurn - tmp.waladjustment / (1 + _yield / 200)

        tmp["_price"] = tmp["cleanprice"]
        return [tmp._price, tmp._moddurn, tmp._wal]


def pricegen():
    self = current._df

    global tmp  # globalized so it can be run by the pdbc35 program
    tmp = self.copy()
    if "servicing_fee" not in tmp:
        tmp["servicing_fee"] = 0
    computedprice = _pdbc35(_yield=tmp["_yield"], forsolver=False)  # + all['mtmprice']
    pandasprice = pd.DataFrame(computedprice)
    pandasprice = pandasprice.transpose()
    del tmp
    # newdf = deepcopy(self)
    self["_price"] = pandasprice._price
    self["_wal"] = pandasprice._wal
    self["_moddurn"] = pandasprice._moddurn
    # return newdf


def yieldgen(self):
    from scipy import optimize

    self = current._df

    # Note: this is very prone to producing bad results if/when field have missing values
    global tmp  # globalized so it can be run be the pdbc35 program
    tmp = copy(self)
    if "servicing_fee" not in tmp:
        tmp["servicing_fee"] = 0
    sol = optimize.root(
        _pdbc35, self["rate"] - 0.50, method="df-sane", tol=0.00001
    )  # initial guess = yield is 50bp under the note rate
    del tmp
    # newdf = deepcopy(self)
    self["_yield"] = sol.x  # scipyyield._yield
    # self["temp_price"] = self._price
    # self = self.pricegen()  # run pricegen to get wal and moddurn
    # newdf[
    #     "_price"
    # ] = (
    #     newdf.temp_price
    # )  # It a problem when pivoting yield table if prices aren't identical
    # del newdf["temp_price"]
    # return newdf


mtgprice = pricegen


# def _bc35_price(
#     beyield,
#     coupon,
#     cpr,
#     age,
#     origfixedterm,
#     origterm,
#     dayofmonth=1,
#     delay=47,
#     servicing_fee=0,
#     root=None,
# ):  # 47 is market standard according to Goldmach Sachs
#     """This implements BC35 in core Python (vs columnwise in a pandas.DataFrame)
#     """
#     epsilon = servicing_fee / 1200

#     r = coupon / 1200
#     y = (1 + beyield / 200) ** (1 / 6) - 1
#     s = 1 - (1 - cpr / 100) ** (1 / 12)

#     m = origfixedterm - age
#     n = origterm - age

#     qn = 1 - 1 / (1 + r) ** n
#     l1 = (r * (1 - s) - epsilon + s * (1 + r)) / qn  # lambda 1
#     l2 = (s * (1 + r) - epsilon) * (1 - 1 / qn)  # lambda 2
#     l3 = (1 - 1 / qn) * ((1 + r) * (1 - s)) ** m + (1 / qn) * (1 - s) ** m  # lambda 3

#     pvl1 = (l1 / (y + s)) * (1 - ((1 - s) / (1 + y)) ** m)  # PV of lamda 1 term
#     pvl2 = (l2 / (y - (1 + r) * (1 - s) + 1)) * (
#         1 - ((1 + r) * (1 - s) / (1 + y)) ** m
#     )  # PV of lamda 2 term
#     pvb = l3 / (1 + y) ** m  # PV of the balloon term
#     price = 100 * (pvl1 + pvl2 + pvb)

#     # Mod Durn
#     dvl1 = (l1 / (y + s)) * ((m / (1 + y)) * ((1 - s) / (1 + y)) ** m) - (
#         l1 / (y + s) ** 2
#     ) * (1 - ((1 - s) / (1 + y)) ** m)
#     dvl2 = (l2 / (y - (1 + r) * (1 - s) + 1)) * (
#         (m / (1 + y)) * ((1 + r) * (1 - s) / (1 + y)) ** m
#     ) - (l2 / (y - (1 + r) * (1 - s) + 1) ** 2) * (
#         1 - ((1 + r) * (1 - s) / (1 + y)) ** m
#     )
#     dvb = -m * l3 / (1 + y) ** (m + 1)
#     adjfactor = 12 * (1 + beyield / 200) ** (5 / 6)
#     staticdv01 = -(dvl1 + dvl2 + dvb) / adjfactor  # adjustment factor to reflect
#     # derivative based on bond equivalent yield (using the chain rule)
#     moddurn = staticdv01 / (price / 100)

#     # WAL
#     l1 = (r * (1 - s) + s * (1 + r)) / qn  # HACK: lambda 1 assuming no servicing fee;
#     # price/moddurn fine withou the servicing fee adjustment, but the WAL math breaks
#     l2 = (s * (1 + r)) * (1 - 1 / qn)  # HACK: lambda 2 assuming no servicing fee;
#     # price/moddurn fine withou the servicing fee adjustment, but the WAL math breaks
#     multl1 = l1 - r / qn
#     wall1 = (
#         (1 - ((1 - s)) ** (m + 1)) / (1 - ((1 - s))) - (m + 1) * ((1 - s)) ** m
#     ) / (1 - ((1 - s)))
#     multl2 = l2 + (r / qn) / (1 + r) ** n
#     wall2 = (
#         (1 - ((1 - s) * (1 + r)) ** (m + 1)) / (1 - ((1 - s) * (1 + r)))
#         - (m + 1) * ((1 - s) * (1 + r)) ** m
#     ) / (1 - ((1 - s) * (1 + r)))

#     qnlessm = 1 - 1 / (1 + r) ** (n - m)
#     walb = m * qnlessm / qn * (1 - s) ** (m)

#     wal = (multl1 * wall1 + multl2 * wall2 + walb) / 12  # wal1+wal2+walb

#     # day and delay adjustments
#     forwardprice = price * (1 + y) ** ((dayofmonth - 1 + 30 - delay) / 30)
#     cleanprice = forwardprice - coupon * (dayofmonth - 1) / 360

#     waladjustment = (dayofmonth - 1 + 30 - delay) / 360
#     adjwal = wal - waladjustment
#     adjmoddurn = moddurn - waladjustment / (1 + beyield / 200)

#     if root is None:
#         return (cleanprice, adjmoddurn, adjwal)
#     else:
#         return cleanprice - root


# # def bc35_price_gen(
# def mtgprice(
#     beyield="beyield",
#     coupon="coupon",
#     cpr="cpr",
#     age="age",
#     origfixedterm="origfixedterm",
#     origterm="origterm",
#     dayofmonth=1,
#     delay=47,
#     servicing_fee="servicing_fee",
#     price="price",
#     moodurn="moddurn",
#     wal="wal",
# ):
#     self = current._df

#     cleanprice, adjmoddurn, adjwal = _bc35_price(
#         beyield=self[beyield],
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
#     self[price] = pd.Series(cleanprice)
#     self[moodurn] = pd.Series(adjmoddurn)
#     self[wal] = pd.Series(adjwal)
#     # return df
'''
