
<div style="width: 100%; clear: both; font-family: Verdana;">
<div style="float: left; width: 50%;font-family: Verdana;">
<img src="https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Almacen_Segregacion/image/encabezado.png" align="left">
</div>
<div style="float: right; width: 200%;">
<p style="margin: 0; padding-top: 20px; text-align:right;color:rgb(193, 38, 184)"><strong>Axity - AT&T.
    Ciclo de vida de elementos de inventario</strong></p>
</div>
</div>
<div style="width:100%;">&nbsp;</div>

<div style="width: 100%; clear: both; font-family: Verdana;">
<h1 align="center">Exploratory Data Analysis</h1>
</div>

### Descripción
Analizaremos los datos de las fuentes de inventarios de AT&T con un tratamiento estadístico descriptivo para hacer el tracking del ciclo de vida de los elementos de red. Se creará un EDA enfocado a la salida de almacén. Serán documentados los catálogos propuestos junto a su respectivo tratamiento de datos. La fuente que corresponde a este análisis es:

* **Segregación Almacén (Almacén inventario)**  

Primero cargamos las librerías necesarias.

## Se tomará para el análisis la partición correspondiente a Noviembre 28 

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
conf = SparkConf().setAppName('Segregacion')  \
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

from pyspark.sql.functions import udf ,col
from pyspark.sql.types import IntegerType,StringType

%matplotlib inline

from bokeh.io import show, output_notebook, output_file 
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20_11, Category20c_20, Category10_5,Category10_6, Category20_20, Plasma256
output_notebook()
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="7366d328-256d-49a2-9c93-37631e116fa5">Loading BokehJS ...</span>
    </div>




### Recolección de los datos: 

#### Creamos una función para tratamiento de datos en spark:


```python
def validate_rule(string):
    search_list=[u" ",u'!',u'%',u'$',u'¡',u'¿',u'~',u'#',u'Ñ',u"Ã",u"Åƒ",u"Ã‹",u"Ã³",u'Ë',u'*',u"ILEGIBLE", u"VICIBLE",u"VISIBLE",u"INCOMPLETO"]    
    str_temp = string
    if str_temp.upper() == u"BORRADO":
      return 1
    elif len(str_temp) < 6:
      return 1
    elif any(ext in str_temp.upper()for ext in search_list):
      return 1
    else:
      return 0
```

Esta fuente en particular contiene la historia de los elementos en el almacén, consideramos las fechas de cada partición, es decir, fechas de cada archivo ingestado. Para conocer las particiones de la fuente es necesario realizar un query en el cluster **SHOW PARTITIONS tx_almacen_inventory** y escogemos las particiones del mes que se quiere analizar.

_10=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=10")
df_10=_10.toPandas()

_11=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=11")
df_11=_11.toPandas()

_12=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=12")
df_12=_12.toPandas()

_13=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=13")
df_13=_13.toPandas()

_17=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=17")
df_17=_17.toPandas()

_18=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=18")
df_18=_18.toPandas()

_19=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=19")
df_19=_19.toPandas()

_24=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=24")
df_24=_24.toPandas()

_26=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=26")
df_26=_26.toPandas()

_03=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=03")
df_03=_03.toPandas()

_30=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,estatus_cip,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=30")

validate_rule_udf = udf(validate_rule, IntegerType())
df_serie = _30.withColumn("serie_cleaned",validate_rule_udf(col("serie")))

df_30=df_serie.toPandas()

_04=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=04")
df_04=_04.toPandas()

_05=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=05")
df_05=_05.toPandas()

_06=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=06")
df_06=_06.toPandas()

_09=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=09 and day=09")
df_09=_09.toPandas()


```python
_28Nov=spark.sql("SELECT id, qr as qr_alm, org,sub_inv,almacen, articulo,descripcion,lpn_nuevo, ubicacion_nueva,estado_fisico_usadonuevo,tipo_de_articulo,serie,etiqueta,activo,mxn,usd,tipo_de_ubicacion_resum_1,datasetname,filedate,year,month,day FROM tx_almacen_inventory WHERE year=2019 and month=11 and day=28").cache() 

validate_rule_udf = udf(validate_rule, IntegerType())
df_serie = _28Nov.withColumn("serie_cleaned",validate_rule_udf(col("serie")))

df_28Nov=df_serie.toPandas()
```

*Hemos recolectado los campos a analizar de la fuente: inventario almacén.*

frames=[df_03,df_04,df_05,df_06,
        df_09,df_10,df_11,df_12,
        df_13,df_17,df_18,df_19,
        df_24,df_26,df_30]
df=pd.concat(frames,ignore_index=True)


```python
df=df_28Nov
```

## Segregación Almacén
Una visualización de la fuente de segregación.


