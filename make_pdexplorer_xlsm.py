def make_vba_formula(file_contents, file_name):
    # TODO: there are still many corner cases where this doesn't work
    lines = file_contents.strip().split("\n")
    for i in range(len(lines)):
        lines[i] = lines[i].replace('"', '""""')
        lines[i] = '"' + lines[i] + '"'
    lines.append('""')
    lines.append('"""""'+file_name+'"""""')
    joined_lines = ' & Chr(10) & '.join(lines)
    return joined_lines

def make_vba_formula2R1C1(formula_string, cell_reference):
    return f'Range("{cell_reference}").Formula2R1C1 = "=PY("' + formula_string + '",1)"'

def make_list_of_vba_formula2R1C1_commands(module_names):
    import os
    module_formulas = []
    row_number = 0
    for module_name in module_names:
        row_number += 1
        with open(os.path.join('pdexplorer', module_name), "r", encoding="utf-8") as f:
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
        formula_str = make_vba_formula2R1C1(make_vba_formula(filtered_code, module_name), "A"+ str(row_number))

        # filtered_code +
        # filtered_code += f'\n\n"{module_name}"'
        # formula_str = f"""'=PY({filtered_code}\n"""
        module_formulas.append(formula_str)

    return module_formulas

def make_vba_macro(module_formulas):
    # insert 4 spaces before each line
    module_formulas = [f"    {line}" for line in module_formulas]
    return 'Sub InsertPythonCells\n' + '\n'.join(module_formulas) + '\nEnd Sub'



def insert_and_run_vba(xlsm_file_path, vba_code):
    """
    Injects a VBA module into the .xlsm file, creating the file if it doesn't exist,
    and runs a macro that processes cells with '=PY(...)' formulas.
    """
    import os
    import win32com.client as win32

    # Launch Excel via COM, make it visible for SendKeys functionality
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    excel.Visible = True  # Required for SendKeys to work reliably

    # Create a new .xlsm file if it doesn't exist
    if not os.path.exists(xlsm_file_path):
        wb = excel.Workbooks.Add()
        wb.SaveAs(os.path.abspath(xlsm_file_path), FileFormat=52)  # 52 = xlOpenXMLWorkbookMacroEnabled
        wb.Close()

    # Open the existing or newly created .xlsm file
    wb = excel.Workbooks.Open(os.path.abspath(xlsm_file_path))

    # Access the VBA project
    vbproject = wb.VBProject

    # Define the module name
    module_name = "InsertPythonCells"

    # Add or retrieve the VBA module
    try:
        vb_module = vbproject.VBComponents(module_name)
    except:
        vb_module = vbproject.VBComponents.Add(1)  # 1 = vbext_ct_StdModule
        vb_module.Name = module_name

    # Insert or replace VBA code in the module
    code_module = vb_module.CodeModule
    code_module.DeleteLines(1, code_module.CountOfLines)
    code_module.AddFromString(vba_code)

    # Run the macro
    macro_name = f"{module_name}.InsertPythonCells"
    excel.Run(macro_name)

    # Save and close the workbook
    wb.Save()
    wb.Close()
    excel.Quit()

    print("VBA macro injected, executed, and the workbook saved.")


if __name__ == "__main__":
    # module_names = [
    #     "tmp123.py"] # ,"_search.py"]
    module_names = ["_search.py","_dataset.py","_get_custom_attributes.py","_patsify.py","_print.py",
                    "_commandarg.py","_quietly.py","_print_horizontal_line.py","preserve.py","use.py",
                    "sort.py","_by.py","regress.py","scatter.py","histogram.py","logit.py","drop.py"]
    module_formulas = make_list_of_vba_formula2R1C1_commands(module_names)
    vba_code = make_vba_macro(module_formulas)
    # print(make_list_of_vba_formula2R1C1_commands(module_names))
    insert_and_run_vba('example4.xlsm', vba_code)
    # print(vba_code)
