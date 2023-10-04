# from ._singleton import singleton
from ._dataset import current

# from .browse import turned_on


def _print(obj):
    """Modified print statement using global settings"""
    if not current.quietly and not current.browse_turned_on:
        print(obj)
