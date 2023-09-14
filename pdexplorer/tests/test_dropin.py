from ..dataset import current
from ..keep import keep
from ..webuse import webuse
from ..dropin import dropin
from ..keepif import keepif
from ..quietly import quietly


def test_dropin1():
    with quietly():
        webuse("auto", use_local=True)
        row_count0 = len(current.df)
        dropin(f"{row_count0 - 5}:")
        row_count1 = len(current.df)
        assert row_count0 - row_count1 == 5


def test_dropin2():
    with quietly():
        webuse("auto", use_local=True)
        keepif("price > 5000")
        row_count0 = len(current.df)
        dropin(f"{row_count0 - 5}:")
        row_count1 = len(current.df)
        assert row_count0 - row_count1 == 5
    # print(row_count0)
