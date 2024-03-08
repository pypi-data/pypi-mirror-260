# -*- coding: latin-1 -*-
import logging
from os.path import join, isfile

from morphonet.plugins import MorphoPlugin
import numpy as np
from ...tools import printv, imsave
from ..functions import get_torch_device, read_time_points


#FROM CSDEEP
def normalize(x, pmin=3, pmax=99.8, axis=None, clip=False, eps=1e-20, dtype=np.float32):
    """Percentile-based image normalization."""
    mi = np.percentile(x,pmin,axis=axis,keepdims=True)
    ma = np.percentile(x,pmax,axis=axis,keepdims=True)
    return normalize_mi_ma(x, mi, ma, clip=clip, eps=eps, dtype=dtype)

def normalize_mi_ma(x, mi, ma, clip=False, eps=1e-20, dtype=np.float32):
    if dtype is not None:
        x   = x.astype(dtype,copy=False)
        mi  = dtype(mi) if np.isscalar(mi) else mi.astype(dtype,copy=False)
        ma  = dtype(ma) if np.isscalar(ma) else ma.astype(dtype,copy=False)
        eps = dtype(eps)

    try:
        import numexpr
        x = numexpr.evaluate("(x - mi) / ( ma - mi + eps )")
    except ImportError:
        x =                   (x - mi) / ( ma - mi + eps )

    if clip:
        x = np.clip(x,0,1)

    return x

