import numpy as np

from .GridVolume import GridVolume
from .GridVolumeFromDeformation import GridVolumeFromDeformation
from .DeformationImage import DeformationImage, DeformationImageOnValues
from .Mesh import Mesh


def initializeVolume(originalMesh = None, deformedMesh = None):
    SHAPE = [8] * 3 # TODO do not hard code grid size
    shape = np.array(SHAPE, dtype=int)
    #volume = GridVolume(shape)
    volume = GridVolumeFromDeformation(shape, deformedMesh)
    return volume

def initializeData(data : np.array, mesh : str, mesh_deform : str, mesh_translation, mesh_scaling, background, cell=None, time=None,):
    if cell!=None:
        originalData = DeformationImageOnValues(data, np.array([1]*3), np.zeros(3), background, [cell])
    else:
        originalData = DeformationImage(data, np.array([1]*3), np.zeros(3), background)
    deformedData = originalData.clone()

    # === Contruct meshes ===
    originalMesh = Mesh.constructFromObjString(mesh, cell, time)
    deformedMesh = Mesh.constructFromObjString(mesh_deform, cell, time)
    # Transform Meshes to world coordinates
    originalMesh.transformCoordinates(mesh_translation, mesh_scaling)
    deformedMesh.transformCoordinates(mesh_translation, mesh_scaling)
    if not np.array_equal(originalMesh.triangles, deformedMesh.triangles):
        moreExp = f" (original triangles : {len(originalMesh.triangles)}, deformedMesh triangles : {len(deformedMesh.triangles)})" if len(originalMesh.triangles)!=len(deformedMesh.triangles) else " (but number of triangles matches)"
        raise InvalidMeshDeformationException("OriginalMesh's triangles does not match with DeformedMesh's triangles"+moreExp)

    # === Construct volume ===
    volume = initializeVolume(originalMesh, deformedMesh)

    return originalData, originalMesh, deformedData, deformedMesh, volume

class InvalidMeshDeformationException(Exception):
    pass
