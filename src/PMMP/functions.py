# -*- coding: utf-8 -*-

"""
PMMP.functions
~~~~~~~~~

This module provides useful classes for functions
"""
import copy
import math
from typing import Any
from scipy.signal import fftconvolve
import logging

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s - %(message)s", level=logging.DEBUG
)


class NumFunc:
    """
    NumFunc
    -------
    This class is used to represent functions of one variable

    Attributes
    ----------
    f: Function
        The function to represent

    Methods
    -------
    first_derivative(accuracy=0.01)
        Calculates the first derivative. Returns :class:`NumFunc` object.

    nth_derivative(n, accuracy=0.01)
        Calculates the nth derivative. Returns :class:`NumFunc` object.

    solve(accuracy=0.01, iterations=10, guess=1, inf=False)
        Solves the function for x


    """

    def __init__(self, f):

        self.f = f

    def __call__(self, n):
        return self.f(n)

    def first_derivative(self, accuracy: float = 0.01):

        return NumFunc(lambda n: (self.f(n + accuracy) - self.f(n)) / accuracy)

    def nth_derivative(self, n: int, accuracy=0.01):

        if n < 0:
            return NotImplemented
        if n == 0:
            return self
        if n == 1:
            return self.first_derivative(accuracy=accuracy)
        return self.nth_derivative(n - 1, accuracy=accuracy).first_derivative(
            accuracy=accuracy
        )

    def _solve_inf(self, accuracy=0.01, guess=1):
        new_guess = guess
        while True:
            a = NumFunc(
                lambda x: x - self(x) / self.first_derivative(accuracy=accuracy)(x)
            )
            new_guess = a(new_guess)
            yield new_guess

    def solve(self, accuracy=0.01, iterations=10, guess=1, inf=False):

        new_guess = guess
        if inf:
            return self._solve_inf(accuracy=accuracy, guess=guess)

        a = NumFunc(lambda x: x - self(x) / self.first_derivative(accuracy=accuracy)(x))
        return self.solve(accuracy=accuracy, iterations=iterations - 1, guess=a(guess))

    def __add__(self, other):
        return NumFunc(lambda x: self(x) + other(x))

    def __sub__(self, other):
        return NumFunc(lambda x: self(x) - other(x))

    def __truediv__(self, other):
        return NumFunc(lambda x: self(x) / other(x))

    def __mul__(self, other):
        return NumFunc(lambda x: self(x) * other(x))


class Polynomial(NumFunc):
    def __init__(self, *coeff):
        self.coeff = coeff

    @property
    def degree(self):
        return len(self.coeff) - 1

    def __call__(self, n):
        return sum([self.coeff[i] * n ** i for i in range(len(self.coeff))])

    def __mul__(self, other):
        return Polynomial(*fftconvolve(self.coeff, other.coeff))

    def __add__(self, other):
        coeff1 = copy.deepcopy(self.coeff)
        coeff2 = copy.deepcopy(other.coeff)
        if len(coeff1) < len(coeff2):
            # Pad coeff1 with zeros
            coeff1 = coeff1 + [0] * (len(coeff2) - len(coeff1))
        elif len(coeff2) < len(coeff1):
            # Pad coeff2 with zeros
            coeff2 = coeff2 + [0] * (len(coeff1) - len(coeff2))

        return Polynomial(*[coeff1[i] + coeff2[i] for i in range(len(coeff1))])

    def __neg__(self):
        return Polynomial(*[-self.coeff[i] for i in range(len(self.coeff))])

    def __sub__(self, other):
        return self + (-other)