```python
df.head(15)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>qr_alm</th>
      <th>org</th>
      <th>sub_inv</th>
      <th>almacen</th>
      <th>articulo</th>
      <th>descripcion</th>
      <th>lpn_nuevo</th>
      <th>ubicacion_nueva</th>
      <th>estado_fisico_usadonuevo</th>
      <th>...</th>
      <th>activo</th>
      <th>mxn</th>
      <th>usd</th>
      <th>tipo_de_ubicacion_resum_1</th>
      <th>datasetname</th>
      <th>filedate</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>22</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840187.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>22</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840187.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>23</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840183.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>23</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840183.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>29</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840196.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>29</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840196.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>30</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840191.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>30</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840191.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>33</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840194.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>33</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840194.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>34</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840195.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>34</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840195.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>35</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840197.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>35</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840197.0</td>
      <td></td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>37</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVOS</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2844305.0</td>
      <td></td>
      <td>672.33585163775513</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>15 rows × 23 columns</p>
</div>




```python
df.columns
```




    Index([u'id', u'qr_alm', u'org', u'sub_inv', u'almacen', u'articulo',
           u'descripcion', u'lpn_nuevo', u'ubicacion_nueva',
           u'estado_fisico_usadonuevo', u'tipo_de_articulo', u'serie', u'etiqueta',
           u'activo', u'mxn', u'usd', u'tipo_de_ubicacion_resum_1', u'datasetname',
           u'filedate', u'year', u'month', u'day', u'serie_cleaned'],
          dtype='object')



### Diccionario de datos

A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  **Carina**
    
* **id**: Código interno que identifica al elemento en el almacén.
* **qr**: Código QR interno que identifica al elemento en el almacén por organización.
* **org**: Código que identifica sitios en un almacén.
* **subinv**: Señala estado del articulo (Nuevo, usado, obsoleto, dañado, ...).
* **almacen**:Nombre del almacén en el que se encuentra el elemento.
* **articulo**: Identificador único de Oracle.
* **descripcion**: Descripción general del elemento.
* **upd**: Unidad de medida.
* **lpn_nuevo**: Identificador QR de un elemento cuando ha cambiado de almacén.
* **ubicacion_nueva**: Ubicación dentro del almacén a donde se ha movido el elemento.
* **estado_fisico**: Estatus del elemento (Nuevo, usado).
* **cantidad**: Número de elementos.
* **tipo de control**: Identificador de como se encontró el elemento.
* **pasillo**: Pasillo donde se encuentra el elemento.
* **nivel**: Nivel donde se encuentra el elemento.
* **parnon**: Parnon donde se encuentra el elemento.
* **tipo_articulo**: Tipo de Artículo.
* **serie**: Identificador único que tiene el proveedor.
* **etiqueta**: Id único del elemento de red que da AT&T (Activo).


### 2. Descripción de las fuentes.
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
camposSegg=df.columns
print('Columnas de la fuente segregacion son: ',list(camposSegg))
pd.DataFrame(df.dtypes,columns=['Tipo de objeto Segregación'])
```

    ('Columnas de la fuente segregacion son: ', ['id', 'qr_alm', 'org', 'sub_inv', 'almacen', 'articulo', 'descripcion', 'lpn_nuevo', 'ubicacion_nueva', 'estado_fisico_usadonuevo', 'tipo_de_articulo', 'serie', 'etiqueta', 'activo', 'mxn', 'usd', 'tipo_de_ubicacion_resum_1', 'datasetname', 'filedate', 'year', 'month', 'day', 'serie_cleaned'])





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Tipo de objeto Segregación</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>qr_alm</th>
      <td>object</td>
    </tr>
    <tr>
      <th>org</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sub_inv</th>
      <td>object</td>
    </tr>
    <tr>
      <th>almacen</th>
      <td>object</td>
    </tr>
    <tr>
      <th>articulo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>descripcion</th>
      <td>object</td>
    </tr>
    <tr>
      <th>lpn_nuevo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ubicacion_nueva</th>
      <td>object</td>
    </tr>
    <tr>
      <th>estado_fisico_usadonuevo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>tipo_de_articulo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>object</td>
    </tr>
    <tr>
      <th>etiqueta</th>
      <td>object</td>
    </tr>
    <tr>
      <th>activo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>mxn</th>
      <td>object</td>
    </tr>
    <tr>
      <th>usd</th>
      <td>object</td>
    </tr>
    <tr>
      <th>tipo_de_ubicacion_resum_1</th>
      <td>object</td>
    </tr>
    <tr>
      <th>datasetname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>filedate</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>year</th>
      <td>int32</td>
    </tr>
    <tr>
      <th>month</th>
      <td>int32</td>
    </tr>
    <tr>
      <th>day</th>
      <td>int32</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>int32</td>
    </tr>
  </tbody>
</table>
</div>




```python
print('renglones = ',df.shape[0],' columnas = ',df.shape[1])
```

    ('renglones = ', 356922, ' columnas = ', 23)



```python
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
              'transaction_status', 'year', 'month', 'day']

relevantes=[v for v in df.columns if v not in NOrelevantes]

df[relevantes].describe(include='all')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>qr_alm</th>
      <th>org</th>
      <th>sub_inv</th>
      <th>almacen</th>
      <th>articulo</th>
      <th>descripcion</th>
      <th>lpn_nuevo</th>
      <th>ubicacion_nueva</th>
      <th>estado_fisico_usadonuevo</th>
      <th>tipo_de_articulo</th>
      <th>serie</th>
      <th>etiqueta</th>
      <th>activo</th>
      <th>mxn</th>
      <th>usd</th>
      <th>tipo_de_ubicacion_resum_1</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922</td>
      <td>356922.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>333471</td>
      <td>15257</td>
      <td>48</td>
      <td>19</td>
      <td>46</td>
      <td>10586</td>
      <td>10934</td>
      <td>10873</td>
      <td>7949</td>
      <td>5</td>
      <td>7</td>
      <td>298327</td>
      <td>182737</td>
      <td>68820</td>
      <td>1</td>
      <td>2533</td>
      <td>4</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>111768</td>
      <td>0.0</td>
      <td>2PX</td>
      <td>USADODISP</td>
      <td>DHL Tepotzotlan</td>
      <td>W.1013182</td>
      <td>ANTENA TIPO: DIRECTED POLE PANEL POLARIZACION:...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NUEVO</td>
      <td>W</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>4</td>
      <td>215668</td>
      <td>156022</td>
      <td>182684</td>
      <td>156022</td>
      <td>8362</td>
      <td>8105</td>
      <td>214612</td>
      <td>214612</td>
      <td>327096</td>
      <td>196192</td>
      <td>35094</td>
      <td>150084</td>
      <td>266108</td>
      <td>356922</td>
      <td>266108</td>
      <td>260600</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.127966</td>
    </tr>
    <tr>
      <th>std</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.334053</td>
    </tr>
    <tr>
      <th>min</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>



#### De esta tabla describe, podemos observar que hay:
* Podría crearse un catálogo de almacenes, tipos de artículo y sub_inv
* En su mayoría, contamos con variables categóricas, razón por la cuál las secciones estadísticas no arrojan información. 


Se proponen los siguientes catálogos derivados de la fuente de Almacén Inventario:

* **sub_inv**: Señala estado del articulo (Nuevo, usado, obsoleto, dañado, ...).
* **almacen**: Nombre del almacén en el que se encuentra el elemento.
* **tipo_articulo**: Tipo de Artículo.

Estos catálogos nos ayudarán a mapear todas las diferentes variantes que existen para cada elemento. 

Se utilizó el catálogo de Almacenes **Info_almacenes**.

### 3. Exploración de los datos.
De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los catálogos. 

#### Para empezar, haremos una limpieza por columna:


```python
df.qr_alm.replace('0',np.NaN,inplace=True)
df.lpn_nuevo.replace('0',np.NaN,inplace=True)
df.ubicacion_nueva.replace('0',np.NaN,inplace=True)
df.estado_fisico_usadonuevo.replace('0',np.NaN,inplace=True)
df.estado_fisico_usadonuevo.replace('-',np.NaN,inplace=True)
df.etiqueta.replace('',np.NaN,inplace=True)
df.serie.replace('',np.NaN,inplace=True)
df.activo.replace('',np.NaN,inplace=True)
df.mxn.replace('',np.NaN,inplace=True)
```


```python
df.serie[(df.serie=='INCOMPLETO') | (df.serie=='ILEGIBLE') | 
     (df.serie=='BORRADO') | (df.serie=='VICIBLE') | 
     (df.serie=='VISIBLE')]=np.NaN
      
df.etiqueta[(df.etiqueta=='NOTIENE') | (df.etiqueta=='REVISAR') |
     (df.etiqueta=='VISIBLE') | (df.etiqueta=='ERROR') |
     (df.etiqueta=='VIDIBLE') | (df.etiqueta=='SINACTIVO') |
     (df.etiqueta=='ILEGIBLE') | (df.etiqueta=='IP3CAB6CAA') |
     (df.etiqueta=='3G113642') | (df.etiqueta=='3G083109') | 
     (df.etiqueta=='VISIVLE')]=np.NaN


