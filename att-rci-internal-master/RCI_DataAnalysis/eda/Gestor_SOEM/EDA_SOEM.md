
![Encabezado](image/encabezado.png)

# Exploratory Data Analysis

## Descripción

Analizaremos los datos del gestor SOEM con un tratamiento estadístico descriptivo para hacer el tracking del ciclo de vida de los elementos de red. 

Se creará un EDA enfocado a las tres fuentes proporcionadas por SOEM, las cuales están identificadas como **hw**, **ne** y **sw**. 

Serán documentados los catálogos propuestos junto a su respectivo tratamiento de datos. 

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
conf = SparkConf().setAppName('EDA_SOEM')  \
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
from bokeh.palettes import Category20_11, Category20c_9, Category10_5,Category10_6, Category20_20, Plasma256
output_notebook()
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="14300267-9f52-4b9e-a714-0e267567f6fe">Loading BokehJS ...</span>
    </div>




### Recolección de los datos: 

Para analizar el gestor SOEM en conjunto, se realiza una unión de las fuentes (hw, ne y sw) para trabajar con el universo completo de SOEM.

La tabla que se utiliza como fuente es ```tx_soem_hw``` ya que aquí encontramos el número de serie, el cual utilizaremos para rastrear el ciclo de vida del elemento.

Los campos por los cuales se unen son los siguientes: ```tx_soem_hw.ne_id = tx_soem_ne.id```  y ```tx_soem_sw.hw_module_id = tx_soem_hw.id ```


Los datos con los que se trabajan a lo largo del EDA corresponden a la partición de **20191031** de las tablas ```default.tx_soem_hw```, ```default.tx_soem_ne``` y ```default.tx_soem_sw```.

*IMPORTANTE*: Si se requieren ver datos de otro periódo, se debe cambiar los filtros ```year = <año-a-ejecutar>```, ```month = <mes-a-ejecutar>```, ```day = <día-a-ejecutar>``` de las tablas en la siguiente celda:


```python
df_location = spark.sql("SELECT * FROM inventario.raw_panda_location").toPandas()
```


```python
df_load = spark.sql("SELECT a.id as id_hw, a.serialnumber as serie, a.ne_id as ne_id, b.address, b.nename as ne_name, b.location as location_id, c.typeofswunit, c.swproductnumber FROM tx_soem_hw a LEFT JOIN tx_soem_ne b on trim(a.ne_id) = trim(b.id) LEFT JOIN tx_soem_sw c on trim(c.hw_module_id) = trim(a.id) WHERE a.year = 2019 and a.month = 10 and a.day = 31 and b.year = 2019 and b.month = 10 and b.day = 31 and c.year = 2019 and c.month = 10 and c.day = 31").cache()
```

Creamos una funcion para el tratamiento de datos en spark el cual contiene la reglas proporcionadas por la tabla ```inventario.cat_regex_cleanup``` para la columna serie:


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

Se crea un udf en spark sobre la funcion ya creada.


```python
validate_rule_udf = udf(validate_rule, IntegerType())
```

Se le agrega una nueva columna al dataframe de spark; la nueva columna es la validacion de la columna serie con respecto al udf que creamos.


```python
df_serie = df_load.withColumn("serie_cleaned",validate_rule_udf(col("serie"))).cache()
```

Se convierte el dataframe de spark a un dataframe de pandas.


```python
df = df_serie.toPandas()
```

Hemos recolectado los campos a analizar de las fuentes *hw* y *ne* correspondientes a SOEM.

Muestra de los datos recolectados:


