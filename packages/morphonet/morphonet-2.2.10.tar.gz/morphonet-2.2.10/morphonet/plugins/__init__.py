# -*- coding: latin-1 -*-
from .MorphoPlugin import MorphoPlugin
__all__ = [
    'MorphoPlugin'
]

#from functions import  get_borders

defaultPlugins=[]


from .CreateSegmentation import defaultPlugins as DP
defaultPlugins+=DP

from .CreateSeeds import defaultPlugins as DP
defaultPlugins+=DP

from .CreateSegmentationFromSeeds import defaultPlugins as DP
defaultPlugins+=DP

from .EditObjects import defaultPlugins as DP
defaultPlugins+=DP


from .EditTemporalLinks import defaultPlugins as DP
defaultPlugins+=DP

from .PropagateSegmentation import defaultPlugins as DM
defaultPlugins+=DM
