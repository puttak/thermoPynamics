#coding: utf-8
import numpy as np
from GetData import ReadDataUNIFAC
class Fluid:
    def __init__(self, ID):
        self.ID = ID



class FluiDataUNIFAC:
    def __init__(self,fluid):
        dataUNIFAC = ReadDataUNIFAC(fluid.ID)

        [self.NG, self.v, self.k, self.matrizG]=dataUNIFAC.GetComponentGroupSpecification()
        [self.r, self.q] = dataUNIFAC.Get_r_and_q()
        self.a_m_n = dataUNIFAC.GetGroup_interaction_parameter()




