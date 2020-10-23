# -*- coding: utf-8 -*-
# Version: 1.1.0
import os
import time
import sys
from pyspark.sql import SparkSession, HiveContext
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql.functions import udf ,col, lit,unix_timestamp, current_date, date_format
from pyspark.sql.types import *
from pyspark.sql.functions import *
import sys
import uuid
from datetime import datetime
import pyspark.sql.functions as f
import utils

listArgs = sys.argv
print listArgs
#Obtener parametros
global amb
global table_target,table_totals_finance,table_totals_gral
global sufix
global cols
env = listArgs[1]
sufix = listArgs[2]

if env == "dev":
    amb = "dev_"
else:
    amb = ""

environment=env
cols = ['ctl_tid','table_name','type_source','lifecycle','source_name','rows','assets','updates','match','w_model','genericModel','w_location','duplicated','n_model','n_location','AVG_BIDS','AVG_PROPS','AVG_APROPS','NO_BIDS','INVALIDS','no_values','created_on']
table_target = "rci_db_inventory.{}cr_rci_sem_control_table{}".format(amb,sufix)
table_totals_finance = "rci_db_inventory.{}cg_rci_total_stats{}".format(amb,sufix)
table_totals_gral = "rci_db_inventory.{}cg_rci_total_rows{}".format(amb,sufix)
log_table_name = "rci_db_inventory.{}cr_rci_control_processed_sources{}".format(amb,sufix)

print "la vista de control sera {}".format(table_target)
print "la vista del log sera {}".format(log_table_name)


conf = SparkConf().setAppName(amb+'control_view'). \
        setMaster('yarn').\
		set("yarn.nodemanager.vmem-check-enabled","false").\
		set("spark.serializer", "org.apache.spark.serializer.KryoSerializer").\
		set("spark.sql.autoBroadcastJoinThreshold", -1)
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)

log4jlogger = sc._jvm.org.apache.log4j
global logger
logger = log4jlogger.LogManager.getLogger('LOGGER')

os.system("hdfs dfs -get /user/raw_rci/attdlkrci/{0}/config/{0}_rci_ingesta_generacion_avro.properties".format(env))
os.system("chmod +x {0}_rci_ingesta_generacion_avro.properties".format(env))
global prop
prop=utils.read_properties('{0}_rci_ingesta_generacion_avro.properties'.format(env))
logger.info("Inicia la ejecucion de la vista control")

logger.info("la vista de control sera {}".format(table_target))
logger.info("la vista del log sera {}".format(log_table_name))

# Obtención de fuentes del modelo de control
global base
source = spark.read.format('org.apache.kudu.spark.kudu').options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx', 'kudu.table':'impala::{0}.{1}'.format(prop['schema_table_config'],prop['table_source'])}).load().cache().createOrReplaceTempView("cg_source")
table = spark.read.format('org.apache.kudu.spark.kudu').options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx', 'kudu.table':'impala::{0}.{1}'.format(prop['schema_table_config'],prop['table_names'])}).load().cache().createOrReplaceTempView("cg_table")
base = spark.sql("SELECT A.ctl_tid, A.table_name, A.type_source, A.lifecycle, B.source_name FROM cg_table A \
        INNER JOIN cg_source B ON A.ctl_sid = B.ctl_sid").cache()

cgProperties = spark.read.format('org.apache.kudu.spark.kudu').options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx', 'kudu.table':'impala::{0}.cg_rci_asset_properties'.format(prop['schema_table_config'])}).load().cache().createOrReplaceTempView("cg_properties")
lnkProperties = spark.read.format('org.apache.kudu.spark.kudu').options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx', 'kudu.table':'impala::{0}.lnk_rci_asset_properties'.format(prop['schema_table_config'])}).load().cache().createOrReplaceTempView("lnk_properties")

#Functions to generate log

def generate_acn():
    return str(uuid.uuid1())

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

