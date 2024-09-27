import statsmodels.api as sm
import numpy as np
import pandas as pd
from pandas import CategoricalDtype
from pprint import pprint

from pdexplorer import (
    webuse,
    regress,
    methods,
    properties,
    describe,
    current,
    logit,
    # logistic2,
)

webuse("lbw")
describe()

results = logit("low age lwt race smok ptl ht ui")
methods()
