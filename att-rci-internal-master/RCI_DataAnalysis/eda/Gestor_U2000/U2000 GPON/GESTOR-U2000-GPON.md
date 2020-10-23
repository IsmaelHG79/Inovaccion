<div style="width: 100%; clear: both; font-family: Verdana;">
<div style="float: left; width: 100%;font-family: Verdana;">
<img src="./image/axity-logo.png" align="left">
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

Para hacer más fácil la revisión de este documento, aquí solo se revisaran los datos del gestor **U2000 GPON**, la información del gestor de microondas TX tiene su propio documento de análisis.

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
conf = SparkConf().setAppName('tx_gpon_u2000')  \
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
        <span id="69c17c54-620a-49d3-8f73-ac6ecb254e71">Loading BokehJS ...</span>
    </div>




# U2000 GPON

La fuente está compuesta de varias tablas que se tratarán de forma separada durante la exploración, si se identifican similitudes entre estas será en el modelo cuando se unan para conformar uno o varios catálogos; las tablas que la componen son:

1. Board Report
2. NE Report
3. Subrack Report

Para analizar el gestor U2000 GPON en conjunto, se realiza una unión de las fuentes Board Report, NE Report y Subrack Report para trabajar una parte del universo de GPON. La tablas que se utilizan como fuentes son ```tx_gpon_u2000_board```, ```tx_gpon_u2000_ne``` y ```tx_gpon_u2000_subrack```.

## U2000 GPON Board Report

### 1.1 Recolección de los datos: 

Los datos con los que se trabajan a lo largo del EDA corresponden a la partición de **20191013** para todas las tablas.

*IMPORTANTE*: Si se requieren ver datos de otro periodo, se debe cambiar los filtros ```year = <año-a-ejecutar>```, ```month = <mes-a-ejecutar>```, ```day = <día-a-ejecutar>``` de las tablas en la siguiente celda:


```python
df_load =spark.sql("select * from tx_gpon_u2000_board where year = 2019 and month = 10 and day = 13")
```


```python
df_load.columns
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



Creamos una funcion para el tratamiento de datos en spark el cual contiene la reglas definidas para la columna ```ne```:


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
df_serie = df_load.withColumn("serie_cleaned",validate_rule_udf(col("snbar_code"))).cache()
```


```python
df_serie.select("filedate","year","month","day").show()
```

    +--------+----+-----+---+
    |filedate|year|month|day|
    +--------+----+-----+---+
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    |20191013|2019|   10| 13|
    +--------+----+-----+---+
    only showing top 20 rows
    


Se convierte el dataframe de spark a un dataframe de pandas


```python
df = df_serie.toPandas()
```

