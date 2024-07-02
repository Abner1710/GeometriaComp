from collections import namedtuple
import math

EPS = 1e-7

Point = namedtuple("Point", ["x", "y"])

def min_y_point(p1: Point, p2: Point):
    """Returns lower of the two given points"""
    return p1 if p1.y < p2.y else p2

def max_y_point(p1: Point, p2: Point):
    """Returns higher of the two given points"""
    return p1 if p1.y > p2.y else p2

def point_add(p1,p2):
    return Point(p1.x+p2.x, p1.y+p2.y)

def point_scale(p, xscale, yscale):
    return Point(p.x*xscale, p.y*yscale)

def point_diff(p1, p2):
    return Point(p1.x - p2.x, p1.y - p2.y)

def point_norm(p):
    return math.sqrt(p.x * p.x + p.y * p.y)

def point_scalar(p1, p2):
    return (p1.x * p2.x + p1.y * p2.y) / (point_norm(p1) * point_norm(p2))

def point_eq(p1, p2):
    return p1.x == p2.x and p1.y == p2.y