from ._dataset import current
from ._print import _print


def predict(newvar: str) -> None:
    if current.predict_fnc:
        current.predict_fnc(newvar)
        current.metadata["variable_labels"][newvar] = "Fitted values"
    else:
        _print("last estimates not found")
