import pandas as pd
#from pathFiles import defectosFiles,casosPruebaFiles,transformacionFilePath,soporteFilePath
from cleaners import *
from utils import getAppsToRows,getNextSprintNumber
from rowModel import TransformacionRow,rowFeeder
from folderFilesToDataFrame import *
from dataWrangling import defectosDataWrangling,casosPruebaDataWrangling

global defectosFiles,casosPruebaFiles,transformacionFilePath,soporteFilePath

def pathConstructor(paths):
    global defectosFiles,casosPruebaFiles,transformacionFilePath,soporteFilePath
    defectosFiles=paths.defectosFiles
    casosPruebaFiles=paths.casosPruebaFiles
    transformacionFilePath=paths.transformacionFilePath
    soporteFilePath=paths.soporteFilePath

def process(Direccion,baseDataFrame):

    sprintNumber=getNextSprintNumber(baseDataFrame)
    DataFrameToAppend=baseDataFrame.drop(baseDataFrame.index, inplace=False)
    AppendedDataFrame = baseDataFrame.append(DataFrameToAppend, ignore_index=True)

    defectosDataFrames=folderPathToDataFrames(defectosFiles)
    casosPruebasDataFrames=folderPathToDataFrames(casosPruebaFiles)

    wraggledDefectosDatasets,wraggledCasosPruebasDatasets,FileNames=getWraggledDataFrames(
        defectosDataFrames,casosPruebasDataFrames,Direccion,sprintNumber
        )

    rowToAggregate=getRowsToAggregate(wraggledDefectosDatasets,wraggledCasosPruebasDatasets,sprintNumber,FileNames)

    updatedDataFrameToExcel(rowToAggregate,AppendedDataFrame,baseDataFrame,'consolidado{}.xlsx'.format(Direccion))

def startProcessSoporte():
    #print("Hola..X2")
    Direccion='Soporte'
    baseDataFrame=pd.read_excel(soporteFilePath)
    process(Direccion,baseDataFrame)

def startProcessTransformacion():
    #print("hola")
    Direccion='Transformacion'
    baseDataFrame=pd.read_excel(transformacionFilePath)
    process(Direccion,baseDataFrame)

def getWraggledDataFrames(defectosDataFrames,casosPruebasDataFrames,Direccion,sprintNumber):

    wraggledDefectosDatasets=[]
    wraggledCasosPruebasDatasets=[]
    FileNames=[]

    for file in range(len(defectosDataFrames)):

        FileNames.append(defectosFiles[file])

        defectosDataFrame=defectosDataFrames[file]
        defectosDataFrame=defectosDataWrangling(defectosDataFrame,Direccion,sprintNumber)

        casosPruebasDataFrame=casosPruebasDataFrames[file]
        print(defectosFiles[file])
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
