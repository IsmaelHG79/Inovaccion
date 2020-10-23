
<div style="width: 100%; clear: both; font-family: Verdana;">
<div style="float: left; width: 50%;font-family: Verdana;">
<img src="https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/WLOG/image/encabezado.png" align="left">
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

* **Salida de Almacén (WLOG)**

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
```


```python
conf = SparkConf().setAppName('Segregacion')  \
    .setMaster('yarn') 
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

from bokeh.io import show, output_notebook 
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20_11, Category20c_20,Category20c_19
output_notebook()
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="fec83723-f8d2-4d25-bfc3-3d6d7ed5ae37">Loading BokehJS ...</span>
    </div>




### Recolección de los datos: 

*IMPORTANTE*: Si se requieren ver datos de otro periódo, se debe cambiar los filtros ```year = <año-a-ejecutar>```, ```month = <mes-a-ejecutar>```, ```day = <día-a-ejecutar>``` de las tablas en la creación del dataframe.

#### Reglas para serie con pyspark:
Sobre el df que se carga con pyspark, se le agrega una columna con el nombre de serie_cleaned. el cual contiene valores 0 y 1.

Se crea el dataframe de spark


```python
df_load=spark.sql("SELECT * FROM tx_wlog").cache()
```


```python
def validate_rule(string):
    
    search_list=[" ",'!','%','$',"<",">","^",'¡',"+","N/A",u'¿','~','#','Ñ',"Ã","Åƒ","Ã‹","Ã³",'Ë','*','?',"ILEGIBLE", "VICIBLE","VISIBLE","INCOMPLETO"]
    str_temp = string.encode('utf-8')
    if str_temp.upper() == "BORRADO":
      return 1
    elif len(str_temp) < 6:
      return 1
    elif any(ext in str_temp.upper()for ext in search_list):
      return 1
    else:
      return 0
```

Se crea un udf en spark sobre la funcion ya creada 


```python
validate_rule_udf = udf(validate_rule, IntegerType())
```

Se le agrega una nueva columna al dataframe de spark; la nueva columna es la validacion de la columna serie con respecto al udf que creamos.


```python
df_serie = df_load.withColumn("serie_cleaned",validate_rule_udf(col("serie"))).cache()
```

Se convierte el dataframe de spark a un dataframe de pandas 


```python
df = df_serie.toPandas()
```

Hemos recolectado los campos a analizar de las fuente wlog.

## Salida de Almacén WLOG
Una muestra de la fuente WLOG


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
      <th>id</th>
      <th>organizacion</th>
      <th>lpn_salida</th>
      <th>num_pedido_att</th>
      <th>num_pedido</th>
      <th>sku_oracle</th>
      <th>sku_descripcion</th>
      <th>serie</th>
      <th>activo</th>
      <th>parte</th>
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
      <td>1192917</td>
      <td>2PX</td>
      <td>MEX6516341261058730EMB</td>
      <td>65163412</td>
      <td>P2019111320193</td>
      <td>T.9047112</td>
      <td>MODEM-EA</td>
      <td>164964</td>
      <td>NA</td>
      <td>NA</td>
      <td>...</td>
      <td>6040e0fbcc34b85f6314be26e9e89e232d94b2a7b4f89c...</td>
      <td>Salida de Almacen</td>
      <td>2019:111:02:18:28:17</td>
      <td>tx_wlog_embarques</td>
      <td>20191202</td>
      <td>delete</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1196556</td>
      <td>2PX</td>
      <td>MEX6522697561058835EMB</td>
      <td>65226975</td>
      <td>P2019111520352</td>
      <td>W.9047309</td>
      <td>BGK90160/1 O&amp;M ADAPTER FOR CABLE</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>...</td>
      <td>b69e82e4a533194f6e78ba0c96b6d6be9cc0e4e5ea0243...</td>
      <td>Salida de Almacen</td>
      <td>2019:111:02:18:28:17</td>
      <td>tx_wlog_embarques</td>
      <td>20191202</td>
      <td>delete</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1197110</td>
      <td>2PX</td>
      <td>MEX6522697561058835EMB</td>
      <td>65226975</td>
      <td>P2019111520352</td>
      <td>W.9047311</td>
      <td>NTK102260/10 CLAMP 4.8/8.3MM 10 PCS</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>...</td>
      <td>0598c6e028a0daf45d7b19df7adc3fb70fb09055322153...</td>
      <td>Salida de Almacen</td>
      <td>2019:111:02:18:28:17</td>
      <td>tx_wlog_embarques</td>
      <td>20191202</td>
      <td>delete</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1197826</td>
      <td>2PX</td>
      <td>MEX6531997061059129EMB</td>
      <td>65319970</td>
      <td>P2019112020418</td>
      <td>T.3402996</td>
      <td>IUSA-FH NYLON CABLE TIES</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>...</td>
      <td>83f2d2fe5ee2ed6c337ba0f4fec0a0d9feef62c8827855...</td>
      <td>Salida de Almacen</td>
      <td>2019:111:02:18:28:17</td>
      <td>tx_wlog_embarques</td>
      <td>20191202</td>
      <td>delete</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1199435</td>
      <td>2PX</td>
      <td>MEX6532605761059419EMB</td>
      <td>65326057</td>
      <td>P2019112220515</td>
      <td>W.1011018</td>
      <td>TARJETA DE APERTURA ELECTRICA BLUETOOTH MX5</td>
      <td>NA</td>
      <td>01185632</td>
      <td>NA</td>
      <td>...</td>
      <td>bc55c2018f5d47048ac7b44ee6355dea97d2a4c72a1675...</td>
      <td>Salida de Almacen</td>
      <td>2019:111:02:18:28:17</td>
      <td>tx_wlog_embarques</td>
      <td>20191202</td>
      <td>delete</td>
      <td>2019</td>
      <td>11</td>
      <td>28</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 33 columns</p>
</div>



### Diccionario de datos.
A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

