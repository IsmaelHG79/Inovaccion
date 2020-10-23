
<div style="width: 100%; clear: both; font-family: Verdana;">
<div style="float: left; width: 50%;font-family: Verdana;">
<img src="https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Ciena/image/encabezado.png" align="left">
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

* **Gestor Ciena**

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
import re

from pyspark.sql.functions import udf ,col
from pyspark.sql.types import IntegerType,StringType

%matplotlib inline

from bokeh.io import show, output_notebook, output_file 
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20_11, Category20c_20, Category10_5,Category10_6, Category20_20, Plasma256,Category20c_18
output_notebook()
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="49a6e880-217b-416e-901e-8f1353d5844c">Loading BokehJS ...</span>
    </div>




### Recolección de los datos: 

*IMPORTANTE*: Si se requieren ver datos de otro periódo, se debe cambiar los filtros ```year = <año-a-ejecutar>```, ```month = <mes-a-ejecutar>```, ```day = <día-a-ejecutar>``` de las tablas en la siguiente celda:

Se crea el dataframe de spark


```python
df_load =spark.sql("SELECT *, serial_number as serie FROM default.tx_ciena").cache()#.toPandas() 
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
df_serie = df_load.withColumn("serie_cleaned",validate_rule_udf(col("serie"))).cache()
```

<div style="width: 100%; clear: both; font-family: Verdana;">
    <p> 
    Se convierte el dataframe de spark a un dataframe de pandas 
    </p>
</div>


```python
df = df_serie.toPandas()
```

Hemos recolectado los campos a analizar de la fuente **tx_ciena**.

## Características de los elementos de red en Ciena
Una muestra de la fuente Ciena