def write_processed_sources(last_ctl_eid, ctl_tid, table_name, ctl_created_by,stage,state):
    uuid = generate_acn()
    created_on_log = get_time()

    res_df = spark.createDataFrame(
        [
            (str(uuid), str(last_ctl_eid), int(ctl_tid), str(table_name), str(ctl_created_by)),
        ],
        ['id', 'ctl_eid', 'ctl_tid', 'table_name', 'ctl_created_by']
    )

    res_df\
        .withColumn("stage",lit(stage)) \
        .withColumn("state", lit(state))\
        .withColumn("ctl_created_on",lit(created_on_log))\
        .write.format("parquet").mode("append").saveAsTable(log_table_name)

#General functions
asset = spark.sql("""SELECT  A.ctl_rid, A.acn FROM rci_db_inventory.{}cg_rci_asset_master{} A INNER JOIN
                (SELECT max(created_on) as maxcreated FROM rci_db_inventory.{}cg_rci_asset_master{}) 
                B on A.created_on = B.maxcreated""".format(amb,sufix,amb,sufix)).cache().createOrReplaceTempView("asset_master")

anomalias = spark.sql("""SELECT A.acn, B.anomaly_mlocation,B.anomaly_model_missing, B.anomaly_model_generic, B.ctl_rid FROM asset_master A INNER JOIN rci_db_inventory.{}cr_rci_anomalies{} B
            ON A.ctl_rid = B.ctl_rid""".format(amb,sufix)).cache().createOrReplaceTempView("anomalies")

def refresh_tables():
    try:
        spark.sql("refresh table rci_db_inventory.{}cg_rci_asset_master{}".format(amb,sufix))
        spark.sql("refresh table rci_db_inventory.{}cr_rci_asset_group{}".format(amb,sufix))
        spark.sql("refresh table rci_db_inventory.{}cr_rci_anomalies{}".format(amb,sufix))
        spark.sql("refresh table rci_db_inventory.{}cr_rci_processed_records{}".format(amb,sufix))
        spark.sql("refresh table rci_db_inventory.{}cr_rci_asset_properties_count_gral{}".format(amb,sufix))
    except:
        print "No se pudo hacer el refreh"

def get_name_source(ctl_tid):
    names = base.where(col("ctl_tid")==ctl_tid).select("table_name").collect()
    name = str(names[0]['table_name'])
    return name

def get_name_tables(ctl_tid):
    sources = base.where(col("ctl_tid")==ctl_tid)
    return sources

def calculate_total_rows(ctl_tid,ctl_eid):    
    #Total de rows
    spark.sql("refresh rci_db_inventory.{}".format(prop['table_statistics']))
    total_rows = spark.sql("""SELECT ctl_tid, sum(insert_count) as `rows` FROM rci_db_inventory.{} where ctl_tid = {} and
                    ctl_eid = {} group by ctl_tid""".format(prop['table_statistics'],ctl_tid,ctl_eid))

    return total_rows

def calculate_total_rows_2(ctl_tid,ctl_eid,name):    
    #Total de rows
    total_rows = spark.sql("""SELECT {} as ctl_tid, count(*) as `rows` FROM rci_db_inventory.{}{}
    where ctl_eid = {}""".format(ctl_tid,amb,name,ctl_eid)).cache()
    return total_rows

def calculate_assets(ctl_tid):
    #Se obtienen de los activos por ctl_tid, el número de elementos únicos 
    assets = spark.sql("""SELECT {} as ctl_tid, count(distinct(acn)) as assets FROM asset_master""".format(ctl_tid)).cache()
    return assets

def calculate_rids(ctl_tid):
    #Se calculan los updates
    d=spark.sql("""with asset_records as (
    SELECT  * FROM rci_db_inventory.{}cr_rci_processed_records{} A INNER JOIN
    (SELECT max(created_on) as maxcreated FROM rci_db_inventory.{}cr_rci_processed_records{}) 
    B on A.created_on = B.maxcreated)
    SELECT {} as ctl_tid, count(distinct(ctl_rid)) as rids 
    FROM asset_records""".format(amb,sufix,amb,sufix,ctl_tid)).cache()
    return d

