#coding: utf-8
from calculations.BolP.BolP import BolP
from ThermoPkgs.SRK.SRK import SRK
from ThermoPkgs.SRK.interfaceSRK import FluidSRK, FluidDataSRK
from ThermoPkgs.PR.PR import PR
import inspect
import time
import numpy as np
from ThermoPkgs.modUNIFAC.interface import Fluid, FluiDataUNIFAC
from ThermoPkgs.PR_LCVM_modUNIFAC.interfacePRLCVMUNIFAC import FluidPRLCVMUNIFAC,FluidDataPRLCVMUNIFAC
from ThermoPkgs.PR_LCVM_modUNIFAC.PR_LCVM_UNIFAC import PR_LCVM_UNIFAC
start=time.time()

ID=[47,194]
# fluido=FluidSRK(ID)
# fdata=FluidDataSRK(fluido)
#
# modelLiq=SRK(fluido, fdata)
# modelVap=SRK(fluido, fdata)
# modelLiq.kij=np.array([[0.0 ,0.0512],[0.0512 ,0.0]])
# modelVap.kij=np.array([[0.0 ,0.0512],[0.0512 ,0.0]])
fluido = FluidPRLCVMUNIFAC(ID)
fdata = FluidDataPRLCVMUNIFAC(fluido)
dataunifac=FluiDataUNIFAC(fluido)
modelLiq = PR_LCVM_UNIFAC(fluido, fdata, dataunifac)
modelVap = PR_LCVM_UNIFAC(fluido,fdata, dataunifac)
lam = -0.2
modelLiq.lamb=lam
modelVap.lamb=lam

a=BolP(modelLiq.computeFUG, modelVap.computeFUG, ID)
xvolatil=0.9002
# yco2 = 0.95
# print a.compute_Pbol_ybol(300, [xvolatil, 1 - xvolatil])
# a.plot_BolP_Pxy(273.15+25,50,[0.0596,0.1548,0.2601,0.3495,0.4886,0.6451,0.7685,0.9002])
# a.plot_BolP_xy(473)
a.write_BolP_xy(273.15+25, 30)
end = time.time()

print 'durou ' + str(end-start) + 'segundos'
