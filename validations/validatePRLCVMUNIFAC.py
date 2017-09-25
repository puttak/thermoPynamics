#coding: utf-8
from ThermoPkgs.PR_LCVM_UNIFAC.PR_LCVM_UNIFAC import PR_LCVM_UNIFAC
from ThermoPkgs.PR_LCVM_UNIFAC.interfacePRLCVMUNIFAC import FluidDataPRLCVMUNIFAC, FluidPRLCVMUNIFAC
from ThermoPkgs.UNIFAC.interface import FluiDataUNIFAC
import numpy as np

def write_fug(computefunction, T, y, Pvec):
    conditions = open('conditions.dat','w')
    outputfileVapor = open('outputVapor.dat', 'w')
    outputfileLiquid = open('outputLiquid.dat', 'w')

    for i in range(len(Pvec)):
        fvapor = computefunction(T,Pvec[i],y,'vapor')
        fvapor = np.log(fvapor)
        fliquid = computefunction(T, Pvec[i], y, 'liquid')
        fliquid = np.log(fliquid)
        conditions.write('P=' + str(Pvec[i])+'\n')

        outputfileLiquid.write(str(fliquid)+'\n')
        outputfileVapor.write(str(fvapor) + '\n')


    outputfileLiquid.close()
    outputfileVapor.close()
    conditions.close()

ID=[194,342]
globalComposition=[0.9, 0.1]
T=350 #Kelvin

Pvec=[0.1, 0.5, 1.0]
x=np.linspace(10.0, 100, 10 )
for xi in x:
    Pvec.append(xi)

fluido = FluidPRLCVMUNIFAC(ID)

eosdata = FluidDataPRLCVMUNIFAC(fluido)
unifacdata = FluiDataUNIFAC(fluido)

eos = PR_LCVM_UNIFAC(fluido, eosdata, unifacdata)

write_fug(eos.computeFUG,T, globalComposition,Pvec )
'''
condições:
ID=[194,342]
globalComposition=[0.9, 0.1]
T=350 #Kelvin

Pvec=[0.1, 0.5, 1.0]
x=np.linspace(10.0, 100, 10 )
for xi in x:
    Pvec.append(xi)

outputliquid: 
[ 2.89574288  1.84185683]
[ 1.28689569  0.23234054]
[ 0.59448721 -0.46090359]
[-1.69474589 -2.76504447]
[-2.3729426  -3.45952229]
[-2.76334781 -3.86593135]
[-3.03587098 -4.15420026]
[-3.24376585 -4.37759978]
[-3.41075705 -4.55986989]
[-3.54950292 -4.7136827 ]
[-3.66756147 -4.84660871]
[-3.76980938 -4.96353593]
[-3.85957764 -5.06780568] '''

'''outputVapor:
[-0.00158253 -0.00146191]
[-0.00792986 -0.00732677]
[-0.01590338 -0.0146972 ]
[-0.16830943 -0.15624064]
[-0.36866324 -0.34446666]
[-2.76334781 -3.86593135]
[-3.03587098 -4.15420026]
[-3.24376585 -4.37759978]
[-3.41075705 -4.55986989]
[-3.54950292 -4.7136827 ]
[-3.66756147 -4.84660871]
[-3.76980938 -4.96353593]
[-3.85957764 -5.06780568]'''
