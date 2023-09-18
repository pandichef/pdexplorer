from pprint import pprint, pformat

# import pandas as pd
# import ._command_abbreviation # type: ignore
from .regress import regress
from .regress import regress as reg
from .regress import regress as regr
from .regress import regress as regres
from .webuse import webuse
from .logit import logit
from .drop import drop
from .browse import browse
from .gsort import gsort
from .order import order
from .keep import keep
from .scatter import scatter
from .xpose import xpose
from .lst import lst

from .clear import clear
from .clear import clearall
from .use import use
from .keepin import keepin
from .keepif import keepif
from .dropif import dropif
from .dropin import dropin
from .generate import generate
from .replace import replace
from .summarize import summarize  # "describe" in pandas
from .describe import describe  # "info" in pandas
from .tabulate import tabulate
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
from .by import by
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

# from .dataset import Dataset
# from .dataset import current
from pdexplorer.dataset import current


def methods():
    # global singleton
    for k, v in current.methods.items():
        print(k + ": ", v)


def properties():
    pprint(current.properties)


# def describe():
#     singleton.df.info()


# props = pformat(singleton.properties)
