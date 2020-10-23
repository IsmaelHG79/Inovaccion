
![Encabezado](images/encabezado.png)

# Exploratory Data Analysis

## ODK 99 - Inventario de Sitio (DG) / Inventario de Sitio RAN

## Descripción

Analizaremos los datos de la fuente **ODK 99** que corresponde al inventario de los elementos en sitio de 
red de acceso de radio y DG.

#### Conectando al Datalake


```python
import os
os.environ['JAVA_HOME'] = '/usr/java/jdk1.8.0_162'
os.environ['SPARK_HOME'] = '/opt/cloudera/parcels/CDH-6.2.0-1.cdh6.2.0.p0.967373/lib/spark'
import findspark
findspark.init()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import HiveContext
```


```python
conf = SparkConf().setAppName('EDA_ODK_99')  \
    .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)
```


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import re
import pandasql
import folium
from folium import plugins


import nltk
from nltk.probability import FreqDist
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#from pyspark.sql.functions import udf ,col
#from pyspark.sql.types import IntegerType,StringType

%matplotlib inline

from bokeh.io import show, output_notebook, output_file 
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20_11, Category20c_20, Category10_5,Category10_6, Category20_20, Plasma256
output_notebook()
```





### 1. Recolección de los datos: 

Se crea el dataframe de spark con el universo de datos crudos.  

Los datos se van a recolectar de la tabla ```rci_network_db.tx_stg_tabla_columnar_odk_99``` obtenida previamente en el notebook *ODK_99*.


```python
df_load = spark.sql("SELECT a.*, b.status as status_id, meta_started, meta_finished, meta_device_id, meta_user, id_site, cve_vendor, geo_lon, geo_lat, geo_alt, geo_acc, orig_site_code, orig_cve_vendor, comments, created_on, updated_on FROM rci_network_db.tx_stg_tabla_columnar_odk_99 a LEFT JOIN inventario.raw_panda_eform_site b ON  a.id_form = b.id AND a.cve_type = b.cve_type WHERE b.status NOT IN ('CN', 'AR', 'PE')")
```


```python
df_load = df_load.toPandas()
```


```python
df_load.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cve_type</th>
      <th>id_form</th>
      <th>groups</th>
      <th>key_dad</th>
      <th>Elemento</th>
      <th>Activo</th>
      <th>Altura</th>
      <th>Altura_del_Rack</th>
      <th>Ancho</th>
      <th>Azimuth</th>
      <th>...</th>
      <th>cve_vendor</th>
      <th>geo_lon</th>
      <th>geo_lat</th>
      <th>geo_alt</th>
      <th>geo_acc</th>
      <th>orig_site_code</th>
      <th>orig_cve_vendor</th>
      <th>comments</th>
      <th>created_on</th>
      <th>updated_on</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupStruct-0:groupTwelement-4</td>
      <td>root</td>
      <td>RFA</td>
      <td>00493991</td>
      <td>32.500</td>
      <td></td>
      <td></td>
      <td>24.000</td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupStruct-0:groupTwelement-19</td>
      <td>root</td>
      <td>RFA</td>
      <td>00493990</td>
      <td>32.500</td>
      <td></td>
      <td></td>
      <td>139.000</td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupShelter-0:groupPowerdc-1</td>
      <td>root</td>
      <td>REC</td>
      <td>3G065697</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupShelter-0:groupSbbank-2:groupSbat...</td>
      <td>root</td>
      <td>Bateria</td>
      <td>No cuenta con activo fijó</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupStruct-0:groupTwelement-3</td>
      <td>root</td>
      <td>ODU</td>
      <td>3G091092</td>
      <td>26.200</td>
      <td></td>
      <td></td>
      <td>395.000</td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>5</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupShelter-0:groupSbbank-6:groupSbat...</td>
      <td>root</td>
      <td>Bateria</td>
      <td>No cuenta con activo fijó</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupShelter-0:groupSrack-0:groupIrack-9</td>
      <td>EQUIPO EN RACK-9</td>
      <td>CARD</td>
      <td>00629548</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>7</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupShelter-0:groupSbbank-4:groupSbat...</td>
      <td>root</td>
      <td>Bateria</td>
      <td>No cuenta con activo fijó</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>8</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupStruct-0:groupTwelement-15</td>
      <td>root</td>
      <td>RET</td>
      <td>No cuenta con activo fijo</td>
      <td>32.500</td>
      <td></td>
      <td></td>
      <td>139.000</td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupStruct-0</td>
      <td>Estructura-0</td>
      <td>Estructura</td>
      <td></td>
      <td>12.000</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
  </tbody>
</table>
<p>10 rows × 75 columns</p>
</div>



Para las fuentes de los ODK's nos interesa conocer todos los elementos en sitio, por lo que haremos una limpieza en los campos que contengan características de los mismos.

En la consulta anterior se obtiene la tabla columnar del ODK 99 haciendo un JOIN con la tabla raw_panda_eform_site para obtener el estatus en el que se encuentra cada id_form.

### Una muestra del ODK 32:


```python
df=df_load.copy()
df.head(5)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cve_type</th>
      <th>id_form</th>
      <th>groups</th>
      <th>key_dad</th>
      <th>Elemento</th>
      <th>Activo</th>
      <th>Altura</th>
      <th>Altura_del_Rack</th>
      <th>Ancho</th>
      <th>Azimuth</th>
      <th>...</th>
      <th>cve_vendor</th>
      <th>geo_lon</th>
      <th>geo_lat</th>
      <th>geo_alt</th>
      <th>geo_acc</th>
      <th>orig_site_code</th>
      <th>orig_cve_vendor</th>
      <th>comments</th>
      <th>created_on</th>
      <th>updated_on</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupStruct-0:groupTwelement-4</td>
      <td>root</td>
      <td>RFA</td>
      <td>00493991</td>
      <td>32.500</td>
      <td></td>
      <td></td>
      <td>24.000</td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupStruct-0:groupTwelement-19</td>
      <td>root</td>
      <td>RFA</td>
      <td>00493990</td>
      <td>32.500</td>
      <td></td>
      <td></td>
      <td>139.000</td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupShelter-0:groupPowerdc-1</td>
      <td>root</td>
      <td>REC</td>
      <td>3G065697</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupShelter-0:groupSbbank-2:groupSbat...</td>
      <td>root</td>
      <td>Bateria</td>
      <td>No cuenta con activo fijó</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SINV</td>
      <td>184242</td>
      <td>id:root:groupStruct-0:groupTwelement-3</td>
      <td>root</td>
      <td>ODU</td>
      <td>3G091092</td>
      <td>26.200</td>
      <td></td>
      <td></td>
      <td>395.000</td>
      <td>...</td>
      <td>HWI</td>
      <td>-99.143916</td>
      <td>19.424428</td>
      <td>2256.0</td>
      <td>14.0</td>
      <td>ATT-HMEX0566</td>
      <td>HWI</td>
      <td>Torre en buen estado</td>
      <td>2019-09-18 16:43:47.243</td>
      <td>2019-09-18 16:55:22.227</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 75 columns</p>
</div>



### 2. Descripción de las fuentes.
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
print 'renglones = ',df.shape[0],' columnas = ',df.shape[1]
```

    renglones =  60514  columnas =  75


#### Breve descripción de los campos

El dataframe que se estará usando para la presentación del EDA, esta conformado por la unión de dos tablas, la fuente principal ```rci_network_db.tx_stg_tabla_columnar_odk_99``` de la cual se obtienen las siguientes columnas:

**clave_form**: Clave de identificación del ODK.  
**id_form**: Número de formulario.  
**form_element**: Jerarquía del registro.  
**key_dad**: Grupo padre al que pertenece el registro.  
**Elemento**: Tipo de elemento al que pertenece el registro.  
**filedate**: Fecha de la partición que se esta utilizando.  
**year**: Año de la partición que se esta utilizando.  
**month**: Mes de la partición que se esta utilizando.  
**day**: Día de la partición que se esta utilizando.  
**meta_date_marked_as_complete**: Fecha en la que se completo el odk.  
**Activo**: Número de activo fijo (manual o escaner).  
**Altura**: Altura de la torre.  
**Altura_del_Rack**: Altura del rack.  
**Ancho**: Ancho de la torre.  
**Azimuth**: Medida azimuth.  
**Bancos_de_baterias**: Cantidad de los bancos de baterias que existen.  
**Capacidad**: *Por definir*.  
**Codigo_de_Sitio**: Código de sitio donde se realiza el leventamiento del odk.  
**Elabora_Reporte**: Nombre de la persona que elaboro el formulario.  
**Enviar_acuse_a**: Correo electrónico de la persona que recibe el formulario.  
**Equipos_Adicionales?**: *Por definir*.  
**Firma**: Imagen de la firma de la persona que lleno el formulario.  
**Gabinetes_en_Sitio**: Cantidad de gabinetes en el sitio.  
**Generadores_en_Sitio**: Afirmación o Negación sobre si hay o no generadores en sitio.  
**Largo**: Largo de la torre.  
**Marca**: Marca del elemento de red.  
**Modelo**: Modelo del elemento de red.  
**Nombre_del_Proveedor**: Proveedor en el sitio.  
**Pierna_de_la_Torre**: *Por definir*.  
**Proyecto**: Proyecto al que pertenece el formulario.  
**Racks**: Cantida de racks en sitio.  
**Sector**: Sector del sitio al que se hace inventario.  
**Serie**: Número de serie (manual o escaner).  
**Shelters_en_Sitio**: Número de shelters en sitio.  
**Status**: Estatus físico en el que se encuentra el elemento de red.  
**TS_Finalizacion**: Fecha en la que se finalizo el formulario.  
**Tipo_Cerradura**: Tipo de cerradura.  
**Tipo_Equipo**: Tipo de equipo al que se le hace inventario.  
**Tipo_Shelter**: Tipo de shelter en sitio.  
**Tipo_de_Base**: Tipo de base.  
**Tipo_de_Cerradura**: Tipo de cerradura.  
**Tipo_de_Contenedores**: Tipo de contenedores.  
**Tipo_de_Instalacion**: Tipo de instalacipon.  
**Tipo_de_Pierna**: Tipo de pierna.  
**Tipo_de_Proteccion**: Tipo de protección.  
**Tipo_de_Soporte**: Tipo de soporte.  
**Tipo_de_estructura**: Tipo de estructura del sitio.  
**Tipo_de_inventario**: Tipo de Inventario.  
**Tipo_elemento**: Tipo de elemento de red.  
**Ubicacion**: *Por definir*.  
**Unidades_de_Rack**: *Por definir*.  
**Uso_de_Gabinete**: *Por definir*.  
**Vista_Activo_Fijo**: Imagen.  
**Vista_Banco_Baterias**:  Imagen.  
**Vista_Etiqueta_SN**: Imagen.  
**Vista_Frontal_del_Rack**: Imagen.  
**Vista_Gabinete_Frontal**: Imagen.  
**Vista_Gabinete_Trasera**: Imagen.  
**Vista_Numero_Serie**: Imagen.  
**Vista_Shelter_Frontal**: Imagen.  
**Vista_Shelter_Pasamuros_exterior**: Imagen.  
**Vista_Trasera_del_Rack**: Imagen.  
**Vista__de_la_estructura**: Imagen.  
**Vista_de_espacio_banco_de_baterias**: Imagen.  
**Vista_del_elemento**: Imagen.  
**torres_o_estructuras**: *Por definir*.  

La segunda fuente es el catálogo ```inventario.raw_panda_eform_site```, el cual contiene el status de los formularios, códigos de sitios, logitud, latitud y fechas importantes para el análisis.  
De esta fuente se tomán las siguientes columnas:

**status_id**: Estatus en el que se encuentra el formulario.  
**meta_started**: La fecha en la que se abrio el formulario para ser llenado.  
**meta_finished**: La fecha en la que se termino de llenar el formulario.  
**meta_device_id**: *Por definir*.  
**meta_user**: *Por definir*.  
**id_site**: Id del sitio.  
**cve_vendor**: Clave del proveedor.  
**geo_lon**: Longitud (coordenada del sitio).  
**geo_lat**: Latitud (coordenada del sitio). 
**geo_alt**: *Por definir*.  
**geo_acc**: *Por definir*.  
**orig_site_code**: Código de sitio.  
**orig_cve_vendor**: Clave del proveedor.  
**comments**: Comentarios informativos sobre el odk o el estatus.  
**created_on**: Fecha de creación del formulario.  
**updated_on**: Fecha de actualización del formulario. 

Esta segunda fuente es importante ya que nos dice en que estatus se encuentra el odk y los mantiene actualizados.

### 3. Exploración de los datos.

Entraremos en mas profundidad a los datos que existen en el odk 99 y se realizarán limpiezas si los datos así lo requieren.

Las claves que contiene la tabla del odk 99 son:


```python
claves = pd.unique(df['cve_type']).tolist()
claves
```




    [u'SINV']



**SINV**: Inventario de Sitio (DG)  
**SINR**:  Inventario de Sitio RAN

Conteo por clave form:


```python
conteo = pandasql.sqldf("SELECT COUNT(*) as conteo, cve_type from df GROUP BY cve_type;", locals())
conteo
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>conteo</th>
      <th>cve_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>60514</td>
      <td>SINV</td>
    </tr>
  </tbody>
</table>
</div>



A continuación, se muestra una lista de todos los elementos en sitio que se identificaron durante la adquisición:


```python
elementos = pd.unique(df['Elemento']).tolist()
elementos
```




    [u'RFA',
     u'REC',
     u'Bateria',
     u'ODU',
     u'CARD',
     u'RET',
     u'Estructura',
     u'root',
     u'IDU',
     u'RRU',
     u'Rack',
     u'POWP',
     u'OTH',
     u'Banco de baterias',
     u'shelter',
     u'MWC',
     u'BBU',
     u'ACE',
     u'PD',
     u'SWI',
     u'Gabinete',
     u'MWA',
     u'GEN',
     u'P3',
     u'PDI',
     u'ROU',
     u'DES',
     u'ACS',
     u'BOARD',
     u'LIGH',
     u'TRAN']



Algunos elementos son claramente identificables como: *Gabinete* o *Bateria* y otros están representados por una abreviatura de 3 o mas letras.

A continuación se muestra la frecuencia de los elementos que existen:


```python
Freq_Elementos=pd.DataFrame(df.Elemento.value_counts())
Freq_Elementos
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Elemento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Gabinete</th>
      <td>16058</td>
    </tr>
    <tr>
      <th>Bateria</th>
      <td>8925</td>
    </tr>
    <tr>
      <th>Banco de baterias</th>
      <td>6072</td>
    </tr>
    <tr>
      <th>CARD</th>
      <td>5828</td>
    </tr>
    <tr>
      <th>RRU</th>
      <td>4887</td>
    </tr>
    <tr>
      <th>RFA</th>
      <td>3213</td>
    </tr>
    <tr>
      <th>RET</th>
      <td>3183</td>
    </tr>
    <tr>
      <th>OTH</th>
      <td>2694</td>
    </tr>
    <tr>
      <th>ODU</th>
      <td>1925</td>
    </tr>
    <tr>
      <th>REC</th>
      <td>1104</td>
    </tr>
    <tr>
      <th>MWC</th>
      <td>976</td>
    </tr>
    <tr>
      <th>MWA</th>
      <td>919</td>
    </tr>
    <tr>
      <th>Estructura</th>
      <td>672</td>
    </tr>
    <tr>
      <th>Rack</th>
      <td>611</td>
    </tr>
    <tr>
      <th>root</th>
      <td>609</td>
    </tr>
    <tr>
      <th>PDI</th>
      <td>538</td>
    </tr>
    <tr>
      <th>ACE</th>
      <td>411</td>
    </tr>
    <tr>
      <th>BBU</th>
      <td>368</td>
    </tr>
    <tr>
      <th>PD</th>
      <td>294</td>
    </tr>
    <tr>
      <th>POWP</th>
      <td>235</td>
    </tr>
    <tr>
      <th>shelter</th>
      <td>212</td>
    </tr>
    <tr>
      <th>IDU</th>
      <td>202</td>
    </tr>
    <tr>
      <th>P3</th>
      <td>163</td>
    </tr>
    <tr>
      <th>SWI</th>
      <td>119</td>
    </tr>
    <tr>
      <th>ROU</th>
      <td>96</td>
    </tr>
    <tr>
      <th>BOARD</th>
      <td>63</td>
    </tr>
    <tr>
      <th>ACS</th>
      <td>45</td>
    </tr>
    <tr>
      <th>DES</th>
      <td>39</td>
    </tr>
    <tr>
      <th>GEN</th>
      <td>35</td>
    </tr>
    <tr>
      <th>LIGH</th>
      <td>17</td>
    </tr>
    <tr>
      <th>TRAN</th>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
Freq_Elementos[:25].plot(kind='bar',figsize=(10,6),rot=90,colormap='jet')

