#coding: utf-8

from calculations.JTcooling.pyJT import JT
import time

start=time.time()

ID=[193, 125,295,47,249]
y=[0.79942,0.05029,0.03000,0.02090,0.09939]

a=JT(300, 300, ID, y,fase='vapor',flagEOS='SRK')

#
print a.computeT2(280.0) #T2=298.531558557


end=time.time()

print 'Execução levou ' + str( end - start) + ' segundos'