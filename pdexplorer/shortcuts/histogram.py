import altair as alt
from .._altair_mapper import barchart  # type: ignore


def histogram(varname) -> alt.Chart:
    return barchart().encode(alt.X(varname, bin=True), y="count()")
