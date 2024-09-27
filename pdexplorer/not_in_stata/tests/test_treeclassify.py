from ..ml.treeclassify import treeclassify
from ..._quietly import quietly
from ...webuse import webuse
from ...keep import keep
from ...tabulate import tabulate
from ..._dataset import current


def test_treeclassify_1():
    with quietly():
        webuse("iris", "sklearn", use_local=True)
        # keep("price")
        clf = treeclassify(
            "target sepal* petal*",
            max_depth=2,
            show_graphviz=False,
            use_regressor=False,
        )
        assert clf.predict([[1, 1, 1, 1]])[0] in ["setosa", "versicolor", "virginica"]