* **id**: ID identificador de registros consecutivo.
* **organizacion**: Código que identifica sitios de almacén.
* **lpn_salida**: Código que identifica a los pallets en la salida de almacén.
* **num_pedido_att**: Código de número de pedido ATT.
* **num_pedido**: Código de númoer de pedido ATT.
* **sku_oracle (article)**: Identificador único de artículo en Oracle.
* **sku_descripcion (descripción)**: Descripción del identificador único de artículo en Oracle.
* **series**: Número de serie único que tiene el proveedor.
* **activo**: Id único del elemento de red en AT&T.
* **parte**: Código que identifica partes del elemento.
* **quantity**: Cantidad de elementos.
* **units**: Unidad de medida de conteo de los elementos.
* **area_usuaria**: Área usuaria.
* **control_serie**: Bandera que indica si existe o no número de serie.
* **control_activo**: Bandera que indica si el activo está con vida o ha sido retirado.
* **site_name**: Nombre del sitio.
* **site_id**: Código del sitio.
* **proyecto**: Nombre del Proyecto.
* **orden_compra**: Código de la orden de compra.
* **tipo_transporte**: A quién pertenece el trasporte de carga.
* **audit_cierre_embarque**: Fecha de salida de almacén hacía el embarque.
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

### 2. Descripción de las fuentes.
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
camposwlog=df.columns
print 'Columnas de la fuente WLOG son: ',list(camposwlog)
pd.DataFrame(df.dtypes,columns=['Tipo de objeto WLOG'])
```

    Columnas de la fuente WLOG son:  ['id', 'organizacion', 'lpn_salida', 'num_pedido_att', 'num_pedido', 'sku_oracle', 'sku_descripcion', 'serie', 'activo', 'parte', 'cantidad', 'units', 'area_usuaria', 'control_serie', 'control_activo', 'site_name', 'site_id', 'proyecto', 'orden_compra', 'tipo_transporte', 'audit_cierre_embarque', 'filedate', 'filename', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie_cleaned']





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
      <th>Tipo de objeto WLOG</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>organizacion</th>
      <td>object</td>
    </tr>
    <tr>
      <th>lpn_salida</th>
      <td>object</td>
    </tr>
    <tr>
      <th>num_pedido_att</th>
      <td>object</td>
    </tr>
    <tr>
      <th>num_pedido</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sku_oracle</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sku_descripcion</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>object</td>
    </tr>
    <tr>
      <th>activo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>parte</th>
      <td>object</td>
    </tr>
    <tr>
      <th>cantidad</th>
      <td>object</td>
    </tr>
    <tr>
      <th>units</th>
      <td>object</td>
    </tr>
    <tr>
      <th>area_usuaria</th>
      <td>object</td>
    </tr>
    <tr>
      <th>control_serie</th>
      <td>object</td>
    </tr>
    <tr>
      <th>control_activo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>site_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>proyecto</th>
      <td>object</td>
    </tr>
    <tr>
      <th>orden_compra</th>
      <td>object</td>
    </tr>
    <tr>
      <th>tipo_transporte</th>
      <td>object</td>
    </tr>
    <tr>
      <th>audit_cierre_embarque</th>
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
print 'renglones = ',df.shape[0],' columnas = ',df.shape[1]
```

    renglones =  17741  columnas =  33



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
      <th>id</th>
      <th>organizacion</th>
      <th>lpn_salida</th>
      <th>num_pedido_att</th>
      <th>num_pedido</th>
      <th>sku_oracle</th>
      <th>sku_descripcion</th>
      <th>serie</th>
      <th>activo</th>
      <th>parte</th>
      <th>...</th>
      <th>area_usuaria</th>
      <th>control_serie</th>
      <th>control_activo</th>
      <th>site_name</th>
      <th>site_id</th>
      <th>proyecto</th>
      <th>orden_compra</th>
      <th>tipo_transporte</th>
      <th>audit_cierre_embarque</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>...</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741</td>
      <td>17741.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>4587</td>
      <td>1</td>
      <td>803</td>
      <td>671</td>
      <td>206</td>
      <td>423</td>
      <td>383</td>
      <td>1544</td>
      <td>1673</td>
      <td>111</td>
      <td>...</td>
      <td>25</td>
      <td>17</td>
      <td>27</td>
      <td>512</td>
      <td>527</td>
      <td>78</td>
      <td>22</td>
      <td>20</td>
      <td>656</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>1193260</td>
      <td>2PX</td>
      <td>MEX6522708161059104EMB</td>
      <td>65227081</td>
      <td>P2019112220515</td>
      <td>CW.9056368</td>
      <td>null</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>...</td>
      <td>ATT INFRA</td>
      <td>NO</td>
      <td>NO</td>
      <td>null</td>
      <td>null</td>
      <td>Chapas Electronicas</td>
      <td>NA</td>
      <td>PROVEEDOR</td>
      <td>November- 25 2019 23:50:12</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>8</td>
      <td>17741</td>
      <td>632</td>
      <td>728</td>
      <td>2880</td>
      <td>1504</td>
      <td>2393</td>
      <td>12502</td>
      <td>10101</td>
      <td>15531</td>
      <td>...</td>
      <td>7173</td>
      <td>10399</td>
      <td>8313</td>
      <td>2393</td>
      <td>2393</td>
      <td>2880</td>
      <td>15083</td>
      <td>7045</td>
      <td>728</td>
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
      <td>0.734457</td>
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
      <td>0.441634</td>
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
<p>11 rows × 22 columns</p>
</div>



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

* Podemos notar que hay solamente una organización, esta es **2PX**. Además, podemos ver como posibilidad, catálogos para **units, area_usuaria, control_serie, control_activo y tipo_transporte**.
* Después de dar una revisión a fondo a **control_activo** y **control_serie** se observó que necesita fuertes reglas de calidad, es debido a la falta de estas, que presenta varios valores únicos, cuando la naturaleza de este campo sería ser booleano.
* **sku_descripcion** necesita tratamiento de nulos, mismo aplica para **serie, activo, site_name, site_id y orden_compra**.

