#coding: utf-8

import scipy.optimize as opt
from calculations.hydrates.PCAL import PCAL
from calculations.JTcooling.pyJT import JT
import numpy as np




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