```python
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_hw</th>
      <th>serie</th>
      <th>ne_id</th>
      <th>address</th>
      <th>ne_name</th>
      <th>location_id</th>
      <th>typeofswunit</th>
      <th>swproductnumber</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>16796_1_B</td>
      <td>TY12747513</td>
      <td>16796</td>
      <td>10.245.150.70</td>
      <td>MXSLPSLP1516MW03</td>
      <td>SANTA ROSA</td>
      <td>AMM 6p D</td>
      <td>CXP9010021_1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>16838_1/7_N</td>
      <td>A23108DNHX</td>
      <td>16838</td>
      <td>10.245.178.83</td>
      <td>MXGROCHB0071MW07</td>
      <td>ALQUITRAN</td>
      <td>NPU3 C</td>
      <td>CXP 901 2516/5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>16846_1/3_M</td>
      <td>A23105LLJW</td>
      <td>16846</td>
      <td>10.245.148.80</td>
      <td>MXQTOMQS1324MW02</td>
      <td>AEROPUERTO QUERETARO</td>
      <td>MMU2 H</td>
      <td>CXP 901 1133/6</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>17066_1030_1.1</td>
      <td>CR9N285902</td>
      <td>17066</td>
      <td>10.245.248.20</td>
      <td>MORCVA0193</td>
      <td>CUERNAVACA</td>
      <td>network release</td>
      <td>CXP9026371_3_R12B51_2-11.def</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>16734_1/8_E</td>
      <td>A23109EXPR</td>
      <td>16734</td>
      <td>10.245.145.199</td>
      <td>MXGUASIL0500MW01</td>
      <td>ADUANA [LA ESPERANZA]</td>
      <td>ETU3</td>
      <td>CXCR 102 051/1</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



### Diccionario de datos

A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  

Fuente HW:

* **nodename**: nombre del nodo o fuente
* **id**: id único del registro
* **ammposition**: por definir
* **assetid**: por definir
* **typeofunit**: por definir
* **productnumber**: número del producto
* **version**: por definir
* **serialnumber**: número de serie
* **productiondate**: por definir
* **elapsedruntime**: por definir
* **ne_id**: id que se utiliza para hacer la unión con SOEM ne
* **nealias**: por definir
* **notes**: por definir
* **updatedate**: por definir
* **moduleproductnumber**: por definir
* **moduleserialnumber**: por definir
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

Fuente NE:

* **nodename**: nombre del nodo o fuente
* **id**: id único del registro
* **type**: por definir
* **address**: por definir
* **nename**: por definir
* **location**: código de ubicación
* **information**: por definir
* **site_id**: número de serie
* **nealias**: por definir
* **nenotes**: por definir
* **updatedate**: por definir
* **neaddedtime**: por definir
* **nelastmanagedtime**: por definir
* **nelaststartedtime**: por definir
* **nelastmodifiedtime**: por definir
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

Fuente SW:

* **nodename**: nombre del nodo o fuente
* **id**: id único del registro
* **minimumswversion**: por definir
* **typeofswunit**: por definir
* **swproductnumber**: por definir
* **activesw**: por definir
* **passivesw**: por definir
* **hw_module_id**: id único para unir con hw
* **nealias**: por definir
* **updatedate**: por definir

### 2. Descripción de las fuentes
En este apartado se hará una descripción a detalle de el dataframe para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
campos=df.columns
print('Columnas de la fuente SOEM son: ',list(campos))
pd.DataFrame(df.dtypes,columns=['Tipo de objeto SOEM'])
```

    ('Columnas de la fuente SOEM son: ', ['id_hw', 'serie', 'ne_id', 'address', 'ne_name', 'location_id', 'typeofswunit', 'swproductnumber', 'serie_cleaned'])





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Tipo de objeto SOEM</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>id_hw</th>
      <td>object</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>address</th>
      <td>object</td>
    </tr>
    <tr>
      <th>ne_name</th>
      <td>object</td>
    </tr>
    <tr>
      <th>location_id</th>
      <td>object</td>
    </tr>
    <tr>
      <th>typeofswunit</th>
      <td>object</td>
    </tr>
    <tr>
      <th>swproductnumber</th>
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

    ('renglones = ', 1318, ' columnas = ', 9)



