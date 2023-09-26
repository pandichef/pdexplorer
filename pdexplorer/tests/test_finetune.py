import os
import pytest
import sys
from ..webuse import webuse
from ..use import use
from .._dataset import current
from ..nn.finetune import finetune


@pytest.mark.slow
@pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
@pytest.mark.skip
def test_finetune2():
    # import datasets
    # import torch
    # import numpy as np
    # import evaluate
    # from datasets import load_dataset
    # from transformers import (
    #     pipeline,
    #     AutoTokenizer,
    #     AutoModelForSequenceClassification,  # text-classification
    #     AutoModelForMaskedLM,  # fill-mask
    #     TrainingArguments,
    #     Trainer,
    # )

    use(os.path.join(os.path.dirname(__file__), "yelp_mini.dta"))  # fixture
    finetune("label text", num_examples=10)
    assert current.df._finetuned[0] == 4
    assert current.df._finetuned[0] == 4


# @pytest.mark.slow
# @pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
# def test_huggingface():
#     import torch
#     import numpy as np
#     import evaluate
#     from datasets import load_dataset
#     from transformers import (
#         pipeline,
#         AutoTokenizer,
#         AutoModelForSequenceClassification,  # text-classification
#         AutoModelForMaskedLM,  # fill-mask
#         TrainingArguments,
#         Trainer,
#     )

#     # BERT = encoder only = fill-mask #
#     # DistilBERT pretrained on the same data as BERT, which is BookCorpus, #
#     # a dataset consisting of 11,038 unpublished books and #
#     # English Wikipedia (excluding lists, tables and headers). #
#     model_name = "distilbert-base-uncased"  # bert-base-cased is much larger #
#     tokenizer = AutoTokenizer.from_pretrained(model_name)

#     # fill-mask example: shortcut specification #
#     mask_test_sentence = "The goal of life is [MASK]."  # https://huggingface.co/distilbert-base-uncased?text=The+goal+of+life+is+%5BMASK%5D. #
#     fill_mask_pipeline = pipeline(model=model_name)  # fill-mask is default task #
#     fill_mask_result2 = fill_mask_pipeline(mask_test_sentence)
#     assert fill_mask_result2[0]["token_str"] == "happiness"
#     assert fill_mask_result2[1]["token_str"] == "survival"
#     assert fill_mask_result2[2]["token_str"] == "salvation"
#     assert fill_mask_result2[3]["token_str"] == "freedom"
#     assert fill_mask_result2[4]["token_str"] == "unity"

#     # fill-mask example: full specification #
#     fill_mask_pipeline2 = pipeline(
#         "fill-mask",
#         model=AutoModelForMaskedLM.from_pretrained(model_name),
#         tokenizer=tokenizer,
#     )
#     fill_mask_result2 = fill_mask_pipeline2(mask_test_sentence)
#     assert fill_mask_result2[0]["token_str"] == "happiness"
#     assert fill_mask_result2[1]["token_str"] == "survival"
#     assert fill_mask_result2[2]["token_str"] == "salvation"
#     assert fill_mask_result2[3]["token_str"] == "freedom"
#     assert fill_mask_result2[4]["token_str"] == "unity"

#     # text-classification example: shortcut specification #
#     text_classification_pipeline = pipeline("text-classification", model=model_name)
#     fine_tuning_dataset = "yelp_review_full"
#     dataset = load_dataset(fine_tuning_dataset)
#     classification_test_label = dataset["train"][0]["label"]
#     classification_test_sentence = dataset["train"][0]["text"]
#     assert classification_test_label == 4
#     assert classification_test_sentence.startswith(
#         "dr. goldberg offers everything i look for in a general practitioner"
#     )
#     text_classification_results = text_classification_pipeline(
#         classification_test_sentence
#     )
#     assert text_classification_results[0]["label"] in ["LABEL_0", "LABEL_1"]
#     assert isinstance(text_classification_results[0]["score"], float)

#     # text-classification example: full specification #
#     text_classification_pipeline2 = pipeline(
#         "text-classification",
#         model=AutoModelForSequenceClassification.from_pretrained(model_name),
#         tokenizer=tokenizer,
#     )  # num_labels=2 appears to be the default #
#     text_classification_results2 = text_classification_pipeline2(
#         classification_test_sentence
#     )
#     assert text_classification_results2[0]["label"] in ["LABEL_0", "LABEL_1"]
#     assert isinstance(text_classification_results2[0]["score"], float)

#     # Other parameters #
#     output_dir = "test_trainer"
#     number_of_examples = 100  # number of observations used from the fine-tuning dataset

#     # tokenize the fine-tuning dataset #
#     def tokenize_function(examples):
#         return tokenizer(examples["text"], padding="max_length", truncation=True)

#     tokenized_datasets = dataset.map(tokenize_function, batched=True,)

#     # sample from fine-tuning dataset #
#     small_train_dataset = (
#         tokenized_datasets["train"].shuffle(seed=42).select(range(number_of_examples))
#     )
#     small_eval_dataset = (
#         tokenized_datasets["test"].shuffle(seed=42).select(range(number_of_examples))
#     )

#     # load model for specific application #
#     # e.g., distilbert-base-uncased loaded for text classification with 5 stars #
#     model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=5)

#     # train the model
#     def compute_metrics(eval_pred):
#         logits, labels = eval_pred
#         predictions = np.argmax(logits, axis=-1)
#         return evaluate.load("accuracy").compute(
#             predictions=predictions, references=labels
#         )

#     trainer = Trainer(
#         model=model,
#         args=TrainingArguments(
#             output_dir=output_dir,
#             evaluation_strategy="epoch",
#             no_cuda=not torch.cuda.is_available(),
#             report_to="none"
#             # per_device_train_batch_size=8,
#             # per_gpu_eval_batch_size=8,
#         ),
#         train_dataset=small_train_dataset,
#         eval_dataset=small_eval_dataset,
#         compute_metrics=compute_metrics,
#     )
#     trainer.train()
#     trainer.save_model()  # saved to output_dir

#     # check that fine tuned model works for classification_test_sentence #
#     fine_tuned_text_classification_pipeline = pipeline(
#         "text-classification",
#         model=AutoModelForSequenceClassification.from_pretrained("test_trainer"),
#         tokenizer=tokenizer,
#     )
#     fine_tuned_text_classification_results = fine_tuned_text_classification_pipeline(
#         classification_test_sentence
#     )
#     assert fine_tuned_text_classification_results[0]["label"] == "LABEL_" + str(
#         classification_test_label
#     )
#     assert isinstance(fine_tuned_text_classification_results[0]["score"], float)
