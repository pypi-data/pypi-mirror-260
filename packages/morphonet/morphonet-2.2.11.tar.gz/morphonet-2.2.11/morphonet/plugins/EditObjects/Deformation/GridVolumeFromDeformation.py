
from .TetrahedralVolume import TetrahedralVolume

import numpy as np
from .Mesh import Mesh
from .utils import vecLenSqr, vecNorm

class GridVolumeFromDeformation(TetrahedralVolume):

    def __init__(self, shape, deformedMesh):
        super().__init__()
        self.shape = np.array(shape)
        self.pointsShape = self.shape + 1
        self.n_vertices = self.pointsShape[0] * self.pointsShape[1] * self.pointsShape[2]
        self.deformedMesh = deformedMesh

    def constructTetrahedralMesh(self, originalMesh: Mesh):
        """ Initialize vertices, tetrahedrons and bounding box"""
        self.vertices = np.zeros((self.n_vertices, 3))
        self.tetrahedrons = []

        self.borderVertices = []
        self.borderTetrahedrons = []

        """
          6----7
         /|   /|
        2----3 |
        | 4--|-5
        |/   |/
        0----1
        """
        tets = [\
            [0, 1, 5, 3],\
            [0, 2, 3, 6],\
            [0, 5, 4, 6],\
            [0, 3, 5, 6],\
            [3, 5, 6, 7],\
        ]
        tetsReverse = [\
            [1, 2, 4, 0],\
            [1, 7, 2, 3],\
            [1, 4, 7, 5],\
            [2, 7, 4, 6],\
            [1, 4, 2, 7],\
        ]

        borderVerticesIndexDict = dict()

        totalPointShape = self.pointsShape + 2
        totalPointShapeIter = self.pointsShape + 1
        for cz in range(-1, totalPointShapeIter[2]):
            for cy in range(-1, totalPointShapeIter[1]):
                for cx in range(-1, totalPointShapeIter[0]):
                    if     (cz == -1 or cz == self.pointsShape[2]) \
                        or (cy == -1 or cy == self.pointsShape[1]) \
                        or (cx == -1 or cx == self.pointsShape[0]):
                        index = cz*totalPointShape[1]*totalPointShape[0] + cy*totalPointShape[0] + cx
                        borderVerticesIndexDict[index] = len(self.borderVertices)
                        self.borderVertices.append([cx, cy, cz])
                    else:
                        index = cz*self.pointsShape[1]*self.pointsShape[0] + cy*self.pointsShape[0] + cx
                        self.vertices[index] = [cx, cy, cz]

                    
        epsilon = 3.0
        epsilon **= 2
        deformPos = np.where(np.sum((self.deformedMesh.vertices - originalMesh.vertices)**2, axis=1) > epsilon)

        if len(deformPos[0]) > 0:
            orDvs = originalMesh.vertices[deformPos]
            ormin = np.min(orDvs, axis=0)
            ormax = np.max(orDvs, axis=0)
            dDvs = self.deformedMesh.vertices[deformPos]
            dmin = np.min(dDvs, axis=0)
            dmax = np.max(dDvs, axis=0)

            newbbmin = np.min([ormin, dmin], axis=0)
            newbbmax = np.max([ormax, dmax], axis=0)
                
            self.bbmin = newbbmin
            self.bbmax = newbbmax
        
            #bbOver = 0.5 * (self.bbmax - self.bbmin) / self.shape
            bbOver = .16 * (self.bbmax - self.bbmin) # scale by 16% of diagonal
            self.bbmin -= bbOver
            self.bbmax += bbOver
            self.bbspan = self.bbmax - self.bbmin
        else:
            self.bbmin = (originalMesh.bbmin + originalMesh.bbmax) * 0.5
            self.bbmax = self.bbmin
            self.bbspan = self.bbmax - self.bbmin
            self.vertices = np.asarray([])
            self.tetrahedrons = np.asarray([], dtype=int)
            return

        factor = self.bbspan / self.shape;
        self.vertices       = self.vertices       * factor + self.bbmin
        self.borderVertices = self.borderVertices * factor + self.bbmin

        borderVerticesOffset = len(self.vertices)

        totaShape = self.shape + 2
        totaShapeIter = self.shape + 1
        for cz in range(-1, totaShapeIter[2]):
            for cy in range(-1, totaShapeIter[1]):
                for cx in range(-1, totaShapeIter[0]):
                    pointsId = np.zeros(8, dtype=int)
                    for z in range(2):
                        for y in range(2):
                            for x in range(2):
                                i = z * 4 + y * 2 + x
                                nz = cz+z
                                ny = cy+y
                                nx = cx+x
                                if     (nz == -1 or nz == self.pointsShape[2]) \
                                    or (ny == -1 or ny == self.pointsShape[1]) \
                                    or (nx == -1 or nx == self.pointsShape[0]):
                                    curIndex = nz*totalPointShape[1]*totalPointShape[0] + ny*totalPointShape[0] + nx
                                    pointsId[i] = borderVerticesIndexDict[curIndex] + borderVerticesOffset
                                else:
                                    curIndex = nz*self.pointsShape[1]*self.pointsShape[0] + ny*self.pointsShape[0] + nx
                                    pointsId[i] = curIndex

                    curCubeIsReversed = (cx + cy + cz) % 2 == 0
                    curTests = tetsReverse if curCubeIsReversed else tets

                    listToConcat = self.tetrahedrons
                    if     (cz == -1 or cz == self.shape[2]) \
                        or (cy == -1 or cy == self.shape[1]) \
                        or (cx == -1 or cx == self.shape[0]):
                        listToConcat = self.borderTetrahedrons
                        
                    for tet in curTests:
                        listToConcat.append(pointsId[tet])

        self.tetrahedrons = np.array(self.tetrahedrons, dtype=int)

        self.vertices = np.array(self.vertices)
        self.borderTetrahedrons = np.array(self.borderTetrahedrons, dtype=int)