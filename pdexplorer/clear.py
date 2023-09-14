import pandas as pd
from .dataset import current


def clear(include_preserved=True):
    current.clear()


def clearall():
    current.clearall()
