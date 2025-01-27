from make_pdexplorer_xlsm import make_vba_formula,  make_vba_formula2R1C1


def test_make_vba_formula_one_line():
    file_contents = """a = 1"""
    file_name = "tmp123.py"
    vba_string = (
    '''"a = 1" & Chr(10) & "" & Chr(10) & """""tmp123.py"""""'''
)
    assert make_vba_formula(file_contents, file_name) == vba_string


def test_make_vba_formula_two_lines():
    file_contents = """a = 1
b = 2
"""
    file_name = "tmp123.py"
    vba_string = (
    '''"a = 1" & Chr(10) & "b = 2" & Chr(10) & "" & Chr(10) & """""tmp123.py"""""'''
)
    assert make_vba_formula(file_contents, file_name) == vba_string

def test_make_vba_formula_a_function():
    file_contents = """def my_function():
    return 'hello world'
"""
    file_name = "tmp123.py"
    vba_string = (
    '''"def my_function():" & Chr(10) & "    return 'hello world'" & Chr(10) & "" & Chr(10) & """""tmp123.py"""""'''
)
    assert make_vba_formula(file_contents, file_name) == vba_string

def test_make_vba_formula2R1C1_a_function():
    file_contents = """def my_function():
    return 'hello world'
"""
    file_name = "tmp123.py"
    vba_string = (
    '''Range("A1").Formula2R1C1 = "=PY(""def my_function():" & Chr(10) & "    return 'hello world'" & Chr(10) & "" & Chr(10) & """""tmp123.py"""""",1)"'''
)
    
    assert make_vba_formula2R1C1(make_vba_formula(file_contents, file_name), "A1") == vba_string
    # print()
    # print(make_vba_formula2R1C1(make_vba_formula(file_contents, file_name)))
    # print(vba_string)
