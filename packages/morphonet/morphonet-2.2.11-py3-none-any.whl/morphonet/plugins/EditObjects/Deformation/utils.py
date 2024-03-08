import math
import numpy as np

def clamp(s, minS, maxS):
    return min(max(s, minS), maxS)

def clampWithCheck(s, minS, maxS):
    # Also returns true if value was changed
    if s < minS:
        return minS, True
    if s > maxS:
        return maxS, True
    return s, False

def vecAdd(v0, v1):
    return [v0[0] + v1[0], v0[1] + v1[1], v0[2] + v1[2]]

def vecSub(v0, v1):
    return [v0[0] - v1[0], v0[1] - v1[1], v0[2] - v1[2]]

def vecLenSqr(v):
    return v[0] * v[0] + v[1] * v[1] + v[2] * v[2]

def vecNorm(v):
    return math.sqrt(vecLenSqr(v))

def vecMultScal(v0, s):
    return [v0[0] * s, v0[1] * s, v0[2] * s]

def vecMultVec(v0, v1):
    return [v0[0] * v1[0], v0[1] * v1[1], v0[2] * v1[2]]

def vecDot(v0, v1):
    return v0[0] * v1[0] + v0[1] * v1[1] + v0[2] * v1[2]

def vecCross(v0, v1):
    return [v0[1] * v1[2] - v0[2] * v1[1], v0[2] * v1[0] - v0[0] * v1[2], v0[0] * v1[1] - v0[1] * v1[0]]

def vecNormalized(v):
    norm = vecNorm(v)
    return [v[0] / norm, v[1] / norm, v[2] / norm]

def vecNormalizedOrValueIfZero(v, value):
    norm = vecNorm(v)
    if norm > 0:
        return [v[0] / norm, v[1] / norm, v[2] / norm]
    else:
        return value

def vecInvert(v):
    return [1.0 / v[0], 1.0 / v[1], 1.0 / v[2]]

def vecFloor(v):
    return [math.floor(v[0]), math.floor(v[1]), math.floor(v[2])]

def vecClamp(v, minV, maxV):
    return [clamp(v[0], minV[0], maxV[0]), clamp(v[1], minV[1], maxV[1]), clamp(v[2], minV[2], maxV[2])]

def vecClampWithCheck(v, minV, maxV):
    # Also returns true if value was changed
    v0, t0 = clampWithCheck(v[0], minV[0], maxV[0])
    v1, t1 = clampWithCheck(v[1], minV[1], maxV[1])
    v2, t2 = clampWithCheck(v[2], minV[2], maxV[2])
    return [v0, v1, v2], t0 or t1 or t2


def vecOf(s):
    return [s, s, s]

def vecSpanDeterminant(v0, v1, v2):
    return vecDot(vecCross(v0, v1), v2)


def sameSide(p, v1, v2, v3, v4):
    normal = vecCross(v2 - v1, v3 - v1)
    dotV4 = vecDot(normal, v4 - v1)
    dotP = vecDot(normal, p - v1)
    return dotV4 * dotP >= 0
def pointInTetrahedron(p, v1, v2, v3, v4):
    return sameSide(p, v1, v2, v3, v4) and \
           sameSide(p, v2, v3, v4, v1) and \
           sameSide(p, v3, v4, v1, v2) and \
           sameSide(p, v4, v1, v2, v3)
def pointInTet(p, tet):
    return pointInTetrahedron(p, tet[0], tet[1], tet[2], tet[3])


def getTetrahedronBarycentricCoordinates(p, tet):
    p1 = tet[0]
    p2 = tet[1]
    p3 = tet[2]
    p4 = tet[3]

    a = p1[0] - p4[0]
    b = p2[0] - p4[0]
    c = p3[0] - p4[0]
    
    d = p1[1] - p4[1]
    e = p2[1] - p4[1]
    f = p3[1] - p4[1]

    g = p1[2] - p4[2]
    h = p2[2] - p4[2]
    k = p3[2] - p4[2]

    det = a*(e*k - h*f) + b*(g*f - d*k) + c*(d*h - g*e)

    A = e*k - f*h
    D = c*h - b*k
    G = b*f - c*e

    B = f*g - d*k
    E = a*k - c*g
    H = c*d - a*f
    
    C = d*h - e*g
    F = g*b - a*h
    K = a*e - b*d

    ld0 = ((p[0] - p4[0])*A + (p[1] - p4[1])*D + (p[2] - p4[2])*G )/ det
    ld1 = ((p[0] - p4[0])*B + (p[1] - p4[1])*E + (p[2] - p4[2])*H )/ det
    ld2 = ((p[0] - p4[0])*C + (p[1] - p4[1])*F + (p[2] - p4[2])*K )/ det
    ld3 = 1 - ld0 - ld1 - ld2

    return (ld0, ld1, ld2, ld3)


