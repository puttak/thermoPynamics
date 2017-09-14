#coding: utf-8
import sqlite3 as sql
import numpy as np
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
        self.conector = sql.connect(fileName)
        self.conectorUNIFAC = sql.connect(fileUNIFAC)
        os.chdir(originalDir)

        self.__cursor = self.conector.cursor()
        self.cursorUNIFAC = self.conectorUNIFAC.cursor()

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

        for i in range(self.NC):
            v_k[i]=[xx for yy,xx in sorted(zip(k[i],v_k[i]))]
            k[i].sort()

        componentK = list(k)
        noduplicate_k=[]
        for ki in k:
            noduplicate_k =noduplicate_k+ki

        # for l in range( len(v_k) ):
        #     v_k[l]= tuple(v_k[l])
        # v_k=tuple(v_k)
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
        self.subGroupsOfEachComponent=componentK

        self.NG_i=[]
        for i in range(self.NC):
            lista=[]
            for k in componentK[i]:
                lista.append(self.GetMainGroup(k))

            lista=list(set(tuple(lista)))
            self.NG_i.append(len(lista))

        return [NG, v, self.k, matrizG,componentK, self.NG_i ]

    def Get_r_and_q(self):
        R_k=[]
        Q_k=[]
        for sg_id in self.k:
            self.cursorUNIFAC.execute('SELECT R, Q FROM subgroupParameters WHERE subgroupID=%d'%(sg_id))
            row=self.cursorUNIFAC.fetchall()
            R_k.append(row[0][0])
            Q_k.append(row[0][1])

        return [R_k,Q_k]

    def GetMainGroup(self,sg_id):
        for listinha in self.matrizG:
            if sg_id in listinha[1]:
                return listinha[0]
        raise RuntimeError('Grupo principal do subgrupo %d não encontrado' % (sg_id))


    def GetGroup_interaction_parameter(self):
        a_m_n=np.zeros([self.NG, self.NG])
        self.cursorUNIFAC.execute('SELECT A_i_j, A_j_i FROM interactionParametersUNIFAC WHERE groupID_i=%d and groupID_j=%d' % (1, 42))
        row=self.cursorUNIFAC.fetchall()

        #vou só percorrer a parte de cima da matriz NGxNG. E definir Amxn e Anxm. se eu não achar no DB ixj, tentar jxi. se não tiver ambor, é pq n tem no banco de dados.
        #
        for sg_i in self.k:
            sg_j_list = [sg_j for sg_j in self.k if sg_j>sg_i]
            main_i = self.GetMainGroup(sg_i)
            for sg_j in sg_j_list:
                main_j = self.GetMainGroup(sg_j)
                if main_i==main_j:
                    a_m_n[self.k.index(sg_i)][self.k.index(sg_j)]=0.0
                    continue
                try:

                    self.cursorUNIFAC.execute('SELECT A_i_j, A_j_i FROM interactionParametersUNIFAC WHERE '
                                              'groupID_i=%d and groupID_j=%d' % (main_i, main_j))
                    row = self.cursorUNIFAC.fetchall()
                    a_m_n[self.k.index(sg_i)][self.k.index(sg_j)] = row[0][0]
                    a_m_n[self.k.index(sg_j)][self.k.index(sg_i)] = row[0][1]
                except:
                    try:
                        self.cursorUNIFAC.execute('SELECT A_i_j, A_j_i FROM interactionParametersUNIFAC WHERE '
                                                  'groupID_i=%d and groupID_j=%d' % (main_j, main_i))
                        row = self.cursorUNIFAC.fetchall()
                        a_m_n[self.k.index(sg_i)][self.k.index(sg_j)] = row[0][1]
                        a_m_n[self.k.index(sg_j)][self.k.index(sg_i)] = row[0][0]
                    except:

                        raise ValueError('Parâmetro de interação dos grupos %d e %d não encontrados no banco de dados UNIFAC'
                                         %(main_i, main_j))


        return a_m_n






