#coding: utf-8
import numpy as np
import scipy.optimize as scyopt
import ThermoPkgs.SRK.SRK as tmp
from ThermoPkgs.SRK.interface import FluidData, Fluid
from ThermoPkgs.IDEAL.Ideal import Ideal


class JT:
    def __init__(self, T1,P1,ID, y, fase, flagEOS):
        #T em K e P em bar.

       #################################################################################################################
        ############### VERIFICAÇÃO DOS INPUTS E ARMAZENAMENTO COMO ATRIBUTOS DA CLASSE ################################

        self.T1 = float(T1)
        self.P1 = float(P1)

        self.modelosSuportados = ['SRK']
        self.ID = ID
        self.NC = len(ID)
        self.y  = y
        self.fase = fase
        self.flagEOS = flagEOS

        bol1 =  type(self.T1) == float and type(self.P1) == float

        bol1 = bol1 and len(y) == self.NC and self.fase in ['vapor', 'liquid'] and self.flagEOS in self.modelosSuportados
        try:
            assert bol1
        except:
            raise ValueError('Problema nos inputs de JT')
        ################################################################################################################

        fluid = Fluid(self.ID, self.y)
        fluidData = FluidData(fluid)
        #TODO: por um if que escolhe o modelo. passar computeHR para o arquivo da EoS.
        self.thermoObj = tmp.SRK( fluid, fluidData)

        self.R = self.thermoObj.R
        self.CPobject = Ideal (self.ID, self.y, self.R)


    def computeT2(self, P2,T2guess=None):
        self.P2=float(P2)

        self.HR1 = self.computeResidualEnthalpy(T=self.T1, P=self.P1)

        if T2guess==None:
            CPt1 = self.CPobject.computeCP(self.T1)
            T2guess=self.T1 + self.HR1/CPt1
        raiz = scyopt.newton(self.fT2, T2guess)
        return raiz



    def computeResidualEnthalpy(self, T, P):
        Z = self.thermoObj.computeZ(T=T, P=P, Phase=self.fase)
        Tr = T/self.thermoObj.Tc[0]
        m = 0.480 + 1.574 * self.thermoObj.w[0] - 0.176 * self.thermoObj.w[0] ** 2
        a=self.thermoObj.ai_aaa[0]
        alfaT = (1 + m * (1 - (T / self.thermoObj.Tc[0]) ** 0.5)) ** 2
        dadT = a*(alfaT)**0.5*(-m*Tr**0.5/T)
        b=self.thermoObj.bSRK
        v=Z*self.R*T/P
        parcela1 = (a-T*dadT)/b
        HR = self.R*T*(1-Z) + parcela1*np.log(1+b/v)

        return HR


    def fT2(self, T2):
        integralCp = self.CPobject.computeMeanCP(Tlower=self.T1, Tupper=T2)*(T2-self.T1)

        HR2 = self.computeResidualEnthalpy(T=T2, P=self.P2)
        f = integralCp + self.HR1 - HR2

        return f









