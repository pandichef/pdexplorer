from .._commandarg import parse
from .._dataset import current
from .._search import search_iterable
from .._print import _print

graphviz_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Graphviz Graph</title>
</head>
<body>
    <h1>My Graph</h1>
    <img src="{}" alt="Graph" />
</body>
</html>
"""


def treeclassify(
    commandarg: str, max_depth=None, show_graphviz=False, use_regressor=False
):
    from sklearn import tree

    _ = parse(commandarg, "varlist")
    varlist_as_list = _["varlist"].split()
    yvar = varlist_as_list[0]
    xvars = varlist_as_list[1:]
    # xvars = search_iterable(current.df.columns, " ".join(xvars))
    X = current.df.dropna()[xvars].values
    y = current.df.dropna()[yvar].values
    _DecisionTree = (
        tree.DecisionTreeRegressor if use_regressor else tree.DecisionTreeClassifier
    )
    decision_tree = _DecisionTree(random_state=0, max_depth=max_depth).fit(X, y)

    if show_graphviz:
        import graphviz
        from .._webbrowser import webbrowser_open

        # import subprocess

        dot_data = tree.export_graphviz(
            decision_tree,
            out_file=None,
            feature_names=xvars,
            class_names=list(current.df[yvar].cat.categories),
            filled=True,
            rounded=True,
            special_characters=True,
        )
        graph = graphviz.Source(dot_data)  # type: ignore
        graph.render("graphviz", format="svg")
        print("SVG file saved as 'graphviz.svg'")
        graph_viz_filename = "graphviz.html"
        with open(graph_viz_filename, "w") as f:
            f.write(graphviz_html.format("graphviz.svg"))
        webbrowser_open(graph_viz_filename)
    else:
        _print(tree.export_text(decision_tree, feature_names=xvars))

    return decision_tree
