
# Adquisición de datos para ODK 76

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
conf = SparkConf().setAppName('EDA_ODK_76')  \
    .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)
```

## ANTES DE EMPEZAR VALIDAR SU `ID_FORM`

```
select * from tx_stg_06_1_odk
WHERE id_form  = 179490 --and element_group = "groupAntennaRRU-0"
ORDER BY element_group, element
```

## Lectura de datos requeridos para el proceso

En este caso estamos leyendo la tabla `tx_stg_06_1_odk` la cual contiene la información agrupada y aplanada a nivel:
- id_form, clave del formulario `n->many`.
- clave_form, clave para relacionar con eñ catálogo de ODK's `n->many`
- element_group, elemento padre agrupador de la estructura del formulario, el cual es dinamico de acuerdo a la operación y concepto del ODK. 
- element, elemento hijo y corresponde `n->to one` element_group.
- value, Lista de campos y  valores posibles para cada tipo de ODK. 


```python
df_txodk01 = spark.read.table("tx_stg_06_1_odk") 
```


```python
df_tyest =  df_txodk01.withColumn("test",split(df_txodk01.element_group,"-")[0])
```


```python
df_tyest.select("test").show(truncate=False)
```

    +--------------------+
    |test                |
    +--------------------+
    |groupAntennaRRU     |
    |groupBbus           |
    |groupSectors        |
    |groupMaterials      |
    |groupSectors        |
    |groupMaterials      |
    |groupMaterials      |
    |groupAntennaRRU     |
    |groupAntennaRRU     |
    |root                |
    |groupAntennaRRU     |
    |groupMaterials      |
    |groupMaterials      |
    |groupAntennaRRU     |
    |groupAntennaRRU     |
    |groupMaterials      |
    |groupMaterials      |
    |groupMaterials      |
    |groupAntennaRRU     |
    |groupAntennaRRUVwGrp|
    +--------------------+
    only showing top 20 rows
    



```python
df_txodk01.show()
```

    +-------+----------+--------------------+--------------------+--------------------+------+
    |id_form|clave_form|       element_group|             element|               value|odk_no|
    +-------+----------+--------------------+--------------------+--------------------+------+
    | 100005|     DECOR|   groupAntennaRRU-0|          strUnity-0|       [Unidad, Pza]|  0038|
    | 100028|     AIATP|         groupBbus-0|        groupCards-3|[TARJETAS BBU 04,...|  0032|
    | 100041|     AIATP|      groupSectors-0|         groupRrus-2|[RRU 03, , Vista ...|  0032|
    | 100834|     DECOR|   groupMaterials-25|          strUnity-8|       [Unidad, Pza]|  0038|
    | 100835|     AIATP|      groupSectors-1|      groupAntenas-0|[ANTENA 01, , Eti...|  0032|
    | 100842|     DECOR|    groupMaterials-4|    groupMaterials-4|[GRUPO DE MATERIA...|  0038|
    | 100849|     DECOR|    groupMaterials-6|        strTypeOth-8|[Tipo de Material...|  0038|
    | 100852|     DECOR|   groupAntennaRRU-0|          intHight-0|[Altura, 30, Altu...|  0038|
    | 100852|     DECOR|   groupAntennaRRU-2|       intQuantity-0|       [Cantidad, 2]|  0038|
    | 100860|     DECOR|                root|                root|[TS Finalización,...|  0038|
    | 100870|     DECOR|   groupAntennaRRU-0|    strAssetNumber-0|[Número de activo...|  0038|
    | 100884|     DECOR|   groupMaterials-17|   groupMaterials-17|[GRUPO DE MATERIA...|  0038|
    | 100889|     DECOR|    groupMaterials-1|       intQuantity-8|       [Cantidad, 9]|  0038|
    | 100891|     DECOR|   groupAntennaRRU-3|groupSubAntennaRRU-0|[SUBGRUPO DE ANTE...|  0038|
    | 100906|     DECOR|   groupAntennaRRU-0|    strAssetNumber-0|[Número de activo...|  0038|
    | 100921|     DECOR|    groupMaterials-6|          strUnity-8|    [Unidad, Piesas]|  0038|
    | 100923|     DECOR|    groupMaterials-8| groupSubMaterials-3|[SUBGRUPO DE MATE...|  0038|
    | 100924|     DECOR|   groupMaterials-18|       intQuantity-8|       [Cantidad, 1]|  0038|
    | 100927|     DECOR|   groupAntennaRRU-2|     strManualMode-0|[Número de serie ...|  0038|
    | 100938|     DECOR|groupAntennaRRUVw...|groupAntennaRRUVw...|[VISTA GABINETES ...|  0038|
    +-------+----------+--------------------+--------------------+--------------------+------+
    only showing top 20 rows
    



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
    


# Filtrado para pruebas controladas, los siguientes escenarios se contemplan:

- filtrado de `id_form`, para identificar el tipo de documento a validar.
- filtrado de `clave_form`, para identificar el tipo de ODK's a validar.


```python
df_txodk02 = df_txodk01.filter(df_txodk01["id_form"]=="179490").select("id_form","clave_form","element_group","element","value").withColumn('value_str', concat_ws(',', 'value')).orderBy(df_txodk01["clave_form"])
```

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

    +----------------------+-----+
    |element_group         |count|
    +----------------------+-----+
    |groupPedMovimiento-0  |2    |
    |groupPedMovimiento-1  |2    |
    |groupPedMovimiento-10 |2    |
    |groupPedMovimiento-100|2    |
    |groupPedMovimiento-101|2    |
    |groupPedMovimiento-102|2    |
    |groupPedMovimiento-103|2    |
    |groupPedMovimiento-104|2    |
    |groupPedMovimiento-105|2    |
    |groupPedMovimiento-106|2    |
    |groupPedMovimiento-107|2    |
    |groupPedMovimiento-108|2    |
    |groupPedMovimiento-109|2    |
    |groupPedMovimiento-11 |2    |
    |groupPedMovimiento-110|2    |
    |groupPedMovimiento-111|2    |
    |groupPedMovimiento-112|2    |
    |groupPedMovimiento-113|2    |
    |groupPedMovimiento-114|2    |
    |groupPedMovimiento-115|2    |
    |groupPedMovimiento-116|2    |
    |groupPedMovimiento-117|2    |
    |groupPedMovimiento-118|2    |
    |groupPedMovimiento-119|2    |
    |groupPedMovimiento-12 |2    |
    |groupPedMovimiento-120|2    |
    |groupPedMovimiento-121|2    |
    |groupPedMovimiento-122|2    |
    |groupPedMovimiento-123|2    |
    |groupPedMovimiento-124|2    |
    |groupPedMovimiento-125|2    |
    |groupPedMovimiento-126|2    |
    |groupPedMovimiento-127|2    |
    |groupPedMovimiento-128|2    |
    |groupPedMovimiento-129|2    |
    |groupPedMovimiento-13 |2    |
    |groupPedMovimiento-130|2    |
    |groupPedMovimiento-131|2    |
    |groupPedMovimiento-132|2    |
    |groupPedMovimiento-133|2    |
    |groupPedMovimiento-134|2    |
    |groupPedMovimiento-135|2    |
    |groupPedMovimiento-136|2    |
    |groupPedMovimiento-137|2    |
    |groupPedMovimiento-138|2    |
    |groupPedMovimiento-139|2    |
    |groupPedMovimiento-14 |2    |
    |groupPedMovimiento-140|2    |
    |groupPedMovimiento-141|2    |
    |groupPedMovimiento-142|2    |
    |groupPedMovimiento-143|2    |
    |groupPedMovimiento-15 |2    |
    |groupPedMovimiento-16 |2    |
    |groupPedMovimiento-17 |2    |
    |groupPedMovimiento-18 |2    |
    |groupPedMovimiento-19 |2    |
    |groupPedMovimiento-2  |2    |
    |groupPedMovimiento-20 |2    |
    |groupPedMovimiento-21 |2    |
    |groupPedMovimiento-22 |2    |
    |groupPedMovimiento-23 |2    |
    |groupPedMovimiento-24 |2    |
    |groupPedMovimiento-25 |2    |
    |groupPedMovimiento-26 |2    |
    |groupPedMovimiento-27 |2    |
    |groupPedMovimiento-28 |2    |
    |groupPedMovimiento-29 |2    |
    |groupPedMovimiento-3  |2    |
    |groupPedMovimiento-30 |2    |
    |groupPedMovimiento-31 |2    |
    |groupPedMovimiento-32 |2    |
    |groupPedMovimiento-33 |2    |
    |groupPedMovimiento-34 |2    |
    |groupPedMovimiento-35 |2    |
    |groupPedMovimiento-36 |2    |
    |groupPedMovimiento-37 |2    |
    |groupPedMovimiento-38 |2    |
    |groupPedMovimiento-39 |2    |
    |groupPedMovimiento-4  |2    |
    |groupPedMovimiento-40 |2    |
    |groupPedMovimiento-41 |2    |
    |groupPedMovimiento-42 |2    |
    |groupPedMovimiento-43 |2    |
    |groupPedMovimiento-44 |2    |
    |groupPedMovimiento-45 |2    |
    |groupPedMovimiento-46 |2    |
    |groupPedMovimiento-47 |2    |
    |groupPedMovimiento-48 |2    |
    |groupPedMovimiento-49 |2    |
    |groupPedMovimiento-5  |2    |
    |groupPedMovimiento-50 |2    |
    |groupPedMovimiento-51 |2    |
    |groupPedMovimiento-52 |2    |
    |groupPedMovimiento-53 |2    |
    |groupPedMovimiento-54 |2    |
    |groupPedMovimiento-55 |2    |
    |groupPedMovimiento-56 |2    |
    |groupPedMovimiento-57 |2    |
    |groupPedMovimiento-58 |2    |
    |groupPedMovimiento-59 |2    |
    |groupPedMovimiento-6  |2    |
    |groupPedMovimiento-60 |2    |
    |groupPedMovimiento-61 |2    |
    |groupPedMovimiento-62 |2    |
    |groupPedMovimiento-63 |2    |
    |groupPedMovimiento-64 |2    |
    |groupPedMovimiento-65 |2    |
    |groupPedMovimiento-66 |2    |
    |groupPedMovimiento-67 |2    |
    |groupPedMovimiento-68 |2    |
    |groupPedMovimiento-69 |2    |
    |groupPedMovimiento-7  |2    |
    |groupPedMovimiento-70 |2    |
    |groupPedMovimiento-71 |2    |
    |groupPedMovimiento-72 |2    |
    |groupPedMovimiento-73 |2    |
    |groupPedMovimiento-74 |2    |
    |groupPedMovimiento-75 |2    |
    |groupPedMovimiento-76 |2    |
    |groupPedMovimiento-77 |2    |
    |groupPedMovimiento-78 |2    |
    |groupPedMovimiento-79 |2    |
    |groupPedMovimiento-8  |2    |
    |groupPedMovimiento-80 |2    |
    |groupPedMovimiento-81 |2    |
    |groupPedMovimiento-82 |2    |
    |groupPedMovimiento-83 |2    |
    |groupPedMovimiento-84 |2    |
    |groupPedMovimiento-85 |2    |
    |groupPedMovimiento-86 |2    |
    |groupPedMovimiento-87 |2    |
    |groupPedMovimiento-88 |2    |
    |groupPedMovimiento-89 |2    |
    |groupPedMovimiento-9  |2    |
    |groupPedMovimiento-90 |2    |
    |groupPedMovimiento-91 |2    |
    |groupPedMovimiento-92 |2    |
    |groupPedMovimiento-93 |2    |
    |groupPedMovimiento-94 |2    |
    |groupPedMovimiento-95 |2    |
    |groupPedMovimiento-96 |2    |
    |groupPedMovimiento-97 |2    |
    |groupPedMovimiento-98 |2    |
    |groupPedMovimiento-99 |2    |
    |root                  |1    |
    +----------------------+-----+
    



```python
df_txodk02.select("*").where(df_txodk02["element_group"]=="groupPedMovimiento-1").show()

