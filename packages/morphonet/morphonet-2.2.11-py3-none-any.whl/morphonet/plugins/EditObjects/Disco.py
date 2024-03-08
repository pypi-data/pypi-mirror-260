# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np

from morphonet.tools import printv


class Disco(MorphoPlugin):
    """ This plugin can be used to split any object made up of several sub-objects that are not in contact with each other.Any split object will replace the previous object.

    Parameters
    ----------
    The selected or labeled objects on MorphoNet
    time points: list of time range
        Current times : will only delete all objects at the current time point
        All times : will delete all objects at all time points

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Disco.png")
        self.set_image_name("Disco.png")
        self.set_name("Disco : Split the selected objects for unconnected objects")
        self.add_dropdown("time points",["Current time","All times"])
        self.set_parent("Edit Objects")
        self.set_description("This plugin can be used to split any object made up of several sub-objects that are not in"
                             " contact with each other. Any split object will replace the previous object.\n \n"
                              "Parameters : \n \n "
                             "- time points : List of time range \n"
                             "    Current : Current time point in MorphoNet \n"
                             "    All : will delete all objects at all time points \n ")

    def split_unconnected_at(self, t, channel, dataset):
        import numpy as np
        from skimage.measure import label
        data = dataset.get_seg(t)  #Get segmentations at the time
        lastID = dataset.get_last_id(t) + 1
        cells_updated = []
        for o in dataset.get_all_objects_at(t,channel):  # For all objects in segmentation from morphonet
            bb = dataset.get_regionprop("bbox", o)
            data_cell = data[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]]
            labels = label(data_cell==o.id, background=dataset.background)
            ids, counts = np.unique(labels, return_counts=True)  # Get the differents  connected components
            w=ids!=0 #Remove background (ATTENTION it's not dataset.background !)
            counts=counts[w]
            ids=ids[w]
            if len(ids) > 1:  # If we have 2 connected components
                printv('Found Object to split ' + str(o.get_name()) + " at " + str(t)+", channel "+str(channel), 0)
                idx = np.where(counts == counts.max())  #from all the connected components to split, the biggest will get the previous cell ids
                id_cell = ids[idx][0]  # Keep this cell
                printv("Let's keep id : "+str(id_cell),1)
                cells_updated.append(o.id)
                for other_cell in ids: #for each other connected components
                    if other_cell != id_cell:
                        printv("We need to update cell with id : "+str(other_cell),1)  #Each component get a new id in the segmentation
                        data_cell[labels == other_cell] = lastID
                        printv('Create a new ID ' + str(lastID),0)
                        lastID += 1
                        #cell to refresh
                        cells_updated.append(lastID)
                data[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]]=data_cell

        #If we changed a cell , write segmentation
        if len(cells_updated) > 0:
            dataset.set_seg(t, data, channel, cells_updated=cells_updated)

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,objects_require=False):
            return None
        #Start the split for the sequence of times or the single times depending of user choice
        if str(self.get_dropdown("time points")) == "All times":
            for c in self.dataset.segmented_channels:
                for i in range(self.dataset.begin, self.dataset.end + 1):
                    printv('Perform Disco at ' + str(t) + ', channel '+str(c), 0)
                    self.split_unconnected_at(i,c,dataset)
        else:
            for c in self.dataset.segmented_channels:
                self.split_unconnected_at(t,c,dataset)
        self.restart()
