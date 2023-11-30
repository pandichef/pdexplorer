import pandas as pd
from ._dataset import current
from ._get_custom_attributes import _get_custom_attributes
from ._patsify import _patsify
from ._print import _print


def logit(varlist: str):
    import statsmodels.formula.api as smf

    df = current.df.copy()
    depvarname = varlist.split()[0]
    if df[depvarname].dtype == "category":
        newcolumn_as_df = pd.get_dummies(df[depvarname], drop_first=True, dtype=int)
        df[depvarname] = newcolumn_as_df[newcolumn_as_df.columns[0]]
    patsy_formula = _patsify(varlist)
    # print(patsy_formula)
    model = smf.logit(patsy_formula, data=df)
    # print(234)
    results = model.fit()
    _print(results.summary())
    current.methods, current.properties = _get_custom_attributes(results)

    # todo: results and predict command (see regress for examples)
    print("(post-estimation not yet supported)")

    return results
