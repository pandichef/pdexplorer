import pandas as pd
from ..dataset import current
from .._print import _print


def generate_split(*args, **kwargs):
    from sklearn.model_selection import train_test_split

    train, test = train_test_split(current.df, *args, **kwargs)
    train["split"] = "train"  # type: ignore
    test["split"] = "test"  # type: ignore
    current.df = pd.concat([train, test], axis=0).reset_index(drop=True)  # type: ignore
    _print(current.df)
