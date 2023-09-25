import pandas as pd
from .._dataset import current
from ..use import use
from ..merge import merge
from ..lis import lis
from .._quietly import quietly
from ..keep import keep
from ..preserve import preserve


def test_merge1():
    # https://www.stata.com/manuals/dmerge.pdf, page 7
    using = pd.DataFrame({"id": [1, 2, 4], "wgt": [130, 180, 110],})
    master = pd.DataFrame({"id": [1, 2, 5], "age": [22, 56, 17],})
    with quietly():
        use(using)
        preserve()
        use(master)
        merge("id", how="outer")
        # res = master.merge(using, how="outer", on="id", indicator=True)
        # print(res)
        assert len(current.df) == 4
        keep('if _merge == "both"')
        assert len(current.df) == 2


def test_merge2():
    # https://www.stata.com/manuals/dmerge.pdf, page 7
    using = pd.DataFrame({"id": [1, 2, 4], "wgt": [130, 180, 110],})
    master = pd.DataFrame({"id": [1, 2, 5], "age": [22, 56, 17],})
    with quietly():
        use(using)
        preserve()
        use(master)
        merge("id")
        assert len(current.df) == 3
