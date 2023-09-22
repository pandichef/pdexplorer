# from ._singleton import singleton
from ._dataset import current


def _print(obj):
    """Modified print statement using global settings"""
    if not current.quietly:
        print(obj)
