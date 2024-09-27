from ._dataset import current
from ._quietly import quietly
from copy import copy
from ._print_horizontal_line import print_horizontal_line
from .use import use
import functools
from .sort import sort


# def enhanced_wraps(original_func):
#     def decorator(wrapper_func):
#         # Use functools.wraps to apply standard metadata preservation
#         wrapped = functools.wraps(original_func)(wrapper_func)

#         # Store the original function as a custom attribute
#         wrapped._original = original_func

#         # Preserve additional attributes or information if necessary
#         wrapped.__dict__.update(original_func.__dict__)

#         return wrapped

#     return decorator


# decorator that indicates that a given command supports the by context
def byable(command):
    @functools.wraps(command)
    def wrapper(*args, **kwargs):
        global current
        if current.byvar:
            orig_current = copy(current)
            try:
                with quietly():
                    sort(current.byvar)
                # Loop through byvar
                for this in current.df[current.byvar].unique().tolist():
                    _df = orig_current.df
                    _df = _df[_df[current.byvar] == this]  # filtered
                    with quietly():
                        use(_df)
                    print_horizontal_line()
                    print(f"-> {current.byvar} = {this}")
                    command(*args, **kwargs)  # by context cannot support return values
                current = orig_current
            except:
                current = orig_current
        else:
            return command(*args, **kwargs)

    # wrapper.__wrapped__ = command
    return wrapper


# by context manager
class by:
    def __init__(self, byvar: str) -> None:
        current.byvar = byvar

    def __enter__(self):
        return None  # The part after "as"

    def __exit__(self, exc_type, exc_value, traceback_obj):
        current.byvar = None


###########################################

# import os
# import sys
# import importlib
# from typing import Callable
# from functools import wraps


# def fix_autoreload(decorator):
#     """
#     Fix autoreload for decorators so decorated functions properly autoreload
#     """
#     if "autoreload" not in sys.modules:
#         return decorator

#     def autoreload_fixed_decorator(func):

#         module = sys.modules[func.__module__]
#         mdate = os.path.getmtime(module.__file__)
#         decorated = decorator(func)

#         @wraps(func)
#         def autoreload_func(*args, **kwargs):
#             nonlocal mdate, decorated

#             _mdate = os.path.getmtime(module.__file__)
#             if _mdate != mdate:
#                 mdate = _mdate
#                 decorated = importlib.reload(module).__dict__[func.__name__].__wrapped__

#             return decorated(*args, **kwargs)

#         return autoreload_func

#     return autoreload_fixed_decorator


# byable = fix_autoreload(byable)
