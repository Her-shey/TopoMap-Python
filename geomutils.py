import numpy as np
from scipy.spatial import ConvexHull

class Point:
    def __init__(self, _x = 0, _y = 0):
        self.x = _x
        self.y = _y


class Vertex:
    def __init__(self, _point, _id):
        self.p = _point
        self.id = _id


class Component:
    def __init__(self):
        self.vertices = []


class Transformation:
    def __init__(self, _tx, _ty, _cos, _sin):
        self.tx = _tx
        self.ty = _ty
        self.cos = _cos
        self.sin = _sin


class Edge:
    def __init__(self, _p1, _p2):
        self.p1 = _p1
        self.p2 = _p2

    def length(self, type='Euclidean'):
        if type == 'Euclidean':
            return np.sqrt(np.sum((p1-p2)**2))


class WeightEdge(Edge):
    def __init__(self, _p1, _p2, _weight):
        super(Edge, self).__init__(_p1, _p2)
        self.weight = _weight

    def __eq__(self, other):
        return self.weight == other.weight
    
    def __gt__(self, other):
        return self.weight > other.weight
    
    def __lt__(self, other):
        return self.weight < other.weight


def findAngle(point1, point2, transform):
    vec = point1 - point2
    N = Edge(vec).length()
    transform.cos = vec[0] / N
    transform.sin = np.sqrt(1.0 - transform.cos**2)
    if(vec[1] >= 0):
        transform.sin = -transform.sin


def computeConvexHull(points):
    convex_hull = []
    if len(points) == 1:
        convex_hull.append(points[0])
        convex_hull.append(points[0])
        return convex_hull
    elif len(points) == 2:
        convex_hull.append(points[0])
        convex_hull.append(points[1])
        convex_hull.append(points[0])
        return convex_hull
    




