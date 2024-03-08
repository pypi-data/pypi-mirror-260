# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from skimage.morphology import extrema
from skimage.filters import gaussian
from skimage.measure import label
import numpy as np
from ...tools import printv


class Seedin(MorphoPlugin):
    """ This plugin generates seeds that can be used in other plugins (mainly watershed segmentation).
    Seeds are generated at the minimum intensity where no segmentation labels are found (in the background)


    Parameters
    ----------
    sigma : int, default :8
        The standard deviation for the Gaussian kernel when sigma>0, the plugin first applies a gaussian filter on the intensity image. (>=0)
    h minima value : int, default :2
        If using the  H Minima method, determines the minimal depth of all extracted minima. (>=0)
    method : (list of methods)
        Method used to find local minima of intensity in the intensity image.
        H Minima method determine all minima of the image with depth >= h_minima_value
        Local minima  method finds the  local minima in the intensity image. The local minima are defined as connected
        sets of voxels with equal gray level (plateaus) strictly smaller than the gray levels of all voxels in the neighborhood.

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_parent("Create Seeds")
        self.set_icon_name("Seedin.png")
        self.set_image_name("Seedin.png")
        self.set_name("Seedin : Create seeds from minimum local intensity images  (without selected objects)")
        self.add_inputfield("Membrane Channel", default=0)
        self.add_inputfield("sigma", default=8)
        self.add_dropdown("method", ["H Minima", "Local Minima"])
        self.add_inputfield("h minima value", default=2)
        self.set_description( "This plugin generates seeds that can be used in other plugins (mainly watershed segmentation). \n"
                              " Seeds are generated at the minimum intensity where no segmentation labels are found "
                              "(in the background)  \n \n"
                              "Parameters : \n \n"
                              "- h minima value (numeric,default:2) : If using the  H Minima method, determines the "
                              "minimal depth of extracted minima. (>=0) \n \n"
                                "- method : method used to find local minima \n"
                                 "     H minimal : all minima with depth > h minima value \n"
                                 "     Local minima : minima using connected set of voxels with low grey level compared to "
                                 "neighborhood")


    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False,backup=False):
            return None
        # Value of the smoothing user want to apply on raw data to find the` seeds
        s_sigma = int(self.get_inputfield("sigma"))
        #Minimal depths of the minima to find in the image , if using H Minima method
        h_value = float(self.get_inputfield("h minima value"))
        # h-minima or local minima
        method = self.get_dropdown("method")
        membrane_channel = int(self.get_inputfield("Membrane Channel"))

        nbc = 0
        data = dataset.get_seg(t,channel=membrane_channel) #Load segmentation data in memory
        #Load raw image data in memory
        rawdata = dataset.get_raw(t,channel=membrane_channel)
        if rawdata is None:
            print("Miss raw file")
            return
        # If user wants to smooth
        if s_sigma > 0.0:  # Smoothing
            printv("Perform gaussian with sigma=" + str(s_sigma),0)
            rawdata = gaussian(rawdata, sigma=s_sigma, preserve_range=True)

        # Compute the minimas depending on the method
        if method == "H Minima":
            local = extrema.h_minima(rawdata, h_value)
        if method == "Local Minima":
            local = extrema.local_minima(rawdata)


        printv("Perform  labelisation",0)
        #Get the labels of the local minimas in the segmentation
        label_maxima, nbElts = label(local, return_num=True)
        if nbElts > 100:
            printv("Found too many seeds : " + str(nbElts),0)
        else:
            #For each local minima found
            for elt in range(1, nbElts + 1):
                #Get the coordinate of the local minima
                coord = np.where(label_maxima == elt)
                v = dataset.background
                #If segmentation is loaded , check if the minima is inside a cell
                if data is not None:
                    v = data[coord[0][0], coord[1][0], coord[2][0]]
                #If minima is not a cell , add seed to morphonet
                if v == dataset.background:
                    dataset.add_seed([coord[0][0], coord[1][0], coord[2][0]])
                    nbc += 1

            printv("Found " + str(nbc) + " new seeds",0)
        #Send data back to morphonet
        self.restart()

