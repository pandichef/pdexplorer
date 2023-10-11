import pandas as pd
from .._dataset import current
from ..use import use
from ..merge import merge
from ..lis import lis
from .._quietly import quietly

# from ..keepif import keepif
from ..reshape import reshapelong, reshapewide
from ..save import save
from ..xpose import xpose
from pandas.testing import assert_frame_equal
from ..sysuse import sysuse
from ..sample import sample


def test_sample_percentage():
    sysuse("nlswork")
    assert len(current.df) == 28534
    counts = current.df["race"].value_counts()
    assert counts["White"] == 20180
    sample(10, random_state=0)
    assert len(current.df) == 2853
    counts = current.df["race"].value_counts()
    assert counts["White"] == 2008


def test_sample_percentage_and_groupby():
    sysuse("nlswork")
    sample(10, by="race", random_state=0)
    assert len(current.df) == 2853
    counts = current.df["race"].value_counts()
    assert counts["White"] == 2018


def test_sample_count():
    sysuse("nlswork")
    sample(100, count=True, random_state=0)
    assert len(current.df) == 100
    counts = current.df["race"].value_counts()
    assert counts["White"] == 60


def test_sample_count_and_groupby():
    sysuse("nlswork")
    sample(100, by="race", count=True, random_state=0)
    assert len(current.df) == 300
    counts = current.df["race"].value_counts()
    assert counts["White"] == 100
