from ._dataset import current


def doedit(filename: str) -> None:
    import subprocess

    subprocess.run(f"code {filename}", shell=True)
    current.active_python_script = filename


# def _run_active_python_script():
#     os.subprocess(f'ipython -c "%run {current.active_python_script}"', s)


def run_active_python_script() -> None:
    from IPython.core.getipython import get_ipython

    if current.active_python_script:
        get_ipython().run_line_magic("run", current.active_python_script)
    else:
        print("No active python script. Run doedit command first.")