plt.title('Histograma de los elementos del ODK')
plt.ylabel('Frequencia del elemento')
plt.xlabel('Elementos')
```




    Text(0.5,0,'Elementos')




![Freq_Elementos](images/freq_elementos.png)


Podemos observar que el elemento Gabinete es el elemento que se encuentra mas frecuente en el inventario.

Obtenemos también la distribución de estatus de los distintos formularios.


```python
Freq_status=pd.DataFrame((df.status_id.value_counts()/df.status_id.value_counts().sum())*100)
Freq_status.plot(kind='bar',grid=True,figsize=(9,6),colormap='jet')
plt.title(u'Distribución de status por id_form')
plt.ylabel(u'Frecuencia')
plt.xlabel(u'Status')

Freq_status
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>status_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>AC</th>
      <td>86.399841</td>
    </tr>
    <tr>
      <th>OR</th>
      <td>7.226427</td>
    </tr>
    <tr>
      <th>RJ</th>
      <td>5.696203</td>
    </tr>
    <tr>
      <th>RE</th>
      <td>0.677529</td>
    </tr>
  </tbody>
</table>
</div>




![Freq_Status](images/freq_status.png)


El estatus en el que se encuentra el 85% de los formularios es aceptado.

Antes de realizar la limpieza, se separaran las columnas serie y activo para el calculo de indicadores. Esto se requiere hacer debido a la forma en la que se adquirieron los datos, los espacios en blanco no representan activos no trazables, estos registros están vacíos porque en donde hay datos es en otra columna de dataframe. A este dataframe también se le hará la limpieza igual que al dataframe general.


```python
df_kpi = df[['Serie','Activo']]
df_kpi.head(5)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Serie</th>
      <th>Activo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>15CN102650712</td>
      <td>00493991</td>
    </tr>
    <tr>
      <th>1</th>
      <td>15CN102650716</td>
      <td>00493990</td>
    </tr>
    <tr>
      <th>2</th>
      <td>011101217671R483200C10</td>
      <td>3G065697</td>
    </tr>
    <tr>
      <th>3</th>
      <td>No cuenta con número de serie</td>
      <td>No cuenta con activo fijó</td>
    </tr>
    <tr>
      <th>4</th>
      <td>215241248910BB000512</td>
      <td>3G091092</td>
    </tr>
  </tbody>
</table>
</div>



Siguiendo con la exploración de los datos, tenemos el campo de **serie** y **activo**, a continuación una muestra:


```python
df.Serie.head(20).tolist()
```




    [u'15CN102650712',
     u'15CN102650716',
     u'011101217671R483200C10',
     u'No cuenta con n\xfamero de serie',
     u'215241248910BB000512',
     u'No cuenta con n\xfamero de serie',
     u'2102319897D0F6022730',
     u'No cuenta con n\xfamero de serie',
     u'CN10152914848',
     u'',
     u'022HEM6TFB603244',
     u'',
     u'CN10152914837',
     u'No cuenta con n\xfamero de serie',
     u'No cuenta con n\xfamero de serie',
     u'21021132546TB7907691',
     u'No cuenta con n\xfamero de serie',
     u'210305488510DB005367',
     u'2102310SFMBTF7015327',
     u'No cuenta con n\xfamero de serie']




```python
df.Activo.head(20).tolist()
```




    [u'00493991',
     u'00493990',
     u'3G065697',
     u'No cuenta con activo fij\xf3',
     u'3G091092',
     u'No cuenta con activo fij\xf3',
     u'00629548',
     u'No cuenta con activo fij\xf3',
     u'No cuenta con activo fijo',
     u'',
     u'No cuenta con activo fij\xf3',
     u'',
     u'No cuenta con activo fijo',
     u'No cuenta con activo fij\xf3',
     u'No cuenta con activo fij\xf3',
     u'3G091109',
     u'No cuenta con activo fij\xf3',
     u'00699895',
     u'No cuenta con activo fij\xf3',
     u'No cuenta con activo fij\xf3']



Como se puede ver, hay números de serie y activo con datos como *NO VISIBLE* o *Sin etiqueta*, estos datos requieren limpieza para su manipulación, se hará a continuación:

#### Limpieza para homologar los campos de serie y activo:

Se homologan las letras a mayúsculas, se eliminan espacios en blanco (en caso de que haya después o antes de un número de serie o activo), se reemplazan acentos y se cambian espacios en blanco por la palabara *null*.


```python
df.Serie = df.Serie.str.lower()
df.Serie = df.Serie.str.strip()
df.Serie.replace(u'á',u'a',regex=True,inplace=True)
df.Serie.replace(u'é',u'e',regex=True,inplace=True)
df.Serie.replace(u'í',u'i',regex=True,inplace=True)
df.Serie.replace(u'ó',u'o',regex=True,inplace=True)
df.Serie.replace(u'ú',u'u',regex=True,inplace=True)
```


```python
df.Activo = df.Activo.str.lower()
df.Activo = df.Activo.str.strip()
df.Activo.replace(u'á',u'a',regex=True,inplace=True)
df.Activo.replace(u'é',u'e',regex=True,inplace=True)
df.Activo.replace(u'í',u'i',regex=True,inplace=True)
df.Activo.replace(u'ó',u'o',regex=True,inplace=True)
df.Activo.replace(u'ú',u'u',regex=True,inplace=True)
```


```python
df_kpi.Serie = df_kpi.Serie.str.lower()
df_kpi.Serie = df_kpi.Serie.str.strip()
df_kpi.Serie.replace(u'á',u'a',regex=True,inplace=True)
df_kpi.Serie.replace(u'é',u'e',regex=True,inplace=True)
df_kpi.Serie.replace(u'í',u'i',regex=True,inplace=True)
df_kpi.Serie.replace(u'ó',u'o',regex=True,inplace=True)
df_kpi.Serie.replace(u'ú',u'u',regex=True,inplace=True)
```


```python
df_kpi.Activo = df_kpi.Activo.str.lower()
df_kpi.Activo = df_kpi.Activo.str.strip()
df_kpi.Activo.replace(u'á',u'a',regex=True,inplace=True)
df_kpi.Activo.replace(u'é',u'e',regex=True,inplace=True)
df_kpi.Activo.replace(u'í',u'i',regex=True,inplace=True)
df_kpi.Activo.replace(u'ó',u'o',regex=True,inplace=True)
df_kpi.Activo.replace(u'ú',u'u',regex=True,inplace=True)
```

De el dataframe **df_kpi** solamente traeremos los registros donde la longitud de la serie o la longitud de el activo sea mayor a 0, esto descarta los registros vacíos que no representan ningún elemento.


```python
df_kpi_aux = pandasql.sqldf("SELECT * from df_kpi WHERE length(serie) > 0 OR length(activo) > 0;", locals())
df_kpi_aux.head(5)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Serie</th>
      <th>Activo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>15cn102650712</td>
      <td>00493991</td>
    </tr>
    <tr>
      <th>1</th>
      <td>15cn102650716</td>
      <td>00493990</td>
    </tr>
    <tr>
      <th>2</th>
      <td>011101217671r483200c10</td>
      <td>3g065697</td>
    </tr>
    <tr>
      <th>3</th>
      <td>no cuenta con numero de serie</td>
      <td>no cuenta con activo fijo</td>
    </tr>
    <tr>
      <th>4</th>
      <td>215241248910bb000512</td>
      <td>3g091092</td>
    </tr>
  </tbody>
</table>
</div>



#### Hacemos más limpieza para poder eliminar basura.
Esta limpieza se sigue tomando del catálogo que se encuentra en Hive *regex_cat_cleanup* y adicional, se aregan a la lista campos que salieron de acuerdo al análisis.


