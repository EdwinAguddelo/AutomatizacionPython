def getNextSprintNumber(baseDataSet):
    return (max(baseDataSet['SPRINT'].tolist())+1)

def getAppsToRows(listaCasosPruebaSumadosDataset,listaDefectosSumadosDataset):

    listaAppsCasosPrueba=listaCasosPruebaSumadosDataset.index.tolist()
    listaAppsDefectos=listaDefectosSumadosDataset.index.get_level_values(0).tolist()
    toAggregate=listaAppsDefectos
    total=listaAppsCasosPrueba
    for appCasoPrueba in listaAppsCasosPrueba:
        for appDefectos in listaAppsDefectos:
            if appDefectos in appCasoPrueba:
                toAggregate.remove(appDefectos)
    total=total+toAggregate
    return total

