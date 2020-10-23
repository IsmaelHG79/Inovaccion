#!/usr/bin/env python
# coding: utf-8
# Version: 1.1.0
import os 
import sys
import time
import uuid
from pyspark.sql import SparkSession, HiveContext
from pyspark import SparkContext, SparkConf, SQLContext
from datetime import datetime
import pyspark.sql.functions as f
from pyspark.sql.functions import udf ,col, lit,unix_timestamp, current_date, date_format
from pyspark.sql.types import *
from pyspark.sql.functions import *
import utils

listArgs = sys.argv
print listArgs

#Define Variables
global amb
global sufix
global log_table_name
global created_by

#Get Parameters
env = listArgs[1]
sufix = listArgs[2]

if env == "dev":
    amb = "dev_"
else:
    amb = ""

environment=env
#sufix = ""
log_table_name = "rci_db_inventory.{}cr_rci_finance_processed_sources{}".format(amb,sufix)
print "la vista del log sera {}".format(log_table_name)
#Spark Configuratoion
conf = SparkConf().setAppName(amb+'finance_sem'). \
        setMaster('yarn').\
		set("yarn.nodemanager.vmem-check-enabled","false").\
		set("spark.serializer", "org.apache.spark.serializer.KryoSerializer").\
		set("spark.sql.autoBroadcastJoinThreshold", -1)
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)

#Start Function Logger Information
log4jlogger = sc._jvm.org.apache.log4j
global logger
logger = log4jlogger.LogManager.getLogger('LOGGER')

os.system("hdfs dfs -get /user/raw_rci/attdlkrci/{0}/config/{0}_rci_ingesta_generacion_avro.properties".format(env))
os.system("chmod +x {0}_rci_ingesta_generacion_avro.properties".format(env))
global prop
prop=utils.read_properties('{0}_rci_ingesta_generacion_avro.properties'.format(env))
logger.info("Inicia la ejecucion de la vista financiera")
created_by='{0}'.format(prop['user'])

#Block Functions

#Function Generate Hash
def generate_acn():
    return str(uuid.uuid1())

#Function Generate Sysdate
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

#Function to Write Status of Process
def write_processed_sources(ctl_created_by,stage,state):
    uuid = generate_acn()
    created_on_log = get_time()
    res_df = spark.createDataFrame(
        [
            (str(uuid), str(ctl_created_by)),
        ],
        ['id','ctl_created_by']
    )
    res_df\
        .withColumn("stage",f.lit(stage)) \
        .withColumn("state", f.lit(state))\
        .withColumn("ctl_created_on",f.lit(created_on_log))\
        .write.format("parquet").mode("append").saveAsTable(log_table_name)

#Function to Finance Values
def get_finance_view():
    df=spark.sql("""SELECT acn, prop, value, created_on FROM rci_db_inventory.{}cr_rci_asset_properties_count_bysrc{}\
                WHERE ctl_tid in (1,7) AND prop IN ('MXN', 'USD', 'UNIDADES', 'VNL_ACTIVO_MXN', 'VNL_ASIGNADO_MXN') """.format(amb,sufix)).cache()
    df2 = df.withColumn("total_value", regexp_replace(regexp_replace(regexp_replace("value", "\(", "-"), "\)", ""), " ", "").cast(FloatType())).cache()
    df3 = df2.drop("value").withColumnRenamed("total_value","value").cache()
    df4=df3.groupby("acn","created_on","prop").agg(sum("value").alias("value")).cache()
    df_finance = df4.groupby(df4.acn, df4.created_on).pivot("prop").agg(first("value")).cache()
    df_finance_2 = df_finance.select("acn","MXN","UNIDADES","USD","VNL_ACTIVO_MXN","VNL_ASIGNADO_MXN","created_on")\
            .withColumn("created_on", to_timestamp("created_on", "yyyy-MM-dd HH:mm:ss"))\
            .withColumn("date_id",date_format("created_on",'yyyyMM')).cache()
    return df_finance_2

#Function to Finance Properties
def get_cat_properties():
    df=spark.sql("""WITH asset_properties AS (
            SELECT acn, prop, value, created_on, (row_number() over (PARTITION BY acn,prop order by repeated DESC)) AS rn from (
                SELECT acn, prop, value, created_on,
                COUNT() over (partition by acn, CONCAT(prop, value) order by created_on) repeated
                FROM rci_db_inventory.{}cr_rci_asset_properties_count_bysrc{}
                WHERE ctl_tid in (1,7) AND prop IN ('LEGAL_ENTITY', 'LOC_CODE', 'ARTICLE','INVOICE_NO','BOOK', 'PURCHASE_ORDER', 'ACCOUNT', 'SUBACCOUNT', 'CATEGORY', 'VENDOR')
                ) t1 )SELECT * FROM asset_properties WHERE rn = 1 """.format(amb,sufix)).cache()
    df_props = df.groupby(df.acn, df.created_on).pivot("prop").agg(first("value")).cache()
    df_props_2 = df_props\
            .withColumn("created_on", to_timestamp("created_on", "yyyy-MM-dd HH:mm:ss"))\
            .withColumn("date_id",date_format("created_on",'yyyyMM')).cache()
    return df_props_2