```python
df.describe(include='all')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_hw</th>
      <th>serie</th>
      <th>ne_id</th>
      <th>address</th>
      <th>ne_name</th>
      <th>location_id</th>
      <th>typeofswunit</th>
      <th>swproductnumber</th>
      <th>serie_cleaned</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1318</td>
      <td>1286</td>
      <td>1318</td>
      <td>1318</td>
      <td>1318</td>
      <td>1318</td>
      <td>1318</td>
      <td>1286</td>
      <td>1318.000000</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>1318</td>
      <td>1250</td>
      <td>192</td>
      <td>192</td>
      <td>187</td>
      <td>134</td>
      <td>20</td>
      <td>13</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>top</th>
      <td>17032_1/3.1_R</td>
      <td>CR9N280625</td>
      <td>5664</td>
      <td>10.245.225.2</td>
      <td>MXHID9002MW05</td>
      <td>TEXCOCO</td>
      <td>MMU2 H</td>
      <td>CXP 901 2878</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>1</td>
      <td>2</td>
      <td>18</td>
      <td>18</td>
      <td>18</td>
      <td>54</td>
      <td>328</td>
      <td>371</td>
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
      <td>0.000759</td>
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
      <td>0.027545</td>
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
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>



De la tabla podemos observar que el total de elementos que existen para la fuente son *1,318* registros.

* **números de serie únicos**: 1,251
* **números de serie duplicados**: 67

#### Se proponen catálogos derivados de la fuente SOEM con los siguientes campos:
    
* **ne_name**: Código del sitio.
* **location_id**: Identificador del sitio.  

Estos catálogos nos ayudarán a complementar el catálogo ```inventario.raw_panda_location``` y a homologar los nombres y códigos que se tienen de los sitios y location.


### 3. Exploración de los datos.
De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas.

#### Para empezar, se hará una limpieza general a los datos:


```python
df.replace('null',np.NaN,inplace=True)
df.replace('NA',np.NaN,inplace=True)
df.replace('UNKNOWN',np.NaN,inplace=True)
```

### Catálogo Location

Empezaremos con el catálogo de **location_id**. Se hará una revisión de frecuencias de datos y se mostrará en  diferentes tipos de gráficas para su visualización. Este catálogo será llamado después en el apartado de catálogos, nuestra intención por el momento es simplemente explorar los datos.


```python
location_id=pd.DataFrame(df.location_id.value_counts()[:10])
```


```python
#Revisamos frecuencias:
location=pd.DataFrame(df.location_id.value_counts()[:10])

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
location.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'location_id')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Frecuencia de Locations')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
explode_list=[0,0,0,0,0,0,0,0,0,0] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue']

location['location_id'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Frecuencia de Locations',y=1.12)
ax1.axis('equal')
ax1.legend(labels=location.index,loc='upper left')

plt.show()
```


![Grafica1](image/Grafica1.png)


Podemos observar que el locatio con mas frecuencia es Texcoco con un **21.4%** de frecuencia en la fuente.

#### Visualización de los datos de trazabilidad: 


```python
pd.DataFrame(df.serie.value_counts()[:15])
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>serie</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>CR9N280625</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9N285918</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9M954394</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9M935934</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9P377329</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9K968705</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9N280632</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9N026545</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9N157637</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9L847073</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9M935936</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9M729732</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9N280469</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9P377335</th>
      <td>2</td>
    </tr>
    <tr>
      <th>CR9P548015</th>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



#### Es de interés haber observado los datos que se usaran para la trazabilidad, NOTAS OBSERVABLES. 
* Activo: no hay en la fuente de SOEM un campo activo.
* Serie: existen números de serie duplicados y vacíos.

### 4. Calidad de los datos
Se documentará la calidad de los datos y analizará las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

### Missings Values
Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.


```python
nas=df.isna().sum()
porcentaje_nas=nas/df.isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_9))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])
```








  <div class="bk-root" id="dfb35563-4630-4b86-8110-395a7db3f579"></div>








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
      <th>id_hw</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>2.427921</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>address</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>ne_name</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>location_id</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>typeofswunit</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>swproductnumber</th>
      <td>2.427921</td>
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
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_9))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])
```








  <div class="bk-root" id="40fd5de4-2d9c-4dcd-8351-e59816beddd7"></div>








<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Porcentaje de Not nulls</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>id_hw</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>97.572079</td>
    </tr>
    <tr>
      <th>ne_id</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>address</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>ne_name</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>location_id</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>typeofswunit</th>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>swproductnumber</th>
      <td>97.572079</td>
    </tr>
    <tr>
      <th>serie_cleaned</th>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



El campo de serie el cual ocupamos para la trazabilidad de elementos, tiene un **2.42%** de nulos y de los cueles perdemos la trazabilidad en este gestor.

### 5. Catálogos.

#### Catálogo location_id

A continuación se muestra el catálogo limpio para los location y sus ne names.


```python
Catalogo_location = pandasql.sqldf("WITH cat_ne as( SELECT CASE WHEN bandera_limpieza = 1 THEN substr(ne_name, instr(ne_name, 'MX')+2, instr(ne_name, 'MW')-3) WHEN bandera_limpieza = 2 THEN substr(ne_name, 1, instr(ne_name, '_')-1) ELSE ne_name END ne_name, location_id FROM( SELECT DISTINCT ne_name, CASE WHEN ne_name LIKE 'MX%MW%' THEN 1 WHEN ne_name LIKE '%\\_%' THEN 2 ELSE 0 END bandera_limpieza, location_id FROM df)a), cat_location as (SELECT DISTINCT latitude, longitude, location_attid FROM df_location WHERE location_attid IS NOT NULL) SELECT location_id, ne_name, latitude, longitude FROM cat_ne LEFT JOIN cat_location ON trim(ne_name) = trim(location_attid)", locals())
Catalogo_location.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>location_id</th>
      <th>ne_name</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SANTA ROSA</td>
      <td>SLPSLP1516</td>
      <td>22.191422</td>
      <td>-100.999888</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ALQUITRAN</td>
      <td>GROCHB0071</td>
      <td>17.395645</td>
      <td>-99.519063</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AEROPUERTO QUERETARO</td>
      <td>QTOMQS1324</td>
      <td>20.602450</td>
      <td>-100.202870</td>
    </tr>
    <tr>
      <th>3</th>
      <td>CUERNAVACA</td>
      <td>MORCVA0193</td>
      <td>18.890000</td>
      <td>-99.221056</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ADUANA [LA ESPERANZA]</td>
      <td>GUASIL0500</td>
      <td>21.008472</td>
      <td>-101.517250</td>
    </tr>
  </tbody>
