#coding: utf-8

import os
import numpy as np
import sqlite3 as sqlite

class GetDataPCAL():
    def __init__(self, InputOBJ):

        self.InputOBJ = InputOBJ
        originalDir = os.getcwd()

        fileName='hydratecomponentdata.db'
        thisScript = os.path.abspath( __file__  )
        thisDirectory = os.path.dirname(thisScript)

        os.chdir(thisDirectory)
        conector = sqlite.connect(fileName)
        os.chdir(originalDir)

        self.__cursor = conector.cursor()


        self.NumberOfHydrateFormers()
        # PreProcessData.__init__(self) #A classe pre process é inicializada aqui de modo que tem-se os dados em mãos no momento da
        #inicialização.


    def NumberOfHydrateFormers(self):
        NFH1 = []
        NFH2 = []
        KTYPE=[]
        EP=[]
        SIG=[]
        ACORE=[]
        TMD=[]
        ASOL=[]
        BSOL=[]
        CSOL=[]
        DSOL=[]

        for id in self.InputOBJ.ID:

            self.__cursor.execute('SELECT NFH1,NFH2,KTYPE,EP,SIG,ACORE,TMD,ASOL,BSOL,CSOL,DSOL FROM hyd WHERE ID=?', [id])
            row = self.__cursor.fetchall()
            NFH1.append(row[0][0])
            NFH2.append(row[0][1])
            KTYPE.append(row[0][2])
            EP.append(row[0][3])
            SIG.append(row[0][4])
            ACORE.append(row[0][5])
            TMD.append(row[0][6])
            ASOL.append(row[0][7])
            BSOL.append(row[0][8])
            CSOL.append(row[0][9])
            DSOL.append(row[0][10])

        self.NFH1 = sum(NFH1)
        self.NFH2 = sum(NFH2)
        self.NFH  = self.NFH1 + self.NFH2

        self.KTYPE=KTYPE
        self.EP=np.array(EP)
        self.SIG=np.array(SIG)
        self.ACORE=np.array(ACORE)
        self.TMD=np.array(TMD)
        self.ASOL=np.array(ASOL)
        self.BSOL=np.array(BSOL)
        self.CSOL=np.array(CSOL)
        self.DSOL=np.array(DSOL)










