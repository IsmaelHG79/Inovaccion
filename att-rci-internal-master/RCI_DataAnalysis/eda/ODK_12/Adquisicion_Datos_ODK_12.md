
# Adquisición de datos para ODK 12

## Sección para import's de `Python` y `Spark`


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
import pandasql

from pyspark.sql.functions import col, split, regexp_extract, array_contains, regexp_replace,concat_ws, create_map, create_map, lit
import pyspark.sql.functions as f
```

## Creando SparkContext


```python
conf = SparkConf().setAppName('Adquisicion_Datos_ODK_12')  \
    .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)
```

## Validación `ID_FORM`

```
select * from tx_stg_06_1_odk
WHERE id_form  = '99977'
ORDER BY element_group, element
```
Este `id_form` pertenece al *ODK 12 ATP Instalación MW*.

## Lectura de datos requeridos para el proceso

En este caso estamos leyendo la tabla `tx_stg_06_1_odk` la cual contiene la información agrupada y aplanada a nivel:
- id_form, clave del formulario `n->many`.
- clave_form, clave para relacionar con eñ catálogo de ODK's `n->many`
- element_group, elemento padre agrupador de la estructura del formulario, el cual es dinamico de acuerdo a la operación y concepto del ODK. 
- element, elemento hijo y corresponde `n->to one` element_group.
- value, lista de campos y  valores posibles para cada tipo de ODK.
- odk_no, número del odk.


```python
df_txodk01 = spark.read.table("tx_stg_06_1_odk")
```

Esquema de la tabla:


```python
df_txodk01.printSchema()
```

    root
     |-- id_form: string (nullable = true)
     |-- clave_form: string (nullable = true)
     |-- element_group: string (nullable = true)
     |-- element: string (nullable = true)
     |-- value: array (nullable = true)
     |    |-- element: string (containsNull = true)
     |-- odk_no: string (nullable = true)
    


# Filtrado para pruebas controladas, los siguientes escenarios se contemplan:

- filtrado de `id_form`, para identificar el tipo de documento a validar.
- filtrado de `clave_form`, para identificar el tipo de ODK's a validar.


```python
df_txodk02 = df_txodk01.filter(df_txodk01["odk_no"]=="0012").select("id_form","clave_form","odk_no","element_group","element","value").withColumn('value_str', concat_ws(',', 'value')).orderBy(df_txodk01["clave_form"])
```


```python
df_txodk02.printSchema()
```

    root
     |-- id_form: string (nullable = true)
     |-- clave_form: string (nullable = true)
     |-- odk_no: string (nullable = true)
     |-- element_group: string (nullable = true)
     |-- element: string (nullable = true)
     |-- value: array (nullable = true)
     |    |-- element: string (containsNull = true)
     |-- value_str: string (nullable = false)
    



```python
df_txodk02.count()
```




    45615



## Verificamos la estructura del documento, agrupando por:

- `element_group`, elemento padre agrupador de la estructura del formulario, el cual es dinámico de acuerdo a la operación y concepto del ODK.

Este comportamiento estará variando de acuerdo a al filtrado anterior el cual analizará la estructura de los ODK's dentro del alcance, que corresponde a:

1. `12`, Instalación
2. `32`, Instalación y comisionamiento. 
3. `38`, Decomiso. 
4. `76`, Salida de Almacen
5. `99`, Operaciones (Site Survey)

NOTA, la combinación de 12 & 32 es un caso para analizar como parte del EDA de ODK's.


```python
df_txodk02.orderBy("element_group").select("element_group").groupBy("element_group").count().show(150, truncate = False)
```

    +--------------------+-----+
    |element_group       |count|
    +--------------------+-----+
    |groupChTarjetas-0   |1    |
    |groupCommisioning-0 |3874 |
    |groupConfigTest-0   |5    |
    |groupFloorA-0       |3501 |
    |groupFloorB-0       |3501 |
    |groupHorizontalA-0  |3499 |
    |groupHorizontalB-0  |3501 |
    |groupInstallCON-0   |1    |
    |groupInstallHPS-0   |1    |
    |groupInstallPHO-0   |1    |
    |groupInstallTRA-0   |1    |
    |groupInventory-0    |1    |
    |groupMWData-0       |1    |
    |groupMWDataA-0      |3501 |
    |groupMWDataA-1      |469  |
    |groupMWDataB-0      |3501 |
    |groupMWDataB-1      |465  |
    |groupSideA-0        |4437 |
    |groupSideB-0        |4428 |
    |groupSiteInventory-0|1    |
    |groupTaskList-0     |13   |
    |groupTaskList-1     |4    |
    |groupTaskList-2     |4    |
    |groupTaskList-3     |4    |
    |groupTaskList-4     |4    |
    |groupTaskList-5     |4    |
    |groupTaskList-6     |2    |
    |groupTaskList-7     |1    |
    |groupVerticalA-0    |3500 |
    |groupVerticalB-0    |3499 |
    |root                |3890 |
    +--------------------+-----+
    


## Sección adicional de import de `pyspark` para manejo de colecciones (DF), búsqueda y mapeo de datos principales correspondientes a cada ODK

__IMPORTANTE__: ES REQUERIDO validar esta estrategia para optimizar el performance y la obtención ordenada de cada expr por ODK. La propuesta es manejar un `DF` por cada set de reglas de mapeo de datos por ODK, por lo cual debemos generar dataframes Base para cada tipo de ODK y trabajarlo por separado, después hacer merge de los DF's. 


```python
from pyspark.sql.types import ArrayType, StructType, StructField, IntegerType
from pyspark.sql.functions import col, udf, explode, expr, flatten
from pyspark.sql import functions as F
```

## Primer `approach`: Estructura unificada tipo `k/v`

#### Las ventajas pueden ser las siguientes:
- Separando los dataframes por cada set de campos a identificar, esto permite crear más `expr` para obtener los campos que sean requeridos en un futuro.
- Se considera una estructura estándar unificada por campo.

#### Mejoras identificadas:
- El DF base contiene todo el universo de datos (todos los conjuntos de elementos y grupos para todos los ODK's), evaluamos el comportamiento y determinamos si hacemos `split` por ODK.

#### Casos de prueba:


| id_form |  element_group     |     element        | no_odk |           value                     |    tipo   |
|:-------:|:------------------:|:------------------:|:------:|:------------------------------------|:---------:|
| 99977   | groupFloorA-0      | groupFloorA-0      | 12     | Número de serie (manual)            | UNICO     |
| 99977   | groupFloorA-0      | groupFloorA-0      | 12     | Número de serie (escáner)           | UNICO     |
| 99977   | groupFloorA-0      | groupFloorA-0      | 12     | Número de activo fijo (escáner)     | UNICO     |
| 99977   | groupFloorA-0      | groupFloorA-0      | 12     | Número de activo fijo (scanner)     | UNICO     |
| 99977   | groupFloorA-0      | groupFloorA-0      | 12     | Número de activo fijo (manual)      | UNICO     |
| 99977   | groupFloorA-0      | groupFloorA-0      | 12     | Modelo                              | UNICO     |
| 99977   | groupFloorA-0      | groupFloorA-0      | 12     | Modelo de IDU                       | UNICO     |
| 99977   | groupFloorA-0      | groupFloorA-0      | 12     | Fabricante                          | UNICO     |
| 99977   | groupFloorA-0      | groupFloorA-0      | 12     | Fabricante / Modelo IDU             | UNICO     |
| 99977   | groupFloorB-0      | groupFloorB-0      | 12     | Número de serie (manual)            | UNICO     | 
| 99977   | groupFloorB-0      | groupFloorB-0      | 12     | Número de serie (escáner)           | UNICO     |
| 99977   | groupFloorB-0      | groupFloorB-0      | 12     | Número de activo fijo (escáner)     | UNICO     |
| 99977   | groupFloorA-0      | groupFloorB-0      | 12     | Número de activo fijo (scanner)     | UNICO     |
| 99977   | groupFloorB-0      | groupFloorB-0      | 12     | Número de activo fijo (manual)      | UNICO     |
| 99977   | groupFloorB-0      | groupFloorB-0      | 12     | Modelo                              | UNICO     |
| 99977   | groupFloorB-0      | groupFloorB-0      | 12     | Modelo de IDU                       | UNICO     |
| 99977   | groupFloorB-0      | groupFloorB-0      | 12     | Fabricante                          | UNICO     |
| 99977   | groupFloorB-0      | groupFloorB-0      | 12     | Fabricante / Modelo IDU             | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | Número de serie (manual)            | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | Número de serie (escáner)           | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | Número de activo fijo (escáner)     | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | Número de activo fijo (manual)      | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | Modelo                              | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | Modelo de ODU                       | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | Fabricante                          | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | Fabricante / Modelo ODU             | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | Modelo de la antena de MW           | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | Fabricante / Modelo de antena de MW | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | Número de serie (manual)            | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | Número de serie (escáner)           | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | Número de activo fijo (escáner)     | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | Número de activo fijo (manual)      | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | Modelo                              | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | Modelo de ODU                       | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | Fabricante                          | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | Fabricante / Modelo ODU             | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | Modelo de la antena de MW           | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | Fabricante / Modelo de antena de MW | UNICO     |
| 99977   | groupHorizontalA-0 | groupHorizontalA-0 | 12     | Barra de Tierra                     | UNICO     |
| 99977   | groupHorizontalB-0 | groupHorizontalB-0 | 12     | Barra de Tierra                     | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | Atizador                            | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | Atizador                            | UNICO     |
| 99977   | groupMWDataA-0     | groupMWDataA-0     | 12     | PTR                                 | UNICO     |
| 99977   | groupMWDataB-0     | groupMWDataB-0     | 12     | PTR                                 | UNICO     |
| 99977   | groupVerticalA-0   | groupVerticalA-0   | 12     | Barra de Tierra en Torre            | UNICO     |
| 99977   | groupVerticalB-0   | groupVerticalB-0   | 12     | Barra de Tierra en Torre            | UNICO     |
| 99977   | groupVerticalA-0   | groupVerticalA-0   | 12     | Segunda Barra de Tierra en Torre    | UNICO     |
| 99977   | groupVerticalB-0   | groupVerticalB-0   | 12     | Segunda Barra de Tierra en Torre    | UNICO     |

## Seccion definicíon de Reglas de parseo de variables

Empezamos con las cargas de los campos de root

Proseguimos con los campos del element *id:root:groupFloorA-0*


```python
user_func = udf (lambda x,y: [[t, x[t+1]] for t in xrange(len(x)) if x[t]==y])
```


```python
df_txodk03_1 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorA") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de serie (manual)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_1 = df_txodk03_1.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")


