#coding: utf-8

import scipy.optimize as opt
from calculations.hydrates.PCAL import PCAL
from calculations.JTcooling.pyJT import JT
import numpy as np

###Compute maximum pressure drop to avoid hydrate formation

class maxDeltaP:
    def __init__(self,T1,P1,ID,y):
        self.T1=T1
        self.P1=P1
        self.ID=ID
        self.y=y
        self.jt = JT(self.T1, self.P1, ID=self.ID, y=self.y,
                     fase='vapor', flagEOS='SRK')
        self.hyd = PCAL(ID=self.ID, y=self.y, isThereInib=0, InibID=None, InibMassFraction=None, flagEOS='SRK')



    def f_hyd(self,X):

        Tx=float(X[0])
        Px=float(X[1])

        return -Px + self.hyd.computePD(Tx,1.0)

    def f_jt(self,X):
        Tx=X[0]
        Px=X[1]

        return -Tx + self.jt.computeT2(Px)

    def sistema(self,X):
        f=[]
        f.append(self.f_hyd(X))
        f.append(self.f_jt(X))
        return f

    def solve(self,Xguess):
        xraiz=opt.fsolve(self.sistema,Xguess)
        return xraiz


class PlotHydLimit:
    def __init__(self, isotherms, P1initial, P1final, ID,y, NumberOfPoints=20):
        #Isotherms: ...List... contains the temperature which will be used in calculations.

        assert type(isotherms) in [list, np.ndarray]

        self.isotherms = isotherms

        assert type(P1final) in [int, float]
        self.P1final = P1final
        assert type(P1initial) in [int, float]
        self.P1initial = P1initial
        self.NumberOfIsotherms = len(isotherms)

        self.P1vector = np.linspace(P1initial, P1final, NumberOfPoints)


    def computeValues(self):

        all_P2x=[]

        # for T in self.isotherms:
            #TODO:Computar os valores de P2 aqui inserindo P1





