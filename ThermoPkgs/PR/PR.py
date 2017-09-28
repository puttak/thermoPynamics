# -*- coding: utf-8 -*-

#Temperatura Kelvin
#Pressao bar
#Volume cm3
#Qtde de materia g-mol
import numpy as np
import scipy.integrate as scint


class PR:

    def __init__(self,fluid, fluidData):

        self.R = 83.144621  # bar.cm3/(mol.K)

        try:
            self.ID = fluid.ID
            assert type(self.ID) == list
            self.NC = len(self.ID)
        except:
            raise ValueError('ID não definido corretamente na instancia fluid')

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


    def computeFUG(self,T,P,z,Phase):

        if type(z)==list:
            z=np.array(z)

        try:
            assert type(z) == np.ndarray
            assert self.NC == len(self.ID)
        except:
            raise ValueError('z não definido corretamente em computeFUG')
        try:
            assert type(T) in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeFUG. T deve ser do tipo float')
        try:
            assert type(P)in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeFUG. P deve ser do tipo float')

        localZ=self.computeZ(T, P,z, Phase)

        fugCoefficient=self._FUG(localZ, z)

        return fugCoefficient

    def computeZ(self, T, P, z , Phase):

        if type(z) == list:
            z = np.array(z)

        try:
            assert type(z) == np.ndarray
            assert self.NC == len(self.ID)
        except:
            raise ValueError('z não definido corretamente em computeZ')

        try:
            assert type(T) in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeZ. T deve ser do tipo float')
        try:
            assert type(P)in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeZ. P deve ser do tipo float')

        p=np.poly1d(self._EOS(T, P, z))
        allZvalues=np.roots(p)

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


    def _EOS(self, T, P, z):
        # EOS_SRK pode ser chamado por um método que ajeite as entradas. De modo que quando for add uma EOS, apenas por as equações.
        #Ok
        ai=0.45724*self.R**2*self.Tc**2/self.Pc #Ok
        bi=0.07780*self.R*self.Tc/self.Pc  #Ok
        self.ai_aaa=ai
        m=0.37464 + 1.54226*self.w-0.26992*self.w**2
        alfaT=(1 + m*(1-(T/self.Tc)**0.5 ) )**2

        aci=ai*alfaT
        self.aiT=aci
        self.biT=bi

        ncomp=int(len(z))
        aij=np.zeros((ncomp,ncomp))
        for i in range(ncomp):
            for j in range(ncomp):
                expression1=(aci[i]*aci[j])**0.5
                expression1=expression1*(1-self.kij[i][j])
                aij[i][j]=expression1
        ac=0.0
        b=0.0
        for i in range(ncomp):
            b+= z[i] * bi[i]
            for j in range(ncomp):
                expression1= z[i] * z[j] * aij[i][j]
                ac+=expression1

        self.aijSRK=aij
        self.aSRK=ac
        self.bSRK=b
        A=ac*P/(self.R*T)**2
        B=b*P/(self.R*T)
        self.A_SRK=A
        self.B_SRK=B


        c3=1
        c2=-1*(1-B)
        c1=A-2*B-3*B**2
        c0=-1*(A*B-B**2-B**3)

        #Variáveis que saem por self. ficaram aqui:
        self.a = ac
        self.b = b
        self.m = m
        self.ai = aci
        self.aci = ai
        self.alfaT = alfaT

        return [c3,c2,c1,c0]


    def _FUG(self, localZ, z):

        A=self.A_SRK
        B=self.B_SRK
        CoFug=[]
        AX=-np.log(localZ-B)
        BX=(A/(2**1.5*B))*np.log((localZ+B*(2**0.5+1))/(localZ-B*(2**0.5-1)))
        for k in range(self.NC):
            soma=0.0
            for i in range(self.NC):
                soma=soma+z[i]*self.aijSRK[i][k]
            S=soma*2.0/self.aSRK - self.biT[k] / self.bSRK
            AP=(localZ-1.0)*self.biT[k] / self.bSRK + AX - S * BX
            CoFug.append(AP)

        CoFug=np.exp(CoFug)


        return CoFug

    def computeResidualEnthalpy(self,T,P,z, Phase):
        Z = self.computeZ(T, P, z, Phase)
        ac_i = self.aci
        alfaT_i = self.alfaT
        a_i = self.ai
        a_T = self.a
        b=self.b
        v = Z*self.R*T/P
        m_i = self.m
        Tc_i = self.Tc
        k_i_j = self.kij

        dadT_i =[]
        for i in range(self.NC):
            termo1=ac_i[i]*alfaT_i[i]**0.5
            termo2=-m_i[i]*(T/Tc_i[i])**0.5/T
            dadT_i.append(termo1*termo2)

        del termo2
        del termo1

        dadT = 0.0

        for i in range(self.NC):
            for j in range(self.NC):
                termo1 = z[i]*z[j]*(1-k_i_j[i][j])
                termo2 = dadT_i[i]*(a_i[j]/a_i[i])**0.5/2+dadT_i[j]*(a_i[i]/a_i[j])**0.5/2
                dadT+=termo1*termo2

        parcela1 = (a_T - T * dadT) / (2*b*2**0.5)
        dentroLn = (v + b + b*2**0.5) / (v+b-b*2**0.5)
        HR = self.R * T * (1 - Z) + parcela1 * np.log(dentroLn)

        return HR

    def computeHR_numerical(self,T,P,z,Phase):
        self.tolHR = 1E-9
        tol = self.tolHR*T

        dZdT_P = lambda P_lambda: (tol*P_lambda) ** -1 * (self.computeZ(T + tol, P_lambda, z, Phase) - self.computeZ(T, P_lambda, z, Phase))
        [HR,erro_inegral] =  scint.quad(dZdT_P, 0, P)
        HR = self.R * T ** 2 *HR
        assert erro_inegral<1E-2
        return HR


