#coding: utf-8
import numpy as np
import scipy.optimize as scyopt
from ThermoPkgs.IDEAL.Ideal import Ideal



class JT:
    def __init__(self, T1,P1,ID, y, fase, flagEOS):
        #T em K e P em bar.

       #################################################################################################################
        ############### VERIFICAÇÃO DOS INPUTS E ARMAZENAMENTO COMO ATRIBUTOS DA CLASSE ################################

        self.T1 = float(T1)
        self.P1 = float(P1)

        self.modelosSuportados = ['SRK', 'PR']
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

        assert flagEOS in self.modelosSuportados
        ################################################################################################################
        if flagEOS == 'SRK':
            import ThermoPkgs.SRK.SRK as tmp
            from ThermoPkgs.SRK.interfaceSRK import FluidDataSRK, FluidSRK
            fluid = FluidSRK(self.ID)
            fluidData = FluidDataSRK(fluid)
            self.thermoObj = tmp.SRK(fluid, fluidData)
        elif flagEOS == 'PR':
            import ThermoPkgs.PR.PR as tmp
            from ThermoPkgs.PR.interfacePR import FluidPR, FluidDataPR
            fluid = FluidPR(self.ID)
            fluidData = FluidDataPR(fluid)
            self.thermoObj = tmp.PR(fluid, fluidData)
        else:
            raise RuntimeError('EOS %s not supported yet in JT' % (flagEOS))

        self.R = self.thermoObj.R
        self.CPobject = Ideal (self.ID, self.y, self.R)


    def computeT2(self, P2,T2guess=None):
        self.P2=float(P2)
        self.HR1 = self.thermoObj.computeResidualEnthalpy(self.T1,self.P1, self.y, self.fase)

        if T2guess==None:
            CPt1 = self.CPobject.computeCP(self.T1)
            T2guess=self.T1 + self.HR1/CPt1
        raiz = scyopt.newton(self.fT2, T2guess)
        return raiz


    def fT2(self, T2):
        integralCp = self.CPobject.computeMeanCP(Tlower=self.T1, Tupper=T2)*(T2-self.T1)
        HR2 = self.thermoObj.computeResidualEnthalpy(T2,self.P2,self.y,self.fase)
        f = integralCp + self.HR1 - HR2
        return f









