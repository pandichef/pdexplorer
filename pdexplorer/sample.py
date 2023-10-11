from ._dataset import current
from ._print import _print


def sample(percentage_or_count, by=None, count=False, random_state=None):
    if count:
        kwargs = {"n": percentage_or_count}
    else:
        kwargs = {"frac": percentage_or_count / 100}
    if random_state is not None:
        kwargs.update({"random_state": random_state})

    if by:
        current.df = (
            current.df.groupby(by)
            .apply(lambda x: x.sample(**kwargs))
            .reset_index(drop=True)
        )
    else:
        current.df = current.df.sample(**kwargs)
    _print(current.df)
