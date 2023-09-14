import pandas as pd
from ..dataset import current
from ..use import use
from ..merge import merge
from ..lst import lst
from ..quietly import quietly
from ..keepif import keepif
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
        keepif('_merge == "both"')
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
