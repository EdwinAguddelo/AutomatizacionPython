import pandas as pd

def backupBuild(BackUpPathFile):
    backupDataSet = pd.read_excel(BackUpPathFile)

    backupDataSet = backupDataSet[['EQUIPO','USUARIO DE RED BANCO']]
    backupDataSet = backupDataSet.rename(columns = {'USUARIO DE RED BANCO':'USUARIO'})
    backupDataSet['USUARIO'] = backupDataSet['USUARIO'].str.lower()

    return backupDataSet


def  buildDtf(files,shtName):
    dataframesArray = []
    for path in files:
        data = pd.read_excel(path,sheet_name = shtName)
        dataframesArray.append(data)
    return dataframesArray
