#!/usr/bin/env python
# coding: utf-8

import os 
import sys
import time
from pyspark.sql import SparkSession, HiveContext
from pyspark import SparkContext, SparkConf, SQLContext

conf = SparkConf().setAppName('dev_snapshot_finance').setMaster('yarn').set("spark.yarn.queue","root.eda").set("spark.jars", "/home/raw_rci/jars/kudu-spark-tools-1.4.0.jar").set("spark.yarn.queue","root.eda").set("yarn.nodemanager.vmem-check-enabled","false").set("spark.serializer", "org.apache.spark.serializer.KryoSerializer").set("spark.sql.shuffle.partitions", "10")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)

from pyspark.sql.functions import udf ,col, lit,unix_timestamp, current_date, date_format
from pyspark.sql.types import *
from pyspark.sql.functions import *

log4jlogger = sc._jvm.org.apache.log4j
global logger
logger = log4jlogger.LogManager.getLogger('LOGGER')

logger.info("Inicia la ejecucion de la vista control")

listArgs = sys.argv
print listArgs

#Obtener parametros
env = listArgs[1]
logger.info(env)
#Global Variables

#Environment

global amb
global ref
if env == "dev":
    amb = "dev_"
    ref = "cr_rci_executions_id_references_tst"
    cifras = "cr_rci_statistics_tst"
    tr = "dev_"
else:
    amb = "prd_"
    ref = "cr_rci_executions_id_references"
    cifras = "cr_rci_statistics"
    tr = ""

print amb + "cr_rci_asset_identifiers_count_bysrc"
print 'rci_db_metadata.'+ref

print cifras

environment=env
schema="rci_db_metadata"
user="raw_rci"

