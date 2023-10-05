import uuid
import numpy as np

# import pandas as pd

# from pdexplorer.tests.fixtures import yelp_reviews
from pdexplorer._print import _print
from pdexplorer._dataset import current
from pdexplorer._commandarg import parse

# df = pd.DataFrame.from_records(yelp_reviews)


def sentiment_analysis(
    # df: pd.DataFrame,
    commandarg: str,
    # model_name: str = "distilbert-base-uncased",
    model_name: str,
    test_size: float = 0.3,
) -> None:
    """
    https://huggingface.co/docs/transformers/tasks/sequence_classification
    """
    import torch
    import datasets
    import evaluate
    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        DataCollatorWithPadding,
        TrainingArguments,
        Trainer,
    )

    _ = parse(commandarg, "varlist")
    assert len(_["varlist"].split()) == 2  # label and text columns only #
    label_var = _["varlist"].split()[0]  # assumed to be "label" #
    text_var = _["varlist"].split()[1]  # assumed to be "text" #

    df = current.df.rename(columns={label_var: "label", text_var: "text"})

    # task = "sentiment-analysis"
    ds = datasets.Dataset.from_pandas(df)
    ds = ds.train_test_split(test_size=test_size)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def preprocess_function(examples):
        return tokenizer(examples["text"], truncation=True)

    tokenized_ds = ds.map(preprocess_function, batched=True)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    accuracy = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return accuracy.compute(predictions=predictions, references=labels)

    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=df["label"].nunique(),
        torch_dtype=torch.bfloat16 if current.use_torch_bfloat16 else "auto",
    )
    print(f"""Uses {model.get_memory_footprint()/1073741824} GB.""")

    output_dir = f"ft-{model_name}-{str(uuid.uuid4())[:8]}"
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir=output_dir,
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            num_train_epochs=2,
            weight_decay=0.01,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            # push_to_hub=True,
            no_cuda=not torch.cuda.is_available(),
            report_to="none",  # prevent input() #
        ),
        train_dataset=tokenized_ds["train"],
        eval_dataset=tokenized_ds["test"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.save_model()  # saved to output_dir
    _print(f"Saved model to ./{output_dir}")
    torch.cuda.empty_cache()
    current.last_huggingface_ftmodel_dir = output_dir


# print(_sentiment_analysis("stars text"))
