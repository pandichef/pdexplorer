> "...succinctness is power... we take the trouble to develop high-level languages...
> so that we can say (and more importantly, think) in 10 lines of a high-level language what would require 1000 lines of machine language... -[Paul Graham, Succinctness is Power](http://www.paulgraham.com/power.html)

## Installation

`pdexplorer` is available on [PyPI](https://pypi.org/project/pdexplorer/). Run `pip` to install:

```
pip install pdexplorer
```

Then import the `pdexplorer` commands with

```python
from pdexplorer import *
```

## pdexplorer

**pdexplorer** is a Stata emulator for Python/pandas. In contrast to raw Python/pandas, Stata syntax achieves succinctness by:

- Using spaces and commas rather than parentheses, brackets, curly braces, and quotes (where possible)
- Specifying a set of concise commands on the "current" dataset rather than cluttering the namespace with multiple datasets
- Being verbose by default i.e., displaying output that represents the results of the command
- Having sensible defaults that cover the majority of use cases and demonstrate common usage
- Allowing for namespace abbreviations for both commands and variable names
- Employing two types of column names: Variable name are concise and used for programming. Variable labels are verbose
  and used for presentation.
- Packages are imported lazily e.g., `import torch` is loaded only when it's first used by a command. This ensures that
  `from pdexplorer import *` runs quickly.

## Examples

### Load Stata dataset and perform exploratory data analysis

```python
webuse('auto')
browse()
```

See https://www.stata.com/manuals/dwebuse.pdf

### Summarize Data by Subgroups

```python
webuse('auto')
with by('foreign'):
    summarize('mpg weight')
```

See https://www.stata.com/manuals/rsummarize.pdf

### Ordinary Least Squares (OLS) Regression

```python
webuse('auto')
regress('mpg weight foreign')
ereturnlist()
```

## Return Values

In the last example, note the use of `ereturnlist()`, corresponding to the Stata command [`ereturn list`](https://www.stata.com/manuals/pereturn.pdf). Additionally, a Python object may also be available as the command's return value. For example,

```python
webuse('auto')
results = regress('mpg weight foreign')
```

Here, `results` is a [RegressionResultsWrapper](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html) object from the [statsmodels](https://www.statsmodels.org/) package.

Similarly,

```python
results = regress('mpg weight foreign', library='scikit-learn')
```

Now, `results` is a [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) object from the [scikit-learn](https://scikit-learn.org/) package.

Finally,

```python
results = regress('mpg weight foreign', library='pytorch')
```

Here, `results` is a [torch.nn.Linear](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html) object from the [PyTorch](https://pytorch.org/) package.

## My Story

I used Stata for 7 years for both data exploration and programming. After that, I used Python/pandas for 3 years and
found that pandas is just too verbose and "explicit" for rapid data exploration. So I started working on this project
on September 3, 2023.

## Why not use Stata instead of pandas?

Stata is great, but Python/pandas is free and easier to integrate with other applications. For example, you can
build a web server in Python, but not Stata; You can run Python in AWS SageMmaker, but not Stata.

Additionally, even for devout Stata users, there is utility in being able to run Stata commands through a Python stack for
comparison purposes.

## How `pdexplorer` fulfills the [Zen of Python](https://peps.python.org/pep-0020/) (relative to pandas)

| YES                                                                   | NO                                                        |
| --------------------------------------------------------------------- | --------------------------------------------------------- |
| Beautiful is better than ugly.                                        | Explicit is better than implicit.                         |
| Simple is better than complex.                                        | In the face of ambiguity, refuse the temptation to guess. |
| Flat is better than nested.                                           |
| Readability counts.                                                   |
| Although practicality beats purity.                                   |
| There should be one-- and preferably only one --obvious way to do it. |
| Now is better than never.                                             |

## How `pdexplorer` differs from Stata

- Commands are implemented as Python functions and hence require at least one set of parentheses
- `pdexplorer` uses Python libraries under the hood. (The result of a command reflects the output of those libraries. See above.)
- There is no support for [mata](https://www.stata.com/features/overview/introduction-to-mata/). Under the hood,
  `pdexplorer` is just the Python data stack.
- The API for producing charts is based on [Altair](https://altair-viz.github.io/), not Stata.

## Syntax summary

With few exceptions, the basic Stata language syntax (as documented [here](https://www.stata.com/manuals/u11.pdf)) is

```stata
[by varlist:] command [varlist] [=exp] [if exp] [in range] [weight] [, options]
```

where square brackets distinguish optional qualifiers and options from required ones. In this diagram,
varlist denotes a list of variable names, command denotes a Stata command, exp denotes an algebraic
expression, range denotes an observation range, weight denotes a weighting expression, and options
denotes a list of options.

The `by varlist:` prefix causes Stata to repeat a command for each subset of the data for which the
values of the variables in varlist are equal. When prefixed with by varlist:, the result of the command
will be the same as if you had formed separate datasets for each group of observations, saved them,
and then gave the command on each dataset separately. The data must already be sorted by varlist,
although by has a sort option.

In pdexplorer, this gets translated to

```python
with by('varlist'):
    command("[varlist] [=exp] [if exp] [in range] [weight] [, options]", *args, **kwargs)
```

where `*args`, and `**kwargs` represent additional arguments that are available in a `pdexplorer` command but
not in the equivalent Stata command.

Sometimes, Stata commands are two words. In such cases, the `pdexplorer` command is a concatenation of the two words. For example,

```stata
label data "label"
```

becomes

```python
labeldata("label")
```

## Module Dependencies

| File location        | Description                                                                        | Dependencies     |
| -------------------- | ---------------------------------------------------------------------------------- | ---------------- |
| `/*.py`              | commands that are native to Stata related to data wrangling or statistics          | `pandas`         |
| `/_altair_mapper.py` | commands that are native to Altair for charting                                    | `altair`         |
| `shortcuts/*.py`     | shortcut commands related to data wrangling, statistics, or charting               | all of the above |
| `finance/*.py`       | commands that are specific to financial applications                               | all of the above |
| `ml/*.py`            | commands that use machine learning techniques (and are outside the scope of Stata) | `scikit-learn`   |
| `nn/*.py`            | commands that use neutral networks (primarily built using PyTorch)                 | `PyTorch`        |
| `data/*.py`          | python scripts that collect data from various sources                              | Data suppliers   |
| `experimental/*.py`  | commands that are current under development and not yet stable                     | N/A              |

## Command Dependencies

| `pdexplorer` command | package dependency                                                                                                                                                         |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cf                   | [ydata-profiling](https://github.com/ydataai/ydata-profiling) or [sweetviz](https://github.com/fbdesignpro/sweetviz)                                                       |
| browse               | [dtale](https://github.com/man-group/dtale)                                                                                                                                |
| regress              | [statsmodels](https://github.com/statsmodels/statsmodels) or [scikit-learn](https://github.com/scikit-learn/scikit-learn) or [PyTorch](https://github.com/pytorch/pytorch) |

## Charts

`pdexplorer` departs somewhat from Stata in producing charts. Rather than emulating Stata's chart syntax,
`pdexplorer` uses [Altair](https://altair-viz.github.io/) with some syntactic sugar.
Take the example ["Simple Scatter Plot with Tooltips"](https://altair-viz.github.io/gallery/scatter_tooltips.html):

```python
import webbrowser
import altair as alt
from vega_datasets import data
source = data.cars()
chart = alt.Chart(source).mark_circle(size=60).encode(
    x="Horsepower",
    y="Miles_per_Gallon",
    color='Origin',
    tooltip=["Name", "Origin", "Horsepower", "Miles_per_Gallon"],
)
chart.save('mychart.html')
webbrowser.open('mychart.html')
```

In `pdexplorer`, this becomes:

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart("miles_per_gallon horsepower, \
    color(origin) tooltip(name origin horsepower miles_per_gallon)",
    size=60,
)
```

In other words, `pdexplorer` supports a `varlist` parameter for `y`/`x` encodings. Additional encodings are specified via the
Stata options syntax.

In the above example, `circlechart` automatically displays the chart in a web browser. However, sometimes it's necessary to add features to the `alt.Chart` Altair object. To use the `alt.Chart` object, we can use `circlechart_` instead of `circlechart`. For example,

```python
import webbrowser
from pdexplorer import *
webuse("cars", "vega")
altair_chart_object = circlechart_(
    "miles_per_gallon horsepower, color(origin) \
    tooltip(name origin horsepower miles_per_gallon)",
    size=60,
)
altair_chart_object.configure_legend(
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=10,
    cornerRadius=10,
    orient='top-right'
) # See https://altair-viz.github.io/user_guide/configuration.html#legend-configuration
altair_chart_object.save('mychart.html')
webbrowser.open('mychart.html')
```

Instead of saving the chart, explicitly, we can also write

```python
altair_chart_object()
```

The `()` at the end tells Altair to open the chart in a web browser. This method is not available in `alt.Charts` itself,
but we monkey patched this into the class for convenience.

Similarly, the following two statements are identical,

```python
circlechart_("miles_per_gallon horsepower")() # the object-oriented style
circlechart("miles_per_gallon horsepower") # the imperative style
```

In this example, `circlechart_` itself simply returns a `alt.Chart` object and `()` indicates that the chart should be displayed in
a web browser.

Since we can access the `alt.Chart` object, we can also specify encodings explicitly using Altair's `encode` method e.g.,

```python
from pdexplorer import *
webuse("cars", "vega") # note that names are forced to be lower case by default
circlechart_(size=60).encode(
    x="horsepower",
    y="miles_per_gallon",
    color="origin",
    tooltip=["name", "origin", "horsepower", "miles_per_gallon"],
)()  # () indicates that the chart is complete and should be opened in a web browser
```

<!-- `pdexplorer` charts also support a `varlist` parameter with `y`/`x` encodings and additional encodings via options e.g., the previous block can be written as

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart(
    "miles_per_gallon horsepower, color(origin) \
    tooltip(name origin horsepower miles_per_gallon)",
    size=60,
)
```

Note here that there is no underscore after `circlechart` and there is no `()`. `circlechart()` imperatively displays a chart in the
a web browser. In contrast, `circlechart_` returns Altair's `alt.Chart` object.

Here, `pdexplorer` uses variable labels for the y- and x- axes.

Also, note that `encode()` is optional here. So, for a quick scatterplot, we can write

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart("miles_per_gallon horsepower")()
``` -->

Since `pdexplorer` charts are just [`alt.Chart`](https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html) objects,
[Layered and Multi-View Charts](https://altair-viz.github.io/user_guide/compound_charts.html) are also supported e.g.,

```python
from pdexplorer import *
webuse("cars", "vega")
chartA = circlechart_("miles_per_gallon weight_in_lbs")
chartB = circlechart_("horsepower weight_in_lbs")
(chartA & chartB)() # Vertically concatenate chartA and chartB
```

Finally, `pdexplorer` also offers syntactic sugar for charting multiple `x`/`y` variables. More specifically, the previous block can be
written as

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart("miles_per_gallon horsepower weight_in_lbs", stacked=True)
```

Note that Stata's `varlist` interpretation is used here by default i.e., `var1 var2 var3` is assumed to represent
`yvar1 yvar2 xvar`. We can change this interpretation with the optional argument `yX`.

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart("miles_per_gallon horsepower weight_in_lbs", yX=True, stacked=True)
```

Now `var1 var2 var3` is assumed to represent `yvar xvar1 xvar2` as it would be for the `regress` command.

The Stata default is to layer all variables onto a single chart. The `stacked=True` option allows the graphs to be shown on
separate grids. If `stacked=False`, the charts are all shown on the same grid i.e.,

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart("miles_per_gallon horsepower weight_in_lbs") # stacked=False is the default option
```

Note that `pdexplorer` uses Altair's [`transform_fold`](https://altair-viz.github.io/user_guide/transform/fold.html#user-guide-fold-transform) method under the hood. For further customization, the Altair methods can be used explicitly e.g.,

```python
import altair as alt
from pdexplorer import *
webuse("cars", "vega")
circlechart_().transform_fold(
    ["Miles_per_Gallon", "Horsepower"] # Note that circlechart_ variable labels are accessible
).encode(
    y="value:Q", x=alt.X("weight_in_lbs", title="Weight_in_lbs"), color="key:N"
)()
```

<!-- In this example, `transform_calculate_variable_labels` is monkey patched into `alt.Chart` to enable access to variable labels in the
`transform_fold` method.  -->

`alt.Chart.transform_fold` is Altair's version of `pandas.melt`. So another option is to first reshape the data using
pandas and then use Altair for charting.

```python
import altair as alt
from pdexplorer import *
webuse("cars", "vega")
melt("miles_per_gallon horsepower,  keep(weight_in_lbs)")
alt.Chart(current.df_labeled).mark_circle().encode(
    y="value:Q", x='Weight_in_lbs', color="variable:N"
)()
```

Note that the [Altair documentation](https://altair-viz.github.io/user_guide/transform/index.html) suggests the latter approach
in most cases where a data transformation is required.

## Abbreviations

As mentioned ealier, Stata supports name abbreviations for both variable names as well as command names. In `pdexplorer`, all the following regression statements are equivalent:

```python
from pdexplorer import *
webuse("auto")
reg('price mpg weight')
regr('price mpg weight')
regre('price mpg weight')
regres('price mpg weight')
regress('price mpg weight')
reg('pr mpg wei')
```

Similarly, for charting,

```python
from pdexplorer import *
webuse("cars", "vega")
circle("miles_per_gallon horsepower")()
circlec("miles_per_gallon horsepower")()
circlech("miles_per_gallon horsepower")()
circlecha("miles_per_gallon horsepower")()
circlechar("miles_per_gallon horsepower")()
circlechart("miles_per_gallon horsepower")()
circle("miles horse")()
```

## References

- https://aeturrell.github.io/coding-for-economists/coming-from-stata.html
- https://www.stata.com/manuals13/u27.pdf
- https://www.stata.com/manuals13/u11.pdf
