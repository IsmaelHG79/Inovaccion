
<div style="width: 100%; clear: both; font-family: Verdana;">
<div style="float: left; width: 50%;font-family: Verdana;">
<img src="https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Sedona/image/encabezado.png" align="left">
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
Analizaremos los datos de las fuentes de inventarios de AT&T con un tratamiento estadístico descriptivo para hacer el tracking del ciclo de vida de los elementos de red. Se creará un EDA enfocado al gestor Sedona. Serán documentados los catálogos propuestos junto a su respectivo tratamiento de datos. La fuente que corresponde a este análisis es el:

* **Gestor Sedona**

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
conf = SparkConf().setAppName('Sedona')  \
    .setMaster('yarn').set("spark.yarn.queue","root.eda")  \
    .set("spark.kryoserializer.buffer.mb","128").set("spark.yarn.executor.memoryOverhead","409")
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
from bokeh.palettes import Category20_9,Category20c_7,Category10_5,Category10_6,Category20c_8,Plasma256
output_notebook()
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="566f9c9d-1915-4754-8eeb-2ad5a2769fb4">Loading BokehJS ...</span>
    </div>




---
### 1.1 Recolección de los datos: 

*IMPORTANTE*: Si se requieren ver datos de otro periódo, se debe cambiar los filtros ```year = <año-a-ejecutar>```, ```month = <mes-a-ejecutar>```, ```day = <día-a-ejecutar>``` de las tablas en la siguiente celda:


```python
# reglas para serie con pyspark
#sobre el df que se carga con pysaprk, se le agrega una columna 
#con el nombre de serie_cleaned. el cual contiene valores 0 y 1
```

Se crea el dataframe de spark


```python
df_load1 = spark.sql("SELECT inventory_type,serial_number,system_name,site_id,ip,longitude,latitude FROM tx_sedona_huawei").cache()#.toPandas() 
```

Creamos una función para el tratamiento de datos en spark el cual contiene la reglas definidas para la columna serie:


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

Se crea un udf en spark sobre la función ya creada.


```python
validate_rule_udf = udf(validate_rule, IntegerType())
```

Se le agrega una nueva columna al dataframe de spark; la nueva columna es la validacion de la columna serie con respecto al udf que creamos.


```python
df_serie1 = df_load1.withColumn("serie_cleaned",validate_rule_udf(col("serial_number"))).cache()
```


```python
def coding_rule(string):
    test = u'%s' % (string)
    str_temp = test.encode('utf-8')
    return str_temp
coding_str_udf = udf(coding_rule, StringType())
```


```python
df_carga = df_load1.withColumn("inventory_type_Cod",coding_str_udf(col("inventory_type"))) \
                    .withColumn("longitude_Cod",coding_str_udf(col("longitude"))) \
                    .withColumn("latitude_Cod",coding_str_udf(col("latitude"))) \
                    .withColumn("system_name_Cod",coding_str_udf(col("system_name"))) \
                    .withColumn("serial_number_Cod",coding_str_udf(col("serial_number"))) \
                    .withColumn("site_id_Cod",coding_str_udf(col("site_id"))) \
                    .withColumn("ip_Cod",coding_str_udf(col("ip")))
                    #.withColumn("serie_cleaned_Cod",coding_str_udf(col("serie_cleaned"))) \
```

Se convierte el dataframe de spark a un dataframe de pandas.


```python
Sedona_hwi = df_load1.toPandas()
```

Hemos recolectado los campos a analizar de la fuente Sedona_huawei.

Por razones técnicas, se creará la bandera *serie_cleaned* desde python para este caso.


```python
search_list=[" ",'!','%','$',"<",">","^",'¡',"+","N/A",u'¿','~','#',
             'Ñ',"Ã","Åƒ","Ã‹","Ã³",'Ë','*','?',"ILEGIBLE", "VICIBLE",
             "VISIBLE","INCOMPLETO","BORRADO"]

Sedona_hwi['serie_cleaned']=0
Sedona_hwi.serie_cleaned.loc[(Sedona_hwi.serial_number.isin(search_list)) |
                            (Sedona_hwi.serial_number.str.len<6)]=1
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/pandas/core/algorithms.py:421: UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
      f = lambda x, y: htable.ismember_object(x, values)
    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/pandas/core/indexing.py:189: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self._setitem_with_indexer(indexer, value)


## Gestor Sedona Huawei
Una muestra de la fuente Sedona Huawei.


```python
Sedona_hwi.head()
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
      <th>inventory_type</th>
      <th>serial_number</th>
      <th>system_name</th>
      <th>site_id</th>
      <th>ip</th>
      <th>longitude</th>
      <th>latitude</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Router</td>
      <td>210235230610F4000008</td>
      <td>MX-HMEX0269-CX6X1-1</td>
      <td>ST/37a575e4-0074-469a-9c76-aa4919b4a3bc</td>
      <td>10.33.107.26</td>
      <td>-98.878425</td>
      <td>19.515802</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Router</td>
      <td>210235230610E8000005</td>
      <td>MX-HMEX0437-CX6X1-1</td>
      <td>ST/FGKnlQvyXcUigNIdaeMs</td>
      <td>10.33.107.27</td>
      <td>-99.0975111</td>
      <td>19.7960917</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Router</td>
      <td>210235230610C6000046</td>
      <td>MXBCNENS0020RTBHCSRMOB02</td>
      <td>ST/HENS0018</td>
      <td>10.38.217.128</td>
      <td>-116.588083</td>
      <td>31.875861</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Router</td>
      <td>210235230610C6000048</td>
      <td>MXBCNENS0022RTBHCSRMOB02</td>
      <td>ST/13042844-62fd-445f-8479-027de59a654d</td>
      <td>10.38.217.129</td>
      <td>-116.606996</td>
      <td>31.857608</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Router</td>
      <td>210235230610C6000031</td>
      <td>MXBCNMXC0076RTBHCSRMOB02</td>
      <td>ST/82745db6-f9f6-419c-8ff5-faba9c8b006d</td>
      <td>10.38.217.131</td>
      <td>-115.485845</td>
      <td>32.662752</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



