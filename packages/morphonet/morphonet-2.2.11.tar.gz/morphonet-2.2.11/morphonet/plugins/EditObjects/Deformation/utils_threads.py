import numpy as np
import os
from multiprocessing import Process, shared_memory, Pipe
from threading import Thread

from morphonet.tools import printv

from .MVC import computeCoordinates
from .utils import *

def computeCoordinatesForVertices(vertices_ids_min, vertices_ids_max, vertices, meshTriangles, meshVertices, meshNormals, verticesWeights, advancementPipe=None):
    monitorThisProcess = advancementPipe is not None
    if monitorThisProcess:
        i = 0
        ni = vertices_ids_max - vertices_ids_min

    for v in range(vertices_ids_min, vertices_ids_max):
        if monitorThisProcess:
            advancementPipe.send(str(int(100*i/ni)))
            i += 1
        computeCoordinates(vertices[v],
                            meshTriangles, meshVertices, meshNormals,
                            verticesWeights[v])

    if monitorThisProcess:
        advancementPipe.send("done")
        advancementPipe.close()

def computeCoordinatesForVertices_Shared(vertices_ids_min, vertices_ids_max, n_vertices, n_mesh_vertices, n_mesh_triangles, advancementPipe=None):
    # Get shared memory
    #    Input
    sh_vertices        = shared_memory.SharedMemory(name='vertices')
    sh_meshVertices    = shared_memory.SharedMemory(name='meshVertices')
    sh_meshTriangles   = shared_memory.SharedMemory(name='meshTriangles')
    sh_meshNormals     = shared_memory.SharedMemory(name='meshNormals')
    #    Output
    sh_verticesWeights = shared_memory.SharedMemory(name='verticesWeights')
    # Create ndarray of buffers (buffers are shared, using numpy is just a convenient way to read/write shared data)
    #    Input
    vertices        = np.ndarray((n_vertices, 3,),               dtype=np.float32, buffer=sh_vertices.buf)
    meshVertices    = np.ndarray((n_mesh_vertices, 3,),          dtype=np.float32, buffer=sh_meshVertices.buf)
    meshTriangles   = np.ndarray((n_mesh_triangles, 3,),         dtype=np.int32,   buffer=sh_meshTriangles.buf)
    meshNormals     = np.ndarray((n_mesh_triangles, 3,),         dtype=np.float32, buffer=sh_meshNormals.buf)
    #    Output
    verticesWeights = np.ndarray((n_vertices, n_mesh_vertices,), dtype=np.float32, buffer=sh_verticesWeights.buf)

    # Work
    computeCoordinatesForVertices(vertices_ids_min, vertices_ids_max, vertices, meshTriangles, meshVertices, meshNormals, verticesWeights, advancementPipe)

    # Close shared memory acess
    sh_verticesWeights.close()
    sh_vertices.close()
    sh_meshVertices.close()
    sh_meshTriangles.close()
    sh_meshNormals.close()

