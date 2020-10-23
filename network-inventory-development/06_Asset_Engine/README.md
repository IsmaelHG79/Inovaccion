# Proceso de alta para fuentes por procesar en Asset Engine

## Instrucciones de ejecución

1. Es necesario que la fuente se encuentre registrada en la tabla **rci_db_metadata.cfg_rci_source**
1. Es necesario dar de alta la(s) tabla(s) que estén asociadas a la fuente porque el Asset Engine procesa por tabla y no por fuente.
1. Dentro de la tabla **rci_db_metadata.cg_rci_business_identifiers** es necesario validar si es que se ha de añadir un nuevo business identifier además de **serie**, **etiqueta** o **MAC Address**.
1. Dentro de la tabla de **rci_db_metadata.lnk_rci_business_identifiers** es necesario añadir las columnas de la nueva fuente que se asociarán a las que tenemos en el catálogo **rci_db_metadata.cg_rci_business_identifiers**, con esto mapearemos las columnas reconocidas como algún business identifier en esta tabla.  
1. Dentro de la tabla **rci_db_metadata.cg_rci_asset_properties** es necesario validar si es que se deben añadir nuevas propiedades o con las que contamos en este catálogo serán suficientes para buscar en la nueva fuente.
1. Dentro de la tabla **rci_db_metadat.lnk_rci_asset_properties** es necesario realizar el mapeo entre las propiedades del catálogo con respecto a las columnas que correspondan en la nueva fuente.
 1. El proceso de monitore del **Asset Engine** se ejecutará todos los días en un horario de **07:00 hrs a 22:00 hrs** con el propósito de censar las llegadas de nueva información en la capa de RAW. En caso de ser necesario, se podrá ejecutar de manera manual el shell que invoca al **Asset Engine** con los siguientes comandos:

*Para las tablas de RAW en desarrollo y las estructuras del Asset Model con el prefijo "dev_":*

```
/home/raw_rci/attdlkrci/shells/rci_start_asset_engine_monitor.sh dev
````
*Para las tablas de RAW productivas y las estructuras del Asset Model productivas:*

```
/home/raw_rci/attdlkrci/shells/rci_start_asset_engine_monitor.sh prd
````

<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
>>>>>>> c3cb3f8... Doc_Fixing Asset Engine Documentation
El horario de ejecución es un horario propuesto por Axity, sin embargo, este horario podrá ser personalizado desde el crontab de la manera que sea más útil para AT&T derivado de las necesidades de procesamiento de las fuentes por incluir en el Data Lake.
=======
>>>>>>> fe04ddc... Solving merge issues
* a - Prefijo del ambiente en el que estaremos trabajando
* b.- Solo en caso de requerir hacer pruebas para crear tablas nuevas, añadir en caso de no requerirse dejar solo “ ”
* c. - Espacio de trabajo donde estaremos leyendo los datos, en este caso: rci_db_inventory
* d. - Tabla que será procesada por ejemplo: tx_rci_fixed_asset
* e. - Execution ID, buscar el último ctl_eid asociado a la tabla de la fuente nueva dentro de la tabla rci_db_metadata.cr_rci_validation

## Objetivos
*  El objetivo del asset engine, es clasificar los datos raw de las fuentes que fueron ingestadas en el data lake, se clasifican de acuerdo a las claves de negocio que se regitraron en las tablas de propiedades; además de que el asset engine tambien proporciona un perfilamiento de la calidad de los datos de las fuentes.


## Importacion de librerias de python
```python
import hashlib
import sys
import uuid
from datetime import datetime
from difflib import SequenceMatcher
from functools import reduce
import pyspark.sql.functions as f
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import arrays_zip, explode_outer
from pyspark.sql.functions import broadcast ,lit
from pyspark.sql.functions import concat_ws
from pyspark.sql.functions import udf
from pyspark.sql.types import *
import itertools
import os
```

## Funciones

* Función que determina la location, model y vendor, utiliza el catalogo de **rci_db_metadata.cg_rci_vendor**

```python
def get_catalogs_vendor_model():
    #global lst_models
    global lst_vendors

    spark.read.format('org.apache.kudu.spark.kudu').options(**{
    'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
    'kudu.table': 'impala::rci_db_metadata.cg_rci_vendor'}).load().cache().createOrReplaceTempView("cg_vendor")


    cat_vendors = spark.sql("SELECT * FROM cg_vendor").select("cve_manufacturer","vendor_name","short_name","business_name").collect()

    #cat_models = spark.sql("SELECT * FROM cg_model").select("model").collect()

    lst_vendors = map(str,list(map(lambda x: x[0].upper(), cat_vendors))) + map(str,list(map(lambda x: x[1].upper(), cat_vendors)))\
                + map(str,list(map(lambda x: x[2].upper(), cat_vendors))) + map(str,list(map(lambda x: x[3].upper(), cat_vendors)))

    #lst_models = map(str,list(map(lambda x: x[0].upper(), cat_models)))

    lst_vendors = list(set(lst_vendors))
    #lst_vendors.remove("NULL")

    #lst_models = list(set(lst_models))
    
    return True
```
* Funcion que se encarga de buscar e inferir el nombre

```python
def search_infered_name(values):
    if len(values)>0:
        h = values[0]
        t = values[1:]
        if h.upper() in lst_vendors:
            return h
        else:
            return search_infered_name(t)
    else:
        return ""
```

* Función que se encarga buscar en el catalogo de **VENDOR**

```python
def search_in_cat(string, col):
    dic = {'VENDOR':lst_vendors}
    print col
    if col == "VENDOR":
        if string.upper() in dic[col]:
            return string
        else:
            return search_infered_name(source_table.split("_")[-2:])
    else:
        return string
```

* Funcion recursiva que se encarga 

```python
def recursive_lst_search_cat(df, cols):
    if len(cols) > 0:
        head = cols[0]
        tail = cols[1:]
        df_trans = df.withColumn(head, search_cat_udf(head,lit(head)))
        return recursive_lst_search_cat(df_trans, tail)
    else:
        return df
```

* Funcion que se encarga de obtener la fecha actual en timestamp

```python
def get_time():

    dateTimeObj = datetime.now()
    year = dateTimeObj.year
    month = "0%s" % (dateTimeObj.month) if len("%s" % (dateTimeObj.month)) == 1 else "%s" % (dateTimeObj.month)
    day = "0%s" % (dateTimeObj.day) if len("%s" % (dateTimeObj.day)) == 1 else "%s" % (dateTimeObj.day)
    hour = "0%s" % (dateTimeObj.hour) if len("%s" % (dateTimeObj.hour)) == 1 else "%s" % (dateTimeObj.hour)
    minute = "0%s" % (dateTimeObj.minute) if len("%s" % (dateTimeObj.minute)) == 1 else "%s" % (dateTimeObj.minute)
    second = "0%s" % (dateTimeObj.second) if len("%s" % (dateTimeObj.second)) == 1 else "%s" % (dateTimeObj.second)
    str_date = "%s-%s-%s" % (year, month, day)
    str_time = "%s:%s:%s.%s" % (hour, minute, second, dateTimeObj.microsecond)
    return str_date + ' ' + str_time
```

* Funcion que se encarga de encontrar la similitud entre palabras, y retorna un ratio de similitud de 0 - 1

```python
def str_similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
```

* Funcion que se encarga filtrar las columnas que se encuentren en la lista

```python
def match_columns(list_collect):
    list_match = [x for x in columns_list if x in list_collect]
    return list_match
```

* Funcion que se encarga de obtener la diferencia de las columns con respecto a la *list_match*

```python
def diff_columns(list_match):
    list_diff = list(set(columns_list) - set(list_match))
    return list_diff
```

* Funcion recursiva que se encarga de agregar columnas de acuerdo a lista dada

```python
def recursive_list_add_col(df, columns_list):

    if len(columns_list) > 0:
        head, tail = (lambda lst: (lst[0], lst[1:]))(columns_list)
        if head:
            df_pre = df.withColumn(head, lit(""))
            return recursive_list_add_col(df_pre, tail)
        else:
            return df
    else:
        return df
```

* Funcion que se encarga obtener el nombre de las tablas de la bd

```python
def hive_data(hive_table, last_partition, spark):

    describe_hive_table = "describe %s" % hive_table
    describe_hive_table_df = spark.sql(describe_hive_table)
    row_list_collect = describe_hive_table_df.select("col_name").collect()
    list_collect = list(map(lambda x: x[0], row_list_collect))
    list_match = match_columns(list_collect)
    list_match_str = ",".join(list_match)
    hive_query = "select %s from %s %s " % (list_match_str, hive_table, last_partition)
    return (hive_query, list_match)
```

*  Funcion que se encarga de limpiar los **string**, de acuerdo a ciertos patrones

