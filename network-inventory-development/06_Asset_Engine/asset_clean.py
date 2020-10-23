# -*- coding: utf-8 -*-
# Version: 1.1.0
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

## constantes

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

## funciones

def upperTrim_cols(df, props_list):
    size = len(props_list)
    if size > 0:
        head, tail = (lambda lista: (lista[0], lista[1:]))(props_list)
        if head:
            df2 = df.withColumn(head, f.upper(f.col(head))).withColumn(head, f.trim(f.col(head)))
            return upperTrim_cols(df2,tail)
    else:
        return df

def clean_columns(raw_df, lista):

    size_list = len(lista)
    if size_list > 0:
        head, tail = (lambda lista: (lista[0], lista[1:]))(lista)
        if head:
            head_name = head['source_col_name']
            df_clean = raw_df.withColumn(head_name, replace_values_udf(head_name))
            return clean_columns(df_clean, tail)
    else:
        return raw_df


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


def chunks(lst, n):
    for i in xrange(0, len(lst), n):
        yield lst[i:i + n]


def clean_raw_source(df, wrong_lst):

    size_list = len(wrong_lst)
    if size_list > 0:
        head, tail = (lambda lista: (lista[0], lista[1:]))(wrong_lst)
        if head:
            # print head
            df_clean = df.replace(to_replace=head, value='').persist()
            return clean_raw_source(df_clean, tail)
    else:
        return df


def recursive_zero_eval(s):
    if s is not None and s.startswith('0'):
        str_tem = s[1:]
        return recursive_zero_eval(str_tem)
    else:
        return s


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


def replace_values(cadena):

    try:
        cadena = cadena.encode('ascii', 'ignore')
        cadena = cadena.replace("ó", "o").replace("á", "a").replace("é", "e").replace("í", "i").replace("ú", "u")
        cadena = cadena.replace("Ó", "O").replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ú", "U")
        return cadena

    except:
        return cadena


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


## udf

replace_values_udf = udf(replace_values, StringType())
recursive_zero_eval_udf = udf(recursive_zero_eval, StringType())


def get_bid_props():
    global columns_list, list_match, lst_source_bi, lst_source_prop, source_id, cycle_stage, lst_union, lst_items_asset_names, lst_dict_bi
    global lid, cts_lst, lst_dict_all, lst_all_asset_names, lst_filter, lst_dict_prop, spark, anomaly_upper, dirt_lower , source_table_name_clean_str
    global created_by, ctl_eid, cr_rci_asset_identifiers_str, cr_rci_asset_identifiers_gral_str, cr_rci_asset_properties_gral_str, cr_rci_asset_properties_str, cr_rci_anomalies_str, cr_rci_ae_processed_sources_str, cr_rci_asset_events_str, cr_rci_processed_records_str, cr_rci_asset_group_str, asset_trace_table_str, cg_rci_asset_master_str, source_table_name_str

    spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cfg_rci_table'}).load().cache().createOrReplaceTempView("cg_source")
    spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_rci_business_identifiers'}).load().cache().createOrReplaceTempView(
        "cg_business_identifiers")
    spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_rci_asset_properties'}).load().cache().createOrReplaceTempView(
        "cg_properties")
    spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.lnk_rci_business_identifiers'}).load().cache().createOrReplaceTempView(
        "lnk_business_identifiers")
    spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.lnk_rci_asset_properties'}).load().cache().createOrReplaceTempView(
        "lnk_properties")

    query_row_data_source = "select * from cg_source where table_name = '%s' " % (source_table.replace("dev_", ""))
    lst_row_data_source = spark.sql(query_row_data_source).collect()
    source_id = str(lst_row_data_source[0]['ctl_tid'])
    cycle_stage = str(lst_row_data_source[0]['lifecycle'])

    query_bi = "select s.table_name,s.lifecycle , cbi.bid_name ,cbi.evaluation_order , lbi.id , lbi.ctl_tid , lbi.bid_id , lbi.bid_source_col_name   from cg_source s  inner join lnk_business_identifiers lbi on s.ctl_tid = lbi.ctl_tid inner join cg_business_identifiers cbi on cbi.id = lbi.bid_id   where s.table_name= '%s' " % (
        source_table.replace("dev_", ""))
    bi_table_df = spark.sql(query_bi).cache()

    query_prop = "select s.table_name,s.lifecycle , cprop.prop_name ,  lprop.id , lprop.ctl_tid, lprop.prop_id, lprop.prop_source_col_name from cg_source s    inner join lnk_properties lprop on s.ctl_tid = lprop.ctl_tid inner join cg_properties cprop on cprop.id = lprop.prop_id   where s.table_name= '%s' " % (
        source_table.replace("dev_", ""))
    prop_table_df = spark.sql(query_prop).cache()

    query_describe = "describe %s" % (source_table_name_str)
    describe_table_df = spark.sql(query_describe).cache()
    lst_describe_collect = describe_table_df.select("col_name").collect()
    lst_table_source_columns = list(map(lambda x: str(x[0].upper()), lst_describe_collect))

    lst_prop = prop_table_df.select("prop_name", "prop_source_col_name", 'id', 'ctl_tid', 'prop_id').collect()
    lst_dict_prop = list(map(
        lambda x: {"source_col_name": str(x.prop_source_col_name).upper(), "asset_name": str(x.prop_name).upper(),
                   "lnk_column_id": str(x.id), "source_id": str(x.ctl_tid), "cg_prop_id": str(x.prop_id),
                   "type": 'prop'}, lst_prop))

    lst_bi = bi_table_df.select("bid_name", "bid_source_col_name", 'id', 'ctl_tid', 'bid_id',
                                'evaluation_order').collect()
    lst_dict_bi = list(map(
        lambda x: {"source_col_name": str(x.bid_source_col_name).upper(), "asset_name": str(x.bid_name).upper(),
                   "lnk_column_id": str(x.id), "source_id": str(x.ctl_tid), "cg_prop_id": str(x.bid_id),
                   "evaluation_order": int(x.evaluation_order),
                   "type": 'bi'}, lst_bi))

    lst_dict_all = lst_dict_bi + lst_dict_prop
    lst_filter = list(filter(lambda x: x['source_col_name'] in lst_table_source_columns, lst_dict_all))
    lst_alias = list(map(lambda x: "regexp_replace( %s ,'[^a-zA-Z0-90]+', '') as %s" % (x['source_col_name'], x['source_col_name']) if x['type'] == 'bi' else "%s as %s" % (x['source_col_name'], x['source_col_name']), lst_filter))
    str_alias = ",".join(lst_alias)
    query_load_raw_table = "select %s,%s  from %s where ctl_eid = '%s'" % (str_alias, ctl_cols_str, source_table_name_str, ctl_eid)
    return query_load_raw_table


