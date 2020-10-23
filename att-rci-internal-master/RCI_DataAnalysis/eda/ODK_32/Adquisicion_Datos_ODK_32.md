
![Encabezado](image/encabezado.png)

# Adquisición de datos para ODK 32

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
conf = SparkConf().setAppName('Adquisicion_Datos_ODK_32')  \
    .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)
```

## Validación `ODK 32`

```
select * from tx_stg_06_a_1_odk
WHERE odk_no  = '0032'
ORDER BY element_group, element
```

## Lectura de datos requeridos para el proceso

En este caso estamos leyendo la tabla `tx_stg_06_1_odk` la cual contiene la información agrupada y aplanada a nivel:
- id_form, clave del formulario `n->many`.
- clave_form, clave para relacionar con el catálogo de ODK's `n->many`
- element_group, elemento padre agrupador de la estructura del formulario, el cual es dinámico de acuerdo a la operación y concepto del ODK. 
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
df_txodk02 = df_txodk01.filter(df_txodk01["odk_no"]=="0032").select("id_form","clave_form","odk_no","element_group","element","value").withColumn('value_str', concat_ws(',', 'value')).orderBy(df_txodk01["clave_form"])
```


```python
df_txodk02.count()
```




    258335




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
    


## Verificamos la estructura del documento, agrupando por:

- `element_group`, elemento padre agrupador de la estructura del formulario, el cual es dinámico de acuerdo a la operación y concepto del ODK.

Este comportamiento estará variando de acuerdo a al filtrado anterior el cual analizará la estructura de los ODK's dentro del alcance, que corresponde a:

1. `12`, Instalación
2. `32`, Instalación y comisionamiento. 
3. `38`, Decomiso. 
4. `76`, Salida de Almacén
5. `99`, Operaciones (Site Survey)

NOTA, la combinación de 12 & 32 es un caso para analizar como parte del EDA de ODK's.


```python
df_txodk02.orderBy("element_group").select("element_group").groupBy("element_group").count().show(150, truncate = False)
```

    +---------------+-----+
    |element_group  |count|
    +---------------+-----+
    |groupAzimuts-0 |7214 |
    |groupAzimuts-1 |7097 |
    |groupAzimuts-10|1    |
    |groupAzimuts-2 |6760 |
    |groupAzimuts-3 |228  |
    |groupAzimuts-4 |193  |
    |groupAzimuts-5 |91   |
    |groupAzimuts-6 |3    |
    |groupAzimuts-7 |3    |
    |groupAzimuts-8 |3    |
    |groupAzimuts-9 |1    |
    |groupBattery-0 |2    |
    |groupBattery-1 |1    |
    |groupBbus-0    |44430|
    |groupBbus-1    |42626|
    |groupBbus-2    |7    |
    |groupCabinet-0 |5101 |
    |groupCabinet-1 |2494 |
    |groupCabinet-2 |8    |
    |groupCabinet-3 |3    |
    |groupCabinet-4 |2    |
    |groupCabinet-5 |1    |
    |groupCabinet-6 |1    |
    |groupComm-0    |3554 |
    |groupInv-0     |2    |
    |groupInv-1     |2    |
    |groupInv-10    |1    |
    |groupInv-11    |1    |
    |groupInv-12    |1    |
    |groupInv-13    |1    |
    |groupInv-14    |1    |
    |groupInv-15    |1    |
    |groupInv-2     |2    |
    |groupInv-3     |2    |
    |groupInv-4     |2    |
    |groupInv-5     |2    |
    |groupInv-6     |2    |
    |groupInv-7     |2    |
    |groupInv-8     |2    |
    |groupInv-9     |2    |
    |groupNodeb-0   |2    |
    |groupPaths-0   |7214 |
    |groupSectors-0 |40353|
    |groupSectors-1 |39602|
    |groupSectors-10|1    |
    |groupSectors-2 |37876|
    |groupSectors-3 |852  |
    |groupSectors-4 |725  |
    |groupSectors-5 |331  |
    |groupSectors-6 |9    |
    |groupSectors-7 |9    |
    |groupSectors-8 |7    |
    |groupSectors-9 |1    |
    |groupShelter-0 |4243 |
    |groupShelter-1 |34   |
    |groupTaskList-0|4    |
    |groupTaskList-1|4    |
    |root           |7218 |
    +---------------+-----+
    



```python
#df_txodk02.filter(df['element_group'] == "groupShelter-0").show(150, truncate = False)
```

