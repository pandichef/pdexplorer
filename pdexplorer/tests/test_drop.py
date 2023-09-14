from ..dataset import current
from ..drop import drop
from ..webuse import webuse
from ..quietly import quietly

# from magicpandas.frame import MagicDataFrame
# import warnings

# with warnings.catch_warnings():
#     warnings.simplefilter("ignore")
import statsmodels.api as sm


def test_drop_columns():
    with quietly():
        webuse("auto", use_local=True)
    assert len(current.df.columns) == 12  # type: ignore
    with quietly():
        drop("mak*")  # drop any column that starts with "mak"
    assert len(current.df.columns) == 11  # type: ignore
