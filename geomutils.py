#from ctypes.wintypes import POINT
import numpy as np
from scipy.spatial import ConvexHull
import math


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
        self.hull = []


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
            return np.sqrt(np.sum((self.p1-self.p2)**2))


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


def findAngle(point1: np.ndarray, point2: np.ndarray, transform: Transformation):
    # point should be point
    # But I prefer array type, this need further discussion
    vec = np.array([[point1.x-point2.x, point1.y-point2.y]])#point1 - point2
    norm = np.linalg.norm(vec)
    transform.cos = vec[0][0] / norm
    transform.sin = np.sqrt(1.0 - transform.cos**2)
    if(vec[0][1] >= 0):
        transform.sin = -transform.sin


def computeConvexHull(points: np.ndarray, convex_hull: list):
    convex_hull.clear()
    if len(points) == 1:
        convex_hull.append(points[0])
        convex_hull.append(points[0])
        return convex_hull
    elif len(points) == 2:
        convex_hull.append(points[0])
        convex_hull.append(points[1])
        convex_hull.append(points[0])
        return convex_hull
    
    hull = ConvexHull(points)
    convex_hull.extend(points[hull.vertices].tolist())
    convex_hull.append(convex_hull[0])
    return convex_hull

def distance2(p1:Point,p2:Point) -> float:
    return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

# unitest
if __name__ == '__main__':
    points = np.random.rand(30,2)
    hull = []
    print('Random Points:',points)
    #hull = computeConvexHull(points)
    #print('Convex Hull Index:',hull.vertices.tolist())