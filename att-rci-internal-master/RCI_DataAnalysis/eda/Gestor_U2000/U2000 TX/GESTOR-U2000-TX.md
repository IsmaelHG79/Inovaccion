
<div style="width: 100%; clear: both; font-family: Verdana;">
<div style="float: left; width: 50%;font-family: Verdana;">
<img src="https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/doc/att-logo1.png" align="left">
</div>
<div style="float: right; width: 200%;">
<p style="margin: 0; padding-top: 20px; text-align:right;color:rgb(193, 38, 184)"><strong>Axity - AT&T.
    Ciclo de vida de elementos de inventario</strong></p>
</div>
</div>
<div style="width:100%;">&nbsp;</div>

# Exploratory Data Analysis
## Ciclo de vida de elementos de inventario.
### Axity - AT&T.

## Descripción
Analizaremos los datos de las fuentes de inventarios de AT&T con un tratamiento estadístico descriptivo para hacer el tracking del ciclo de vida de los elementos de red. Se creará un EDA enfocado a la salida de almacén. Serán documentados los catálogos propuestos junto a su respectivo tratamiento de datos. La fuente que corresponde al gestor está dividida en dos partes:

* **GESTOR U2000 GPON**
* **GESTOR U2000 TX**

Para hacer más fácil la revisión de este documento, aquí solo se revisaran los datos del gestor **U2000 TX**, la información del gestor de fibra óptica GPON tiene su propio documento de análisis.

Primero cargamos las librerías necesarias:

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
from pyspark.sql.types import *
from pyspark.sql.functions import lit


```


```python
conf = SparkConf().setAppName('tx_fbb_u2000')  \
        .setMaster('yarn').set("spark.yarn.queue","root.eda").set("spark.executor.extrajavaoptions","-Xmx1024m").set("spark.sql.autoBroadcastJoinThreshold","50485760").set("spark.sql.join.preferSortMergeJoin", "true").set("spark.sql.codegen.wholeStage","true").set("spark.sql.inMemoryColumnarStorage.compressed","true").set("spark.sql.codegen","true").set("spark.kryoserializer.buffer.mb","128").set("spark.yarn.executor.memoryOverhead","20g")
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
from pyspark.sql.types import *

%matplotlib inline

from bokeh.io import show, output_notebook, output_file 
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20_11, Category20c_20, Category10_5,Category10_6, Category20_20, Plasma256
output_notebook()
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="2eceefd0-5696-440c-bad6-2578348725a6">Loading BokehJS ...</span>
    </div>




# U2000 TX

La fuente está compuesta de varias tablas que se tratarán de forma separada durante la exploración, si se identifican similitudes entre estas será en el modelo cuando se unan para conformar uno o varios catálogos; las tablas que la componen son:

1. Board Report
2. NE Report
3. Subrack Report
4. Optical Module
5. Subcard Report

Se utilizan como fuentes las tablas ```tx_fbb_u2000_board```, ```tx_fbb_u2000_ne```, ```tx_fbb_u2000_optical```, ```tx_fbb_u2000_subcard``` y ```tx_fbb_u2000_subrack```. El campo que tienen en común todas las tablas es ```NE```, que corresponde al sitio, sin embargo, no todas las tablas tienen la misma granularidad por lo que hacer joins podría crear un producto cartesiano de los conjuntos, complicando la medición de los indicadores; por esta razón se trataran las tablas por separado y una vez en el modelo estas se relacionarán.

## 1. U2000 GPON Board Report

## 1.1 Recolección de los datos: 

Los datos con los que se trabajan a lo largo del EDA corresponden a la partición de **20191113** para todas las tablas.

*IMPORTANTE*: Si se requieren ver datos de otro periodo, se debe cambiar los filtros ```year = <año-a-ejecutar>```, ```month = <mes-a-ejecutar>```, ```day = <día-a-ejecutar>``` de las tablas en la siguiente celda:


```python
df =spark.sql("select * from tx_fbb_u2000_board where year = 2019 and month = 11 and day = 13")
```


```python
df.columns
```




    ['ne',
     'board_name',
     'board_type',
     'ne_type',
     'subrack_id',
     'slot_id',
     'hardware_version',
     'software_version',
     'snbar_code',
     'alias',
     'remarks',
     'customized_column',
     'subrack_type',
     'ne_id',
     'bios_version',
     'fpga_version',
     'board_status',
     'pnbom_codeitem',
     'model',
     'rev_issue_number',
     'management',
     'description',
     'manufacture_date',
     'create_time',
     'filedate',
     'filename',
     'fileip',
     'hash_id',
     'sourceid',
     'registry_state',
     'datasetname',
     'timestamp',
     'transaction_status',
     'year',
     'month',
     'day']



Creamos una funcion para el tratamiento de datos en spark el cual contiene la reglas definidas para la columna ```snbar_code```:


```python
def validate_rule(string):
    
    search_list=[" ",'!','%','$',"<",">","^",'¡',"+","N/A",'¿','~','#','Ñ',"Ã","Åƒ","Ã‹","Ã³",'Ë','*','?',"ILEGIBLE", "VICIBLE","VISIBLE","INCOMPLETO"]
    test = u'%s' % (string)
    str_temp = test.decode('utf-8')
    if str_temp.upper() == "BORRADO":
      return 0
    elif len(str_temp) < 6:
      return 0
    elif any(ext.decode("utf-8") in str_temp.upper()for ext in search_list):
      return 0
    else:
      return 1
```

Se crea un udf en spark sobre la funcion ya creada 


```python
validate_rule_udf = udf(validate_rule, IntegerType())
```

Se le agrega una nueva columna al dataframe de spark; la nueva columna es la validacion de la columna serie con respecto al udf que creamos.


```python
df_serie = df.withColumn("serie_cleaned",validate_rule_udf(col("snbar_code"))).cache()
```

Se convierte el dataframe de spark a un dataframe de pandas


```python
df = df_serie.toPandas()
```

Hemos recolectado los campos a analizar de la fuente U2000 TX Board.

### Gestor U2000 Board Report
Cargamos una muestra de la fuente tx_gpon_u2000_board


```python
df.head(5)
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
      <th>ne</th>
      <th>board_name</th>
      <th>board_type</th>
      <th>ne_type</th>
      <th>subrack_id</th>
      <th>slot_id</th>
      <th>hardware_version</th>
      <th>software_version</th>
      <th>snbar_code</th>
      <th>alias</th>
      <th>...</th>
      <th>hash_id</th>
      <th>sourceid</th>
      <th>registry_state</th>
      <th>datasetname</th>
      <th>timestamp</th>
      <th>transaction_status</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MSO-TLA-1</td>
      <td>Frame:0/Slot:1</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>1</td>
      <td>0000</td>
      <td>0120</td>
      <td></td>
      <td>--</td>
      <td>...</td>
      <td>1660c7b356674d8ee7bba9b38cc1956464eb3a9aaafe8e...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MSO-TLA-1</td>
      <td>Frame:0/Slot:2</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>2</td>
      <td>0000</td>
      <td>0120</td>
      <td></td>
      <td>--</td>
      <td>...</td>
      <td>436325ecc98521cdf28c1f54f041c601c76d25ba441ef3...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MSO-REV-1</td>
      <td>Frame:0/Slot:1</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>1</td>
      <td>0000</td>
      <td>0120</td>
      <td></td>
      <td>--</td>
      <td>...</td>
      <td>7fea74f4d8d565965cdfa21f0f3e3db200e2696e6bc1bd...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MSO-REV-1</td>
      <td>Frame:0/Slot:2</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>2</td>
      <td>0000</td>
      <td>0120</td>
      <td></td>
      <td>--</td>
      <td>...</td>
      <td>969ab950ab95baa99187c5fdaa12195532915297497803...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MSO-TIJ-1</td>
      <td>Frame:0/Slot:1</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>1</td>
      <td>0000</td>
      <td>0120</td>
      <td></td>
      <td>--</td>
      <td>...</td>
      <td>9d33428dc21e92b428af4a2fb4277c8e6f720da108c3ad...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 37 columns</p>
</div>



### Diccionario de datos.
A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

* **ne**: ID del negocio.
* **board_name**: Familia de productos al que pertenece.
* **board_type**: Fecha de creacion, validar si es de carga.
* **ne_type**: Pendiente.
* **subrack_id**: Tipo de Software.
* **slot_id**: Pendiente, es un estatus.
* **hardware_version**: Versión del hardware del dispositivo.
* **software_version**: Versión del software del dispositivo.
* **snbar_code**: Numero de serie.
* **alias**: Nombre del sheet.
* **remarks**: Pendiente.
* **customized_column**: Pendiente.
* **ne_id**: Estado.
* **bios_version**: Versión del BIOS del dispositivo.
* **fpga_version**: Pendiente.
* **board_status**: Estado de servicio del dispositivo.
* **pnbom_codeitem**: Pendiente.
* **model**: Pendiente.
* **rev_issue_number**: Pendiente.
* **management**: Pendiente.
* **description**: Pendiente.
* **manufacture_date**: Fecha de fabricación del dispositivo.
* **create_time**: Pendiente.
* **filedate**: Fecha de carga del archivo fuente.
* **filename**: Nombre del archivo fuente.
* **hash_id**: Identificador único hash de la fuente.
* **source_id**: Fuente de archivo.
* **registry_state**: Timestamp de carga.
* **datasetname**: Nombre indentificador de la fuente.
* **timestamp**: Fecha de carga.
* **transaction_status**: Estatus de registro.
* **year**: Año de la partición.
* **month**: Mes de la partición.
* **day**: Día de la partición.

## 1.2 Descripción de las fuentes
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos=df.columns
print('Columnas de la fuente TX Board son: ',list(campos))
pd.DataFrame(df.dtypes,columns=['Tipo de objeto TX Board'])
```

    ('Columnas de la fuente TX Board son: ', ['ne', 'board_name', 'board_type', 'ne_type', 'subrack_id', 'slot_id', 'hardware_version', 'software_version', 'snbar_code', 'alias', 'remarks', 'customized_column', 'subrack_type', 'ne_id', 'bios_version', 'fpga_version', 'board_status', 'pnbom_codeitem', 'model', 'rev_issue_number', 'management', 'description', 'manufacture_date', 'create_time', 'filedate', 'filename', 'fileip', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie_cleaned'])





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
      <th>Tipo de objeto TX Board</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ne</th>
      <td>object</td>
    </tr>
    <tr>
      <th>board_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>board_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subrack_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>slot_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>object</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>object</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>object</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bios_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>fpga_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>board_status</th>
      <td>object</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>object</td>
    </tr>
    <tr>
      <th>model</th>
      <td>object</td>
    </tr>
    <tr>
      <th>rev_issue_number</th>
      <td>object</td>
    </tr>
    <tr>
      <th>management</th>
      <td>object</td>
    </tr>
    <tr>
      <th>description</th>
      <td>object</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>object</td>
    </tr>
    <tr>
      <th>create_time</th>
      <td>object</td>
    </tr>
    <tr>
      <th>filedate</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>filename</th>
      <td>object</td>
    </tr>
    <tr>
      <th>fileip</th>
      <td>object</td>
    </tr>
    <tr>
      <th>hash_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sourceid</th>
      <td>object</td>
    </tr>
    <tr>
      <th>registry_state</th>
      <td>object</td>
    </tr>
    <tr>
      <th>datasetname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>timestamp</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>transaction_status</th>
      <td>object</td>
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

    ('renglones = ', 107509, ' columnas = ', 37)



```python
#Pasamos las columnas que queremos ver en nuestro describe:
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
      <th>ne</th>
      <th>board_name</th>
      <th>board_type</th>
      <th>ne_type</th>
      <th>subrack_id</th>
      <th>slot_id</th>
      <th>hardware_version</th>
      <th>software_version</th>
      <th>snbar_code</th>
      <th>alias</th>
      <th>...</th>
      <th>board_status</th>
      <th>pnbom_codeitem</th>
      <th>model</th>
      <th>rev_issue_number</th>
      <th>management</th>
      <th>description</th>
      <th>manufacture_date</th>
      <th>create_time</th>
      <th>fileip</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>...</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509</td>
      <td>107509.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>8186</td>
      <td>218</td>
      <td>336</td>
      <td>24</td>
      <td>4</td>
      <td>88</td>
      <td>188</td>
      <td>182</td>
      <td>88048</td>
      <td>2</td>
      <td>...</td>
      <td>3</td>
      <td>214</td>
      <td>4</td>
      <td>6</td>
      <td>2</td>
      <td>316</td>
      <td>2425</td>
      <td>4700</td>
      <td>4</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>MXTLAM02SDH05</td>
      <td>ODU</td>
      <td>SL91ISU2 (SL91ISU2)</td>
      <td>OptiX RTN 950</td>
      <td>--</td>
      <td>9</td>
      <td>--</td>
      <td>1.0</td>
      <td>/</td>
      <td>--</td>
      <td>...</td>
      <td>Normal</td>
      <td>/</td>
      <td></td>
      <td></td>
      <td>--</td>
      <td>/</td>
      <td>/</td>
      <td>--</td>
      <td>10.32.233.36</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>70</td>
      <td>27708</td>
      <td>10988</td>
      <td>39020</td>
      <td>102567</td>
      <td>7858</td>
      <td>28710</td>
      <td>32569</td>
      <td>17798</td>
      <td>103433</td>
      <td>...</td>
      <td>104927</td>
      <td>17867</td>
      <td>101516</td>
      <td>101516</td>
      <td>103181</td>
      <td>17796</td>
      <td>18839</td>
      <td>52578</td>
      <td>33520</td>
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
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.821289</td>
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
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.383112</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
<p>11 rows × 26 columns</p>
</div>




```python
df["board_status"].unique()
```




    array([u'Normal', u'Fault', u'Unknown'], dtype=object)



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

Todas las columnas contienen campos alfanuméricos que aunque proporcionan una forma de clasificación no son entendibles a simple vista, sin embargo, nuestro conocimiento del negocio nos permite intuir que varias de estas columnas serán útiles en el futuro como son:
1. Board Type
2. Board Status
3. Hardware Version
4. Software Version
5. NE Type

Se proponen catálogos derivados de la fuente U2000 TX Board con dichos campos.

## 1.3 Exploración de los datos
De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los potenciales catálogos que acabamos de identificar, estos serán llamado más adelante en el apartado de *Catálogos* de este mismo documento; nuestra intención por el momento es simplemente explorar los datos.

#### Para empezar, se hará una limpieza general a los datos:


```python
df.replace('null',np.NaN,inplace=True)
df.replace('NA',np.NaN,inplace=True)
df.replace('NULL',np.NaN,inplace=True)
df.replace('<NULL>',np.NaN,inplace=True)
df.replace('NAN',np.NaN,inplace=True)
df.replace('na',np.NaN,inplace=True)
df.replace('',np.NaN,inplace=True)
df.replace(' ',np.NaN,inplace=True)
df.replace('--',np.NaN,inplace=True)
df.description.replace('\/(?!\w)',np.NaN,inplace=True,regex=True)
df.hardware_version.replace('\/(?!\w)',np.NaN,inplace=True,regex=True)
df.software_version.replace('\/(?!\w)',np.NaN,inplace=True,regex=True)
df.software_version.replace('0',np.NaN,inplace=True)
df.software_version.replace('0000',np.NaN,inplace=True)
df.snbar_code.replace('0000','0',inplace=True,regex=True)
df.snbar_code.replace('0000000000000000',np.NaN,inplace=True)
df.snbar_code.replace('0000',np.NaN,inplace=True)
df.snbar_code.replace('/',np.NaN,inplace=True)
df.snbar_code.replace('0',np.NaN,inplace=True)
#Se puede hacer más y por columna en caso de ser necesario
```

### Primer catálogo: *Board Type*

Empezaremos con el catálogo *Board Type*. Este catalogo nos permite concer y agrupar los datos por medio del tipo de tarjeta de control del dispositivo de fibra óptica.


```python
#Revisamos frecuencias:
campo_boardtype=pd.DataFrame(df.board_type.value_counts()[:20])

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_boardtype.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Board Type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Board Type Top 20')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_boardtype['board_type'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción por Board Type Top 20',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_boardtype.index,loc='upper left')

plt.show()
```


![png](output_38_0.png)


Podemos observar que no se necesitan muchas reglas de limpieza, ya que todos siguen el mismo patrón y no existen valores nulos o inválidos muy recurrentes.

### Segundo catálogo: *Board Status*

El siguiente catálogo es *Board Status*; este catalogo nos permite conocer y agrupar los datos por medio del estado de servicio de la tarjeta.


```python
#Revisamos frecuencias:
campo_board_status=pd.DataFrame(df.board_status.value_counts())

#print campo_softwaretype['softwaretype'].size
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_board_status.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Estatus')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Board Status')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_board_status['board_status'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Proporción Board Status',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_board_status.index,loc='upper left')

plt.show()
```


![png](output_42_0.png)


### Tercer Catálogo: *Hardware Version*

El siguiente catálogo es *Hardware Version*. Este catalogo nos permite agrupar los datos por la versión del producto.


```python
#Revisamos frecuencias:
campo_hardware=pd.DataFrame(df.hardware_version.value_counts()[:30])

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_hardware.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Board Type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Board Type Top 30')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_hardware['hardware_version'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción por version de Hardware Top 30',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_hardware.index,loc='upper left')

plt.show()
```


![png](output_45_0.png)


### Cuarto catálogo: *Software Version*

El siguiente catálogo es *Software Version*; este catalogo nos permite agrupar los datos por la versión del firmware del producto.


```python
#Revisamos frecuencias:
campo_software=pd.DataFrame(df.software_version.value_counts()[:15])

