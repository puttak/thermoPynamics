#coding: utf-8
from databases.GetDataBaseDir import GetDataBaseDir
from UNIFAC import UNIFAC
from interface import Fluid, FluiDataUNIFAC
import time
start = time.time()

fluido = Fluid(ID=[193,125], z=[1.0])

data = FluiDataUNIFAC(fluido)

end = time.time()

print 'durou '+str(end-start)+' segundos'



