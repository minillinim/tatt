import sys
import numpy as np
from matplotlib.collections import PatchCollection
import matplotlib
import matplotlib.pyplot as plt

from star import Star
from attrs import Point

class Layout(object):
    def __init__(self, config):
        self._load_stars(config)
        self.limits = {
            "xmin": sys.float_info.max,
            "ymin": sys.float_info.max,
            "ymax": sys.float_info.min,
            "xmax": sys.float_info.min,
            }

    def render(self, ax):
        for star in self.stars:
            splines = star.get_splines()
            for spline in splines:
                xs = spline[0]
                ys = spline[1]
                self._update_limits(xs, ys)
                ax.plot( xs, ys, '-', color=star.color, linewidth=star.line_width)

        plt.rcParams['axes.facecolor']='black'
        plt.rcParams['savefig.facecolor']='black'

        ax.set_xlim([self.limits["xmin"] - 1, self.limits["xmax"] + 1])
        ax.set_ylim([self.limits["ymin"] - 1, self.limits["ymax"] + 1])

    def _update_limits(self, xs, ys):
        xmin = np.min(xs)
        xmax = np.max(xs)
        ymin = np.min(ys)
        ymax = np.max(ys)

        if xmin < self.limits["xmin"]: self.limits["xmin"] = xmin
        if xmax > self.limits["xmax"]: self.limits["xmax"] = xmax
        if ymin < self.limits["ymin"]: self.limits["ymin"] = ymin
        if ymax > self.limits["ymax"]: self.limits["ymax"] = ymax

    def _load_stars(self, config):


        from random import randint
        r = lambda: randint(0,255)
        choose = lambda: '#%02X%02X%02X' % (r(),r(),r())

        self.stars = []

        dupe_width_mod = 3.
        dupe_color = "#aaaaaa"
        dupe_rotate = 3.
        decay = 3.

        real_star_indicies = []

        for data in config.stars:
            star = Star(
                sides=data.sides,
                inner_radius=float(data.inner_radius),
                outer_radius=float(data.outer_radius),
                position=data.position,
                rotation=float(data.rotation),
                tees=data.tees,
                color="#555555",#choose(),#data.color,
                orientation=data.orientation,
                line_width=float(data.line_width),
                scaler=float(data.scaler),
                )
            star.initialise()
 
            sd = star.duplicate()
            sd.color = "#555555"#dupe_color
            sd.rotation = star.rotation + dupe_rotate / 180. * np.pi
            sd.line_width = star.line_width * dupe_width_mod
            sd.initialise()

            #self.stars.append(sd)
            self.stars.append(star)
            real_star_indicies.append(len(self.stars)-1)
            break

        for rsi in real_star_indicies:
            for c in range(1, 12):
                star = self.stars[rsi].duplicate()
                star.color="#555555"#Schoose()
                star.rotation = float(c * np.pi / 7.) 
                star.outer_radius = star.outer_radius + (float(c) * 1./decay)
                star.position = Point(star.position.x + (c * 10.), star.position.y)
                star.initialise()
                
                sd = star.duplicate()
                sd.color = "#555555"#Sdupe_color
                sd.rotation = star.rotation + dupe_rotate / 180. * np.pi
                sd.line_width = star.line_width * dupe_width_mod
                sd.initialise()

                #self.stars.append(sd)
                self.stars.append(star)