Hemos recolectado los campos a analizar de la fuente U2000 GPON.

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
      <td>MXJALGDL0707OLT01</td>
      <td>Frame:0/Slot:0</td>
      <td>H807GPBH</td>
      <td>MA5608T</td>
      <td>0</td>
      <td>0</td>
      <td>H807GPBH VER A</td>
      <td>476(2015-2-14)</td>
      <td>022MLNCNF7000419</td>
      <td>H807GPBH_0_0</td>
      <td>...</td>
      <td>a99d81a3f272e2e2f1a424b0261773317f779b94ee5fb9...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:16:11:46</td>
      <td>Board_Report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>10</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MXJALGDL0707OLT01</td>
      <td>Frame:0/Slot:1/Subslot:0</td>
      <td>H801O2CE</td>
      <td>MA5608T</td>
      <td>0</td>
      <td>1</td>
      <td>H801O2CE VER A</td>
      <td>--</td>
      <td>020FCM10C2000073</td>
      <td>-</td>
      <td>...</td>
      <td>c36e12aa1a745a54319a762058ab6007e9cbdcdf16412a...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:16:11:46</td>
      <td>Board_Report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>10</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MXJALGDL0707OLT01</td>
      <td>Frame:0/Slot:1</td>
      <td>H801TOPA</td>
      <td>MA5608T</td>
      <td>0</td>
      <td>1</td>
      <td>H801TOPA VER B</td>
      <td>279(2014-4-15)</td>
      <td>020BEK10C2000031</td>
      <td>H801TOPA_0_1</td>
      <td>...</td>
      <td>9181efa5a992144cda063b07e594668d744abf0742e7c6...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:16:11:46</td>
      <td>Board_Report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>10</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MXJALGDL0707OLT01</td>
      <td>Frame:0/Slot:2/Subslot:0</td>
      <td>H801CPCB</td>
      <td>MA5608T</td>
      <td>0</td>
      <td>2</td>
      <td>H801CPCB VER A</td>
      <td>--</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>218a4846a54fbbe2d6a85f64f85c50ed7708a09694ff06...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:16:11:46</td>
      <td>Board_Report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>10</td>
      <td>13</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MXJALGDL0707OLT01</td>
      <td>Frame:0/Slot:2</td>
      <td>H801MCUD1</td>
      <td>MA5608T</td>
      <td>0</td>
      <td>2</td>
      <td>H801MCUD VER A</td>
      <td>MA5600V800R015C10</td>
      <td>021UEU10F7000661</td>
      <td>H801MCUD1_0_2</td>
      <td>...</td>
      <td>b4db0fc58a0e4368350248645f006f6611cf9b8bf3013f...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:16:11:46</td>
      <td>Board_Report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>10</td>
      <td>13</td>
      <td>1</td>
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
print('Columnas de la fuente GPON Board son: ',list(campos))
pd.DataFrame(df.dtypes,columns=['Tipo de objeto GPON Board'])
```

    ('Columnas de la fuente GPON Board son: ', ['ne', 'board_name', 'board_type', 'ne_type', 'subrack_id', 'slot_id', 'hardware_version', 'software_version', 'snbar_code', 'alias', 'remarks', 'customized_column', 'subrack_type', 'ne_id', 'bios_version', 'fpga_version', 'board_status', 'pnbom_codeitem', 'model', 'rev_issue_number', 'management', 'description', 'manufacture_date', 'create_time', 'filedate', 'filename', 'fileip', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie_cleaned'])





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
      <th>Tipo de objeto GPON Board</th>
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

    ('renglones = ', 2811, ' columnas = ', 37)



```python
#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'fileip', 'timestamp',
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
      <th>fpga_version</th>
      <th>board_status</th>
      <th>pnbom_codeitem</th>
      <th>model</th>
      <th>rev_issue_number</th>
      <th>management</th>
      <th>description</th>
      <th>manufacture_date</th>
      <th>create_time</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>...</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811</td>
      <td>2811.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>760</td>
      <td>24</td>
      <td>27</td>
      <td>5</td>
      <td>1</td>
      <td>13</td>
      <td>22</td>
      <td>15</td>
      <td>1296</td>
      <td>34</td>
      <td>...</td>
      <td>1</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>107</td>
      <td>1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>MXMICMRL1147OLT01</td>
      <td>Frame:0/Slot:0</td>
      <td>H831EPFE</td>
      <td>MA5628</td>
      <td>0</td>
      <td>0</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>H831EPFE_0_2</td>
      <td>...</td>
      <td>--</td>
      <td>Normal</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>Managed</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>14</td>
      <td>764</td>
      <td>599</td>
      <td>1812</td>
      <td>2811</td>
      <td>779</td>
      <td>1379</td>
      <td>1702</td>
      <td>1507</td>
      <td>599</td>
      <td>...</td>
      <td>2811</td>
      <td>2793</td>
      <td>2811</td>
      <td>2811</td>
      <td>2619</td>
      <td>2811</td>
      <td>2811</td>
      <td>1632</td>
      <td>2811</td>
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
      <td>0.463892</td>
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
      <td>0.498783</td>
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
<p>11 rows × 25 columns</p>
</div>




```python
df["board_status"].unique()
```




    array([u'Normal', u'Fault', u'Unknown'], dtype=object)



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

Todas las columnas contienen campos alfanuméricos que aunque proporcionan una forma de clasificación no son entendibles a simple vista, sin embargo, nuestro conocimiento del negocio nos permite intuir que varias de estas columnas serán útiles en el futuro como son:
1. Board Type
2. NE Type
3. Hardware Version
4. Software Version
5. Subrack Type
6. BIOS Version
7. Board Status

#### Se proponen catálogos derivados de la fuente tx_gpon_u2000_board con los siguientes campos:
    
* **Board Type**: Tipo de tarjeta de control del dispositivo.
* **Board Status**: Estado de servicio de la tarjeta de control.

Estos catálogos nos ayudarán a enriquecer la lista de activos con la que ya contamos.


## 1.3 Exploración de los datos
De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los catálogos.

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
df.remarks.replace('-',np.NaN,inplace=True)
df.customized_column.replace('-',np.NaN,inplace=True)
df.alias.replace('-',np.NaN,inplace=True)
df.description.replace('--',np.NaN,inplace=True)
df.create_time.replace('-',np.NaN,inplace=True)
#Se puede hacer más y por columna en caso de ser necesario
```

### Primer catálogo: *Board Type*

Empezaremos con el catálogo boardType. Este catalogo nos permite concer y agrupar los datos por medio del tipo de tarjeta de control del dispositivo de fibra óptica. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
campo_boardtype=pd.DataFrame(df.board_type.value_counts())

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_boardtype.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Board Type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Board Type')

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
ax1.set_title(u'Proporción por Board Type',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_boardtype.index,loc='upper left')

plt.show()
```

![catalogo01][img2]

Podemos observar que no se necesitan muchas reglas de limpieza, ya que todos siguen el mismo patrón y no existen valores nulos o inválidos.
Se llamará al catálogo limpio en el apartado de catálogos.

### Segundo catálogo: *board_status*

El siguiente catálogo es board_status; este catalogo nos permite concer y agrupar los datos por medio del estado de servicio de la tarjeta. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


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
ax0.set_xlabel(u'NOMBRE softwaretype')
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


![catalogo02][img3]


### Tercer catálogo: *Hardware Version*


```python
#Revisamos frecuencias:
campo_hardware=pd.DataFrame(df.hardware_version.value_counts())

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_boardtype.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Board Type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma Hardware Version')

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
ax1.set_title(u'Proporción por Hardware Version',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_hardware.index,loc='upper left')

plt.show()
```


