#coding: utf-8
import time
start=time.time()
import calculations.JTcooling.pyJT as jt

end=time.time()
print 'Execução levou ' + str( end - start) + ' segundos'

a=jt.PlotIsenthalpic([193,125],300, 350, [0.7, 0.3], 'vapor', 'SRK')
a.saveFig([270, 320])


