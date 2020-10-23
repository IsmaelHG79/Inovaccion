#!/usr/bin/env python
# coding: utf-8
#####################################################################################################################################################
# # Creación del Dominio FINANZAS
#####################################################################################################################################################
# El dominio Finanzas se define como todos los datos que se refieren a la administración del dinero de la compañía, estos incluyen actividades como gastos, inversiones, préstamos, presupuestos y desempeño de proyectos.
# El diseño de este código de creación se detalla en el documento *Diseño del pipeline de Finanzas*.
# 
# Empresa:          Axity
# Elaborado por:    Erick Rubio
# Version:          1.0
# Proyecto:         Reconciliación de inventarios
#####################################################################################################################################################


# ### A. Importar librerias

import os
import sys
import hashlib
import re
import findspark
findspark.init()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql import functions as F
from functools import reduce
from pyspark.sql.types import *
from pyspark.sql import HiveContext
from pyspark.sql import Row
from pyspark.sql.functions import lower,arrays_zip,explode,explode_outer, col, split, regexp_extract, array_contains, regexp_replace, concat_ws, create_map, create_map, lit
import pyspark.sql.functions as f
from pyspark.sql.functions import size
from pyspark.sql.functions import concat_ws
from pyspark.sql.functions import split, trim
from pyspark.sql.functions import first
from pyspark.sql.functions import udf
from pyspark.sql.types import LongType
from pyspark.sql.types import StringType ,BooleanType
from pyspark.sql.functions import map_keys,map_values
from pyspark.sql.functions import when, sum, avg, col
from pyspark.sql.functions import concat
from pyspark.sql import types as T
from functools import partial 
from pyspark.sql.functions import substring, length, col, expr
from pyspark.sql import DataFrame
from pyspark.sql import functions
from datetime import datetime
from pyspark.sql.functions import desc, row_number, monotonically_increasing_id


# ### B. Creación de funciones definidas (UDF)

dirt=['no visible', 'sin etiqueta', 'ni visible', 'n/v','nv','ilegible','n/a', 's/a', 'na','no legible', 'no cuenta con activo fijo', \
          'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene','no visble', \
          'no viaible', '.fhy', 'bxfj', 'cambiar la foto', 'hdjdjjdjfjfj', 'hdjrnnfjfjf', 'hffhthjih', 'hhyhigch', \
          'hswkwjj', 'no aplica', 'no pude borrar elemnto', 'ns no visible', 'sin serie', 'sitio ibs no aplica', 'tutj', \
          'uflp serie no visible', 'xxxxxxx', 'hsid# djdncg', 'sin informacion disponible', 'no tiene numero de serie', \
          'hdkoe kg udkke' 'no se ve', 'ninguna', 'no tiene etiqueta y no se alcnaza a ver.', 'fue un error', \
          'no legible', 'sin etiqueta', 'no disponible', 'no tiene', 'sin datos', 'num de serie no legible', 'etiqueta no legible', 'no cuenta con numero de serie', \
          'no aplica por error se selecciona una tarjeta mas', 'enviado ya en reporte anterior', 'hlk', 'ninguno', 'la antena no tiene etiqueta por lo tanto tampoco numero de serie', 'no leguible', \
          'sin targeta (por equivocacion se agrego este eslot 18 )', 'no cuenta con numeros de serie', 'enviados en reporte anterior .', 'sin etiqueta de numero de serie', \
          'sin numero', 'sin informacion disponible', 'sin acceso a la antena', 'no tiene serie', 'sin acceso', 'no se pudo sacar ya que esta clausurado el sitio', \
          'no se hizo por que no tenemos tarjeta se las llevo el ing de huawei gabriel lopez', 'sin informacion disponible', 'no aplica ta este segmento', \
          'sin numero de serie visible', 'enviada en reporte  anterior', 'no hay antena', 'no se pudo sacar ya que esta clausurado y nos sacaron de sitio', \
          'sin serie falta etiqueta', 'sin numero de serie no cuenta con la etiqueta', 'no tiene etiqueta', 'no existe', 'no serie visible', 'no hay bbu esta en resguardo por el ing gabriel lopez', \
          'no legible', 'na', 'na hay  tarjeta', 'sin acceso al numero de serie', 'no visibles', 'uelp serie no visible', 'sin informacion disponible', 'sin tarjeta', 'fue un error de dedo no ay mas slot', \
          'codigo no visible', 'num de serie no visible', 'sin informacion', 'no se aprecia el codigo', 'sin numero de serie', 'no trae la etiketa de numero de serie', \
          'no aplica.', 'no se pudo sacar el numero  de serie ya q nos sacaron del sitio ya q esta clausurado', 'no tiene serie visible', 'no tiene serial ala vista', \
          'no se tiene acceso a la antena', 'etiqueta no visible', 'no se puede tomar la foto porque tenemos la fan', 'n/a  no se instalan antenas', 'no aplica sitio ibs', \
          'sin numero', 'kcuvicuv', 'error no hay mas', 'no se puede apreciar el codigo', 'no aplica es ibs.', 'no  cuenta con etiquetas de n/s', 'esta ultima no vale', \
          'no hay tarjeta', 'esta no vale', 'falta','NOVSIBLE','INACCESIBLE','Novisible','#N/A', '$']


