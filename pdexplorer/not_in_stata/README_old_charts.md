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
circle("miles_per_gallon horsepower")
circlec("miles_per_gallon horsepower")
circlech("miles_per_gallon horsepower")
circlecha("miles_per_gallon horsepower")
circlechar("miles_per_gallon horsepower")
circlechart("miles_per_gallon horsepower")
circle("miles horse")
```