![catalogo02][img4]


## 1.4 Calidad de los datos
Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

#### Visualización de los datos de trazabilidad: 

No existe una columna que contenga el número de serie o de activo del elemento, por lo tanto todos se considerarán NO trazables.

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

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 25), ('counts_nas', 25)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="f0f767e6-d3b8-408e-9874-a5dc9c856e5f"></div>








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
      <td>0.0</td>
    </tr>
    <tr>
      <th>board_name</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>board_type</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>ne_type</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>subrack_id</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>slot_id</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bios_version</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>fpga_version</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>board_status</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>model</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>rev_issue_number</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>management</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>description</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>create_time</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>0.0</td>
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

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 25), ('counts_nas', 25)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="1e7b2882-5ae5-48c5-997b-051f1dad8c3a"></div>








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
      <td>100.000000</td>
    </tr>
    <tr>
      <th>slot_id</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>50.942725</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>39.452152</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>46.389185</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>87.726788</td>
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
      <th>subrack_type</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>bios_version</th>
      <td>39.452152</td>
    </tr>
    <tr>
      <th>fpga_version</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>board_status</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>pnbom_codeitem</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>model</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>rev_issue_number</th>
      <td>6.830309</td>
    </tr>
    <tr>
      <th>management</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>description</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>41.942369</td>
    </tr>
    <tr>
      <th>create_time</th>
      <td>0.000000</td>
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

#### Catálogo NE Type:


```python
Catalogo_ne_type = pd.DataFrame(df.ne_type.unique())
Catalogo_ne_type.columns=['ne_type']

#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios.
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
      <th>3</th>
      <td>MA5603T</td>
    </tr>
    <tr>
      <th>0</th>
      <td>MA5608T</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MA5628</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MA5669</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MA5800-X2</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Software version:


```python
Catalogo_software = pd.DataFrame(df.software_version.unique())
Catalogo_software.columns=['software_version']

#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios.
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
      <th>8</th>
      <td>150(2014-12-18)</td>
    </tr>
    <tr>
      <th>14</th>
      <td>173(2014-12-26)</td>
    </tr>
    <tr>
      <th>10</th>
      <td>204(2015-1-8)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>279(2014-4-15)</td>
    </tr>
    <tr>
      <th>7</th>
      <td>283(2014-10-25)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>319(2018-8-27)</td>
    </tr>
    <tr>
      <th>0</th>
      <td>476(2015-2-14)</td>
    </tr>
    <tr>
      <th>13</th>
      <td>606(2014-12-22)</td>
    </tr>
    <tr>
      <th>11</th>
      <td>694(2015-2-12)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MA5600V800R015C10</td>
    </tr>
  </tbody>
</table>
</div>



## 6. Preparación de los datos
Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos en los dos catálogos: 

* Se eliminan los siguientes caracteres especiales:    '-','#','%','/','_'
* Se eliminan espacios.
* Se eliminan valores que indican nulos como "--".
* Pasar todo a uppercase


```python
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
    CS_CA                  int64
    CS_SA                  int64
    SS_CA                  int64
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

## 7 Métricas KPI

Se mostrarán los KPIs generados. 


```python
Total_Elementos=df.shape[0]
Total_Elementos
```




    2811




```python
df.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables



```python
Total_Tr=df.loc[(df.snbar_code!='vacio') ].shape[0]
Total_Tr
```




    1304



#### Total Elementos NO Trazables



