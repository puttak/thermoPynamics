#coding: utf-8
import numpy as np
import sqlite3 as sqlite
import openpyxl, os

class ReadData:
    def __init__(self, ID):

        self.ID = ID

        originalDirectory = os.getcwd()
        CPfile='idealGasCpData.db'
        thisScript = os.path.abspath( __file__  )
        thisDirectory = os.path.dirname(thisScript)
        os.chdir(thisDirectory)

        self.conn = sqlite.connect(CPfile)

        os.chdir(originalDirectory)

        self.__cursor = self.conn.cursor()

        self.CoefficientsCP = self.get_cp_data()

    def get_cp_data(self):
        # Equação na forma: Cp/R = a0 + T*a1*10^-3 + T^2*a2*10^-5 + T^3*a3*10^-8 + T^4*a4*10^-11
        # Array com os coeficientes:   [[a01,...,a0NC],
        #                               [a11,...,a1NC],
        #                               [a21,...,a2NC],
        #                               [a31,...,a3NC],
        #                               [a41,...,a4NC]]
        # Dados são retirados do The properties of gases and liquids 5ed

        ID = self.ID


        # TempRangeLower = [50]
        # TempRangeUpper = [1000]
        # a0 = 3.259
        # a1 = 1.356
        # a2 = 1.502
        # a3 = 2.374
        # a4 = 1.056
        # CPcoefficients = [[a0], [a1], [a2], [a3], [a4]]
        # CPcoefficients = np.array(CPcoefficients)
        # return CPcoefficients
        a0 = []
        a1 = []
        a2 = []
        a3 = []
        a4 = []

        for id in self.ID:
            self.__cursor.execute('SELECT a0, a1, a2, a3, a4 FROM idealCp WHERE ID=%d' % (id))
            row=self.__cursor.fetchall()

            a0.append(float(row[0][0]))
            a1.append(float(row[0][1]))
            a2.append(float(row[0][2]))
            a3.append(float(row[0][3]))
            a4.append(float(row[0][4]))

        a0 = np.array(a0)
        a1 = np.array(a1)
        a2 = np.array(a2)
        a3 = np.array(a3)
        a4 = np.array(a4)

        return [a0, a1, a2, a3, a4]


