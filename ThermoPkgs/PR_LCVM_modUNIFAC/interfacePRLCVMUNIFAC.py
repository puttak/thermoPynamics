import numpy as np
from getsqldata import ReadSqlData

class FluidPRLCVMUNIFAC:
    def __init__(self, ID):
        self.ID = ID


class FluidDataPRLCVMUNIFAC:
    def __init__(self, fluid):

        data=ReadSqlData(fluid.ID)

        critical=data.GetCritical()
        self.Tc=critical[0]
        self.Pc=critical[1]
        self.w=critical[2]
        self.Name=data.GetName()