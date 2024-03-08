# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np
from ..functions import _centerInShape, get_seeds_in_image, watershed
from ...tools import printv


class Wata(MorphoPlugin):
    """ This plugin creates new objects using a watershed algorithm from seed generated using a plugin or placed in the
    MorphoNet Viewer.  The watershed algorithm generates new objects based on the segmentation image for each seed
    inside a box that is not in another object.  If the new generated objects are under the volume threshold defined by
    the user, the object is not created.


    Parameters
    ----------
    minimum volume: int, default : 1000
        The minimal volume (in number of voxels) allowed for the new objects to be created (>=0)
    box size : int , defaut : 50
        Boundaries (in number of voxel) of working area around a seed to generate a new object
    Seeds: Coordinate List
        List of seeds added on the MorphoNet Window

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Wata.png")
        self.set_image_name("Wata.png")
        self.set_name("Wata : Perform a watershed segmentation (without intensity images and without selected objects)")
        self.add_inputfield("Segmentation Channel", default=0)
        self.add_inputfield("minimum volume", default=1000)
        self.add_inputfield("box size", default=50)
        self.add_coordinates("Add a Seed")
        self.set_parent("Create Segmentation from Seeds")
        self.set_description(" This plugin creates new objects using a watershed algorithm from seed generated  using a "
                             "plugin or placed in theMorphoNet Viewer.  The watershed algorithm generates new objects "
                             "based on the segmentation image for each seedinside a box that is not in another object."
                             "If the new generated objects are under the volume threshold defined by the user, "
                             "the object is not created.")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        segmentation_channel = int(self.get_inputfield("Segmentation Channel"))
        min_vol = int(self.get_inputfield("minimum volume")) # User chosen min volume accepted as a cell to segment
        box_size = int(self.get_inputfield("box size")) # Size of the bounding box around to work around the seeds


        data = dataset.get_seg(t)  # Load segmentation in memory
        seeds = self.get_coordinates("Add a Seed") # Get list of seeds coordinates from MorphoNet seed system
        if len(seeds) == 0:
            printv("no seeds for watershed", 0)
            return None
        printv("Found " + str(len(seeds)) + " seeds ", 1)

        dataset.get_center(data)# Compute center of the segmentation
        seeds = get_seeds_in_image(dataset, seeds) # Get coordinates of the seeds in the image (coordinates in morphonet != coordinates in images)
        new_seed = []

        for seed in seeds: # For each seed
            if _centerInShape(seed, data.shape): # if seed is in image
                olid = data[seed[0], seed[1], seed[2]]# Get the cell id at the seed
                if olid == dataset.background: # if it's background , it will be used for segmentation
                    new_seed.append(seed)
                    printv("add seed " + str(seed), 1)
                else:# else we skip it
                    printv("remove this seed " + str(seed) + " which already correspond to cell " + str(olid), 1)
            else:
                printv("this seed " + str(seed) + " is out of the image", 1)


        if len(new_seed) == 0: # If no seed found, we can stop
            self.restart()
            return None

        # Compute a box around the seed, according to the box size given by user
        if box_size > 0:
            seedsa = np.array(new_seed)
            box_coords = {}
            for i in range(3):
                mi = max(0, seedsa[:, i].min() - box_size)
                ma = min(data.shape[i], seedsa[:, i].max() + box_size)
                box_coords[i] = [mi, ma]

            # Crop the data around the box
            ndata = data[box_coords[0][0]:box_coords[0][1], box_coords[1][0]:box_coords[1][1],
                    box_coords[2][0]:box_coords[2][1]]

            # Replace the seed in the box
            box_seed = []
            for s in new_seed:
                box_seed.append([s[0] - box_coords[0][0], s[1] - box_coords[1][0], s[2] - box_coords[2][0]])
            new_seed = box_seed
        else:
            ndata = data

        # mark the box sides with background in the mask image
        markers = np.zeros(ndata.shape, dtype=np.uint16)
        markers[0, :, :] = 1
        markers[:, 0, :] = 1
        markers[:, :, 0] = 1
        markers[ndata.shape[0] - 1, :, :] = 1
        markers[:, ndata.shape[1] - 1, :] = 1
        markers[:, :, ndata.shape[2] - 1] = 1

        # Mark the seeds in the mask image with a separate id for each
        newId = 2
        for seed in new_seed:
            markers[seed[0], seed[1], seed[2]] = newId
            newId += 1

        # Create a new mask images, , with background at true
        mask = np.ones(ndata.shape, dtype=bool)
        mask[ndata != dataset.background] = False

        #watershed from seeds
        printv("Process watershed with " + str(len(new_seed)) + " seeds", 0)
        labelw = watershed(mask, markers=markers, mask=mask)

        #Compute the identifiers of the cells created during watershed
        cMax = data.max() + 1
        nbc = 0
        new_ids = np.unique(labelw)
        new_ids = new_ids[new_ids > 1]  #Do not create cells at the bounding box borders
        # If we created an object
        if len(new_ids) > 0:
            printv("Combine new objects", 1)
            cells_updated = []
            for new_id in new_ids: #For each id of cell created by watershed
                newIdCoord = np.where(labelw == new_id) #Get its coordinates
                if len(newIdCoord[0]) > min_vol: #If the cell is big enough compared to user volume threshold
                    if box_size > 0: #Get the cell coord in the segmentation image
                        newIdCoord = (newIdCoord[0] + box_coords[0][0], newIdCoord[1] + box_coords[1][0],
                                      newIdCoord[2] + box_coords[2][0])

                    data[newIdCoord] = cMax + nbc #Mark it as the next id in the images
                    printv("add object " + str(nbc + cMax) + ' with  ' + str(len(newIdCoord[0])) + " voxels", 0)
                    cells_updated.append(cMax + nbc)#Add cell to refresh in morphonet
                    nbc += 1
                else:
                    printv("remove object with  " + str(len(newIdCoord[0])) + " voxels", 0)
            #Save segmentation
            if len(cells_updated) > 0:
                dataset.set_seg(t, data, channel=segmentation_channel, cells_updated=cells_updated)
        printv(" --> Found  " + str(nbc) + " new labels", 0)
        #Send data to MorphoNet
        self.restart()
