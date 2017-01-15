import numpy as np
np.seterr(all='raise')

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

class Star(object):
    
    def __init__(
        self,
        sides,
        inner_radius,
        outer_radius,
        position,
        rotation,
        distortion,
        ):

        self.sides = sides
                
        self.shard = Shard(
            inner_angle=np.pi*2./float(self.sides),
            inner_radius=inner_radius,
            outer_radius=outer_radius,
            position=position)

    def get_points(self):
        points = []
        for i in np.arange(self.sides):
            points.append(self.shard.get_points())    
            self.shard.rotate_to_next()
        return np.array(points)
    
    def get_polygons(self):
        return [Polygon(p, False) for p in self.get_points()]

class Shard(object):

    def __init__(
        self,
        inner_angle,
        inner_radius,
        outer_radius,
        position,
        direction=0.):
        
        self.inner_angle = inner_angle
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.position = position
        self.direction = direction

    def get_points(self):
    
        upper_angle = (self.direction + self.inner_angle / 2.) % (2. * np.pi)
        lower_angle = (self.direction - self.inner_angle / 2.) % (2. * np.pi)

        points = [
            (self.position.x, self.position.y),
            (
                self.position.x + self.inner_radius * np.cos(upper_angle),
                self.position.y + self.inner_radius * np.sin(upper_angle)
            ),
            (
                self.position.x + self.outer_radius * np.cos(self.direction),
                self.position.y + self.outer_radius * np.sin(self.direction)                
            ),
            (
                self.position.x + self.inner_radius * np.cos(lower_angle),
                self.position.y + self.inner_radius * np.sin(lower_angle)
            ),
            (self.position.x, self.position.y)]

        return points

    def rotate_to_next(self):
        self.direction = (self.direction + self.inner_angle) % (2. * np.pi) 
