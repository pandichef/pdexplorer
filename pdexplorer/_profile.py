# "profile" isn't a stata command
# these commands are used for the "cf" command
import os
from ._dataset import current
import webbrowser
import tempfile
from .use import _use
from .keep import _keep
from ._search import search_iterable


def sweetviz_profile(varlist=None, compare_to=None):
    import sweetviz as sv

    if varlist:
        columns_to_keep = search_iterable(current.df.columns, varlist)
    else:
        columns_to_keep = list(current.df.columns)

    if compare_to is not None:
        # https://www.stata.com/manuals/dcf.pdf
        master_df = _keep(current.df, columns_to_keep)
        using_df = _keep(_use(compare_to)[0], columns_to_keep)
        report = sv.compare(master_df, using_df)
    else:
        report = sv.analyze(current.df)
    report.show_html()


def ydata_profile(varlist=None, compare_to=None):
    # This primarily used for the cf command since dtale doesn't apparently
    # support comparisons directly
    # Note: this isn't a Stata command, but it should have been
    from ydata_profiling import ProfileReport

    if varlist:
        columns_to_keep = search_iterable(current.df.columns, varlist)
    else:
        columns_to_keep = list(current.df.columns)

    if compare_to is not None:
        # https://ydata-profiling.ydata.ai/docs/master/pages/use_cases/comparing_datasets.html
        # https://www.stata.com/manuals/dcf.pdf
        # using_df = _use(compare_to)[0]
        master_df = _keep(current.df, columns_to_keep)
        using_df = _keep(_use(compare_to)[0], columns_to_keep)
        master_report = ProfileReport(master_df, title="master")
        using_report = ProfileReport(using_df, title="using")
        report = master_report.compare(using_report)
    else:
        # see  https://ydata-profiling.ydata.ai/docs/master/pages/use_cases/metadata.html
        master_df = _keep(current.df, columns_to_keep)
        report = master_df.profile_report(
            title=current.metadata["data_label"].split("\n")[0],
            dataset={"description": current.metadata["data_label"]},
            variables={"descriptions": current.metadata["variable_labels"]},
        )

    temp_dir = tempfile.gettempdir()
    temp_file_name = os.path.join(temp_dir, "tmpqbxcec2k.html")
    report.to_file(temp_file_name)
    webbrowser.open(temp_file_name)