## Sección adicional de import de `pyspark` para manejo de colecciones (DF) y búsqueda y mapeo de datos pricipales correspondientes a cada ODK

__IMPORTANTE__: ES REQUERIDO validar esta estrategia para optimizar el performance y la obtención ordenada de cada expr por ODK. La propuesta es manejar un `DF` por cada set de reglas de mapeo de datos por ODK, por lo cual debemos generar Data Frames Base para cada tipo de ODK y trabajarlo por separado, después hacer merge de los DF's. 


```python
from pyspark.sql.types import ArrayType, StructType, StructField, IntegerType
from pyspark.sql.functions import col, udf, explode, expr, flatten
from pyspark.sql import functions as F
```

## Primer `approach`: Estructura unificada tipo `k/v`

#### Las ventajas pueden ser las siguientes:
- Separando los DataFrames por cada set de campos a identificar, esto permite crear mas `expr` para obtener los campos que sean requeridos en un futuro.
- Se considera una estructura estándar unificada por campo.

#### Mejoras identificadas:
- El DF base contiene todo el universo de datos (todos los conjuntos de elementos y grupos para todos los ODK's), evaluamos el comprotamiento y determinamos si hacemos `split` por ODK.

#### casos de prueba:

Campos para ODK32 identificados son (podrían existir mas):

|  element_group |     element    | no_odk |              value               |    tipo   |
|:--------------:|:--------------:|:------:|:--------------------------------:|:---------:|
| root           | root           | 32     | Código de Sitio                  | ÚNICO     |
| root           | root           | 32     | Tipo de Instalación              | ÚNICO     |
| root           | root           | 32     | TS Finalización                  | ÚNICO     |
| groupBbus      | groupBbus      | 32     | Serie BBU (M)                    | ÚNICO     |
| groupBbus      | groupCards     | 32     | Modelo Tarjeta                   | ÚNICO     |
| groupBbus      | groupCards     | 32     | Número de Serie (Manual)         | ÚNICO     |
| groupBbus      | groupCards     | 32     | Numero de Serie (Escanner)       | ÚNICO     |
| groupCabinet   | groupCabinet   | 32     | Modelo de Gabinete               | ÚNICO     |
| groupCabinet   | groupCabinet   | 32     | Tipo de Gabinete                 | ÚNICO     |
| groupSectors   | groupAntenas   | 32     | Marca y Modelo Antena RF         | ÚNICO     |
| groupSectors   | groupAntenas   | 32     | Modelo Antenna RF                | ÚNICO     |
| groupSectors   | groupAntenas   | 32     | Número de Serie (Manual)         | ÚNICO     |
| groupSectors   | groupRrus      | 32     | Número de activo fijo (manual)   | ÚNICO     |
| groupSectors   | groupRrus      | 32     | Número de Serie (Manual)         | ÚNICO     |
| groupSectors   | groupRrus      | 32     | RRU                              | ÚNICO     |
| groupSectors   | groupAntenas   | 32     | Número de Serie (Escanner)       | ÚNICO     |
| groupSectors   | groupAntenas   | 32     | Número de activo fijo (Escanner) | ÚNICO     |
| groupSectors   | groupAntenas   | 32     | Etiqueta RCU RET                 | ÚNICO     |
| groupSectors   | groupAntenas   | 32     | Etiqueta RCU RET 2 (Si aplica)   | ÚNICO     |
| groupShelter   | groupShelter   | 32     | SHELTER                          | ÚNICO     |
| groupShelter   | groupRack      | 32     | RACK                             | ÚNICO     |

## Sección de Reglas de parseo de variables

### Root: Código de Sitio


```python
df_txodk03_root_cs = df_txodk02 \
.filter(df_txodk02["element_group"] == "root") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Código de Sitio')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Código de Sitio')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Código de Sitio')")], ","))
```

### Root: Tipo de Instalación


```python
df_txodk03_root_tdi = df_txodk02 \
.filter(df_txodk02["element_group"] == "root") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Tipo de Instalación')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Tipo de Instalación')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Tipo de Instalación')")], ","))
```

### Root: TS Finalización


```python
df_txodk03_root_tsf = df_txodk02 \
.filter(df_txodk02["element_group"] == "root") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'TS Finalización')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'TS Finalización')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'TS Finalización')")], ","))
```

### groupBbus: Serie BBU (M)


```python
df_txodk03_groupBbus_sbbu = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupBbus") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Serie BBU (M)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Serie BBU (M)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Serie BBU (M)')")], ","))
```

### groupBbus: Modelo Tarjeta


```python
df_txodk03_groupBbus_mt = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupBbus") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo Tarjeta')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo Tarjeta')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Modelo Tarjeta')")], ","))
```

### groupBbus: Número de Serie (Manual)


```python
df_txodk03_groupBbus_nsM = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupBbus") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de Serie (Manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de Serie (Manual)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de Serie (Manual)')")], ","))
```

### groupBbus: Número de Serie (Escanner)


```python
df_txodk03_groupBbus_nsE = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupBbus") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Numero de Serie (Escanner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Numero de Serie (Escanner)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Numero de Serie (Escanner)')")], ","))
```

### groupCabinet: Modelo de Gabinete


```python
df_txodk03_groupCabinet_mg = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupCabinet") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo de Gabinete')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo de Gabinete')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Modelo de Gabinete')")], ","))
```

### groupCabinet: Tipo de Gabinete


```python
df_txodk03_groupCabinet_tg = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupCabinet") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Tipo de Gabinete')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Tipo de Gabinete')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Tipo de Gabinete')")], ","))
```

### groupSectors: Marca y Modelo Antena RF


```python
df_txodk03_groupSectors_mymARF = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Marca y Modelo Antena RF')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Marca y Modelo Antena RF')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Marca y Modelo Antena RF')")], ","))
```

### groupSectors: Modelo Antenna RF


```python
df_txodk03_groupSectors_mARF = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo Antenna RF')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo Antenna RF')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Modelo Antenna RF')")], ","))
```

### groupSectors: Número de Serie (Manual)


```python
df_txodk03_groupSectors_nsM = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de Serie (Manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de Serie (Manual)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de Serie (Manual)')")], ","))
```

### groupSectors: Número de serie (manual)


```python
df_txodk03_groupSectors_nsm = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de serie (manual)')")], ","))
```

### groupSectors: Número de Serie (Escanner)


```python
df_txodk03_groupSectors_nsE = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Numero de Serie (Escanner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Numero de Serie (Escanner)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Numero de Serie (Escanner)')")], ","))
```

### groupSectors: Número de activo fijo (manual)


```python
df_txodk03_groupSectors_nAFM = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo fijo (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (manual)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de activo fijo (manual)')")], ","))
```

### groupSectors: Número de activo fijo (Escanner)


```python
df_txodk03_groupSectors_nAFE = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Numero de activo fijo (Escanner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo fijo (Escanner)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de activo fijo (Escanner)')")], ","))
```

### groupSectors: Etiqueta RCU RET


```python
df_txodk03_groupSectors_rcu = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Etiqueta RCU RET')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Etiqueta RCU RET')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Etiqueta RCU RET')")], ","))
```

### groupSectors: Etiqueta RCU RET 2 (Si aplica)


```python
df_txodk03_groupSectors_rcu2 = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Etiqueta RCU RET 2 (Si aplica)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Etiqueta RCU RET 2 (Si aplica)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Etiqueta RCU RET 2 (Si aplica)')")], ","))
```

### groupSectors: RRU 01


```python
df_txodk03_groupSectors_rru01 = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'RRU 01')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'RRU 01')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'RRU 01')")], ","))
```

### groupSectors: RRU 02


```python
df_txodk03_groupSectors_rru02 = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'RRU 02')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'RRU 02')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'RRU 02')")], ","))
```

### groupSectors: RRU 03


```python
df_txodk03_groupSectors_rru03 = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSectors") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'RRU 03')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'RRU 03')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'RRU 03')")], ","))
```

### groupSectors: SHELTER 01


```python
df_txodk03_groupShelter_sh01 = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupShelter") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'SHELTER 01')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'SHELTER 01')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'SHELTER 01')")], ","))
```

### groupSectors: SHELTER 02


```python
df_txodk03_groupShelter_sh02 = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupShelter") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'SHELTER 02')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'SHELTER 02')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'SHELTER 02')")], ","))
```

### groupSectors: RACK 01


```python
df_txodk03_groupShelter_rack01 = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupShelter") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'RACK 01')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'RACK 01')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'RACK 01')")], ","))
```

### groupSectors: RACK 02


```python
df_txodk03_groupShelter_rack02 = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupShelter") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'RACK 02')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'RACK 02')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'RACK 02')")], ","))
```

## Reglas de parseo de variables


```python
# import modules
from functools import reduce
from pyspark.sql import DataFrame
# create list of dataframes
dfs = [df_txodk03_root_cs, \
       df_txodk03_root_tdi, \
       df_txodk03_root_tsf, \
       df_txodk03_groupBbus_mt, \
       df_txodk03_groupBbus_nsM, \
       df_txodk03_groupBbus_sbbu, \
       df_txodk03_groupCabinet_mg, \
       df_txodk03_groupCabinet_tg, \
       df_txodk03_groupSectors_mARF, \
       df_txodk03_groupSectors_mymARF, \
       df_txodk03_groupSectors_nAFM, \
       df_txodk03_groupSectors_nsM, \
       df_txodk03_groupSectors_rru02, \
       df_txodk03_groupBbus_nsE, \
       df_txodk03_groupSectors_nsE, \
       df_txodk03_groupSectors_nAFE, \
       df_txodk03_groupSectors_rcu, \
       df_txodk03_groupSectors_rcu2, \
       df_txodk03_groupSectors_rru01, \
       df_txodk03_groupSectors_rru03, \
       df_txodk03_groupShelter_sh01, \
       df_txodk03_groupShelter_rack01, \
       df_txodk03_groupShelter_sh02, \
       df_txodk03_groupShelter_rack02, \
       df_txodk03_groupSectors_nsm
       ]
# create merged dataframe
df_txodk04 = reduce(DataFrame.unionAll, dfs)
```


```python
df_txodk05 = df_txodk04.select("id_form","clave_form","element_group","element","exist",df_txodk04["TipoElemento_key"].alias("TipoElemento_key"),"TipoElemento_value")
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
df_txodk06.show(20)
```

    +-------+----------+-------------+-------+-----+----------------+--------------------+
    |id_form|clave_form|element_group|element|exist|TipoElemento_key|  TipoElemento_value|
    +-------+----------+-------------+-------+-----+----------------+--------------------+
    |  29274|     AIATP|         root|   root| true| Código de Sitio|            HCUN0057|
    |  32456|     AIATP|         root|   root| true| Código de Sitio|           MORL-9045|
    |  37458|     AIATP|         root|   root| true| Código de Sitio|            HTOL0058|
    |  37512|     AIATP|         root|   root| true| Código de Sitio|           HVIC-0040|
    |  42653|     AIATP|         root|   root| true| Código de Sitio|       ATT-HPTV-0008|
    |  45251|     AIATP|         root|   root| true| Código de Sitio|          YUCMER0736|
    |  45385|     AIATP|         root|   root| true| Código de Sitio|        ATT-JAL-5147|
    |  46288|     AIATP|         root|   root| true| Código de Sitio|.MEXECA1058 ARINC...|
    |  53304|     AIATP|         root|   root| true| Código de Sitio|          QTOQTO2175|
    |  63315|     AIATP|         root|   root| true| Código de Sitio|         COATOR-1601|
    |  63593|     AIATP|         root|   root| true| Código de Sitio|          DIFIZT1175|
    |  64239|     AIATP|         root|   root| true| Código de Sitio|          NLEJRZ1493|
    |  68600|     AIATP|         root|   root| true| Código de Sitio|GUALEO1817 campirano|
    |  89585|     AIATP|         root|   root| true| Código de Sitio|      ATT-MEXALJ1479|
    |  91346|     AIATP|         root|   root| true| Código de Sitio|ATT-JALZAP2030- C...|
    |  96055|     AIATP|         root|   root| true| Código de Sitio|MEXNEZ1140-SANTA ...|
    |  99521|     AIATP|         root|   root| true| Código de Sitio|            MEX-9052|
    | 102577|     AIATP|         root|   root| true| Código de Sitio|          NLEPGG0886|
    |  28974|     AIATP|         root|   root| true| Código de Sitio|            GUE-7047|
    |  34401|     AIATP|         root|   root| true| Código de Sitio|             CHI-165|
    +-------+----------+-------------+-------+-----+----------------+--------------------+
    only showing top 20 rows
    


## Persistiendo los valores en formato:

- `df_txodk06`, formato basado en rows `tabular`

Y guardamos en una tabla en hive.


```python
df_txodk06.write.format("parquet").mode("Overwrite").saveAsTable("default.tx_stg_06_tabular_odk_32")
```
