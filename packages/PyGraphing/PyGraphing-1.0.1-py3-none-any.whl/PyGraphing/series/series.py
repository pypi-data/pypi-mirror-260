from ..plot import Plot
from PySVG import G, Path
from numpy import ndarray
from ..icon import Icon


class Series(G):
    def __init__(self, plot: Plot, x: ndarray, y: ndarray):
        super().__init__()
        self.plot = plot
        self.X = x
        self.Y = y

    def _process(self):
        pass

    def construct(self, depth):
        self._process()
        return super().construct(depth)


class Scatter(Series):
    def __init__(self, icon: Icon, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = icon

    def _process(self):
        x = self.plot.cart2pixel_x(self.X) - self.icon.w / 2
        y = self.plot.cart2pixel_y(self.Y) - self.icon.h / 2

        _ = [self._set_icon(i, j) for i, j in zip(x, y)]

    def _set_icon(self, x: float, y: float):
        icon = self.icon.copy()
        icon.x = x
        icon.y = y

        self.add_child(icon.root)


class Line(Series):
    def __init__(self, path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.add_child(self.path)

    def _process(self):
        x = self.plot.cart2pixel_x(self.X)
        y = self.plot.cart2pixel_y(self.Y)
        f = ['M'] + ['L'] * (len(x) - 1)

        self.path.points = [(i, j, k) for i, j, k in zip(f, x, y)]
