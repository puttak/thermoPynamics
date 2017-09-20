#coding: utf-8
from ThermoPkgs.PR.PR import PR
from ThermoPkgs.PR.interfacePR import FluidDataPR, FluidPR
import numpy as np
from ThermoPkgs.SRK.SRK import SRK
import matplotlib.pyplot as plt
##############
## Aqui será colocado os testes em geral. Validações são adicionadas separadamente quando um novo módulo é terminado. ####
#TODO: Olhar TODOS

#
#
fluido=FluidPR(ID=[193, 31])
fdata=FluidDataPR(fluido)

eos=SRK(fluido, fdata)
P=np.linspace(0.1, 130, 1000)

f=[]
for p in P:
     f.append(eos.computeFUG(273.15+(100 - 32) / 9 * 5, p, z=[0.5, 0.5], Phase='liquid'))


dFdP = np.diff(f)/np.diff(P)
dfdp2 =[]

for i in range(len(P)):
    if 0==i:
        dfdp2.append((f[i+1][0]-f[i][0])/(P[i+1]-P[i]))
        continue
    dfdp2.append((f[i][0] - f[i-1][0]) / (P[i] - P[i-1]))

# plt.plot( P, f, P, dfdp2)
plt.plot( P, dfdp2)
axes=plt.gca()
axes.set_ylim([-0.5, 0.1])
plt.show()