### Diccionario de datos.
A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

* **inventory_type**: Tipo de elemento del inventario.
* **serial_number**: Número de serie.
* **system_name**: Nombre del sistema.
* **site_id**: Código de sitio.
* **ip**: Dirección IP.
* **longitude**: Coordenada Longitud.
* **latitude**: Coordenada Latitud.
* **serie_cleaned**: Bandera que indica el estado del número de serie, 0 implica buen estado, 1 implica mal estado.

---
### 1.2 Recolección de los datos:


```python
df_load2 = spark.sql("SELECT system_name,ip_address,vendor,serial_number,site_id FROM tx_sedona_ne").cache()#.toPandas() 
```


```python
df_serie2 = df_load2.withColumn("serie_cleaned",validate_rule_udf(col("serial_number"))).cache()
```


```python
Sedona_ne = df_serie2.toPandas()
```

Hemos recolectado los campos a analizar de la fuente Sedona_ne.

## Gestor Sedona NE
Una muestra de la fuente Sedona NE.


```python
Sedona_ne.head()
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
      <th>system_name</th>
      <th>ip_address</th>
      <th>vendor</th>
      <th>serial_number</th>
      <th>site_id</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>TIJMTX-BCN1015-CA</td>
      <td>10.190.0.0</td>
      <td>ALU</td>
      <td>NS114861119</td>
      <td>PORFIRIO DIAZ</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>TIJMTX-BCN1015-CB</td>
      <td>10.190.0.1</td>
      <td>ALU</td>
      <td>NS120767855</td>
      <td>PORFIRIO DIAZ</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>TIJGTA-IUSTB00956-WA</td>
      <td>10.190.0.10</td>
      <td>ALU</td>
      <td>NS120767842</td>
      <td>TIJUANA(GTAC)</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>CULMTX-CUL011-CA</td>
      <td>10.190.0.100</td>
      <td>ALU</td>
      <td>NS121366557</td>
      <td>SWITCH CULIACAN</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>CULMTX-CUL011-CB</td>
      <td>10.190.0.101</td>
      <td>ALU</td>
      <td>NS121366573</td>
      <td>SWITCH CULIACAN</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



### Diccionario de datos.
A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

* **system_name**: Nombre del sistema.
* **ip_address**: Dirección IP.
* **vendor**: Proveedor.
* **serial_number**: Número de serie.
* **site_id**: Sitio.
* **serie_cleaned**: Bandera que indica el estado del número de serie, 0 implica buen estado, 1 implica mal estado.

---
### 1.3 Recolección de los datos:


```python
df_load3 = spark.sql("SELECT vendor,inventory_type,ip,site_id,longitude,latitude,serial_number,system_name FROM tx_sedona_nokia").cache()#.toPandas() 
```


```python
df_serie3 = df_load3.withColumn("serie_cleaned",validate_rule_udf(col("serial_number"))).cache()
```


```python
Sedona_Nokia = df_serie3.toPandas()
```

Hemos recolectado los campos a analizar de la fuente Sedona_nokia.

### Gestor Sedona Nokia
Una muestra de la fuente Sedona Nokia.


```python
Sedona_Nokia.head()
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
      <th>vendor</th>
      <th>inventory_type</th>
      <th>ip</th>
      <th>site_id</th>
      <th>longitude</th>
      <th>latitude</th>
      <th>serial_number</th>
      <th>system_name</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ALU</td>
      <td>Router</td>
      <td>10.190.3.19</td>
      <td>ST/d269211b-6008-4239-9c73-21e446f411e1</td>
      <td>-86.8575889</td>
      <td>21.152367</td>
      <td>NS12186M667</td>
      <td>CANMTX-ROO8018-SA</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ALU</td>
      <td>Router</td>
      <td>10.190.3.20</td>
      <td>ST/d269211b-6008-4239-9c73-21e446f411e1</td>
      <td>-86.8575889</td>
      <td>21.152367</td>
      <td>NS12076B820</td>
      <td>CANMTX-ROO8018-SB</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ALU</td>
      <td>Router</td>
      <td>10.190.0.247</td>
      <td>ST/8dfc8f8c-8897-4bad-9da6-cc0591fa24e9</td>
      <td>-106.077358</td>
      <td>28.64176</td>
      <td>NS12176C557</td>
      <td>CHIMTX-CHI100-SA</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ALU</td>
      <td>Router</td>
      <td>10.190.0.248</td>
      <td>ST/8dfc8f8c-8897-4bad-9da6-cc0591fa24e9</td>
      <td>-106.077358</td>
      <td>28.64176</td>
      <td>NS12186M688</td>
      <td>CHIMTX-CHI100-SB</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ALU</td>
      <td>Router</td>
      <td>10.190.1.2</td>
      <td>ST/3f84f77e-210e-415b-8408-0ee5a93db378</td>
      <td>-106.427003</td>
      <td>31.722933</td>
      <td>NS12166P802</td>
      <td>JUAMTX-JUA002-SA</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



### Diccionario de datos.
A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

* **vendor**: Proveedor.
* **inventory_type**: Tipo de elemento del inventario.
* **ip**: Dirección IP.
* **site_id**: Código de sitio.
* **longitude**: Coordenada Longitud.
* **latitude**: Coordenada Latitud.
* **serial_number**: Número de serie.
* **system_name**: Nombre del sistema.
* **serie_cleaned**: Bandera que indica el estado del número de serie, 0 implica buen estado, 1 implica mal estado.