```


```python

df_txodk03_2 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorA") \
.filter(df_txodk02["element_group"] == "groupFloorA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de serie (escáner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_2 = df_txodk03_2.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")


```


```python

df_txodk03_3 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorA") \
.filter(df_txodk02["element_group"] == "groupFloorA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (escáner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (escáner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_3 = df_txodk03_3.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_4 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorA") \
.filter(df_txodk02["element_group"] == "groupFloorA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (scanner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (scanner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (scanner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_4 = df_txodk03_4.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_5 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorA") \
.filter(df_txodk02["element_group"] == "groupFloorA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (manual)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (manual)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_5 = df_txodk03_5.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_6 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorA") \
.filter(df_txodk02["element_group"] == "groupFloorA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Modelo')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_6 = df_txodk03_6.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_7 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorA") \
.filter(df_txodk02["element_group"] == "groupFloorA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo de IDU')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo de IDU')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Modelo de IDU')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_7 = df_txodk03_7.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_8 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorA") \
.filter(df_txodk02["element_group"] == "groupFloorA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Fabricante')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Fabricante')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Fabricante')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_8 = df_txodk03_8.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_9 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorA") \
.filter(df_txodk02["element_group"] == "groupFloorA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Fabricante / Modelo IDU')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Fabricante / Modelo IDU')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Fabricante / Modelo IDU')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_9 = df_txodk03_9.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```

Cargamos los campos del grupo *id:root:groupFloorB-0*


```python

df_txodk03_10 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorB") \
.filter(df_txodk02["element_group"] == "groupFloorB-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de serie (manual)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_10 = df_txodk03_10.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_11 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorB") \
.filter(df_txodk02["element_group"] == "groupFloorB-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de serie (escáner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_11 = df_txodk03_11.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_12 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorB") \
.filter(df_txodk02["element_group"] == "groupFloorB-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (escáner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (escáner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_12 = df_txodk03_12.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_13 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (scanner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (scanner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (scanner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_13 = df_txodk03_13.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_14 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorB") \
.filter(df_txodk02["element_group"] == "groupFloorB-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (manual)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (manual)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_14 = df_txodk03_14.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_15 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorB") \
.filter(df_txodk02["element_group"] == "groupFloorB-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Modelo')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_15 = df_txodk03_15.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_16 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorB") \
.filter(df_txodk02["element_group"] == "groupFloorB-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo de IDU')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo de IDU')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Modelo de IDU')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_16 = df_txodk03_16.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_17 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorB") \
.filter(df_txodk02["element_group"] == "groupFloorB-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Fabricante')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Fabricante')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Fabricante')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_17 = df_txodk03_17.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_18 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupFloorB") \
.filter(df_txodk02["element_group"] == "groupFloorB-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Fabricante / Modelo IDU')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Fabricante / Modelo IDU')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Fabricante / Modelo IDU')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_18 = df_txodk03_18.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```

Luego, cargamos los campos para *id:root:groupMWDataA-0*


```python

df_txodk03_19 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.filter(df_txodk02["element_group"] == "groupMWDataA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de serie (manual)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_19 = df_txodk03_19.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_20 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.filter(df_txodk02["element_group"] == "groupMWDataA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de serie (escáner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_20 = df_txodk03_20.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_21 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.filter(df_txodk02["element_group"] == "groupMWDataA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (escáner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (escáner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_21 = df_txodk03_21.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_22 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (scanner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (scanner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (scanner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_22 = df_txodk03_22.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_23 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.filter(df_txodk02["element_group"] == "groupMWDataA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (manual)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (manual)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_23 = df_txodk03_23.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

<<<<<<< HEAD
df_txodk03_24 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
=======
df_txodk03_26 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0]== "groupMWDataA") \
.filter(df_txodk02["element_group"] == "groupMWDataA-0") \
>>>>>>> 17a03a79429caa675c9d571e6d500ed09315de82
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Modelo')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_24 = df_txodk03_24.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_25 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.filter(df_txodk02["element_group"] == "groupMWDataA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo de ODU')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo de ODU')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Modelo de ODU')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_25 = df_txodk03_25.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_26 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.filter(df_txodk02["element_group"] == "groupMWDataA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Fabricante')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Fabricante')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Fabricante')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_26 = df_txodk03_26.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_27 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Fabricante / Modelo ODU')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Fabricante / Modelo ODU')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Fabricante / Modelo ODU')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_27 = df_txodk03_27.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_28 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.filter(df_txodk02["element_group"] == "groupMWDataA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo de la antena de MW')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo de la antena de MW')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Modelo de la antena de MW')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_28 = df_txodk03_28.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_29 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.filter(df_txodk02["element_group"] == "groupMWDataA-0") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Fabricante / Modelo de antena de MW')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Fabricante / Modelo de antena de MW')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Fabricante / Modelo de antena de MW')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_29 = df_txodk03_29.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```

Agregamos los campos de groupMWDataB-0


```python