```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    1507



#### Total Elementos Trazables Únicos



```python
Total_Tr_Unic=df[['snbar_code']].loc[(df.snbar_code!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic
```




    1295



#### Total de elementos trazables duplicados



```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    9



###  KPIS


```python
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
      <td>2811</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>1304</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>1507</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>1295</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_hive_kpis = spark.createDataFrame(KPIs)
```


```python
df_hive_kpis_final = df_hive_kpis.withColumn("filedate",lit(20191113)).withColumn("year",lit(2019)).withColumn("month",lit(11)).withColumn("day",lit(13))
```


```python
df_hive_kpis_final.write.mode("overwrite").saveAsTable("rci_network_db.kpi_u2000_gpon_board")
```

## 2. NE Report

### 2.1 Recolección de los datos:

Se crea el dataframe de spark




```python
df_load_2 =spark.sql("SELECT * FROM tx_gpon_u2000_ne where year = 2019 and month=10 and day=13").cache()
```


```python
df_load_1_2019_10 = df_load_2.withColumn("serie_cleaned",validate_rule_udf(col("ne_name"))).cache()
```

Se carga a pandas


```python
df_1 = df_load_1_2019_10.toPandas()
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
      <td>MXJALGDL0707OLT01</td>
      <td>MA5608T</td>
      <td>10.105.51.228</td>
      <td>D4-94-E8-00-50-02</td>
      <td>--</td>
      <td>MA5600V800R015C10</td>
      <td>REGION R5 - GDL</td>
      <td>03/10/2016 21:53:22</td>
      <td>0</td>
      <td>Normal</td>
      <td>...</td>
      <td>0b09ffaf9e1538821ddf42b696fe01811386db0317d4c1...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:16:1:45</td>
      <td>NE_Report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>10</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MXJALGDL0707OLT01/MDU_10.105.51.230</td>
      <td>MA5628</td>
      <td>10.105.51.230</td>
      <td>5C-4C-A9-0F-EE-41</td>
      <td>--</td>
      <td>MA5628V800R310C00</td>
      <td>REGION R5 - JAL</td>
      <td>04/29/2016 13:03:21</td>
      <td>0</td>
      <td>Normal</td>
      <td>...</td>
      <td>b81e923c69c7dcb6e2343e83431c1a9f3908c95080d973...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:16:1:45</td>
      <td>NE_Report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>10</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MXJALGDL0707OLT01/MDU_10.105.51.231</td>
      <td>MA5628</td>
      <td>10.105.51.231</td>
      <td>5C-4C-A9-10-79-8F</td>
      <td>--</td>
      <td>MA5628V800R310C00</td>
      <td>REGION R5 - JAL</td>
      <td>04/29/2016 13:04:39</td>
      <td>0</td>
      <td>Normal</td>
      <td>...</td>
      <td>3eb909828b70b203d56781b71a9a56d820d79d6d5baf58...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:16:1:45</td>
      <td>NE_Report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>10</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MXJALGDL0707OLT01/MDU_10.105.51.232</td>
      <td>MA5628</td>
      <td>10.105.51.232</td>
      <td>5C-4C-A9-10-06-8A</td>
      <td>--</td>
      <td>MA5628V800R310C00</td>
      <td>REGION R5 - JAL</td>
      <td>11/24/2016 03:47:00</td>
      <td>0</td>
      <td>Normal</td>
      <td>...</td>
      <td>eee24be50baaaec3e4d34cfea6288e72db486ed1fa8466...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:16:1:45</td>
      <td>NE_Report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>10</td>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MXJALGDL0707OLT01/MDU_10.105.51.233</td>
      <td>MA5628</td>
      <td>10.105.51.233</td>
      <td>5C-4C-A9-10-05-37</td>
      <td>--</td>
      <td>MA5628V800R310C00</td>
      <td>REGION R5 - JAL</td>
      <td>05/02/2016 12:27:34</td>
      <td>0</td>
      <td>Normal</td>
      <td>...</td>
      <td>d97191c8f98ab412aed2df7168eaf03ac5cb6a4f17158b...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:16:1:45</td>
      <td>NE_Report</td>
      <td>20191128</td>
      <td>full</td>
      <td>2019</td>
      <td>10</td>
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
df_1["physical_location"].unique
```




    <bound method Series.unique of 0                        REGION R5 - GDL
    1                        REGION R5 - JAL
    2                        REGION R5 - JAL
    3                        REGION R5 - JAL
    4                        REGION R5 - JAL
    5                         REGION R9 - DF
    6                       REGION R9 - CDMX
    7                         REGION R9 - DF
    8                       REGION R9 - CDMX
    9                                     --
    10                        REGION R9 - DF
    11                        REGION R9 - DF
    12                      REGION R9 - CDMX
    13                      REGION R9 - CDMX
    14                      REGION R9 - CDMX
    15                      REGION R9 - CDMX
    16                      REGION R9 - CDMX
    17                      REGION R9 - CDMX
    18                                    --
    19                      REGION R9 - CDMX
    20                                    --
    21                                    --
    22                                    --
    23                      REGION R9 - CDMX
    24                        REGION R9 - DF
    25                      REGION R9 - CDMX
    26                        REGION R9 - DF
    27                  REGION R7 - ACAPULCO
    28                  REGION R7 - ACAPULCO
    29                  REGION R7 - ACAPULCO
                         ...                
    771                   REGION R8 - MERIDA
    772                      REGION R6 - AGS
    773                                   --
    774    REGION R5 - TEPIC-RANCHO QUEVEDEO
    775              REGION R5 - GUADALAJARA
    776              REGION R5 - GUADALAJARA
    777                       REGION R9 - DF
    778                       REGION R9 - DF
    779                    REGION R9 - CD MX
    780                    REGION R9 - CD MX
    781                    REGION R9 - CD MX
    782                    REGION R9 - CD MX
    783                    REGION R9 - CD MX
    784                    REGION R9 - CD MX
    785                    REGION R9 - CD MX
    786                    REGION R9 - CD MX
    787                    REGION R9 - CD MX
    788                     REGION R9 - CDMX
    789                     REGION R9 - CDMX
    790                    REGION R9 - CD MX
    791                       REGION R9 - DF
    792                  REGION R6 - MORELIA
    793                     REGION R9 - CDMX
    794                       REGION R9 - DF
    795                     REGION R9 - CDMX
    796                                   --
    797                                   --
    798                       REGION R9 - DF
    799                       REGION R9 - DF
    800                                   --
    Name: physical_location, Length: 801, dtype: object>



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

En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


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

    ('renglones = ', 801, ' columnas = ', 38)



```python
#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes_1=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
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
      <th>maintenance_status</th>
      <th>gateway_type</th>
      <th>gateway</th>
      <th>optical_ne</th>
      <th>subrack_type</th>
      <th>conference_call</th>
      <th>orderwire_phone</th>
      <th>ne_subtype</th>
      <th>fileip</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>...</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801.0</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>797</td>
      <td>6</td>
      <td>800</td>
      <td>759</td>
      <td>1</td>
      <td>6</td>
      <td>91</td>
      <td>800</td>
      <td>1</td>
      <td>3</td>
      <td>...</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>6</td>
      <td>1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>MXMEX115OLT01</td>
      <td>MA5628</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>MA5628V800R310C00</td>
      <td>REGION R9 - DF</td>
      <td>07/18/2019 23:31:14</td>
      <td>0</td>
      <td>Normal</td>
      <td>...</td>
      <td>Normal</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>MA5628</td>
      <td>10.105.100.2</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>2</td>
      <td>599</td>
      <td>2</td>
      <td>37</td>
      <td>801</td>
      <td>593</td>
      <td>139</td>
      <td>2</td>
      <td>801</td>
      <td>496</td>
      <td>...</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>801</td>
      <td>599</td>
      <td>801</td>
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
      <td>1.0</td>
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
      <td>0.0</td>
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
      <td>1.0</td>
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
      <td>1.0</td>
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
      <td>1.0</td>
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
      <td>1.0</td>
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
      <td>1.0</td>
    </tr>
  </tbody>
</table>
<p>11 rows × 27 columns</p>
</div>




```python
df_1["running_status"].unique()
```




    array([u'Normal', u'Pre-deployed', u'Offline'], dtype=object)



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

* Como se puede observar las columnas que mas se adecuan para ser un catalogo son *ne_type*, physical_location y running_status, ya que son columnas que nos proporciona una forma de clasificacion y agrupacion del set de datos , y son columnas que pueden agregar cierto valor al negocio.

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
df_1.replace('-',np.NaN,inplace=True)
df_1.replace('--',np.NaN,inplace=True)
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


![png](output_107_0.png)


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


![png](output_109_0.png)


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
ax0.set_xlabel(u'NE Subtype')
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
ax1.set_title(u'Frecuencia NE Subtype',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_subtype.index,loc='upper left')

plt.show()
```


![png](output_111_0.png)


### Cuarto catálogo: Running Status


```python
campo_status=pd.DataFrame(df_1.running_status.value_counts()).head(20)

#print campo_type['physical_location'].size
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_status.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'NE Status')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Histograma NE Status')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_status['running_status'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1)
ax1.set_title(u'Frecuencia NE Status',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_status.index,loc='upper left')

plt.show()
```


![png](output_113_0.png)


## 4.1 Calidad de los datos

Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

#### Visualización de los datos de trazabilidad:

La fuente no tiene un campo que indique el número de serie o de activo, por lo que todos los registros se consideran NO trazables.

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

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 27), ('counts_nas', 27)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="d647c6b2-d3b3-4cd2-84d8-41cd667056c9"></div>








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
      <td>0.0</td>
    </tr>
    <tr>
      <th>ne_type</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>ne_ip_address</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>ne_mac_address</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>physical_location</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>create_time</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>fibercable_count</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>running_status</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>subnet</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>subnet_path</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>patch_version_list</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>lsr_id</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>maintenance_status</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>gateway_type</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>gateway</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>optical_ne</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>conference_call</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>orderwire_phone</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>ne_subtype</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>fileip</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>0.0</td>
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

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 27), ('counts_nas', 27)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="1d3278c8-84aa-412a-aafa-17b943a959b5"></div>








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
      <td>100.0</td>
    </tr>
    <tr>
      <th>ne_type</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>ne_ip_address</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>ne_mac_address</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>physical_location</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>create_time</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>fibercable_count</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>running_status</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>subnet</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>subnet_path</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>remarks</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>patch_version_list</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>customized_column</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>lsr_id</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>maintenance_status</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>gateway_type</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>gateway</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>optical_ne</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>subrack_type</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>conference_call</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>orderwire_phone</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>ne_subtype</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>fileip</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.0</td>
    </tr>
  </tbody>
