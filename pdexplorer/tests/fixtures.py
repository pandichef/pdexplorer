import pandas as pd
import numpy as np

df1 = pd.DataFrame(
    {
        "rate": [5, 4.5, 4, 3.5, 3],
        "origfixedterm": [60, 84, 120, 180, 360],
        "origterm": [360, 360, 360, 180, 360],
        "origltv": [50, 60, 70, 80, 90],
        "origfico": [620, 640, 660, 680, 700],
        "age": [12, 12, 12, 12, 12],
        "origupb": [100, 200, 300, 400, 500],
        "upb": [100, 200, 300, 400, 500],
    }
)

"""
df2 = pd.DataFrame({
    'rate': [5, 4.5, 4, 3.5, 3],
    'origfixedterm': [60, 84, 120, 180, 360],
    'origterm': [360, 360, 360, 180, 360],
    'origltv': [50, 60, 70, 80, 90],
    'origfico': [620, 640, 660, 680, 700],
    'age': [12, 12, 12, 12, 12],
    'origupb': [100, 200, 300, 400, 500],
    'upb': [100, 200, 300, 400, 500],
    'isnonagy': [0, 0, 0, 1, 1],
    'occupancy': ['investment',
                  'investment',
                  'investment',
                  'secondhome',
                  'ownerocc']
})

df3 = pd.DataFrame({
    'rate': [5, 4.5, 4, 3.5, 3],
    'origfixedterm': [60, 84, 120, np.nan, np.nan],
    'origterm': [360, 360, 360, 180, 360],
    'origltv': [50, 60, 70, 80, 90],
    'origfico': [620, 640, 660, 680, 700],
    'age': [12, 12, 12, 12, 12],
    'origupb': [100, 200, 300, 400, 500],
    'upb': [100, 200, 300, 400, 500],
    'isnonagy': [0, 0, 0, 1, 1],
    'occupancy': ['investment',
                  'investment',
                  'investment',
                  'secondhome',
                  'ownerocc']
})

df4 = df3.copy()
df4['moincome'] = pd.Series(range(10000,60000,10000))

df5 = df4.copy() # test django views
df5['sellerid'] = '4001'

df5['offer_price'] = 101
df5['mtm_benchmark_instrument'] = 'US5Y'
df5['mtm_hedge_ratio'] = -3
# df5['mtm_benchmark_level'] = 2.5

df5['min_servicing_fee'] = 0
df5['max_servicing_fee'] = 0
df5['more_servicing_preferred'] = 0
df5['servicing_multiple'] = 3

df5['proptype'] = "sfr"
df5['purpose'] = "purchase"
df5['tractlevel'] = "low"
df5['incomelevel'] = "low"
df5['state'] = "CA"
df5['isarm'] = 0
df5['isharp'] = 0
df5['descrstr'] = "30-Year Fixed Rate"
df5['_yield'] = pd.Series([1,2,3,4,5])

df6 = df5.copy()
"""

