from ._dataset import current


def doedit(filename: str) -> None:
    import subprocess

    subprocess.run(f"code {filename}", shell=True)
    current.active_python_script = filename


# def _run_active_python_script():
#     os.subprocess(f'ipython -c "%run {current.active_python_script}"', s)
###################################################################################
def check_script_for_input(script_path):
    """
    input() crashes when used with a hotkey
    This is true for both the keyboard and pynput packages
    """
    import ast

    class InputNotAllowedException(Exception):
        pass

    with open(script_path, "r") as script_file:
        script_source = script_file.read()

    # Parse the script source code into an Abstract Syntax Tree (AST)
    try:
        tree = ast.parse(script_source)
    except SyntaxError as e:
        print(f"Syntax error in the script: {e}")
        return

    # Walk through the AST to check for 'input' calls
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "input"
        ):
            raise InputNotAllowedException(
                "The 'input()' function is not allowed in this script"
            )


def run_active_python_script() -> None:
    from IPython.core.getipython import get_ipython

    if current.active_python_script:
        check_script_for_input(current.active_python_script)
        print(f"Running {current.active_python_script}.")
        get_ipython().run_line_magic("run", current.active_python_script)
    else:
        print("No active python script. Run doedit command first.")