df_txodk03_30 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de serie (manual)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_30 = df_txodk03_30.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_31 = df_txodk02 \
<<<<<<< HEAD
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de serie (escáner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_31 = df_txodk03_31.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_32 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (escáner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (escáner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_32 = df_txodk03_32.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_33 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (scanner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (scanner)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (scanner)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_33 = df_txodk03_33.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_34 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (manual)')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Número de activo fijo (manual)')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_34 = df_txodk03_34.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_35 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Modelo')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_35 = df_txodk03_35.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_36 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo de ODU')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo de ODU')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Modelo de ODU')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_36 = df_txodk03_36.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_37 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Fabricante')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Fabricante')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Fabricante')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_37 = df_txodk03_37.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_38 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Fabricante / Modelo ODU')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Fabricante / Modelo ODU')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Fabricante / Modelo ODU')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_38 = df_txodk03_38.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_39 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo de la antena de MW')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo de la antena de MW')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Modelo de la antena de MW')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_39 = df_txodk03_39.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_40 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
=======
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.filter(df_txodk02["element_group"] == "groupMWDataA-0") \
>>>>>>> 17a03a79429caa675c9d571e6d500ed09315de82
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Fabricante / Modelo de antena de MW')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Fabricante / Modelo de antena de MW')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Fabricante / Modelo de antena de MW')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_40 = df_txodk03_40.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```

