#coding: utf-8
from databases.GetDataBaseDir import GetDataBaseDir
from UNIFAC import UNIFAC
from interface import Fluid, FluiDataUNIFAC

fluido = Fluid(ID=[342], z=[1.0])

data = FluiDataUNIFAC(fluido)