```python
dirt=['no visible', 'sin etiqueta', 'ni visible', 'n/v','nv','ilegible','n/a', 's/a', 'na','no legible', 'no cuenta con activo fijo',
      'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene','no visble',
      'no viaible', '.fhy', 'bxfj', 'cambiar la foto', 'hdjdjjdjfjfj', 'hdjrnnfjfjf', 'hffhthjih', 'hhyhigch',
      'hswkwjj', 'no aplica', 'no pude borrar elemnto', 'ns no visible', 'sin serie', 'sitio ibs no aplica', 'tutj',
      'uflp serie no visible', 'xxxxxxx', 'hsid# djdncg', 'sin informacion disponible', 'no tiene numero de serie',
      'hdkoe kg udkke' 'no se ve', 'ninguna', 'no tiene etiqueta y no se alcnaza a ver.', 'fue un error',
      'no legible', 'sin etiqueta', 'no disponible', 'no tiene', 'sin datos', 'num de serie no legible', 'etiqueta no legible', 'no cuenta con numero de serie',
      'no aplica por error se selecciona una tarjeta mas', 'enviado ya en reporte anterior', 'hlk', 'ninguno', 'la antena no tiene etiqueta por lo tanto tampoco numero de serie', 'no leguible',
      'sin targeta (por equivocacion se agrego este eslot 18 )', 'no cuenta con numeros de serie', 'enviados en reporte anterior .', 'sin etiqueta de numero de serie',
      'sin numero', 'sin informacion disponible', 'sin acceso a la antena', 'no tiene serie', 'sin acceso', 'no se pudo sacar ya que esta clausurado el sitio',
      'no se hizo por que no tenemos tarjeta se las llevo el ing de huawei gabriel lopez', 'sin informacion disponible', 'no aplica ta este segmento',
      'sin numero de serie visible', 'enviada en reporte  anterior', 'no hay antena', 'no se pudo sacar ya que esta clausurado y nos sacaron de sitio',
      'sin serie falta etiqueta', 'sin numero de serie no cuenta con la etiqueta', 'no tiene etiqueta', 'no existe', 'no serie visible', 'no hay bbu esta en resguardo por el ing gabriel lopez',
      'no legible', 'na', 'na hay  tarjeta', 'sin acceso al numero de serie', 'no visibles', 'uelp serie no visible', 'sin informacion disponible', 'sin tarjeta', 'fue un error de dedo no ay mas slot',
      'codigo no visible', 'num de serie no visible', 'sin informacion', 'no se aprecia el codigo', 'sin numero de serie', 'no trae la etiketa de numero de serie',
      'no aplica.', 'no se pudo sacar el numero  de serie ya q nos sacaron del sitio ya q esta clausurado', 'no tiene serie visible', 'no tiene serial ala vista',
      'no se tiene acceso a la antena', 'etiqueta no visible', 'no se puede tomar la foto porque tenemos la fan', 'n/a  no se instalan antenas', 'no aplica sitio ibs',
      'sin numero', 'kcuvicuv', 'error no hay mas', 'no se puede apreciar el codigo', 'no aplica es ibs.', 'no  cuenta con etiquetas de n/s', 'esta ultima no vale',
      'no hay tarjeta', 'esta no vale', 'falta']
```


```python
df.Serie.replace(dirt,np.NaN,regex=True,inplace=True)
```


```python
df.Activo.replace(dirt,np.NaN,regex=True,inplace=True)
```


```python
df_kpi_aux.replace(dirt,"NULL",regex=True,inplace=True)
```

Después de la limpieza, se pueden observar los campos de Serie y Activos limpios:


```python
df.Serie.head(20)
```




    0              15cn102650712
    1              15cn102650716
    2     011101217671r483200c10
    3                        NaN
    4       215241248910bb000512
    5                        NaN
    6       2102319897d0f6022730
    7                        NaN
    8              cn10152914848
    9                           
    10          022hem6tfb603244
    11                          
    12             cn10152914837
    13                       NaN
    14                       NaN
    15      21021132546tb7907691
    16                       NaN
    17      210305488510db005367
    18      2102310sfmbtf7015327
    19                       NaN
    Name: Serie, dtype: object




```python
df.Activo.head(20)
```




    0     00493991
    1     00493990
    2     3g065697
    3          NaN
    4     3g091092
    5          NaN
    6     00629548
    7          NaN
    8          NaN
    9             
    10         NaN
    11            
    12         NaN
    13         NaN
    14         NaN
    15    3g091109
    16         NaN
    17    00699895
    18         NaN
    19         NaN
    Name: Activo, dtype: object




```python
df_kpi_aux.head(20)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Serie</th>
      <th>Activo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>15cn102650712</td>
      <td>00493991</td>
    </tr>
    <tr>
      <th>1</th>
      <td>15cn102650716</td>
      <td>00493990</td>
    </tr>
    <tr>
      <th>2</th>
      <td>011101217671r483200c10</td>
      <td>3g065697</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>4</th>
      <td>215241248910bb000512</td>
      <td>3g091092</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2102319897d0f6022730</td>
      <td>00629548</td>
    </tr>
    <tr>
      <th>7</th>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>8</th>
      <td>cn10152914848</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>9</th>
      <td>022hem6tfb603244</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>10</th>
      <td>cn10152914837</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>11</th>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>12</th>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>13</th>
      <td>21021132546tb7907691</td>
      <td>3g091109</td>
    </tr>
    <tr>
      <th>14</th>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>15</th>
      <td>210305488510db005367</td>
      <td>00699895</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2102310sfmbtf7015327</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>17</th>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>18</th>
      <td>cn10153546548</td>
      <td>NULL</td>
    </tr>
    <tr>
      <th>19</th>
      <td>21023198974mb5038386</td>
      <td>NULL</td>
    </tr>
  </tbody>
</table>
</div>



Además de la limpieza en los campos principales que nos ayudarán con la trazabilidad de los elementos de red, podemos encontrar catálogos dentro del ODK 99, a continuación se muestra la limpieza de los campos para los catálogos que se mostrarán en el apartado **5. Catálogos**:

### Limpieza Campo Marca


```python
df_marca = pandasql.sqldf("SELECT DISTINCT upper(trim(marca)) as marca FROM df WHERE marca not like '%|%' AND length(marca) != 0 AND marca != 'OTH';", locals())
df_marca.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marca</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CMAN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>COMMS</td>
    </tr>
    <tr>
      <th>2</th>
      <td>EMRSN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>HWI</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MEI</td>
    </tr>
    <tr>
      <th>5</th>
      <td>CISCO</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NEC</td>
    </tr>
    <tr>
      <th>7</th>
      <td>STAHLIN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>HUAWEI</td>
    </tr>
    <tr>
      <th>9</th>
      <td>HUEB</td>
    </tr>
  </tbody>
</table>
</div>



Retiramos del catálogo los siguientes registros que no son una marca


```python
limpieza_marca = pandasql.sqldf("SELECT DISTINCT marca FROM df_marca WHERE lower(marca) like 'no %' OR lower(marca) like 'sin %';", locals())
limpieza_marca
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marca</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NO VISIBLE</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NO TIENE</td>
    </tr>
  </tbody>
</table>
</div>




```python
dirt = [limpieza_marca]
df_marca.replace(dirt,'',regex=True,inplace=True)
```

Para obtener el nombre de la marca, cargamos la tabla ```inventario.raw_panda_vendor```


```python
df_vendor = spark.sql("SELECT DISTINCT upper(trim(cve_vendor)) cve_vendor, vendor_name FROM inventario.raw_panda_vendor").cache().toPandas()
df_vendor.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cve_vendor</th>
      <th>vendor_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MIDIT</td>
      <td>Miditel</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WNSM</td>
      <td>WNSMEXICO SA DE CV</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AGLNT</td>
      <td>Agilent Technologies</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ATM</td>
      <td>Atelcom</td>
    </tr>
    <tr>
      <th>4</th>
      <td>COMDE</td>
      <td>Comde</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ATELI</td>
      <td>ATELIER K&amp;V</td>
    </tr>
    <tr>
      <th>6</th>
      <td>GZ-N</td>
      <td>Guzman-Nasich</td>
    </tr>
    <tr>
      <th>7</th>
      <td>INSMX</td>
      <td>Instalación Maxima en Tecnologia</td>
    </tr>
    <tr>
      <th>8</th>
      <td>TXSRG</td>
      <td>Telextorage SA</td>
    </tr>
    <tr>
      <th>9</th>
      <td>PCI01</td>
      <td>Prefabricados y Construcciones Industriales S.A</td>
    </tr>
  </tbody>
</table>
</div>



Se hace la unión a la tabla ```inventario.raw_panda_vendor``` usando cve_vendor y marca