#### Se propone un catálogo derivado de la fuente WLOG con los siguientes campos:
    
* **site_id**: Código identificador del sitio.
* **area_usuaria**: Área.
* **tipo_transporte**: A quién pertenece el trasporte de carga.
* **units**: Formato de la medida de conteo de los elementos.

Este catálogo nos ayudará a mapear todos los diferentes proyectos que existen en los cuales hay un activo. A continuación se indican los únicos de cada campo:


### 3. Exploración de los datos.
De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los catálogos.

#### Para empezar, se hará una limpieza general a los datos:


```python
df.replace('null',np.NaN,inplace=True)
df.replace('NA',np.NaN,inplace=True)
```

### Primer catálogo: *site_id*

Empezaremos con el catálogo de códigos de sitio. Siendo un catálogo muy grande, aplicaremos una normalización a los datos para poder trabajarlos. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Se hace catálogo:
ind=list(range(0,20))
principales=pd.DataFrame(df.site_id.value_counts()[:20])
sitecodes=principales.index
sitecodes=pd.DataFrame(sitecodes,index=ind)
sitecodes.columns=['Sitecodes']
principales.index=ind
principales.columns=['Frecuencias']

principales=pd.concat([sitecodes,principales],axis=1)

medios=df.site_id.value_counts()[20:70].sum()
Otros=df.site_id.value_counts()[70:].sum()

Medios=pd.DataFrame({'Sitecodes':'Medios','Frecuencias':medios},index=[0])
Otros=pd.DataFrame({'Sitecodes':'Otros','Frecuencias':Otros},index=[0])

Total=pd.concat([principales,Medios,Otros])
Total.reset_index(inplace=True,drop=True)
First=Total.Sitecodes[0]
Total
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/ipykernel_launcher.py:18: FutureWarning: Sorting because non-concatenation axis is not aligned. A future version
    of pandas will change to not sort by default.
    
    To accept the future behavior, pass 'sort=False'.
    
    To retain the current behavior and silence the warning, pass 'sort=True'.
    





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
      <th>Frecuencias</th>
      <th>Sitecodes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>360</td>
      <td>VER-7087</td>
    </tr>
    <tr>
      <th>1</th>
      <td>352</td>
      <td>PUE-7021</td>
    </tr>
    <tr>
      <th>2</th>
      <td>312</td>
      <td>MEX-9049</td>
    </tr>
    <tr>
      <th>3</th>
      <td>276</td>
      <td>TAMREY2169</td>
    </tr>
    <tr>
      <th>4</th>
      <td>240</td>
      <td>Solicitud Interna</td>
    </tr>
    <tr>
      <th>5</th>
      <td>240</td>
      <td>HMAZ0017</td>
    </tr>
    <tr>
      <th>6</th>
      <td>240</td>
      <td>HMAZ0011</td>
    </tr>
    <tr>
      <th>7</th>
      <td>180</td>
      <td>VER-7131</td>
    </tr>
    <tr>
      <th>8</th>
      <td>176</td>
      <td>HMEX8061</td>
    </tr>
    <tr>
      <th>9</th>
      <td>176</td>
      <td>HMEX0540</td>
    </tr>
    <tr>
      <th>10</th>
      <td>176</td>
      <td>HMEX0311</td>
    </tr>
    <tr>
      <th>11</th>
      <td>174</td>
      <td>HMEX0735</td>
    </tr>
    <tr>
      <th>12</th>
      <td>168</td>
      <td>HMEX0461</td>
    </tr>
    <tr>
      <th>13</th>
      <td>168</td>
      <td>HMEX0603</td>
    </tr>
    <tr>
      <th>14</th>
      <td>168</td>
      <td>HMEX0663</td>
    </tr>
    <tr>
      <th>15</th>
      <td>168</td>
      <td>HMEX0095</td>
    </tr>
    <tr>
      <th>16</th>
      <td>168</td>
      <td>HMEX0648</td>
    </tr>
    <tr>
      <th>17</th>
      <td>168</td>
      <td>HMEX0433</td>
    </tr>
    <tr>
      <th>18</th>
      <td>168</td>
      <td>HMEX0626</td>
    </tr>
    <tr>
      <th>19</th>
      <td>168</td>
      <td>MEX-9388</td>
    </tr>
    <tr>
      <th>20</th>
      <td>6044</td>
      <td>Medios</td>
    </tr>
    <tr>
      <th>21</th>
      <td>5058</td>
      <td>Otros</td>
    </tr>
  </tbody>
</table>
</div>



Después de hacer una normalización del catálogo ahora podemos hacer la visualización más adecuada.
Empezaremos usando un Histograma.


```python
principales_aux=principales.set_index('Sitecodes')
principales_aux.plot(kind='bar',figsize=(10,6),rot=90,colormap='rainbow_r')
plt.xlabel('Sitios')
plt.ylabel('Frecuencia')
plt.title('Frecuencia de sitios en WLOG')
```




    Text(0.5,1,'Frecuencia de sitios en WLOG')




![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/WLOG/image/output_37_1.png)


Ahora representamos los mismos datos pero con un gráfico tipo piechart.


```python
color_list=['gold','yellowgreen','lightcoral','turquoise',
            'springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','royalblue','limegreen',
            'linen','magenta','maroon','mediumaquamarine','mediumblue','mediumorchid',
            'mediumpurple','mediumseagreen']
explode_list=[0.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,.15]
principales_aux['Frecuencias'].plot(kind='pie',
                    figsize=(15,6),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                    explode=explode_list)
plt.title('Frecuencia de los sitios en WLOG',y=1.12)
plt.axis('equal')
plt.legend(labels=principales_aux.index,loc='upper left')

plt.show()

```


![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/WLOG/image/output_39_0.png)


Hay una gran diversidad de sitios, siendo el más poblado:           


```python
print First
```

    VER-7087


