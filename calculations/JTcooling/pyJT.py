#coding: utf-8
import numpy as np
import scipy.optimize as scyopt
from ThermoPkgs.IDEAL.Ideal import Ideal



class JT:
    def __init__(self, T1,P1,ID, y, fase, flagEOS, **kwargs):
        #T em K e P em bar.

       #################################################################################################################
        ############### VERIFICAÇÃO DOS INPUTS E ARMAZENAMENTO COMO ATRIBUTOS DA CLASSE ################################

        self.T1 = float(T1)
        self.P1 = float(P1)

        self.modelosSuportados = ['SRK', 'PR', 'PRLCVMUNIFAC', 'PRLCVMmodUNIFAC']
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

        argumentos = ['analytical']

        for key, valor in kwargs.items():
            assert key in argumentos

        try:
            analitical = kwargs['analytical']
            assert type(analitical) is bool
            analitical_UserDefined = True
        except:
            analitical=False
            analitical_UserDefined = False

        ################################################################################################################
        if flagEOS == 'SRK':
            import ThermoPkgs.SRK.SRK as tmp
            from ThermoPkgs.SRK.interfaceSRK import FluidDataSRK, FluidSRK
            fluid = FluidSRK(self.ID)
            fluidData = FluidDataSRK(fluid)
            self.thermoObj = tmp.SRK(fluid, fluidData)

            if not analitical_UserDefined:
                self.HRfunc = self.thermoObj.computeResidualEnthalpy
            else:
                if analitical:
                    self.HRfunc = self.thermoObj.computeResidualEnthalpy
                else:
                    self.HRfunc = self.thermoObj.computeHR_numerical

        elif flagEOS == 'PR':
            import ThermoPkgs.PR.PR as tmp
            from ThermoPkgs.PR.interfacePR import FluidPR, FluidDataPR
            fluid = FluidPR(self.ID)
            fluidData = FluidDataPR(fluid)
            self.thermoObj = tmp.PR(fluid, fluidData)

            if not analitical_UserDefined:
                self.HRfunc = self.thermoObj.computeResidualEnthalpy
            else:
                if analitical:
                    self.HRfunc = self.thermoObj.computeResidualEnthalpy
                else:
                    self.HRfunc = self.thermoObj.computeHR_numerical
        elif flagEOS == 'PRLCVMUNIFAC':
            import ThermoPkgs.PR_LCVM_UNIFAC.PR_LCVM_UNIFAC as tmp
            from ThermoPkgs.PR_LCVM_UNIFAC.interfacePRLCVMUNIFAC import FluidDataPRLCVMUNIFAC, FluidPRLCVMUNIFAC
            from ThermoPkgs.UNIFAC.interface import FluiDataUNIFAC
            fluid = FluidPRLCVMUNIFAC(self.ID)
            fluidData = FluidDataPRLCVMUNIFAC(fluid)
            unifacdata = FluiDataUNIFAC(fluid)
            self.thermoObj = tmp.PR_LCVM_UNIFAC(fluid, fluidData, unifacdata)

            if analitical:
                raise RuntimeError('PRLCVMUNIFAC não suporta entalpia residual calculada analiticamente')
            else:
                self.HRfunc = self.thermoObj.computeHR_numerical

        elif flagEOS == 'PRLCVMmodUNIFAC':
            import ThermoPkgs.PR_LCVM_modUNIFAC.PR_LCVM_UNIFAC as tmp
            from ThermoPkgs.PR_LCVM_modUNIFAC.interfacePRLCVMUNIFAC import FluidDataPRLCVMUNIFAC, FluidPRLCVMUNIFAC
            from ThermoPkgs.modUNIFAC.interface import FluiDataUNIFAC
            fluid = FluidPRLCVMUNIFAC(self.ID)
            fluidData = FluidDataPRLCVMUNIFAC(fluid)
            unifacdata = FluiDataUNIFAC(fluid)
            self.thermoObj = tmp.PR_LCVM_UNIFAC(fluid, fluidData, unifacdata)

            if analitical:
                raise RuntimeError('PRLCVMUNIFAC não suporta entalpia residual calculada analiticamente')
            else:
                self.HRfunc = self.thermoObj.computeHR_numerical
        else:
            raise RuntimeError('EOS %s not supported yet in JT' % (flagEOS))

        self.R = self.thermoObj.R
        self.CPobject = Ideal (self.ID, self.y, self.R)


    def computeT2(self, P2,T2guess=None):
        self.P2=float(P2)
        self.HR1 = self.HRfunc(self.T1,self.P1, self.y, self.fase)

        if T2guess==None:
            CPt1 = self.CPobject.computeCP(self.T1)
            T2guess=self.T1 + self.HR1/CPt1
        raiz = scyopt.newton(self.fT2, T2guess)
        return raiz


    def fT2(self, T2):
        integralCp = self.CPobject.computeMeanCP(Tlower=self.T1, Tupper=T2)*(T2-self.T1)
        HR2 = self.HRfunc(T2,self.P2,self.y,self.fase)
        f = integralCp + self.HR1 - HR2
        return f