def calculate_match(ctl_tid):
    #Numero de grupos formados
    matchs = spark.sql("""SELECT {} as ctl_tid, count(distinct(F.acn)) AS match FROM (
            SELECT A.acn, A.ctl_rid, B.`count` FROM asset_master A LEFT JOIN rci_db_inventory.{}cr_rci_asset_group{} B 
            ON A.acn = B.acn ) F where F.`count`> 1""".format(ctl_tid,amb,sufix)).cache()
    
    return matchs

def calculate_model(ctl_tid):
    #Assets con modelo
    model = spark.sql("""SELECT {} as ctl_tid, count(distinct(acn)) as w_model from anomalies 
    where anomaly_model_missing = 0""".format(ctl_tid)).cache()
    return model

def calculate_nmodel(ctl_tid):
    #Assets con modelo
    nmodel = spark.sql("""SELECT {} as ctl_tid, count(distinct(acn)) as n_model from anomalies 
    where anomaly_model_missing = 1""".format(ctl_tid)).cache()
    return nmodel

def calculate_model_generic(ctl_tid):
    #Assets con modelo
    gmodel = spark.sql("""SELECT {} as ctl_tid, count(distinct(acn)) as genericModel from anomalies 
    where anomaly_model_generic = 1""".format(ctl_tid)).cache()
    return gmodel

def calculate_wlocation(ctl_tid):
    #Assets con modelo
    wloc = spark.sql("""SELECT {} as ctl_tid, count(distinct(acn)) as w_location from anomalies 
    where anomaly_mlocation = 0""".format(ctl_tid)).cache()
    return wloc

def calculate_nlocation(ctl_tid):
    #Assets con modelo
    nloc = spark.sql("""SELECT {} as ctl_tid, count(distinct(acn)) as n_location from anomalies 
    where anomaly_mlocation = 1""".format(ctl_tid)).cache()
    return nloc

def calculate_duplicated(ctl_tid):
    #Assets con rfp duplicado
    du = spark.sql("""SELECT {} as ctl_tid, count(distinct(C.acn)) as duplicated FROM (
                SELECT A.acn, B.anomaly_model_missing FROM asset_master A INNER JOIN rci_db_inventory.{}cr_rci_anomalies{} B
                on A.acn = B.acn where B.anomaly_rfp = True ) C""".format(ctl_tid,amb,sufix))
    return du

def avg_bids(ctl_tid):
    bids = spark.sql("""SELECT {} as ctl_tid, sum(D.bids) as acn_by_bids from (
                SELECT C.acn, count(distinct(C.bid)) as bids FROM (
                SELECT A.acn, A.ctl_rid, B.bid, B.value, B.`count` FROM asset_master A 
                LEFT JOIN rci_db_inventory.{}cr_rci_asset_identifiers_count_gral{} B on A.acn = B.acn) C 
                group by C.acn ) D """.format(ctl_tid,amb,sufix)).cache()
    return bids

def avg_props(ctl_tid):
    props = spark.sql("""SELECT {} as ctl_tid, sum(D.props) as acn_by_props from (
                SELECT C.acn, count(distinct(C.prop)) as props FROM (
                SELECT A.acn, A.ctl_rid, B.prop, B.value, B.`count` FROM asset_master A 
                LEFT JOIN rci_db_inventory.{}cr_rci_asset_properties_count_gral{} B on A.acn = B.acn
                WHERE B.prop in ("LOC_CODE","MODEL","VENDOR")) C 
                group by C.acn ) D """.format(ctl_tid,amb,sufix)).cache()
    return props.fillna({'acn_by_props':0})

def aprops(ctl_tid):
    aprops = spark.sql("""SELECT {} as ctl_tid, sum(D.aprops) as aprops from (
                SELECT C.acn, count(distinct(C.prop)) as aprops FROM (
                SELECT A.acn, A.ctl_rid, B.prop, B.value, B.`count` FROM asset_master A 
                LEFT JOIN rci_db_inventory.{}cr_rci_asset_properties_count_gral{} B on A.acn = B.acn
                WHERE B.prop not in ("LOC_CODE","MODEL","VENDOR")) C 
                group by C.acn ) D """.format(ctl_tid,amb,sufix)).cache()
    return aprops.fillna({'aprops':0})

