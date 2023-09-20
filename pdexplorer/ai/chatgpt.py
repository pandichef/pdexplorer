import io
import sys
from contextlib import contextmanager
from ..dataset import current


@contextmanager
def capture_stdout():
    # Create a StringIO object to capture stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        yield sys.stdout
    finally:
        # Restore the original stdout
        sys.stdout = old_stdout


def chatgpt(
    prompt: str = "Can you summarize this data?",
    head=100,
    use_variable_labels=False,
    openai_model="gpt-3.5-turbo",
):
    # See https://platform.openai.com/account/billing/overview
    import os
    import openai

    if use_variable_labels:
        _current_df = current.df.rename(columns=current.metadata["variable_labels"])
    else:
        _current_df = current.df

    with capture_stdout() as captured_output:
        _current_df.info()

    # print(captured_output.getvalue())
    # print(captured_output.getvalue())

    if head:
        prompt = (
            _current_df.head(head).to_csv()
            + "\n\n"
            + captured_output.getvalue()
            + f"\n\n{prompt}"
        )
    else:
        prompt = (
            _current_df.to_csv() + "\n\n" + captured_output.getvalue() + f"\n\n{prompt}"
        )

    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
        model=openai_model, messages=[{"role": "user", "content": prompt,}],
    )

    return completion.choices[0].message.content