def discriminateDeformationAmount(originalTet, deformedTet, epsilonDetectDeformationSquared, epsilonDetectLargeDeformationSquared):
    defAmount = np.max(np.sum((deformedTet - originalTet)**2, axis=1))
    if defAmount < epsilonDetectDeformationSquared:
        return 0
    allAnglesOriginal = np.zeros(12)
    allAnglesDeformed = np.zeros(12)
    count = 0
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            k = j+1
            if k == i:
                k+=1
            k = k%4
            vecij = originalTet[j] - originalTet[i]
            vecik = originalTet[k] - originalTet[i]
            vecij_norm = vecNorm(vecij)
            vecik_norm = vecNorm(vecik)
            if vecij_norm == 0.0 or vecik_norm == 0.0:
                allAnglesOriginal[count] = 0.0
            else:
                allAnglesOriginal[count] = math.acos(vecDot(vecMultScal(vecij, 1.0/vecij_norm), vecMultScal(vecik, 1.0/vecik_norm)))
            vecij = deformedTet[j] - deformedTet[i]
            vecik = deformedTet[k] - deformedTet[i]
            vecij_norm = vecNorm(vecij)
            vecik_norm = vecNorm(vecik)
            if vecij_norm == 0.0 or vecik_norm == 0.0:
                allAnglesDeformed[count] = 0.0
            else:
                allAnglesDeformed[count] = math.acos(vecDot(vecMultScal(vecij, 1.0/vecij_norm), vecMultScal(vecik, 1.0/vecik_norm)))
            count += 1
    maxAngleDiff = np.max(allAnglesDeformed - allAnglesOriginal)
    if maxAngleDiff < epsilonDetectLargeDeformationSquared:
        return 1
    else:
        return 2
    




















def saveOff(fileName, vertices, triangles):
    out = open(fileName, 'w')

    out.write("OFF\n")
    out.write("%s %s %s\n" % (len(vertices), len(triangles), 0))

    for i in range(len(vertices)):
        out.write("%s %s %s\n" % (vertices[i][0], vertices[i][1], vertices[i][2]))

    for i in range(len(triangles)):
        out.write("%s %s %s %s\n" % (3, triangles[i][0], triangles[i][1], triangles[i][2]))

    out.close()

def saveOffFromTetrahedralMesh(filename, vertices, tetrahedras):
    """
           3
          /|\
         / | \
        /  |  \
       0'-.1.-'2
    """

    faces = [\
        [0, 2, 1],\
        [0, 1, 3],\
        [0, 3, 2],\
        [1, 2, 3],\
        ]

    triangles = []

    for tet in tetrahedras:
        for f in faces:
            triangles.append(tet[f])

    triangles = np.array(triangles, dtype=int)

    saveOff(filename, vertices, triangles)


def saveMesh(fileName, vertices, verticesDimensions, tetrahedra, tetrahedraDomains):
    out = open(fileName, 'w')
    
    out.write("MeshVersionFormatted %s\n" % 1)
    out.write("Dimension %s\n" % 3)
    out.write("Vertices\n")

    out.write("%s\n" % len(vertices))

    for i in range(len(vertices)):
        out.write("%s %s %s %s\n" % (vertices[i][0], vertices[i][1], vertices[i][2], verticesDimensions[i]))

    out.write("Triangles\n")
    out.write("%s\n" % 0)

    out.write("Tetrahedra\n")
    out.write("%s\n" % len(tetrahedra))

    for i in range(len(tetrahedra)):
        out.write("%s %s %s %s %s\n" % (tetrahedra[i][0]+1, tetrahedra[i][2]+1, tetrahedra[i][1]+1, tetrahedra[i][3]+1, tetrahedraDomains[i]))
    
    out.close()

