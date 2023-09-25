import warnings
from .._dataset import current
from .._print import _print


def gpt2(newvarname: str):
    # newvarname = namelist.split()[0]
    # textvar = namelist.split()[1]

    from transformers import pipeline

    generator = pipeline(model="gpt2", device=0)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        current._df["gpt2"] = current._df[newvarname].apply(
            lambda x: generator(x)[0]["generated_text"]
        )
    _print(current.df)
