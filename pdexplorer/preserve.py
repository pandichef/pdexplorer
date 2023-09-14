# from ._singleton import singleton
from .dataset import current


def preserve(quietly=True):
    current.df_preserved = current.df
    current.metadata_preserved = current.metadata
    current.has_preserved = True

    if not quietly:
        print(current.df)
