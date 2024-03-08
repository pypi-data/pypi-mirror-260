
from .Volume import Volume

import numpy as np
from .MVC import computeCoordinates
from .Mesh import Mesh
from .utils import *

from .utils_threads import parralelComputeCoordinates, computeCoordinatesForVertices, parralelRasterizeDeformation, rasterizeDeformationForTetrahedron

class TetrahedralVolume(Volume):

    def __init__(self):
        self.vertices = []
        self.tetrahedrons = []

        self.borderVertices = []
        self.borderTetrahedrons = []

        self.verticesWeights = []
        self.deformedVertices = []

        self.bbmin = np.zeros(3)
        self.bbmax = np.zeros(3)
        self.bbspan = np.zeros(3)

        self.deformedbbmin = np.zeros(3)
        self.deformedbbmax = np.zeros(3)
        self.deformedbbspan = np.zeros(3)

    def constructTetrahedralMesh(self, originalMesh: Mesh):
        """ Initialize vertices, tetrahedrons and bounding box"""
        pass

    def computeVerticesWeights(self, originalMesh: Mesh):
        """ Initialize vertices weights """
        # Only parallelize if there are more than 128 vertices
        if len(self.vertices) > 128:
            self.verticesWeights = parralelComputeCoordinates(self.vertices, originalMesh.vertices, originalMesh.triangles, originalMesh.trianglesNormals)
        else:
            self.verticesWeights = np.zeros((len(self.vertices), len(originalMesh.vertices)), dtype=np.float32)
            computeCoordinatesForVertices(0, len(self.vertices), self.vertices, originalMesh.triangles, originalMesh.vertices, originalMesh.trianglesNormals, self.verticesWeights)

    def construct(self, originalMesh):
        """ Initialize the volume around the original mesh """
        self.constructTetrahedralMesh(originalMesh)

    def computeDeformedVertices(self, deformedMesh: Mesh):
        """ Initialize deformedVertices """
        self.deformedVertices = np.matmul(self.verticesWeights, deformedMesh.vertices)
        self.deformedbbmin = np.min([np.min(self.deformedVertices, axis=0), np.min(self.borderVertices, axis=0)], axis=0)
        self.deformedbbmax = np.max([np.max(self.deformedVertices, axis=0), np.max(self.borderVertices, axis=0)], axis=0)
        self.deformedbbspan = self.deformedbbmax - self.deformedbbmin

    def optimiseTetrahedrons(self, originalMesh: Mesh, deformedMesh: Mesh, nbIter = 1):
        self.computeVerticesWeights(originalMesh)
        self.computeDeformedVertices(deformedMesh)
        # TODO : check if deformed vertices bb is not inside vertices bb
        # TODO : subdivide tet mesh
        self.vertices         = np.concatenate((self.vertices,         self.borderVertices))
        self.deformedVertices = np.concatenate((self.deformedVertices, self.borderVertices))
        self.tetrahedrons     = np.concatenate((self.tetrahedrons, self.borderTetrahedrons))

    def rasterizeDeformation(self, originalData, deformedData):
        outsideTetrahedronPresent = False
        # Only parallelize if there are more than 64 tetrahedrons
        if len(self.tetrahedrons) > 64:
            outsideTetrahedronPresent = parralelRasterizeDeformation(originalData, self, deformedData)
        elif len(self.tetrahedrons) > 0:
            outsideTetrahedronPresent = rasterizeDeformationForTetrahedron(0, len(self.tetrahedrons),
                                   	self.vertices, self.deformedVertices, self.tetrahedrons,
                                   	originalData, deformedData, [1]*3, [0]*3, originalData.modifiableCellIds, originalData.background)
        else:
            print("Warning : volume is empty, nothing has been done")

        if outsideTetrahedronPresent:
            print("Warning : a Tetrahedra has been found outside of the image range")

    def applyTransformation(self, originalData, originalMesh, deformedData, deformedMesh):
        """ Generate a new image wich is the original image deformed by the mesh's transformation """

        self.optimiseTetrahedrons(originalMesh, deformedMesh, 3)

        self.rasterizeDeformation(originalData, deformedData)
