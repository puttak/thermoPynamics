#coding: utf-8
from databases.GetDataBaseDir import GetDataBaseDir
from UNIFAC import UNIFAC
print GetDataBaseDir()
a=UNIFAC()
print a.computeGama(300, [0.1])
