from .._dataset import current
from .._print import _print
from .._quietly import quietly
from .._commandarg import parse


def fthuggingface(
    commandarg: str,
    # output_dir="output_dir",
    num_examples=100,
    model_name="distilbert-base-uncased",  # BERT is an encoder only model
    num_labels=5,
):
    print(current.df)
    import uuid

    output_dir = f"ft-{model_name}-{str(uuid.uuid4())[:8]}"

    _ = parse(commandarg, "varlist")
    assert len(_["varlist"].split()) == 2
    yvar = _["varlist"].split()[0]  # assumed to be "label"
    xvar = _["varlist"].split()[1]
    # https://huggingface.co/docs/transformers/training#train-with-pytorch-trainer
    import datasets
    import torch
    import numpy as np
    import evaluate
    from datasets import load_dataset
    from transformers import (
        pipeline,
        AutoTokenizer,
        AutoModelForSequenceClassification,  # text-classification
        AutoModelForMaskedLM,  # fill-mask
        TrainingArguments,
        Trainer,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    dataset = datasets.DatasetDict()
    dataset["train"] = current.get_huggingface_dataset(split="train")
    dataset["test"] = current.get_huggingface_dataset(split="test")

    # tokenize the fine-tuning dataset #
    def tokenize_function(examples):
        return tokenizer(examples[xvar], padding="max_length", truncation=True)

    tokenized_datasets = dataset.map(tokenize_function, batched=True,)

    # sample from fine-tuning dataset #
    small_train_dataset = (
        tokenized_datasets["train"]
        .shuffle(seed=42)
        .select(range(min(num_examples, len(current.df.query('split=="train"')))))
    )
    small_eval_dataset = (
        tokenized_datasets["test"]
        .shuffle(seed=42)
        .select(range(min(num_examples, len(current.df.query('split=="test"')))))
    )

    # load model for specific application #
    # e.g., distilbert-base-uncased loaded for text classification with 5 stars #
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=num_labels
    )

    # train the model
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return evaluate.load("accuracy").compute(
            predictions=predictions, references=labels
        )

    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir=output_dir,
            evaluation_strategy="epoch",
            no_cuda=not torch.cuda.is_available(),
            # no_cuda=True,
            report_to="none"
            # per_device_train_batch_size=8,
            # per_gpu_eval_batch_size=8,
        ),
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    trainer.save_model()  # saved to output_dir
    _print(f"Saved model to ./{output_dir}")

    torch.cuda.empty_cache()

    current.last_huggingface_ftmodel_dir = output_dir
    # current.last_huggingface_tokenizer = AutoTokenizer.from_pretrained(  # type: ignore
    #     "distilbert-base-uncased"
    # )


def askhuggingface(prompt, auto_model=None):
    from transformers import (
        pipeline,
        AutoTokenizer,
        AutoModelForSequenceClassification,  # text-classification
        AutoModelForMaskedLM,  # fill-mask
        TrainingArguments,
        Trainer,
    )

    if auto_model is None:
        auto_model = AutoModelForSequenceClassification

    task_map = {AutoModelForSequenceClassification: "text-classification"}
    # AutoModelForQuestionAnswering	question-answering
    # AutoModelForTokenClassification	token-classification
    # AutoModelForMultipleChoice	multiple-choice
    # AutoModelForMaskedLM	fill-mask
    # AutoModelForSeq2SeqLM	translation

    # output_dir = current.last_huggingface_ftmodel_dir
    base_model_name = "-".join(current.last_huggingface_ftmodel_dir.split("-")[1:-1])  # type: ignore

    tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    model = auto_model.from_pretrained(current.last_huggingface_ftmodel_dir)

    fine_tuned_text_classification_pipeline = pipeline(
        task_map[auto_model], model=model, tokenizer=tokenizer,
    )

    print(fine_tuned_text_classification_pipeline(prompt)[0])  # type: ignore


##################################################
def fthuggingface_old(
    commandarg: str,
    output_dir="output_dir",
    num_examples=100,
    model_name="distilbert-base-uncased",
    num_labels=5,
    run_in_sample=False,
):
    # Deprecated #
    _ = parse(commandarg, "varlist")
    assert len(_["varlist"].split()) == 2
    yvar = _["varlist"].split()[0]
    xvar = _["varlist"].split()[1]
    # https://huggingface.co/docs/transformers/training#train-with-pytorch-trainer
    import datasets
    import torch
    import numpy as np
    import evaluate
    from datasets import load_dataset
    from transformers import (
        pipeline,
        AutoTokenizer,
        AutoModelForSequenceClassification,  # text-classification
        AutoModelForMaskedLM,  # fill-mask
        TrainingArguments,
        Trainer,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    dataset = datasets.DatasetDict()
    dataset["train"] = current.get_huggingface_dataset(split="train")
    dataset["test"] = current.get_huggingface_dataset(split="test")

    # tokenize the fine-tuning dataset #
    def tokenize_function(examples):
        return tokenizer(examples[xvar], padding="max_length", truncation=True)

    tokenized_datasets = dataset.map(tokenize_function, batched=True,)

    # sample from fine-tuning dataset #
    small_train_dataset = (
        tokenized_datasets["train"].shuffle(seed=42).select(range(num_examples))
    )
    small_eval_dataset = (
        tokenized_datasets["test"].shuffle(seed=42).select(range(num_examples))
    )

    # load model for specific application #
    # e.g., distilbert-base-uncased loaded for text classification with 5 stars #
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=num_labels
    )

    if run_in_sample:
        text_classification_pipeline = pipeline(
            "text-classification", model=model, tokenizer=tokenizer
        )

        def _text_classification_pipeline(x):
            try:
                return int(
                    text_classification_pipeline(x)[0][yvar].replace("LABEL_", "")
                )
            except RuntimeError:
                return -1

        current._df["_pretrained"] = current._df[xvar].apply(
            _text_classification_pipeline
        )

    # train the model
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return evaluate.load("accuracy").compute(
            predictions=predictions, references=labels
        )

    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir=output_dir,
            evaluation_strategy="epoch",
            no_cuda=not torch.cuda.is_available(),
            # no_cuda=True,
            report_to="none"
            # per_device_train_batch_size=8,
            # per_gpu_eval_batch_size=8,
        ),
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    trainer.save_model()  # saved to output_dir
    _print(f"Saved model to ./{output_dir}")

    if run_in_sample:
        fine_tuned_text_classification_pipeline = pipeline(
            "text-classification",
            model=AutoModelForSequenceClassification.from_pretrained(output_dir),
            tokenizer=tokenizer,
        )

        def _fine_tuned_text_classification_pipeline(x):
            try:
                return int(
                    fine_tuned_text_classification_pipeline(x)[0][yvar].replace(
                        "LABEL_", ""
                    )
                )
            except RuntimeError:
                return -1

        current._df["_finetuned"] = current._df[xvar].apply(
            _fine_tuned_text_classification_pipeline
        )
        _print(current.df)
    torch.cuda.empty_cache()