#print campo_softwaretype['softwaretype'].size
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_software.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Estatus')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Software Version')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_software['software_version'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción Software Version',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_software.index,loc='upper left')

plt.show()
```


![png](output_48_0.png)


Será necesaria hacer una pequeña homologación de los números de version, especialmente en casos que varian por ceros finales como es el caso de *1.0* y *1.00*.

### Quinto catálogo: *NE Type*

El último catálogo es *NE Type*; éste catálogo nos permite agrupar los datos por la versión del tipo de NE. Esté dato aparece en varias tablas a lo largo de la fuente U2000 TX e incluso tiene una tabla especializada por lo que los datos que se pudieran descubrir aquí servirán para nutrir el catálogo que saldráde la tabla `tx_fbb_u2000_ne`.


```python
#Revisamos frecuencias:
campo_ne=pd.DataFrame(df.ne_type.value_counts())

#print campo_softwaretype['softwaretype'].size
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_ne.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Estatus')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma NE Type')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_ne['ne_type'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción NE Type',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_ne.index,loc='upper left')

plt.show()
```


![png](output_52_0.png)


## 1.4 Calidad de los datos
Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.


```python
df.head(10)
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
      <th>ne</th>
      <th>board_name</th>
      <th>board_type</th>
      <th>ne_type</th>
      <th>subrack_id</th>
      <th>slot_id</th>
      <th>hardware_version</th>
      <th>software_version</th>
      <th>snbar_code</th>
      <th>alias</th>
      <th>...</th>
      <th>hash_id</th>
      <th>sourceid</th>
      <th>registry_state</th>
      <th>datasetname</th>
      <th>timestamp</th>
      <th>transaction_status</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MSO-TLA-1</td>
      <td>Frame:0/Slot:1</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>1</td>
      <td>0000</td>
      <td>0120</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1660c7b356674d8ee7bba9b38cc1956464eb3a9aaafe8e...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MSO-TLA-1</td>
      <td>Frame:0/Slot:2</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>2</td>
      <td>0000</td>
      <td>0120</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>436325ecc98521cdf28c1f54f041c601c76d25ba441ef3...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MSO-REV-1</td>
      <td>Frame:0/Slot:1</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>1</td>
      <td>0000</td>
      <td>0120</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>7fea74f4d8d565965cdfa21f0f3e3db200e2696e6bc1bd...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MSO-REV-1</td>
      <td>Frame:0/Slot:2</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>2</td>
      <td>0000</td>
      <td>0120</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>969ab950ab95baa99187c5fdaa12195532915297497803...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MSO-TIJ-1</td>
      <td>Frame:0/Slot:1</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>1</td>
      <td>0000</td>
      <td>0120</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>9d33428dc21e92b428af4a2fb4277c8e6f720da108c3ad...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>MSO-TIJ-1</td>
      <td>Frame:0/Slot:2</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>2</td>
      <td>0000</td>
      <td>0120</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>d86523a457b6d5a2bab27d81c8a3db37c19f218d02c214...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>MSO-MER-1</td>
      <td>Frame:0/Slot:1</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>1</td>
      <td>0000</td>
      <td>0120</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>ae94ea2f0853523657d65656fa2d7235e9eb60a8a91748...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>MSO-MER-1</td>
      <td>Frame:0/Slot:2</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>2</td>
      <td>0000</td>
      <td>0120</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>427741ff94d6407dc05e7bb3701589a3be5641e4ec6b3b...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>MSO-TLA-2</td>
      <td>Frame:0/Slot:1</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>1</td>
      <td>0000</td>
      <td>0120</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>730d59938e3da4235b7a0a851a699d589b2594f7c73dbd...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>MSO-TLA-2</td>
      <td>Frame:0/Slot:2</td>
      <td>LCIM</td>
      <td>BITS</td>
      <td>0</td>
      <td>2</td>
      <td>0000</td>
      <td>0120</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>a1e7212462714afbe5bc228974a5b3e17990e369e07d0d...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:101:28:19:6:0</td>
      <td>Board_Report</td>
      <td>20191129</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>10 rows × 37 columns</p>
</div>



#### Visualización de los datos de trazabilidad: 

Creamos una tabla donde se observarán los número de serie repetidos para un mejor análisis.


```python
pd.DataFrame(df.snbar_code.value_counts()[:15])
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
      <th>snbar_code</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>215241248610C8000175</th>
      <td>3</td>
    </tr>
    <tr>
      <th>021PFKCNF2002507</th>
      <td>3</td>
    </tr>
    <tr>
      <th>020VVT10C8009074</th>
      <td>3</td>
    </tr>
    <tr>
      <th>020VWWW0DA002218</th>
      <td>3</td>
    </tr>
    <tr>
      <th>020VVT6TDA606221</th>
      <td>3</td>
    </tr>
    <tr>
      <th>021PFKCNF2002680</th>
      <td>3</td>
    </tr>
    <tr>
      <th>021UDHCNFA004938</th>
      <td>3</td>
    </tr>
    <tr>
      <th>215241249210DB028</th>
      <td>3</td>
    </tr>
    <tr>
      <th>21021207626TF8907607</th>
      <td>3</td>
    </tr>
    <tr>
      <th>215241331210F4002</th>
      <td>3</td>
    </tr>
    <tr>
      <th>020VVTCNDB000988</th>
      <td>3</td>
    </tr>
    <tr>
      <th>020VVT10C8005321</th>
      <td>3</td>
    </tr>
    <tr>
      <th>020VVT10C8009077</th>
      <td>3</td>
    </tr>
    <tr>
      <th>215241248610C8000180</th>
      <td>3</td>
    </tr>
    <tr>
      <th>215241249210DB030</th>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



### Missings Values
Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.


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
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de NAs por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 26), ('counts_nas', 26)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="4a3ee2fc-a353-411c-b2aa-19618e06a965"></div>








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
      <th>ne</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>board_name</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>board_type</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>ne_type</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subrack_id</th>
      <td>95.403176</td>
    </tr>
    <tr>
      <th>slot_id</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>29.577059</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>3.913161</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>17.931522</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>96.208690</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>0.398106</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>4.189417</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>3.606210</td>
    </tr>
    <tr>
      <th>bios_version</th>
      <td>81.688045</td>
    </tr>
    <tr>
      <th>fpga_version</th>
      <td>46.491922</td>
    </tr>
    <tr>
      <th>board_status</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>2.032388</td>
    </tr>
    <tr>
      <th>model</th>
      <td>99.030779</td>
    </tr>
    <tr>
      <th>rev_issue_number</th>
      <td>96.377978</td>
    </tr>
    <tr>
      <th>management</th>
      <td>95.974291</td>
    </tr>
    <tr>
      <th>description</th>
      <td>17.268322</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>1.903096</td>
    </tr>
    <tr>
      <th>create_time</th>
      <td>48.905673</td>
    </tr>
    <tr>
      <th>fileip</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>



#### Visualización de datos NOT NULL: 


```python
notmiss=(1-porcentaje_nas)*100

columnas=list(notmiss.keys())
counts_nas=list(notmiss.values)

#Mismo aplica aquí para color
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 26), ('counts_nas', 26)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="c799f8cd-14c8-4394-a408-a1f840655f90"></div>








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
      <th>ne</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>board_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>board_type</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>ne_type</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subrack_id</th>
      <td>4.596824</td>
    </tr>
    <tr>
      <th>slot_id</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>70.422941</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>96.086839</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>82.068478</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>3.791310</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>99.601894</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>95.810583</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>96.393790</td>
    </tr>
    <tr>
      <th>bios_version</th>
      <td>18.311955</td>
    </tr>
    <tr>
      <th>fpga_version</th>
      <td>53.508078</td>
    </tr>
    <tr>
      <th>board_status</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>97.967612</td>
    </tr>
    <tr>
      <th>model</th>
      <td>0.969221</td>
    </tr>
    <tr>
      <th>rev_issue_number</th>
      <td>3.622022</td>
    </tr>
    <tr>
      <th>management</th>
      <td>4.025709</td>
    </tr>
    <tr>
      <th>description</th>
      <td>82.731678</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>98.096904</td>
    </tr>
    <tr>
      <th>create_time</th>
      <td>51.094327</td>
    </tr>
    <tr>
      <th>fileip</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



Se observa que muchas de las columnas tienen un 100% de datos no nulos, las columnas que indican atributos del producto son los mas incompletos como la version del hardware, software y la fecha de fabricación. Existen cuatro campos sin datos válidos.

## 1.5 Catálogos

#### Catálogo de Board Type:


```python
Catalogo_board_type=pd.DataFrame(df.board_type.unique())
Catalogo_board_type.columns=['board_type']

Catalogo_board_type.reset_index(drop=True)
Catalogo_board_type.dropna(inplace=True)
Catalogo_board_type.sort_values(by='board_type').head(10)
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
      <th>board_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>196</th>
      <td>BP2 (SSN1BA201)</td>
    </tr>
    <tr>
      <th>101</th>
      <td>BP2 (SSN1BA203)</td>
    </tr>
    <tr>
      <th>137</th>
      <td>BP2 (SSN1BA204)</td>
    </tr>
    <tr>
      <th>201</th>
      <td>BP2 (SSN1BA205)</td>
    </tr>
    <tr>
      <th>139</th>
      <td>BPA_EX (SSN1BPA01)</td>
    </tr>
    <tr>
      <th>162</th>
      <td>BPA_EX (SSN1BPA02)</td>
    </tr>
    <tr>
      <th>289</th>
      <td>CLOCK</td>
    </tr>
    <tr>
      <th>309</th>
      <td>CN1510</td>
    </tr>
    <tr>
      <th>291</th>
      <td>CR57LPUF120A</td>
    </tr>
    <tr>
      <th>282</th>
      <td>CR5D00E1NC76</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de Board Status:


```python
Catalogo_board_status=pd.DataFrame(df.board_status.unique())
Catalogo_board_status.columns=['board_status']

Catalogo_board_status.reset_index(drop=True)
Catalogo_board_status.dropna(inplace=True)
Catalogo_board_status.sort_values(by='board_status').head(10)
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
      <th>board_status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>Fault</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Normal</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Unknown</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de Hardware Version:


```python
Catalogo_hardware=pd.DataFrame(df.hardware_version.unique())
Catalogo_hardware.columns=['hardware_version']

Catalogo_hardware.reset_index(drop=True)
Catalogo_hardware.dropna(inplace=True)
Catalogo_hardware.sort_values(by='hardware_version').head(10)
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
      <th>hardware_version</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0001</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0002</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0003</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0004</td>
    </tr>
    <tr>
      <th>174</th>
      <td>1</td>
    </tr>
    <tr>
      <th>167</th>
      <td>32</td>
    </tr>
    <tr>
      <th>169</th>
      <td>CR52FCBA REV A</td>
    </tr>
    <tr>
      <th>139</th>
      <td>CR52FCBD REV B</td>
    </tr>
    <tr>
      <th>147</th>
      <td>CR52FCBE REV A</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de Software Version:


```python
Catalogo_software=pd.DataFrame(df.software_version.unique())
Catalogo_software.columns=['software_version']

#Remover los sucios
#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios, un ejemplo puede ser:
#Catalogo_CAMPO.drop(labels=[67,346,369,279,171,313],axis=0,inplace=True)

#Se le da 
Catalogo_software.reset_index(drop=True)
Catalogo_software.dropna(inplace=True)
Catalogo_software.sort_values(by='software_version').head(10)
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
      <th>software_version</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3</th>
      <td>0106</td>
    </tr>
    <tr>
      <th>0</th>
      <td>0120</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0138</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0140</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0142</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0146</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0170</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0210</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0618</td>
    </tr>
    <tr>
      <th>12</th>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de NE Type:


```python
Catalogo_ne=pd.DataFrame(df.ne_type.unique())
Catalogo_ne.columns=['ne_type']

Catalogo_ne.reset_index(drop=True)
Catalogo_ne.dropna(inplace=True)
Catalogo_ne.sort_values(by='ne_type').head(10)
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
      <th>ne_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BITS</td>
    </tr>
    <tr>
      <th>16</th>
      <td>CX600</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Eudemon1000E</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Eudemon8000E</td>
    </tr>
    <tr>
      <th>17</th>
      <td>NE40E</td>
    </tr>
    <tr>
      <th>18</th>
      <td>NE40E(V8)</td>
    </tr>
    <tr>
      <th>12</th>
      <td>OptiX Metro 1000V3</td>
    </tr>
    <tr>
      <th>8</th>
      <td>OptiX Metro 1050</td>
    </tr>
    <tr>
      <th>9</th>
      <td>OptiX OSN 1500</td>
    </tr>
    <tr>
      <th>13</th>
      <td>OptiX OSN 1800</td>
    </tr>
  </tbody>
</table>
</div>



## 1.6 Preparación de los datos
Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos en los dos catálogos: 

* Se eliminan los siguientes caracteres especiales:    '-','#','%','/','_'
* Se eliminan espacios.
* Se eliminan valores que indican nulos como "--".
* Pasar todo a uppercase


```python
df.snbar_code.replace('/',np.NaN,inplace=True)
df['trazabilidad']=0
df.trazabilidad.loc[(df.serie_cleaned==0) ]=1
```


```python
df.dtypes
```




    ne                    object
    board_name            object
    board_type            object
    ne_type               object
    subrack_id            object
    slot_id               object
    hardware_version      object
    software_version      object
    snbar_code            object
    alias                 object
    remarks               object
    customized_column     object
    subrack_type          object
    ne_id                 object
    bios_version          object
    fpga_version          object
    board_status          object
    pnbom_codeitem        object
    model                 object
    rev_issue_number      object
    management            object
    description           object
    manufacture_date      object
    create_time           object
    filedate               int64
    filename              object
    fileip                object
    hash_id               object
    sourceid              object
    registry_state        object
    datasetname           object
    timestamp              int64
    transaction_status    object
    year                   int64
    month                  int64
    day                    int64
    serie_cleaned          int64
    trazabilidad           int64
    dtype: object



## 1.7 Métricas KPI

Se mostrarán los KPIs generados. 


```python
Total_Elementos=df.shape[0]
Total_Elementos
```




    107509




```python
df.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables


```python
Total_Tr=df.loc[(df.snbar_code!='vacio') ].shape[0]
Total_Tr
```




    88231



#### Total Elementos NO Trazables


```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    19278



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=df[['snbar_code']].loc[(df.snbar_code!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic
```




    88043



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    188




```python
df.columns
```




    Index([u'ne', u'board_name', u'board_type', u'ne_type', u'subrack_id',
           u'slot_id', u'hardware_version', u'software_version', u'snbar_code',
           u'alias', u'remarks', u'customized_column', u'subrack_type', u'ne_id',
           u'bios_version', u'fpga_version', u'board_status', u'pnbom_codeitem',
           u'model', u'rev_issue_number', u'management', u'description',
           u'manufacture_date', u'create_time', u'filedate', u'filename',
           u'fileip', u'hash_id', u'sourceid', u'registry_state', u'datasetname',
           u'timestamp', u'transaction_status', u'year', u'month', u'day',
           u'serie_cleaned'],
          dtype='object')



### KPIS


```python
#Ajustar el df contra los kpis de la siguiente tabla:

KPIs=pd.DataFrame({'KPI':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos,Total_Tr,Total_NOTr,
                              Total_Tr_Unic,Total_Tr_Dupli]})

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
      <td>107509</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>88231</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>19278</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>88043</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>188</td>
    </tr>
  </tbody>
</table>
</div>



Se envían los resultados a Hive:


```python
df_hive_kpis = spark.createDataFrame(KPIs)
```


```python
df_hive_kpis_final = df_hive_kpis.withColumn("filedate",lit(20191113)).withColumn("year",lit(2019)).withColumn("month",lit(11)).withColumn("day",lit(13))
```


```python
df_hive_kpis_final.write.mode("overwrite").saveAsTable("rci_network_db.kpi_u2000_tx_board")
```

## 2. NE Report

### 2.1 Recolección de los datos

Se crea el dataframe de spark




```python
df_load_2 = spark.sql("select * from tx_fbb_u2000_ne where year = 2019 and month = 11 and day = 13")
```


```python
df_load_1_2019_11 = df_load_2.withColumn("serie_cleaned",validate_rule_udf(col("ne_name"))).cache()
```

Se carga a pandas


```python
df_1 = df_load_1_2019_11.toPandas()
```

Una muestra de la fuente tx_gpon_u2000_ne


```python
df_1.head(5)
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
      <th>ne_name</th>
      <th>ne_type</th>
      <th>ne_ip_address</th>
      <th>ne_mac_address</th>
      <th>ne_id</th>
      <th>software_version</th>
      <th>physical_location</th>
      <th>create_time</th>
      <th>fibercable_count</th>
      <th>running_status</th>
      <th>...</th>
      <th>hash_id</th>
      <th>sourceid</th>
      <th>registry_state</th>
      <th>datasetname</th>
      <th>timestamp</th>
      <th>transaction_status</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MXCMXM01RTCOREBH01</td>
      <td>CX600</td>
      <td>10.33.79.9</td>
      <td>78:1D:BA:56:8F:C7</td>
      <td>0-0</td>
      <td>VRP5.160 V600R008C10</td>
      <td>Beijing China</td>
      <td>10/31/2016 17:06:34</td>
      <td>0</td>
      <td>Normal</td>
      <td>...</td>
      <td>8ba7a4c14f9f17fc6c6510573fcd4edaa72bfe7c3507c5...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:10:27:17:38:4</td>
      <td>NE_Report</td>
      <td>20191127</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MXJALTLZ0892MW01</td>
      <td>OptiX RTN 950A</td>
      <td>10.60.212.223</td>
      <td>38-4C-4F-F8-28-30</td>
      <td>6-546</td>
      <td>V100R008C10SPC300</td>
      <td>--</td>
      <td>10/28/2016 21:36:33</td>
      <td>2</td>
      <td>--</td>
      <td>...</td>
      <td>9fea5951550ce9a4da74278439d3d73e8a16a81590ae4f...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:10:27:17:38:4</td>
      <td>NE_Report</td>
      <td>20191127</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MXMICMRL3316MW01</td>
      <td>OptiX RTN 910</td>
      <td>10.60.118.13</td>
      <td>80-FB-06-E0-29-6D</td>
      <td>6-560</td>
      <td>V100R006C00SPC200</td>
      <td>--</td>
      <td>11/01/2016 18:47:14</td>
      <td>2</td>
      <td>--</td>
      <td>...</td>
      <td>e4491bf18fde2e5497df52e4ab8c1c83b363d7d9a4b7c8...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:10:27:17:38:4</td>
      <td>NE_Report</td>
      <td>20191127</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MXMICTAR1197MW02</td>
      <td>OptiX RTN 950</td>
      <td>10.60.216.87</td>
      <td>4C-1F-CC-ED-F6-C6</td>
      <td>6-498</td>
      <td>V100R008C10SPC200</td>
      <td>--</td>
      <td>11/01/2016 18:59:31</td>
      <td>3</td>
      <td>--</td>
      <td>...</td>
      <td>86882e396ff0133ffea4f0cb39a6f9c4f04127551fce1a...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:10:27:17:38:4</td>
      <td>NE_Report</td>
      <td>20191127</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MXMICCUI3430MW01</td>
      <td>OptiX RTN 950</td>
      <td>10.60.216.86</td>
      <td>4C-1F-CC-ED-F6-42</td>
      <td>6-496</td>
      <td>V100R008C10SPC200</td>
      <td>--</td>
      <td>11/01/2016 19:52:36</td>
      <td>3</td>
      <td>--</td>
      <td>...</td>
      <td>249889d320d8a3314fd39f94794b0b316bb78c8aeac8cc...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:10:27:17:38:4</td>
      <td>NE_Report</td>
      <td>20191127</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 38 columns</p>
</div>




```python
df_1.columns
```




    Index([u'ne_name', u'ne_type', u'ne_ip_address', u'ne_mac_address', u'ne_id',
           u'software_version', u'physical_location', u'create_time',
           u'fibercable_count', u'running_status', u'subnet', u'subnet_path',
           u'alias', u'remarks', u'patch_version_list', u'customized_column',
           u'lsr_id', u'maintenance_status', u'gateway_type', u'gateway',
           u'optical_ne', u'subrack_type', u'conference_call', u'orderwire_phone',
           u'ne_subtype', u'filedate', u'filename', u'fileip', u'hash_id',
           u'sourceid', u'registry_state', u'datasetname', u'timestamp',
           u'transaction_status', u'year', u'month', u'day', u'serie_cleaned'],
          dtype='object')




