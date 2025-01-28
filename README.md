<!-- > "...succinctness is power... we take the trouble to develop high-level languages...
> so that we can say (and more importantly, think) in 10 lines of a high-level language what would require 1000 lines of machine language... -[Paul Graham, Succinctness is Power](http://www.paulgraham.com/power.html) -->

**pdexplorer** is a Stata emulator for Python/pandas.

## Installation

`pdexplorer` is available on [PyPI](https://pypi.org/project/pdexplorer/). Run `pip` to install:

```
pip install pdexplorer
```

## Usage

`pdexplorer` can be run in three modes:

1\. Stata-like Emulation

```python
from pdexplorer import *
```

This import adds Stata-like commands into the Python namespace. For example,

```python
webuse('auto')
reg('mpg price')
```

2\. Pure Stata Emulation

```python
from pdexplorer import do
do() # Launches a Stata emulator that can run normal Stata commands
```

Now you can run regular Stata commands e.g.,

```stata
webuse auto
reg mpg price
```

`do()` also supports running the contents of do-file e.g.,

```python
do('working.do')
```

Under the hoods, the Stata emulator translates pure Stata commands into their Pythonic equivalents.
For example, `reg mpg price` becomes `reg('mpg price')`.

3\. Inline Stata  
For example,

```python
from pdexplorer import do, current
do(inline="""
webuse auto
reg mpg price
""") # Launches a Stata emulator that can run normal Stata commands
print(current.df) # access DataFrame object in Python
```

The rest of this documentation shows examples using Stata-like emulation, but these commands can all be run using pure Stata emulation as well.

## How `pdexplorer` differs from Stata

<!-- - Commands are implemented as Python functions and hence require at least one set of parentheses -->

- `pdexplorer` uses Python libraries under the hood. (The result of a command reflects the output of those libraries and may differ slightly from equivalent Stata output.)
- There is no support for [mata](https://www.stata.com/features/overview/introduction-to-mata/). Under the hood,
  `pdexplorer` is just the Python data stack.

<!-- - The API for producing charts is based on [Altair](https://altair-viz.github.io/), not Stata.
- `pdexplorer` adds commands for machine learning (using sklearn, PyTorch, and huggingface) -->

## Philosophy

Stata is great for its conciseness and readability. But Python/pandas is free and easier to integrate with other applications. For example, you can build a web server in Python, but not Stata; You can run Python in AWS SageMmaker, but not Stata.

`pdexplorer` enables Stata to be easily integrated into the Python ecosystem.

<!-- Additionally, even for devout Stata users, there is utility in being able to run Stata commands through a Python stack for
comparison purposes. -->

In contrast to raw Python/pandas, Stata syntax achieves succinctness by:

- Using spaces and commas rather than parentheses, brackets, curly braces, and quotes (where possible)
- Specifying a set of concise commands on the "current" dataset rather than cluttering the namespace with multiple datasets
- Being verbose by default i.e., displaying output that represents the results of the command
- Having sensible defaults that cover the majority of use cases and demonstrate common usage
- Allowing for namespace abbreviations for both commands and variable names
- Employing two types of column names: Variable name are concise and used for programming. Variable labels are verbose
  and used for presentation.
- Packages are imported lazily e.g., `import statsmodels` is loaded only when it's first used by a command. This ensures that
  `from pdexplorer import *` runs quickly.

## Examples

### Load Stata dataset and perform exploratory data analysis

```python
webuse('auto')
li() # List the contents of the data
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

<!-- Similarly,

```python
results = regress('mpg weight foreign', library='scikit-learn')
```

Now, `results` is a [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) object from the [scikit-learn](https://scikit-learn.org/) package.

Finally,

```python
results = regress('mpg weight foreign', library='pytorch')
```

Here, `results` is a [torch.nn.Linear](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html) object from the [PyTorch](https://pytorch.org/) package. -->

<!-- ## My Story

I used Stata for 7 years for both data exploration and programming. After that, I used Python/pandas for 3 years and
found that pandas is just too verbose and "explicit" for rapid data exploration. So I started working on this project
on September 3, 2023. -->

<!-- ## How `pdexplorer` fulfills the [Zen of Python](https://peps.python.org/pep-0020/) (relative to pandas)

| YES                                                                   | NO                                                        |
| --------------------------------------------------------------------- | --------------------------------------------------------- |
| Beautiful is better than ugly.                                        | Explicit is better than implicit.                         |
| Simple is better than complex.                                        | In the face of ambiguity, refuse the temptation to guess. |
| Flat is better than nested.                                           |
| Readability counts.                                                   |
| Although practicality beats purity.                                   |
| There should be one-- and preferably only one --obvious way to do it. |
| Now is better than never.                                             | -->

## Syntax summary

With few exceptions, the basic Stata language syntax (as documented [here](https://www.stata.com/manuals/u11.pdf)) is

```stata
[by varlist:] command [subcommand] [varlist] [=exp] [if exp] [in range] [weight] [, options]
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
    command("[subcommand] [varlist] [=exp] [if exp] [in range] [weight] [, options]", *args, **kwargs)
```

where `*args`, and `**kwargs` represent additional arguments that might available in a `pdexplorer` command but
not in the equivalent Stata command. (This is rarely used.)

Sometimes, Stata commands are two words. In such cases, the `pdexplorer` command is a concatenation of the two words. For example,

```stata
label data "label"
```

becomes

```python
labeldata("label")
```

<!--
## Module Dependencies

| File location        | Description                                                                        | Dependencies     |
| -------------------- | ---------------------------------------------------------------------------------- | ---------------- |
| `/*.py`              | commands that are native to Stata related to data wrangling or statistics          | `statsmodels`    |
| `/_altair_mapper.py` | commands that are native to Altair for charting                                    | `altair`         |
| `shortcuts/*.py`     | shortcut commands related to data wrangling, statistics, or charting               | all of the above |
| `finance/*.py`       | commands that are specific to financial applications                               | all of the above |
| `ml/*.py`            | commands that use machine learning techniques (and are outside the scope of Stata) | `scikit-learn`   |
| `nn/*.py`            | commands that use neutral networks (primarily built using PyTorch)                 | `PyTorch`        |
| `data/*.py`          | python scripts that collect data from various sources                              | Data suppliers   |
| `not_in_stata/`      | Random stuff that doesn't exist in Stata                                           | N/A              |
 -->

## Command Dependencies

| `pdexplorer` command | package dependency                                                                                                   |
| -------------------- | -------------------------------------------------------------------------------------------------------------------- |
| cf                   | [ydata-profiling](https://github.com/ydataai/ydata-profiling) or [sweetviz](https://github.com/fbdesignpro/sweetviz) |
| browse               | [xlwings](https://github.com/xlwings/xlwings)                                                                        |
| regress              | [statsmodels](https://github.com/statsmodels/statsmodels)                                                            |

<!-- | regress              | [statsmodels](https://github.com/statsmodels/statsmodels) or [scikit-learn](https://github.com/scikit-learn/scikit-learn) or [PyTorch](https://github.com/pytorch/pytorch) | -->

## Python-In-Excel Support

`pdexplorer` can be used with Excel's new [Python-in-Excel](https://support.microsoft.com/en-us/office/introduction-to-python-in-excel-55643c2e-ff56-4168-b1ce-9428c8308545) feature.

Usage:

```
insert_pdexplorer my_excel_sheet.xlsm
```

This script inserts (or overrides) a worksheet called `_pdexplorer` into `my_excel_sheet.xlsm` which contains the core modules of `pdexplorer`.

## References

- https://aeturrell.github.io/coding-for-economists/coming-from-stata.html
- https://www.stata.com/manuals13/u27.pdf
- https://www.stata.com/manuals13/u11.pdf
