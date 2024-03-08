# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from skimage.morphology import extrema, binary_dilation
from skimage.filters import gaussian
from skimage.measure import label
import numpy as np
from ..functions import watershed
from ...tools import printv
from skimage.transform import resize

class Mars(MorphoPlugin):
    """ This plugin uses an intensity image from a local dataset at a specific time point, to perform a segmentation
    using a seeded watershed  algorithm.


    Parameters
    ----------
    downsampling: int, default 2
        The resolution reduction applied to each axis of the input image before performing segmentation, 1 meaning that
        no reduction is applied. Increasing the reduction factor may reduce segmentation quality (>=1)
    sigma : int, default 8
        The standard deviation for the Gaussian kernel when sigma>0, the plugin first applies a gaussian filter on the
        intensity image. (>=0)
    h minima value : int, default 2
        If using the  H Minima method, determines the minimal depth of all extracted minima.
        Optional , >= 0
    method : (list of methods)
        Method used to find local minima of intensity in the intensity image.
        H Minima method determine all minima of the image with depth >= h_minima_value
        Local minima  method finds the  local minima in the intensity image. The local minima are defined as connected
        sets of voxels with equal gray level (plateaus) strictly smaller than the gray levels of all voxels in the
        neighborhood.

    Reference : Fernandez R, Das P, Mirabet V, Moscardi E, Traas J, Verdeil JL, Malandain G, Godin C. Imaging plant
    growth in 4D: robust tissue reconstruction and lineaging at cell resolution. Nat Methods. 2010 Jul;7(7):547-53.
    doi: 10.1038/nmeth.1472. Epub 2010 Jun 13. PMID: 20543845.
    """


    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_parent("Create Segmentation")
        self.set_icon_name("Mars.png")
        self.set_image_name("Mars.png")
        self.set_name("Mars : Perform membrane segmentation on intensity images using seeded watershed")
        self.add_inputfield("Membrane Channel", default=0)
        self.add_inputfield("downsampling", default=2)
        self.add_inputfield("sigma", default=8)
        self.add_dropdown("method", ["H Minima", "Local Minima"])
        self.add_inputfield("h minima value", default=2)
        self.set_description("This plugin uses an intensity image from a local dataset at a specific time point, to "
                             "perform a segmentation using a seeded watershed  algorithm. \n \n "
                             "Parameters : \n \n "
                             "- downsampling (numeric,default:2) : Resolution reduction to input image \n"
                             "- sigma (numeric,default:8) : Start deviation for the Gaussian kernel. If > 0 , a gaussian filter is applied \n"
                             "- h minima value (numeric,default:2) : Minimal depths of minima if using H Minima method \n "
                             "- method : method used to find local minima \n"
                             "     H minimal : all minima with depth > h minima value \n"
                             "     Local minima : minima using connected set of voxels with low grey level compared to "
                             "neighborhood")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        downsampling = int(self.get_inputfield("downsampling"))
        s_sigma = int(self.get_inputfield("sigma")) # Value of the smoothing user want to apply on raw data to find the seeds
        h_value = float(self.get_inputfield("h minima value")) #Minimal depths of the minima to find in the image , if using H Minima method
        method=self.get_dropdown("method") # h-minima or local minima
        membrane_channel = int(self.get_inputfield("Membrane Channel"))

        rawdata = dataset.get_raw(t)  # Load raw data in memory
        if rawdata is None:
            printv("please specify the rawdata", 0)
        else:
            init_shape = rawdata.shape
            if downsampling > 1:
                rawdata = rawdata[::downsampling, ::downsampling, ::downsampling]

            #maxi = np.max(rawdata) # Get the maximum intensity in rawdata
            if s_sigma > 0.0:  # Smoothing
                printv("Perform gaussian with sigma=" + str(s_sigma),0)
                raw_mask = gaussian(rawdata, sigma=s_sigma,preserve_range=True)#Get the mask after smoothing
            else:
                raw_mask = rawdata  #Get the mask

            # Compute the minimas depending on the method
            if method=="H Minima":
                local = extrema.h_minima(raw_mask, h_value)
            if method=="Local Minima":
                local = extrema.local_minima(raw_mask)

            printv("Perform labelisation",0)
            markers, nbElts = label(local, return_num=True) # Get the labels of the local minimas in the segmentation
            if nbElts>100:
                printv("Found too much seeds : "+str(nbElts)+" Please, change parameters ",1)
            else:
                printv("Process watershed with " + str(nbElts) + " seeds", 0)
                data = watershed(rawdata, markers=markers ) # Watershed on the rawdata ,  using seed images computed

                data[data != 0] += dataset.get_last_id(t)  # Create New Ids

                if downsampling > 1:
                    data = resize(data,init_shape,preserve_range=True,order=0)
                dataset.set_seg(t, data,channel=membrane_channel,cells_updated=None)

            printv(" --> Found " + str(nbElts) + " objects",0)

        self.restart() #Send back data to MorphoNet