---
### 2.1 Descripción de las fuentes.
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos=Sedona_hwi.columns
print 'Columnas de la fuente Sedona_NE son: ',list(campos)
pd.DataFrame(Sedona_hwi.dtypes,columns=['Tipo de objeto Sedona_hwi'])
```

    Columnas de la fuente Sedona_NE son:  ['inventory_type', 'serial_number', 'system_name', 'site_id', 'ip', 'longitude', 'latitude', 'serie_cleaned']





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
      <th>Tipo de objeto Sedona_hwi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>inventory_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>object</td>
    </tr>
    <tr>
      <th>system_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ip</th>
      <td>object</td>
    </tr>
    <tr>
      <th>longitude</th>
      <td>object</td>
    </tr>
    <tr>
      <th>latitude</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>int64</td>
    </tr>
  </tbody>
</table>
</div>




```python
print 'renglones = ',Sedona_hwi.shape[0],' columnas = ',Sedona_hwi.shape[1]
```

    renglones =  1213798  columnas =  8



```python
#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes=[v for v in Sedona_hwi.columns if v not in NOrelevantes]

Sedona_hwi[relevantes].describe(include='all')
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
      <th>inventory_type</th>
      <th>serial_number</th>
      <th>system_name</th>
      <th>site_id</th>
      <th>ip</th>
      <th>longitude</th>
      <th>latitude</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1213798</td>
      <td>1213798</td>
      <td>1213798</td>
      <td>1213798</td>
      <td>1213798</td>
      <td>1213798</td>
      <td>1213798</td>
      <td>1213798.0</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>5</td>
      <td>17283</td>
      <td>520</td>
      <td>389</td>
      <td>519</td>
      <td>388</td>
      <td>388</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>Router Port</td>
      <td></td>
      <td>MXTLAM01RTCOREMOB08</td>
      <td></td>
      <td>10.33.77.20</td>
      <td></td>
      <td></td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>870274</td>
      <td>391331</td>
      <td>10879</td>
      <td>1191481</td>
      <td>10879</td>
      <td>1191481</td>
      <td>1191481</td>
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
      <td>0.0</td>
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
      <td>0.0</td>
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
      <td>0.0</td>
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
      <td>0.0</td>
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
      <td>0.0</td>
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
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

* Como posibles catálogos se tienen: *inventory_type*, y *site_id*.
* Se observa que existen campos en blanco en varios campos.

#### Se proponen catálogos derivados de la fuente Sedona_hwi con los siguientes campos:
    
* **inventory_type**: Tipo de elemento del inventario..
* **site_id**: Código de sitio.  

Estos catálogos nos ayudarán a mapear todos los diferentes proyectos que existen en los cuales hay un activo.


---
### 2.2 Descripción de las fuentes.
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos=Sedona_ne.columns
print 'Columnas de la fuente Sedona_NE son: ',list(campos)
pd.DataFrame(Sedona_ne.dtypes,columns=['Tipo de objeto Sedona_NE'])
```

    Columnas de la fuente Sedona_NE son:  ['system_name', 'ip_address', 'vendor', 'serial_number', 'site_id', 'serie_cleaned']





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
      <th>Tipo de objeto Sedona_NE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>system_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ip_address</th>
      <td>object</td>
    </tr>
    <tr>
      <th>vendor</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>object</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>int32</td>
    </tr>
  </tbody>
</table>
</div>




```python
print 'renglones = ',Sedona_ne.shape[0],' columnas = ',Sedona_ne.shape[1]
```

    renglones =  56672  columnas =  6



```python
#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes=[v for v in Sedona_ne.columns if v not in NOrelevantes]

Sedona_ne[relevantes].describe(include='all')
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
      <th>system_name</th>
      <th>ip_address</th>
      <th>vendor</th>
      <th>serial_number</th>
      <th>site_id</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>56672</td>
      <td>56672</td>
      <td>56672</td>
      <td>56672</td>
      <td>56672</td>
      <td>56672.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>1289</td>
      <td>1288</td>
      <td>2</td>
      <td>1290</td>
      <td>767</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>VILLAV-MEX9322-GA</td>
      <td>10.35.77.158</td>
      <td>ALU</td>
      <td>NS12086H212</td>
      <td>MEGACENTRO</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>44</td>
      <td>44</td>
      <td>33836</td>
      <td>44</td>
      <td>880</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.000018</td>
    </tr>
    <tr>
      <th>std</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.004201</td>
    </tr>
    <tr>
      <th>min</th>
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
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
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
      <td>0.000000</td>
    </tr>
    <tr>
      <th>max</th>
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



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

* Tenemos dos únicos vendors, donde predomina **ALU**.
* Esta tabla contiene más sites id que la anterior.

#### Se proponen catálogos derivados de la fuente Sedona_ne con los siguientes campos:
    
* **site_id**: Código de sitio.

Estos catálogos nos ayudarán a mapear todos los diferentes proyectos que existen en los cuales hay un activo.

---
### 2.3 Descripción de las fuentes.
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos=Sedona_Nokia.columns
print 'Columnas de la fuente Sedona_Nokia son: ',list(campos)
pd.DataFrame(Sedona_Nokia.dtypes,columns=['Tipo de objeto Sedona_Nokia'])
```

    Columnas de la fuente Sedona_Nokia son:  ['vendor', 'inventory_type', 'ip', 'site_id', 'longitude', 'latitude', 'serial_number', 'system_name', 'serie_cleaned']





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
      <th>Tipo de objeto Sedona_Nokia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>vendor</th>
      <td>object</td>
    </tr>
    <tr>
      <th>inventory_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ip</th>
      <td>object</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>longitude</th>
      <td>object</td>
    </tr>
    <tr>
      <th>latitude</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>object</td>
    </tr>
    <tr>
      <th>system_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>int32</td>
    </tr>
  </tbody>
</table>
</div>




```python
print 'renglones = ',Sedona_Nokia.shape[0],' columnas = ',Sedona_Nokia.shape[1]
```

    renglones =  2044812  columnas =  9



```python
#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes=[v for v in Sedona_Nokia.columns if v not in NOrelevantes]

