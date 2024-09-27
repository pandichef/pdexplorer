from os.path import dirname, abspath
import os
import sys

statement_list = """
from pdexplorer import *
"""

statement_list = statement_list.strip().split("\n")

load_modules(statement_list)


force_autoreload(modules_i_am_actively_developing=["pdexplorer"])
