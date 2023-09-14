import math
import pandas as pd
from ..dataset import current
from ..use import use
from ..merge import merge
from ..lst import lst
from ..quietly import quietly
from ..keepif import keepif
from ..keep import keep
from ..collapse import collapse
from ..webuse import webuse
from ..preserve import preserve


_use_local = True


def test_collapse1():
    # https://www.stata.com/manuals/dmerge.pdf, page 7
    # webuse("iris", "vega")
    with quietly():
        webuse("iris", "vega", use_local=_use_local)
        keepif('species == "setosa"')
        sepallength__mean = current.df.sepallength.mean()
        sepalwidth__mean = current.df.sepalwidth.mean()
        petallength__sum = current.df.petallength.sum()
        petalwidth__sum = current.df.petalwidth.sum()
        webuse("iris", "vega", use_local=_use_local)
        collapse(
            "(mean) sepallength sepalwidth (sum) petallength petalwidth, by(species)"
        )
        keepif('species == "setosa"')
        assert math.isclose(current.df.sepallength[0], sepallength__mean)
        assert math.isclose(current.df.sepalwidth[0], sepalwidth__mean)
        assert math.isclose(current.df.petallength[0], petallength__sum)
        assert math.isclose(current.df.petalwidth[0], petalwidth__sum)


def test_collapse2():  # weights
    with quietly():
        webuse("iris", "vega", use_local=_use_local)
        keepif('species == "setosa"')
        denominator = current.df.petalwidth.sum()
        sepallength__mean = (
            current.df.sepallength * current.df.petalwidth
        ).sum() / denominator
        sepalwidth__mean = (
            current.df.sepalwidth * current.df.petalwidth
        ).sum() / denominator
        webuse("iris", "vega", use_local=_use_local)
        collapse("(mean) sepallength sepalwidth [w=petalwidth], by(species)")
        keep('if species == "setosa"')
        assert math.isclose(current.df.sepallength[0], sepallength__mean)
        assert math.isclose(current.df.sepalwidth[0], sepalwidth__mean)
