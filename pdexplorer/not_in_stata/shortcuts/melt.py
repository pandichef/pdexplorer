import pandas as pd
from ..._commandarg import parse, parse_options
from ..._dataset import current
from ..._print import _print


def melt(commandarg, use_labels=True):
    # e.g., melt("miles_per_gallon horsepower,  keep(weight_in_lbs)")
    _ = parse(commandarg)
    parsed_options = parse_options(_["options"])
    value_vars = _["anything"].split()
    id_vars = parsed_options["keep"].split()
    if use_labels:
        for var in value_vars:
            current._df = current._df.rename(
                columns={var: current.metadata["variable_labels"][var]}
            )
        value_vars = list(
            map(lambda x: current.metadata["variable_labels"][x], value_vars)
        )

    current._df = pd.melt(current._df, id_vars=id_vars, value_vars=value_vars)
    _print(current._df)
