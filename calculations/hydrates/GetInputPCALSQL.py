#coding: utf-8
import os, warnings
import numpy as np
import openpyxl
import ThermoPkgs.SRK.getsqldata as GetMyData


class GetInputPCAL:
    def __init__(self, ID = None, y=None, isThereInib=None, InibID=None,InibMassFraction=None,flagEOS = None,InputFileName = 'InputPCAL.xlsx'):

        self.isThereInib=isThereInib
        if isThereInib not in [None,1,0,True,False]:
            raise ValueError('isThereInib deve ser boolean ou None')

        self.ID = ID
        self.NC = len(self.ID)
        self.y = y
        self.InibID = InibID
        self.InibMassFraction = InibMassFraction
        self.preprocess()

    def preprocess(self):
        #Normalizar composição e dar um warn!!
        soma = float(sum(self.y))

        if abs(soma-1.0) >= 1E-8: #Evitar problemas com casas decimais demais. se soma != de 1.0, é o que quer ser testado.
            warnings.warn('Somatório das composições não é igual a 1. A composição inserida será normalizada')
            for i in range(self.NC):
                self.y[i]=float(self.y[i])/soma

        #Adicionar todos os preprocess aqui nesse método.
        #Acredito que como são poucos inputs, não é necessário fazer como no GetDataPCAL. Lá são muitos dados, que podem precisar de mais preprocessamentos.
        #Transforma fração mássica dos inibidores em Molar
        #Criar vetor de id componentes da gase aquosa => componentes vapor + inibidores + água
        self.idwater = 342 #caso id água mude
        self.IDaqPHASE = list(self.ID)
        self.IDaqPHASE.append(self.idwater)
        self.XaqPHASEwithoutGas=[1.0]
        if self.isThereInib == True:
            for idinib in self.InibID:
                self.IDaqPHASE.append(idinib)
            aqData = GetMyData.ReadSqlData(ID=[self.idwater] + self.InibID)
            MM = aqData.GetMM()
            wa = 1 - sum(self.InibMassFraction)
            try:
                assert wa > 0
            except: raise ValueError('Fração mássicas dos inibidores excedem 1')
            self.XaqPHASEwithoutGas = list([wa] +self.InibMassFraction)
            moltotal = sum([self.XaqPHASEwithoutGas[i] / MM[i] for i in range(len(MM))])
            for i in range( len( self.XaqPHASEwithoutGas   )   ):
                self.XaqPHASEwithoutGas[i] = float(self.XaqPHASEwithoutGas[i])/MM[i]/moltotal

        self.XaqPHASEwithoutGas = [0.0 for i in range(len(self.ID))] + self.XaqPHASEwithoutGas












            #Essa parte do código gera um vetor ID e composição para a fase aquosa. Em ACT, a composição do gás entra. Ou seja, todos os inputs necessários para Thermo.