```python
df.drop(columns=['serial_number'],inplace=True)
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
      <th>system_name</th>
      <th>ne_type</th>
      <th>component</th>
      <th>component_subtype</th>
      <th>clei_code</th>
      <th>part_number</th>
      <th>manufacture_date</th>
      <th>hardware_version</th>
      <th>firmware_version</th>
      <th>software_version</th>
      <th>...</th>
      <th>sourceid</th>
      <th>registry_state</th>
      <th>datasetname</th>
      <th>timestamp</th>
      <th>transaction_status</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>serie</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CAGSNFO0027OTN1401</td>
      <td>6500-14</td>
      <td>10-ene</td>
      <td>100GOCLD</td>
      <td>WOTRCPLFAA</td>
      <td>NTK539UD</td>
      <td>2015-44</td>
      <td>8</td>
      <td>--</td>
      <td>REL1121Z.AW</td>
      <td>...</td>
      <td>Gestores-CIENA</td>
      <td>2019:10:26:13:32:46</td>
      <td>tx_ciena</td>
      <td>20191126</td>
      <td>insert</td>
      <td>2019</td>
      <td>7</td>
      <td>15</td>
      <td>NNTMRT0DE0K6</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CAGSNFO0027OTN1401</td>
      <td>6500-14</td>
      <td>oct-13</td>
      <td>PKTOTN</td>
      <td>WOTRC9SFAB</td>
      <td>NTK667AA</td>
      <td>2014-38</td>
      <td>5</td>
      <td>--</td>
      <td>REL1121Z.AW</td>
      <td>...</td>
      <td>Gestores-CIENA</td>
      <td>2019:10:26:13:32:46</td>
      <td>tx_ciena</td>
      <td>20191126</td>
      <td>insert</td>
      <td>2019</td>
      <td>7</td>
      <td>15</td>
      <td>NNTMRT08RV55</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CAGSNFO0027OTN1401</td>
      <td>6500-14</td>
      <td>10-13-1</td>
      <td>P10GSOEL</td>
      <td>WOTRANAKAC</td>
      <td>NTTP84BA</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>...</td>
      <td>Gestores-CIENA</td>
      <td>2019:10:26:13:32:46</td>
      <td>tx_ciena</td>
      <td>20191126</td>
      <td>insert</td>
      <td>2019</td>
      <td>7</td>
      <td>15</td>
      <td>FNSRMYUUF12F2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>CAGSNFO0027OTN1401</td>
      <td>6500-14</td>
      <td>10-13-2</td>
      <td>P10GSOEL</td>
      <td>WOTRCD2FAA</td>
      <td>NTTP84AA</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>...</td>
      <td>Gestores-CIENA</td>
      <td>2019:10:26:13:32:46</td>
      <td>tx_ciena</td>
      <td>20191126</td>
      <td>insert</td>
      <td>2019</td>
      <td>7</td>
      <td>15</td>
      <td>EXLGCN5713860683</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>CAGSNFO0027OTN1401</td>
      <td>6500-14</td>
      <td>10-13-3</td>
      <td>P10GSOEL</td>
      <td>WOTRANAKAC</td>
      <td>NTTP84BA</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>...</td>
      <td>Gestores-CIENA</td>
      <td>2019:10:26:13:32:46</td>
      <td>tx_ciena</td>
      <td>20191126</td>
      <td>insert</td>
      <td>2019</td>
      <td>7</td>
      <td>15</td>
      <td>FNSRMYUUF12EK</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 29 columns</p>
</div>



### Diccionario de datos.
A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

* **system_name**: Nombre del sistema.
* **ne_type**: Tipo de elemento de red.
* **component**: Nombre del componente.
* **component_subtype**: Tipo de componente.
* **clei_code**: Código único DEFINIR.
* **part_number**:Código número de parte.
* **manufacture_date**: Fecha de manufactura.
* **hardware_version**: Versión Hardware.
* **firmware_version**: Versión firmware.
* **software_version**: Versión Software.
* **operational_status**: Definición del negocio.
* **model_id**: Clave del modelo.
* **accuracy_date**: Definición del negocio.
* **wavelength**: Longitud de onda.
* **frequency**: Frecuencia de onda.
* **channel_number**: Definición del negocio.
* **serie**: Código de trazabilidad que da el proveedor.
* **serie_cleaned**: Campo agregado por la función Spark, es una bandera booleana que señala la consistencia de la serie.
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

### 2. Descripción de las fuentes.
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos=df.columns
print('Columnas de la fuente Ciena son: ',list(campos))
pd.DataFrame(df.dtypes,columns=['Tipo de objeto SOURCE'])
```

    ('Columnas de la fuente Ciena son: ', ['system_name', 'ne_type', 'component', 'component_subtype', 'clei_code', 'part_number', 'manufacture_date', 'hardware_version', 'firmware_version', 'software_version', 'operational_status', 'model_id', 'accuracy_date', 'wavelength', 'frequency', 'channel_number', 'filedate', 'filename', 'hash_id', 'sourceid', 'registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month', 'day', 'serie', 'serie_cleaned'])





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
      <th>system_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_type</th>
      <td>object</td>
    </tr>
    <tr>
      <th>component</th>
      <td>object</td>
    </tr>
    <tr>
      <th>component_subtype</th>
      <td>object</td>
    </tr>
    <tr>
      <th>clei_code</th>
      <td>object</td>
    </tr>
    <tr>
      <th>part_number</th>
      <td>object</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>object</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>firmware_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>object</td>
    </tr>
    <tr>
      <th>operational_status</th>
      <td>object</td>
    </tr>
    <tr>
      <th>model_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>accuracy_date</th>
      <td>object</td>
    </tr>
    <tr>
      <th>wavelength</th>
      <td>object</td>
    </tr>
    <tr>
      <th>frequency</th>
      <td>object</td>
    </tr>
    <tr>
      <th>channel_number</th>
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
      <th>serie</th>
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
print('renglones = ',df.shape[0],' columnas = ',df.shape[1])
```

    ('renglones = ', 3785, ' columnas = ', 29)



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
      <th>system_name</th>
      <th>ne_type</th>
      <th>component</th>
      <th>component_subtype</th>
      <th>clei_code</th>
      <th>part_number</th>
      <th>manufacture_date</th>
      <th>hardware_version</th>
      <th>firmware_version</th>
      <th>software_version</th>
      <th>operational_status</th>
      <th>model_id</th>
      <th>accuracy_date</th>
      <th>wavelength</th>
      <th>frequency</th>
      <th>channel_number</th>
      <th>serie</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>130</td>
      <td>4</td>
      <td>578</td>
      <td>26</td>
      <td>56</td>
      <td>54</td>
      <td>180</td>
      <td>14</td>
      <td>1</td>
      <td>5</td>
      <td>3</td>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>3775</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>CMDFMEX9226OTN3201</td>
      <td>6500-14</td>
      <td>1-PWR1</td>
      <td>P10GSOEL</td>
      <td>WOTRANAKAC</td>
      <td>NTTP84BA</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>IS</td>
      <td>--</td>
      <td>Current</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>--</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>115</td>
      <td>1781</td>
      <td>80</td>
      <td>932</td>
      <td>843</td>
      <td>843</td>
      <td>1475</td>
      <td>1485</td>
      <td>3785</td>
      <td>2362</td>
      <td>3782</td>
      <td>3785</td>
      <td>3769</td>
      <td>3785</td>
      <td>3785</td>
      <td>3785</td>
      <td>10</td>
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
      <td>0.002642</td>
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
      <td>0.051339</td>
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



#### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

* Sobre el campo colocado *serie_describe* podemos ver que la mayoría de registros del campo *serie* se encuentran en mal estado.
* Los nulos son registrados como "**--**". Habrá que darles formato de NaN.
* Se observo anteriormente en el head que el campo *component* los datos han tomado formato de fecha. Esto será marcado como data error.
* Según lo que se puede observar, serán explorados para propuesta de catálogos los campos: **ne_type, hardware_version, software_version** y **operational_status**.

#### Se proponen catálogos derivados de la fuente Ciena con los siguientes campos:
    
* **ne_type**: Tipo de elemento de red.
* **hardware_version**: Versión Hardware.
* **software_version**: Versión Software.
* **operational_status**: DESCRIPCIÓN NEGOCIO.

Estos catálogos nos ayudarán a mapear todos los diferentes proyectos que existen en los cuales hay un activo.


### 3. Exploración de los datos.
De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los catálogos.

#### Para empezar, se hará una limpieza general a los datos:


```python
df.replace('null',np.NaN,inplace=True)
df.replace('NA',np.NaN,inplace=True)
df.replace(u'--',np.NaN,inplace=True)
#Se puede hacer más y por columna en caso de ser necesario
```

### Primer catálogo: *ne_type*

Empezaremos con el catálogo de **ne_type**.   
Se harán charts para visualizar la distribución de las categorías. Este catálogo será llamado después en el apartado de catálogos. Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
ne_type=pd.DataFrame(df.ne_type.value_counts())

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
ne_type.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Tipo de elemento de red')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Distribución de los tipos de elementos de red')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
explode_list=[.2,0,0,.17] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue']

ne_type['ne_type'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Distribución de los tipos de elementos de red',y=1.12)
ax1.axis('equal')
ax1.legend(labels=ne_type.index,loc='upper left')

plt.show()
```


