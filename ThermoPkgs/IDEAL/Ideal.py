#coding: utf-8
import numpy as np
from GetDataSQLIdealCp import ReadData


class Ideal:
    def __init__(self, ID, y, R):

        self.ID = ID
        self.NC = len(ID)
        self.y = y
        self.R = R
        assert len(self.y)==self.NC
        data = ReadData(ID)
        self.CPcoefficients = data.CoefficientsCP

    def computeCP(self,T):

        coefs = self.CPcoefficients
        CpComponent_i=[]
        CP=0.0
        for i in range(self.NC):
            a0 = float( coefs[0][i])
            a1 = float(coefs[1][i])
            a2 = float(coefs[2][i])
            a3 = float(coefs[3][i])
            a4 = float(coefs[4][i])

            cpAdmensional = a0 + a1*T + a2*T**2 + a3*T**3 + a4*T**4
            CpComponent_i.append(cpAdmensional)
            CP += self.y[i]*CpComponent_i[i]

        CP=CP*self.R

        return CP


    def computeMeanCP(self,Tlower,Tupper):
        if float(Tlower) == float(Tupper):
            Tupper=Tupper*1.0000001

        coefs = self.CPcoefficients

        dif1 = Tupper - Tlower
        dif2 =  Tupper**2-Tlower**2
        dif3 =  Tupper**3-Tlower**3
        dif4 = Tupper**4-Tlower**4
        dif5 = Tupper**5-Tlower**5

        A=0.0
        B=0.0
        C=0.0
        D=0.0
        E=0.0
        for i in range(self.NC):

            A += float(coefs[0][i])*self.y[i]
            B += float(coefs[1][i])*self.y[i]
            C += float(coefs[2][i])*self.y[i]
            D += float(coefs[3][i])*self.y[i]
            E += float(coefs[4][i])*self.y[i]

        intgCP = A*dif1 + B/2*dif2 + C/3*dif3 + D/4*dif4 +E/5*dif5

        return self.R*intgCP/dif1




