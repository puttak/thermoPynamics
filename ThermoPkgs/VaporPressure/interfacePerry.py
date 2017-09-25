#coding: utf-8
from GetDataPerry import ReadPerrVaporPressureData
class FluidPerryVaporPressure:
    def __init__(self, ID):
        self.ID = ID

class FluidDataPerry:
    def __init__(self, fluido):
        self.ID = fluido.ID
        data = ReadPerrVaporPressureData(self.ID)
        [self.C1, self.C2, self.C3, self.C4, self.C5] = data.GetCoef()