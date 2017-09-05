#coding: utf-8
import sqlite3 as sql
import os
from databases.GetDataBaseDir import GetDataBaseDir

class ReadDataUNIFAC:
    def __init__(self,ID):
        self.ID = ID
        self.NC = len(self.ID)

        originalDir = os.getcwd()

        fileName = 'pureComponentData.db'
        fileUNIFAC='GroupParametersUNIFAC.db'
        DBfileDir = GetDataBaseDir()
        os.chdir(DBfileDir)
        conector = sql.connect(fileName)
        conectorUNIFAC = sql.connect(fileUNIFAC)
        os.chdir(originalDir)

        self.__cursor = conector.cursor()
        self.cursorUNIFAC = conectorUNIFAC.cursor()

    def GetComponentGroupSpecification(self):


        #cria matriz v (número de ocorrência de cada grupo em cada componente), vetor k e matriz G ([mainGroupNumber,[subgrupos relacionados], ..., [mainGroupNumber,[subgrupos relacionados] ]

        #matriz v -> [  [numéro de oc. grupo 1 comp1,...,numéro de oc. grupo NG comp1] ... [numéro de oc. grupo 1 compNC,...,numéro de oc. grupo NG compNC]
        #vetor k -> [IDsubgrupo1, IDsubgrupo2, ..., ...IDsubgrupoNG]


        #Essa parte dá um nó na mente... mas de boa. É só pra estruturar os dados pros cálculos. UNIFAC tem mt tipo de dado
        #Dados em relação aos componentes e em relação aos grupos. Uma embolação.

        k=[]
        v_k=[]
        main_g_id=[]


        for id in self.ID:
            self.__cursor.execute('SELECT groupID, subGroupID, NumberOfOccurrences '
                                  'FROM [UNIFAC_component_group_specifications] WHERE componentID=%d' % (id))

            row=self.__cursor.fetchall()

            try:
                assert len(row)!=0
            except:
                raise ValueError('componente %d não tem parâmetros do UNIFAC especificados no banco de dados' % (id))

            ki = []
            v_k_i=[]
            for dados_de_id in row:
                main_g_id.append(dados_de_id[0])
                ki.append(dados_de_id[1])
                v_k_i.append(dados_de_id[2])
            k.append(ki)
            v_k.append(v_k_i)


        noduplicate_k=[]
        for ki in k:
            noduplicate_k =noduplicate_k+ki

        noduplicate_k=tuple( noduplicate_k )
        noduplicate_k = list (set ( noduplicate_k))

        noduplicate_k.sort()

        NG = len(noduplicate_k)


        vki=[int(0) for i in range(NG)]
        almost_there_vki=[]
        for i in range(self.NC):
            almost_there_vki.append(list(vki))

        del(vki)

        for i_k,subGid in enumerate(noduplicate_k):
           for i_comp in range(self.NC):
               try:
                   almost_there_vki[i_comp][i_k] = int(v_k[i_comp][k[i_comp].index(subGid)])
               except:
                   almost_there_vki[i_comp][i_k]=int(0)

        v=list(almost_there_vki) #matriz que tem o número de ocorrências de cada grupo em cada componente

        k=list(noduplicate_k)    #subgrupos presentes ordenados em um vetor

        main_g_id = list(set(tuple(main_g_id)))
        main_g_id.sort()
        matrizG=[]
        for g_id in main_g_id:
            g=[]
            g2=[]
            self.cursorUNIFAC.execute('SELECT [subGroup I], [subGroup II], [subGroup III], [subGroup IV],'
                                      '[subGroup V], [subGroup VI], [subGroup VII], [subGroup VIII] FROM groupNAME WHERE'
                                      ' groupID=%d' % (g_id))
            row=self.cursorUNIFAC.fetchall()
            g.append(g_id)

            for sg_id in row[0]:
                g2.append(sg_id)
            g2=[n for n in g2 if type(n)==int]
            g.append(g2)
            matrizG.append(g)


        self.NG = NG
        self.v = v
        self.k = k
        self.matrizG = matrizG

        return [NG, v, k, matrizG ]

    def GetRandQ(self):
        self.R=None
        self.Q=None
        return [self.R, self.Q]






