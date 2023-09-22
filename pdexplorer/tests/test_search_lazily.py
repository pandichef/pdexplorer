from .fixtures import df1 as df
from .._search import _search_lazily


def test_basic_example():
    # unique matches work
    assert _search_lazily(df.columns, "origfix origfic") == [
        "origfixedterm",
        "origfico",
    ]


def test_exact_match():
    assert _search_lazily(df.columns, "origfixedterm origfico") == [
        "origfixedterm",
        "origfico",
    ]


def test_nameerror_ambiguous():
    # with pytest.raises(NameError, message='asdf') as excinfo:
    try:
        _search_lazily(df.columns, "orig")
    except Exception as e:
        assert type(e) == NameError
        assert str(e) == "orig ambiguous abbreviation"


def test_nameerror_var_not_found():
    # with pytest.raises(NameError, message='asdf') as excinfo:
    try:
        _search_lazily(df.columns, "hello")
    except Exception as e:
        assert type(e) == NameError
        assert str(e) == "variable hello not found"