dirt_upper = map(lambda x: x.upper() , dirt)


# Creación de columna de Hash
def acn_hash(column):
    column_str =u''.join(column+"").encode('ascii', 'ignore').strip()
    result = hashlib.md5(column_str.encode()).hexdigest()
    return result


# Función de limpieza para campos tipo string
def clean_str(string):
    temp = ""
    if string != None :
        temp = string
    str_clean_1  = re.sub("[,;:{}()\\n\\t=]","",temp.encode("utf-8"))
    str_clean_2 = str_clean_1.replace("Á","A").replace("É","E").replace("Í","I").replace("Ó","O").replace("Ú","U")
    return str_clean_2


def clean_numbers(string):

    str_clean_1  = string.replace(" ","")
    res =re.match("[()]", str_clean_1)
    if res:
        no = "-"+re.sub("[()]","",str_clean_1.encode("utf-8"))
        return no
    else :
        return string.replace(" ","")


def dash_as_empty(x):
    d = '-' 
    return when(col(x) != d, col(x)).otherwise("")


def flag_trazable(string1, string2):
    return when((length(col(string1)) == 0) & (length(col(string2)) == 0), 0).otherwise(1)


# Función de limpieza genérica para campos de métricas
def clean_float(string):
    temp = ""
    if string != None :
        temp = string
    str_clean = re.sub("[,;:{}()\\n\\t=]","",temp.encode("utf-8"))
    return str_clean


def get_time():
    dateTimeObj = datetime.now()
    year = dateTimeObj.year
    month = "0%s"%(dateTimeObj.month) if len("%s"%(dateTimeObj.month)) == 1 else "%s"%(dateTimeObj.month)
    day = "0%s"%(dateTimeObj.day) if len("%s"%(dateTimeObj.day)) == 1 else "%s"%(dateTimeObj.day)
    hour = "0%s"%(dateTimeObj.hour) if len("%s"%(dateTimeObj.hour)) == 1 else "%s"%(dateTimeObj.hour)
    minute = "0%s"%(dateTimeObj.minute) if len("%s"%(dateTimeObj.minute)) == 1 else "%s"%(dateTimeObj.minute)
    second = "0%s"%(dateTimeObj.second) if len("%s"%(dateTimeObj.second)) == 1 else "%s"%(dateTimeObj.second)
    str_date = "%s-%s-%s"%(year, month ,day)
    str_time = "%s:%s:%s.%s"%(hour ,minute,second,dateTimeObj.microsecond)
    return str_date+' '+str_time


