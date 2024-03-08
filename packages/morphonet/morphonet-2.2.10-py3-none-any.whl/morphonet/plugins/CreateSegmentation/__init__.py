# -*- coding: latin-1 -*-
defaultPlugins=[]

from .Stardist import Stardist
defaultPlugins.append(Stardist())

from .Cellpose import Cellpose
defaultPlugins.append(Cellpose())

from .CellPoseTrain import CellposeTrain
defaultPlugins.append(CellposeTrain())

from .Mars import Mars
defaultPlugins.append(Mars())

from .Binarize import Binarize
defaultPlugins.append(Binarize())
