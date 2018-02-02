#coding: utf-8

from calculations.hydrates.PCAL import PCAL

ID = [193] #Metano
y = [1.0] #Puro
isThereInib = True #Tem inibidor
InibID =[137] #etilenoglicol

T1 = [ 270.24, 273.49, 280.19, 287.1]
Pguess1 = [24.2,34,65.3 ,156.1]

T2 = [267.59 ,269.73 ,274.36 , 280.14 ,279.89 ]
Pguess2 = [37.7,49.3,78.6,161.4,163.8]

T3 = [263.43,266.32,266.48]
Pguess3 = [98.9,140.8,152.4]


InibMassFraction_1 = [0.1] #Fração Mássica do inibidor

InibMassFraction_2 = [0.30]
InibMassFraction_3 = [0.5]


flagEOS = 'PRLCVMUNIFAC' #Seleciona a equação de estado
flagGamma = 'UNIFAC'     #Seleciona o modelo de gamma

etano_EtilenoGlycol = PCAL(ID=ID, y=y, isThereInib=isThereInib, InibID=InibID,
                           InibMassFraction=InibMassFraction_1, flagEOS=flagEOS, flagGamma=flagGamma)   #Classe que tem os cálculos

f = open('D:\MetanoEtilenoglicol.csv', 'w') #arquivo que vai receber os resultados




resultado =[]
for i in range( len(T1) ):
    P = etano_EtilenoGlycol.computePD(T1[i], Pguess1[i])
    resultado.append(P)

print(resultado)

titulo = "Gás = Metano ; Inibidor = EtilenoGlicol ; Modelo = PR-LCVM-UNIFAC \n"

f.write(titulo)

cabecalho = "Temperatura (K) ; Pressão (K) ; Inibidor (wt%) \n"
f.write(cabecalho)


for i in range(len(resultado)):
    t = str(T1[i])
    p = str(resultado[i])
    w = str(InibMassFraction_1[0])
    linha = t + ";" + p + ';' + w +"\n"
    f.write(linha)




#Segunda fração do inibidor
etano_EtilenoGlycol = PCAL(ID=ID, y=y, isThereInib=isThereInib, InibID=InibID,
                           InibMassFraction=InibMassFraction_2, flagEOS=flagEOS, flagGamma=flagGamma)   #Classe que tem os cálculos



resultado =[]
for i in range( len(T2) ):
    P = etano_EtilenoGlycol.computePD(T2[i], Pguess2[i])
    resultado.append(P)

print(resultado)

for i in range(len(resultado)):
    t = str(T2[i])
    p = str(resultado[i])
    w = str(InibMassFraction_2[0])
    linha = t + ";" + p + ';' + w + "\n"
    f.write(linha)

#terceira fração do inibidor
etano_EtilenoGlycol = PCAL(ID=ID, y=y, isThereInib=isThereInib, InibID=InibID,
                           InibMassFraction=InibMassFraction_3, flagEOS=flagEOS, flagGamma=flagGamma)   #Classe que tem os cálculos



resultado =[]
for i in range( len(T3) ):
    P = etano_EtilenoGlycol.computePD(T3[i], Pguess3[i])
    resultado.append(P)

print(resultado)

for i in range(len(resultado)):
    t = str(T3[i])
    p = str(resultado[i])
    w = str(InibMassFraction_3[0])
    linha = t + ";" + p + ';' + w + "\n"
    f.write(linha)

f.close()

print('finished')