Sedona_Nokia[relevantes].describe(include='all')
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
      <th>vendor</th>
      <th>inventory_type</th>
      <th>ip</th>
      <th>site_id</th>
      <th>longitude</th>
      <th>latitude</th>
      <th>serial_number</th>
      <th>system_name</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2044812</td>
      <td>2044812</td>
      <td>2044812</td>
      <td>2044812</td>
      <td>2044812</td>
      <td>2044812</td>
      <td>2044812</td>
      <td>2044812</td>
      <td>2.044812e+06</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>1</td>
      <td>5</td>
      <td>769</td>
      <td>418</td>
      <td>417</td>
      <td>417</td>
      <td>24838</td>
      <td>769</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>ALU</td>
      <td>Router Port</td>
      <td>10.190.3.154</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>TOLBUE-MEX9295-SA</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>2044812</td>
      <td>1454032</td>
      <td>15369</td>
      <td>2010976</td>
      <td>2010976</td>
      <td>2010976</td>
      <td>799058</td>
      <td>15369</td>
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
      <td>3.924410e-01</td>
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
      <td>4.882941e-01</td>
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
      <td>0.000000e+00</td>
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
      <td>0.000000e+00</td>
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
      <td>0.000000e+00</td>
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
      <td>1.000000e+00</td>
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
      <td>1.000000e+00</td>
    </tr>
  </tbody>
</table>
</div>



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

* Existe un único *vendor* que es **ALU**.
* Se encuentran muchos registros en blanco.
* También tiene sites id, será revisado este campo junto a los catálogos de las tablas anteriores. 

#### Se proponen catálogos derivados de la fuente Sedona_Nokia con los siguientes campos:
    
* **site_id**: Código de sitio.

Estos catálogos nos ayudarán a mapear todos los diferentes proyectos que existen en los cuales hay un activo.

---
### 3.1 Exploración de los datos.
De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los catálogos.

#### Para empezar, se hará una limpieza general a los datos:


```python
Sedona_hwi.replace('null',np.NaN,inplace=True)
Sedona_hwi.replace(r'^\s*$',np.NaN,regex=True,inplace=True)
```

### Primer catálogo: *inventory_type*

Empezaremos con el catálogo de inventory_type. Nuestra intención por el momento es simplemente explorar los datos.


```python
pd.DataFrame(Sedona_hwi.inventory_type.value_counts())
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
      <th>inventory_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Router Port</th>
      <td>870274</td>
    </tr>
    <tr>
      <th>Router Card</th>
      <td>260620</td>
    </tr>
    <tr>
      <th>Router Power Supply</th>
      <td>38270</td>
    </tr>
    <tr>
      <th>Router Fan</th>
      <td>22317</td>
    </tr>
    <tr>
      <th>Router</th>
      <td>22317</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Revisamos frecuencias:
inventory_type=pd.DataFrame(Sedona_hwi.inventory_type.value_counts())

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
inventory_type.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'inventory_type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Distribuciones de los tipos de elemento en inventario')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
explode_list=[.2,0,0,0,0.1] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

inventory_type['inventory_type'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Distribuciones de los tipos de elemento en inventario',y=1.12)
ax1.axis('equal')
ax1.legend(labels=inventory_type.index,loc='upper left')

plt.show()
```


![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Sedona/image/output_71_0.png)


Parece un campo limpio, sin embargo no sabemos qué tipo de Router son los que sólo vienen con esta categoría.
Se encontrará el catálogo en el apartado **Catálogos**.

### Segundo catálogo *site_id*


```python
Sedona_hwi.site_id.value_counts().count()
```




    388




