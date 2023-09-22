import pandas as pd
from .._dataset import current
from ..use import use
from ..merge import merge
from ..lst import lst
from .._quietly import quietly

# from ..keepif import keepif
from ..reshape import reshapelong, reshapewide
from ..save import save
from ..xpose import xpose
from pandas.testing import assert_frame_equal

long = pd.DataFrame(
    {"i": [1, 1, 2, 2], "j": [1, 2, 1, 2], "stub": [4.1, 4.5, 3.3, 3.0]}
)
wide = pd.DataFrame({"i": [1, 2], "stub1": [4.1, 3.3], "stub2": [4.5, 3.0]})


def test_reshape1():
    # https://www.stata.com/manuals/dmerge.pdf, page 7
    with quietly():
        use(long)
        reshapewide("stub", "i", "j")
    assert_frame_equal(current.df, wide)


def test_reshape2():
    # https://www.stata.com/manuals/dmerge.pdf, page 7
    with quietly():
        use(wide)
        reshapelong("stub", "i", "j")
    assert_frame_equal(current.df, long)
