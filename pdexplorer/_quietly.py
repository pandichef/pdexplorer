import sys
from io import StringIO
import contextlib
from ._dataset import current
from functools import wraps


@contextlib.contextmanager
def quietly(hard=False):
    if hard:
        original_stdout = sys.stdout
        captured_output_hard = StringIO()
        sys.stdout = captured_output_hard
        yield captured_output_hard
        sys.stdout = original_stdout
        current.captured_output = captured_output_hard
    else:
        original_value = current.quietly
        current.quietly = True
        current.captured_output = StringIO()
        # try:
        yield current.captured_output
        # finally:
        current.quietly = original_value


def quietly_decorator(hard=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with quietly(hard=hard) as captured_output:
                return func(*args, **kwargs)

        return wrapper

    return decorator


# @contextlib.contextmanager
# def quietly(hard=False):
#     if hard:
#         original_stdout = sys.stdout
#         captured_output = StringIO()
#         sys.stdout = captured_output
#         yield captured_output
#         sys.stdout = original_stdout
#     else:
#         original_value = current.quietly
#         current.quietly = True
#         current.captured_output = StringIO()
#         try:
#             yield current.captured_output
#         finally:
#             current.quietly = original_value
