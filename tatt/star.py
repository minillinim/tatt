import numpy as np
np.seterr(all='raise')

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

from scipy import interpolate

from attrs import Point

class Star(object):
    
    def __init__(
        self,
        sides,
        inner_radius,
        outer_radius,
        position,
        rotation,
        tees,
        color,
        orientation,
        line_width=1,
        scaler=5.,
        ):

        self.sides = sides
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.position = position
        self.rotation = rotation
        self.tees = tees
        self.color = color
        self.orientation = orientation
        self.line_width = line_width
        self.scaler = scaler

    def initialise(self):
        scaler = self.scaler / (self.inner_radius + self.outer_radius)
        self.shard = Shard(
            inner_angle=np.pi*2./float(self.sides),
            inner_radius=self.inner_radius * scaler,
            outer_radius=self.outer_radius * scaler,
            position=self.position,
            tees=self.tees,
            direction=self.rotation,
            orientation=self.orientation,
            )

    def duplicate(self):
        return Star(
            self.sides,
            self.inner_radius,
            self.outer_radius,
            self.position,
            self.rotation,
            self.tees,
            self.color,
            self.orientation,
            line_width=self.line_width,
            scaler=self.scaler,
            )

    def get_splines(self):
        splines = []
        for i in np.arange(self.sides):
            for spline in self.shard.get_splines():
                splines.append(spline)
            self.shard.rotate_to_next()
        return splines
    
    def get_polygons(self):
        return [Polygon(p, False) for p in self.get_splines()]

class Shard(object):

    def __init__(
        self,
        inner_angle,
        inner_radius,
        outer_radius,
        position,
        tees,
        orientation="counter",
        direction=0.):
        
        self.inner_angle = inner_angle
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.position = position
        self.orientation = orientation
        self.direction = direction
        self.tees = [Tee(self._to_rad(t.angle), t.width, t.length) for t in tees]

    def _to_rad(self, angle):
        return float(angle)/180.*np.pi

    def get_splines(self):
    
        upper_angle = (self.direction + self.inner_angle / 2.) % (2. * np.pi)
        lower_angle = (self.direction - self.inner_angle / 2.) % (2. * np.pi)

        right_point = Point (
                self.position.x + self.inner_radius * np.cos(upper_angle),
                self.position.y + self.inner_radius * np.sin(upper_angle)
                )

        left_point = Point (
                self.position.x + self.inner_radius * np.cos(lower_angle),
                self.position.y + self.inner_radius * np.sin(lower_angle)
                )

        current_direction = self.direction
        remaining_width = right_point.distance(left_point)
        remaining_length = self.outer_radius

        if self.orientation == "counter":
            left_points = [self.position, left_point]
            right_points = [right_point]
        else:
            left_points = [left_point]
            right_points = [self.position, right_point]

        for t in self.tees:
            new_points = t.get_next_left_right(
                remaining_width,
                remaining_length,
                current_direction,
                left_points[-1],
                right_points[-1])
            
            if(len(new_points) == 1):
                return self.make_splines(left_points + new_points, right_points + new_points)
            else:
                left_points.append(new_points[0])
                right_points.append(new_points[1])
                current_direction = current_direction + t.angle
                remaining_width = remaining_width * (1. - t.width)
                remaining_length = remaining_length * (1. - t.length)

    def make_splines(self, left_points, right_points):
        return (
            self._splinify([p.x for p in left_points], [p.y for p in left_points]),
            self._splinify([p.x for p in right_points], [p.y for p in right_points])
            )

    def _splinify(self, xs, ys):
        try:
            tck,u = interpolate.splprep( [xs,ys] , k=4)
        except TypeError:
            tck,u = interpolate.splprep( [xs,ys] , k=3)
        return interpolate.splev(
            np.linspace( 0, 1, 100 ),
            tck,der = 0
            )

    def rotate_to_next(self):
        self.direction = (self.direction + self.inner_angle) % (2. * np.pi) 

class Tee(object):
    def __init__(self, angle, width, length):
        self.angle = float(angle)
        self.width = float(width)
        self.length = float(length)

    def get_next_left_right(
        self,
        width,
        length,
        direction,
        left_point,
        right_point
        ):
        t_length = self.length * length
        t_direction = self.angle + direction
        u_vector = Point(t_length * np.cos(t_direction), t_length * np.sin(t_direction))
        center_point = left_point.midpoint(right_point)
        far_point = center_point.translate(u_vector)
        if self.width == 1.:
            return [far_point]
        
        t_width = self.width * width / 2.
        points = []
        for a in [-1. * np.pi/2., np.pi/2.]:
            tmp_dir = t_direction + a
            tmp_vector = Point(t_width * np.cos(tmp_dir), t_width * np.sin(tmp_dir))
            points.append(far_point.translate(tmp_vector))            
        return points