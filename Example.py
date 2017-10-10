#coding: utf-8

#This example shows how to compute some properties using the implemented models


from ThermoPkgs.UNIFAC.interface import FluiDataUNIFAC
from ThermoPkgs.PR_LCVM_UNIFAC.interfacePRLCVMUNIFAC import FluidDataPRLCVMUNIFAC, FluidPRLCVMUNIFAC
from ThermoPkgs.PR_LCVM_UNIFAC.PR_LCVM_UNIFAC import PR_LCVM_UNIFAC

fluid = FluidPRLCVMUNIFAC(ID=[194,342]) #This object has only one attribute that identifies the component [194 (Methanol), 342 (Water)]

criticalProperties = FluidDataPRLCVMUNIFAC(fluid) #This object contains the crictical properties that is read from the database when the __init__ method is executed.

unifacParameters = FluiDataUNIFAC(fluid) #This object contais the unifac parameters that is read from the database when the __init__ method is executed.

EoSmodel = PR_LCVM_UNIFAC(fluid, criticalProperties, unifacParameters) #This object is the model. The previous objectes are input to this method.


#Compressibility factor
print EoSmodel.computeZ(T=300, P=15, z=[0.7, 0.3], Phase='liquid') #Method that compute Z (compressibility factor) T =temperature in Kelvin,
print EoSmodel.computeZ(T=300, P=15, z=[0.7, 0.3], Phase='vapor')  # P = pressure in bar, z = molar composition vector, Phase = indicate the desired Cubic EoS root.
                                                                   #If there's 3 roots : vapor will return the max root, liquid will return the min root
                                                                   #If there's only one root, both flags (vapor or liquid) will return the same value.
#Fugacity coefficient
print EoSmodel.computeFUG(T=300, P=15, z=[0.7, 0.3], Phase='liquid') #Fugacity coefficient
print EoSmodel.computeFUG(T=300, P=15, z=[0.7, 0.3], Phase='vapor')

#Residual enthalpy
print EoSmodel.computeHR_numerical(T=300, P=15, z=[0.7, 0.3], Phase='vapor') #Residual Enthalpy
print EoSmodel.computeHR_numerical(T=300, P=15, z=[0.7, 0.3], Phase='liquid')