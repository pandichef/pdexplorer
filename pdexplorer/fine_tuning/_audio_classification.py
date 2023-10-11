# https://colab.research.google.com/drive/1FjTsqbYKphl9kL-eILgUc-bl4zVThL8F?usp=sharing
# https://huggingface.co/blog/fine-tune-wav2vec2-english
import uuid
import numpy as np
from pdexplorer._print import _print
from pdexplorer._dataset import current
from pdexplorer._commandarg import parse


def audio_classification(
    # df: pd.DataFrame,
    commandarg: str,
    # model_name: str = "distilbert-base-uncased",
    model_name: str,
    test_size: float = 0.3,
    sampling_rate=96000,
) -> None:
    """https://huggingface.co/docs/transformers/tasks/audio_classification"""
    import torch
    import datasets
    import evaluate
    from transformers import (
        AutoFeatureExtractor,
        AutoModelForSequenceClassification,
        AutoTokenizer,
        AutoModelForAudioClassification,
        DataCollatorWithPadding,
        TrainingArguments,
        Trainer,
    )

    _ = parse(commandarg, "varlist")
    assert len(_["varlist"].split()) == 2  # label and text columns only #
    label_var = _["varlist"].split()[0]  # assumed to be "label" #
    audio_var = _["varlist"].split()[1]  # assumed to be "audio" #

    df = current.df.rename(columns={label_var: "label", audio_var: "audio"})
    columns_to_drop = list(df.columns)
    columns_to_drop.remove("label")
    columns_to_drop.remove("audio")
    df = df.drop(columns_to_drop, axis=1)
    ds = datasets.Dataset.from_pandas(df)
    ds = ds.train_test_split(test_size=test_size)

    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
    ds = ds.cast_column("audio", datasets.Audio(sampling_rate=sampling_rate))

    def preprocess_function(examples):
        audio_arrays = [x["array"] for x in examples["audio"]]
        inputs = feature_extractor(
            audio_arrays,
            sampling_rate=feature_extractor.sampling_rate,
            max_length=sampling_rate,
            truncation=True,
        )
        return inputs

    encoded_ds = ds.map(preprocess_function, remove_columns="audio", batched=True)
    accuracy = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        predictions = np.argmax(eval_pred.predictions, axis=1)
        return accuracy.compute(predictions=predictions, references=eval_pred.label_ids)

    model = AutoModelForAudioClassification.from_pretrained(
        model_name, num_labels=df["label"].nunique()
    )

    output_dir = f"ft-{model_name.replace('/','_')}-{str(uuid.uuid4())[:8]}"
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=3e-5,
        per_device_train_batch_size=32,
        gradient_accumulation_steps=4,
        per_device_eval_batch_size=32,
        num_train_epochs=10,
        warmup_ratio=0.1,
        logging_steps=10,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        # push_to_hub=True,
        use_cpu=not torch.cuda.is_available(),
        report_to="none",  # prevent input() #
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=encoded_ds["train"],
        eval_dataset=encoded_ds["test"],
        tokenizer=feature_extractor,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.save_model()  # saved to output_dir
    _print(f"Saved model to ./{output_dir}")
    torch.cuda.empty_cache()
    current.last_huggingface_ftmodel_dir = output_dir


# print(_sentiment_analysis("stars text"))
