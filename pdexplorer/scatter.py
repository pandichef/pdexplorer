# TODO: support multiple variables e.g.,  scatter yvar1 yvar2 xvar
# Deprecated: use altair_mapper instead
from .dataset import current
from .search import search_iterable
import warnings
from .commandarg import parse_commandarg


def scatter(commandarg: str, byvar=None) -> None:
    import matplotlib.pyplot as plt

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import seaborn as sns  # produces a bunch of warnings during tests

    sns.set()

    parsed_commandarg = parse_commandarg(commandarg)
    df = current.df
    # try:
    varlist = search_iterable(df.columns, parsed_commandarg["anything"])
    # fig, ax = plt.subplots()
    assert len(varlist) == 2, "Scatterplot only supports two variables"
    # ax.scatter(labels[1], labels[0], data=df)
    scatterplot = sns.scatterplot(x=varlist[1], y=varlist[0], data=df)

    try:
        scatterplot.set(
            xlabel=current.metadata["variable_labels"][varlist[1]],
            ylabel=current.metadata["variable_labels"][varlist[0]],
        )
    except KeyError:
        scatterplot.set(xlabel=varlist[1], ylabel=varlist[0])

    if byvar:
        for index, row in df.iterrows():
            plt.text(row[varlist[1]], row[varlist[0]], row[byvar], fontsize=12)
    plt.show()