especiales=['!','¡',u'¿','~','#','Ñ',"Ã“","Åƒ","Ã‹","Ã³",'Ë']
df.replace(especiales,np.NaN,regex=True,inplace=True)
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/ipykernel_launcher.py:3: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      This is separate from the ipykernel package so we can avoid doing imports until
    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/ipykernel_launcher.py:10: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      # Remove the CWD from sys.path while we load stuff.


#### Primer catálogo: *sub_inv*.

Empezaremos con el catálogo de sub_inv. Siendo un catálogo con entradas manuales, aplicaremos una limpieza a los datos para poder trabajarlos.


```python
aux=["Ã“","Åƒ","Ã‹","Ã³"]
df.sub_inv=df.sub_inv.str.upper()
df.sub_inv.replace(u'Á',u'A', regex=True, inplace=True)
df.sub_inv.replace(u'É',u'E', regex=True, inplace=True)
df.sub_inv.replace(u'Í',u'I', regex=True, inplace=True)
df.sub_inv.replace(u'Ó',u'O', regex=True, inplace=True)
df.sub_inv.replace(u'Ú',u'U', regex=True, inplace=True)
df.sub_inv.replace(u'Ń',u'U', regex=True, inplace=True)
df.sub_inv.replace(u'Đ',u'N', regex=True, inplace=True)
df.sub_inv.replace(u'Ñ',u'N', regex=True, inplace=True)
df.sub_inv.replace(u'Ë',u'E', regex=True, inplace=True)
df.sub_inv.replace(u'USADIS',u'USADO', regex=True, inplace=True)
df.sub_inv.replace(u'USADODISP',u'USADO', regex=True, inplace=True)
df.sub_inv.replace(u'UDISP',u'USADO', regex=True, inplace=True)
df.sub_inv.replace(u'USADOS',u'USADO', regex=True, inplace=True)
df.sub_inv.replace(u'OBSOLETO',u'OBS', regex=True, inplace=True)
df.sub_inv.replace(u'NUEVOS',u'NUEVO', regex=True, inplace=True)
df.sub_inv.replace(u'ACLARACIEN',u'ACLARACION', regex=True, inplace=True)
df.sub_inv.replace(u'DANADO',u'DAN', regex=True, inplace=True)
df.sub_inv.replace(u'REFA-DAU',u'REFA-DAN', regex=True, inplace=True)
df.sub_inv.replace(u'RF',u'REFA', regex=True, inplace=True)
df.sub_inv.replace(aux,'', regex=True, inplace=True)
df.sub_inv=df.sub_inv.str.strip()

catsub_inv=pd.DataFrame(df.sub_inv.value_counts())
index=list(range(0,catsub_inv.shape[0]))           
subinv=pd.DataFrame(catsub_inv.index,index=index)
subinv.columns=['Sub_inventario']
catsub_inv.index=index
catsub_inv.columns=['Frecuencia']
catsub_inv=pd.concat([subinv,catsub_inv],axis=1)
catsub_inv
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Sub_inventario</th>
      <th>Frecuencia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USADO</td>
      <td>182899</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NUEVO</td>
      <td>138258</td>
    </tr>
    <tr>
      <th>2</th>
      <td>REFA-USADO</td>
      <td>11272</td>
    </tr>
    <tr>
      <th>3</th>
      <td>REFA-NUEVO</td>
      <td>8980</td>
    </tr>
    <tr>
      <th>4</th>
      <td>OBS</td>
      <td>8320</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IBS-NUEVO</td>
      <td>5495</td>
    </tr>
    <tr>
      <th>6</th>
      <td>REFA-DAÐ</td>
      <td>578</td>
    </tr>
    <tr>
      <th>7</th>
      <td>REFA-OBS</td>
      <td>531</td>
    </tr>
    <tr>
      <th>8</th>
      <td>MOBILIARIO</td>
      <td>328</td>
    </tr>
    <tr>
      <th>9</th>
      <td>DAN</td>
      <td>90</td>
    </tr>
    <tr>
      <th>10</th>
      <td>REFA-REP</td>
      <td>77</td>
    </tr>
    <tr>
      <th>11</th>
      <td>CUARENTENA</td>
      <td>65</td>
    </tr>
    <tr>
      <th>12</th>
      <td>REFA-DAN</td>
      <td>16</td>
    </tr>
    <tr>
      <th>13</th>
      <td>ACLARACION</td>
      <td>7</td>
    </tr>
    <tr>
      <th>14</th>
      <td>DEV-NUEVO</td>
      <td>3</td>
    </tr>
    <tr>
      <th>15</th>
      <td>RMA</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



Después de limpiar el catálogo, ahora podemos hacer la visualización más adecuada.
Empezaremos usando un Histograma.


```python
catsub_inv.plot(x='Sub_inventario',
                y='Frecuencia',
                kind='bar',
                figsize=(10,6),
                rot=90,colormap='rainbow_r')
plt.xlabel('Sub inventario')
plt.ylabel('Frecuencia')
plt.title('Distribucion de los estados del Inventario de Almacen')
```




    Text(0.5,1,'Distribucion de los estados del Inventario de Almacen')




![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Almacen_Segregacion/image/output_49_1NOV.png)


Parece que hemos logrado un catálogo bien definido. Podrá revisarse en la sección de catálogos.

#### Segundo catálogo: *Almacén*
Seguimos el mismo procedimiento, limpieza, normalización y visualización.


```python
alm_catalogo=pd.read_csv('/home/cz014h/Info_Almacenes_clean.csv')
alm_catalogo.columns=['org','almacen','latitud','longitud']

df.merge(alm_catalogo,on='org', how='left')
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>qr_alm</th>
      <th>org</th>
      <th>sub_inv</th>
      <th>almacen</th>
      <th>articulo</th>
      <th>descripcion</th>
      <th>lpn_nuevo</th>
      <th>ubicacion_nueva</th>
      <th>estado_fisico_usadonuevo</th>
      <th>...</th>
      <th>activo</th>
      <th>mxn</th>
      <th>usd</th>
      <th>tipo_de_ubicacion_resum_1</th>
      <th>datasetname</th>
      <th>filedate</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>22</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVO</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840187.0</td>
      <td>NaN</td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>22</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVO</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840187.0</td>
      <td>NaN</td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>23</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVO</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840183.0</td>
      <td>NaN</td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>23</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVO</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840183.0</td>
      <td>NaN</td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>29</td>
      <td>2PX1S19-001051</td>
      <td>2PX</td>
      <td>NUEVO</td>
      <td>DHL Tepotzotlan</td>
      <td>W.9044002</td>
      <td>MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE...</td>
      <td>ANC2018073000010</td>
      <td>FR002A</td>
      <td>NUEVO</td>
      <td>...</td>
      <td>2840196.0</td>
      <td>NaN</td>
      <td>667.7504461461715</td>
      <td>Warehouse</td>
      <td>sa_almacen_inventory</td>
      <td>20191128</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 23 columns</p>
</div>



#### Veamos en un mapa la distribución de los almacenes:


