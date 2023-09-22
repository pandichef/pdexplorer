import contextlib
from ._dataset import current


@contextlib.contextmanager
def quietly():
    original_value = current.quietly
    current.quietly = True

    try:
        yield
    finally:
        current.quietly = original_value
