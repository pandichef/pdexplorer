import io
import json
from .._dataset import current


def _convert_tabular_format_to_openai_format(df) -> list:
    # Convert DataFrame to dictionary with 'records' orientation
    df_dict = df.to_dict(orient="records")

    # Use map to transform each record into the desired format
    records = list(
        map(
            lambda record: {
                "messages": [
                    {"role": role, "content": content}
                    for role, content in record.items()
                ]
            },
            df_dict,
        )
    )

    return records


def _write_records_to_stringio(records: list) -> io.StringIO:
    output = io.StringIO()
    for record in records:
        output.write(json.dumps(record))
        output.write("\n")
    output.seek(0)
    return output


class FineTuningJobHelper:
    def __init__(self, openai_ftjob_id: str) -> None:
        self.openai_ftjob_id = openai_ftjob_id

    def retrieve(self):
        import openai

        return openai.FineTuningJob.retrieve(self.openai_ftjob_id)

    def cancel(self):
        import openai

        return openai.FineTuningJob.cancel(self.openai_ftjob_id)

    def list_events(self, limit=10):
        import openai

        return openai.FineTuningJob.list_events(  # type: ignore
            id=self.openai_ftjob_id, limit=limit
        )

    def delete_model(self):
        import openai

        model_name = self.retrieve().to_dict()["fine_tuned_model"]
        return openai.Model.delete(model_name)


def ftopenai(model="gpt-3.5-turbo"):
    """
    1. creates a training file for OpenAI Fine-tuning API
    2. Upload a training file; https://platform.openai.com/docs/guides/fine-tuning/upload-a-training-file
    3. Create a fine-tuned model; https://platform.openai.com/docs/guides/fine-tuning/create-a-fine-tuned-model

    """
    from time import sleep
    import os
    import openai

    openai.api_key = os.getenv("OPENAI_API_KEY")
    # openai.File.create(file=open("mydata.jsonl", "rb"), purpose="fine-tune")

    records = _convert_tabular_format_to_openai_format(current.df)
    stringio_object = _write_records_to_stringio(records)
    openai_file_object = openai.File.create(file=stringio_object, purpose="fine-tune")
    openai_file_id = openai_file_object.to_dict()["id"]  # type: ignore
    openai_ftjob_object = openai.FineTuningJob.create(
        training_file=openai_file_id, model=model
    )
    openai_ftjob_id = openai_ftjob_object.to_dict()["id"]  # type: ignore
    ftjob_helper = FineTuningJobHelper(openai_ftjob_id)
    current.last_openai_ftjob_id = openai_ftjob_id
    sleep(15)  # wait some time for file validation
    error_value = ftjob_helper.retrieve().to_dict()["error"]
    assert error_value is None, str(error_value)
    return ftjob_helper


def askgpt(user_content="Hello!", system_content="You are a helpful assistant."):
    import openai

    ftjob_helper = FineTuningJobHelper(current.last_openai_ftjob_id)  # type: ignore
    try:
        model_name = ftjob_helper.retrieve().to_dict()["fine_tuned_model"]
        print(f"(Using fine tuned model {current.last_openai_ftjob_id}.)")
        print()
    except Exception as e:
        model_name = "gpt-3.5-turbo-0613"
        print(f"(Fine tuned model not found.  Using base model {model_name} instead.)")
        print()

    completion = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
    )

    print(completion.choices[0].message["content"])  # type: ignore
