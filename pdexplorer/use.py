from typing import Tuple, Dict

# import statsmodels.api as sm
from .dataset import current

# import requests
from urllib.parse import urljoin

# import pyreadstat
# import tempfile
import os
from pandas.io.stata import StataReader
import pandas as pd
from .preserve import preserve
from ._print import _print


# def _use(file_path=None, html_index=0) -> Tuple[pd.DataFrame, Dict]:
def _use(file_path=None) -> Tuple[pd.DataFrame, Dict]:
    """Version of use that returns a """
    if not isinstance(file_path, pd.DataFrame) and not file_path:
        return pd.read_clipboard(), current.METADATA_DEFAULT
    elif not isinstance(file_path, str):  # i.e., it's a DataFrame
        return file_path.copy(), current.METADATA_DEFAULT
    # elif file_path.startswith("http"):
    #     return pd.read_html(file_path)[html_index], current.METADATA_DEFAULT
    else:
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == ".dta":
            _df_to_return = pd.read_stata(file_path, convert_categoricals=False)
            _metadata_to_return = {}
            with StataReader(file_path) as reader:
                _metadata_to_return["data_label"] = reader.data_label
                _metadata_to_return["variable_labels"] = reader.variable_labels()
                _metadata_to_return["value_labels"] = reader.value_labels()
            return _df_to_return, _metadata_to_return
        elif file_extension == ".csv":
            return pd.read_csv(file_path), current.METADATA_DEFAULT
        elif file_extension in [".xlsx", ".xls"]:
            return pd.read_csv(file_path), current.METADATA_DEFAULT
        else:
            raise TypeError("Invalid file path.")
            # return pd.DataFrame(), {}


# def use(file_path=None, preserve_=True, html_index=0) -> None:
def use(file_path=None, preserve_=False) -> None:
    if preserve_:
        preserve()

    # current.df, current.metadata = _use(file_path=file_path, html_index=html_index)
    current.df, current.metadata = _use(file_path=file_path)

    _print(current.df)