![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Ciena/image/output_35_0.png)


Parece que el campo ya viene bien homologado. No hace falta hacer limpieza.  
Podrá encontrarse el catálogo en la sección de catálogos.

#### Segundo catálogo: *hardware_version*

Se harán charts para visualizar la distribución de las categorías. Este catálogo será llamado después en el apartado de ***catálogos***.   
Nuestra intención por el momento es simplemente explorar los datos.


```python
#Revisamos frecuencias:
hardware_version=pd.DataFrame(df.hardware_version.value_counts())

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
hardware_version.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Versión de Hardware')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Distribución de las versiones de Hardware del elemento')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
explode_list=[.2,0,0,0,0,0,0,0,0,0,0,0,.17] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','firebrick',
            'plum','indianred','azure','chartreuse','aqua','fuchsia','orchid','hotpink']

hardware_version['hardware_version'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Distribución de las versiones de Hardware del elemento',y=1.12)
ax1.axis('equal')
ax1.legend(labels=hardware_version.index,loc='upper left')

plt.show()
```


![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Ciena/image/output_39_0.png)


Parece que es un campo limpio, sin embargo, podriamos inferir que deben existir muchas más versiones de Hardware. Por lo tanto, se considerará como un catálogo incompleto hasta el momento. Se podrá revisar en el apartado ***catálogos***.