def saveMeshSimple(fileName, vertices, tetrahedra):
    verticesDimensions = np.zeros(len(vertices)).astype(int)
    verticesDimensions.fill(3)
    tetrahedraDomains = np.zeros(len(tetrahedra)).astype(int)
    tetrahedraDomains.fill(1)

    saveMesh(fileName, vertices, verticesDimensions, tetrahedra, tetrahedraDomains)



"""

In testing : 

def optimiseTetrahedrons(self, originalMesh: Mesh, deformedMesh: Mesh, nbIter = 1):
        self.computeVerticesWeights(originalMesh)
        self.computeDeformedVertices(deformedMesh)
        
        print("Start optimization")
        tetrahedronsToProcess = self.tetrahedrons
        epsilonDetectDeformationSquared = 2.0**2
        epsilonDetectLargeDeformationSquared = (math.pi/8)**2
        faces = [\
            [0, 2, 1],\
            [0, 1, 3],\
            [0, 3, 2],\
            [1, 2, 3],\
            ]
        deformedTetrahedrons = []
        for it in range(nbIter):
            print("Iteration", it+1, ":", len(tetrahedronsToProcess), "tetrahedrons to process")
            # Remove unmodified tetrahedrons and subdivide largely deformed tetrahedrons
            highlyDeformedTetrahedrons = []
            newVertices = []
            print("Remove or subdivide tetrahedrons")
            debug_discr_list = []
            for t in tetrahedronsToProcess:
                v  = self.vertices[t]
                dv = self.deformedVertices[t]
                discr = discriminateDeformationAmount(v, dv, epsilonDetectDeformationSquared, epsilonDetectLargeDeformationSquared)
                debug_discr_list.append(discr)
                if discr > 0:
                     # if the tretrahedra is deformed enough
                    if discr == 2:
                        # if the tretrahedra is highly deformed
                        newVerticesIndex = len(self.vertices) + len(newVertices)
                        newVertices.append(np.sum(v, axis=0) * 0.25)
                        for f in range(4):
                            highlyDeformedTetrahedrons.append(list(t[faces[f]]) + [newVerticesIndex])
                    else:
                        #if the tretrahedra is not highly deformed
                        deformedTetrahedrons.append(t)

            debug_discr_list.sort()
            print(debug_discr_list)
            
            if len(newVertices) > 0:
                print("Add", len(newVertices), "vertices")
                # Compute new vertices coordinates
                newVertices = np.asarray(newVertices)
                if len(newVertices) > 128:
                    newVerticesWeights = parralelComputeCoordinates(newVertices, originalMesh.vertices, originalMesh.triangles, originalMesh.trianglesNormals)
                else:
                    newVerticesWeights = np.zeros((len(newVertices), len(originalMesh.vertices)), dtype=np.float32)
                    computeCoordinatesForVertices(0, len(newVertices), newVertices, originalMesh.triangles, originalMesh.vertices, originalMesh.trianglesNormals, newVerticesWeights)

                self.vertices = np.append(self.vertices, newVertices, axis=0)
                self.verticesWeights = np.append(self.verticesWeights, newVerticesWeights, axis=0)
                # compute deformed vertices from all vertices (can be changed to only added vertices for optimisation)
                self.computeDeformedVertices(deformedMesh)

            tetrahedronsToProcess = np.asarray(highlyDeformedTetrahedrons)

        self.tetrahedrons = np.asarray(deformedTetrahedrons + highlyDeformedTetrahedrons, dtype=int)

        print("self.tetrahedrons", len(self.tetrahedrons))
        print("self.vertices", len(self.vertices))
        if True:
            saveMeshSimple("C:/Users/aclement/Desktop/dev/MorphoNet/originalGrid.nmesh", self.vertices, self.tetrahedrons)
            saveMeshSimple("C:/Users/aclement/Desktop/dev/MorphoNet/deformedGrid.nmesh", self.deformedVertices, self.tetrahedrons)
            saveOffFromTetrahedralMesh("C:/Users/aclement/Desktop/dev/MorphoNet/originalGrid.off", self.vertices, self.tetrahedrons)
            saveOffFromTetrahedralMesh("C:/Users/aclement/Desktop/dev/MorphoNet/deformedGrid.off", self.deformedVertices, self.tetrahedrons)
"""