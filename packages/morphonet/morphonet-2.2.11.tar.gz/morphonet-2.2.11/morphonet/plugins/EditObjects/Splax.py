# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class Splax(MorphoPlugin):
    """ This plugin splits any selected objects in two new objects in the middle of one of the given image axes. The new
     objects will replace the previous selected ones.


    Parameters
    ----------
    Objects: 
        The selected or labeled objects on MorphoNet
    axis : Dropdown (X,Y,Z)
         axis chosen to split the objects, corresponding to axis in the image (independent of the rotation of the object in MorphoNet)

    """
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self)
        self.set_icon_name("Splax.png")
        self.set_image_name("Splax.png")
        self.set_name("Splax : Split the selected objects in the middle of a given axis")
        self.add_dropdown("axis",["X","Y","Z"])
        self.set_parent("Edit Objects")
        self.set_description("This plugin splits any selected objects in two new objects in the middle of one of the "
                             "given image axes. The new objects will replace the previous selected ones.\n \n"
                              "Parameters : \n \n "
                             "- axis : axis chosen to split the objects, corresponding to axis in the image (independent"
                             " of the rotation of the object in MorphoNet) \n")


    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        import numpy as np
        #Determine which axis in the image
        which=self.get_dropdown("axis")
        xyz=-1
        if which=="X":
            xyz=0
        elif which=="Y":
            xyz=1
        elif which=="Z":
            xyz=2
        if xyz==-1:
            printv('ERROR' + which+ " unknown ....",2)
        else:
            for channel in dataset.get_channels(objects):
                for t in dataset.get_times(objects):  # For each time point in objects to split
                    data = dataset.get_seg(t, channel)  # Load the segmentations
                    cells_updated = []
                    for o in dataset.get_objects_at(objects, t):  # For each object at time point
                        printv('Split Object '+str(o.get_name())+ " in "+str(which),0)

                        coords=dataset.np_where(o)  # Get the object to split coordinates in image

                        xyzList=np.unique(coords[xyz])  # Get the object coords in axis
                        xyzList.sort()

                        lastID=int(data.max())  # Find the object new id (max id of seg +1)
                        lastID=lastID+1
                        # get the upper half of the object along the choosen axis
                        w=np.where(coords[xyz]>int(xyzList.mean()))
                        new_coords=(coords[0][w],coords[1][w],coords[2][w])

                        data[new_coords]=lastID  # apply the new ids to the upper coords
                        printv('Create a new ID '+str(lastID)+ " with "+str(len(new_coords[0]))+ " pixels",0)

                        cells_updated.append(o.id)  #add to refresh in morphonet
                        cells_updated.append(lastID)
                    if len(cells_updated)>0:
                        # If we created a cell ,save it to seg
                        dataset.set_seg(t,data,channel, cells_updated=cells_updated)

        self.restart()  # send data back to morphonet