def parralelComputeCoordinates(vertices, meshVertices, meshTriangles, meshNormals, maxNumberOfProcess=None):
    if maxNumberOfProcess is None:
        maxNumberOfProcess=os.cpu_count()

    batch_size = int(len(vertices) / maxNumberOfProcess)

    verticesWeights = np.zeros((len(vertices), len(meshVertices)), dtype=np.float32)

    # https://docs.python.org/3/library/multiprocessing.shared_memory.html
    # Create shared memory
    #    Input
    sh_vertices        = shared_memory.SharedMemory(name="vertices",        create=True, size=vertices.nbytes)
    sh_meshVertices    = shared_memory.SharedMemory(name="meshVertices",    create=True, size=meshVertices.nbytes)
    sh_meshTriangles   = shared_memory.SharedMemory(name="meshTriangles",   create=True, size=meshTriangles.nbytes)
    sh_meshNormals     = shared_memory.SharedMemory(name="meshNormals",     create=True, size=meshNormals.nbytes)
    #    Output
    sh_verticesWeights = shared_memory.SharedMemory(name="verticesWeights", create=True, size=verticesWeights.nbytes)

    # Create ndarray of buffers (buffers are shared)
    bf_vertices        = np.ndarray(vertices.shape,        dtype=np.float32, buffer=sh_vertices.buf)
    bf_meshVertices    = np.ndarray(meshVertices.shape,    dtype=np.float32, buffer=sh_meshVertices.buf)
    bf_meshTriangles   = np.ndarray(meshTriangles.shape,   dtype=np.int32,   buffer=sh_meshTriangles.buf)
    bf_meshNormals     = np.ndarray(meshNormals.shape,     dtype=np.float32, buffer=sh_meshNormals.buf)
    bf_verticesWeights = np.ndarray(verticesWeights.shape, dtype=np.float32, buffer=sh_verticesWeights.buf)

    # Copy data into the buffers (using numpy is just a convenient way to read/write shared data)
    bf_verticesWeights.fill(0)

    bf_vertices[:]      = vertices[:]
    bf_meshVertices[:]  = meshVertices[:]
    bf_meshTriangles[:] = meshTriangles[:]
    bf_meshNormals[:]   = meshNormals[:]

    # Launch [maxNumberOfProcess] processes dividing almost equally the task (batch_size vertices per process, so floor(len(vertices) / maxNumberOfProcess))
    process = []
    advancementPipe_parent, advancementPipe_child = Pipe()
    for b in range(maxNumberOfProcess):
        tc = Process(target=computeCoordinatesForVertices_Shared,
                                      args=(b*batch_size, (b+1)*batch_size, len(vertices), len(meshVertices), len(meshTriangles),
                                            advancementPipe_child if b == 0 else None,))
        tc.start()
        process.append(tc)

    # Compute what's left of the task (rest of len(vertices) / maxNumberOfProcess vertices)
    vertices_ids_min = maxNumberOfProcess*batch_size
    vertices_ids_max = len(vertices)
    computeCoordinatesForVertices(vertices_ids_min, vertices_ids_max, bf_vertices, bf_meshTriangles, bf_meshVertices, bf_meshNormals, bf_verticesWeights)

    # Receive advancement
    percent = advancementPipe_parent.recv()
    while percent != "done":
        printv(f"Defomation step 1 : about {percent}% done", 0)
        percent = advancementPipe_parent.recv()
    advancementPipe_parent.close()
    # Wait all processes
    printv(f"Finishing work ...", 0)
    while len(process)>0:
        tc = process.pop(0)
        tc.join()
        tc.close()

    # copy results from buffer
    verticesWeights[:] = bf_verticesWeights[:]

    sh_verticesWeights.close()
    sh_vertices.close()
    sh_meshVertices.close()
    sh_meshTriangles.close()
    sh_meshNormals.close()

    sh_verticesWeights.unlink()
    sh_vertices.unlink()
    sh_meshVertices.unlink()
    sh_meshTriangles.unlink()
    sh_meshNormals.unlink()

    return verticesWeights