def finance_view():
    print "Iniciando procesamiento"
    global df_finance, asset_properties

    #Block to Get Finance Information Values
    write_processed_sources(created_by, "Agregated values financial view", "START")
    try:
        df_finance = get_finance_view()
    except Exception as excep:
        write_processed_sources(created_by, "Agregated values financial view","ERROR:%s" % (excep))
        raise Exception("Exception: " + str(excep))
    write_processed_sources(created_by, "Agregated values financial view", "END")
    
    #Block to Get Finance Information Properties
    write_processed_sources(created_by, "Get financial properties", "START")
    try:
        print("Get Properties")
        assets_properties = get_cat_properties()
    except Exception as excep:
        write_processed_sources(created_by, "Get financial properties","ERROR:%s" % (excep))
        raise Exception("Exception: " + str(excep))
    write_processed_sources(created_by, "Get financial properties", "END")
    
    #Block to Persist Tables
    write_processed_sources(created_by, "Persisting tables", "START")
    try:
        df_finance.write.format("parquet").mode("append").saveAsTable("rci_db_inventory.{}cr_rci_sem_finance_table{}".format(amb,sufix))
        assets_properties.write.format("parquet").mode("append").saveAsTable("rci_db_inventory.{}cg_rci_model_properties_fi{}".format(amb,sufix))
    except Exception as excep:
        write_processed_sources(created_by, "Persisting tables","ERROR:%s" % (excep))
        raise Exception("Exception: " + str(excep))
    write_processed_sources(created_by, "Persisting tables", "END")
    print "Termino la fista financiera"

references = spark.read.format('org.apache.kudu.spark.kudu').options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx', 'kudu.table':'impala::{0}.{1}'.format(prop['schema_table_config'],prop['table_execution_references'])}).load().cache().createOrReplaceTempView("cg_references")
table = spark.read.format('org.apache.kudu.spark.kudu').options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx', 'kudu.table':'impala::{0}.{1}'.format(prop['schema_table_config'],prop['table_names'])}).load().cache().createOrReplaceTempView("cg_table")
pending = spark.sql("select t.table_name, r.ctl_tid, r.ctl_eid, r.ctl_eid_origin from cg_references r inner join cg_table t on r.ctl_tid=t.ctl_tid where r.status = '{0}' and r.ctl_tid in (1,7) ".format(prop['status_pending_finance'])).cache()
pends = pending.count()
if pends >= 1:	
	logger.info("Processing financial view")
	params = pending.select("table_name","ctl_tid","ctl_eid").collect()
	for i in params:
		table_id = int(i['ctl_tid'])
		status = '{0}'.format(prop['status_processing_finance'])
		logger.info("Se cambia el status a {0}".format(status))
		print table_id
		ctl_eid = str(i['ctl_eid'])
		print ctl_eid
		source_table = str(i['table_name'])
		print source_table
		print "Invocar funcion para enviar correo"
		mail_environment=env
		mail_type="start" #Manda correo notificando el inicio de la ejecución
		mail_err="NA" #Para enviar un archivo adjunto setear la ruta del HDFS en esta variable ie: /user/raw_rci/attdlkrci/tmp/dev_tx_fixed_asset.txt, para no enviar nada poner como NA
		mail_type_flow="finance"
		utils.send_notification(mail_environment, mail_type, '{0}'.format(prop['schema_table_rci']), source_table, mail_err, mail_type_flow)
		id_query = 1
		utils.update_status(mail_environment, prop['schema_table_config'], prop['table_execution_references'], prop['status_processing_control_view'], prop['user'], table_id, ctl_eid, 1)
		time.sleep(5)
	
	#write_processed_sources(created_by, "Create financial view", "START")
	finance_view()
	#write_processed_sources(created_by, "Create financial view", "STOP")
	
	for i in params:
		table_id = int(i['ctl_tid'])
		print table_id
		ctl_eid = str(i['ctl_eid'])
		print ctl_eid
		source_table = str(i['table_name'])
		print source_table
		print "Invocar funcion para enviar correo"
		mail_environment=env
		mail_type="end" #Manda correo notificando el inicio de la ejecución
		mail_err="NA" #Para enviar un archivo adjunto setear la ruta del HDFS en esta variable ie: /user/raw_rci/attdlkrci/tmp/dev_tx_fixed_asset.txt, para no enviar nada poner como NA
		mail_type_flow="finance"
		utils.send_notification(mail_environment, mail_type, '{0}'.format(prop['schema_table_rci']), source_table, mail_err, mail_type_flow)
		time.sleep(5)
	
	logger.info("Finishing financial view")
else:
    print "No hay archivos nuevos para procesar por el semantic finance"
    logger.info("No hay archivos nuevos para procesar por el semantic finance")

sc.stop()
spark.stop()