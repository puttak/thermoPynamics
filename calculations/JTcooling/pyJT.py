#coding: utf-8
import scipy.optimize as scyopt
import numpy as np
from ThermoPkgs.IDEAL.Ideal import Ideal
import matplotlib.pyplot as plt
import datetime


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
        del self.P2
        return raiz


    def fT2(self, T2):
        integralCp = self.CPobject.computeMeanCP(Tlower=self.T1, Tupper=T2)*(T2-self.T1)
        HR2 = self.HRfunc(T2,self.P2,self.y,self.fase)
        f = integralCp + self.HR1 - HR2
        return f

    def computeP2(self, T2, P2guess = None):
        self.T2=float(T2)
        self.HR1 = self.HRfunc(self.T1,self.P1, self.y, self.fase)
        if P2guess==None:
            P2guess = self.P1*0.8
        raiz = scyopt.newton(self.fP2, P2guess)
        del self.T2
        return raiz

    def fP2(self,P2):
        integralCp = self.CPobject.computeMeanCP(Tlower=self.T1, Tupper=self.T2)*(self.T2-self.T1)
        HR2 = self.HRfunc(self.T2,P2,self.y,self.fase)
        f = integralCp + self.HR1 - HR2
        return f



class PlotIsenthalpic:
    def __init__(self, ID, T1,P1,z, Phase, flagEOS):

        self.ID = ID
        self.T1 = T1
        self.P1 = P1
        self.z = z
        self.Phase = Phase
        self.flagEOS = flagEOS
        self.JTinstance = JT(self.T1, self.P1, self.ID, self.z, self.Phase, self.flagEOS)

    def figura(self, Plimits, NumberOfPoints = 10):
        assert type(Plimits)== list
        assert len(Plimits) == 2

        Pmin = min(Plimits)
        Pmax = max(Plimits)

        Pvec = np.linspace(Pmin, Pmax, NumberOfPoints)

        Tvec = []


        for p in Pvec:
            T2 = self.JTinstance.computeT2(p, self.T1)
            Tvec.append(T2)


        figura = plt.figure()
        plt.plot(Tvec, Pvec)
        return figura

    def plot(self, Plimits, NumberOfPoints = 10):
        f = self.figura(Plimits, NumberOfPoints)
        plt.show()

    def saveFig(self, Plimits, NumberOfPoints = 10):
        f = self.figura(Plimits, NumberOfPoints)

        now = datetime.datetime.now()
        tempo = [now.year, now.month, now.day, now.hour, now.minute, now.second]
        stringa = ''
        for s in tempo:
            stringa = stringa + str(s) + '_'
        stringa = stringa[:-1]
        import calculations.outputfiles.GetoutputPath
        pat = calculations.outputfiles.GetoutputPath.thisPath()
        fileName = pat+stringa + 'isenthalPic.png'
        plt.savefig(fileName)
