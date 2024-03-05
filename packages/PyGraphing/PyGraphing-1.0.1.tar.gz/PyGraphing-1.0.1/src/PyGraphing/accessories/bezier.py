import numpy as np
from numpy import ndarray as nd


def _tridiagonal(n: int):
    """
    creates the Bezier (X) matrix which has a strict definition as tridiaganol in all cases.
    ex. for n = 7

        2   1   0   0   0   0   0
        1   4   1   0   0   0   0
        0   1   4   1   0   0   0
        0   0   1   4   1   0   0
        0   0   0   1   4   1   0
        0   0   0   0   1   4   1
        0   0   0   0   0   2   7

    """
    a = np.ones((n - 1,))
    a[-1] = 2

    b = 4 * np.ones((n,))
    b[0] = 2
    b[-1] = 7

    c = np.ones((n - 1,))

    return a, b, c


def _build_equals_vector(vector: nd) -> nd:
    """Solution Vector (Y) for the generalized linear solution X*b=Y"""
    vector = np.array(vector)
    p = 2 * (2 * vector[0:-1] + vector[1:])
    p[0] = vector[0] + 2 * vector[1]
    p[-1] = 8 * vector[-2] + vector[-1]

    return p


def _thomas(vector: nd) -> nd:
    """
    Use Thomas Algorithm to solve the tridiagonal system xb=y.
    """
    n = len(vector) - 1
    tL, tD, tU = _tridiagonal(n)
    y = _build_equals_vector(vector)

    c = np.zeros((n - 1,))
    d = np.zeros((n,))

    for i in range(n):
        if i == 0:
            c[i] = tU[i] / tD[i]
            d[i] = y[i] / tD[i]
        else:
            ai = tL[i - 1]
            bi = tD[i]
            di = y[i]
            if i < n - 1:
                ci = tU[i]
                c[i] = ci / (bi - ai * c[i - 1])

            d[i] = (di - ai * d[i - 1]) / (bi - ai * c[i - 1])

    b = np.zeros((n,))
    b[-1] = d[-1]
    for i in range(n - 2, -1, -1):
        b[i] = (d[i] - c[i] * b[i + 1])

    return b


def interpolate(vector: nd) -> tuple[nd, nd]:
    a = _thomas(vector)

    b = np.zeros((len(vector) - 1,))
    b[:-1] = 2 * vector[1:-1] - a[1:]
    b[-1] = (a[-1] + vector[-1]) / 2

    return a, b


class BezierCurve:
    def __init__(self, x: nd, y: nd):
        self.x = np.array(x)
        self.y = np.array(y)
        self.ax, self.bx = interpolate(self.x)
        self.ay, self.by = interpolate(self.y)

        self.n = len(self.x)

        self.grain = 25

    def path_points(self, fill_line=None):
        if fill_line is not None:
            points = [('M', self.x[0], fill_line),
                      ('L', self.x[0], self.y[0])]
        else:
            points = [('M', self.x[0], self.y[0])]

        for i in range(self.n - 1):
            if i == 0:
                points.append(('C', self.ax[i], self.ay[i]))
            else:
                points.append(('', self.ax[i], self.ay[i]))
            points.append(('', self.bx[i], self.by[i]))
            points.append(('', self.x[i + 1], self.y[i + 1]))

        if fill_line is not None:
            points.append(('L', self.x[-1], fill_line))
            points.append(('Z', '', ''))

        return points

    def cubes(self):
        t = np.linspace(0, 1, self.grain)

        def cube(a, b, c, d):
            return np.power(1 - t, 3) * a + \
                   3 * np.power(1 - t, 2) * t * b + \
                   3 * (1 - t) * np.power(t, 2) * c + \
                   np.power(t, 3) * d

        x = cube(self.x[:-1], self.ax, self.bx, self.x[1:])
        y = cube(self.y[:-1], self.ay, self.by, self.y[1:])

        return x, y

    def integrate(self):

        def cube(a, b, c, d, t):
            p1 = (-a / 4) * np.power(1 - t, 4)
            p2 = 3 * b * (np.power(t, 4) / 4 - 2 * np.power(t, 3) / 3 + np.power(t, 2) / 2)
            p3 = 3 * c * (np.power(t, 3) / 3 - np.power(t, 4) / 4)
            p4 = d * np.power(t, 4) / 4

            return p1 + p2 + p3 + p4

        return cube(self.y[:-1], self.ay, self.by, self.y[1:], 1) - cube(self.y[:-1], self.ay, self.by, self.y[1:], 0)


q = 1
