import sys
import numpy as np
from matplotlib.collections import PatchCollection
import matplotlib
import matplotlib.pyplot as plt

from star import Star, Point

class Layout(object):
    def __init__(self, config=None):
        self.stars = []
        if config is not None:
            for data in config.stars:
                star = Star(
                    name=data.name,
                    data=data.sides,
                    inner_radius=float(data.inner_radius),
                    outer_radius=float(data.outer_radius),
                    center=data.center,
                    initial_rotation=float(data.initial_rotation),
                    tees=data.tees,
                    color=data.color,
                    orientation=data.orientation,
                    line_width=float(data.line_width),
                    scaler=float(data.scaler),
                    )

                self.stars.append(star)

    def do_mods(self, num_mods, mod_decay):
        num_stars = len(self.stars)
        for idx in range(num_stars):
            for mod_idx in range(1, num_mods):
                star = self.stars[idx].duplicate()
                star.initial_rotation += float(mod_idx * np.pi / (star.sides+3))
                star.outer_radius += (float(mod_idx) * 1./mod_decay)
                star.center = Point(star.center.x + (mod_idx * 10.), star.center.y)
                self.stars.append(star)

    def randomize(self, count):
        X = 0
        Y = 0
        adder = 25
        cols = int(np.sqrt(count))
        col = 0
        center = Point(0,0)
        for _ in range(count):
            self.stars.append(Star(center=center))
            col += 1
            if col == cols:
                X = 0
                Y += adder
                col = 0
            else:
                X += adder
            center = Point(X, Y)

    def render(self, ax):
        xmins = []
        ymins = []
        xmaxs = []
        ymaxs = []
        for star in self.stars:
            xmin, xmax, ymin, ymax = star.render(ax)
            xmins.append(xmin)
            xmaxs.append(xmax)
            ymins.append(ymin)
            ymaxs.append(ymax)

        ax.set_xlim([np.min(xmins), np.max(xmaxs)])
        ax.set_ylim([np.min(ymins), np.max(ymaxs)])