```python
df_1["ne_type"].unique
```




    <bound method Series.unique of 0                CX600
    1       OptiX RTN 950A
    2        OptiX RTN 910
    3        OptiX RTN 950
    4        OptiX RTN 950
    5        OptiX RTN 950
    6        OptiX RTN 950
    7       OptiX RTN 950A
    8        OptiX RTN 950
    9        OptiX RTN 950
    10       OptiX RTN 950
    11      OptiX RTN 950A
    12       OptiX RTN 950
    13       OptiX RTN 950
    14               CX600
    15               CX600
    16               CX600
    17               CX600
    18               CX600
    19               CX600
    20               CX600
    21               CX600
    22               CX600
    23               CX600
    24               CX600
    25               CX600
    26               CX600
    27               CX600
    28               CX600
    29               CX600
                 ...      
    8189    OptiX RTN 950A
    8190    OptiX RTN 950A
    8191     OptiX RTN 950
    8192    OptiX RTN 950A
    8193    OptiX RTN 950A
    8194    OptiX RTN 950A
    8195    OptiX RTN 950A
    8196     OptiX RTN 980
    8197    OptiX RTN 950A
    8198    OptiX RTN 950A
    8199    OptiX RTN 950A
    8200     OptiX RTN 910
    8201    OptiX RTN 950A
    8202    OptiX RTN 950A
    8203    OptiX RTN 950A
    8204    OptiX RTN 950A
    8205     OptiX RTN 950
    8206     OptiX RTN 950
    8207     OptiX RTN 980
    8208     OptiX RTN 950
    8209    OptiX RTN 950A
    8210    OptiX RTN 950A
    8211    OptiX RTN 950A
    8212    OptiX RTN 950A
    8213    OptiX RTN 950A
    8214    OptiX RTN 950A
    8215    OptiX RTN 950A
    8216    OptiX RTN 950A
    8217    OptiX RTN 380H
    8218    OptiX RTN 380H
    Name: ne_type, Length: 8219, dtype: object>



### Diccionario de datos.

A continuación se enlistan los campos de la fuente con una breve descripción de negocio.



* **ne**: ID del negocio.
* **board_name**: Familia de productos al que pertenece.
* **board_type**: Fecha de creacion, validar si es de carga.
* **ne_type**: Pendiente.
* **subrack_id**: Tipo de Software.
* **slot_id**: Pendiente, es un estatus.
* **hardware_version**: Versión del hardware del dispositivo.
* **software_version**: Versión del software del dispositivo.
* **snbar_code**: Numero de serie.
* **alias**: Nombre del sheet.
* **remarks**: Pendiente.
* **customized_column**: Pendiente.
* **ne_id**: Estado.
* **bios_version**: Versión del BIOS del dispositivo.
* **fpga_version**: Pendiente.
* **board_status**: Estado de servicio del dispositivo.
* **pnbom_codeitem**: Pendiente.
* **model**: Pendiente.
* **rev_issue_number**: Pendiente.
* **management**: Pendiente.
* **description**: Pendiente.
* **manufacture_date**: Fecha de fabricación del dispositivo.
* **create_time**: Pendiente.
* **filedate**: Fecha de carga del archivo fuente.
* **filename**: Nombre del archivo fuente.
* **hash_id**: Identificador único hash de la fuente.
* **source_id**: Fuente de archivo.
* **registry_state**: Timestamp de carga.
* **datasetname**: Nombre indentificador de la fuente.
* **timestamp**: Fecha de carga.
* **transaction_status**: Estatus de registro.
* **year**: Año de la partición.
* **month**: Mes de la partición.
* **day**: Día de la partición.

## 2.2 Descripción de las fuentes

En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada tabla se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos_1=df_1.columns
print('Columnas de la fuente NE Report son: ',list(campos_1))
pd.DataFrame(df_1.dtypes,columns=['Tipo de objeto NE Report'])
```

    ('Columnas de la fuente NE Report son: ', ['ne_name', 'ne_type', 'ne_ip_address', 'ne_mac_address', 'ne_id', 'software_version', 'physical_location', 'create_time', 'fibercable_count', 'running_status', 'subnet', 'subnet_path', 'alias', 'remarks', 'patch_version_list', 'customized_column', 'lsr_id', 'maintenance_status', 'gateway_type', 'gateway', 'optical_ne', 'subrack_type', 'conference_call', 'orderwire_phone', 'ne_subtype', 'filedate', 'filename', 'fileip', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie_cleaned'])





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
      <th>Tipo de objeto NE Report</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ne_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_ip_address</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_mac_address</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>physical_location</th>
      <td>object</td>
    </tr>
    <tr>
      <th>create_time</th>
      <td>object</td>
    </tr>
    <tr>
      <th>fibercable_count</th>
      <td>object</td>
    </tr>
    <tr>
      <th>running_status</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subnet</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subnet_path</th>
      <td>object</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>object</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>object</td>
    </tr>
    <tr>
      <th>patch_version_list</th>
      <td>object</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>object</td>
    </tr>
    <tr>
      <th>lsr_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>maintenance_status</th>
      <td>object</td>
    </tr>
    <tr>
      <th>gateway_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>gateway</th>
      <td>object</td>
    </tr>
    <tr>
      <th>optical_ne</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>conference_call</th>
      <td>object</td>
    </tr>
    <tr>
      <th>orderwire_phone</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_subtype</th>
      <td>object</td>
    </tr>
    <tr>
      <th>filedate</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>filename</th>
      <td>object</td>
    </tr>
    <tr>
      <th>fileip</th>
      <td>object</td>
    </tr>
    <tr>
      <th>hash_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sourceid</th>
      <td>object</td>
    </tr>
    <tr>
      <th>registry_state</th>
      <td>object</td>
    </tr>
    <tr>
      <th>datasetname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>timestamp</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>transaction_status</th>
      <td>object</td>
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
print('renglones = ',df_1.shape[0],' columnas = ',df_1.shape[1])
```

    ('renglones = ', 8219, ' columnas = ', 38)



```python
#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes_1=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'fileip', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes_1=[v for v in df_1.columns if v not in NOrelevantes_1]

df_1[relevantes_1].describe(include='all')
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
      <th>ne_name</th>
      <th>ne_type</th>
      <th>ne_ip_address</th>
      <th>ne_mac_address</th>
      <th>ne_id</th>
      <th>software_version</th>
      <th>physical_location</th>
      <th>create_time</th>
      <th>fibercable_count</th>
      <th>running_status</th>
      <th>...</th>
      <th>lsr_id</th>
      <th>maintenance_status</th>
      <th>gateway_type</th>
      <th>gateway</th>
      <th>optical_ne</th>
      <th>subrack_type</th>
      <th>conference_call</th>
      <th>orderwire_phone</th>
      <th>ne_subtype</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>...</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219</td>
      <td>8219.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>8196</td>
      <td>25</td>
      <td>8090</td>
      <td>7909</td>
      <td>7585</td>
      <td>41</td>
      <td>8</td>
      <td>8218</td>
      <td>23</td>
      <td>4</td>
      <td>...</td>
      <td>567</td>
      <td>2</td>
      <td>3</td>
      <td>984</td>
      <td>2</td>
      <td>18</td>
      <td>4</td>
      <td>48</td>
      <td>28</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>MXHIDTGB0098MW01</td>
      <td>OptiX RTN 950</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>V100R008C10SPC200</td>
      <td>--</td>
      <td>11/10/2017 01:21:45</td>
      <td>2</td>
      <td>--</td>
      <td>...</td>
      <td>--</td>
      <td>Normal</td>
      <td>Non-gateway</td>
      <td>--</td>
      <td></td>
      <td>Subrack Type II</td>
      <td>999</td>
      <td>0</td>
      <td>OptiX RTN 950</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>2</td>
      <td>3485</td>
      <td>32</td>
      <td>298</td>
      <td>581</td>
      <td>4821</td>
      <td>7591</td>
      <td>2</td>
      <td>3899</td>
      <td>7593</td>
      <td>...</td>
      <td>7652</td>
      <td>8216</td>
      <td>6653</td>
      <td>641</td>
      <td>7592</td>
      <td>6271</td>
      <td>7540</td>
      <td>7461</td>
      <td>3485</td>
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
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.983696</td>
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
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.126648</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
<p>11 rows × 26 columns</p>
</div>




```python
df_1["ne_type"].unique()
```




    array([u'CX600', u'OptiX RTN 950A', u'OptiX RTN 910', u'OptiX RTN 950',
           u'Eudemon1000E', u'NE40E', u'Eudemon8000E', u'OptiX RTN 980',
           u'S5300', u'SVN3000', u'OptiX OSN 1500', u'OptiX OSN 3500',
           u'NE40E(V8)', u'OptiX RTN 980L', u'OptiX OSN 2500',
           u'OptiX PTN 3900', u'OptiX Metro 1050', u'OptiX Metro 1000V3',
           u'OptiX OSN 1800', u'OptiX RTN 310', u'OptiX RTN 380',
           u'OptiX RTN 605', u'Dummy Device', u'BITS', u'OptiX RTN 380H'],
          dtype=object)



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

No cuenta con un campo que permita la trazabilidad de sus elementos, todos serán clasificados por default como *No trazables*. Como se puede observar las columnas que mas se adecuan para ser un catalogo son:

1. ne_type.
2. physical_location
3. ne_subtype
4. parch_version
4. subnet

Estas parecen proporcionar una forma de clasificacion y agrupacion del set de datos , y son columnas que pueden agregar cierto valor al negocio.

## 2.3 Exploración de los datos

#### Para empezar, se hará una limpieza general a los datos:


```python
df_1.replace('null',np.NaN,inplace=True)
df_1.replace('NA',np.NaN,inplace=True)
df_1.replace('na',np.NaN,inplace=True)
df_1.replace('NULL',np.NaN,inplace=True)
df_1.replace('<NULL>',np.NaN,inplace=True)
df_1.replace(' ',np.NaN,inplace=True)
df_1.replace('',np.NaN,inplace=True)
df_1.replace('--',np.NaN,inplace=True)
df_1.replace('/',np.NaN,inplace=True)
df_1.replace('-',np.NaN,inplace=True)
df_1.patch_version_list.replace('-',np.NaN,inplace=True)
df_1.customized_column.replace('-',np.NaN,inplace=True)
```

### Primer catálogo: NE Type


```python
#Revisamos frecuencias:
netype =pd.DataFrame(df_1.ne_type.value_counts())
#print campo_rnc['rnc'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
netype.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'NOMBRE rnc')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma NE Type')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

netype['ne_type'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción por NE Type',y=1.12)
ax1.axis('equal')
ax1.legend(labels=netype.index,loc='upper left')

plt.show()

```


![png](output_122_0.png)


### Segundo catálogo: Physical Location


```python
campo_location=pd.DataFrame(df_1.physical_location.value_counts()).head(20)

#print campo_type['physical_location'].size
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_location.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'NOMBRE type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Physical Location')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_location['physical_location'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Frecuencia de Physical Location',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_location.index,loc='upper left')

plt.show()
```


![png](output_124_0.png)


### Tercer catálogo: NE Subtype


```python
campo_subtype=pd.DataFrame(df_1.ne_subtype.value_counts()).head(20)

#print campo_type['physical_location'].size
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_subtype.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'NE Type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma NE Subtype')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_subtype['ne_subtype'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción de NE Subtype',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_subtype.index,loc='upper left')

plt.show()
```


![png](output_126_0.png)


### Cuarto catálogo: Subnet


```python
campo_subnet=pd.DataFrame(df_1.subnet.value_counts()).head(20)

#print campo_type['physical_location'].size
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_subnet.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Subnet')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Top 20 Subnet')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_subnet['subnet'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporcion Top 20 Physical Location',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_subnet.index,loc='upper left')

plt.show()
```


![png](output_128_0.png)


### Quinto catálogo: Patch Version


```python
campo_patch=pd.DataFrame(df_1.patch_version_list.value_counts()).head(20)

#print campo_type['physical_location'].size
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_patch.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Patch Version')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Patch Version')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_patch['patch_version_list'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción de Patch Version',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_patch.index,loc='upper left')

plt.show()
```


![png](output_130_0.png)


## 2.4 Calidad de los datos

Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

#### Visualización de los datos de trazabilidad: 

La fuente no contiene un campo que indique el número de serie o de activo por lo que todos los registros se considerarán como NO trazables.

### Missings Values

Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.


```python
nas=df_1[relevantes_1].isna().sum()
porcentaje_nas=nas/df_1[relevantes_1].isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 26), ('counts_nas', 26)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="02ffcf8f-3c6a-4c2c-a7e5-63dbbb987259"></div>








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
      <th>ne_name</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>ne_type</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>ne_ip_address</th>
      <td>0.389342</td>
    </tr>
    <tr>
      <th>ne_mac_address</th>
      <td>3.625745</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>7.068986</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>0.085169</td>
    </tr>
    <tr>
      <th>physical_location</th>
      <td>92.383502</td>
    </tr>
    <tr>
      <th>create_time</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>fibercable_count</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>running_status</th>
      <td>92.383502</td>
    </tr>
    <tr>
      <th>subnet</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subnet_path</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>98.698138</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>15.354666</td>
    </tr>
    <tr>
      <th>patch_version_list</th>
      <td>9.782212</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>lsr_id</th>
      <td>93.101351</td>
    </tr>
    <tr>
      <th>maintenance_status</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>gateway_type</th>
      <td>7.068986</td>
    </tr>
    <tr>
      <th>gateway</th>
      <td>7.799002</td>
    </tr>
    <tr>
      <th>optical_ne</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>1.192359</td>
    </tr>
    <tr>
      <th>conference_call</th>
      <td>8.212678</td>
    </tr>
    <tr>
      <th>orderwire_phone</th>
      <td>8.212678</td>
    </tr>
    <tr>
      <th>ne_subtype</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>



Visualización de datos NOT NULL:


```python
notmiss=(1-porcentaje_nas)*100

columnas=list(notmiss.keys())
counts_nas=list(notmiss.values)

#Mismo aplica aquí para color
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 26), ('counts_nas', 26)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="dafcb187-59a3-41be-aad1-7dc2fcf0bb32"></div>








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
      <th>ne_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>ne_type</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>ne_ip_address</th>
      <td>99.610658</td>
    </tr>
    <tr>
      <th>ne_mac_address</th>
      <td>96.374255</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>92.931014</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>99.914831</td>
    </tr>
    <tr>
      <th>physical_location</th>
      <td>7.616498</td>
    </tr>
    <tr>
      <th>create_time</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>fibercable_count</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>running_status</th>
      <td>7.616498</td>
    </tr>
    <tr>
      <th>subnet</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subnet_path</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>1.301862</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>84.645334</td>
    </tr>
    <tr>
      <th>patch_version_list</th>
      <td>90.217788</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>lsr_id</th>
      <td>6.898649</td>
    </tr>
    <tr>
      <th>maintenance_status</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>gateway_type</th>
      <td>92.931014</td>
    </tr>
    <tr>
      <th>gateway</th>
      <td>92.200998</td>
    </tr>
    <tr>
      <th>optical_ne</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>98.807641</td>
    </tr>
    <tr>
      <th>conference_call</th>
      <td>91.787322</td>
    </tr>
    <tr>
      <th>orderwire_phone</th>
      <td>91.787322</td>
    </tr>
    <tr>
      <th>ne_subtype</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



##  2.5 Catálogos

De los potenciales catálogos que se plantearon en la sección anterior se descartó a *Physical Location* porque no tenía las características necesarias para convertirse en catálogo, los datos tenían menos de 5% de no nulos además de poseer valores extraños.

#### Catálogo de NE Type:


```python
Catalogo_ne_type=pd.DataFrame(df_1.ne_type.unique())
Catalogo_ne_type.columns=['ne_type']

Catalogo_ne_type.reset_index(drop=True)
Catalogo_ne_type.dropna(inplace=True)
Catalogo_ne_type.sort_values(by='ne_type').head(10)
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
      <th>ne_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>23</th>
      <td>BITS</td>
    </tr>
    <tr>
      <th>0</th>
      <td>CX600</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Dummy Device</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Eudemon1000E</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Eudemon8000E</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NE40E</td>
    </tr>
    <tr>
      <th>12</th>
      <td>NE40E(V8)</td>
    </tr>
    <tr>
      <th>17</th>
      <td>OptiX Metro 1000V3</td>
    </tr>
    <tr>
      <th>16</th>
      <td>OptiX Metro 1050</td>
    </tr>
    <tr>
      <th>10</th>
      <td>OptiX OSN 1500</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de NE Subtype:


```python
Catalogo_ne_subtype=pd.DataFrame(df_1.ne_subtype.unique())
Catalogo_ne_subtype.columns=['ne_subtype']

Catalogo_ne_subtype.reset_index(drop=True)
Catalogo_ne_subtype.dropna(inplace=True)
Catalogo_ne_subtype.sort_values(by='ne_subtype').head(10)
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
      <th>ne_subtype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>26</th>
      <td>BITS</td>
    </tr>
    <tr>
      <th>4</th>
      <td>CX600-X1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>CX600-X16</td>
    </tr>
    <tr>
      <th>0</th>
      <td>CX600-X3</td>
    </tr>
    <tr>
      <th>5</th>
      <td>CX600-X8</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Dummy Device</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Eudemon1000E-U6</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Eudemon8160E</td>
    </tr>
    <tr>
      <th>8</th>
      <td>NE40E-X3</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NE40E-X8A(V8)</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de Subnet:


```python
Catalogo_subnet=pd.DataFrame(df_1.subnet.unique())
Catalogo_subnet.columns=['subnet']

Catalogo_subnet.reset_index(drop=True)
Catalogo_subnet.dropna(inplace=True)
Catalogo_subnet.sort_values(by='subnet').head(10)
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
      <th>subnet</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>110</th>
      <td>ACA-MTX - SWITCH</td>
    </tr>
    <tr>
      <th>476</th>
      <td>AGS-062 - INDUSTRIAL (COLLOCATE SW)</td>
    </tr>
    <tr>
      <th>383</th>
      <td>AGUAGU0006 - MONTE BELLO</td>
    </tr>
    <tr>
      <th>375</th>
      <td>AGUAGU0008 - CAMPESTRE</td>
    </tr>
    <tr>
      <th>468</th>
      <td>AGUAGU0011 - Las Hadas</td>
    </tr>
    <tr>
      <th>360</th>
      <td>AGUAGU0013 - AGUASCALIENTES SURESTE / PERCEO</td>
    </tr>
    <tr>
      <th>367</th>
      <td>AGUAGU0025 - ESTRELLA</td>
    </tr>
    <tr>
      <th>381</th>
      <td>AGUAGU0033 - PIRULES</td>
    </tr>
    <tr>
      <th>274</th>
      <td>Anillo Fronterizo SDH</td>
    </tr>
    <tr>
      <th>89</th>
      <td>BB071M - TELMEX IXTAPA</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de Patch version:


