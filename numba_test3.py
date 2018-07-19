import numba
print(numba.__version__)


def bubblesort(X):
    N = len(X)
    for end in range(N, 1, -1):
        for i in range(end - 1):
            cur = X[i]
            if cur > X[i + 1]:
                tmp = X[i]
                X[i] = X[i + 1]
                X[i + 1] = tmp


import numpy as np

original = np.arange(0.0, 10.0, 0.01, dtype='f4')
shuffled = original.copy()
np.random.shuffle(shuffled)
sorted = shuffled.copy()
bubblesort(sorted)
print(np.array_equal(sorted, original))


@numba.jit("void(f4[:])")
def bubblesort_jit(X):
    N = len(X)
    for end in range(N, 1, -1):
        for i in range(end - 1):
            cur = X[i]
            if cur > X[i + 1]:
                tmp = X[i]
                X[i] = X[i + 1]
                X[i + 1] = tmp


sorted[:] = shuffled[:] # reset to shuffled before sorting
bubblesort_jit(sorted)
print(np.array_equal(sorted, original))
