# print("Loading pdexplorer functions")
print("■", end="")
from pprint import pprint, pformat

# import pandas as pd
# import ._command_abbreviation # type: ignore
from .regress import regress as reg
from .regress import regress as regr
from .regress import regress as regre
from .regress import regress as regres

from .regress import regress as regress

from .not_in_stata.nn.regressnn import regressnn
from .not_in_stata.nn.easytorch import easytorch
from .not_in_stata.ml.regressml import regressml
from .not_in_stata.ml.treeclassify import treeclassify as tree
from .not_in_stata.ml.treeclassify import treeclassify as treec
from .not_in_stata.ml.treeclassify import treeclassify as treecl
from .not_in_stata.ml.treeclassify import treeclassify as treecla
from .not_in_stata.ml.treeclassify import treeclassify as treeclas
from .not_in_stata.ml.treeclassify import treeclassify as treeclass
from .not_in_stata.ml.treeclassify import treeclassify as treeclassi
from .not_in_stata.ml.treeclassify import treeclassify as treeclassif
from .not_in_stata.ml.treeclassify import treeclassify as treeclassify

from .webuse import webuse
from .sysuse import sysuse
from .logit import logit
from .drop import drop

from .browse import browse as br
from .browse import browse as bro
from .browse import browse as brow
from .browse import browse as brows
from .browse import browse as browse
from .not_in_stata.shortcuts.dfedit import dfedit as dfed
from .not_in_stata.shortcuts.dfedit import dfedit as dfedi
from .not_in_stata.shortcuts.dfedit import dfedit as dfedit
from .gsort import gsort
from .order import order
from .keep import keep

from .not_in_stata.finance.mtgyield import mtgyield
from .not_in_stata.finance.mtgprice import mtgprice
from .plus.srecode import srecode
from .not_in_stata.shortcuts.profile import profile
from .doedit import doedit as doed
from .doedit import doedit as doedi
from .doedit import doedit as doedit
from .doedit import doedit as pyed
from .doedit import doedit as pyedi
from .doedit import doedit as pyedit

# from .scatter import scatter as scatter_old
from .xpose import xpose
from .lis import lis as li
from .lis import lis as lis

from .clear import clear

# from .clear import clearall
from .use import use

# from .keepin import keepin
# from .keepif import keepif
# from .dropif import dropif
# from .dropin import dropin
from .generate import generate as gen
from .generate import generate as gene
from .generate import generate as gener
from .generate import generate as genera
from .generate import generate as generat
from .generate import generate as generate
from .replace import replace

# from .summarize import summarize as sum
from .summarize import summarize as su  # "describe" in pandas

# from .summarize import summarize as sum  # don't override built-in python function
from .summarize import summarize as summ  # "describe" in pandas
from .summarize import summarize as summa
from .summarize import summarize as summar
from .summarize import summarize as summari
from .summarize import summarize as summariz
from .summarize import summarize as summarize
from .describe import describe as d  # eq "info" in pandas
from .describe import describe as de
from .describe import describe as des
from .describe import describe as desc
from .describe import describe as descr
from .describe import describe as descri
from .describe import describe as describ
from .describe import describe as describe
from .tabulate import tabulate as tab
from .tabulate import tabulate as tabu
from .tabulate import tabulate as tabul
from .tabulate import tabulate as tabula
from .tabulate import tabulate as tabulat
from .tabulate import tabulate as tabulate
from .rename import rename
from .save import save
from .preserve import preserve
from .merge import merge
from .restore import restore
from ._quietly import quietly as qui
from ._quietly import quietly as quie
from ._quietly import quietly as quiet
from ._quietly import quietly as quietl
from ._quietly import quietly as quietly
from .collapse import collapse
from .egen import egen
from .reshape import reshapelong, reshapewide
from .sort import sort
from ._by import by  # context manager
from .not_in_stata.shortcuts.melt import melt
from ._print_horizontal_line import print_horizontal_line
from .cf import cf
from .returnlist import (
    returnlist,
    r_,
    ereturnlist,
    e_,
    sreturnlist,
    s_,
    nreturnlist,
    n_,
    creturnlist,
    c_,
)


# from ._dataset import Dataset
# from ._dataset import current
# from pdexplorer._dataset import current
from pdexplorer._dataset import current

# current2 = current


