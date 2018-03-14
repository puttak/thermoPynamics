#coding: utf-8
#This shows how to compute the Joule-Thomson cooling effect through a isenthalpic valve expansion.

from calculations.JTcooling.pyJT import JT


ID=[193, 125,295,47,249] #The ID of the components in the database => Methane, Etane, Propane, CO2, N2.
y=[0.79942,0.05029,0.03000,0.02090,0.09939] #Molar composition of the gas.

a=JT(300, 300, ID, y,fase='vapor',flagEOS='SRK')    # (T1 -> Temperature before expansion , P1-> Pressure before expansion, ID, y, fase -> vapor or liquid, flagEOS->C-EOS flag)

#SRK stands for SRK cubic equations of state.

#
print a.computeT2(280.0) #T2=298.531558557

