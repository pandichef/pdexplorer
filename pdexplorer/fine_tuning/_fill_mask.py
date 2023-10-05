import uuid
import numpy as np
from pdexplorer._print import _print
from pdexplorer._dataset import current
from pdexplorer._commandarg import parse


# from pdexplorer.tests.fixtures import eli5

# import pandas as pd

# df = pd.DataFrame.from_records(eli5)


def fill_mask(
    # df: pd.DataFrame,
    commandarg: str,
    model_name: str = "distilroberta-base",
    test_size=0.3,
    block_size=128,
):
    """
    https://huggingface.co/docs/transformers/tasks/masked_language_modeling
    """
    import torch
    import datasets
    from transformers import (
        AutoModelForMaskedLM,
        AutoTokenizer,
        DataCollatorForLanguageModeling,
        TrainingArguments,
        Trainer,
    )

    _ = parse(commandarg, "varlist")
    assert len(_["varlist"].split()) == 1  # text column only #
    text_var = _["varlist"].split()[0]  # assumed to be "text" #

    df = current.df.rename(columns={text_var: "text"})

    # task = "sentiment-analysis"
    ds = datasets.Dataset.from_pandas(df)
    ds = ds.train_test_split(test_size=test_size)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    ds = ds.flatten()

    def preprocess_function(examples):
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return tokenizer([" ".join(x) for x in examples["text"]])

    tokenized_ds = ds.map(
        preprocess_function,
        batched=True,
        num_proc=4,
        remove_columns=ds["train"].column_names,
    )

    def group_texts(examples):
        # Concatenate all texts.
        concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
        total_length = len(concatenated_examples[list(examples.keys())[0]])
        # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
        # customize this part to your needs.
        if total_length >= block_size:
            total_length = (total_length // block_size) * block_size
        # Split by chunks of block_size.
        result = {
            k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
            for k, t in concatenated_examples.items()
        }
        return result

    lm_dataset = tokenized_ds.map(group_texts, batched=True, num_proc=4)

    # Documentation pads this way: #
    # tokenizer.pad_token = tokenizer.eos_token #
    # This worked in a script, but not within a function call #
    tokenizer.add_special_tokens({"pad_token": "[PAD]"})

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm_probability=0.15,
    )

    model = AutoModelForMaskedLM.from_pretrained(model_name)

    output_dir = f"ft-{model_name}-{str(uuid.uuid4())[:8]}"

    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        num_train_epochs=3,
        weight_decay=0.01,
        # push_to_hub=True,
        no_cuda=not torch.cuda.is_available(),
        report_to="none",  # prevent input() #
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=lm_dataset["train"],
        eval_dataset=lm_dataset["test"],
        data_collator=data_collator,
    )

    trainer.train()
    trainer.save_model()  # saved to output_dir
    _print(f"Saved model to ./{output_dir}")
    torch.cuda.empty_cache()
    current.last_huggingface_ftmodel_dir = output_dir
