import os

class setupPaths:
    def __init__(self,resourcesPath):
        self.resourcesPath = resourcesPath

        self.soportePath = "baseSoporte/"

        self.soporteFile = "CERTIFICACIÓN.xlsx"
        self.regresionFile = "Regresion.xlsm"


        self.soportePathFolder = os.path.join(self.resourcesPath,self.soportePath)

        self.soportePathFile = os.path.join(self.soportePathFolder,self.soporteFile)
        self.regresionPathFile = os.path.join(self.resourcesPath,self.regresionFile)  
