# THIS TURNED OUT NOT TO WORK SO WELL
# ALTAIR GRINDS TO A HALT FOR LARGE N
import webbrowser
import altair as alt
from .._dataset import current
from .._commandarg import parse, parse_options
from .._search import search_iterable

# print("asdfas")
# alt.data_transformers.disable_max_rows()
# alt.data_transformers.enable("vegafusion")

# import vegafusion as vf

# vf.enable()

# monkey patch callable method
def _call(self):
    filename = "tmpqbxcec2k.html"
    self.save(filename)
    from .._webbrowser import webbrowser_open

    webbrowser_open(filename)


def _transform_calculate_variable_labels(self):
    reversed_variable_labels = {
        v: "datum." + k for k, v in current.metadata["variable_labels"].items()
    }
    return alt.Chart.transform_calculate(self, **reversed_variable_labels)


alt.Chart.__call__ = _call  # type: ignore
alt.Chart.transform_calculate_variable_labels = _transform_calculate_variable_labels  # type: ignore
alt.LayerChart.__call__ = _call  # type: ignore
alt.LayerChart.transform_calculate_variable_labels = _transform_calculate_variable_labels  # type: ignore
alt.HConcatChart.__call__ = _call  # type: ignore
alt.HConcatChart.transform_calculate_variable_labels = _transform_calculate_variable_labels  # type: ignore
alt.VConcatChart.__call__ = _call  # type: ignore
alt.VConcatChart.transform_calculate_variable_labels = _transform_calculate_variable_labels  # type: ignore


# def _get_kwargs_list(commandarg, yX=True):
def _get_kwargs_list(commandarg, yX=True, use_labels=True):
    """get encodings as keywords"""
    _ = parse(commandarg)
    non_x_y_encodings = parse_options(_["options"], split_values=True)
    for k, v in non_x_y_encodings.items():
        if len(v) == 1:
            non_x_y_encodings[k] = v[0]

    varlist = search_iterable(current.df.columns, _["anything"])
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
    yX: If True, the "v1 v2 v3" is mapped as "y x1 x2"
    stacked: If False, all charts are layered onto a single grid
    """
    _kwargs_list = (
        _get_kwargs_list(commandarg, yX=yX, use_labels=use_labels) if commandarg else []
    )
    # print(_kwargs_list)
    if len(_kwargs_list) == 0:
        return mark_method(*args, **kwargs)
    if len(_kwargs_list) == 1:
        return mark_method(*args, **kwargs).encode(**_kwargs_list[0])
    else:
        if not stacked:
            # sugar for layered charts in the Stata-like manner
            _ = parse(commandarg)
            layered_encodings = parse_options(_["options"], split_values=True)
            for k, v in layered_encodings.items():
                # Becuase Altair doesn't like lists of length 1
                if len(v) == 1:
                    layered_encodings[k] = v[0]
            if yX:
                xvars = _["anything"].split()
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
                    # .transform_calculate_variable_labels()
                    return (
                        mark_method(*args, **kwargs)
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
                yvars = _["anything"].split()
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
    _chart(mark_method, commandarg, use_labels, *args, **kwargs)()
"""

