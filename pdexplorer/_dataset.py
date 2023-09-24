import pandas as pd
from copy import copy
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


class Dataset:
    METADATA_DEFAULT = {"data_label": "", "variable_labels": {}}

    def __init__(self) -> None:
        # self.dtale_browser: DtaleData | None = None
        self.dtale_browser = None  # type DtaleData
        self.quietly = False
        self.has_preserved = False
        self.stored_results = {
            "r": {},  # results from general commands
            "e": {},  # results from estimation commands
            "s": {},  # results from parsing commands
            "n": {},  # commands that do not store in r(), e(), or s()
            "c": {},  # contains the values of system parameters and settings
        }
        self._clear_data()
        self._clear_settings()
        self._clear_results()
        # self.within_by_context_manager = False
        self.byvar: str | None = None

    def _clear_data(self, include_preserved=True):
        self._df: pd.DataFrame = pd.DataFrame()
        self.metadata = copy(Dataset.METADATA_DEFAULT)
        if include_preserved:
            self._df_preserved: pd.DataFrame = pd.DataFrame()
            self.metadata_preserved = copy(Dataset.METADATA_DEFAULT)
            self.has_preserved = False

    def _clear_results(self):
        self.methods: dict = {}  # See statsmodel old documentation
        self.properties: dict = {}  # See statsmodel old documentation

    def _clear_settings(self):
        # self.quietly = False
        pass

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
        if self.metadata["variable_labels"]:
            self._df = value
        else:
            # print("setter")
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

    def get_pytorch_dataset(self, varlist: str):
        varlist = " ".join(search_iterable(self._df.columns, varlist))

        from torch.utils.data import DataLoader
        import torch

        class PyTorchDataset(Dataset):
            # PyTorch dataset is a iterable that separates the X variables from the y variable
            def __init__(self, df, varlist):

                # self.nobs = len(df)
                varlist_as_list = varlist.split()
                yvar = varlist_as_list[0]
                xvars = varlist_as_list[1:]
                xvars = search_iterable(df.columns, " ".join(xvars))

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

        return PyTorchDataset(self._df, varlist)

    def get_pytorch_dataloader(self, varlist: str, batch_size=10, shuffle=False):
        from torch.utils.data import DataLoader

        varlist = " ".join(search_iterable(self._df.columns, varlist))
        dataset = self.get_pytorch_dataset(varlist)
        return DataLoader(dataset=dataset, batch_size=batch_size, shuffle=shuffle)  # type: ignore


current = Dataset()  # https://www.stata.com/stata16/multiple-datasets-in-memory/
# current = default  # https://www.stata.com/stata16/multiple-datasets-in-memory/
# df = current._df
# print(current._df)
# print(df)
# def _supports_byvar():
#     if current.within_by_context_manager:
#         raise WithinByContextManager
