import time
import numpy as np
from calculations.ExpansionHydLimit.JT_pydrates import maxDeltaP
from calculations.hydrates.PCAL import PCAL
from calculations.JTcooling.pyJT import JT
import matplotlib.pyplot as plt

start=time.time()

#grafico 1
hyd=PCAL(ID=[193, 125,295,47,249],  y=[0.79942,0.05029,0.03000,0.02090,0.09939],isThereInib=None, InibMassFraction=None, flagEOS='SRK')
T=np.linspace(275, 310, 100)
Pd=[]
for t in T:
    Pd.append(hyd.computePD(t, 1.0))

#grafico 2

isentalpica=JT(300.0, 300.0,ID=[193, 125,295,47,249], y=[0.79942,0.05029,0.03000,0.02090,0.09939], fase='vapor', flagEOS='SRK' )
T2=[]
P2=np.linspace(300, 190, 100)
for p2 in P2:
    T2.append(isentalpica.computeT2(p2, 299.0))

#deltaP

# # 0.0066
#
# aaa=maxDeltaP(311,136.195,ID=[193, 125,295], y=[0.9267,0.0529,0.0204])
# fa = aaa.solve(Xguess=[300.0,120.0])

# print fa
# pontoT=fa[0]
# pontoP=fa[1]

end=time.time()

print 'durou ' + str(end-start) + 'segundos'
plt.plot(T,Pd,T2,P2)
plt.show()
