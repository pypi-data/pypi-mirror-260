# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np
from ..functions import _centerInShape,get_seeds_in_image,watershed,gaussian
from ...tools import printv


class Wati(MorphoPlugin):
    """ This plugin creates new objects using a watershed algorithm from seed generated or placed in the MorphoNet Viewer.
    The watershed algorithm generates new objects based on the intensity image  for each seed that is not in another object.
    If the new generated objects are under the volume threshold defined by the user, the object is not created.

   
    Parameters
    ----------
    sigma : int, default :2
        The standard deviation for the Gaussian kernel when sigma>0, the plugin first applies a gaussian filter on the
        intensity image. (>=0)
    minimum volume: int, default : 1000
        The minimal volume (in number of voxels) allowed for the new objects to be created (>=0)
    box size: int, default : 50
         Boundaries (in number of voxel) of working area around a seed to generate a new object (>=0)
    Seeds: Coordinate List
        List of seeds added on the MorphoNet Window

    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self)
        self.set_icon_name("Wati.png")
        self.set_image_name("Wati.png")
        self.set_name("Wati : Perform a watershed segmentation on intensity images (without selected objects)")
        self.add_inputfield("Membrane Channel", default=0)
        self.add_inputfield("Segmentation Channel", default=0)
        self.add_inputfield("sigma",default=2)
        self.add_inputfield("minimum volume",default=1000)
        self.add_inputfield("box size", default=50)
        self.add_coordinates("Add a Seed")
        self.set_parent("Create Segmentation from Seeds")
        self.set_description("This plugin creates new objects using a watershed algorithm from seed generated or placed "
                             "in the MorphoNet Viewer. The watershed algorithm generates new objects based on the "
                             "intensity image  for each seed that is not in another object. If the new generated "
                             "objects are under the volume threshold defined by the user, the object is not created.")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,objects_require=False):
            return None

        s_sigma=int(self.get_inputfield("sigma")) #Get the smoothing applied to the raw images from user
        min_vol=int(self.get_inputfield("minimum volume")) #Get the threshold volume for new cells from user
        box_size = int(self.get_inputfield("box size")) #Get the box size around the seed to watershed from user
        membrane_channel = int(self.get_inputfield("Membrane Channel"))
        segmentation_channel = int(self.get_inputfield("Segmentation Channel"))

        data=dataset.get_seg(t,segmentation_channel)#Load segmentation in memory
        rawdata=dataset.get_raw(t,membrane_channel)  #Load raw images in memory
        if rawdata is None:#Plugin can't work without raw images
            return

        if data is None: #If segmentation is empty , we can still work with an empty image
            data=np.zeros(rawdata.shape).astype(np.uint16)

        seeds = self.get_coordinates("Add a Seed") #Get the list of morphonet seed
        if len(seeds) == 0:
            printv("no seeds for watershed",0)
            return None
        printv("Found " + str(len(seeds)) + " seeds ",1)

        dataset.get_center(data)  #Get the segmentation center
        seeds = get_seeds_in_image(dataset, seeds)#Seeds from morphonet space to segmentation space
        new_seed=[]
        for seed in seeds:

            if _centerInShape(seed,data.shape): #If the seed is inside the segmentation
                olid=data[seed[0],seed[1],seed[2]]
                if olid==dataset.background:  #If the seed is in the backgrund, we can create a cell
                    new_seed.append(seed)
                    printv("add seed "+str(seed),1)
                # if not, remove the seed from working list
                else:
                    printv("remove this seed "+str(seed)+ " which already correspond to cell "+str(olid),1)
            else:
                printv("this seed "+str(seed)+ " is out of the image",1)
        #If no seeds are correct , stop here
        if len(new_seed)==0:
            self.restart()
            return None

        #Create a working box around the seeds to constrain the segmentation
        if box_size>0:
            seedsa = np.array(new_seed)
            box_coords = {}
            for i in range(3):
                mi=max(0,seedsa[:,i].min()-box_size)
                ma=min(data.shape[i],seedsa[:,i].max()+box_size)
                box_coords[i]=[mi,ma]

            #Only get theraw data around the boxes
            ndata=data[box_coords[0][0]:box_coords[0][1],box_coords[1][0]:box_coords[1][1],box_coords[2][0]:box_coords[2][1]]
            rawdata = rawdata[box_coords[0][0]:box_coords[0][1], box_coords[1][0]:box_coords[1][1],
                      box_coords[2][0]:box_coords[2][1]]
            #Smooth the raw data if needed
            if s_sigma>0:
                printv("Perform gaussian with sigma=" + str(s_sigma) +" for box "+str(box_coords),0)
                rawdata = gaussian(rawdata, sigma=s_sigma, preserve_range=True)

            #Seed replaced in the box
            box_seed=[]
            for s in new_seed:
                box_seed.append([s[0]-box_coords[0][0],s[1]-box_coords[1][0],s[2]-box_coords[2][0]])
            new_seed=box_seed
        #If no box specified, gaussian the raw data
        else:
            rawdata = self.gaussian_rawdata(t, sigma=s_sigma, preserve_range=True)
            ndata=data

        # Mark the box borders for the segmentation
        markers=np.zeros(ndata.shape,dtype=np.uint16)
        markers[0,:,:]=1
        markers[:,0,:]=1
        markers[:,:,0]=1
        markers[ndata.shape[0]-1,:,:]=1
        markers[:,ndata.shape[1]-1,:]=1
        markers[:,:,ndata.shape[2]-1]=1

        #Mark the seeds in the watershed markers (seeds source) images, with unique ids
        newId=2
        for seed in new_seed: #For Each Seeds ...
            markers[seed[0],seed[1],seed[2]]=newId
            newId+=1

        #Create the mark to work on for the watershed from the box
        mask=np.ones(ndata.shape,dtype=bool)
        mask[ndata!=dataset.background]=False

        #Watershed on the rawdata , constrained by the mask  , using seed images computed
        printv("Process watershed with "+str( len(new_seed))+" seeds",0)
        labelw=watershed(rawdata,markers=markers, mask=mask)

        #next id is the segmentation max + 1
        cMax=data.max()+1
        nbc = 0
        #Compute the id new cells created by watershed
        new_ids=np.unique(labelw)
        #Borders are not cells
        new_ids=new_ids[new_ids>1] #REMOVE THE BORDERS
        #If we created at least a cell
        if len(new_ids)>0:
            printv("Combine new objects",1)
            cells_updated = []
            #For each cell
            for new_id in new_ids:
                #Compute its mask coordinates
                newIdCoord=np.where(labelw==new_id)
                #If the volume is above the user threshold
                if len(newIdCoord[0])>min_vol:
                    #Compute its coordinate in the segmentation space
                    if box_size>0:
                        newIdCoord=(newIdCoord[0]+box_coords[0][0],newIdCoord[1]+box_coords[1][0],newIdCoord[2]+box_coords[2][0])
                    #Write the new cell in the segmentation
                    data[newIdCoord]=cMax+nbc
                    printv("add object "+str(nbc+cMax)+' with  '+str(len(newIdCoord[0]))+ " voxels",0)
                    cells_updated.append(cMax + nbc)
                    nbc+=1
                else:
                    printv("remove object with  "+str(len(newIdCoord[0]))+ " voxels",0)
            if len(cells_updated)>0:
                #Save the new cells in morphonet data
                dataset.set_seg(t, data,channel=segmentation_channel, cells_updated=cells_updated)
        printv("Found  "+str(nbc)+" new labels",0)
        #Send everything back to MorphoNet
        self.restart()




