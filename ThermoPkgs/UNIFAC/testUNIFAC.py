#coding: utf-8
from databases.GetDataBaseDir import GetDataBaseDir
from UNIFAC import UNIFAC
from interface import Fluid, FluiDataUNIFAC
import time
start = time.time()

fluido = Fluid(ID=[5,279])

data = FluiDataUNIFAC(fluido)
a=UNIFAC(fluido, data)

a.computeGama(307, [0.047, 1-0.047])


end = time.time()

print 'durou '+str(end-start)+' segundos'



