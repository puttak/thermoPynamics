import time
from calculations.ExpansionHydLimit.JT_pydrates import maxDeltaP

start=time.time()
aaa=maxDeltaP(300,300,ID=[193, 125,295,47,249], y=[0.79942,0.05029,0.03000,0.02090,0.09939])
fa = aaa.solve(Xguess=[298.54,281.0])

print fa

end=time.time()

print end-start