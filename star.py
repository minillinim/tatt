import numpy as np
from matplotlib.patches import Polygon

class Shard(object):

    def __init__(
        self,
        inner_angle=np.pi/5.,
        inner_radius=1.,
        outer_radius=4.,
        base=(0., 0,),
        direction=0.):
        
        self.inner_angle = inner_angle
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.base = base
        self.direction = direction

    def calc(self):
    
        upper_angle = (self.direction + self.inner_angle / 2.) % (2. * np.pi)
        lower_angle = (self.direction - self.inner_angle / 2.) % (2. * np.pi)

        points = [
            self.base,
            (
                self.inner_radius * np.cos(upper_angle),
                self.inner_radius * np.sin(upper_angle)
            ),
            (
                self.outer_radius * np.cos(self.direction),
                self.outer_radius * np.sin(self.direction)                
            ),
            (
                self.inner_radius * np.cos(lower_angle),
                self.inner_radius * np.sin(lower_angle)
            ),
            self.base]

        return points

    def rotate(self):
        self.direction = (self.direction + self.inner_angle) % (2. * np.pi) 

class Star(object):
    
    def __init__(
        self,
        sides=5,
        inner_radius=1.,
        outer_radius=4.,
        base=(0., 0,)):

        self.sides = sides
                
        self.shard = Shard(
            inner_angle=np.pi*2./float(sides),
            inner_radius=inner_radius,
            outer_radius=outer_radius,
            base=base)

    def shards(
        self):
        
        points = []
        for i in np.arange(self.sides):
            points.append(self.shard.calc())    
            self.shard.rotate()
        return points
    
    def render(
        self,
        shards=None):
        
        if shards == None:
            shards = self.shards()
        
        return [Polygon(s, False) for s in shards]

