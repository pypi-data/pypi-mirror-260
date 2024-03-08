# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv
from skimage.registration import optical_flow_ilk,optical_flow_tvl1
import numpy as np

def get_iou(bb1, bb2):
    '''
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    '''

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1[0], bb2[0])
    y_top = max(bb1[1], bb2[1])
    z_up = max(bb1[2], bb2[2])
    x_right = min(bb1[3], bb2[3])
    y_bottom = min(bb1[4], bb2[4])
    z_down = min(bb1[5], bb2[5])

    if x_right < x_left or y_bottom < y_top  or z_down< z_up :
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top) * (z_down - z_up)

    # compute the area of both AABBs
    bb1_area = (bb1[3] - bb1[0]) * (bb1[4] - bb1[1]) * (bb1[5] - bb1[2])
    bb2_area = (bb2[3] - bb2[0]) * (bb2[4] - bb2[1]) * (bb2[5] - bb2[2])

    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    return iou



def get_best_oberlap(bbox,bboxs):
    o=0
    best=None
    #computing the best = one by one computing
    for mo in bboxs:
        #get the iou count for the box
        ov=get_iou(bbox,bboxs[mo])
        #if iou is more than the previous best, choose this box
        if ov>o:
            o=ov
            best=mo
    return best




class Tracko(MorphoPlugin):
    """This plugin creates a complete object lineage using the maximum of overlap between objects.
    The overlap is calculated between the bounding box enveloping each object. After the execution, the lineage property
    is updated, and sent back to MorphoNet.


    Parameters
    ----------
    time direction : dropdown
        Forward : The  tracking is performed from the the current time point to last one
        Backward : The tracking is performed from the the current time point to first one

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_image_name("Tracko.png")
        self.set_icon_name("Tracko.png")
        self.set_name("Track : Create temporal links on all objects using maks overlap between time steps")
        self.set_parent("Edit Temporal Links")
        self.add_inputfield("Intensity channel", default=0)
        self.add_dropdown("time direction", ["forward", "backward"])
        self.add_dropdown("optical flow", ["none","TV-L1", "iLK"])
        self.add_inputfield("downsampling", default=2)
        self.set_description("This plugin creates a complete object lineage using the maximum of overlap between objects. "
                             "The overlap is calculated between the bounding box enveloping each object."
                             " After the execution, the lineage property is updated, and sent back to MorphoNet..\n \n"
                              "Parameters : \n \n "
                             "- time direction : Direction of tracking \n "
                             "    Forward : from the the current time point to last one \n"
                             "    Backward : from the the current time point to first one \n ")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,objects_require=False):
            return None
        #Get the lineage propagation direction
        direction=self.get_dropdown("time direction")
        optical=self.get_dropdown("optical flow")
        downsampling = int(self.get_inputfield("downsampling"))
        channel = int(self.get_inputfield("Intensity channel"))
        printv("start overlap tracking from "+str(t),0)
        if direction=="forward" :
            while t<self.dataset.end: #From t to t max
                self.compute_links(t,t+1,channel,optical,downsampling,direction) #compute lineage by overlaping
                t+=1
        if direction == "backward":
            while t > self.dataset.begin: #from t to t min
                self.compute_links(t, t - 1,channel,optical,downsampling,direction) # compute lineage by overlaping
                t -= 1

        self.restart()

    def compute_links(self,t, tp, channel,optical,downsampling, direction):
        printv("compute links at " + str(t)+", channel "+str(channel), 0)
        flow=None
        if optical != "none":
            rawdata0 = self.dataset.get_raw(t, channel)
            rawdata1 = self.dataset.get_raw(tp, channel)
            if rawdata0 is None or rawdata1 is None:
                printv("cannot use optical flow without intensity images", 0)
            else:
                m = max(rawdata0.max(), rawdata1.max())
                init_shape = rawdata0.shape
                if downsampling > 1:
                    rawdata0 = rawdata0[::downsampling, ::downsampling, ::downsampling]
                    rawdata1 = rawdata1[::downsampling, ::downsampling, ::downsampling]

                #Pass in 8 bit
                rawdata0 = np.uint8(rawdata0 * 255.0 / m)
                rawdata1 = np.uint8(rawdata1 * 255.0 / m)
                printv("Compute optical flow " + optical+ " at "+str(t), 1)
                if optical != "iLK":
                    flow = optical_flow_ilk(rawdata0, rawdata1)
                else:
                    flow=optical_flow_tvl1(rawdata0, rawdata1)

                flow = np.swapaxes(flow, 0, 3)
                flow = np.swapaxes(flow, 0, 2)
                flow = np.swapaxes(flow, 0, 1)



        bboxs = self.dataset.get_regionprop_at("bbox", t, channel) #Get the different cells bounding box
        next_bboxs = self.dataset.get_regionprop_at("bbox", tp, channel) #Get the next time points bounding box
        for mo in bboxs:
            bb=bboxs[mo]
            if flow is not None:
                bb=np.uint16(np.array(bb)/downsampling)
                vectors = flow[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5], :]
                vector = [vectors[..., 0].mean(), vectors[..., 1].mean(),
                          vectors[..., 2].mean()]  # Average the displacement
                vector = vector * 2  # Duplicate the list

                bb = np.uint16(bb+vector)
                if downsampling > 1:  bb*=downsampling
                bb[bb < 0] = 0  # Restore outliers
                bb[3] = min(bb[3], init_shape[0])
                bb[4] = min(bb[4], init_shape[1])
                bb[5] = min(bb[5], init_shape[2])

            next_mo = get_best_oberlap(bb, next_bboxs) #For each box at t , find the best overlapping one at t+1
            if direction == "forward":
                self.dataset.add_daughter(mo, next_mo) #link the corresponding cells in lineage
            else:
                self.dataset.add_daughter(next_mo,mo)  # link the corresponding cells in lineage