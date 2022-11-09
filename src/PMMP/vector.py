from typing import List

from PMMP import Complex

class Point:
    def __init__(self, *args):
        self.coords: list = list(args)

    def __getitem__(self, item):
        return self.coords[item]

    def __setitem__(self, key: int, value):
        self.coords[key] = value

    def __add__(self, other):
        return Point(*[self[i] + other[i] for i in range(len(self))])

    def __sub__(self, other):
        return Point(*[self[i] - other[i] for i in range(len(self))])

    def __len__(self):
        return len(self.coords)

    def __str__(self):
        return "(" + ", ".join([str(i) for i in self.coords]) + ")"

    def __repr__(self):
        return "Point" + str(self)

    def __eq__(self, other):
        return self.coords == other.coords

    def __hash__(self):
        return hash(tuple(self.coords))

    def __copy__(self):
        return Point(*self.coords)

    def __deepcopy__(self, memodict={}):
        return Point(*self.coords)

    def __iter__(self):
        return iter(self.coords)

    def __contains__(self, item):
        return item in self.coords

class TwoDimensionalPoint(Point):
    def __init__(self, x, y):
        super().__init__(x, y)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class ThreeDimensionalPoint(Point):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"


class Matrix:
    def __init__(self, arr: List[List[float]]):
        self.arr = arr
        for i in self.arr:
            if len(i) != len(self.arr[0]):
                raise ValueError("All rows must be the same length")

    def dimensions(self):
        return len(self.arr), len(self.arr[0])

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.dimensions()[1] != other.dimensions()[0]:
                raise ValueError("The number of columns in the first matrix must equal the number of rows in the "
                                 "second matrix")
            else:
                return Matrix([[sum([self.arr[i][k] * other.arr[k][j] for k in range(len(self.arr[i]))]) for j in range(
                    len(other.arr[0]))] for i in range(len(self.arr))])
        elif isinstance(other, Point):
            if self.dimensions()[1] != len(other):
                raise ValueError("The number of columns in the matrix must equal the number of rows in the point")
            else:
                return Point(*[sum([self.arr[i][k] * other[k] for k in range(len(self.arr[i]))]) for i in range(len(self.arr))])
        elif isinstance(other, (int, float, Complex)):
            return Matrix([[i * other for i in j] for j in self.arr])

    def det(self):
        if self.dimensions()[0] != self.dimensions()[1]:
            raise ValueError("The matrix must be square")
        else:
            if len(self.arr) == 1:
                return self.arr[0][0]
            else:
                return sum([(-1) ** i * self.arr[0][i] * Matrix([j[:i] + j[i + 1:] for j in self.arr[1:]]).det() for i in range(len(self.arr[0]))])

    def __rmul__(self, other):
        return self * other

    def __repr__(self):  # TODO: Make this look better
        return f"Matrix({self.arr})"
