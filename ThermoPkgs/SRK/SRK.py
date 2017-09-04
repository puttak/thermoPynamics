# -*- coding: utf-8 -*-

#Temperatura Kelvin
#Pressao bar
#Volume cm3
#Qtde de materia g-mol


import numpy as np



class SRK:

    def __init__(self,fluid, fluidData):

        self.R = 83.144621  # bar.cm3/(mol.K)

        try:
            self.ID = fluid.ID
            assert type(self.ID) == list
        except:
            raise ValueError('ID não definido corretamente na instancia fluid')

        try:
            self.z = fluid.z
            assert type(self.z) == np.ndarray
        except:
            raise ValueError('z não definido corretamente na instancia fluid')

        self.NC = len(self.z)

        assert self.NC == len(self.ID)

        try:
            self.Tc = fluidData.Tc
            assert type(self.Tc) == np.ndarray
        except:
            raise ValueError('Tc não definido corretamente na instancia fluidData')
        try:
            self.Pc = fluidData.Pc
            assert type(self.Pc) == np.ndarray
        except:
            raise ValueError('Pc não definido corretamente na instancia fluidData')
        try:
            self.w = fluidData.w
            assert type(self.w) == np.ndarray
        except:
            raise ValueError('w não definido corretamente na instancia fluidData')
        try:
            self.kij = fluidData.kij
            assert type(self.kij) == np.ndarray
        except:
            raise ValueError('kij não definido corretamente na instancia fluidData')


    def computeFUG(self,T,P,Phase):
        try:
            assert type(T) in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeFUG. T deve ser do tipo float')
        try:
            assert type(P)in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeFUG. P deve ser do tipo float')


        localZ=self.computeZ(T, P,Phase)

        fugCoefficient=self.FUG(localZ)

        return fugCoefficient

    def computeZ(self, T, P,Phase):
        try:
            assert type(T) in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeZ. T deve ser do tipo float')
        try:
            assert type(P)in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeZ. P deve ser do tipo float')


        c=self.EOS(T,P)
        p=np.poly1d(c)

        allZvalues=np.roots(p)
        # print 'allzvalues', allZvalues
        # Remove raizes complexas
        realZ = []
        for i in range(len(allZvalues)):
            bol = allZvalues[i].imag != 0
            if not bol:
                realZ.append(allZvalues[i].real)

        Zmax = max(realZ)
        Zmin = min(realZ)

        if Zmax < 0:
            raise ValueError('EOS forneceu raiz negativa')


        if Phase == 'vapor':
            Z = Zmax
        elif Phase == 'liquid':
            Z = Zmin
        else:
            raise ValueError('Estado fisico nao reconhecido')

        return Z


    def EOS(self, T, P):
        # EOS_SRK pode ser chamado por um método que ajeite as entradas. De modo que quando for add uma EOS, apenas por as equações.

        #Ok
        ai=0.42747*self.R**2*self.Tc**2/self.Pc #Ok
        bi=0.08664*self.R*self.Tc/self.Pc  #Ok
        self.ai_aaa=ai
        m=0.480 + 1.574*self.w-0.176*self.w**2
        alfaT=(1 + m*(1-(T/self.Tc)**0.5 ) )**2

        aci=ai*alfaT
        self.aiSRK=aci
        self.biSRK=bi

        ncomp=int(len(self.z))
        aij=np.zeros((ncomp,ncomp))
        for i in range(ncomp):
            for j in range(ncomp):
                expression1=(aci[i]*aci[j])**0.5
                expression1=expression1*(1-self.kij[i][j])
                aij[i][j]=expression1
        ac=0.0
        b=0.0
        for i in range(ncomp):
            b+= self.z[i] * bi[i]
            for j in range(ncomp):
                expression1= self.z[i] * self.z[j] * aij[i][j]
                ac+=expression1

        self.aijSRK=aij
        self.aSRK=ac
        self.bSRK=b
        A=ac*P/(self.R*T)**2
        B=b*P/(self.R*T)
        self.A_SRK=A
        self.B_SRK=B


        c3=1
        c2=-1
        c1=A-B-B**2
        c0=-A*B
        return [c3,c2,c1,c0]


    def FUG(self, localZ):
        #Ok
        A=self.A_SRK
        B=self.B_SRK
        CoFug=[]
        AX=-np.log(localZ-B)
        BX=A*np.log(1+B/localZ)/B
        for k in range(self.NC):
            soma=0.0
            for i in range(self.NC):
                soma=soma+self.z[i]*self.aijSRK[i][k]
            S=soma*2.0/self.aSRK - self.biSRK[k]/self.bSRK
            AP=(localZ-1.0)*self.biSRK[k]/self.bSRK + AX - S*BX
            CoFug.append(AP)

        CoFug=np.exp(CoFug)


        return CoFug