```python
cat_marca = pandasql.sqldf("SELECT marca, CASE WHEN vendor_name IS NULL THEN 'Por Definir' ELSE vendor_name END 'descripcion_marca' FROM (SELECT marca, vendor_name FROM df_marca LEFT JOIN df_vendor ON marca = cve_vendor WHERE marca != '')a", locals())
cat_marca.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marca</th>
      <th>descripcion_marca</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CMAN</td>
      <td>Andrew</td>
    </tr>
    <tr>
      <th>1</th>
      <td>COMMS</td>
      <td>Commscope</td>
    </tr>
    <tr>
      <th>2</th>
      <td>EMRSN</td>
      <td>Emerson</td>
    </tr>
    <tr>
      <th>3</th>
      <td>HWI</td>
      <td>Huawei</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MEI</td>
      <td>MEXICANA DE ELECTRONICA INDUSTRIAL SA DE CV</td>
    </tr>
    <tr>
      <th>5</th>
      <td>CISCO</td>
      <td>Cisco</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NEC</td>
      <td>Nec Mexico</td>
    </tr>
    <tr>
      <th>7</th>
      <td>STAHLIN</td>
      <td>Por Definir</td>
    </tr>
    <tr>
      <th>8</th>
      <td>HUAWEI</td>
      <td>Por Definir</td>
    </tr>
    <tr>
      <th>9</th>
      <td>HUEB</td>
      <td>HUEBBELL</td>
    </tr>
  </tbody>
</table>
</div>



### Limpieza catálogo Elemento - Marca - Modelo


```python
df_modelo_marca = pandasql.sqldf("SELECT DISTINCT lower(trim(elemento)) as elemento, upper(trim(marca)) as marca, upper(trim(modelo)) as modelo FROM df WHERE modelo not like '%|%' AND length(modelo) != 0 AND modelo != 'OTH' AND marca not like '%|%' AND length(marca) != 0 AND marca != 'OTH';", locals())
df_modelo_marca.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>elemento</th>
      <th>marca</th>
      <th>modelo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>rfa</td>
      <td>CMAN</td>
      <td>DBXLH-6565EC-A2M</td>
    </tr>
    <tr>
      <th>1</th>
      <td>rfa</td>
      <td>COMMS</td>
      <td>DBXLH-6565EC-A2M</td>
    </tr>
    <tr>
      <th>2</th>
      <td>rec</td>
      <td>EMRSN</td>
      <td>R48-3200</td>
    </tr>
    <tr>
      <th>3</th>
      <td>odu</td>
      <td>HWI</td>
      <td>XMC 23G-2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>card</td>
      <td>HWI</td>
      <td>UPEUC</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ret</td>
      <td>COMMS</td>
      <td>ATM2OO-A20</td>
    </tr>
    <tr>
      <th>6</th>
      <td>card</td>
      <td>HWI</td>
      <td>UBBPD6</td>
    </tr>
    <tr>
      <th>7</th>
      <td>card</td>
      <td>HWI</td>
      <td>PIU</td>
    </tr>
    <tr>
      <th>8</th>
      <td>idu</td>
      <td>HWI</td>
      <td>RTN 910</td>
    </tr>
    <tr>
      <th>9</th>
      <td>card</td>
      <td>HWI</td>
      <td>UMPTB1</td>
    </tr>
  </tbody>
</table>
</div>



Retiramos del catálogo los siguientes registros que no son un modelo o una marca


```python
limpieza_modelo = pandasql.sqldf("SELECT DISTINCT modelo FROM df_modelo_marca WHERE lower(modelo) like 'no %' OR lower(modelo) like 'sin %';", locals())
limpieza_marca = pandasql.sqldf("SELECT DISTINCT marca FROM df_modelo_marca WHERE lower(marca) like 'no %' OR lower(marca) like 'sin %';", locals())
```


```python
dirt = [limpieza_modelo, limpieza_marca]
df_modelo_marca.replace(dirt,'',regex=True,inplace=True)
```

Para el catálogo modelo no se cuenta con alguna tabla previa, así que los registros únicos que se tienen en el campo modelo formarán parte del catálogo:


```python
cat_modelo_marca = pandasql.sqldf("SELECT * FROM df_modelo_marca WHERE modelo != '' AND marca != ''", locals())
cat_modelo_marca.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>elemento</th>
      <th>marca</th>
      <th>modelo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>rfa</td>
      <td>CMAN</td>
      <td>DBXLH-6565EC-A2M</td>
    </tr>
    <tr>
      <th>1</th>
      <td>rfa</td>
      <td>COMMS</td>
      <td>DBXLH-6565EC-A2M</td>
    </tr>
    <tr>
      <th>2</th>
      <td>rec</td>
      <td>EMRSN</td>
      <td>R48-3200</td>
    </tr>
    <tr>
      <th>3</th>
      <td>odu</td>
      <td>HWI</td>
      <td>XMC 23G-2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>card</td>
      <td>HWI</td>
      <td>UPEUC</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ret</td>
      <td>COMMS</td>
      <td>ATM2OO-A20</td>
    </tr>
    <tr>
      <th>6</th>
      <td>card</td>
      <td>HWI</td>
      <td>UBBPD6</td>
    </tr>
    <tr>
      <th>7</th>
      <td>card</td>
      <td>HWI</td>
      <td>PIU</td>
    </tr>
    <tr>
      <th>8</th>
      <td>idu</td>
      <td>HWI</td>
      <td>RTN 910</td>
    </tr>
    <tr>
      <th>9</th>
      <td>card</td>
      <td>HWI</td>
      <td>UMPTB1</td>
    </tr>
  </tbody>
</table>
</div>



### Tipo de Elemento

El catálogo de tipo de elemento se conforma con los distintos que se tienen en dicho campo, sin contar el root el cual es un default que se le ponen a todos aquellos registros que lo tengan como padre directo.


```python
cat_elemento = pandasql.sqldf("SELECT DISTINCT UPPER(elemento) AS elemento FROM df WHERE elemento != 'root'", locals())
cat_elemento
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>elemento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>RFA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>REC</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BATERIA</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ODU</td>
    </tr>
    <tr>
      <th>4</th>
      <td>CARD</td>
    </tr>
    <tr>
      <th>5</th>
      <td>RET</td>
    </tr>
    <tr>
      <th>6</th>
      <td>ESTRUCTURA</td>
    </tr>
    <tr>
      <th>7</th>
      <td>IDU</td>
    </tr>
    <tr>
      <th>8</th>
      <td>RRU</td>
    </tr>
    <tr>
      <th>9</th>
      <td>RACK</td>
    </tr>
    <tr>
      <th>10</th>
      <td>POWP</td>
    </tr>
    <tr>
      <th>11</th>
      <td>OTH</td>
    </tr>
    <tr>
      <th>12</th>
      <td>BANCO DE BATERIAS</td>
    </tr>
    <tr>
      <th>13</th>
      <td>SHELTER</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MWC</td>
    </tr>
    <tr>
      <th>15</th>
      <td>BBU</td>
    </tr>
    <tr>
      <th>16</th>
      <td>ACE</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PD</td>
    </tr>
    <tr>
      <th>18</th>
      <td>SWI</td>
    </tr>
    <tr>
      <th>19</th>
      <td>GABINETE</td>
    </tr>
    <tr>
      <th>20</th>
      <td>MWA</td>
    </tr>
    <tr>
      <th>21</th>
      <td>GEN</td>
    </tr>
    <tr>
      <th>22</th>
      <td>P3</td>
    </tr>
    <tr>
      <th>23</th>
      <td>PDI</td>
    </tr>
    <tr>
      <th>24</th>
      <td>ROU</td>
    </tr>
    <tr>
      <th>25</th>
      <td>DES</td>
    </tr>
    <tr>
      <th>26</th>
      <td>ACS</td>
    </tr>
    <tr>
      <th>27</th>
      <td>BOARD</td>
    </tr>
    <tr>
      <th>28</th>
      <td>LIGH</td>
    </tr>
    <tr>
      <th>29</th>
      <td>TRAN</td>
    </tr>
  </tbody>
</table>
</div>



### Limpieza campo proyecto


```python
df_proyecto = pandasql.sqldf("SELECT DISTINCT UPPER(trim(proyecto)) as proyecto FROM df WHERE proyecto not like '%|%' AND length(proyecto) != 0 AND proyecto != 'OTH';", locals())
df_proyecto
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>proyecto</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>317E2E</td>
    </tr>
    <tr>
      <th>1</th>
      <td>DEPLOVR</td>
    </tr>
  </tbody>
</table>
</div>



Podemos observar que solo se tienen 28 proyectos y podemos identificar que los registros como **NO** y **HUAWEI** no son proyectos, así que estos junto con los que solamente tengan 1 número, no serán identificados como proyectos y se quitarán del catálogo.


```python
cat_proyecto = pandasql.sqldf("SELECT proyecto FROM df_proyecto WHERE length(trim(proyecto)) > 1 AND proyecto != 'NO' AND proyecto != 'HUAWEI';", locals())
cat_proyecto
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>proyecto</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>317E2E</td>
    </tr>
    <tr>
      <th>1</th>
      <td>DEPLOVR</td>
    </tr>
  </tbody>
