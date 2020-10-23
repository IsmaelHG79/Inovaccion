
<div style="width: 100%; clear: both; font-family: Verdana;">
<div style="float: left; width: 50%;font-family: Verdana;">
<img src="https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Blaulabs/image/encabezado.png" align="left">
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

* **Gestor Blaulabs**

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
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import re
import fuzzywuzzy
from fuzzywuzzy import process, fuzz

from pyspark.sql.functions import udf ,col
from pyspark.sql.types import IntegerType,StringType

%matplotlib inline

from bokeh.io import show, output_notebook, output_file 
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20c_11,Category20c_13, Category20c_20, Category10_5,Category10_6, Category20_20, Plasma256
output_notebook()
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="4b2f6d12-aaea-447a-b0ee-df705d7ada8b">Loading BokehJS ...</span>
    </div>




### 1.1 Recolección de los datos: 

*IMPORTANTE*: Si se requieren ver datos de otro periódo, se debe cambiar los filtros ```year = <año-a-ejecutar>```, ```month = <mes-a-ejecutar>```, ```day = <día-a-ejecutar>``` de las tablas en la siguiente celda:


```python
# reglas para serie con pyspark
#sobre el df que se carga con pysaprk, se le agrega una columna 
#con el nombre de serie_cleaned. el cual contiene valores 0 y 1 
```

<div style="width: 100%; clear: both; font-family: Verdana;">
    <p> 
    Se crea el dataframe de spark
    </p>
</div>


```python
df_load1=spark.sql("SELECT * FROM tx_bl_inventarione").cache()#.toPandas() 
```

<div style="width: 100%; clear: both; font-family: Verdana;">
    <p> 
    Creamos una funcion para el tratamiento de datos en spark el cual contiene la reglas definidas para la columna serie:
    </p>
</div>


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
df_serie1 = df_load1.withColumn("serie_cleaned",validate_rule_udf(col("serie"))).cache()
```

<div style="width: 100%; clear: both; font-family: Verdana;">
    <p> 
    Se convierte el dataframe de spark a un dataframe de pandas 
    </p>
</div>


```python
df_ne = df_serie1.toPandas()
```

Hemos recolectado los campos a analizar de la fuente **Blaulabs_NE**.

## Gestor: Blaulabs
Una muestra de la fuente **Blaulabs_NE**


```python
df_ne.head(5)
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
      <th>region</th>
      <th>mso</th>
      <th>sala</th>
      <th>pasillo</th>
      <th>rack</th>
      <th>elemento</th>
      <th>tipo</th>
      <th>marca</th>
      <th>modelo</th>
      <th>serie</th>
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
      <td>Region 1</td>
      <td>Otay</td>
      <td>Sala pop evolution telcos 3</td>
      <td>Fila 1</td>
      <td>Rack 001</td>
      <td>C406-0978</td>
      <td>NE</td>
      <td>ACCEDIAN</td>
      <td>LT</td>
      <td>C406-0978</td>
      <td>...</td>
      <td>c46a939ab0324df2a3679229ad42e276670ae323858024...</td>
      <td>InventarioEM</td>
      <td>2019:101:28:23:35:22</td>
      <td>bl_inventario</td>
      <td>20191129</td>
      <td>insert</td>
      <td>2019</td>
      <td>8</td>
      <td>7</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Region 1</td>
      <td>Otay</td>
      <td>Sala pop evolution telcos 3</td>
      <td>Fila 1</td>
      <td>Rack 001</td>
      <td>ODF FRONTERAODF 30</td>
      <td>NE</td>
      <td>PANDUIT</td>
      <td>OPTICOM</td>
      <td>NE</td>
      <td>...</td>
      <td>c52f0c516c831581ea9b1163490e4676036eab9b02dd9c...</td>
      <td>InventarioEM</td>
      <td>2019:101:28:23:35:22</td>
      <td>bl_inventario</td>
      <td>20191129</td>
      <td>insert</td>
      <td>2019</td>
      <td>8</td>
      <td>7</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Region 1</td>
      <td>Otay</td>
      <td>Sala pop evolution telcos 3</td>
      <td>Fila 1</td>
      <td>Rack 001</td>
      <td>ODF LADO A</td>
      <td>NE</td>
      <td>PANDUIT</td>
      <td>OPTICOM</td>
      <td>NE</td>
      <td>...</td>
      <td>c52f0c516c831581ea9b1163490e4676036eab9b02dd9c...</td>
      <td>InventarioEM</td>
      <td>2019:101:28:23:35:22</td>
      <td>bl_inventario</td>
      <td>20191129</td>
      <td>insert</td>
      <td>2019</td>
      <td>8</td>
      <td>7</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Region 1</td>
      <td>Otay</td>
      <td>Sala pop evolution telcos 3</td>
      <td>Fila 1</td>
      <td>Rack 001</td>
      <td>ODF LADO B</td>
      <td>NE</td>
      <td>PANDUIT</td>
      <td>OPTICOM</td>
      <td>NE</td>
      <td>...</td>
      <td>c52f0c516c831581ea9b1163490e4676036eab9b02dd9c...</td>
      <td>InventarioEM</td>
      <td>2019:101:28:23:35:22</td>
      <td>bl_inventario</td>
      <td>20191129</td>
      <td>insert</td>
      <td>2019</td>
      <td>8</td>
      <td>7</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Region 1</td>
      <td>Otay</td>
      <td>Sala pop evolution telcos 3</td>
      <td>Fila 1</td>
      <td>Rack 001</td>
      <td>TIJ-MTY</td>
      <td>NE</td>
      <td>ACCEDIAN</td>
      <td>METRONID</td>
      <td>NE</td>
      <td>...</td>
      <td>d1db8d095e18cede2016e5e360269f0c98cde8d6a21daa...</td>
      <td>InventarioEM</td>
      <td>2019:101:28:23:35:22</td>
      <td>bl_inventario</td>
      <td>20191129</td>
      <td>insert</td>
      <td>2019</td>
      <td>8</td>
      <td>7</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 22 columns</p>
</div>



### Diccionario de datos.
A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

* **region**: Región en donde se encuentra el elemento.
* **mso**: Oficina ATT.
* **sala**: Pendiente.
* **pasillo**: Pendiente.
* **rack**: Número de Rack.
* **elemento**: Nombre del elemento.
* **tipo**: Pendiente. *Podría ser nombre del dataset*
* **marca**: Marca.
* **modelo**: Modelo.
* **serie**: Código de trazabilidad que da el proveedor.
* **serie_cleaned**: Campo colocado en proceso Spark. Es una bandera que revisa la consistencia de la serie.
* **filedate**: Fecha de carga del archivo.
* **filename**: Nombre del archivo cargado.
* **hash_id**: Identificador único Hash.
* **source_id**: Fuente de archivo.
* **registry_state**: Timestamp de carga.
* **datasetname**: Nombre del ....
* **timestamp**: Fecha de carga.
* **transaction_status**: Estatus de carga.
* **year**: Año del archivo.
* **month**: Mes del archivo.
* **day**: Día del archivo.

### 1.2 Recolección de los datos:


```python
df_load2=spark.sql("SELECT * FROM tx_bl_inventarioem").cache()#.toPandas()
```


```python
df_serie2 = df_load2.withColumn("serie_cleaned",validate_rule_udf(col("serie"))).cache()
```


```python
df_em = df_serie2.toPandas()
```

Hemos recolectado los campos a analizar de la fuente **Blaulabs_EM**.

