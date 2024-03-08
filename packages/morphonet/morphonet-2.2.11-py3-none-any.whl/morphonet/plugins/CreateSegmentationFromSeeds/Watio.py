# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np
from ..functions import  get_borders, apply_new_label,get_seed_at,get_seeds_in_mask,get_seeds_in_image,watershed,gaussian,get_barycenter
from ...tools import printv

class Watio(MorphoPlugin):
    """ This plugin creates new objects using a watershed algorithm from seed generated using a plugin or manually
    placed in the MorphoNet Viewer inside selected object. The watershed algorithm generates new objects based on
    the intensity image and replaces the selected objects.  If the new generated objects are under the volume threshold
    defined by the user, the object is not created.


    Parameters
    ----------
    The selected or labeled objects on MorphoNet
    sigma : int, default :2
        The standard deviation for the Gaussian kernel when sigma>0, the plugin first applies a gaussian filter on the
        intensity image. (>=0)
    minimum volume: int, default : 1000
        The minimal volume (in number of voxels) allowed for the new objects to be created (>=0)
    Seeds: Coordinate List
        List of seeds added on the MorphoNet Window

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Watio.png")
        self.set_image_name("Watio.png")
        self.set_name("Watio : Perform a watershed segmentation on intensity images on selected objects")
        self.add_inputfield("Membrane Channel", default=0)
        self.add_inputfield("sigma", default=2)
        self.add_inputfield("minimum volume", default=1000)
        self.add_coordinates("Add a Seed")
        self.set_parent("Create Segmentation from Seeds")
        self.set_description("his plugin creates new objects using a watershed algorithm from seed generated using a "
                             "plugin or manually placed in the MorphoNet Viewer inside selected object. The watershed "
                             "algorithm generates new objects based on the intensity image and replaces the selected "
                             "objects.  If the new generated objects are under the volume threshold defined by the user,"
                             " the object is not created.")

    # Perform a watershed on a list of seed
    def _water_on_seed(self, dataset, t, seeds, objects, rawdata):
        printv("perform watershed at " + str(t),1)

        new_seeds = []  # Compute seeds from the new cells barycenter, for next time points
        for channel in dataset.get_channels(objects):
            cells_updated = []
            data = dataset.get_seg(t,channel)  # Get the segmentation at t
            for o in dataset.get_objects_at(objects,t):#For each object, get its coord
                cellCoords = np.where(data == o.id)
                printv('Look in object ' + str(o.get_name()) + " with " + str(len(cellCoords[0])) + " voxels ",0)
                xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data, cellCoords)#compute bounding box and create a mask around it
                cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
                mask = np.zeros(cellShape, dtype=bool)
                mask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True

                nseeds = get_seed_at(seeds, xmin, ymin, zmin) #Get the seeds that are in the mask only
                seeds_in_cell_mask = get_seeds_in_mask(nseeds, mask)
                #We need 2 seeds at least to split a cell
                if len(seeds_in_cell_mask) < 2:  # If we have some seeds in this mask
                    printv(str(len(seeds_in_cell_mask)) + "  is not enough  seeds in this mask",0)
                else:
                    printv("Found " + str(len(seeds_in_cell_mask)) + " seeds in this mask",0)
                    markers = np.zeros(mask.shape, dtype=np.uint16)#Create markers (seed) images for watershed, with specific ids for each seed
                    newId = 1
                    for seed in seeds_in_cell_mask:  # For Each Seeds ...
                        markers[seed[0], seed[1], seed[2]] = newId
                        newId += 1

                    seed_preimage = rawdata[xmin:xmax + 1, ymin:ymax + 1, zmin:zmax + 1] #Crop raw image around the box
                    #If we need to smooth, do it
                    if self.s_sigma > 0.0:
                        printv("Perform gaussian with sigma=" + str(self.s_sigma) + " at " + str(t),0)
                        seed_preimage = gaussian(seed_preimage, sigma=self.s_sigma, preserve_range=True)
                    # apply watershed on mask from seeds, using raw images as source
                    printv(" --> Process watershed ",0)
                    labelw = watershed(seed_preimage, markers=markers, mask=mask)

                    data, c_newIds = apply_new_label(data, xmin, ymin, zmin, labelw, minVol=self.min_vol) #Apply the labels to the segmentations , if volume is ok

                    if len(c_newIds) > 0: #if we created new cells, add them to refresh in morphonet
                        c_newIds.append(o.id)
                        cells_updated += c_newIds

            if len(cells_updated) > 0:
                dataset.set_seg(t, data, channel=channel,cells_updated=cells_updated) # Set segmentation in MorphoNet
                for c in cells_updated:
                    new_seeds.append(get_barycenter(data,c))

        return new_seeds

    def _water_time(self, dataset, t, seeds, objects):

        rawdata = dataset.get_raw(t,self.membrane_channel)#Get the raw data at t
        if rawdata is None:
            return
        new_seeds = self._water_on_seed(dataset, t, seeds, objects, rawdata)#Apply watershed and get the new cells barycenters as next seeds
        if len(new_seeds) > 0 and t+1 in self.times: #Continue if we're in the time is in working times, and that we generated seeds
            self._water_time(dataset, t + 1, new_seeds, objects)


    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects):
            return None

        self.s_sigma = int(self.get_inputfield("sigma")) # Get the value of the smoothing  from morphonet
        self.min_vol = int(self.get_inputfield("minimum volume")) #Get the min volume for cell to create from morphonet
        seeds = self.get_coordinates("Add a Seed") #get the seeds position from morphonet
        self.membrane_channel = int(self.get_inputfield("Membrane Channel"))

        if len(seeds) == 0: #If no seeds, nothing to do
            printv("no seeds for watershed",0)

        else:  #Else propagate watershed in time from seeds
            printv("Found " + str(len(seeds)) + " seeds ",0)
            seeds=get_seeds_in_image(dataset,seeds)
            self.times=dataset.get_times(objects)
            self._water_time(dataset, self.times[0], seeds, objects)
        self.restart()