```

    +-------+----------+--------------------+--------------------+--------------------+--------------------+
    |id_form|clave_form|       element_group|             element|               value|           value_str|
    +-------+----------+--------------------+--------------------+--------------------+--------------------+
    | 179490|     ALMCN|groupPedMovimiento-1|groupPedMovimiento-1|[Pedido de Movimi...|Pedido de Movimie...|
    | 179490|     ALMCN|groupPedMovimiento-1|       groupPallet-0|[PALLETS-0, , Fot...|PALLETS-0,,Foto d...|
    +-------+----------+--------------------+--------------------+--------------------+--------------------+
    


## Sección adicional de import de `pyspark` para manejo de colecciones (DF), búsqueda y mapeo de datos principales correspondientes a cada ODK

__IMPORTANTE__: ES REQUERIDO validar esta estrategia para optimizar el performance y la obtención ordenada de cada expr por ODK. La propuesta es manejar un `DF` por cada set de reglas de mapeo de datos por ODK, por lo cual debemos generar dataframes Base para cada tipo de ODK y trabajarlo por separado, después hacer merge de los DF's. 


```python
from pyspark.sql.types import ArrayType, StructType, StructField, IntegerType
from pyspark.sql.functions import col, udf, explode, expr, flatten
from pyspark.sql import functions as F
```

## Primer `approach`: Estructura unificada tipo `k/v`

#### Las ventajas pueden ser las siguientes:
- Separando los dataframes por cada set de campos a identificar, esto permite crear mas `expr` para obtener los campos que sean requeridos en un futuro.
- Se considera una estructura estándar unificada por campo.

#### Mejoras identificadas:
- El DF base contiene todo el universo de datos (todos los conjuntos de elementos y grupos para todos los ODK's), evaluamos el comportamiento y determinamos si hacemos `split` por ODK.

#### casos de prueba:

Campos para ODK identificados son (podrían existir mas):

| id_form |  element_group     |     element        | no_odk |              value             |    tipo   |
|:-------:|:------------------:|:------------------:|:------:|:------------------------------:|:---------:|
| 179490  | root               | root               | 76     | TS Finalización                | ÚNICO     |
| 179490  | groupPedMovimiento | groupPedMovimiento | 76     | QR                             | ÚNICO     |
| 179490  | groupPedMovimiento | groupPedMovimiento | 76     | Codigo de sitio destino.       | ÚNICO     |
| 179490  | groupPedMovimiento | groupPedMovimiento | 76     | Pedido de Movimiento           | ÚNICO     |



## Seccion definicíon de Reglas de parseo de variables

### Root: TS Finalización


```python
df_txodk03_root_tsf = df_txodk02 \
.filter(df_txodk02["element_group"] == "root") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'TS Finalización')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'TS Finalización')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'TS Finalización')")], ","))
```


```python
df_txodk03_root_tsf_clean= df_txodk03_root_tsf.filter(df_txodk03_root_tsf['exist'] == "true")
```

### GroupPedMovimiento: Pedido de Movimiento



```python
# este es un ejemplo recursivo
df_txodk03_groupPedMovimiento_pmv = df_txodk02 \
.filter(df_txodk02["element_group"].substr(1, 18) == "groupPedMovimiento") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Pedido de Movimiento')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Pedido de Movimiento')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Pedido de Movimiento')")], ","))


