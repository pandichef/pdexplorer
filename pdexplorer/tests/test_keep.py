from ..dataset import current
from ..keep import keep
from ..webuse import webuse
from ..quietly import quietly

# from magicpandas.frame import MagicDataFrame
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import statsmodels.api as sm


def test_keep_columns():
    # singleton.df = sm.datasets.get_rdataset("Duncan", "carData").data
    with quietly():
        webuse("auto", use_local=True)
    assert len(current.df.columns) == 12  # type: ignore
    with quietly():
        keep("mak*")  # keep any column that starts with "mak"
    assert len(current.df.columns) == 1  # type: ignore
