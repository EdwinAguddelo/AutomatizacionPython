import os

class pathFiles():
    def __init__(self,resourcesPath):
        self.resourcesPath = resourcesPath

        self.transformacionFile='baseTransformacion/TRANSFORMACION.xls'
        self.soporteFile='baseSoporte/CERTIFICACIÓN.xlsx'

        self.casosPruebaPath='Queries Qc/QC 12/'
        self.defectosPath='Queries Qc/QC 12/DEFECTOS/'

        self.defectosPath=os.path.join(self.resourcesPath,self.defectosPath)
        self.casosPruebaPath=os.path.join(self.resourcesPath,self.casosPruebaPath)

        self.defectosFiles=[]
        self.casosPruebaFiles=[]

        self.transformacionFilePath=os.path.join(self.resourcesPath,self.transformacionFile)
        self.soporteFilePath=os.path.join(self.resourcesPath,self.soporteFile)


        for file in os.listdir(self.defectosPath):
            if file.endswith(".xlsx"):
                self.defectosFiles.append(os.path.join(self.defectosPath, file))

        for file in os.listdir(self.casosPruebaPath):
            if file.endswith(".xlsx"):
                self.casosPruebaFiles.append(os.path.join(self.casosPruebaPath, file))