Una vez visto esto, recomendamos que en futuras visualizaciones y estudios a este catálogo, siempre se haga una normalización.

### Segundo catálogo: *area_usuaria*.
Seguimos el mismo procedimiento, pero para este caso no es necesario normalizar.


```python
#Revisamos frecuencias:
areas=pd.DataFrame(df.area_usuaria.value_counts())

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
areas.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Áreas')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Distribución de elementos por área')

#Subplot2: Bar chart
explode_list=[.2,0,0,0,0,0.1,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

areas['area_usuaria'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Distribución de elementos por área',y=1.12)
ax1.axis('equal')
ax1.legend(labels=areas.index,loc='upper left')

plt.show()
```


![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/WLOG/image/output_44_0.png)


Podemos observar en primer lugar, que se necesitan reglas de limpieza, existen outliers que al parecer son datos sucios.
Se llamará al catálogo limpio en el apartado de catálogos.

### Tercer catálogo: *tipo_transporte*.


```python
#Revisamos frecuencias:
trasportes=pd.DataFrame(df.tipo_transporte.value_counts())

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
trasportes.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Unidades')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Distribución de tipo de transporte')

#Subplot2: Bar chart
explode_list=[.2,0,0.1,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid']

trasportes['tipo_transporte'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Distribución de tipo de transporte',y=1.12)
ax1.axis('equal')
ax1.legend(labels=areas.index,loc='upper left')

plt.show()
```


![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/WLOG/image/output_47_0.png)


Hemos identificado que este campo necesitará aclaraciones de parte del negocio. Hay muchos valores que no concuerdan, códigos y nombres. 

### Cuarto catálogo: *units*.



```python
#Revisamos frecuencias:
units=pd.DataFrame(df.units.value_counts())

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
areas.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Unidades')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Distribución de unidades de medida de elementos')

#Subplot2: Bar chart
explode_list=[.2,.1,0,0,0,0,0,0,0,0,0,0,0]
color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue']

units['units'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Distribución de unidades de medida de elementos',y=1.12)
ax1.axis('equal')
ax1.legend(labels=areas.index,loc='upper left')

plt.show()
```


![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/WLOG/image/output_50_0.png)


Nos encontramos con un problema muy parecido: Encontramos valores atípicos que parecen ser datos sucios. Habrá que pasar reglas de limpieza.  
**No** se hará catálogo de este campo debido a su condición.

#### Visualización de los datos de trazabilidad: 