def main():

    global columns_list, list_match, lst_source_bi, lst_source_prop, source_id, cycle_stage, lst_union, lst_items_asset_names, lst_dict_bi
    global lid, cts_lst, lst_dict_all, lst_all_asset_names, lst_filter, lst_dict_prop, spark, anomaly_upper, dirt_lower , source_table_name_clean_str
    global created_by, ctl_eid, cr_rci_asset_identifiers_str, cr_rci_asset_identifiers_gral_str, cr_rci_asset_properties_gral_str, cr_rci_asset_properties_str, cr_rci_anomalies_str, cr_rci_ae_processed_sources_str, cr_rci_asset_events_str, cr_rci_processed_records_str, cr_rci_asset_group_str, asset_trace_table_str, cg_rci_asset_master_str, source_table_name_str

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

    kudu_cg_clean_patterns_df = spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_clean_patterns'}) \
        .load()


    cg_clean_patterns_df = kudu_cg_clean_patterns_df.select("text_pattern").cache()

    cg_clean_patterns_lst = cg_clean_patterns_df.collect()

    dirt_lower = list(map(lambda x: str(x["text_pattern"].encode('ascii', 'ignore')).upper(), cg_clean_patterns_lst))

    query_load_raw_table = get_bid_props()

    tid = "_" + lst_filter[0]['source_id']
    source_table_name_clean_str = source_table_name_clean_str + tid
    try:
        source_clean = source_table_name_clean_str.split(".")
        delete_path(spark, source_clean[0], source_clean[1] )
    except:
        pass

    raw_source_df = spark.sql(query_load_raw_table).persist()

    source_fill_na_df = raw_source_df.fillna('').checkpoint(False)

    clean_source_df = source_fill_na_df.replace(to_replace= dirt_lower, value='').checkpoint(False)

    lst_source_bi = list(map(lambda x: x['source_col_name'], list(filter(lambda x: x['type'] == 'bi', lst_filter))))

    lst_source_props = list(map(lambda x: x['source_col_name'], list(filter(lambda x: x['type'] == 'prop', lst_filter))))

    source_clean_load_df = recursive_lst_zero_eval(clean_source_df, lst_source_bi).checkpoint(False)

    source_replace_clean_df = clean_columns(source_clean_load_df, lst_filter).checkpoint(False)

    source_replace_clean_df_upper = upperTrim_cols(source_replace_clean_df,lst_source_props).checkpoint(False)

    source_replace_clean_df_upper.coalesce(20)\
        .write\
        .format("parquet")\
        .mode("overwrite") \
        .saveAsTable(source_table_name_clean_str)


if __name__ == "__main__":

    listArgs = sys.argv

    if len(listArgs) > 0:

        prefix = listArgs[1]
        subfix = listArgs[2]
        source_database = listArgs[3]
        source_table = listArgs[4]
        ctl_eid = listArgs[5]

        source_table_name_str = '%s.%s' % (source_database, source_table)

        source_table_name_clean_str = '%s.%s_clean_%s' % (source_database ,source_table,ctl_eid)

        main()

    else:
        print("Not enough arguments")