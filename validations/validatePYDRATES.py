#coding: utf-8

from calculations.hydrates.PCAL import PCAL
import time
start=time.time()

a=PCAL(ID=[193, 125,295,47,249], y=[0.79942,0.05029,0.03000,0.02090,0.09939],isThereInib=1, InibID=[346],InibMassFraction=[0.1], flagEOS='PRLCVMUNIFAC', flagGamma='UNIFAC')

print a.computePD(275.0,1.0) #=278.508

end=time.time()

print 'Execução levou ' + str( end - start) + ' segundos'