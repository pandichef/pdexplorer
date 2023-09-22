from ._dataset import current


def labelvariable(varname: str, label: str):
    current.metadata["data_label"][varname] = label