Cargamos los campos extras que corresponden a los elementos **No Trazables** para los KPIs que son: PTR, Barra de Tierra, Barra de Tierra en Torre, Segunda Barra de Tierra en Torre, Atizador.


```python

df_txodk03_41 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Atizador')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Atizador')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Atizador')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_41 = df_txodk03_41.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")


```


```python

df_txodk03_42 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Atizador')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Atizador')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Atizador')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_42 = df_txodk03_42.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_43 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataA") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'PTR')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'PTR')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('PTR')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_43 = df_txodk03_43.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_44 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupMWDataB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'PTR')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'PTR')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('PTR')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_44 = df_txodk03_44.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")


```


```python

df_txodk03_45 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupHorizontalA") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Barra de Tierra')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Barra de Tierra')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Barra de Tierra')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_45 = df_txodk03_45.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_46 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupHorizontalB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Barra de Tierra')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Barra de Tierra')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Barra de Tierra')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_46 = df_txodk03_46.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_47 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupVerticalA") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Barra de Tierra en Torre')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Barra de Tierra en Torre')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Barra de Tierra en Torre')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_47 = df_txodk03_47.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_48 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupVerticalB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Barra de Tierra en Torre')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Barra de Tierra en Torre')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Barra de Tierra en Torre')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_48 = df_txodk03_48.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_49 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupVerticalA") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Segunda Barra de Tierra en Torre')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Segunda Barra de Tierra en Torre')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Segunda Barra de Tierra en Torre')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_49 = df_txodk03_49.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")

```


