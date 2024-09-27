import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from pdexplorer import (
    webuse,
    methods,
    describe,
    logit,
)

webuse("lbw")
describe()

results = logit("low age lwt race smok ptl ht ui")
methods()
