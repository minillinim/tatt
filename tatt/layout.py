import sys
import numpy as np
from matplotlib.collections import PatchCollection
import matplotlib
import matplotlib.pyplot as plt

from star import Star, Point

class Layout(object):
    def __init__(self, config):
        self.stars = []
        for data in config.stars:
            star = Star(
                data.name,
                data.sides,
                float(data.inner_radius),
                float(data.outer_radius),
                data.center,
                float(data.initial_rotation),
                data.tees,
                data.color,
                data.orientation,
                line_width=float(data.line_width),
                scaler=float(data.scaler),
                )

            star.initialise()
            self.stars.append(star)

    def do_mods(self, num_mods, mod_decay):
        num_stars = len(self.stars)
        for idx in range(num_stars):
            for mod_idx in range(1, num_mods):
                star = self.stars[idx].duplicate()
                star.initial_rotation += float(mod_idx * np.pi / (star.sides+3))
                star.outer_radius += (float(mod_idx) * 1./mod_decay)
                star.center = Point(star.center.x + (mod_idx * 10.), star.center.y)

                star.initialise()
                self.stars.append(star)

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