```python

df_txodk03_50 = df_txodk02 \
.filter(split(df_txodk02["element_group"],"-")[0] == "groupVerticalB") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Segunda Barra de Tierra en Torre')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Segunda Barra de Tierra en Torre')")) \
.withColumn("TipoElemento_tup", f.split(user_func(df_txodk02["value"],lit('Segunda Barra de Tierra en Torre')),",")) \
.withColumn("TipoElemento_str", concat_ws(',','TipoElemento_tup')) \
.withColumn("TipoElemento_value", f.split(regexp_replace(regexp_replace('TipoElemento_str',"\\[+\d+,",""),"\\]",""),","))

df_txodk03_50 = df_txodk03_50.select("id_form","clave_form","element_group","element","value","exist","TipoElemento_key","TipoElemento_value")
```

## TERMINA Sección definición de reglas de parseo de variables


```python
# import modules
from functools import reduce
from pyspark.sql import DataFrame
# create list of dataframes
dfs = [df_txodk03_1, \
       df_txodk03_2, \
       df_txodk03_3, \
       df_txodk03_4, \
       df_txodk03_5, \
       df_txodk03_6, \
       df_txodk03_7, \
       df_txodk03_8, \
       df_txodk03_9, \
       df_txodk03_10, \
       df_txodk03_11, \
       df_txodk03_12, \
       df_txodk03_13, \
       df_txodk03_14, \
       df_txodk03_15, \
       df_txodk03_16, \
       df_txodk03_17, \
       df_txodk03_18, \
       df_txodk03_19, \
       df_txodk03_20, \
       df_txodk03_21, \
       df_txodk03_22, \
       df_txodk03_23, \
       df_txodk03_24, \
       df_txodk03_25, \
       df_txodk03_26, \
       df_txodk03_27, \
       df_txodk03_28, \
       df_txodk03_29, \
       df_txodk03_30, \
       df_txodk03_31, \
       df_txodk03_32, \
       df_txodk03_33, \
       df_txodk03_34, \
       df_txodk03_35, \
       df_txodk03_36, \
       df_txodk03_37, \
       df_txodk03_38, \
       df_txodk03_39, \
       df_txodk03_40, \
       df_txodk03_41, \
       df_txodk03_42, \
       df_txodk03_43, \
       df_txodk03_44, \
       df_txodk03_45, \
       df_txodk03_46, \
       df_txodk03_47, \
       df_txodk03_48, \
       df_txodk03_49]

# create merged dataframe
df_txodk04 = reduce(DataFrame.unionAll, dfs)
```


```python
df_txodk05 = df_txodk04.select("id_form","clave_form","element_group","element","exist",df_txodk04["TipoElemento_key"].alias("TipoElemento_key"),"TipoElemento_value")
```


```python
#df_txodk05.filter(df_txodk05['exist'] == "true").show(50,truncate = False)
```


