from .fixtures import df1 as df
from ..search import _search_by_ranges


def test_basic_example():
    # Note: Multiple range (e.g., "rate-origterm age-upb" do not work
    assert _search_by_ranges(df.columns, "origterm-age") == [
        "origterm",
        "origltv",
        "origfico",
        "age",
    ]


def test_two_arguments():
    assert _search_by_ranges(df.columns, "rate-origterm age-upb") == [
        "rate",
        "origfixedterm",
        "origterm",
        "age",
        "origupb",
        "upb",
    ]
