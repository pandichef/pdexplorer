from pprint import pprint, pformat

# import pandas as pd
# import ._command_abbreviation # type: ignore
from .regress import regress as reg
from .regress import regress as regr
from .regress import regress as regre
from .regress import regress as regres
from .regress import regress as regress
from .webuse import webuse
from .logit import logit
from .drop import drop
from .browse import browse
from .gsort import gsort
from .order import order
from .keep import keep
from .scatter import scatter as scatter_old
from .xpose import xpose
from .lst import lst

from .clear import clear
from .clear import clearall
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
from .quietly import quietly
from .collapse import collapse
from .egen import egen
from .reshape import reshapelong, reshapewide
from .profile import ydata_profile
from .sort import sort
from .by import by  # context manager
from .melt import melt
from .ai.flan_t5_base import flan_t5_base
from .ai.generate_split import generate_split
from .ai.nnlinear import nnlinear
from ._print_horizontal_line import print_horizontal_line
from .cf import cf
from .returnlist import (
    returnlist,
    _r,
    ereturnlist,
    _e,
    sreturnlist,
    _s,
    nreturnlist,
    _n,
    creturnlist,
    _c,
)

from .ai.bard import bard
from .ai.chatgpt import chatgpt
from .ai.streamlit import streamlit


# from .dataset import Dataset
# from .dataset import current
from pdexplorer.dataset import current
from pdexplorer.altair_mapper import (
    histogram,
    scatter,
    arcchart,  # type: ignore
    areachart,  # type: ignore
    barchart,  # type: ignore
    circlechart,  # type: ignore
    geoshapechart,  # type: ignore
    imagechart,  # type: ignore
    linechart,  # type: ignore
    pointchart,  # type: ignore
    rectchart,  # type: ignore
    rulechart,  # type: ignore
    squarechart,  # type: ignore
    textchart,  # type: ignore
    tickchart,  # type: ignore
    trailchart,  # type: ignore
    boxplotchart,  # type: ignore
    errorbandchart,  # type: ignore
    errorbarchart,  # type: ignore
)


def methods():
    # global singleton
    for k, v in current.methods.items():
        print(k + ": ", v)


def properties():
    pprint(current.properties)


# def describe():
#     singleton.df.info()


# props = pformat(singleton.properties)
