# UNDER CONSTRUCTION
import uuid
import numpy as np
from pdexplorer._print import _print
from pdexplorer._dataset import current
from pdexplorer._commandarg import parse


iso_639_1 = {
    "en": "English",
    "es": "Spanish",
    "zh": "Chinese",
    "hi": "Hindi",
    "ar": "Arabic",
    "bn": "Bengali",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "pa": "Punjabi",
    "de": "German",
    "jv": "Javanese",
    "id": "Indonesian",
    "te": "Telugu",
    "vi": "Vietnamese",
    "ko": "Korean",
    "fr": "French",
    "mr": "Marathi",
    "tr": "Turkish",
    "ta": "Tamil",
    "ur": "Urdu",
    "it": "Italian",
    "th": "Thai",
    "gu": "Gujarati",
    "fa": "Persian",
    "pl": "Polish",
    "uk": "Ukrainian",
    "ro": "Romanian",
    "nl": "Dutch",
    "kk": "Kazakh",
    "ml": "Malayalam",
    "yue": "Cantonese",
    "sv": "Swedish",
    "sr": "Serbian",
    "hu": "Hungarian",
    "ne": "Nepali",
    "ka": "Georgian",
    "tl": "Tagalog",
    "th": "Thai",
    "gu": "Gujarati",
    "fa": "Persian",
    "pl": "Polish",
    "uk": "Ukrainian",
    "ro": "Romanian",
    "nl": "Dutch",
    "kk": "Kazakh",
    "ml": "Malayalam",
    "yue": "Cantonese",
    "sv": "Swedish",
    "sr": "Serbian",
    "hu": "Hungarian",
    "ne": "Nepali",
    "ka": "Georgian",
    "tl": "Tagalog",
    "he": "Hebrew",
    "he-": "Hebrew",
    # "he-BI": "Biblical Hebrew",
    "en-GB": "English (United Kingdom)",
    "es-PR": "Spanish (Puerto Rico)",
}


def translation(
    # df: pd.DataFrame,
    commandarg: str,
    # model_name: str = "distilgpt2",
    model_name: str,
    # source_lang: str = "en",
    # target_lang: str = "fr",
    test_size: float = 0.3,
    # block_size: int = 128,
) -> None:
    """https://www.science.co.il/language/Codes.php"""
    import torch
    from datasets import load_dataset
    from transformers import AutoTokenizer
    from transformers import (
        AutoModelForSeq2SeqLM,
        Seq2SeqTrainingArguments,
        Seq2SeqTrainer,
    )
    from transformers import DataCollatorForSeq2Seq
    import evaluate
    import numpy as np
    import datasets

    _ = parse(commandarg, "varlist")  # must be a varlist
    assert len(_["varlist"].split()) == 2  # label and audio file column only #
    target_lang = _["varlist"].split()[0]  # assumed to be "label" #
    source_lang = _["varlist"].split()[1]  # assumed to be "audio" #
    df = current.df.copy()
    # df = current.df.rename(columns={en_var: "en", fr_var: "fr"})
    columns_to_drop = list(df.columns)
    columns_to_drop.remove(target_lang)
    columns_to_drop.remove(source_lang)
    df = df.drop(columns_to_drop, axis=1)
    df = df.reset_index()
    df = df.rename(columns={"index": "id"})
    df["translation"] = df.apply(
        lambda row: {source_lang: row[source_lang], target_lang: row[target_lang],},
        axis=1,
    )
    ds = datasets.Dataset.from_pandas(df)

    ds = ds.train_test_split(test_size=test_size)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    prefix = f"translate {iso_639_1[source_lang]} to {iso_639_1[target_lang]}: "

    def preprocess_function(examples):
        inputs = [prefix + example[source_lang] for example in examples["translation"]]
        targets = [example[target_lang] for example in examples["translation"]]
        model_inputs = tokenizer(
            inputs, text_target=targets, max_length=128, truncation=True
        )
        return model_inputs

    tokenized_ds = ds.map(preprocess_function, batched=True)

    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model_name)

    metric = evaluate.load("sacrebleu")

    def postprocess_text(preds, labels):
        preds = [pred.strip() for pred in preds]
        labels = [[label.strip()] for label in labels]

        return preds, labels

    def compute_metrics(eval_preds):
        preds, labels = eval_preds
        if isinstance(preds, tuple):
            preds = preds[0]
        decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)

        result = metric.compute(predictions=decoded_preds, references=decoded_labels)
        result = {"bleu": result["score"]}

        prediction_lens = [
            np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds
        ]
        result["gen_len"] = np.mean(prediction_lens)
        result = {k: round(v, 4) for k, v in result.items()}
        return result

    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    output_dir = f"ft-{model_name.replace('/','_')}-{str(uuid.uuid4())[:8]}"
    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        # evaluation_strategy="epoch",
        save_strategy="no",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        weight_decay=0.01,
        save_total_limit=3,
        num_train_epochs=2,
        predict_with_generate=True,
        fp16=True,
        # push_to_hub=False,
        use_cpu=not torch.cuda.is_available(),
        report_to="none",  # prevent input() #
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
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
