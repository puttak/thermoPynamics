#coding: utf-8
import numpy as np
from getsqldata import ReadSqlData
##### Este arquivo contem as classes que atuam como interface, ou seja,  que entram como parametro na classe da EOS

class FluidSRK:
    def __init__(self, ID):
        self.ID = ID

class FluidDataSRK:
    def __init__(self, fluid):

        data=ReadSqlData(fluid.ID)

        critical=data.GetCritical()
        self.Tc=critical[0]
        self.Pc=critical[1]
        self.w=critical[2]
        self.kij=data.GetEOSkij('SRK')

        self.Name=data.GetName()