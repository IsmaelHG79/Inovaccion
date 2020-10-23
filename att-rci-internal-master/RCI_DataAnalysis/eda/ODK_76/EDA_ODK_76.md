
<div style="width: 100%; clear: both; font-family: Verdana;">
<div style="float: left; width: 50%;font-family: Verdana;">
<img src="https://github.com/javierOrtaAxity/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/ODK_76/image/encabezado.png" align="left">
</div>
<div style="float: right; width: 200%;">
<p style="margin: 0; padding-top: 20px; text-align:right;color:rgb(193, 38, 184)"><strong>Axity - AT&T.
    Ciclo de vida de elementos de inventario</strong></p>
</div>
</div>
<div style="width:100%;">&nbsp;</div>

# Exploratory Data Analysis


## Descripción

Analizaremos los datos de la fuente **ODK 12** que corresponde a los elementos que se encuentran en instalación de AT&T con un tratamiento estadístico descriptivo para la exploración, explotación y descubrimiento de los datos para un correcto tracking del ciclo de vida de los elementos de red. 

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
import pandasql
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
        <span id="232dfe4c-5f1d-450d-b73f-3ed155afede0">Loading BokehJS ...</span>
    </div>




## 1. ODK 76
### 1. Recolección de los datos: 

Se crea el dataframe de spark con el universo de datos crudos.


```python
df_load = spark.sql("SELECT * FROM default.tx_stg_06_tabular_odk_76").cache().toPandas()
```

Para las fuentes de los ODK's nos interesa conocer todos los elementos en sitio, por lo que haremos una limpieza en los campos que contengan características de los mismos. Creamos una funcion para el tratamiento del campo de sitio en spark el cual contiene ciertas reglas definidas para su limpieza.

Una muestra del ODK 76


```python
df_load.head()
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
      <th>id_form</th>
      <th>clave_form</th>
      <th>element_group</th>
      <th>element</th>
      <th>exist</th>
      <th>TipoElemento_key</th>
      <th>TipoElemento_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>179490</td>
      <td>ALMCN</td>
      <td>groupPedMovimiento-108</td>
      <td>groupPedMovimiento-108</td>
      <td>True</td>
      <td>Codigo de sitio destino.</td>
      <td>MEX-9221</td>
    </tr>
    <tr>
      <th>1</th>
      <td>179490</td>
      <td>ALMCN</td>
      <td>groupPedMovimiento-14</td>
      <td>groupPedMovimiento-14</td>
      <td>True</td>
      <td>Codigo de sitio destino.</td>
      <td>MEX-502H</td>
    </tr>
    <tr>
      <th>2</th>
      <td>179490</td>
      <td>ALMCN</td>
      <td>groupPedMovimiento-107</td>
      <td>groupPedMovimiento-107</td>
      <td>True</td>
      <td>Pedido de Movimiento</td>
      <td>63512719</td>
    </tr>
    <tr>
      <th>3</th>
      <td>179490</td>
      <td>ALMCN</td>
      <td>groupPedMovimiento-115</td>
      <td>groupPedMovimiento-115</td>
      <td>True</td>
      <td>Pedido de Movimiento</td>
      <td>63512811</td>
    </tr>
    <tr>
      <th>4</th>
      <td>179490</td>
      <td>ALMCN</td>
      <td>groupPedMovimiento-125</td>
      <td>groupPedMovimiento-125</td>
      <td>True</td>
      <td>Pedido de Movimiento</td>
      <td>63499475</td>
    </tr>
  </tbody>
</table>
</div>



### 2. Descripción de las fuentes.
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos=df_load.columns
print 'Columnas de la fuente SOURCE son: ',list(campos)
pd.DataFrame(df_load.dtypes,columns=['Tipo de objeto SOURCE'])
```

    Columnas de la fuente SOURCE son:  ['id_form', 'clave_form', 'element_group', 'element', 'exist', 'TipoElemento_key', 'TipoElemento_value']





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
      <th>id_form</th>
      <td>object</td>
    </tr>
    <tr>
      <th>clave_form</th>
      <td>object</td>
    </tr>
    <tr>
      <th>element_group</th>
      <td>object</td>
    </tr>
    <tr>
      <th>element</th>
      <td>object</td>
    </tr>
    <tr>
      <th>exist</th>
      <td>bool</td>
    </tr>
    <tr>
      <th>TipoElemento_key</th>
      <td>object</td>
    </tr>
    <tr>
      <th>TipoElemento_value</th>
      <td>object</td>
    </tr>
  </tbody>
</table>
</div>



Con la transformación que se llevo a cabo previamente, los campos **id_form, clave_form, element_group, element, exist** sirven para tener un control y mejor manejo del odk. Los campos **TipoElemento_key y TipoElemento_value** son los que se utilizarán para sacar indicadores.

A continuación se muestran los datos únicos en el campo **TipoElemento_Key**


