
<div style="width: 100%; clear: both; font-family: Verdana;">
<div style="float: left; width: 50%;font-family: Verdana;">
<img src="https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Digidata_NETCM/image/encabezado.png" align="left">
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
Analizaremos los datos de las fuentes de inventarios de AT&T con un tratamiento estadístico descriptivo para hacer el tracking del ciclo de vida de los elementos de red. Se creará un EDA enfocado a la salida de almacén. Serán documentados los catálogos propuestos junto a su respectivo tratamiento de datos. La fuente que corresponde a este análisis es:

* **GESTOR DIGIDATA**

Primero cargamos las librerías necesarias.

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

```


```python
conf = SparkConf().setAppName('tx_netcm_cisco_epn')  \
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
        <span id="923e0e82-4acf-4532-a766-ee572aab3bc8">Loading BokehJS ...</span>
    </div>




# NETCM

## 1.1 NETCM Cisco EPN

### Recolección de los datos: 

Para analizar el gestor NETCM en conjunto, se realiza una unión de las fuentes huawei_cobs y huawei_bts para trabajar una parte del universo de NETCM.

La tablas que se utilizan como fuentes son ```tx_netcm_huawei_cobs```, ```tx_netcm_huawei_bts```, ```tx_netcm_cisco_epn``` y ```tx_netcm_ericsson```.

El campo utilizado para la unión de las tablas de huawei es: ```serial_number```.

Los datos con los que se trabajan a lo largo del EDA corresponden a la partición de **201911** para todas las tablas.

*IMPORTANTE*: Si se requieren ver datos de otro periodo, se debe cambiar los filtros ```year = <año-a-ejecutar>```, ```month = <mes-a-ejecutar>```, ```day = <día-a-ejecutar>``` de las tablas en la siguiente celda:

<div style="width: 100%; clear: both; font-family: Verdana;">
    <p> 
    Se crea el dataframe de spark
    </p>
</div>


```python
df_load =spark.sql("select * from tx_netcm_cisco_epn where year = 2019 and month=11").cache()#.toPandas() 
```


```python
df_load.columns
```




    ['omip',
     'productfamily',
     'creationtime',
     'nodename',
     'softwaretype',
     'managementstatus',
     'ipaddress',
     'devicename',
     'serial_number',
     'sheet_name',
     'technology',
     'manufacturerpartnr',
     'adminstatus',
     'location',
     'reachability',
     'devicetypeparameter',
     'filedate',
     'filename',
     'hash_id',
     'sourceid',
     'registry_state',
     'datasetname',
     'timestamp',
     'transaction_status',
     'year',
     'month',
     'day']



<div style="width: 100%; clear: both; font-family: Verdana;">
    <p> 
    Creamos una funcion para el tratamiento de datos en spark el cual contiene la reglas definidas para la columna serie:
    </p>
</div>


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

<div style="width: 100%; clear: both; font-family: Verdana;">
    <p> 
    Se crea un udf en spark sobre la funcion ya creada 
    </p>
</div>


```python
validate_rule_udf = udf(validate_rule, IntegerType())
```

<div style="width: 100%; clear: both; font-family: Verdana;">
    <p> 
    Se le agrega una nueva columna al dataframe de spark; la nueva columna es la validacion de la columna serie con respecto al udf que creamos.
    </p>
</div>


```python
df_serie = df_load.withColumn("serie_cleaned",validate_rule_udf(col("serial_number"))).cache()
```

<div style="width: 100%; clear: both; font-family: Verdana;">
    <p> 
    Se convierte el dataframe de spark a un dataframe de pandas 
    </p>
</div>


```python
df = df_serie.toPandas()
```

Hemos recolectado los campos a analizar de la fuente NOMBRE_SOURCE.

### Gestor NETCM CISCO EPN
Cargamos una muestra de la fuente tx_netcm_cisco_epn


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
      <th>omip</th>
      <th>productfamily</th>
      <th>creationtime</th>
      <th>nodename</th>
      <th>softwaretype</th>
      <th>managementstatus</th>
      <th>ipaddress</th>
      <th>devicename</th>
      <th>serial_number</th>
      <th>sheet_name</th>
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
      <td></td>
      <td>Generic Cisco Device Family</td>
      <td>2019-09-23T17:29:16.245-05:00</td>
      <td></td>
      <td>IOS-XE</td>
      <td>MANAGED_AND_SYNCHRONIZED</td>
      <td>10.241.104.55</td>
      <td>MXTAMREY1591RTBHCSRMOB01.att.com</td>
      <td></td>
      <td>0 - Cisco EPNM - Audit ALL Site</td>
      <td>...</td>
      <td>d81c258a191fc5776e56c3551d7ffb55ef93f1498f3b00...</td>
      <td>Gestores-NETCM</td>
      <td>2019:10:26:17:32:39</td>
      <td>tx_netcm_cisco_epn</td>
      <td>20191126</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td></td>
      <td>Generic Cisco Device Family</td>
      <td>2019-09-23T11:46:29.120-05:00</td>
      <td></td>
      <td>IOS-XE</td>
      <td>MANAGED_AND_SYNCHRONIZED</td>
      <td>10.241.96.202</td>
      <td>MXNLEGDP1440RTBHCSRMOB01.att.com</td>
      <td></td>
      <td>0 - Cisco EPNM - Audit ALL Site</td>
      <td>...</td>
      <td>346287408daefb2a1e2ea110b52225fb2e73d5804965c9...</td>
      <td>Gestores-NETCM</td>
      <td>2019:10:26:17:32:39</td>
      <td>tx_netcm_cisco_epn</td>
      <td>20191126</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td></td>
      <td>Generic Cisco Device Family</td>
      <td>2019-09-23T11:46:14.652-05:00</td>
      <td></td>
      <td>IOS-XE</td>
      <td>MANAGED_AND_SYNCHRONIZED</td>
      <td>10.241.96.208</td>
      <td>MXNLEJRZ1489RTBHCSRMOB01.att.com</td>
      <td></td>
      <td>0 - Cisco EPNM - Audit ALL Site</td>
      <td>...</td>
      <td>43228acda9e7f3d269a62f64059fb8288979a4f7ca418e...</td>
      <td>Gestores-NETCM</td>
      <td>2019:10:26:17:32:39</td>
      <td>tx_netcm_cisco_epn</td>
      <td>20191126</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td></td>
      <td>Generic Cisco Device Family</td>
      <td>2019-09-23T11:45:50.092-05:00</td>
      <td></td>
      <td>IOS-XE</td>
      <td>MANAGED_AND_SYNCHRONIZED</td>
      <td>10.241.96.207</td>
      <td>MXNLEJRZ0707RTBHCSRMOB01.att.com</td>
      <td></td>
      <td>0 - Cisco EPNM - Audit ALL Site</td>
      <td>...</td>
      <td>083bf9b89c8d4ea526d86a7cbfe3afa397dd3c24db30f6...</td>
      <td>Gestores-NETCM</td>
      <td>2019:10:26:17:32:39</td>
      <td>tx_netcm_cisco_epn</td>
      <td>20191126</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td></td>
      <td>Generic Cisco Device Family</td>
      <td>2019-09-23T11:45:32.725-05:00</td>
      <td></td>
      <td>IOS-XE</td>
      <td>MANAGED_AND_SYNCHRONIZED</td>
      <td>10.241.96.204</td>
      <td>MXNLEJRZ0698RTBHCSRMOB01.att.com</td>
      <td></td>
      <td>0 - Cisco EPNM - Audit ALL Site</td>
      <td>...</td>
      <td>4f637b2c9bbe37c43fac3192f3efa88a342d2eb9b92945...</td>
      <td>Gestores-NETCM</td>
      <td>2019:10:26:17:32:39</td>
      <td>tx_netcm_cisco_epn</td>
      <td>20191126</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>5</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 28 columns</p>
</div>



### Diccionario de datos.
A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

* **omip**: ID del negocio.
* **productfamily**: Familia de productos al que pertenece.
* **creationtime**: Fecha de creacion, validar si es de carga.
* **nodename**: Pendiente.
* **softwaretype**: Tipo de Software.
* **managementstatus**: Pendiente, es un estatus.
* **ipaddress**: Direccion IP.
* **devicename**: Nombre del dispositivo.
* **serial_number**: Numero de serie.
* **sheet_name**: Nombre del sheet.
* **technology**: Pendiente.
* **manufacturerpartnr**: Partner.
* **adminstatus**: Estado.
* **location**: Locacion.
* **reachability**: Pendiente.
* **devicetypeparameter**: Pendiente.
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