</table>
</div>



##  2.5 Catálogos

#### Catálogo de ne_type:


```python
Catalogo_ne_type=pd.DataFrame(df_1.ne_type.unique())
Catalogo_ne_type.columns=['ne_type']

#Remover los sucios
#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios, un ejemplo puede ser:
#Catalogo_CAMPO.drop(labels=[67,346,369,279,171,313],axis=0,inplace=True)

#Se le da 
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
      <th>4</th>
      <td>MA5603T</td>
    </tr>
    <tr>
      <th>0</th>
      <td>MA5608T</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MA5628</td>
    </tr>
    <tr>
      <th>5</th>
      <td>MA5669</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MA5800-X2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MDU</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de physical location:


```python
df_1.physical_location.replace('REGION R1 - TIJ','REGION R1 - TIJUANA',inplace=True)
df_1.physical_location.replace('REGION R6 - CEL','REGION R6 - LEON',inplace=True)
df_1.physical_location.replace('REGION R2 - CUL','REGION R2 - CULIACAN',inplace=True)
df_1.physical_location.replace('REGION R9 - DF','REGION R9 - CDMX',inplace=True)
df_1.physical_location.replace('--',np.NaN,inplace=True)
df_1.physical_location.replace('--',np.NaN,inplace=True)
Catalogo_location=pd.DataFrame(df_1.physical_location.unique())
Catalogo_location.columns=['physical_location']