def main():

    spark = SparkSession \
        .builder.appName("Dominio_de_Propiedades") \
        .config("spark.yarn.queue", "root.eda") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.executor.instances", "4") \
        .config("spark.executor.cores", "5") \
        .config("spark.driver.memory", "8g") \
        .config("spark.executor.memory", "8g") \
        .config("spark.sql.tungsten.enabled", "true") \
        .config("spark.io.compression.codec", "snappy") \
        .config("spark.sql.crossJoin.enabled", "true") \
        .config("spark.kryoserializer.buffer.mb", "128") \
        .config("spark.sql.autoBroadcastJoinThreshold", -1) \
        .config("spark.sql.shuffle.partition", "2001") \
        .config("spark.shuffle.compress", "true") \
        .config("spark.shuffle.spill.compress", "true") \
        .config("spark.jars", "/home/raw_rci/jars/kudu-spark-tools-1.4.0.jar") \
        .getOrCreate()


    df_extkudu = spark.read.format('org.apache.kudu.spark.kudu') \
                    .options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx:7051', 'kudu.table':'impala::rci_network_db.dm_propiedades_test'}) \
                    .load().select(col("idk").alias("idk_old"), col("ida").alias("ida_old"), col("fecha_ins").alias("fecha_ins_old")).cache()

    df_old = df_extkudu.count()

    # Creación de funciones definidas por el usuario:

    clean_str_udf = udf(clean_str, StringType())
    clean_float_udf = udf(clean_float, FloatType())
    acn_hash_udf = udf(acn_hash,StringType())
    udf_SysDate = get_time()
    clean_numbers_udf = udf(clean_numbers, StringType())


    # ### C. Procesamiento

    df_timestart = udf_SysDate


    # ### 1. Importar datos desde el Data Lake

    # **CIP Finanzas:**


    df_cip = spark.sql("SELECT         numeroetiqueta AS etiqueta,         numeroserie AS serie,         articulo,         areaok AS cip_areaok,         categoria,         categoriamastplann AS cip_categoriamastplann,         categoriamastercipbudget AS cip_categoriamastercipbudget,         categoria_budget1_jc AS cip_categoria_budget1_jc,         categoria_budget2_jc AS cip_categoria_budget2_jc,         conspolsaldocuentas,         consecpapeldetrabajo,         cuenta,         days AS cip_days,         dias AS cip_dias,         id,         legalentity,         libro,         mxn,         noubicado AS cip_noubicado,         nofactura,         notransaccion,         nuevooenproceso,         ordendecompra,         parametrosdays,         polizacap AS cip_polizacap,         ref AS cip_ref,         subarea,         sub_cta AS cip_sub_cta,         tarea,         tc as cip_tc,         tc18 as cip_tc18,         tc20 AS cip_tc20,         tipocuenta AS cip_tipocuenta,         ubicado AS cip_ubicado,         unidades AS cip_unidades,         units_assigned,         usd,         valid,         column_year AS cip_column_year,         oracle as id_oracle,         obsv as cip_observaciones,         disponiblesgermanluna as cip_disponiblesgermanluna,         controldecambiosenproceso as cip_controldecambiosenproceso,         month,         year,         filedate,         filename     FROM rci_network_db.tx_finance_cip ")


    # **Activo Fijo:**


    df_af = spark.sql("SELECT         serie,         activo,         etiqueta,         codigo_del_articulo as articulo,         unidades as unidades,         oc,         vnl_del_activo_mxn,         vnl_asignado_mxn,         filedate,         filename         FROM rci_network_db.tx_fixed_asset         ")


    # ### 2. Unión de tablas


    df_dataframes = [df_cip, df_af]


    cols = set()
    for df in df_dataframes:
        for x in df.columns:
            cols.add(x)
    cols = sorted(cols)


    dfs = {}
    for i, d in enumerate(df_dataframes):
        new_name = 'df' + str(i)
        dfs[new_name] = d
        for x in cols:
            if x not in d.columns:
                dfs[new_name] = dfs[new_name].withColumn(x, lit(""))
        dfs[new_name] = dfs[new_name].select(cols)


    df_union = dfs['df0']
    dfs_to_add = dfs.keys()
    dfs_to_add.remove('df0')
    for x in dfs_to_add:
        df_UnionAll = df_union.union(dfs[x])

    df_UnionAll.cache()

    # ### 3. Limpieza de datos

    # Convertir a mayúsculas
    df_mayus = df_UnionAll.withColumn("activo",trim(F.upper(F.col("activo")))). \
        withColumn("articulo",trim(F.upper(F.col("articulo")))). \
        withColumn("cip_areaok",trim(F.upper(F.col("cip_areaok")))). \
        withColumn("cip_categoria_budget1_jc",trim(F.upper(F.col("cip_categoria_budget1_jc")))). \
        withColumn("cip_categoria_budget2_jc",trim(F.upper(F.col("cip_categoria_budget2_jc")))). \
        withColumn("cip_categoriamastercipbudget",trim(F.upper(F.col("cip_categoriamastercipbudget")))). \
        withColumn("cip_categoriamastplann",trim(F.upper(F.col("cip_categoriamastplann")))). \
        withColumn("cip_days",trim(F.upper(F.col("cip_days")))). \
        withColumn("cip_ref",trim(F.upper(F.col("cip_ref")))). \
        withColumn("cip_tipocuenta",trim(F.upper(F.col("cip_tipocuenta")))). \
        withColumn("conspolsaldocuentas",trim(F.upper(F.col("conspolsaldocuentas")))). \
        withColumn("cuenta",trim(F.upper(F.col("cuenta")))). \
        withColumn("etiqueta",trim(F.upper(F.col("etiqueta")))). \
        withColumn("libro",trim(F.upper(F.col("libro")))). \
        withColumn("nuevooenproceso",trim(F.upper(F.col("nuevooenproceso")))). \
        withColumn("parametrosdays",trim(F.upper(F.col("parametrosdays")))). \
        withColumn("serie",trim(F.upper(F.col("serie")))). \
        withColumn("subarea",trim(F.upper(F.col("subarea")))). \
        withColumn("valid",trim(F.upper(F.col("valid"))))
    df_mayus.cache()

    df_mayus_1 = df_mayus.withColumn("etiqueta", dash_as_empty("etiqueta")) \
        .withColumn("serie", dash_as_empty("serie")) \
        .withColumn("articulo", dash_as_empty("articulo")) \
        .withColumn("cip_areaok", dash_as_empty("cip_areaok")) \
        .withColumn("categoria", dash_as_empty("categoria")) \
        .withColumn("cip_categoriamastplann", dash_as_empty("cip_categoriamastplann")) \
        .withColumn("cip_categoriamastercipbudget", dash_as_empty("cip_categoriamastercipbudget")) \
        .withColumn("cip_categoria_budget1_jc", dash_as_empty("cip_categoria_budget1_jc")) \
        .withColumn("cip_categoria_budget2_jc", dash_as_empty("cip_categoria_budget2_jc")) \
        .withColumn("conspolsaldocuentas", dash_as_empty("conspolsaldocuentas")) \
        .withColumn("consecpapeldetrabajo", dash_as_empty("consecpapeldetrabajo")) \
        .withColumn("cuenta", dash_as_empty("cuenta")) \
        .withColumn("cip_days", dash_as_empty("cip_days")) \
        .withColumn("cip_dias", dash_as_empty("cip_dias")) \
        .withColumn("id", dash_as_empty("id")) \
        .withColumn("legalentity", dash_as_empty("legalentity")) \
        .withColumn("libro", dash_as_empty("libro")) \
        .withColumn("mxn", dash_as_empty("mxn")) \
        .withColumn("cip_noubicado", dash_as_empty("cip_noubicado")) \
        .withColumn("nofactura", dash_as_empty("nofactura")) \
        .withColumn("notransaccion", dash_as_empty("notransaccion")) \
        .withColumn("nuevooenproceso", dash_as_empty("nuevooenproceso")) \
        .withColumn("ordendecompra", dash_as_empty("ordendecompra")) \
        .withColumn("parametrosdays", dash_as_empty("parametrosdays")) \
        .withColumn("cip_polizacap", dash_as_empty("cip_polizacap")) \
        .withColumn("cip_ref", dash_as_empty("cip_ref")) \
        .withColumn("subarea", dash_as_empty("subarea")) \
        .withColumn("cip_sub_cta", dash_as_empty("cip_sub_cta")) \
        .withColumn("tarea", dash_as_empty("tarea")) \
        .withColumn("cip_tc", dash_as_empty("cip_tc")) \
        .withColumn("cip_tc18", dash_as_empty("cip_tc18")) \
        .withColumn("cip_tc20", dash_as_empty("cip_tc20")) \
        .withColumn("cip_tipocuenta", dash_as_empty("cip_tipocuenta")) \
        .withColumn("cip_ubicado", dash_as_empty("cip_ubicado"))\ 
        .withColumn("cip_unidades", dash_as_empty("cip_unidades")) \
        .withColumn("units_assigned", dash_as_empty("units_assigned")) \
        .withColumn("usd", dash_as_empty("usd")) \
        .withColumn("valid", dash_as_empty("valid")) \
        .withColumn("cip_column_year", dash_as_empty("cip_column_year"))

    #Limpieza de campos llave
    df_keys =  df_mayus_1.withColumn("serie_clean", F.col("serie")).replace(to_replace=dirt_upper, value='',subset="serie_clean")                     .withColumn("etiqueta_clean", F.col("etiqueta")).replace(to_replace=dirt_upper, value='',subset="etiqueta_clean")                     .withColumn("articulo_clean", F.col("articulo")).replace(to_replace=dirt_upper, value='',subset="articulo_clean")                     .withColumn("activo_clean", F.col("activo")).replace(to_replace=dirt_upper, value='',subset="activo_clean")                     .withColumn("calc_filedate", df_mayus_1.filedate.cast("Int"))

    #Se cambian las columnas limpias por las anteriores
    df = df_keys.drop("serie").drop("etiqueta").drop("articulo").drop("activo")

    df_1 = df.withColumnRenamed("serie_clean","serie"). \
        withColumnRenamed("etiqueta_clean","etiqueta"). \
        withColumnRenamed("articulo_clean","articulo"). \
        withColumnRenamed("activo_clean","activo")


    df_1 = df_1.withColumn("serie",regexp_replace('serie', '[^0-9a-zA-Z ]', '')).withColumn("etiqueta",regexp_replace('etiqueta', '[^0-9a-zA-Z ]', ''))

    #Limpieza de parentésis, guiones y espacios en blanco

    df_2 = df_1.withColumn("mxn", clean_numbers_udf("mxn")).withColumn("usd", clean_numbers_udf("usd")).withColumn("cip_tc18", clean_numbers_udf("cip_tc18")).withColumn("cip_tc20", clean_numbers_udf("cip_tc20")).withColumn("cip_ubicado", clean_numbers_udf("cip_ubicado"))

    # Casteo registros numéricos
    df_3 = df_2.withColumn("cip_tc", F.col("cip_tc").cast("float")) \
        .withColumn("cip_tc18", F.col("cip_tc18").cast("float")) \+
        .withColumn("units_assigned", F.col("units_assigned").cast("int")) \
        .withColumn("unidades", F.col("unidades").cast("int")) \
        .withColumn("cip_dias", F.col("cip_dias").cast("int")) \
        .withColumn("filedate", F.col("filedate").cast("int")) \
        .withColumn("mxn", F.col("mxn").cast("float"))     .withColumn("usd", F.col("usd").cast("float"))     .withColumn("cip_tc18", F.col("cip_tc18").cast("float"))     .withColumn("cip_tc20", F.col("cip_tc20").cast("float"))     .withColumn("cip_ubicado", F.col("cip_ubicado").cast("float"))



    # ### 4. Transformación de datos y reglas de negocio

    df_id_1 = df_2.withColumn("id_num", monotonically_increasing_id())


    columns_lst_lower = map( lambda x: x.lower(),df_id_1.columns)
    no_lst = ["articulo","serie","etiqueta", "filedate", "id_num"]
    lst_filter = [x for x in columns_lst_lower if x not in no_lst  ]

    df_nonulos = df_id_1.na.fill("",no_lst).na.fill("",lst_filter)

    df_concatkeys = df_nonulos.withColumn("calc_fecha", lit(udf_SysDate)).                 withColumn("calc_idk", F.concat(*no_lst)).                 withColumn("calc_ida", F.concat(*lst_filter))

    df_transrules_1 = df_concatkeys.withColumn("idk", acn_hash_udf("calc_idk")).withColumn("ida", acn_hash_udf("calc_ida")).drop("filedate")
    df_transrules_2 = df_transrules_1.withColumn("fecha_upd", col("calc_fecha")).withColumnRenamed("calc_fecha", "fecha_ins").withColumnRenamed("calc_filedate","filedate")
    df_transrules_3 = df_transrules_2.drop("calc_idk").drop("calc_ida")
    df_transrules_4 = df_transrules_3.withColumn("bandera_trazable", flag_trazable("serie", "etiqueta"))
    df_transrules = df_transrules_4.drop("id_num").cache()
    df_read = df_transrules.count()


    # ### 5. Validar incrementabilidad de los registros

    # df_extkudu = spark.read.format('org.apache.kudu.spark.kudu')         .options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx:7051', 'kudu.table':'impala::rci_network_db.dm_finanzas'}).load()
    # df_extkudu = df_extkudu.select(col("idk").alias("idk_old"), col("ida").alias("ida_old"), col("fecha_ins").alias("fecha_ins_old")).cache()

    # df_extkudu.count()

    df_finanzas = df_transrules.join(df_extkudu, df_transrules.idk == df_extkudu.idk_old, "left_outer")

    df_insert = df_finanzas.where(F.col("idk_old").isNull()).drop("idk_old").drop("ida_old").drop("fecha_ins_old").cache()

    df_ins = df_insert.count()

    df_update = df_finanzas.where(F.col("idk_old").isNotNull()).where(F.col("ida") != F.col("ida_old"))              .drop("idk_old").drop("ida_old").drop("fecha_ins").withColumnRenamed("fecha_ins_old", "fecha_ins").cache()


    df_upd = df_update.count()


    # ### 6. Actualizar registros del Dominio de Finanzas en Kudu



    #### Actualización de registros en parquet


    # ### 7. Insertar registros del Dominio Finanzas en Kudu



    df_insert.write.format('org.apache.kudu.spark.kudu') .options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx:7051', 'kudu.table':'impala::rci_network_db.dm_finanzas'}) .mode("append").save()


    # ### 6. Obtener y registrar cifras control


    dateTimeObj = datetime.now()
    year = dateTimeObj.year
    month = "0%s"%(dateTimeObj.month) if len("%s"%(dateTimeObj.month)) == 1 else "%s"%(dateTimeObj.month)
    day = "0%s"%(dateTimeObj.day) if len("%s"%(dateTimeObj.day)) == 1 else "%s"%(dateTimeObj.day)
    hour = "0%s"%(dateTimeObj.hour) if len("%s"%(dateTimeObj.hour)) == 1 else "%s"%(dateTimeObj.hour)
    minute = "0%s"%(dateTimeObj.minute) if len("%s"%(dateTimeObj.minute)) == 1 else "%s"%(dateTimeObj.minute)
    second = "0%s"%(dateTimeObj.second) if len("%s"%(dateTimeObj.second)) == 1 else "%s"%(dateTimeObj.second)
    str_date = "%s-%s-%s"%(year, month ,day)
    str_time = "%s:%s:%s.%s"%(hour ,minute,second,dateTimeObj.microsecond)
    df_enddate = str_date+' '+str_time
    df_cifras = spark.createDataFrame(
        [
            ("Dominio de Finanzas",df_timestart,df_enddate,df_read,df_ins,df_upd,udf_SysDate)
        ],
        ["domain_name","start_process","end_process","read_rows","ins_rows","upd_rows","date_load"]
    ).withColumn("id_execution", acn_hash_udf(F.concat(col("domain_name"),col("date_load"))))\
    .withColumn("id_process", acn_hash_udf(col("domain_name"))) \
    .select(col("id_execution"),col("id_process"),col("domain_name"),col("start_process"),col("end_process") \
        ,col("read_rows").cast("Int"),col("ins_rows").cast("Int"),col("upd_rows").cast("Int"), \
            F.substring("date_load", 1, 10).alias('date_load'))


    df_cifras.write.format('org.apache.kudu.spark.kudu') .options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx:7051', 'kudu.table':'impala::rci_metadata_db.dm_cifras_control'}) \
        .mode("append").save()

    spark.stop()

if __name__ == "__main__":
    main()