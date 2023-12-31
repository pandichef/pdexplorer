from pprint import pprint, pformat

# import pandas as pd
# import ._command_abbreviation # type: ignore
from .regress import regress as reg
from .regress import regress as regr
from .regress import regress as regre
from .regress import regress as regres

from .regress import regress as regress

from .nn.regressnn import regressnn
from .nn.easytorch import easytorch
from .ml.regressml import regressml
from .ml.treeclassify import treeclassify as tree
from .ml.treeclassify import treeclassify as treec
from .ml.treeclassify import treeclassify as treecl
from .ml.treeclassify import treeclassify as treecla
from .ml.treeclassify import treeclassify as treeclas
from .ml.treeclassify import treeclassify as treeclass
from .ml.treeclassify import treeclassify as treeclassi
from .ml.treeclassify import treeclassify as treeclassif
from .ml.treeclassify import treeclassify as treeclassify

from .webuse import webuse
from .sysuse import sysuse
from .logit import logit
from .drop import drop

from .browse import browse as br
from .browse import browse as bro
from .browse import browse as brow
from .browse import browse as brows
from .browse import browse as browse
from .shortcuts.dfedit import dfedit as dfed
from .shortcuts.dfedit import dfedit as dfedi
from .shortcuts.dfedit import dfedit as dfedit
from .gsort import gsort
from .order import order
from .keep import keep

from .finance.mtgyield import mtgyield
from .finance.mtgprice import mtgprice
from .plus.srecode import srecode
from .shortcuts.profile import profile
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
from .summarize import summarize as sum  # "describe" in pandas
from .summarize import summarize as summ
from .summarize import summarize as summa
from .summarize import summarize as summar
from .summarize import summarize as summari
from .summarize import summarize as summariz
from .summarize import summarize as summarize
from .describe import describe  # "info" in pandas
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
from .shortcuts.melt import melt
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
from pdexplorer._dataset import current


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

from ._altair_mapper import (
    arcchart as arc,  # type: ignore
    arcchart as arcc,  # type: ignore
    arcchart as arcch,  # type: ignore
    arcchart as arccha,  # type: ignore
    arcchart as arcchar,  # type: ignore
    arcchart as arcchart,  # type: ignore
    areachart as area,  # type: ignore
    areachart as areac,  # type: ignore
    areachart as areach,  # type: ignore
    areachart as areacha,  # type: ignore
    areachart as areachar,  # type: ignore
    areachart as areachart,  # type: ignore
    barchart as bar,  # type: ignore
    barchart as barc,  # type: ignore
    barchart as barch,  # type: ignore
    barchart as barcha,  # type: ignore
    barchart as barchar,  # type: ignore
    barchart as barchart,  # type: ignore
    circlechart as circle,  # type: ignore
    circlechart as circlec,  # type: ignore
    circlechart as circlech,  # type: ignore
    circlechart as circlecha,  # type: ignore
    circlechart as circlechar,  # type: ignore
    circlechart as circlechart,  # type: ignore
    geoshapechart as geoshape,  # type: ignore
    geoshapechart as geoshapec,  # type: ignore
    geoshapechart as geoshapech,  # type: ignore
    geoshapechart as geoshapecha,  # type: ignore
    geoshapechart as geoshapechar,  # type: ignore
    geoshapechart as geoshapechart,  # type: ignore
    imagechart as image,  # type: ignore
    imagechart as imagec,  # type: ignore
    imagechart as imagech,  # type: ignore
    imagechart as imagecha,  # type: ignore
    imagechart as imagechar,  # type: ignore
    imagechart as imagechart,  # type: ignore
    linechart as line,  # type: ignore
    linechart as linec,  # type: ignore
    linechart as linech,  # type: ignore
    linechart as linecha,  # type: ignore
    linechart as linechar,  # type: ignore
    linechart as linechart,  # type: ignore
    pointchart as point,  # type: ignore
    pointchart as pointc,  # type: ignore
    pointchart as pointch,  # type: ignore
    pointchart as pointcha,  # type: ignore
    pointchart as pointchar,  # type: ignore
    pointchart as pointchart,  # type: ignore
    rectchart as rect,  # type: ignore
    rectchart as rectc,  # type: ignore
    rectchart as rectch,  # type: ignore
    rectchart as rectcha,  # type: ignore
    rectchart as rectchar,  # type: ignore
    rectchart as rectchart,  # type: ignore
    rulechart as rule,  # type: ignore
    rulechart as rulec,  # type: ignore
    rulechart as rulech,  # type: ignore
    rulechart as rulecha,  # type: ignore
    rulechart as rulechar,  # type: ignore
    rulechart as rulechart,  # type: ignore
    squarechart as square,  # type: ignore
    squarechart as squarec,  # type: ignore
    squarechart as squarech,  # type: ignore
    squarechart as squarecha,  # type: ignore
    squarechart as squarechar,  # type: ignore
    squarechart as squarechart,  # type: ignore
    textchart as text,  # type: ignore
    textchart as textc,  # type: ignore
    textchart as textch,  # type: ignore
    textchart as textcha,  # type: ignore
    textchart as textchar,  # type: ignore
    textchart as textchart,  # type: ignore
    tickchart as tick,  # type: ignore
    tickchart as tickc,  # type: ignore
    tickchart as tickch,  # type: ignore
    tickchart as tickcha,  # type: ignore
    tickchart as tickchar,  # type: ignore
    tickchart as tickchart,  # type: ignore
    trailchart as trail,  # type: ignore
    trailchart as trailc,  # type: ignore
    trailchart as trailch,  # type: ignore
    trailchart as trailcha,  # type: ignore
    trailchart as trailchar,  # type: ignore
    trailchart as trailchart,  # type: ignore
    boxplotchart as boxplot,  # type: ignore
    boxplotchart as boxplotc,  # type: ignore
    boxplotchart as boxplotch,  # type: ignore
    boxplotchart as boxplotcha,  # type: ignore
    boxplotchart as boxplotchar,  # type: ignore
    boxplotchart as boxplotchart,  # type: ignore
    errorbandchart as errorband,  # type: ignore
    errorbandchart as errorbandc,  # type: ignore
    errorbandchart as errorbandch,  # type: ignore
    errorbandchart as errorbandcha,  # type: ignore
    errorbandchart as errorbandchar,  # type: ignore
    errorbandchart as errorbandchart,  # type: ignore
    errorbarchart as errorbar,  # type: ignore
    errorbarchart as errorbarc,  # type: ignore
    errorbarchart as errorbarch,  # type: ignore
    errorbarchart as errorbarcha,  # type: ignore
    errorbarchart as errorbarchar,  # type: ignore
    errorbarchart as errorbarchart,  # type: ignore
)

