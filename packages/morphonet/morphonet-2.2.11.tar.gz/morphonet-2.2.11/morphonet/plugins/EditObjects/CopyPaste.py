# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv
from ..functions import _centerInShape, get_seeds_in_image, watershed
import numpy as np
from scipy.spatial.transform import Rotation as R


class CopyPaste(MorphoPlugin):
    """ This plugin give the possibility to copy an object (a segmented cell for example)  and paste it at another time steps and/or another location.


    Parameters
    ----------
    Objects:
        The selected objects to apply deformation on MorphoNet
     Seeds: Coordinate List
        List of seeds where to paste the selected object
    """

    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("CopyPaste.png")
        self.set_image_name("CopyPaste.png")
        self.set_parent("Edit Objects")
        self.set_name("Copy Paste")
        self.transformations_inputs = {}
        self._set_transform_inputs("copy_objects","copy_objects")
        self.set_description("This  give the possibility to copy an object (a segmented cell for example) \n"
                             " and paste it at another time steps and/or another location. \n"
                             "\n"
                             "To copy a picked object , use C \n"
                             "To move a copy instance, put your mouse over it and press M \n"
                             "To delete a copy instance, put your mouse over it and press D \n"
                             "To scale a copy instance, put your mouse over it and press S , and than scroll \n"
                             "To rotate a copy instance , put your mouse over it and press R , than move your mouse.")

    def _get_btn(self):
        c=self._cmd()+";"+self.parent
        for tf in self.inputfields:
            c+=";IF_"+str(tf)
            if self.inputfields[tf] is not None:
                c+=";DF_"+str(self.inputfields[tf])
        for dd in self.dropdowns:
            c+=";DD_"+str(dd)+"_"
            for v in self.dropdowns[dd]:
                c+=str(v)+"_"
        for cd in self.coordinates:
            c+=";CD_"+str(cd)
        for ti in self.transformations_inputs:
            c+=";TI_"+str(ti)
        return c

    def _set_transform_inputs(self,text_name,value):
        self.transformations_inputs[text_name]=value
    def process(self,t,dataset,objects,transforms): #PLUGIN EXECUTION
        from morphonet.tools import imsave
        if not self.start(t,dataset,objects,objects_require=True):
            return None
        if len(objects)!=1:
            printv(" --> this plugin required only on object selected ",0)
            self.restart(cancel=True)
            return None

        if transforms is None or len(transforms) == 0:
            #transform format : translate.x,translate.y,translate.z,rotation.x,rotation.y,rotation.z,rotation.w,scaling_factor
            printv("no cell paste found", 0)
            self.restart(cancel=True)
            return None

        #print("object : ")
        #print(objects)
        poped_object = objects[0]
        #print(poped_object)
        object=dataset.get_object(poped_object) #Get the Object to copy
        data = dataset.get_seg(t, object.channel)
        #print(object)
        coords = dataset.np_where(object)
        #np.save("coords.npy",coords)
        #print(coords)
        #printv(transforms, 1)
        barycenter=np.uint16([coords[0].mean(),coords[1].mean(),coords[2].mean()])
        #print(barycenter)
        #imsave("data_input_copypaste.tiff",data)
        cells_updated=[]
        for transform in transforms:  # For each coordinates
            #printv(transform,1)
            split_transform = transform.split(",")
            translation=np.float32([split_transform[0],split_transform[1],split_transform[2]])/dataset.get_voxel_size(t)
            rotation=np.float32([split_transform[3],split_transform[4],split_transform[5],split_transform[6]])
            scaling_factor=np.float32(split_transform[7])

            coords = [coords[0] - barycenter[0], coords[1] - barycenter[1], coords[2] - barycenter[2]] # We center the coord to the barycenter of the cell
            coords = [coords[0] * scaling_factor, coords[1] * scaling_factor, coords[2] * scaling_factor]  # We rescale the cell
            r = R.from_quat(rotation) # We apply the rotation
            coords = np.transpose(r.apply(np.transpose(coords)))
            coords = [translation[0] + coords[0] + barycenter[0], translation[1] + coords[1] + barycenter[1],  translation[2] + coords[2] + barycenter[2]] # We apply the translation
            coords = np.uint16(coords)# Convert in integer

            # We trunck the coords outside the images
            idx = np.zeros_like(coords[0])
            for i in range(3):
                idx += np.uint8(coords[i] >= 0) + np.uint8(coords[i] < data.shape[i])
            keep_index = idx == 6
            coords = [coords[0][keep_index], coords[1][keep_index], coords[2][keep_index]]

            # Now we check if there is not object in the coordinates to paste  (or we remove)
            values = data[coords[0], coords[1], coords[2]]
            cells_existing = np.unique(values)
            idx_to_remove = np.zeros_like(values)  # Initialise all at False
            for c in cells_existing:
                if c != dataset.background:  # We can only past in the background
                    idx_to_remove += np.uint16(values == c)  # Remove this index
            index_to_keep = idx_to_remove == 0
            coords = [coords[0][index_to_keep], coords[1][index_to_keep], coords[2][index_to_keep]]
            # Finaly we assign the values
            if len(coords[0]) == 0:
                printv("no background found in this area ", 0)
            else:
                last_id = dataset.get_last_id(t)+1
                data[coords[0], coords[1], coords[2]] = last_id  # Set the new cell id
                cells_updated.append(last_id)
                printv("Create a new object at " + str(t) + " with id " + str(last_id), 0)


        if len(cells_updated)>0:  # If we updated at least one object, save segmentation and recompute mesh
            dataset.set_seg(t,data,channel=object.channel,cells_updated=cells_updated)
            self.restart() #Resend data to MorphoNet viewer
        else:
            self.restart(cancel=True)