#### Una visualización de la fuente **Blaulabs_EM**: 


```python
df_em.head()
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
      <th>region</th>
      <th>mso</th>
      <th>sala</th>
      <th>elemento</th>
      <th>descripcion</th>
      <th>capacidad</th>
      <th>tipo</th>
      <th>plataforma</th>
      <th>marca</th>
      <th>modelo</th>
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
      <td>Region 3</td>
      <td>Ciudad Juárez</td>
      <td>Sala Switch</td>
      <td>MSOJUA01-PDF02</td>
      <td>Ciudad Juárez-Sala Switch-MSOJUA01-PDF02</td>
      <td>800 Amp</td>
      <td>EM</td>
      <td>PDF</td>
      <td>GE</td>
      <td>H569445</td>
      <td>...</td>
      <td>7e543bc0819aca2e378e4ce8458d6ab5191a22a3bc9980...</td>
      <td>InventarioEM</td>
      <td>2019:101:28:21:39:20</td>
      <td>bl_inventario</td>
      <td>20191129</td>
      <td>update</td>
      <td>2019</td>
      <td>9</td>
      <td>10</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Region 1</td>
      <td>Otay</td>
      <td>Sala DC 3G</td>
      <td>MSOTIJ01-INV02</td>
      <td>Otay-Sala DC 3G-MSOTIJ01-INV02</td>
      <td></td>
      <td>EM</td>
      <td>Inversor</td>
      <td>MGE UPS SYSTEM</td>
      <td>NE</td>
      <td>...</td>
      <td>07043227d78a2bef90431bd4cbf7a797c83639ac037f57...</td>
      <td>InventarioEM</td>
      <td>2019:101:28:21:39:20</td>
      <td>bl_inventario</td>
      <td>20191129</td>
      <td>delete</td>
      <td>2019</td>
      <td>9</td>
      <td>10</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Region 3</td>
      <td>Ciudad Juárez</td>
      <td>Sala Switch</td>
      <td>MSOJUA01-PDB03</td>
      <td>Ciudad Juárez-Sala Switch-MSOJUA01-PDB03</td>
      <td>300 Amp</td>
      <td>EM</td>
      <td>PDB</td>
      <td>GE</td>
      <td>ED83368-30 G4</td>
      <td>...</td>
      <td>01d16e28d6038a4a3c4fbbc8f535033498c94e1ee912fc...</td>
      <td>InventarioEM</td>
      <td>2019:101:28:21:39:20</td>
      <td>bl_inventario</td>
      <td>20191129</td>
      <td>delete</td>
      <td>2019</td>
      <td>9</td>
      <td>10</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Region 9</td>
      <td>Megacentro</td>
      <td>Sala Verde</td>
      <td>MSOMEX1-PDUB104.03</td>
      <td>Megacentro-Sala Verde-MSOMEX1-PDUB104.03</td>
      <td></td>
      <td>EM</td>
      <td>PDU</td>
      <td>CPI</td>
      <td>NE</td>
      <td>...</td>
      <td>4fc37bba98258df58076bcbc7b76696c5df2bb84dc3ca8...</td>
      <td>InventarioEM</td>
      <td>2019:101:28:21:39:20</td>
      <td>bl_inventario</td>
      <td>20191129</td>
      <td>update</td>
      <td>2019</td>
      <td>9</td>
      <td>10</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Region 1</td>
      <td>Otay</td>
      <td>Sala Telco 1 Evolution</td>
      <td>MSOTIJ01-TEL1E-ST-01</td>
      <td>Otay-Sala Telco 1 Evolution-MSOTIJ01-TEL1E-ST-01</td>
      <td></td>
      <td>EM</td>
      <td>Temperatura</td>
      <td>ENDRESS+HAUSER</td>
      <td>TST434-J1B3D4</td>
      <td>...</td>
      <td>3363b47ce00815319662872254811c6ddd238efa31a910...</td>
      <td>InventarioEM</td>
      <td>2019:101:28:21:39:20</td>
      <td>bl_inventario</td>
      <td>20191129</td>
      <td>insert</td>
      <td>2019</td>
      <td>9</td>
      <td>10</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 24 columns</p>
</div>



### Diccionario de datos.
A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

* **region**: Región en donde se encuentra el elemento.
* **mso**: Oficina ATT.
* **sala**: Pendiente.
* **elemento**: Nombre del elemento.
* **descripcion**: Pendiente.
* **capacidad**: Capacidad de la antena.
* **tipo**: Pendiente. *Podría ser nombre del dataset*
* **plataforma**: Pendiente.
* **marca**: Marca.
* **modelo**: Modelo.
* **serie**: Código de trazabilidad que da el proveedor.
* **activofijo**: Código de trazabilidad que da el proveedor.
* **serie_cleaned**: Campo colocado en proceso Spark. Es una bandera que revisa la consistencia de la serie.
* **filedate**: Fecha de carga del archivo.
* **filename**: Nombre del archivo cargado.
* **hash_id**: Identificador único Hash.
* **source_id**: Fuente de archivo.
* **registry_state**: Timestamp de carga.
* **datasetname**: Nombre del ....
* **timestamp**: Fecha de carga.
* **transaction_status**: Estatus de carga.
* **year**: Año del archivo.
* **month**: Mes del archivo.
* **day**: Día del archivo.

### 2.1 Descripción de las fuentes.
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos=df_ne.columns
print 'Columnas de la fuente Blaulabs_NE son: ',list(campos)
pd.DataFrame(df_ne.dtypes,columns=['Tipo de objeto Blaulabs_NE'])
```

    Columnas de la fuente Blaulabs_NE son:  ['region', 'mso', 'sala', 'pasillo', 'rack', 'elemento', 'tipo', 'marca', 'modelo', 'serie', 'filedate', 'filename', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie_cleaned']





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
      <th>Tipo de objeto Blaulabs_NE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>region</th>
      <td>object</td>
    </tr>
    <tr>
      <th>mso</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sala</th>
      <td>object</td>
    </tr>
    <tr>
      <th>pasillo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>rack</th>
      <td>object</td>
    </tr>
    <tr>
      <th>elemento</th>
      <td>object</td>
    </tr>
    <tr>
      <th>tipo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>marca</th>
      <td>object</td>
    </tr>
    <tr>
      <th>modelo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serie</th>
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
print 'renglones = ',df_ne.shape[0],' columnas = ',df_ne.shape[1]
```

    renglones =  6678  columnas =  22



```python
#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes_ne=[v for v in df_ne.columns if v not in NOrelevantes]

df_ne[relevantes_ne].describe(include='all')
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
      <th>region</th>
      <th>mso</th>
      <th>sala</th>
      <th>pasillo</th>
      <th>rack</th>
      <th>elemento</th>
      <th>tipo</th>
      <th>marca</th>
      <th>modelo</th>
      <th>serie</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>6678</td>
      <td>6678</td>
      <td>6678</td>
      <td>6678</td>
      <td>6678</td>
      <td>6678</td>
      <td>6678</td>
      <td>6678</td>
      <td>6678</td>
      <td>6678</td>
      <td>6678.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>7</td>
      <td>13</td>
      <td>35</td>
      <td>60</td>
      <td>965</td>
      <td>5034</td>
      <td>1</td>
      <td>286</td>
      <td>1209</td>
      <td>1428</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>Region 9</td>
      <td>Megacentro</td>
      <td>Sala core</td>
      <td>Fila 103</td>
      <td>Rack 104.05</td>
      <td>PDU</td>
      <td>NE</td>
      <td>HUBBELL</td>
      <td>NEXTFRAME</td>
      <td>NE</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>2490</td>
      <td>1367</td>
      <td>988</td>
      <td>789</td>
      <td>64</td>
      <td>129</td>
      <td>6678</td>
      <td>1429</td>
      <td>336</td>
      <td>5129</td>
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
      <td>0.815514</td>
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
      <td>0.387909</td>
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
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

* Según lo observado en los uniques de la tabla describe, podrían proponerse para catálogos los campos **region, mso, marca** y **modelo**.
* No hay variables continuas.
* Hay muchos valores *NE* en el campo **serie**, estos serán tratados como data errors y marcados como nulos.

#### Se proponen catálogos derivados de la fuente Blaulabs_NE con los siguientes campos:
    
* **region**: Región en donde se encuentra el elemento.
* **mso**: Oficina ATT.  
* **marca**: Marca.  
* **modelo**: Modelo.    

Estos catálogos nos ayudarán a mapear todos los diferentes proyectos que existen en los cuales hay un activo.


### 2.2 Descripción de las fuentes.

#### Continuamos con Blaulabs_EM


```python
campos=df_em.columns
print 'Columnas de la fuente Blaulabs_EM son: ',list(campos)
pd.DataFrame(df_em.dtypes,columns=['Tipo de objeto Blaulabs_EM'])
```

    Columnas de la fuente Blaulabs_EM son:  ['region', 'mso', 'sala', 'elemento', 'descripcion', 'capacidad', 'tipo', 'plataforma', 'marca', 'modelo', 'serie', 'activofijo', 'filedate', 'filename', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie_cleaned']





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
      <th>Tipo de objeto Blaulabs_EM</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>region</th>
      <td>object</td>
    </tr>
    <tr>
      <th>mso</th>
      <td>object</td>
    </tr>
    <tr>
      <th>sala</th>
      <td>object</td>
    </tr>
    <tr>
      <th>elemento</th>
      <td>object</td>
    </tr>
    <tr>
      <th>descripcion</th>
      <td>object</td>
    </tr>
    <tr>
      <th>capacidad</th>
      <td>object</td>
    </tr>
    <tr>
      <th>tipo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>plataforma</th>
      <td>object</td>
    </tr>
    <tr>
      <th>marca</th>
      <td>object</td>
    </tr>
    <tr>
      <th>modelo</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>object</td>
    </tr>
    <tr>
      <th>activofijo</th>
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
print 'renglones = ',df_em.shape[0],' columnas = ',df_em.shape[1]
```

    renglones =  2830  columnas =  24



```python
#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes_em=[v for v in df_em.columns if v not in NOrelevantes]

df_em[relevantes_em].describe(include='all')
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
      <th>region</th>
      <th>mso</th>
      <th>sala</th>
      <th>elemento</th>
      <th>descripcion</th>
      <th>capacidad</th>
      <th>tipo</th>
      <th>plataforma</th>
      <th>marca</th>
      <th>modelo</th>
      <th>serie</th>
      <th>activofijo</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2830</td>
      <td>2830</td>
      <td>2830</td>
      <td>2830</td>
      <td>2830</td>
      <td>2830</td>
      <td>2830</td>
      <td>2830</td>
      <td>2830</td>
      <td>2830</td>
      <td>2830</td>
      <td>2830</td>
      <td>2830.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>12</td>
      <td>19</td>
      <td>138</td>
      <td>1612</td>
      <td>1669</td>
      <td>108</td>
      <td>2</td>
      <td>18</td>
      <td>102</td>
      <td>237</td>
      <td>978</td>
      <td>730</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>Region 9</td>
      <td>Megacentro</td>
      <td>Sala Switch</td>
      <td>MSOTIJ01-PDF109.00</td>
      <td></td>
      <td></td>
      <td>EM</td>
      <td>PDU</td>
      <td>ENDRESS+HAUSER</td>
      <td>TST434-J1B3D4</td>
      <td>NE</td>
      <td>NE</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>677</td>
      <td>742</td>
      <td>253</td>
      <td>6</td>
      <td>6</td>
      <td>1690</td>
      <td>2828</td>
      <td>500</td>
      <td>866</td>
      <td>808</td>
      <td>978</td>
      <td>854</td>
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
      <td>0.378799</td>
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
      <td>0.485174</td>
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
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

* Según lo observado en los uniques de la tabla describe, podrían proponerse para catálogos los campos **region, mso, marca** y **modelo**. Estos serán corroborados usando los que se proponen en Blaulabs_NE
* No hay variables continuas.
* Hay muchos valores *NE* en los campos **serie** y **activofijo**, estos serán tratados como data errors y marcados como nulos.
* En el campo **capacidad** hay nulos no mapeados.

#### Se proponen catálogos derivados de la fuente Blaulabs_EM con los siguientes campos:
    
* **region**: Región en donde se encuentra el elemento.
* **mso**: Oficina ATT.  
* **marca**: Marca.  
* **modelo**: Modelo.    

Estos catálogos nos ayudarán a mapear todos los diferentes proyectos que existen en los cuales hay un activo.

### 3.1 Exploración de los datos.
De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los catálogos.  
Se empezará analizando el source **Blaulabs_NE**.

#### Para empezar, se hará una limpieza general a los datos:


```python
df_ne.replace('null',np.NaN,inplace=True)
df_ne.replace('NA',np.NaN,inplace=True)
df_ne.replace('',np.NaN,inplace=True)
df_ne.replace('NE',np.NaN,inplace=True)
#Se puede hacer más y por columna en caso de ser necesario
```

### Primer catálogo: *region*

Empezaremos con el catálogo de region. Según lo apreciado en el describe, este campo se encuentra limpio, se harán visualizaciones para corroborar, ver las distintas categorías y sus frecuencias. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
region=pd.DataFrame(df_ne.region.value_counts())

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
region.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Región')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Distribución de las regiones')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
explode_list=[.2,0,0,0,0,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

region['region'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Distribución de las regiones',y=1.12)
ax1.axis('equal')
ax1.legend(labels=region.index,loc='upper left')

plt.show()
```


![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Blaulabs/image/output_52_0.png)


Como se esperaba, es un catálogo limpio, pero se observa que faltan categorías. Se espera poder encontrar más con la fuente *Blaulabs_EM*.  
Se podrá encontrar el catálogo en el apartado **Catálogos**.

#### Segundo catálogo: *mso*


```python
len(df_ne.mso.value_counts())
```




    13




```python
#Revisamos frecuencias:
mso=pd.DataFrame(df_ne.mso.value_counts())

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
mso.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'MSO')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Exploración de MSO')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
explode_list=[.2,0,0,0,0,0,0,0,0,0,0,0.1,0.15] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

mso['mso'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Exploración de MSO',y=1.12)
ax1.axis('equal')
ax1.legend(labels=mso.index,loc='upper left')

plt.show()
```


![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Blaulabs/image/output_56_0.png)


Se tiene un campo limpio, se podrá encontrar el catálogo en el apartado **Catálogos**.

#### Tercer catálogo: *marca* .


```python
pd.DataFrame(df_ne.marca.value_counts()[:45])
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
      <th>marca</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>HUBBELL</th>
      <td>1429</td>
    </tr>
    <tr>
      <th>HUAWEI</th>
      <td>980</td>
    </tr>
    <tr>
      <th>CISCO</th>
      <td>759</td>
    </tr>
    <tr>
      <th>ADC</th>
      <td>596</td>
    </tr>
    <tr>
      <th>HP</th>
      <td>386</td>
    </tr>
    <tr>
      <th>DELL</th>
      <td>202</td>
    </tr>
    <tr>
      <th>TELLABS</th>
      <td>159</td>
    </tr>
    <tr>
      <th>PANDUIT</th>
      <td>147</td>
    </tr>
    <tr>
      <th>HPE</th>
      <td>124</td>
    </tr>
    <tr>
      <th>Cisco Systems Inc</th>
      <td>110</td>
    </tr>
    <tr>
      <th>CIENA</th>
      <td>93</td>
    </tr>
    <tr>
      <th>Cisco Systems</th>
      <td>78</td>
    </tr>
    <tr>
      <th>SUN ORACLE</th>
      <td>77</td>
    </tr>
    <tr>
      <th>NETWORK INSTRUMENT</th>
      <td>74</td>
    </tr>
    <tr>
      <th>ALCATEL LUCENT</th>
      <td>74</td>
    </tr>
    <tr>
      <th>EXTREME NETWORKS</th>
      <td>62</td>
    </tr>
    <tr>
      <th>NORTEL NETWORKS</th>
      <td>60</td>
    </tr>
    <tr>
      <th>IBM</th>
      <td>40</td>
    </tr>
    <tr>
      <th>IXIA</th>
      <td>36</td>
    </tr>
    <tr>
      <th>EQUIPO POR RETIRAR</th>
      <td>36</td>
    </tr>
    <tr>
      <th>FORTINET</th>
      <td>29</td>
    </tr>
    <tr>
      <th>ALCATEL</th>
      <td>28</td>
    </tr>
    <tr>
      <th>NORTEL</th>
      <td>28</td>
    </tr>
    <tr>
      <th>MEJ</th>
      <td>24</td>
    </tr>
    <tr>
      <th>TEJAS NETWORKS</th>
      <td>23</td>
    </tr>
    <tr>
      <th>NETWORK INSTRUMENTS</th>
      <td>23</td>
    </tr>
    <tr>
      <th>COOMSCOPE</th>
      <td>22</td>
    </tr>
    <tr>
      <th>JUNIPER</th>
      <td>22</td>
    </tr>
    <tr>
      <th>ADVA</th>
      <td>21</td>
    </tr>
    <tr>
      <th>ERICSSON</th>
      <td>20</td>
    </tr>
    <tr>
      <th>NETSCOUT</th>
      <td>20</td>
    </tr>
    <tr>
      <th>LUCENT</th>
      <td>19</td>
    </tr>
    <tr>
      <th>CORNING</th>
      <td>19</td>
    </tr>
    <tr>
      <th>ALCATEL-LUCENT</th>
      <td>18</td>
    </tr>
    <tr>
      <th>HEWLETT PACKARD</th>
      <td>18</td>
    </tr>
    <tr>
      <th>SUN MICROSYSTEMS</th>
      <td>17</td>
    </tr>
    <tr>
      <th>COMMSCOPE</th>
      <td>16</td>
    </tr>
    <tr>
      <th>TELECT</th>
      <td>16</td>
    </tr>
    <tr>
      <th>SONUS</th>
      <td>15</td>
    </tr>
    <tr>
      <th>ARISTA</th>
      <td>14</td>
    </tr>
    <tr>
      <th>SYMMETRICOM</th>
      <td>14</td>
    </tr>
    <tr>
      <th>NI TAP</th>
      <td>14</td>
    </tr>
    <tr>
      <th>HITACHI</th>
      <td>14</td>
    </tr>
    <tr>
      <th>A10</th>
      <td>14</td>
    </tr>
    <tr>
      <th>SYSTIMAX</th>
      <td>12</td>
    </tr>
  </tbody>
</table>
</div>




```python
aux=pd.DataFrame(df_ne.marca)
aux.columns=['marca']
aux.dropna(inplace=True)
marcas=list(aux.marca)
marcas=(" ").join(marcas)
marca_wordcloud=WordCloud(background_color='white',max_words=100,collocations=False,stopwords=None).generate(marcas)

plt.figure(figsize=(10,7))
plt.imshow(marca_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
```


![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Blaulabs/image/output_60_0.png)


Observamos que hace falta un poco de limpieza. Hay marcas que difieren como *CISCO* y *Cisco Systems Inc*.  
Encontramos también la presencia de *HPE* y *HP*. Hay múltiples casos en los que se tendría que definir con negocio si son marcas distintas o son la misma. 

#### Cuarto catálogo: modelo


```python
pd.DataFrame(df_ne.modelo.value_counts())
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
      <th>modelo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>NEXTFRAME</th>
      <td>336</td>
    </tr>
    <tr>
      <th>NEXT FRAME</th>
      <td>252</td>
    </tr>
    <tr>
      <th>CAT 6</th>
      <td>239</td>
    </tr>
    <tr>
      <th>CAT6</th>
      <td>221</td>
    </tr>
    <tr>
      <th>UCS C240 M4</th>
      <td>185</td>
    </tr>
    <tr>
      <th>NEXTSPEED6</th>
      <td>147</td>
    </tr>
    <tr>
      <th>PARC</th>
      <td>114</td>
    </tr>
    <tr>
      <th>NEXTSPEED 6</th>
      <td>102</td>
    </tr>
    <tr>
      <th>TRUENET</th>
      <td>99</td>
    </tr>
    <tr>
      <th>PAN-NET</th>
      <td>93</td>
    </tr>
    <tr>
      <th>POWER EDGE R730XD</th>
      <td>76</td>
    </tr>
    <tr>
      <th>AGREGGATION</th>
      <td>72</td>
    </tr>
    <tr>
      <th>DI-R2CU1</th>
      <td>69</td>
    </tr>
    <tr>
      <th>UMG8900</th>
      <td>67</td>
    </tr>
    <tr>
      <th>DPD 100-6-20</th>
      <td>67</td>
    </tr>
    <tr>
      <th>NCS-5501-SE</th>
      <td>62</td>
    </tr>
    <tr>
      <th>4-24419-0361</th>
      <td>57</td>
    </tr>
    <tr>
      <th>NEXTSPEE D6</th>
      <td>56</td>
    </tr>
    <tr>
      <th>OSTA 2.0</th>
      <td>50</td>
    </tr>
    <tr>
      <th>C240 M4</th>
      <td>43</td>
    </tr>
    <tr>
      <th>7750 SR-12</th>
      <td>39</td>
    </tr>
    <tr>
      <th>QUIDWAY S5300 SERIES</th>
      <td>39</td>
    </tr>
    <tr>
      <th>DI-D2GU1</th>
      <td>39</td>
    </tr>
    <tr>
      <th>4-26673-0011</th>
      <td>38</td>
    </tr>
    <tr>
      <th>POWEREDGE R630</th>
      <td>37</td>
    </tr>
    <tr>
      <th>DPD100-6-20</th>
      <td>36</td>
    </tr>
    <tr>
      <th>EQUIPO POR RETIRAR</th>
      <td>36</td>
    </tr>
    <tr>
      <th>UCS 5108</th>
      <td>36</td>
    </tr>
    <tr>
      <th>UCS C220 M4</th>
      <td>36</td>
    </tr>
    <tr>
      <th>PROLIANT DL380 GEN 9</th>
      <td>34</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>RN2285</th>
      <td>1</td>
    </tr>
    <tr>
      <th>TIMEPROVIDER 5000</th>
      <td>1</td>
    </tr>
    <tr>
      <th>SYSTEMAX 1100</th>
      <td>1</td>
    </tr>
    <tr>
      <th>3600</th>
      <td>1</td>
    </tr>
    <tr>
      <th>1031282</th>
      <td>1</td>
    </tr>
    <tr>
      <th>TN-1</th>
      <td>1</td>
    </tr>
    <tr>
      <th>QIP-1210-RAID</th>
      <td>1</td>
    </tr>
    <tr>
      <th>CAT 6 +</th>
      <td>1</td>
    </tr>
    <tr>
      <th>BAYSTACK 60-8T HUB</th>
      <td>1</td>
    </tr>
    <tr>
      <th>UCS-FI-6248UP</th>
      <td>1</td>
    </tr>
    <tr>
      <th>1100 PSE</th>
      <td>1</td>
    </tr>
    <tr>
      <th>POWER EDGE R320</th>
      <td>1</td>
    </tr>
    <tr>
      <th>T120</th>
      <td>1</td>
    </tr>
    <tr>
      <th>PROLIANT ML350</th>
      <td>1</td>
    </tr>
    <tr>
      <th>VNX 5100 SERIES</th>
      <td>1</td>
    </tr>
    <tr>
      <th>CISCO UCS C240 M4</th>
      <td>1</td>
    </tr>
    <tr>
      <th>SUMMITt SUMMIT X450 A 48T</th>
      <td>1</td>
    </tr>
    <tr>
      <th>FLEX SYSTEM ENTERPRISE</th>
      <td>1</td>
    </tr>
    <tr>
      <th>GMX</th>
      <td>1</td>
    </tr>
    <tr>
      <th>E01S</th>
      <td>1</td>
    </tr>
    <tr>
      <th>POWERWOX</th>
      <td>1</td>
    </tr>
    <tr>
      <th>NEXTS PEE D6</th>
      <td>1</td>
    </tr>
    <tr>
      <th>HP PROLIANT DL 380 G7</th>
      <td>1</td>
    </tr>
    <tr>
      <th>HSTNS-1026</th>
      <td>1</td>
    </tr>
    <tr>
      <th>DPR2700</th>
      <td>1</td>
    </tr>
    <tr>
      <th>HP PROLIANT DL380</th>
      <td>1</td>
    </tr>
    <tr>
      <th>ASSY</th>
      <td>1</td>
    </tr>
    <tr>
      <th>FORTIGATE 5050</th>
      <td>1</td>
    </tr>
    <tr>
      <th>IGB PROBE</th>
      <td>1</td>
    </tr>
    <tr>
      <th>MICROCELULA</th>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>1206 rows × 1 columns</p>
</div>




```python
print 'El campo actualmente tiene: ',df_ne.modelo.unique().shape[0],' Registros unicos'
```

    El campo actualmente tiene:  1207  Registros unicos


#### Observamos que este es un campo con muy mala calidad.
Se hacen reglas de limpieza:


```python
aux=pd.DataFrame(df_ne.modelo)
aux.columns=['modelo']
aux.replace(' ','',regex=True,inplace=True)
aux.replace('NEXTSPPED6','NEXTSPEED6',regex=True,inplace=True)
aux.modelo.str.strip()
aux.drop_duplicates(inplace=True)
print'Se han reducido los unicos a: ',aux.shape[0]
aux.head()
```

    Se han reducido los unicos a:  1108





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
      <th>modelo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>LT</td>
    </tr>
    <tr>
      <th>1</th>
      <td>OPTICOM</td>
    </tr>
    <tr>
      <th>4</th>
      <td>METRONID</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NEXTSPEED6</td>
    </tr>
    <tr>
      <th>13</th>
      <td>SUPERVISERYMODULOSM32</td>
    </tr>
  </tbody>
</table>
</div>




```python
aux.dropna(inplace=True)
modelo=list(aux.modelo)
modelo=(" ").join(modelo)
modelo_wordcloud=WordCloud(background_color='white',max_words=100,collocations=False,stopwords=None).generate(modelo)

plt.figure(figsize=(10,7))
plt.imshow(modelo_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
```


![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Blaulabs/image/output_67_0.png)


Para este campo, se tomará como referencia el catálogo que nos ha proveído AT&T.  
Podremos encontrarlo en el apartado **Catálogos**.

#### Visualización de los datos de trazabilidad: 


```python
pd.DataFrame(df_ne.serie.value_counts()[:15])
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
      <th>EQUIPO POR RETIRAR</th>
      <td>36</td>
    </tr>
    <tr>
      <th>PROVEEDOR (IT)</th>
      <td>10</td>
    </tr>
    <tr>
      <th>CX600 SERIES</th>
      <td>7</td>
    </tr>
    <tr>
      <th>SG7000</th>
      <td>3</td>
    </tr>
    <tr>
      <th>8290</th>
      <td>3</td>
    </tr>
    <tr>
      <th>8280</th>
      <td>3</td>
    </tr>
    <tr>
      <th>605365610906000000</th>
      <td>3</td>
    </tr>
    <tr>
      <th>QUIDWAY CX600 SERIES</th>
      <td>3</td>
    </tr>
    <tr>
      <th>S5352C-E1</th>
      <td>2</td>
    </tr>
    <tr>
      <th>NTJS63</th>
      <td>2</td>
    </tr>
    <tr>
      <th>NETENGINE 40 E SERIES</th>
      <td>2</td>
    </tr>
    <tr>
      <th>2553</th>
      <td>2</td>
    </tr>
    <tr>
      <th>439539</th>
      <td>2</td>
    </tr>
    <tr>
      <th>USE124NDNN</th>
      <td>2</td>
    </tr>
    <tr>
      <th>351801005</th>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



Encontramos un problema muy grave de calidad en el campo **serie**.

### 3.2 Exploración de los datos.
Para el caso del source **Blaulabs_EM** se corroborarán los campos contra los analizados anteriormente.

#### Para empezar, se hará una limpieza general a los datos:


```python
df_em.replace('null',np.NaN,inplace=True)
df_em.replace('NA',np.NaN,inplace=True)
df_em.replace('',np.NaN,inplace=True)
df_em.replace('NE',np.NaN,inplace=True)
#Se puede hacer más y por columna en caso de ser necesario
```

### Primer catálogo: *region*

Empezaremos con el catálogo de region. Según lo apreciado en el describe, este campo se encuentra limpio, se harán visualizaciones para corroborar, ver las distintas categorías y sus frecuencias. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
pd.DataFrame(df_em.region.value_counts().keys(),columns=['Regiones']).sort_values(by='Regiones')
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
      <th>Regiones</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>Region 1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Region 2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Region 3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Region 4</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Region 5</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Region 6</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Region 7</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Region 8</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Region 9</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Region 9 Norte</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Region 9 Sur</td>
    </tr>
  </tbody>
</table>
</div>



Hay más registros, es un catálogo mucho más completo, pero se encuentra que el la *región 9* existen más subcategorías.  
Escogeremos este catálogo. Se corroborará con negocio la parte de las subcategorías.
Se podrá encontrar el catálogo en el apartado **Catálogos**.

#### Segundo catálogo: *mso*


```python
print 'MSO en Blaulabs_NE', df_em.mso.value_counts().keys()
print 'MSO en Blaulabs_EM', df_ne.mso.value_counts().keys()
```

    MSO en Blaulabs_NE Index([u'Megacentro', u'Otay', u'Toluca', u'Apodaca', u'Ceylán',
           u'Tlaquepaque', u'Ciudad Juárez', u'Chihuahua', u'Mérida',
           u'Revolución', u'Cancún', u'Puebla', u'R Michel', u'Buenos Aires',
           u'Culiacán', u'Acapulco', u'León Centro', u'Torreón'],
          dtype='object')
    MSO en Blaulabs_EM Index([u'Megacentro', u'Apodaca', u'Tlaquepaque', u'Otay', u'Buenos Aires',
           u'R Michel', u'Revolución', u'Ceylán', u'Toluca', u'Puebla',
           u'Chihuahua', u'Culiacán', u'Ciudad Juárez'],
          dtype='object')


Habiendo comparado los campos en los distintos dataframes, escogemos como catálogo el encontrado en **Blaulabs_NE**.

#### Tercer catálogo: *marca* .


```python
print 'Hay ',df_ne.marca.value_counts().shape[0], ' registros en Blaulabs_NE'
print 'Hay ',df_em.marca.value_counts().shape[0], ' registros en Blaulabs_EM'
```

    Hay  285  registros en Blaulabs_NE
    Hay  100  registros en Blaulabs_EM



```python
marca_ne=list(df_ne.marca.value_counts().keys())
marca_em=list(df_em.marca.value_counts().keys())
marcas=marca_ne+marca_em
cat_marca=set(marcas)
print 'El tamaño del catálogo es: ',len(cat_marca), ' registros'
```

    El tamaño del catálogo es:  373  registros


Hemos concatenado un catálogo con todos los registros que existen en ambas fuentes **Blaulabs**

#### Cuarto catálogo: modelo


```python
print 'Número de registros en Blaulabs_NE: ',df_ne.modelo.unique().shape[0]
print 'Número de registros en Blaulabs_EM: ',df_em.modelo.value_counts().shape[0]
```

    Número de registros en Blaulabs_NE:  1207
    Número de registros en Blaulabs_EM:  235



```python
modelo_NE=list(df_ne.modelo.value_counts().keys())
modelo_EM=list(df_em.modelo.value_counts().keys())
cat_modelos=modelo_NE+modelo_EM
cat_modelos=pd.DataFrame(cat_modelos,columns=['modelos'])
cat_modelos.modelos.str.strip()
cat_modelos.replace(' ','',regex=True,inplace=True)
cat_modelos.drop_duplicates(inplace=True)
cat_modelos.head(10)
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
      <th>modelos</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NEXTFRAME</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CAT6</td>
    </tr>
    <tr>
      <th>4</th>
      <td>UCSC240M4</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NEXTSPEED6</td>
    </tr>
    <tr>
      <th>6</th>
      <td>PARC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>TRUENET</td>
    </tr>
    <tr>
      <th>9</th>
      <td>PAN-NET</td>
    </tr>
    <tr>
      <th>10</th>
      <td>POWEREDGER730XD</td>
    </tr>
    <tr>
      <th>11</th>
      <td>AGREGGATION</td>
    </tr>
    <tr>
      <th>12</th>
      <td>DI-R2CU1</td>
    </tr>
  </tbody>
</table>
</div>



Hemos concatenado el campo *modelo* de ambas fuentes.
El catálogo podrá encontrarse en el apartado **Catálogos**.


```python
aux=pd.DataFrame(df_ne.modelo)
aux.columns=['modelo']
aux.replace(' ','',regex=True,inplace=True)
aux.replace('NEXTSPPED6','NEXTSPEED6',regex=True,inplace=True)
aux.modelo.str.strip()
aux.drop_duplicates(inplace=True)
print'Se han reducido los unicos a: ',aux.shape[0]
aux.head()
```

    Se han reducido los unicos a:  1108





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
      <th>modelo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>LT</td>
    </tr>
    <tr>
      <th>1</th>
      <td>OPTICOM</td>
    </tr>
    <tr>
      <th>4</th>
      <td>METRONID</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NEXTSPEED6</td>
    </tr>
    <tr>
      <th>13</th>
      <td>SUPERVISERYMODULOSM32</td>
    </tr>
  </tbody>
</table>
</div>



#### Visualización de los datos de trazabilidad: 


```python
pd.DataFrame(df_em.serie.value_counts()[:15])
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
      <th>No visible</th>
      <td>27</td>
    </tr>
    <tr>
      <th>1112701</th>
      <td>12</td>
    </tr>
    <tr>
      <th>N8042823176</th>
      <td>10</td>
    </tr>
    <tr>
      <th>SIN DATO</th>
      <td>8</td>
    </tr>
    <tr>
      <th>605365610906000000</th>
      <td>8</td>
    </tr>
    <tr>
      <th>N8045323176</th>
      <td>7</td>
    </tr>
    <tr>
      <th>1434BL00086</th>
      <td>6</td>
    </tr>
    <tr>
      <th>240065-002</th>
      <td>6</td>
    </tr>
    <tr>
      <th>1434BL00087</th>
      <td>6</td>
    </tr>
    <tr>
      <th>N8044F23176</th>
      <td>6</td>
    </tr>
    <tr>
      <th>N803F923176</th>
      <td>6</td>
    </tr>
    <tr>
      <th>N803F323176</th>
      <td>6</td>
    </tr>
    <tr>
      <th>N8040A23176</th>
      <td>5</td>
    </tr>
    <tr>
      <th>13KZ09018603</th>
      <td>5</td>
    </tr>
    <tr>
      <th>N8040F23176</th>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>



#### Podemos observar: 
Es también un problema de calidad lo que se tiene en el campo *serie* de la fuente **Blaulabs_EM** :
* Serie: `SELECT * FROM default.tx_bl_inventarioem WHERE serie =='No visible';`  
Se observa que el campo se encuentra en malas condiciones de calidad.

### 4. Calidad de los datos
Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

### Missings Values
Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.

#### Blaulabs_NE:


```python
df_ne[relevantes_ne].shape[1]
```




    11




```python
nas=df_ne[relevantes_ne].isna().sum()
porcentaje_nas=nas/df_ne[relevantes_ne].isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_11))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```

![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Blaulabs/image/bokeh_plot.png)

  <div class="bk-root" id="e358eca9-6391-495c-bdb3-11ffbe39c184"></div>


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
      <th>region</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>mso</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>sala</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>pasillo</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>rack</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>elemento</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>tipo</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>marca</th>
      <td>0.733753</td>
    </tr>
    <tr>
      <th>modelo</th>
      <td>1.317760</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>76.984127</td>
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
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_11))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```

![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Blaulabs/image/bokeh_plot(1).png)






  <div class="bk-root" id="e12b2ac2-6182-46c9-9de0-069895f2be41"></div>








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
      <th>region</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>mso</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>sala</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>pasillo</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>rack</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>elemento</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>tipo</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>marca</th>
      <td>99.266247</td>
    </tr>
    <tr>
      <th>modelo</th>
      <td>98.682240</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>23.015873</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



Se observa que los campos **tipo** y **serie** reportan graves problemas de missings. El campo *tipo* es completamente nulo, mientras que el campo *serie* usado para trazabilidad, no tiene cumple con más del 25% de registros. Esto sin contar los datos sucios.

#### Data Errors
* **serie**: Contiene múltiples datos sucios. 
* **marca**: No está bien homologado.
* **modelo**: No está bien homologado.

#### Blaulabs_EM:


```python
df_em[relevantes_em].shape[1]
```




    13




```python
nas=df_em[relevantes_em].isna().sum()
porcentaje_nas=nas/df_em[relevantes_em].isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_13))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```






![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Blaulabs/image/bokeh_plot(2).png)

  <div class="bk-root" id="0c5aa472-6e19-48cb-998a-4cf9c3a5b85c"></div>








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
      <th>region</th>
      <td>0.070671</td>
    </tr>
    <tr>
      <th>mso</th>
      <td>0.070671</td>
    </tr>
    <tr>
      <th>sala</th>
      <td>0.070671</td>
    </tr>
    <tr>
      <th>elemento</th>
      <td>0.070671</td>
    </tr>
    <tr>
      <th>descripcion</th>
      <td>0.212014</td>
    </tr>
    <tr>
      <th>capacidad</th>
      <td>59.717314</td>
    </tr>
    <tr>
      <th>tipo</th>
      <td>0.070671</td>
    </tr>
    <tr>
      <th>plataforma</th>
      <td>0.070671</td>
    </tr>
    <tr>
      <th>marca</th>
      <td>15.901060</td>
    </tr>
    <tr>
      <th>modelo</th>
      <td>21.590106</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>35.441696</td>
    </tr>
    <tr>
      <th>activofijo</th>
      <td>45.830389</td>
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
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_13))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```


