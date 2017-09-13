#coding: utf-8
from ThermoPkgs.PR.PR import PR
from ThermoPkgs.PR.interface import FluidData, Fluid
import numpy as np
##############
## Aqui será colocado os testes em geral. Validações são adicionadas separadamente quando um novo módulo é terminado. ####
#TODO: Olhar TODOS

#
#
# fluido=Fluid(ID=[31,47], z=[0.5, 0.5])
# fdata=FluidData(fluido)
#
# eos=PR(fluido, fdata)
#
# print eos.computeFUG(300, 1, 'vapor')
#
x=[0.0, 0,0,1.0]

for i in range(len(x)):
    if x[i] == 0:
        x[i] = 1E-12
        for ii in range(len(x)):
            x[ii]=x[ii]/sum(x)

print x