```python
pd.DataFrame(df.serie.value_counts()[:15])
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
      <th>serie</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>850NM</th>
      <td>72</td>
    </tr>
    <tr>
      <th>0.7M</th>
      <td>44</td>
    </tr>
    <tr>
      <th>CAPACIDAD NOMINAL DE 500 LTS</th>
      <td>43</td>
    </tr>
    <tr>
      <th>P/N: ATM200-A20</th>
      <td>20</td>
    </tr>
    <tr>
      <th>698-960MHZ/4DBI</th>
      <td>14</td>
    </tr>
    <tr>
      <th>GREY</th>
      <td>9</td>
    </tr>
    <tr>
      <th>EM184000062320</th>
      <td>8</td>
    </tr>
    <tr>
      <th>2102352571P0K1000179</th>
      <td>8</td>
    </tr>
    <tr>
      <th>21021207316TG3902075</th>
      <td>8</td>
    </tr>
    <tr>
      <th>CAT2332U3EZ</th>
      <td>8</td>
    </tr>
    <tr>
      <th>CAT2332U3EG</th>
      <td>8</td>
    </tr>
    <tr>
      <th>MA19021612797</th>
      <td>8</td>
    </tr>
    <tr>
      <th>21524320803AJ5U00271</th>
      <td>8</td>
    </tr>
    <tr>
      <th>16US462473605</th>
      <td>8</td>
    </tr>
    <tr>
      <th>CF86601880</th>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.DataFrame(df.activo.value_counts()[:15])
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
      <th>activo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>LC</th>
      <td>72</td>
    </tr>
    <tr>
      <th>BLUE/BLACK</th>
      <td>44</td>
    </tr>
    <tr>
      <th>1710-2700MHZ/5DBI</th>
      <td>14</td>
    </tr>
    <tr>
      <th>SILICONE RUBBER</th>
      <td>9</td>
    </tr>
    <tr>
      <th>01303258</th>
      <td>8</td>
    </tr>
    <tr>
      <th>01303210</th>
      <td>8</td>
    </tr>
    <tr>
      <th>01144765</th>
      <td>8</td>
    </tr>
    <tr>
      <th>01110660</th>
      <td>8</td>
    </tr>
    <tr>
      <th>01185631</th>
      <td>8</td>
    </tr>
    <tr>
      <th>01185769</th>
      <td>8</td>
    </tr>
    <tr>
      <th>01185630</th>
      <td>8</td>
    </tr>
    <tr>
      <th>01340076</th>
      <td>8</td>
    </tr>
    <tr>
      <th>01340702</th>
      <td>8</td>
    </tr>
    <tr>
      <th>00503793</th>
      <td>8</td>
    </tr>
    <tr>
      <th>01185633</th>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.DataFrame(df.lpn_salida.value_counts()[:15])
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
      <th>lpn_salida</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>MEX6522708161059104EMB</th>
      <td>632</td>
    </tr>
    <tr>
      <th>MEX6521791761058921EMB</th>
      <td>600</td>
    </tr>
    <tr>
      <th>MEX6521772161058911EMB</th>
      <td>552</td>
    </tr>
    <tr>
      <th>MEX6524578561059054EMB</th>
      <td>336</td>
    </tr>
    <tr>
      <th>MEX6503641361058068EMB</th>
      <td>328</td>
    </tr>
    <tr>
      <th>MEX6524588561059058EMB</th>
      <td>328</td>
    </tr>
    <tr>
      <th>MEX6534406461059618EMB</th>
      <td>228</td>
    </tr>
    <tr>
      <th>MEX6520236261058825EMB</th>
      <td>222</td>
    </tr>
    <tr>
      <th>MEX6520220361058821EMB</th>
      <td>222</td>
    </tr>
    <tr>
      <th>MEX6522723061058836EMB</th>
      <td>180</td>
    </tr>
    <tr>
      <th>MEX6532603461059417EMB</th>
      <td>176</td>
    </tr>
    <tr>
      <th>MEX6532590161059413EMB</th>
      <td>176</td>
    </tr>
    <tr>
      <th>MEX6532617961059429EMB</th>
      <td>176</td>
    </tr>
    <tr>
      <th>MEX6532614361059427EMB</th>
      <td>168</td>
    </tr>
    <tr>
      <th>MEX6532597661059414EMB</th>
      <td>168</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.DataFrame(df.sku_oracle.value_counts()[:15])
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
      <th>sku_oracle</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>CW.9056368</th>
      <td>1504</td>
    </tr>
    <tr>
      <th>W.6019020</th>
      <td>1360</td>
    </tr>
    <tr>
      <th>W.1011018</th>
      <td>1360</td>
    </tr>
    <tr>
      <th>W.1040226</th>
      <td>843</td>
    </tr>
    <tr>
      <th>W.1013179</th>
      <td>441</td>
    </tr>
    <tr>
      <th>W.9056071</th>
      <td>420</td>
    </tr>
    <tr>
      <th>W.1040221</th>
      <td>375</td>
    </tr>
    <tr>
      <th>W.1040220</th>
      <td>299</td>
    </tr>
    <tr>
      <th>T.9023243</th>
      <td>287</td>
    </tr>
    <tr>
      <th>W.4501720</th>
      <td>248</td>
    </tr>
    <tr>
      <th>W.9047300</th>
      <td>200</td>
    </tr>
    <tr>
      <th>W.9056175</th>
      <td>188</td>
    </tr>
    <tr>
      <th>W.9055008</th>
      <td>185</td>
    </tr>
    <tr>
      <th>T.3402996</th>
      <td>165</td>
    </tr>
    <tr>
      <th>W.6019018</th>
      <td>161</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.DataFrame(df.orden_compra.value_counts()[:15])
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
      <th>orden_compra</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>OPERACIONES</th>
      <td>58</td>
    </tr>
    <tr>
      <th>ATT INFRA</th>
      <td>40</td>
    </tr>
    <tr>
      <th>ALVARO OBREGON M2925X</th>
      <td>24</td>
    </tr>
    <tr>
      <th>SEVILLA/RIO NILO 0661MX</th>
      <td>24</td>
    </tr>
    <tr>
      <th>TROCADERO M2924X</th>
      <td>24</td>
    </tr>
    <tr>
      <th>METRO CIUDAD MX</th>
      <td>21</td>
    </tr>
    <tr>
      <th>REFACCIONES</th>
      <td>20</td>
    </tr>
    <tr>
      <th>EL TRAPICHE</th>
      <td>8</td>
    </tr>
    <tr>
      <th>Conscripto</th>
      <td>8</td>
    </tr>
    <tr>
      <th>NO</th>
      <td>8</td>
    </tr>
    <tr>
      <th>SI</th>
      <td>8</td>
    </tr>
    <tr>
      <th>Galerias</th>
      <td>5</td>
    </tr>
    <tr>
      <th>HLEO0050</th>
      <td>4</td>
    </tr>
    <tr>
      <th>HGDL1123</th>
      <td>4</td>
    </tr>
    <tr>
      <th>HCOL0007</th>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



#### Es de interés haber observado los datos que se usaran para la trazabilidad, se han identificado valores sucios y repetidos. 
Podemos utilizar los siguientes queries como ejemplos para visualizar en HUE:
* Activo: `SELECT * FROM tx_wlog WHERE activo=='100% ALGODÓN';` 
* Serie: `SELECT * FROM tx_wlog WHERE serie=='P/N: ATM200-A20';`

### 4. Calidad de los datos.
Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

### Missings Values
Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.


```python
Navi=[u'id', u'organizacion', u'lpn_salida', u'num_pedido_att', u'num_pedido',
       u'sku_oracle', u'sku_descripcion', u'serie', u'activo', u'parte',
       u'cantidad', u'units', u'area_usuaria', u'site_name', u'site_id',
      u'proyecto',u'orden_compra', u'tipo_transporte', u'audit_cierre_embarque']
```


```python
wlog_nas=df[Navi].isna().sum()
porcentaje_wlog_nas=wlog_nas/df[Navi].isna().count()

columnas=list(porcentaje_wlog_nas.keys())
counts_nas=list(porcentaje_wlog_nas.values)
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_19))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_wlog_nas*100,columns=['Porcentaje de NAs'])
```








  <div class="bk-root" id="ebff3997-f4ba-4a86-bffa-f898ba73a8fd"></div>








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
      <th>organizacion</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>lpn_salida</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>num_pedido_att</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>num_pedido</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>sku_oracle</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>sku_descripcion</th>
      <td>13.488529</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>70.469534</td>
    </tr>
    <tr>
      <th>activo</th>
      <td>56.935911</td>
    </tr>
    <tr>
      <th>parte</th>
      <td>87.542980</td>
    </tr>
    <tr>
      <th>cantidad</th>
      <td>0.648216</td>
    </tr>
    <tr>
      <th>units</th>
      <td>14.097289</td>
    </tr>
    <tr>
      <th>area_usuaria</th>
      <td>0.591849</td>
    </tr>
    <tr>
      <th>site_name</th>
      <td>13.736542</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>13.488529</td>
    </tr>
    <tr>
      <th>proyecto</th>
      <td>13.488529</td>
    </tr>
    <tr>
      <th>orden_compra</th>
      <td>98.506285</td>
    </tr>
    <tr>
      <th>tipo_transporte</th>
      <td>13.933826</td>
    </tr>
    <tr>
      <th>audit_cierre_embarque</th>
      <td>0.073277</td>
    </tr>
  </tbody>
</table>
</div>



#### Visualización de datos NOT NULL WLOG: 


```python
notmiss=(1-porcentaje_wlog_nas)*100

