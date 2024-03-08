# -*- coding: latin-1 -*-
from skimage.transform import resize

from morphonet.plugins import MorphoPlugin
import numpy as np
from ..functions import get_borders, apply_new_label,get_seed_at,get_seeds_in_mask,get_seeds_in_image,watershed,get_barycenter
from morphonet.tools import imsave
from ...tools import printv

class Wato(MorphoPlugin):
    """ This plugin creates new objects using a watershed algorithm from seed generated  using a plugin or placed in the
     MorphoNet Viewer inside selected objects. The watershed algorithm generates new objects based on the segmentation
     image for each seed and replaces the selected objects.  If the new generated objects are under the volume threshold
     defined by the user, the object is not created.

    Parameters
    ----------
    The selected or labeled objects on MorphoNet
    minimum volume: int, default : 1000
       The minimal volume (in number of voxels) allowed for the new objects to be created (>=0)
    Seeds: Coordinate List
        List of seeds added on the MorphoNet Window

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Wato.png")
        self.set_image_name("Wato.png")
        self.set_name("Wato : Perform a watershed segmentation on selected objects  (without intensity images)")
        self.add_inputfield("minimum volume", default=1000)
        self.add_toggle("rescale with voxel size", default=True)
        self.add_coordinates("Add a Seed")
        self.set_parent("Create Segmentation from Seeds")
        self.set_description("This plugin creates new objects using a watershed algorithm from seed generated  using a "
                             "plugin or placed in the MorphoNet Viewer inside selected objects. The watershed algorithm "
                             "generates new objects based on the segmentation image for each seed and replaces the "
                             "selected objects.  If the new generated objects are under the volume threshold defined by "
                             "the user, the object is not created.")

    # Perform a watershed on a list of seed
    def _water_on_seed(self, dataset, t, data, seeds, objects):
        printv("Perform watershed at " + str(t),0)
        cells_updated = []
        #For each object
        for o in dataset.get_objects_at(objects,t):
            #Get its coordinates
            cellCoords = np.where(data == o.id)
            printv('Look in object ' + str(o.get_name()) + " with " + str(len(cellCoords[0])) + " voxels ",0)
            #Get its bounding box and create a mask from the box
            xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data, cellCoords)
            cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
            mask = np.zeros(cellShape, dtype=bool)
            mask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True
            # Only retrieve seeds in the box
            nseeds=get_seed_at(seeds,xmin,ymin,zmin)
            seeds_in_cell_mask = get_seeds_in_mask(nseeds,mask)
            #Stop watershed for this object if we don't have enough seeds to split
            if len(seeds_in_cell_mask) < 2: # If we have some seeds in this mask
                printv(str(len(seeds_in_cell_mask)) + "  is not enough  seeds in this mask",0)
            else:
                printv(str(len(seeds_in_cell_mask))  + " seeds in this mask",0)
                #Place all seeds in watershed markers image, with unique ids
                markers = np.zeros(mask.shape, dtype=np.uint16)
                newId = 1
                for seed in seeds_in_cell_mask:  # For Each Seeds ...
                    markers[seed[0] , seed[1], seed[2] ] = newId
                    newId+=1

                printv("Process watershed ",0)
                if self.voxel_size_toggle:
                    vx=dataset.get_voxel_size(t)
                    orignal_shape=mask.shape
                    vx=[x/min(vx) for x in vx] #[1,1,10]
                    new_shape=np.uint16([mask.shape[0]*vx[0],mask.shape[1]*vx[1],mask.shape[2]*vx[2]])
                    mask=resize(mask,new_shape,preserve_range=True,order=0)
                    markers = resize(markers, new_shape,preserve_range=True, order=0)

                #Watershed on the mask
                labelw = watershed(255-mask, markers=markers, mask=mask)
                if self.voxel_size_toggle:
                    labelw=resize(labelw,orignal_shape,preserve_range=True,order=0)

                #Apply the cells in the segmentation if volumes is big enough
                data, c_newIds = apply_new_label(data, xmin, ymin, zmin, labelw, minVol=self.min_vol)
                #Store the new created cells to propagate cells barycenter
                if len(c_newIds) > 0:
                    c_newIds.append(o.id)
                    cells_updated+=c_newIds

        if len(cells_updated) > 0:
            #Apply the segmentation
            dataset.set_seg(t, data, cells_updated=cells_updated)
            #New seeds are created cells barycenters
            new_seeds=[]
            for c in cells_updated:
                new_seeds.append(get_barycenter(data,c))
            return new_seeds
        return []


    def _water_time(self, dataset, t, seeds, objects):
        #Load segmentation at time t
        data = dataset.get_seg(t)
        #Start watershed at t
        new_seeds = self._water_on_seed(dataset, t, data, seeds, objects)
        #Continue watersheds at t+1 if we have a seed and is in working times
        if len(new_seeds) > 0 and t + 1 in self.times:
            self._water_time(dataset, t + 1, new_seeds, objects)


    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects):
            return None
        #Get the min vol for cells to create from MorphoNet
        self.min_vol = int(self.get_inputfield("minimum volume"))
        self.voxel_size_toggle = int(self.get_toggle("rescale with voxel size"))
        #Get the seeds list from morphonet
        seeds = self.get_coordinates("Add a Seed")
        if len(seeds) == 0:
            printv("no seeds for watershed",0)
        else:
            printv("Found "+str( len(seeds))+ " seeds ",0)
            #Convert morphonet space seeds to segmentation space
            seeds = get_seeds_in_image(dataset, seeds)
            #Retrieve time list in objects list
            self.times = dataset.get_times(objects)
            #Start watershed sequence from seeds
            self._water_time(dataset, self.times[0], seeds, objects)
        self.restart()
