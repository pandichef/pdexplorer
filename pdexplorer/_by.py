from ._dataset import current
from ._quietly import quietly
from copy import copy
from ._print_horizontal_line import print_horizontal_line
from .use import use
import functools
from .sort import sort

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

    return wrapper


# by context manager
class by:
    def __init__(self, byvar: str) -> None:
        current.byvar = byvar

    def __enter__(self):
        return None  # The part after "as"

    def __exit__(self, exc_type, exc_value, traceback_obj):
        current.byvar = None