```python
Catalogo_patch=pd.DataFrame(df_1.patch_version_list.unique())
Catalogo_patch.columns=['patch_version_list']

#Remover los sucios
#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios.

Catalogo_patch.reset_index(drop=True)
Catalogo_patch.dropna(inplace=True)
Catalogo_patch.sort_values(by='patch_version_list').head(10)
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
      <th>patch_version_list</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>20</th>
      <td>SPC001 SPH006</td>
    </tr>
    <tr>
      <th>21</th>
      <td>SPC002</td>
    </tr>
    <tr>
      <th>10</th>
      <td>SPC100 SPH011</td>
    </tr>
    <tr>
      <th>18</th>
      <td>SPC160</td>
    </tr>
    <tr>
      <th>12</th>
      <td>SPC200</td>
    </tr>
    <tr>
      <th>15</th>
      <td>SPC200 SPH002</td>
    </tr>
    <tr>
      <th>11</th>
      <td>SPC235 SPH238</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SPC300</td>
    </tr>
    <tr>
      <th>14</th>
      <td>SPC300 SPH063</td>
    </tr>
    <tr>
      <th>0</th>
      <td>SPC300 SPH088</td>
    </tr>
  </tbody>
</table>
</div>



## 2.6 Preparación de los datos

Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos: 


* Se eliminan los siguientes caracteres especiales:    '-','#','%','/','_'
* Pasar todo a uppercase



```python
df_1['trazabilidad']=0
df_1.trazabilidad.loc[(df_1.serie_cleaned==0) ]=1
```


```python
df_1.dtypes
```




    ne_name                object
    ne_type                object
    ne_ip_address          object
    ne_mac_address         object
    ne_id                  object
    software_version       object
    physical_location      object
    create_time            object
    fibercable_count       object
    running_status         object
    subnet                 object
    subnet_path            object
    alias                  object
    remarks                object
    patch_version_list     object
    customized_column     float64
    lsr_id                 object
    maintenance_status     object
    gateway_type           object
    gateway                object
    optical_ne            float64
    subrack_type           object
    conference_call        object
    orderwire_phone        object
    ne_subtype             object
    filedate                int64
    filename               object
    fileip                 object
    hash_id                object
    sourceid               object
    registry_state         object
    datasetname            object
    timestamp               int64
    transaction_status     object
    year                    int64
    month                   int64
    day                     int64
    serie_cleaned           int64
    trazabilidad            int64
    dtype: object



##  7.1 Métricas KPI

Se mostrarán los KPIs generados.

#### Total de elementos:


```python
Total_Elementos=df_1.shape[0]
Total_Elementos
```




    8219




```python
df_1.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables

No hay elementos trazables por no tener campos con el número de serie o de activo.

#### Total Elementos NO Trazables


```python
Total_NOTr=Total_Elementos
Total_NOTr
```




    8219



###  KPIS


```python
KPIs_1=pd.DataFrame({'KPI':['Total Elementos','Total NO Trazables'],
                  'Resultado':[Total_Elementos,Total_NOTr]})

KPIs_1
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
      <td>8219</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total NO Trazables</td>
      <td>8219</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_hive_kpis = spark.createDataFrame(KPIs_1)
```


```python
df_hive_kpis_final = df_hive_kpis.withColumn("filedate",lit(20191113)).withColumn("year",lit(2019)).withColumn("month",lit(11)).withColumn("day",lit(13))
```


```python
df_hive_kpis_final.write.mode("overwrite").saveAsTable("rci_network_db.kpi_u2000_tx_ne")
```

# 3. Subrack Report 

## 3.1 Recolección de los datos:

Se crea el dataframe de spark


```python
 df_load_2 =spark.sql("select * from tx_fbb_u2000_subrack where year = 2019 and month = 11 and day = 13").limit(400000).cache()
```


```python
df_pre_2 = df_load_2.withColumn("serie_cleaned",validate_rule_udf(col("snbar_code"))).cache()
```


```python
df_pre_2.printSchema()
```

    root
     |-- ne: string (nullable = true)
     |-- subrack_name: string (nullable = true)
     |-- subrack_type: string (nullable = true)
     |-- subrack_id: string (nullable = true)
     |-- software_version: string (nullable = true)
     |-- ne_id: string (nullable = true)
     |-- alias: string (nullable = true)
     |-- subrack_status: string (nullable = true)
     |-- snbar_code: string (nullable = true)
     |-- telecommunications_room: string (nullable = true)
     |-- rack: string (nullable = true)
     |-- subrack_no: string (nullable = true)
     |-- pnbom_codeitem: string (nullable = true)
     |-- description: string (nullable = true)
     |-- manufacture_date: string (nullable = true)
     |-- subnet: string (nullable = true)
     |-- subnet_path: string (nullable = true)
     |-- equipment_no: string (nullable = true)
     |-- remarks: string (nullable = true)
     |-- customized_column: string (nullable = true)
     |-- filedate: long (nullable = true)
     |-- filename: string (nullable = true)
     |-- fileip: string (nullable = true)
     |-- hash_id: string (nullable = true)
     |-- sourceid: string (nullable = true)
     |-- registry_state: string (nullable = true)
     |-- datasetname: string (nullable = true)
     |-- timestamp: long (nullable = true)
     |-- transaction_status: string (nullable = true)
     |-- year: integer (nullable = true)
     |-- month: integer (nullable = true)
     |-- day: integer (nullable = true)
     |-- serie_cleaned: integer (nullable = true)
    



```python
df_pre_2.columns
```




    ['ne',
     'subrack_name',
     'subrack_type',
     'subrack_id',
     'software_version',
     'ne_id',
     'alias',
     'subrack_status',
     'snbar_code',
     'telecommunications_room',
     'rack',
     'subrack_no',
     'pnbom_codeitem',
     'description',
     'manufacture_date',
     'subnet',
     'subnet_path',
     'equipment_no',
     'remarks',
     'customized_column',
     'filedate',
     'filename',
     'fileip',
     'hash_id',
     'sourceid',
     'registry_state',
     'datasetname',
     'timestamp',
     'transaction_status',
     'year',
     'month',
     'day',
     'serie_cleaned']




```python
df_2 = df_pre_2.toPandas()
```

Una muestra de la fuente *tx_fbb_u2000_subrack*


```python
df_2.head(5)
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
      <th>ne</th>
      <th>subrack_name</th>
      <th>subrack_type</th>
      <th>subrack_id</th>
      <th>software_version</th>
      <th>ne_id</th>
      <th>alias</th>
      <th>subrack_status</th>
      <th>snbar_code</th>
      <th>telecommunications_room</th>
      <th>...</th>
      <th>hash_id</th>
      <th>sourceid</th>
      <th>registry_state</th>
      <th>datasetname</th>
      <th>timestamp</th>
      <th>transaction_status</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MXSINCUL0451MW01</td>
      <td>MXSINCUL0451MW01</td>
      <td>OptiX RTN 980 Subrack</td>
      <td>--</td>
      <td>V100R008C10SPC300</td>
      <td>21-150</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>03f07aa07bbcc3362cf1fd6dd95c141e858a9f4adc45bc...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:28:26</td>
      <td>Subrack_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MXBCNTIJ0164MW01</td>
      <td>MXBCNTIJ0164MW01</td>
      <td>OptiX RTN 950A Subrack Type II</td>
      <td>--</td>
      <td>V100R008C10SPC300</td>
      <td>11-110</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>7b9b47eeab2fc090b1865e42b3f15be61bcaf5499099df...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:28:26</td>
      <td>Subrack_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MXBCNMXC6002MW01</td>
      <td>MXBCNMXC6002MW01</td>
      <td>OptiX RTN 910 Subrack Type II</td>
      <td>--</td>
      <td>V100R006C00SPC200</td>
      <td>11-53</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>d9fc868b5797c553e65bdc39d52caf15fdb4054d07b6e8...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:28:26</td>
      <td>Subrack_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MXSINCUL0483MW01</td>
      <td>MXSINCUL0483MW01</td>
      <td>OptiX RTN 950A Subrack Type II</td>
      <td>--</td>
      <td>V100R008C10SPC300</td>
      <td>21-156</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>aa4a9daaf52b1a58e5c83d143c24bc87866061a0db2b9e...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:28:26</td>
      <td>Subrack_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MXSONMGD0768MW01</td>
      <td>MXSONMGD0768MW01</td>
      <td>OptiX RTN 950A Subrack Type II</td>
      <td>--</td>
      <td>V100R008C10SPC300</td>
      <td>21-394</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>b0c4349207e1d94118054a0741571b91b52f197727b294...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:28:26</td>
      <td>Subrack_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 33 columns</p>
</div>



### Diccionario de Datos

* **cobts_mbts**: Pendiente.
* **cobts_manufacturerdata**: Pendiente.
* **cobts_boardname**: Nombre del tablero.
* **cobts_serialnumber**: Numero de Serie.
* **cobts_boardtype**: Tipo de tablero.
* **cobts_filedate**: Fecha de carga del archivo fuente.
* **cobts_filename**: Nombre del archivo fuente.
* **cobts_hash_id**: Identificador único hash de la fuente.
* **cobts_sourceid**: Fuente de archivo.
* **cobts_registry_state**: Timestamp de carga.
* **cobts_datasetname**: Nombre indentificador de la fuente.
* **cobts_transaction_status**: Estado de la transaccion.
* **cobts_year**: Año de la partición.
* **cobts_month**:  Mes de la partición.
* **cobts_day**: Día de la partición.
* **bts_bts**: Pendiente.
* **bts_serial_number_count**: Conteo de Numero de serie.
* **bts_site**: Sitio.
* **bts_manufacturerdata**: Pendiente.
* **bts_sheet_name**: Nombre del sheet.
* **bts_boardname**: Nombre del tablero.
* **bts_serialnumber**: Numero de serie.
* **bts_boardtype**: Pendiente, podria ser tipo de tablero.
* **bts_filedate**: Fecha de carga del archivo fuente.
* **bts_filename**: Nombre del archivo fuente.
* **bts_hash_id**: Identificador único hash de la fuente.
* **bts_sourceid**: Fuente de archivo.
* **bts_registry_state**: Timestamp de carga.
* **bts_datasetname**: Nombre indentificador de la fuente.
* **bts_transaction_status**: Estatus de registro.
* **bts_year**: Año de la partición.
* **bts_month**: Mes de la partición.
* **bts_day**: Día de la partición.
* **serie_cleaned**: Filtro aplicado de acuerdo a las reglas.


## 3.2 Descripción de las fuentes


```python
campos=df_2.columns
print('Columnas de la fuente Subrack Report son: ',list(campos))
pd.DataFrame(df_2.dtypes,columns=['Tipo de objeto Subrack Report'])
```

    ('Columnas de la fuente Subrack Report son: ', ['ne', 'subrack_name', 'subrack_type', 'subrack_id', 'software_version', 'ne_id', 'alias', 'subrack_status', 'snbar_code', 'telecommunications_room', 'rack', 'subrack_no', 'pnbom_codeitem', 'description', 'manufacture_date', 'subnet', 'subnet_path', 'equipment_no', 'remarks', 'customized_column', 'filedate', 'filename', 'fileip', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie_cleaned'])





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
      <th>Tipo de objeto Subrack Report</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ne</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subrack_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subrack_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subrack_status</th>
      <td>object</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>object</td>
    </tr>
    <tr>
      <th>telecommunications_room</th>
      <td>object</td>
    </tr>
    <tr>
      <th>rack</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subrack_no</th>
      <td>object</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>object</td>
    </tr>
    <tr>
      <th>description</th>
      <td>object</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subnet</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subnet_path</th>
      <td>object</td>
    </tr>
    <tr>
      <th>equipment_no</th>
      <td>object</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>object</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>object</td>
    </tr>
    <tr>
      <th>filedate</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>filename</th>
      <td>object</td>
    </tr>
    <tr>
      <th>fileip</th>
      <td>object</td>
    </tr>
    <tr>
      <th>hash_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sourceid</th>
      <td>object</td>
    </tr>
    <tr>
      <th>registry_state</th>
      <td>object</td>
    </tr>
    <tr>
      <th>datasetname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>timestamp</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>transaction_status</th>
      <td>object</td>
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
print('renglones = ',df_2.shape[0],' columnas = ',df_2.shape[1])
```

    ('renglones = ', 8134, ' columnas = ', 33)



```python
NOrelevantes_2 =['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'fileip', 'timestamp',
              'transaction_status', 'year', 'month', 'day']

relevantes_2=[v for v in df_2.columns if v not in NOrelevantes_2]

df_2[relevantes_2].describe(include='all')
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
      <th>ne</th>
      <th>subrack_name</th>
      <th>subrack_type</th>
      <th>subrack_id</th>
      <th>software_version</th>
      <th>ne_id</th>
      <th>alias</th>
      <th>subrack_status</th>
      <th>snbar_code</th>
      <th>telecommunications_room</th>
      <th>...</th>
      <th>subrack_no</th>
      <th>pnbom_codeitem</th>
      <th>description</th>
      <th>manufacture_date</th>
      <th>subnet</th>
      <th>subnet_path</th>
      <th>equipment_no</th>
      <th>remarks</th>
      <th>customized_column</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>...</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134</td>
      <td>8134.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>8107</td>
      <td>7553</td>
      <td>33</td>
      <td>4</td>
      <td>35</td>
      <td>7585</td>
      <td>2</td>
      <td>3</td>
      <td>356</td>
      <td>1</td>
      <td>...</td>
      <td>1</td>
      <td>5</td>
      <td>12</td>
      <td>44</td>
      <td>612</td>
      <td>617</td>
      <td>1</td>
      <td>4805</td>
      <td>1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>MXDIFALO0076L7CPRI01</td>
      <td>CX600-X3 frame</td>
      <td>OptiX RTN 950 Subrack Type II</td>
      <td>--</td>
      <td>V100R008C10SPC200</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>HMEX0427 - AV. CENTRAL</td>
      <td>Physical Root/AT&amp;T R9/Mexico/R1 Mexico/HMEX042...</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>3</td>
      <td>234</td>
      <td>3481</td>
      <td>7561</td>
      <td>4821</td>
      <td>492</td>
      <td>7606</td>
      <td>7596</td>
      <td>7739</td>
      <td>8134</td>
      <td>...</td>
      <td>8134</td>
      <td>8016</td>
      <td>7561</td>
      <td>8014</td>
      <td>56</td>
      <td>56</td>
      <td>8134</td>
      <td>1702</td>
      <td>8134</td>
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
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.044259</td>
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
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.205682</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
<p>11 rows × 21 columns</p>
</div>




```python
df_2["subrack_name"].unique()
```




    array([u'MXSINCUL0451MW01', u'MXBCNTIJ0164MW01', u'MXBCNMXC6002MW01', ...,
           u'MXMEXTOL0780MW01', u'MXHMEX0048MW01', u'MXMEXTLB0738MW01'],
          dtype=object)



## 3.3 Exploración de los datos


```python
df_2.replace('null',np.NaN,inplace=True)
df_2.replace('NA',np.NaN,inplace=True)
df_2.replace('NULL',np.NaN,inplace=True)
df_2.replace('<NULL>',np.NaN,inplace=True)
df_2.replace('na',np.NaN,inplace=True)
df_2.replace('',np.NaN,inplace=True)
df_2.replace(' ',np.NaN,inplace=True)
df_2.replace('--',np.NaN,inplace=True)
df_2.replace('-',np.NaN,inplace=True)
df_2.replace('NAN',np.NaN,inplace=True)
```


```python
df_2["description"].unique()
```




    array([nan, u'CX600-X3 frame', u'CX600-X1 frame', u'CX600-X8 frame',
           u'CX600-X16 frame', u'Eudemon1000E-U6', u'NE40E-3 frame',
           u'Assembling Components,NetEngine40E,CR5B0BKP0871,NE40E-X8A Integrated Chassis DC Components (Including 2 Fan Tray)',
           u'TSR_WHOLE frame', u'Quidway S5300 Routing Switch',
           u'Quidway SVN3000'], dtype=object)



### Primer Catálogo: Subrack Type


```python
#Revisamos frecuencias:
subrack_type =pd.DataFrame(df_2.subrack_type.value_counts())
#print campo_rnc['rnc'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
netype.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'subrack type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma subrack type')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

subrack_type['subrack_type'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción por subrack_type',y=1.12)
ax1.axis('equal')
ax1.legend(labels=subrack_type.index,loc='upper left')

plt.show()

```


![png](output_189_0.png)


### Segundo Catálogo: Subnet


```python
#Revisamos frecuencias:
subnet =pd.DataFrame(df_2.subnet.value_counts()[:15])
#print campo_rnc['rnc'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
netype.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Subnet')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Top 15 Subnet')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

subnet['subnet'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción Top 15 por Subnet',y=1.12)
ax1.axis('equal')
ax1.legend(labels=subnet.index,loc='upper left')

plt.show()

```


![png](output_191_0.png)


### Tercer Catálogo: Subnet Path


```python
#Revisamos frecuencias:
subnet_path =pd.DataFrame(df_2.subnet_path.value_counts()[:15])
#print campo_rnc['rnc'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
subnet_path.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Subnet Path')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Top 15 Subnet Path')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

subnet_path['subnet_path'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción Top 15 por Subnet Path',y=1.12)
ax1.axis('equal')
ax1.legend(labels=subnet_path.index,loc='upper left')

plt.show()

```


![png](output_193_0.png)


### Cuarto Catálogo: Subrack Name


```python
#Revisamos frecuencias:
subrack_name =pd.DataFrame(df_2.subrack_name.value_counts()[:15])
#print campo_rnc['rnc'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
netype.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'subrack name')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Top 15 Subrack Name')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

subrack_name['subrack_name'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción Top 15 por Subrack Name',y=1.12)
ax1.axis('equal')
ax1.legend(labels=subrack_name.index,loc='upper left')

plt.show()

```


![png](output_195_0.png)


### Quinto Catálogo: Software Version


```python
#Revisamos frecuencias:
campo_software =pd.DataFrame(df_2.software_version.value_counts()[:15])
#print campo_rnc['rnc'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_software.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Software Version')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Top 15 Software version')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_software['software_version'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción Top 15 por Software Name',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_software.index,loc='upper left')

plt.show()

```


![png](output_197_0.png)


## 3.4 Calidad de los datos

#### Visualización de los datos de trazabilidad: 

Creamos una tabla donde se observarán los número de serie repetidos para un mejor análisis.


```python
pd.DataFrame(df_2.snbar_code.value_counts()[:15])
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
      <th>snbar_code</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2102350AFWP0GB000137</th>
      <td>2</td>
    </tr>
    <tr>
      <th>2102350AFWP0G7000032</th>
      <td>2</td>
    </tr>
    <tr>
      <th>2102350AFWP0GB000224</th>
      <td>2</td>
    </tr>
    <tr>
      <th>2102350AFWP0GB000175</th>
      <td>2</td>
    </tr>
    <tr>
      <th>2102350AFWP0GB000204</th>
      <td>2</td>
    </tr>
    <tr>
      <th>2102350AFWP0G7000024</th>
      <td>2</td>
    </tr>
    <tr>
      <th>2102351598P0C4000059</th>
      <td>1</td>
    </tr>
    <tr>
      <th>210235230610D7000169</th>
      <td>1</td>
    </tr>
    <tr>
      <th>2102351932P0C1000243</th>
      <td>1</td>
    </tr>
    <tr>
      <th>2102351932P0B3000090</th>
      <td>1</td>
    </tr>
    <tr>
      <th>2102351932P0C1000132</th>
      <td>1</td>
    </tr>
    <tr>
      <th>210235230610C6000284</th>
      <td>1</td>
    </tr>
    <tr>
      <th>210235230610D1000125</th>
      <td>1</td>
    </tr>
    <tr>
      <th>210235230610C6000287</th>
      <td>1</td>
    </tr>
    <tr>
      <th>2102351932P0B2000065</th>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
nas=df_2[relevantes_2].isna().sum()
porcentaje_nas=nas/df_2[relevantes_2].isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de NAs por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 21), ('counts_nas', 21)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="851f569e-04ed-4dcd-acba-f3caf2712790"></div>








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
      <th>ne</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subrack_name</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subrack_id</th>
      <td>92.955495</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>0.036882</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>6.048685</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subrack_status</th>
      <td>93.385788</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>95.574133</td>
    </tr>
    <tr>
      <th>telecommunications_room</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>rack</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subrack_no</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>98.979592</td>
    </tr>
    <tr>
      <th>description</th>
      <td>93.385788</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>98.955004</td>
    </tr>
    <tr>
      <th>subnet</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subnet_path</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>equipment_no</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>21.047455</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>



