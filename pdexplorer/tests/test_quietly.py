import sys
from io import StringIO
from math import isclose
import pytest
from ..webuse import webuse
from .._dataset import current
from .._quietly import quietly, quietly_decorator
from ..regress import regress


def rprint():
    print("rprinted")


@pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
def test_quietly_hard():
    with quietly(hard=True) as captured_output:
        webuse("auto", use_local=True)
        rprint()
    s = captured_output.getvalue()
    assert s.lower().startswith("(1978 automobile data)") and s.endswith("rprinted\n")
    s2 = current.captured_output.getvalue()
    assert s2.lower().startswith("(1978 automobile data)") and s2.endswith("rprinted\n")


@pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
def test_quietly_soft():
    with quietly(hard=False) as captured_output:
        webuse("auto", use_local=True)
        rprint()
    s = captured_output.getvalue()
    assert s.lower().startswith("(1978 automobile data)") and not s.endswith(
        "rprinted\n"
    )
    s2 = current.captured_output.getvalue()
    assert s2.lower().startswith("(1978 automobile data)") and not s2.endswith(
        "rprinted\n"
    )


@quietly_decorator(hard=True)
def fnc_to_wrap_hard():
    webuse("auto", use_local=True)
    rprint()


@quietly_decorator(hard=False)
def fnc_to_wrap_soft():
    webuse("auto", use_local=True)
    rprint()


@pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
def test_quietly_decorator_hard():
    fnc_to_wrap_hard()
    s2 = current.captured_output.getvalue()
    # print(s2)
    # assert False
    # assert s2.lower().startswith("(1978 automobile data)")
    assert s2.lower().startswith("(1978 automobile data)")
    assert s2.endswith("rprinted\n")


@pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
def test_quietly_decorator_soft():
    fnc_to_wrap_soft()
    s2 = current.captured_output.getvalue()
    assert s2.lower().startswith("(1978 automobile data)") and not s2.endswith(
        "rprinted\n"
    )