def methods():
    # global singleton
    for k, v in current.methods.items():
        print(k + ": ", v)


def properties():
    pprint(current.properties)


# def describe():
#     singleton.df.info()


# props = pformat(singleton.properties)

# from pdexplorer._altair_mapper import circlechart_ as circle_  # type: ignore

# print(_circlechart)
# print(_circlechart)
# print(_circlechart)
# print(_circlechart)
#  as blahblah  # type: ignore

# _circle = blahblah


from .scatter import scatter as sc
from .scatter import scatter as sca
from .scatter import scatter as scat
from .scatter import scatter as scatt
from .scatter import scatter as scatte
from .scatter import scatter as scatter
from .histogram import histogram as hist
from .histogram import histogram as histo
from .histogram import histogram as histog
from .histogram import histogram as histogr
from .histogram import histogram as histogra
from .histogram import histogram as histogram

# Experimental commands might not have dependencies specified in setup.py
try:
    from .not_in_stata.experimental.flan_t5_base import flan_t5_base
    from .not_in_stata.experimental.generate_split import generate_split
    from .not_in_stata.experimental.nnlinear import nnlinear
    from .not_in_stata.experimental.bard import bard
    from .not_in_stata.experimental.chatgpt import chatgpt
    from .not_in_stata.experimental.streamlit import streamlit
    from .not_in_stata.experimental.scatter_seaborn import scatter as scatter_seaborn
except:
    pass

from .not_in_stata.nn.gpt2 import gpt2
from .export import export

# from .not_in_stata.nn.finetune import finetune
from .not_in_stata.fine_tuning.fthuggingface import fthuggingface
from .not_in_stata.nn.pipeline import pipeline

# from .data.thegraph.utils import (
#     extract_api_requests,
#     tothegraph,
#     searchframes,
#     searchqueries,
# )

# from .data.thegraph.uniswap_v3.pool_page import *

from .doedit import run_active_python_script

# from IPython.core.getipython import get_ipython

# get_ipython().run_line_magic("shortcut", "Ctrl-D", "run_active_python_script")
# from time import time

# t0 = time()
# try:
#     import keyboard

# keyboard.add_hotkey("ctrl+f9", run_active_python_script)
# except:
#     pass  # fails in github actions
# print(time() - t0)

# from .browse import browse_off

# keyboard.as

# import keyboard

# keyboard.add_hotkey("ctrl+f9", lambda: input("How are you?"))
try:
    from ._hotkeys import hotkey_ctrl_f9

    hotkey_ctrl_f9(run_active_python_script)
except:
    pass


# from pynput import keyboard

# listener = keyboard.GlobalHotKeys({"<ctrl>+h": run_active_python_script})
# listener.start()

from .not_in_stata.fine_tuning.ftgpt import ftgpt, askgpt
from .not_in_stata.fine_tuning.fthuggingface import fthuggingface, askhuggingface
from .predict import predict
from .sample import sample

import warnings

warnings.filterwarnings("ignore")

##############################################################################
##############################################################################
##############################################################################
# STATA INTERACTIVE
def _exec_without_exit(command):
    try:
        exec(command)
        print()
    except Exception as e:
        RED = "\033[31m"
        RESET = "\033[0m"
        print(RED + type(e).__name__ + RESET + ": " + str(e) + "\n")


def _make_python_context(stata_context: str) -> str:
    stata_context_split = stata_context.split()
    if len(stata_context_split) == 2:
        context_name, context_arg = stata_context.split()
        return f'with {context_name}("{context_arg}"):\n    '
    elif len(stata_context_split) == 1:
        context_name = stata_context_split[0]
        return f"with {context_name}():\n    "
    else:
        return ""


def _extract_stata_context(user_input_plus_context: str) -> tuple:
    if user_input_plus_context.find(":") > -1:
        context, user_input = user_input_plus_context.split(":")
        if context == "python":  # "python:" doesn't signify python context
            context, user_input = "", user_input_plus_context
    else:
        context = ""
        user_input = user_input_plus_context
    return context, user_input