####  Visualización de datos NOT NULL:



```python
notmiss=(1-porcentaje_nas)*100

columnas=list(notmiss.keys())
counts_nas=list(notmiss.values)

#Mismo aplica aquí para color
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 21), ('counts_nas', 21)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="42b5c7ca-cf76-4953-b373-5d70f6b2cbfe"></div>








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
      <th>ne</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subrack_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subrack_id</th>
      <td>7.044505</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>99.963118</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>93.951315</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subrack_status</th>
      <td>6.614212</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>4.425867</td>
    </tr>
    <tr>
      <th>telecommunications_room</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>rack</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subrack_no</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>1.020408</td>
    </tr>
    <tr>
      <th>description</th>
      <td>6.614212</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>1.044996</td>
    </tr>
    <tr>
      <th>subnet</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subnet_path</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>equipment_no</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>78.952545</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_2[relevantes_2].head(5)
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
      <th>ne</th>
      <th>subrack_name</th>
      <th>subrack_type</th>
      <th>subrack_id</th>
      <th>software_version</th>
      <th>ne_id</th>
      <th>alias</th>
      <th>subrack_status</th>
      <th>snbar_code</th>
      <th>telecommunications_room</th>
      <th>...</th>
      <th>subrack_no</th>
      <th>pnbom_codeitem</th>
      <th>description</th>
      <th>manufacture_date</th>
      <th>subnet</th>
      <th>subnet_path</th>
      <th>equipment_no</th>
      <th>remarks</th>
      <th>customized_column</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MXSINCUL0451MW01</td>
      <td>MXSINCUL0451MW01</td>
      <td>OptiX RTN 980 Subrack</td>
      <td>NaN</td>
      <td>V100R008C10SPC300</td>
      <td>21-150</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>SINCUL0451 - Francisco I Madero</td>
      <td>Physical Root/AT&amp;T/R2/SINALOA/Culiacan/SINCUL0...</td>
      <td>NaN</td>
      <td>FRANCISCO I MADERO</td>
      <td>NaN</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MXBCNTIJ0164MW01</td>
      <td>MXBCNTIJ0164MW01</td>
      <td>OptiX RTN 950A Subrack Type II</td>
      <td>NaN</td>
      <td>V100R008C10SPC300</td>
      <td>11-110</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>BCNTIJ0179 Marmol</td>
      <td>Physical Root/AT&amp;T/R1/BAJA CALIFORNIA NORTE/BC...</td>
      <td>NaN</td>
      <td>Deshuesadero</td>
      <td>NaN</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MXBCNMXC6002MW01</td>
      <td>MXBCNMXC6002MW01</td>
      <td>OptiX RTN 910 Subrack Type II</td>
      <td>NaN</td>
      <td>V100R006C00SPC200</td>
      <td>11-53</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>BCNMXC0046 - CABALLITO</td>
      <td>Physical Root/AT&amp;T/R1/BAJA CALIFORNIA NORTE/Me...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MXSINCUL0483MW01</td>
      <td>MXSINCUL0483MW01</td>
      <td>OptiX RTN 950A Subrack Type II</td>
      <td>NaN</td>
      <td>V100R008C10SPC300</td>
      <td>21-156</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>SINCUL0451 - Francisco I Madero</td>
      <td>Physical Root/AT&amp;T/R2/SINALOA/Culiacan/SINCUL0...</td>
      <td>NaN</td>
      <td>CALAGUA</td>
      <td>NaN</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MXSONMGD0768MW01</td>
      <td>MXSONMGD0768MW01</td>
      <td>OptiX RTN 950A Subrack Type II</td>
      <td>NaN</td>
      <td>V100R008C10SPC300</td>
      <td>21-394</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>SONSAN0809 - SANTA ANA</td>
      <td>Physical Root/AT&amp;T/R2/SONORA/R2 Nogales/SONSAN...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>



## 3.5 Catálogos

#### Catálogo Subrack Type:


```python
Catalogo_subrack_type = pd.DataFrame(df_2.subrack_type.unique())
Catalogo_subrack_type.columns=['subrack_type']
#Remover los sucios

#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios.
Catalogo_subrack_type.reset_index(drop=True)
Catalogo_subrack_type.dropna(inplace=True)
Catalogo_subrack_type.sort_values(by='subrack_type').head(10)
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
      <th>subrack_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10</th>
      <td>CX600-X1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>CX600-X16</td>
    </tr>
    <tr>
      <th>9</th>
      <td>CX600-X3</td>
    </tr>
    <tr>
      <th>11</th>
      <td>CX600-X8</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Eudemon1000E</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NE40E-X3</td>
    </tr>
    <tr>
      <th>14</th>
      <td>NE40E-X3 DC</td>
    </tr>
    <tr>
      <th>16</th>
      <td>NE80E_NE5000E</td>
    </tr>
    <tr>
      <th>26</th>
      <td>OptiX Metro 1000V3 Subrack Type I</td>
    </tr>
    <tr>
      <th>25</th>
      <td>OptiX Metro 1050 Subrack Type I</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Subrack Name:


```python
Catalogo_subrack_name = pd.DataFrame(df_2.subrack_name.unique())
Catalogo_subrack_name.columns=['subrack_name']
#Remover los sucios

#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios.
Catalogo_subrack_name.reset_index(drop=True)
Catalogo_subrack_name.dropna(inplace=True)
Catalogo_subrack_name.sort_values(by='subrack_name').head(10)
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
      <th>subrack_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>6589</th>
      <td>401-Nuevo Laredo</td>
    </tr>
    <tr>
      <th>6590</th>
      <td>402-Monterrey-1</td>
    </tr>
    <tr>
      <th>6588</th>
      <td>403-Monterrey-2</td>
    </tr>
    <tr>
      <th>6591</th>
      <td>405-Reynosa</td>
    </tr>
    <tr>
      <th>6220</th>
      <td>43-MTY Core</td>
    </tr>
    <tr>
      <th>6586</th>
      <td>44-Passport-MTY-02</td>
    </tr>
    <tr>
      <th>6471</th>
      <td>938-Vista Hermosa</td>
    </tr>
    <tr>
      <th>2801</th>
      <td>AEROPUERTO-DIR. CLUB DE CAZA</td>
    </tr>
    <tr>
      <th>7313</th>
      <td>ALTZOMONI-MSO REVOLUCION</td>
    </tr>
    <tr>
      <th>7314</th>
      <td>ALTZOMONI-SAN ALFONSO</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Subnet:


```python
Catalogo_subnet = pd.DataFrame(df_2.subnet.unique())
Catalogo_subnet.columns=['subnet']
#Remover los sucios

#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios.
Catalogo_subnet.reset_index(drop=True)
Catalogo_subnet.dropna(inplace=True)
Catalogo_subnet.sort_values(by='subnet').head(10)
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
      <th>subnet</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>430</th>
      <td>ACA-MTX - SWITCH</td>
    </tr>
    <tr>
      <th>287</th>
      <td>AGS-062 - INDUSTRIAL (COLLOCATE SW)</td>
    </tr>
    <tr>
      <th>194</th>
      <td>AGUAGU0006 - MONTE BELLO</td>
    </tr>
    <tr>
      <th>184</th>
      <td>AGUAGU0008 - CAMPESTRE</td>
    </tr>
    <tr>
      <th>279</th>
      <td>AGUAGU0011 - Las Hadas</td>
    </tr>
    <tr>
      <th>169</th>
      <td>AGUAGU0013 - AGUASCALIENTES SURESTE / PERCEO</td>
    </tr>
    <tr>
      <th>176</th>
      <td>AGUAGU0025 - ESTRELLA</td>
    </tr>
    <tr>
      <th>191</th>
      <td>AGUAGU0033 - PIRULES</td>
    </tr>
    <tr>
      <th>566</th>
      <td>Anillo Fronterizo SDH</td>
    </tr>
    <tr>
      <th>409</th>
      <td>BB071M - TELMEX IXTAPA</td>
    </tr>
  </tbody>
</table>
</div>



## 3.6  Preparación de los datos


```python
df_2.dtypes
```




    ne                          object
    subrack_name                object
    subrack_type                object
    subrack_id                  object
    software_version            object
    ne_id                       object
    alias                      float64
    subrack_status              object
    snbar_code                  object
    telecommunications_room    float64
    rack                       float64
    subrack_no                 float64
    pnbom_codeitem              object
    description                 object
    manufacture_date            object
    subnet                      object
    subnet_path                 object
    equipment_no               float64
    remarks                     object
    customized_column          float64
    filedate                     int64
    filename                    object
    fileip                      object
    hash_id                     object
    sourceid                    object
    registry_state              object
    datasetname                 object
    timestamp                    int64
    transaction_status          object
    year                         int64
    month                        int64
    day                          int64
    serie_cleaned                int64
    dtype: object




```python
df_2['trazabilidad']=0
df_2.trazabilidad.loc[(df_2.serie_cleaned==0) ]=1
```


```python
mySchema_2 = StructType([ StructField("cobts_mbts", StringType(), True)\
                       ,StructField("cobts_manufacturerdata", StringType(), True)\
                       ,StructField("cobts_boardname", StringType(), True)\
                       ,StructField("cobts_serialnumber", StringType(), True)\
                       ,StructField("cobts_boardtype", StringType(), True)\
                       ,StructField("cobts_filedate", IntegerType(), True)\
                       ,StructField("cobts_filename", StringType(), True)\
                       ,StructField("cobts_hash_id", StringType(), True)\
                       ,StructField("cobts_sourceid", StringType(), True)\
                       ,StructField("cobts_registry_state", StringType(), True)\
                       ,StructField("cobts_datasetname", StringType(), True)\
                       ,StructField("cobts_transaction_status", StringType(), True)\
                       ,StructField("cobts_year", IntegerType(), True)\
                       ,StructField("cobts_month", IntegerType(), True)\
                       ,StructField("cobts_day", IntegerType(), True)\
                       ,StructField("bts_bts", StringType(), True)\
                       ,StructField("bts_serial_number_count", StringType(), True)\
                       ,StructField("bts_site", StringType(), True)\
                       ,StructField("bts_manufacturerdata", StringType(), True)\
                       ,StructField("bts_sheet_name", StringType(), True)\
                       ,StructField("bts_boardname", StringType(), True)\
                       ,StructField("bts_serialnumber", StringType(), True)\
                       ,StructField("bts_boardtype", StringType(), True)\
                       ,StructField("bts_filedate", IntegerType(), True)\
                        ,StructField("bts_filename", StringType(), True)\
                       ,StructField("bts_hash_id", StringType(), True)\
                       ,StructField("bts_sourceid", StringType(), True)\
                       ,StructField("bts_registry_state", StringType(), True)\
                       ,StructField("bts_datasetname", StringType(), True)\
                       ,StructField("bts_transaction_status", StringType(), True)\
                       ,StructField("bts_year", IntegerType(), True)\
                       ,StructField("bts_month", IntegerType(), True)\
                       ,StructField("bts_day", IntegerType(), True)\
                        ,StructField("serie_cleaned", IntegerType(), True)\
                       ,StructField("trazabilidad", IntegerType(), True)\
                       ,StructField("CS_CA", IntegerType(), True)\
                       ,StructField("CS_SA", IntegerType(), True)\
                       ,StructField("SS_CA", IntegerType(), True)])
```

## 7.3  Métricas KPI.


```python
Total_Elementos=df_2.shape[0]
Total_Elementos
```




    8134




```python
df_2.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables



```python
Total_Tr=df_2.loc[(df_2.snbar_code!='vacio') ].shape[0]
Total_Tr
```




    360



#### Total Elementos NO Trazables



```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    7774



#### Total Elementos Trazables Únicos



```python
Total_Tr_Unic=df_2[['snbar_code']].loc[(df_2.snbar_code!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic
```




    354



#### Total de elementos trazables duplicados



```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    6



###  KPIS


```python
KPIs_2=pd.DataFrame({'KPI':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos,Total_Tr,Total_NOTr,
                              Total_Tr_Unic,Total_Tr_Dupli]})

KPIs_2
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
      <td>8134</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>360</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>7774</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>354</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_hive_kpis = spark.createDataFrame(KPIs_2)
```


```python
df_hive_kpis_final = df_hive_kpis.withColumn("filedate",lit(20191113)).withColumn("year",lit(2019)).withColumn("month",lit(11)).withColumn("day",lit(13))
```


```python
df_hive_kpis_final.write.mode("overwrite").saveAsTable("rci_network_db.kpi_u2000_tx_subrack")
```

## 4. Optical Module

### 4.1 Recolección de los datos: 

Se crea el dataframe de spark:


```python
df_3 =spark.sql("select * from tx_fbb_u2000_optical_module where year = 2019 and month = 11 and day = 13")
```


```python
df_3.columns
```




    ['serial_no',
     'opticalelectrical_type',
     'ne_name',
     'port_name',
     'port_description',
     'port_type',
     'receive_optical_powerdbm',
     'reference_receive_optical_powerdbm',
     'reference_receive_time',
     'receive_status',
     'upper_threshold_for_receive_optical_powerdbm',
     'low_threshold_for_receive_optical_powerdbm',
     'transmit_optical_powerdbm',
     'reference_transmit_optical_powerdbm',
     'reference_transmit_time',
     'transmit_status',
     'upper_threshold_for_transmit_optical_powerdbm',
     'low_threshold_for_transmit_optical_powerdbm',
     'singlemodemultimode',
     'speedmbs',
     'wave_lengthnm',
     'transmission_distancem',
     'fiber_type',
     'pmanufacturer',
     'optical_mode_authentication',
     'port_remark',
     'port_custom_column',
     'opticaldirectiontype',
     'vendor_pn',
     'model',
     'revissue_number',
     'pnbom_codeitem',
     'filedate',
     'filename',
     'fileip',
     'hash_id',
     'sourceid',
     'registry_state',
     'datasetname',
     'timestamp',
     'transaction_status',
     'year',
     'month',
     'day']




```python
def validate_rule(string):
    
    search_list=[" ",'!','%','$',"<",">","^",'¡',"+","N/A",'¿','~','#','Ñ',"Ã","Åƒ","Ã‹","Ã³",'Ë','*','?',"ILEGIBLE", "VICIBLE","VISIBLE","INCOMPLETO"]
    test = u'%s' % (string)
    str_temp = test.decode('utf-8')
    if str_temp.upper() == "BORRADO":
      return 0
    elif len(str_temp) < 6:
      return 0
    elif any(ext.decode("utf-8") in str_temp.upper()for ext in search_list):
      return 0
    else:
      return 1
```

Se crea un udf en Spark sobre la función ya creada: 


```python
validate_rule_udf = udf(validate_rule, IntegerType())
```

Se le agrega una nueva columna al dataframe de spark; la nueva columna es la validacion de la columna serie con respecto al udf que creamos.


```python
df_3 = df_3.withColumn("serie_cleaned",validate_rule_udf(col("serial_no"))).cache()
```

Se convierte el dataframe de spark a un dataframe de pandas


```python
df_3 = df_3.toPandas()
```

Hemos recolectado los campos a analizar de la fuente U2000 GPON.


```python
df_3.head(5)
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
      <th>serial_no</th>
      <th>opticalelectrical_type</th>
      <th>ne_name</th>
      <th>port_name</th>
      <th>port_description</th>
      <th>port_type</th>
      <th>receive_optical_powerdbm</th>
      <th>reference_receive_optical_powerdbm</th>
      <th>reference_receive_time</th>
      <th>receive_status</th>
      <th>...</th>
      <th>hash_id</th>
      <th>sourceid</th>
      <th>registry_state</th>
      <th>datasetname</th>
      <th>timestamp</th>
      <th>transaction_status</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HA11040121534</td>
      <td>ESFP</td>
      <td>MXCMXM01RTCOREBH01</td>
      <td>GigabitEthernet1/1/1</td>
      <td>To-MXCMXM01RTCOREBH02-GE1/1/1</td>
      <td>Ethernet</td>
      <td>-6.1</td>
      <td></td>
      <td></td>
      <td>Normal</td>
      <td>...</td>
      <td>57153f8b33bacacd4469f23f99e050a78e47d8cccf3a67...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:39:22</td>
      <td>OpticalModule_Information</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>HA11040120147</td>
      <td>ESFP</td>
      <td>MXCMXM01RTCOREBH01</td>
      <td>GigabitEthernet1/1/2</td>
      <td>To-MXHMEX0172RTBHCSRMOB02-GE1/0/0-11138-ETH-19...</td>
      <td>Ethernet</td>
      <td>-7.13</td>
      <td></td>
      <td></td>
      <td>Normal</td>
      <td>...</td>
      <td>1c3b48e48d6f9a349ae0dd5e4cf2357e890bcdef1dc63e...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:39:22</td>
      <td>OpticalModule_Information</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>HA11040120150</td>
      <td>ESFP</td>
      <td>MXCMXM01RTCOREBH01</td>
      <td>GigabitEthernet1/1/3</td>
      <td></td>
      <td>Ethernet</td>
      <td>-8.76</td>
      <td></td>
      <td></td>
      <td>Normal</td>
      <td>...</td>
      <td>a56a65da81d56ba0e91bcee87f6a5911465fc17ed4b4ce...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:39:22</td>
      <td>OpticalModule_Information</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>HA11040120123</td>
      <td>ESFP</td>
      <td>MXCMXM01RTCOREBH01</td>
      <td>GigabitEthernet1/1/4</td>
      <td>To-MXDIFMGH0768RTBHCSRMOB02-GE1/0/0-11138-ETH-...</td>
      <td>Ethernet</td>
      <td>-6.48</td>
      <td></td>
      <td></td>
      <td>Normal</td>
      <td>...</td>
      <td>c7d163415f99335d6c722efd115b145c61acdf39faa7d3...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:39:22</td>
      <td>OpticalModule_Information</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>HA11040120131</td>
      <td>ESFP</td>
      <td>MXCMXM01RTCOREBH01</td>
      <td>GigabitEthernet1/1/5</td>
      <td>To-MXDIFBEJ0192RTBHCSRMOB02-GE1/0/0-11138-ETH-198</td>
      <td>Ethernet</td>
      <td>-8.01</td>
      <td></td>
      <td></td>
      <td>Normal</td>
      <td>...</td>
      <td>84bee632e6381ad51251d5d666db832e5c954b8b8f62b4...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:39:22</td>
      <td>OpticalModule_Information</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 45 columns</p>
