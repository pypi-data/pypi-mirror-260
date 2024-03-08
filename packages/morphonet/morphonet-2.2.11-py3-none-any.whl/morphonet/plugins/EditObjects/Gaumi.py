# -*- coding: latin-1 -*-
from skimage.transform import resize

from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv
import numpy as np

def get_model(n_components,method):
    r = np.random.RandomState(seed=1234)
    from sklearn.mixture import GaussianMixture
    return GaussianMixture(n_components=n_components, init_params=method, tol=1e-9, max_iter=0,random_state=r)



class Gaumi(MorphoPlugin):
    """ This plugin calculates the gaussian mixture model probability distribution on selected objects in order to split
     them into several objects which will replace the selected ones.

    Parameters
    ----------
    Objects:
        The selected or labeled objects on MorphoNet
    n_components : int , default 2
        The number of mixture components which correspond to the number of new objects to be created in each input
        object (>1)
    method : list of methods
        The method used to initialize the weights, the means and the precisions of the algorithms

    Reference : this plugin use the Gaussian Mixture function in scikit-learn : https://scikit-learn.org/stable/modules/
    generated/sklearn.mixture.GaussianMixture.html

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Gaumi.png")
        self.set_image_name("Gaumi.png")
        self.set_name("Gaumi : Split the selected objects using probability distribution")
        self.add_dropdown("method",["kmeans", "randomFromData", "k-means++", "random"])
        self.add_dropdown("image", ["segmentation", "intensity"])
        self.add_inputfield("n components", default=2)
        self.add_toggle("rescale with voxel size", default=True)
        self.set_description("This plugin calculates the gaussian mixture model probability distribution on selected "
                             "objects in order to splitthem into several objects which will replace the selected ones\n \n"
                             "Parameters : \n \n"
                             "- nb components (numeric,default:2) : Number of object to be created \n"
                             "- method : method used to initialize the weights, the means and the precisions of the "
                             "algorithms\n"
                             "- image : in the segmentation mode, we use only the coordinates, "
                             "in the intensity mode, we ponderate the cordinates by the value of intensity inside the area "
                             )
        self.set_parent("Edit Objects")


    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        method=self.get_dropdown("method")
        image=self.get_dropdown("image")
        n_components= int(self.get_inputfield("n components"))
        voxel_size_toggle = int(self.get_toggle("rescale with voxel size"))
        cancel = True


        for channel in dataset.get_channels(objects):  # For each time point in objects to split
            for t in dataset.get_times(objects): #For each time point in objects to split

                data = dataset.get_seg(t,channel)  #Load the segmentations
                raw=dataset.get_raw(t,channel)  if image=="intensity" else None
                vx=dataset.get_voxel_size(t,channel)

                cells_updated = []
                for o in dataset.get_objects_at(objects, t): #For each object at time point
                    printv('Split Object '+str(o.get_name())+ " with  "+str(method),0)

                    bbox = self.dataset.get_regionprop("bbox", o)
                    databox = data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                    if voxel_size_toggle:
                        orignal_shape = databox.shape
                        vx = [x / min(vx) for x in vx]  # [1,1,10]
                        new_shape = np.uint16([databox.shape[0] * vx[0], databox.shape[1] * vx[1], databox.shape[2] * vx[2]])
                        databox = resize(databox, new_shape, preserve_range=True, order=0)

                    coords=np.where(databox==o.id)
                    if len(coords)<2 or len(coords[0])<4 :  #Cannot split empty area
                        printv("Cannot split this object with no coords ...  " , 0)
                    else:

                        X = np.float64(np.array(coords).transpose())

                        model = get_model(n_components, method)
                        if raw is not None:
                            rawbox=raw[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                            if voxel_size_toggle:
                               rawbox = resize(rawbox, new_shape, preserve_range=True, order=0)

                            raw_weight = rawbox[coords[0], coords[1], coords[2]]
                            X_all=np.zeros([raw_weight.sum(),3])
                            for j in range(3): X_all[:,j]=np.repeat(coords[j],raw_weight)
                            model.fit(X_all)
                        else:
                            model.fit(X)
                        Y = model.predict(X)

                        cells_updated.append(o.id)
                        lastID = int(data.max())+1

                        box_result=np.zeros(databox.shape,np.uint16)
                        for i in range(1,n_components): #The 0 Componnent stay the origin cell
                            w = Y == i
                            nb_pixels=len(coords[0][w])
                            if nb_pixels==0:
                                printv('The split did not work well .... ', 0)
                            else:
                                box_result[coords[0][w], coords[1][w], coords[2][w]] = lastID
                                printv('Create a new ID ' + str(lastID) + " with " + str(len(coords[0][w])) + " pixels", 0)
                                cells_updated.append(lastID)
                                lastID += 1

                        if voxel_size_toggle:
                            box_result = resize(box_result,orignal_shape, preserve_range=True, order=0)
                        data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]][box_result>0]=box_result[box_result>0]

                if len(cells_updated) > 0:
                    cancel=False
                    dataset.set_seg(t, data, channel=channel ,cells_updated=cells_updated) #If we created a cell ,save it to seg

        self.restart(cancel=cancel)   #send data back to morphonet
