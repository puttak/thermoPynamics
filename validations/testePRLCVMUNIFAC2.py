from ThermoPkgs.PR_LCVM_UNIFAC.PR_LCVM_UNIFAC import PR_LCVM_UNIFAC
from ThermoPkgs.PR_LCVM_UNIFAC.interface import Fluid, FluidData
from ThermoPkgs.UNIFAC.interface import FluiDataUNIFAC
import scipy.optimize as opt
import numpy as np
import matplotlib.pyplot as plt

# fluido=Fluid([194,342], [0.1, 0.9])
# fdata=FluidData(fluido)
# unidata=FluiDataUNIFAC(fluido)
#
# a=PR_LCVM_UNIFAC(fluido, fdata, unidata)
#
# print a.computeZ(300,1.0, 'liquid')
#
# print a.computeFUG(300, 1.0, 'liquid')
#
# print a.computeZ(300,1.0, 'vapor')
#
# print a.computeFUG(300, 1.0, 'vapor')



class PhaseEquilibria:
    def __init__(self, ID):
        self.ID = ID
        self.NC = len(ID)

    def BolP(self, T, x):
        fluido_L = Fluid(self.ID, x)
        fdata_L = FluidData(fluido_L)
        unidata_L = FluiDataUNIFAC(fluido_L)
        self.liquido=PR_LCVM_UNIFAC(fluido_L, fdata_L, unidata_L)
        self.T=T
        self.x_L=x

        X0=[0.3]
        for i in range(self.NC-1):
            X0.append(x[i])

        X0=np.array(X0)
        bd=((0.0,None), (0.0, 1.0))
        Xraiz = opt.minimize(self.__bol, X0, bounds=bd).x

        return Xraiz



    def __bol(self,X):
        P = abs(X[0])
        y=[]
        for i in range(self.NC-1):
            y.append(abs(X[i+1]))
        y.append(1-sum(y))

        fluido_V = Fluid( self.ID, y )
        fdata_V = FluidData(fluido_V)
        unidata_V = FluiDataUNIFAC(fluido_V)
        vapor = PR_LCVM_UNIFAC(fluido_V, fdata_V, unidata_V)

        fi_L = self.liquido.computeFUG(self.T, P, 'liquid')
        fi_V = vapor.computeFUG(self.T, P, 'vapor')
        F = []

        for i in range(self.NC):
            F.append((self.x_L[i]*fi_L[i]-y[i]*fi_V[i])**2)

        return sum(F)

testando_porfavor = PhaseEquilibria([194,342])

# x=0.01
# print testando_porfavor.BolP(330,[x, 1-x])

x1=np.linspace(0.0, 1.0,50)

resultados = [ testando_porfavor.BolP(330,[x1i,1-x1i])  for x1i in x1]
y = [ ]
P=[]

for i in range(len(x1)):
    y.append(resultados[i][1])
    P.append(resultados[i][0])
# print P
# print y
plt.plot(x1,P, y, P)
plt.show()
print resultados



