import numpy as np

from .utils import *

from vtkmodules.vtkCommonDataModel import vtkGenericCell

class Mesh(object):
    def __init__(self):
        self.vertices = []
        self.triangles = []
        self.trianglesNormals = []

        self.bbmin  = np.zeros(3)
        self.bbmax  = np.zeros(3)
        self.bbspan = np.zeros(3)

    def __repr__(self) -> str:
        return str(len(self.vertices)) + " vertices :\n" + str(self.vertices) + "\n" + str(len(self.triangles)) + " triangles :\n" + str(self.triangles)

    def computeTrianglesNormals(self):
        self.trianglesNormals = np.zeros((len(self.triangles), 3))

        for t in range(len(self.triangles)):
            p0 = self.vertices[self.triangles[t][0]]
            p1 = self.vertices[self.triangles[t][1]]
            p2 = self.vertices[self.triangles[t][2]]
            self.trianglesNormals[t] = vecNormalizedOrValueIfZero(vecCross(p1-p0, p2-p0), [1.0, 0.0, 0.0])

    def computeBoundingBox(self):
        self.bbmin = self.vertices.min(axis=0)
        self.bbmax = self.vertices.max(axis=0)
        self.bbspan = self.bbmax - self.bbmin

    def transformCoordinates(self, translation, scaling):
        self.vertices = self.vertices * scaling + translation
        self.bbmin    = self.bbmin * scaling + translation
        self.bbmax    = self.bbmax * scaling + translation
        self.bbspan   = self.bbmax - self.bbmin

    def transformCoordinatesFromNormalizedImageToWorld(self, imageShape, vsize, origin):
        factor = imageShape * vsize
        self.vertices = self.vertices * factor + origin
        self.bbmin    = self.bbmin * factor + origin
        self.bbmax    = self.bbmax * factor + origin
        self.bbspan   = self.bbmax - self.bbmin

    def constructFromVtkMesh(self, vtkMesh):
        """ Get mesh data from vtkMesh """

        n_vertices  = vtkMesh.GetNumberOfPoints()
        n_triangles = vtkMesh.GetNumberOfCells()

        self.vertices         = np.zeros((n_vertices,  3))
        self.triangles        = np.zeros((n_triangles, 3)).astype(int)

        for i in range(n_vertices):
            self.vertices[i] = np.array(vtkMesh.GetPoint(i))
            
        self.bbmin = self.vertices.min(axis=0)
        self.bbmax = self.vertices.max(axis=0)
        self.bbspan = self.bbmax - self.bbmin

        it = vtkMesh.NewCellIterator()
        it.InitTraversal()
        cell = vtkGenericCell()
        i = 0
        while not it.IsDoneWithTraversal():
            it.GetCell(cell)
            self.triangles[i] = [cell.GetPointId(0), cell.GetPointId(1), cell.GetPointId(2)]
            it.GoToNextCell()
            i += 1

        self.computeTrianglesNormals()

    @classmethod
    def constructFromObjString(cls, objString, cellId=None, time=None):
        cellId = str(cellId)
        time = str(time)
        mesh = cls()
        cellsString = objString.replace("\r", "").split("g")
        for cell in cellsString[1:]:
            lines = cell.split("\n")
            cellDef = lines[0].replace(" ", "").split(",")
            if len(cellDef) < 2:
               print("Error : Cell without id and timestamp !")
               continue
            curTime, curCell = cellDef[:2]
            if cellId != "None" and time != "None":
                if cellId != curCell or time != curTime:
                    print(f"Warning : skipped cell of id {curCell} and time {curTime} (looking for cell {cellId} and time {time})")
                    continue
            
            indexOffset = -1
            if len(cellDef) > 2:
                indexOffset = int(cellDef[2])

            for line in lines[1:]:
                lineDef = line.split(" ")
                if lineDef[0] == 'v':
                    mesh.vertices.append(np.asarray(lineDef[1:], dtype=np.float32))
                elif lineDef[0] == 'f':
                    mesh.triangles.append(np.asarray(lineDef[1:], dtype=np.uint32) + indexOffset)
                elif lineDef[0] != '' or len(lineDef) > 1:
                    print("Warning : Unrecognized mesh line :", line)

        mesh.vertices = np.asarray(mesh.vertices)
        mesh.triangles = np.asarray(mesh.triangles)

        mesh.computeTrianglesNormals()
        mesh.computeBoundingBox()

        return mesh

