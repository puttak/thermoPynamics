#coding: utf-8
import numpy as np

class modUNIFAC:
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
        self.b_m_n = unifacdata.b_m_n
        self.c_m_n = unifacdata.c_m_n
        self.T0 = unifacdata.T0
        self.matrizG = unifacdata.matrizG
        self.ComponentsSubGroups=unifacdata.ComponentsSubGroups
        self.NG_i = unifacdata.NG_i

    def computeGama(self, T, x):


        assert sum(x)-1.0<1.0e-5
        assert len(x) == self.NC

        for i in range(len(x)):
            if x[i] == 0:
                x[i] = 1E-12
                for ii in range(len(x)):
                    x[ii] = x[ii] / sum(x)

        x = np.array(x)
        a=np.zeros((self.NG, self.NG))
        for i in range(self.NG):
            for j in range(self.NG):
                a[i][j]=self.a_m_n[i][j]+self.b_m_n[i][j]*(T-self.T0[i][j])+self.c_m_n[i][j]*(T-self.T0[i][j])**2
        PSI_m_n = np.exp(-a/T)

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
        #COMBINATORIAL

        ln_g_c_i=[]
        li=[]
        for i in range(self.NC):
            li.append(5*(r_component[i]-q_component[i])-(r_component[i]-1))

        for i in range(self.NC):
            termo1=np.log(FI_component_seg_fraction[i]/x[i])
            termo2=5*q_component[i]*np.log(Q_area_component_fraction[i]/FI_component_seg_fraction[i])
            termo3=li[i]
            termo4=-FI_component_seg_fraction[i]/x[i]*sum(x*li)
            ln_g_c_i.append(termo1+termo2+termo3+termo4)

        #RESIDUAL
        #GROUP ACTIVITY COEFFICIENT ln GAMMA_k

        ln_GAMMA_k = self.__groupGamma( self.NG, self.PSI_m_n, Xm, self.Q_k) #DA MISTURA

        #COMPONENT GROUP ACTIVITY COEFFICIENT ln_GAMMA_k_i



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



        ln_g_r_i=[]

        for ii in range(self.NC):
            soma = 0.0
            for kk in range(self.NsG_i[ii]):
                soma+=self.v[ii][self.k.index(self.ComponentsSubGroups[ii][kk])]*(ln_GAMMA_k[self.k.index(self.ComponentsSubGroups[ii][kk])]-ln_GAMMA_i_k[ii][kk])
            ln_g_r_i.append(soma)
        Gamma_i=[]
        for i in range(self.NC):
            Gamma_i.append(np.exp(ln_g_c_i[i]+ln_g_r_i[i]))

        return Gamma_i

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





