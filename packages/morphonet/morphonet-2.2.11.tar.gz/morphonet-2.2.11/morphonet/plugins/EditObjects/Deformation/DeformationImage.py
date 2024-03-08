import numpy as np

class DeformationImage(np.ndarray):
    def __new__(cls, data, vsize = np.asarray([1]*3), origin = np.asarray([0]*3), background = 0):
        obj = np.asarray(data).view(cls)
        obj.vsize = vsize
        obj.invvsize = np.array(list(1.0 / s for s in vsize))
        obj.origin = origin
        obj.background = background
        return obj

    def clone(self):
        return DeformationImage(self.copy(), self.vsize, self.origin, self.background)

    def setValue(self, vx, vy, vz, value):
        self[vx, vy, vz] = value

    def fillWithin(self, aabbMin, aabbMax, value):
        self[aabbMin[0]:aabbMax[0], aabbMin[1]:aabbMax[1], aabbMin[2]:aabbMax[2]].fill(value)


    def setVSize(self, newVSize):
        self.vsize = newVSize
        self.invvsize = np.array(list(1.0 / s for s in newVSize))

    def convertCoordFromImageToWorld(self, p):
        return (p + 0.5) * self.vsize + self.origin

    def convertCoordsFromWorldToImage(self, p):
        return (p - self.origin) * self.invvsize

class DeformationImageOnValues(DeformationImage):
    def __new__(cls, data, vsize = np.asarray([1]*3), origin = np.asarray([0]*3), background = 0, *args, **kwargs):
        return DeformationImage.__new__(cls, data, vsize, origin, background)
    def __init__(self, data, vsize = np.asarray([1]*3), origin = np.asarray([0]*3), background = 0, modifiableCellIds = {}):
        self.modifiableCellIds = set(modifiableCellIds)
        self.modifiableCellIds.add(self.background)

    def clone(self):
        return DeformationImageOnValues(self.copy(), self.vsize, self.origin, self.background, self.modifiableCellIds.copy())

    def setValue(self, vx, vy, vz, value):
        if value in self.modifiableCellIds and self[vx, vy, vz] in self.modifiableCellIds:
            self[vx, vy, vz] = value

    def fillWithin(self, aabbMin, aabbMax, value):
        arrWithBbox = self[aabbMin[0]:aabbMax[0], aabbMin[1]:aabbMax[1], aabbMin[2]:aabbMax[2]]
        arrWithBbox[np.where(np.isin(arrWithBbox, list(self.modifiableCellIds)))] = value