columnas=list(notmiss.keys())
counts_nas=list(notmiss.values)
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_19))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```








  <div class="bk-root" id="d0d7658c-b1ad-4a2b-8a4f-a59831a13f0b"></div>








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
      <th>organizacion</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>lpn_salida</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>num_pedido_att</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>num_pedido</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>sku_oracle</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>sku_descripcion</th>
      <td>86.511471</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>29.530466</td>
    </tr>
    <tr>
      <th>activo</th>
      <td>43.064089</td>
    </tr>
    <tr>
      <th>parte</th>
      <td>12.457020</td>
    </tr>
    <tr>
      <th>cantidad</th>
      <td>99.351784</td>
    </tr>
    <tr>
      <th>units</th>
      <td>85.902711</td>
    </tr>
    <tr>
      <th>area_usuaria</th>
      <td>99.408151</td>
    </tr>
    <tr>
      <th>site_name</th>
      <td>86.263458</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>86.511471</td>
    </tr>
    <tr>
      <th>proyecto</th>
      <td>86.511471</td>
    </tr>
    <tr>
      <th>orden_compra</th>
      <td>1.493715</td>
    </tr>
    <tr>
      <th>tipo_transporte</th>
      <td>86.066174</td>
    </tr>
    <tr>
      <th>audit_cierre_embarque</th>
      <td>99.926723</td>
    </tr>
  </tbody>
</table>
</div>



Después de visualizar estos porcentajes, podemos observar que la trazabilidad del elemento se vuelve un tema difícil.  
Los campos **series** y **activo** que son usados para la trazabilidad, nos muestran un alto índice de missings.
También observamos que el campo que se considerará para una mejor relación entre as fuentes es **lpn_salida**, **num_pedido_att**, **sku_oracle** y **site_id**.

#### 4.2 Data Errors
* **control_serie**: El campo contiene registros una gran diversidad de datos sucios. Siendo un campo booleano, tiene múltiples valores únicos.
* **control_activo**: El campo contiene registros una gran diversidad de datos sucios. Siendo un campo booleano, tiene múltiples valores únicos.
* **activo**: El campo contiene registros nulos mal identificados: "'NA". Se encontraron valores que no corresponden a este campo. 
* **serie**: El campo contiene registros nulos mal identificados: "'NA". No hay un formato estándar. Hay valores que quedaron con notación científica. Hay muchos valores sucios.
* **site_id**: Se hace la notación de que se encuentra un registro con alta frequencia "*Solicitud interna*".
* **area_usuaria**: Se encuentran valores atípicos y no congruentes.
* **tipo_transporte**: Se encuentran valores atípicos y no congruentes.
* **units**: Se encuentran valores atípicos y no congruentes.

### 5. Catálogos.

#### Catálogo de site_id:


```python
Catalogo_Siteid=pd.DataFrame(df.site_id.unique())
Catalogo_Siteid.columns=['Site_ids']

#Remover los sucios
dirt=['Piezas','PIEZAS']
Catalogo_Siteid=Catalogo_Siteid.loc[Catalogo_Siteid.Site_ids.str.len()>6]
Catalogo_Siteid.replace(dirt,np.NaN,regex=True,inplace=True)
Catalogo_Siteid.dropna(inplace=True)
Catalogo_Siteid.reset_index(drop=True)
Catalogo_Siteid.sort_values(by='Site_ids').head(10)
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
      <th>Site_ids</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>443</th>
      <td>ACA-002</td>
    </tr>
    <tr>
      <th>458</th>
      <td>ACA-003</td>
    </tr>
    <tr>
      <th>387</th>
      <td>ACA-010</td>
    </tr>
    <tr>
      <th>406</th>
      <td>ACA-013</td>
    </tr>
    <tr>
      <th>523</th>
      <td>ACA-017</td>
    </tr>
    <tr>
      <th>510</th>
      <td>ACA-019</td>
    </tr>
    <tr>
      <th>58</th>
      <td>ACA-MTX</td>
    </tr>
    <tr>
      <th>251</th>
      <td>AGUAGU1606</td>
    </tr>
    <tr>
      <th>504</th>
      <td>AGUAGU1654</td>
    </tr>
    <tr>
      <th>194</th>
      <td>AGUAGU1655</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo área usuaria:


```python
Catalogo_areas=areas.head(9)
Catalogo_areas=pd.DataFrame(Catalogo_areas.index)
Catalogo_areas.columns=['Áreas']
Catalogo_areas=Catalogo_areas[(Catalogo_areas['Áreas']!='PIEZAS') & (Catalogo_areas['Áreas']!='LTE-850')]
Catalogo_areas
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
      <th>Áreas</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ATT INFRA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>PLANEACION</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NETWORK SECURITY</td>
    </tr>
    <tr>
      <th>4</th>
      <td>METRO CIUDAD MX</td>
    </tr>
    <tr>
      <th>5</th>
      <td>OPERACIONES</td>
    </tr>
    <tr>
      <th>6</th>
      <td>RF REGIONAL</td>
    </tr>
    <tr>
      <th>7</th>
      <td>REFACCIONES</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo: *tipo_transporte*


```python
Catalogo_transportes=pd.DataFrame(trasportes.index)
Catalogo_transportes.columns=['Transportes']
Catalogo_transportes=Catalogo_transportes[(Catalogo_transportes.Transportes=='PROVEEDOR') |
                                          (Catalogo_transportes.Transportes=='AT&T') |
                                          (Catalogo_transportes.Transportes=='PAQUETERIA') |
                                          (Catalogo_transportes.Transportes=='TRANSPORTE DHL') |
                                          (Catalogo_transportes.Transportes=='MSO MEGACENTRO') |
                                          (Catalogo_transportes.Transportes=='OPERACIONES')
                                         ]
