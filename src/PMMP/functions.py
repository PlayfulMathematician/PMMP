# -*- coding: utf-8 -*-

"""
PMMP.functions
~~~~~~~~~

This module provides useful classes for functions
"""
import copy
import math
from typing import Any
import logging
logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(message)s',
                    level=logging.DEBUG)


class NumFunc:
    """ A numerical function

    Provides derivatives of any degree.
    Basic Usage::
    >>> import PMMP
    >>> func = PMMP.NumFunc(lambda x: x*2)
    >>> print(func(2))
    4
    """

    def __init__(self, f):

        self.f = f

    def __call__(self, n):
        return self.f(n)

    def first_derivative(self, accuracy: float = 0.01):
        """
        Calculates the first derivative. Returns :class:`NumFunc` object.
        :param accuracy: The \"dx\" value in the derivative
        """
        return NumFunc(lambda n: (self.f(n + accuracy) - self.f(n)) / accuracy)

    def nth_derivative(self, n: int, accuracy=0.01):
        """
        Calculates the first derivative. Returns :class:`NumFunc` object.
        :param n: The order of the derivative
        :param accuracy: The \"dx\" value in the derivative
        """
        if n < 0:
            return NotImplemented
        if n == 0:
            return self
        if n == 1:
            return self.first_derivative(accuracy=accuracy)
        return self.nth_derivative(n - 1, accuracy=accuracy).first_derivative(accuracy=accuracy)

    def solve(self, accuracy=0.01, iterations=10, guess=1, inf=False):
        """
        Solves using newtons method
        :param inf:
        :param accuracy:
        :param iterations:
        :param guess:
        :return:
        """
        new_guess = guess
        if inf:
            while True:
                a = NumFunc(lambda x: x - self(x) / self.first_derivative(accuracy=accuracy)(x))
                new_guess = a(new_guess)
                yield new_guess

        if iterations == 0:
            return guess

        a = NumFunc(lambda x: x - self(x) / self.first_derivative(accuracy=accuracy)(x))
        return self.solve(accuracy=accuracy, iterations=iterations - 1, guess=a(guess))


class Polynomial(NumFunc):
    """
    A polynomial
    Provides addition, subtraction.
    """
    def __init__(self, *args):
        self.contents = {i: coeff for i, coeff in enumerate(*args)}

    @property
    def f(self):
        """

        :return: The function equal to the polynomial
        """
        return lambda n: sum([coeff * n ** i for i, coeff in enumerate(list(self.contents.values()))])

    def __call__(self, n):
        return self.f(n)

    def __str__(self):
        return str(self.contents)

    def __add__(self, other): # todo
        pass

    def __sub__(self, other): # todo
        pass

    def __neg__(self):
        _temp = copy.copy(self)

        _temp.contents = {t[0]: -t[1] for t in zip(self.contents.keys(), self.contents.values())}
        return _temp