```python
pd.DataFrame(Sedona_hwi.site_id.value_counts()).head(20)
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
      <th>site_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ST/HMEX0585</th>
      <td>645</td>
    </tr>
    <tr>
      <th>ST/HMTY1012</th>
      <td>602</td>
    </tr>
    <tr>
      <th>ST/HGDL1029</th>
      <td>473</td>
    </tr>
    <tr>
      <th>ST/HTIJ0128</th>
      <td>301</td>
    </tr>
    <tr>
      <th>ST/HLEO0008</th>
      <td>301</td>
    </tr>
    <tr>
      <th>ST/HCUN0013</th>
      <td>258</td>
    </tr>
    <tr>
      <th>ST/ee8c8761-c38a-4c28-a769-02960a82a239</th>
      <td>258</td>
    </tr>
    <tr>
      <th>ST/HCUL0032</th>
      <td>258</td>
    </tr>
    <tr>
      <th>ST/HTPC0020</th>
      <td>258</td>
    </tr>
    <tr>
      <th>ST/HPUE0054</th>
      <td>258</td>
    </tr>
    <tr>
      <th>ST/HCHI0032</th>
      <td>258</td>
    </tr>
    <tr>
      <th>ST/HVER0019</th>
      <td>258</td>
    </tr>
    <tr>
      <th>ST/HREY0013</th>
      <td>258</td>
    </tr>
    <tr>
      <th>ST/eb1edfa0-d433-4c87-93c7-f929426b3829</th>
      <td>258</td>
    </tr>
    <tr>
      <th>ST/HJRZ0015</th>
      <td>215</td>
    </tr>
    <tr>
      <th>ST/HCAB0008</th>
      <td>215</td>
    </tr>
    <tr>
      <th>ST/929abefc-5bcf-4ea9-a5b8-f9d468632a24</th>
      <td>215</td>
    </tr>
    <tr>
      <th>ST/HHER0030</th>
      <td>215</td>
    </tr>
    <tr>
      <th>ST/HVHE0015</th>
      <td>215</td>
    </tr>
    <tr>
      <th>ST/486a1c7a-a0ab-4916-afd6-e9435da0e0b7</th>
      <td>215</td>
    </tr>
  </tbody>
</table>
</div>



#### Para este catálogo se hará un cruce los los catálogos del mismo campo en las demás tablas, se buscará obtener un catálogo completo.
Pueden observarse registros con formato irregular, sin embargo por la frequencia de los mismos, no se tomarán como sucios.

#### Visualización de los datos de trazabilidad: 


```python
pd.DataFrame(Sedona_hwi.serial_number.value_counts()[:15])
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
      <th>030MGEW0C5000004</th>
      <td>86</td>
    </tr>
    <tr>
      <th>2102120529P0B5000164</th>
      <td>86</td>
    </tr>
    <tr>
      <th>030MDQ10C8000079</th>
      <td>86</td>
    </tr>
    <tr>
      <th>2102120529P0B5000109</th>
      <td>86</td>
    </tr>
    <tr>
      <th>2102120514P0C3000361</th>
      <td>86</td>
    </tr>
    <tr>
      <th>030MDQ10DB000019</th>
      <td>86</td>
    </tr>
    <tr>
      <th>2102120529P0B7000424</th>
      <td>86</td>
    </tr>
    <tr>
      <th>2102120514P0C3000363</th>
      <td>86</td>
    </tr>
    <tr>
      <th>2102120529P0B4000311</th>
      <td>86</td>
    </tr>
    <tr>
      <th>2102120529P0B4000316</th>
      <td>86</td>
    </tr>
    <tr>
      <th>2102120529P0B5000165</th>
      <td>86</td>
    </tr>
    <tr>
      <th>030MDQ10C8000075</th>
      <td>86</td>
    </tr>
    <tr>
      <th>2102120529P0B5000168</th>
      <td>86</td>
    </tr>
    <tr>
      <th>2102120529P0B5000169</th>
      <td>86</td>
    </tr>
    <tr>
      <th>2102120529P0B4001088</th>
      <td>86</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.DataFrame(Sedona_hwi.serie_cleaned.value_counts()).plot(kind='barh',
                                                           figsize=(8,5),
                                                           title='Estado del campo serie',
                                                          colormap='coolwarm')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f99b52c07d0>




![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Sedona/image/output_79_1.png)


#### Es de interés haber observado los datos que se usaran para la trazabilidad.
Se nota que el campo serie mantiene un formato estándar y según los datos que nos muestra el plot, también son datos saludables.

---
### 3.2 Exploración de los datos.

#### Para empezar, se hará una limpieza general a los datos:


```python
Sedona_ne.replace('null',np.NaN,inplace=True)
Sedona_ne.replace(r'^\s*$', np.NaN,regex=True,inplace=True)
```

### Catálogo: *site_id*

Para este campo, se buscará ver si hay relación con los registros únicos encontrados en el catálogo de la tabla anterior y los de la tabla Sedona NE.


```python
Sedona_ne.site_id.value_counts().count()
```




    766




```python
Cat_site_id=list(Sedona_ne.site_id.unique())
Cat_site_id[:15]
```




    [u'PORFIRIO DIAZ',
     u'TIJUANA(GTAC)',
     u'SWITCH CULIACAN',
     u'DIAMANTE',
     u'CULIACAN / TV AZTECA',
     u'CONSTITUYENTES / INDEPENDENCIA',
     u'CULIACAN(GTAC)',
     u'SWITCH (MAZ-220(001))',
     u'SORIANA VALLE DORADO',
     u'ZAPATA (MZ3047)',
     u'SWITCH (GUY-480)',
     u'SHILLIS / LOS ALAMOS',
     u'SWITCH (CDO-531)',
     u'MAGISTERIO(SW)',
     u'MAZATLAN(GTAC)']



No son el mismo tipo de registros. Se tratarán como catálogos distintos.
Se llamará al catálogo limpio en el apartado de catálogos.

#### Visualización de los datos de trazabilidad: 


