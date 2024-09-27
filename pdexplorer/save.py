import os
from ._dataset import current
import pandas as pd
from .lis import lis
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
            current_df_copy = current.df.copy()
            # fixed error:
            # has a maximum value of infinity which is outside the range supported by Stata.
            import numpy as np

            current_df_copy.replace([np.inf, -np.inf], np.nan, inplace=True)

            # Sept 2024: Not sure why I decide to save dta files this way
            # caused tests to fail
            # for catcol in current_df_copy.select_dtypes(
            #     include=["category"]
            # ).columns.tolist():
            #     current_df_copy[catcol] = current_df_copy[catcol].cat.codes

            current_df_copy.to_stata(
                file_path,
                data_label=current.metadata["data_label"],
                variable_labels=current.metadata["variable_labels"],
                # value_labels=current.metadata["value_labels"],
                write_index=False,
                version=118,
            )
        elif file_extension == ".csv":
            current.df.to_csv(file_path)
        elif file_extension in [".xlsx", ".xls"]:
            current.df.to_excel(file_path)
        elif file_extension in [".pkl"]:
            import pickle

            with open(file_path, "wb") as file:
                # Serialize and save the object to the file
                pickle.dump(current, file)
        elif file_extension in [".parquet"]:
            import json
            from copy import copy
            import pyarrow as pa
            import pyarrow.parquet as pq

            custom_metadata = current.metadata
            table = pa.Table.from_pandas(current.df)

            new_metadata = copy(table.schema.metadata)
            encoded_custom_metadata = json.dumps(custom_metadata).encode("utf-8")
            new_metadata.update({b"custom": encoded_custom_metadata})

            table = table.replace_schema_metadata(new_metadata)

            pq.write_table(table, file_path)

        else:
            print("Didn't save file.  Something went wrong.")
