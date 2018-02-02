#coding: utf-8

import scipy.optimize as opt
from calculations.hydrates.PCAL import PCAL
from calculations.JTcooling.pyJT import JT
import numpy as np

###Compute maximum pressure drop to avoid hydrate formation

class maxDeltaP:
    def __init__(self,T1,P1,ID,y, isThereInib, InibID, InibMassFraction,flagEOS):
        self.T1=T1
        self.P1=P1
        self.ID=ID
        self.y=y
        self.flagEOS = flagEOS
        self.isThereInib = isThereInib
        self.InibID = InibID
        self.InibMassFraction = InibMassFraction

        self.jt = JT(self.T1, self.P1, ID=self.ID, y=self.y,
                     fase='vapor', flagEOS=self.flagEOS)
        self.hyd = PCAL(ID=self.ID, y=self.y, isThereInib=0, InibID=None, InibMassFraction=None, flagEOS=self.flagEOS)

        p0 = self.hyd.computePD(T1, 1.0)

        if p0 < P1:
            self.AlreadyStable = True
        else:
            self.AlreadyStable = False



    def f_hyd(self,X):

        Tx=float(X[0])
        Px=float(X[1])

        return -Px + self.hyd.computePD(Tx,1.0)

    def f_jt(self,X):
        Tx=X[0]
        Px=X[1]

        return  -Tx + self.jt.computeT2(Px)

    def sistema(self,X):
        f=[]
        f.append(self.f_hyd(X))
        f.append(self.f_jt(X))
        return f

    def solve(self,Xguess):

        assert not self.AlreadyStable

        xraiz=opt.fsolve(self.sistema,Xguess)

        return xraiz


class PlotHydLimit:
    def __init__(self, isotherms, P1initial, P1final, ID,y,isThereInib, InibID, InibMassFraction, flagEOS, NumberOfPoints=20):
        #Isotherms: ...List... contains the temperature which will be used in calculations.

        assert type(isotherms) in [list, np.ndarray]
        assert type(ID) in [list, np.ndarray]
        assert type(y) in [list, np.ndarray]

        self.isotherms = isotherms

        self.ID = ID
        self.y = y
        self.isThereInib = isThereInib
        self.InibID = InibID
        self.InibMassFraction = InibMassFraction

        self.flagEOS = flagEOS

        assert type(P1final) in [int, float]
        self.P1final = P1final
        assert type(P1initial) in [int, float]
        self.P1initial = P1initial
        self.NumberOfIsotherms = len(isotherms)

        self.P1vector = np.linspace(P1initial, P1final, NumberOfPoints)


    def computeValues(self):

        all_P2x=[]
        self.all_dontPlot=[]
        for T in self.isotherms:
            p2=[]
            dontPlot = []
            for P in self.P1vector:
                model = maxDeltaP(T, P, self.ID, self.y,self.isThereInib, self.InibID, self.InibMassFraction, self.flagEOS)
                if model.AlreadyStable:
                    dontPlot.append(True)
                    p2.append(0)

                else:
                    try:
                        p2.append(model.solve([T, P])[1])
                        dontPlot.append(False)
                    except:
                        dontPlot.append(True)
                        p2.append(0)

            all_P2x.append(p2)
            self.all_dontPlot.append(dontPlot)

        return all_P2x

    def calculateHydLim(self):
        P2 = self.computeValues()
        #Create vector that will be plotted
        allP2plot=[]
        allP1plot = []
        for i in range(len(self.isotherms)):
            pOne=[]
            p2 = []
            for j in range(len(self.all_dontPlot[i])):
                if not self.all_dontPlot[i][j]:
                    pOne.append(self.P1vector[j])
                    p2.append(P2[i][j])

            allP1plot.append(pOne)
            allP2plot.append(p2)
        return allP1plot, allP2plot



    def plotHydLim(self):
        [allP1plot,allP2plot]=self.calculateHydLim()
        import matplotlib.pyplot as plt

        for i in range(self.NumberOfIsotherms):
            plt.plot(allP2plot[i], allP1plot[i], 'bs')
        plt.show()

    def writeHydLim(self):
        [allP1plot,allP2plot]=self.calculateHydLim()

        import datetime
        now = datetime.datetime.now()
        tempo = [now.year, now.month, now.day, now.hour, now.minute, now.second]
        stringa = ''
        for s in tempo:
            stringa = stringa + str(s) + '_'
        stringa = stringa[:-1]
        from calculations.outputfiles.GetoutputPath import thisPath
        nome = thisPath() +'/'+ stringa + 'output.csv'
        arquivo = open(nome,'w')

        for i in range(self.NumberOfIsotherms):
            for j in range(len(allP1plot[i])):
                stringDeDados = str(allP1plot[i][j])+';'+str(allP2plot[i][j])+'\n'
                arquivo.write(stringDeDados)
            for k in range(5):
                arquivo.write('\n')

        arquivo.close()
