```python
pd.DataFrame(Sedona_ne.serial_number.value_counts()[:15])
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
      <th>NS12086H212</th>
      <td>44</td>
    </tr>
    <tr>
      <th>NS121366590</th>
      <td>44</td>
    </tr>
    <tr>
      <th>NS121861551</th>
      <td>44</td>
    </tr>
    <tr>
      <th>NS152466711</th>
      <td>44</td>
    </tr>
    <tr>
      <th>NS114963198</th>
      <td>44</td>
    </tr>
    <tr>
      <th>NS114963199</th>
      <td>44</td>
    </tr>
    <tr>
      <th>2102351933P0B1000023</th>
      <td>44</td>
    </tr>
    <tr>
      <th>210305254610B4000480</th>
      <td>44</td>
    </tr>
    <tr>
      <th>NS114963193</th>
      <td>44</td>
    </tr>
    <tr>
      <th>NS114963195</th>
      <td>44</td>
    </tr>
    <tr>
      <th>NS114963196</th>
      <td>44</td>
    </tr>
    <tr>
      <th>NS152466715</th>
      <td>44</td>
    </tr>
    <tr>
      <th>NS152165709</th>
      <td>44</td>
    </tr>
    <tr>
      <th>2102351933P0BC000027</th>
      <td>44</td>
    </tr>
    <tr>
      <th>210305254610B6000340</th>
      <td>44</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.DataFrame(Sedona_ne.serie_cleaned.value_counts()).plot(kind='barh',
                                                          figsize=(8,5),
                                                          title='Estado del campo serie',
                                                          colormap='Spectral')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f99b52c0050>




![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Sedona/image/output_91_1.png)


#### Es de interés haber observado los datos que se usaran para la trazabilidad, parece que el campo serie se encuentra con buena salud. 

---
### 3.3 Exploración de los datos.
De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los catálogos.

#### Para empezar, se hará una limpieza general a los datos:


```python
Sedona_Nokia.replace('null',np.NaN,inplace=True)
Sedona_Nokia.replace(r'^\s*$', np.NaN,regex=True,inplace=True)
```

### Catálogo: *site_id*

Se buscará saber con qué tabla tiene relación este campo. Una vez encontrada, se cruzará para generar un catálogo completo.


```python
Sedona_Nokia.site_id.value_counts()[:15]
```




    ST/HMEX0183                                528
    ST/86af7e72-8ee2-4db5-9528-78a7aa265325    440
    ST/cdd60825-213b-41f2-b9d9-0b4b82bb182a    396
    ST/098af68f-8094-4b82-b7ee-6e79edd91f16    352
    ST/5e42596d-dd44-49be-a612-55aca7dc51f5    352
    ST/b5aa401d-33ff-4c8d-a315-036b8207b2b5    352
    ST/59f8d0b8-d057-4775-9bf0-ada03262c293    352
    ST/7cfffc24-c9d9-432f-a8cf-5b16685c0d45    352
    ST/78a4a75c-bcc5-4893-9e13-a04b68195d69    352
    ST/8e2732dc-5af3-47f6-ad50-df8719ed77b8    308
    ST/34ddbd4e-7aee-4a74-a936-5f2fe0a34cab    308
    ST/1fa40243-db8b-4651-8618-739cc68f79f6    308
    ST/3f84f77e-210e-415b-8408-0ee5a93db378    308
    ST/d269211b-6008-4239-9c73-21e446f411e1    308
    ST/a5509ad5-ea71-4096-b26d-38fd64983cf1    308
    Name: site_id, dtype: int64



Podemos ver que es el mismo campo que en la tabla **Sedona_hwi**.


```python
Cat_sitios=set(list(Sedona_hwi.site_id.unique())+list(Sedona_Nokia.site_id.unique()))
Cat_sitios=list(Cat_sitios)
Cat_sitios[:15]
```




    [u'ST/HMEX0319',
     u'ST/HTPC0030',
     u'ST/8172d32a-0255-4599-9038-307c3fff845a',
     nan,
     u'ST/c7ca5781-4d60-42bd-bd78-5547b90a375b',
     u'ST/7079af29-edfd-45e0-a0dc-550d1045da2c',
     u'ST/51681910-0d11-4732-abed-198f3956ccbe',
     u'ST/37a575e4-0074-469a-9c76-aa4919b4a3bc',
     u'ST/b149a9b1-3ea0-4a6a-8196-f87848c8db9a',
     u'ST/b01fca08-13c4-40ac-a2ab-085dc7c3d2d9',
     u'ST/9bf4c821-12df-482a-88cb-57b12e9c6d3c',
     u'ST/HFBS9001',
     u'ST/HMEX0484',
     u'ST/3321f85e-a67b-4d02-8601-feac29f396b7',
     u'ST/HJRZ0023']



Tenemos el catálogo completo.

#### Visualización de los datos de trazabilidad: 


```python
pd.DataFrame(Sedona_Nokia.serial_number.value_counts()[:15])
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
      <th>PMA5VZL</th>
      <td>4323</td>
    </tr>
    <tr>
      <th>NS1547F0270</th>
      <td>264</td>
    </tr>
    <tr>
      <th>NS152364765</th>
      <td>264</td>
    </tr>
    <tr>
      <th>NS1706F0325</th>
      <td>264</td>
    </tr>
    <tr>
      <th>NS1527F0838</th>
      <td>264</td>
    </tr>
    <tr>
      <th>NS152364779</th>
      <td>264</td>
    </tr>
    <tr>
      <th>NS1546F1019</th>
      <td>264</td>
    </tr>
    <tr>
      <th>NS152364764</th>
      <td>264</td>
    </tr>
    <tr>
      <th>none</th>
      <td>262</td>
    </tr>
    <tr>
      <th>NS152665740</th>
      <td>249</td>
    </tr>
    <tr>
      <th>NS153360859</th>
      <td>249</td>
    </tr>
    <tr>
      <th>NS153360891</th>
      <td>249</td>
    </tr>
    <tr>
      <th>NS153360892</th>
      <td>249</td>
    </tr>
    <tr>
      <th>NS153562312</th>
      <td>246</td>
    </tr>
    <tr>
      <th>NS153562313</th>
      <td>246</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.DataFrame(Sedona_Nokia.serie_cleaned.value_counts()).plot(kind='barh',
                                                          figsize=(8,5),
                                                          title='Estado del campo serie',
                                                          colormap='Accent')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f9a1a5f2790>




![png](https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Sedona/image/output_104_1.png)


#### Es de interés haber observado los datos que se usaran para la trazabilidad, se encontró un campo saludable.
Se pasarán algunas reglas de limpieza.

---
### 4.1 Calidad de los datos
Se documentará la calidad de los datos y analizarán las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

### Missings Values
Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.


```python
Sedona_hwi.shape
```




    (1213798, 8)




