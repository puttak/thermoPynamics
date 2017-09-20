#encoding: utf-8
import numpy as np
from ThermoPkgs.PR_LCVM_UNIFAC.PR_LCVM_UNIFAC import PR_LCVM_UNIFAC
from ThermoPkgs.PR_LCVM_UNIFAC.interfacePRLCVMUNIFAC import FluidPRLCVMUNIFAC, FluidDataPRLCVMUNIFAC
from ThermoPkgs.UNIFAC.interface import FluiDataUNIFAC
from Solvers.BoilPoint import newton_bolP
import inspect

#TODO: Bolar uma maneira de organizar como os 'calculations' definem os modelos.


#TODO: COPIAR PARA EVERNOTE.
#TODO: Colocar um indicador (FLAG) de que modelo usar não é um bom approach. Isso requer que o código do bolP seja modificado a cada vez que um moddelo novo seja adicionado.
#Um approach melhor é alimentar o BOLP com o próprio modelo.
#Talvez esteja me perguntando: 'como usar o BOLP na biblioteca?" e esteja confundindo com "qual o uso do BOLP pra o usuário do programa?"
#A resposta pra segunda pergunta é a interface.
#A respota pra primeira pergunta pode ser inspirada pelos simuladores.
#Os calculos são alimentados com um modelo. Um tipo de modelo (que tenha certos métodos, ou API, sei la.)
#Então os cálculos são alimentados só com o modelo, ou talvez com um tipo de modelo. Então os modelos teriam que ser classificados.
#Cada tipo de modelo tem uma série de métodos que são padronizados. Cada modelo pode ter métodos específicos, mas todos terão os métodos padrão.


#TODO: GROSSO DO BOLP.


class BolP():
    def __init__(self, fug_liq,fug_vap):
        #TODO: O Número de componentes é a dimensão da saida do fug_liq e fug_vap tem q ser iguais

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

        self.tol = 1E-7
        self.maxIter = 10**3




    def compute_Pbol_ybol(self, T, x, GUESS_Pbol = 1.0,GUESS_y=None):
        #TODO: TESTAR tipo T e x, GUESS_PBOL, GUESS_Y
        if type(x)!=np.ndarray:
            x=np.array(x)
        self.NC = len(x)

        if GUESS_y == None:
            volatil = x[0]+0.3
            GUESS_y = []
            GUESS_y.append(volatil)
            for i in range(self.NC-1):
                GUESS_y.append(x[i+1])
            GUESS_y = np.array(GUESS_y)
            GUESS_y = GUESS_y/ sum(GUESS_y)

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

            deltaIter_y = 1.0 + tol
            count_y = 0

            while deltaIter_y >= tol and count_y <= self.maxIter:
                # LOOP y

                ki = fiL(OLDP) / fiV(OLDP, OLDyi)
                yi = []
                for i in range(self.NC):
                    yi.append(ki[i] * x[i])

                sumKtimesXi = sum(yi)
                yi = np.array(yi)
                yi = yi / sumKtimesXi

                deltaIter_y = abs(sum(yi) - sum(OLDyi))
                OLDyi = yi
                count_y += 1

            assert count_y <= self.maxIter
            print OLDP, yi
            deltaIter_P = abs(sumKtimesXi-1.0)

            dGdP = (self.__GdeP(OLDP+1, yi)-self.__GdeP(OLDP, yi) )/1

            #TODO: O PROBLEMA é o cálculo da nova pressão. TA SENSÍVEL AO CHUTE INICIAL.

            a = -self.__GdeP(OLDP, yi)/dGdP
            OLDP += a


            count_P += 1

        assert count_P<=self.maxIter

        return OLDP, yi



            # def BolP(self, T, x):
    #     fluido_L = Fluid(self.ID, x)
    #     fdata_L = FluidData(fluido_L)
    #     unidata_L = FluiDataUNIFAC(fluido_L)
    #     self.liquido=PR_LCVM_UNIFAC(fluido_L, fdata_L, unidata_L)
    #     self.T=T
    #     self.x_L=x
    #
    #     X0=[0.3]
    #     for i in range(self.NC-1):
    #         X0.append(x[i])
    #
    #     X0=np.array(X0)
    #     bd=((0.0,None), (0.0, 1.0))
    #     Xraiz = opt.minimize(self.__bol, X0, bounds=bd).x
    #
    #     return Xraiz
    #
    #
    #
    # def __bol(self,X):
    #     P = abs(X[0])
    #     y=[]
    #     for i in range(self.NC-1):
    #         y.append(abs(X[i+1]))
    #     y.append(1-sum(y))
    #
    #     fluido_V = Fluid( self.ID, y )
    #     fdata_V = FluidData(fluido_V)
    #     unidata_V = FluiDataUNIFAC(fluido_V)
    #     vapor = PR_LCVM_UNIFAC(fluido_V, fdata_V, unidata_V)
    #
    #     fi_L = self.liquido.computeFUG(self.T, P, 'liquid')
    #     fi_V = vapor.computeFUG(self.T, P, 'vapor')
    #     F = []
    #
    #     for i in range(self.NC):
    #         F.append((self.x_L[i]*fi_L[i]-y[i]*fi_V[i])**2)
    #
    #     return sum(F)

    def __fugCoefLiquid(self, P):
        return self.fug_liq(self.T, P, self.x, 'liquid')
    def __fugCoefVapor(self, P, y):
        return self.fug_vap(self.T, P, y, 'vapor')

    def __GdeP(self, P, y):

        ki=self.__fugCoefLiquid(P)/self.__fugCoefVapor(P, y)
        soma=0.0
        for i in range(self.NC):
            soma+=ki[i]*self.x[i]

        return soma-1.0