</table>
</div>



Este mismo catálogo lo podemos observar en un mapa usando las latitudes y longitudes obtenidas  del catálogo **raw_panda_invenatrio**.


```python
mapa_location=Catalogo_location.loc[:,['location_id','latitude','longitude']].dropna()
mapa_location.drop_duplicates(inplace=True)
```


```python
import folium
from folium import plugins

Latitud=21.607871
Longitud=-101.201933
mapa=folium.Map(location=[Latitud,Longitud],zoom_start=4.8)

storages = folium.map.FeatureGroup()

for lat, lng, in zip(mapa_location.latitude, mapa_location.longitude):
    storages.add_child(
        folium.features.Marker(
            [lat, lng]
        )
    )
    
latitudes = list(mapa_location.latitude)
longitudes = list(mapa_location.longitude)
labels = list(mapa_location.location_id)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(storages) 
mapa.save('Mapa de Locations en Gestor SOEM.html')
mapa.add_child(storages)
```


![MapaLocation](image/mapaLocation.png)



### 6. Preparación de los datos.
Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos: 

* **location_id**: quitar nomenclaturas MX y MW para obtener el código que se encuentra dentro de la cadena.
* Para todos los campos se recomienda transformarlas a mayúsculas.

### 7. Métricas KPI.
Se mostrarán los KPIs generados. 


```python
Total_Elementos=df.shape[0]
Total_Elementos
```




    1318




```python
df.replace(np.NaN,'vacio',inplace=True)
```

#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=df[['serie']].loc[(df.serie!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic
```




    1250



#### Total de elementos duplicados


```python
Total_Tr_Dupli=Total_Elementos-Total_Tr_Unic
Total_Tr_Dupli
```




    68



De este gestor solo se pueden tomar los indicadores total de elementos, total de elementos únicos por serie y total de elementos duplicados, los otros KPI's no se pueden calcular ya que la fuente no cuenta con número de activo.


```python
Total_Tr = 0
Total_NOTr = 0
Total_Tr_Unic_CS_CA = 0
Total_Tr_Unic_CS_SA = 0
Total_Tr_Unic_SS_CA = 0
```


```python
KPIs=pd.DataFrame({'KPI':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Unicos',
                         'Total Duplicados',
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
      <td>1318</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Unicos</td>
      <td>1250</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Duplicados</td>
      <td>68</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Total CS CA</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Total CS SA</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Total SS CA</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
sc.stop()
```
