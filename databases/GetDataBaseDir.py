import os

def GetDataBaseDir():
    databaseDir = os.path.dirname( os.path.abspath(__file__) )
    return databaseDir
