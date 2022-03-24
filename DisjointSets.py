
class DisjointSets:

    def __init__(self):
        self.set = []

    def find(self, x):
        f = self.set[x]
        if f < 0:
            return x
        else:
            xx = self.find(f)
            self.set[x] = xx
            return xx

    def merge(self, ele1, ele2):
        self.mergeSet(self.find(ele1),self.find(ele2))

    def mergeSet(self, root1, root2):
        if root1 == root2:
            return
        
        r1 = self.set[root1]
        r2 = self.set[root2]

        if r2 < r1:
            self.set[root1] = root2
        else:
            if r1 == r2:
                r1 -= 1
                self.set[root1] = r1
            self.set[root2] = root1

