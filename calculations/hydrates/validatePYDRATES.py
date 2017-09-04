from PCAL import PCAL

a=PCAL(ID=[193, 125,295,47,249], y=[0.79942,0.05029,0.03000,0.02090,0.09939],isThereInib=0, InibMassFraction=None, flagEOS='SRK')

print a.computePD(298.5,1.0) #=278.508