## 2. Descripción de las fuentes
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos=df.columns
print('Columnas de la fuente SOURCE son: ',list(campos))
pd.DataFrame(df.dtypes,columns=['Tipo de objeto SOURCE'])
```

    ('Columnas de la fuente SOURCE son: ', ['omip', 'productfamily', 'creationtime', 'nodename', 'softwaretype', 'managementstatus', 'ipaddress', 'devicename', 'serial_number', 'sheet_name', 'technology', 'manufacturerpartnr', 'adminstatus', 'location', 'reachability', 'devicetypeparameter', 'filedate', 'filename', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie_cleaned'])





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
      <th>Tipo de objeto SOURCE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>omip</th>
      <td>object</td>
    </tr>
    <tr>
      <th>productfamily</th>
      <td>object</td>
    </tr>
    <tr>
      <th>creationtime</th>
      <td>object</td>
    </tr>
    <tr>
      <th>nodename</th>
      <td>object</td>
    </tr>
    <tr>
      <th>softwaretype</th>
      <td>object</td>
    </tr>
    <tr>
      <th>managementstatus</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ipaddress</th>
      <td>object</td>
    </tr>
    <tr>
      <th>devicename</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sheet_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>technology</th>
      <td>object</td>
    </tr>
    <tr>
      <th>manufacturerpartnr</th>
      <td>object</td>
    </tr>
    <tr>
      <th>adminstatus</th>
      <td>object</td>
    </tr>
    <tr>
      <th>location</th>
      <td>object</td>
    </tr>
    <tr>
      <th>reachability</th>
      <td>object</td>
    </tr>
    <tr>
      <th>devicetypeparameter</th>
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

    ('renglones = ', 86138, ' columnas = ', 28)



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
      <th>omip</th>
      <th>productfamily</th>
      <th>creationtime</th>
      <th>nodename</th>
      <th>softwaretype</th>
      <th>managementstatus</th>
      <th>ipaddress</th>
      <th>devicename</th>
      <th>serial_number</th>
      <th>sheet_name</th>
      <th>technology</th>
      <th>manufacturerpartnr</th>
      <th>adminstatus</th>
      <th>location</th>
      <th>reachability</th>
      <th>devicetypeparameter</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138</td>
      <td>86138.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>1140</td>
      <td>8</td>
      <td>1878</td>
      <td>1139</td>
      <td>5</td>
      <td>6</td>
      <td>1916</td>
      <td>1905</td>
      <td>1138</td>
      <td>14</td>
      <td>2</td>
      <td>5</td>
      <td>4</td>
      <td>365</td>
      <td>4</td>
      <td>30</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td></td>
      <td>Routers</td>
      <td></td>
      <td></td>
      <td>IOS-XE</td>
      <td>MANAGED_AND_SYNCHRONIZED</td>
      <td></td>
      <td></td>
      <td></td>
      <td>Cisco EPNM - Node Inventory wit</td>
      <td></td>
      <td></td>
      <td>Managed</td>
      <td>CDMX</td>
      <td>REACHABLE</td>
      <td>Cisco ASR 920-12SZ-IM Router</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>72482</td>
      <td>58046</td>
      <td>13656</td>
      <td>72482</td>
      <td>69574</td>
      <td>63398</td>
      <td>13656</td>
      <td>13656</td>
      <td>72482</td>
      <td>25433</td>
      <td>72482</td>
      <td>72482</td>
      <td>71870</td>
      <td>22682</td>
      <td>71002</td>
      <td>41244</td>
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
      <td>0.158536</td>
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
      <td>0.365245</td>
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
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
df["managementstatus"].unique()
```




    array([u'MANAGED_AND_SYNCHRONIZED', u'MANAGED_BUT_CONFLICTINGCREDENTIALS',
           u'MANAGED_BUT_OUTOFSYNC', u'INSERVICE_MAINTENANCE',
           u'MANAGED_BUT_INCOMPLETE', u''], dtype=object)



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

* Como se puede observar las columnas que mas se adecuan para ser un catalogo son productfamily,softwaretype, managementstatus y managementstatus, ya que son columnas que nos proporciona una forma de clasificacion y agrupacion del set de datos, y son columnas que tienen valor ya que no es un campo alfanumerico y es entedible.


#### Se proponen catálogos derivados de la fuente tx_netcm_cisco_epn con los siguientes campos:
    
* **productfamily**: Familia de productos.
* **softwaretype**: Tipo de software.
* **managementstatus**: Estado.
* **manufacturerpartnr**: Partner.

Estos catálogos nos ayudarán a mapear todos los diferentes proyectos que existen en los cuales hay un activo.


## 3. Exploración de los datos
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
#Se puede hacer más y por columna en caso de ser necesario
```


```python
df.productfamily.replace("GenericCisco Device Family","Generic Cisco Device Family",inplace=True)
df.productfamily.replace("Generic CiscoDevice Family","Generic Cisco Device Family",inplace=True)
df.productfamily.replace("Generic Cisco DeviceFamily","Generic Cisco Device Family",inplace=True)
df.productfamily.replace("Generic Cisco Device Family","Generic Cisco Device Family",inplace=True)

```

### Primer catálogo: *productfamily*

Empezaremos con el catálogo de productfamily. Este catalogo nos permite concer y agrupar los datos por medio de la familia del producto. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
campo_productfamily=pd.DataFrame(df.productfamily.value_counts())

#print campo_productfamily['productfamily'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_productfamily.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'NOMBRE productfamily')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'NOMBRE DEL CHART')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_productfamily['productfamily'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'NOMBRE DEL CHART',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_productfamily.index,loc='upper left')

plt.show()
```


![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Digidata/image/output_39_0.png)


Podemos observar en primer lugar, que se necesitan reglas de limpieza, existen outliers que al parecer son datos sucios.
Se llamará al catálogo limpio en el apartado de catálogos.

### Segundo catálogo: *softwaretype*

El siguiente catálogo es softwaretype. Este catalogo nos permite concer y agrupar los datos por medio de la familia del tipo de software. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
campo_softwaretype=pd.DataFrame(df.softwaretype.value_counts())

#print campo_softwaretype['softwaretype'].size
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_softwaretype.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'NOMBRE softwaretype')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'NOMBRE DEL CHART')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_softwaretype['softwaretype'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'NOMBRE DEL CHART',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_softwaretype.index,loc='upper left')

plt.show()
```


![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Digidata/image/output_43_0.png)


### Tercer catálogo: *managementstatus*

El siguiente catálogo es managementstatus. Este catalogo nos permite concer y agrupar los datos por medio del estado. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
campo_managementstatus=pd.DataFrame(df.managementstatus.value_counts())

#print campo_managementstatus['managementstatus'].size
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_managementstatus.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'NOMBRE managementstatus')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'NOMBRE DEL CHART')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15,0,0] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_managementstatus['managementstatus'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'NOMBRE DEL CHART',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_managementstatus.index,loc='upper left')

plt.show()
```


![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Digidata/image/output_46_0.png)


#### Visualización de los datos de trazabilidad: 

Creamos una tabla donde se observarán los número de serie repetidos para un mejor análisis.


```python
pd.DataFrame(df.serial_number.value_counts()[:15])
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
      <th>serial_number</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>CAT1944U1S6</th>
      <td>24</td>
    </tr>
    <tr>
      <th>CAT2145U2WL</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT1941U2ST</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT1947U1PH</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT2122U5BP</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT2106U78T</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT2122U5BW</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT1947U1PQ</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT2145U2WF</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT2122U5B8</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT2124U5GY</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT2124U5GP</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT2124U5GM</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT2124U5GL</th>
      <td>12</td>
    </tr>
    <tr>
      <th>CAT1940U322</th>
      <td>12</td>
    </tr>
  </tbody>
</table>
</div>



## 4 Calidad de los datos
Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

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

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 17), ('counts_nas', 17)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="5fa626df-14bf-4ca0-bb2d-e9b394ce7f21"></div>








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
      <th>omip</th>
      <td>84.146370</td>
    </tr>
    <tr>
      <th>productfamily</th>
      <td>16.243702</td>
    </tr>
    <tr>
      <th>creationtime</th>
      <td>15.853630</td>
    </tr>
    <tr>
      <th>nodename</th>
      <td>84.146370</td>
    </tr>
    <tr>
      <th>softwaretype</th>
      <td>16.431772</td>
    </tr>
    <tr>
      <th>managementstatus</th>
      <td>15.853630</td>
    </tr>
    <tr>
      <th>ipaddress</th>
      <td>15.853630</td>
    </tr>
    <tr>
      <th>devicename</th>
      <td>16.243702</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>84.146370</td>
    </tr>
    <tr>
      <th>sheet_name</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>technology</th>
      <td>84.146370</td>
    </tr>
    <tr>
      <th>manufacturerpartnr</th>
      <td>84.146370</td>
    </tr>
    <tr>
      <th>adminstatus</th>
      <td>15.853630</td>
    </tr>
    <tr>
      <th>location</th>
      <td>16.362117</td>
    </tr>
    <tr>
      <th>reachability</th>
      <td>15.853630</td>
    </tr>
    <tr>
      <th>devicetypeparameter</th>
      <td>16.243702</td>
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

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 17), ('counts_nas', 17)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="47eebec8-ab99-464d-813e-b0a34a97c81f"></div>








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
      <th>omip</th>
      <td>15.853630</td>
    </tr>
    <tr>
      <th>productfamily</th>
      <td>83.756298</td>
    </tr>
    <tr>
      <th>creationtime</th>
      <td>84.146370</td>
    </tr>
    <tr>
      <th>nodename</th>
      <td>15.853630</td>
    </tr>
    <tr>
      <th>softwaretype</th>
      <td>83.568228</td>
    </tr>
    <tr>
      <th>managementstatus</th>
      <td>84.146370</td>
    </tr>
    <tr>
      <th>ipaddress</th>
      <td>84.146370</td>
    </tr>
    <tr>
      <th>devicename</th>
      <td>83.756298</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>15.853630</td>
    </tr>
    <tr>
      <th>sheet_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>technology</th>
      <td>15.853630</td>
    </tr>
    <tr>
      <th>manufacturerpartnr</th>
      <td>15.853630</td>
    </tr>
    <tr>
      <th>adminstatus</th>
      <td>84.146370</td>
    </tr>
    <tr>
      <th>location</th>
      <td>83.637883</td>
    </tr>
    <tr>
      <th>reachability</th>
      <td>84.146370</td>
    </tr>
    <tr>
      <th>devicetypeparameter</th>
      <td>83.756298</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



Se observa que en todas las columnas tienen cierto nivel de missings, pero los que destacan son omip,nodename,technology, manufacturerpartnr 

## 5. Catálogos

#### Catálogo de productfamily:


```python
Catalogo_productfamily=pd.DataFrame(df.productfamily.unique())
Catalogo_productfamily.columns=['productfamily']