```python
mapa_alm=alm_catalogo.loc[:,['almacen','latitud','longitud']].dropna()
mapa_alm.drop_duplicates(inplace=True)

import folium
from folium import plugins

Latitud=21.607871
Longitud=-101.201933
mapa=folium.Map(location=[Latitud,Longitud],zoom_start=4.8)

storages = folium.map.FeatureGroup()

for lat, lng, in zip(mapa_alm.latitud, mapa_alm.longitud):
    storages.add_child(
        folium.features.Marker(
            [lat, lng]
        )
    )
    
latitudes = list(mapa_alm.latitud)
longitudes = list(mapa_alm.longitud)
labels = list(mapa_alm.almacen)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(storages) 
mapa.save('Mapa de almacenes ATT.html')
mapa.add_child(storages)
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/folium/__init__.py:59: UserWarning: This version of folium is the last to support Python 2. Transition to Python 3 to be able to receive updates and fixes. Check out https://python3statement.org/ for more info.
      UserWarning





![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Almacen_Segregacion/image/Screenshot_2019-12-04%20Segregaci%C3%B3n%20Inventario.png)




```python
aux=df.loc[:,['org','almacen','tipo_de_articulo','serie','activo','mxn','etiqueta']]
#aux.dropna(thresh=5,inplace=True)
aux.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>org</th>
      <th>almacen</th>
      <th>tipo_de_articulo</th>
      <th>serie</th>
      <th>activo</th>
      <th>mxn</th>
      <th>etiqueta</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2PX</td>
      <td>DHL Tepotzotlan</td>
      <td>W</td>
      <td>21524311663AG7004232</td>
      <td>2840187.0</td>
      <td>NaN</td>
      <td>00895089</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2PX</td>
      <td>DHL Tepotzotlan</td>
      <td>W</td>
      <td>21524311663AG7004232</td>
      <td>2840187.0</td>
      <td>NaN</td>
      <td>00895089</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2PX</td>
      <td>DHL Tepotzotlan</td>
      <td>W</td>
      <td>21524311663AG7004237</td>
      <td>2840183.0</td>
      <td>NaN</td>
      <td>00895091</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2PX</td>
      <td>DHL Tepotzotlan</td>
      <td>W</td>
      <td>21524311663AG7004237</td>
      <td>2840183.0</td>
      <td>NaN</td>
      <td>00895091</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2PX</td>
      <td>DHL Tepotzotlan</td>
      <td>W</td>
      <td>21524311663AG7004263</td>
      <td>2840196.0</td>
      <td>NaN</td>
      <td>00895099</td>
    </tr>
  </tbody>
</table>
</div>



#### Normalización:


```python
counts=(aux.almacen.value_counts()/aux.almacen.value_counts().sum())*100

Ind=list(range(0,len(counts)))
Alm_counts=pd.DataFrame(counts)
Alm_counts.columns=['Porcentaje']
Almacenes=pd.DataFrame(Alm_counts.index)
Almacenes.columns=['almacen']
Alm_counts.index=Ind
Alm_counts= pd.concat([Almacenes,Alm_counts],axis=1)

for v in range(0,len(counts)):
    if Alm_counts.Porcentaje[v] < 3:
        Alm_counts.almacen[v]='Otros'

Alm_counts.Porcentaje.loc[Alm_counts['almacen'] == 'Otros'] = Alm_counts[Alm_counts.almacen=='Otros'].Porcentaje.sum()
Alm_counts=Alm_counts.head(5)
Alm_counts
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/ipykernel_launcher.py:13: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      del sys.path[0]
    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/pandas/core/indexing.py:189: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self._setitem_with_indexer(indexer, value)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>almacen</th>
      <th>Porcentaje</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>DHL Tepotzotlan</td>
      <td>43.713192</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Sta Cecilia AT&amp;T</td>
      <td>36.641619</td>
    </tr>
    <tr>
      <th>2</th>
      <td>PROVA SMO</td>
      <td>7.832524</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Glaco AT&amp;T</td>
      <td>3.948202</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Otros</td>
      <td>7.864463</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
Alm_counts.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel('almacen')
ax0.set_ylabel('Frecuencia')
ax0.set_title('Distribucion de frecuencias de Almacenes')

#Subplot2: Bar chart
explode_list=[.2,0,.13,0,0]
color_list=['royalblue','lightcoral','powderblue','slateblue','silver']
Alm_counts['Porcentaje'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title('Distribucion de frecuencias de Almacenes')
ax1.axis('equal')
ax1.legend(labels=Alm_counts.almacen,loc='upper left')

plt.show()
```


![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Almacen_Segregacion/image/output_58_0NOV.png)


Podemos observar que es en los almacenes: "**DHL Tepotzotlan, STA Cecilia y** y los correspondientes a **PROVA SMO**" donde se distribuyen la mayoría de elementos.  
Esto podría ser un indicador interesante en un futuro. Se encontrará el catálogo en la sección de catálogos.

<div style="width: 100%; clear: both; font-family: Verdana;">
    <p> Tercer catálogo: <strong>Tipo de artículo</strong>.
        <br>Procederemos a usar limpieza  en caso necesario y visualización.
        </p>
</div>


```python
df.tipo_de_articulo=df.tipo_de_articulo.str.upper()
aux.tipo_de_articulo=aux.tipo_de_articulo.str.upper()
TipoArt=pd.DataFrame(aux.tipo_de_articulo.unique())
TipoArt.columns=['Tipo_Artículo']
TipoArt
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Tipo_Artículo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>W</td>
    </tr>
    <tr>
      <th>1</th>
      <td>V</td>
    </tr>
    <tr>
      <th>2</th>
      <td>T</td>
    </tr>
    <tr>
      <th>3</th>
      <td>C</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NP</td>
    </tr>
    <tr>
      <th>5</th>
      <td>N</td>
    </tr>
  </tbody>
</table>
</div>




```python
ArtCounts=pd.Series((aux.tipo_de_articulo.value_counts()/aux.tipo_de_articulo.value_counts().sum())*100)
TipoArt['Porcentaje']=ArtCounts.values

columnas=list(TipoArt['Tipo_Artículo'])
Freq=list(TipoArt.Porcentaje)
source=ColumnDataSource(dict(columnas=columnas, Freq=Freq, color=Category10_6))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,80),
         title='Distribución de los tipos de Artículo')
p.vbar(x='columnas',top='Freq',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
TipoArt
```






![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Almacen_Segregacion/image/bokeh_plotNOV.png)

  <div class="bk-root" id="d57ed2fc-410e-4ef5-9d90-e9091d6cdb9a"></div>








<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Tipo_Artículo</th>
      <th>Porcentaje</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>W</td>
      <td>54.967752</td>
    </tr>
    <tr>
      <th>1</th>
      <td>V</td>
      <td>37.021814</td>
    </tr>
    <tr>
      <th>2</th>
      <td>T</td>
      <td>6.754697</td>
    </tr>
    <tr>
      <th>3</th>
      <td>C</td>
      <td>1.109486</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NP</td>
      <td>0.145970</td>
    </tr>
    <tr>
      <th>5</th>
      <td>N</td>
      <td>0.000280</td>
    </tr>
  </tbody>
</table>
</div>



<div style="width: 100%; clear: both; font-family: Verdana;">
<h2>4. Calidad de los datos</h2>
    <p> Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.
    </p>
</div>

#### Missings Values
Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.


```python
aux2=df
```


```python
output_file("Porcentaje de NAsSegg.html")
nas=aux2.isna().sum()
porcentaje_nas=nas/aux2.isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1),
         title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.6, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 23), ('counts_nas', 23)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))







