import webbrowser
import altair as alt
from .dataset import current
from .commandarg import parse_commandarg, parse_options
from .search import search_iterable

# monkey patch callable method
def _call(self):
    self.save("tmpqbxcec2k.html")
    webbrowser.open("tmpqbxcec2k.html")


def _transform_calculate_variable_labels(self):
    reversed_variable_labels = {
        v: "datum." + k for k, v in current.metadata["variable_labels"].items()
    }
    return alt.Chart.transform_calculate(self, **reversed_variable_labels)


alt.Chart.__call__ = _call  # type: ignore
alt.Chart.transform_calculate_variable_labels = _transform_calculate_variable_labels  # type: ignore
alt.LayerChart.__call__ = _call  # type: ignore
alt.HConcatChart.__call__ = _call  # type: ignore
alt.VConcatChart.__call__ = _call  # type: ignore


# def _get_kwargs_list(commandarg, yX=True):
def _get_kwargs_list(commandarg, yX=True, use_labels=True):
    """get encodings as keywords"""
    parsed_commandarg = parse_commandarg(commandarg)
    non_x_y_encodings = parse_options(parsed_commandarg["options"], values_as_list=True)
    for k, v in non_x_y_encodings.items():
        if len(v) == 1:
            non_x_y_encodings[k] = v[0]
    # varlist = parsed_commandarg["anything"].split()

    varlist = search_iterable(current.df.columns, parsed_commandarg["anything"])
    if yX:
        if len(varlist) == 1:
            yvar = varlist[0]
            xvars = list(current.df.columns)
            xvars.remove(yvar)
        else:
            yvar = varlist.pop(0)
            xvars = varlist
        kwargs_list = []
        for xvar in xvars:
            if use_labels:
                this_kwargs = {
                    # "y": current.metadata["variable_labels"][yvar],
                    # "x": current.metadata["variable_labels"][xvar],
                    "y": alt.Y(yvar, title=current.metadata["variable_labels"][yvar]),
                    "x": alt.X(xvar, title=current.metadata["variable_labels"][xvar]),
                }
            else:
                this_kwargs = {"y": yvar, "x": xvar}
            this_kwargs.update(non_x_y_encodings)
            kwargs_list.append(this_kwargs)
        return kwargs_list
    else:
        if len(varlist) == 1:
            xvar = varlist[0]
            yvars = list(current.df.columns)
            yvars.remove(xvar)
        else:
            xvar = varlist.pop()
            yvars = varlist
        kwargs_list = []
        for yvar in yvars:
            # this_kwargs = {"y": yvar, "x": xvar}
            if use_labels:
                this_kwargs = {
                    # "y": current.metadata["variable_labels"][yvar],
                    # "x": current.metadata["variable_labels"][xvar],
                    "y": alt.Y(yvar, title=current.metadata["variable_labels"][yvar]),
                    "x": alt.X(xvar, title=current.metadata["variable_labels"][xvar]),
                }
            else:
                this_kwargs = {"y": yvar, "x": xvar}
            this_kwargs.update(non_x_y_encodings)
            kwargs_list.append(this_kwargs)
        return kwargs_list


