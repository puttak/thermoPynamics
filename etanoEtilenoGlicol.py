#coding: utf-8

from calculations.hydrates.PCAL import PCAL

ID = [125] #Etano
y = [1.0] #Puro
isThereInib = True #Tem inibidor
InibID =[137] #etilenoglicol
InibMassFraction_1 = [0.25] #Fração Mássica do inibidor
InibMassFraction_2 = [0.50]

flagEOS = 'PRLCVMUNIFAC' #Seleciona a equação de estado
flagGamma = 'UNIFAC'     #Seleciona o modelo de gamma

etano_EtilenoGlycol = PCAL(ID=ID, y=y, isThereInib=isThereInib, InibID=InibID,
                           InibMassFraction=InibMassFraction_1, flagEOS=flagEOS, flagGamma=flagGamma)   #Classe que tem os cálculos

f = open('D:\etanoEtilenoglicol.csv', 'w') #arquivo que vai receber os resultados


TemperaturaS = [261.95, 266.75, 272.95 ] #Kelvin

chutePressoeS = [2.4, 5.1, 11.0] #bar



resultado =[]
for i in range( len(TemperaturaS) ):
    P = etano_EtilenoGlycol.computePD(TemperaturaS[i], chutePressoeS[i])
    resultado.append(P)

print(resultado)
titulo = "Gás = Etano ; Inibidor = EtilenoGlicol ; Modelo = PR-LCVM-UNIFAC \n"

f.write(titulo)

cabecalho = "Temperatura (K) ; Pressão (K) ; Inibidor (wt%) \n"
f.write(cabecalho)

for i in range(len(resultado)):
    t = str(TemperaturaS[i])
    p = str(resultado[i])
    w = str(InibMassFraction_1)
    linha = t + ";" + p + ';' + w +"\n"
    f.write(linha)




#Segunda fração do inibidor
etano_EtilenoGlycol = PCAL(ID=ID, y=y, isThereInib=isThereInib, InibID=InibID,
                           InibMassFraction=InibMassFraction_2, flagEOS=flagEOS, flagGamma=flagGamma)   #Classe que tem os cálculos



TemperaturaS = [247.85 , 252.25 , 255.95, 260.95] #Kelvin

chutePressoeS = [2.4 , 4.3 , 7 ,12.3] #bar


resultado =[]
for i in range( len(TemperaturaS) ):
    P = etano_EtilenoGlycol.computePD(TemperaturaS[i], chutePressoeS[i])
    resultado.append(P)

for i in range(len(resultado)):
    t = str(TemperaturaS[i])
    p = str(resultado[i])
    w = str(InibMassFraction_2)
    linha = t + ";" + p + ';' + w + "\n"
    f.write(linha)

f.close()

print('finished')




