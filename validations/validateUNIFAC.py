#coding: utf-8
from databases.GetDataBaseDir import GetDataBaseDir
from ThermoPkgs.UNIFAC.UNIFAC import UNIFAC
from ThermoPkgs.UNIFAC.interface import Fluid, FluiDataUNIFAC
import time
import numpy as np
import matplotlib.pyplot as plt


start = time.time()

fluido = Fluid(ID=[194,342])

data = FluiDataUNIFAC(fluido)
a=UNIFAC(fluido, data)



T=50+273.15
x1=np.linspace(0.0, 1.0, 11)
pvap194=417.4
pvap342=92.5
gamma=[]
P=[]
y=[]
for x in x1:
    if x==0:
        y.append(x)
        P.append(pvap342)
        continue
    elif x==1.0:
        y.append(x)
        P.append(pvap194)
        continue

    g=a.computeGama(T, [x,1-x])
    p=x*g[0]*pvap194+(1-x)*g[1]*pvap342

    y.append(x*g[0]*pvap194/p)
    P.append(p)
    gamma.append(g)


yvalidacao=[0.0, 0.46871508744417661, 0.61788915940523659,
            0.70075152635189586, 0.75962200988609185, 0.80755098298446781,
            0.84986328685262347, 0.88912975419795937, 0.92674333574715195, 0.9635266461767017, 1.0]
Pvalidacao=[92.5, 158.63833839213214, 202.11369992345607,
            235.48769471007361, 264.04368117377311, 290.29018989778399, 315.53404132402579,
            340.50753559043517, 365.64553819196249, 391.21837382162062, 417.4]
soma_e=[]
some_e_p=[]
for i in range(len(P)):
    soma_e.append(yvalidacao[i]-y[i])
    some_e_p.append(Pvalidacao[i]-P[i])

print sum(soma_e), sum(some_e_p)

end = time.time()

print 'durou '+str(end-start)+' segundos'

plt.plot(x1,P,y,P)
plt.show()


