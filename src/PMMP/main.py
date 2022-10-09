import copy


class NumFunc:
    def __init__(self, f):
        self.f = f

    def __call__(self, n):
        return self.f(n)

    def first_derivative(self, accuracy=0.01):
        return NumFunc(lambda n: (self.f(n + accuracy) - self.f(n))/accuracy)

    def nth_derivative(self, n: int, accuracy=0.01):
        if n < 0:
            return NotImplemented
        if n == 0:
            return self
        if n == 1:
            return self.first_derivative(accuracy=accuracy)
        return self.nth_derivative(n-1, accuracy=accuracy).first_derivative(accuracy=accuracy)


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
    def __init__(self, a, b=0):
        self.a = a
        self.b = b

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


