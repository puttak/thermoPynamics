#coding:utf-8
import sqlite3 as sql
import os
from databases.GetDataBaseDir import GetDataBaseDir
import numpy as np

class ReadPerrVaporPressureData:
    def __init__(self, ID):
        self.ID = ID

        originalDir = os.getcwd()

        fileName = 'pureComponentData.db'
        DBfileDir = GetDataBaseDir()
        os.chdir(DBfileDir)
        conector = sql.connect(fileName)
        os.chdir(originalDir)

        self.__cursor = conector.cursor()

    def GetCoef(self):

        C1=[]
        C2=[]
        C3=[]
        C4=[]
        C5=[]

        for id in self.ID:
            self.__cursor.execute('SELECT C1, C2, C3, C4, C5 FROM [VaporPressurePerry2-8] WHERE ID=?', [id])
            row = self.__cursor.fetchall()
            C1.append(float(row[0][0]))
            C2.append(float(row[0][1]))
            C3.append(float(row[0][2]))
            C4.append(float(row[0][3]))
            C5.append(float(row[0][4]))

        C1 = np.array(C1)
        C2 = np.array(C2)
        C3 = np.array(C3)
        C4 = np.array(C4)
        C5 = np.array(C5)

        return [C1, C2, C3, C4, C5]