Catalogo_transportes
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
      <th>Transportes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>PROVEEDOR</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AT&amp;T</td>
    </tr>
    <tr>
      <th>2</th>
      <td>PAQUETERIA</td>
    </tr>
    <tr>
      <th>3</th>
      <td>TRANSPORTE DHL</td>
    </tr>
    <tr>
      <th>9</th>
      <td>MSO MEGACENTRO</td>
    </tr>
    <tr>
      <th>10</th>
      <td>OPERACIONES</td>
    </tr>
  </tbody>
</table>
</div>



### 6. Preparación de los datos.
Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos: 

* **series**:
    * Tratamiento de missings. 
    * Dar un formato estándar 
    * Revisar valores con notación científica o pasarlos como *NaN* 
    * Revisar datos atípicos, decidir si estos serán marcados como *NaN*.
* **activo**: 
    * Tratamiento de missings 
    * Revisar datos atípicos, decidir si estos serán marcados como *NaN*.
* **quantity**: 
    * Pasar formato a int.
* **units**: 
    * Revisar con negocio cuál será la regla para este campo.
* **area_usuaria**: 
    * Revisar si hay un catálogo existente, de lo contrario, se eliminarían los datos atípicos.
    * Se elimina la palabra *PIEZAS*.
* **control_serie**: 
    * Pasar todos los registros no booleanos a *NaN. Puede ser recuperado tomando como referencia el campo **serie**.
* **control_activo**: 
    * Pasar todos los registros no booleanos a *NaN. Puede ser recuperado tomando como referencia el campo **activo**.
* **site_id**: 
    * Revisar con negocio la regla para los registros *Solicitud interna*.
    * longitud mayor a seis caracteres
    * replace('PIEZAS',np.NaN)
* **orden_compra**: 
    * Revisar si este campo debería ser un código, un booleano o un campo de descripción. Pareciendo más un campo booleano, entonces se propone reemplazar todos los registros sucios por *Si* EN caso de existencia de la PO.
* **tipo_transporte**: 
    * Se busca crear un catálogo. En caso de que no exista uno hecho anteriormente, se propone uno eliminando valores más atípicos.


```python
df_clean=df.copy()

df_clean.site_id.loc[df_clean.site_id.str.len()>6]==np.NaN
df_clean.site_id.replace()

df_clean.area_usuaria.replace('PIEZAS',np.NaN,regex=True,inplace=True)
df_clean.area_usuaria.replace('Piezas',np.NaN,regex=True,inplace=True)
df_clean.area_usuaria.replace('LTE-850',np.NaN,regex=True,inplace=True)
df_clean.replace('vacio',np.NaN,regex=True,inplace=True)

trans_dirt=list(df.tipo_transporte.unique())
trans_clean=['PROVEEDOR','AT&T','PAQUETERIA','TRANSPORTE DHL','MSO MEGACENTRO','OPERACIONES']
trans_dirt=[v for v in trans_dirt if v not in trans_clean]
df_clean.tipo_transporte.replace(trans_dirt,np.NaN,regex=True,inplace=True)

po_clean=list(df.orden_compra.unique())
po_dirt=['vacio','NO','no']
po_clean=[v for v in po_clean if v not in po_dirt]
df_clean.tipo_transporte.replace(po_clean,'SI',regex=True,inplace=True)

#df_clean=df_clean.loc[df_clean.serie_cleaned==0]
df_clean.reset_index(drop=True,inplace=True)
df_clean.head()
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
      <th>organizacion</th>
      <th>lpn_salida</th>
      <th>num_pedido_att</th>
      <th>num_pedido</th>
      <th>sku_oracle</th>
      <th>sku_descripcion</th>
      <th>serie</th>
      <th>activo</th>
      <th>parte</th>
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
      <td>1199829</td>
      <td>2PX</td>
      <td>MEX6490345261059545EMB</td>
      <td>64903452</td>
      <td>P2019112120490</td>
      <td>T.9023243</td>
      <td>ETIQUETA ENROLLABLE AZUL LEYENDA AT&amp;T TAMA?O 4...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>a8c2f91a3ce0cb608eeb5a7bb26179f0cceeda2c8e76e0...</td>
      <td>Salida de Almacen</td>
      <td>2019:111:02:17:57:18</td>
      <td>tx_wlog_embarques</td>
      <td>20191202</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>26</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1194867</td>
      <td>2PX</td>
      <td>MEX6521791761058921EMB</td>
      <td>65217917</td>
      <td>P2019111420284</td>
      <td>CW.1017039</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NTM2012977-2</td>
      <td>...</td>
      <td>868749ebb8e662b6583fa5fd6f29c81ebd3e3da4c75cd6...</td>
      <td>Salida de Almacen</td>
      <td>2019:111:02:17:57:18</td>
      <td>tx_wlog_embarques</td>
      <td>20191202</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>26</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1194850</td>
      <td>2PX</td>
      <td>MEX6521791761058921EMB</td>
      <td>65217917</td>
      <td>P2019111420284</td>
      <td>CW.9056368</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NTAC45840</td>
      <td>...</td>
      <td>2ce3babc03a21cdf66d3bb53d7ea922e58bfee1e418a7e...</td>
      <td>Salida de Almacen</td>
      <td>2019:111:02:17:57:18</td>
      <td>tx_wlog_embarques</td>
      <td>20191202</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>26</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1195310</td>
      <td>2PX</td>
      <td>MEX6522708161059104EMB</td>
      <td>65227081</td>
      <td>P2019111420286</td>
      <td>CW.1017039</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TPM90110-15M</td>
      <td>...</td>
      <td>904311fbe5af95d85a282cb4b697abd1b1245fed38df2f...</td>
      <td>Salida de Almacen</td>
      <td>2019:111:02:17:57:18</td>
      <td>tx_wlog_embarques</td>
      <td>20191202</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>26</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1193216</td>
      <td>2PX</td>
      <td>MEX6518764961058522EMB</td>
      <td>65187649</td>
      <td>P2019111420245</td>
      <td>W.3410142</td>
      <td>JUMPER N-M TO N-M 1M (JP-NM/NM1M-SF12(FR))</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>7a5ed90556fc12f88f8a067db6f6d18c2a0ff13e4d71bb...</td>
      <td>Salida de Almacen</td>
      <td>2019:111:02:17:57:18</td>
      <td>tx_wlog_embarques</td>
      <td>20191202</td>
      <td>delete</td>
      <td>2019</td>
      <td>11</td>
      <td>26</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 33 columns</p>
</div>




```python
#Trazabilidad
df_clean['trazabilidad']=0
df_clean.trazabilidad.loc[(df_clean.serie_cleaned==0) | (df_clean.activo!=np.NaN)]=1

