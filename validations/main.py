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

xi=np.array(range(11))
li=np.array(range(11))
print xi, li, xi*li
print sum(xi*li)