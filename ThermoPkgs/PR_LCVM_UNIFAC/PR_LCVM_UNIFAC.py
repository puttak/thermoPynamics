# -*- coding: utf-8 -*-

#Temperatura Kelvin
#Pressao bar
#Volume cm3
#Qtde de materia g-mol

import numpy as np
from ThermoPkgs.UNIFAC.UNIFAC import UNIFAC

#TODO: A CLASSE PODE TER UM MÉTODO QUE CALCULA BOLP. PORÉM O CODIGO DO BOLP TEM QUE ESTAR EM UM LUGAR SÓ. ASSIM, QUALQUER MODIFICAÇÃO FICA MAIS SIMPLES DE SER FEITA.

class PR_LCVM_UNIFAC:

    def __init__(self,fluid, fluidData, unifacdata):

        self.R = 83.144621  # bar.cm3/(mol.K)
        self.PARAMETER_LAMBA_LCVM = 0.36
        self.lamb=self.PARAMETER_LAMBA_LCVM

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
        self.unifac=UNIFAC(fluid,unifacdata)

    def computeFUG(self,T,P,z,Phase):

        if type(z)==list:
            z=np.array(z)

        try:
            assert type(z) == np.ndarray
            assert self.NC == len(self.ID)
        except:
            raise ValueError('z não definido corretamente em computeFUG')

        for i in range(self.NC):
            if z[i] == 0:
                z[i] = 1E-12
        for i in range(self.NC):
            z[i] = z[i] / sum(z)


        try:
            assert type(T) in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeFUG. T deve ser do tipo float')
        try:
            assert type(P)in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeFUG. P deve ser do tipo float')

        localZ=self.computeZ(T, P,z,Phase)

        fugCoefficient=self._FUG(localZ, T,z)

        return fugCoefficient

    def computeZ(self, T, P,z,Phase):

        for i in range(len(z)):
            if z[i] == 0:
                z[i] = 1E-12
        for i in range(self.NC):
            z[i] = z[i] / sum(z)

        try:
            assert type(T) in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeZ. T deve ser do tipo float')
        try:
            assert type(P)in [float, np.float64, np.float16, np.float32, int]
        except:
            raise ValueError('Erro em computeZ. P deve ser do tipo float')

        p=np.poly1d(self._EOS(T, P,z))
        allZvalues=np.roots(p)

        # Remove raizes complexas
        realZ = []
        for i in range(len(allZvalues)):
            bol = allZvalues[i].imag != 0
            if not bol:
                realZ.append(allZvalues[i].real)

        Zmax = max(realZ)
        Zmin = min(realZ)
        # print Zmax,'eaaaaa'
        if Zmax < 0:
            raise ValueError('EOS forneceu raiz negativa')


        if Phase == 'vapor':
            Z = Zmax
        elif Phase == 'liquid':
            Z = Zmin
        else:
            raise ValueError('Estado fisico nao reconhecido')

        return Z


    def _EOS(self, T, P,z):
        # TODO: IMPORTANTE. VALIDAR CALCULO DO Z (VOLUME MOLAR)

        ai=0.45724*self.R**2*self.Tc**2/self.Pc #Ok
        bi=0.07780*self.R*self.Tc/self.Pc  #Ok
        self.ai_aaa=ai
        m=0.37464 + 1.54226*self.w-0.26992*self.w**2
        alfaT=(1 + m*(1-(T/self.Tc)**0.5 ) )**2

        aci=ai*alfaT
        self.aiT=aci
        self.biT=bi


        ncomp=self.NC

        bm=0.0
        for i in range(ncomp):
            bm+= z[i] * bi[i]

        Av=0.623
        Am=-0.52

        self.Av=Av
        self.Am=Am

        gamma = self.unifac.computeGama(T,z)
        self.gamma = gamma

        ge_RT=0.0
        for i in range(ncomp):
            ge_RT+=z[i]*np.log(gamma[i])
        termo1=(self.lamb/Av+(1-self.lamb)/Am)*ge_RT
        soma2=0.0
        termo3=0.0
        for i in range(ncomp):
            soma2+=z[i]*np.log(bm/bi[i])
            termo3+=z[i]*ai[i]/(bi[i]*self.R*T)
        termo2=(1-self.lamb)/Am*soma2

        alfaLCVM=termo1+termo2+termo3

        am=alfaLCVM*bm*self.R*T


        self.aSRK=am
        self.bSRK=bm
        A=am*P/(self.R*T)**2
        B=bm*P/(self.R*T)
        self.A_SRK=A
        self.B_SRK=B

        c3=1
        c2=-1*(1-B)
        c1=A-2*B-3*B**2
        c0=-1*(A*B-B**2-B**3)

        return [c3,c2,c1,c0]


    def _FUG(self, localZ, T,z):

        #Ok
        A=self.A_SRK
        B=self.B_SRK
        bi=self.biT
        ai=self.aiT
        bm=self.bSRK
        lamb=self.lamb
        Av=self.Av
        Am=self.Am
        gamma=self.gamma

        CoFug=[]
        for i in range(self.NC):
            termo1=bi[i]/bm*(localZ-1)
            termo2=-np.log(localZ-B)

            d_alfa_i=( lamb/Av + (1-lamb)/Am )*np.log( gamma[i] )
            d_alfa_i+=(1-lamb)/Am*(np.log(bm/bi[i]) + bi[i]/bm - 1)
            d_alfa_i+=ai[i]/(bi[i]*self.R*T)
            termo3_b=np.log( ( localZ+B*(1+2**0.5) )/ ( localZ+B*(1-2**0.5) )  )
            termo3=-(1/2**1.5)*d_alfa_i*termo3_b

            CoFug.append(termo1+termo2+termo3)
        CoFug=np.exp(CoFug)

        return CoFug