#Remover los sucios
#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios, un ejemplo puede ser:
#Catalogo_CAMPO.drop(labels=[67,346,369,279,171,313],axis=0,inplace=True)

#Se le da 
Catalogo_productfamily.reset_index(drop=True)
Catalogo_productfamily.dropna(inplace=True)
Catalogo_productfamily.sort_values(by='productfamily').head(10)
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
      <th>productfamily</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Generic Cisco Device Family</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Routers</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Switches and Hubs</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de softwaretype:


```python
Catalogo_softwaretype=pd.DataFrame(df.softwaretype.unique())
Catalogo_softwaretype.columns=['productfamily']

#Remover los sucios
#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios, un ejemplo puede ser:
#Catalogo_CAMPO.drop(labels=[67,346,369,279,171,313],axis=0,inplace=True)

#Se le da 
Catalogo_softwaretype.reset_index(drop=True)
Catalogo_softwaretype.dropna(inplace=True)
Catalogo_softwaretype.sort_values(by='productfamily').head(10)
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
      <th>productfamily</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>IOS XR</td>
    </tr>
    <tr>
      <th>0</th>
      <td>IOS-XE</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NX-OS</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de managementstatus:


```python
Catalogo_managementstatus=pd.DataFrame(df.managementstatus.unique())
Catalogo_managementstatus.columns=['managementstatus']

#Remover los sucios
#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios, un ejemplo puede ser:
#Catalogo_CAMPO.drop(labels=[67,346,369,279,171,313],axis=0,inplace=True)

#Se le da 
Catalogo_managementstatus.reset_index(drop=True)
Catalogo_managementstatus.dropna(inplace=True)
Catalogo_managementstatus.sort_values(by='managementstatus').head(10)
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
      <th>managementstatus</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3</th>
      <td>INSERVICE_MAINTENANCE</td>
    </tr>
    <tr>
      <th>0</th>
      <td>MANAGED_AND_SYNCHRONIZED</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MANAGED_BUT_CONFLICTINGCREDENTIALS</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MANAGED_BUT_INCOMPLETE</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MANAGED_BUT_OUTOFSYNC</td>
    </tr>
  </tbody>
</table>
</div>



## 6. Preparación de los datos
Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos: 

* **serie:**
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

* **marca**: REGLA DE LIMPIEZA.
    * Se eliminan los siguientes caracteres especiales:    '-','#','%','/','_'
    * replace('ALACATEL LUCENT','ALCATEL LUCENT')
    * replace('ALCATEL . LUCENT','ALCATEL LUCENT')
    * replace('ALCATEL TLUCEN','ALCATEL LUCENT')
    * replace('ALCATEL.LUCENT','ALCATEL LUCENT')
    * replace('A 10','A10')
    * replace('ALCATEL-LUNCENT','ALCATEL LUCENT')
    * replace(especiales,' ',)

* Pasar todo a uppercase


```python
df['trazabilidad']=0
df.trazabilidad.loc[(df.serie_cleaned==0) ]=1
#CS CA
df['CS_CA']=0
df.CS_CA.loc[(df.serie_cleaned==0) ]=1
#CS SA
df['CS_SA']=0
df.CS_SA.loc[(df.serie_cleaned==0) ]=1
#SS CA
df['SS_CA']=0
df.SS_CA.loc[(df.serie_cleaned==1) ]=1
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/pandas/core/indexing.py:189: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self._setitem_with_indexer(indexer, value)



```python
df.dtypes
```




    omip                   object
    productfamily          object
    creationtime           object
    nodename               object
    softwaretype           object
    managementstatus       object
    ipaddress              object
    devicename             object
    serial_number          object
    sheet_name             object
    technology             object
    manufacturerpartnr     object
    adminstatus            object
    location               object
    reachability           object
    devicetypeparameter    object
    filedate                int64
    filename               object
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
    CS_CA                   int64
    CS_SA                   int64
    SS_CA                   int64
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


```python
#df_hive_tx_netcm_cisco_epn = spark.createDataFrame(df,schema=mySchema)
```


```python
#df_hive_tx_netcm_cisco_epn.write.mode("overwrite").saveAsTable("default.eda_tx_netcm_cisco_epn")

```

## 7 Métricas KPI

Se mostrarán los KPIs generados. 


```python
Total_Elementos=df.shape[0]
Total_Elementos
```




    86138




```python
df.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables


```python
Total_Tr=df.loc[(df.serial_number!='vacio') ].shape[0]
Total_Tr
```




    13656



#### Total Elementos NO Trazables


```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    72482



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=df[['serial_number']].loc[(df.serial_number!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic
```




    1137



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    12519




```python
df.columns
```




    Index([u'omip', u'productfamily', u'creationtime', u'nodename',
           u'softwaretype', u'managementstatus', u'ipaddress', u'devicename',
           u'serial_number', u'sheet_name', u'technology', u'manufacturerpartnr',
           u'adminstatus', u'location', u'reachability', u'devicetypeparameter',
           u'filedate', u'filename', u'hash_id', u'sourceid', u'registry_state',
           u'datasetname', u'timestamp', u'transaction_status', u'year', u'month',
           u'day', u'serie_cleaned', u'trazabilidad', u'CS_CA', u'CS_SA',
           u'SS_CA'],
          dtype='object')



### EN CASO DE EXISTIR NOMBRE DE ALMACENES:

#### Total de elementos en almacén Trazables Únicos en NOMBREALMACEN


```python
NOMBREALMACEN_Tr_Unic=df[['serial_number']].loc[((df.serial_number!='vacio') )].drop_duplicates().shape[0]
NOMBREALMACEN_Tr_Unic
```




    1137



#### Total de elementos en almacén Trazables Únicos con NSerie, con Nactivo


```python
Total_Tr_Unic_CS_CA=df[['serial_number']].loc[(df.serial_number!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_CS_CA
```




    1137



#### Total de elementos en almacén Trazables Únicos con NSerie, sin Nactivo 


```python
Total_Tr_Unic_CS_SA=df[['serial_number']].loc[(df.serial_number!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic_CS_SA
```




    1137



#### Total de elementos en almacén Trazables Únicos sin NSerie, con Nactivo


```python
Total_Tr_Unic_SS_CA=df[['serial_number']].loc[(df.serial_number=='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic_SS_CA
```




    1



### KPIS