![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Blaulabs/image/bokeh_plot(3).png)





  <div class="bk-root" id="cc89b61b-a746-42b9-bff5-da3e5829e6e1"></div>








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
      <th>region</th>
      <td>99.929329</td>
    </tr>
    <tr>
      <th>mso</th>
      <td>99.929329</td>
    </tr>
    <tr>
      <th>sala</th>
      <td>99.929329</td>
    </tr>
    <tr>
      <th>elemento</th>
      <td>99.929329</td>
    </tr>
    <tr>
      <th>descripcion</th>
      <td>99.787986</td>
    </tr>
    <tr>
      <th>capacidad</th>
      <td>40.282686</td>
    </tr>
    <tr>
      <th>tipo</th>
      <td>99.929329</td>
    </tr>
    <tr>
      <th>plataforma</th>
      <td>99.929329</td>
    </tr>
    <tr>
      <th>marca</th>
      <td>84.098940</td>
    </tr>
    <tr>
      <th>modelo</th>
      <td>78.409894</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>64.558304</td>
    </tr>
    <tr>
      <th>activofijo</th>
      <td>54.169611</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



Hay más diversidad de campos con missings, nos preocupa en particular el campo *serie*. El campo capacidad también se encuentra con problemas fuertes.

#### Data Errors
* **serie**: Contiene múltiples datos sucios. 
* **capacidad**: No tiene formato estándar.
* **modelo**: No está bien homologado.
* **marca**: No está bien homologado.