```python
def clean_str(str_text):

    str_clean = ''
    str_text_u = u'%s' % (str_text)

    if str_text_u != None or str_text_u != '':
        str_clean = str_text.replace('"', "").replace('.', '').replace(',', '').replace('`', '').replace('#',
                                                                                                         '').replace(
            '|', '').replace(' ', '').replace('-', '').replace('_', '').replace("'", '').replace('!', '').replace('¿',
                                                                                                                  '').replace(
            '?', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('$', '').replace('&',
                                                                                                                  '').replace(
            '/', '').replace('*', '').replace('+', '').replace(';', '').replace('°', '').replace('<', '').replace('>',
                                                                                                                  '').replace(
            '=', '').replace('{', '').replace('}', '')
    return str_clean
```

* Funcion que se encarga de clasificar una lista de **string**, utilizando el algoritmo de **k-means**

```python
def lst_cluster_k_means(lst_test):

    lst_gral = []
    res = []

    for x in lst_test:
        item_lst = []
        for y in lst_test:
            percentage = SequenceMatcher(None, x, y).ratio()
            find_text = x.find(y)
            if percentage > 0.55:
                item_lst.append(y)
        lst_gral.append(item_lst)

    lst_gral_order = list(map(lambda x: sorted(x), lst_gral))
    for i in lst_gral_order:
        if i not in res:
            res.append(i)
    return res
```

* Funcion que se encarga de ordenar una tupla de acuerdo a un patron

```python
def sort_tuple(tup):

    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup
```

* Funcion que se encarga de obtener la ultima fecha de una lista de fechas

```python
def get_last_date(element, list_tuple):

    list_universe_filter = list(filter(lambda x: x[0] == element, list_tuple))
    size = len(list_universe_filter)
    last_date = int(sort_tuple(list_universe_filter)[size - 1][1])
    return last_date
```

* Funcion que se encarga de ordenar las columnas y darle un valor de acuerdo a la fecha, clasifica los valores dandole un valor o peso extra de acuero a la fecha mas reciente; esta funcion se utiliza en el algoritmo de **k-means**

```python
def homologate_columns_date(set_data):

    clear_set = ["", " ", None]
    mode = ""

    if len(set_data) > 1:
        lst_clear = filter(lambda x: x[0] not in clear_set, set_data)
        if len(lst_clear) > 0:
            sort_lst = sort_tuple(lst_clear)
            size = len(sort_tuple(sort_lst))
            mode = sort_lst[size - 1][0]
        else:
            mode = set_data[0]

    return mode
```

* Función que se encarga de buscar un elemento en una matriz

```python
def find_element(item, mtrx):

    index = -1
    lst_enum = list(enumerate(mtrx))
    lst = list(filter(lambda x: item in x[1], lst_enum))
    if len(lst) > 0:
        index = lst[0][0]
    return index
```

* Función que se encarga de buscar un elemento en un set, y aplicar un filtrado de acuerdo al ratio de comparación

```python
def find_element_set(element, set_list, index_group):

    list_percentage = list(filter(lambda x: SequenceMatcher(None, element, x).ratio() > 0.7, set_list))
    get_size = True if len(list_percentage) > 0 else False
    if get_size:
        return index_group
    else:
        return -1
```

* Función de crear un hash md5 de acuerdo a la columna del DF dada y un string

```python
def acn_hash(column, text):

    column_str = u''.join(column + text).encode('ascii', 'ignore').strip()
    result = hashlib.md5(column_str.encode()).hexdigest()
    return result
```

* Función que se encarga validar la columna dada del DF, y validar que sea un valor aceptable, regresa un boolean

```python
def validate_field(column_str):

    lst = dirt_lower
    str_tmp = column_str.strip().lower() if column_str is not None else ""
    status = True if str_tmp not in lst else False
    return status
```


* Función que se encarga de limpiar una cadena, quitando los 0 de derecha a izquierda, ejemplo: "000999" ->  "999"

```python
def recursive_zero_eval(s):

    if s is not None and s.startswith('0'):
        str_tem = s[1:]
        return recursive_zero_eval(str_tem)
    else:
        return s
```

* Función que se encarga de validar una cadena, una limpieza lógica lo cual es un etiquetado de acuerdo si cumple con la regla, de si es un valor con contenido o no

```python
def logic_clean(str_col):
    val_str = str(str_col.encode('ascii', 'ignore'))
    if val_str != '':
        res_val = True
    else:
        res_val = False
    return res_val
```

* Función que se encarga de convertir un time stamp en string, a un formatu numérico int

```python
def concat_date(year, month, day, partition):

    if partition == 'ym':
        year_temp = year
        month_temp = "0%s" % (month) if len("%s" % (month)) == 1 else "%s" % (month)
        return int("%s-%s" % (year_temp, month_temp))

    elif partition == 'ymd':
        year_temp = year
        month_temp = "0%s" % (month) if len("%s" % (month)) == 1 else "%s" % (month)
        day_temp = "0%s" % (day) if len("%s" % (day)) == 1 else "%s" % (day)

        return int("%s-%s-%s" % (year_temp, month_temp, day_temp))
```

* Función que se encarga de agregar recursivamente una columna vacia, de acuerdo a una lista dada

```python
def recursive_add_column(df, columns_list):

    if len(columns_list) > 0:
        head, tail = (lambda lst: (lst[0], lst[1:]))(columns_list)
        if head:
            df_pre = df.withColumn(head, f.lit(""))
            return recursive_add_column(df_pre, tail)
        else:
            return df
    else:
        return df
```

*  Función que se encarga de aplicar la limpieza del udf, de acuerdo a la función logic_clean

```python
def recursive_lst_validate(df, columns_list):

    if len(columns_list) > 0:
        head, tail = (lambda lst: (lst[0], lst[1:]))(columns_list)
        if head:
            df_pre = df.withColumn("validate_%s" % (head), logic_clean_udf(head))
            return recursive_lst_validate(df_pre, tail)
        else:
            return df
    else:
        return df
```

* Función que se encarga de ejecutar la función del udf de limpiar la cadena quitando los 0 de derecha a izquierda

```python
def recursive_lst_zero_eval(df, columns_list):
    if len(columns_list) > 0:
        head, tail = (lambda lst: (lst[0], lst[1:]))(columns_list)
        if head:
            df_pre = df.withColumn(head, recursive_zero_eval_udf(head))
            return recursive_lst_zero_eval(df_pre, tail)
        else:
            return df
    else:
        return df
```

* Función que se encarga de buscar de acuerdo a una columna dada del DF, y obtener valores de metadata, es decir si es un campo de BID ó de PROP

```python
def search_metada(str_col_name):

    lst_search = list(filter(lambda x: x['asset_name'] == str_col_name, lst_dict_all))
    lst_map_res = list(map(
        lambda x: {"cg_prop_id": x['cg_prop_id'], "lnk_column_id": x['lnk_column_id'], "source_id": x['source_id'],
                   "prop_type": x['type']}, lst_search))
    if len(lst_map_res) > 0:
        item_find = lst_map_res[0]
    else:
        item_find = {'cg_prop_id': '', 'lnk_column_id': '', 'prop_type': '', 'source_id': ''}
    return item_find
```

* Función que genera el acn, es cual es string uuid

```python
def generate_acn():

    return str(uuid.uuid1())
```

* Función que se encarga de validar si el id de la tabla de groups ya existe, y validar si ya existe y siel grupo es nuevo crear su id correspondiente

```python
def get_group_id(group_id_lst):

    group_id = ''
    group_id_filter_lst = list(filter(lambda x: x != '', group_id_lst))
    size = len(group_id_filter_lst)

    if size > 0:
        group_id = group_id_filter_lst[0]
    else:
        group_id = generate_acn()

    return group_id
```

* Función que se encarga de obtener el último ctl_rid de un grupo, como tal es una lista de ctl_rid

```python
def get_last_ctl_rid(ctl_rid_lst):

    ctl_rid = ''
    ctl_rid_filter_lst = list(filter(lambda x: x != '', ctl_rid_lst))
    size = len(ctl_rid_filter_lst)

    if size > 0:
        ctl_rid = ctl_rid_filter_lst[size - 1]

    return ctl_rid
```


* Función udf que se encarga de validar los anomaly de acuerdo al campo dado y tambien tiene que ver si son campos de tipo BID o PROP

```python
def get_anomaly(col_val, type_str, array):

    dirt_lower_filter = list(filter(lambda x: x != '', dirt_lower))
    enum_array = list(enumerate(array))
    gral_lst = []

    size = len(array)
    if size > 0:
        if col_val != '':

            splt_lst = col_val.split("||||")
            splt_enum_lst = list(enumerate(splt_lst))

            empty_filter_lst = list(filter(lambda x: x[1] == '', splt_enum_lst))
            empty_filter_size = len(empty_filter_lst)

            if empty_filter_size > 0:
                anomaly_empty_get_key = list(filter(lambda x: "MISSING_VALUE" in x, anomaly_upper))[0]
                map_empty = list(map(lambda x: x[0], empty_filter_lst))
                array_get_empty = list(filter(lambda x: x[0] in map_empty, enum_array))
                res_map_empty = list(map(lambda x: "%s:%s" % (x[1], anomaly_empty_get_key), array_get_empty))
                gral_lst.append(res_map_empty)

            wrong_filter_lst = list(filter(lambda x: x[1] in dirt_lower_filter, splt_enum_lst))
            wrong_filter_size = len(wrong_filter_lst)

            if wrong_filter_size > 0:
                anomaly_wrong_get_key = list(filter(lambda x: "WRONG_VALUE" in x, anomaly_upper))[0]
                map_wrong = list(map(lambda x: x[0], wrong_filter_lst))
                array_get_wrong = list(filter(lambda x: x[0] in map_wrong, enum_array))
                res_map_wrong = list(map(lambda x: "%s:%s" % (x[1], anomaly_wrong_get_key), array_get_wrong))
                gral_lst.append(res_map_wrong)

            gral_count_str = empty_filter_size + wrong_filter_size

            return (gral_count_str, list(itertools.chain(*gral_lst)))

        else:

            anomaly_empty_get_key = list(filter(lambda x: "MISSING_VALUE" in x, anomaly_upper))[0]
            map_array = list(map(lambda x: "%s:%s" % (x[1], anomaly_empty_get_key), enum_array))
            gral_lst.append(map_array)
            return (size, list(itertools.chain(*gral_lst)))

    else:

        if type_str.upper() == 'BID':
            anomaly_empty_get_key_bid = list(filter(lambda x: "NO_BID" in x, anomaly_upper))[0]
            return (0, [anomaly_empty_get_key_bid])

        elif type_str.upper() == 'PROP':
            anomaly_empty_get_key_prop = list(filter(lambda x: "NO_PROP" in x, anomaly_upper))[0]
            return (0, [anomaly_empty_get_key_prop])
```

*  Función que se encarga de obtener todos los campo de tipo BID del asset trace y pasarlo a un modelo tabular para despues ser utilizada en el algoritmo del asset engine

```python
def get_last_asset_trace(asset_trace_table, str_col_head):

    try:
        load_asset_trace_df = spark.sql("select * from %s where type = 'bi' and  VALUE != '' " % (asset_trace_table)).cache()

        asset_trace_column_df = load_asset_trace_df\
            .groupBy("id", 'acn').pivot("COL_NAME")\
            .agg(f.collect_list("VALUE")).cache()

        lst_explode_cols = list(set(asset_trace_column_df.columns) - {'id', 'acn'})

        asset_trace_tabular_df = asset_trace_column_df\
            .select('id', 'acn',f.explode(f.arrays_zip(*lst_explode_cols))).cache()

        lst_select_cols = list(map(lambda x: "col.%s" % (x), lst_explode_cols))

        asset_trace_df = asset_trace_tabular_df.select('id', 'acn', *lst_select_cols).cache()

        group_df = asset_trace_df\
            .where(f.col(str_col_head) != '')\
            .groupBy(str_col_head)\
            .agg(f.collect_set(f.struct("id","acn")).alias("data") )\
            .withColumn("explode",f.explode("data"))\
            .drop("data")\
            .withColumn("id",f.col("explode.id"))\
            .withColumn("acn",f.col("explode.acn"))\
            .drop("explode")\
            .groupBy(str_col_head)\
            .agg(f.collect_list('id').alias('id'), f.collect_list('acn').alias('acn')).cache()

        return group_df

    except:

        field = [
            StructField('id', ArrayType(StringType()), True),
            StructField('acn', ArrayType(StringType()), True),
            StructField(str_col_head, StringType(), True),
        ]

        empty_schema = StructType(field)
        res_df = spark.createDataFrame([], empty_schema)

        return res_df
```

* Función que se encarga de crear un modelo tabular a un modelo columnar de acuerdo al DF dado, las columnas de referencia para creal el modelo columnar son: id, acn,concat,count

```python
def create_columnar_model(complete_tabular_df, lst_stack):

    def switch_val(x):
        if "count" in x:
            return " '%s',cast(%s as string) " % (x, x)
        elif "ctl_" not in x:
            return " '%s',cast(%s as string) " % (x, x)
        else:
            return " '%s',array_join(%s,',') " % (x, x)

    lst_stack_cols = list(map(lambda x: switch_val(x), lst_stack))
    str_stack_cols = " , ".join(lst_stack_cols)
    size = len(lst_stack)

    str_stack_query = "stack( %s, %s) as (COL_NAME, VALUE)" % (size, str_stack_cols)

    column_model_df = complete_tabular_df.selectExpr("id", "acn","concat",'count', str_stack_query).cache()

    column_data_df = column_model_df.withColumn("type", get_type_udf("COL_NAME")) \
        .withColumn("source_id", f.lit(source_id)) \
        .withColumn("created_by", f.lit(created_by)).withColumn("created_on",f.lit(created_on)).cache()

    return column_data_df
```

* Función que se encarga de obtener el tipo de columna ya sea si es BID o PROP de acuerdo a la lista de diccionarios de assets

```python
def get_type(str_col):

    type_str = "None"
    if str_col in cts_lst:
        type_str = "ctl"
    else:
        item = list(filter(lambda x: str_col == x["asset_name"], lst_dict_all))
        if len(item) > 0:
            type_str = item[0]["type"]

    return type_str
```

* Función que se encarga de crear una lista a un set de acuerdo a la lista dada de columnas

```python
def lst_to_set(array_col):

    size = len(array_col)
    if size > 0:
        lst_unique = list(set(array_col))
        return lst_unique
    else:
        lst_unique = list(set())
        return lst_unique
```

* Función que se encarga de crear la tabla: **cr_rci_asset_events**, recibe como entrada el DF del asset trace, y de ahi parte validando si trae la columna de **LOC_CODE**, se encarga de agrupar por medio de las columnas de id y acn, una vez agrupados se procede a colectar los ctl_rid y despues aplicarle un explode para segregar esa columna de ctl_rid.

```python
def cr_rci_asset_events(df):

    validate_location = True if "LOC_CODE" in df.columns else False

    if validate_location == True:

        gp_df = df.groupBy("id", "acn", "LOC_CODE").agg(
            f.split(f.concat_ws(",", f.collect_list("ctl_rid")), ",").alias("ctl_rids")) \
            .select("id", "acn", f.col("LOC_CODE").alias("location"), f.explode("ctl_rids").alias("ctl_rid")).cache()

        res_df = gp_df.withColumn("type", lit(cycle_stage)) \
            .withColumn("created_on", lit(created_on)) \
            .withColumn("created_by", lit(created_by)).cache()

        return res_df

    else:

        gp_df = df.groupBy("id", "acn").agg(
            f.split(f.concat_ws(",", f.collect_list("ctl_rid")), ",").alias("ctl_rids"))\
            .select("id", "acn",f.explode("ctl_rids").alias("ctl_rid")).cache()

        res_df = gp_df.withColumn("type", lit(cycle_stage))\
            .withColumn("created_on", lit(created_on))\
            .withColumn("location",lit(""))\
            .withColumn("created_by", lit(created_by)).cache()

        return res_df
```

* Función que se encarga de crear la tabla: **cr_rci_processed_records**, la cual toma como entrada el DF del asset trace, se encarga de agrupar los campos por id y acn, y se realiza un colect sobre los campos ctl_rid y ctl_rfp, y generar un array para despues segregarlos

```python
def cr_rci_processed_records(df):

    lst_explode_cols = ["ctl_rid", "ctl_rfp"]

    gp_df = df.groupBy("id", "acn")\
        .agg(f.split(f.concat_ws(",", f.collect_list("ctl_rid")), ",").alias("ctl_rid"),
            f.split(f.concat_ws(",", f.collect_list("ctl_rfp")), ",").alias("ctl_rfp"))\
        .select("id", f.explode(f.arrays_zip(*lst_explode_cols)))\
        .select("id", "col.ctl_rid", "col.ctl_rfp").cache()

    res_df = gp_df.withColumn("created_by", lit(created_by))\
        .withColumn("created_on", lit(created_on)).cache()
    return res_df
```

* Función que se encarga de generar de un modelo columnar a un modelo tabular, se encarga de pasar la tabla asset trace que es una tabla columnar a un DF tabular, de acuerdo a los campos de referencia id, acn, concat, count

```python
def get_tabular_asset(load_asset_trace_df):

    const_cols_lst = ['id',
                      'acn',
                      "concat",
                      'created_on',
                      'ctl_eid',
                      'ctl_file_date',
                      'ctl_file_name',
                      'ctl_sid',
                      'ctl_tid',
                      'ctl_ts',
                      'count']

    count = load_asset_trace_df.count()
    if count > 0:

        asset_trace_column_df = load_asset_trace_df.groupBy("id", 'acn',"concat","count")\
            .pivot("COL_NAME").agg(f.collect_list("VALUE")).cache()

        cols_gral_lst = asset_trace_column_df.columns

        lst_explode_cols = list(set(cols_gral_lst) - set(const_cols_lst))

        asset_trace_tabular_df = asset_trace_column_df \
            .select("id", 'acn',"concat","count", f.explode(f.arrays_zip(*lst_explode_cols))).cache()

        lst_select_cols = list(map(lambda x: "col.%s" % (x), lst_explode_cols))

        asset_trace_df = asset_trace_tabular_df.select("id", 'acn',"concat","count",  *lst_select_cols).cache()

        return asset_trace_df
    else:
        return None
```

* Función que se encarga de crear la tabla de: cr_rci_asset_identifiers, se le pasa como entrada la tabla de asset trace, en el cual se le aplica un filtro de que solo sean los rows de tipo bi y sean distinto de vacio, depues se agrupa de acuerdo a los campos necesarios para mantener los conteos por id, acn y el valor, son conteos por source.

```python
def cr_rci_asset_identifiers(df):

    gp_df = df.where((f.col("VALUE") != "") & (f.col("type") == "bi")) \
        .groupBy("id", "acn", "COL_NAME", "VALUE", f.col("source_id").alias("ctl_tid")) \
        .agg(f.sum("count").alias("count")).cache()

    res_df = gp_df.withColumnRenamed("COL_NAME", "bid") \
        .withColumn("created_by", lit(created_by)) \
        .withColumn("created_on", lit(created_on)).cache()
    return res_df
```

* Función que se encarga de crear la tabla de: cr_rci_asset_properties, se le pasa como entrada la tabla de asset trace, en el cual se le aplica un filtro de que solo sean los rows de tipo prop y sean distinto de vacio, depues se agrupa de acuerdo a los campos necesarios para mantener los conteos por id, acn y el valor, son conteos por source.

```python
def cr_rci_asset_properties(df):

    gp_df = df.where((f.col("VALUE") != "") & (f.col("type") == "prop")) \
        .groupBy("id", "acn", "COL_NAME", "VALUE", f.col("source_id").alias("ctl_tid") ) \
        .agg(f.sum("count").alias("count")).cache()

    res_df = gp_df.withColumnRenamed("COL_NAME", "prop") \
        .withColumn("created_by", lit(created_by)) \
        .withColumn("created_on", lit(created_on)).cache()
    return res_df
```

* Funcion que se encarga de generar conteos generales por id, acn, bid, values, para mantener conteo globales por todas las fuenes de acuerdo al valor de identifiers, toma como entrada la tabla de conteos por src 

```python
def cr_rci_asset_identifiers_gral():

    df = spark.sql("select * from %s"%(cr_rci_asset_identifiers_str)).cache()

    gp_df = df \
        .groupBy("id", "acn", "bid", "value") \
        .agg(f.sum("count").alias("count")) \
        .withColumn("created_by", lit(created_by)) \
        .withColumn("created_on", lit(created_on)).cache()

    gp_df.write.format("parquet").mode("overwrite") \
        .saveAsTable(cr_rci_asset_identifiers_gral_str)
```

* Funcion que se encarga de generar conteos generales por id, acn, bid, values, para mantener conteo globales por todas las fuenes de acuerdo al valor de properties, toma como entrada la tabla de conteos por src 

```python
def cr_rci_asset_properties_gral():

    df = spark.sql("select * from %s" % (cr_rci_asset_properties_str)).cache()

    gp_df = df \
        .groupBy("id", "acn", "prop", "value" ) \
        .agg(f.sum("count").alias("count")) \
        .withColumn("created_by", lit(created_by)) \
        .withColumn("created_on", lit(created_on)).cache()

    gp_df.write.format("parquet").mode("overwrite") \
        .saveAsTable(cr_rci_asset_properties_gral_str)
```

*  Función que se encarga de generar la tabla: cg_rci_asset_master, se le aplica un filtro donde sean los rows de tipo ctl_rid, ya que es una tabla columnar se le aplica ese filtro y se obtiene el ctl_rid, ese ctl_rid despues se utiliza en unos filtros para obtener el primer ctl_rid, por cada grupo de id y acn.

```python
def cg_rci_asset_master(df):

    gp_df = df.where(f.col("col_name") == "ctl_rid")\
        .groupBy("id", "acn") \
        .agg(f.split(f.concat_ws(",", f.collect_list("value")), ",").alias("ctl_rids")) \
        .cache()

    asset_df = gp_df.select("*", gp_df["ctl_rids"][0].alias("ctl_rid")).drop("ctl_rids") \
        .withColumn("created_by", lit(created_by)) \
        .withColumn("created_on", lit(created_on)).cache()

    return asset_df
```

* Función que se encarga de crear la tabla: cr_rci_asset_group, se encarga d generar los grupos existentes por ls campos de id y acn, además de que calcula el último ctl_rid del grupo

```python
def cr_rci_asset_group(df):

    lst_cols = ["group_id","id","acn","count","ctl_rid_last","created_by","created_on"]

    numeric_created_on = get_numeric_timestamp()

    tab_df = df.withColumn("created_by", f.lit(numeric_created_on))\
        .withColumn("created_on", f.lit(""))\
        .withColumnRenamed("ctl_rid", "ctl_rid_last") \
        .withColumn("group_id", f.lit("")).select(*lst_cols).cache()

    last_created_on = get_last_partition()
    asset_group_data = get_asset_group(last_created_on)
    asset_group_temp_df = asset_group_data[0].select(*lst_cols).cache()
    asset_group_validate = asset_group_data[1]

    union_df = asset_group_temp_df.union(tab_df)
    gp_df = union_df.groupBy("id", "acn") \
        .agg(f.collect_set("group_id").alias("group_id"),
             f.split(f.concat_ws(",", f.collect_list("ctl_rid_last")), ",").alias("ctl_rid_last"),
             f.sum("count").alias("count")).cache()

    if asset_group_validate == True:

        gp_df\
            .withColumn("group_id",get_group_id_udf("group_id"))\
            .withColumn("ctl_rid_last",get_last_ctl_rid_udf("ctl_rid_last")) \
            .withColumn("created_by", f.lit(created_by)) \
            .withColumn("created_on", f.lit(numeric_created_on))\
            .select(*lst_cols).write.format("parquet").mode("overwrite") \
            .insertInto(cr_rci_asset_group_str)

        drop_partition(cr_rci_asset_group_str, last_created_on)

    else:

        gp_df \
            .withColumn("group_id", get_group_id_udf("group_id")) \
            .withColumn("ctl_rid_last", get_last_ctl_rid_udf("ctl_rid_last")) \
            .withColumn("created_by", f.lit(created_by)) \
            .withColumn("created_on", f.lit(numeric_created_on))\
            .select(*lst_cols).write.format("parquet").mode("overwrite") \
            .partitionBy("created_on").saveAsTable(cr_rci_asset_group_str)
```

* Función que se encarga de generar la tabla : cr_rci_anomalies, se encarga de realizas las validaciones correspondientes para agrear dicha evaluación de cada anomaly a la tabla, en esta función no se agregan todos, hay otras funciones quetambien agregan mas; esta se encarga de agregar los anoalies de bid y prop, se evaluan cada uno de los campos de bid y prop de que sea un valor valido, es por eso que hay un if con tres validaciones, la primera para validar que el DF tenga bid y prop, la segunda que tenga bid y no tenga prop, y la última que tenga prp y no bid, en esta función se llama al udf: **get_anomaly_udf** que se encarga de evaluar cada uno de los bid o prop, la evaluación se hacen por conjuntos, un xonjunto de bid y otro de prop, y por cada conjunto se obtiene como resultado una lista con la evaluación uno para bid y otro para prop, y esos resultado se agregan como columnas.
Además, tambien icluye la validación de model, location.

```python
def cr_rci_anomalies(df):

    check_anomaly_model = lambda prop_lst: True if "MODEL" not in prop_lst else False
    check_anomaly_location = lambda prop_lst: True if "LOC_CODE" not in prop_lst else False

    col_bi_concat = list(map(lambda y: y['asset_name'], list(filter(lambda x: x['type'] == 'bi', lst_filter))))
    col_prop_concat = list(map(lambda y: y['asset_name'], list(filter(lambda x: x['type'] == 'prop', lst_filter))))

    col_bi_concat_size = len(col_bi_concat)
    col_prop_concat_size = len(col_prop_concat)

    if col_bi_concat_size > 0 and col_prop_concat_size > 0:

        bids_rprops_df = df\
            .withColumn("bi_concat", concat_ws("||||", *col_bi_concat)) \
            .withColumn("prop_concat", concat_ws("||||", *col_prop_concat)) \
            .withColumn("lst_bids_affected", get_anomaly_udf("bi_concat", f.lit("bid"),f.array( list(map( lambda x : f.lit(x) , col_bi_concat)) ))  ) \
            .withColumn("lst_rprops_affected", get_anomaly_udf("prop_concat", f.lit("prop"),f.array( list(map( lambda x : f.lit(x) , col_prop_concat)) )) )\
            .withColumn("bids_affected", f.col("lst_bids_affected").getItem("count") )\
            .withColumn("desc_bids_affected", f.col("lst_bids_affected").getItem("elements") ) \
            .withColumn("rprops_affected", f.col("lst_rprops_affected").getItem("count") ) \
            .withColumn("desc_rprops_affected", f.col("lst_rprops_affected").getItem("elements") ) \
            .drop("lst_bids_affected","lst_rprops_affected") .cache()
        #Modified by Eduardo
        if not check_anomaly_location(col_prop_concat) or not check_anomaly_model(col_prop_concat):
            print "Trae LOC_CODE o MODEL"
            colNew = list(filter(lambda x: x == 'LOC_CODE' or x == 'MODEL' or x == 'VENDOR' or x == 'CATEGORY', col_prop_concat))
            print colNew
            res_df = bids_rprops_df \
                .withColumn("ctl_rid", f.split("ctl_rid", ",")) \
                .withColumn("ctl_rfp", f.split("ctl_rfp", ",")) \
                .select("id", "acn", "bids_affected", "desc_bids_affected", "rprops_affected", "desc_rprops_affected",f.explode(f.arrays_zip(*["ctl_rid","ctl_rfp"])) ,*colNew)\
                .withColumn("ctl_rid",f.col("col.ctl_rid")).withColumn("ctl_rfp",f.col("col.ctl_rfp")).drop("col") \
                .withColumn("ANOMALY_MODEL_MISSING", lit(check_anomaly_model(col_prop_concat) )) \
                .withColumn("ANOMALY_MLOCATION", lit(check_anomaly_location(col_prop_concat) )) \
                .withColumn("created_by", lit(created_by)) \
                .withColumn("created_on", lit(created_on)).cache()
        else:
            print "no trae loc_code o model"
            res_df = bids_rprops_df \
                .withColumn("ctl_rid", f.split("ctl_rid", ",")) \
                .withColumn("ctl_rfp", f.split("ctl_rfp", ",")) \
                .select("id", "acn", "bids_affected", "desc_bids_affected", "rprops_affected", "desc_rprops_affected",f.explode(f.arrays_zip(*["ctl_rid","ctl_rfp"])))\
                .withColumn("ctl_rid",f.col("col.ctl_rid")).withColumn("ctl_rfp",f.col("col.ctl_rfp")).drop("col") \
                .withColumn("ANOMALY_MODEL_MISSING", lit(check_anomaly_model(col_prop_concat) )) \
                .withColumn("ANOMALY_MLOCATION", lit(check_anomaly_location(col_prop_concat) )) \
                .withColumn("created_by", lit(created_by)) \
                .withColumn("created_on", lit(created_on)).cache()

        return res_df

    elif col_bi_concat_size > 0 and col_prop_concat_size == 0:

        bids_rprops_df = df \
            .withColumn("bi_concat", concat_ws("||||", *col_bi_concat)) \
            .withColumn("lst_bids_affected",get_anomaly_udf("bi_concat", f.lit("bid"), f.array(list(map( lambda x : f.lit(x) , col_bi_concat) ) ))) \
            .withColumn("bids_affected", f.col("lst_bids_affected").getItem("count")) \
            .withColumn("desc_bids_affected", f.col("lst_bids_affected").getItem("elements")) \
            .withColumn("lst_rprops_affected",get_anomaly_udf(f.lit(""), f.lit("prop"), f.array(list(map(lambda x: f.lit(x), []))))) \
            .withColumn("rprops_affected", f.col("lst_rprops_affected").getItem("count")) \
            .withColumn("desc_rprops_affected", f.col("lst_rprops_affected").getItem("elements"))\
            .drop("lst_bids_affected").cache()

        res_df = bids_rprops_df \
            .withColumn("ctl_rid", f.split("ctl_rid", ",")) \
            .withColumn("ctl_rfp", f.split("ctl_rfp", ",")) \
            .select("id", "acn", "bids_affected", "desc_bids_affected", "rprops_affected", "desc_rprops_affected",f.explode(f.arrays_zip(*["ctl_rid","ctl_rfp"]))) \
            .withColumn("ctl_rid",f.col("col.ctl_rid")).withColumn("ctl_rfp",f.col("col.ctl_rfp")).drop("col") \
            .withColumn("ANOMALY_MODEL_MISSING", lit(check_anomaly_model(col_prop_concat))) \
            .withColumn("ANOMALY_MLOCATION", lit(check_anomaly_location(col_prop_concat))) \
            .withColumn("created_by", lit(created_by)) \
            .withColumn("created_on", lit(created_on)).cache()

        return res_df

    elif col_bi_concat_size == 0 and col_prop_concat_size > 0:

        bids_rprops_df = df \
            .withColumn("prop_concat", concat_ws("||||", *col_prop_concat)) \
            .withColumn("lst_rprops_affected",get_anomaly_udf("prop_concat", f.lit("prop"), f.array(list(map( lambda x : f.lit(x) , col_prop_concat)) ))) \
            .withColumn("rprops_affected", f.col("lst_rprops_affected").getItem("count")) \
            .withColumn("desc_rprops_affected", f.col("lst_rprops_affected").getItem("elements")) \
            .withColumn("lst_bids_affected",get_anomaly_udf(f.lit(""), f.lit("bid"), f.array(list(map(lambda x: f.lit(x), []))))) \
            .withColumn("bids_affected", f.col("lst_bids_affected").getItem("count")) \
            .withColumn("desc_bids_affected", f.col("lst_bids_affected").getItem("elements")) \
            .drop( "lst_rprops_affected","lst_bids_affected").cache()

        res_df = bids_rprops_df \
            .withColumn("ctl_rid", f.split("ctl_rid", ",")) \
            .withColumn("ctl_rfp", f.split("ctl_rfp", ",")) \
            .select("id", "acn", "bids_affected", "desc_bids_affected", "rprops_affected", "desc_rprops_affected",f.explode(f.arrays_zip(*["ctl_rid","ctl_rfp"]))) \
            .withColumn("ctl_rid",f.col("col.ctl_rid")).withColumn("ctl_rfp",f.col("col.ctl_rfp")).drop("col") \
            .withColumn("ANOMALY_MODEL_MISSING", lit(check_anomaly_model(col_prop_concat))) \
            .withColumn("ANOMALY_MLOCATION", lit(check_anomaly_location(col_prop_concat))) \
            .withColumn("created_by", lit(created_by)) \
            .withColumn("created_on", lit(created_on)).cache()

        return res_df
```

* Función que se encarga de llenar el asset trace con los datos de las fuentes de cr_rci_asset_identifiers_str y cr_rci_asset_properties_str por fuente, esta funcion se ejecuta antes de que el engine procese la fuente y clasificarla, esto se hace ya que en las tablas anteriores se encuentran los registros mas recientes haste ese momento y para mantener ese  trace se toman esas fuentes como datos previos de asset y asi mantener a trazabilidad con lo mas reciente, para despues complementar el asset trace con los datos evaluados e la fuente que se proceso

```python
def fill_trace():

    try:
        bid_df = spark.sql("select * from %s"%(cr_rci_asset_identifiers_str))\
            .withColumnRenamed("bid","col_name" ) \
            .withColumnRenamed("ctl_tid", "source_id") \
            .withColumn("type", lit("bi")).cache()

        prop_df= spark.sql("select * from %s"%(cr_rci_asset_properties_str))\
            .withColumnRenamed("prop","col_name" ) \
            .withColumnRenamed("ctl_tid", "source_id") \
            .withColumn("type", lit("prop")).cache()

        union_trace = bid_df.union(prop_df)\
            .withColumn("found", lit(""))\
            .withColumn("traceable", lit(-1))\
            .withColumn("concat", lit(""))
        return union_trace

    except:

        field = [
            StructField('id',StringType(), True),
            StructField('acn', StringType(), True),
            StructField('concat', StringType(), True),
            StructField('count', LongType(), True),
            StructField('col_name', StringType(), True),
            StructField('value', StringType(), True),
            StructField('type', StringType(), True),
            StructField('source_id', StringType(), True),
            StructField('created_by', StringType(), True),
            StructField('created_on', StringType(), True),
            StructField('found', StringType(), True),
            StructField('traceable', IntegerType(), True)]
        empty_schema = StructType(field)
        df = spark.createDataFrame([], empty_schema)
        return df
```

* Función que se encarga de obtener la ultima partición de acuerdo al campo **created_on** de la tabla en formato int. Se utiliza en la función: **cr_rci_asset_group**

```python
def get_last_partition():

    try:
        last_created_on = spark.table(cr_rci_asset_group_str).select(f.max("created_on").alias("last_created_on")).take(1)[0][0]
        return last_created_on

    except:
        last_created_on = 0
        return last_created_on
```

* Función que se encarga de generar la tabla: cr_rci_acn_mapping, esta tabla son los id de negocio con un formato de acn y un valor numerico incremental de 0 a n, ya que spark como tal no puede generar numeros incremental, encontramos esta manera de generarlos, de acuerdo al calculo de diferencia entre lo obtenido hasta ese momento y los nuevo procesado, y de acuerdo a esa diferencia se genera un rango y una lista con respecto a ese rango y de ahi calcular apartir de que numero se inicia y hata cuando termina y generar los id acn en string

```python
def cr_rci_acn_mapping():

    acn_mapping_df = get_acn_mapping().cache()

    id_acn_master_df = get_id_acn_master().cache()
    id_acn_mapping_df = acn_mapping_df.select("id", "acn").cache()
    diff_df = id_acn_master_df.subtract(id_acn_mapping_df).cache()

    index_start = acn_mapping_df.count()
    diff_count= diff_df.count()

    if diff_count > 0:

        index_end = index_start + diff_count

        auto_increment_rdd = spark.sparkContext.parallelize( ["ACN%s" % (x) for x in range(index_start + 1, index_end + 1)] ).zipWithIndex().repartition(1).cache()
        diff_rdd = diff_df.rdd.zipWithIndex().repartition(1).cache()

        data_df = diff_rdd.toDF()\
            .withColumnRenamed("_1", "data")\
            .withColumnRenamed("_2", "index").cache()

        auto_increment_df = auto_increment_rdd.toDF()\
            .withColumnRenamed("_1", "bi_acn")\
            .withColumnRenamed("_2","index").cache()

        join_df = data_df.join(auto_increment_df, ["index"], how="inner").cache()

        res_df = join_df.select("data.id","data.acn","bi_acn")\
            .withColumn("created_on", f.lit(created_on))

        return res_df

    else:
        return None
```

* Función que se encarga de borrar la partición, utilizando el sql de spark, tiene como entrada la particion numerica y la tabla a la cual se le va a borrar la partición

```python
def drop_partition(cr_rci_asset_group_str, last_created_on):

    drop_partition_query = "ALTER TABLE %s DROP IF EXISTS PARTITION(created_on = %s)" % (cr_rci_asset_group_str, last_created_on)

    try:
        spark.sql(drop_partition_query)
    except:
        pass
```

* Función que se encarga de obtener en un DF la tabla de asset master solo con los campos de id y acn, con los datos mas recientes hasta ese momento excluyendo los nuevos que se van a procesar de la fuente, esto se realiza para hacer calculos posteriores con los nuevo datos entrantes

```python
def get_id_acn_master():

    try:
        id_acn_df = spark.sql("select id,acn from %s" % (cg_rci_asset_master_str)).cache()
        return id_acn_df

    except:

        field = [
            StructField('id', StringType(), True),
            StructField('acn', StringType(), True),
        ]

        empty_schema = StructType(field)
        df = spark.createDataFrame([], empty_schema)
        return df
```

* Función que se encarga de obtener en un DF la tabla de cr_rci_acn_mapping_str, con los datos mas recientes hasta ese momento excluyendo los nuevos que se van a procesar de la fuente, esto se realiza para hacer calculos posteriores con los nuevo datos entrantes

```python
def get_acn_mapping():

    try:
        bid_df = spark.sql("select * from %s" % (cr_rci_acn_mapping_str)).cache()

        return bid_df

    except:

        field = [
            StructField('id', StringType(), True),
            StructField('acn', StringType(), True),
            StructField('bi_acn', StringType(), True),
            StructField('created_on', StringType(), True)]

        empty_schema = StructType(field)
        df = spark.createDataFrame([], empty_schema)
        return df
```

* Función que se encarga de obtener en un DF la tabla de cr_rci_asset_group con una lista de columnas necesarias y un filtro con el campo de created_on, con los datos mas recientes hasta ese momento excluyendo los nuevos que se van a procesar de la fuente, esto se realiza para hacer calculos posteriores con los nuevo datos entrantes

```python
def get_asset_group(last_created_on):

    lst_cols = ["group_id", "id", "acn", "count", "ctl_rid_last", "created_by", "created_on"]
    try:
        group_temp_df = spark.sql("select * from %s where created_on = %s " % (cr_rci_asset_group_str, last_created_on))
        res_df = group_temp_df.select(*lst_cols).cache()
        return (res_df, True)

    except:

        empty_schema = StructType([
            StructField("group_id", StringType(), True),
            StructField("id", StringType(), True),
            StructField("acn", StringType(), True),
            StructField("count", IntegerType(), True),
            StructField("ctl_rid_last", StringType(), True),
            StructField("created_by", StringType(), True),
            StructField("created_on", LongType(), True)])

        res_df = spark.createDataFrame([], empty_schema)
        return (res_df, False)
```

* Función que se encarga de escribir los logs en una tabla con un formato dado, estos logs se ejecutan en ciertos puntos claves del codigo durante la ejecución para pode cachar en que proceso va o si surgio algún error, en que momento y con una descripción general

```python
def write_processed_sources(last_ctl_eid, ctl_tid, table_name, ctl_created_by,stage,state):

    uuid = generate_acn()
    created_on_log = get_time()

    res_df = spark.createDataFrame(
        [
            (str(uuid), str(last_ctl_eid), int(ctl_tid), str(table_name), str(ctl_created_by)),
        ],
        ['id', 'last_ctl_eid', 'ctl_tid', 'table_name', 'ctl_created_by']
    )

    res_df\
        .withColumn("stage",f.lit(stage)) \
        .withColumn("state", f.lit(state))\
        .withColumn("ctl_created_on",f.lit(created_on_log))\
        .write.format("parquet").mode("append").saveAsTable(cr_rci_ae_processed_sources_str)
```

* Función que se encarga de obtener los datos de la tabla: cr_rci_processed_records ya que en esta tabla se encuentran los rfp, se utiliza esta tabla para realizar la función que encuentra en las anomalias, el cual valida si es un rfp que ya existe en el asset o es nuevo ese row.

```python
def get_historic_rfp():
    try:
        query = 'select distinct(ctl_rfp) from %s' % (cr_rci_processed_records_str)
        unique_rfp_df = spark.sql(query).withColumn("anomaly_rfp", f.lit(True)).cache()

        return unique_rfp_df
    except:

        field = [
            StructField('ctl_rfp', StringType(), True),
            StructField('anomaly_rfp', BooleanType(), True),
        ]

        empty_schema = StructType(field)
        res_df = spark.createDataFrame([], empty_schema)
        return res_df
```
* Función que se encarga de obtener la **anomaly_rfp** esto de acuerdo a los datos del cr_rci_processed_records, se hace un left de lo nuevo contra lo existente para validar cual es nuevo y cual no, y asi agregar dicha columna en un formato boolean

```python
def val_rfp_anomaly(cr_rci_anomalies_df):
    get_historic_rfp_df = get_historic_rfp()
    anomaly_join_df = broadcast(cr_rci_anomalies_df).join(get_historic_rfp_df, ["ctl_rfp"], how='left').cache()
    anomaly_df = anomaly_join_df.fillna({'anomaly_rfp': False}).drop("ctl_rfp").cache()
    return anomaly_df
```

* Función que se encarga de borrar una tabla dada desde el hdfs y en sql, esto se le aplica a la tabla de asset trace, para cada procesamiento, es por eso que en cada nuevo procesamiento primero se borra la tabla, despues con el fill trace se llena con los datos mas recientes hasta ese momento de los props y bids by source esto para seguir manteniendo el treca de los id y acn, y al final se llena con los datos entrante de la fuente y su evaluación correspondiente por el engine

```python
def delete_path(spark, db, table):

    path = "hdfs://attdatalakehdfs/user/hive/warehouse/%s.db/%s"%(db,table)
    drop_table_query = "drop table %s.%s"%(db,table)

    sc = spark.sparkContext
    fs = (sc._jvm.org
          .apache.hadoop
          .fs.FileSystem
          .get(sc._jsc.hadoopConfiguration())
          )

    fs.delete(sc._jvm.org.apache.hadoop.fs.Path(path), True)
    spark.sql(drop_table_query)
```


* Declaración de los udf's

```python
str_similar_udf = udf(str_similar, DoubleType())
lst_cluster_udf = udf(lst_cluster_k_means, ArrayType(StringType()))
recursive_zero_eval_udf = udf(recursive_zero_eval, StringType())
find_element_udf = udf(find_element, IntegerType())
clean_str_udf = udf(clean_str, StringType())
homologate_columns_date_udf = udf(homologate_columns_date, StringType())
find_element_set_udf = udf(find_element_set, LongType())
acn_hash_udf = udf(acn_hash, StringType())
validate_field_udf = udf(validate_field, BooleanType())
logic_clean_udf = udf(logic_clean, BooleanType())
concat_date_udf = udf(concat_date, IntegerType())
search_metada_udf = udf(search_metada, MapType(StringType(), StringType()))
generate_acn_udf = udf(generate_acn, StringType())
get_type_udf = udf(get_type, StringType())
lst_to_set_size_udf = udf(lst_to_set_size, IntegerType())
lst_to_set_udf = udf(lst_to_set, ArrayType(StringType()))
get_group_id_udf = udf(get_group_id, StringType())
get_last_ctl_rid_udf = udf(get_last_ctl_rid, StringType())
udf_clean_values = udf(clean_values, StringType())
#New udf's
fix_locs_udf=udf(fix_locs,StringType())
missing_location_udf = udf(missing_location,BooleanType())
search_cat_udf = udf(search_in_cat, StringType())
udf_check_model_missing = udf(check_model_missing, BooleanType())
udf_check_model_generic = udf(check_model_generic, BooleanType())

schema = StructType([
    StructField("count", IntegerType(), True),
    StructField("elements",  ArrayType(StringType()), True),
])
get_anomaly_udf = udf(get_anomaly,schema )
```

* Declaración de las variables constantes utilizadas

```python
cts_lst = [
    'id',
    'acn',
    "concat",
    'ctl_rid',
    'ctl_sid',
    'ctl_file_date',
    'ctl_eid',
    'ctl_file_name',
    'ctl_tid',
    'ctl_ts',
    'ctl_rfp',
    'count']

ctl_cols_lst = [
    "ctl_rid",
    "ctl_rfp",
    "ctl_ts",
    "ctl_file_name",
    "ctl_tid",
    "ctl_sid",
    "ctl_file_date",
    "ctl_eid"
]

order_trace_lst = [
            'id',
            'acn',
            "concat",
            'count',
            'col_name',
            'value',
            'type',
            'source_id',
            'created_by',
            'created_on',
            'found',
            'traceable']

dirt_props = [
    "no visible",
    "no aplica",
    "#na",
    "na",
    "n/a",
    "#n/a",
    "n-a",
    "#n-a",
    "novisible",
    "noaplica",
    "no",
    None,
    "null",
    ""]

ctl_cols_str = ",".join(ctl_cols_lst)
get_timestamp = get_time()
created_on = get_timestamp
```

# Funciones principales y core del asset engine

* Función que se encarga de obtener los bid's y prop's de cada fuente de acuerdo al mapeo dado en las tablas de kudu las cuales son : **lnk_rci_asset_properties** , **cfg_rci_table** , **cg_business_identifiers** , **cg_rci_asset_properties** , **lnk_business_identifiers**, se obtienen los mapeos por dicha fuente y se le aplican filtros de validación si los mapeos existen como columnas en la fuente, además que retorna el query de acuerdo a dichos mapeos para generar el df al momento de cargar la tabla fuente

```python
def get_bid_props():

    global columns_list, list_match, lst_source_bi, lst_source_prop, source_id, cycle_stage, lst_union, lst_items_asset_names, lst_dict_bi
    global lid, cts_lst, lst_dict_all, lst_all_asset_names, lst_filter, lst_dict_prop, spark , anomaly_upper , dirt_lower
    global created_by , ctl_eid, cr_rci_asset_identifiers_str , cr_rci_asset_identifiers_gral_str , cr_rci_asset_properties_gral_str , cr_rci_asset_properties_str, cr_rci_anomalies_str,cr_rci_ae_processed_sources_str , cr_rci_asset_events_str, cr_rci_processed_records_str, cr_rci_asset_group_str, asset_trace_table_str, cg_rci_asset_master_str, source_table_name_str

    spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cfg_rci_table'}).load().cache().createOrReplaceTempView("cg_source")
    spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_rci_business_identifiers'}).load().cache().createOrReplaceTempView(
        "cg_business_identifiers")
    spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_rci_asset_properties'}).load().cache().createOrReplaceTempView("cg_properties")
    spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.lnk_rci_business_identifiers'}).load().cache().createOrReplaceTempView(
        "lnk_business_identifiers")
    spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.lnk_rci_asset_properties'}).load().cache().createOrReplaceTempView("lnk_properties")

    query_row_data_source = "select * from cg_source where table_name = '%s' " % (source_table.replace("dev_",""))
    lst_row_data_source = spark.sql(query_row_data_source).collect()
    source_id = str(lst_row_data_source[0]['ctl_tid'])
    cycle_stage = str(lst_row_data_source[0]['lifecycle'])

    query_bi = "select s.table_name,s.lifecycle , cbi.bid_name ,cbi.evaluation_order , lbi.id , lbi.ctl_tid , lbi.bid_id , lbi.bid_source_col_name   from cg_source s  inner join lnk_business_identifiers lbi on s.ctl_tid = lbi.ctl_tid inner join cg_business_identifiers cbi on cbi.id = lbi.bid_id   where s.table_name= '%s' " % (source_table.replace("dev_",""))
    bi_table_df = spark.sql(query_bi).cache()
    #Modified by Eduardo
    query_prop = "select s.table_name,s.lifecycle , cprop.prop_name ,  lprop.id , lprop.ctl_tid, lprop.prop_id, lprop.prop_source_col_name, lprop.required from cg_source s    inner join lnk_properties lprop on s.ctl_tid = lprop.ctl_tid inner join cg_properties cprop on cprop.id = lprop.prop_id   where s.table_name= '%s' "% (source_table.replace("dev_",""))
    prop_table_df = spark.sql(query_prop).cache()

    query_describe = "describe %s" % (source_table_name_str)
    describe_table_df = spark.sql(query_describe).cache()
    lst_describe_collect = describe_table_df.select("col_name").collect()
    lst_table_source_columns = list(map(lambda x: str(x[0].upper()), lst_describe_collect))
    #Modified by Eduardo
    lst_prop = prop_table_df.select("prop_name", "prop_source_col_name", 'id', 'ctl_tid','prop_id','required').collect()
    lst_dict_prop = list(map(
        lambda x: {"source_col_name": str(x.prop_source_col_name).upper(), "asset_name": str(x.prop_name).upper(),
                   "lnk_column_id": str(x.id), "source_id": str(x.ctl_tid), "cg_prop_id": str(x.prop_id),
                   "type": 'prop', "required":str(x.required)}, lst_prop))

    lst_bi = bi_table_df.select("bid_name", "bid_source_col_name", 'id', 'ctl_tid', 'bid_id','evaluation_order').collect()
    lst_dict_bi = list(map(
        lambda x: {"source_col_name": str(x.bid_source_col_name).upper(), "asset_name": str(x.bid_name).upper(),
                   "lnk_column_id": str(x.id), "source_id": str(x.ctl_tid), "cg_prop_id": str(x.bid_id), "evaluation_order":int(x.evaluation_order),
                   "type": 'bi'}, lst_bi))

    lst_dict_all = lst_dict_bi + lst_dict_prop
    lst_filter = list(filter(lambda x: x['source_col_name'] in lst_table_source_columns, lst_dict_all))
    lst_alias = list(map(lambda x: "%s as %s" % (x['source_col_name'], x['asset_name']) if x['type'] == 'bi' else "%s as %s" % (x['source_col_name'], x['asset_name']), lst_filter))
    str_alias = ",".join(lst_alias)
    query_load_raw_table = "select %s,%s  from %s_clean where ctl_eid = '%s'" % (str_alias, ctl_cols_str, source_table_name_str, ctl_eid)
    return query_load_raw_table
