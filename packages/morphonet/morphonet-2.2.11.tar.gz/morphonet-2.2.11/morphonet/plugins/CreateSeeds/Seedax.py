# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.plugins.functions import is_in_image
from morphonet.tools import printv


class Seedax(MorphoPlugin):
    """This plugin generates seeds that can be used in other plugins (mainly watershed segmentation).
    The longest axis of the segmentation shape is computed, and then split in 2. At ?  and ? of the axis,  2 seeds are
    created inside the selected objects.


    Parameters
    ----------
    The selected or labeled objects on MorphoNet
    elongation factor : int, default :8
        The elongation factor applied to the objects different axis to compute the distance (>=0)

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_parent("Create Seeds")
        self.set_icon_name("Seedax.png")
        self.set_image_name("Seedax.png")
        self.set_name("Seedax : Create Seeds on the long axis of the selected objects (without intensity images)")
        self.add_inputfield("number of seeds", default=2)
        self.set_description( "This plugin generates seeds that can be used in other plugins (mainly watershed segmentation).\n "
                              "The longest axis of the segmentation shape is computed, and then split in 2. At 1/3  and 2/3 of the axis,  "
                              "2 seeds are created inside the selected objects. \n \n"
                              "Parameters : \n \n"
                              "- number of seeds (numeric,default:2) : The number of seeds in the long axis")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, backup=False):
            return None
        #Get user elongation factor for the long axis found, for the seed positioning
        number_of_seeds = int(self.get_inputfield("number of seeds"))
        import numpy as np
        from scipy.spatial.distance import cdist
        nbc = 0
        for channel in dataset.get_channels(objects):  # For each channels in selected object
            for t in dataset.get_times(objects): # For each time point in cells labeled
                data = dataset.get_seg(t,channel) #Forces to load the segmentation in memory
                for o in dataset.get_objects_at(objects, t): # For each cell to this time point
                    bbox = dataset.get_regionprop("bbox", o) #Get The Boox
                    databbox= data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                    totalsize=databbox.shape[0]*databbox.shape[1]*databbox.shape[2]
                    reduce=1
                    while totalsize>200000: #Reduce the bounding box size (to avoid computing issue
                        databbox=databbox[::2,::2,::2]
                        totalsize=databbox.shape[0]*databbox.shape[1]*databbox.shape[2]
                        reduce+=1

                    coords =np.where(databbox==o.id) #Get the cell coordinates
                    printv('look for  object ' + str(o.get_name()) + " with ~ " + str(reduce*len(coords[0])) + " voxels ",0)

                    vT = np.zeros([len(coords[0]), len(coords)])
                    for s in range(len(coords)):   vT[:, s] = coords[s]  #Create distance matrix for each axis
                    dist = cdist(vT, vT) #Compute distance matrix of the image
                    maxi = dist.max() #Get the maximum distance from the matrix
                    coords_maxi = np.where(dist == maxi) #Find the corresponding coordinates
                    if len(coords_maxi[0]) >= 2:
                        ipt1 = coords_maxi[0][0]
                        ipt2 = coords_maxi[0][1]
                        #Get the this long distance according to the factor of elongation
                        pt1 = np.array([coords[0][ipt1], coords[1][ipt1], coords[2][ipt1]])
                        pt2 = np.array([coords[0][ipt2], coords[1][ipt2], coords[2][ipt2]])
                        v = pt2 - pt1
                        # Divide the axis in severage portion
                        vd = v / (number_of_seeds + 1)
                        for s in range(number_of_seeds):
                            seed = np.int32((pt1 + vd * (1+s)) * reduce)
                            for i in range(3): seed[i]+=bbox[i]
                            if is_in_image(seed, data.shape):
                                dataset.add_seed(seed)
                                nbc += 1
                            else:
                                printv("Seed "+str(seed)+" is not in the image",1)




        printv(" --> Found " + str(nbc) + " new seeds",0)
        self.restart()