### 5. Catálogos.

#### Catálogo de Región:


```python
Catalogo_region=pd.DataFrame(df_em.region.unique())
Catalogo_region.columns=['region']

#Vamos a ocultar los subniveles por región:

Catalogo_region.replace('Region 9 Norte',np.NaN,inplace=True)
Catalogo_region.replace('Region 9 Sur',np.NaN,inplace=True)

#Se le da 
Catalogo_region.dropna(inplace=True)
Catalogo_region.reset_index(drop=True)
print 'Las regiones pueden tener subcategorías'
Catalogo_region.sort_values(by='region').head(10)
```

    Las regiones pueden tener subcategorías





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
      <th>region</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>Region 1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Region 2</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Region 3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Region 4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Region 5</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Region 6</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Region 7</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Region 8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Region 9</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de *MSO*.


```python
Catalogo_MSO=pd.DataFrame(df_ne.mso.unique())
Catalogo_MSO.columns=['mso']
Catalogo_MSO.dropna(inplace=True)
Catalogo_MSO.reset_index(drop=True)
Catalogo_MSO.sort_values(by='mso').head(10)
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
      <th>mso</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>Apodaca</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Buenos Aires</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Ceylán</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Chihuahua</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ciudad Juárez</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Culiacán</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Megacentro</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Otay</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Puebla</td>
    </tr>
    <tr>
      <th>6</th>
      <td>R Michel</td>
    </tr>
  </tbody>
</table>
</div>



#### Tercer catálogo: *Marca*.


```python
cat_marca=list(cat_marca)
Catalogo_marca=pd.DataFrame(cat_marca)
Catalogo_marca.columns=['marca']
especiales=['-','#','%','/','$','_']
Catalogo_marca.replace('ALACATEL LUCENT','ALCATEL LUCENT',regex=True,inplace=True)
Catalogo_marca.replace('ALCATEL . LUCENT','ALCATEL LUCENT',regex=True,inplace=True)
Catalogo_marca.replace('ALCATEL TLUCEN','ALCATEL LUCENT',regex=True,inplace=True)
Catalogo_marca.replace('ALCATEL.LUCENT','ALCATEL LUCENT',regex=True,inplace=True)
Catalogo_marca.replace('A 10','A10',regex=True,inplace=True)
Catalogo_marca.replace('ALCATEL-LUNCENT','ALCATEL LUCENT',regex=True,inplace=True)
Catalogo_marca.replace(especiales,' ',regex=True,inplace=True)
Catalogo_marca.marca=Catalogo_marca.marca.str.upper()
Catalogo_marca.drop_duplicates(inplace=True)
Catalogo_marca.dropna(inplace=True)
Catalogo_marca.reset_index(drop=True)
Catalogo_marca.sort_values(by='marca').head(30)
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
      <th>marca</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>367</th>
      <td>0TT0M0T0RES</td>
    </tr>
    <tr>
      <th>194</th>
      <td>3COM</td>
    </tr>
    <tr>
      <th>24</th>
      <td>3M</td>
    </tr>
    <tr>
      <th>267</th>
      <td>A10</td>
    </tr>
    <tr>
      <th>365</th>
      <td>ACCEDIAN</td>
    </tr>
    <tr>
      <th>199</th>
      <td>ACDATA</td>
    </tr>
    <tr>
      <th>216</th>
      <td>ACME PACKET</td>
    </tr>
    <tr>
      <th>183</th>
      <td>ADC</td>
    </tr>
    <tr>
      <th>333</th>
      <td>ADS</td>
    </tr>
    <tr>
      <th>218</th>
      <td>ADVA</td>
    </tr>
    <tr>
      <th>15</th>
      <td>ADVANCED TCA</td>
    </tr>
    <tr>
      <th>219</th>
      <td>ADVC</td>
    </tr>
    <tr>
      <th>125</th>
      <td>AFL</td>
    </tr>
    <tr>
      <th>120</th>
      <td>AHVESHAN</td>
    </tr>
    <tr>
      <th>154</th>
      <td>ALBER</td>
    </tr>
    <tr>
      <th>184</th>
      <td>ALCATEL</td>
    </tr>
    <tr>
      <th>29</th>
      <td>ALCATEL LUCENT</td>
    </tr>
    <tr>
      <th>195</th>
      <td>ALLIED TELESYN</td>
    </tr>
    <tr>
      <th>140</th>
      <td>ALLOT</td>
    </tr>
    <tr>
      <th>371</th>
      <td>ALPHA</td>
    </tr>
    <tr>
      <th>312</th>
      <td>AMP</td>
    </tr>
    <tr>
      <th>306</th>
      <td>AMP NETCONNECT</td>
    </tr>
    <tr>
      <th>116</th>
      <td>APC</td>
    </tr>
    <tr>
      <th>96</th>
      <td>APC SCHNEIDER</td>
    </tr>
    <tr>
      <th>346</th>
      <td>ARGUS</td>
    </tr>
    <tr>
      <th>368</th>
      <td>ARISTA</td>
    </tr>
    <tr>
      <th>126</th>
      <td>ARRIED TLESYN</td>
    </tr>
    <tr>
      <th>254</th>
      <td>ASCOM</td>
    </tr>
    <tr>
      <th>138</th>
      <td>ASTEC</td>
    </tr>
    <tr>
      <th>55</th>
      <td>ATEN</td>
    </tr>
  </tbody>
