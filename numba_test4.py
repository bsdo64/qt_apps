import timeit

import numpy as np
import numba as nb
from numba import cuda


def f_big(A, k, std_A, std_k, mean_A=10, mean_k=0.2, hh=100):
    return (1 / (std_A * std_k * 2 * np.pi)) * A * (hh / 50) ** k * np.exp(
        -1 * (k - mean_k) ** 2 / (2 * std_k ** 2) - (A - mean_A) ** 2 / (
                    2 * std_A ** 2))


def func():
    outer_sum = 0
    dk = 0.01  # 0.000001
    for k in np.arange(dk, 0.4, dk):
        inner_sum = 0
        for A in np.arange(dk, 20, dk):
            inner_sum += dk * f_big(A, k, 1e-5, 1e-5)
        outer_sum += inner_sum * dk

    return outer_sum


@nb.njit()
def f_big_nb(A, k, std_A, std_k, mean_A=10, mean_k=0.2, hh=100):
    return (1 / (std_A * std_k * 2 * np.pi)) * A * (hh / 50) ** k * np.exp(
        -1 * (k - mean_k) ** 2 / (2 * std_k ** 2) - (A - mean_A) ** 2 / (
                    2 * std_A ** 2))


@nb.njit()
def func_nb():
    outer_sum = 0
    dk = 0.01  # 0.000001
    X = np.arange(dk, 0.4, dk)
    Y = np.arange(dk, 20, dk)
    for i in range(X.shape[0]):
        k = X[i]  # faster to do lookup than iterate over an array directly
        inner_sum = 0
        for j in range(Y.shape[0]):
            A = Y[j]
            inner_sum += dk * f_big_nb(A, k, 1e-5, 1e-5)
        outer_sum += inner_sum * dk

    return outer_sum


@cuda.jit()
def func_cd():
    outer_sum = 0
    dk = 0.01  # 0.000001
    X = np.arange(dk, 0.4, dk)
    Y = np.arange(dk, 20, dk)
    for i in range(X.shape[0]):
        k = X[i]  # faster to do lookup than iterate over an array directly
        inner_sum = 0
        for j in range(Y.shape[0]):
            A = Y[j]
            inner_sum += dk * f_big_nb(A, k, 1e-5, 1e-5)
        outer_sum += inner_sum * dk

    return outer_sum


threadsperblock = 256
blockspergrid = math.ceil(data.shape[0] / threadsperblock)
my_kernel[blockspergrid, threadsperblock](data)


print(timeit.timeit('func()', globals=globals(), number=10))
print(timeit.timeit('func_nb()', globals=globals(), number=10))
print(timeit.timeit('func_cd()', globals=globals(), number=10))
