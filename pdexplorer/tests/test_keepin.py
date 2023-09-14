from ..dataset import current
from ..keep import keep
from ..webuse import webuse
from ..keepin import keepin
from ..keepif import keepif
from ..quietly import quietly


def test_keepin1():
    with quietly():
        webuse("auto", use_local=True)
        row_count0 = len(current.df)
        keepin(f"{row_count0 - 5}:")
        row_count1 = len(current.df)
        assert row_count1 == 5
