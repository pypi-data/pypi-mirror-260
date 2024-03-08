# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class Delink(MorphoPlugin):
    """This plugin delete temporal links at several time points on objects sharing the same label.
    After the execution, the lineage property is updated, and sent back to MorphoNet.

    Parameters
    ----------
    Objects: 
        The labeled objects on MorphoNet
    """
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self)
        self.set_image_name("DeLink.png")
        self.set_icon_name("DeLink.png")
        self.set_name("Delink : Delete temporal links on labeled objects")
        self.set_parent("Edit Temporal Links")
        self.set_description("This plugin delete temporal links at several time points on objects sharing the same label"
                             ".After the execution, the lineage property is updated, and sent back to MorphoNet.")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        links_deleted=0
        # For each object to remove the link from
        for cid in objects:
            o=dataset.get_object(cid)
            if o is not None:
                #If we have temporal links
                if len(o.mothers)>0 or len(o.daughters)>0:
                    printv("remove "+str(len(o.mothers))+ " mothers and "+str(len(o.daughters))+ " daughters for object "+str(o.id)+" at "+str(o.t),0)
                    #Remove mother links in lineage
                    for m in o.mothers:
                        if dataset.del_mother(o,m):
                            links_deleted+=1
                    #Remove daughter links in lineage
                    ds = o.daughters.copy()
                    for d in ds:
                        if dataset.del_daughter(o,d):
                            links_deleted+=1
        printv(str(links_deleted) + " links where deleted", 0)
        #Send data to morphonet
        self.restart(cancel=links_deleted==0)
