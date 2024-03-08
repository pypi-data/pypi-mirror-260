import numpy as np
import os

from morphonet.tools import printv


def _centerInShape(c, s):
    if c[0] < 0 or c[1] < 0 or c[2] < 0 or c[0] >= s[0] or c[1] >= s[1] or c[2] >= s[2]:
        return False
    return True


def shift_bbox(bbox,border=2,shape=None):
    newbox=np.array([bbox[0]-border,bbox[3]+border,bbox[1]-border,bbox[4]+border,bbox[2]-border,bbox[5]+border])
    if shape is not None:
        for i in [0,2,4]: newbox[i]=max(0,newbox[i])
        newbox[1] = min(shape[0], newbox[1])
        newbox[3] = min(shape[1], newbox[3])
        newbox[5] = min(shape[2], newbox[5])
    return newbox[0],newbox[1],newbox[2],newbox[3],newbox[4],newbox[5]


def get_borders(data,cellCoords,border=4):
    xmin=max(0,cellCoords[0].min()-border)
    xmax=min(data.shape[0],cellCoords[0].max()+border)
    ymin=max(0,cellCoords[1].min()-border)
    ymax=min(data.shape[1],cellCoords[1].max()+border)
    zmin=max(0,cellCoords[2].min()-border)
    zmax=min(data.shape[2],cellCoords[2].max()+border)
    return xmin,xmax,ymin,ymax,zmin,zmax


def force_apply_new_label(data,xmin,ymin,zmin,labelw,minVol=0,minimal_count=2):
    import numpy as np
    labels=np.unique(labelw)
    labels=labels[labels!=0] #Remove Background
    if len(labels)<minimal_count:
        print(" ---> no new labels : not enough labels")
        return data,[]
    #First We check of all coords have the required minimum of size
    #The biggest cell get the same label
    newIds=[]
    lastID=int(data.max())+1
    for l in labels:
        new_coords=np.where(labelw==l)
        if len(new_coords[0])>=minVol:
            data[new_coords[0]+xmin,new_coords[1]+ymin,new_coords[2]+zmin]=lastID
            print('     ----->>>>>  Create a new object '+str(lastID)+ " with "+str(len(new_coords[0]))+ " voxels")
            newIds.append(lastID)
            lastID += 1
        else:
            print("     ----->>>>>  Do not create with "+str(len(new_coords[0]))+ " voxels")
    return data,newIds


def apply_new_label(data,xmin,ymin,zmin,labelw,minVol=0,minimal_count=2):
    import numpy as np
    labels=np.unique(labelw)
    labels=labels[labels!=0] #Remove Background
    if len(labels)<minimal_count:
        print(" ---> no new labels : not enough labels")
        return data,[]
    #First We check of all coords have the required minimum of size
    #The biggest cell get the same label
    #TODO THIS TYPE OF METHOD IS REALLY FASTER
    # ids, counts = np.unique(labels, return_counts=True)
    # BigestL=ids[counts==counts[1:].max()][0]
    Labelsize={}
    Bigest=0
    BigestL=-1
    for l in labels:
        Labelsize[l]=len(np.where(labelw==l)[0])
        if Labelsize[l]>Bigest:
            Bigest=Labelsize[l]
            BigestL=l

    labels=labels[labels!=BigestL]
    newIds=[]
    lastID=int(data.max())+1
    for l in labels:
        new_coords=np.where(labelw==l)
        if len(new_coords[0])>=minVol:
            data[new_coords[0]+xmin,new_coords[1]+ymin,new_coords[2]+zmin]=lastID
            print('     ----->>>>>  Create a new object '+str(lastID)+ " with "+str(len(new_coords[0]))+ " voxels")
            newIds.append(lastID)
            lastID += 1
        else:
            print("     ----->>>>>  Do not create with "+str(len(new_coords[0]))+ " voxels")
    return data,newIds


def is_in_image(coord,shape):
    for i in range(3):
        if np.uint16(coord[i]) < 0:
            return False
        if np.uint16(coord[i]) >= shape[i]:
            return False
    return True

def get_seeds_in_image(dataset,seeds):
    center = dataset.get_center()
    voxel_size = dataset.get_current_voxel_size()
    corrected_seeds = [np.int32([(s[0]/voxel_size[0])+center[0],(s[1]/voxel_size[1])+center[1],(s[2]/voxel_size[2])+center[2]]) for s in seeds]
    return corrected_seeds

def get_barycenter(data,cell_id):
    coords = np.where(data == cell_id)
    return np.uint16([coords[0].mean(),coords[1].mean(),coords[2].mean()])

def get_seed_at(seeds,xmin,ymin,zmin):
    nseeds=[]
    for seed in seeds:
        nseed = [seed[0] - xmin, seed[1] - ymin, seed[2] - zmin]
        nseeds.append(nseed)
    return nseeds

def get_seeds_in_mask(seeds,mask):
    seeds_in_cell_mask=[]
    for seed in seeds:
        if seed[0] >= 0 and seed[1] >= 0 and seed[2] >= 0 and seed[0] < mask.shape[0] and seed[1] < mask.shape[1] and \
                seed[2] < mask.shape[2]:
            if mask[seed[0], seed[1], seed[2]]:
                seeds_in_cell_mask.append(seed)
    return seeds_in_cell_mask


#Local Redefinition of some tools
def watershed(data,markers=None,mask=None):
    from skimage.segmentation import watershed as sk_watershed
    return  sk_watershed(data, markers=markers, mask=mask)

def gaussian(data, sigma=2, preserve_range=False):
    from skimage.filters import gaussian as sk_gaussian
    return sk_gaussian(data,sigma=sigma,preserve_range=preserve_range)


def get_torch_device():
    from cellpose import core
    import torch

    which = "CPU"
    if core.use_gpu():  which = "GPU"
    device = None
    if torch.backends.mps.is_available():
        printv("torch metal available on silicon architecture ",1)
        which = "GPU"
        device = torch.device("mps")
    return which,device


def read_time_points(time_points,t):
    time_points = time_points.strip()
    times = []
    try:
        if time_points == "current":
            times.append(t)
        elif time_points.find(":") > 0:
            tabtime = time_points.split(":")
            for t in range(int(tabtime[0]), int(tabtime[1]) + 1): times.append(t)
        elif time_points.find(",") > 0:
            for elt in time_points.split(","):
                times.append(int(elt))
        else:
            times.append(int(time_points))
    except Exception as e:
        printv("Error time points are in wrong format",0)
    return times
