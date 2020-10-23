
![Encabezado](image/encabezado.png)

# Adquisición de datos ODK 38

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
conf = SparkConf().setAppName('Adquisicion_Datos_ODK_38')  \
    .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)
```

## Lectura de datos requeridos para el proceso

En este caso estamos leyendo la tabla `tx_stg_06_1_odk` la cual contiene la información agrupada y aplanada a nivel:
- id_form, clave del formulario `n->many`.
- clave_form, clave para relacionar con eñ catálogo de ODK's `n->many`
- element_group, elemento padre agrupador de la estructura del formulario, el cual es dinámico de acuerdo a la operación y concepto del ODK. 
- element, elemento hijo y corresponde `n->to one` element_group.
- value, lista de campos y  valores posibles para cada tipo de ODK. 


```python
df_txodk01 = spark.read.table("tx_stg_06_1_odk")
```


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

- Filtrado de `id_form`, para identificar el tipo de documento a validar.
- Filtrado de `clave_form`, para identificar el tipo de ODK's a validar.


```python
df_txodk02 = df_txodk01.filter(df_txodk01["clave_form"]=="DECOR").select("id_form","clave_form","element_group","element","value").withColumn('value_str', concat_ws(',', 'value')).orderBy(df_txodk01["clave_form"])
```


```python
df_txodk02.printSchema()
```

    root
     |-- id_form: string (nullable = true)
     |-- clave_form: string (nullable = true)
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


```python
df_txodk02.orderBy("element_group").select("element_group").groupBy("element_group").count().show(50)
```

    +--------------------+-----+
    |       element_group|count|
    +--------------------+-----+
    |   groupAntennaRRU-0|76295|
    |   groupAntennaRRU-1|50866|
    |  groupAntennaRRU-10|  268|
    |  groupAntennaRRU-11|  177|
    |  groupAntennaRRU-12|  137|
    |  groupAntennaRRU-13|  139|
    |  groupAntennaRRU-14|  129|
    |  groupAntennaRRU-15|   84|
    |  groupAntennaRRU-16|   61|
    |  groupAntennaRRU-17|   45|
    |  groupAntennaRRU-18|   13|
    |  groupAntennaRRU-19|   15|
    |   groupAntennaRRU-2|29571|
    |  groupAntennaRRU-20|   15|
    |  groupAntennaRRU-21|   16|
    |   groupAntennaRRU-3|11552|
    |   groupAntennaRRU-4| 5213|
    |   groupAntennaRRU-5| 2881|
    |   groupAntennaRRU-6| 1714|
    |   groupAntennaRRU-7| 1129|
    |   groupAntennaRRU-8|  724|
    |   groupAntennaRRU-9|  517|
    |groupAntennaRRUVw...| 4579|
    |groupAntennaRRUVw...| 3596|
    |groupAntennaRRUVw...|  473|
    |groupAntennaRRUVw...|  421|
    |groupAntennaRRUVw...|  375|
    |groupAntennaRRUVw...|  317|
    |groupAntennaRRUVw...|  230|
    |groupAntennaRRUVw...|  157|
    |groupAntennaRRUVw...|  121|
    |groupAntennaRRUVw...|  105|
    |groupAntennaRRUVw...|   77|
    |groupAntennaRRUVw...|   67|
    |groupAntennaRRUVw...| 2416|
    |groupAntennaRRUVw...|   53|
    |groupAntennaRRUVw...|   42|
    |groupAntennaRRUVw...|   32|
    |groupAntennaRRUVw...|   23|
    |groupAntennaRRUVw...|   18|
    |groupAntennaRRUVw...|   14|
    |groupAntennaRRUVw...|   11|
    |groupAntennaRRUVw...|   11|
    |groupAntennaRRUVw...|   10|
    |groupAntennaRRUVw...|    8|
    |groupAntennaRRUVw...| 1524|
    |groupAntennaRRUVw...|    8|
    |groupAntennaRRUVw...|    7|
    |groupAntennaRRUVw...|    7|
    |groupAntennaRRUVw...|    4|
    +--------------------+-----+
    only showing top 50 rows
    


## Sección adicional de import de `pyspark` para manejo de colecciones (DF) y búsqueda y mapeo de datos principales correspondientes a cada ODK

__IMPORTANTE__: ES REQUERIDO validar ésta estrategia para optimizar el performance y la obtención ordenada de cada expr por ODK. La propuesta es manejar un `DF` por cada set de reglas de mapeo de datos por ODK, por lo cual debemos generar dataframes base para cada tipo de ODK y trabajarlo por separado, después hacer merge de los DF's. 


```python
from pyspark.sql.types import ArrayType, StructType, StructField, IntegerType
from pyspark.sql.functions import col, udf, explode, expr, flatten
from pyspark.sql import functions as F
```

## Segundo `approach`, intentando poner una estructura unificada tipo `k/v` las ventajas pueden ser las siguientes:
- Separando los dataframes por cada set de campos a identificar, esto permite crear más `expr` para sacar más campos en un futuro.
- Se considera una estructura estándar unificada por campo.

## Mejoras identificadas:
- El DF base contiene todo el universo de datos (todos los conjuntos de elementos y grupos para todos los ODK's), evaluamos el comportamiento y determinamos si hacemos `split` por ODK.

## casos de prueba:
- Primer caso, tomaremos el ODK38, para hacer pruebas.
  - Los campos para ODK38 identificados son (podrían existir más):
    - TS Finalización **ÚNICO**
    - Código de sitio **ÚNICO**
    - Número de serie (manual) **RECURSIVO**
    - Número de activo(manual) **RECURSIVO**
    - Marca **UNICO**
    - Modelo **UNICO**
- Segundo caso, tomaremos todos los ODK's y seleccionar campos entre diferentes ODK's.

## Sección definición de reglas de parseo de variables


```python
user_func = udf (lambda x,y: [i for i, e in enumerate(x) if e==y ])
user_func_val = udf (lambda x,y: [i for i, e in enumerate(x) if e==y])
```

#### Root 

#### TS Finalización 


```python
df_txodk03_root_TS_F = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "root") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'TS Finalización')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'TS Finalización')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'TS Finalización')")], ","))
```

#### Folio interno de embarque 


```python
df_txodk03_root_F_E = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "root") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Folio Interno de Embarque')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Folio Interno de Embarque')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Folio Interno de Embarque')")], ","))
```

#### Proyecto


```python
df_txodk03_root_PRO = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "root") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Proyecto')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Proyecto')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Proyecto')")], ","))
```

#### Código de sitio


```python
df_txodk03_root_CD_S = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "root") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Código de sitio')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Código de sitio')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Código de sitio')")], ","))
```

#### Vendor


```python
df_txodk03_root_V = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "root") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Vendor')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Vendor')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Vendor')")], ","))
```

----
#### groupAntennaRRU 

#### Marca 


```python
df_txodk03_groupAntennaRRU_MA = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupAntennaRRU") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Marca')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Marca')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Marca')")], ","))
```

#### Modelo 


```python
df_txodk03_groupAntennaRRU_MO = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupAntennaRRU") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Modelo')")], ","))
```

#### Número de serie (manual) 


```python
df_txodk03_groupAntennaRRU_NS_MN = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupAntennaRRU") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de serie (manual)')"))
#.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de serie (manual)')")], ","))
```

#### Número de activo


```python
df_txodk03_groupAntennaRRU_NA = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupAntennaRRU") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de activo')"))
#.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de activo')")], ","))
```

#### Número de activo(manual)


```python
df_txodk03_groupAntennaRRU_NA_MN = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupAntennaRRU") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo(manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo(manual)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de activo(manual)')"))
#.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de activo')")], ","))
```

#### Número de serie (escáner)


```python
df_txodk03_groupAntennaRRU_NS_SC = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupAntennaRRU") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de serie (escáner)')"))
```

#### Tipo de elemento 


```python
df_txodk03_groupAntennaRRU_TE = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupAntennaRRU") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Tipo de elemento')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Tipo de elemento')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Tipo de elemento')")], ","))
```

----
#### groupEquipoElectronico 

#### Marca 


```python
df_txodk03_groupEquipoElectronico_MA = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupEquipoElectronico") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Marca')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Marca')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Marca')")], ","))
```

#### Modelo 


```python
df_txodk03_groupEquipoElectronico_MO = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupEquipoElectronico") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Modelo')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Modelo')")], ","))
```

#### Número de serie (escáner) 


```python
df_txodk03_groupEquipoElectronico_NS_SC = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupEquipoElectronico") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de serie (escáner)')")], ","))
```

#### Número de activo(manual)


```python
df_txodk03_groupEquipoElectronico_NA_MN = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupEquipoElectronico") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo(manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo(manual)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de activo(manual)')")], ","))
#.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de activo(manual)')"))
```

#### Descripción u observaciones


```python
df_txodk03_groupEquipoElectronico_DES_OB = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupEquipoElectronico") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Descripción u observaciones')")], ","))
#.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de activo(manual)')"))
```

---
#### groupBatteryBank 

#### Descripción u observaciones 


```python
df_txodk03_groupBatteryBank_DES_OB = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupBatteryBank") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Descripción u observaciones')")], ","))
#.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de activo(manual)')"))
```

#### Número de serie (manual)


```python
df_txodk03_groupBatteryBank_NS_MN = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupBatteryBank") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de serie (manual)')"))
```

#### Número de serie (escáner)


```python
df_txodk03_groupBatteryBank_NS_SC = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupBatteryBank") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de serie (escáner)')"))
```

---
#### groupBatteryBankVwGrp 

#### Vista de banco de baterías


```python
df_txodk03_groupBatteryBankVwGrp_V_B = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupBatteryBankVwGrp") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Vista de banco de baterías')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Vista de banco de baterías')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Vista de banco de baterías')")], ","))
```

---
#### groupCabinetRack 

#### Número de serie (manual) 


```python
df_txodk03_groupCabinetRack_NS_MN = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupCabinetRack") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de serie (manual)')"))
#.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de serie (manual)')")], ","))
```

#### Número de serie (escáner)


```python
df_txodk03_groupCabinetRack_NS_SC = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupCabinetRack") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de serie (escáner)')"))
```

#### Número de activo(escaner)


```python
df_txodk03_groupCabinetRack_NA_SC = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupCabinetRack") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo(escaner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo(escaner)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de activo(escaner)')"))
#.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de activo(escaner)')")], ","))
```

#### Número de activo(manual)


```python
df_txodk03_groupCabinetRack_NA_MN = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupCabinetRack") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo(manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo(manual)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de activo(manual)')")], ","))
```

#### Descripción u observaciones


```python
df_txodk03_groupCabinetRack_DES_OB = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupCabinetRack") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Descripción u observaciones')"))
#.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Descripción u observaciones')")], ","))
```

#### Tipo de elemento


```python
df_txodk03_groupCabinetRack_TE = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupCabinetRack") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Tipo de elemento)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Tipo de elemento')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Tipo de elemento')")], ","))
```

-----
#### groupCabinetRackVwGrp 

#### Vista de gabinetes y racks


```python
df_txodk03_groupCabinetRackVwGrp_V_GyR = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupCabinetRackVwGrp") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Vista de gabinetes y racks)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Vista de gabinetes y racks')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Vista de gabinetes y racks')")], ","))
```

-----
#### groupEquipoElectronico 

#### Tipo de elemento


```python
df_txodk03_groupEquipoElectronico_TE = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupEquipoElectronico") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Tipo de elemento')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Tipo de elemento')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Tipo de elemento')")], ","))
```

#### Número de serie (manual)


```python
df_txodk03_groupEquipoElectronico_NS_MN = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupEquipoElectronico") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de serie (manual)')")], ","))
```

---
### groupEquipoElectronicoVwGrp 

#### Equipos electrónicos


```python
df_txodk03_groupEquipoElectronicoVwGrp_EE = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupEquipoElectronicoVwGrp") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Equipos electrónicos')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Equipos electrónicos')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Equipos electrónicos')"))
#.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Equipos electrónicos')")], ","))
```

---
### groupMaterials

#### Número de serie (manual)


```python
df_txodk03_groupMaterials_NS_MN = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupMaterials") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de serie (manual)')"))
```

#### Número de serie (escáner)


```python
df_txodk03_groupMaterials_NS_SC = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupMaterials") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de serie (escáner)')"))
```

#### Tipo de Material


```python
df_txodk03_groupMaterials_TM = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupMaterials") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Tipo de Material')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Tipo de Material')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Tipo de Material')")], ","))
```

#### Cantidad


```python
df_txodk03_groupMaterials_C = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupMaterials") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Cantidad')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'v')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Cantidad')")], ","))
```

#### Descripción u observaciones


```python
df_txodk03_groupMaterials_DES_OB = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupMaterials") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Descripción u observaciones')")], ","))
```

-----
#### groupMtlVwGrp 

#### Vista de materiales


```python
df_txodk03_groupMtlVwGrp_V_M = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupMtlVwGrp") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Vista de materiales')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Vista de materiales')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Vista de materiales')")], ","))
```

-----
#### groupPwrPnt 

#### Número de serie (manual) 


```python
df_txodk03_groupPwrPnt_NS_MN = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupPwrPnt") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (manual)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de serie (manual)')"))
#.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de serie (manual)')")], ","))
```

#### Número de serie (escáner) 


```python
df_txodk03_groupPwrPnt_NS_SC = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupPwrPnt") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de serie (escáner)')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Número de serie (escáner)')"))
```

#### Número de activo(escaner)


```python
df_txodk03_groupPwrPnt_NA_SC = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupPwrPnt") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo(escaner)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo(escaner)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de activo(escaner)')")], ","))
```

#### Número de activo(manual)


```python
df_txodk03_groupPwrPnt_NA_MN = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupPwrPnt") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Número de activo(manual)')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Número de activo(manual)')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Número de activo(manual)')")], ","))
```

#### Marca


```python
df_txodk03_groupPwrPnt_MA = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupPwrPnt") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Marca')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Marca')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Marca')")], ","))
```

#### Descripción u observaciones


```python
df_txodk03_groupPwrPnt_DES_OB = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupPwrPnt") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_value", expr("filter(value, x -> x != 'Descripción u observaciones')"))
#.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Descripción u observaciones')")], ","))
```

---
#### groupShelterVwGrp 

#### Vista de shelters


```python
df_txodk03_groupShelterVwGrp_V_SH = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupShelterVwGrp") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Vista de shelters')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Vista de shelters')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Vista de shelters')")], ","))
```

---
#### groupSupportsVwGrp 

#### Vista de soportes


```python
df_txodk03_groupSupportsVwGrp_V_SOP = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSupportsVwGrp") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Vista de soportes')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Vista de soportes')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Vista de soportes')")], ","))
```

---
#### groupPedMovimiento 

#### QR 


```python
df_txodk03_groupPedMovimiento_QR = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupPedMovimiento") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Marca')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Marca')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'QR')")], ","))
```

#### Pedido de Movimiento 


```python
df_txodk03_groupPedMovimiento_PM = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupPedMovimiento") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Pedido de Movimiento')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Pedido de Movimiento')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Pedido de Movimiento')")], ","))
```

#### Vendor destino 


```python
df_txodk03_groupPedMovimiento_VD = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupPedMovimiento") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Vendor destino')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Vendor destino')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Vendor destino')")], ","))
```

#### Código de sitio destino


```python
df_txodk03_groupPedMovimiento_CSD = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupPedMovimiento") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Codigo de sitio destino.')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Codigo de sitio destino.')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Codigo de sitio destino.')")], ","))
```

---
#### groupSupports

#### Descripción u observaciones


```python
df_groupSupports_DES_OB = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupSupports") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Descripción u observaciones')")], ","))
```

---
#### groupTowers 

#### Descripción u observaciones


```python
df_groupTowers_DES_OB = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupTowers") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Descripción u observaciones')")], ","))
```

---
#### groupTransfers 

#### Descripción u observaciones


```python
df_groupTransfers_DES_OB = df_txodk02 \
.filter(split(df_txodk02.element_group,"-")[0] == "groupTransfers") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Descripción u observaciones')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Descripción u observaciones')")], ","))
```

## TERMINA Sección definición de reglas de parseo de variables


```python
# import modules
from functools import reduce
from pyspark.sql import DataFrame
# create list of dataframes
dfs = [df_txodk03_root_TS_F, \
       df_txodk03_root_F_E, \
       df_txodk03_root_PRO, \
       df_txodk03_root_CD_S, \
       df_txodk03_root_V, \
       df_txodk03_groupAntennaRRU_MA, \
       df_txodk03_groupAntennaRRU_MO, \
       df_txodk03_groupAntennaRRU_NS_MN, \
       df_txodk03_groupAntennaRRU_NS_SC, \
       df_txodk03_groupAntennaRRU_NA, \
       df_txodk03_groupAntennaRRU_NA_MN, \
       df_txodk03_groupAntennaRRU_TE, \
       df_txodk03_groupEquipoElectronico_MA, \
       df_txodk03_groupEquipoElectronico_MO, \
       df_txodk03_groupEquipoElectronico_NS_SC, \
       df_txodk03_groupEquipoElectronico_NA_MN, \
       df_txodk03_groupEquipoElectronico_DES_OB, \
       df_txodk03_groupBatteryBank_DES_OB, \
       df_txodk03_groupBatteryBank_NS_MN, \
       df_txodk03_groupBatteryBank_NS_SC, \
       df_txodk03_groupBatteryBankVwGrp_V_B, \
       df_txodk03_groupCabinetRack_NS_MN, \
       df_txodk03_groupCabinetRack_NS_SC, \
       df_txodk03_groupCabinetRack_NA_SC, \
       df_txodk03_groupCabinetRack_NA_MN, \
       df_txodk03_groupCabinetRack_DES_OB, \
       df_txodk03_groupCabinetRack_TE, \
       df_txodk03_groupCabinetRackVwGrp_V_GyR, \
       df_txodk03_groupEquipoElectronico_TE, \
       df_txodk03_groupEquipoElectronico_NS_MN, \
       df_txodk03_groupEquipoElectronicoVwGrp_EE, \
       df_txodk03_groupMaterials_NS_MN, \
       df_txodk03_groupMaterials_NS_SC, \
       df_txodk03_groupMaterials_TM, \
       df_txodk03_groupMaterials_C, \
       df_txodk03_groupMaterials_DES_OB, \
       df_txodk03_groupPwrPnt_NS_MN, \
       df_txodk03_groupPwrPnt_NS_SC, \
       df_txodk03_groupPwrPnt_NA_SC, \
       df_txodk03_groupPwrPnt_NA_MN, \
       df_txodk03_groupPwrPnt_MA, \
       df_txodk03_groupPwrPnt_DES_OB, \
       df_txodk03_groupShelterVwGrp_V_SH, \
       df_groupSupports_DES_OB, \
       df_txodk03_groupSupportsVwGrp_V_SOP, \
       df_txodk03_groupMtlVwGrp_V_M, \
       df_groupTowers_DES_OB, \
       df_groupTransfers_DES_OB, \
       df_txodk03_groupPedMovimiento_QR, \
       df_txodk03_groupPedMovimiento_PM, \
       df_txodk03_groupPedMovimiento_VD, \
       df_txodk03_groupPedMovimiento_CSD
      ]

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
dfW = df.filter(df['exist'] == "true")
```

## Persistiendo los valores en dos formatos:

- `df_txodk05`, formato basado en columns `plano`
- `df`, formato basado en rows `tabular`


```python
#df_txodk05.write.format("parquet").mode("Overwrite").saveAsTable("default.tx_stg_06_plano_odk_<numero>")
```


```python
dfW.write.format("parquet").mode("Overwrite").saveAsTable("default.tx_stg_06_tabular_odk_38")
```
