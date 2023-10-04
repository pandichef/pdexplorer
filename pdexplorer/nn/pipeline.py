from .._dataset import current
from .._print import _print
from .._commandarg import parse


def pipeline(
    # namelist: str,
    # task: str = "text-classification",
    # model_name: str = "distilbert-base-uncased",
    commandarg: str,
    output_dir="output_dir",
    # num_examples=100,
    tokenizer_model_name="distilbert-base-uncased",
    # num_labels=5,
    # run_in_sample=False,
):
    """Run pipeline on every row; deprecated"""
    _ = parse(commandarg, "varlist")
    assert len(_["varlist"].split()) == 1
    # yvar = _["varlist"].split()[0]
    xvar = _["varlist"].split()[0]

    from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

    fine_tuned_text_classification_pipeline = pipeline(
        "text-classification",
        model=AutoModelForSequenceClassification.from_pretrained(output_dir),
        tokenizer=AutoTokenizer.from_pretrained(tokenizer_model_name),
    )

    def _fine_tuned_text_classification_pipeline(x):
        try:
            return int(
                fine_tuned_text_classification_pipeline(x)[0]["label"].replace(
                    "LABEL_", ""
                )
            )
        except RuntimeError:
            return -1

    current._df["_finetuned"] = current._df[xvar].apply(
        _fine_tuned_text_classification_pipeline
    )
    _print(current.df)
    # from transformers import pipeline

    # pipe_fnc = pipeline(task=task, model=model_name)  # fill-mask is default task #

    # assert len(namelist.split()) == 2
    # newvarname = namelist.split()[0]
    # inputvarname = namelist.split()[1]

    # def _pipeline(x):
    #     return pipe_fnc(x[:1000])[0]["label"]  # Error if >1940 or so #

    # current._df[newvarname] = current._df[inputvarname].apply(_pipeline)
    # # current._df["len"] = current._df[inputvarname].apply(len)
    # _print(current.df)
