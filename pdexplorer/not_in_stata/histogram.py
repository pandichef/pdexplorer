# from ._altair_mapper import circlechart  # type: ignore
from .dataset import current

# scatter = circlechart

# def scatter(anything) -> None:
#     raise NotImplementedError(
#         "Stata's scatter command isn't implemeted.  Try circlechart or pointchart instead"
#     )


def histogram(varlist, *args, **kwargs):
    import seaborn as sns

    sns.set_theme()  # set global theme

    import matplotlib.pyplot as plt

    split = varlist.split(" ")
    assert len(split) == 1, "Histplot takes exactly one variable name"

    chart = sns.histplot(data=current.df, x=current.df[split[0]], *args, **kwargs)
    chart.set_xlabel(current.metadata["variable_labels"].get(split[0], split[0]))
    # chart.set_ylabel(current.metadata["variable_labels"].get(split[1], split[1]))

    plt.show()


# def   atter(varlist):
#     import matplotlib.pyplot as plt

#     split = varlist.split(" ")
#     assert len(split) == 2, "Scatter takes exactly two variable names"

#     plt.scatter(current.df[split[0]], current.df[split[1]])
#     plt.show()