```


```python
df_txodk03_groupPedMovimiento_pmv_clean= df_txodk03_groupPedMovimiento_pmv.filter(df_txodk03_groupPedMovimiento_pmv['exist'] == "true")
```

### GroupPedMovimiento: Codigo de sitio destino.



```python
# este es un ejemplo recursivo
df_txodk03_groupPedMovimiento_csd = df_txodk02 \
.filter(df_txodk02["element_group"].substr(1, 18) == "groupPedMovimiento") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'Codigo de sitio destino.')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'Codigo de sitio destino.')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'Codigo de sitio destino.')")], ","))


```


```python
df_txodk03_groupPedMovimiento_csd_clean= df_txodk03_groupPedMovimiento_csd.filter(df_txodk03_groupPedMovimiento_csd['exist'] == "true")
```

### GroupPedMovimiento: QR



```python
# este es un ejemplo recursivo
df_txodk03_groupPedMovimiento_qr = df_txodk02 \
.filter(df_txodk02["element_group"].substr(1, 18) == "groupPedMovimiento") \
.select("id_form","clave_form","element_group","element","value") \
.withColumn("exist", expr("exists(value, x -> x = 'QR')")) \
.withColumn("TipoElemento_key", expr("filter(value, x -> x = 'QR')")) \
.withColumn("TipoElemento_value", split(df_txodk02["value"][expr("array_position(value, 'QR')")], ","))