def rasterizeDeformationForTetrahedron(tetrahedrons_ids_min, tetrahedrons_ids_max,
                                       vertices, deformedVertices, tetrahedrons,
                                       originalData, deformedData, vsize, origin, modifiableCellIds, background,
                                       advancementPipe = None):
    """
    For each tetrahedron
        get vertices before and after deformation   (world coordinates)
        get vertices after deformation           in (image coordinate, but float)
        get AABB of vertices after deformation   in (image coordinate)
        For each voxel in the AABB                  (image coordinate)
            get the voxel position               in (world coordinate)
            if voxel position is in the tetrahedron (world coordinate)
                compute the barycentric coordinate of the voxel position in the deformed tetrahderon (barycentric coordinate)
                apply the barycentric coordinate in the original tetrahedron (world coordinate)
                get the image coordinate of that point (image coordinate)
                set the current voxel in the deformed image as the value of that point (image coordinate)
    """
    monitorThisProcess = advancementPipe is not None

    outsideTetrahedronPresent = False
    imageShape = list(originalData.shape)
    imageShapeMaxIndex = vecSub(imageShape, [1]*3)
    invvsize = vecInvert(vsize)

    if monitorThisProcess:
        i = 0
        ni = tetrahedrons_ids_max - tetrahedrons_ids_min

    for t_id in range(tetrahedrons_ids_min, tetrahedrons_ids_max):
        if monitorThisProcess:
            advancementPipe.send(str(int(100*i/ni)))
            i += 1

        t = tetrahedrons[t_id]
        v  = vertices[t]
        dv = deformedVertices[t]
        imgDv = (dv - origin) * invvsize

        aabbMinPrev =  imgDv.min(axis=0)     .astype(int)
        aabbMaxPrev = (imgDv.max(axis=0) + 1).astype(int)
        aabbMin, wasMinOutside = vecClampWithCheck(aabbMinPrev, [0]*3, imageShape)
        aabbMax, wasMaxOutside = vecClampWithCheck(aabbMaxPrev, [0]*3, imageShape)
        if wasMinOutside or wasMaxOutside:
            outsideTetrahedronPresent = True
        for vx in range(aabbMin[0], aabbMax[0]):
            for vy in range(aabbMin[1], aabbMax[1]):
                for vz in range(aabbMin[2], aabbMax[2]):
                    voxelPoint = (np.asarray([vx, vy, vz]) + 0.5) * vsize + origin
                            
                    coords = np.asarray(getTetrahedronBarycentricCoordinates(voxelPoint, dv))
                    if coords.min() > 0 and coords.max() < 1:
                        originalVoxelPointInWorld = np.matmul(coords, v)
                        originalVoxelPointInImage = ((originalVoxelPointInWorld - origin) * invvsize).astype(int)
                        orVoxel, wasOutside = vecClampWithCheck(originalVoxelPointInImage, [0]*3, imageShapeMaxIndex)
                        if wasOutside:
                            outsideTetrahedronPresent = True
                        value = originalData[orVoxel[0], orVoxel[1], orVoxel[2]]
                        if value not in modifiableCellIds:
                            value = background
                        if deformedData[vx, vy, vz] in modifiableCellIds:
                            deformedData[vx, vy, vz] = value

    if monitorThisProcess:
        advancementPipe.send("done")
        advancementPipe.close()

    return outsideTetrahedronPresent

def rasterizeDeformationForTetrahedrons_Shared(conn,
                                               tetrahedrons_ids_min, tetrahedrons_ids_max,
                                               n_vertices, n_tetrahedrons,
                                               image_shape, image_dtype, vsize, origin, modifiableCellIds, background,
                                               advancementPipe = None):
    # Get shared memory
    #    Input
    sh_vertices         = shared_memory.SharedMemory(name='vertices')
    sh_deformedVertices = shared_memory.SharedMemory(name='deformedVertices')
    sh_tetrahedrons     = shared_memory.SharedMemory(name='tetrahedrons')
    sh_originalData     = shared_memory.SharedMemory(name='originalData')
    #    Output
    sh_deformedData     = shared_memory.SharedMemory(name='deformedData')
    # Create ndarray of buffers (buffers are shared, using numpy is just a convenient way to read/write shared data)
    #    Input
    vertices         = np.ndarray((n_vertices, 3,),     dtype=np.float32,  buffer=sh_vertices.buf)
    deformedVertices = np.ndarray((n_vertices, 3,),     dtype=np.float32,  buffer=sh_deformedVertices.buf)
    tetrahedrons     = np.ndarray((n_tetrahedrons, 4,), dtype=np.int32,    buffer=sh_tetrahedrons.buf)
    #originalData     = deformation_image_class(np.ndarray(image_shape, dtype=image_dtype, buffer=sh_originalData.buf))
    ##    Output
    #deformedData     = deformation_image_class(np.ndarray(image_shape, dtype=image_dtype, buffer=sh_deformedData.buf))
    originalData     = np.ndarray(image_shape, dtype=image_dtype, buffer=sh_originalData.buf)
    #    Output
    deformedData     = np.ndarray(image_shape, dtype=image_dtype, buffer=sh_deformedData.buf)

    # Work
    outsideTetrahedronPresent = rasterizeDeformationForTetrahedron(
                                    tetrahedrons_ids_min, tetrahedrons_ids_max,
                                    vertices, deformedVertices, tetrahedrons,
                                    originalData, deformedData, vsize, origin, modifiableCellIds, background,
                                    advancementPipe)

    # Send values
    conn.send(outsideTetrahedronPresent)
    conn.close()

    # Close shared memory acess
    #    Input
    sh_vertices.close()
    sh_deformedVertices.close()
    sh_tetrahedrons.close()
    sh_originalData.close()
    #    Output
    sh_deformedData.close()