```

* Función cerebro del asset engine, es el que se encarga de clasificar los elemntos de la fuente, es una función recursiva ya que se evaluan de acuerdo a una lidta bid, y con respecto a esa lista se realiza la evaución; lo que se trata esta función es de que le pasas la fuente que se va a evaluar y de acuerdo al cricterio de la blista de bids y de su map, es como se van a evaluar, durante la evaluación se van haciendo comparaciones contra los datos que se ecnuentren el asset trace, es por eso que previamente en el proceso en el fill trace se llena una parte del asset trace, para mantener el trace de id y acn y utilizarce en estas evaluacion, como tal las comparaciones son join de acuerdo a acada bid de la lista dadd, y de ese join se ontienen si el registro con ese campo ya xiste se le registra los id y acn encontrado para ese registro de acuerdo al bid que se este evaluando, un registro puede tener muchos id y acn que le pertenecen, ya que el algoritmo dado  asi funciona busca de acuerdo a los bid y los que se haga match se obtienen y al registro se le asignan todos los id's y acn's encontrados para ese row, y en ese monemnto se escribe el el asset trace con motivo de que esos rows evaluados de la fuente y que ya fueron clasificados ya sea coo nuevos o existentes se encuentran disponible para la siguente evaluación ya que como se comentaba es recursiva de acuero al map de sus bid's.

```python
def asset_engine(df, lst):

    global columns_list, list_match, lst_source_bi, lst_source_prop, source_id, cycle_stage, lst_union, lst_items_asset_names, lst_dict_bi
    global lid, cts_lst, lst_dict_all, lst_all_asset_names, lst_filter, lst_dict_prop, spark , anomaly_upper , dirt_lower
    global created_by , ctl_eid, cr_rci_asset_identifiers_str, cr_rci_asset_identifiers_gral_str , cr_rci_asset_properties_gral_str , cr_rci_asset_properties_str, cr_rci_anomalies_str,cr_rci_ae_processed_sources_str,  cr_rci_asset_events_str, cr_rci_processed_records_str, cr_rci_asset_group_str, asset_trace_table_str, cg_rci_asset_master_str, source_table_name_str

    size_lst = len(lst)

    if size_lst > 0:

        head, tail = (lambda lst: (lst[0], lst[1:]))(lst)
        if head:

            head_bi_name = head['asset_name']
            str_where = 'validate_%s' % (head_bi_name)
            lst_filter_engine = list(filter(lambda x: x not in head_bi_name, lst_union)) + ctl_cols_lst + ['count',"concat"]
            lst_collect = list(map(lambda x: "collect_list(%s) as %s" % (x, x), lst_filter_engine))
            str_collect = ",".join(lst_collect)
            lst_select_col = list(map(lambda x: "col.%s" % (x), lst_filter_engine))

            df.createOrReplaceTempView("tmp_%s_table" % (head_bi_name))

            str_query_source = 'select %s  , %s from %s where %s = True group  by %s' % (head_bi_name, str_collect, 'tmp_%s_table' % (head_bi_name), str_where, head_bi_name)

            unique_group_df = spark.sql(str_query_source).cache()
            empty = unique_group_df.rdd.isEmpty()
            if empty == True:
                return asset_engine(df, tail)

            ## asste trace
            str_col_head = head_bi_name

            asset_trace_table_df = get_last_asset_trace(asset_trace_table_str, str_col_head).cache()

            look_df = broadcast(unique_group_df) \
                .join(asset_trace_table_df, unique_group_df[head_bi_name] == asset_trace_table_df[head_bi_name], how='left') \
                .select(unique_group_df['*'], asset_trace_table_df.id, asset_trace_table_df.acn).distinct().persist()

            new_df = look_df.where(f.col("id").isNull()).drop("id", 'acn') \
                .withColumn("acn", generate_acn_udf()) \
                .withColumn('id', acn_hash_udf(f.col(head_bi_name), lit(head_bi_name))) \
                .select(head_bi_name, "id", "acn", explode_outer(arrays_zip(*lst_filter_engine))) \
                .select(head_bi_name, "id", "acn", *lst_select_col).cache()

            found_df = look_df.where(f.col("id").isNotNull()) \
                .withColumn("explode", f.explode(f.arrays_zip(*["id", "acn"]))).drop("id", 'acn') \
                .select("*", "explode.id", "explode.acn") \
                .select(head_bi_name, "id", "acn", explode_outer(arrays_zip(*lst_filter_engine))) \
                .select(head_bi_name, "id", "acn", *lst_select_col).cache()

            union_df = new_df.union(found_df).cache()

            complete_tabular_df = union_df.alias("complete_tabular_df").cache()

            ### column model
            lst_group_cols = ['id', 'acn' , 'count',"concat"]
            lst_cols = [head_bi_name] + lst_filter_engine
            lst_cols_stk = [x for x in lst_cols if x not in lst_group_cols]

            columnar_df = create_columnar_model(complete_tabular_df, lst_cols_stk).checkpoint(False)

            columnar_df.coalesce(10) \
                .withColumn("found", lit(head_bi_name)) \
                .withColumn("traceable", lit(1)) \
                .select(*order_trace_lst) \
                .write.format("parquet").mode("append") \
                .saveAsTable(asset_trace_table_str)

            temp_str = "%s_temp"%(head_bi_name)
            tab_df = complete_tabular_df.alias("tab_df").withColumnRenamed(head_bi_name, temp_str).cache()
            haulage_df = df.join(tab_df, df[head_bi_name] == tab_df[temp_str], how='leftanti').persist()

            return asset_engine(haulage_df, tail)
    else:
        return df