</div>



### Diccionario de datos.
A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

* **ne**: ID del negocio.
* **board_name**: Familia de productos al que pertenece.
* **board_type**: Fecha de creacion, validar si es de carga.
* **ne_type**: Pendiente.
* **subrack_id**: Tipo de Software.
* **slot_id**: Pendiente, es un estatus.
* **hardware_version**: Versión del hardware del dispositivo.
* **software_version**: Versión del software del dispositivo.
* **snbar_code**: Numero de serie.
* **alias**: Nombre del sheet.
* **remarks**: Pendiente.
* **customized_column**: Pendiente.
* **ne_id**: Estado.
* **bios_version**: Versión del BIOS del dispositivo.
* **fpga_version**: Pendiente.
* **board_status**: Estado de servicio del dispositivo.
* **pnbom_codeitem**: Pendiente.
* **model**: Pendiente.
* **rev_issue_number**: Pendiente.
* **management**: Pendiente.
* **description**: Pendiente.
* **manufacture_date**: Fecha de fabricación del dispositivo.
* **create_time**: Pendiente.
* **filedate**: Fecha de carga del archivo fuente.
* **filename**: Nombre del archivo fuente.
* **hash_id**: Identificador único hash de la fuente.
* **source_id**: Fuente de archivo.
* **registry_state**: Timestamp de carga.
* **datasetname**: Nombre indentificador de la fuente.
* **timestamp**: Fecha de carga.
* **transaction_status**: Estatus de registro.
* **year**: Año de la partición.
* **month**: Mes de la partición.
* **day**: Día de la partición.

## 4.2. Descripción de las fuentes
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos=df_3.columns
print('Columnas de la fuente TX Optical son: ',list(campos))
pd.DataFrame(df.dtypes,columns=['Tipo de objeto TX Optical'])
```

    ('Columnas de la fuente TX Optical son: ', ['serial_no', 'opticalelectrical_type', 'ne_name', 'port_name', 'port_description', 'port_type', 'receive_optical_powerdbm', 'reference_receive_optical_powerdbm', 'reference_receive_time', 'receive_status', 'upper_threshold_for_receive_optical_powerdbm', 'low_threshold_for_receive_optical_powerdbm', 'transmit_optical_powerdbm', 'reference_transmit_optical_powerdbm', 'reference_transmit_time', 'transmit_status', 'upper_threshold_for_transmit_optical_powerdbm', 'low_threshold_for_transmit_optical_powerdbm', 'singlemodemultimode', 'speedmbs', 'wave_lengthnm', 'transmission_distancem', 'fiber_type', 'pmanufacturer', 'optical_mode_authentication', 'port_remark', 'port_custom_column', 'opticaldirectiontype', 'vendor_pn', 'model', 'revissue_number', 'pnbom_codeitem', 'filedate', 'filename', 'fileip', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie_cleaned'])





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
      <th>Tipo de objeto TX Optical</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ne</th>
      <td>object</td>
    </tr>
    <tr>
      <th>board_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>board_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subrack_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>slot_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>object</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>object</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>object</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bios_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>fpga_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>board_status</th>
      <td>object</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>object</td>
    </tr>
    <tr>
      <th>model</th>
      <td>object</td>
    </tr>
    <tr>
      <th>rev_issue_number</th>
      <td>object</td>
    </tr>
    <tr>
      <th>management</th>
      <td>object</td>
    </tr>
    <tr>
      <th>description</th>
      <td>object</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>object</td>
    </tr>
    <tr>
      <th>create_time</th>
      <td>object</td>
    </tr>
    <tr>
      <th>filedate</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>filename</th>
      <td>object</td>
    </tr>
    <tr>
      <th>fileip</th>
      <td>object</td>
    </tr>
    <tr>
      <th>hash_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sourceid</th>
      <td>object</td>
    </tr>
    <tr>
      <th>registry_state</th>
      <td>object</td>
    </tr>
    <tr>
      <th>datasetname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>timestamp</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>transaction_status</th>
      <td>object</td>
    </tr>
    <tr>
      <th>year</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>month</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>day</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>int64</td>
    </tr>
  </tbody>
</table>
</div>




```python
print('renglones = ',df_3.shape[0],' columnas = ',df_3.shape[1])
```

    ('renglones = ', 12352, ' columnas = ', 45)



```python
#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'fileip', 'datasetname', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes=[v for v in df_3.columns if v not in NOrelevantes]

df_3[relevantes].describe(include='all')
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
      <th>serial_no</th>
      <th>opticalelectrical_type</th>
      <th>ne_name</th>
      <th>port_name</th>
      <th>port_description</th>
      <th>port_type</th>
      <th>receive_optical_powerdbm</th>
      <th>reference_receive_optical_powerdbm</th>
      <th>reference_receive_time</th>
      <th>receive_status</th>
      <th>...</th>
      <th>pmanufacturer</th>
      <th>optical_mode_authentication</th>
      <th>port_remark</th>
      <th>port_custom_column</th>
      <th>opticaldirectiontype</th>
      <th>vendor_pn</th>
      <th>model</th>
      <th>revissue_number</th>
      <th>pnbom_codeitem</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>...</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352</td>
      <td>12352.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>12075</td>
      <td>8</td>
      <td>529</td>
      <td>456</td>
      <td>3568</td>
      <td>2</td>
      <td>1070</td>
      <td>2</td>
      <td>1</td>
      <td>4</td>
      <td>...</td>
      <td>35</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>3</td>
      <td>74</td>
      <td>2</td>
      <td>2</td>
      <td>4</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>1</td>
      <td>ESFP</td>
      <td>MXTLAM01RTCOREMOB08</td>
      <td>GigabitEthernet1/0/0</td>
      <td></td>
      <td>Ethernet</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>--</td>
      <td>...</td>
      <td>HG GENUINE</td>
      <td>Authenticated</td>
      <td></td>
      <td></td>
      <td>twoFiberBidirection</td>
      <td>MXPD-243S</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>96</td>
      <td>5959</td>
      <td>224</td>
      <td>215</td>
      <td>5655</td>
      <td>12091</td>
      <td>5486</td>
      <td>12104</td>
      <td>12352</td>
      <td>5486</td>
      <td>...</td>
      <td>4022</td>
      <td>11709</td>
      <td>12104</td>
      <td>12104</td>
      <td>6754</td>
      <td>3883</td>
      <td>12008</td>
      <td>12332</td>
      <td>12085</td>
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
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.989637</td>
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
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.101273</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
<p>11 rows × 33 columns</p>
</div>




```python
df_3["receive_status"].unique()
```




    array([u'Normal', u'Critical Alert', u'--', u'Warning Alert'],
          dtype=object)



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

Podemos identificar rápidamente que n entendibles a simple vista, sin embargo, nuestro conocimiento del negocio nos permite intuir que varias de estas columnas serán útiles en el futuro como son:
1. Optical/Electrical Type
2. Port Type
3. Receive Status
4. Manufacturer
5. Port Description

La columna *fileip* se inserta artificialmente a los datos durante la ingesta, por lo tanto no se considera para formar un catálogo.

## 4.3 Exploración de los datos
De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los catálogos.

Para empezar, se hará una limpieza general a los datos:


```python
df_3.replace('null',np.NaN,inplace=True)
df_3.replace('NA',np.NaN,inplace=True)
df_3.replace('NULL',np.NaN,inplace=True)
df_3.replace('<NULL>',np.NaN,inplace=True)
df_3.replace('NAN',np.NaN,inplace=True)
df_3.replace('na',np.NaN,inplace=True)
df_3.replace('',np.NaN,inplace=True)
df_3.replace(' ',np.NaN,inplace=True)
df_3.replace('--',np.NaN,inplace=True)
df_3.replace('-',np.NaN,inplace=True)
df_3.serial_no.replace('1',np.NaN,inplace=True)
#Se puede hacer más y por columna en caso de ser necesario
```

### Primer catálogo: *Optical/Electrical Type*

Empezaremos con el catálogo board Type. Este catalogo nos permite concer y agrupar los datos por medio del tipo de tarjeta de control del dispositivo de fibra óptica. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
campo_optical=pd.DataFrame(df_3.opticalelectrical_type.value_counts()[:15])

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_optical.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Optical Type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Optical Type')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_optical['opticalelectrical_type'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción Optical Type',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_optical.index,loc='upper left')

plt.show()
```


![png](output_258_0.png)


### Segundo catálogo: *Port Type*

Continuamos con el catálogo *port_type*. Este catalogo nos permite concer y agrupar los datos por medio del tipo de tarjeta de control del dispositivo de fibra óptica. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
campo_port_type=pd.DataFrame(df_3.port_type.value_counts()[:20])

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_port_type.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Port Type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Port Type')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_port_type['port_type'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción Port Type',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_port_type.index,loc='upper left')

plt.show()
```


![png](output_261_0.png)


### Tercer catálogo: *Receive Status*

Continuamos con el catálogo *receive status*. Este catalogo nos permite concer y agrupar los datos por medio del tipo de tarjeta de control del dispositivo de fibra óptica. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
campo_status = pd.DataFrame(df_3.receive_status.value_counts()[:20])

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_status.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Receive Status')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Receive Status')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_status['receive_status'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción Receive Status',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_status.index,loc='upper left')

plt.show()
```


![png](output_264_0.png)


### Cuarto catálogo: *Manufacturer*

Empezaremos con el catálogo hardware_version. Este catalogo nos permite concer y agrupar los datos por medio del tipo de tarjeta de control del dispositivo de fibra óptica. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
campo_manufacturer=pd.DataFrame(df_3.pmanufacturer.value_counts()[:20])

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_manufacturer.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Manufacturer')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Manufacturer')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_manufacturer['pmanufacturer'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción Manufacturer',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_manufacturer.index,loc='upper left')

plt.show()
```


![png](output_267_0.png)


### Quinto catálogo: *Port Description*

Empezaremos con el catálogo hardware_version. Este catalogo nos permite concer y agrupar los datos por medio del tipo de tarjeta de control del dispositivo de fibra óptica. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
campo_description=pd.DataFrame(df_3.port_description.value_counts()[:20])

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_description.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Manufacturer')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Top 20 Manufacturer')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_description['port_description'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción Top 20 Port Description',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_description.index,loc='upper left')

plt.show()
```


![png](output_270_0.png)


#### Visualización de los datos de trazabilidad:


```python
pd.DataFrame(df_3.serial_no.value_counts()[:15])
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
      <th>serial_no</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>AF1648F0011</th>
      <td>2</td>
    </tr>
    <tr>
      <th>AF1624F005H</th>
      <td>2</td>
    </tr>
    <tr>
      <th>E801-0876</th>
      <td>2</td>
    </tr>
    <tr>
      <th>FG44303006E6</th>
      <td>2</td>
    </tr>
    <tr>
      <th>INGBM0510749</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030SBF6TGB337450</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030SBF6TGB335740</th>
      <td>2</td>
    </tr>
    <tr>
      <th>FG45303006A3</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030SBF6TGB336390</th>
      <td>2</td>
    </tr>
    <tr>
      <th>INGBJ0497454</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030SBF6TGB326200</th>
      <td>2</td>
    </tr>
    <tr>
      <th>INGBJ0494915</th>
      <td>2</td>
    </tr>
    <tr>
      <th>AF1652F001V</th>
      <td>2</td>
    </tr>
    <tr>
      <th>INGBJ0497432</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030SBF6TF9200970</th>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



## 4.4 Calidad de los datos
Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.


```python
df_3.head(5)
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
      <th>serial_no</th>
      <th>opticalelectrical_type</th>
      <th>ne_name</th>
      <th>port_name</th>
      <th>port_description</th>
      <th>port_type</th>
      <th>receive_optical_powerdbm</th>
      <th>reference_receive_optical_powerdbm</th>
      <th>reference_receive_time</th>
      <th>receive_status</th>
      <th>...</th>
      <th>hash_id</th>
      <th>sourceid</th>
      <th>registry_state</th>
      <th>datasetname</th>
      <th>timestamp</th>
      <th>transaction_status</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HA11040121534</td>
      <td>ESFP</td>
      <td>MXCMXM01RTCOREBH01</td>
      <td>GigabitEthernet1/1/1</td>
      <td>To-MXCMXM01RTCOREBH02-GE1/1/1</td>
      <td>Ethernet</td>
      <td>-6.1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Normal</td>
      <td>...</td>
      <td>57153f8b33bacacd4469f23f99e050a78e47d8cccf3a67...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:39:22</td>
      <td>OpticalModule_Information</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>HA11040120147</td>
      <td>ESFP</td>
      <td>MXCMXM01RTCOREBH01</td>
      <td>GigabitEthernet1/1/2</td>
      <td>To-MXHMEX0172RTBHCSRMOB02-GE1/0/0-11138-ETH-19...</td>
      <td>Ethernet</td>
      <td>-7.13</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Normal</td>
      <td>...</td>
      <td>1c3b48e48d6f9a349ae0dd5e4cf2357e890bcdef1dc63e...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:39:22</td>
      <td>OpticalModule_Information</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>HA11040120150</td>
      <td>ESFP</td>
      <td>MXCMXM01RTCOREBH01</td>
      <td>GigabitEthernet1/1/3</td>
      <td>NaN</td>
      <td>Ethernet</td>
      <td>-8.76</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Normal</td>
      <td>...</td>
      <td>a56a65da81d56ba0e91bcee87f6a5911465fc17ed4b4ce...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:39:22</td>
      <td>OpticalModule_Information</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>HA11040120123</td>
      <td>ESFP</td>
      <td>MXCMXM01RTCOREBH01</td>
      <td>GigabitEthernet1/1/4</td>
      <td>To-MXDIFMGH0768RTBHCSRMOB02-GE1/0/0-11138-ETH-...</td>
      <td>Ethernet</td>
      <td>-6.48</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Normal</td>
      <td>...</td>
      <td>c7d163415f99335d6c722efd115b145c61acdf39faa7d3...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:39:22</td>
      <td>OpticalModule_Information</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>HA11040120131</td>
      <td>ESFP</td>
      <td>MXCMXM01RTCOREBH01</td>
      <td>GigabitEthernet1/1/5</td>
      <td>To-MXDIFBEJ0192RTBHCSRMOB02-GE1/0/0-11138-ETH-198</td>
      <td>Ethernet</td>
      <td>-8.01</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Normal</td>
      <td>...</td>
      <td>84bee632e6381ad51251d5d666db832e5c954b8b8f62b4...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:39:22</td>
      <td>OpticalModule_Information</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 45 columns</p>
</div>



### Missings Values
Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.


```python
nas=df_3[relevantes].isna().sum()
porcentaje_nas=nas/df_3[relevantes].isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de NAs por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 33), ('counts_nas', 33)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="844cae6a-81fa-4f4e-9796-c3199f2843d6"></div>








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
      <th>serial_no</th>
      <td>1.036269</td>
    </tr>
    <tr>
      <th>opticalelectrical_type</th>
      <td>1.036269</td>
    </tr>
    <tr>
      <th>ne_name</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>port_name</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>port_description</th>
      <td>45.782060</td>
    </tr>
    <tr>
      <th>port_type</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>receive_optical_powerdbm</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>reference_receive_optical_powerdbm</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>reference_receive_time</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>receive_status</th>
      <td>44.413860</td>
    </tr>
    <tr>
      <th>upper_threshold_for_receive_optical_powerdbm</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>low_threshold_for_receive_optical_powerdbm</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>transmit_optical_powerdbm</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>reference_transmit_optical_powerdbm</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>reference_transmit_time</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>transmit_status</th>
      <td>44.413860</td>
    </tr>
    <tr>
      <th>upper_threshold_for_transmit_optical_powerdbm</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>low_threshold_for_transmit_optical_powerdbm</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>singlemodemultimode</th>
      <td>44.146697</td>
    </tr>
    <tr>
      <th>speedmbs</th>
      <td>1.036269</td>
    </tr>
    <tr>
      <th>wave_lengthnm</th>
      <td>44.616256</td>
    </tr>
    <tr>
      <th>transmission_distancem</th>
      <td>0.777202</td>
    </tr>
    <tr>
      <th>fiber_type</th>
      <td>51.173899</td>
    </tr>
    <tr>
      <th>pmanufacturer</th>
      <td>0.259067</td>
    </tr>
    <tr>
      <th>optical_mode_authentication</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>port_remark</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>port_custom_column</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>opticaldirectiontype</th>
      <td>1.643459</td>
    </tr>
    <tr>
      <th>vendor_pn</th>
      <td>1.870142</td>
    </tr>
    <tr>
      <th>model</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>revissue_number</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>97.838407</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>



#### Visualización de datos NOT NULL: 


```python
notmiss=(1-porcentaje_nas)*100

columnas=list(notmiss.keys())
counts_nas=list(notmiss.values)

#Mismo aplica aquí para color
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 33), ('counts_nas', 33)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="bd8d17f8-e63a-4545-809f-891af6bb9c4a"></div>








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
      <th>serial_no</th>
      <td>98.963731</td>
    </tr>
    <tr>
      <th>opticalelectrical_type</th>
      <td>98.963731</td>
    </tr>
    <tr>
      <th>ne_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>port_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>port_description</th>
      <td>54.217940</td>
    </tr>
    <tr>
      <th>port_type</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>receive_optical_powerdbm</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>reference_receive_optical_powerdbm</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>reference_receive_time</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>receive_status</th>
      <td>55.586140</td>
    </tr>
    <tr>
      <th>upper_threshold_for_receive_optical_powerdbm</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>low_threshold_for_receive_optical_powerdbm</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>transmit_optical_powerdbm</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>reference_transmit_optical_powerdbm</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>reference_transmit_time</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>transmit_status</th>
      <td>55.586140</td>
    </tr>
    <tr>
      <th>upper_threshold_for_transmit_optical_powerdbm</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>low_threshold_for_transmit_optical_powerdbm</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>singlemodemultimode</th>
      <td>55.853303</td>
    </tr>
    <tr>
      <th>speedmbs</th>
      <td>98.963731</td>
    </tr>
    <tr>
      <th>wave_lengthnm</th>
      <td>55.383744</td>
    </tr>
    <tr>
      <th>transmission_distancem</th>
      <td>99.222798</td>
    </tr>
    <tr>
      <th>fiber_type</th>
      <td>48.826101</td>
    </tr>
    <tr>
      <th>pmanufacturer</th>
      <td>99.740933</td>
    </tr>
    <tr>
      <th>optical_mode_authentication</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>port_remark</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>port_custom_column</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>opticaldirectiontype</th>
      <td>98.356541</td>
    </tr>
    <tr>
      <th>vendor_pn</th>
      <td>98.129858</td>
    </tr>
    <tr>
      <th>model</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>revissue_number</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>2.161593</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



Se observa que muchas de las columnas tienen un 100% de datos no nulos, las columnas que indican atributos del producto son los mas incompletos como la version del hardware, software y la fecha de fabricación. Existen cuatro campos sin datos válidos.

## 4.5 Catálogos

#### Catálogo Optical Type:


```python
Catalogo_type=pd.DataFrame(df_3.opticalelectrical_type.unique())
Catalogo_type.columns=['opticalelectrical_type']
Catalogo_type.reset_index(drop=True)
Catalogo_type.dropna(inplace=True)
Catalogo_type.sort_index(ascending=True).head(10)
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
      <th>opticalelectrical_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ESFP</td>
    </tr>
    <tr>
      <th>1</th>
      <td>XFP</td>
    </tr>
    <tr>
      <th>2</th>
      <td>COPPER</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SFP</td>
    </tr>
    <tr>
      <th>4</th>
      <td>CFP</td>
    </tr>
    <tr>
      <th>5</th>
      <td>CFP2</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SFPPLUS</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Port Type:


