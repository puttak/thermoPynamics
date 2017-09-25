#encoding: utf-8
import numpy as np
from ThermoPkgs.PR_LCVM_UNIFAC.PR_LCVM_UNIFAC import PR_LCVM_UNIFAC
from ThermoPkgs.PR_LCVM_UNIFAC.interfacePRLCVMUNIFAC import FluidPRLCVMUNIFAC, FluidDataPRLCVMUNIFAC
from ThermoPkgs.UNIFAC.interface import FluiDataUNIFAC
from ThermoPkgs.VaporPressure.interfacePerry import FluidDataPerry, FluidPerryVaporPressure
from ThermoPkgs.VaporPressure.VaporPressure import Psat
from ThermoPkgs.SRK.getsqldata import ReadSqlData
import matplotlib.pyplot as plt
import csv
import inspect

#Bolar uma maneira de organizar como os 'calculations' definem os modelos.



#Colocar um indicador (FLAG) de que modelo usar não é um bom approach. Isso requer que o código do bolP seja modificado a cada vez que um moddelo novo seja adicionado.
#Um approach melhor é alimentar o BOLP com o próprio modelo.
#Talvez esteja me perguntando: 'como usar o BOLP na biblioteca?" e esteja confundindo com "qual o uso do BOLP pra o usuário do programa?"
#A resposta pra segunda pergunta é a interface.
#A respota pra primeira pergunta pode ser inspirada pelos simuladores.
#Os calculos são alimentados com um modelo. Um tipo de modelo (que tenha certos métodos, ou API, sei la.)
#Então os cálculos são alimentados só com o modelo, ou talvez com um tipo de modelo. Então os modelos teriam que ser classificados.
#Cada tipo de modelo tem uma série de métodos que são padronizados. Cada modelo pode ter métodos específicos, mas todos terão os métodos padrão.


