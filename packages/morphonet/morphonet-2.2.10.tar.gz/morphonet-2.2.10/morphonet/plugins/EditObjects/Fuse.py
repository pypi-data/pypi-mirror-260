# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class Fuse(MorphoPlugin):
    """ This plugin performs the fusion of selected objects into a single one.
    If multiple objects are selected , they are fused together at the current time point. Else if objects are labeled it
    will apply a fusion between all objects sharing the same label (for each individual time points)

    Parameters
    ----------
    Objects:
        The selected or labeled objects on MorphoNet
    """

    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Fuse.png")
        self.set_image_name("Fuse.png")
        self.set_name("Fuse : Fuse the selected objects")
        self.set_parent("Edit Objects")
        self.set_description("This plugin performs the fusion of selected objects into a single one."
                             "If multiple objects are selected , they are fused together at the current time point. "
                             "Else if objects are labeled it will apply a fusion between all objects sharing the same "
                             "label (for each individual time points)")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
        import numpy as np
        for channel in dataset.get_channels(objects):#For each channels in selected object
            for t in dataset.get_times(objects):#For each time points in selected object
                tofuse={}
                #Get the list of ids to fuse , split with the differents selections (each selection will be fused)
                for o in dataset.get_objects_at(objects,t):
                    if o.s not in tofuse:
                        tofuse[o.s]=[]
                    tofuse[o.s].append(o.id)
                #Load the segmentation
                data=dataset.get_seg(t,channel)
                cells_updated=[]
                #For each group of cells to fuse together
                for s in tofuse:
                    #Fuse only if we have multiple objects
                    if len(tofuse[s])>1 :
                        #Get the smallest ids among the cells to fuse
                        minFuse=np.array(tofuse[s]).min()
                        cells_updated.append(minFuse)
                        printv("Fuse objects "+str(tofuse[s])+" at "+str(t) + " into object "+str(minFuse),0)
                        cell = dataset.get_object(t, minFuse,channel)
                        #For each object to fuse
                        for tof in tofuse[s]:
                            #Only fuse the biggest ids
                            if tof!=minFuse:
                                cells_updated.append(tof) #Update List of Cells to recompute
                                #Get the morphonet object
                                cell_to_fuse = dataset.get_object(t, tof,channel)
                                #cell = dataset.get_object(t, minFuse) #Already get before
                                # apply the smalles id to this object
                                # Change the lineage information to the new id
                                #cell_to_fuse.channel = channel
                                dataset.set_cell_value(cell_to_fuse,minFuse)  #Set this cell to the global one
                                dataset.del_cell_from_properties(cell_to_fuse)
                                #Lineage Modification
                                for m in cell_to_fuse.mothers:
                                    if cell.nb_mothers() > 0:
                                        for mother in cell.mothers:
                                            dataset.del_mother(cell,mother)
                                    dataset.add_mother(cell,m) #We only add the mother if the new cell do not have one...
                                    dataset.del_mother(cell_to_fuse,m)

                                for d in cell_to_fuse.daughters:
                                    dataset.add_daughter(cell,d)
                                    dataset.del_daughter(cell_to_fuse,d)
                #Change the segmentation
                if len(cells_updated)>0:
                    dataset.set_seg(t,data,channel=channel,cells_updated=cells_updated)
        #Send data to morphonet
        self.restart()