</table>
</div>



### Coordenadas de sitio

Utilizando las coordenadas de latitud y longitud proporcionadas por el catálogo ```inventario.raw_panda_eform_site``` junto con el código de sitio, podemos obtener un mapa con la ubicación donde se ha llevado a cabo inventario perteneciente al odk 99.


```python
cat_ubicacion = pandasql.sqldf("SELECT DISTINCT orig_site_code as site_code, geo_lat as latitude, geo_lon as longitude FROM df;", locals())
cat_ubicacion
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>site_code</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ATT-HMEX0566</td>
      <td>19.424428</td>
      <td>-99.143916</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ATT-HMEX1060</td>
      <td>19.526274</td>
      <td>-99.145531</td>
    </tr>
    <tr>
      <th>2</th>
      <td>DIFMGH1194</td>
      <td>19.417597</td>
      <td>-99.200032</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ATT-HMEX0654</td>
      <td>19.561957</td>
      <td>-99.223175</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ATT-HMEX0654</td>
      <td>19.561896</td>
      <td>-99.223144</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ATT-MEX-9554</td>
      <td>19.391322</td>
      <td>-99.281997</td>
    </tr>
    <tr>
      <th>6</th>
      <td>MEXIXP1107</td>
      <td>19.322203</td>
      <td>-98.875723</td>
    </tr>
    <tr>
      <th>7</th>
      <td>MEX-9746</td>
      <td>19.318073</td>
      <td>-99.136943</td>
    </tr>
    <tr>
      <th>8</th>
      <td>ATT-HMEX1542</td>
      <td>19.382742</td>
      <td>-99.008296</td>
    </tr>
    <tr>
      <th>9</th>
      <td>ATT-JAL-5237</td>
      <td>20.699498</td>
      <td>-103.407303</td>
    </tr>
    <tr>
      <th>10</th>
      <td>MEX-9348</td>
      <td>19.311643</td>
      <td>-99.080715</td>
    </tr>
    <tr>
      <th>11</th>
      <td>ATT-HMEX0329</td>
      <td>19.372515</td>
      <td>-99.179588</td>
    </tr>
    <tr>
      <th>12</th>
      <td>ATT-HMEX8429</td>
      <td>19.318454</td>
      <td>-99.238140</td>
    </tr>
    <tr>
      <th>13</th>
      <td>ATT-MEX-9287</td>
      <td>19.414065</td>
      <td>-99.078079</td>
    </tr>
    <tr>
      <th>14</th>
      <td>ATT-MEX-91402</td>
      <td>19.589966</td>
      <td>-99.007761</td>
    </tr>
    <tr>
      <th>15</th>
      <td>ATT-JAL-5093</td>
      <td>20.675261</td>
      <td>-103.372582</td>
    </tr>
    <tr>
      <th>16</th>
      <td>ATT-MEX-9108</td>
      <td>19.430462</td>
      <td>-99.092025</td>
    </tr>
    <tr>
      <th>17</th>
      <td>ATT-MEX-195</td>
      <td>19.672113</td>
      <td>-99.234359</td>
    </tr>
    <tr>
      <th>18</th>
      <td>ATT-HMEX0560</td>
      <td>19.424502</td>
      <td>-99.195189</td>
    </tr>
    <tr>
      <th>19</th>
      <td>MEX-9388</td>
      <td>19.305139</td>
      <td>-99.210568</td>
    </tr>
    <tr>
      <th>20</th>
      <td>ATT-MEX-9539</td>
      <td>19.389721</td>
      <td>-99.291572</td>
    </tr>
    <tr>
      <th>21</th>
      <td>ATT-MEX-9917</td>
      <td>19.830153</td>
      <td>-98.900340</td>
    </tr>
    <tr>
      <th>22</th>
      <td>MEX-92129</td>
      <td>19.317491</td>
      <td>-99.249179</td>
    </tr>
    <tr>
      <th>23</th>
      <td>HID-9019</td>
      <td>19.846775</td>
      <td>-98.972079</td>
    </tr>
    <tr>
      <th>24</th>
      <td>ATT-HMEX1456</td>
      <td>19.432844</td>
      <td>-99.213313</td>
    </tr>
    <tr>
      <th>25</th>
      <td>HMEX0564</td>
      <td>19.556134</td>
      <td>-99.229430</td>
    </tr>
    <tr>
      <th>26</th>
      <td>ATT-HMEX1496</td>
      <td>19.606517</td>
      <td>-99.184405</td>
    </tr>
    <tr>
      <th>27</th>
      <td>DIFCUJ1090</td>
      <td>19.379440</td>
      <td>-99.285535</td>
    </tr>
    <tr>
      <th>28</th>
      <td>MEXTEO1235</td>
      <td>19.687805</td>
      <td>-98.826063</td>
    </tr>
    <tr>
      <th>29</th>
      <td>ATT-HGDL1029</td>
      <td>20.609883</td>
      <td>-103.402072</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>569</th>
      <td>ATT-JAL-5156</td>
      <td>20.558291</td>
      <td>-103.463600</td>
    </tr>
    <tr>
      <th>570</th>
      <td>ATT-HMEX1622</td>
      <td>19.310808</td>
      <td>-98.944254</td>
    </tr>
    <tr>
      <th>571</th>
      <td>ATT-MEX-91448</td>
      <td>19.459565</td>
      <td>-99.172328</td>
    </tr>
    <tr>
      <th>572</th>
      <td>ATT-JAL-5184</td>
      <td>20.721862</td>
      <td>-103.435365</td>
    </tr>
    <tr>
      <th>573</th>
      <td>ATT-DIFIZT1438</td>
      <td>19.325222</td>
      <td>-99.027577</td>
    </tr>
    <tr>
      <th>574</th>
      <td>ATT-JAL-5156</td>
      <td>20.558412</td>
      <td>-103.463591</td>
    </tr>
    <tr>
      <th>575</th>
      <td>ATT-DIFIZT1438</td>
      <td>19.325168</td>
      <td>-99.027578</td>
    </tr>
    <tr>
      <th>576</th>
      <td>ATT-HMEX1498</td>
      <td>19.522183</td>
      <td>-98.874667</td>
    </tr>
    <tr>
      <th>577</th>
      <td>ATT-MEXPAZ1588-LA TIA</td>
      <td>19.373647</td>
      <td>-98.922313</td>
    </tr>
    <tr>
      <th>578</th>
      <td>ATT-HMEX1430</td>
      <td>19.497523</td>
      <td>-98.928447</td>
    </tr>
    <tr>
      <th>579</th>
      <td>ATT-MEX-9547</td>
      <td>19.403243</td>
      <td>-99.269134</td>
    </tr>
    <tr>
      <th>580</th>
      <td>JALZAP2049</td>
      <td>20.718730</td>
      <td>-103.471341</td>
    </tr>
    <tr>
      <th>581</th>
      <td>ATT-MEX-91359</td>
      <td>19.613798</td>
      <td>-99.048576</td>
    </tr>
    <tr>
      <th>582</th>
      <td>ATT-MEX-9012</td>
      <td>19.599417</td>
      <td>-99.011400</td>
    </tr>
    <tr>
      <th>583</th>
      <td>MEXTEO1236</td>
      <td>19.667257</td>
      <td>-98.871169</td>
    </tr>
    <tr>
      <th>584</th>
      <td>ATT-HGDL0083</td>
      <td>20.699525</td>
      <td>-103.415480</td>
    </tr>
    <tr>
      <th>585</th>
      <td>MEX-435H</td>
      <td>19.437971</td>
      <td>-99.219980</td>
    </tr>
    <tr>
      <th>586</th>
      <td>DIFALO0964</td>
      <td>19.332882</td>
      <td>-99.275017</td>
    </tr>
    <tr>
      <th>587</th>
      <td>ATT-HMEX1047</td>
      <td>19.639208</td>
      <td>-99.002587</td>
    </tr>
    <tr>
      <th>588</th>
      <td>ATT-MEX-435</td>
      <td>19.438149</td>
      <td>-99.220257</td>
    </tr>
    <tr>
      <th>589</th>
      <td>ATT-HGDL1115</td>
      <td>20.494167</td>
      <td>-103.410154</td>
    </tr>
    <tr>
      <th>590</th>
      <td>MEX-9745</td>
      <td>19.272669</td>
      <td>-99.186644</td>
    </tr>
    <tr>
      <th>591</th>
      <td>ATT-MEX-9972</td>
      <td>19.325896</td>
      <td>-98.895281</td>
    </tr>
    <tr>
      <th>592</th>
      <td>MEX-9745</td>
      <td>19.272714</td>
      <td>-99.186600</td>
    </tr>
    <tr>
      <th>593</th>
      <td>DIFITZ1438</td>
      <td>19.325159</td>
      <td>-99.027607</td>
    </tr>
    <tr>
      <th>594</th>
      <td>DIFIZT1438</td>
      <td>19.325131</td>
      <td>-99.027488</td>
    </tr>
    <tr>
      <th>595</th>
      <td>ATT-MEX-9568</td>
      <td>19.440334</td>
      <td>-99.143815</td>
    </tr>
    <tr>
      <th>596</th>
      <td>ATT-MEX-9241</td>
      <td>19.430244</td>
      <td>-99.204754</td>
    </tr>
    <tr>
      <th>597</th>
      <td>ATT-MEX-9734</td>
      <td>19.489138</td>
      <td>-99.048552</td>
    </tr>
    <tr>
      <th>598</th>
      <td>DIFTLP0857</td>
      <td>19.304020</td>
      <td>-99.205252</td>
    </tr>
  </tbody>
</table>
<p>599 rows × 3 columns</p>
</div>



### 4. Calidad de los datos.

#### Missings Values

Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Para evitar traer columnas que no son relevantes para el calculo de KPIs o catálogos que probbablemente sean vistas, haremos una lista con las columnas de las cuales nos interesa saber su porcentaje, y acontinuación, calculamos el porcentaje de NA's que tiene la fuente por columna:


```python
#Limpieza de registros vacíos
df.replace('',np.NaN,inplace=True)
relevantes=['Activo', 'Serie', 'Bancos_de_baterias', 'Codigo_de_Sitio', 'Marca', 'Modelo',
               'Proyecto', 'Shelters_en_Sitio', 'meta_started', 'meta_finished']
