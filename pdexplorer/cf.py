from .profile import profile


def cf(varlist, using):
    profile(varlist=varlist, compare_to=using)
