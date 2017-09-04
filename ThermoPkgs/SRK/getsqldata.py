# coding: utf-8
import numpy as np
import sqlite3 as sql
import os


class ReadSqlData:
    def __init__(self, ID):
        self.ID = ID
        # self.NC = len(self.ID)

        originalDir = os.getcwd()

        fileName = 'pureComponentData.db'
        thisScript = os.path.abspath(__file__)
        thisDirectory = os.path.dirname(thisScript)
        # fileName = os.path.join(thisDirectory,fileName)
        os.chdir(thisDirectory)
        conector = sql.connect(fileName)
        os.chdir(originalDir)

        self.__cursor = conector.cursor()

    def GetCritical(self):

        self.Tc = []
        self.Pc = []
        self.w = []

        for id in self.ID:
            self.__cursor.execute('SELECT Tc, Pc, [Acentric Factor] FROM criticalContants WHERE ID=?', [id])
            row = self.__cursor.fetchall()
            self.Tc.append(row[0][0])
            self.Pc.append(row[0][1])
            self.w.append(row[0][2])

        self.Tc = np.array(self.Tc)
        self.Pc = np.array(self.Pc)
        self.w = np.array(self.w)

        Critical = [self.Tc, self.Pc, self.w]

        return Critical

    def GetMM(self):
        self.MM = []

        for id in self.ID:
            self.__cursor.execute('SELECT [Mol Wt] FROM criticalContants WHERE ID=?', [id])
            row = self.__cursor.fetchall()
            self.MM.append(row[0][0])

        return self.MM

    def GetEOSkij(self, EOS):
        if EOS == 'SRK':
            tableString = 'EOS_SRK_PARAMETER'
        elif EOS == 'PR':
            tableString = 'EOS_PR_PARAMETER'
        else:
            raise ValueError('Nome EOS nao reconhecido')

        self.kij = []

        for id_i in self.ID:
            line = []
            for id_j in self.ID:
                self.__cursor.execute('SELECT kij FROM %s WHERE ID_i=%d AND ID_j=%d' % (tableString, id_i, id_j))
                row = self.__cursor.fetchall()
                if len(row) == 0:
                    line.append(0.0)
                else:
                    line.append(row[0][0])
            self.kij.append(line)

        self.kij = np.array(self.kij)
        return self.kij

    def GetName(self):
        self.Name = []
        for id in self.ID:
            self.__cursor.execute('SELECT Name FROM components WHERE ID=?', [id])
            row = self.__cursor.fetchall()
            self.Name.append(row[0][0])

        return self.Name




