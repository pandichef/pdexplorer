from .fixtures import df1 as df
from ..search import _search_by_wildcard


def test_basic_example():
    assert _search_by_wildcard(df.columns, "orig*") == [
        "origfixedterm",
        "origterm",
        "origltv",
        "origfico",
        "origupb",
    ]


def test_two_arguments():
    assert _search_by_wildcard(df.columns, "orig* *upb") == [
        "origfixedterm",
        "origterm",
        "origltv",
        "origfico",
        "origupb",
        "upb",
    ]
