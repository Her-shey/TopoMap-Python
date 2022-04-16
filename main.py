from Topomap import TopoMap
import numpy as np
test = TopoMap()
arr = pts = np.array([[1,2,3,4],[8,7,6,5],[10,11,12,13]]).T
test.project(arr,1)