def finance_view():
    # Finanzas
    finance = spark.sql("WITH max_date AS( SELECT numeroserie, numeroetiqueta, MAX(ctl_file_date) AS ctl_file_date      FROM rci_db_inventory."+tr+"tx_rci_finance_cip       GROUP BY numeroserie, numeroetiqueta)  SELECT C.id, B.mxn, B.usd, B.tc  FROM max_date A  LEFT JOIN rci_db_inventory."+tr+"tx_rci_finance_cip B      ON A.numeroserie = B.numeroserie AND (A.numeroetiqueta = B.numeroetiqueta) AND (A.ctl_file_date = B.ctl_file_date)  LEFT JOIN rci_db_inventory."+amb+"cr_rci_processed_records C ON B.ctl_rid = C.ctl_rid AND C.id IS NOT NULL")
    #Activo Fijo
    fixed_asset = spark.sql("WITH max_date AS(     SELECT etiqueta, serie, MAX(ctl_file_date) AS ctl_file_date     FROM rci_db_inventory."+tr+"tx_rci_fixed_asset     GROUP BY etiqueta, serie ) SELECT C.id, B.unidades, B.vnl_del_activo_mxn, B.vnl_asignado_mxn FROM max_date A  LEFT JOIN rci_db_inventory."+tr+"tx_rci_fixed_asset B     ON A.etiqueta = B.etiqueta AND (A.serie = B.serie) AND (A.ctl_file_date = B.ctl_file_date) LEFT JOIN rci_db_inventory."+amb+"cr_rci_processed_records AS C ON (B.ctl_rid = C.ctl_rid)")
    # Propiedades
    assets = spark.sql("WITH asset_properties AS ( select id, prop, value, created_on, (row_number() over (partition by id,prop order by repeated DESC)) AS rn from (     select id, prop, value, created_on,      count() over (partition by id, CONCAT(prop, value) order by created_on) repeated     FROM rci_db_inventory."+amb+"cr_rci_asset_properties_count_bysrc     WHERE (ctl_tid = '1' OR ctl_tid = '7') ) t1  ) SELECT * FROM asset_properties WHERE rn = 1")
    # Tabla totales
    totales = spark.sql("SELECT COUNT(*) total_rows, COUNT(DISTINCT(id)) total_assets FROM rci_db_inventory."+amb+"cg_rci_asset_master").cache()
    # ### Agregación
    # Finanzas
    replaceCharsFinance = finance.withColumn("total_MXN", regexp_replace(regexp_replace("mxn", "\(", "-"), "\)", "").cast(FloatType()))
    replaceCharsFinance = replaceCharsFinance.withColumn("total_USD", regexp_replace(regexp_replace("usd", "\(", "-"), "\)", "").cast(FloatType()))
    agg_finance = replaceCharsFinance.groupBy("id").agg(sum("total_MXN"), sum("total_USD"), avg("tc"))
    # Activo Fijo
    agg_fixed_asset = fixed_asset.groupBy("id").agg(sum("unidades"), sum("vnl_del_activo_mxn"), sum("vnl_asignado_mxn"))
    # ### Snapshot Fact
    df = agg_finance.join(agg_fixed_asset, on=['id'], how='fullouter')
    df = df.withColumnRenamed("sum(total_USD)","usd").withColumnRenamed("sum(total_MXN)","mxn").withColumnRenamed("avg(tc)","tc").withColumnRenamed("sum(unidades)","unidades").withColumnRenamed("sum(vnl_del_activo_mxn)","vnl_del_activo_mxn").withColumnRenamed("sum(vnl_asignado_mxn)","vnl_asignado_mxn")
    df = df[['id', 'mxn', 'usd', 'tc', 'unidades', 'vnl_del_activo_mxn', 'vnl_asignado_mxn']]
    df = df.withColumn("date_id",date_format(current_date(), 'yyyyMMdd')).withColumn("created_on",current_timestamp())
    # ### Catálogo Assets
    df_assets = assets.groupby(assets.id, assets.created_on).pivot("prop").agg(first("value"))
    #df_assets = df_assets.withColumn("created_on",date_format(current_timestamp(), 'yyyyMMdd HH:mm:ss'))
    df_assets = df_assets.withColumn("created_on",current_timestamp())
    # ### Tabla totales
    df_total = totales.withColumn("date_id",date_format(current_date(), 'yyyyMMdd')).withColumn("created_on",current_timestamp())
    # ### Cargar tablas al Data Lake
    # Snapshot Fact
    df.write.format("parquet").mode("append").saveAsTable("rci_db_inventory."+amb+"cr_rci_finance_snapshot")
    # Catálogo de propiedades
    df_assets.write.format("parquet").mode("overwrite").saveAsTable("rci_db_inventory."+amb+"cg_rci_model_properties")
    # Tabla de totales
    df_total.write.format("parquet").mode("append").saveAsTable("rci_db_inventory."+amb+"cg_rci_total_rows")

    print "Se ejecuto exitosamente la vista de finanzas"
    logger.info("Se ejecuto exitosamente la vista de finanzas")


while True:
    references = spark.read.format('org.apache.kudu.spark.kudu').options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx', 'kudu.table':'impala::rci_db_metadata.'+ref}).load().cache().createOrReplaceTempView("cg_references")
    pending = spark.sql("SELECT * from cg_references where status = 'PENDING_FINANCE'").cache()
    l=pending.select('ctl_tid').distinct().collect()
    ctl_tids = list(map(lambda x : x[0],l))
    params = pending.select("ctl_tid","ctl_eid").collect()
    if 1 in ctl_tids and 7 in ctl_tids:
        print ("Se procesara la vista de finanzas")
        logger.info("Se procesara la vista de finanzas")
        finance_view()
        logger.info("Vista de finanzas actualizada")
        print "Se actualizara la tabla {}".format(ref)
        logger.info("Se actualizara la tabla {}".format(ref))
        for i in params:
            table_id = int(i['ctl_tid'])
            status = "FINISHED"
            logger.info("Se cambia el status a FINISHED")
            ctl_eid = str(i['ctl_eid'])
            id_query = 1
            print table_id
            os.system("/home/raw_rci/attdlkrci/{0}/shells/lib/{0}_rci_template_update_kudu.sh {1} {2} {3} {4} {5} {6} {7}".format(environment,schema,ref,status,user,table_id,ctl_eid,id_query))
            time.sleep(5)
        logger.info("Se termino el procesamiento, volviendo a revisar si hay flujos pendientes")
        time.sleep(40)
    else:
        print ("Sensando actualizaciones de activo fijo y cip finanzas")
        logger.info("Sensando actualizaciones de activo fijo y cip finanzas")
        time.sleep(40)