#Catalogo_location.reset_index(drop=True)
#Catalogo_location.dropna(inplace=True)
#Catalogo_location.sort_values(by='physical_location').head(10)
Catalogo_location.head(10)
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
      <th>physical_location</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>REGION R5 - GDL</td>
    </tr>
    <tr>
      <th>1</th>
      <td>REGION R5 - JAL</td>
    </tr>
    <tr>
      <th>2</th>
      <td>REGION R9 - CDMX</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>REGION R7 - ACAPULCO</td>
    </tr>
    <tr>
      <th>5</th>
      <td>REGION R9 - MEX</td>
    </tr>
    <tr>
      <th>6</th>
      <td>REGION R6 - LEON</td>
    </tr>
    <tr>
      <th>7</th>
      <td>REGION R6 - CELAYA</td>
    </tr>
    <tr>
      <th>8</th>
      <td>REGION R6 - GTO</td>
    </tr>
    <tr>
      <th>9</th>
      <td>REGION R6 - LEO</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Status:


```python
Catalogo_status = pd.DataFrame(df_1.running_status.unique())
Catalogo_status.columns=['running_status']

#Catalogo_status.reset_index(drop=True)
#Catalogo_status.dropna(inplace=True)
#Catalogo_status.sort_values(by='running_status').head(10)
Catalogo_status.head(10)
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
      <th>running_status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Normal</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Pre-deployed</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Offline</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo NE Subtype:


```python
Catalogo_ne_subtype=pd.DataFrame(df_1.ne_subtype.unique())
Catalogo_ne_subtype.columns=['ne_subtype']

#Catalogo_ne_subtype.reset_index(drop=True)
#Catalogo_ne_subtype.dropna(inplace=True)
#Catalogo_ne_subtype.sort_values(by='ne_subtype').head(10)
Catalogo_ne_subtype.head(10)
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
      <th>0</th>
      <td>MA5608T</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MA5628</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MA5800-X2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MDU</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MA5603T</td>
    </tr>
    <tr>
      <th>5</th>
      <td>MA5669</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Patch Version:


