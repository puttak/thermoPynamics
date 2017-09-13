#coding: utf-8
import numpy as np

##ACREDITO QUE JA TODOS OS DADOS NECESSÁRIOS JA ESTÃO SENDO PÊGOS NO BANCO DE DADOS. AGORA JÁ É POSSÍVEL INICIAR OS CÁLCULOS.

class UNIFAC:
    def __init__(self, fluid, unifacdata):

        self.R = 83.144621  # bar.cm3/(mol.K)

        try:
            self.ID = fluid.ID
            assert type(self.ID) == list
        except:
            raise ValueError('ID não definido corretamente na instancia fluid')


        #TODO: Add conferir entradas.

        self.NC = len(self.ID)

        self.NG = unifacdata.NG
        self.v = unifacdata.v
        self.k = unifacdata.k

        self.R_k = unifacdata.R_k
        self.Q_k = unifacdata.Q_k
        self.a_m_n = unifacdata.a_m_n
        self.matrizG = unifacdata.matrizG
        self.ComponentsSubGroups=unifacdata.ComponentsSubGroups
        self.NG_i = unifacdata.NG_i



    def computeGama(self, T, x):


        assert sum(x)==1
        assert len(x) == self.NC
        x = np.array(x)

        PSI_m_n = np.exp(-self.a_m_n/T)

        self.PSI_m_n = PSI_m_n

        viXi=np.dot(x,self.v)
        Xm = viXi/sum(viXi)


        r_component=[]
        q_component=[]
        for i in range(self.NC):
            r_component.append(np.dot(self.v[i], self.R_k))
            q_component.append(np.dot(self.v[i], self.Q_k))

        produto_q_x = q_component*x
        produto_r_x = r_component*x

        Q_area_component_fraction = produto_q_x/sum(produto_q_x)
        FI_component_seg_fraction = produto_r_x/sum(produto_r_x)

        produto_m = self.Q_k * Xm
        TETAm = produto_m/sum(produto_m)

        #GROUP ACTIVITY COEFFICIENT ln GAMMA_k

        ln_GAMMA_k = self.__groupGamma( self.NG, self.PSI_m_n, Xm, self.Q_k) #DA MISTURA

        #COMPONENT GROUP ACTIVITY COEFFICIENT ln_GAMMA_k_i

        #TODO: Gerar os inputs de __groupGamma pra cada componente puro. Posso aporveitar as variáveis que acabei criando no unifacdata. Também importei o método GetMainGroup, se não precisar, só tirar.

        self.NsG_i= [ ]
        for i in self.ComponentsSubGroups:
            self.NsG_i.append( len(i) )

        PSI_m_n_i=[]

        for i in range(self.NC):
            PSI_m_n_i.append(np.zeros([self.NsG_i[i],self.NsG_i[i]]))


        for i in range(self.NC):
            for k1 in range(self.NsG_i[i]):
                for k2 in range(self.NsG_i[i]):
                    PSI_m_n_i[i][k1][k2] = \
                        PSI_m_n[self.k.index(self.ComponentsSubGroups[i][k1])][self.k.index(self.ComponentsSubGroups[i][k2])]

        X_i_k=[]
        Q_k_i=[]
        for i in range(self.NC):
            X = []
            Q=[]
            for c_sg in self.ComponentsSubGroups[i]:
                X.append(float(self.v[i][self.k.index(c_sg)]) / sum(self.v[i]) )
                Q.append(self.Q_k[self.k.index(c_sg)])
            X_i_k.append(X)
            Q_k_i.append(Q)

        ln_GAMMA_i_k=[]
        for i in range(self.NC):
            ln_GAMMA_i_k.append(self.__groupGamma(self.NsG_i[i], PSI_m_n_i[i], X_i_k[i], Q_k_i[i]))
        print ln_GAMMA_i_k #TODO: CONFERIR SE OS VALORES ESTÃO CERTOS COM O LIVRO. DAI PASSAR PRA CALCULAR O GAMMA RESIDUAL
        ln_residual_gamma_i=[]
        matrix_component_group_gamma_k=self.__component_group_gamma_k()

        for i in range(self.NC):
            soma=0.0
            for kk in range(self.NG):
                # if self.v[i][kk]==0:
                #     continue
                soma+=self.v[i][kk]*(ln_GAMMA_k[kk]- matrix_component_group_gamma_k[i][kk])
                # print ln_GAMMA_k[kk], '=ln_GAMMA_k', matrix_component_group_gamma_k[i][kk], '=matrix_component_group_gamma_k'
            ln_residual_gamma_i.append(soma)

    def __groupGamma(self, NG, PSI_m_n, Xm, Q_k):
        Xm=np.array(Xm)
        produto_m = Q_k * Xm
        TETAm = produto_m/sum(produto_m)

        SOMA_TETAm_vezes_PSImk_k = []
        ln_SOMA_TETAm_vezes_PSImk_k = []
        sum_ratio_teta_times_PSI_k = []
        ln_GAMMA_k = []
        for kk in range(NG):

            soma_k = 0.0
            for m in range(NG):
                soma_k += TETAm[m] * PSI_m_n[m][kk]

            SOMA_TETAm_vezes_PSImk_k.append(soma_k)
            ln_SOMA_TETAm_vezes_PSImk_k.append(np.log(soma_k))

            sum_ratio_k = 0.0
            for m in range(NG):
                soma_k_2 = 0.0
                for n in range(NG):
                    soma_k_2 += TETAm[n] * PSI_m_n[n][m]
                sum_ratio_k += TETAm[m] * PSI_m_n[kk][m] / soma_k_2

            sum_ratio_teta_times_PSI_k.append(sum_ratio_k)



        for kk in range(NG):
            ln_GAMMA_k.append(Q_k[kk] * (1 - ln_SOMA_TETAm_vezes_PSImk_k[kk] - sum_ratio_teta_times_PSI_k[kk]))

        return ln_GAMMA_k


    def __component_group_gamma_k(self):


        #TODO: DELETAR ESSE MÉTODO. TALVEZ APROVEITE ALGO DELE.
        matriz_total=[]
        for i in range(self.NC):
            matriz_grupo=[]
            if self.NG_i[i]==1:
                matriz_grupo=[0.0 for i in range(self.NG)]
                matriz_total.append(matriz_grupo)
                continue

            X_i_k=[]
            for kk in range(self.NG):
                matriz_grupo.append(1.0)
                X_i_k.append(float(self.v[i][kk]) / sum(self.v[i]) )

            TETA_m_i = []
            X_i_k=np.array(X_i_k)

            for k_2 in range(self.NG):
                if self.v[i][k_2] == 0:
                    TETA_m_i.append(0.0)
                    continue
                TETA_m_i.append(self.Q_k[k_2]*X_i_k[k_2]/sum(self.Q_k*X_i_k))

            SOMA_TETAm_vezes_PSImk_k = []
            ln_SOMA_TETAm_vezes_PSImk_k = []
            sum_ratio_teta_times_PSI_k = []


            for k_2 in range(self.NG):
                if self.v[i][k_2] == 0:
                    ln_SOMA_TETAm_vezes_PSImk_k.append(0.0)
                    sum_ratio_teta_times_PSI_k.append(0.0)
                    continue

                soma_k = 0.0
                for m in range(self.NG):
                    if self.v[i][m] == 0:
                        continue
                    soma_k += TETA_m_i[m] * self.PSI_m_n[m][k_2]

                SOMA_TETAm_vezes_PSImk_k.append(soma_k)
                ln_SOMA_TETAm_vezes_PSImk_k.append(np.log(soma_k))

                sum_ratio_k = 0.0
                for m in range(self.NG):
                    if self.v[i][m] == 0:
                        continue
                    # print TETA_m_i[m], self.PSI_m_n[m][k_2], soma_k
                    sum_ratio_k += TETA_m_i[m] * self.PSI_m_n[m][k_2] / soma_k

                sum_ratio_teta_times_PSI_k.append(sum_ratio_k)

            # print ln_SOMA_TETAm_vezes_PSImk_k, sum_ratio_teta_times_PSI_k

            for k_2 in range(self.NG):
                if self.v[i][k_2] == 0:
                    matriz_grupo.append(0.0)
                    continue
                matriz_grupo.append(self.Q_k[k_2]*(1-ln_SOMA_TETAm_vezes_PSImk_k[k_2]-sum_ratio_teta_times_PSI_k[k_2])  )

            matriz_total.append(matriz_grupo)

        return matriz_total

    def __GetMainGroup(self,sg_id):
        for listinha in self.matrizG:
            if sg_id in listinha[1]:
                return listinha[0]
        raise RuntimeError('Grupo principal do subgrupo %d não encontrado' % (sg_id))
