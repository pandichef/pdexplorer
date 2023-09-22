from .fixtures import df1 as df
from .._search import search_iterable


def test_wildcard() -> None:
    assert search_iterable(df.columns, "orig* *upb") == [
        "origfixedterm",
        "origterm",
        "origltv",
        "origfico",
        "origupb",
        "upb",
    ]


def test_range() -> None:
    assert search_iterable(df.columns, "origterm-age") == [
        "origterm",
        "origltv",
        "origfico",
        "age",
    ]


def test_range_two_arguments() -> None:
    assert search_iterable(df.columns, "rate-origterm age-upb") == [
        "rate",
        "origfixedterm",
        "origterm",
        "age",
        "origupb",
        "upb",
    ]


def test_lazily() -> None:
    assert search_iterable(df.columns, "origfix origfic") == [
        "origfixedterm",
        "origfico",
    ]


def test_mixed() -> None:
    assert search_iterable(df.columns, "rate ag origterm-origfico *upb") == [
        "rate",
        "age",
        "origterm",
        "origltv",
        "origfico",
        "origupb",
        "upb",
    ]


def test_subtract() -> None:
    assert search_iterable(
        df.columns, "rate ag origterm-origfico *upb", subtract=True
    ) == ["origfixedterm"]
