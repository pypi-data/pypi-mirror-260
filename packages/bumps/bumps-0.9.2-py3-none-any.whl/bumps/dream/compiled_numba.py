from numba import njit, guvectorize, prange
from . import util
import numpy as np


# args = (len(pop), len(self.low), pop.ctypes,
                            # self.low.ctypes, self.high.ctypes)

# @guvectorize(["void(float64[:], float64[:], float64[:,:])"], target="parallel", nopython=True)
# def vreflect_bounds(low, high, y):
#     minn, maxn = np.expand_dims(low, axis=0), np.expand_dims(high, axis=0)
#     y = pop
#     idx = y < minn
#     y[idx] = 2*minn[idx] - y[idx]
#     idx = y > maxn
#     y[idx] = 2*maxn[idx] - y[idx]

#     # Randomize points which are still out of bounds
#     idx = (y < minn) | (y > maxn)
#     print(idx.shape)
#     y[idx] = minn[idx] + util.rng.rand(sum(idx))*(maxn[idx]-minn[idx])


@njit(cache=True)
def reflect_bounds(low, high, pop):
    """
    Update x so all values lie within bounds

    Returns x for convenience.  E.g., y = bounds.apply(x+0)
    """
    minn, maxn = low, high
    for y in pop:
        # Reflect points which are out of bounds
        idx = y < minn
        y[idx] = 2*minn[idx] - y[idx]
        idx = y > maxn
        y[idx] = 2*maxn[idx] - y[idx]

        # Randomize points which are still out of bounds
        idx = (y < minn) | (y > maxn)
        y[idx] = minn[idx] + util.rng.rand(sum(idx))*(maxn[idx]-minn[idx])


@njit(cache=True)
def clip_bounds(low, high, y):
    minn, maxn = low, high
    idx = y < minn
    y[idx] = minn[idx]
    idx = y > maxn
    y[idx] = maxn[idx]

    return y

@njit(cache=True)
def fold_bounds(low, high, y):
    minn, maxn = low, high

    # Deal with semi-infinite cases using reflection
    idx = (y < minn) & isinf(maxn)
    y[idx] = 2*minn[idx] - y[idx]
    idx = (y > maxn) & isinf(minn)
    y[idx] = 2*maxn[idx] - y[idx]

    # Wrap points which are out of bounds
    idx = y < minn
    y[idx] = maxn[idx] - (minn[idx] - y[idx])
    idx = y > maxn
    y[idx] = minn[idx] + (y[idx] - maxn[idx])

    # Randomize points which are still out of bounds
    idx = (y < minn) | (y > maxn)
    y[idx] = minn[idx] + util.rng.rand(sum(idx))*(maxn[idx]-minn[idx])

    return y

@njit(cache=True)
def random_bounds(low, high, y):
    minn, maxn = low, high

    # Deal with semi-infinite cases using reflection
    idx = (y < minn) & isinf(maxn)
    y[idx] = 2*minn[idx] - y[idx]
    idx = (y > maxn) & isinf(minn)
    y[idx] = 2*maxn[idx] - y[idx]

    # The remainder are selected uniformly from the bounded region
    idx = (y < minn) | (y > maxn)
    y[idx] = minn[idx] + util.rng.rand(sum(idx))*(maxn[idx]-minn[idx])

    return y

@njit(cache=True)
def ignore_bounds(low, high, y):
    return pop