</table>
</div>



#### Cuarto catálogo: *Modelo*.

Se mostrará el catálogo que el equipo AT&T nos ha proveído:


```python
Catalogo_modelo=spark.sql("SELECT model FROM inventario.raw_panda_physical_inventory").toPandas() 
```


```python
Catalogo_modelo.replace(u'',np.NaN,regex=True,inplace=True)
Catalogo_modelo.drop_duplicates(inplace=True)
Catalogo_modelo.dropna(inplace=True)
Catalogo_modelo.reset_index(drop=True,inplace=True)
Catalogo_modelo.drop(labels=1,axis=0,inplace=True)
Catalogo_modelo.reset_index(drop=True,inplace=True)
Catalogo_modelo.head(10)
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
      <th>model</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>�A�Q�U�4�5�1�8�R�2�1�</td>
    </tr>
    <tr>
      <th>1</th>
      <td>�H�B�X�X�-�6�5�1�6�D�S�-�A�2�M�</td>
    </tr>
    <tr>
      <th>2</th>
      <td>�D�B�X�L�H�-�6�5�6�5�B�-�A�2�M�</td>
    </tr>
    <tr>
      <th>3</th>
      <td>�B�M�L�1�6�1�1�7�9�/�3�</td>
    </tr>
    <tr>
      <th>4</th>
      <td>�B�M�G�9�8�0�3�5�1�/�3�</td>
    </tr>
    <tr>
      <th>5</th>
      <td>�K�D�U� �1�3�7� �6�2�4�</td>
    </tr>
    <tr>
      <th>6</th>
      <td>�K�D�U� �1�3�7� �7�3�9�</td>
    </tr>
    <tr>
      <th>7</th>
      <td>�K�D�U� �1�3�7� �1�7�4�</td>
    </tr>
    <tr>
      <th>8</th>
      <td>�O�D�V�2�-�0�6�5�R�1�8�K�-�G�V�1�</td>
    </tr>
    <tr>
      <th>9</th>
      <td>�O�D�V�3�-�0�6�5�R�1�8�K�-�G�V�1�</td>
    </tr>
  </tbody>
</table>
</div>



### 6. Preparación de los datos.
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

* **marca**: Se enlistan las reglas utilizadas para un catálogo óptimo:
    * Se eliminan los siguientes caracteres especiales:    '-','#','%','/','_'
    * replace('ALACATEL LUCENT','ALCATEL LUCENT')
    * replace('ALCATEL . LUCENT','ALCATEL LUCENT')
    * replace('ALCATEL TLUCEN','ALCATEL LUCENT')
    * replace('ALCATEL.LUCENT','ALCATEL LUCENT')
    * replace('A 10','A10')
    * replace('ALCATEL-LUNCENT','ALCATEL LUCENT')
    * replace(especiales,' ')
    * Pasar todo a uppercase

### 7.1 Métricas KPI.
Se mostrarán los KPIs generados. **Blaulabs_NE**. 


```python
NE_Total_Elementos=df_ne.shape[0]
NE_Total_Elementos
```




    6678




```python
df_ne.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables


