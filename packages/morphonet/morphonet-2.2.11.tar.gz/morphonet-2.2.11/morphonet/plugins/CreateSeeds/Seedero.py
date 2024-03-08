# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ..functions import  get_borders
from ...tools import printv


class Seedero(MorphoPlugin):
    """ This plugin generates seeds that can be used in other (mainly segmentation) algorithms.
    This plugin applies multiple erosion steps of each selected object, until objects can be separated into multiple parts.
    Then a seed is at the barycenter of each individual sub-part.

    Parameters
    ----------
    minimum volume : int, default : 1000
        The minimal volume of each individual part that will be kept to generate a seed, after the erosion

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_parent("Create Seeds")
        self.set_icon_name("Seedero.png")
        self.set_image_name("Seedero.png")
        self.set_name("Seedero : Create seeds from the erosion of selected objects (without intensity images)")
        self.add_inputfield("minimum volume", default=1000)
        self.set_description( "This plugin generates seeds that can be used in other (mainly segmentation) algorithms. \n"
                              "This plugin applies multiple erosion steps of each selected object, until objects can be separated into multiple parts. \n"
                              "Then a seed is at the barycenter of each individual sub-part. \n \n"
                              "Parameters : \n \n"
                              "- minimum volume (numeric,default:1000) : The minimal volume of each individual part that"
                              " will be kept to generate a seed, after the erosion")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects,backup=False):
            return None

        from skimage.morphology import binary_erosion
        from skimage.measure import label

        #Treshold of volume of cells to consider ok to get a seed
        min_vol = int(self.get_inputfield("minimum volume"))
        import numpy as np
        nbc = 0
        for channel in dataset.get_channels(objects):  # For each channels in selected object
            for t in dataset.get_times(objects):  # For each time point in cells labeled
                data = dataset.get_seg(t, channel)  #  load the segmentation in memory
                for o in dataset.get_objects_at(objects, t): #For each cell
                    cellCoords = dataset.np_where(o) #Get cells coordinate
                    printv('Look for object ' + str(o.get_name()) + " with " + str(len(cellCoords[0])) + " voxels ",0) #compute a mask around the cell
                    if len(cellCoords[0])>0:
                        xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data, cellCoords)
                        cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
                        omask = np.zeros(cellShape, dtype=bool)
                        omask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True
                        mask = np.copy(omask)
                        new_objects=[1]
                        iteration=0
                        while len(new_objects)>=1 and len(new_objects)<2:
                            mask = binary_erosion(mask)  #apply the erosion iteration on the mask
                            splitted = label(mask) #Determine the number of shards the cells has been split into due to erosion
                            new_objects = np.unique(splitted)
                            new_objects = new_objects[new_objects != dataset.background] #Get the list of cell shards except background
                            printv("at iteration "+str(iteration)+" found objects "+str(new_objects), 1)
                            iteration+=1

                    nbc = 0
                    if len(new_objects)>=2: #If the cell has been split at least in 2
                        for no in new_objects:  #For each shard
                            coords = np.where(splitted == no)  #Get its coordinates
                            #If it's too small depending on the treshold , do not create a seed
                            if len(coords[0]) <= min_vol:
                                printv("found a small cell with  only " + str(len(coords[0])) + " voxels",0)
                            else:
                                printv("add a cell with " + str(len(coords[0])) + " voxels",0)
                                cc = np.uint16([coords[0].mean()+xmin, coords[1].mean()+ymin, coords[2].mean()+zmin]) #Get cell barycenter
                                dataset.add_seed(cc) #Add seed at this barycenter point
                                nbc += 1
                    #If didn't find two shards big enough to get a seed, warn the user
                    if nbc <= 2:
                        printv("not splittable ",0)
        #Send back to morphonet
        printv("Found " + str(nbc) + " new seeds",0)
        self.restart()

