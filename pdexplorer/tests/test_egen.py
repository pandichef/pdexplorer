from math import isclose
import pandas as pd
from ..dataset import current
from ..use import use
from ..merge import merge
from ..lst import lst
from ..quietly import quietly
from ..keepif import keepif
from ..collapse import collapse
from ..webuse import webuse
from ..preserve import preserve
from ..egen import egen
from ..save import save


def test_egen1():
    with quietly():
        webuse("iris", "vega", use_local=True)
        egen("asdf = sum(  petalwidth)", by="species")
        keepif('species == "setosa"')
        egen_calculation = current.df.asdf[0]
        pandas_calculation = current.df.petalwidth.mean()
        isclose(egen_calculation, pandas_calculation)


def test_egen2():
    with quietly():
        webuse("iris", "vega", use_local=True)
        egen("count = count(petalwidth)", by="species")
        isclose(current.df["count"][0], 50)
        egen("median = median(petalwidth)", by="species")
        isclose(current.df["median"][0], 0.2)
        egen("min = min(petalwidth)", by="species")
        isclose(current.df["min"][0], 0.1)
        egen("max = max(petalwidth)", by="species")
        isclose(current.df["max"][0], 0.6)


def test_egen3():
    with quietly():
        webuse("iris", "vega", use_local=True)
        egen("rank = rank(petalwidth)", by="species")
        isclose(current.df["rank"][0], 20.0)
