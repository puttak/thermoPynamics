#coding: utf-8
import sqlite3 as sql
import os
from databases.GetDataBaseDir import GetDataBaseDir

class ReadDataUNIFAC:
    def __init__(self,ID):
        self.ID = ID

        originalDir = os.getcwd()

        fileName = 'pureComponentData.db'
        DBfileDir = GetDataBaseDir()
        os.chdir(DBfileDir)
        conector = sql.connect(fileName)
        os.chdir(originalDir)

        self.__cursor = conector.cursor()

    def GetComponentGroupSpecification(self):
        #cria matriz v_k e matriz G ([mainGroupNumber,[subgrupos relacionados], ..., [mainGroupNumber,[subgrupos relacionados] ]


        for id in self.ID:
            self.__cursor.execute('SELECT groupID, subGroupID, NumberOfOccurrences '
                                  'FROM [UNIFAC_component_group_specifications] WHERE componentID=%d' % (id))
            row=self.__cursor.fetchall()
            #pegar todos os sub grupos de todos os componentes em vetores de dim variáveis.
            #pegar o número total de sg diferentes. Armazenar vk em um vetor com dim NG e organizar como na folha.

            #TODO: OLHAR COMO E A MATRIZ COM OS GRUPOS EM THERMO E CRIAR UMA MATRIZ SEMELHANTE AQUI.
            #TODO: ARMAZENAR EM UMA MATRIZ O NÚMERO DE OCORRÊNCIA E NÚMERO DO SUBGRUPO.



