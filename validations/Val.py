#coding: utf-8
import numpy as np
import inspect

#This functions will assume that the inputs are Ok. Temperature is a positive number. Composition is a vector, etc.

def TemperatureIsOk(T):

    try:
        assert type(T) in [float, np.float64, np.float16, np.float32, int]
    except:
        callerMethodName = 11
        raise ValueError('Error in %s. T must be float' % ('testando'))

def componentIDisOk(ID):
    try:
        assert type(ID) in [list, np.ndarray]
    except:
        raise ValueError('Error in %s. T must be a iterable' % ('testando'))