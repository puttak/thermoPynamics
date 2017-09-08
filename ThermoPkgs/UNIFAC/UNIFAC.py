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

        self.r = unifacdata.r
        self.q = unifacdata.q
        self.a_m_n = unifacdata.a_m_n







    def computeGama(self, T, x):
        assert sum(x)==1
        assert len(x) == self.NC
        x = np.array(x)

        PSI_m_n = np.exp(-self.a_m_n/T)

        viXi=np.dot(x,self.v)
        Xm = viXi/sum(viXi)

        r_comp=[]
        q_comp=[]
        for i in range(self.NC):
            r_comp.append( np.dot(self.v[i],self.r) )
            q_comp.append(np.dot(self.v[i], self.q) )

        produto_q_x = q_comp*x
        produto_r_x = r_comp*x

        Q_area_fraction = produto_q_x/sum(produto_q_x)
        FI_seg_fraction = produto_r_x/sum(produto_r_x)

        produto_m = self.q*Xm
        TETAm = produto_m/sum(produto_m)
        #TODO: CRIAR UMA FUNÇÃO QUE RECEBA COMPONENTES E COMPOSIÇÃO. DE MODO QUE POSSA SE FAZER PARA CADA COMPONENTE PURO E DEPOIS PARA TODOS.






