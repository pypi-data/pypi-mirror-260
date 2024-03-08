
from TetrahedralVolume import TetrahedralVolume

import numpy as np
from Mesh import Mesh
from utils import readMesh

class MeshVolume(TetrahedralVolume):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def constructTetrahedralMesh(self, originalMesh: Mesh):
        """ Initialize vertices, tetrahedrons and bounding box"""
       
        self.vertices, verticesDimensions, self.tetrahedrons, tetrahedraDomains = readMesh(self.filename)

        self.bbmin = self.vertices.min(axis=0)
        self.bbmax =self.vertices.max(axis=0)
        self.bbspan = self.bbmax - self.bbmin

        if True:
            from utils import saveMeshSimple, saveOffFromTetrahedralMesh
            saveMeshSimple("C:/Users/aclement/Desktop/dev/Seafile/Stage_Ange/data/deformationOutput/originalGrid.nmesh", self.vertices, self.tetrahedrons)
            saveOffFromTetrahedralMesh("C:/Users/aclement/Desktop/dev/Seafile/Stage_Ange/data/deformationOutput/originalGrid.off", self.vertices, self.tetrahedrons)
