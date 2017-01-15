import sys
import numpy as np
from matplotlib.collections import PatchCollection
import matplotlib
from star import Star

class Layout(object):
    def __init__(self, config):
        self.stars = self._load_stars(config)
        self.limits = {
            "xmin": sys.float_info.max,
            "ymin": sys.float_info.max,
            "ymax": sys.float_info.min,
            "xmax": sys.float_info.min,
            }

    def render(self, ax):
        for star in self.stars.values():
            polygons = star.get_polygons()
            p = PatchCollection(polygons, cmap=matplotlib.cm.jet, alpha=0.4)
            colors = 100*np.random.rand(len(polygons))
            p.set_array(np.array(colors))
            ax.add_collection(p)
            self._update_limits(np.ravel(star.get_points()).reshape(star.sides*5, 2))
            
        ax.set_xlim([self.limits["xmin"] - 1, self.limits["xmax"] + 1])
        ax.set_ylim([self.limits["ymin"] - 1, self.limits["ymax"] + 1])

    def _update_limits(self, boundaries):
        xmin = np.min(boundaries[:,0])
        xmax = np.max(boundaries[:,0])
        ymin = np.min(boundaries[:,1])
        ymax = np.max(boundaries[:,1])

        if xmin < self.limits["xmin"]: self.limits["xmin"] = xmin
        if xmax > self.limits["xmax"]: self.limits["xmax"] = xmax
        if ymin < self.limits["ymin"]: self.limits["ymin"] = ymin
        if ymax > self.limits["ymax"]: self.limits["ymax"] = ymax

    def _load_stars(self, config):
        stars = {}
        for data in config.stars:
            star = Star(
                sides=data.sides,
                inner_radius=data.inner_radius,
                outer_radius=data.outer_radius,
                position=data.position,
                rotation=data.rotation,
                distortion=data.distortion,
                )
 
            stars[data.name] = star

        return stars