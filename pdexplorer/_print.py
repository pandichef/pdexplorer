from io import StringIO
import sys
from ._dataset import current

from rich import print as rich_print


def _print(obj):
    """Modified print statement using global settings"""
    if not current.quietly and not current.browse_turned_on:
        rich_print(obj)
    else:
        # new_captured_output = StringIO()
        # current.captured_output = new_captured_output
        current.captured_output.write(str(obj) + "\n")


# def _print(obj):
#     """Modified print statement using global settings"""
#     if not current.quietly and not current.browse_turned_on:
#         print(obj)
#     else:
#         original_stdout = sys.stdout
#         captured_output = StringIO()
#         sys.stdout = captured_output
#         print(obj)
#         sys.stdout = original_stdout
#         return captured_output.getvalue()
