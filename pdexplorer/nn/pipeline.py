from .._dataset import current
from .._print import _print


def pipeline(
    namelist: str,
    task: str = "text-classification",
    model_name: str = "distilbert-base-uncased",
):
    from transformers import pipeline

    pipe_fnc = pipeline(task=task, model=model_name)  # fill-mask is default task #

    assert len(namelist.split()) == 2
    newvarname = namelist.split()[0]
    inputvarname = namelist.split()[1]

    def _pipeline(x):
        return pipe_fnc(x[:1000])[0]["label"]  # Error if >1940 or so #

    current._df[newvarname] = current._df[inputvarname].apply(_pipeline)
    # current._df["len"] = current._df[inputvarname].apply(len)
    _print(current.df)