def calculate_no_values(ctl_tid):
    required_props = spark.sql("""
            SELECT B.prop_name FROM lnk_properties A INNER JOIN cg_properties B 
            on A.prop_id = B.id  where A.ctl_tid = {} and A.required = True """.format(ctl_tid)).cache()
    
    array = required_props.select("prop_name").collect()
    properties_required = list(map(lambda y: str(y['prop_name']),array))
    number_required = len(properties_required)
    properties = spark.sql("""SELECT A.acn, B.prop, B.value FROM asset_master A 
                LEFT JOIN rci_db_inventory.{}cr_rci_asset_properties_count_gral{} B on A.acn = B.acn""".format(amb,sufix)).cache()
    
    properties_filter = properties.where(col("prop").isin(properties_required)).cache()
    properties_group = properties_filter.groupBy("acn").agg(countDistinct("prop").alias("props")).cache()
    properties_group_2 = properties_group.withColumn("no_values",lit(number_required - col("props"))).cache()
    properties_group_3 = properties_group_2.select(sum("no_values").alias("no_values")).withColumn("ctl_tid",lit(ctl_tid))\
                        .select("ctl_tid","no_values").cache()
    total_assets = properties.select("acn").distinct().count()
    total_assets_wrproperties = properties_filter.select("acn").distinct().count()
    no_values2 = (total_assets - total_assets_wrproperties) * number_required
    properties_final = properties_group_3.withColumn("no_values",col("no_values") + no_values2).na.fill(0).cache()
    return properties_final

def check_if_exist():
    try:
        df_control_view = spark.sql("SELECT * FROM {}".format(table_target))
        tbl = True
    except:
        tbl=False
    return tbl

def join_dfs(sources,total_rows,assets,rids,match,w_model,n_model,g_model,w_location,n_location,avg_bids_,avg_props_,aprops_,duplicated,no_values):
    # Se juntan la base y el número total de registros procesados
    source0 = sources.join(total_rows, on=['ctl_tid'], how='left') # Total de números procesados
    source1 = source0.join(assets, on=['ctl_tid'], how='left') # Total de elementos únicos
    source2 = source1.join(rids, on=['ctl_tid'], how='left') # Total de elementos únicos
    source3 = source2.join(match, on=['ctl_tid'], how='left') # Total de matches, coincidiencias de rfp's
    source4 = source3.join(w_model, on=['ctl_tid'], how='left') # Total de elementos con marca
    source5 = source4.join(g_model, on=['ctl_tid'], how='left') # Total de elementos con modelo
    source6 = source5.join(w_location, on=['ctl_tid'], how='left') # Total de elementos con location
    source7 = source6.join(avg_bids_, on=['ctl_tid'], how='left' )
    source8 = source7.join(avg_props_, on=['ctl_tid'], how='left' )
    source9 = source8.join(aprops_, on=['ctl_tid'], how='left' )
    source10 = source9.join(duplicated, on=['ctl_tid'], how='left')
    source11 = source10.join(n_model, on=['ctl_tid'], how='left')
    source12 = source11.join(n_location, on=['ctl_tid'], how='left')
    source13 = source12.join(no_values,on=['ctl_tid'], how='left')
    return source13


