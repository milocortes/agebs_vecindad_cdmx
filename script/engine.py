from shapely.geometry import Polygon, Point,LineString,MultiPolygon
from shapely.geometry.base import BaseMultipartGeometry
import shapely.wkt
import numpy as np
from tqdm import tqdm

def touches_geometria(evalua,geometria):
    if isinstance(evalua,BaseMultipartGeometry):
        resultados = []
        for objetos in evalua:
            resultados.append(touches_geometria(objetos,geometria))
        return any(resultados)
    else:
        evalua_status = evalua.is_valid
        geometria_status = geometria.is_valid

        if isinstance(geometria,BaseMultipartGeometry):
            geometria = geometria.buffer(0)
            geometria_status = geometria.is_valid
        if (geometria_status == False and evalua_status == False ):
            return geometria.boundary.touches(evalua.boundary)
        elif (geometria_status == True and evalua_status == False ):
            return geometria.touches(evalua.boundary)
        elif (geometria_status == False and evalua_status == True ):
            return geometria.boundary.touches(evalua)
        else:
            return geometria.touches(evalua)


def layer2net(capa):
    almacena = {}
    agebs_total = capa.shape[0]

    for geometria in tqdm(range(agebs_total)):
        cvegeo=capa.loc[geometria,"CVEGEO"]
        vecinos = np.array(capa['geometry'].apply(lambda x: touches_geometria(x,capa.loc[geometria,"geometry"])),dtype=int)
        almacena[cvegeo]= vecinos

    return almacena
