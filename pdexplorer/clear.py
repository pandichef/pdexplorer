import pandas as pd
from ._dataset import current


def clear(include_preserved=True):
    current.clear()


def clearall():
    current.clearall()
