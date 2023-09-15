from .profile import ydata_profile, sweetviz_profile


def cf(varlist, using, package="ydata_profiler"):
    if package == "ydata_profiler":
        ydata_profile(varlist=varlist, compare_to=using)
    elif package == "sweetviz":
        sweetviz_profile(varlist=varlist, compare_to=using)
    else:
        raise Exception(f"Package {package} not found.")