class CellposeTrain(MorphoPlugin):
    """ This plugin uses an intensity image of the membranes from a local dataset at a specific time point, to compute a segmentation of the membranes,
    using the 3D Cellpose deep learning algorithm.

    Parameters
    ----------
    downsampling : int, default :2
        The resolution reduction applied to each axis of the input image before performing segmentation, 1 meaning that
        no reduction is applied. Increasing the reduction factor may reduce segmentation quality

    model type : list of models
        The model used to compute segmentations. A detailed documentation on models can be found https://cellpose.readthedocs.io/en/latest/models.html

    Reference : Stringer, C., Wang, T., Michaelos, M. et al. Cellpose: a generalist algorithm for cellular segmentation.
    Nat Methods 18, 100?106 (2021). https://doi.org/10.1038/s41592-020-01018-x
    https://www.cellpose.org
    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("CellposeTrain.png")
        self.set_image_name("CellposeTrain.png")
        self.set_name("CellPose Train  : Train the CellPose model on your own data")
        self.add_inputfield("Intensity Channel", default=0)
        self.add_inputfield("downsampling", default=2)
        self.add_inputfield("epochs", default=10)
        self.add_dropdown("dimension", ['3D', '2D'])
        self.add_dropdown("model type",['cyto','nuclei','tissuenet','livecell', 'cyto2', 'general','CP', 'CPx', 'TN1', 'TN2', 'TN3', 'LC1', 'LC2', 'LC3', 'LC4'])
        self.add_inputfield("time points", default="current")
        self.add_inputfield("number 2D images per epochs", default=8)
        self.set_parent("Create Segmentation")
        self.set_description("This plugin train the CellPose algorithm on your own data (based on the model type) \n \n"
                             "Parameters : \n \n "
                             "- downsampling (numeric,default:2) : he resolution reduction applied to each axis of the "
                             "input image before performing segmentation, 1 meaning that no reduction is applied. "
                             "Increasing the reduction factor may reduce segmentation quality \n"
                             "- epochs: ( default 10.) : the number of epochs to train the algorithm \n"
                             "- model type : The model used to compute segmentations. A detailed documentation on models"
                             " can be found https://cellpose.readthedocs.io/en/latest/models.html \n"
                             "- dimension: train Cellpose on the 3 axes (XY,XZ and YZ) or only on XY planes. \n"
                            "- number 2D images per epochs: batch size, depending on your image size.  \n"
                             "- time points : apply CellPose at the current time point or specify the number or specify the begin:end")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        from cellpose import models
        import logging
        logging.basicConfig(level=logging.INFO) #To have cellpose log feedback on the terminalk

        which,device=get_torch_device()
        printv("CellPose Train will run on " + which, 1)

        intensity_channel= int(self.get_inputfield("Intensity Channel"))
        downsampling = int(self.get_inputfield("downsampling"))
        model_type = self.get_dropdown("model type")
        n_epochs = int(self.get_inputfield("epochs"))
        nimg_per_epoch=int(self.get_inputfield("number 2D images per epochs"))
        dimension = self.get_dropdown("dimension")

        learning_rate = 0.1
        weight_decay = 0.0001
        channels = [0]
        train_dir = join(dataset.parent.temp_path, "CellPoseModel")
        model_name = model_type+"_downsampling"+str(downsampling)

        times=read_time_points(self.get_inputfield("time points"),t)
        if len(times)==0:
            printv("No time points",0)
        else:
            printv(" Train on "+str(times)+ " time point",2)

            #Colllect the selected data at the given time point
            train_data = []
            train_labels = []

            for t in times:
                rawdata = dataset.get_raw(t, intensity_channel)
                data = dataset.get_seg(t, intensity_channel)
                nb_image=0
                nb_cells=0
                if dimension=="3D":
                    if downsampling > 1:
                        data = data[::downsampling, ::downsampling, ::downsampling]
                        rawdata = rawdata[::downsampling, ::downsampling, ::downsampling]
                    if dataset.background != 0: data[data == dataset.background] = 0 # We do it after the rescaling to go faster
                    for dim in range(3):
                        for c in range(data.shape[dim]): #ADD Slicdes
                            if dim==0:
                                rawslice=rawdata[c,...]
                                segslice=data[c,...]
                            elif dim==1:
                                rawslice = rawdata[:,c,:]
                                segslice = data[:,c,:]
                            else:
                                rawslice = rawdata[...,c]
                                segslice = data[...,c]
                            im = normalize(rawslice)
                            im = np.reshape(im, (1,) + im.shape)
                            cells = np.unique(segslice)
                            if len(cells) > 5:  # Minimum Required by Cell Pose
                                train_data.append(im)
                                train_labels.append(segslice)
                                nb_image+=1
                                nb_cells += len(cells) - 1
                else: #2D
                    if downsampling>1:
                        data=data[::downsampling,::downsampling,:]
                        rawdata = rawdata[::downsampling, ::downsampling, :]
                    if dataset.background != 0: data[ data == dataset.background] = 0  # We do it after the rescaling to go faster

                    for c in range(data.shape[2]):  # ADD Slicdes
                        segslice = data[..., c]
                        cells=np.unique(segslice)
                        if len(cells) > 5:  # Minimum Required by Cell Pose
                            im = normalize(rawdata[..., c])
                            train_data.append(im)
                            train_labels.append(segslice)
                            nb_image+=1
                            nb_cells+=len(cells)-1
                printv(" --> "+str(nb_cells)+" "+dimension+" cells added at " + str(t), 0)

            if len(train_data)==0:
                printv("ERROR Cannot Train with not images",0)
            else:
                printv("Start Train CellPose on " + str(len(train_data)) + " 2D images from model : "+model_type,0)
                if isfile(join(train_dir, model_name)): #Continue to train
                    model = models.CellposeModel(gpu=which=="GPU", device=device, model_type=model_type,pretrained_model=join(train_dir, model_name))
                else:
                    model = models.CellposeModel(gpu=which=="GPU", device=device, model_type=model_type)
                new_model_path = model.train(train_data, train_labels,
                                             channels=channels,
                                             save_path=train_dir,
                                             n_epochs=n_epochs,
                                             learning_rate=learning_rate,
                                             weight_decay=weight_decay,
                                             nimg_per_epoch=nimg_per_epoch,
                                             model_name=model_name)
                printv("Model Saved",0)


        logging.basicConfig(level=logging.WARNING)
        self.restart(cancel=True) #We do not change anything




