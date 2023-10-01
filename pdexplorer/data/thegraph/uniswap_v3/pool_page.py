import os
import json
from ..utils import tothegraph


def get_pool_page_queries():
    # print(os.path.dirname(__file__))
    with open(os.path.join(os.path.dirname(__file__), "pool_page.json"), "r") as f:
        pool_page = json.loads(f.read())
    return pool_page


# 0: TS daily
# 1: cf 6 other pools
# 2: cf 50 other pools
# 3: transactions
# 4: factory summary
# 5: block number (scalar value) i.e., 18245306 use in [12, 15, 20, 24, 28, 32, 34, 38]
# 6: cf 7 other pools
# 7: cf 50 other tokens
# 8: transactions
# 9: error
# 10: empty
# 11: block number (scalar value) i.e., 18238166 use in [13, 16, 21, 25, 29, 31, 35, 39]
# 12: cf 6 other pools
# 13: cf 6 other pools
# 14: cf 6 other pools
# 15: empty
# 16: empty
