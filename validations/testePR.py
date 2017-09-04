#coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from ThermoPkgs.PR.PR import PR
from ThermoPkgs.PR.interface import Fluid, FluidData
import time

start=time.time()

fluido=Fluid(ID=[10], z=[1.0])
dados=FluidData(fluido)
co2=PR(fluido, dados)

end=time.time()

print co2.computeZ(dados.Tc[0],dados.Pc[0], 'vapor') #Z=0.321379025174

print 'Execução levou ' + str( end - start) + ' segundos'



