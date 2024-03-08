# -*- coding: latin-1 -*-
defaultPlugins=[]

from .Seedio import Seedio
defaultPlugins.append(Seedio())

from .Seedin import Seedin
defaultPlugins.append(Seedin())

from .Seedis import Seedis
defaultPlugins.append(Seedis())

from .Seedax import Seedax
defaultPlugins.append(Seedax())

from .Seedero import Seedero
defaultPlugins.append(Seedero())