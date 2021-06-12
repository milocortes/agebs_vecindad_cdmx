# Cargamos la librerías
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point,LineString
import matplotlib.pyplot as plt
import warnings
from engine import *

import os
## Desactivamos los future warnings
warnings.simplefilter(action='ignore', category=Warning)

# Nos cambiamos al directorio data
os.chdir("../data")

## Cargamos la geometría de las agebs del MGN2020
print("%-----------------------------------------%")
print("Cargamos la geometría de las agebs de la CDMX")
print("%-----------------------------------------%")
agebs = gpd.read_file("MGN2020_AGEB.zip").query("CVE_ENT=='09'").reset_index(drop=True)

# Reproyectamos las geometrías
agebs = agebs.to_crs("EPSG:4326")
# Obtenemos los centroides de los agebs
agebs['centroide']= agebs['geometry'].centroid

# Obtenemos los vecinos de cada ageb
print("%-----------------------------------------%")
print("Obtenemos los vecinos de cada ageb")
print("%-----------------------------------------%")

net_agebs = layer2net(agebs)

# Generamos un geodataframe con las LineString entre los centroides de los agebs vecinos
print("%-----------------------------------------%")
print("Generamos un geodataframe con las LineString entre los centroides de los agebs vecinos")
print("%-----------------------------------------%")
origen_lista = []
destino_lista = []
geometry_lista = []
for k,v in tqdm(net_agebs.items()):
    origen = agebs.query("CVEGEO =='{}'".format(k))["centroide"].item()
    indice_vecinos = list(np.where((net_agebs[k]==1))[0])
    lista_vecinos = np.take(list(net_agebs.keys()),indice_vecinos)
    for vecino in lista_vecinos:
        destino = agebs.query("CVEGEO =='{}'".format(vecino))["centroide"].item()
        origen_lista.append(k)
        destino_lista.append(vecino)
        geometry_lista.append(LineString([origen,destino]))

## Generamos el geopandas con la información anterior
df = pd.DataFrame({"origen": origen_lista,'destino': destino_lista,"geometry":geometry_lista})
gdf = gpd.GeoDataFrame(df, geometry='geometry')

gdf.plot(ax=agebs.boundary.plot(figsize=(20, 20),color='black'), alpha=.5,color ='red', edgecolor='black')
os.chdir("../output")
plt.savefig('agebs_vecindad.jpg')
plt.show()
