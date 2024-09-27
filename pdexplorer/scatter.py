# from ._altair_mapper import circlechart  # type: ignore
from ._dataset import current
from ._commandarg import parse

# scatter = circlechart

# def scatter(anything) -> None:
#     raise NotImplementedError(
#         "Stata's scatter command isn't implemeted.  Try circlechart or pointchart instead"
#     )


def scatter(commandarg, *args, **kwargs):
    import seaborn as sns

    sns.set_theme()  # set global theme

    import matplotlib.pyplot as plt

    parsed = parse(commandarg)

    split = parsed["anything"].split(" ")
    # print(parsed.get("by"))
    assert len(split) == 2, "Scatter takes exactly two variable names"

    chart = sns.relplot(
        data=current.df,
        x=current.df[split[0]],
        y=current.df[split[1]],
        col=parsed.get("by"),
        *args,
        **kwargs
    )
    # chart.set_xlabel(current.metadata["variable_labels"].get(split[0], split[0]))
    # chart.set_ylabel(current.metadata["variable_labels"].get(split[1], split[1]))
    chart.set_axis_labels(
        current.metadata["variable_labels"].get(split[0], split[0]),
        current.metadata["variable_labels"].get(split[1], split[1]),
    )

    plt.show()


# def scatter(varlist):
#     import matplotlib.pyplot as plt

#     split = varlist.split(" ")
#     assert len(split) == 2, "Scatter takes exactly two variable names"

#     plt.scatter(current.df[split[0]], current.df[split[1]])
#     plt.show()