def _chart(
    mark_method,
    commandarg=None,
    use_labels=True,
    yX=False,
    stacked=False,
    *args,
    **kwargs
):
    """
    xvars: If True, the "v1 v2 v3" is mapped as "y x1 x2"
    layered: If True, all charts are layered onto a single grid
    """
    _kwargs_list = (
        _get_kwargs_list(commandarg, yX=yX, use_labels=use_labels) if commandarg else []
    )
    # print(_kwargs_list)
    if len(_kwargs_list) == 0:
        return mark_method(*args, **kwargs)
    if len(_kwargs_list) == 1:
        # print("asdfasdfasfd")
        return mark_method(*args, **kwargs).encode(**_kwargs_list[0])
    else:
        if not stacked:
            # sugar for layered charts in the Stata-like manner
            parsed_commandarg = parse_commandarg(commandarg)
            layered_encodings = parse_options(
                parsed_commandarg["options"], values_as_list=True
            )
            for k, v in layered_encodings.items():
                # Becuase Altair doesn't like lists of length 1
                if len(v) == 1:
                    layered_encodings[k] = v[0]
            if yX:
                xvars = parsed_commandarg["anything"].split()
                yvar = xvars.pop(0)
                layered_encodings.update({"color": "key:N"})
                layered_encodings.update({"x": "value:Q"})
                layered_encodings.update(
                    {
                        "y": alt.Y(
                            yvar, title=current.metadata["variable_labels"][yvar]
                        )
                        if use_labels
                        else yvar
                    }
                )
                if use_labels:
                    return (
                        mark_method(*args, **kwargs)
                        .transform_calculate_variable_labels()
                        .encode(**layered_encodings)
                        .transform_fold(
                            list(
                                map(
                                    lambda x: current.metadata["variable_labels"][x],
                                    xvars,
                                )
                            )
                        )
                    )
                else:
                    return (
                        mark_method(*args, **kwargs)
                        .encode(**layered_encodings)
                        .transform_fold(xvars)
                    )
            else:
                yvars = parsed_commandarg["anything"].split()
                xvar = yvars.pop()
                layered_encodings.update({"color": "key:N"})
                layered_encodings.update({"y": "value:Q"})
                layered_encodings.update(
                    {
                        "x": alt.X(
                            xvar, title=current.metadata["variable_labels"][xvar]
                        )
                        if use_labels
                        else xvar
                    }
                )
                # print(layered_encodings)
                # print(yvars)
                if use_labels:
                    return (
                        mark_method(*args, **kwargs)
                        .transform_calculate_variable_labels()
                        .encode(**layered_encodings)
                        .transform_fold(
                            list(
                                map(
                                    lambda x: current.metadata["variable_labels"][x],
                                    yvars,
                                )
                            )
                        )
                    )
                else:
                    return (
                        mark_method(*args, **kwargs)
                        .encode(**layered_encodings)
                        .transform_fold(yvars)
                    )
        else:
            # Stacked version here
            vconcat = mark_method(*args, **kwargs).encode(**_kwargs_list[0])
            for i, _kwargs in enumerate(_kwargs_list):
                if i > 0:
                    vconcat = vconcat & (
                        mark_method(*args, **kwargs).encode(**_kwargs_list[i])
                    )
            return vconcat


marktypes = [  # https://altair-viz.github.io/user_guide/marks/index.html
    "arc",  # https://altair-viz.github.io/user_guide/marks/arc.html#user-guide-arc-marks
    "area",  # https://altair-viz.github.io/user_guide/marks/area.html#user-guide-area-marks
    "bar",  # https://altair-viz.github.io/user_guide/marks/bar.html#user-guide-bar-marks
    "circle",  # https://altair-viz.github.io/user_guide/marks/circle.html#user-guide-circle-marks
    "geoshape",  # https://altair-viz.github.io/user_guide/marks/geoshape.html#user-guide-geoshape-marks
    "image",  # https://altair-viz.github.io/user_guide/marks/image.html#user-guide-image-marks
    "line",  # https://altair-viz.github.io/user_guide/marks/line.html#user-guide-line-marks
    "point",  # https://altair-viz.github.io/user_guide/marks/point.html#user-guide-point-marks
    "rect",  # https://altair-viz.github.io/user_guide/marks/rect.html#user-guide-rect-marks
    "rule",  # https://altair-viz.github.io/user_guide/marks/rule.html#user-guide-rule-marks
    "square",  # https://altair-viz.github.io/user_guide/marks/square.html#user-guide-square-marks
    "text",  # https://altair-viz.github.io/user_guide/marks/text.html#user-guide-text-marks
    "tick",  # https://altair-viz.github.io/user_guide/marks/tick.html#user-guide-tick-marks
    "trail",  # https://altair-viz.github.io/user_guide/marks/trail.html#user-guide-trail-marks
    "boxplot",  # https://altair-viz.github.io/user_guide/marks/boxplot.html#user-guide-boxplot-marks
    "errorband",  # https://altair-viz.github.io/user_guide/marks/errorband.html#user-guide-errorband-marks
    "errorbar",  # https://altair-viz.github.io/user_guide/marks/errorbar.html#user-guide-errorbar-marks
]

fnc = """def {marktype}chart(commandarg=None, use_labels=True, *args, **kwargs):
    mark_method = alt.Chart(current.df).mark_{marktype}
    return _chart(mark_method, commandarg, use_labels, *args, **kwargs)
"""
# fnc = """def {marktype}chart(use_labels=True, *args, **kwargs):
#     if use_labels:
#         mark_method = alt.Chart(current.df_labeled).mark_{marktype}
#     else:
#         mark_method = alt.Chart(current.df).mark_{marktype}
#     return _chart(mark_method, use_labels=use_labels, *args, **kwargs)
# """

for marktype in marktypes:
    exec(fnc.format(marktype=marktype))

##################################################################
# Stata-like Sugar Below
def histogram(varname):
    barchart().encode(alt.X(varname, bin=True), y="count()")()  # type: ignore


def scatter(commandarg):
    circlechart(commandarg)()  # type: ignore
