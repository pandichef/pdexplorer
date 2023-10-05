# import statsmodels.api as sm

# from ._singleton import singleton

# from ._dataset import current as _current

from ._dataset import current

# import pdexplorer.dataset

# current = pdexplorer.dataset.current

# current = _current

# print(id(_current))
# print(id(current))


import requests
from urllib.parse import urljoin

# import pyreadstat
import tempfile
import os
from pandas.io.stata import StataReader
import pandas as pd
from .preserve import preserve
from .use import use
from .save import save
from ._print import _print
from ._quietly import quietly
from .clear import clear


def _webuse_stata(name, baseurl="https://www.stata-press.com/data/r11/"):
    # For whatever reason, NamedTemporaryFile wasn't working
    # Note that statsmodels itself has an implementation of webuse, but it doesn't grab the metadata
    url_to_datafile = urljoin(baseurl, name + ".dta")
    response = requests.get(url_to_datafile)

    if response.status_code == 200:
        # Save the downloaded data to a local file

        temp_dir = tempfile.gettempdir()
        temp_file_name = os.path.join(temp_dir, "tmpqbxcec2k.dta")

        with open(temp_file_name, "wb") as temp_file:
            temp_file.write(response.content)
        # singleton.df, singleton.metadata = pyreadstat.read_dta(temp_file_name)
        with StataReader(temp_file_name) as reader:
            reader.read
            current.metadata["data_label"] = reader.data_label
            current.metadata["variable_labels"] = reader.variable_labels()
            if name == "auto":
                _dct = reader.value_labels()
                _dct["foreign"] = _dct["origin"]
                del _dct["origin"]
                current.metadata["value_labels"] = _dct
            else:
                current.metadata["value_labels"] = reader.value_labels()
        current.df = pd.read_stata(temp_file_name, convert_categoricals=False)
        os.remove(temp_file_name)
    else:
        raise Exception("Data not found.")


# def webuse(name=None, source="stata"):
def webuse(name, source="stata", preserve_=False, use_local=False, base_path=""):
    if preserve_:
        preserve()

    def _fetch_with_cache(source, _exec):
        if source.startswith("http"):
            source = source.split("/")[-1].split(".")[0]

        if use_local:
            try:
                with quietly():
                    # datasets sometimes uses forward slashes
                    use(f"{str(name).replace('/','_')}__{source}.dta")
            except FileNotFoundError:
                print("File not found locally.  Retrieving from server.")
                exec(_exec)
                save(f"{str(name).replace('/','_')}__{source}.dta")
        else:
            exec(_exec)

    if isinstance(name, int) and source.startswith("http"):
        # why use requests.get first:
        #  https://www.linkedin.com/pulse/solution-http-error-403-forbidden-when-using-ya-yasmine-wen
        _fetch_with_cache(
            source,
            _exec=f"clear(); import requests; current.df = pd.read_html(requests.get('{source}').text)[{name}]",
        )
    elif source == "stata":
        _fetch_with_cache(source, _exec="_webuse_stata(name=name)")
    elif source == "vega":
        _fetch_with_cache(
            source,
            _exec=f"clear(); from vega_datasets import data; current.df = data.{name}()",
        )
    elif source == "seaborn":
        _fetch_with_cache(
            source,
            _exec=f"clear(); import seaborn as sns; current.df = sns.load_dataset('{name}')",
        )
    elif (
        source == "rdatasets"
    ):  # https://www.statsmodels.org/devel/datasets/index.html#using-datasets-from-r
        name_split = str(name).split("__")
        if len(name_split) == 1:
            name_split.append("datasets")  # This is the default in Rdatasets
        _fetch_with_cache(
            source,
            _exec=f"clear(); import statsmodels.api as sm; current.df = sm.datasets.get_rdataset('{name_split[0]}', '{name_split[1]}').data",
        )
    elif (
        source == "statsmodels"
    ):  # https://www.statsmodels.org/devel/datasets/index.html#available-datasets
        _fetch_with_cache(
            source,
            _exec=f"clear(); import statsmodels.api as sm; current.df = sm.datasets.{name}.load_pandas().data",
        )
    elif source == "datasets":  # hugging face
        _fetch_with_cache(
            source,
            _exec=f"""
clear()
from datasets import load_dataset_builder
from datasets import load_dataset

ds_builder = load_dataset_builder('{name}')
current.metadata["data_label"] = ds_builder.info.description
dataset = load_dataset('{name}')  # get all splits
_df_all_splits = pd.DataFrame()
for split_name, split_data in dataset.data.items():
    _df_this_split = split_data.to_pandas()
    _df_this_split["split"] = split_name
    _df_all_splits = pd.concat(
        [_df_all_splits, _df_this_split], ignore_index=False
    )
current.df = _df_all_splits
current.metadata['data_label'] = '{name}'
""",
        )
    elif source == "sklearn":
        _fetch_with_cache(
            source,
            _exec=f"""
clear()
from sklearn.datasets import load_{name}
data = load_{name}()
current.metadata["data_label"] = data.DESCR
_df_x = pd.DataFrame(data.data)
for i, name in enumerate(data.feature_names):
    _df_x.rename(columns={{i: name}}, inplace=True)
# _df_y = pd.DataFrame(data.target, ).rename(columns={{0: "target"}})
_df_x['target'] = pd.Series(pd.Categorical.from_codes(data.target, categories=data.target_names), dtype="category")
# data.target_names
current.df = _df_x
""",
        )

    else:
        raise Exception("Source not found.")

    _print("(" + current.metadata["data_label"] + ")")
    _print(current.df)
    # print("--------")
