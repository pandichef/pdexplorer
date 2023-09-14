import pandas as pd
from .dataset import current
from ._print import _print


def restore(swap=True):
    if swap:
        current.df, current.df_preserved = current.df_preserved, current.df
        current.metadata, current.metadata_preserved = (
            current.metadata_preserved,
            current.metadata,
        )
    else:
        current.df = current.df_preserved
        current.metadata = current.metadata_preserved
        current.df_preserved = pd.DataFrame()
        current.metadata_preserved = {}
        current.has_preserved = False

    _print(current.df)