```

* Función main es como el main de java, se encarga de orquestar y darle orden a cada una de las ejecuciones, en sta funcion se inicia la sesión de spark y se procede a utilizar ciertas funciones y udf's explicadas anterioremnte, e igualmente tiene un orden para generar las tablas ya que en algunos puntos se necesitan que se encuentren cargadas ciertas tablas pra poder generar el resultado de la función que se le paso, es como una codependencia entre ellas es por eso que se tiene u orden, tambien en esta función se cachan los logs que se esciben, tambien durante todo el codigo se hace uso de variables globales, los Df principales son: el DF de la fuente, el DF del asset trace en tabular y el DF del asset trace en columnar, estos sirven como la entrada para las funciones de pendiendo de cada función cual utilice ya sea el df del asset en formato tabular o columnar, el tabular solo contiene el asset trace pero lo recien evaluado, y el columnar obtienen todo el asset tarce que se escribio, estos DF del asset trace son los principales DF; e igualmente la tabla de la fuente pasa por el algoritmo del asset_engine el cual lo lasifica y lo escribe en el asset trace, esto se hace anstes de cargar las tablas columnar y taular del asset trace, para que cuando se ejecuten las unciones que generan el tabular y columnar se tenga ya un trace completo

```python
def main():

    global columns_list, list_match, lst_source_bi, lst_source_prop, source_id, cycle_stage, lst_union, lst_items_asset_names, lst_dict_bi
    global lid, cts_lst, lst_dict_all, lst_all_asset_names, lst_filter, lst_dict_prop, spark , anomaly_upper , dirt_lower
    global created_by , ctl_eid, cr_rci_asset_identifiers_str, cr_rci_asset_identifiers_gral_str , cr_rci_asset_properties_gral_str , cr_rci_asset_properties_str, cr_rci_anomalies_str, cr_rci_ae_processed_sources_str , cr_rci_asset_events_str, cr_rci_processed_records_str, cr_rci_asset_group_str, asset_trace_table_str, cg_rci_asset_master_str, source_table_name_str

    spark = SparkSession.builder.appName('asset_engine_dev') \
        .config("spark.hadoop.validateOutputSpecs", "false") \
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
        .config("hive.exec.dynamic.partition", "true") \
        .config("hive.exec.dynamic.partition.mode", "nonstrict") \
        .config("spark.sql.avro.compression.codec", "snappy") \
        .config("spark.speculation", "false") \
        .config("yarn.resourcemanager.am.max-attempts", "1") \
        .getOrCreate()

    sc = spark.sparkContext
    spark_id = sc.applicationId
    sc.setCheckpointDir("hdfs://attdatalakehdfs/user/raw_rci/Pyspark/tmp")

    print "Invocar funcion para enviar correo"
    mail_environment='dev'
    mail_type="start" #Manda correo notificando el inicio de la ejecución
    send_notification(mail_environment, mail_type, source_database, source_table)
	
    kudu_cg_anomalies_df = spark.read.format('org.apache.kudu.spark.kudu') \
        .options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_anomalies'}) \
        .load()

    kudu_cg_clean_patterns_df = spark.read.format('org.apache.kudu.spark.kudu') \
        .options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_clean_patterns'}) \
        .load()

    cg_clean_patterns_df = kudu_cg_clean_patterns_df.select("text_pattern").cache()
    cg_clean_patterns_lst = cg_clean_patterns_df.collect()
    dirt_lower = list(map(lambda x: str(x["text_pattern"].encode('ascii', 'ignore')).lower(), cg_clean_patterns_lst)) + [None]

    cg_anomalies_df = kudu_cg_anomalies_df.select("text_anomaly").cache()
    cg_anomalies_lst = cg_anomalies_df.collect()
    anomaly_upper = list(map(lambda x: str(x["text_anomaly"].encode('ascii', 'ignore')).upper(), cg_anomalies_lst))

    ## get bid, props , query
    query_load_raw_table = get_bid_props()
    write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "asset engine process","START")

    raw_df = spark.sql(query_load_raw_table).checkpoint(False)
    raw_df = search_vendor(raw_df).checkpoint(False)
    stg_tbl = "%s_tmp_stg" % (source_table_name_str.split(".")[1])
    raw_df.createOrReplaceTempView(stg_tbl)
    collect_ctl_cols_lst = list(map(lambda x: "collect_list(%s) as %s" % (x, x), ctl_cols_lst))
    collect_ctl_cols_str = ",".join(collect_ctl_cols_lst)
    str_alias_tmp = reduce(lambda x, y: "%s,%s" % (x, y), list(map(lambda x: x['asset_name'], lst_filter)) )
    query_stg_load_table = "select %s, %s  , count(*) as count from %s group by %s" % (str_alias_tmp, collect_ctl_cols_str, stg_tbl, str_alias_tmp)
    source_complete_df = spark.sql(query_stg_load_table).checkpoint(False)

    lst_source_bi = list(map(lambda x: x['asset_name'],  list(filter(lambda x: x['type'] == 'bi', lst_filter)) ))
    lst_source_prop = list(map(lambda x: x['asset_name'], list(filter(lambda x: x['type'] == 'prop', lst_filter)) ))
    lst_union = lst_source_bi + lst_source_prop

    source_validate_load_df = recursive_lst_validate(source_complete_df, lst_source_bi).withColumn("concat",f.concat_ws(",",*lst_union)).checkpoint(False)

    lst_filter_join_sort = sorted( list(filter(lambda x: x['type'] == 'bi', lst_filter)) , key=lambda i: i['evaluation_order'])

    ## get tables
    db_tables = spark.sql("show tables in %s" % (source_database)).select("tableName").collect()
    lst_tables = list(map(lambda x: source_database+"." + str(x['tableName']), db_tables))

    ## fill asset trace
    try:
        asset_data = asset_trace_table_str.split(".")
        delete_path(spark, asset_data[0], asset_data[1])
    except:
        pass

    fill_trace_df = fill_trace().persist()

    fill_trace_df.select(*order_trace_lst) \
        .write.format("parquet")\
        .mode("overwrite")\
        .saveAsTable(asset_trace_table_str)

    ## Asset Engine
    write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_asset_trace", "START")
    try:
        rest_asset_engine_df = asset_engine(source_validate_load_df, lst_filter_join_sort)
        ## No traceable
        ##no_traceable(rest_asset_engine_df.alias("no_traceable_df") )
    except Exception as excep:
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_asset_trace","ERROR:%s" % (excep))
        raise Exception("Exception: " + str(excep))
    write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_asset_trace", "END")

    ## LOAD ASSET TRACE
    asset_trace_created_on_df = spark.sql("select * from %s where created_on = '%s' " % (asset_trace_table_str,created_on))
    tabular_asset_model = get_tabular_asset(asset_trace_created_on_df)

    if tabular_asset_model is not None:

        tabular_asset_model_df = tabular_asset_model.cache()

        asset_trace_all_df = spark.sql("select * from %s  " % (asset_trace_table_str)).checkpoint(False)

        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_group", "START")
        try:
            cr_rci_asset_group(tabular_asset_model_df)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_group","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_group", "END")

        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cg_rci_asset_master", "START")
        try:

            master_temp_df = get_asset_master()
            cg_rci_asset_master_all_df = cg_rci_asset_master(asset_trace_all_df)
            cg_rci_asset_master_df = cg_rci_asset_master_all_df.join(master_temp_df, ["id", "acn"],how='leftanti').cache()
            cg_rci_asset_master_df.write.format("parquet").mode("append") \
                .saveAsTable(cg_rci_asset_master_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "asset cg_rci_asset_master","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cg_rci_asset_master", "END")

        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_identifiers","START")
        try:

            if cr_rci_asset_identifiers_str not in lst_tables:
                sql = "CREATE TABLE %s (id STRING,acn STRING,bid STRING,value STRING , count BIGINT,created_by STRING,created_on STRING ) PARTITIONED BY (ctl_tid STRING ) STORED AS PARQUET" % (
                    cr_rci_asset_identifiers_str)
                spark.sql(sql)

            cr_rci_asset_identifiers_df = cr_rci_asset_identifiers(asset_trace_all_df)
            cr_rci_asset_identifiers_df.write.partitionBy("ctl_tid").format("hive").mode("overwrite") \
                .saveAsTable(cr_rci_asset_identifiers_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_identifiers","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_identifiers","END")

        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_properties","START")
        try:

            if cr_rci_asset_properties_str not in lst_tables:
                sql = "CREATE TABLE %s (id STRING,acn STRING,prop STRING,value STRING,count BIGINT,created_by STRING, created_on STRING) PARTITIONED BY (ctl_tid STRING ) STORED AS PARQUET" % (
                    cr_rci_asset_properties_str)
                spark.sql(sql)

            cr_rci_asset_properties_df = cr_rci_asset_properties(asset_trace_all_df)
            cr_rci_asset_properties_df.write.partitionBy("ctl_tid").format("hive").mode("overwrite") \
                .saveAsTable(cr_rci_asset_properties_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_properties","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_properties", "END")

        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_events", "START")
        try:
            cr_rci_asset_events_df = cr_rci_asset_events(tabular_asset_model_df)
            #Line of Code add by Eduardo
            cr_rci_asset_events_df_2 = cr_rci_asset_events_fixed(cr_rci_asset_events_df)
            cr_rci_asset_events_df_2.write.format("parquet").mode("append") \
                .saveAsTable(cr_rci_asset_events_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_events","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_events", "END")

        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_anomalies", "START")
        try:
            cr_rci_anomalies_rfp_df = cr_rci_anomalies(tabular_asset_model_df)
            cr_rci_anomalies_df = val_rfp_anomaly(cr_rci_anomalies_rfp_df).cache()

            #Line of Code add by Eduardo
            cr_rci_anomalies_df_2 = cr_rci_anomalies_fixed(cr_rci_anomalies_df)
            cr_rci_anomalies_df_2.write.format("parquet").mode("append") \
                .saveAsTable(cr_rci_anomalies_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_anomalies","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_anomalies", "END")

        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_processed_records","START")
        try:
            cr_rci_processed_records_df = cr_rci_processed_records(tabular_asset_model_df)
            cr_rci_processed_records_df.write.format("parquet").mode("append") \
                .saveAsTable(cr_rci_processed_records_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_processed_records",
                                    "ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_processed_records","END")

        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_acn_mapping", "START")
        try:
            cr_rci_acn_mapping_res = cr_rci_acn_mapping()
            if cr_rci_acn_mapping_res != None:
                cr_rci_acn_mapping_df = cr_rci_acn_mapping_res.cache()
                cr_rci_acn_mapping_df.write.format("parquet").mode("append") \
                    .saveAsTable(cr_rci_acn_mapping_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_acn_mapping","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_acn_mapping", "END")

        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_properties_gral","START")
        try:
            cr_rci_asset_properties_gral()
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by,"cr_rci_asset_properties_gral", "ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_properties_gral","END")

        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_identifiers_gral","START")
        try:
            cr_rci_asset_identifiers_gral()
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by,"cr_rci_asset_identifiers_gral", "ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_identifiers_gral","END")

    else:
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "empty source", "ERROR")

    write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "asset engine process", "END")

    try:
        source_clean = source_table_name_str.split(".")
        delete_path(spark, source_clean[0], "%s_clean"%(source_clean[1]))
    except:
        pass

    print "Invocar funcion para enviar correo"
    mail_environment='dev'
    mail_type="end" #Manda correo notificando el inicio de la ejecución
    send_notification(mail_environment, mail_type, source_database, source_table)
	
    spark.stop()
```
<<<<<<< HEAD
=======
>>>>>>> 86a4d6d... doc readme del asset engine
>>>>>>> fe04ddc... Solving merge issues