```python
nas=Sedona_hwi.isna().sum()
porcentaje_nas=nas/Sedona_hwi.isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_8))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```








  <div class="bk-root" id="158fa0f2-4fd6-4db0-9801-5de81fd01d55"></div>








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
      <th>inventory_type</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>32.240208</td>
    </tr>
    <tr>
      <th>system_name</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>98.161391</td>
    </tr>
    <tr>
      <th>ip</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>longitude</th>
      <td>98.161391</td>
    </tr>
    <tr>
      <th>latitude</th>
      <td>98.161391</td>
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
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_8))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```








  <div class="bk-root" id="116ac4bc-9bfd-4c81-9afa-f97f8e65aabb"></div>








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
      <th>inventory_type</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>67.759792</td>
    </tr>
    <tr>
      <th>system_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>1.838609</td>
    </tr>
    <tr>
      <th>ip</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>longitude</th>
      <td>1.838609</td>
    </tr>
    <tr>
      <th>latitude</th>
      <td>1.838609</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



Los missings se centran en los campos de longitud, latitud y site_id.

---
### 4.2 Calidad de los datos
Se documentará la calidad de los datos y analizarán las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

### Missings Values
Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.


```python
Sedona_ne.shape
```




    (56672, 6)




```python
nas=Sedona_ne.isna().sum()
porcentaje_nas=nas/Sedona_ne.isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category10_6))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```








  <div class="bk-root" id="3545de7e-5c1e-49ab-a893-942bd5f18bd7"></div>








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
      <th>system_name</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>ip_address</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>vendor</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>0.001765</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>0.155280</td>
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
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category10_6))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```








  <div class="bk-root" id="813e57ae-43b5-49cf-8b55-512e0d4b21cb"></div>








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
      <th>system_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>ip_address</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>vendor</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>99.998235</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>99.844720</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



Esta tabla se encuentra en perfecto estado.

---

### 4.3 Calidad de los datos
Se documentará la calidad de los datos y analizarán las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

### Missings Values
Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.


```python
Sedona_Nokia.shape
```




    (2044812, 9)




```python
nas=Sedona_Nokia.isna().sum()
porcentaje_nas=nas/Sedona_Nokia.isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20_9))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```








  <div class="bk-root" id="aee8e640-3cf9-4f7e-a5a9-4d12b6ab158e"></div>








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
      <th>vendor</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>inventory_type</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>ip</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>98.345276</td>
    </tr>
    <tr>
      <th>longitude</th>
      <td>98.345276</td>
    </tr>
    <tr>
      <th>latitude</th>
      <td>98.345276</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>39.077333</td>
    </tr>
    <tr>
      <th>system_name</th>
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
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20_9))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```








  <div class="bk-root" id="cc67d50e-cc2a-41ae-bce9-1fb8a31663d8"></div>








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
      <th>vendor</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>inventory_type</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>ip</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>site_id</th>
      <td>1.654724</td>
    </tr>
    <tr>
      <th>longitude</th>
      <td>1.654724</td>
    </tr>
    <tr>
      <th>latitude</th>
      <td>1.654724</td>
    </tr>
    <tr>
      <th>serial_number</th>
      <td>60.922667</td>
    </tr>
    <tr>
      <th>system_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



En esta tabla los missings matienen una distribución parecida a la de la tabla **Sedona_hwi**.

Según lo observado en los campos *serial_number* se hará una limpieza para estos campos:


```python
Sedona_Nokia.serial_number.fillna(np.NaN,inplace=True)
```

---
### 5 Catálogos.

#### Catálogo *inventory_type*:


```python
Cat_inventory_type=pd.DataFrame(Sedona_hwi.inventory_type.unique())
Cat_inventory_type.columns=['inventory_type']
Cat_inventory_type.sort_values(by='inventory_type').head(10)
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
      <th>inventory_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Router</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Router Card</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Router Fan</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Router Port</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Router Power Supply</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo *Site_code*:


```python
Cat_site_codes=pd.DataFrame(Cat_sitios)
Cat_site_codes.columns=['Site_codes']
Cat_site_codes.replace(u'nan',np.NaN,regex=True,inplace=True)
Cat_site_codes.replace(u'N/A',np.NaN,regex=True,inplace=True)
Cat_site_codes.replace(u'ST/','',regex=True,inplace=True)
Cat_site_codes.dropna(inplace=True)
Cat_site_codes.reset_index(inplace=True,drop=True)
Cat_site_codes.head()
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
      <th>Site_codes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HMEX0319</td>
    </tr>
    <tr>
      <th>1</th>
      <td>HTPC0030</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8172d32a-0255-4599-9038-307c3fff845a</td>
    </tr>
    <tr>
      <th>3</th>
      <td>c7ca5781-4d60-42bd-bd78-5547b90a375b</td>
    </tr>
    <tr>
      <th>4</th>
      <td>7079af29-edfd-45e0-a0dc-550d1045da2c</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo *Sites*: 


```python
Cat_sitios=pd.DataFrame(Sedona_ne.site_id.unique(),columns=['Sitios'])
Cat_sitios.head()
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
      <th>Sitios</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>PORFIRIO DIAZ</td>
    </tr>
    <tr>
      <th>1</th>
      <td>TIJUANA(GTAC)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SWITCH CULIACAN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>DIAMANTE</td>
    </tr>
    <tr>
      <th>4</th>
      <td>CULIACAN / TV AZTECA</td>
    </tr>
  </tbody>
</table>
</div>



---
### 6. Preparación de los datos.
Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos: 

* **Reglas generales**:
    * Eliminar registros en blanco.
    * Eliminar registros 'nan'.
    * Eliminar iniciales 'ST/' para site_codes.
    * Eliminar registros None.

---
### 7.1 Métricas KPI.
Se mostrarán los KPIs generados. 


