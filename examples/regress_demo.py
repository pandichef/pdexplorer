import statsmodels.api as sm
import numpy as np
import pandas as pd
from pandas import CategoricalDtype
from pprint import pprint

from pdexplorer import *

webuse("auto")
results = regress(varlist="mpg weight foreign")
# print(dir(results))
# print(results.params)
# print(results.bse)
# print(vars(results))
# pprint(results)
# methods()
# properties()
# print(props)
