import sys
from timeit import timeit
sys.path.extend(['.', '..'])
from src.PMMP.functions import Polynomial
import src
import numpy as np
import inspect
def test_polynomial():

    # Generate a random polynomial
    p = Polynomial(*np.random.rand(10000))
    q = Polynomial(*np.random.rand(10000))
    # Time Multiplication
    x = 100_000
    print(timeit(lambda: p * q, number=x)/x)

test_polynomial()