```python
Catalogo_patch = pd.DataFrame(df_1.patch_version_list.unique())
Catalogo_patch.columns=['patch_version_list']

#Catalogo_patch.reset_index(drop=True)
#Catalogo_patch.dropna(inplace=True)
#Catalogo_patch.sort_values(by='ne_subtype').head(10)
Catalogo_patch.head(10)
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
      <th>0</th>
      <td>SPC101 HP1006</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SPC100 SPH111</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SPH108</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SPC100</td>
    </tr>
    <tr>
      <th>5</th>
      <td>SPC200</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SPC100 SPH110</td>
    </tr>
    <tr>
      <th>7</th>
      <td>SPC100 SPH101</td>
    </tr>
    <tr>
      <th>8</th>
      <td>SPC100 SPH108</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SPC101</td>
    </tr>
  </tbody>
</table>
</div>



## 2.6 Preparación de los datos

Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos: 


* **Reglas:**
    * Homologar formatos en los casos posibles. 
    * Se marcan como *np.NaN* : campos que contengan:
        * ESPACIOS
        * La palabra BORRADO
        * La palabra VICIBLE
        * La palabra VISIBLE
        * CARACTER ESPECIAL
        * ILEGIBLE
        * INCOMPLETO
        * Registros que sean completamente alfabéticos.

    * replace(especiales,' ',)
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
    ne_id                 float64
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
    lsr_id                float64
    maintenance_status     object
    gateway_type          float64
    gateway               float64
    optical_ne            float64
    subrack_type          float64
    conference_call       float64
    orderwire_phone       float64
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




```python
mySchema_1 = StructType([ StructField("site", StringType(), True)\
                       ,StructField("ru", StringType(), True)\
                       ,StructField("operstate", StringType(), True)\
                       ,StructField("rnc", StringType(), True)\
                       ,StructField("antennaserialnumber", StringType(), True)\
                       ,StructField("node", StringType(), True)\
                       ,StructField("rurevision", StringType(), True)\
                       ,StructField("maxsupportedelectricaltilt", StringType(), True)\
                       ,StructField("bootrom", StringType(), True)\
                       ,StructField("state", StringType(), True)\
                       ,StructField("btsswver", StringType(), True)\
                       ,StructField("eq_class", StringType(), True)\
                       ,StructField("f_timestamp", StringType(), True)\
                       ,StructField("rulogicalid", StringType(), True)\
                       ,StructField("adminstate", StringType(), True)\
                       ,StructField("productname", StringType(), True)\
                       ,StructField("bsc", StringType(), True)\
                       ,StructField("productiondate", StringType(), True)\
                       ,StructField("prodname", StringType(), True)\
                       ,StructField("minsupportedelectricaltilt", StringType(), True)\
                       ,StructField("electricalantennatilt", StringType(), True)\
                       ,StructField("powerstate", StringType(), True)\
                       ,StructField("tg_count", StringType(), True)\
                       ,StructField("productrevision", StringType(), True)\
                       ,StructField("serialno", StringType(), True)\
                         ,StructField("ruserialno_count", StringType(), True)\
                         ,StructField("mo", StringType(), True)\
                         ,StructField("serialnumber", StringType(), True)\
                         ,StructField("antennamodelnumber", StringType(), True)\
                         ,StructField("prodno", StringType(), True)\
                         ,StructField("ruserialno", StringType(), True)\
                         ,StructField("productnumber", StringType(), True)\
                         ,StructField("eq", StringType(), True)\
                         ,StructField("nodeb", StringType(), True)\
                         ,StructField("sheet_name", StringType(), True)\
                         ,StructField("type", StringType(), True)\
                         ,StructField("manweek", StringType(), True)\
                         ,StructField("tg", StringType(), True)\
                         ,StructField("revision", StringType(), True)\
                         ,StructField("fsbrole", StringType(), True)\
                         ,StructField("enodeb", StringType(), True)\
                         ,StructField("filedate", StringType(), True)\
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

##  2.7 Métricas KPI

Se mostrarán los KPIs generados.

#### Total de elementos:


```python
Total_Elementos=df_1.shape[0]
Total_Elementos
```




    801




```python
df_1.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos NO Trazables


```python
Total_NOTr=Total_Elementos
Total_NOTr
```




    801



###  KPIS


```python
KPIs_1=pd.DataFrame({'KPI':['Total Elementos', 'Total NO Trazables'],
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
      <td>801</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total NO Trazables</td>
      <td>801</td>
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
df_hive_kpis_final.write.mode("overwrite").saveAsTable("rci_network_db.kpi_u2000_gpon_ne")
```

## 1.3 Subrack Report 

Recolección de los datos:

Se crea el dataframe de spark


```python
 df_load_2 =spark.sql("select * from tx_gpon_u2000_subrack where year = 2019 and month = 11 and day = 13").limit(400000).cache()
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

Una muestra de la fuente tx_gpon_u2000_subrack


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
      <td>MEX-91343_0754_LEGARIA_AYARZA</td>
      <td>Frame:0</td>
      <td>H821MABC</td>
      <td>0</td>
      <td>--</td>
      <td>--</td>
      <td>H821MABC_0</td>
      <td>Normal</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>85fc89a5aef6998fdda8f265a67b699cc29a8d2785df8d...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:15:56:31</td>
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
      <td>MXMEXTOL0806OLT01/MDU_10.105.90.16</td>
      <td>Frame:0</td>
      <td>H821MABC</td>
      <td>0</td>
      <td>--</td>
      <td>--</td>
      <td>H821MABC_0</td>
      <td>Normal</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>859473f60ca07691ee27dff0c7be024f769405e6501beb...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:15:56:31</td>
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
      <td>MEX-91007_PARQUE_LINDAVISTA</td>
      <td>Frame:0</td>
      <td>H821MABC</td>
      <td>0</td>
      <td>--</td>
      <td>--</td>
      <td>H821MABC_0</td>
      <td>Normal</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>67817727747118df57ff68094da6a3ab871c0cc32bf824...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:15:56:31</td>
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
      <td>MEX-91191_POLITECNICO</td>
      <td>Frame:0</td>
      <td>H821MABC</td>
      <td>0</td>
      <td>--</td>
      <td>--</td>
      <td>H821MABC_0</td>
      <td>Normal</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>78d0b61f984a01de6839c26c57de244578037552343f50...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:15:56:31</td>
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
      <td>MEX-91385_0976_TEPEYAC_INSURGENTES</td>
      <td>Frame:0</td>
      <td>H821MABC</td>
      <td>0</td>
      <td>--</td>
      <td>--</td>
      <td>H821MABC_0</td>
      <td>Normal</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>44dc8784c9b45487424dfafa788a7a2d3115186e520fbc...</td>
      <td>Gestores-U2000-GPON</td>
      <td>2019:11:28:15:56:31</td>
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


## 2.2 Descripción de las fuentes


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

    ('renglones = ', 702, ' columnas = ', 33)



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
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>...</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>702.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>698</td>
      <td>1</td>
      <td>5</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>5</td>
      <td>1</td>
      <td>124</td>
      <td>1</td>
      <td>...</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>21</td>
      <td>146</td>
      <td>146</td>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>MXJALGDL0714OLT01</td>
      <td>Frame:0</td>
      <td>H821MABC</td>
      <td>0</td>
      <td>--</td>
      <td>--</td>
      <td>H821MABC_0</td>
      <td>Normal</td>
      <td>--</td>
      <td>-</td>
      <td>...</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>MEXICO_68_AT&amp;T</td>
      <td>Physical Root/R7/PUEBLA/MEXICO_68_AT&amp;T</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>2</td>
      <td>702</td>
      <td>537</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>537</td>
      <td>702</td>
      <td>578</td>
      <td>702</td>
      <td>...</td>
      <td>702</td>
      <td>702</td>
      <td>702</td>
      <td>579</td>
      <td>20</td>
      <td>20</td>
      <td>702</td>
      <td>569</td>
      <td>702</td>
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
      <td>0.176638</td>
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
      <td>0.381634</td>
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



## 3.2 Exploración de los datos


```python
df_2.replace('null',np.NaN,inplace=True)
df_2.replace('NA',np.NaN,inplace=True)
df_2.replace('NULL',np.NaN,inplace=True)
df_2.replace('<NULL>',np.NaN,inplace=True)
df_2.replace('na',np.NaN,inplace=True)
df_2.replace('',np.NaN,inplace=True)
df_2.replace(' ',np.NaN,inplace=True)
df_2.replace('--',np.NaN,inplace=True)
df_2.replace('/',np.NaN,inplace=True)
df_2.replace('-',np.NaN,inplace=True)
df_2.replace('NAN',np.NaN,inplace=True)
```

### Visualización de los datos de trazabilidad:



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
      <th>021RSTW0F7000247</th>
      <td>2</td>
    </tr>
    <tr>
      <th>021HKYW0FA000104</th>
      <td>1</td>
    </tr>
    <tr>
      <th>023WEBD0JB000195</th>
      <td>1</td>
    </tr>
    <tr>
      <th>021RSTW0F7000495</th>
      <td>1</td>
    </tr>
    <tr>
      <th>023WEBD0J1000169</th>
      <td>1</td>
    </tr>
    <tr>
      <th>021RSTW0F7000490</th>
      <td>1</td>
    </tr>
    <tr>
      <th>023WEBD0K3000027</th>
      <td>1</td>
    </tr>
    <tr>
      <th>023WEBD0K4000064</th>
      <td>1</td>
    </tr>
    <tr>
      <th>023WEBD0J2000179</th>
      <td>1</td>
    </tr>
    <tr>
      <th>023WEBD0J2000178</th>
      <td>1</td>
    </tr>
    <tr>
      <th>023WEBD0K4000340</th>
      <td>1</td>
    </tr>
    <tr>
      <th>023WEBD0J2000177</th>
      <td>1</td>
    </tr>
    <tr>
      <th>021RSTW0F7000483</th>
      <td>1</td>
    </tr>
    <tr>
      <th>023WEBD0JB000183</th>
      <td>1</td>
    </tr>
    <tr>
      <th>023WEBD0J2000186</th>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



## 4.2 Calidad de los datos


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

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 21), ('counts_nas', 21)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="dda659fc-61b7-465d-800c-0d97e2689d59"></div>








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
      <td>0.000000</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>subrack_status</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>82.336182</td>
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
      <td>100.000000</td>
    </tr>
    <tr>
      <th>description</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>82.478632</td>
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
      <td>100.000000</td>
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









  <div class="bk-root" id="d5dabffa-377c-42ca-a17f-fc3ae77fc153"></div>








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
      <td>100.000000</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>alias</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>subrack_status</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>snbar_code</th>
      <td>17.663818</td>
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
      <td>0.000000</td>
    </tr>
    <tr>
      <th>description</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>17.521368</td>
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
      <td>0.000000</td>
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
df_2.dtypes
```




    ne                          object
    subrack_name                object
    subrack_type                object
    subrack_id                  object
    software_version           float64
    ne_id                      float64
    alias                       object
    subrack_status              object
    snbar_code                  object
    telecommunications_room    float64
    rack                       float64
    subrack_no                 float64
    pnbom_codeitem             float64
    description                float64
    manufacture_date            object
    subnet                      object
    subnet_path                 object
    equipment_no               float64
    remarks                    float64
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

## 5.2  Métricas KPI.



```python
Total_Elementos=df_2.shape[0]
Total_Elementos
```




    702




```python
df_2.replace(np.NaN,'vacio',inplace=True)

```

#### Total Elementos Trazables



```python
Total_Tr=df_2.loc[(df_2.snbar_code!='vacio') ].shape[0]
Total_Tr
```




    124



#### Total Elementos NO Trazables



```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    578



#### Total Elementos Trazables Únicos



```python
Total_Tr_Unic=df_2[['snbar_code']].loc[(df_2.snbar_code!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic
```




    123



#### Total de elementos trazables duplicados



```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    1



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
      <td>702</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>124</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>578</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>123</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>1</td>
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
df_hive_kpis_final.write.mode("overwrite").saveAsTable("rci_network_db.kpi_u2000_gpon_subrack")
```

[img1]: ./image/axity-logo.png "Logo Axity"
[img2]: images/U2000GPON-eda-01.png "Board Type"
[img3]: images/U2000GPON-eda-02.png "Board Status"
[img4]: images/U2000GPON-eda-03.png "Hardware Version"
[img5]: images/U2000GPON-eda-04.png "NE Type"
[img6]: images/U2000GPON-eda-05.png "Physical Location"
[img7]: images/U2000GPON-eda-06.png "NE Subtype"
[img8]: images/U2000GPON-eda-07.png "Running Status"