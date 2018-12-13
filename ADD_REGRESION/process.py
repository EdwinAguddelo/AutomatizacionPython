from datetime import datetime
import unicodedata
import pandas as pd
from DesignStart import *
from utils import getNextSprintNumber



def addYear(RegresiondataSet):    
    RegresiondataSet['AÑO'] = datetime.now().year
    columna = RegresiondataSet['AÑO']
    del RegresiondataSet['AÑO']
    del RegresiondataSet['Código de la Aplicación']
    RegresiondataSet['Aplicación '] = RegresiondataSet['Aplicación '].str.upper()
    RegresiondataSet.insert(0,'Año',columna)

    return RegresiondataSet

def AppendDataFrames(soportedataSet,RegresiondataSet):
    ConsolidadoDT = soportedataSet.append(RegresiondataSet,sort=False)
    ConsolidadoDT = ConsolidadoDT.sort_values(by=['SPRINT'],ascending=False)
    ConsolidadoDT['Aplicación '] = ConsolidadoDT['Aplicación '].str.upper()

    return ConsolidadoDT

def cleanSpaces(SoporteConsolidadoDT):
    limpiar = []
    for app in SoporteConsolidadoDT['Aplicación ']:
        app = unicodedata.normalize("NFKD",app)
        limpiar.append(app)

    SoporteConsolidadoDT = SoporteConsolidadoDT.reset_index().drop('index', axis=1)
    SoporteConsolidadoDT['Aplicación '] = pd.DataFrame(limpiar)

    return SoporteConsolidadoDT

def findRepetedData(SoporteConsolidadoDT,sprintActual):
    SoporteConsolidadoDT = SoporteConsolidadoDT.groupby(['SPRINT']).get_group(sprintActual)
    apps = SoporteConsolidadoDT['Aplicación '].tolist()
    noAppsRepeted = []
    serepite =[]
    for app in apps:
        app = unicodedata.normalize("NFKD",app)
        if app not in noAppsRepeted:
            noAppsRepeted.append(app)
        else:
            serepite.append(app)

    return serepite,SoporteConsolidadoDT

def selectDataOfDataFrame(serepite,SoporteConsolidadoDT):
    dat=pd.DataFrame(columns=['Año','SPRINT','PITTs','Aplicación ','Tx E2E objetivo','Tx E2E Activas','% Cobertura E2E','Tx Reg objetivo','Tx Reg Activas','% Cobertura Reg','CP Manuales','CP Automáticos','CP Totales','Defectos Manuales','Defectos Automáticos','Defectos Totales','Impacto Alto','Impacto\nMedio','Impacto\nBajo'])
    SoporteConsolidadoDT = SoporteConsolidadoDT.fillna(0)
    for i in range(len(serepite)):
        datasol = SoporteConsolidadoDT[SoporteConsolidadoDT['Aplicación '] == serepite[i]]
        ElegirColumna = max(datasol.loc[:,('% Cobertura E2E','% Cobertura Reg')])
        if ElegirColumna ==  '% Cobertura E2E':
            Elmenor = min(datasol.loc[:,'% Cobertura E2E'])
            Elmayor = max(datasol.loc[:,'% Cobertura E2E'])
            if Elmayor == Elmenor:
                datasol=datasol.drop_duplicates(subset='Aplicación ',keep='first')
                dat=dat.append(datasol,sort=False)
            else:
                datasol = datasol[datasol['% Cobertura E2E'] > Elmenor]
                dat=dat.append(datasol,sort=False)
        else:
            Elmenor = min(datasol.loc[:,'% Cobertura Reg'])
            Elmayor = max(datasol.loc[:,'% Cobertura Reg'])
            if Elmayor == Elmenor:
                datasol=datasol.drop_duplicates(subset='Aplicación ',keep='first')
                dat=dat.append(datasol,sort=False)
            else:
                datasol = datasol[datasol['% Cobertura Reg'] > Elmenor]
                dat=dat.append(datasol,sort=False)

    return dat

def appendFinalData(SoporteConsolidadoDT,consolidadoFinalDT,dat,sprintActual):
    Consolidadofinal = SoporteConsolidadoDT.drop_duplicates(subset = 'Aplicación ', keep = False, inplace = False)
    Consolidadofinal = Consolidadofinal.append(dat)
    consolidadoFinalDTf = consolidadoFinalDT[consolidadoFinalDT['SPRINT'] < sprintActual]
    consolidadoFinalDTf = consolidadoFinalDTf.append(Consolidadofinal)
    consolidadoFinalDTf = consolidadoFinalDTf.sort_values(by=['SPRINT'],ascending=False)

    return consolidadoFinalDTf

def exportarAexcel(datasetFinal,filepath):
        datasetFinal.to_excel(filepath,index=False)
        print('Exportado a {}'.format(filepath))



def startProcess(dgs):
    Regresionfile = dgs.getfileRegresion()
    soportefile = dgs.getfilesSoporteDT()
    print(soportefile['Aplicación '])
    soporteRute = dgs.getSoporteRute()
    sprintActual = getNextSprintNumber(soportefile)
    RegresionDataF = addYear(Regresionfile)
    SoporteDataF = AppendDataFrames(soportefile,RegresionDataF)
    SoporteDataF = cleanSpaces(SoporteDataF)
    print('pasó!!')
    AppsRepeted,SoporteFiltradoDT = findRepetedData(SoporteDataF,sprintActual)
    dataSelectedToappend = selectDataOfDataFrame(AppsRepeted,SoporteFiltradoDT)
    DataFrameFinal = appendFinalData(SoporteFiltradoDT,SoporteDataF,dataSelectedToappend,sprintActual)
    exportarAexcel(DataFrameFinal,soporteRute)
