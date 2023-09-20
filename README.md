> "...succinctness is power... we take the trouble to develop high-level languages...
> so that we can say (and more importantly, think) in 10 lines of a high-level language what would require 1000 lines of machine language... -[Paul Graham, Succinctness is Power](http://www.paulgraham.com/power.html)

## pdexplorer

**pdexplorer** is a Stata emulator for Python/pandas. In contrast to pandas, Stata syntax achieves succinctness by:

- Using spaces and commas rather than parentheses, brackets, curly braces, and quotes (where possible)
- Specifying a set of concise commands on the "current" dataset rather than cluttering the namespace with multiple datasets
- Being verbose by default i.e., displaying output that represents the results of the command
- Having sensible defaults that cover the majority of use cases and demonstrate common usage
- Allowing for namespace abbreviations for both commands and variable names
- Employing two types of column names: Variable name are concise and used for programming. Variable labels are verbose
  and used for presentation.

## Installation

`pdexplorer` is available on [PyPI](https://pypi.org/project/pdexplorer/). Run `pip` to install:

```
pip install pdexplorer
```

Then import the `pdexplorer` commands with

```python
from pdexplorer import *
```

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

## Dependencies

| `pdexplorer` command | package dependency                                                                                                                                                         |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cf                   | [ydata-profiling](https://github.com/ydataai/ydata-profiling) or [sweetviz](https://github.com/fbdesignpro/sweetviz)                                                       |
| browse               | [dtale](https://github.com/man-group/dtale)                                                                                                                                |
| regress              | [statsmodels](https://github.com/statsmodels/statsmodels) or [scikit-learn](https://github.com/scikit-learn/scikit-learn) or [PyTorch](https://github.com/pytorch/pytorch) |
| scatter              | [seaborn](https://github.com/mwaskom/seaborn)                                                                                                                              |

## Subfolders

`core/`: stata commands for data wrangling  
`plus/`: data wrangling commands that are not in Stata  
`finance/`: financial functions  
`ai/`: Machine Learning and Artificial Intelligence  
`experimental/`: Commands that are no longer actively maintained

## Charts

`pdexplorer` departs somewhat from Stata in producing charts. Rather than emulating Stata's chart syntax,
`pdexplorer` uses [Altair](https://altair-viz.github.io/) with some syntactic sugar.
Take the example ["Simple Scatter Plot with Tooltips"](https://altair-viz.github.io/gallery/scatter_tooltips.html):

```python
import altair as alt
from vega_datasets import data
source = data.cars()
alt.Chart(source).mark_circle(size=60).encode(
    x="Horsepower",
    y="Miles_per_Gallon",
    color='Origin',
    tooltip=["Name", "Origin", "Horsepower", "Miles_per_Gallon"],
)
```

In `pdexplorer`, this becomes:

```python
from pdexplorer import *
webuse("cars", "vega") # note that names are forced to be lower case by default
circlechart(size=60).encode(
    x="horsepower",
    y="miles_per_gallon",
    color='origin',
    tooltip=["name", "origin", "horsepower", "miles_per_gallon"]
)() # () indicates that the chart is complete and should be opened in a web browser
```

The `()` at the end tells Altair to open the chart in a web browser. This method is not available in `alt.Charts` itself,
but we monkey patched this into the class for convenience. In this example, `circlechart()` itself simple returns a `alt.Chart` object.

`pdexplorer` charts also support a `varlist` parameter with `y`/`x` encodings and additional encodings via options e.g., the previous block can be written as

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart(
    "miles_per_gallon horsepower, color(origin) \
    tooltip(name origin horsepower miles_per_gallon)",
    size=60,
)()
```

Here, `pdexplorer` uses variable labels for the y- and x- axes.

Also, note that `encode()` is optional here. So, for a quick scatterplot, we can write

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart("miles_per_gallon horsepower")()
```

Since `pdexplorer` charts are regular [`alt.Chart`](https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html) objects,
[Layered and Multi-View Charts](https://altair-viz.github.io/user_guide/compound_charts.html) are also supported e.g.,

```python
from pdexplorer import *
webuse("cars", "vega")
chartA = circlechart("miles_per_gallon weight_in_lbs")
chartB = circlechart("horsepower weight_in_lbs")
(chartA & chartB)() # Vertically concatenate chartA and chartB
```

Finally, `pdexplorer` also offers syntactic sugar for charting multiple `x`/`y` variables. More specifically, the previous block can be
written as

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart("miles_per_gallon horsepower weight_in_lbs", stacked=True)()
```

Note that the Stata `varlist` interpretation is used here by default i.e., `var1 var2 var3` is assumed to represent
`yvar1 yvar2 xvar`. We can change this interpretation with the optional argument `yX`.

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart("miles_per_gallon horsepower weight_in_lbs", yX=True, stacked=True)()
```

Now `var1 var2 var3` is assumed to represent `yvar xvar1 xvar2` as it would be for the `regress` command.

Moreover, the Stata default is to layer all variables onto a single chart. The `stacked=True` option allows the graphs to be shown on
separate grids. If `stacked=False`, the graphs on all shows on the same grid i.e.,

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart("miles_per_gallon horsepower weight_in_lbs")() # stacked=False is the default option
# TODO: apply variable labels to legend names
```

Note that `pdexplorer` uses Altair's [`transform_fold`](https://altair-viz.github.io/user_guide/transform/fold.html#user-guide-fold-transform) method under the hood. For further customization, the Altair methods can be used explicitly e.g.,

```python
from pdexplorer import *
webuse("cars", "vega")
circlechart().encode(y="value:Q", x="weight_in_lbs", color="key:N").transform_fold(
    ["miles_per_gallon", "horsepower"]
)()
```

## References

- https://aeturrell.github.io/coding-for-economists/coming-from-stata.html
- https://www.stata.com/manuals13/u27.pdf
- https://www.stata.com/manuals13/u11.pdf
