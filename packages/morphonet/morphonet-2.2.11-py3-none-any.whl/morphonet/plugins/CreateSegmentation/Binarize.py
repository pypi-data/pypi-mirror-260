# -*- coding: latin-1 -*-
import logging
from os.path import join, isfile

from morphonet.plugins import MorphoPlugin
import numpy as np
from ...tools import printv
from ..functions import read_time_points


class Binarize(MorphoPlugin):
    """ This plugin apply a threshold to intensity image and create label by connected component

    Parameters
    ----------
    Threshold : int, default :1
        The threshold value

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Binarize.png")
        self.set_image_name("Binarize.png")
        self.set_name("Binarize : apply a threshold to intensity image")
        self.add_inputfield("threshold", default=1)
        self.add_inputfield("Intensity Channel", default=0)
        self.add_inputfield("time points", default="current")
        self.set_parent("Create Segmentation")
        self.set_description("This plugin apply a threshold to intensity image and label each binary objeccts by connected component\n"
                             "- threshold: (float, default 1.) : the theshold value in the intensity images  \n"
                             "- time points : apply CellPose at the current time point or specify the number or specify the begin:end")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        from skimage.measure import label
        threshold = float(self.get_inputfield("threshold"))
        intensity_channel = int(self.get_inputfield("Intensity Channel"))

        cancel = True
        #If objects are selected, we run cellpose on the global bounding box of the object
        if len(objects)>=1 and objects[0]!="":
            for t in dataset.get_times(objects):  # Get all times in the labeled objects list
                rawdata = dataset.get_raw(t, intensity_channel)
                data = dataset.get_seg(t, intensity_channel)
                if rawdata is not None and data is not None:
                    cells_updated = []
                    last_id = dataset.get_last_id(t)
                    for o in dataset.get_objects_at(objects, t):
                        printv("add object " + str(o.id) + " at " + str(o.t),1)
                        bbox = dataset.get_regionprop("bbox", o)

                        rawdata_box = rawdata[bbox[0]:bbox[3]+1, bbox[1]:bbox[4]+1, bbox[2]:bbox[5]+1]

                        #Compute the mask for this cell
                        data_mask = np.zeros(rawdata_box.shape, dtype=np.uint16)
                        coords = dataset.np_where(o)
                        data_mask[coords[0] - bbox[0], coords[1] - bbox[1], coords[2] - bbox[2]] = 1

                        rawdata_box[data_mask==0]=0 #Remove values outsidee the mask

                        data_box=label(rawdata_box>threshold) #Label by connected component

                        cells=np.unique(data_box)
                        cells=cells[cells!=0]  #Remove background
                        nb_cells = len(cells)
                        if nb_cells ==0:  # Only background...
                            printv("did not find any new cells in "+str(o.id)+ " at "+ str(o.t), 0)
                        else:
                            printv("found " + str(nb_cells) + " cells   in "+str(o.id)+ " at "+ str(o.t), 0)

                            prev_databox = data[bbox[0]:bbox[3] + 1, bbox[1]:bbox[4] + 1, bbox[2]:bbox[5] + 1]
                            prev_databox[data_mask == 1] = 0  # Remove Previous Values
                            #Now we have to give the new cells ids
                            new_cells=data_box>0
                            data_box[new_cells]+=last_id
                            prev_databox[data_mask == 1] = data_box[data_mask == 1]
                            data[bbox[0]:bbox[3]+1, bbox[1]:bbox[4]+1, bbox[2]:bbox[5]+1]=prev_databox
                            for c in cells:  cells_updated.append(c+last_id)
                            last_id+=cells.max()
                    dataset.set_seg(t, data, channel=intensity_channel, cells_updated=cells_updated)
                    cancel = False

        else: #Predict on the full images
            times = read_time_points(self.get_inputfield("time points"), t)
            if len(times) == 0:
                printv("No time points", 0)
            else:
                for t in  times:
                    rawdata = dataset.get_raw(t,intensity_channel)
                    if rawdata is not None:
                        data = label(np.uint8(rawdata > threshold))  # Label by connected component
                        nb_cells = len(np.unique(data))
                        if nb_cells == 1:  # Only background...
                            printv("did not find any cells", 0)
                        else:
                            printv("found " + str(nb_cells) + " cells  at " + str(t), 0)
                            dataset.set_seg(t, data, channel=intensity_channel, cells_updated=None)  # ALL
                            cancel = False

        self.restart(cancel=cancel)