![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Almacen_Segregacion/image/bokeh_plot(1)NOV.png)

  <div class="bk-root" id="47637568-69b0-4e6b-a46f-7f38433e7c39"></div>








<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Porcentaje de NAs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>id</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>qr_alm</th>
      <td>0.003082</td>
    </tr>
    <tr>
      <th>org</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>sub_inv</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>almacen</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>articulo</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>descripcion</th>
      <td>1.695048</td>
    </tr>
    <tr>
      <th>lpn_nuevo</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>ubicacion_nueva</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>estado_fisico_usadonuevo</th>
      <td>7.266293</td>
    </tr>
    <tr>
      <th>tipo_de_articulo</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>9.832681</td>
    </tr>
    <tr>
      <th>etiqueta</th>
      <td>42.049523</td>
    </tr>
    <tr>
      <th>activo</th>
      <td>74.556346</td>
    </tr>
    <tr>
      <th>mxn</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>usd</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>tipo_de_ubicacion_resum_1</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>datasetname</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>filedate</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>year</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>month</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>day</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>



Visualización de datos NOT NULL WLOG: 


```python
output_file("Porcentaje de NotNullSegg.html")
notmiss=(1-porcentaje_nas)*100

columnas=list(notmiss.keys())
counts_nas=list(notmiss.values)
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 23), ('counts_nas', 23)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))







![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Almacen_Segregacion/image/bokeh_plot(2)NOV.png)

  <div class="bk-root" id="69739d74-99de-4776-8591-85c7608a63d2"></div>








<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Porcentaje de Not nulls</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>id</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>qr_alm</th>
      <td>99.996918</td>
    </tr>
    <tr>
      <th>org</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>sub_inv</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>almacen</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>articulo</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>descripcion</th>
      <td>98.304952</td>
    </tr>
    <tr>
      <th>lpn_nuevo</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>ubicacion_nueva</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>estado_fisico_usadonuevo</th>
      <td>92.733707</td>
    </tr>
    <tr>
      <th>tipo_de_articulo</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>90.167319</td>
    </tr>
    <tr>
      <th>etiqueta</th>
      <td>57.950477</td>
    </tr>
    <tr>
      <th>activo</th>
      <td>25.443654</td>
    </tr>
    <tr>
      <th>mxn</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>usd</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>tipo_de_ubicacion_resum_1</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>datasetname</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>filedate</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>year</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>month</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>day</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



#### 4.2 Data Errors

* De manera general, se encuentran en varias columnas, nulos que se rellenaron con '0'. Ejemplos de estos casos, son las columnas: **qr**, **lpn_nuevo**, **ubicacion_nueva**.
* Tuvo que hacerse una preparación para identificar los NaNs, debido a que son ingresados como **0** ,"-" o simplemente un empty string.
* Hay datos sin **id**.
* Los campos de fecha tienen formato string.


### 5. Preparación de los datos.
Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos. 

 * **qr:** Se recomienda optar por un nuevo nombre, pasar los nulos '0' a NaN.
 * **almacén:**
    * Se utilizó el catálogo proporcionado por el equipo ATT, utilizando el campo **org**
        
* **sub_inv:** 
    * Pasar todo a uppercase
    * replace 'USADIS' to 'USADO'
    * replace 'USADODISP' to 'USADO'
    * replace 'UDISP' to 'USADO'
    * replace 'USADOS' to 'USADO'
    * replace 'OBSOLETO' to 'OBS'
    * replace 'NUEVOS' to 'NUEVO'
    * replace 'ACLARACIEN' to 'ACLARACION'
    * replace 'DANADO' to 'DAN'
    * replace 'REFA-DAU' to 'REFA-DAN'
    * replace 'RF' to 'REFA'
    * Eliminar acentos
    * Hay datos con caracteres desconocidos, debido a los acentos
        
* **series:**
    * Homologar formatos en los casos posibles. 
    * replace "'NA" to 'np.NaN'
    * Se deben revisar datos que vienen con notación científica
    * Se marcan como *np.NaN* : campos que contengan:
        * ESPACIOS
        * La palabra BORRADO
        * La palabra VICIBLE
        * La palabra VISIBLE
        * CARACTER ESPECIAL
        * ILEGIBLE
        * INCOMPLETO
        * LONGITUD de caracteres menores a 6

* **etiqueta:**
    * Se marcan como *np.NaN* : campos que contengan:
        * CARACTERES ESPECIALES
        * ESPACIOS
        * La palabra ILEGIBLE
        * LONGITUD menor a 4
        * La palabra VISIVLE
        * La palabra NOTIENE
        * La palabra REVISAR
        * La palabra VISIBLE
        * La palabra ERROR
        * La palabra VIDIBLE
        * La palabra SINACTIVO
    * Campos iguales a:
        * IP3CAB6CAA
        * 3G113642
        * 3G083109
* **mxn:**
    * reemplazar ('E',5,)
    * Dar formato 'float'
    
* **De manera general:**
    * Tratamiento de missings.
    * Eliminar acentos
    * Revisar caracteres desconocidos
    * Pasar a Uppercase o Lowercase por columna, según sea el formato estándar
    * Se deben revisar datos que vienen con notación científica


### 6. Catálogos
Se mostrarán los catálogos finales. 

#### Catálogo de sub inventario:


```python
pd.DataFrame(catsub_inv['Sub_inventario'])
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Sub_inventario</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USADO</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NUEVO</td>
    </tr>
    <tr>
      <th>2</th>
      <td>REFA-USADO</td>
    </tr>
    <tr>
      <th>3</th>
      <td>REFA-NUEVO</td>
    </tr>
    <tr>
      <th>4</th>
      <td>OBS</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IBS-NUEVO</td>
    </tr>
    <tr>
      <th>6</th>
      <td>REFA-DAÐ</td>
    </tr>
    <tr>
      <th>7</th>
      <td>REFA-OBS</td>
    </tr>
    <tr>
      <th>8</th>
      <td>MOBILIARIO</td>
    </tr>
    <tr>
      <th>9</th>
      <td>DAN</td>
    </tr>
    <tr>
      <th>10</th>
      <td>REFA-REP</td>
    </tr>
    <tr>
      <th>11</th>
      <td>CUARENTENA</td>
    </tr>
    <tr>
      <th>12</th>
      <td>REFA-DAN</td>
    </tr>
    <tr>
      <th>13</th>
      <td>ACLARACION</td>
    </tr>
    <tr>
      <th>14</th>
      <td>DEV-NUEVO</td>
    </tr>
    <tr>
      <th>15</th>
      <td>RMA</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de almacenes:
*Este fue un catálogo proporcionado por el equipo ATT*


```python
pd.DataFrame(alm_catalogo['almacen']).head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>almacen</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Tijuana Sistema AT&amp;T</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Sta Cecilia Sistemas AT&amp;T</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Sta Cecilia AT&amp;T</td>
    </tr>
    <tr>
      <th>3</th>
      <td>DHL-TRADE MARKETING</td>
    </tr>
    <tr>
      <th>4</th>
      <td>GDL AT&amp;T</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Sta Cecilia AT&amp;T</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Tijuana AT&amp;T</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Glaco AT&amp;T</td>
    </tr>
    <tr>
      <th>8</th>
      <td>DHL Tepotzotlan</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Sta Cecilia AT&amp;T</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de tipo de artículo:


```python
TipoArt
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Tipo_Artículo</th>
      <th>Porcentaje</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>W</td>
      <td>54.967752</td>
    </tr>
    <tr>
      <th>1</th>
      <td>V</td>
      <td>37.021814</td>
    </tr>
    <tr>
      <th>2</th>
      <td>T</td>
      <td>6.754697</td>
    </tr>
    <tr>
      <th>3</th>
      <td>C</td>
      <td>1.109486</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NP</td>
      <td>0.145970</td>
    </tr>
    <tr>
      <th>5</th>
      <td>N</td>
      <td>0.000280</td>
    </tr>
  </tbody>
</table>
</div>



#### Se hará una limpieza al dataframe según las reglas documentadas, para generar un universo limpio. 


```python
df.almacen.replace(u'Á','A',regex=True,inplace=True)
df.almacen.replace(u'É','A',regex=True,inplace=True)
df.almacen.replace(u'Í','A',regex=True,inplace=True)
df.almacen.replace(u'Ó','A',regex=True,inplace=True)
df.almacen.replace(u'Ú','A',regex=True,inplace=True)
df.almacen.replace(u'á','a',regex=True,inplace=True)
df.almacen.replace(u'é','e',regex=True,inplace=True)
df.almacen.replace(u'í','i',regex=True,inplace=True)
df.almacen.replace(u'ó','o',regex=True,inplace=True)
df.almacen.replace(u'ú','u',regex=True,inplace=True)
```


```python
#Trazabilidad
df['trazabilidad']=0
df.trazabilidad.loc[(df.serie_cleaned==0) | (df.etiqueta!=np.NaN)]=1

#CS CA
df['CS_CA']=0
df.CS_CA.loc[(df.serie_cleaned==0) & (df.etiqueta!=np.NaN)]=1

#CS SA
df['CS_SA']=0
df.CS_SA.loc[(df.serie_cleaned==0) & (df.etiqueta==np.NaN)]=1

#SS CA
df['SS_CA']=0
df.SS_CA.loc[(df.serie_cleaned==1) & (df.etiqueta!=np.NaN)]=1

```


```python
#from pyspark.sql.types import *
```

mySchema = StructType([ StructField("id", StringType(), True)\
                       ,StructField("qr_alm", StringType(), True)\
                       ,StructField("org", StringType(), True)\
                       ,StructField("sub_inv", StringType(), True)\
                       ,StructField("almacen", StringType(), True)\
                       ,StructField("articulo", StringType(), True)\
                       ,StructField("descripcion", StringType(), True)\
                       ,StructField("lpn_nuevo", StringType(), True)\
                       ,StructField("ubicacion_nueva", StringType(), True)\
                       ,StructField("estado_fisico_usadonuevo", StringType(), True)\
                       ,StructField("tipo_de_articulo", StringType(), True)\
                       ,StructField("serie", StringType(), True)\
                       ,StructField("etiqueta", StringType(), True)\
                       ,StructField("activo", StringType(), True)\
                       ,StructField("mxn", StringType(), True)\
                       ,StructField("usd", StringType(), True)\
                       ,StructField("tipo_de_ubicacion_resum_1", StringType(), True)\
                       ,StructField("filedate", StringType(), True)\
                       ,StructField("datasetname", StringType(), True)\
                       ,StructField("year", IntegerType(), True)\
                       ,StructField("month", IntegerType(), True)\
                       ,StructField("day", IntegerType(), True)\
                       ,StructField("serie_cleaned", IntegerType(), True)\
                       ,StructField("trazabilidad", IntegerType(), True)\
                       ,StructField("CS_CA", IntegerType(), True)\
                       ,StructField("CS_SA", IntegerType(), True)\
                       ,StructField("SS_CA", IntegerType(), True)])

df_hive = spark.createDataFrame(df,schema = mySchema)

df_hive.write.mode("overwrite").saveAsTable('default.eda_segregacion')

df.to_excel('Universo_Almacen_Segregacion28NOV.xlsx')


### 7. Métricas KPI.
Se mostrarán los KPIs generados. 

#### Total de elementos en almacén (todos los almacenes) 


```python
Total_Elementos=df.shape[0]
Total_Elementos
```




    356922




```python
df.replace(np.NaN,'vacio',inplace=True)
```

#### Total de elementos Trazables


```python
Total_Tr=df.loc[((df.serie!='vacio') | (df.etiqueta!='vacio'))].shape[0]
Total_Tr
```




    336628



#### Total de elementos no trazables 