```


```python
df_txodk03_groupPedMovimiento_qr_clean= df_txodk03_groupPedMovimiento_qr.filter(df_txodk03_groupPedMovimiento_qr['exist'] == "true")
```

## TERMINA Seccion definicíon de Reglas de parseo de variables


```python
# import modules
from functools import reduce
from pyspark.sql import DataFrame
# create list of dataframes
dfs = [df_txodk03_root_tsf, \
       df_txodk03_groupPedMovimiento_pmv_clean, \
       df_txodk03_groupPedMovimiento_csd_clean, \
       df_txodk03_groupPedMovimiento_qr_clean]

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
df_final_clean=df.filter(df['exist'] == "true").distinct()#.show(50,truncate = False)
```


```python
df_final_clean.printSchema()
```

    root
     |-- id_form: string (nullable = true)
     |-- clave_form: string (nullable = true)
     |-- element_group: string (nullable = true)
     |-- element: string (nullable = true)
     |-- exist: boolean (nullable = true)
     |-- TipoElemento_key: string (nullable = true)
     |-- TipoElemento_value: string (nullable = true)
    


## Persistiendo los valores en formato:

- `df_txodk06`, formato basado en rows `tabular`

Y guardamos en una tabla en hive.


```python
#df_final_clean.write.format("parquet").mode("overwrite").saveAsTable("default.tx_stg_06_tabular_odk_76")
```


```python

```
