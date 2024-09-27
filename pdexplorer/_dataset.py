import io
import pandas as pd
from copy import copy
from typing import Optional, Callable
from ._search import search_iterable


# import dtale
# from dtale.views import DtaleData

# df = pd.DataFrame()
# class WithinByContextManager(Exception):
#     pass


# varlist_as_list = varlist.split()
# yvar = varlist_as_list[0]
# xvars = varlist_as_list[1:]
# xvars = search_iterable(current.df.columns, " ".join(xvars))
# x_train = current.df.dropna()[xvars].values
# y_train = current.df.dropna()[[yvar]].values
# X = torch.tensor(x_train).to(torch.float32)
# y = torch.tensor(y_train).to(torch.float32)

from xlwings import Book


class Dataset:
    METADATA_DEFAULT = {"data_label": "", "variable_labels": {}}

    def __init__(self) -> None:
        # self.dtale_browser: DtaleData | None = None
        self._clear_data()
        self._clear_settings()
        self._clear_results()
        self.xlwings_workbook: None | Book = None
        # context manager variables #
        self.byvar: str | None = None
        self.quietly = False

    def _clear_data(self, include_preserved=True):
        self._df: pd.DataFrame = pd.DataFrame()
        self.metadata = copy(Dataset.METADATA_DEFAULT)
        if include_preserved:
            self._df_preserved: pd.DataFrame = pd.DataFrame()
            self.metadata_preserved = copy(Dataset.METADATA_DEFAULT)
            self.has_preserved = False

    def _clear_results(self):
        self.stored_results = {
            "r": {},  # results from general commands
            "e": {},  # results from estimation commands
            "s": {},  # results from parsing commands
            "n": {},  # commands that do not store in r(), e(), or s()
            "c": {},  # contains the values of system parameters and settings
        }
        self.predict_fnc: Optional[Callable[[str], None]] = None
        self.methods: dict = {}  # See statsmodel old documentation
        self.properties: dict = {}  # See statsmodel old documentation

    def _clear_settings(self):
        # self.quietly = False
        self.dtale_browser = None  # type DtaleData
        self.has_preserved = False
        self.active_python_script: Optional[str] = None  # see doedit
        self.last_openai_ftjob_id: Optional[str] = None
        self.last_huggingface_ftmodel_dir: Optional[str] = None
        self.browse_turned_on = False
        self.use_torch_bfloat16 = True
        # self.last_huggingface_tokenizer = None
        self.captured_output = io.StringIO()

    # @property
    def clear(self):
        self._clear_data(include_preserved=False)

    # @property
    def clearall(self):
        self._clear_data()
        self._clear_settings()
        self._clear_results()

    @property
    def df(self):
        # returns a copy of df
        # use current._df to return a reference
        # print(
        #     "Making a copy of current dataframe.  Use current._df to get a reference to the current dataframe."
        # )
        # return self._df.copy()
        return self._df

    @property
    def df_labeled(self):
        return self._df.rename(columns=self.metadata["variable_labels"])

    @df.setter
    def df(self, value: pd.DataFrame):
        # if self.metadata["variable_labels"]:
        #     self._df = value
        # else:
        column_mapping = {}
        for col in value.columns:
            if isinstance(col, str):  # type error without this
                column_mapping[col] = (
                    col.replace(" ", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace(",", "")
                    .lower()
                )  # Stata default is to remove spaces
            else:
                column_mapping[col] = col
        self._df = value.rename(columns=column_mapping)
        self.metadata["variable_labels"] = {
            value: key for key, value in column_mapping.items()
        }

    @property
    def df_preserved(self):
        return self._df_preserved

    @df_preserved.setter
    def df_preserved(self, value):
        self._df_preserved = value
        self.has_preserved = True

    def split(self, name: str) -> pd.DataFrame:
        _return_df = self._df.query(f"split == '{name}'", inplace=False)
        if _return_df.empty:
            print(f'Split "{name}" not found.  Split values:')
            print(self._df.split.value_counts())
        return _return_df

    def get_huggingface_dataset(
        self, varlist: Optional[str] = None, split: Optional[str] = None
    ):
        import datasets

        if not varlist:
            varlist = "*"
        varlist = " ".join(search_iterable(self._df.columns, varlist))
        if split:
            dataset = datasets.Dataset.from_pandas(
                self._df[varlist.split()].query(f"""split=='{split}'""")
            )
        else:
            dataset = datasets.Dataset.from_pandas(self._df[varlist.split()])
        return dataset

    def get_pytorch_dataset(
        self, varlist: Optional[str] = None, split: Optional[str] = None, tokenizer=None
    ):

        # from transformers import AutoTokenizer

        if not varlist:
            varlist = "*"
        varlist = " ".join(search_iterable(self._df.columns, varlist))
        xvars = varlist.split()
        yvar = xvars.pop(0)
        df_split = self._df.copy()

        if split:
            df_split = df_split.query(f"""split=='{split}'""")

        # ds = self.get_huggingface_dataset(varlist, split)
        # model expects the argument to be named labels #
        # ds = ds.rename_column(yvar, "labels")
        # ds.set_format("torch")
        # model_name = "distilbert-base-uncased"  # bert-base-cased is much larger #
        # tokenizer = AutoTokenizer.from_pretrained(model_name)

        # def tokenize_function(examples):
        #     return tokenizer(examples[xvar], padding="max_length", truncation=True)

        # tokenized_datasets = dataset.map(tokenize_function, batched=True,)

        # dataset.set_format(type="torch")
        # https://huggingface.co/docs/datasets/use_with_pytorch#dataset-format #
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # ds = dataset.with_format("torch", device=device)
        # return ds

        # from torch.utils.data import DataLoader
        import torch
        from torch.utils.data import Dataset as PyTorchDataset

        class _PyTorchDataset(PyTorchDataset):
            # PyTorch dataset is a iterable that separates the X variables from the y variable
            def __init__(self, df):

                # self.nobs = len(df)
                # varlist_as_list = varlist.split()
                # yvar = varlist_as_list[0]
                # xvars = varlist_as_list[1:]
                # xvars = search_iterable(df.columns, " ".join(xvars))

                x_train = df.dropna()[xvars].values
                y_train = df.dropna()[[yvar]].values
                # below fails if not float32
                self.x_train = torch.tensor(x_train).to(torch.float32)
                self.y_train = torch.tensor(y_train).to(torch.float32)

                # x_df = df[xvars]
                # y_series = df[yvar]

                # self.x_train = torch.tensor(x_df.values)
                # self.y_train = torch.tensor(y_series)

            def __len__(self):
                return len(self.y_train)

            def __getitem__(self, idx):
                # idx = torch.long(idx)
                # idx = torch.arange(self.nobs, dtype=torch.long)
                # print(type(idx))
                return self.x_train[idx], self.y_train[idx]

        return _PyTorchDataset(df_split)

    def get_pytorch_dataloader(
        self,
        varlist: Optional[str] = None,
        split: Optional[str] = None,
        batch_size=100,
        shuffle=False,
    ):
        from torch.utils.data import DataLoader

        # varlist = " ".join(search_iterable(self._df.columns, varlist))
        ds = self.get_pytorch_dataset(varlist, split)
        dl = DataLoader(dataset=ds, batch_size=batch_size, shuffle=shuffle)  # type: ignore
        return dl


current = Dataset()

# def clearall_global():
#     global current
#     current = Dataset()


# current = Dataset()  # https://www.stata.com/stata16/multiple-datasets-in-memory/
# current = default  # https://www.stata.com/stata16/multiple-datasets-in-memory/
# df = current._df
# print(current._df)
# print(df)
# def _supports_byvar():
#     if current.within_by_context_manager:
#         raise WithinByContextManager