def table_totals_af_cip():
    spark.sql("refresh table {}".format(table_target))
    ctl_tids = spark.sql("SELECT * FROM {}".format(table_target)).select("ctl_tid").distinct().collect()
    lista = list(map(lambda y: (y['ctl_tid']),ctl_tids))
    if 7 in lista and 1 in lista:
        print("bien")
        df=spark.sql("SELECT sum(rows) as total_rows, sum(assets) as total_assets FROM {}".format(table_target)).cache()
        cip = spark.sql("SELECT sum(assets) as total_assets_cip FROM {} where ctl_tid = 1".format(table_target)).collect()[0][0]
        af = spark.sql("SELECT sum(assets) as total_assets_af FROM {} where ctl_tid = 7".format(table_target)).collect()[0][0]
        afcip=spark.sql("SELECT sum(assets) as total_assets_af_cip FROM {} where ctl_tid in (1,7)".format(table_target)).collect()[0][0]
        df2=df.withColumn("assets_cip",lit(cip)).withColumn("assets_af",lit(af)).withColumn("assets_cip_af",lit(afcip)).cache()
        df3 = df2.withColumn("assets_porcentaje_cip",col("assets_cip")/col("total_assets")).withColumn("assets_porcentaje_af",col("assets_af")/col("total_assets"))\
                .withColumn("assets_porcentaje_cip_af",col("assets_cip_af")/col("total_assets")).cache()
        df4=df3.withColumn("created_on",current_timestamp()).na.fill(0).cache()
        df5=df4.withColumn("date_id",date_format("created_on",'yyyyMM')).cache()
        df_totals = df5.select("total_rows","total_assets","created_on","date_id").cache()
        df6 = df5.drop("total_rows","total_assets").cache()
        print("Persiting Tables")
        df6.write.format("parquet").mode("append").saveAsTable(table_totals_finance)
        df_totals.write.format("parquet").mode("append").saveAsTable(table_totals_gral)
        return "bien"
    else:
        return "mal"


