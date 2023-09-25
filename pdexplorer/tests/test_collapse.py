import math
import pandas as pd
from .._dataset import current
from ..use import use
from ..merge import merge
from ..lis import lis
from .._quietly import quietly
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
        keep('if species == "setosa"')
        sepallength__mean = current._df.sepallength.mean()
        sepalwidth__mean = current._df.sepalwidth.mean()
        petallength__sum = current._df.petallength.sum()
        petalwidth__sum = current._df.petalwidth.sum()
        webuse("iris", "vega", use_local=_use_local)
        collapse(
            "(mean) sepallength sepalwidth (sum) petallength petalwidth, by(species)"
        )
        keep('if species == "setosa"')
        assert math.isclose(current._df.sepallength[0], sepallength__mean)
        assert math.isclose(current._df.sepalwidth[0], sepalwidth__mean)
        assert math.isclose(current._df.petallength[0], petallength__sum)
        assert math.isclose(current._df.petalwidth[0], petalwidth__sum)


def test_collapse2():  # weights
    with quietly():
        webuse("iris", "vega", use_local=_use_local)
        keep('if species == "setosa"')
        denominator = current._df.petalwidth.sum()
        sepallength__mean = (
            current._df.sepallength * current._df.petalwidth
        ).sum() / denominator
        sepalwidth__mean = (
            current._df.sepalwidth * current._df.petalwidth
        ).sum() / denominator
        webuse("iris", "vega", use_local=_use_local)
        collapse("(mean) sepallength sepalwidth [w=petalwidth], by(species)")
        keep('if species == "setosa"')
        assert math.isclose(current._df.sepallength[0], sepallength__mean)
        assert math.isclose(current._df.sepalwidth[0], sepalwidth__mean)
