import re
import subprocess
from ..dataset import current
from .chatgpt import chatgpt

streamlit_script_filename = "tmpqbxcec2k.py"
dataframe_csv_filename = "tmpqbxcec2k.csv"


def streamlit(
    prompt: str = """Present this data in the best way that will impress my CEO.""",
    chart_library=None,
    use_variable_labels=False,
    openai_model="gpt-4",
):
    if use_variable_labels:
        _current_df = current.df.rename(columns=current.metadata["variable_labels"])
    else:
        _current_df = current.df

    _current_df.to_csv(dataframe_csv_filename, index=False)
    # _current_df.to_csv(dataframe_csv_filename, index=True)
    full_prompt = f"""Can you write a streamlit script.  Double check that the streamlit syntax is valid.  {prompt} Assume the data is stored in a csv file called {dataframe_csv_filename}."""

    if chart_library:
        full_prompt = (
            f"""  Wherever possible, use the {chart_library} for all charts."""
        )

    if current.metadata["data_label"]:
        full_prompt += f" Use {current.metadata['data_label']} as the script title."

    chatgpt_response_text = chatgpt(
        full_prompt, use_variable_labels=use_variable_labels, openai_model=openai_model
    )

    start_position = chatgpt_response_text.find("```python\n")
    end_position = chatgpt_response_text.find("```\n")

    python_script_text = "\n".join(
        chatgpt_response_text[start_position:end_position].split("\n")[1:]
    )

    with open(streamlit_script_filename, "w") as file:
        file.write(python_script_text)

    print(python_script_text)

    subprocess.run(
        f"streamlit run {streamlit_script_filename} --deprecation.showPyplotGlobalUse=false",
        shell=True,
    )

    # return python_script_text