def semantic_engine(table):
    for i in table:
        print i
        print "refresh tables"
        refresh_tables()
        global control_view
        print "Se va a procesar el ctl_tid {}".format(i['ctl_tid'])
        logger.info("Se va a procesar el ctl_tid {}".format(i['ctl_tid']))
        source_table_name = get_name_source(i['ctl_tid'])
        created_by = "raw_rci"
        
        write_processed_sources(i['ctl_eid'], i['ctl_tid'], source_table_name, created_by, "GET COUNTS","START")
        try:
            #Se obtienen los conteos principaes
            sources = get_name_tables(i['ctl_tid'])

            total_rows = calculate_total_rows(i['ctl_tid'],i['ctl_eid_origin'])
            #total_rows = calculate_total_rows_2(i['ctl_tid'],i['ctl_eid_origin'],source_table_name)

            assets = calculate_assets(i['ctl_tid'])

            rids = calculate_rids(i['ctl_tid'])

            match = calculate_match(i['ctl_tid'])

            w_model = calculate_model(i['ctl_tid'])
            n_model = calculate_nmodel(i['ctl_tid'])


            g_model = calculate_model_generic(i['ctl_tid'])

            w_location = calculate_wlocation(i['ctl_tid'])
            n_location = calculate_nlocation(i['ctl_tid'])

            
            avg_bids_ = avg_bids(i['ctl_tid'])
            
            avg_props_ = avg_props(i['ctl_tid'])
            
            aprops_ = aprops(i['ctl_tid'])
            print ("bien")
            duplicated = calculate_duplicated(i['ctl_tid'])
            
            no_values = calculate_no_values(i['ctl_tid'])

            # Se juntan la base y el número total de registros procesados
            source9 = join_dfs(sources,total_rows,assets,rids,match,w_model,n_model,g_model,w_location,n_location,avg_bids_,avg_props_,aprops_,duplicated,no_values).cache()

            source11 = source9.withColumn("AVG_BIDS", col("acn_by_bids")/col("assets")).withColumn("AVG_PROPS", col("acn_by_props")/col("assets"))\
                    .withColumn("AVG_APROPS", col("aprops")/col("assets")).withColumn("updates",col("rids")-col("assets"))\
                    .withColumn("NO_BIDS",col("rows")-(col("assets") + col("updates")))\
                    .drop("acn_by_bids","acn_by_props","aprops","rids").cache()
            source12 = source11.withColumn("INVALIDS",col("NO_BIDS")+col("duplicated")).cache()
            control_view = source12.withColumn("created_on",current_timestamp()).select(*cols).cache()
        
        except Exception as excep:
            write_processed_sources(i['ctl_eid'], i['ctl_tid'], source_table_name, created_by, "GET COUNTS","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(i['ctl_eid'], i['ctl_tid'], source_table_name, created_by, "GET COUNTS","END")
        
        write_processed_sources(i['ctl_eid'], i['ctl_tid'], source_table_name, created_by, "PERSISTING TABLE","START")
        try:
            tbl = check_if_exist()
            if tbl:
                print "La tabla vista de control ya existe"
                control_view.write.format("parquet").mode("append").saveAsTable(table_target)
            else:
                print "Se crea la vista de control por primera vez"
                control_view.write.format("parquet").mode("overwrite").saveAsTable(table_target)
        except Exception as excep:
            write_processed_sources(i['ctl_eid'], i['ctl_tid'], source_table_name, created_by, "PERSISTING TABLE","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(i['ctl_eid'], i['ctl_tid'], source_table_name, created_by, "PERSISTING TABLE","END")
        
    print "Calculando totales"
    table_totals_af_cip_ = table_totals_af_cip()
    print table_totals_af_cip_
    print "Se ejecutaron exitosamente los {} flujos pendientes".format(table)
    logger.info("Se ejecutaron exitosamente los {} flujos pendientes".format(table))

references = spark.read.format('org.apache.kudu.spark.kudu').options(**{'kudu.master':'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx', 'kudu.table':'impala::{0}.{1}'.format(prop['schema_table_config'],prop['table_execution_references'])}).load().cache().createOrReplaceTempView("cg_references")
pending = spark.sql("SELECT * from cg_references where status in ('{0}','{1}')".format(prop['status_pending_control_view'],prop['status_processing_control_view'])).cache()
pends = pending.count()
if pends >= 1:	
    print "Hay flujos pendientes"
    logger.info("Hay flujos pendientes")
    msj = "Hay flujos pendientes"
    params = pending.select("ctl_tid","ctl_eid","ctl_eid_origin").collect()
    lista_processing = list(map(lambda x : {"ctl_tid":x['ctl_tid'], "ctl_eid":str(x['ctl_eid']), 'ctl_eid_origin':str(x['ctl_eid_origin'])},params))    
    
    print "Invocar funcion para enviar correo"
    mail_environment=env
    mail_type="start" #Manda correo notificando el inicio de la ejecución
    mail_err="NA" #Para enviar un archivo adjunto setear la ruta del HDFS en esta variable ie: /user/raw_rci/attdlkrci/tmp/dev_tx_fixed_asset.txt, para no enviar nada poner como NA
    mail_type_flow="control"
    source_table = get_name_source(lista_processing[0]['ctl_tid'])
    utils.send_notification(mail_environment, mail_type, '{0}'.format(prop['schema_table_rci']), source_table, mail_err, mail_type_flow)
    utils.update_status(mail_environment, prop['schema_table_config'], prop['table_execution_references'], prop['status_processing_control_view'], prop['user'], lista_processing[0]['ctl_tid'], lista_processing[0]['ctl_eid'], 1)
    
    print "Hay {} flujos pendientes para procesar".format(len(lista_processing))
    print "Hay {} flujos pendientes para procesar".format(len(lista_processing))
    logger.info("Hay {} flujos pendientes para procesar".format(len(lista_processing)))
    print "Iniciando..."
    logger.info("Iniciando...")
    semantic_engine(lista_processing)
    logger.info("Se termino el procesamientO")
    
    print "Invocar funcion para enviar correo"
    mail_environment=env
    mail_type="end" #Manda correo notificando el fin de la ejecución
    mail_err="NA" #Para enviar un archivo adjunto setear la ruta del HDFS en esta variable ie: /user/raw_rci/attdlkrci/tmp/dev_tx_fixed_asset.txt, para no enviar nada poner como NA
    mail_type_flow="control"
    utils.send_notification(mail_environment, mail_type, '{0}'.format(prop['schema_table_rci']), source_table, mail_err, mail_type_flow)
else:
    print "No hay archivos nuevos para procesar por el semantic engine"
    logger.info("No hay archivos nuevos para procesar por el semantic engine")

sc.stop()
spark.stop()




