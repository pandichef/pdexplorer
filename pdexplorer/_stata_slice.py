def _stata_slice(in_):
    # convert stata slice (e.g., 1/10) to python slice (e.g., 0:10)
    if isinstance(in_, str) and in_.find("/") > -1:  # Stata's slicing syntax
        in_ = in_.replace("/", ":")
        _in_list = in_.split(":")
        in_ = str(int(_in_list[0]) - 1) + ":" + _in_list[1]
        return in_
    else:
        return in_