```python
Catalogo_port_type=pd.DataFrame(df_3.port_type.unique())
Catalogo_port_type.columns=['opticalelectrical_type']
Catalogo_port_type.reset_index(drop=True)
Catalogo_port_type.dropna(inplace=True)
Catalogo_port_type.sort_index(ascending=True).head(10)
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
      <th>opticalelectrical_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Ethernet</td>
    </tr>
    <tr>
      <th>1</th>
      <td>POS</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Receive Status:


```python
Catalogo_status=pd.DataFrame(df_3.receive_status.unique())
Catalogo_status.columns=['receive_status']

#Se eliminan los caracteres inválidos
Catalogo_status.dropna(inplace=True)
Catalogo_status.reset_index(drop=False)
Catalogo_status.sort_index(ascending=True).head(10)
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
      <th>receive_status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Normal</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Critical Alert</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Warning Alert</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Manufacturer:


```python
Catalogo_manufacturer=pd.DataFrame(df_3.pmanufacturer.unique())
Catalogo_manufacturer.columns=['pmanufacturer']

#Se eliminan los caracteres inválidos
Catalogo_manufacturer.dropna(inplace=True)
Catalogo_manufacturer.reset_index(drop=False)
Catalogo_manufacturer.sort_index(ascending=True).head(10)
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
      <th>pmanufacturer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HG GENUINE</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WTD</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NEOPHOTONICS</td>
    </tr>
    <tr>
      <th>3</th>
      <td>FINISAR CORP.</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SumitomoElectric</td>
    </tr>
    <tr>
      <th>5</th>
      <td>AVAGO</td>
    </tr>
    <tr>
      <th>6</th>
      <td>HISILICON</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Accedian</td>
    </tr>
    <tr>
      <th>8</th>
      <td>CISCO</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Hisense</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Port Description:


```python
Catalogo_description=pd.DataFrame(df_3.port_description.unique())
Catalogo_description.columns=['port_description']

#Se eliminan los caracteres inválidos
Catalogo_description.dropna(inplace=True)
Catalogo_description.reset_index(drop=False)
Catalogo_description.sort_index(ascending=True).head(10)
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
      <th>port_description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>To-MXCMXM01RTCOREBH02-GE1/1/1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>To-MXHMEX0172RTBHCSRMOB02-GE1/0/0-11138-ETH-19...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>To-MXDIFMGH0768RTBHCSRMOB02-GE1/0/0-11138-ETH-...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>To-MXDIFBEJ0192RTBHCSRMOB02-GE1/0/0-11138-ETH-198</td>
    </tr>
    <tr>
      <th>5</th>
      <td>To-MXHCUE0010RTBHCSRMOB02-GE2/1/7-11138-ETH-22...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>To-MXHMEX0225RTBHCSRMOB02</td>
    </tr>
    <tr>
      <th>7</th>
      <td>To-MXDIFCYN0399RTBHCSRMOB02</td>
    </tr>
    <tr>
      <th>8</th>
      <td>to MXMEXCHL0096RTBHCSRMOB02 |1/0/0| ETAA000245...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>To-HMEX0222</td>
    </tr>
    <tr>
      <th>10</th>
      <td>To-MXCMXM01RTCOREBH02</td>
    </tr>
  </tbody>
</table>
</div>



## 4.6 Preparación de los datos
Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos en los dos catálogos: 

* Se eliminan los siguientes caracteres especiales:    '-','#','%','/','_'
* Se eliminan espacios.
* Se eliminan valores que indican nulos como "--".
* Pasar todo a uppercase


```python
df_clean=df_3.copy()

#df_clean.site_id.loc[df_clean.site_id.str.len()>6]==np.NaN
df_clean.site_id.replace()

df_clean.area_usuaria.replace('PIEZAS',np.NaN,regex=True,inplace=True)
df_clean.area_usuaria.replace('Piezas',np.NaN,regex=True,inplace=True)
df_clean.area_usuaria.replace('LTE-850',np.NaN,regex=True,inplace=True)
df_clean.replace('vacio',np.NaN,regex=True,inplace=True)
trans_clean = ['PROVEEDOR','AT&T','PAQUETERIA','TRANSPORTE DHL','MSO MEGACENTRO','OPERACIONES']
df_clean.tipo_transporte.replace(trans_clean,np.NaN,regex=True,inplace=True)
po_clean=list(df.orden_compra.unique())
po_dirt=['vacio','NO','no']
po_clean=[v for v in po_clean if v not in po_dirt]
df_clean.tipo_transporte.replace(po_clean,'SI',regex=True,inplace=True)

#df_clean=df_clean.loc[df_clean.serie_cleaned==0]
df_clean.reset_index(drop=True,inplace=True)
df_clean.head()
```


```python
df_3['trazabilidad']=0
df_3.trazabilidad.loc[(df.serie_cleaned==0) ]=1
```


```python
df_3.dtypes
```




    serial_no                                         object
    opticalelectrical_type                            object
    ne_name                                           object
    port_name                                         object
    port_description                                  object
    port_type                                         object
    receive_optical_powerdbm                          object
    reference_receive_optical_powerdbm               float64
    reference_receive_time                           float64
    receive_status                                    object
    upper_threshold_for_receive_optical_powerdbm      object
    low_threshold_for_receive_optical_powerdbm        object
    transmit_optical_powerdbm                         object
    reference_transmit_optical_powerdbm              float64
    reference_transmit_time                          float64
    transmit_status                                   object
    upper_threshold_for_transmit_optical_powerdbm     object
    low_threshold_for_transmit_optical_powerdbm       object
    singlemodemultimode                               object
    speedmbs                                          object
    wave_lengthnm                                     object
    transmission_distancem                            object
    fiber_type                                        object
    pmanufacturer                                     object
    optical_mode_authentication                       object
    port_remark                                      float64
    port_custom_column                               float64
    opticaldirectiontype                              object
    vendor_pn                                         object
    model                                            float64
    revissue_number                                  float64
    pnbom_codeitem                                    object
    filedate                                           int64
    filename                                          object
    fileip                                            object
    hash_id                                           object
    sourceid                                          object
    registry_state                                    object
    datasetname                                       object
    timestamp                                          int64
    transaction_status                                object
    year                                               int64
    month                                              int64
    day                                                int64
    serie_cleaned                                      int64
    trazabilidad                                       int64
    dtype: object




```python
mySchema = StructType([ StructField("omip", StringType(), True)\
                       ,StructField("productfamily", StringType(), True)\
                       ,StructField("creationtime", StringType(), True)\
                       ,StructField("nodename", StringType(), True)\
                       ,StructField("softwaretype", StringType(), True)\
                       ,StructField("managementstatus", StringType(), True)\
                       ,StructField("ipaddress", StringType(), True)\
                       ,StructField("devicename", StringType(), True)\
                       ,StructField("serial_number", StringType(), True)\
                       ,StructField("sheet_name", StringType(), True)\
                       ,StructField("technology", StringType(), True)\
                       ,StructField("manufacturerpartnr", StringType(), True)\
                       ,StructField("adminstatus", StringType(), True)\
                       ,StructField("location", StringType(), True)\
                       ,StructField("reachability", StringType(), True)\
                       ,StructField("devicetypeparameter", StringType(), True)\
                       ,StructField("filedate", IntegerType(), True)\
                       ,StructField("filename", StringType(), True)\
                       ,StructField("hash_id", StringType(), True)\
                       ,StructField("sourceid", StringType(), True)\
                       ,StructField("registry_state", StringType(), True)\
                       ,StructField("datasetname", StringType(), True)\
                       ,StructField("timestamp", IntegerType(), True)\
                       ,StructField("transaction_status", StringType(), True)\
                       ,StructField("year", IntegerType(), True)\
                       ,StructField("month", IntegerType(), True)\
                       ,StructField("day", IntegerType(), True)\
                       ,StructField("serie_cleaned", IntegerType(), True)\
                       ,StructField("trazabilidad", IntegerType(), True)\
                       ,StructField("CS_CA", IntegerType(), True)\
                       ,StructField("CS_SA", IntegerType(), True)\
                       ,StructField("SS_CA", IntegerType(), True)])
```

## 1.7 Métricas KPI

Se mostrarán los KPIs generados. 


```python
Total_Elementos=df_3.shape[0]
Total_Elementos
```




    12352




