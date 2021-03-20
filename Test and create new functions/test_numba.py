from time import time
from math import sqrt
from numba import njit


@njit
def f(n):
    s = 0
    for i in range(n):
        s += sqrt(i)
    return s


start = time()
f(10 ** 9)
end = time()
print(end - start)
