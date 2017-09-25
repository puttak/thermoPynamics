#coding: utf-8
import numpy as np
import os
import sqlite3 as sql
from databases.GetDataBaseDir import GetDataBaseDir
from ThermoPkgs.SRK.getsqldata import ReadSqlData

class Perry:
    def __init__(self, fluido, perrydata):
        self.ID = fluido.ID
        self.NC = len(self.ID)

        self.C1 = perrydata.C1
        self.C2 = perrydata.C2
        self.C3 = perrydata.C3
        self.C4 = perrydata.C4
        self.C5 = perrydata.C5

        a=ReadSqlData(self.ID)
        [self.Tc,pc,w]=a.GetCritical()

    def computePsat(self,T):
        Psat=[]
        for i in range(self.NC):
            try:
                assert T<=self.Tc[i]
            except:
                raise ValueError('Temperatura acima da T crítica do componente %s' % (self.ID[i]))
            lnPsat = self.C1[i]+ self.C2[i]/T + self.C3[i]*np.log(T) +self.C4[i]*T**self.C5[i]
            psat = np.exp(lnPsat)
            PascalToBar = psat/10**5
            Psat.append(PascalToBar)
        return Psat

def Psat(T, id):
    assert type(id) == int
    a = ReadSqlData([id])
    [Tc, pc, w] = a.GetCritical()
    try:
        assert T<=Tc[0]
    except:
        raise ValueError('Temperatura maior que Tc')
    originalDir = os.getcwd()

    fileName = 'pureComponentData.db'
    DBfileDir = GetDataBaseDir()
    os.chdir(DBfileDir)
    conector = sql.connect(fileName)
    os.chdir(originalDir)

    cursor = conector.cursor()

    cursor.execute('SELECT C1, C2, C3, C4, C5 FROM [VaporPressurePerry2-8] WHERE ID=?', [id])
    row = cursor.fetchall()

    C1 = float(row[0][0])
    C2 = float(row[0][1])
    C3 = float(row[0][2])
    C4 = float(row[0][3])
    C5 = float(row[0][4])

    psat = C1 + C2/T + C3*np.log(T) + C4*T**C5
    psat=np.exp(psat)
    psat=psat/10**5
    return psat
