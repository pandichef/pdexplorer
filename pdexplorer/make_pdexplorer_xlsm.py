"""
This script creates a template file called _pdexplorer.xlsm that
contains all the python code in the pdexplorer package.

When a user runs the insert_pdexplorer script, the code in the 
_pdexplorer.xlsm file will be inserted into user's Excel workbook.

Example usage:
insert_pdexplorer my_excel_sheet.xlsm
"""
import os
import shutil
import sys
import pandas as pd
from openpyxl import load_workbook
from openpyxl.formula.translate import Translator
import click
import xlwings as  xw

file_dir = os.path.dirname(os.path.abspath(__file__))

xlsm_template_file = '_pdexplorer.xlsm'

module_names = ["_search.py","_dataset.py","_get_custom_attributes.py","_patsify.py","_print.py",
                    "_commandarg.py","_quietly.py","_print_horizontal_line.py","preserve.py","use.py",
                    "sort.py","_by.py","regress.py","scatter.py","histogram.py","logit.py","drop.py",
                    "order.py"]

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
            formula_str = f"""=PY("{filtered_code.replace('"','""')}",1)\n"""
        else:
            formula_str = f"""{filtered_code}\n"""
        module_formulas.append(formula_str)

    return module_formulas

def create_pdexplorer_xlsm(xlsm_template_file):
    wb = xw.Book(xlsm_template_file)
    sheet = wb.sheets[0]
    sheet.clear_contents()
    sheet.range("A1").value = "Module Name"
    sheet.range("B1").value = "Python Object"
    python_cell_list = make_module_contents_list(module_names)
    for i, module_name in enumerate(module_names):
        sheet.range(f"A{i+2}").value = module_name
        sheet.range(f"B{i+2}").formula2 = python_cell_list[i]
    wb.save(xlsm_template_file)
    wb.close()


if __name__ == "__main__":
    create_pdexplorer_xlsm(xlsm_template_file)
    # list(map(make_module_contents_list, module_names))
    # df = pd.DataFrame({"Module": module_names, "Python Object": make_module_contents_list(module_names)})
    # df.to_excel("pdexplorer.xlsm")
    # if os.path.exists("pdexplorer.xlsm"):
    #     os.remove("pdexplorer.xlsm")
    # wb = xw.Book(xlsm_template_file)
    # sheet = wb.sheets[0]
    # sheet.clear_contents()
    # sheet.range("A1").value = "Module Name"
    # sheet.range("B1").value = "Python Object"
    # python_cell_list = make_module_contents_list(module_names)
    # for i, module_name in enumerate(module_names):
    #     sheet.range(f"A{i+2}").value = module_name
    #     sheet.range(f"B{i+2}").formula2 = python_cell_list[i]
    # wb.save(xlsm_template_file)
    # wb.close()