fnc2 = """def {marktype}chart_(commandarg=None, use_labels=True, calculate_variable_labels=True, *args, **kwargs):
    mark_method = alt.Chart(current.df).mark_{marktype}
    if calculate_variable_labels:
        return _chart(mark_method, commandarg, use_labels, *args, **kwargs).transform_calculate_variable_labels()
    else:
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
    exec(fnc2.format(marktype=marktype))

##################################################################
# Stata-like Sugar Below
# def histogram(varname):
#     barchart().encode(alt.X(varname, bin=True), y="count()")()  # type: ignore


# def scatter(commandarg):
#     circlechart(commandarg)()  # type: ignore
"""
# from ._altair_mapper import (
#     arcchart as arc,  # type: ignore
#     arcchart as arcc,  # type: ignore
#     arcchart as arcch,  # type: ignore
#     arcchart as arccha,  # type: ignore
#     arcchart as arcchar,  # type: ignore
#     arcchart as arcchart,  # type: ignore
#     areachart as area,  # type: ignore
#     areachart as areac,  # type: ignore
#     areachart as areach,  # type: ignore
#     areachart as areacha,  # type: ignore
#     areachart as areachar,  # type: ignore
#     areachart as areachart,  # type: ignore
#     barchart as bar,  # type: ignore
#     barchart as barc,  # type: ignore
#     barchart as barch,  # type: ignore
#     barchart as barcha,  # type: ignore
#     barchart as barchar,  # type: ignore
#     barchart as barchart,  # type: ignore
#     circlechart as circle,  # type: ignore
#     circlechart as circlec,  # type: ignore
#     circlechart as circlech,  # type: ignore
#     circlechart as circlecha,  # type: ignore
#     circlechart as circlechar,  # type: ignore
#     circlechart as circlechart,  # type: ignore
#     geoshapechart as geoshape,  # type: ignore
#     geoshapechart as geoshapec,  # type: ignore
#     geoshapechart as geoshapech,  # type: ignore
#     geoshapechart as geoshapecha,  # type: ignore
#     geoshapechart as geoshapechar,  # type: ignore
#     geoshapechart as geoshapechart,  # type: ignore
#     imagechart as image,  # type: ignore
#     imagechart as imagec,  # type: ignore
#     imagechart as imagech,  # type: ignore
#     imagechart as imagecha,  # type: ignore
#     imagechart as imagechar,  # type: ignore
#     imagechart as imagechart,  # type: ignore
#     linechart as line,  # type: ignore
#     linechart as linec,  # type: ignore
#     linechart as linech,  # type: ignore
#     linechart as linecha,  # type: ignore
#     linechart as linechar,  # type: ignore
#     linechart as linechart,  # type: ignore
#     pointchart as point,  # type: ignore
#     pointchart as pointc,  # type: ignore
#     pointchart as pointch,  # type: ignore
#     pointchart as pointcha,  # type: ignore
#     pointchart as pointchar,  # type: ignore
#     pointchart as pointchart,  # type: ignore
#     rectchart as rect,  # type: ignore
#     rectchart as rectc,  # type: ignore
#     rectchart as rectch,  # type: ignore
#     rectchart as rectcha,  # type: ignore
#     rectchart as rectchar,  # type: ignore
#     rectchart as rectchart,  # type: ignore
#     rulechart as rule,  # type: ignore
#     rulechart as rulec,  # type: ignore
#     rulechart as rulech,  # type: ignore
#     rulechart as rulecha,  # type: ignore
#     rulechart as rulechar,  # type: ignore
#     rulechart as rulechart,  # type: ignore
#     squarechart as square,  # type: ignore
#     squarechart as squarec,  # type: ignore
#     squarechart as squarech,  # type: ignore
#     squarechart as squarecha,  # type: ignore
#     squarechart as squarechar,  # type: ignore
#     squarechart as squarechart,  # type: ignore
#     textchart as text,  # type: ignore
#     textchart as textc,  # type: ignore
#     textchart as textch,  # type: ignore
#     textchart as textcha,  # type: ignore
#     textchart as textchar,  # type: ignore
#     textchart as textchart,  # type: ignore
#     tickchart as tick,  # type: ignore
#     tickchart as tickc,  # type: ignore
#     tickchart as tickch,  # type: ignore
#     tickchart as tickcha,  # type: ignore
#     tickchart as tickchar,  # type: ignore
#     tickchart as tickchart,  # type: ignore
#     trailchart as trail,  # type: ignore
#     trailchart as trailc,  # type: ignore
#     trailchart as trailch,  # type: ignore
#     trailchart as trailcha,  # type: ignore
#     trailchart as trailchar,  # type: ignore
#     trailchart as trailchart,  # type: ignore
#     boxplotchart as boxplot,  # type: ignore
#     boxplotchart as boxplotc,  # type: ignore
#     boxplotchart as boxplotch,  # type: ignore
#     boxplotchart as boxplotcha,  # type: ignore
#     boxplotchart as boxplotchar,  # type: ignore
#     boxplotchart as boxplotchart,  # type: ignore
#     errorbandchart as errorband,  # type: ignore
#     errorbandchart as errorbandc,  # type: ignore
#     errorbandchart as errorbandch,  # type: ignore
#     errorbandchart as errorbandcha,  # type: ignore
#     errorbandchart as errorbandchar,  # type: ignore
#     errorbandchart as errorbandchart,  # type: ignore
#     errorbarchart as errorbar,  # type: ignore
#     errorbarchart as errorbarc,  # type: ignore
#     errorbarchart as errorbarch,  # type: ignore
#     errorbarchart as errorbarcha,  # type: ignore
#     errorbarchart as errorbarchar,  # type: ignore
#     errorbarchart as errorbarchart,  # type: ignore
# )

