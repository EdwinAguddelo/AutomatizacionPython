import pandas as pd
import os
#from pathFiles import defectosFiles,casosPruebaFiles,transformacionFilePath,soporteFilePath
from cleaners import *
from utils import getAppsToRows,getNextSprintNumber,getNextSprintNumberUpdate
from rowModel import TransformacionRow,rowFeeder
from folderFilesToDataFrame import *
from dataWrangling import defectosDataWrangling,casosPruebaDataWrangling

global defectosFiles,casosPruebaFiles,transformacionFilePath,soporteFilePath

def pathConstructor(paths):
    global defectosFiles,casosPruebaFiles,transformacionFilePath,soporteFilePath,resourcesFiles,pittsFilePath
    defectosFiles=paths.defectosFiles
    casosPruebaFiles=paths.casosPruebaFiles
    transformacionFilePath=paths.transformacionFilePath
    soporteFilePath=paths.soporteFilePath
    resourcesFiles = paths.resourcesPath
    pittsFilePath = paths.pittsFilePath

def process(Direccion,baseDataFrame,sprintNumber):


    DataFrameToAppend=baseDataFrame.drop(baseDataFrame.index, inplace=False)
    AppendedDataFrame = baseDataFrame.append(DataFrameToAppend, ignore_index=True)
    defectosDataFrames=folderPathToDataFrames(defectosFiles)
    casosPruebasDataFrames=folderPathToDataFrames(casosPruebaFiles)

    wraggledDefectosDatasets,wraggledCasosPruebasDatasets,FileNames=getWraggledDataFrames(
        defectosDataFrames,casosPruebasDataFrames,Direccion,sprintNumber)

    rowToAggregate=getRowsToAggregate(wraggledDefectosDatasets,wraggledCasosPruebasDatasets,sprintNumber,FileNames)
    #updatedDataFrameToExcel(rowToAggregate,AppendedDataFrame,baseDataFrame,'consolidado{}.xlsx'.format(Direccion))
    if Direccion == 'Transformacion':
        datasetDireccion = updatedDataFrameToExcel(rowToAggregate,AppendedDataFrame,baseDataFrame,transformacionFilePath)
    elif Direccion == 'Soporte':
        datasetDireccion = updatedDataFrameToExcelSoporte(rowToAggregate,AppendedDataFrame,baseDataFrame,soporteFilePath)

    return datasetDireccion


def startProcessSoporte():
    Direccion='Soporte'
    baseDataFrame=pd.read_excel(soporteFilePath)
    sprintNumber=getNextSprintNumber(baseDataFrame)
    soporteDataset = process(Direccion,baseDataFrame,sprintNumber)
    soporteDataset['Area']='Soporte'
    return soporteDataset

def startProcessTransformacion():
    Direccion='Transformacion'
    baseDataFrame=pd.read_excel(transformacionFilePath)
    sprintNumber=getNextSprintNumber(baseDataFrame)
    transformacionDataset = process(Direccion,baseDataFrame,sprintNumber)
    transformacionDataset['Area']='Transformacion'
    return transformacionDataset

def processFinal():
    transformacionDataset = startProcessTransformacion()
    soporteDataset = startProcessSoporte()
    sprintNumberSoporte=getNextSprintNumberUpdate(soporteDataset)
    JoinDataSetFinals(transformacionDataset,soporteDataset,sprintNumberSoporte)



def getWraggledDataFrames(defectosDataFrames,casosPruebasDataFrames,Direccion,sprintNumber):

    wraggledDefectosDatasets=[]
    wraggledCasosPruebasDatasets=[]
    FileNames=[]

    for file in range(len(defectosDataFrames)):

        FileNames.append(defectosFiles[file])

        defectosDataFrame=defectosDataFrames[file]
        defectosDataFrame=defectosDataWrangling(defectosDataFrame,Direccion,sprintNumber)

        casosPruebasDataFrame=casosPruebasDataFrames[file]
        casosPruebasDataFrame=casosPruebaDataWrangling(casosPruebasDataFrame,Direccion,sprintNumber)

        wraggledDefectosDatasets.append(defectosDataFrame)
        wraggledCasosPruebasDatasets.append(casosPruebasDataFrame)

    return wraggledDefectosDatasets,wraggledCasosPruebasDatasets,FileNames

def getRowsToAggregate(wraggledDefectosDatasets,wraggledCasosPruebasDatasets,sprintNumber,FileNames):
    rowToAggregate=[]
    for index,wraggledDefectosDatasets in enumerate(wraggledDefectosDatasets):
        total=getAppsToRows(wraggledCasosPruebasDatasets[index],wraggledDefectosDatasets)

        for releaseName in total:

            feed = rowFeeder(releaseName,wraggledDefectosDatasets,wraggledCasosPruebasDatasets[index])

            rowToAggregate.append(
                TransformacionRow(
                    releaseName,sprintNumber,feed,FileNames[index]
                    ).getRow()
                )
    return rowToAggregate

def updatedDataFrameToExcel(rowToAggregate,AppendedDataFrame,baseDataFrame,excelFileName):
    for i,row in enumerate(rowToAggregate):
        DataFrameToAppend=baseDataFrame.drop(baseDataFrame.index, inplace=False)
        DataFrameToAppend.loc[i, :] = row
        AppendedDataFrame = AppendedDataFrame.append(DataFrameToAppend, ignore_index=True)


    AppendedDataFrame=AppendedDataFrame.sort_values(by=['SPRINT'],ascending=False)
    AppendedDataFrame=AppendedDataFrame.reset_index()
    AppendedDataFrame=AppendedDataFrame.drop('index',axis=1)
    AppendedDataFrame.to_excel(excelFileName,index=False)

    return AppendedDataFrame

def updatedDataFrameToExcelSoporte(rowToAggregate,AppendedDataFrame,baseDataFrame,excelFileName):
    for i,row in enumerate(rowToAggregate):
        DataFrameToAppend=baseDataFrame.drop(baseDataFrame.index, inplace=False)
        DataFrameToAppend.loc[i, :] = row
        AppendedDataFrame = AppendedDataFrame.append(DataFrameToAppend, ignore_index=True)


    AppendedDataFrame=AppendedDataFrame.sort_values(by=['SPRINT'],ascending=False)
    AppendedDataFrame=AppendedDataFrame.reset_index()
    AppendedDataFrame=AppendedDataFrame.drop('index',axis=1)

    pittsDataSet=pd.read_excel(pittsFilePath)
    AppendedDataFrame = AppendedDataFrame.merge(pittsDataSet,left_on='PITTs',right_on='Subdominio',how='inner')
    AppendedDataFrame['PITTs_x']=AppendedDataFrame['PITTs_y'].tolist()
    AppendedDataFrame = AppendedDataFrame.drop(columns=['PITTs_y','Subdominio'])
    AppendedDataFrame = AppendedDataFrame.sort_values(by=['SPRINT'],ascending=False,)
    AppendedDataFrame = AppendedDataFrame.rename(columns={'PITTs_x':'PITTs'})

    AppendedDataFrame.to_excel(excelFileName,index=False)

    return AppendedDataFrame

def JoinDataSetFinals(transformacionDataset,soporteDataset,sprintNumber):
    datasetJoined =  transformacionDataset.append(soporteDataset)
    pathToExport='consolidado Sprint{}.xlsx'.format(sprintNumber)
    pathFinal=os.path.join(resourcesFiles,pathToExport)
    datasetJoined.to_excel(pathFinal,index=False)jijijij
    print('exportado '+pathToExport)
