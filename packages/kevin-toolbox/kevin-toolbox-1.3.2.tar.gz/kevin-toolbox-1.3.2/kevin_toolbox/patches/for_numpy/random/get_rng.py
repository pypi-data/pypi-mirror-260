import numpy as np


class DEFAULT_RNG:
    pass


for name in np.random.__all__:
    setattr(DEFAULT_RNG, name, getattr(np.random, name))


def get_rng(seed=None, rng=None, **kwargs):
    if seed is not None:
        rng = np.random.default_rng(seed=seed)
    if rng is not None:
        return rng
    else:
        return DEFAULT_RNG