```python
df_load.TipoElemento_key.groupby(df_load['TipoElemento_key']).count()

```




    TipoElemento_key
    Codigo de sitio destino.    144
    Pedido de Movimiento        144
    QR                          144
    TS Finalización               1
    Name: TipoElemento_key, dtype: int64



Para el cálculo de indicadores que se va a realizar mas adelante, nos vamos a enfocar en el campo QR.


```python
dfSerie2 =  df_load.TipoElemento_value.loc[(df_load.TipoElemento_key == 'QR')]
```


```python
dfSerie2.describe(include='all')
```




    count                        144
    unique                       144
    top       MEX6349895361050752EMB
    freq                           1
    Name: TipoElemento_value, dtype: object



Podemos observar que en la tabla tenemos el total del número de serie con el **count**, los campos únicos con **unique** y el valor que más se repite con el **top** y cuántas veces se retipe con el **freq**.

Podemos observar lo siguiente para los campos que contienen número de serie:

* Existen **144** registros con **QR**.
* **144** elementos con **QR** son únicos.
* El registro con **NMEX6349895361050752EMB** tiene una freuencia.

### Tamaño de la fuente


```python
print('rows = ',df_load.shape[0],' columnas = ',df_load.shape[1])
```

    ('rows = ', 577, ' columnas = ', 7)


### 3. Exploración de los datos.

Se puede hace exploración de los datos para la fuente.


```python
#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes=[v for v in df_load.columns if v not in NOrelevantes]

df_load[relevantes].describe(include='all')
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
      <th>id_form</th>
      <th>clave_form</th>
      <th>element_group</th>
      <th>element</th>
      <th>exist</th>
      <th>TipoElemento_key</th>
      <th>TipoElemento_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>577</td>
      <td>577</td>
      <td>577</td>
      <td>577</td>
      <td>577</td>
      <td>433</td>
      <td>577</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>1</td>
      <td>1</td>
      <td>145</td>
      <td>146</td>
      <td>1</td>
      <td>4</td>
      <td>433</td>
    </tr>
    <tr>
      <th>top</th>
      <td>179490</td>
      <td>ALMCN</td>
      <td>groupPedMovimiento-42</td>
      <td>groupPallet-0</td>
      <td>True</td>
      <td>Codigo de sitio destino.</td>
      <td>NA</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>577</td>
      <td>577</td>
      <td>4</td>
      <td>288</td>
      <td>577</td>
      <td>144</td>
      <td>144</td>
    </tr>
  </tbody>
</table>
</div>



### 4. Calidad de los datos
En el parseo de nuestra fuente de ODK se creo el campo de *exist* que corresponde a la limpieza de los atributos que se encuentran en el formulario, con esto eliminando missing values.

### 5. Catalogos
Para estas fuentes no se encontraron catálogos.


### 6. Preparación de los datos


Se realiza una limpieza, es decir se remplazan los valores **NULL**,** **,**NA**, como **vacio**


```python
df_load.replace(np.NaN,'vacio',inplace=True)
df_load.replace("NA",'vacio',inplace=True)
df_load.replace("NA",'vacio',inplace=True)
df_load.replace("null",'vacio',inplace=True)
df_load.replace("NULL",'vacio',inplace=True)

#pd.Series(['foo', 'fuz', np.nan]).str.replace('f.', np.NaN, regex=True,inplace=True)
```

### 7. Metricas KPI

Se mostrarán los KPIs generados. Se va a considerar el QR para hacer lo conteos ya que no tiene numero de serie.

#### Total de QR


```python
Total_Elementos=df_load.loc[(df_load.TipoElemento_key=='QR') ].shape[0]
Total_Elementos
```




    144



#### Total Elementos Trazables
Como no hay numero de serie, como tal no hay elementos trazables y solo son conteos.

#### Total Elementos NO Trazables
Igual como no existe trazabilidad, no se puede definir algun elemento trazable.

#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=df_load.TipoElemento_value.loc[(df_load.TipoElemento_key=='QR') & (df_load.TipoElemento_value!='vacio') ].drop_duplicates().shape[0]
Total_Tr_Unic
```




    144



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli=Total_Tr_Unic
Total_Tr_Dupli
```




    144



### Otros KPIS

En este apartado se muestra algunos de los hayazgos vistos en la exploración.


```python
#Ajustar el df contra los kpis de la siguiente tabla:

KPIs=pd.DataFrame({'KPI':['Total Elementos'
                         ,'Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos,
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
      <td>144</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Trazables Unicos</td>
      <td>144</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total Trazables Duplicados</td>
      <td>144</td>
    </tr>
  </tbody>
</table>
</div>




```python
#df_hive_kpi = spark.createDataFrame(KPIs)

```


```python
#df_hive_kpi.write.mode("overwrite").saveAsTable("default.kpi_odk_76")
```


```python
#sc.stop()
```
