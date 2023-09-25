import os
from ._dataset import current
import pandas as pd
from .lst import lst
from ._print import _print


def save(file_path=None, use_variable_labels=False):
    if use_variable_labels:
        column_labels = current.metadata["variable_labels"]
    else:
        column_labels = {}

    # df = singleton.df
    if not file_path:
        current.df.rename(columns=column_labels).to_clipboard()
        _print("(Data saved to clipboard)")
    elif os.path.splitext(file_path)[1] == "":
        current.get_huggingface_dataset().save_to_disk(file_path)
    else:
        assert (
            not use_variable_labels
        ), "dta files save variable labels as metadata.  Set use_variable_labels to False."
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == ".dta":
            # print("current.df")
            # print(current.df)
            current.df.to_stata(
                file_path,
                data_label=current.metadata["data_label"],
                variable_labels=current.metadata["variable_labels"],
                # value_labels=current.metadata["value_labels"],
                write_index=False,
                version=118,
            )
        elif file_extension == ".csv":
            current.df.rename(columns=column_labels).to_csv(file_path)
        elif file_extension in [".xlsx", ".xls"]:
            current.df.rename(columns=column_labels).to_excel(file_path)