```python
NE_Total_Tr=df_ne.loc[(df_ne.serie_cleaned==0)].shape[0]
NE_Total_Tr
```




    1232



#### Total Elementos NO Trazables


```python
NE_Total_NOTr=NE_Total_Elementos-NE_Total_Tr
NE_Total_NOTr
```




    5446



#### Total Elementos Trazables Únicos


```python
NE_Total_Tr_Unic=df_ne[['serie']].loc[(df_ne.serie_cleaned==0)].drop_duplicates().shape[0]
NE_Total_Tr_Unic
```




    1183



#### Total de elementos trazables duplicados


```python
NE_Total_Tr_Dupli=NE_Total_Tr-NE_Total_Tr_Unic
NE_Total_Tr_Dupli
```




    49




```python
KPIs=pd.DataFrame({'KPI':['Total Elementos en Blaulabs_ne','Total Elementos Trazables en Blaulabs_ne',
                         'Total NO Trazables en Blaulabs_ne','Total Trazables Unicos en Blaulabs_ne',
                         'Total Trazables Duplicados en Blaulabs_ne'],
                  'Resultado':[NE_Total_Elementos,NE_Total_Tr,NE_Total_NOTr,
                              NE_Total_Tr_Unic,NE_Total_Tr_Dupli]})

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
      <td>Total Elementos en Blaulabs_ne</td>
      <td>6678</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables en Blaulabs_ne</td>
      <td>1232</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables en Blaulabs_ne</td>
      <td>5446</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos en Blaulabs_ne</td>
      <td>1183</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados en Blaulabs_ne</td>
      <td>49</td>
    </tr>
  </tbody>
</table>
</div>



### 7.2 Métricas KPI.
Se mostrarán los KPIs generados. **Blaulabs_EM**. 


```python
EM_Total_Elementos=df_em.shape[0]
EM_Total_Elementos
```




    2830




```python
df_em.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables


