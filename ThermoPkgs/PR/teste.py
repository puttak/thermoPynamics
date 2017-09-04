import numpy as np
import matplotlib.pyplot as plt
from PR import PR
from interface import Fluid, FluidData
fluido=Fluid(ID=[10], z=[1.0])
dados=FluidData(fluido)
co2=PR(fluido, dados)


print co2.computeZ(dados.Tc[0],dados.Pc[0], 'vapor') #Z=0.321379025174