#### Tercer catálogo: *software_version*


```python
#Revisamos frecuencias:
software_version=pd.DataFrame(df.software_version.value_counts())

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
software_version.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Versión de Hardware')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Distribución de las versiones de Software del elemento')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
explode_list=[.2,0,0,.17] #Cada entrada corresponde a un registro del catálogo

color_list=['plum','azure','chartreuse','aqua','fuchsia']

software_version['software_version'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Distribución de las versiones de Software del elemento',y=1.12)
ax1.axis('equal')
ax1.legend(labels=software_version.index,loc='upper left')

plt.show()
```


![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Ciena/image/output_42_0.png)


Observamos que también son registros limpios. El catálogo será colocado en la sección ***catálogos***.

#### Cuarto catálogo: *operational_status*


```python
#Revisamos frecuencias:
operational_status=pd.DataFrame(df.operational_status.value_counts())

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
operational_status.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'Estatus de operación')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Distribución de los estatus de operación')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
explode_list=[.2,0,.17] #Cada entrada corresponde a un registro del catálogo

color_list=['azure','chartreuse','fuchsia']

operational_status['operational_status'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Distribución de los estatus de operación',y=1.12)
ax1.axis('equal')
ax1.legend(labels=operational_status.index,loc='upper left')

plt.show()
```


![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Ciena/image/output_45_0.png)


Puede notarse la gran diferencia de frecuencia entre estos estatus. Siendo *IS* el estatus más sobresaliente.  
Debido a la distribución que tiene este campo, **no se hará un catálogo**. 

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
      <th>NNTMRT0DT5RK</th>
      <td>2</td>
    </tr>
    <tr>
      <th>FNSRMYUUF0GUS</th>
      <td>1</td>
    </tr>
    <tr>
      <th>FNSRMYUUE1BVA</th>
      <td>1</td>
    </tr>
    <tr>
      <th>NNTMRT0DTL20</th>
      <td>1</td>
    </tr>
    <tr>
      <th>NNTMRT0C8NGC</th>
      <td>1</td>
    </tr>
    <tr>
      <th>NNTMRT0LMR9N</th>
      <td>1</td>
    </tr>
    <tr>
      <th>NNTMRT0DE8PX</th>
      <td>1</td>
    </tr>
    <tr>
      <th>NNTMRT0DGYPX</th>
      <td>1</td>
    </tr>
    <tr>
      <th>NNTMRT0D01CP</th>
      <td>1</td>
    </tr>
    <tr>
      <th>NNTMRT0DTL29</th>
      <td>1</td>
    </tr>
    <tr>
      <th>NNTMRT0DD3T7</th>
      <td>1</td>
    </tr>
    <tr>
      <th>OPCP8771343</th>
      <td>1</td>
    </tr>
    <tr>
      <th>NNTMRT0DD3T5</th>
      <td>1</td>
    </tr>
    <tr>
      <th>OPCP8771341</th>
      <td>1</td>
    </tr>
    <tr>
      <th>NNTMRT0FEYK8</th>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



Podemos observar que el campo **serie** que usaremos para trazabilidad se enceuntra en buen estado.

### 4. Calidad de los datos
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
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_18))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```

![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Ciena/image/bokeh_plot.png)

  <div class="bk-root" id="d76932e6-432f-42bb-afd3-d8de90b59d16"></div>








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
      <th>ne_type</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>component</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>component_subtype</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>clei_code</th>
      <td>0.264201</td>
    </tr>
    <tr>
      <th>part_number</th>
      <td>1.532365</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>38.969617</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>39.233818</td>
    </tr>
    <tr>
      <th>firmware_version</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>62.404227</td>
    </tr>
    <tr>
      <th>operational_status</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>model_id</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>accuracy_date</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>wavelength</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>frequency</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>channel_number</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>0.264201</td>
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
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_18))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```