```python
#Ajustar el df contra los kpis de la siguiente tabla:

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
      <td>86138</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>13656</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>72482</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>1137</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>12519</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Total CS CA</td>
      <td>1137</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Total CS SA</td>
      <td>1137</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Total SS CA</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



## 1.2 NETCM ERICSSON 

### Recolección de los datos:

Se crea el dataframe de spark




```python
df_load_2 =spark.sql("SELECT * FROM tx_netcm_ericsson where year = 2019 and month=11").cache()#.toPandas() 
```


```python
df_load_1_2019_10 = df_load_2.withColumn("serie_cleaned",validate_rule_udf(col("serialnumber"))).cache()
```

Se carga a pandas


```python
df_1 = df_load_1_2019_10.toPandas()
```

### Gestor NETCM ERICSSON


Una muestra de la fuente tx_netcm_ericsson



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
      <th>site</th>
      <th>ru</th>
      <th>operstate</th>
      <th>rnc</th>
      <th>antennaserialnumber</th>
      <th>node</th>
      <th>rurevision</th>
      <th>maxsupportedelectricaltilt</th>
      <th>bootrom</th>
      <th>state</th>
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
      <td>CHHJRZ0146</td>
      <td>2</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>1/BFL 901 009/4       R2B</td>
      <td></td>
      <td></td>
      <td>OPER</td>
      <td>...</td>
      <td>545b2046fe000aa9a593211fca2658c1b1b0476fb93428...</td>
      <td>Gestores-NETCM</td>
      <td>2019:10:27:17:57:27</td>
      <td>tx_netcm_ericsson</td>
      <td>20191127</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>16</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CHHJRZ0146</td>
      <td>0 &amp; 5 &amp; 6</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>KRC 161 299/2         R1M</td>
      <td></td>
      <td></td>
      <td>OPER &amp; OPER &amp; OPER &amp; OPER &amp; OPER</td>
      <td>...</td>
      <td>545b2046fe000aa9a593211fca2658c1b1b0476fb93428...</td>
      <td>Gestores-NETCM</td>
      <td>2019:10:27:17:57:27</td>
      <td>tx_netcm_ericsson</td>
      <td>20191127</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>16</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHHJRZ0146</td>
      <td>0 &amp; 7 &amp; 8</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>KRC 161 299/2         R1M</td>
      <td></td>
      <td></td>
      <td>OPER &amp; OPER &amp; OPER &amp; OPER &amp; OPER</td>
      <td>...</td>
      <td>545b2046fe000aa9a593211fca2658c1b1b0476fb93428...</td>
      <td>Gestores-NETCM</td>
      <td>2019:10:27:17:57:27</td>
      <td>tx_netcm_ericsson</td>
      <td>20191127</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>16</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>CHHJRZ0146</td>
      <td>0 &amp; 3 &amp; 4</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>KRC 161 299/2         R1M</td>
      <td></td>
      <td></td>
      <td>OPER &amp; OPER &amp; OPER &amp; OPER &amp; OPER</td>
      <td>...</td>
      <td>545b2046fe000aa9a593211fca2658c1b1b0476fb93428...</td>
      <td>Gestores-NETCM</td>
      <td>2019:10:27:17:57:27</td>
      <td>tx_netcm_ericsson</td>
      <td>20191127</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>16</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>CHHJRZ0146</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>527/BFL 901 009       R1A</td>
      <td></td>
      <td></td>
      <td>OPER</td>
      <td>...</td>
      <td>545b2046fe000aa9a593211fca2658c1b1b0476fb93428...</td>
      <td>Gestores-NETCM</td>
      <td>2019:10:27:17:57:27</td>
      <td>tx_netcm_ericsson</td>
      <td>20191127</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>16</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 53 columns</p>
</div>




```python
df_1.columns
```




    Index([u'site', u'ru', u'operstate', u'rnc', u'antennaserialnumber', u'node',
           u'rurevision', u'maxsupportedelectricaltilt', u'bootrom', u'state',
           u'btsswver', u'eq_class', u'f_timestamp', u'rulogicalid', u'adminstate',
           u'productname', u'bsc', u'productiondate', u'prodname',
           u'minsupportedelectricaltilt', u'electricalantennatilt', u'powerstate',
           u'tg_count', u'productrevision', u'serialno', u'ruserialno_count',
           u'mo', u'serialnumber', u'antennamodelnumber', u'prodno', u'ruserialno',
           u'productnumber', u'eq', u'nodeb', u'sheet_name', u'type', u'manweek',
           u'tg', u'revision', u'fsbrole', u'enodeb', u'filedate', u'filename',
           u'hash_id', u'sourceid', u'registry_state', u'datasetname',
           u'timestamp', u'transaction_status', u'year', u'month', u'day',
           u'serie_cleaned'],
          dtype='object')




```python
df_1["bootrom"].unique
```




    <bound method Series.unique of 0          
    1          
    2          
    3          
    4          
    5          
    6          
    7          
    8          
    9          
    10         
    11         
    12         
    13         
    14         
    15         
    16         
    17         
    18         
    19         
    20         
    21         
    22         
    23         
    24         
    25         
    26         
    27         
    28         
    29         
             ..
    360281     
    360282     
    360283     
    360284     
    360285     
    360286     
    360287     
    360288     
    360289     
    360290     
    360291     
    360292     
    360293     
    360294     
    360295     
    360296     
    360297     
    360298     
    360299     
    360300     
    360301     
    360302     
    360303     
    360304     
    360305     
    360306     
    360307     
    360308     
    360309     
    360310     
    Name: bootrom, Length: 360311, dtype: object>



### Diccionario de datos.

A continuación se enlistan los campos de la fuente con una breve descripción de negocio.



* **site**: Sitio.
* **operstate**: Pendiente.
* **rnc**: Pendiente.
* **antennaserialnumber**: Numero de seria de la antena.
* **node**: Nodo.
* **rurevision**: Pendiente.
* **maxsupportedelectricaltilt**: Maximo soporte electrico.
* **bootrom**: Pendiente.
* **state**: Estado.
* **btsswver**: Pendiente.
* **eq_class**: Pendiente.
* **f_timestamp**: Fecha y hora.
* **rulogicalid**: Pendiente, podria ser un id.
* **adminstate**: Estado de admin.
* **productname**: Nombre de producto.
* **bsc**: Pendiente.
* **productiondate**: Fecha del producto.
* **prodname**: Nombre del producto.
* **minsupportedelectricaltilt**: Pendiente.
* **electricalantennatilt**: Pendiente.
* **powerstate**: Estado de la carga
* **tg_count**: Conteo
* **productrevision**: Revision de producto
* **serialno**: Serial
* **ruserialno_count**: Conteo de serial
* **mo**: Pendiente
* **serialnumber**: Numero de serie
* **antennamodelnumber**: Numero del modelo de antena
* **ruserialno**: Pendiente.
* **productnumber**: Numero de producto
* **eq**: Pendiente
* **nodeb**: Pendiente.
* **sheet_name**: Nombre del sheet.
* **type**: Tipo.
* **manweek**: Pendiente.
* **tg**: Pendiente.
* **revision**: Revision.
* **fsbrole**: Pendiente.
* **filedate**: Fecha de carga del archivo fuente.
* **filename**: Nombre del archivo fuente.
* **hash_id**: Identificador único hash de la fuente.
* **sourceid**: Fuente de archivo.
* **registry_state**: Timestamp de carga.
* **datasetname**: Nombre indentificador de la fuente.
* **timestamp**: Fecha de carga.
* **transaction_status**: Estatus de registro.
* **year**: Año de la partición.
* **month**: Mes de la partición.
* **day**: Día de la partición.


## 2.1 Descripción de las fuentes

En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos_1=df_1.columns
print('Columnas de la fuente SOURCE son: ',list(campos_1))
pd.DataFrame(df_1.dtypes,columns=['Tipo de objeto SOURCE'])
```

    ('Columnas de la fuente SOURCE son: ', ['site', 'ru', 'operstate', 'rnc', 'antennaserialnumber', 'node', 'rurevision', 'maxsupportedelectricaltilt', 'bootrom', 'state', 'btsswver', 'eq_class', 'f_timestamp', 'rulogicalid', 'adminstate', 'productname', 'bsc', 'productiondate', 'prodname', 'minsupportedelectricaltilt', 'electricalantennatilt', 'powerstate', 'tg_count', 'productrevision', 'serialno', 'ruserialno_count', 'mo', 'serialnumber', 'antennamodelnumber', 'prodno', 'ruserialno', 'productnumber', 'eq', 'nodeb', 'sheet_name', 'type', 'manweek', 'tg', 'revision', 'fsbrole', 'enodeb', 'filedate', 'filename', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie_cleaned'])





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
      <th>Tipo de objeto SOURCE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>site</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ru</th>
      <td>object</td>
    </tr>
    <tr>
      <th>operstate</th>
      <td>object</td>
    </tr>
    <tr>
      <th>rnc</th>
      <td>object</td>
    </tr>
    <tr>
      <th>antennaserialnumber</th>
      <td>object</td>
    </tr>
    <tr>
      <th>node</th>
      <td>object</td>
    </tr>
    <tr>
      <th>rurevision</th>
      <td>object</td>
    </tr>
    <tr>
      <th>maxsupportedelectricaltilt</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bootrom</th>
      <td>object</td>
    </tr>
    <tr>
      <th>state</th>
      <td>object</td>
    </tr>
    <tr>
      <th>btsswver</th>
      <td>object</td>
    </tr>
    <tr>
      <th>eq_class</th>
      <td>object</td>
    </tr>
    <tr>
      <th>f_timestamp</th>
      <td>object</td>
    </tr>
    <tr>
      <th>rulogicalid</th>
      <td>object</td>
    </tr>
    <tr>
      <th>adminstate</th>
      <td>object</td>
    </tr>
    <tr>
      <th>productname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bsc</th>
      <td>object</td>
    </tr>
    <tr>
      <th>productiondate</th>
      <td>object</td>
    </tr>
    <tr>
      <th>prodname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>minsupportedelectricaltilt</th>
      <td>object</td>
    </tr>
    <tr>
      <th>electricalantennatilt</th>
      <td>object</td>
    </tr>
    <tr>
      <th>powerstate</th>
      <td>object</td>
    </tr>
    <tr>
      <th>tg_count</th>
      <td>object</td>
    </tr>
    <tr>
      <th>productrevision</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serialno</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ruserialno_count</th>
      <td>object</td>
    </tr>
    <tr>
      <th>mo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serialnumber</th>
      <td>object</td>
    </tr>
    <tr>
      <th>antennamodelnumber</th>
      <td>object</td>
    </tr>
    <tr>
      <th>prodno</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ruserialno</th>
      <td>object</td>
    </tr>
    <tr>
      <th>productnumber</th>
      <td>object</td>
    </tr>
    <tr>
      <th>eq</th>
      <td>object</td>
    </tr>
    <tr>
      <th>nodeb</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sheet_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>manweek</th>
      <td>object</td>
    </tr>
    <tr>
      <th>tg</th>
      <td>object</td>
    </tr>
    <tr>
      <th>revision</th>
      <td>object</td>
    </tr>
    <tr>
      <th>fsbrole</th>
      <td>object</td>
    </tr>
    <tr>
      <th>enodeb</th>
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

    ('renglones = ', 360311, ' columnas = ', 53)



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
      <th>site</th>
      <th>ru</th>
      <th>operstate</th>
      <th>rnc</th>
      <th>antennaserialnumber</th>
      <th>node</th>
      <th>rurevision</th>
      <th>maxsupportedelectricaltilt</th>
      <th>bootrom</th>
      <th>state</th>
      <th>...</th>
      <th>eq</th>
      <th>nodeb</th>
      <th>sheet_name</th>
      <th>type</th>
      <th>manweek</th>
      <th>tg</th>
      <th>revision</th>
      <th>fsbrole</th>
      <th>enodeb</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>...</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311</td>
      <td>360311.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>242</td>
      <td>15</td>
      <td>2</td>
      <td>13</td>
      <td>3044</td>
      <td>3</td>
      <td>32</td>
      <td>13</td>
      <td>3</td>
      <td>24</td>
      <td>...</td>
      <td>43</td>
      <td>1854</td>
      <td>8</td>
      <td>4</td>
      <td>18</td>
      <td>185</td>
      <td>4</td>
      <td>4</td>
      <td>945</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>100</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td>Ericsson BTS - Antenna Serial N</td>
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
      <td>335451</td>
      <td>335451</td>
      <td>358631</td>
      <td>131716</td>
      <td>131716</td>
      <td>358631</td>
      <td>335451</td>
      <td>136986</td>
      <td>358631</td>
      <td>335451</td>
      <td>...</td>
      <td>358631</td>
      <td>131716</td>
      <td>182803</td>
      <td>358631</td>
      <td>358631</td>
      <td>335451</td>
      <td>358631</td>
      <td>358631</td>
      <td>255135</td>
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
      <td>0.291792</td>
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
      <td>0.454588</td>
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
<p>11 rows × 42 columns</p>
</div>




```python
df_1["antennamodelnumber"].unique()

```




    array([u'', u'80010510V01_B1', u'80010510V01_B2', u'NULL', u'HBXX3319DS',
           u'HBXX6516DS', u'HBXXX6516DS', u'2V65R18K-R', u'3V65R18K-T',
           u'3V65R18K-B', u'3V65R18K-M', u'2V65R18K-L', u'80010510V01',
           u'80010510V01_R', u'HBXX3817TB1', u'HBXX6516D5', u'HBX6513DS',
           u'80010622V01_Y2', u'80010622V01_Y1', u'ODI2-065R18K-GQ',
           u'HBXX6513DS', u'OPA65R-W4A-HW01', u'80010510V01_L',
           u'ODI3-065R18K-GQ', u'80010727_Y3', u'80010727_Y2', u'80010727_Y1',
           u'RVV-33B-R3', u'?????}z????????', u'???????????????'],
          dtype=object)



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

* Como se puede observar las columnas que mas se adecuan para ser un catalogo son rnc,node, type y revision, ya que son columnas que nos proporciona una forma de clasificacion y agrupacion del set de datos , y son columnas que pueden agregar cierto valor al negocio, solo se tiene que conocer bien el conexto, por  ejemplo la revision, el nodo, etc.

## 3.1 Exploración de los datos

#### Para empezar, se hará una limpieza general a los datos:


```python
df_1.replace('null',np.NaN,inplace=True)
df_1.replace('NA',np.NaN,inplace=True)
df_1.replace('na',np.NaN,inplace=True)
df_1.replace('NULL',np.NaN,inplace=True)
df_1.replace('<NULL>',np.NaN,inplace=True)
df_1.replace(' ',np.NaN,inplace=True)
df_1.replace('',np.NaN,inplace=True)
```

### Primer catálogo: rnc


```python
#Revisamos frecuencias:
campo_rnc =pd.DataFrame(df_1.rnc.value_counts())
#print campo_rnc['rnc'].size

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_rnc.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'NOMBRE rnc')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'NOMBRE DEL CHART')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_rnc['rnc'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'NOMBRE DEL CHART',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_rnc.index,loc='upper left')

plt.show()

```


![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Digidata/image/output_121_0.png)


### Segundo catálogo: type


```python
campo_type=pd.DataFrame(df_1.type.value_counts())

#print campo_type['type'].size
#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
campo_type.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'NOMBRE type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'NOMBRE DEL CHART')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
#explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
explode_list=[.2,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

campo_type['type'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'NOMBRE DEL CHART',y=1.12)
ax1.axis('equal')
ax1.legend(labels=campo_type.index,loc='upper left')

plt.show()
```


![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Digidata/image/output_123_0.png)


#### Visualización de los datos de trazabilidad:


```python
pd.DataFrame(df_1.serialnumber.value_counts()[:15])

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
      <th>serialnumber</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A530000003</th>
      <td>100</td>
    </tr>
    <tr>
      <th>CH40152173</th>
      <td>40</td>
    </tr>
    <tr>
      <th>TU8XZ65942</th>
      <td>40</td>
    </tr>
    <tr>
      <th>TU8XW69574</th>
      <td>40</td>
    </tr>
    <tr>
      <th>BR84749894</th>
      <td>40</td>
    </tr>
    <tr>
      <th>TU8XZ65840</th>
      <td>40</td>
    </tr>
    <tr>
      <th>TU8XZ65841</th>
      <td>40</td>
    </tr>
    <tr>
      <th>TU8XZ14882</th>
      <td>40</td>
    </tr>
    <tr>
      <th>CH40147665</th>
      <td>40</td>
    </tr>
    <tr>
      <th>TU8XZ65929</th>
      <td>40</td>
    </tr>
    <tr>
      <th>CH40147632</th>
      <td>40</td>
    </tr>
    <tr>
      <th>TU8XZ52440</th>
      <td>40</td>
    </tr>
    <tr>
      <th>CH40151190</th>
      <td>40</td>
    </tr>
    <tr>
      <th>BR84614964</th>
      <td>40</td>
    </tr>
    <tr>
      <th>TU8XZ52373</th>
      <td>40</td>
    </tr>
  </tbody>
</table>
</div>



## 4.1 Calidad de los datos

Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

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

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 42), ('counts_nas', 42)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="017171ea-623f-4563-ab92-90674dd389d7"></div>








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
      <th>site</th>
      <td>93.100405</td>
    </tr>
    <tr>
      <th>ru</th>
      <td>93.100405</td>
    </tr>
    <tr>
      <th>operstate</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>rnc</th>
      <td>36.556197</td>
    </tr>
    <tr>
      <th>antennaserialnumber</th>
      <td>62.695005</td>
    </tr>
    <tr>
      <th>node</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>rurevision</th>
      <td>93.105956</td>
    </tr>
    <tr>
      <th>maxsupportedelectricaltilt</th>
      <td>36.556197</td>
    </tr>
    <tr>
      <th>bootrom</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>state</th>
      <td>93.100405</td>
    </tr>
    <tr>
      <th>btsswver</th>
      <td>93.105956</td>
    </tr>
    <tr>
      <th>eq_class</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>f_timestamp</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>rulogicalid</th>
      <td>93.105956</td>
    </tr>
    <tr>
      <th>adminstate</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>productname</th>
      <td>70.809662</td>
    </tr>
    <tr>
      <th>bsc</th>
      <td>93.100405</td>
    </tr>
    <tr>
      <th>productiondate</th>
      <td>70.809662</td>
    </tr>
    <tr>
      <th>prodname</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>minsupportedelectricaltilt</th>
      <td>36.556197</td>
    </tr>
    <tr>
      <th>electricalantennatilt</th>
      <td>36.556197</td>
    </tr>
    <tr>
      <th>powerstate</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>tg_count</th>
      <td>93.100405</td>
    </tr>
    <tr>
      <th>productrevision</th>
      <td>70.809662</td>
    </tr>
    <tr>
      <th>serialno</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>ruserialno_count</th>
      <td>93.100405</td>
    </tr>
    <tr>
      <th>mo</th>
      <td>93.100405</td>
    </tr>
    <tr>
      <th>serialnumber</th>
      <td>70.809662</td>
    </tr>
    <tr>
      <th>antennamodelnumber</th>
      <td>39.117873</td>
    </tr>
    <tr>
      <th>prodno</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>ruserialno</th>
      <td>93.105956</td>
    </tr>
    <tr>
      <th>productnumber</th>
      <td>70.809662</td>
    </tr>
    <tr>
      <th>eq</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>nodeb</th>
      <td>36.556197</td>
    </tr>
    <tr>
      <th>sheet_name</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>type</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>manweek</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>tg</th>
      <td>93.100405</td>
    </tr>
    <tr>
      <th>revision</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>fsbrole</th>
      <td>99.533736</td>
    </tr>
    <tr>
      <th>enodeb</th>
      <td>70.809662</td>
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

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 42), ('counts_nas', 42)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="a8d8cecb-da56-41a1-8211-89ed5411632e"></div>








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
      <th>site</th>
      <td>6.899595</td>
    </tr>
    <tr>
      <th>ru</th>
      <td>6.899595</td>
    </tr>
    <tr>
      <th>operstate</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>rnc</th>
      <td>63.443803</td>
    </tr>
    <tr>
      <th>antennaserialnumber</th>
      <td>37.304995</td>
    </tr>
    <tr>
      <th>node</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>rurevision</th>
      <td>6.894044</td>
    </tr>
    <tr>
      <th>maxsupportedelectricaltilt</th>
      <td>63.443803</td>
    </tr>
    <tr>
      <th>bootrom</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>state</th>
      <td>6.899595</td>
    </tr>
    <tr>
      <th>btsswver</th>
      <td>6.894044</td>
    </tr>
    <tr>
      <th>eq_class</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>f_timestamp</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>rulogicalid</th>
      <td>6.894044</td>
    </tr>
    <tr>
      <th>adminstate</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>productname</th>
      <td>29.190338</td>
    </tr>
    <tr>
      <th>bsc</th>
      <td>6.899595</td>
    </tr>
    <tr>
      <th>productiondate</th>
      <td>29.190338</td>
    </tr>
    <tr>
      <th>prodname</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>minsupportedelectricaltilt</th>
      <td>63.443803</td>
    </tr>
    <tr>
      <th>electricalantennatilt</th>
      <td>63.443803</td>
    </tr>
    <tr>
      <th>powerstate</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>tg_count</th>
      <td>6.899595</td>
    </tr>
    <tr>
      <th>productrevision</th>
      <td>29.190338</td>
    </tr>
    <tr>
      <th>serialno</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>ruserialno_count</th>
      <td>6.899595</td>
    </tr>
    <tr>
      <th>mo</th>
      <td>6.899595</td>
    </tr>
    <tr>
      <th>serialnumber</th>
      <td>29.190338</td>
    </tr>
    <tr>
      <th>antennamodelnumber</th>
      <td>60.882127</td>
    </tr>
    <tr>
      <th>prodno</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>ruserialno</th>
      <td>6.894044</td>
    </tr>
    <tr>
      <th>productnumber</th>
      <td>29.190338</td>
    </tr>
    <tr>
      <th>eq</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>nodeb</th>
      <td>63.443803</td>
    </tr>
    <tr>
      <th>sheet_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>type</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>manweek</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>tg</th>
      <td>6.899595</td>
    </tr>
    <tr>
      <th>revision</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>fsbrole</th>
      <td>0.466264</td>
    </tr>
    <tr>
      <th>enodeb</th>
      <td>29.190338</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



##  5.1 Catálogos

#### Catálogo de rnc:



```python
Catalogo_rnc=pd.DataFrame(df_1.rnc.unique())
Catalogo_rnc.columns=['rnc']

#Remover los sucios
#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios, un ejemplo puede ser:
#Catalogo_CAMPO.drop(labels=[67,346,369,279,171,313],axis=0,inplace=True)

#Se le da 
Catalogo_rnc.reset_index(drop=True)
Catalogo_rnc.dropna(inplace=True)
Catalogo_rnc.sort_values(by='rnc').head(10)
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
      <th>rnc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>11</th>
      <td>BCNRNC210</td>
    </tr>
    <tr>
      <th>7</th>
      <td>BCNRNC211</td>
    </tr>
    <tr>
      <th>12</th>
      <td>BCSRNC212</td>
    </tr>
    <tr>
      <th>8</th>
      <td>CHHRNC232</td>
    </tr>
    <tr>
      <th>2</th>
      <td>LTE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>LTE_BAJA_C_SUR</td>
    </tr>
    <tr>
      <th>4</th>
      <td>LTE_CHIHUAHUA</td>
    </tr>
    <tr>
      <th>5</th>
      <td>LTE_SINALOA</td>
    </tr>
    <tr>
      <th>6</th>
      <td>LTE_SONORA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>LTE_TIJUANA</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de node:


```python
Catalogo_node=pd.DataFrame(df_1.node.unique())
Catalogo_node.columns=['node']

#Remover los sucios
#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios, un ejemplo puede ser:
#Catalogo_CAMPO.drop(labels=[67,346,369,279,171,313],axis=0,inplace=True)

#Se le da 
Catalogo_node.reset_index(drop=True)
Catalogo_node.dropna(inplace=True)
Catalogo_node.sort_values(by='node').head(10)
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
      <th>node</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>MXPTLM01SGSNMME01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MXTIJM01SGSNMME01</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de type:



```python
Catalogo_type=pd.DataFrame(df_1.type.unique())
Catalogo_type.columns=['type']

#Remover los sucios
#Esta parte depende del estado del catálogo, deben quedar sólamente los valores limpios, un ejemplo puede ser:
#Catalogo_CAMPO.drop(labels=[67,346,369,279,171,313],axis=0,inplace=True)

#Se le da 
Catalogo_type.reset_index(drop=True)
Catalogo_type.dropna(inplace=True)
Catalogo_type.sort_values(by='type').head(10)
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
      <th>type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>FSB</td>
    </tr>
    <tr>
      <th>1</th>
      <td>GEP</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SMXB</td>
    </tr>
  </tbody>
</table>
</div>




```python
#df_serie_cleaned_2 = df_1.loc[df_1["serie_cleaned"]== 1]

```


```python
#df_serie_cleaned_2.to_excel("clean_tx_netcm_ericsson_2019_11.xlsx") 

```

## 6.1 Preparación de los datos

Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos: 


* **serie:**
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

* **marca**: REGLA DE LIMPIEZA.
    * Se eliminan los siguientes caracteres especiales:    '-','#','%','/','_'
    * replace('ALACATEL LUCENT','ALCATEL LUCENT')
    * replace('ALCATEL . LUCENT','ALCATEL LUCENT')
    * replace('ALCATEL TLUCEN','ALCATEL LUCENT')
    * replace('ALCATEL.LUCENT','ALCATEL LUCENT')
    * replace('A 10','A10')
    * replace('ALCATEL-LUNCENT','ALCATEL LUCENT')
    * replace(especiales,' ',)
    * Pasar todo a uppercase



```python
df_1['trazabilidad']=0
df_1.trazabilidad.loc[(df_1.serie_cleaned==0) ]=1
#CS CA
df_1['CS_CA']=0
df_1.CS_CA.loc[(df_1.serie_cleaned==0) ]=1
#CS SA
df_1['CS_SA']=0
df_1.CS_SA.loc[(df_1.serie_cleaned==0) ]=1
#SS CA
df_1['SS_CA']=0
df_1.SS_CA.loc[(df_1.serie_cleaned==1) ]=1
```


```python
df_1.dtypes
```




    site                          object
    ru                            object
    operstate                     object
    rnc                           object
    antennaserialnumber           object
    node                          object
    rurevision                    object
    maxsupportedelectricaltilt    object
    bootrom                       object
    state                         object
    btsswver                      object
    eq_class                      object
    f_timestamp                   object
    rulogicalid                   object
    adminstate                    object
    productname                   object
    bsc                           object
    productiondate                object
    prodname                      object
    minsupportedelectricaltilt    object
    electricalantennatilt         object
    powerstate                    object
    tg_count                      object
    productrevision               object
    serialno                      object
    ruserialno_count              object
    mo                            object
    serialnumber                  object
    antennamodelnumber            object
    prodno                        object
    ruserialno                    object
    productnumber                 object
    eq                            object
    nodeb                         object
    sheet_name                    object
    type                          object
    manweek                       object
    tg                            object
    revision                      object
    fsbrole                       object
    enodeb                        object
    filedate                       int64
    filename                      object
    hash_id                       object
    sourceid                      object
    registry_state                object
    datasetname                   object
    timestamp                      int64
    transaction_status            object
    year                           int64
    month                          int64
    day                            int64
    serie_cleaned                  int64
    trazabilidad                   int64
    CS_CA                          int64
    CS_SA                          int64
    SS_CA                          int64
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


```python
#df_hive_tx_netcm_ericsson = spark.createDataFrame(df_1,schema=mySchema_1)

```


```python
#df_hive_tx_netcm_ericsson.write.mode("overwrite").saveAsTable("default.eda_tx_netcm_ericsson")

```

##  7.1 Métricas KPI

Se mostrarán los KPIs generados.

#### Total de elementos:


```python
Total_Elementos=df_1.shape[0]
Total_Elementos
```




    360311




```python
df_1.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables


```python
Total_Tr=df_1.loc[(df_1.serialnumber!='vacio') ].shape[0]
Total_Tr
```




    105176



#### Total Elementos NO Trazables


```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    255135



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=df_1[['serialnumber']].loc[(df_1.serialnumber!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic
```




    5196



#### Total de elementos trazables duplicados



```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    99980



### EN CASO DE EXISTIR NOMBRE DE ALMACENES:

#### Total de elementos en almacén Trazables Únicos en NOMBREALMACEN



```python
NOMBREALMACEN_Tr_Unic=df_1[['serialnumber']].loc[((df_1.serialnumber!='vacio') )].drop_duplicates().shape[0]
NOMBREALMACEN_Tr_Unic
```




    5196



#### Total de elementos en almacén Trazables Únicos con NSerie, con Nactivo



```python
Total_Tr_Unic_CS_CA=df_1[['serialnumber']].loc[(df_1.serialnumber!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_CS_CA
```




    5196



#### Total de elementos en almacén Trazables Únicos con NSerie, sin Nactivo



```python
Total_Tr_Unic_CS_SA=df_1[['serialnumber']].loc[(df_1.serialnumber!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic_CS_SA
```




    5196



#### Total de elementos en almacén Trazables Únicos sin NSerie, con Nactivo



```python
Total_Tr_Unic_SS_CA=df_1[['serialnumber']].loc[(df_1.serialnumber=='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic_SS_CA
```




    1



###  KPIS


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
      <td>360311</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>105176</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>255135</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>5196</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>99980</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Total CS CA</td>
      <td>5196</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Total CS SA</td>
      <td>5196</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Total SS CA</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



## 1.3 NETCM HUAWEI 

Recolección de los datos:

Se crea el dataframe de spark


```python
 df_load_2 =spark.sql("select a.mbts as cobts_mbts ,a.manufacturerdata as cobts_manufacturerdata, a.boardname as cobts_boardname, a.serialnumber as cobts_serialnumber, a.boardtype as cobts_boardtype,a.filedate as cobts_filedate ,a.filename as cobts_filename,a.hash_id as cobts_hash_id ,a.sourceid as cobts_sourceid,a.registry_state as cobts_registry_state,a.datasetname as cobts_datasetname,a.transaction_status as cobts_transaction_status,a.year as cobts_year,a.month as cobts_month,a.day as cobts_day,b.bts as bts_bts,b.serial_number_count as bts_serial_number_count,b.site as bts_site,b.manufacturerdata as bts_manufacturerdata,b.sheet_name as bts_sheet_name,b.boardname as bts_boardname,b.serialnumber as bts_serialnumber,b.boardtype as bts_boardtype,b.filedate as bts_filedate,b.filename as bts_filename,b.hash_id as bts_hash_id,b.sourceid as bts_sourceid,b.registry_state as bts_registry_state,b.datasetname as bts_datasetname,b.transaction_status as bts_transaction_status,b.year as bts_year,b.month as bts_month,b.day as bts_day from tx_netcm_huawei_cobts a  INNER JOIN tx_netcm_huawei_bts  b on a.serialnumber = b.serialnumber where a.year = 2019  and a.month = 11 and  b.year = 2019  and b.month = 11").limit(400000).cache()#.toPandas() 
```


```python
df_pre_2 = df_load_2.withColumn("serie_cleaned",validate_rule_udf(col("cobts_serialnumber"))).cache()
```

### Gestor NETCM HUAWEI 



```python
df_pre_2.printSchema()
```

    root
     |-- cobts_mbts: string (nullable = true)
     |-- cobts_manufacturerdata: string (nullable = true)
     |-- cobts_boardname: string (nullable = true)
     |-- cobts_serialnumber: string (nullable = true)
     |-- cobts_boardtype: string (nullable = true)
     |-- cobts_filedate: long (nullable = true)
     |-- cobts_filename: string (nullable = true)
     |-- cobts_hash_id: string (nullable = true)
     |-- cobts_sourceid: string (nullable = true)
     |-- cobts_registry_state: string (nullable = true)
     |-- cobts_datasetname: string (nullable = true)
     |-- cobts_transaction_status: string (nullable = true)
     |-- cobts_year: integer (nullable = true)
     |-- cobts_month: integer (nullable = true)
     |-- cobts_day: integer (nullable = true)
     |-- bts_bts: string (nullable = true)
     |-- bts_serial_number_count: string (nullable = true)
     |-- bts_site: string (nullable = true)
     |-- bts_manufacturerdata: string (nullable = true)
     |-- bts_sheet_name: string (nullable = true)
     |-- bts_boardname: string (nullable = true)
     |-- bts_serialnumber: string (nullable = true)
     |-- bts_boardtype: string (nullable = true)
     |-- bts_filedate: long (nullable = true)
     |-- bts_filename: string (nullable = true)
     |-- bts_hash_id: string (nullable = true)
     |-- bts_sourceid: string (nullable = true)
     |-- bts_registry_state: string (nullable = true)
     |-- bts_datasetname: string (nullable = true)
     |-- bts_transaction_status: string (nullable = true)
     |-- bts_year: integer (nullable = true)
     |-- bts_month: integer (nullable = true)
     |-- bts_day: integer (nullable = true)
     |-- serie_cleaned: integer (nullable = true)
    



```python
df_pre_2.columns
```




    ['cobts_mbts',
     'cobts_manufacturerdata',
     'cobts_boardname',
     'cobts_serialnumber',
     'cobts_boardtype',
     'cobts_filedate',
     'cobts_filename',
     'cobts_hash_id',
     'cobts_sourceid',
     'cobts_registry_state',
     'cobts_datasetname',
     'cobts_transaction_status',
     'cobts_year',
     'cobts_month',
     'cobts_day',
     'bts_bts',
     'bts_serial_number_count',
     'bts_site',
     'bts_manufacturerdata',
     'bts_sheet_name',
     'bts_boardname',
     'bts_serialnumber',
     'bts_boardtype',
     'bts_filedate',
     'bts_filename',
     'bts_hash_id',
     'bts_sourceid',
     'bts_registry_state',
     'bts_datasetname',
     'bts_transaction_status',
     'bts_year',
     'bts_month',
     'bts_day',
     'serie_cleaned']




```python
df_2 = df_pre_2.toPandas()
```

Una muestra de la fuente tx_netcm_huawei




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
      <th>cobts_mbts</th>
      <th>cobts_manufacturerdata</th>
      <th>cobts_boardname</th>
      <th>cobts_serialnumber</th>
      <th>cobts_boardtype</th>
      <th>cobts_filedate</th>
      <th>cobts_filename</th>
      <th>cobts_hash_id</th>
      <th>cobts_sourceid</th>
      <th>cobts_registry_state</th>
      <th>...</th>
      <th>bts_filename</th>
      <th>bts_hash_id</th>
      <th>bts_sourceid</th>
      <th>bts_registry_state</th>
      <th>bts_datasetname</th>
      <th>bts_transaction_status</th>
      <th>bts_year</th>
      <th>bts_month</th>
      <th>bts_day</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MEXHXC0320</td>
      <td>BBU3900,QWL1WBBPB2,WCDMA BaseBand Processing&amp;I...</td>
      <td>WBBP</td>
      <td>020LAJW0A1000683</td>
      <td>QWL1WBBPB2</td>
      <td>20191106</td>
      <td>Huawei_CO_MPT_BTS_-_MBTS_Board_Serial_Number_I...</td>
      <td>f1e5d70314ffc14b9f43e6bfc1c756876bf61f8b54be7e...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:16:29:36</td>
      <td>...</td>
      <td>Huawei_BTS_-_Serial_Number_Information_2019-11...</td>
      <td>f1e5d70314ffc14b9f43e6bfc1c756876bf61f8b54be7e...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:15:38:0</td>
      <td>tx_netcm_huawei_bts</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>6</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MEXHXC0320</td>
      <td>BBU3900,QWL1WBBPB2,WCDMA BaseBand Processing&amp;I...</td>
      <td>WBBP</td>
      <td>020LAJW0A1000683</td>
      <td>QWL1WBBPB2</td>
      <td>20191106</td>
      <td>Huawei_CO_MPT_BTS_-_MBTS_Board_Serial_Number_I...</td>
      <td>f1e5d70314ffc14b9f43e6bfc1c756876bf61f8b54be7e...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:16:28:9</td>
      <td>...</td>
      <td>Huawei_BTS_-_Serial_Number_Information_2019-11...</td>
      <td>f1e5d70314ffc14b9f43e6bfc1c756876bf61f8b54be7e...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:15:38:0</td>
      <td>tx_netcm_huawei_bts</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>6</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>DIFALO0031</td>
      <td>BBU3900,QWL1WBBPB2,WCDMA BaseBand Processing&amp;I...</td>
      <td>WBBP</td>
      <td>020LAJW0A1001553</td>
      <td>QWL1WBBPB2</td>
      <td>20191106</td>
      <td>Huawei_CO_MPT_BTS_-_MBTS_Board_Serial_Number_I...</td>
      <td>0eb47a18010abefa9b3ad68cbee49ef9fab3fa9919fd19...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:16:29:36</td>
      <td>...</td>
      <td>Huawei_BTS_-_Serial_Number_Information_2019-11...</td>
      <td>0eb47a18010abefa9b3ad68cbee49ef9fab3fa9919fd19...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:15:38:0</td>
      <td>tx_netcm_huawei_bts</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>6</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>DIFALO0031</td>
      <td>BBU3900,QWL1WBBPB2,WCDMA BaseBand Processing&amp;I...</td>
      <td>WBBP</td>
      <td>020LAJW0A1001553</td>
      <td>QWL1WBBPB2</td>
      <td>20191106</td>
      <td>Huawei_CO_MPT_BTS_-_MBTS_Board_Serial_Number_I...</td>
      <td>0eb47a18010abefa9b3ad68cbee49ef9fab3fa9919fd19...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:16:28:9</td>
      <td>...</td>
      <td>Huawei_BTS_-_Serial_Number_Information_2019-11...</td>
      <td>0eb47a18010abefa9b3ad68cbee49ef9fab3fa9919fd19...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:15:38:0</td>
      <td>tx_netcm_huawei_bts</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>6</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>DIFIZT0607</td>
      <td>BBU3900,QWL1WBBPB2,WCDMA BaseBand Processing&amp;I...</td>
      <td>WBBP</td>
      <td>020LAJW0A2002501</td>
      <td>QWL1WBBPB2</td>
      <td>20191106</td>
      <td>Huawei_CO_MPT_BTS_-_MBTS_Board_Serial_Number_I...</td>
      <td>c11239830e8280b958270c21c9cc8e64f9a2b3a3a12bd2...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:16:29:36</td>
      <td>...</td>
      <td>Huawei_BTS_-_Serial_Number_Information_2019-11...</td>
      <td>c11239830e8280b958270c21c9cc8e64f9a2b3a3a12bd2...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:15:38:0</td>
      <td>tx_netcm_huawei_bts</td>
      <td>full</td>
      <td>2019</td>
      <td>11</td>
      <td>6</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 34 columns</p>
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
print('Columnas de la fuente SOURCE son: ',list(campos))
pd.DataFrame(df_2.dtypes,columns=['Tipo de objeto SOURCE'])
```

    ('Columnas de la fuente SOURCE son: ', ['cobts_mbts', 'cobts_manufacturerdata', 'cobts_boardname', 'cobts_serialnumber', 'cobts_boardtype', 'cobts_filedate', 'cobts_filename', 'cobts_hash_id', 'cobts_sourceid', 'cobts_registry_state', 'cobts_datasetname', 'cobts_transaction_status', 'cobts_year', 'cobts_month', 'cobts_day', 'bts_bts', 'bts_serial_number_count', 'bts_site', 'bts_manufacturerdata', 'bts_sheet_name', 'bts_boardname', 'bts_serialnumber', 'bts_boardtype', 'bts_filedate', 'bts_filename', 'bts_hash_id', 'bts_sourceid', 'bts_registry_state', 'bts_datasetname', 'bts_transaction_status', 'bts_year', 'bts_month', 'bts_day', 'serie_cleaned'])





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
      <th>Tipo de objeto SOURCE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>cobts_mbts</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cobts_manufacturerdata</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cobts_boardname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cobts_serialnumber</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cobts_boardtype</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cobts_filedate</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>cobts_filename</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cobts_hash_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cobts_sourceid</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cobts_registry_state</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cobts_datasetname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cobts_transaction_status</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cobts_year</th>
      <td>int32</td>
    </tr>
    <tr>
      <th>cobts_month</th>
      <td>int32</td>
    </tr>
    <tr>
      <th>cobts_day</th>
      <td>int32</td>
    </tr>
    <tr>
      <th>bts_bts</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_serial_number_count</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_site</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_manufacturerdata</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_sheet_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_boardname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_serialnumber</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_boardtype</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_filedate</th>
      <td>int64</td>
    </tr>
    <tr>
      <th>bts_filename</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_hash_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_sourceid</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_registry_state</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_datasetname</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_transaction_status</th>
      <td>object</td>
    </tr>
    <tr>
      <th>bts_year</th>
      <td>int32</td>
    </tr>
    <tr>
      <th>bts_month</th>
      <td>int32</td>
    </tr>
    <tr>
      <th>bts_day</th>
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

    ('renglones = ', 400000, ' columnas = ', 34)



```python
NOrelevantes_2 =['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
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
      <th>cobts_mbts</th>
      <th>cobts_manufacturerdata</th>
      <th>cobts_boardname</th>
      <th>cobts_serialnumber</th>
      <th>cobts_boardtype</th>
      <th>cobts_filedate</th>
      <th>cobts_filename</th>
      <th>cobts_hash_id</th>
      <th>cobts_sourceid</th>
      <th>cobts_registry_state</th>
      <th>...</th>
      <th>bts_filename</th>
      <th>bts_hash_id</th>
      <th>bts_sourceid</th>
      <th>bts_registry_state</th>
      <th>bts_datasetname</th>
      <th>bts_transaction_status</th>
      <th>bts_year</th>
      <th>bts_month</th>
      <th>bts_day</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>400000</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000.0</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000</td>
      <td>...</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000.0</td>
      <td>400000.0</td>
      <td>400000.0</td>
      <td>400000.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>9071</td>
      <td>126</td>
      <td>22</td>
      <td>197051</td>
      <td>118</td>
      <td>NaN</td>
      <td>1</td>
      <td>197051</td>
      <td>1</td>
      <td>2</td>
      <td>...</td>
      <td>1</td>
      <td>197051</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>iUDIFCHT6280Z</td>
      <td>6100Mb/s-850nm-LC-120m(0.05mm)-50m(0.0625mm)</td>
      <td>FModule</td>
      <td>21023172759TB4001048</td>
      <td>FTLF8526P3BNL-HW</td>
      <td>NaN</td>
      <td>Huawei_CO_MPT_BTS_-_MBTS_Board_Serial_Number_I...</td>
      <td>bb574f86fe798e56dd272463973c98bd7406dc529513a0...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:16:29:36</td>
      <td>...</td>
      <td>Huawei_BTS_-_Serial_Number_Information_2019-11...</td>
      <td>bb574f86fe798e56dd272463973c98bd7406dc529513a0...</td>
      <td>Gestores-NETCM</td>
      <td>2019:111:04:15:38:0</td>
      <td>tx_netcm_huawei_bts</td>
      <td>full</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>266</td>
      <td>70694</td>
      <td>221478</td>
      <td>6</td>
      <td>101364</td>
      <td>NaN</td>
      <td>400000</td>
      <td>6</td>
      <td>400000</td>
      <td>200000</td>
      <td>...</td>
      <td>400000</td>
      <td>6</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000</td>
      <td>400000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>20191106.0</td>
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
      <td>2019.0</td>
      <td>11.0</td>
      <td>6.0</td>
      <td>0.999995</td>
    </tr>
    <tr>
      <th>std</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
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
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.002236</td>
    </tr>
    <tr>
      <th>min</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>20191106.0</td>
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
      <td>2019.0</td>
      <td>11.0</td>
      <td>6.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>20191106.0</td>
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
      <td>2019.0</td>
      <td>11.0</td>
      <td>6.0</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>20191106.0</td>
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
      <td>2019.0</td>
      <td>11.0</td>
      <td>6.0</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>20191106.0</td>
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
      <td>2019.0</td>
      <td>11.0</td>
      <td>6.0</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>20191106.0</td>
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
      <td>2019.0</td>
      <td>11.0</td>
      <td>6.0</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
<p>11 rows × 34 columns</p>
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
df_2.replace('NAN',np.NaN,inplace=True)


```

### Visualización de los datos de trazabilidad:



```python
pd.DataFrame(df_2.cobts_serialnumber.value_counts()[:15])

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
      <th>cobts_serialnumber</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>21023172759TB4001048</th>
      <td>6</td>
    </tr>
    <tr>
      <th>172330510</th>
      <td>4</td>
    </tr>
    <tr>
      <th>171981304</th>
      <td>4</td>
    </tr>
    <tr>
      <th>163370075</th>
      <td>4</td>
    </tr>
    <tr>
      <th>171370782</th>
      <td>4</td>
    </tr>
    <tr>
      <th>171981301</th>
      <td>4</td>
    </tr>
    <tr>
      <th>171370524</th>
      <td>4</td>
    </tr>
    <tr>
      <th>171370788</th>
      <td>4</td>
    </tr>
    <tr>
      <th>171371466</th>
      <td>4</td>
    </tr>
    <tr>
      <th>171371212</th>
      <td>4</td>
    </tr>
    <tr>
      <th>171370521</th>
      <td>4</td>
    </tr>
    <tr>
      <th>171300264</th>
      <td>4</td>
    </tr>
    <tr>
      <th>PU60AB5</th>
      <td>4</td>
    </tr>
    <tr>
      <th>21023172756TB4001992</th>
      <td>4</td>
    </tr>
    <tr>
      <th>PU60MU4</th>
      <td>4</td>
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

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 34), ('counts_nas', 34)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="cb3ad184-ca78-4053-b7c0-1ca94cee37e9"></div>








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
      <th>cobts_mbts</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_manufacturerdata</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_boardname</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_serialnumber</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_boardtype</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_filedate</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_filename</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_hash_id</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_sourceid</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_registry_state</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_datasetname</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_transaction_status</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_year</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_month</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>cobts_day</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_bts</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_serial_number_count</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_site</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_manufacturerdata</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_sheet_name</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_boardname</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_serialnumber</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_boardtype</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_filedate</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_filename</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_hash_id</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_sourceid</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_registry_state</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_datasetname</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_transaction_status</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_year</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_month</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>bts_day</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>0.0</td>
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

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/bokeh/models/sources.py:110: BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths: ('color', 20), ('columnas', 34), ('counts_nas', 34)
      "Current lengths: %s" % ", ".join(sorted(str((k, len(v))) for k, v in data.items())), BokehUserWarning))









  <div class="bk-root" id="5ece3f0f-e236-45aa-9551-eafbb065672d"></div>








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
      <th>cobts_mbts</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_manufacturerdata</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_boardname</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_serialnumber</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_boardtype</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_filedate</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_filename</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_hash_id</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_sourceid</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_registry_state</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_datasetname</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_transaction_status</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_year</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_month</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>cobts_day</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_bts</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_serial_number_count</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_site</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_manufacturerdata</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_sheet_name</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_boardname</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_serialnumber</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_boardtype</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_filedate</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_filename</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_hash_id</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_sourceid</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_registry_state</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_datasetname</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_transaction_status</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_year</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_month</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>bts_day</th>
      <td>100.0</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_2.dtypes
```




    cobts_mbts                  object
    cobts_manufacturerdata      object
    cobts_boardname             object
    cobts_serialnumber          object
    cobts_boardtype             object
    cobts_filedate               int64
    cobts_filename              object
    cobts_hash_id               object
    cobts_sourceid              object
    cobts_registry_state        object
    cobts_datasetname           object
    cobts_transaction_status    object
    cobts_year                   int64
    cobts_month                  int64
    cobts_day                    int64
    bts_bts                     object
    bts_serial_number_count     object
    bts_site                    object
    bts_manufacturerdata        object
    bts_sheet_name              object
    bts_boardname               object
    bts_serialnumber            object
    bts_boardtype               object
    bts_filedate                 int64
    bts_filename                object
    bts_hash_id                 object
    bts_sourceid                object
    bts_registry_state          object
    bts_datasetname             object
    bts_transaction_status      object
    bts_year                     int64
    bts_month                    int64
    bts_day                      int64
    serie_cleaned                int64
    dtype: object




```python
df_2['trazabilidad']=0
df_2.trazabilidad.loc[(df_2.serie_cleaned==0) ]=1
#CS CA
df_2['CS_CA']=0
df_2.CS_CA.loc[(df_2.serie_cleaned==0) ]=1
#CS SA
df_2['CS_SA']=0
df_2.CS_SA.loc[(df_2.serie_cleaned==0) ]=1
#SS CA
df_2['SS_CA']=0
df_2.SS_CA.loc[(df_2.serie_cleaned==1) ]=1

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


```python
#df_hive_tx_netcm_huawei = spark.createDataFrame(df_2,schema=mySchema_2)

```


```python
#df_hive_tx_netcm_huawei.write.mode("overwrite").saveAsTable("default.eda_tx_netcm_huawei")

```

## 5.2  Métricas KPI.



```python
Total_Elementos=df_2.shape[0]
Total_Elementos
```




    400000




```python
df_2.replace(np.NaN,'vacio',inplace=True)

```

#### Total Elementos Trazables



```python
Total_Tr=df_2.loc[(df_2.cobts_serialnumber!='vacio') ].shape[0]
Total_Tr
```




    400000



#### Total Elementos NO Trazables



```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    0



#### Total Elementos Trazables Únicos



```python
Total_Tr_Unic=df_2[['cobts_serialnumber']].loc[(df_2.cobts_serialnumber!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic
```




    197051



#### Total de elementos trazables duplicados



```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    202949



### EN CASO DE EXISTIR NOMBRE DE ALMACENES:

#### Total de elementos en almacén Trazables Únicos en NOMBREALMACEN


```python
NOMBREALMACEN_Tr_Unic=df_2[['cobts_serialnumber']].loc[((df_2.cobts_serialnumber!='vacio') )].drop_duplicates().shape[0]
NOMBREALMACEN_Tr_Unic
```




    197051



#### Total de elementos en almacén Trazables Únicos con NSerie, con Nactivo



```python
Total_Tr_Unic_CS_CA=df_2[['cobts_serialnumber']].loc[(df_2.cobts_serialnumber!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_CS_CA
```




    197051



#### Total de elementos en almacén Trazables Únicos con NSerie, sin Nactivo



```python
Total_Tr_Unic_CS_SA=df_2[['cobts_serialnumber']].loc[(df_2.cobts_serialnumber!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic_CS_SA
```




    197051



#### Total de elementos en almacén Trazables Únicos sin NSerie, con Nactivo



```python
Total_Tr_Unic_SS_CA=df_2[['cobts_serialnumber']].loc[(df_2.cobts_serialnumber=='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic_SS_CA
```




    0



###  KPIS


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
      <td>400000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>400000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>197051</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>202949</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Total CS CA</td>
      <td>197051</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Total CS SA</td>
      <td>197051</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Total SS CA</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>


