# -*- coding: latin-1 -*-
defaultPlugins=[]

from .Addlink import Addlink
defaultPlugins.append(Addlink())

from .Delink import Delink
defaultPlugins.append(Delink())

from .Tracko import Tracko
defaultPlugins.append(Tracko())