```


```python
nas=df[relevantes].isna().sum()
porcentaje_nas=nas/df[relevantes].isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de NAs por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 10), ('counts_nas', 10)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="822bfad3-e1d8-47a2-80af-088c9846f273"></div>








<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Porcentaje de NAs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Activo</th>
      <td>55.132697</td>
    </tr>
    <tr>
      <th>Serie</th>
      <td>37.229401</td>
    </tr>
    <tr>
      <th>Bancos_de_baterias</th>
      <td>98.175629</td>
    </tr>
    <tr>
      <th>Codigo_de_Sitio</th>
      <td>99.514162</td>
    </tr>
    <tr>
      <th>Marca</th>
      <td>2.467198</td>
    </tr>
    <tr>
      <th>Modelo</th>
      <td>2.467198</td>
    </tr>
    <tr>
      <th>Proyecto</th>
      <td>98.993621</td>
    </tr>
    <tr>
      <th>Shelters_en_Sitio</th>
      <td>99.846317</td>
    </tr>
    <tr>
      <th>meta_started</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>meta_finished</th>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>



Debido a la estructura del odk y a la manipulación que se hizo previamente para obtener la estructura columnar, podemos ver que las columnas *Banco_de_baterias*, *Codigo_de_Sitio*, *Proyecto*, *Shelters_en_Sitio* y *TS_Finalización* que son columnas que dentro de los formularios aparecian de 1 a 2 veces máximo por id form, tienen mas entre 95% y 99% de valores null.

Podemos observar que columnas como **Activo**, **Serie**, **Marca** y **Modelo** cuentan con un porcentaje menor de campos nulos, lo cual nos interesa mucho ya que, el activo y la serie nos ayudan a sacar indicadores.

Se termina la limpieza de los valores *Nan* o *nulos* en los campos de serie y activo para el cálculo de indicadores.


```python
df.Serie=df.Serie.str.upper()
df.Activo=df.Activo.str.upper()
```


```python
df.fillna('NULL',inplace=True)
```

### 5. Catálogos.
Se enlistan los catálogos que surgieron de la exploración. 

#### Catálogo Elemento


```python
cat_elemento.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>elemento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>RFA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>REC</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BATERIA</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ODU</td>
    </tr>
    <tr>
      <th>4</th>
      <td>CARD</td>
    </tr>
    <tr>
      <th>5</th>
      <td>RET</td>
    </tr>
    <tr>
      <th>6</th>
      <td>ESTRUCTURA</td>
    </tr>
    <tr>
      <th>7</th>
      <td>IDU</td>
    </tr>
    <tr>
      <th>8</th>
      <td>RRU</td>
    </tr>
    <tr>
      <th>9</th>
      <td>RACK</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Marca


```python
cat_marca.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marca</th>
      <th>descripcion_marca</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CMAN</td>
      <td>Andrew</td>
    </tr>
    <tr>
      <th>1</th>
      <td>COMMS</td>
      <td>Commscope</td>
    </tr>
    <tr>
      <th>2</th>
      <td>EMRSN</td>
      <td>Emerson</td>
    </tr>
    <tr>
      <th>3</th>
      <td>HWI</td>
      <td>Huawei</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MEI</td>
      <td>MEXICANA DE ELECTRONICA INDUSTRIAL SA DE CV</td>
    </tr>
    <tr>
      <th>5</th>
      <td>CISCO</td>
      <td>Cisco</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NEC</td>
      <td>Nec Mexico</td>
    </tr>
    <tr>
      <th>7</th>
      <td>STAHLIN</td>
      <td>Por Definir</td>
    </tr>
    <tr>
      <th>8</th>
      <td>HUAWEI</td>
      <td>Por Definir</td>
    </tr>
    <tr>
      <th>9</th>
      <td>HUEB</td>
      <td>HUEBBELL</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Marca y Modelo del Elemento


```python
cat_modelo_marca.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>elemento</th>
      <th>marca</th>
      <th>modelo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>rfa</td>
      <td>CMAN</td>
      <td>DBXLH-6565EC-A2M</td>
    </tr>
    <tr>
      <th>1</th>
      <td>rfa</td>
      <td>COMMS</td>
      <td>DBXLH-6565EC-A2M</td>
    </tr>
    <tr>
      <th>2</th>
      <td>rec</td>
      <td>EMRSN</td>
      <td>R48-3200</td>
    </tr>
    <tr>
      <th>3</th>
      <td>odu</td>
      <td>HWI</td>
      <td>XMC 23G-2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>card</td>
      <td>HWI</td>
      <td>UPEUC</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ret</td>
      <td>COMMS</td>
      <td>ATM2OO-A20</td>
    </tr>
    <tr>
      <th>6</th>
      <td>card</td>
      <td>HWI</td>
      <td>UBBPD6</td>
    </tr>
    <tr>
      <th>7</th>
      <td>card</td>
      <td>HWI</td>
      <td>PIU</td>
    </tr>
    <tr>
      <th>8</th>
      <td>idu</td>
      <td>HWI</td>
      <td>RTN 910</td>
    </tr>
    <tr>
      <th>9</th>
      <td>card</td>
      <td>HWI</td>
      <td>UMPTB1</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Proyecto


```python
cat_proyecto.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>proyecto</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>317E2E</td>
    </tr>
    <tr>
      <th>1</th>
      <td>DEPLOVR</td>
    </tr>
  </tbody>
</table>
</div>



#### Ubicación


