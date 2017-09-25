#coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from ThermoPkgs.SRK.SRK import SRK
from ThermoPkgs.SRK.interfaceSRK import FluidSRK, FluidDataSRK
import time

start=time.time()

fluido=FluidSRK(ID=[10])
dados=FluidDataSRK(fluido)
co2=SRK(fluido, dados)

end=time.time()

print co2.computeZ(dados.Tc[0],dados.Pc[0], [1],'vapor') #Z=0.34666413738

print 'Execução levou ' + str( end - start) + ' segundos'