from ._altair_mapper import (
    arcchart_ as arc_,  # type: ignore
    arcchart_ as arcc_,  # type: ignore
    arcchart_ as arcch_,  # type: ignore
    arcchart_ as arccha_,  # type: ignore
    arcchart_ as arcchar_,  # type: ignore
    arcchart_ as arcchart_,  # type: ignore
    areachart_ as area_,  # type: ignore
    areachart_ as areac_,  # type: ignore
    areachart_ as areach_,  # type: ignore
    areachart_ as areacha_,  # type: ignore
    areachart_ as areachar_,  # type: ignore
    areachart_ as areachart_,  # type: ignore
    barchart_ as bar_,  # type: ignore
    barchart_ as barc_,  # type: ignore
    barchart_ as barch_,  # type: ignore
    barchart_ as barcha_,  # type: ignore
    barchart_ as barchar_,  # type: ignore
    barchart_ as barchart_,  # type: ignore
    circlechart_ as circle_,  # type: ignore
    circlechart_ as circlec_,  # type: ignore
    circlechart_ as circlech_,  # type: ignore
    circlechart_ as circlecha_,  # type: ignore
    circlechart_ as circlechar_,  # type: ignore
    circlechart_ as circlechart_,  # type: ignore
    geoshapechart_ as geoshape_,  # type: ignore
    geoshapechart_ as geoshapec_,  # type: ignore
    geoshapechart_ as geoshapech_,  # type: ignore
    geoshapechart_ as geoshapecha_,  # type: ignore
    geoshapechart_ as geoshapechar_,  # type: ignore
    geoshapechart_ as geoshapechart_,  # type: ignore
    imagechart_ as image_,  # type: ignore
    imagechart_ as imagec_,  # type: ignore
    imagechart_ as imagech_,  # type: ignore
    imagechart_ as imagecha_,  # type: ignore
    imagechart_ as imagechar_,  # type: ignore
    imagechart_ as imagechart_,  # type: ignore
    linechart_ as line_,  # type: ignore
    linechart_ as linec_,  # type: ignore
    linechart_ as linech_,  # type: ignore
    linechart_ as linecha_,  # type: ignore
    linechart_ as linechar_,  # type: ignore
    linechart_ as linechart_,  # type: ignore
    pointchart_ as point_,  # type: ignore
    pointchart_ as pointc_,  # type: ignore
    pointchart_ as pointch_,  # type: ignore
    pointchart_ as pointcha_,  # type: ignore
    pointchart_ as pointchar_,  # type: ignore
    pointchart_ as pointchart_,  # type: ignore
    rectchart_ as rect_,  # type: ignore
    rectchart_ as rectc_,  # type: ignore
    rectchart_ as rectch_,  # type: ignore
    rectchart_ as rectcha_,  # type: ignore
    rectchart_ as rectchar_,  # type: ignore
    rectchart_ as rectchart_,  # type: ignore
    rulechart_ as rule_,  # type: ignore
    rulechart_ as rulec_,  # type: ignore
    rulechart_ as rulech_,  # type: ignore
    rulechart_ as rulecha_,  # type: ignore
    rulechart_ as rulechar_,  # type: ignore
    rulechart_ as rulechart_,  # type: ignore
    squarechart_ as square_,  # type: ignore
    squarechart_ as squarec_,  # type: ignore
    squarechart_ as squarech_,  # type: ignore
    squarechart_ as squarecha_,  # type: ignore
    squarechart_ as squarechar_,  # type: ignore
    squarechart_ as squarechart_,  # type: ignore
    textchart_ as text_,  # type: ignore
    textchart_ as textc_,  # type: ignore
    textchart_ as textch_,  # type: ignore
    textchart_ as textcha_,  # type: ignore
    textchart_ as textchar_,  # type: ignore
    textchart_ as textchart_,  # type: ignore
    tickchart_ as tick_,  # type: ignore
    tickchart_ as tickc_,  # type: ignore
    tickchart_ as tickch_,  # type: ignore
    tickchart_ as tickcha_,  # type: ignore
    tickchart_ as tickchar_,  # type: ignore
    tickchart_ as tickchart_,  # type: ignore
    trailchart_ as trail_,  # type: ignore
    trailchart_ as trailc_,  # type: ignore
    trailchart_ as trailch_,  # type: ignore
    trailchart_ as trailcha_,  # type: ignore
    trailchart_ as trailchar_,  # type: ignore
    trailchart_ as trailchart_,  # type: ignore
    boxplotchart_ as boxplot_,  # type: ignore
    boxplotchart_ as boxplotc_,  # type: ignore
    boxplotchart_ as boxplotch_,  # type: ignore
    boxplotchart_ as boxplotcha_,  # type: ignore
    boxplotchart_ as boxplotchar_,  # type: ignore
    boxplotchart_ as boxplotchart_,  # type: ignore
    errorbandchart_ as errorband_,  # type: ignore
    errorbandchart_ as errorbandc_,  # type: ignore
    errorbandchart_ as errorbandch_,  # type: ignore
    errorbandchart_ as errorbandcha_,  # type: ignore
    errorbandchart_ as errorbandchar_,  # type: ignore
    errorbandchart_ as errorbandchart_,  # type: ignore
    errorbarchart_ as errorbar_,  # type: ignore
    errorbarchart_ as errorbarc_,  # type: ignore
    errorbarchart_ as errorbarch_,  # type: ignore
    errorbarchart_ as errorbarcha_,  # type: ignore
    errorbarchart_ as errorbarchar_,  # type: ignore
    errorbarchart_ as errorbarchart_,  # type: ignore
)

