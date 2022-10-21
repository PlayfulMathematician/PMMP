from typing import Any
import math
"""
PMMP.numbers
~~~~~~~~~

This module provides useful classes for numbers
"""

class Complex:
    """
    Complex Number
    Basic Usage::
    >>> import PMMP
    >>> print(PMMP.Complex(2, 3) * PMMP.Complex(0, 1))
    -3 + 2i


    """
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
        """

        :return: Conjugate of self
        """
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
        """

        :return: Calculates the natural log of e
        """
        return Complex(math.log(abs(self)), math.atan2(self.b, self.a))

    def exp(self):
        """

        :return: Calculates e to the (self)
        """
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
        """

        :return: String in the form a + bi
        """
        return '%s + %si' % (self.a, self.b)