```python
df = df_txodk05.withColumn("new", F.arrays_zip("TipoElemento_key", "TipoElemento_value"))\
       .withColumn("new", F.explode("new"))\
       .select("id_form","clave_form","element_group", "element","exist", F.col("new.TipoElemento_key").alias("TipoElemento_key"), F.col("new.TipoElemento_value").alias("TipoElemento_value"))
```


```python
df_txodk06 = df.filter(df['exist'] == "true")
```


```python
df
```




    DataFrame[id_form: string, clave_form: string, element_group: string, element: string, exist: boolean, TipoElemento_key: string, TipoElemento_value: string]




```python
df_txodk06.show(100,truncate = False)
```

<<<<<<< HEAD
    +-------+----------+-------------+-------------+-----+------------------------+---------------------------------+
    |id_form|clave_form|element_group|element      |exist|TipoElemento_key        |TipoElemento_value               |
    +-------+----------+-------------+-------------+-----+------------------------+---------------------------------+
    |101464 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| S/N                             |
    |104069 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130815                          |
    |104250 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021136216TGB900302            |
    |91295  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 0                               |
    |97170  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| F305T00916                      |
    |97949  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021113821N0F9002150           |
    |99418  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44342                           |
    |113894 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021138216GB900407             |
    |97936  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021207626TG3901613            |
    |101649 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021138216TFA901771            |
    |105016 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44663                           |
    |106118 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 13001                           |
    |90560  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 2102113821N0F9001995 Y SLFB1CASE|
    |94436  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| F316R01714                      |
    |103151 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130488                          |
    |106304 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44650                           |
    |112131 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021138216TGB900998            |
    |113570 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130098                          |
    |91304  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E216B04736                      |
    |91515  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 09152612                        |
    |91732  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130773                          |
    |101772 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130990                          |
    |103996 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| F345200076                      |
    |106379 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44750                           |
    |108907 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| F246E00808                      |
    |95355  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 45121                           |
    |96858  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44878                           |
    |106985 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 117182                          |
    |111477 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E356R04283                      |
    |98079  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| F435O01262                      |
    |103561 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130903                          |
    |104079 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 117126                          |
    |92870  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44712                           |
    |96574  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 34520                           |
    |101637 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E346D07434                      |
    |109854 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130916                          |
    |110633 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| NO VISIBLE                      |
    |96047  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 2102113821N0F8002411            |
    |105008 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| No visible                      |
    |107079 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021138216TGB8900957           |
    |91770  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 210107384N0G3000470             |
    |93485  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44520                           |
    |98419  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E275102071                      |
    |101342 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 1234456                         |
    |93436  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E226004049                      |
    |96290  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130487                          |
    |92223  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E116608129                      |
    |95238  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021138216FT8905208            |
    |95361  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| F435401751                      |
    |99532  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 20016-06                        |
    |101407 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021138216TF8903274            |
    |107083 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E275J02200                      |
    |95452  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 2102113821N0FA001645            |
    |96911  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 2102111746TD6903868             |
    |98744  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130627                          |
    |104462 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44889                           |
    |106157 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44623                           |
    |94393  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44527                           |
    |101075 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| F295T02450                      |
    |96012  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E216604707                      |
    |96573  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 34520                           |
    |99413  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| F325N03151                      |
    |111472 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 129904                          |
    |115798 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130478                          |
    |99054  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E356U04430                      |
    |103251 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130908                          |
    |105079 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 2102120762N0F9000970            |
    |108599 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130825                          |
    |98907  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| F455T02316                      |
    |99215  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130348                          |
    |99674  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130463                          |
    |103649 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| F106H01503                      |
    |91618  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E346J07408                      |
    |99405  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130658                          |
    |99701  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130369                          |
    |105336 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021138216TF8903381            |
    |105943 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130670                          |
    |108272 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021138216TF8905341            |
    |99698  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| F116D04426                      |
    |105799 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| N/A                             |
    |105913 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| NA                              |
    |95718  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| No Visible                      |
    |108171 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 2102113821P0EBOO2188            |
    |92612  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44437                           |
    |100016 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130339                          |
    |103747 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130321                          |
    |108450 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130758                          |
    |92196  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E226T04227                      |
    |98432  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130759                          |
    |99717  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 44681                           |
    |106311 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E346207277                      |
    |97793  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| No aplica                       |
    |93457  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130690                          |
    |105305 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| E346O07526                      |
    |107055 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130345                          |
    |98574  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 21021131746TD5901369            |
    |105036 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130018                          |
    |93461  |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130690                          |
    |103954 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| 130603                          |
    |106622 |ATPMW     |groupFloorA-0|groupFloorA-0|true |Número de serie (manual)| N/V                             |
    +-------+----------+-------------+-------------+-----+------------------------+---------------------------------+
