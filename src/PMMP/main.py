# -*- coding: utf-8 -*-

"""
PMMP.main
~~~~~~~~~

This module provides useful classes for functions and numbers and
polynomials etc.
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
    >>> from PMMP import main as PMMP
    >>> func = NumFunc(lambda x: x*2)
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
    def __init__(self, *args):
        self.contents = {i: coeff for i, coeff in enumerate(args)}

    @property
    def f(self):
        return lambda n: sum([coeff * n ** i for i, coeff in enumerate(list(self.contents.values()))])

    def __call__(self, n):
        return self.f(n)

    def __str__(self):
        return str(self.contents)

    def __add__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented
        _temp = copy.copy(self)
        if len(_temp.contents) < len(other.contents):
            for i in range(max(_temp.contents.keys()) + 1, len(other.contents.keys())):
                _temp.contents[i] = 0
            print(_temp)
            return Polynomial({i: _temp.contents[i] + other.contents[i] for i in _temp.contents.keys()})
        return other + self

    def __neg__(self):
        _temp = copy.copy(self)

        _temp.contents = {t[0]: -t[1] for t in zip(self.contents.keys(), self.contents.values())}
        return _temp

    def __sub__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented
        _temp = copy.copy(self)
        if len(_temp.contents) <= len(other.contents):
            for i in range(max(_temp.contents.keys()) + 1, len(other.contents.keys())):
                _temp.contents[i] = 0
            print(_temp)
            return Polynomial({i: _temp.contents[i] - other.contents[i] for i in _temp.contents.keys()})
        return -(other - self)


class Complex:
    def __init__(self, a: Any, b: Any = 0):

        self.a = a
        self.b = b

    def __round__(self, n=None):

        return Complex(round(self.a, n), round(self.b, n))


    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self.a + other.a, self.b + other.b)
        return self + Complex(other)

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return Complex(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex(self.a * other.a - self.b * other.b, self.a * other.b + self.b * other.a)
        return Complex(other) * self

    def __rmul__(self, other):
        return self * other

    def __abs__(self):
        return (self.a ** 2 + self.b ** 2) ** (1 / 2)

    def conj(self):
        return Complex(self.a, -self.b)

    def __truediv__(self, other):
        if isinstance(other, Complex):
            return self * other.conj() * (1 / abs(other))
        return self * (1 / other)

    def __rtruediv__(self, other):
        if not isinstance(other, Complex):
            return Complex(other) / self
        return other / self

    def ln(self):
        return Complex(math.log(abs(self)), math.atan2(self.b, self.a))

    def exp(self):
        return math.exp(self.a) * Complex(math.cos(self.b), math.sin(self.b))

    def __pow__(self, power, modulo=None):
        if modulo is not None:
            logging.log(logging.INFO, 'Power mod is not yet added')
        if isinstance(power, Complex):
            return (self.ln()*power).exp()

        return self ** Complex(power)

    def __rpow__(self, other):
        return Complex(other) ** self

    def __str__(self):
        return '%s + %si' % (self.a, self.b)







