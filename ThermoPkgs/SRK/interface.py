import numpy as np
from getsqldata import ReadSqlData
##### Este arquivo contem as classes que atuam como interface, ou seja,  que entram como parametro na classe da EOS
#
# class Fluid:
#     def __init__(self, ID, z):
#         self.ID = ID
#         self.z =  np.array(z)
#
# class FluidData:
#     def __init__(self, fluid):
#         data=ReadData(fluid.ID)
#
#         self.Tc=data.GetTc()
#         self.Pc=data.GetPc()
#         self.w=data.GetW()
#         self.kij=data.GetEOSkij('SRK')

#TODO: Renomar FluidData pra indicar que são dados de uma EoS e de qual EoS. Já que fdata vai ser específica pra uma EoS, não é necessário ter um indicador.

class Fluid:
    def __init__(self, ID, z):
        self.ID = ID
        self.z =  np.array(z)

class FluidData:
    def __init__(self, fluid):

        data=ReadSqlData(fluid.ID)

        critical=data.GetCritical()
        self.Tc=critical[0]
        self.Pc=critical[1]
        self.w=critical[2]
        self.kij=data.GetEOSkij('SRK')

        self.Name=data.GetName()