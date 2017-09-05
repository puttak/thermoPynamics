#coding: utf-8
import numpy as np
from GetData import ReadDataUNIFAC
class Fluid:
    def __init__(self, ID, z):
        self.ID = ID
        self.z =  np.array(z)


class FluiDataUNIFAC:
    def __init__(self,fluid):
        dataUNIFAC = ReadDataUNIFAC(fluid.ID)

        dataUNIFAC.GetComponentGroupSpecification()