# from ._altair_mapper import (
#     arcchart_ as arc_,  # type: ignore
#     arcchart_ as arcc_,  # type: ignore
#     arcchart_ as arcch_,  # type: ignore
#     arcchart_ as arccha_,  # type: ignore
#     arcchart_ as arcchar_,  # type: ignore
#     arcchart_ as arcchart_,  # type: ignore
#     areachart_ as area_,  # type: ignore
#     areachart_ as areac_,  # type: ignore
#     areachart_ as areach_,  # type: ignore
#     areachart_ as areacha_,  # type: ignore
#     areachart_ as areachar_,  # type: ignore
#     areachart_ as areachart_,  # type: ignore
#     barchart_ as bar_,  # type: ignore
#     barchart_ as barc_,  # type: ignore
#     barchart_ as barch_,  # type: ignore
#     barchart_ as barcha_,  # type: ignore
#     barchart_ as barchar_,  # type: ignore
#     barchart_ as barchart_,  # type: ignore
#     circlechart_ as circle_,  # type: ignore
#     circlechart_ as circlec_,  # type: ignore
#     circlechart_ as circlech_,  # type: ignore
#     circlechart_ as circlecha_,  # type: ignore
#     circlechart_ as circlechar_,  # type: ignore
#     circlechart_ as circlechart_,  # type: ignore
#     geoshapechart_ as geoshape_,  # type: ignore
#     geoshapechart_ as geoshapec_,  # type: ignore
#     geoshapechart_ as geoshapech_,  # type: ignore
#     geoshapechart_ as geoshapecha_,  # type: ignore
#     geoshapechart_ as geoshapechar_,  # type: ignore
#     geoshapechart_ as geoshapechart_,  # type: ignore
#     imagechart_ as image_,  # type: ignore
#     imagechart_ as imagec_,  # type: ignore
#     imagechart_ as imagech_,  # type: ignore
#     imagechart_ as imagecha_,  # type: ignore
#     imagechart_ as imagechar_,  # type: ignore
#     imagechart_ as imagechart_,  # type: ignore
#     linechart_ as line_,  # type: ignore
#     linechart_ as linec_,  # type: ignore
#     linechart_ as linech_,  # type: ignore
#     linechart_ as linecha_,  # type: ignore
#     linechart_ as linechar_,  # type: ignore
#     linechart_ as linechart_,  # type: ignore
#     pointchart_ as point_,  # type: ignore
#     pointchart_ as pointc_,  # type: ignore
#     pointchart_ as pointch_,  # type: ignore
#     pointchart_ as pointcha_,  # type: ignore
#     pointchart_ as pointchar_,  # type: ignore
#     pointchart_ as pointchart_,  # type: ignore
#     rectchart_ as rect_,  # type: ignore
#     rectchart_ as rectc_,  # type: ignore
#     rectchart_ as rectch_,  # type: ignore
#     rectchart_ as rectcha_,  # type: ignore
#     rectchart_ as rectchar_,  # type: ignore
#     rectchart_ as rectchart_,  # type: ignore
#     rulechart_ as rule_,  # type: ignore
#     rulechart_ as rulec_,  # type: ignore
#     rulechart_ as rulech_,  # type: ignore
#     rulechart_ as rulecha_,  # type: ignore
#     rulechart_ as rulechar_,  # type: ignore
#     rulechart_ as rulechart_,  # type: ignore
#     squarechart_ as square_,  # type: ignore
#     squarechart_ as squarec_,  # type: ignore
#     squarechart_ as squarech_,  # type: ignore
#     squarechart_ as squarecha_,  # type: ignore
#     squarechart_ as squarechar_,  # type: ignore
#     squarechart_ as squarechart_,  # type: ignore
#     textchart_ as text_,  # type: ignore
#     textchart_ as textc_,  # type: ignore
#     textchart_ as textch_,  # type: ignore
#     textchart_ as textcha_,  # type: ignore
#     textchart_ as textchar_,  # type: ignore
#     textchart_ as textchart_,  # type: ignore
#     tickchart_ as tick_,  # type: ignore
#     tickchart_ as tickc_,  # type: ignore
#     tickchart_ as tickch_,  # type: ignore
#     tickchart_ as tickcha_,  # type: ignore
#     tickchart_ as tickchar_,  # type: ignore
#     tickchart_ as tickchart_,  # type: ignore
#     trailchart_ as trail_,  # type: ignore
#     trailchart_ as trailc_,  # type: ignore
#     trailchart_ as trailch_,  # type: ignore
#     trailchart_ as trailcha_,  # type: ignore
#     trailchart_ as trailchar_,  # type: ignore
#     trailchart_ as trailchart_,  # type: ignore
#     boxplotchart_ as boxplot_,  # type: ignore
#     boxplotchart_ as boxplotc_,  # type: ignore
#     boxplotchart_ as boxplotch_,  # type: ignore
#     boxplotchart_ as boxplotcha_,  # type: ignore
#     boxplotchart_ as boxplotchar_,  # type: ignore
#     boxplotchart_ as boxplotchart_,  # type: ignore
#     errorbandchart_ as errorband_,  # type: ignore
#     errorbandchart_ as errorbandc_,  # type: ignore
#     errorbandchart_ as errorbandch_,  # type: ignore
#     errorbandchart_ as errorbandcha_,  # type: ignore
#     errorbandchart_ as errorbandchar_,  # type: ignore
#     errorbandchart_ as errorbandchart_,  # type: ignore
#     errorbarchart_ as errorbar_,  # type: ignore
#     errorbarchart_ as errorbarc_,  # type: ignore
#     errorbarchart_ as errorbarch_,  # type: ignore
#     errorbarchart_ as errorbarcha_,  # type: ignore
#     errorbarchart_ as errorbarchar_,  # type: ignore
#     errorbarchart_ as errorbarchart_,  # type: ignore
# )
"""

