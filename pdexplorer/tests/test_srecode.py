from ..plus.srecode import srecode
from .._quietly import quietly
from ..webuse import webuse
from ..keep import keep
from ..tabulate import tabulate
from .._dataset import current


def test_srecode():
    with quietly():
        webuse("auto")
        keep("price")
        srecode("pcat", "price", 4000)
        # tabulate('pcat')
        counts = current.df.pcat.value_counts()
        assert counts["0.00 - 4000.00"] == 11
        assert counts["4000.01 - 8000.00"] == 49
        assert counts["8000.01 - 12000.00"] == 9
        assert counts["12000.01 - 16000.00"] == 5