```python
cat_ubicacion.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>site_code</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ATT-HMEX0566</td>
      <td>19.424428</td>
      <td>-99.143916</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ATT-HMEX1060</td>
      <td>19.526274</td>
      <td>-99.145531</td>
    </tr>
    <tr>
      <th>2</th>
      <td>DIFMGH1194</td>
      <td>19.417597</td>
      <td>-99.200032</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ATT-HMEX0654</td>
      <td>19.561957</td>
      <td>-99.223175</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ATT-HMEX0654</td>
      <td>19.561896</td>
      <td>-99.223144</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ATT-MEX-9554</td>
      <td>19.391322</td>
      <td>-99.281997</td>
    </tr>
    <tr>
      <th>6</th>
      <td>MEXIXP1107</td>
      <td>19.322203</td>
      <td>-98.875723</td>
    </tr>
    <tr>
      <th>7</th>
      <td>MEX-9746</td>
      <td>19.318073</td>
      <td>-99.136943</td>
    </tr>
    <tr>
      <th>8</th>
      <td>ATT-HMEX1542</td>
      <td>19.382742</td>
      <td>-99.008296</td>
    </tr>
    <tr>
      <th>9</th>
      <td>ATT-JAL-5237</td>
      <td>20.699498</td>
      <td>-103.407303</td>
    </tr>
  </tbody>
</table>
</div>



### 6. Preparación de los datos.

A continuación se presentan las reglas que se siguieron para realizar la limpieza de los datos. 

#### Reglas utilizadas:
* Se eliminan todos los registros: ('no visible','n/v','nv','ilegible','n/a','na','no legible',
    'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene',  
    'No visble','no visble','No viaible', etc...).      
* Se pasa upper case todos los atributos (Las columnas **Serie** y **Activo**).
* Se eliminan espacios sobrantes.
* Se reeplazan los strings 'NA'.
* Se eliminan acentos y caracteres '/\'

### 7. Métricas KPI.
Se mostrarán los KPIs generados. 


```python
aux = df.copy()
```

#### Total de elementos


```python
Total_Elementos=df_kpi_aux.shape[0]
Total_Elementos
```




    52949



#### Total Elementos Trazables


```python
Total_Tr=df_kpi_aux.loc[(df_kpi_aux.Serie!='NULL') | (df_kpi_aux.Activo!='NULL')].shape[0]
Total_Tr
```




    43974



#### Total Elementos NO Trazables


```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    8975



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=df_kpi_aux[['Serie','Activo']].loc[(df_kpi_aux.Serie!='NULL') | (df_kpi_aux.Activo!='NULL')].drop_duplicates().shape[0]
Total_Tr_Unic
```




    39222



#### Total Elementos Trazables Duplicados


```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    4752



#### Total Elementos Trazables Únicos Con Serie Con Activo


```python
Total_Tr_Unic_CS_CA=df_kpi_aux[['Serie','Activo']].loc[(df_kpi_aux.Serie!='NULL') & (df_kpi_aux.Activo!='NULL')].drop_duplicates().shape[0]
Total_Tr_Unic_CS_CA
```




    22186



#### Total Elementos Trazables Únicos Con Serie Sin Activo


```python
Total_Tr_Unic_CS_SA=df_kpi_aux[['Serie','Activo']].loc[(df_kpi_aux.Serie!='NULL') & (df_kpi_aux.Activo=='NULL')].drop_duplicates().shape[0]
Total_Tr_Unic_CS_SA
```




    14220



#### Total Elementos Trazables Únicos Sin Serie Con Activo


```python
Total_Tr_Unic_SS_CA=df_kpi_aux[['Serie','Activo']].loc[(df_kpi_aux.Serie=='NULL') & (df_kpi_aux.Activo!='NULL')].drop_duplicates().shape[0]
Total_Tr_Unic_SS_CA
```




    2816




```python
KPIs=pd.DataFrame({'KPI':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados',
                          'Total CS CA','Total CS SA','Total SS CA'],
                  'Resultado':[Total_Elementos,Total_Tr,Total_NOTr,
                              Total_Tr_Unic,Total_Tr_Dupli,
                               Total_Tr_Unic_CS_CA,Total_Tr_Unic_CS_SA,
                              Total_Tr_Unic_SS_CA]})
KPIs
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>KPI</th>
      <th>Resultado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Total Elementos</td>
      <td>52949</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>43974</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>8975</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>39222</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>4752</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Total CS CA</td>
      <td>22186</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Total CS SA</td>
      <td>14220</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Total SS CA</td>
      <td>2816</td>
    </tr>
  </tbody>
</table>
</div>



Se guarda la tabla de eda y kpi


```python
mySchema = StructType([ StructField("cve_type", StringType(), True)\
                       ,StructField("id_form", StringType(), True)\
                       ,StructField("groups", StringType(), True)\
                       ,StructField("key_dad", StringType(), True)\
                       ,StructField("Elemento", StringType(), True)\
                       ,StructField("Activo", StringType(), True)\
                       ,StructField("Altura", StringType(), True)\
                       ,StructField("Altura_del_Rack", StringType(), True)\
                       ,StructField("Ancho", StringType(), True)\
                       ,StructField("Azimuth", StringType(), True)\
                       ,StructField("Bancos_de_baterias", StringType(), True)\
                       ,StructField("Capacidad", StringType(), True)\
                       ,StructField("Codigo_de_Sitio", StringType(), True)\
                       ,StructField("Elabora_Reporte", StringType(), True)\
                       ,StructField("Enviar_acuse_a", StringType(), True)\
                       ,StructField("Equipos_Adicionales?", StringType(), True)\
                       ,StructField("Firma", StringType(), True)\
                       ,StructField("Gabinetes_en_Sitio", StringType(), True)\
                       ,StructField("Generadores_en_Sitio", StringType(), True)\
                       ,StructField("Largo", StringType(), True)\
                       ,StructField("Marca", StringType(), True)\
                       ,StructField("Modelo", StringType(), True)\
                       ,StructField("Pierna_de_la_Torre", StringType(), True)\
                       ,StructField("Proyecto", StringType(), True)\
                       ,StructField("Racks", StringType(), True)\
                       ,StructField("Sector", StringType(), True)\
                       ,StructField("Serie", StringType(), True)\
                       ,StructField("Shelters_en_Sitio", StringType(), True)\
                       ,StructField("Status", StringType(), True)\
                       ,StructField("Tipo_Cerradura", StringType(), True)\
                       ,StructField("Tipo_Equipo", StringType(), True)\
                       ,StructField("Tipo_Shelter", StringType(), True)\
                       ,StructField("Tipo_de_Base", StringType(), True)\
                       ,StructField("Tipo_de_Cerradura", StringType(), True)\
                       ,StructField("Tipo_de_Contenedores", StringType(), True)\
                       ,StructField("Tipo_de_Instalacion", StringType(), True)\
                       ,StructField("Tipo_de_Pierna", StringType(), True)\
                       ,StructField("Tipo_de_Proteccion", StringType(), True)\
                       ,StructField("Tipo_de_Soporte", StringType(), True)\
                       ,StructField("Tipo_de_estructura", StringType(), True)\
                       ,StructField("Tipo_de_inventario", StringType(), True)\
                       ,StructField("Tipo_elemento", StringType(), True)\
                       ,StructField("Ubicacion", StringType(), True)\
                       ,StructField("Unidades_de_Rack", StringType(), True)\
                       ,StructField("Uso_de_Gabinete", StringType(), True)\
                       ,StructField("Vista_Activo_Fijo", StringType(), True)\
                       ,StructField("Vista_Banco_Baterias", StringType(), True)\
                       ,StructField("Vista_Etiqueta_SN", StringType(), True)\
                       ,StructField("Vista_Frontal_del_Rack", StringType(), True)\
                       ,StructField("Vista_Gabinete_Frontal", StringType(), True)\
                       ,StructField("Vista_Gabinete_Trasera", StringType(), True)\
                       ,StructField("Vista_Numero_Serie", StringType(), True)\
                       ,StructField("Vista_Shelter_Frontal", StringType(), True)\
                       ,StructField("Vista_Shelter_Pasamuros_exterior", StringType(), True)\
                       ,StructField("Vista_Trasera_del_Rack", StringType(), True)\
                       ,StructField("Vista__de_la_estructura", StringType(), True)\
                       ,StructField("Vista_de_espacio_banco_de_baterias", StringType(), True)\
                       ,StructField("Vista_del_elemento", StringType(), True)\
                       ,StructField("torres_o_estructuras", StringType(), True)\
                       ,StructField("status_id", StringType(), True)\
                       ,StructField("meta_started", StringType(), True)\
                       ,StructField("meta_finished", StringType(), True)\
                       ,StructField("meta_device_id", StringType(), True)\
                       ,StructField("meta_user", StringType(), True)\
                       ,StructField("id_site", StringType(), True)\
                       ,StructField("cve_vendor", StringType(), True)\
                       ,StructField("geo_lon", StringType(), True)\
                       ,StructField("geo_lat", StringType(), True)\
                       ,StructField("geo_alt", StringType(), True)\
                       ,StructField("geo_acc", StringType(), True)\
                       ,StructField("orig_site_code", StringType(), True)\
                       ,StructField("orig_cve_vendor", StringType(), True)\
                       ,StructField("comments", StringType(), True)\
                       ,StructField("created_on", StringType(), True)\
                       ,StructField("updated_on'", StringType(), True)])
```


```python
df_hive_eda = spark.createDataFrame(df,schema = mySchema)
df_hive_kpi = spark.createDataFrame(KPIs)
```


```python
#### Se sube la tabla a Hive
df_hive_eda.write.mode("overwrite").saveAsTable("rci_network_db.eda_odk_99")
df_hive_kpi.write.mode("overwrite").saveAsTable("rci_network_db.kpi_odk_99")
```