```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    20294



#### Total de elementos en almacén Trazables Únicos


```python
Total_Tr_Unic=df[['serie','etiqueta']].loc[(df.serie!='vacio') | (df.etiqueta!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic
```




    312198



#### Total de elementos en almacén Trazables Únicos en DHL Tepotzotlan


```python
DHLTepo_Tr_Unic=df[['serie','etiqueta']].loc[((df.almacen=='DHL Tepotzotlan')|(df.almacen==u'DRP TEPOTZOTLÁN'))&((df.serie!='vacio') | (df.etiqueta!='vacio'))].drop_duplicates().shape[0]
DHLTepo_Tr_Unic
```




    115358



#### Total de elementos en almacén Trazables Únicos en Sta Cecilia AT&T


```python
STACeci_Tr_Unic=df[['serie','etiqueta']].loc[((df.almacen=='Sta Cecilia AT&T')|(df.almacen=='Sta Cecilia Sistemas AT&T'))&((df.serie!='vacio') | (df.etiqueta!='vacio'))].drop_duplicates().shape[0]
STACeci_Tr_Unic
```




    138120



#### Total de elementos en almacén Trazables Únicos en Tijuana


```python
Tijuana_Tr_Unic=df[['serie','etiqueta']].loc[((df.almacen=='Tijuana Sistema AT&T')|(df.almacen=='Tijuana AT&T')|(df.almacen=='PROVA TIJUANA')|(df.almacen=='SPC Tijuana')|(df.almacen=='DRP TIJUANA'))&((df.serie!='vacio') | (df.etiqueta!='vacio'))].drop_duplicates().shape[0]
Tijuana_Tr_Unic
```




    6958



#### Total de elementos en almacén Trazables Únicos en GDL


```python
GDL_Tr_Unic=df[['serie','etiqueta']].loc[((df.almacen=='GDL AT&T')|(df.almacen=='PROVA GUADALAJARA')|(df.almacen=='DRP GUADALAJARA'))&((df.serie!='vacio') | (df.etiqueta!='vacio'))].drop_duplicates().shape[0]
GDL_Tr_Unic
```




    7371



#### Total de elementos Trazables Únicos en Otros Almacénes


```python
Otros_Tr_Unic=Total_Tr_Unic-DHLTepo_Tr_Unic-STACeci_Tr_Unic-Tijuana_Tr_Unic-GDL_Tr_Unic
Otros_Tr_Unic
```




    44391



#### Total de elementos en almacén Trazables Únicos con NSerie, con Nactivo


```python
Total_Tr_Unic_CS_CA=df[['serie','etiqueta']].loc[(df.serie!='vacio') & (df.etiqueta!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_CS_CA
```




    169048



#### Total de elementos en almacén Trazables Únicos con NSerie, sin Nactivo


```python
Total_Tr_Unic_CS_SA=df[['serie','etiqueta']].loc[(df.serie!='vacio') & (df.etiqueta=='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_CS_SA
```




    129417



#### Total de elementos en almacén Trazables Únicos sin NSerie, con Nactivo


```python
Total_Tr_Unic_SS_CA=df[['serie','etiqueta']].loc[(df.serie=='vacio') & (df.etiqueta!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_SS_CA
```




    13733



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    24430



#### Costo promedio por elemento:


```python
df.usd.replace('vacio',np.NaN,regex=True,inplace=True)
df.usd.replace('',np.NaN,regex=True,inplace=True)
df.usd.replace(' ',np.NaN,regex=True,inplace=True)

df.usd=df.usd.astype('float')
PROM_USD=df.usd.mean(skipna=True)
PROM_USD=round(PROM_USD,2)
PROM_USD
```




    732.28



#### Costo de activos en CIP


```python
CIP_Tr_Cost=df[['usd']].loc[(df.tipo_de_ubicacion_resum_1=='CIP')].mean(skipna=True)
CIP_Tr_Cost=round(CIP_Tr_Cost,2)
CIP_Tr_Cost
```




    1618.39



#### Costo de activos en CIP Tepotzotlán


```python
CIP_DHLTepo_Cost=df[['usd']].loc[((df.almacen=='DHL Tepotzotlan')|(df.almacen==u'DRP TEPOTZOTLÁN'))&(df.tipo_de_ubicacion_resum_1=='CIP')].mean(skipna=True)
CIP_DHLTepo_Cost=round(CIP_DHLTepo_Cost,2)
CIP_DHLTepo_Cost
```




    1204.43



#### Costo de activos en CIP Santa Cecilia


```python
CIP_STACeci_Cost=df[['usd']].loc[((df.almacen=='Sta Cecilia AT&T')|(df.almacen=='Sta Cecilia Sistemas AT&T'))&(df.tipo_de_ubicacion_resum_1=='CIP')].mean(skipna=True)
CIP_STACeci_Cost=round(CIP_STACeci_Cost,2)
CIP_STACeci_Cost
```




    5749.05



#### Costo de activos en CIP Tijuana


```python
CIP_Tijuana_Cost=df[['usd']].loc[((df.almacen=='Tijuana Sistema AT&T')|(df.almacen=='Tijuana AT&T')|(df.almacen=='PROVA TIJUANA')|(df.almacen=='SPC Tijuana')|(df.almacen=='DRP TIJUANA'))&(df.tipo_de_ubicacion_resum_1=='CIP')].mean(skipna=True)
CIP_Tijuana_Cost=round(CIP_Tijuana_Cost,2)
CIP_Tijuana_Cost
```




    nan



#### Costo de activos en CIP Guadalajara


```python
CIP_GDL_Cost=df['usd'].loc[((df.almacen=='GDL AT&T')|(df.almacen=='PROVA GUADALAJARA')|(df.almacen=='DRP GUADALAJARA'))&(df.tipo_de_ubicacion_resum_1=='CIP')].mean(skipna=True)
CIP_GDL_Cost=round(CIP_GDL_Cost,2)
CIP_GDL_Cost
```




    nan



#### Costo de activos en CIP Otros almacenes 


```python
CIP_Otros_Cost=CIP_Tr_Cost-CIP_DHLTepo_Cost-CIP_STACeci_Cost-CIP_Tijuana_Cost-CIP_GDL_Cost
CIP_Otros_Cost
```




    nan



#### Número total de activos en CIP (de acuerdo con SA)


```python
CIP_Total=df.loc[(df.tipo_de_ubicacion_resum_1!='CIP')].shape[0]
CIP_Total
```




    356289



#### Número de activos en CIP Tepotzotlán


```python
CIP_DHLTepo=df[['serie','etiqueta']].loc[((df.almacen=='DHL Tepotzotlan')|(df.almacen==u'DRP TEPOTZOTLÁN'))&(df.tipo_de_ubicacion_resum_1=='CIP')].shape[0]
CIP_DHLTepo
```




    567



#### Número de activos en CIP Santa Cecilia


```python
CIP_STACeci=df[['serie','etiqueta']].loc[((df.almacen=='Sta Cecilia AT&T')|(df.almacen=='Sta Cecilia Sistemas AT&T'))&(df.tipo_de_ubicacion_resum_1=='CIP')].shape[0]
CIP_STACeci
```




    64



#### Número de activos en CIP Tijuana


```python
CIP_Tijuana=df[['serie','etiqueta']].loc[((df.almacen=='Tijuana Sistema AT&T')|(df.almacen=='Tijuana AT&T')|(df.almacen=='PROVA TIJUANA')|(df.almacen=='SPC Tijuana')|(df.almacen=='DRP TIJUANA'))&(df.tipo_de_ubicacion_resum_1=='CIP')].shape[0]
CIP_Tijuana
```




    0



#### Número de activos en CIP Guadalajara


```python
CIP_GDL=df[['serie','etiqueta']].loc[((df.almacen=='GDL AT&T')|(df.almacen=='PROVA GUADALAJARA')|(df.almacen=='DRP GUADALAJARA'))&(df.tipo_de_ubicacion_resum_1=='CIP')].shape[0]
CIP_GDL
```




    0



#### Número de activos en CIP Otros almacenes


```python
CIP_Otros=CIP_Total-CIP_DHLTepo-CIP_STACeci-CIP_Tijuana-CIP_GDL
CIP_Otros
```




    355658



#### Número de activos en CIP Trazables


```python
CIP_Total_Tr=df.loc[((df.serie!='vacio') | (df.etiqueta!='vacio'))&(df.tipo_de_ubicacion_resum_1=='CIP')].shape[0]
CIP_Total_Tr
```




    633



#### Número de activos en CIP Trazables Únicos 


```python
CIP_Total_Tr_Unic=df[['serie','etiqueta']].loc[((df.serie!='vacio') | (df.etiqueta!='vacio'))&(df.tipo_de_ubicacion_resum_1=='CIP')].drop_duplicates().shape[0]
CIP_Total_Tr_Unic
```




    624



#### Número de activos en CIP Trazables Únicos con NSerie, con Nactivo


```python
CIP_Total_Tr_Unic_CS_CA=df[['serie','etiqueta']].loc[((df.serie!='vacio') & (df.etiqueta!='vacio'))&(df.tipo_de_ubicacion_resum_1=='CIP')].drop_duplicates().shape[0]
CIP_Total_Tr_Unic_CS_CA
```




    366



#### Número de activos en CIP Trazables Únicos con NSerie, sin Nactivo


```python
CIP_Total_Tr_Unic_CS_SA=df[['serie','etiqueta']].loc[((df.serie!='vacio') & (df.etiqueta=='vacio'))&(df.tipo_de_ubicacion_resum_1=='CIP')].drop_duplicates().shape[0]
CIP_Total_Tr_Unic_CS_SA
```




    14



#### Número de activos en CIP Trazables Únicos sin NSerie, con Nactivo


```python
CIP_Total_Tr_Unic_SS_CA=df[['serie','etiqueta']].loc[((df.serie=='vacio') & (df.etiqueta!='vacio'))&(df.tipo_de_ubicacion_resum_1=='CIP')].drop_duplicates().shape[0]
CIP_Total_Tr_Unic_SS_CA
```




    244



#### Número de activos en CIP Trazables Duplicados


```python
CIP_Total_Tr_Dupli=CIP_Total_Tr-CIP_Total_Tr_Unic
CIP_Total_Tr_Dupli
```




    9



#### Número de activos en CIP No Trazables


```python
CIP_Total_NO_Tr=CIP_Total-CIP_Total_Tr
CIP_Total_NO_Tr
```




    355656




```python
KPIs=pd.DataFrame({'KPI':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados','Trazables Únicos en DHL Tepotzotlan',
                          'Trazables Únicos en Sta Cecilia AT&T','Trazables Únicos en Tijuana',
                          'Trazables Únicos en GDL AT&T','Trazables Únicos en Otros Almacénes',
                          'Total CS CA','Total CS SA','Total SS CA',
                         'Costo promedio USD','Costo de activos en CIP','Costo de activos en CIP Tepotzotlán',
                         'Costo de activos en CIP Santa Cecilia',
                          'Costo de activos en CIP Tijuana','Costo de activos en CIP Guadalajara',
                         'Costo de activos en CIP Otros almacenes',
                         'total de activos en CIP (de acuerdo con SA)',
                         'Total activos en CIP Tepotzotlán',
                         'Total activos en CIP Santa Cecilia','Número de activos en CIP Tijuana',
                         'Total de activos en CIP Guadalajara','Total de activos en CIP Otros almacenes',
                         'Total de activos en CIP Trazables','Total activos en CIP Trazables Únicos',
                         'CIP Trazables Únicos con NSerie, con Nactivo','CIP Trazables Únicos con NSerie, sin Nactivo',
                         'CIP Trazables Únicos sin NSerie, con Nactivo','CIP Trazables Duplicados',
                         'CIP No Trazables'],
                  'Resultado':[Total_Elementos,Total_Tr,Total_NOTr,
                              Total_Tr_Unic,Total_Tr_Dupli,DHLTepo_Tr_Unic,
                               STACeci_Tr_Unic,Tijuana_Tr_Unic,GDL_Tr_Unic,
                               Otros_Tr_Unic,
                               Total_Tr_Unic_CS_CA,Total_Tr_Unic_CS_SA,
                              Total_Tr_Unic_SS_CA,PROM_USD,CIP_Tr_Cost,
                              CIP_DHLTepo_Cost,CIP_STACeci_Cost,CIP_Tijuana,
                              CIP_GDL_Cost,CIP_Otros_Cost,CIP_Total,CIP_DHLTepo,
                               CIP_STACeci_Cost, CIP_Tijuana,CIP_GDL,CIP_Otros,
                              CIP_Total_Tr,CIP_Total_Tr_Unic,
                              CIP_Total_Tr_Unic_CS_CA,CIP_Total_Tr_Unic_CS_SA,
                              CIP_Total_Tr_Unic_SS_CA,CIP_Total_Tr_Dupli,
                              CIP_Total_NO_Tr]})

KPIs.replace(np.NaN,0,regex=True,inplace=True)
KPIs
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>356922.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>336628.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>20294.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>312198.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>24430.00</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Trazables Únicos en DHL Tepotzotlan</td>
      <td>115358.00</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Trazables Únicos en Sta Cecilia AT&amp;T</td>
      <td>138120.00</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Trazables Únicos en Tijuana</td>
      <td>6958.00</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Trazables Únicos en GDL AT&amp;T</td>
      <td>7371.00</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Trazables Únicos en Otros Almacénes</td>
      <td>44391.00</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Total CS CA</td>
      <td>169048.00</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Total CS SA</td>
      <td>129417.00</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Total SS CA</td>
      <td>13733.00</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Costo promedio USD</td>
      <td>732.28</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Costo de activos en CIP</td>
      <td>1618.39</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Costo de activos en CIP Tepotzotlán</td>
      <td>1204.43</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Costo de activos en CIP Santa Cecilia</td>
      <td>5749.05</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Costo de activos en CIP Tijuana</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Costo de activos en CIP Guadalajara</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Costo de activos en CIP Otros almacenes</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>20</th>
      <td>total de activos en CIP (de acuerdo con SA)</td>
      <td>356289.00</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Total activos en CIP Tepotzotlán</td>
      <td>567.00</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Total activos en CIP Santa Cecilia</td>
      <td>5749.05</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Número de activos en CIP Tijuana</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Total de activos en CIP Guadalajara</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Total de activos en CIP Otros almacenes</td>
      <td>355658.00</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Total de activos en CIP Trazables</td>
      <td>633.00</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Total activos en CIP Trazables Únicos</td>
      <td>624.00</td>
    </tr>
    <tr>
      <th>28</th>
      <td>CIP Trazables Únicos con NSerie, con Nactivo</td>
      <td>366.00</td>
    </tr>
    <tr>
      <th>29</th>
      <td>CIP Trazables Únicos con NSerie, sin Nactivo</td>
      <td>14.00</td>
    </tr>
    <tr>
      <th>30</th>
      <td>CIP Trazables Únicos sin NSerie, con Nactivo</td>
      <td>244.00</td>
    </tr>
    <tr>
      <th>31</th>
      <td>CIP Trazables Duplicados</td>
      <td>9.00</td>
    </tr>
    <tr>
      <th>32</th>
      <td>CIP No Trazables</td>
      <td>355656.00</td>
    </tr>
  </tbody>
</table>
</div>




```python
sc.stop()
```
