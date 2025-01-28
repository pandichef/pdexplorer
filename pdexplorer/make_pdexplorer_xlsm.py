"""
saves python in cells as strings.
you have to manually remove the leading apostrophe in Excel to get the formulas to work.
"""
import os
import shutil
import sys
import pandas as pd
from openpyxl import load_workbook
from openpyxl.formula.translate import Translator
import click

file_dir = os.path.dirname(os.path.abspath(__file__))

# def python_to_vba_string(python_code, module_name):
#     """
#     Converts Python code into a VBA-compatible string for embedding in Excel.

#     Args:
#         python_code (str): The Python code to convert.
#         module_name (str): The name of the Python module to append.

#     Returns:
#         str: The VBA-compatible string representation.
#     """
#     # Escape double quotes for VBA
#     python_code = python_code.replace('"', '""""')

#     # Split the Python code into lines and format them for VBA
#     vba_lines = []
#     for line in python_code.splitlines():
#         if line.strip():  # Non-empty line
#             vba_lines.append(f'"{line}" & Chr(10)')
#         else:  # Empty line
#             vba_lines.append('" & Chr(10)')

#     # Add the module name and ensure VBA concatenation
#     vba_lines.append(f'"""{module_name}""" & Chr(10)')

#     # Join the lines, adding VBA concatenation (`& _`) for long lines
#     vba_string = " & _\n        ".join(vba_lines)

#     # Wrap everything in =PY(...) as required
#     return f"=PY({vba_string})"


def make_xlsm_file_with_py_function_hack(filename, columnA_contents):
    """
    openpyxl can't directly create a =py() function
    Modern Excel forces the function to be =@py(), which errors out
    """
    if not filename.lower().endswith('.xlsm'):
        raise ValueError(f"Only .xlsm files are supported. Provided: '{filename}'")

    # If the file does not exist, create an empty macro-enabled workbook
    if not os.path.exists(filename):
        template_path = os.path.join(file_dir,"_template.xlsm")  # Path to a macro-enabled workbook template
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template '{template_path}' required to create .xlsm files is missing.")
        shutil.copy(template_path, filename)
        print(f"Created new macro-enabled workbook '{filename}' using the template.")

    # Now load with keep_vba to preserve macros
    try:
        wb = load_workbook(filename, keep_vba=True)
    except Exception as e:
        raise OSError(f"Unable to load '{filename}' as a macro-enabled workbook.") from e

    # Either clear or create the _pdexplorer sheet
    if "_pdexplorer" in wb.sheetnames:
        ws = wb["_pdexplorer"]
        for row in ws.iter_rows():
            for cell in row:
                cell.value = None
    else:
        ws = wb.create_sheet("_pdexplorer")


    # Write the DataFrame to the _pdexplorer sheet
    df = pd.DataFrame({"A": columnA_contents})
    for i, value in enumerate(df["A"], start=1):
        if isinstance(value, str) and value.startswith("=PY("):
            ws[f"A{i}"].value = value  # '=PY("a = 1")'  # Assign the formula
            ws[f"A{i}"].data_type = "s"  # Explicitly mark as string type
        else:
            ws[f"A{i}"].value = value

    # Save the workbook
    wb.save(filename)
    wb.close()
    print(f"Sheet '_pdexplorer' updated in '{filename}'.")


def make_module_contents_list(module_names, wrap_with_xl_py_formula=True):
    """
    Given a list of module filenames (like ["_search.py"]), read each file's contents
    from the current directory, remove full-line comments (prefixed with "#"),
    then wrap them in a formula string =PY("...").
    Return a list of such strings.
    """
    import os
    module_formulas = []
    for module_name in module_names:
        with open(os.path.join(file_dir, module_name), "r", encoding="utf-8") as f:
            lines = f.readlines()

        processed_lines = []
        for line in lines:
            stripped_line = line.strip()
           
            if stripped_line.startswith("#") \
                or stripped_line.startswith("from .") \
                or stripped_line.startswith("from xlwings"):
                continue # line to skip
            if stripped_line.startswith("from rich import print as rich_print"):
                processed_lines.append("rich_print = print\n")
            else:
                processed_lines.append(line)

        # Join the processed lines
        filtered_code = "".join(processed_lines)

        # Add module name and wrap in =PY
        filtered_code += f'\n\n"{module_name}"'
        if wrap_with_xl_py_formula:
            formula_str = f"""'=PY({filtered_code}\n"""
        else:
            formula_str = f"""{filtered_code}\n"""
        module_formulas.append(formula_str)

    return module_formulas

def split_into_chunks(strings, max_length=8192):
    result = []
    current_chunk = ""

    for item in strings:
        if len(current_chunk) + len(item) + 1 <= max_length:  # +1 accounts for the newline
            current_chunk += item + "\n"  # Add item with a newline
        else:
            result.append(current_chunk.rstrip("\n"))  # Save the chunk without the trailing newline
            current_chunk = item + "\n"  # Start a new chunk with the current item

    if current_chunk:  # Add the last chunk if it's not empty
        result.append(current_chunk.rstrip("\n"))

    return result

def minify_python(code):
    # TODO
    return code

# if __name__ == "__main__":
@click.command()
@click.argument("xlsm_file_path")
@click.option("-m", "--minify", is_flag=True, help="Enable code minification.")
def main(xlsm_file_path, minify):
    # def main():
    try:
        # filename = sys.argv[1]
        filename = xlsm_file_path
    except IndexError:
        raise Exception("Please provide a filename as an argument.")
    module_names = ["_search.py","_dataset.py","_get_custom_attributes.py","_patsify.py","_print.py",
                    "_commandarg.py","_quietly.py","_print_horizontal_line.py","preserve.py","use.py",
                    "sort.py","_by.py","regress.py","scatter.py","histogram.py","logit.py","drop.py"]
    if minify:
        columnA_contents_not_wrapped = make_module_contents_list(module_names, wrap_with_xl_py_formula=False)
        # columnA_contents_minified = [python_minifier.minify(s) for s in columnA_contents_not_wrapped]
        columnA_contents_minified = [minify_python(s) for s in columnA_contents_not_wrapped]
        # columnA_contents_minified = [s for s in columnA_contents_not_wrapped]
        # print(columnA_contents_minified[0])
        # char_counts2 = [len(s) for s in columnA_contents_minified]
        # print(char_counts2)
        # char_counts = [len(s) for s in columnA_contents_not_wrapped]
        # print(char_counts)
        columnA_contents_chunked = split_into_chunks(columnA_contents_minified)
        prefixed_lines = [f"""'=PY({line}\n""" for line in columnA_contents_chunked]
        make_xlsm_file_with_py_function_hack(filename, prefixed_lines)
    else:
        columnA_contents = make_module_contents_list(module_names, wrap_with_xl_py_formula=True)
        make_xlsm_file_with_py_function_hack(filename, columnA_contents)

if __name__ == "__main__":
    main()
