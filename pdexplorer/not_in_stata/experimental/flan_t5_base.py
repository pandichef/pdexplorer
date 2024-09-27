from ..webuse import webuse
from ..keep import keep
from ..dataset import current
from .._print import _print
from .._quietly import quietly

# example_indices_full = [40, 80, 120]
# example_index_to_summarize = 200


def flan_t5_base():
    # see https://www.coursera.org/learn/generative-ai-with-llms/lecture/wno7h/lab-1-walkthrough
    with quietly():
        from transformers import AutoModelForSeq2SeqLM
        from transformers import AutoTokenizer
        from transformers import GenerationConfig

        model_name = "google/flan-t5-base"

        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

        webuse("knkarthick/dialogsum", "datasets", use_local=True)
        keep('if split =="test"')
        # current.df.reset_index(inplace=True)
        keep("if index==40 or index==200")
        # observation1 = current.df["dialogue"][0]

        # def tokenizer_lambda(sentence):
        #     return tokenizer(sentence, return_tensors="pt")

        current.df["encoded"] = current.df["dialogue"].apply(
            lambda x: tokenizer(x, return_tensors="pt")["input_ids"]  # type: ignore
        )

        current.df["decoded"] = current.df["encoded"].apply(
            lambda x: tokenizer.decode(x[0], skip_special_tokens=True)
        )

        # print(current.df["dialogue"][0].replace("\n", " "))
        # print(current.df["decoded"][0])
        assert current.df["dialogue"][0].replace("\n", " ") == current.df["decoded"][0]

        #  current.df["decoded"] = current.df["encoded"].apply(

        current.df["yhat"] = current.df["encoded"].apply(
            lambda x: tokenizer.decode(
                model.generate(x, max_new_tokens=50)[0], skip_special_tokens=True
            )
        )

        current.df["prompt"] = current.df.apply(
            lambda row: "Dialogue:\n{}\n\nSummary:\n{}".format(
                row["dialogue"], row["summary"]
            ),
            axis=1,
        )

        print(current.df["prompt"][0])

    # print(observation1)
    # print()
    # print(observation2)

    # print(current.df)