from .shortcuts.scatter import scatter as sc
from .shortcuts.scatter import scatter as sca
from .shortcuts.scatter import scatter as scat
from .shortcuts.scatter import scatter as scatt
from .shortcuts.scatter import scatter as scatte
from .shortcuts.scatter import scatter as scatter
from .shortcuts.histogram import histogram as hist
from .shortcuts.histogram import histogram as histo
from .shortcuts.histogram import histogram as histog
from .shortcuts.histogram import histogram as histogr
from .shortcuts.histogram import histogram as histogra
from .shortcuts.histogram import histogram as histogram

# Experimental commands might not have dependencies specified in setup.py
try:
    from .experimental.flan_t5_base import flan_t5_base
    from .experimental.generate_split import generate_split
    from .experimental.nnlinear import nnlinear
    from .experimental.bard import bard
    from .experimental.chatgpt import chatgpt
    from .experimental.streamlit import streamlit
    from .experimental.scatter_seaborn import scatter as scatter_seaborn
except:
    pass

from .nn.gpt2 import gpt2
from .export import export

# from .nn.finetune import finetune
from .fine_tuning.fthuggingface import fthuggingface
from .nn.pipeline import pipeline

from .data.thegraph.utils import (
    extract_api_requests,
    tothegraph,
    searchframes,
    searchqueries,
)

from .data.thegraph.uniswap_v3.pool_page import *

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

from .browse import browse_off

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

from .fine_tuning.ftgpt import ftgpt, askgpt
from .fine_tuning.fthuggingface import fthuggingface, askhuggingface
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