![png](https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/Gestor_Ciena/image/bokeh_plot(1).png)

  <div class="bk-root" id="0eaf4d90-c708-47e2-95a3-861ed30b1f85"></div>








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
      <th>ne_type</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>component</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>component_subtype</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>clei_code</th>
      <td>99.735799</td>
    </tr>
    <tr>
      <th>part_number</th>
      <td>98.467635</td>
    </tr>
    <tr>
      <th>manufacture_date</th>
      <td>61.030383</td>
    </tr>
    <tr>
      <th>hardware_version</th>
      <td>60.766182</td>
    </tr>
    <tr>
      <th>firmware_version</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>software_version</th>
      <td>37.595773</td>
    </tr>
    <tr>
      <th>operational_status</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>model_id</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>accuracy_date</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>wavelength</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>frequency</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>channel_number</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>99.735799</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



Parece que el campo **serie** se encuentra bastante saludable.   
Podemos ver que los campos **wavelength** y **frecuency**, entre otros varios, son completos nulos. No se podrá hacer ejercicio con variables continuas.

#### 4.2 Data Errors
* **component**: El campo trae muchos datos con formato de fecha, parece ser un problema desde fuente.


### 5. Catálogos.

#### Catálogo de Network Element Type (ne_type):


```python
Catalogo_ne_type=pd.DataFrame(df.ne_type.unique())
Catalogo_ne_type.columns=['ne_type']
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
      <th>0</th>
      <td>6500-14</td>
    </tr>
    <tr>
      <th>3</th>
      <td>6500-32</td>
    </tr>
    <tr>
      <th>2</th>
      <td>6500-7-PKTOTN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6500-7-TYPE2</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de Hardware version (hardware_version):


```python
Catalogo_hardware_version=pd.DataFrame(df.hardware_version.unique())
Catalogo_hardware_version.columns=['hardware_version']
Catalogo_hardware_version.dropna(inplace=True)
Catalogo_hardware_version.sort_values(by='hardware_version')
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
      <th>9</th>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>10</td>
    </tr>
    <tr>
      <th>10</th>
      <td>11</td>
    </tr>
    <tr>
      <th>12</th>
      <td>17</td>
    </tr>
    <tr>
      <th>13</th>
      <td>18</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2</td>
    </tr>
    <tr>
      <th>5</th>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>6</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7</td>
    </tr>
    <tr>
      <th>0</th>
      <td>8</td>
    </tr>
    <tr>
      <th>11</th>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo de Software version (software_version):


```python
software_version=pd.DataFrame(df.software_version.unique())
software_version.columns=['software_version']
software_version.dropna(inplace=True)
software_version
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
      <th>0</th>
      <td>REL1121Z.AW</td>
    </tr>
    <tr>
      <th>2</th>
      <td>REL1110Z.EY</td>
    </tr>
    <tr>
      <th>3</th>
      <td>REL1221Z.CI</td>
    </tr>
    <tr>
      <th>4</th>
      <td>REL1021Z.BC</td>
    </tr>
  </tbody>
</table>
</div>



### 6. Preparación de los datos.
Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos: 

* **De manera general (Aplicado a todos los campos)**: 
    * Se deben remplazar los registros **--** a nulos.
    * Se deberá revisar qué hacer con los campos que se encuentran nulos en su totalidad.
* **series:**
    * Homologar formatos en los casos posibles. 
    * Se marcan como *np.NaN* : campos que contengan:
        * ESPACIOS
        * La palabra BORRADO
        * La palabra VICIBLE
        * La palabra VISIBLE
        * CARACTER ESPECIAL
        * ILEGIBLE
        * INCOMPLETO
        * LONGITUD de caracteres menores a 6



### 7. Métricas KPI.
Se mostrarán los KPIs generados. 


```python
Total_Elementos=df.shape[0]
Total_Elementos
```




    3785




```python
df.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables


```python
Total_Tr=df.loc[(df.serie_cleaned==0)].shape[0]
Total_Tr
```




    3775



#### Total Elementos NO Trazables


```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    10



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=df['serie'].loc[(df.serie_cleaned!=1)].drop_duplicates().shape[0]
Total_Tr_Unic
```




    3774




```python
len(df['serie'].loc[(df.serie_cleaned!=1)].unique())
```




    3774



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    1




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
      <td>3785</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>3775</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>10</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>3774</td>
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
df.to_excel('Universo_Ciena.xlsx')
```


```python
sc.stop()
```