#CS CA
df_clean['CS_CA']=0
df_clean.CS_CA.loc[(df_clean.serie_cleaned==0) & (df_clean.activo!=np.NaN)]=1

#CS SA
df_clean['CS_SA']=0
df_clean.CS_SA.loc[(df_clean.serie_cleaned==0) & (df_clean.activo==np.NaN)]=1

#SS CA
df_clean['SS_CA']=0
df_clean.SS_CA.loc[(df_clean.serie_cleaned==1) & (df_clean.activo!=np.NaN)]=1

```


```python
df_clean.head(3)
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
      <th>organizacion</th>
      <th>lpn_salida</th>
      <th>num_pedido_att</th>
      <th>num_pedido</th>
      <th>sku_oracle</th>
      <th>sku_descripcion</th>
      <th>serie</th>
      <th>activo</th>
      <th>parte</th>
      <th>...</th>
      <th>timestamp</th>
      <th>transaction_status</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie_cleaned</th>
      <th>trazabilidad</th>
      <th>CS_CA</th>
      <th>CS_SA</th>
      <th>SS_CA</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1199829</td>
      <td>2PX</td>
      <td>MEX6490345261059545EMB</td>
      <td>64903452</td>
      <td>P2019112120490</td>
      <td>T.9023243</td>
      <td>ETIQUETA ENROLLABLE AZUL LEYENDA AT&amp;T TAMA?O 4...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>20191202</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>26</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1194867</td>
      <td>2PX</td>
      <td>MEX6521791761058921EMB</td>
      <td>65217917</td>
      <td>P2019111420284</td>
      <td>CW.1017039</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NTM2012977-2</td>
      <td>...</td>
      <td>20191202</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>26</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1194850</td>
      <td>2PX</td>
      <td>MEX6521791761058921EMB</td>
      <td>65217917</td>
      <td>P2019111420284</td>
      <td>CW.9056368</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NTAC45840</td>
      <td>...</td>
      <td>20191202</td>
      <td>insert</td>
      <td>2019</td>
      <td>11</td>
      <td>26</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>3 rows × 37 columns</p>
</div>




```python
from pyspark.sql.types import *
```


```python
mySchema = StructType([ StructField("id", StringType(), True)\
                       ,StructField("organizacion", StringType(), True)\
                       ,StructField("lpn_salida", StringType(), True)\
                       ,StructField("num_pedido_att", StringType(), True)\
                       ,StructField("num_pedido", StringType(), True)\
                       ,StructField("sku_oracle", StringType(), True)\
                       ,StructField("sku_descripcion", StringType(), True)\
                       ,StructField("serie", StringType(), True)\
                       ,StructField("activo", StringType(), True)\
                       ,StructField("parte", StringType(), True)\
                       ,StructField("cantidad", StringType(), True)\
                       ,StructField("units", StringType(), True)\
                       ,StructField("area_usuaria", StringType(), True)\
                       ,StructField("control_serie", StringType(), True)\
                       ,StructField("control_activo", StringType(), True)\
                       ,StructField("site_name", StringType(), True)\
                       ,StructField("site_id", StringType(), True)\
                       ,StructField("proyecto", StringType(), True)\
                       ,StructField("orden_compra", StringType(), True)\
                       ,StructField("tipo_transporte", StringType(), True)\
                       ,StructField("audit_cierre_embarque", StringType(), True)\
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
df_hive = spark.createDataFrame(df_clean,schema = mySchema)

```


```python
df_hive.write.mode("overwrite").saveAsTable('default.eda_wlog')
```


```python
#df_clean.to_excel('Universo_WLOG.xlsx')
```

### 7. Métricas KPI.
Se mostrarán los KPIs generados. 


```python
Total_Elementos=df.shape[0]
Total_Elementos
```




    17741




```python
df.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables


```python
Total_Tr=df.loc[(df.serie_cleaned==0) | (df.activo!='vacio')].shape[0]
Total_Tr
```




    9277



#### Total Elementos NO Trazables


```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    8464



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=df[['serie','activo']].loc[(df.serie_cleaned==0) | (df.activo!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic
```




    2334



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    6943



#### Total de elementos en almacén Trazables Únicos con NSerie, con Nactivo


```python
Total_Tr_Unic_CS_CA=df[['serie','activo']].loc[(df.serie_cleaned==0) & (df.activo!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_CS_CA
```




    812



#### Total de elementos en almacén Trazables Únicos con NSerie, sin Nactivo 


```python
Total_Tr_Unic_CS_SA=df[['serie','activo']].loc[(df.serie_cleaned==0) & (df.activo=='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_CS_SA
```




    662



#### Total de elementos en almacén Trazables Únicos sin NSerie, con Nactivo


```python
Total_Tr_Unic_SS_CA=df[['serie','activo']].loc[(df.serie_cleaned==0) & (df.activo!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_SS_CA
```




    812




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
      <td>17741</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>9277</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>8464</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>2334</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>6943</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Total CS CA</td>
      <td>812</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Total CS SA</td>
      <td>662</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Total SS CA</td>
      <td>812</td>
    </tr>
  </tbody>
</table>
</div>




```python
sc.stop()
```

