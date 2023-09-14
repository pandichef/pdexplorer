from .dataset import current


def labeldata(label: str):
    current.metadata["data_label"] = label
