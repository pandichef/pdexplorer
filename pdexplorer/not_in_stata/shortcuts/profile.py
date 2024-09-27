def profile(varlist=None, package="ydata_profiler"):
    from .._profile import ydata_profile, sweetviz_profile

    if package == "ydata_profiler":
        ydata_profile(varlist=varlist)
    elif package == "sweetviz":
        sweetviz_profile(varlist=varlist)
    else:
        raise Exception(f"Package {package} not found.")
