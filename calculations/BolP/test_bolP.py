#coding: utf-8
from BolP import BolP
from ThermoPkgs.SRK.SRK import SRK
from ThermoPkgs.SRK.interfaceSRK import FluidSRK, FluidDataSRK
from ThermoPkgs.PR.PR import PR
import inspect
import time
start=time.time()
fluido=FluidSRK(ID=[193,31])
fdata=FluidDataSRK(fluido)

modelLiq=SRK(fluido, fdata)
modelVap=SRK(fluido, fdata)

def testando():
    pass

a=BolP(modelLiq.computeFUG, modelVap.computeFUG)

print a.compute_Pbol_ybol(273.15+(100-32)/9*5, [0.5, 0.5], GUESS_Pbol=80)

end = time.time()

print 'durou ' + str(end-start) + 'segundos'