=======
    +-------+----------+-------------+-------+-----+----------------------+--------------------------+
    |id_form|clave_form|element_group|element|exist|TipoElemento_key      |TipoElemento_value        |
    +-------+----------+-------------+-------+-----+----------------------+--------------------------+
    |149029 |WITX2     |root         |root   |true |Código de Sitio       |BCS1063                   |
    |145898 |WITX2     |root         |root   |true |Código de Sitio       |YUCMER-7369               |
    |197353 |WITX2     |root         |root   |true |Código de Sitio       |DIFIZC9238                |
    |157641 |WITX2     |root         |root   |true |Código de Sitio       |MEXHUA0291                |
    |143229 |WITX2     |root         |root   |true |Código de Sitio       |MEXSMP0599                |
    |197351 |WITX2     |root         |root   |true |Código de Sitio       |DIFIZC9243                |
    |149762 |WITX2     |root         |root   |true |Código de Sitio       |CHHJRZ1772  PANFILO NATERA|
    |146455 |WITX2     |root         |root   |true |Código de Sitio       |PALACIO NACIONAL          |
    |160395 |WITX2     |root         |root   |true |Código de Sitio       |CHPPIJ0083                |
    |156366 |WITX2     |root         |root   |true |Código de Sitio       |MEXSMP0600                |
    |149144 |WITX2     |root         |root   |true |Código de Sitio       |CHHRJRZ1767 KATAHDIN      |
    |151834 |WITX2     |root         |root   |true |Código de Sitio       |CHHJRZ1768.   MESA CENTRAL|
    |172768 |WITX2     |root         |root   |true |Código de Sitio       |HMEX0589                  |
    |148948 |WITX2     |root         |root   |true |Código de Sitio       |NLEGAL1429                |
    |172768 |WITX2     |root         |root   |true |Código de Sitio       |HMEX0589                  |
    |148948 |WITX2     |root         |root   |true |Código de Sitio       |NLEGAL1429                |
    |197351 |WITX2     |root         |root   |true |Código de Sitio       |DIFIZC9243                |
    |149762 |WITX2     |root         |root   |true |Código de Sitio       |CHHJRZ1772  PANFILO NATERA|
    |160395 |WITX2     |root         |root   |true |Código de Sitio       |CHPPIJ0083                |
    |156366 |WITX2     |root         |root   |true |Código de Sitio       |MEXSMP0600                |
    |149144 |WITX2     |root         |root   |true |Código de Sitio       |CHHRJRZ1767 KATAHDIN      |
    |146455 |WITX2     |root         |root   |true |Código de Sitio       |PALACIO NACIONAL          |
    |151834 |WITX2     |root         |root   |true |Código de Sitio       |CHHJRZ1768.   MESA CENTRAL|
    |157641 |WITX2     |root         |root   |true |Código de Sitio       |MEXHUA0291                |
    |143229 |WITX2     |root         |root   |true |Código de Sitio       |MEXSMP0599                |
    |105053 |ATPMW     |root         |root   |true |Código de Sitio Lado B|HSLT0056                  |
    |105354 |ATPMW     |root         |root   |true |Código de Sitio Lado B|HPUEZG1405                |
    |12199  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HSAL0012                  |
    |17206  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMEX0264                  |
    |30695  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HNLD0060                  |
    |38922  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HVIC0015                  |
    |39786  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HIZU0001                  |
    |52331  |ATPMW     |root         |root   |true |Código de Sitio Lado B|RTOL0001                  |
    |59815  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |65562  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HDOH0003                  |
    |82538  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |84006  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HREY0012                  |
    |90560  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMOR10002                 |
    |93564  |ATPMW     |root         |root   |true |Código de Sitio Lado B|ATT-HID-9058              |
    |94434  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HID-9031D Xicotepec       |
    |99623  |ATPMW     |root         |root   |true |Código de Sitio Lado B|iMEX0026                  |
    |101151 |ATPMW     |root         |root   |true |Código de Sitio Lado B|MEX-9040                  |
    |101383 |ATPMW     |root         |root   |true |Código de Sitio Lado B|PUEHZG0189 XALMIMILULCO   |
    |106237 |ATPMW     |root         |root   |true |Código de Sitio Lado B|DIFCHT9147                |
    |110008 |ATPMW     |root         |root   |true |Código de Sitio Lado B|HIDTZY1488                |
    |18599  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |29716  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HJRZ0047                  |
    |30704  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HJRZ0058                  |
    |31676  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HJRZ0049                  |
    |36001  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HNOG0009                  |
    |39365  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HSLP0028                  |
    |41491  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HCAM0011                  |
    |61870  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMTY1010                  |
    |66612  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |67793  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |72589  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HGMS0009                  |
    |72928  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMEX0163                  |
    |76209  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HQRO0039                  |
    |93024  |ATPMW     |root         |root   |true |Código de Sitio Lado B|TOL-9023                  |
    |96574  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HID-9060 TLAMIMILOLPA     |
    |106185 |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMEX0526                  |
    |106954 |ATPMW     |root         |root   |true |Código de Sitio Lado B|PUEATX0742                |
    |11389  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HSLP0011                  |
    |13547  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |13928  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HGTO0001                  |
    |38327  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMOR0028                  |
    |39808  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HDOH0001                  |
    |42233  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |52211  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HPDC0005                  |
    |61317  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |66507  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |68240  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HPAR0003                  |
    |69594  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |7108   |ATPMW     |root         |root   |true |Código de Sitio Lado B|HGDL0009                  |
    |72183  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |77096  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |8406   |ATPMW     |root         |root   |true |Código de Sitio Lado B|HTOL0035                  |
    |94951  |ATPMW     |root         |root   |true |Código de Sitio Lado B|MEXNIC1157                |
    |103561 |ATPMW     |root         |root   |true |Código de Sitio Lado B|QTOCRR2114                |
    |108599 |ATPMW     |root         |root   |true |Código de Sitio Lado B|ATT-MEX-127               |
    |11872  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HQRO0026                  |
    |14926  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HGDL0053                  |
    |20209  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMEX0238                  |
    |29296  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HJRZ0069                  |
    |30673  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMER0008                  |
    |36002  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HNOG0009                  |
    |37892  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HGDL0005                  |
    |41355  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMAZ0018                  |
    |43800  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HLEO0101                  |
    |43963  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HPUE0093                  |
    |45350  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HNLD0074                  |
    |6795   |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMEX0589                  |
    |91515  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMEX1041                  |
    |96290  |ATPMW     |root         |root   |true |Código de Sitio Lado B|ATT-GUASMA3326            |
    |99079  |ATPMW     |root         |root   |true |Código de Sitio Lado B|ROOSOL1154                |
    |102493 |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMEX-0426                 |
    |103444 |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMEX-1117                 |
    |104306 |ATPMW     |root         |root   |true |Código de Sitio Lado B|MICAPZ2972                |
    |105389 |ATPMW     |root         |root   |true |Código de Sitio Lado B|COAFRO1906                |
    |110633 |ATPMW     |root         |root   |true |Código de Sitio Lado B|HIDFIM1425                |
    |110889 |ATPMW     |root         |root   |true |Código de Sitio Lado B|NLECDJ1410                |
    |15721  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMER0012                  |
    |18284  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMEX0380                  |
    |18615  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMEX0793                  |
    |20007  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |29493  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HJRZ0048                  |
    |30300  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HJRZ0069                  |
    |31517  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HGSV0004                  |
    |34300  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HXXX0000                  |
    |35693  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HSLT0038                  |
    |36362  |ATPMW     |root         |root   |true |Código de Sitio Lado B|HMTY0044                  |
    +-------+----------+-------------+-------+-----+----------------------+--------------------------+
>>>>>>> 17a03a79429caa675c9d571e6d500ed09315de82
    only showing top 100 rows
    


## Persistiendo los valores en el formato:


- `df`, formato basado en rows `tabular`

Cargamos el dataframe en una tabla hive


```python
df_txodk06.write.format("parquet").mode("Overwrite").saveAsTable("default.tx_stg_06_tabular_odk_12")
```


```python
sc.stop()
```


```python

```