def _make_python_instruction(user_input_plus_context: str) -> str:
    context, user_input = _extract_stata_context(user_input_plus_context)
    # if user_input_plus_context.find(":") > -1:
    #     context, user_input = user_input_plus_context.split(":")
    # else:
    #     context = ""
    #     user_input = user_input_plus_context
    user_input_split = user_input.split()
    if user_input_split:
        if user_input_split[0] == "list":  # since list is a keyword in Python
            user_input_split[0] = "lis"
        if user_input_split[0] == "python:":
            python_instruction = " ".join(user_input_split[1:])
            # _exec_without_exit(python_instruction)
        elif len(user_input_split) == 1:
            python_instruction = user_input_split[0] + "()"
            # _exec_without_exit(python_instruction)
        else:
            commandname = user_input_split[0]
            commandargs = " ".join(user_input_split[1:])
            python_instruction = (
                _make_python_context(context) + f"{commandname}('{commandargs}')"
            )
        return python_instruction
    else:
        return ""


def _do_interactive(save_as="working.do"):
    # cases: end, noargs, python:, else
    saved_command_list = []
    saved_command_list_py = []
    from rich.console import Console

    console = Console()
    console.rule("stata (type end to exit)")
    while True:
        user_input_plus_context = input(". ")
        if user_input_plus_context in ["end", "quit"]:
            do_file = save_as.split(".")[0] + ".do"
            py_file = save_as.split(".")[0] + ".py"
            with open(do_file, "w") as file:
                for item in saved_command_list:
                    file.write(f"{item}\n")
            with open(py_file, "w") as file:
                for item in saved_command_list_py:
                    file.write(f"{item}\n")
            console.rule(f"saved {do_file}/{py_file}")
            break
        # run commands
        # if user_input_plus_context.find(":") > -1:
        #     context, user_input = user_input_plus_context.split(":")
        # else:
        #     context = ""
        #     user_input = user_input_plus_context
        # user_input_split = user_input.split()
        # if user_input_split:
        #     if user_input_split[0] == "list":  # since list is a keyword in Python
        #         user_input_split[0] = "lis"
        #     if user_input_split[0] == "python:":
        #         python_instruction = " ".join(user_input_split[1:])
        #         # _exec_without_exit(python_instruction)
        #     elif len(user_input_split) == 1:
        #         python_instruction = user_input_split[0] + "()"
        #         # _exec_without_exit(python_instruction)
        #     else:
        #         commandname = user_input_split[0]
        #         commandargs = " ".join(user_input_split[1:])
        #         python_instruction = (
        #             _make_context(context) + f"{commandname}('{commandargs}')"
        #         )
        #         # _exec_without_exit(python_instruction)
        #     # save commands
        #     _exec_without_exit(python_instruction)
        #     saved_command_list.append(user_input_plus_context)
        python_instruction = _make_python_instruction(user_input_plus_context)
        # print(python_instruction)
        _exec_without_exit(python_instruction)
        saved_command_list.append(user_input_plus_context)
        saved_command_list_py.append(python_instruction)


def _do_execute(filename="working.do", inline=None):
    if inline:
        file_contents = inline
    else:
        with open(filename, "r") as f:
            file_contents = f.read()
    commands = file_contents.split("\n")
    commands = [item for item in commands if item != ""]

    for user_input_plus_context in commands:
        print(f"\n. {user_input_plus_context}")
        # run commands
        # if user_input_plus_context.find(":") > -1:
        #     context, user_input = user_input_plus_context.split(":")
        # else:
        #     context = ""
        #     user_input = user_input_plus_context
        # user_input_split = user_input.split()
        # if user_input_split:
        #     if user_input_split[0] == "list":  # since list is a keyword in Python
        #         user_input_split[0] = "lis"
        #     if user_input_split[0] == "python:":
        #         python_instruction = " ".join(user_input_split[1:])
        #         # exec(python_instruction)
        #         # print()
        #     elif len(user_input_split) == 1:
        #         python_instruction = user_input_split[0] + "()"
        #         # exec(python_instruction)
        #     else:
        #         commandname = user_input_split[0]
        #         commandargs = " ".join(user_input_split[1:])
        #         python_instruction = (
        #             _make_context(context) + f"{commandname}('{commandargs}')"
        #         )
        #         # exec(python_instruction)
        #     exec(python_instruction)
        python_instruction = _make_python_instruction(user_input_plus_context)
        exec(python_instruction)


def do(filename=None, inline=None):
    if inline:
        _do_execute(inline=inline)
    elif filename:
        _do_execute(filename=filename)
    else:
        _do_interactive()