```python
Sedona_hwi.replace(np.NaN,'vacio',inplace=True)
```

#### Total de elementos


```python
Total_Elementos_hwi=Sedona_hwi.shape[0]
Total_Elementos_hwi
```




    1213798



#### Total Elementos Trazables


```python
Total_Tr_hwi=Sedona_hwi.loc[(Sedona_hwi.serie_cleaned==0) & (Sedona_hwi.serial_number!='vacio')].shape[0]
Total_Tr_hwi
```




    822467



#### Total Elementos NO Trazables


```python
Total_NOTr_hwi=Total_Elementos_hwi-Total_Tr_hwi
Total_NOTr_hwi
```




    391331



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic_hwi=Sedona_hwi['serial_number'].loc[(Sedona_hwi.serie_cleaned==0) &
                                              (Sedona_hwi.serial_number!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_hwi
```




    17282



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli_hwi=Total_Tr_hwi-Total_Tr_Unic_hwi
Total_Tr_Dupli_hwi
```




    805185




```python
print '        KPIs Sedona_hwi'
KPIs=pd.DataFrame({'KPIs Sedona_hwi':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos_hwi,Total_Tr_hwi,Total_NOTr_hwi,
                              Total_Tr_Unic_hwi,Total_Tr_Dupli_hwi]})

KPIs
```

            KPIs Sedona_hwi





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
      <th>KPIs Sedona_hwi</th>
      <th>Resultado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Total Elementos</td>
      <td>1213798</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>822467</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>391331</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>17282</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>805185</td>
    </tr>
  </tbody>
</table>
</div>




```python
#df_hive_kpi = spark.createDataFrame(KPIs)
```


```python
#df_hive_kpi.write.mode("overwrite").saveAsTable("default.kpi_odk_38") #hdfs://attdatalakehdfs/user/hive/warehouse/eda_odk_99
```

---
### 7.2 Métricas KPI.
Se mostrarán los KPIs generados. 


```python
Sedona_ne.replace(np.NaN,'vacio',inplace=True)
```

#### Total de elementos


```python
Total_Elementos_ne=Sedona_ne.shape[0]
Total_Elementos_ne
```




    56672



#### Total Elementos Trazables


```python
Total_Tr_ne=Sedona_ne.loc[(Sedona_ne.serie_cleaned==0) & (Sedona_ne.serial_number!='vacio')].shape[0]
Total_Tr_ne
```




    56671



#### Total Elementos NO Trazables


```python
Total_NOTr_ne=Total_Elementos_ne-Total_Tr_ne
Total_NOTr_ne
```




    1



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic_ne=Sedona_ne['serial_number'].loc[(Sedona_ne.serie_cleaned==0) &
                                                (Sedona_ne.serial_number!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_ne
```




    1289



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli_ne=Total_Tr_ne-Total_Tr_Unic_ne
Total_Tr_Dupli_ne
```




    55382




```python
print '          KPIs Sedona_ne'

KPIs=pd.DataFrame({'KPIs Sedona_ne':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos_ne,Total_Tr_ne,Total_NOTr_ne,
                              Total_Tr_Unic_ne,Total_Tr_Dupli_ne]})

KPIs
```

              KPIs Sedona_ne





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
      <th>KPIs Sedona_ne</th>
      <th>Resultado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Total Elementos</td>
      <td>56672</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>56671</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>1289</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>55382</td>
    </tr>
  </tbody>
</table>
</div>




```python
#df_hive_kpi = spark.createDataFrame(KPIs)
```


```python
#df_hive_kpi.write.mode("overwrite").saveAsTable("default.kpi_odk_38") #hdfs://attdatalakehdfs/user/hive/warehouse/eda_odk_99
```

---
### 7.3 Métricas KPI.
Se mostrarán los KPIs generados. 


```python
Sedona_Nokia.replace(np.NaN,'vacio',inplace=True)
```

#### Total de elementos


```python
Total_Elementos_nk=Sedona_Nokia.shape[0]
Total_Elementos_nk
```




    2044812



#### Total Elementos Trazables


```python
Total_Tr_nk=Sedona_Nokia.loc[(Sedona_Nokia.serie_cleaned==0) & (Sedona_Nokia.serial_number!='vacio')].shape[0]
Total_Tr_nk
```




    1242344



#### Total Elementos NO Trazables


```python
Total_NOTr_nk=Total_Elementos_nk-Total_Tr_nk
Total_NOTr_nk
```




    802468



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic_nk=Sedona_Nokia['serial_number'].loc[(Sedona_Nokia.serie_cleaned==0) &
                                                   (Sedona_Nokia.serial_number!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_nk
```




    24763



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli_nk=Total_Tr_nk-Total_Tr_Unic_nk
Total_Tr_Dupli_nk
```




    1217581




```python
print '         KPIs Sedona_Nokia'

KPIs=pd.DataFrame({'KPIs Sedona_Nokia':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos_nk,Total_Tr_nk,Total_NOTr_nk,
                              Total_Tr_Unic_nk,Total_Tr_Dupli_nk]})

KPIs
```

             KPIs Sedona_Nokia





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
      <th>KPIs Sedona_Nokia</th>
      <th>Resultado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Total Elementos</td>
      <td>2044812</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>1242344</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>802468</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>24763</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>1217581</td>
    </tr>
  </tbody>
</table>
</div>



#### Se suben las tablas a Hive:


```python
#df_hive_kpi = spark.createDataFrame(KPIs)
```


```python
#df_hive_kpi.write.mode("overwrite").saveAsTable("default.kpi_odk_38") #hdfs://attdatalakehdfs/user/hive/warehouse/eda_odk_99
```


```python
sc.stop()
```


```python

```
