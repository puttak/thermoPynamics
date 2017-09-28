#coding: utf-8
import numpy as np
from numpy import log as ALOG
from numpy import exp as EXP
import scipy.optimize as sciopt
import warnings
import GetInputPCALSQL as GetInput
import GetDataPCALSQL as GetData

class PCAL:
    def __init__(self,ID, y, isThereInib=None, InibID=None,InibMassFraction=None, flagEOS='SRK', flagGamma = None):

        self.InputPCAL = GetInput.GetInputPCAL(ID, y, isThereInib, InibID,InibMassFraction, flagEOS)

        self.HydrateDataSet = GetData.GetDataPCAL(self.InputPCAL)

        self.VM = [0.043478, 0.13043, 0.11765, 0.058823]

        if 295 in self.InputPCAL.ID:
            indice=self.InputPCAL.ID.index(295)
            if self.InputPCAL.y[indice]>=0.35:
                self.HydrateDataSet.EP[indice] = 203.31
                self.HydrateDataSet.SIG[indice] = 3.30931

        self.flagGamma = flagGamma
        if flagEOS=='SRK':
            import ThermoPkgs.SRK.SRK as tmp
            from ThermoPkgs.SRK.interfaceSRK import FluidDataSRK, FluidSRK
            fluid = FluidSRK(ID=self.InputPCAL.ID)
            fluidData = FluidDataSRK(fluid)
            self.faseVapor = tmp.SRK(fluid, fluidData)
        elif flagEOS=='PR':
            import ThermoPkgs.PR.PR as tmp
            from ThermoPkgs.PR.interfacePR import FluidDataPR, FluidPR
            fluid = FluidPR(ID=self.InputPCAL.ID)
            fluidData = FluidDataPR(fluid)
            self.faseVapor = tmp.PR(fluid, fluidData)
        elif flagEOS=='PRLCVMUNIFAC':
            import ThermoPkgs.PR_LCVM_UNIFAC.PR_LCVM_UNIFAC as tmp
            from ThermoPkgs.PR_LCVM_UNIFAC.interfacePRLCVMUNIFAC import FluidPRLCVMUNIFAC, FluidDataPRLCVMUNIFAC
            from ThermoPkgs.UNIFAC.interface import FluiDataUNIFAC
            fluid = FluidPRLCVMUNIFAC(ID=self.InputPCAL.ID)
            fluidData = FluidDataPRLCVMUNIFAC(fluid)
            unifacdata = FluiDataUNIFAC(fluid)
            self.faseVapor = tmp.PR_LCVM_UNIFAC(fluid, fluidData, unifacdata)
        elif flagEOS=='PRLCVMmodUNIFAC':
            import ThermoPkgs.PR_LCVM_modUNIFAC.PR_LCVM_UNIFAC as tmp
            from ThermoPkgs.PR_LCVM_modUNIFAC.interfacePRLCVMUNIFAC import FluidPRLCVMUNIFAC, FluidDataPRLCVMUNIFAC
            from ThermoPkgs.modUNIFAC.interface import FluiDataUNIFAC
            fluid = FluidPRLCVMUNIFAC(ID=self.InputPCAL.ID)
            fluidData = FluidDataPRLCVMUNIFAC(fluid)
            unifacdata = FluiDataUNIFAC(fluid)
            self.faseVapor = tmp.PR_LCVM_UNIFAC(fluid, fluidData, unifacdata)
        else:
            raise RuntimeError('EOS model not supported')

        if flagGamma=='UNIFAC':
            from ThermoPkgs.UNIFAC.UNIFAC import UNIFAC
            from ThermoPkgs.UNIFAC.interface import Fluid, FluiDataUNIFAC
            fluidounifac = Fluid(self.InputPCAL.IDaqPHASE)
            unifacdata = FluiDataUNIFAC(fluidounifac)
            self.GammaModel = UNIFAC(fluidounifac, unifacdata)
        elif flagGamma == 'modUNIFAC':
            from ThermoPkgs.modUNIFAC.UNIFAC import UNIFAC
            from ThermoPkgs.modUNIFAC.interface import Fluid, FluiDataUNIFAC
            fluidounifac = Fluid(self.InputPCAL.IDaqPHASE)
            unifacdata = FluiDataUNIFAC(fluidounifac)
            self.GammaModel = UNIFAC(fluidounifac, unifacdata)
        else:
            assert flagGamma==None

    def computePD(self,T, Pguess):

        self.T = float(T)

        P=Pguess
        P = P * 1.01325



        P = P / 1.01325

        R=1.987
        self.RT=R*T
        KIND=1
        if self.HydrateDataSet.NFH2 >=1:
            KIND=2

        pd=[]

        itmax = 1000
        tol = 1E-3
        self.SIMP(T)
        self.ACT()

        PII = -1
        if KIND == 2:

            P=Pguess
            Pnew=P
            self.IterationKind=KIND-1
            oldMinusNew=1.0
            count=0
            while oldMinusNew >= tol and count <= itmax:

                count += 1

                self.BLAT(self.IterationKind + 1)

                try:

                    Pnew = float(sciopt.newton(self.FZ, P, tol=1e-4))
                    # print 'pnew=', Pnew,'P=', P
                    # print oldMinusNew , 'old minus'
                    oldMinusNew = abs(Pnew - P) / P
                    P = Pnew

                except:
                    count=itmax+1
            PII = Pnew
            if count > itmax:
                warnings.warn('Cálculo assumindo estrutura 2 não convergiu em T= %s' % str(T))
                PII = -1


        P = Pguess
        Pnew = P
        self.IterationKind = 0
        oldMinusNew = 1.0
        count = 0
        while oldMinusNew >= tol and count <= itmax:

            count += 1

            self.BLAT(self.IterationKind + 1)

            try:
                Pnew = float(sciopt.newton(self.FZ, P, tol=1e-4))
                # print 'pnew=', Pnew,'P=', P
                # print oldMinusNew , 'old minus'
                oldMinusNew = abs(Pnew - P) / P
                P = Pnew

            except:
                count = itmax + 1
        PI = Pnew
        if count > itmax:
            warnings.warn('Cálculo assumindo estrutura 1 não convergiu em T= %s' % str(T))
            PI = -1

        result = [PI, PII]

        for i in range(2):
            if result[i] < 0.4: #Descarta possível raíz de pressão próxima de zero.
                result[i]=-1

        if result[0] == -1 and result[1] == -1:
            raise RuntimeError('Não convergiu pra valores reais')

        if min(result) != -1:
            Pd=min(result)
        else:
            Pd=max(result)

        self.HydrateType = result.index(Pd) +1

        return Pd



    def FZ(self,P):
        try:
            P = P[0]
        except: pass

        P = P * 1.01325 #Transformação pra bar.
        self.PHV = self.faseVapor.computeFUG(self.T, P, self.InputPCAL.y,'vapor')
        P = P / 1.01325  #Volta pra atm.

        SC = [0.0, 0.0]
        for I in [0, 1]:
            II = self.IterationKind* 2 + I
            for J in range(self.HydrateDataSet.NFH):
                SC[I] = SC[I] + self.CL[II][J] * self.InputPCAL.y[J] * self.PHV[J]
        self.SC = SC

        f = self.BO + P*self.DV/self.RT
        for I in [0,1]:
            II = self.IterationKind*2 + I
            f += -self.VM[II]*ALOG(1.0 + self.SC[I]*P)
        # print 'fz=',f
        # print 'KIND=', self.IterationKind+1
        # print 'f=',f, 'P=', P
        # print 'SC=', self.SC, 'bo=', self.BO, 'DV=', self.DV
        return f




    def SIMP(self, T=None):
        RC=[ 3.95,4.30,3.91,4.73 ]
        Z=[ 20.0 , 24.0 ,20.0 ,28.0 ]

        if T== None:
            T= 1*self.T

        CL=[ [0.0 for i in range(self.HydrateDataSet.NFH)] for j in range(4)  ]

        for j in range(self.HydrateDataSet.NFH):
            for i in range(4):
                if [self.HydrateDataSet.KTYPE[j], i+1] in [[1,1], [1,2], [1,4], [2,2], [2,4], [3,1], [3,2], [3,3], [3, 4], [4,4] ]:
                    A=self.HydrateDataSet.ACORE[j]/RC[i]
                    S1 = ((self.HydrateDataSet.SIG[j] / RC[i]) ** 6) * 2.0 * Z[i] * self.HydrateDataSet.EP[j] / T
                    S2 = S1 * ((self.HydrateDataSet.SIG[j] / RC[i]) ** 6)
                    SUM = 0.0
                    SUMN = 0.0
                    H = 0.02
                    RB = 0.0
                    N = 2

                    lista = [ iii +1 for iii in range(25)]
                    for L in lista:
                        RB = RB + H
                        SUMN = self.functionF1(RB, A, S1, S2) + SUMN
                        RB = RB + H
                        FTEST = 1*self.functionF1(RB , A, S1, S2)

                        if FTEST < 0.00000001:
                            break
                        N = N +2
                        SUM = SUM + 2*FTEST
                    if FTEST >= 0.00000001:
                        raise ValueError('Erro em SIMP')

                    XO = (SUM + 4 * SUMN + FTEST) * RB / float(3 * N)
                    XSE = 1*XO
                    LLL = 1*N
                    SUM = SUM + FTEST
                    X=1
                    xMenosxo = 1
                    # print 'N=', N, 'H=', H,
                    while abs(xMenosxo) >= 0.0001*X or N >= 1000:
                        N = 2 * N
                        SUM = SUM + 2.0 * SUMN
                        HO = 1*H
                        H = H / 2.0
                        KS = N / 2 - 1
                        SUMN = 0.0
                        KSlist = [ii for ii in range(KS)]
                        KSlist.append(KS)
                        for Ldo in KSlist:
                            SUMN = SUMN + self.functionF1(H + float(Ldo) * HO, A,S1,S2)
                        X = (SUM + SUMN * 4.0) * RB / float(3 * N)
                        xMenosxo = X-XO
                        XO = 1*X

                    if N>=1000:
                        raise ValueError('Não convergiu em SIMP')

                    CL[i][j]=(1/1.01325)*12.56637062 * X * (RC[i] ** 3) / (136.24 * T) #Convertido para 1/bar

        self.CL = CL














                        #Vou tentar por aqui dentro do IF, se ficar ruim, crio uma função


    def functionF1(self,R, A,S1,S2):
        F = lambda A, R, N: (1.0/((1.0-R-A)**N)-1.0/((1.0+R-A)**N))/float(N)
        F1 = S2 * (F(A, R, 10) + A * F(A, R, 11)) - S1 * (F(A, R, 4) + A * F(A, R, 5))
        F1 = np.exp(-F1 / R) * (R ** 2)
        return F1

    def ACT(self):
        self.TICE = 273.15
        GAMA = 1.0
        T = float(self.T)


        if self.InputPCAL.isThereInib == True:
            if self.InputPCAL.InibID == [194] and self.flagGamma == None:
                xMet = self.InputPCAL.XaqPHASE[-1]
                self.TICE = self.TICE - xMet * (
                93.622 + xMet * (528.971 - xMet * (5275. - xMet * (30491.3 - xMet * 61414.)))) - .01056
                if T >= self.TICE:
                    GAMA = 1.9462 * ((273.16 / self.TICE) - 1.0) - 4.5920 * np.log(273.16 / self.TICE)
                    GAMA = np.exp(GAMA)
                    GAMA = GAMA / (1.0 - xMet)
            elif self.flagGamma == None:
                raise RuntimeError('You must define a gamma model in order to use a inibihtor different from Methaol')




        self.GAMA = float(GAMA)
        self.InputPCAL.XaqPHASE = 1*self.InputPCAL.XaqPHASEwithoutGas
        if T >= self.TICE:
            for i in range(len(self.InputPCAL.ID)):
                A= float(self.HydrateDataSet.ASOL[i])
                B= float(self.HydrateDataSet.BSOL[i])
                C=float(self.HydrateDataSet.CSOL[i])
                D=float(self.HydrateDataSet.DSOL[i])

                correlacao = (A+B/T+C*np.log(T)+D*T)/1.9872
                GasSolub = np.exp(correlacao)
                self.InputPCAL.XaqPHASE[i]=float(GasSolub)
                self.InputPCAL.XaqPHASE[self.InputPCAL.IDaqPHASE.index(self.InputPCAL.idwater)] += - GasSolub

        if self.flagGamma != None:
            self.GAMA = self.GammaModel.computeGama(T, self.InputPCAL.XaqPHASE)
            self.GAMA = self.GAMA [ self.InputPCAL.IDaqPHASE.index(self.InputPCAL.idwater)]


        self.lnA = np.log( self.GAMA*self.InputPCAL.XaqPHASE[self.InputPCAL.IDaqPHASE.index(self.InputPCAL.idwater)]  )
        return

    def BLAT(self, KIND):
       A= [[23.0439, -1212.2, 0.0], [11.5115, -1023.14, 4071.64]]
       B= [[-3357.57, 44344.0, 0.0], [-4092.37, 34984.3, -193428.8]]
       C = [[-1.85, 187.719, 0.0], [0.316033, 159.923, -599.755]]

       TICE = self.TICE
       T = self.T
       R = 1.987

       RT = R * T
       TR = 273.15

       PR = 0.0

       IFLAG = 1
       if T > 273.15:
           IFLAG = 2

       if KIND == 1:
           SMU = 302.01
           HO = 275.66
           DV = 0.0726
       elif KIND ==2:
           DV = 0.0823
           HO = 193.0
           SMU = 211.0
       else:
           raise ValueError('KIND, indicador da estrutura do hidrato, pode somente assumir os valores 1 ou 2.')

       if T > 291.0 and KIND ==2:
           SMU = 320.902
           PR = 79.5065
           TR = 291.0
           IFLAG = 3


       AR = A[KIND-1][IFLAG-1]
       BR = B[KIND-1][IFLAG-1]
       CR = C[KIND-1][IFLAG-1]


       if T >= TICE:
           DV = DV + 0.0387
       PTR = np.exp(AR + BR/TR + CR*np.log(TR ) )
       PT = np.exp(AR + BR / T + CR * np.log(T))
       BO = (SMU + DV * (PTR - PR)) / (R * TR) - (DV * PT) / RT + (HO / R) * (1. / T - 1. / TR) - self.lnA

       if T >= TICE:
           BO = BO + (20.6166 * ALOG(T / TR) - .0211634 * (T - TR) + 2616.398*(1.0/T-1.0/TR))/R

       N = (int(abs(T - TR)) / 2) * 4 + 30
       H = (T - TR) / float(N)

       SUM = -self.F2(T, AR, BR, CR) + self.F2(TR, AR, BR, CR)

       TS = TR

       upper = 1*N
       lower = 1
       length = (upper - lower) / 2
       lista = [lower + x * 2 for x in range(length+1)]

       for L in lista:
           TS = TS + H
           SUM = 4. * self.F2(TS, AR, BR, CR) + SUM
           TS = TS + H
           SUM = 2. * self.F2(TS , AR, BR, CR) + SUM
       BO = BO + (H / 3.) * SUM * DV / R

       self.BO = BO
       self.DV = DV

    def F2(self, TS, AR, BR, CR):
        P=EXP(AR+BR/TS+CR*ALOG(TS))
        F2 = P * (CR / TS - BR / (TS * TS)) / TS
        return F2



























