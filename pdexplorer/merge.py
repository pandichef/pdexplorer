import os
import pandas as pd
from .dataset import current
from .use import _use
from .restore import restore
from ._print import _print
from .search import search_iterable


def merge(
    varlist: str,
    right="preserved",  # by default, use the preserved dataset
    how="left",  # The standard vlookup style merge
    suffixes=(None, "__right"),
    indicator=True,
    validate="many_to_one",  # The standard vlookup style merge
    update=False,  # This is a stata option for when there are merge conficts
    *args,
    **kwargs
) -> None:
    """
    From the stata manual:
    Because m:m merges are such a bad idea, we are not going to show you an example. If you think
    that you need an m:m merge, then you probably need to work with your data so that you can use a
    1:m or m:1 merge.

    By default, merge treats values from the master as inviolable. When observations match, it is the
    master’s values of the overlapping variables that are recorded in the merged result.

    If you specify the update option, however, then all missing values of overlapping variables in
    matched observations are replaced with values from the using data. Because of this new behavior,
    the merge codes change somewhat. Codes 1 and 2 keep their old meaning. Code 3 splits into codes
    3, 4, and 5. Codes 3, 4, and 5 are filtered according to the following rules; the first applicable rule
    is used.
    """
    # df = singleton.df
    # df = singleton.df
    labels = search_iterable(current.df.columns, varlist)
    # print(labels)

    def _merge(right: pd.DataFrame):
        return current.df.merge(
            right,
            on=labels,
            indicator=indicator,
            suffixes=suffixes,
            how=how,  # type: ignore
            validate=validate,  # The standard vlookup style merge
            *args,
            **kwargs
        )

    if right == "preserved":
        # right = current.df_preserved
        current.df = _merge(current.df_preserved)
        current.metadata["variable_labels"].update(
            current.metadata_preserved["variable_labels"]
        )
    elif not isinstance(right, str):  # DataFrame or named Series
        # current.df = current.df = _merge(right)
        current.df = _merge(right)
        # current.metadata["variable_labels"].update(
        #     current.metadata_preserved["variable_labels"]
        # )
    else:
        # current.df = current.df = _merge(_use(right)[0])
        right_df, right_metadata = _use(right)
        current.df = _merge(right_df)
        current.metadata["variable_labels"].update(right_metadata["variable_labels"])

    if update:
        pass  # under construction; see stata options

    _print(current.df)
