
from .TetrahedralVolume import TetrahedralVolume

import numpy as np
from .Mesh import Mesh

class GridVolume(TetrahedralVolume):

    def __init__(self, shape):
        super().__init__()
        self.shape = np.array(shape)
        self.pointsShape = self.shape + 1
        self.n_vertices = self.pointsShape[0] * self.pointsShape[1] * self.pointsShape[2]

    def constructTetrahedralMesh(self, originalMesh: Mesh):
        """ Initialize vertices, tetrahedrons and bounding box"""
        self.vertices = np.zeros((self.n_vertices, 3))
        self.tetrahedrons = []
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

        # can be done in parallel
        for cz in range(self.pointsShape[2]):
            for cy in range(self.pointsShape[1]):
                for cx in range(self.pointsShape[0]):
                    index = cz*self.pointsShape[1]*self.pointsShape[0] + cy*self.pointsShape[0] + cx
                    self.vertices[index] = [cx, cy, cz]

        bbOver = 0.5 * originalMesh.bbspan / self.shape
        #bbOver = 1.0 * originalMesh.bbspan
        self.bbmin = originalMesh.bbmin - bbOver
        self.bbmax = originalMesh.bbmax + bbOver
        self.bbspan = self.bbmax - self.bbmin
        #todo offset % bb

        self.vertices = (self.vertices / self.shape) * self.bbspan + self.bbmin

        # can be done in parallel
        for cz in range(self.shape[2]):
            for cy in range(self.shape[1]):
                for cx in range(self.shape[0]):
                    index = cz*self.pointsShape[1]*self.pointsShape[0] + cy*self.pointsShape[0] + cx

                    pointsId = np.zeros(8, dtype=int)
                    for z in range(2):
                        for y in range(2):
                            for x in range(2):
                                i = z * 4 + y * 2 + x
                                curIndex = (cz+z)*self.pointsShape[1]*self.pointsShape[0] + (cy+y)*self.pointsShape[0] + (cx+x)
                                pointsId[i] = curIndex
                    
                    curCubeIsReversed = (cx + cy + cz) % 2 == 0
                    curTests = tetsReverse if curCubeIsReversed else tets
                    for tet in curTests:
                        self.tetrahedrons.append(pointsId[tet])

        self.tetrahedrons = np.array(self.tetrahedrons, dtype=int)