```python
df_3.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables


```python
Total_Tr=df_3.loc[(df_3.serial_no!='vacio') ].shape[0]
Total_Tr
```




    12224



#### Total Elementos NO Trazables


```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    128



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=df_3[['serial_no']].loc[(df_3.serial_no!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic
```




    12073



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    151




```python
df_3.columns
```




    Index([u'serial_no', u'opticalelectrical_type', u'ne_name', u'port_name',
           u'port_description', u'port_type', u'receive_optical_powerdbm',
           u'reference_receive_optical_powerdbm', u'reference_receive_time',
           u'receive_status', u'upper_threshold_for_receive_optical_powerdbm',
           u'low_threshold_for_receive_optical_powerdbm',
           u'transmit_optical_powerdbm', u'reference_transmit_optical_powerdbm',
           u'reference_transmit_time', u'transmit_status',
           u'upper_threshold_for_transmit_optical_powerdbm',
           u'low_threshold_for_transmit_optical_powerdbm', u'singlemodemultimode',
           u'speedmbs', u'wave_lengthnm', u'transmission_distancem', u'fiber_type',
           u'pmanufacturer', u'optical_mode_authentication', u'port_remark',
           u'port_custom_column', u'opticaldirectiontype', u'vendor_pn', u'model',
           u'revissue_number', u'pnbom_codeitem', u'filedate', u'filename',
           u'fileip', u'hash_id', u'sourceid', u'registry_state', u'datasetname',
           u'timestamp', u'transaction_status', u'year', u'month', u'day',
           u'serie_cleaned', u'trazabilidad'],
          dtype='object')



### KPIS


```python
#Ajustar el df contra los kpis de la siguiente tabla:

KPIs_3=pd.DataFrame({'KPI':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos,Total_Tr,Total_NOTr,
                              Total_Tr_Unic,Total_Tr_Dupli]})

KPIs_3
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
      <td>12352</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>12224</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>128</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>12073</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>151</td>
    </tr>
  </tbody>
</table>
</div>



Se envían los resultados a Hive:


```python
df_hive_kpis = spark.createDataFrame(KPIs_3)
```


```python
df_hive_kpis_final = df_hive_kpis.withColumn("filedate",lit(20191113)).withColumn("year",lit(2019)).withColumn("month",lit(11)).withColumn("day",lit(13)) 
```


```python
df_hive_kpis_final.write.mode("overwrite").saveAsTable("rci_network_db.kpi_u2000_tx_optical")
```

## 5. Subcard Report

### 5.1 Recolección de los datos: 

Se crea el dataframe de spark:


```python
df_4 =spark.sql("select * from tx_fbb_u2000_subcard where year = 2019 and month = 11 and day = 13")
```


```python
df_4.columns
```




    ['ne',
     'subboard_name',
     'subboard_type',
     'subrack_id',
     'slot_number',
     'subslot_number',
     'subboard_status',
     'hardware_version',
     'software_version',
     'snbar_code',
     'alias',
     'subboard_description',
     'remarks',
     'customized_column',
     'pnbom_codeitem',
     'subboard_manufacture_date',
     'model',
     'rev_issue_number',
     'filedate',
     'filename',
     'fileip',
     'hash_id',
     'sourceid',
     'registry_state',
     'datasetname',
     'timestamp',
     'transaction_status',
     'year',
     'month',
     'day']




```python
def validate_rule(string):
    
    search_list=[" ",'!','%','$',"<",">","^",'¡',"+","N/A",'¿','~','#','Ñ',"Ã","Åƒ","Ã‹","Ã³",'Ë','*','?',"ILEGIBLE", "VICIBLE","VISIBLE","INCOMPLETO"]
    test = u'%s' % (string)
    str_temp = test.decode('utf-8')
    if str_temp.upper() == "BORRADO":
      return 0
    elif len(str_temp) < 6:
      return 0
    elif any(ext.decode("utf-8") in str_temp.upper()for ext in search_list):
      return 0
    else:
      return 1
```

Se crea un udf en Spark sobre la función ya creada: 


```python
validate_rule_udf = udf(validate_rule, IntegerType())
```

Se le agrega una nueva columna al dataframe de spark; la nueva columna es la validacion de la columna serie con respecto al udf que creamos.


```python
df_4 = df_4.withColumn("serie_cleaned",validate_rule_udf(col("snbar_code"))).cache()
```

Se convierte el dataframe de spark a un dataframe de pandas


```python
df_4 = df_4.toPandas()
```

Hemos recolectado los campos a analizar de la fuente U2000 TX Subboard.


```python
df_4.head(5)
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
      <th>ne</th>
      <th>subboard_name</th>
      <th>subboard_type</th>
      <th>subrack_id</th>
      <th>slot_number</th>
      <th>subslot_number</th>
      <th>subboard_status</th>
      <th>hardware_version</th>
      <th>software_version</th>
      <th>snbar_code</th>
      <th>...</th>
      <th>hash_id</th>
      <th>sourceid</th>
      <th>registry_state</th>
      <th>datasetname</th>
      <th>timestamp</th>
      <th>transaction_status</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NVL-4038_BUENOSAIRES(MTY)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>--</td>
      <td>1</td>
      <td>1</td>
      <td>Unknown</td>
      <td>-</td>
      <td>-</td>
      <td>030HUTW09C000944</td>
      <td>...</td>
      <td>07d52f588de4e9374acd1ef63074d8bc198855b51a2377...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NVL-4038_BUENOSAIRES(MTY)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>--</td>
      <td>2</td>
      <td>1</td>
      <td>Unknown</td>
      <td>-</td>
      <td>-</td>
      <td>030HUTW09C000972</td>
      <td>...</td>
      <td>215aa77e8dbf47d368d477d156e5b61da248be3202d423...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NVL-4038_BUENOSAIRES(MTY)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>--</td>
      <td>3</td>
      <td>1</td>
      <td>Unknown</td>
      <td>-</td>
      <td>-</td>
      <td>030HUTW09C001055</td>
      <td>...</td>
      <td>2d4783b22b531356952dd4ef49e0c087376b055e7de832...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NVL-4038_BUENOSAIRES(MTY)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>--</td>
      <td>4</td>
      <td>1</td>
      <td>Unknown</td>
      <td>-</td>
      <td>-</td>
      <td>030HUTW09C000995</td>
      <td>...</td>
      <td>fc553cb6552a7e4ca4353d1351f88b679a4a2abeecea86...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NVL-4038_BUENOSAIRES(MTY)</td>
      <td>1-CD1</td>
      <td>TN81CD1</td>
      <td>--</td>
      <td>6</td>
      <td>1</td>
      <td>Unknown</td>
      <td>-</td>
      <td>-</td>
      <td>020GDLW0A1000100</td>
      <td>...</td>
      <td>01644b206df488d5003b2890442c923bc42967010fd31e...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 31 columns</p>
</div>



### Diccionario de datos.
A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

* **ne**: ID del negocio.
* **board_name**: Familia de productos al que pertenece.
* **board_type**: Fecha de creacion, validar si es de carga.
* **ne_type**: Pendiente.
* **subrack_id**: Tipo de Software.
* **slot_id**: Pendiente, es un estatus.
* **hardware_version**: Versión del hardware del dispositivo.
* **software_version**: Versión del software del dispositivo.
* **snbar_code**: Numero de serie.
* **alias**: Nombre del sheet.
* **remarks**: Pendiente.
* **customized_column**: Pendiente.
* **ne_id**: Estado.
* **bios_version**: Versión del BIOS del dispositivo.
* **fpga_version**: Pendiente.
* **board_status**: Estado de servicio del dispositivo.
* **pnbom_codeitem**: Pendiente.
* **model**: Pendiente.
* **rev_issue_number**: Pendiente.
* **management**: Pendiente.
* **description**: Pendiente.
* **manufacture_date**: Fecha de fabricación del dispositivo.
* **create_time**: Pendiente.
* **filedate**: Fecha de carga del archivo fuente.
* **filename**: Nombre del archivo fuente.
* **hash_id**: Identificador único hash de la fuente.
* **source_id**: Fuente de archivo.
* **registry_state**: Timestamp de carga.
* **datasetname**: Nombre indentificador de la fuente.
* **timestamp**: Fecha de carga.
* **transaction_status**: Estatus de registro.
* **year**: Año de la partición.
* **month**: Mes de la partición.
* **day**: Día de la partición.

## 1.2 Descripción de las fuentes
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos=df_4.columns
print('Columnas de la fuente TX Subcard son: ',list(campos))
pd.DataFrame(df_4.dtypes,columns=['Tipo de objeto TX Subcard'])
```

    ('Columnas de la fuente TX Subcard son: ', ['ne', 'subboard_name', 'subboard_type', 'subrack_id', 'slot_number', 'subslot_number', 'subboard_status', 'hardware_version', 'software_version', 'snbar_code', 'alias', 'subboard_description', 'remarks', 'customized_column', 'pnbom_codeitem', 'subboard_manufacture_date', 'model', 'rev_issue_number', 'filedate', 'filename', 'fileip', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie_cleaned'])





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
      <th>Tipo de objeto TX Subcard</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ne</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subboard_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subboard_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subrack_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>slot_number</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subslot_number</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subboard_status</th>
      <td>object</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>object</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subboard_description</th>
      <td>object</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>object</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>object</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>object</td>
    </tr>
    <tr>
      <th>subboard_manufacture_date</th>
      <td>object</td>
    </tr>
    <tr>
      <th>model</th>
      <td>object</td>
    </tr>
    <tr>
      <th>rev_issue_number</th>
      <td>object</td>
    </tr>
    <tr>
      <th>filedate</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>filename</th>
      <td>object</td>
    </tr>
    <tr>
      <th>fileip</th>
      <td>object</td>
    </tr>
    <tr>
      <th>hash_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sourceid</th>
      <td>object</td>
    </tr>
    <tr>
      <th>registry_state</th>
      <td>object</td>
    </tr>
    <tr>
      <th>datasetname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>timestamp</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>transaction_status</th>
      <td>object</td>
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
print('renglones = ',df_4.shape[0],' columnas = ',df_4.shape[1])
```

    ('renglones = ', 5162, ' columnas = ', 31)



```python
#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'fileip', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes=[v for v in df_4.columns if v not in NOrelevantes]

df_4[relevantes].describe(include='all')
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
      <th>ne</th>
      <th>subboard_name</th>
      <th>subboard_type</th>
      <th>subrack_id</th>
      <th>slot_number</th>
      <th>subslot_number</th>
      <th>subboard_status</th>
      <th>hardware_version</th>
      <th>software_version</th>
      <th>snbar_code</th>
      <th>alias</th>
      <th>subboard_description</th>
      <th>remarks</th>
      <th>customized_column</th>
      <th>pnbom_codeitem</th>
      <th>subboard_manufacture_date</th>
      <th>model</th>
      <th>rev_issue_number</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162</td>
      <td>5162.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>537</td>
      <td>144</td>
      <td>29</td>
      <td>2</td>
      <td>21</td>
      <td>6</td>
      <td>3</td>
      <td>31</td>
      <td>2</td>
      <td>3424</td>
      <td>2</td>
      <td>50</td>
      <td>2</td>
      <td>1</td>
      <td>25</td>
      <td>301</td>
      <td>3</td>
      <td>4</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>MXTLAM01RTCOREDATA02</td>
      <td>PEM0 9</td>
      <td>CFCARD</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>Normal</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>-</td>
      <td>--</td>
      <td>-</td>
      <td>-</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>32</td>
      <td>442</td>
      <td>1554</td>
      <td>5148</td>
      <td>1225</td>
      <td>1781</td>
      <td>5136</td>
      <td>1542</td>
      <td>5148</td>
      <td>1710</td>
      <td>5092</td>
      <td>1206</td>
      <td>5106</td>
      <td>5162</td>
      <td>2762</td>
      <td>2770</td>
      <td>5138</td>
      <td>2766</td>
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
      <td>NaN</td>
      <td>0.666408</td>
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
      <td>NaN</td>
      <td>0.471541</td>
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
      <td>NaN</td>
      <td>1.000000</td>
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
      <td>NaN</td>
      <td>1.000000</td>
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
      <td>NaN</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_4["software_version"].unique()
```




    array([u'-', u'--'], dtype=object)



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

A diferencia de las demás tablas que conforman U2000 TX, el campo *Software Version* no tiene datos significativos, por esta razón se rechaza como catálogo. Nuestro conocimiento del negocio nos permite intuir que varias de estas columnas serán útiles en el futuro como son:
1. Subboard Type
2. Subboard Status
3. Hardware Version
4. Subboard Description


## 5.3 Exploración de los datos
De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los potenciales catálogos que acabamos de identificar, estos serán llamado más adelante en el apartado de *Catálogos* de este mismo documento; nuestra intención por el momento es simplemente explorar los datos.

#### Para empezar, se hará una limpieza general a los datos:


```python
df_4.replace('null',np.NaN,inplace=True)
df_4.replace('NA',np.NaN,inplace=True)
df_4.replace('NULL',np.NaN,inplace=True)
df_4.replace('<NULL>',np.NaN,inplace=True)
df_4.replace('NAN',np.NaN,inplace=True)
df_4.replace('na',np.NaN,inplace=True)
df_4.replace('',np.NaN,inplace=True)
df_4.replace(' ',np.NaN,inplace=True)
df_4.replace('--',np.NaN,inplace=True)
df_4.replace('-',np.NaN,inplace=True)
df_4.replace('/',np.NaN,inplace=True)
```

### Primer catálogo: *Subboard Type*

Empezaremos con el catálogo *Board Type*. Este catalogo nos permite concer y agrupar los datos por medio del tipo de tarjeta de control del dispositivo de fibra óptica.


```python
#Revisamos frecuencias:
campo_type=pd.DataFrame(df_4.subboard_type.value_counts()[:20])

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_type.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Subboard Type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Subboard Type')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_type['subboard_type'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción por Board Type',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_type.index,loc='upper left')

plt.show()
```


![png](output_343_0.png)


### Segundo catálogo: *Subboard Status*

Empezaremos con el catálogo *Board Type*. Este catalogo nos permite concer y agrupar los datos por medio del tipo de tarjeta de control del dispositivo de fibra óptica.


```python
#Revisamos frecuencias:
campo_status=pd.DataFrame(df_4.subboard_status.value_counts()[:20])

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_status.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Subboard Status')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Subboard Status')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_status['subboard_status'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción por Subboard Status',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_status.index,loc='upper left')

plt.show()
```


![png](output_346_0.png)


### Tercer catálogo: *Hardware Version*

Empezaremos con el catálogo *Board Type*. Este catalogo nos permite concer y agrupar los datos por medio del tipo de tarjeta de control del dispositivo de fibra óptica.


```python
#Revisamos frecuencias:
campo_hardware=pd.DataFrame(df_4.hardware_version.value_counts()[:20])

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_hardware.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Subboard Status')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Subboard Status')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_hardware['hardware_version'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción por Subboard Status',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_hardware.index,loc='upper left')

plt.show()
```


![png](output_349_0.png)


### Cuarto catálogo: *Subboard Description*

El catálogo *Subboard Description* puede interpretarse como el modelo de la subtarjeta de control del dispositivo, es diferente al campo *Subboard Name* en el sentido de que este último busca ser una clave identificadora al componerse de la combinación de los campos *Subbboard Type*, *Hardware Version*, *Slot Number* y *Subslot Number*.


```python
#Revisamos frecuencias:
campo_description=pd.DataFrame(df_4.subboard_description.value_counts()[:20])

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_description.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Subboard Status')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Subboard Status')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_description['subboard_description'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Proporción por Subboard Status',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_description.index,loc='upper left')

plt.show()
```


![png](output_352_0.png)


## 5.4 Calidad de los datos
Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.


```python
df_4.head(10)
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
      <th>ne</th>
      <th>subboard_name</th>
      <th>subboard_type</th>
      <th>subrack_id</th>
      <th>slot_number</th>
      <th>subslot_number</th>
      <th>subboard_status</th>
      <th>hardware_version</th>
      <th>software_version</th>
      <th>snbar_code</th>
      <th>...</th>
      <th>sourceid</th>
      <th>registry_state</th>
      <th>datasetname</th>
      <th>timestamp</th>
      <th>transaction_status</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie_cleaned</th>
      <th>trazabilidad</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NVL-4038_BUENOSAIRES(MTY)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>vacio</td>
      <td>1</td>
      <td>1</td>
      <td>Unknown</td>
      <td>vacio</td>
      <td>vacio</td>
      <td>030HUTW09C000944</td>
      <td>...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NVL-4038_BUENOSAIRES(MTY)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>vacio</td>
      <td>2</td>
      <td>1</td>
      <td>Unknown</td>
      <td>vacio</td>
      <td>vacio</td>
      <td>030HUTW09C000972</td>
      <td>...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NVL-4038_BUENOSAIRES(MTY)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>vacio</td>
      <td>3</td>
      <td>1</td>
      <td>Unknown</td>
      <td>vacio</td>
      <td>vacio</td>
      <td>030HUTW09C001055</td>
      <td>...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NVL-4038_BUENOSAIRES(MTY)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>vacio</td>
      <td>4</td>
      <td>1</td>
      <td>Unknown</td>
      <td>vacio</td>
      <td>vacio</td>
      <td>030HUTW09C000995</td>
      <td>...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NVL-4038_BUENOSAIRES(MTY)</td>
      <td>1-CD1</td>
      <td>TN81CD1</td>
      <td>vacio</td>
      <td>6</td>
      <td>1</td>
      <td>Unknown</td>
      <td>vacio</td>
      <td>vacio</td>
      <td>020GDLW0A1000100</td>
      <td>...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NVL-4038_BUENOSAIRES(MTY)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>vacio</td>
      <td>18</td>
      <td>1</td>
      <td>Unknown</td>
      <td>vacio</td>
      <td>vacio</td>
      <td>030HUTW09C001008</td>
      <td>...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>MEX-9295 BUENAVISTA(toluca)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>vacio</td>
      <td>1</td>
      <td>1</td>
      <td>Unknown</td>
      <td>vacio</td>
      <td>vacio</td>
      <td>030HUTW09C000988</td>
      <td>...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>MEX-9295 BUENAVISTA(toluca)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>vacio</td>
      <td>2</td>
      <td>1</td>
      <td>Unknown</td>
      <td>vacio</td>
      <td>vacio</td>
      <td>030HUTW09C000993</td>
      <td>...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>MEX-9295 BUENAVISTA(toluca)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>vacio</td>
      <td>3</td>
      <td>1</td>
      <td>Unknown</td>
      <td>vacio</td>
      <td>vacio</td>
      <td>030HUTW09C000983</td>
      <td>...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>MEX-9295 BUENAVISTA(toluca)</td>
      <td>1-MQ1</td>
      <td>TN81MQ1</td>
      <td>vacio</td>
      <td>4</td>
      <td>1</td>
      <td>Unknown</td>
      <td>vacio</td>
      <td>vacio</td>
      <td>030HUTW09C000954</td>
      <td>...</td>
      <td>Gestores-U2000-FBB-TX</td>
      <td>2019:11:28:17:18:7</td>
      <td>Subcard_report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>13</td>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>10 rows × 32 columns</p>
</div>



#### Visualización de los datos de trazabilidad: 

Creamos una tabla donde se observarán los número de serie repetidos para un mejor análisis.


```python
pd.DataFrame(df_4.snbar_code.value_counts()[:15])
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
      <th>snbar_code</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>030SWL10GB000037</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030QDE10G7000291</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030PMN10G8000250</th>
      <td>2</td>
    </tr>
    <tr>
      <th>210305G05110F4000020</th>
      <td>2</td>
    </tr>
    <tr>
      <th>210305G051Z0C1000122</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030QDE10G7000279</th>
      <td>2</td>
    </tr>
    <tr>
      <th>210305G051Z0B1000035</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030SWL10GB000050</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030SWL10GB000081</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030SWL10GB000047</th>
      <td>2</td>
    </tr>
    <tr>
      <th>210305G05110F4000021</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030QDE10G7000290</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030SWL10GB000048</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030PMN10GA000221</th>
      <td>2</td>
    </tr>
    <tr>
      <th>030PMN10GA000247</th>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



### Missings Values
Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.


```python
nas=df_4[relevantes].isna().sum()
porcentaje_nas=nas/df_4[relevantes].isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de NAs por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 19), ('counts_nas', 19)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="9445dab8-7de3-4792-b235-2a0ce89544e7"></div>








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
      <th>ne</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subboard_name</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subboard_type</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subrack_id</th>
      <td>0.271213</td>
    </tr>
    <tr>
      <th>slot_number</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subslot_number</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subboard_status</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>30.143355</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>33.359163</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subboard_description</th>
      <td>23.363038</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>53.738861</td>
    </tr>
    <tr>
      <th>subboard_manufacture_date</th>
      <td>53.661372</td>
    </tr>
    <tr>
      <th>model</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>rev_issue_number</th>
      <td>54.087563</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>



#### Visualización de datos NOT NULL: 


```python
notmiss=(1-porcentaje_nas)*100

columnas=list(notmiss.keys())
counts_nas=list(notmiss.values)

#Mismo aplica aquí para color
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_20))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 19), ('counts_nas', 19)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="8b975a60-6656-43b2-a93a-446bcd03eb3e"></div>








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
      <th>ne</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subboard_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subboard_type</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subrack_id</th>
      <td>99.728787</td>
    </tr>
    <tr>
      <th>slot_number</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subslot_number</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subboard_status</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>69.856645</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>66.640837</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subboard_description</th>
      <td>76.636962</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>46.261139</td>
    </tr>
    <tr>
      <th>subboard_manufacture_date</th>
      <td>46.338628</td>
    </tr>
    <tr>
      <th>model</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>rev_issue_number</th>
      <td>45.912437</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



## 5.5 Catálogos

#### Catálogo de Subboard Type:


```python
Catalogo_subboard=pd.DataFrame(df_4.subboard_type.unique())
Catalogo_subboard.columns=['subboard_type']

#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios.
Catalogo_subboard.reset_index(drop=True)
Catalogo_subboard.dropna(inplace=True)
Catalogo_subboard.sort_values(by='subboard_type').head(10)
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
      <th>subboard_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>5</th>
      <td>CFCARD</td>
    </tr>
    <tr>
      <th>15</th>
      <td>CR57E1NCB2</td>
    </tr>
    <tr>
      <th>19</th>
      <td>CR57EFGFB REV A</td>
    </tr>
    <tr>
      <th>9</th>
      <td>CR5D00C1CF10</td>
    </tr>
    <tr>
      <th>8</th>
      <td>CR5D0E8GFA70</td>
    </tr>
    <tr>
      <th>17</th>
      <td>CR5D0E8GFA71</td>
    </tr>
    <tr>
      <th>20</th>
      <td>CR5D0L6XFA70</td>
    </tr>
    <tr>
      <th>27</th>
      <td>CXFAN</td>
    </tr>
    <tr>
      <th>28</th>
      <td>CXPOWER</td>
    </tr>
    <tr>
      <th>6</th>
      <td>DEVPOWER</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de Subboard Status:


```python
Catalogo_status=pd.DataFrame(df_4.subboard_status.unique())
Catalogo_status.columns=['subboard_status']

#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios.
Catalogo_status.reset_index(drop=True)
Catalogo_status.dropna(inplace=True)
Catalogo_status.sort_values(by='subboard_status',ascending=True).head(10)
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
      <th>subboard_status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>Fault</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Normal</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Unknown</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de Hardware Version:


```python
Catalogo_hardware=pd.DataFrame(df_4.hardware_version.unique())
Catalogo_hardware.columns=['hardware_version']

#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios.
Catalogo_hardware.reset_index(drop=True)
Catalogo_hardware.dropna(inplace=True)
Catalogo_hardware.sort_values(by='hardware_version',ascending=True).head(10)
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
      <th>hardware_version</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>26</th>
      <td>CFCARD2 REV A</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CR52EBGE REV A</td>
    </tr>
    <tr>
      <th>25</th>
      <td>CR52EBGE REV B</td>
    </tr>
    <tr>
      <th>11</th>
      <td>CR52EBGF REV A</td>
    </tr>
    <tr>
      <th>27</th>
      <td>CR52EBGF REV B</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CR52EBGFB REV B</td>
    </tr>
    <tr>
      <th>10</th>
      <td>CR52EEGFNB REV A</td>
    </tr>
    <tr>
      <th>13</th>
      <td>CR52EEGFNB REV B</td>
    </tr>
    <tr>
      <th>12</th>
      <td>CR52EKGE REV A</td>
    </tr>
    <tr>
      <th>24</th>
      <td>CR52L1XX REV C</td>
    </tr>
  </tbody>
</table>
</div>



#### Subboard Description:


```python
Catalogo_description=pd.DataFrame(df_4.subboard_description.unique())
Catalogo_description.columns=['subboard_description']

#Remover los sucios
#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios, un ejemplo puede ser:
Catalogo_description.reset_index(drop=True)
Catalogo_description.dropna(inplace=True)
Catalogo_description.sort_values(by='subboard_description',ascending=True).head(10)
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
      <th>subboard_description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>30</th>
      <td>1-Port 100GBase-CFP Fixed Card</td>
    </tr>
    <tr>
      <th>12</th>
      <td>1-Port Channelized OC-3c/STM-1c POS-SFP Flexib...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2-Port 10GBase LAN/WAN-XFP Flexible Card A(P40...</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2-Port 10GBase LAN/WAN-XFP Flexible Card A(Sup...</td>
    </tr>
    <tr>
      <th>31</th>
      <td>2-Port 10GBase LAN/WAN-XFP Flexible Card(Suppo...</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2-Port Channelized OC-3c/STM-1c POS-SFP Flexib...</td>
    </tr>
    <tr>
      <th>16</th>
      <td>20-Port 100/1000Base-X-SFP Flexible Card A(P40...</td>
    </tr>
    <tr>
      <th>22</th>
      <td>20-Port 100/1000Base-X-SFP Flexible Card A(Sup...</td>
    </tr>
    <tr>
      <th>39</th>
      <td>24-Port 100/1000Base-X-SFP Flexible Card A(P10...</td>
    </tr>
    <tr>
      <th>36</th>
      <td>24-Port 10GBase LAN/WAN-SFP+ Flexible Card A(P...</td>
    </tr>
  </tbody>
</table>
</div>



## 5.6 Preparación de los datos
Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos en los dos catálogos: 

* Se eliminan los siguientes caracteres especiales:    '-','#','%','/','_'
* Se eliminan espacios.
* Se eliminan valores que indican nulos como "--".
* Pasar todo a uppercase


```python
df_4['trazabilidad']=0
df_4.trazabilidad.loc[(df.serie_cleaned==0) ]=1
```

## 1.7 Métricas KPI

Se mostrarán los KPIs generados. 


```python
Total_Elementos=df_4.shape[0]
Total_Elementos
```




    5162




```python
df_4.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables


```python
Total_Tr=df_4.loc[(df_4.snbar_code!='vacio') ].shape[0]
Total_Tr
```




    3440



#### Total Elementos NO Trazables


```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    1722



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=df_4[['snbar_code']].loc[(df.snbar_code!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic
```




    3423



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    17




```python
df_4.columns
```




    Index([u'ne', u'subboard_name', u'subboard_type', u'subrack_id',
           u'slot_number', u'subslot_number', u'subboard_status',
           u'hardware_version', u'software_version', u'snbar_code', u'alias',
           u'subboard_description', u'remarks', u'customized_column',
           u'pnbom_codeitem', u'subboard_manufacture_date', u'model',
           u'rev_issue_number', u'filedate', u'filename', u'fileip', u'hash_id',
           u'sourceid', u'registry_state', u'datasetname', u'timestamp',
           u'transaction_status', u'year', u'month', u'day', u'serie_cleaned'],
          dtype='object')



### KPIS


```python
#Ajustar el df contra los kpis de la siguiente tabla:

KPIs_4=pd.DataFrame({'KPI':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos,Total_Tr,Total_NOTr,
                              Total_Tr_Unic,Total_Tr_Dupli]})

KPIs_4
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
      <td>5162</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>3440</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>1722</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>3423</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>17</td>
    </tr>
  </tbody>
</table>
</div>



Se envían los resultados a Hive:


```python
df_hive_kpis = spark.createDataFrame(KPIs_4)
```


```python
df_hive_kpis_final = df_hive_kpis.withColumn("filedate",lit(20191113)).withColumn("year",lit(2019)).withColumn("month",lit(11)).withColumn("day",lit(13))
```


```python
df_hive_kpis_final.write.mode("overwrite").saveAsTable("rci_network_db.kpi_u2000_tx_subboard")
```
