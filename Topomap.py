from operator import ge
import geomutils
import DisjointSets
from scipy import spatial
import numpy as np


class TopoMap:
    def __init__(self, emstLeafSize = 1, verbose = False):
        self.verbose = None
        self.leafSize = None
        self.compMap = []
        self.verts = []
        self.comps = set(int)

    def project(self, data: np.ndarray, dimension:int):
        localEdges = []
        localWeights = []

        print("computing emst")
        self.emst(data,dimension,localEdges,localWeights)
        print("placing points")
        return self.placePoints(localEdges,localWeights)

    def emst(self, data:np.ndarray, dim:int, edges, weights) -> None:
        npts = data.size / dim
        pts = np.zeros(dim,npts)

        for i in range(npts):
            for j in range(dim):
                pts[i,j] = data[i*dim + j]
        
        oldFromNew = []
        # 这个地方挺奇怪的，原先有一个OldFrmNew的参数，scipy里面没这个了
        tree = spatial.KDTree(pts,leafsize=self.leafSize)
        # TODO

        pass

    def placePoints(self,edges:np.ndarray, weights:np.ndarray):
        if edges.size != weights.size:
            raise ValueError("edges and lengths don't match")
        comps = DisjointSets()
        self.compMap.clear()

        for i in range(edges.size() + 1):
            newVert = geomutils.Vertex(geomutils.Point(0,0),i)
            self.verts.append(newVert)

            newCM = geomutils.Component()
            newCM.vertices.append(i)
            newCM.hull.append(self.verts[i].p)
            newCM.hull.append(self.verts[i].p)
            self.compMap.append(newCM)

        order = sortEdges(edges,weights) #这又是什么？？
        
        for _i in range(len(order)):
            i = order[_i]
            p1 = edges[i][0]
            p2 = edges[i][1]

            c1 = self.comps.find(p1)
            c2 = self.comps.find(p2)

            if c1 == c2:
                raise ValueError("Error!!! MST edge belongs to the same component!!!") 

            comp1 = self.compMap[c1]
            comp2 = self.compMap[c2]
            comp = self.mergeComponents(comp1,comp2,p1,p2,weights[i])
            self.comps.merge(c1,c2) # 这个merge需要研究研究，c1 c2都是序数，那这里到底要merge啥

            c = self.comps.find(c1)
            self.compMap[c] = comp 
        pts = []
        for i in range(len(self.verts)):
            pts.append(self.verts[i].p)
        return pts





    def allighHull(self,hull,p:geomutils.Point,topEdge:bool) ->geomutils.Transformation:
        v= -1
        for i in range(len(hull)):
            d = geomutils.distance2(hull[i],p)
            # 这里需要去定义distance2
            if v == -1:
                d2 = d
                v = i
            elif d2 > d:
                d2 = d
                v = i
        
        v1 = geomutils.Point()
        v2 = geomutils.Point()
        if topEdge:
            v1 = hull[v]
            v2 = hull[v+1]
        else:
            if v ==0:
                v = len(hull)-1
            v1 = hull[v]
            v2 = hull[v-1]

        trans = geomutils.Transformation(-1*hull[v].x,-1*hull[v].y)
        if (len(hull)>2):
            geomutils.findAngle(v1,v2,trans)
        else:
            trans.sin = 0
            trans.cos = 1
        return trans

    
    def transform(self,p:geomutils.Point,t:geomutils.Transformation,yOffset:float) -> geomutils.Point:
        x = p.x + t.tx
        y = p.y + t.ty
        xx = x * t.cos - y * t.sin
        yy = x*t.sin + y * t.cos
        yy += yOffset
        return geomutils.Point(xx,yy)

    def transformComponent(self,c:geomutils.Component,t:geomutils.Transformation,yOffset:float) -> None:
        for i in range(len(c.vertices)):
            vin = c.vertices[i]
            self.verts[vin].p = self.transform(self.verts[vin].p,t,yOffset)

    
    def mergeComponents(self,c1:geomutils.Component,
            c2:geomutils.Component,v1:int,v2:int,length:float) -> geomutils.Component:
        merged = geomutils.Component()
        merged.vertices.clear()
        merged.vertices.extend(c1)
        merged.vertices.extend(c2)
        merged.hull.clear()

        if length >0:
            t1 = self.allighHull(c1.hull,self.verts[v1].p,True)
            self.transformComponent(c1,t1,0)

            t2 = self.allighHull(c2.hull,self.verts[v2].p,False)
            self.transformComponent(c2,t2,length)

            pts = []
            for i in range(len(c1.hull)):
                pts.append(self.transform(c1.hull[i],t1,0))
            for j in range(len(c2.hull)):
                pts.append(self.transform(c2.hull[i],t2,length))
            geomutils.computeConvexHull(pts,merged.hull)
            #这里怎么接这个语句的返回值啊？
        else:
            if len(c1.hull) !=2 or len(c2.hull) != 2:
                raise ValueError("Error!!! hull cannot have more than one point when edge lenght is 0!!!")
            
            merged.hull.append(c2.hull[0])
            merged.hull.append(c2.hull[1])
        return merged


