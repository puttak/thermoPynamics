import numpy as np
import matplotlib.pyplot as plt
#Exemplo:plotZ(co2.EOS, dados.Tc, dados.Pc)
def plotZ(EOS,T,P ,lower=-1.0, upper=2.0):
    poly_coef = EOS(T,P)
    [c3, c2, c1, c0] = poly_coef

    eosZ = lambda Z: c3 * Z ** 3 + c2 * Z ** 2 + c1 * Z + c0
    Z = list(np.linspace(lower, upper, 1000))
    eosZvalues = []
    for z in Z:
        eosZvalues.append(eosZ(z))
    eixozero = [0.0 for i in range(1000)]
    print poly_coef
    print np.roots(poly_coef)
    plt.plot(Z, eosZvalues, Z, eixozero)
    plt.show()

    return