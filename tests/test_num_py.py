import numpy as np


def test_num_py_functions():
    arr = np.arange(5)
    arr = arr * 10
    print(arr)

    arr_rand = np.random.rand(2, 3, 4)

    zeros = np.zeros((2, 2, 2))

    full = np.full((2, 2, 2), 7)
    ones = np.ones((2, 2, 2))
    arr1 = np.array([[1, 2, 3], [4, 5, 6]])
