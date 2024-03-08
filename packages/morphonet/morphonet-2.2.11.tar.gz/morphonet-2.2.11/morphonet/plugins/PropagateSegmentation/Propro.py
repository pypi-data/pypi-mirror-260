# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ...tools import printv
from .seed_propagation_lib import get_list_of_selections,process_propagation_for_selection



class Propro(MorphoPlugin):
    """ This plugin propagates labeled objects at the current time point through time.
    User applies a specific label to the objects to propagate at the current time, named the source objects.  And then
    label the corresponding objects to propagate on at the next time points, named the destination objects.
    The plugin can be executed Forward (source objects are at the beginning of the time range) or Backward (source
    objects are at the end of  the time range). The  barycenter of the source objects are used as seeds into destination
    objects at the next time point, and then a watershed is computed on the segmented images.  The new objects created
    by the watershed will replace the destination objects

    Parameters
    ----------
    Objects
        The selected or labeled objects on MorphoNet
    time direction : Dropdown
        Forward : The first time point to be propagated is the lowest one
        Backward : THe first time point to be propagated is the latest, and the propagation happens in backwards direction
    minimum volume : int , default 1000
        The minimal volume (in number of voxels) allowed for the new objects to be created (>=0)

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Propo.png")
        self.set_image_name("Propo.png")
        self.set_name("Propro : Propagate barycenters of selected objects through time on the next object (without "
                      "intensity images)")
        self.add_dropdown("time direction",["Forward","Backward"])
        self.add_inputfield("minimum volume", default=1000)
        self.set_parent("Propagate Segmentation")
        self.set_description( "This plugin propagates labeled objects at the current time point through time. User "
                              "applies a specific label to the objects to propagate at the current time.The"
                              "  barycenter of the source objects are used as seeds into empty area at the next time "
                              "point, and then a watershed on the segmentation images.  The new objects will "
                              "replace the destination objects \n \n"
                             "- time direction : Direction of labeled time points tracking (Forward or Backward) \n "
                            "- minimum volume (numeric,default:1000) : The minimal volume (in number of voxels) allowed"
                              " for the new objects to be created \n")


    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects):
            return None

        printv("Propagation of " + str(len(objects)) + " objects", 0)
        #Minimum volume of the cell created by the propagation
        self.min_vol = int(self.get_inputfield("minimum volume"))
        # List Objects by selections , to work on each selection one by one
        selections = get_list_of_selections(dataset,objects)

        new_label = ""
        # Get user direction chosen
        forward = (str(self.get_dropdown("time direction")) == "Forward")
        # For each selection found
        for s in selections:
            new_label += process_propagation_for_selection(selections, s, dataset,forward,self.min_vol,use_raw_images=False,sigma=0)
        #Send back data to MorphoNet
        self.restart(label=new_label)
