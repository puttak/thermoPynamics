#coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from ThermoPkgs.PR.PR import PR
from ThermoPkgs.PR.interfacePR import FluidPR, FluidDataPR
import time

start=time.time()

fluido=FluidPR(ID=[10])
dados=FluidDataPR(fluido)
co2=PR(fluido, dados)

end=time.time()

print co2.computeZ(dados.Tc[0],dados.Pc[0], [1],'vapor') #Z=0.321379025174

print 'Execução levou ' + str( end - start) + ' segundos'



