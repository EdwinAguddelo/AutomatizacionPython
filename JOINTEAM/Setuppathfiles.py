import os

class setupPaths:
    def __init__(self,resourcesPath):
        self.resourcesPath = resourcesPath

        self.DefectosPath = "DEFECTOS/"
        self.BackUpPath = "BKUP/backup.xls"

        self.DefectosPathFolder = os.path.join(self.resourcesPath,self.DefectosPath)
        self.BackUpPathFile = os.path.join(self.resourcesPath, self.BackUpPath)

        self.filesDefectos = []
        self.filesCasosPrueba = []

        for file in os.listdir(self.DefectosPathFolder):
            if file.endswith('.xlsx'):
                if os.path.join(self.DefectosPathFolder,file) not in self.filesDefectos:
                   self.filesDefectos.append(os.path.join(self.DefectosPathFolder,file))

        for file in os.listdir(self.resourcesPath):
            if file.endswith('.xls'):
                if os.path.join(self.resourcesPath,file) not in self.filesCasosPrueba:
                    self.filesCasosPrueba.append(os.path.join(self.resourcesPath,file))