def parralelRasterizeDeformation(originalData, tetrahedralVolume, deformedData, maxNumberOfProcess=None):
    """
    Launches maxNumberOfProcess process to rasterize the deformation
    The final image is deformedData deformedData
    return True if a Tetrahedra is present outside of the image
    """
    if maxNumberOfProcess is None:
        maxNumberOfProcess = os.cpu_count()

    # Compute aabb of volume before and after deformation joined.
    # Used to copy less data to shared memory
    volume_aabbMin = np.min([tetrahedralVolume.bbmin, tetrahedralVolume.deformedbbmin], axis=0)
    volume_aabbMax = np.max([tetrahedralVolume.bbmax, tetrahedralVolume.deformedbbmax], axis=0)

    volume_aabbMin = np.asarray( vecClamp((volume_aabbMin - 1).astype(int), [0]*3, originalData.shape) )
    volume_aabbMax = np.asarray( vecClamp((volume_aabbMax + 2).astype(int), [0]*3, originalData.shape) )

    background = originalData.background
    originalDataInAABB = originalData[volume_aabbMin[0]:volume_aabbMax[0], volume_aabbMin[1]:volume_aabbMax[1], volume_aabbMin[2]:volume_aabbMax[2]]
    deformedDataInAABB = deformedData[volume_aabbMin[0]:volume_aabbMax[0], volume_aabbMin[1]:volume_aabbMax[1], volume_aabbMin[2]:volume_aabbMax[2]]
    
    # Todo : Remove ! Tetrahderons should be sufficiently outside of the deformation
    #deformedDataInAABB[np.where(np.isin(deformedDataInAABB, list(deformedData.modifiableCellIds)))] = deformedData.background

    imageShapeInAABB = originalDataInAABB.shape
    originalDataInAABB_origin = originalData.origin + volume_aabbMin * originalData.vsize

    batch_size = int(len(tetrahedralVolume.tetrahedrons) / maxNumberOfProcess)

    image_dtype = originalData.dtype
    
    # Create shared memory
    sh_vertices         = shared_memory.SharedMemory(name='vertices',         create=True, size=tetrahedralVolume.vertices.nbytes)
    sh_deformedVertices = shared_memory.SharedMemory(name='deformedVertices', create=True, size=tetrahedralVolume.deformedVertices.nbytes)
    sh_tetrahedrons     = shared_memory.SharedMemory(name='tetrahedrons',     create=True, size=tetrahedralVolume.tetrahedrons.nbytes)
    sh_originalData     = shared_memory.SharedMemory(name='originalData',     create=True, size=originalDataInAABB.nbytes)
    sh_deformedData     = shared_memory.SharedMemory(name='deformedData',     create=True, size=deformedDataInAABB.nbytes)

    # Create ndarray of buffers (buffers are shared)
    bf_vertices         = np.ndarray(tetrahedralVolume.vertices.shape,         dtype=np.float32,  buffer=sh_vertices.buf)
    bf_deformedVertices = np.ndarray(tetrahedralVolume.deformedVertices.shape, dtype=np.float32,  buffer=sh_deformedVertices.buf)
    bf_tetrahedrons     = np.ndarray(tetrahedralVolume.tetrahedrons.shape,     dtype=np.int32,    buffer=sh_tetrahedrons.buf)
    bf_originalData     = np.ndarray(imageShapeInAABB,                         dtype=image_dtype, buffer=sh_originalData.buf)
    bf_deformedData     = np.ndarray(imageShapeInAABB,                         dtype=image_dtype, buffer=sh_deformedData.buf)

    # Copy data into the buffers (using numpy is just a convenient way to read/write shared data)
    bf_vertices[:]         = tetrahedralVolume.vertices[:]
    bf_deformedVertices[:] = tetrahedralVolume.deformedVertices[:]
    bf_tetrahedrons[:]     = tetrahedralVolume.tetrahedrons[:]
    bf_originalData[:]     = originalDataInAABB[:]
    bf_deformedData[:]     = deformedDataInAABB[:]

    # Launch [maxNumberOfProcess] processes dividing almost equally the task (batch_size vertices per process, so floor(len(tetrahedrons) / maxNumberOfProcess))
    process = [] # (parent_conn, process)
    advancementPipe_parent, advancementPipe_child = Pipe()
    for b in range(maxNumberOfProcess):
        printv(f"Defomation step 2 : starting ({b+1} / {maxNumberOfProcess})", 0)
        parent_conn, child_conn = Pipe()
        tc = ( parent_conn, Process(target=rasterizeDeformationForTetrahedrons_Shared,
                                            args=(child_conn, 
                                                  b*batch_size, (b+1)*batch_size, 
                                                  len(tetrahedralVolume.vertices), len(tetrahedralVolume.tetrahedrons), 
                                                  imageShapeInAABB, image_dtype, deformedData.vsize, originalDataInAABB_origin, deformedData.modifiableCellIds, background,
                                                  advancementPipe_child if b==0 else None, )) )
        tc[1].start()
        process.append(tc)
    
    printv(f"Defomation step 2 : Working...", 0)
    # Compute what's left of the task (rest of len(tetrahedrons) / maxNumberOfProcess tetrahedrons)
    tetrahedrons_ids_min = maxNumberOfProcess*batch_size
    tetrahedrons_ids_max = len(tetrahedralVolume.tetrahedrons)
    outsideTetrahedronPresent = rasterizeDeformationForTetrahedron(
                                    tetrahedrons_ids_min, tetrahedrons_ids_max,
                                    bf_vertices, bf_deformedVertices, bf_tetrahedrons,
                                    bf_originalData, bf_deformedData, deformedData.vsize, originalDataInAABB_origin, deformedData.modifiableCellIds, background)
    # Receive advancement
    previsousPercent = -1
    percent = advancementPipe_parent.recv()
    while percent != "done":
        if percent != previsousPercent:
            printv(f"Defomation step 2 : about {percent}% done", 0)
        previsousPercent = percent
        percent = advancementPipe_parent.recv()
    advancementPipe_parent.close()
    # Wait all processes
    while len(process)>0:
        printv(f"Defomation step 2 : Finishing work ({maxNumberOfProcess - len(process)}/{maxNumberOfProcess})", 0)
        tc = process.pop(0)
        # receive pipe infos
        outsideTetrahedronPresent |= tc[0].recv()
        tc[0].close()
        # End process
        tc[1].join()
        tc[1].close()

    # copy results from buffer
    deformedDataInAABB[:] = bf_deformedData[:]

    return outsideTetrahedronPresent