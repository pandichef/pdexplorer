from ._dataset import current, Dataset


def clear(commandargs=None):
    if commandargs == "all":
        current.clearall()
    elif not commandargs:
        current.clear()
    else:
        raise Exception("Command argument not valid")
