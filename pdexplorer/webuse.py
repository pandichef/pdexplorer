import os
import functools
import tempfile
from urllib.parse import urljoin
import requests
import pandas as pd
from pandas.io.stata import StataReader
from ._dataset import current
from .preserve import preserve
from .use import use
from .save import save
from ._print import _print
from ._quietly import quietly
from .clear import clear  # , clearall


def cache_file_fetch(webuse_func):
    @functools.wraps(webuse_func)
    def decorator(use_local=False):
        # print('use_local: ', use_local)

        def wrapper(name, *args, **kwargs):
            if use_local:

                def get_local(name, *args, **kwargs):
                    source = webuse_func.__name__.split("_")[-1]
                    try:
                        use(
                            f"{str(name).replace('/','_')}__{source}.dta",
                            suppress_print=True,
                        )
                    except FileNotFoundError:
                        print("File not found locally.  Retrieving from server.")
                        webuse_func(name, *args, **kwargs)
                        file_path = f"{str(name).replace('/','_')}__{source}.dta"
                        save(file_path)
                        # print(current.df.foreign)
                        # use(file_path)
                        print(f"Saving to {file_path}.")

                get_local(name, *args, **kwargs)
            else:
                webuse_func(name, *args, **kwargs)

        return wrapper

    return decorator


def make_metadata_value_labels(df):
    metadata_value_labels = {}
    for catcol in df.select_dtypes(include=["category"]).columns:
        this_label = dict(zip(df[catcol].cat.codes, df[catcol].astype(str)))
        metadata_value_labels.update({catcol: this_label})
    return metadata_value_labels


@cache_file_fetch
def _webuse_stata(
    name="auto", baseurl="https://www.stata-press.com/data/r18/",
):
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
            current.metadata["data_label"] = reader.data_label
            current.metadata["variable_labels"] = reader.variable_labels()
            current.df = reader.read(convert_categoricals=True)
        # reader.value_labels() doesn't work correctly because Stata #
        # uses a value_label name whereas pandas does not #

        current.metadata["value_labels"] = make_metadata_value_labels(current.df)

        # current.df = pd.read_stata(temp_file_name, convert_categoricals=True)
        os.remove(temp_file_name)
    else:
        raise Exception("Data not found.")


@cache_file_fetch
def _webuse_vega(name="cars"):
    clear()
    from vega_datasets import data

    current.df = eval(f"data.{name}()")
    current.metadata["value_labels"] = make_metadata_value_labels(current.df)


@cache_file_fetch
def _webuse_seaborn(name="tips"):
    clear()
    import seaborn as sns

    current.df = eval(f"sns.load_dataset('{name}')")
    current.metadata["value_labels"] = make_metadata_value_labels(current.df)


@cache_file_fetch
def _webuse_rdataset(name="AirPassengers"):
    clear()
    import statsmodels.api as sm

    name_split = str(name).split("__")
    if len(name_split) == 1:
        name_split.append("datasets")  # This is the default in Rdatasets
    current.df = eval(
        f"sm.datasets.get_rdataset('{name_split[0]}', '{name_split[1]}').data"
    )
    current.metadata["value_labels"] = make_metadata_value_labels(current.df)


@cache_file_fetch
def _webuse_statsmodels(name="longley"):
    clear()
    import statsmodels.api as sm

    current.df = eval(f"sm.datasets.{name}.load_pandas().data")
    current.metadata["value_labels"] = make_metadata_value_labels(current.df)


@cache_file_fetch
def _webuse_huggingface(name="imdb"):
    clear()
    from datasets import load_dataset_builder
    from datasets import load_dataset

    ds_builder = load_dataset_builder(name)
    current.metadata["data_label"] = ds_builder.info.description
    dataset = load_dataset(name)
    _df_all_splits = pd.DataFrame()
    for split_name, split_data in dataset.data.items():
        _df_this_split = split_data.to_pandas()
        _df_this_split["split"] = split_name
        _df_all_splits = pd.concat([_df_all_splits, _df_this_split], ignore_index=False)
    current.df = _df_all_splits
    current.metadata["data_label"] = name
    current.metadata["value_labels"] = make_metadata_value_labels(current.df)


@cache_file_fetch
def _webuse_sklearn(name="iris"):
    clear()
    exec(f"from sklearn.datasets import load_{name}")
    data = eval(f"load_{name}()")
    current.metadata["data_label"] = data.DESCR
    _df_x = pd.DataFrame(data.data)
    for i, name in enumerate(data.feature_names):
        _df_x.rename(columns={i: name}, inplace=True)
    _df_x["target"] = pd.Series(
        pd.Categorical.from_codes(data.target, categories=data.target_names),
        dtype="category",
    )
    current.df = _df_x
    current.metadata["value_labels"] = make_metadata_value_labels(current.df)


def webuse(name, source="stata", preserve_=False, use_local=False, base_path=""):
    if preserve_:
        preserve()

    if source == "stata":
        _webuse_stata(use_local)(name=name)
    elif source == "vega":
        _webuse_vega(use_local)(name=name)
    elif source == "seaborn":
        _webuse_seaborn(use_local)(name=name)
    elif source in [
        "rdataset",
        "rdatasets",
    ]:  # https://www.statsmodels.org/devel/datasets/index.html#using-datasets-from-r
        _webuse_rdataset(use_local)(name=name)
    elif (
        source == "statsmodels"
    ):  # https://www.statsmodels.org/devel/datasets/index.html#available-datasets
        _webuse_statsmodels(use_local)(name=name)
    elif source in ["datasets", "huggingface"]:  # hugging face
        _webuse_huggingface(use_local)(name=name)
    elif source == "sklearn":
        _webuse_sklearn(use_local)(name=name)
    else:
        raise Exception("Source not found.")

    _print("(" + current.metadata["data_label"] + ")")
    _print(current.df)
