#coding: utf-8
import matplotlib.pyplot as plt

import time
start=time.time()
import calculations.JTcooling.pyJT as jt
import calculations.ExpansionHydLimit.JT_pydrates as jtHYD



#
# a = jtHYD.PlotHydLimit([300, 310], 70, 400, [193, 125, 295, 236], [0.9, 0.01, 0.02, 0.07],0,None,None,'SRK')
# a.writeHydLim()
#
# # a = jtHYD.maxDeltaP(300, 100, [193, 125, 295], [0.9329, 0.05325, 1 - (0.9329 + 0.05325)])
# # print a.AlreadyStable
# # print a.solve([300, 10])
#
# end=time.time()
# print 'Execução levou ' + str( end - start) + ' segundos'
# #
# # a=jt.PlotIsenthalpic([193,125],300, 350, [0.7, 0.3], 'vapor', 'SRK')
# # a.saveFig([270, 320])

