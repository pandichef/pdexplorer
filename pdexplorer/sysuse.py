from .webuse import webuse


def sysuse(*args, **kwargs):
    webuse(*args, **kwargs, use_local=True)
