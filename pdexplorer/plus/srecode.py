# UNDER CONSTRUCTION
# It currently works, but doesn't support the Stata API
# See https://www.stata.com/products/stb/journals/stb24.pdf
# cf https://pandas.pydata.org/docs/reference/api/pandas.cut.html
# orig implementation: https://github.com/pandichef/magicpandas/blob/master/magicpandas/frame.py#L148
import re
import numpy as np
import pandas as pd
from typing import Optional
from .._dataset import current
from .._print import _print
from pandas.api.types import is_integer_dtype, is_float_dtype

# def pcut(self, step_size: float = None, bin_count: int = None,
#             right: bool = True, format: str = '{:3.2f}') -> MagicSeries:
def srecode(
    newvar,
    varname,
    step_size: Optional[float] = None,
    bin_count: Optional[int] = None,
    right: bool = True,
    format: str = "{:3.2f}",
) -> None:
    """Converts pd.Series of dtype float or int into a ordinal pd.Series of
    dtype category that is formatted in a manner suitable for publishing in
    non-scientific contexts e.g., "1.001 - 2.000" vs (1.001, 2.000].

    TODO: EDIT API SO IT IS CONSISTENT WITH THE STATA COMMAND

    Parameters
    ----------
    step_size : float
        The desired number of steps.  Note: must be None if bin_count is
        not None.
    bin_count : int
        The desired number of bins.  Note: must be None if step_size is
        not None.
    right : bool
        Indicates whether bins includes the rightmost edge or not.
    format : str
        Python style format string e.g., {:3.2f}

    Returns
    -------
    None
    """
    self = current.df[varname]  # self is a Series

    # print(self)

    if not is_float_dtype(self) and not is_integer_dtype(self):
        raise TypeError("Series must of dtype float or int")

    if step_size is not None and bin_count is not None:
        raise ValueError("step_size is not None and bin_count is not None")
    elif step_size is None and bin_count is None:
        raise ValueError("step_size is None and bin_count is None")

    if bin_count is not None:
        step_size = (self.max() - self.min()) / (bin_count - 1)
        step_size = round(step_size, 10)  # type: ignore

    thisformat = (
        format.replace("{:", "{0:") + " - " + format.replace("{:", "{1:")
    )  # e.g., "{0:3.1f} - {1:3.1f}"
    delta = 1 / 10 ** int(
        re.findall(r"\.\d+", format)[0].replace(".", "")
    )  # e.g., 0.01

    minvalue = int(self.min() / step_size) * step_size  # type: ignore
    maxvalue = int(self.max() / step_size + 1) * step_size  # type: ignore

    if right:
        bin_labels = [
            thisformat.format(i + delta, i + step_size)
            for i in np.arange(minvalue, maxvalue, step_size)
        ]
        bin_labels[0] = thisformat.format(minvalue, minvalue + step_size)  # type: ignore
    else:
        bin_labels = [
            thisformat.format(i, i + step_size - delta)
            for i in np.arange(minvalue, maxvalue, step_size)
        ]

    bins = np.arange(minvalue, maxvalue + step_size, step_size)  # type: ignore

    # Below is a hack to handle "ValueError: Bin labels must be one fewer
    # than the number of bin edges."
    if len(bin_labels) == len(bins):
        bin_labels = bin_labels[:-1]

    current._df[newvar] = pd.cut(
        self, bins=bins, right=right, labels=bin_labels, include_lowest=True
    )

    # print(self)
    _print(current.df)
