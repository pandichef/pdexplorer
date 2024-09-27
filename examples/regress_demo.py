import sys
from os.path import dirname, abspath
from pdexplorer import regress, webuse

sys.path.append(dirname(dirname(abspath(__file__))))

webuse("auto")
results = regress("mpg weight foreign")