```python
EM_Total_Tr=df_em.loc[(df_em.serie_cleaned==0)].shape[0]
EM_Total_Tr
```




    1758



#### Total Elementos NO Trazables


```python
EM_Total_NOTr=EM_Total_Elementos-EM_Total_Tr
EM_Total_NOTr
```




    1072



#### Total Elementos Trazables Únicos


```python
EM_Total_Tr_Unic=df_em[['serie']].loc[(df_em.serie_cleaned==0)].drop_duplicates().shape[0]
EM_Total_Tr_Unic
```




    954



#### Total de elementos trazables duplicados


```python
EM_Total_Tr_Dupli=EM_Total_Tr-EM_Total_Tr_Unic
EM_Total_Tr_Dupli
```




    804




```python
KPIs=pd.DataFrame({'KPI':['Total Elementos en Blaulabs_em','Total Elementos Trazables en Blaulabs_em',
                         'Total NO Trazables en Blaulabs_em','Total Trazables Unicos en Blaulabs_em',
                         'Total Trazables Duplicados en Blaulabs_em'],
                  'Resultado':[EM_Total_Elementos,EM_Total_Tr,EM_Total_NOTr,
                              EM_Total_Tr_Unic,EM_Total_Tr_Dupli]})

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
      <td>Total Elementos en Blaulabs_em</td>
      <td>2830</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables en Blaulabs_em</td>
      <td>1758</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables en Blaulabs_em</td>
      <td>1072</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos en Blaulabs_em</td>
      <td>954</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados en Blaulabs_em</td>
      <td>804</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_em_clean=df_em.loc[df_em.serie_cleaned==0]
df_ne_clean=df_ne.loc[df_ne.serie_cleaned==0]
```


```python
df_em_clean.to_excel('Universo_Blaulabs_inventarioem.xlsx')
df_ne_clean.to_excel('Universo_Blaulabs_inventarione.xlsx')
```


```python
sc.stop()
```