class BolP():
    def __init__(self, fug_liq,fug_vap, ID):

        try:
            assert inspect.ismethod(fug_liq) or inspect.isfunction(fug_liq)
        except:
            raise RuntimeError('Função pra cálculo da fugacidade do líquido não definida corretamente')

        try:
            assert inspect.ismethod(fug_vap) or inspect.isfunction(fug_vap)
        except:
            raise RuntimeError('Função pra cálculo da fugacidade do vapor não definida corretamente')


        self.fug_liq=fug_liq
        self.fug_vap=fug_vap

        self.ID = ID

        self.tol = 1E-7
        self.maxIter = 10**2


    def compute_Pbol_ybol(self, T, x, GUESS_Pbol = None,GUESS_y=None):

        if type(x)!=np.ndarray:
            x=np.array(x)
        self.NC = len(x)

        if GUESS_y == None or GUESS_Pbol ==None:
            [gp, gy] = self.__PyGuess(T,x)
            if GUESS_Pbol == None:
                GUESS_Pbol = gp
            if GUESS_y == None:
                GUESS_y = gy
            del gp, gy
        # print GUESS_Pbol, GUESS_y
        self.x = x
        self.T = T


        fiL =  self.__fugCoefLiquid
        fiV =  self.__fugCoefVapor

        tol=self.tol

        ki = fiL(GUESS_Pbol)/fiV(GUESS_Pbol, GUESS_y)

        OLDyi=[]
        for i in range(self.NC):
            OLDyi.append(ki[i]*x[i])

        OLDyi=np.array(OLDyi)
        OLDyi = OLDyi/sum(OLDyi)
        OLDP = GUESS_Pbol

        #LOOP P
        deltaIter_P=1.0+tol
        count_P=0
        while deltaIter_P>=tol and count_P<=self.maxIter:
            print OLDP,OLDyi,ki,x

            deltaIter_y = 1.0 + tol
            count_y = 0

            while deltaIter_y >= tol and count_y <= self.maxIter:
                # LOOP y

                ki = fiL(OLDP) / fiV(OLDP, OLDyi)
                yi = []
                for i in range(self.NC):
                    ki_xi = ki[i] * x[i]
                    yi.append(ki_xi)

                sumKtimesXi = sum(yi)
                yi = np.array(yi)
                yi = yi / sumKtimesXi

                deltaIter_y = abs(sum(yi) - sum(OLDyi))
                OLDyi = yi
                count_y += 1

            assert count_y <= self.maxIter
            deltaIter_P = abs(sumKtimesXi-1.0)
            for i in range(self.NC):
                if abs(yi[i]- x[i])<=1E-3 and x[i]>1E-4 and x[i] <1.0-1E-4:
                    yi[i]+=0.01
            yi=yi/sum(yi)
            OLDyi=yi
            h=tol*1

            dGdP = self.__dGdP(OLDP, yi)
            a = -self._GdeP(OLDP, yi) / dGdP
            OLDP += a

            count_P += 1

        assert count_P<=self.maxIter
        self._CheckEQCriteria(OLDP, yi)
        return OLDP, yi



            # def BolP(self, T, x):


    def BolP_Pxy(self,T,numpoints=20,X1=None):

        if X1==None:
            X1 = np.linspace(0.0, 1.0, numpoints)

        X=[]
        for x1 in X1:
            X.append([x1,1-x1])
        P=[]
        Y=[]
        xvec=[]
        convergence=[]
        for x in X:
            # print P
            try:
                [p, y] = self.compute_Pbol_ybol(T, x)
                P.append(p)
                Y.append(y)
                xvec.append(x[0])
                convergence.append(True)
            except:
                # convergence.append(False)
                # print P[-1]
                # print self.compute_Pbol_ybol(T, x, 1.2 * P[-1])
                try:
                    [p, y] = self.compute_Pbol_ybol(T, x,1.2*P[-1])
                    P.append(p)
                    Y.append(y)
                    xvec.append(x[0])
                    convergence.append(True)
                except:
                    convergence.append(False)


        yvec=[]
        for i in range(len(xvec)):
            yvec.append(Y[i][0])

        return [P,xvec,yvec]

    def plot_BolP_Pxy(self,T,numpoints=20,X1=None):
        [P,xvec,yvec]=self.BolP_Pxy(T,numpoints,X1)

        Pco2=[7.895244,  19.0632855,     30.6467595,   40.02641475, 49.308798, 55.74192225, 58.27099425,  59.52742425]
        yco2=[0.9761,0.9907,0.992,0.9929,0.993,0.9931,0.993,0.993]
        plt.plot(xvec, P, yvec, P,xvec,Pco2,yco2,Pco2)
        plt.show()
    def plot_BolP_xy(self,T,numpoints=20,X1=None):
        [P, xvec, yvec]=self.BolP_Pxy(T, numpoints, X1)
        XxEQy = np.linspace(0.0, 1.0, 10)
        YxEQy = [x for x in XxEQy]
        plt.plot(xvec, yvec, XxEQy, YxEQy)
        plt.show()

    def write_BolP_xy(self,T,numpoints=20,X1=None):
        [P, xvec, yvec] = self.BolP_Pxy(T, numpoints, X1)
        outputcsv=open('Pxy.dat','w')
        for i in range(len(xvec)):
            s1 = str(xvec[i])+','
            s1=s1+str(yvec[i])+','
            s1=s1+str(P[i])+'\n'
            outputcsv.write(s1)
        outputcsv.close()


    def __fugCoefLiquid(self, P):
        return self.fug_liq(self.T, P, self.x, 'liquid')
    def __fugCoefVapor(self, P, y):
        return self.fug_vap(self.T, P, y, 'vapor')

    def _GdeP(self, P, y):

        try:
            NC = self.NC
        except:
            NC = len(self.x)

        ki=self.__fugCoefLiquid(P)/self.__fugCoefVapor(P, y)
        # print self.__fugCoefLiquid(P) , self.__fugCoefVapor(P, y)
        soma=0.0
        for i in range(NC):
            soma+=ki[i]*self.x[i]

        return soma-1.0

    def __dGdP(self, P, y):
        fiL_P=self.__fugCoefLiquid(P)
        fiV_P=self.__fugCoefVapor(P, y)

        fiL_P_tol=self.__fugCoefLiquid(P+self.tol)
        fiV_P_tol=self.__fugCoefVapor(P+self.tol, y)

        dln_L =( np.log(fiL_P_tol)-np.log(fiL_P) )/self.tol
        dln_V = ( np.log(fiV_P_tol)-np.log(fiV_P) )/self.tol
        ki=fiL_P/fiV_P
        soma=0.0
        for i in range(self.NC):
            soma+=self.x[i]*ki[i]*(dln_L[i]-dln_V[i])

        return soma

    def __PyGuess(self, T,x):
        Psat_i=[]
        flag=True
        for i in self.ID:
            try:
                Psat_i.append(Psat(T,i))
            except:
                flag=False
                a=ReadSqlData(self.ID)
                listaCrit = a.GetCritical()
                Tc=listaCrit[0]
                Psat_i.append(Psat(Tc[self.ID.index(i)], i))

        PbolGuess=0.0
        for i in range(len(x)):
            PbolGuess+=x[i]*Psat_i[i]

        yguess =[]
        if not flag:
            y0 = x[0]+0.1
            yguess.append(y0)
            for i in range(len(x)-1):
                yguess.append(x[i+1])
            somay=sum(yguess)
            for i in range(len(yguess)):
                yguess[i]=yguess[i]/somay
        else:
            for i in range(len(x)):
                yg = x[i] * Psat_i[i] / PbolGuess
                yguess.append(yg)

        return [PbolGuess, yguess]

    def _CheckEQCriteria(self, P, y):
        tol=1E-2
        delta_i=[]
        f_liq=self.__fugCoefLiquid(P)
        f_vap=self.__fugCoefVapor(P,y)
        for i in range(self.NC):
            l=self.x[i]*f_liq[i]
            v=y[i]*f_vap[i]
            delta_i.append(l-v)

        for i in range(self.NC):
            if delta_i[i]>tol:
                print 'Condição de equilíbrio não satisfeita para componente %s'% (self.ID[i])



