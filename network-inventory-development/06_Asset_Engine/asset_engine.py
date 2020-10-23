# Version: 1.1.0 
# -*- coding: utf-8 -*-
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

### Block functions

def get_tabular_asset_bien(df):
    ctl_rids_repetidos = df.groupby("ctl_rid").agg(f.count('acn').alias("c"))\
    .where(f.col("c")>1).select("ctl_rid").collect()
    if len(ctl_rids_repetidos)>0:
        print "Se procede al eliminado de rids malos"
        rids_reps = list(map(lambda x: str(x['ctl_rid']),ctl_rids_repetidos))
        tabular_bien_asset_model = df.filter(~f.col('ctl_rid').isin(rids_reps)).cache()
        return tabular_bien_asset_model
    else:
        print "Sin rids repetidos"
        return df

def infered_location(df):
    table = source_table.replace("dev_","")
    srcs = spark.sql("""SELECT * FROM cg_source""").cache()
    value = srcs.where(f.col("table_name")==table).select("default_loc").collect()[0][0]
    if value is None:
        print "No procede el proceso de inferir location"
        return df
    else:
        print "Procede el proceso de inferir location"
        value = str(value)
        print value
        df2 = df.withColumn("loc", assing_default_loc_udf("loc",lit(value)))\
                .withColumn("id_location", assing_default_loc_udf("id_location",lit(value))).cache()
        return df2

def assing_default_loc(word,value):
    if word == "":
        return value
    else:
        return word

def fix_coincidences(df):
    #Registros sin ubicación 
    df_sin_loc = df.where(f.col("id_location")=="").cache()
    #Registros con ubicación (2 o  más coincidencias y solo una coincidencia)
    df_con_loc= df.where(f.col("id_location")!="").cache()
    #Agrupación para saber las coincidencias
    df3 = df_con_loc.groupby("ctl_rid").agg(f.count("id_location").alias("locations")).cache()
    # Obtenemos los registros que tuvieron mas de una coincidencia
    df3_ambiguas = df3.where(f.col("locations")>1).cache()
    #Obtenemos los registros con exactamente una coincidencia
    df3_no_ambiguas = df3.where(f.col("locations")==1).cache()
    #Eliminamos coincidencias del dataframe que si se encontraron ubicaciones
    df_con_loc_nduplicados = df_con_loc.drop_duplicates(subset=['ctl_rid']).cache()
    #Hacemos join entre la tabla origina de anomalias con los registros con coincidencias
    ambiguas = df_con_loc_nduplicados.join(df3_ambiguas, df_con_loc_nduplicados.ctl_rid == df3_ambiguas.ctl_rid, how="inner")\
            .select(df_con_loc_nduplicados['*']).cache()
    #Las que tienen mas de una coincidencia por default, se inserta la anomalia de missing location
    ambiguas2 = ambiguas.withColumn("loc",lit("")).withColumn("id_location",lit("")).drop("locations").cache()
    #Hacemos el join de las de exactamente una coincidencia
    con_location = df_con_loc_nduplicados.join(df3_no_ambiguas, df_con_loc_nduplicados.ctl_rid == df3_no_ambiguas.ctl_rid, how="inner")\
            .select(df_con_loc_nduplicados['*']).cache()
    #Finalmente unimos las tablas de con una coincidencia, sin coincidencia y más de una coincidencia
    dfs = [con_location,df_sin_loc,ambiguas2]
    df_bien =  reduce(DataFrame.unionAll, dfs).cache()
    return df_bien

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

def get_numeric_timestamp():
    dateTimeObj = datetime.now()
    year = dateTimeObj.year
    month = "0%s" % (dateTimeObj.month) if len("%s" % (dateTimeObj.month)) == 1 else "%s" % (dateTimeObj.month)
    day = "0%s" % (dateTimeObj.day) if len("%s" % (dateTimeObj.day)) == 1 else "%s" % (dateTimeObj.day)
    hour = "0%s" % (dateTimeObj.hour) if len("%s" % (dateTimeObj.hour)) == 1 else "%s" % (dateTimeObj.hour)
    minute = "0%s" % (dateTimeObj.minute) if len("%s" % (dateTimeObj.minute)) == 1 else "%s" % (dateTimeObj.minute)
    second = "0%s" % (dateTimeObj.second) if len("%s" % (dateTimeObj.second)) == 1 else "%s" % (dateTimeObj.second)
    str_date = "%s%s%s" % (year, month, day)
    str_time = "%s%s%s" % (hour, minute, second)
    return int(str_date + '' + str_time)

def send_notification(mail_environment, mail_type, mail_schema, mail_table, mail_err, mail_type_flow):
    print "En funcion envia_mail"
    print("Envio de correo ambiente: {0}".format(mail_environment))
    print("Envio de correo tipo:     {0}".format(mail_type))
    print("Envio de correo esquema:  {0}".format(mail_schema))
    print("Envio de correo tabla:    {0}".format(mail_table))
    print("Envio de correo ruta log: {0}".format(mail_err))
    print("Envio de correo tipo comp:{0}".format(mail_type_flow))
    mail_params="{0} {1} {2} {3} {4}".format(mail_type,mail_schema,mail_table,mail_err,mail_type_flow)
    os.system("hdfs dfs -get /user/raw_rci/attdlkrci/{0}/shells/{0}_rci_asset_engine_send_mail.sh".format(mail_environment))
    os.system("chmod +x {0}_rci_asset_engine_send_mail.sh".format(mail_environment))
    os.system("./{1}_rci_asset_engine_send_mail.sh {0}".format(mail_params,mail_environment))
    print("Fin de envio de correo")

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

def recursive_lst_search_cat(df, cols):
    if len(cols) > 0:
        head = cols[0]
        tail = cols[1:]
        df_trans = df.withColumn(head, search_cat_udf(head,lit(head)))
        return recursive_lst_search_cat(df_trans, tail)
    else:
        return df

def search_vendor(df):
    catalogs = get_catalogs_vendor_model()
    lst_props = list(map(lambda x: x['asset_name'], list(filter(lambda x: x['type'] == 'prop', lst_filter)) ))
    lst_vml = filter(lambda x: x in ['VENDOR'], lst_props)
    df1 = recursive_lst_search_cat(df,lst_vml).cache()
    return df1

def logic_clean(str_col):
    val_str = str(str_col.encode('ascii', 'ignore'))
    if val_str != '':
        res_val = True
    else:
        res_val = False
    return res_val

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

def generate_acn():
    return str(uuid.uuid1())

def acn_hash(column, text):
    column_str = u''.join(column + text).encode('ascii', 'ignore').strip()
    result = hashlib.md5(column_str.encode()).hexdigest()
    return result

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

def get_bid_props():
    global columns_list, list_match, lst_source_bi, lst_source_prop, source_id, cycle_stage, lst_union, lst_items_asset_names, lst_dict_bi
    global lid, cts_lst, lst_dict_all, lst_all_asset_names, lst_filter, lst_dict_prop, spark , anomaly_upper , dirt_lower,eid_tid
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
    query_prop = "select s.table_name,s.lifecycle , cprop.prop_name ,  lprop.id , lprop.ctl_tid, lprop.prop_id, lprop.prop_source_col_name, lprop.required from cg_source s    inner join lnk_properties lprop on s.ctl_tid = lprop.ctl_tid inner join cg_properties cprop on cprop.id = lprop.prop_id   where s.table_name= '%s' "% (source_table.replace("dev_",""))
    prop_table_df = spark.sql(query_prop).cache()

    query_describe = "describe %s" % (source_table_name_str)
    describe_table_df = spark.sql(query_describe).cache()
    lst_describe_collect = describe_table_df.select("col_name").collect()
    lst_table_source_columns = list(map(lambda x: str(x[0].upper()), lst_describe_collect))

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
    
    eid_tid = ctl_eid + "_" + lst_filter[0]['source_id']

    query_refresh = "refresh table %s_clean_%s " % (source_table_name_str,eid_tid)
    spark.sql(query_refresh)
    query_load_raw_table = "select %s,%s  from %s_clean_%s where ctl_eid = '%s'" % (str_alias, ctl_cols_str, source_table_name_str,eid_tid, ctl_eid)
    return query_load_raw_table

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

def get_type(str_col):
    type_str = "None"
    if str_col in cts_lst:
        type_str = "ctl"
    else:
        item = list(filter(lambda x: str_col == x["asset_name"], lst_dict_all))
        if len(item) > 0:
            type_str = item[0]["type"]
    return type_str

def get_tabular_asset(load_asset_trace_df):
    const_cols_lst = ['id','acn','concat','created_on','ctl_eid','ctl_file_date','ctl_file_name','ctl_sid','ctl_tid','ctl_ts','count']
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

def get_last_ctl_rid(ctl_rid_lst):
    ctl_rid = ''
    ctl_rid_filter_lst = list(filter(lambda x: x != '', ctl_rid_lst))
    size = len(ctl_rid_filter_lst)
    if size > 0:
        ctl_rid = ctl_rid_filter_lst[size - 1]
    return ctl_rid

def get_group_id(group_id_lst):
    group_id = ''
    group_id_filter_lst = list(filter(lambda x: x != '', group_id_lst))
    size = len(group_id_filter_lst)
    if size > 0:
        group_id = group_id_filter_lst[0]
    else:
        group_id = generate_acn()
    return group_id

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

def get_last_partition():
    try:
        last_created_on = spark.table(cr_rci_asset_group_str).select(f.max("created_on").alias("last_created_on")).take(1)[0][0]
        return last_created_on
    except:
        last_created_on = 0
        return last_created_on

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

def cg_rci_asset_master(df):
    gp_df = df.where(f.col("col_name") == "ctl_rid")\
        .groupBy("id", "acn") \
        .agg(f.split(f.concat_ws(",", f.collect_list("value")), ",").alias("ctl_rids")) \
        .cache()
    asset_df = gp_df.select("*", gp_df["ctl_rids"][0].alias("ctl_rid")).drop("ctl_rids") \
        .withColumn("created_by", lit(created_by)) \
        .withColumn("created_on", lit(created_on)).cache()
    return asset_df

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

def val_rfp_anomaly(cr_rci_anomalies_df):
    get_historic_rfp_df = get_historic_rfp()
    anomaly_join_df = broadcast(cr_rci_anomalies_df).join(get_historic_rfp_df, ["ctl_rfp"], how='left').cache()
    anomaly_df = anomaly_join_df.fillna({'anomaly_rfp': False}).drop("ctl_rfp").cache()
    return anomaly_df

def cr_rci_anomalies_fixed(df_anomalies):
    check_anomaly_location = lambda prop_lst: True if "LOC_CODE" not in prop_lst else False
    check_anomaly_required = lambda prop_lst: True if "LOC_CODE" not in prop_lst else False
    col_prop_concat = list(map(lambda y: y['asset_name'], list(filter(lambda x: x['type'] == 'prop', lst_filter))))
    col_prop_required = list(map(lambda y: y['asset_name'], list(filter(lambda x: x['type'] == 'prop' and x["required"] == 'True', lst_filter))))
    global props
    props = list(map(lambda y: y['asset_name'], list(filter(lambda x: x['type'] == 'prop', lst_filter))))
    colDrop = list(filter(lambda x: x == 'LOC_CODE' or x == 'MODEL' or x == 'VENDOR' or x == 'CATEGORY', col_prop_concat)) 
    if not check_anomaly_location(col_prop_concat):
        print "si hay loc_code"
        spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_rci_location'}).load().cache().createOrReplaceTempView("cg_location")
        cat_location = spark.sql("SELECT alias as loc, id_location FROM cg_location").withColumn("loc",f.upper(f.col("loc"))).withColumn("loc",f.trim(f.col("loc"))).cache()
        df2 = df_anomalies.join(cat_location, df_anomalies.LOC_CODE == cat_location.loc, how="left_outer").na.fill("").cache()
        if df2.count() == df2.select("ctl_rid").distinct().count():
            print "No hay coincidencias"
            df2_fixed = df2.cache()
        else:
            print "si hay coincidencias"
            df2_fixed = fix_coincidences(df2).cache()
        df2_fixed2 = infered_location(df2_fixed).cache()
        df3 = df2_fixed2.withColumn("ANOMALY_MLOCATION",missing_location_udf("loc")) \
            .withColumn("ANOMALY_MREQUIRED_PROPERTY",lit(check_anomaly_required(col_prop_required))).drop("loc","id_location").cache()
    else:
        print "no hay loc_code"
        df3 = df_anomalies.withColumn("ANOMALY_MREQUIRED_PROPERTY",lit(True)).cache()
    if "MODEL" in props:
        spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_rci_model'}).load().cache().createOrReplaceTempView("cg_model")
        spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_rci_vendor'}).load().cache().createOrReplaceTempView("cg_vendor")
        spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_rci_categories'}).load().cache().createOrReplaceTempView("cg_categories")
        print "Hay modelo, se hara el proceso de evaluacion"
        df_anomalies_by_model = df3.withColumn("MODEL",f.upper(f.col("MODEL"))).withColumn("MODEL",f.trim(f.col("MODEL"))).cache()
        firstEval = firstEvaluation(df_anomalies_by_model)
        firstEvalSModel = firstEval.where(f.col("id_model").isNotNull()).cache()
        firstEvalNModel = firstEval.where(f.col("id_model").isNull()).cache()
        secondEval = secondEvaluation(firstEvalNModel)
        secondEvalSModel = secondEval.where(f.col("id_model").isNotNull()).cache()
        secondEvalNModel = secondEval.where(f.col("id_model").isNull()).cache()
        thirdEval = thirdEvaluation(secondEvalNModel).cache()
        thirdEvalSModel = thirdEval.where(f.col("id_model").isNotNull()).cache()
        thirdEvalNModel = thirdEval.where(f.col("id_model").isNull()).cache()
        fourthEval = fourthEvaluation(thirdEvalNModel).cache()
        fourthEvalSModel = fourthEval.where(f.col("id_model").isNotNull()).cache()
        fourthEvalNModel = fourthEval.where(f.col("id_model").isNull()).cache()
        allEvals=unionAll(firstEvalSModel, secondEvalSModel, thirdEvalSModel, fourthEvalSModel, fourthEvalNModel)
        anomalie_model = allEvals.withColumn("ANOMALY_MODEL_MISSING",udf_check_model_missing("id_model","flag_is_generic"))\
            .withColumn("ANOMALY_MODEL_GENERIC",udf_check_model_generic("id_model","flag_is_generic"))\
            .drop("id_model","model2","flag_is_generic")\
            .cache() #
        df_final= anomalie_model.cache()
    else:
        print "No se hara proceso de evaluacion"
        df_final= df3.withColumn("ANOMALY_MODEL_GENERIC",lit(False)).cache()
    return df_final.drop(*colDrop)

def missing_location(loc):
    return False if loc != "" else True

def firstEvaluation(df):
    cat_models = spark.sql("SELECT * FROM cg_model").cache()
    cat_models_2 = cat_models.dropDuplicates(subset=['model']).cache()
    cat_models_2 = cat_models_2.withColumn("model",f.upper(f.col("model"))).withColumn("model",f.trim(f.col("model"))).cache()
    df2 = df.join(cat_models_2, df.MODEL == cat_models_2.model, how="left_outer")\
                        .select(df['*'],cat_models_2.id_model, cat_models_2.model.alias("model2")\
                        ,cat_models_2.flag_is_generic).cache()
    return df2

def secondEvaluation(vc):
    if "VENDOR" in props and "CATEGORY" in props:
        print "Se hara la evaluación por vendor y category"
        vc = vc.withColumn("VENDOR",f.upper(f.col("VENDOR"))).withColumn("CATEGORY",f.upper(f.col("CATEGORY")))\
        .withColumn("VENDOR",f.trim(f.col("VENDOR"))).withColumn("CATEGORY",f.trim(f.col("CATEGORY")))\
        .drop("id_model","model2","flag_is_generic").cache()
        
        df_vendor_cat = spark.sql("""SELECT A.id_model,A.model,A.cve_manufacturer,A.flag_is_generic,A.key_type, B.short_name, B.name, C.cve_manufacturer as vendor,C.vendor_name FROM cg_model A 
                        INNER JOIN cg_categories B ON A.key_type = B.key_type INNER JOIN cg_vendor C ON A.cve_manufacturer = C.cve_manufacturer 
                        where A.flag_is_generic = 1""" ).cache()
        
        df_vendor_cat = df_vendor_cat.withColumn("key_type",f.upper(f.col("key_type"))).withColumn("key_type",f.trim(f.col("key_type")))\
                    .withColumn("vendor",f.upper(f.col("vendor"))).withColumn("vendor",f.trim(f.col("vendor")))\
                    .withColumn("vendor_name",f.upper(f.col("vendor_name"))).withColumn("vendor_name",f.trim(f.col("vendor_name"))).cache()
        
        vc2 = vc.join(df_vendor_cat, ((vc.VENDOR == df_vendor_cat.vendor) | (vc.VENDOR == df_vendor_cat.vendor_name)) &\
                    (vc.CATEGORY == df_vendor_cat.key_type), how="left_outer")\
                    .select(vc['*'],df_vendor_cat.id_model, df_vendor_cat.model.alias("model2"), df_vendor_cat.flag_is_generic).cache()
        vc3 = vc2.dropDuplicates(subset=['ctl_rid']).cache()
        return vc3
    else:
        print "No se hara evaluacion por vendor and category"
        return vc

def thirdEvaluation(v):
    if "VENDOR" in props:
        print "Se hara la evaluacion por vendor"
        v = v.withColumn("VENDOR",f.upper(f.col("VENDOR"))).withColumn("VENDOR",f.trim(f.col("VENDOR")))\
        .drop("id_model","model2","flag_is_generic").cache()
        df_vendor = spark.sql("""SELECT A.id_model,A.model,A.cve_manufacturer,A.flag_is_generic,A.key_type, B.short_name, B.name, C.cve_manufacturer as vendor,C.vendor_name FROM cg_model A 
                            INNER JOIN cg_categories B ON A.key_type = B.key_type INNER JOIN cg_vendor C ON A.cve_manufacturer = C.cve_manufacturer 
                            where A.flag_is_generic = 1 and B.key_type = 'ICGEE' """)
        
        df_vendor = df_vendor.withColumn("vendor",f.upper(f.col("vendor"))).withColumn("vendor",f.trim(f.col("vendor")))\
                    .withColumn("vendor_name",f.upper(f.col("vendor_name"))).withColumn("vendor_name",f.trim(f.col("vendor_name"))).cache()
        
        v2 = v.join(df_vendor,((v.VENDOR == df_vendor.vendor) | (v.VENDOR == df_vendor.vendor_name)),\
                   how="left_outer").select(v['*'],df_vendor.id_model, df_vendor.model.alias("model2"), df_vendor.flag_is_generic).cache()
        v3 = v2.dropDuplicates(subset=['ctl_rid']).cache()
        return v3
    else:
        print "No se hara evaluacion por vendor"
        return v

def fourthEvaluation(c):
    if "CATEGORY" in props:
        print "Se hara la evaluacion por categoria"
        c = c.withColumn("CATEGORY",f.upper(f.col("CATEGORY"))).withColumn("CATEGORY",f.upper(f.trim("CATEGORY")))\
        .drop("id_model","model2","flag_is_generic").cache()
        df_cat = spark.sql("""SELECT A.id_model,A.model,A.cve_manufacturer,A.flag_is_generic,A.key_type, B.short_name, B.name 
                            FROM cg_model A INNER JOIN cg_categories B ON A.key_type = B.key_type
                            where A.flag_is_generic = 1 and A.cve_manufacturer = 'UNKN' """)
        
        df_cat = df_cat.withColumn("key_type",f.upper(f.col("key_type"))).withColumn("key_type",f.trim(f.col("key_type"))).cache()
        
        c2 = c.join(df_cat, (c.CATEGORY == df_cat.key_type), how = "left_outer")\
            .select(c['*'],df_cat.id_model, df_cat.model.alias("model2"), df_cat.flag_is_generic).cache()
        c3 = c2.dropDuplicates(subset=['ctl_rid']).cache()
        return c3
    else:
        print "No se hara evaluacion por category"
        return c

def unionAll(*dfs):
    return reduce(DataFrame.unionAll, dfs)

def check_model_missing(id_model,flag_is_generic):
    if id_model is None:
        return True
    else:
        return False 

def check_model_generic(id_model,flag_is_generic):
    if id_model is None:
        return False
    else:
        if flag_is_generic == 1:
            return True
        else:
            return False

def get_asset_master():
    try:
        master_temp_df = spark.sql("select * from %s" % (cg_rci_asset_master_str))
        return master_temp_df
    except:
        res_df = spark.createDataFrame([("","")], [ "id", "acn"])
        return res_df

def get_asset_anomalies():
    try:
        anomalies_temp_df = spark.sql("select * from %s" % (cr_rci_anomalies_str))
        return anomalies_temp_df
    except:
        res_df = spark.createDataFrame([("","")], [ "id", "acn"])
        return res_df

def cg_rci_asset_master(df):
    gp_df = df.where(f.col("col_name") == "ctl_rid")\
        .groupBy("id", "acn") \
        .agg(f.split(f.concat_ws(",", f.collect_list("value")), ",").alias("ctl_rids")) \
        .cache()
    asset_df = gp_df.select("*", gp_df["ctl_rids"][0].alias("ctl_rid")).drop("ctl_rids") \
        .withColumn("created_by", lit(created_by)) \
        .withColumn("created_on", lit(created_on)).cache()
    return asset_df

def cr_rci_asset_identifiers(df):
    gp_df = df.where((f.col("VALUE") != "") & (f.col("type") == "bi")) \
        .groupBy("id", "acn", "COL_NAME", "VALUE", f.col("source_id").alias("ctl_tid")) \
        .agg(f.sum("count").alias("count")).cache()
    res_df = gp_df.withColumnRenamed("COL_NAME", "bid") \
        .withColumn("created_by", lit(created_by)) \
        .withColumn("created_on", lit(created_on)).cache()
    return res_df

def cr_rci_asset_properties(df):
    gp_df = df.where((f.col("VALUE") != "") & (f.col("type") == "prop")) \
        .groupBy("id", "acn", "COL_NAME", "VALUE", f.col("source_id").alias("ctl_tid") ) \
        .agg(f.sum("count").alias("count")).cache()
    res_df = gp_df.withColumnRenamed("COL_NAME", "prop") \
        .withColumn("created_by", lit(created_by)) \
        .withColumn("created_on", lit(created_on)).cache()
    return res_df

def cr_rci_asset_events_fixed(df_events):
    check_anomaly_location = lambda prop_lst: True if "LOC_CODE" not in prop_lst else False
    col_prop_concat = list(map(lambda y: y['asset_name'], list(filter(lambda x: x['type'] == 'prop', lst_filter))))
    if not check_anomaly_location(col_prop_concat):
        print "Si hay location"
        spark.read.format('org.apache.kudu.spark.kudu').options(**{
        'kudu.master': 'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
        'kudu.table': 'impala::rci_db_metadata.cg_rci_location'}).load().cache().createOrReplaceTempView("cg_location")
        cat_location = spark.sql("SELECT alias as loc, id_location FROM cg_location").withColumn("loc",f.upper(f.col("loc"))).withColumn("loc",f.trim(f.col("loc"))).cache()
        
        df2 = df_events.join(cat_location, df_events.location == cat_location.loc, how="left_outer").na.fill("").cache()
        if df2.count() == df2.select("ctl_rid").distinct().count():
            print "No hay coincidencias"
            df2_fixed = df2.cache()
        else:
            print "si hay coincidencias"
            df2_fixed = fix_coincidences(df2).cache()
        df2_fixed2 = infered_location(df2_fixed).cache()
        df3 = df2_fixed2.withColumn("location",fix_locs_udf("location","loc","id_location")).drop("loc","id_location").cache()
        return df3
    else:
        print "no hay location"
        return df_events

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

def fix_locs(loc_code,loc,id_location):
    if loc != "":
        return id_location
    else:
        return loc_code

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

def drop_partition(cr_rci_asset_group_str, last_created_on):

    drop_partition_query = "ALTER TABLE %s DROP IF EXISTS PARTITION(created_on = %s)" % (cr_rci_asset_group_str, last_created_on)

    try:
        spark.sql(drop_partition_query)
    except:
        pass

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

def cr_rci_asset_properties_gral():
    df = spark.sql("select * from %s" % (cr_rci_asset_properties_str)).cache()
    gp_df = df \
        .groupBy("id", "acn", "prop", "value" ) \
        .agg(f.sum("count").alias("count")) \
        .withColumn("created_by", lit(created_by)) \
        .withColumn("created_on", lit(created_on)).cache()
    gp_df.write.format("parquet").mode("overwrite") \
        .saveAsTable(cr_rci_asset_properties_gral_str)

def cr_rci_asset_identifiers_gral():
    df = spark.sql("select * from %s"%(cr_rci_asset_identifiers_str)).cache()
    gp_df = df \
        .groupBy("id", "acn", "bid", "value") \
        .agg(f.sum("count").alias("count")) \
        .withColumn("created_by", lit(created_by)) \
        .withColumn("created_on", lit(created_on)).cache()
    gp_df.write.format("parquet").mode("overwrite") \
        .saveAsTable(cr_rci_asset_identifiers_gral_str)

### Definicion de UDF´s

search_cat_udf = udf(search_in_cat, StringType())
logic_clean_udf = udf(logic_clean, BooleanType())
generate_acn_udf = udf(generate_acn, StringType())
acn_hash_udf = udf(acn_hash, StringType())
get_type_udf = udf(get_type, StringType())
get_group_id_udf = udf(get_group_id, StringType())
get_last_ctl_rid_udf = udf(get_last_ctl_rid, StringType())
missing_location_udf = udf(missing_location,BooleanType())
udf_check_model_missing = udf(check_model_missing, BooleanType())
udf_check_model_generic = udf(check_model_generic, BooleanType())
fix_locs_udf=udf(fix_locs,StringType())
assing_default_loc_udf = udf(assing_default_loc, StringType())

schema = StructType([
    StructField("count", IntegerType(), True),
    StructField("elements",  ArrayType(StringType()), True),
])
get_anomaly_udf = udf(get_anomaly,schema )

### Variables

cts_lst = ['id','acn',"concat",'ctl_rid','ctl_sid','ctl_file_date','ctl_eid','ctl_file_name','ctl_tid','ctl_ts','ctl_rfp','count']
ctl_cols_lst = ["ctl_rid","ctl_rfp","ctl_ts","ctl_file_name","ctl_tid","ctl_sid","ctl_file_date","ctl_eid"]
order_trace_lst = ['id','acn',"concat",'count','col_name','value','type','source_id','created_by','created_on','found','traceable']

ctl_cols_str = ",".join(ctl_cols_lst)
get_timestamp = get_time()
created_on = get_timestamp

### Main Algorithm

def main():

    global columns_list, list_match, lst_source_bi, lst_source_prop, source_id, cycle_stage, lst_union, lst_items_asset_names, lst_dict_bi
    global lid, cts_lst, lst_dict_all, lst_all_asset_names, lst_filter, lst_dict_prop, spark , anomaly_upper , dirt_lower, mail_environment
    global created_by , ctl_eid, cr_rci_asset_identifiers_str, cr_rci_asset_identifiers_gral_str , cr_rci_asset_properties_gral_str , cr_rci_asset_properties_str, cr_rci_anomalies_str, cr_rci_ae_processed_sources_str , cr_rci_asset_events_str, cr_rci_processed_records_str, cr_rci_asset_group_str, asset_trace_table_str, cg_rci_asset_master_str, source_table_name_str

    spark = SparkSession.builder.appName('asset_engine_dev') \
        .config("spark.hadoop.validateOutputSpecs", "false") \
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
        .config("hive.exec.dynamic.partition", "true") \
        .config("hive.exec.dynamic.partition.mode", "nonstrict") \
        .config("spark.sql.avro.compression.codec", "snappy") \
        .config("spark.speculation", "false") \
        .config("yarn.resourcemanager.am.max-attempts", "1") \
        .config("spark.sql.cbo.enabled","true") \
        .getOrCreate()

    sc = spark.sparkContext
    spark_id = sc.applicationId
    sc.setCheckpointDir("hdfs://attdatalakehdfs/user/raw_rci/Pyspark/tmp")

    print "Invocar funcion para enviar correo"
    mail_type="start" #Manda correo notificando el inicio de la ejecución
    mail_err="NA" #Para enviar un archivo adjunto setear la ruta del HDFS en esta variable ie: /user/raw_rci/attdlkrci/tmp/dev_tx_fixed_asset.txt, para no enviar nada poner como NA
    mail_type_flow="asset"
    send_notification(mail_environment, mail_type, source_database, source_table, mail_err, mail_type_flow)

    #Loading Anomalies Table
    kudu_cg_anomalies_df = spark.read.format('org.apache.kudu.spark.kudu').options(**{'kudu.master': 
    'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
    'kudu.table': 'impala::rci_db_metadata.cg_anomalies'}).load()

    #Loading Clean Patterns Table
    kudu_cg_clean_patterns_df = spark.read.format('org.apache.kudu.spark.kudu').options(**{'kudu.master': 
    'mxtold01dlm01.attdatalake.com.mx,mxtold01dlm02.attdatalake.com.mx,mxtold01dlm03.attdatalake.com.mx',
    'kudu.table': 'impala::rci_db_metadata.cg_clean_patterns'}).load()

    #Listing Clean Patterns
    cg_clean_patterns_df = kudu_cg_clean_patterns_df.select("text_pattern").cache()
    cg_clean_patterns_lst = cg_clean_patterns_df.collect()
    dirt_lower = list(map(lambda x: str(x["text_pattern"].encode('ascii', 'ignore')).lower(), cg_clean_patterns_lst)) + [None]

    #Listing Anomalies
    cg_anomalies_df = kudu_cg_anomalies_df.select("text_anomaly").cache()
    cg_anomalies_lst = cg_anomalies_df.collect()
    anomaly_upper = list(map(lambda x: str(x["text_anomaly"].encode('ascii', 'ignore')).upper(), cg_anomalies_lst))
    cr_rci_ae_processed_sources_str

    #Prepare Query Table To Extract Source Info
    query_load_raw_table = get_bid_props()
    raw_df = spark.sql(query_load_raw_table).checkpoint(False)
    raw_df = search_vendor(raw_df).checkpoint(False)

    write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "asset engine process","START")

    #Prepare Statement Temp
    stg_tbl = "%s_tmp_stg" % (source_table_name_str.split(".")[1])
    raw_df.createOrReplaceTempView(stg_tbl)
    collect_ctl_cols_lst = list(map(lambda x: "collect_list(%s) as %s" % (x, x), ctl_cols_lst))
    collect_ctl_cols_str = ",".join(collect_ctl_cols_lst)
    str_alias_tmp = reduce(lambda x, y: "%s,%s" % (x, y), list(map(lambda x: x['asset_name'], lst_filter)) )
    query_stg_load_table = "select %s, %s  , count(*) as count from %s group by %s" % (str_alias_tmp, collect_ctl_cols_str, stg_tbl, str_alias_tmp)
    source_complete_df = spark.sql(query_stg_load_table).checkpoint(False)

    #Listing New Bids and Properties
    lst_source_bi = list(map(lambda x: x['asset_name'],  list(filter(lambda x: x['type'] == 'bi', lst_filter)) ))
    lst_source_prop = list(map(lambda x: x['asset_name'], list(filter(lambda x: x['type'] == 'prop', lst_filter)) ))
    lst_union = lst_source_bi + lst_source_prop
    source_validate_load_df = recursive_lst_validate(source_complete_df, lst_source_bi).withColumn("concat",f.concat_ws(",",*lst_union)).checkpoint(False)
    lst_filter_join_sort = sorted( list(filter(lambda x: x['type'] == 'bi', lst_filter)) , key=lambda i: i['evaluation_order'])
    db_tables = spark.sql("show tables in %s" % (source_database)).select("tableName").collect()
    lst_tables = list(map(lambda x: source_database+"." + str(x['tableName']), db_tables))

    # Fill Asset Trace
    try:
        asset_data = asset_trace_table_str.split(".")
        delete_path(spark, asset_data[0], asset_data[1])
        print(asset_trace_table_str + " 1")
    except:
        print(asset_trace_table_str + " 2")
        pass

    fill_trace_df = fill_trace().persist()
    fill_trace_df.select(*order_trace_lst).write.format("parquet").mode("overwrite").saveAsTable(asset_trace_table_str)

    ### Asset Engine

    #Fill table cr_asset_trace
    write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_asset_trace", "START")
    try:
        rest_asset_engine_df = asset_engine(source_validate_load_df, lst_filter_join_sort)
        ## No traceable
        ##no_traceable(rest_asset_engine_df.alias("no_traceable_df") )
    except Exception as excep:
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_asset_trace","ERROR:%s" % (excep))
        raise Exception("Exception: " + str(excep))
    write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_asset_trace", "END")

    # Load Asset Trace
    asset_trace_created_on_df = spark.sql("select * from %s where created_on = '%s' " % (asset_trace_table_str,created_on))
    tabular_asset_model = get_tabular_asset(asset_trace_created_on_df)

    if tabular_asset_model is not None:
        tabular_asset_model_df = tabular_asset_model.cache()
        asset_trace_all_df = spark.sql("select * from %s  " % (asset_trace_table_str)).checkpoint(False)

        #Fill table cr_rci_asset_group
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_group", "START")
        try:
            cr_rci_asset_group(tabular_asset_model_df)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_group","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_group", "END")

        #Fill table cr_rci_anomalies
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_anomalies", "START")
        try:
            tabular_asset_model_df_v2 =  get_tabular_asset_bien(tabular_asset_model_df)
            cr_rci_anomalies_rfp_df = cr_rci_anomalies(tabular_asset_model_df_v2)
            cr_rci_anomalies_df = val_rfp_anomaly(cr_rci_anomalies_rfp_df).cache()
            cr_rci_anomalies_df_2 = cr_rci_anomalies_fixed(cr_rci_anomalies_df)
            cr_rci_anomalies_df_2.write.format("parquet").mode("append").saveAsTable(cr_rci_anomalies_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_anomalies","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_anomalies", "END")

        #Fill table cg_rci_asset_master
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cg_rci_asset_master", "START")
        try:
            tab_asset_model_df = get_asset_anomalies()
            master_temp_df = get_asset_master()
            tab_asset_model_df = tab_asset_model_df.groupBy("acn").agg(f.max("ctl_rid").alias("ctl_rid")).withColumnRenamed("acn","acn_2").withColumnRenamed("ctl_rid","ctl_rid_2")
            cg_rci_asset_master_all_df = cg_rci_asset_master(asset_trace_all_df)
            cg_rci_asset_master_df = cg_rci_asset_master_all_df.join(master_temp_df, ["id", "acn"],how='leftanti').cache()
            cg_rci_asset_master_new = cg_rci_asset_master_df.join(tab_asset_model_df, cg_rci_asset_master_all_df.acn == tab_asset_model_df.acn_2,how='left').cache()
            cg_rci_asset_master_new_2 = cg_rci_asset_master_new.drop("acn_2","ctl_rid").withColumnRenamed("ctl_rid_2","ctl_rid").select("id","acn","ctl_rid","created_by","created_on")
            cg_rci_asset_master_new_2.write.format("parquet").mode("append").saveAsTable(cg_rci_asset_master_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "asset cg_rci_asset_master","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cg_rci_asset_master", "END")

        #Fill table cr_rci_asset_identifiers
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_identifiers","START")
        try:
            if cr_rci_asset_identifiers_str not in lst_tables:
                sql = "CREATE TABLE %s (id STRING,acn STRING,bid STRING,value STRING , count BIGINT,created_by STRING,created_on STRING ) PARTITIONED BY (ctl_tid STRING ) STORED AS PARQUET" % (
                        cr_rci_asset_identifiers_str)
                spark.sql(sql)
            cr_rci_asset_identifiers_df = cr_rci_asset_identifiers(asset_trace_all_df)
            cr_rci_asset_identifiers_df.write.partitionBy("ctl_tid").format("hive").mode("overwrite").saveAsTable(cr_rci_asset_identifiers_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_identifiers","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_identifiers","END")

        #Fill table cr_rci_asset_properties
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_properties","START")
        try:
            if cr_rci_asset_properties_str not in lst_tables:
                sql = "CREATE TABLE %s (id STRING,acn STRING,prop STRING,value STRING,count BIGINT,created_by STRING, created_on STRING) PARTITIONED BY (ctl_tid STRING ) STORED AS PARQUET" % (
                    cr_rci_asset_properties_str)
                spark.sql(sql)
            cr_rci_asset_properties_df = cr_rci_asset_properties(asset_trace_all_df)
            cr_rci_asset_properties_df.write.partitionBy("ctl_tid").format("hive").mode("overwrite").saveAsTable(cr_rci_asset_properties_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_properties","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_properties", "END")

        #Fill table cr_rci_asset_events
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_events", "START")
        try:
            tabular_asset_model_df_v2 =  get_tabular_asset_bien(tabular_asset_model_df)
            cr_rci_asset_events_df = cr_rci_asset_events(tabular_asset_model_df_v2)
            cr_rci_asset_events_df_2 = cr_rci_asset_events_fixed(cr_rci_asset_events_df)
            cr_rci_asset_events_df_2.write.format("parquet").mode("append").saveAsTable(cr_rci_asset_events_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_events","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_events", "END")

        #Fill table cr_rci_processed_records
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_processed_records","START")
        try:
            cr_rci_processed_records_df = cr_rci_processed_records(tabular_asset_model_df)
            cr_rci_processed_records_df.write.format("parquet").mode("append").saveAsTable(cr_rci_processed_records_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_processed_records","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_processed_records","END")

        #Fill table cr_rci_acn_mapping
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_acn_mapping", "START")
        try:
            cr_rci_acn_mapping_res = cr_rci_acn_mapping()
            if cr_rci_acn_mapping_res != None:
                cr_rci_acn_mapping_df = cr_rci_acn_mapping_res.cache()
                cr_rci_acn_mapping_df.write.format("parquet").mode("append").saveAsTable(cr_rci_acn_mapping_str)
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_acn_mapping","ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_acn_mapping", "END")

        #Fill table cr_rci_asset_properties_gral
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_properties_gral","START")
        try:
            cr_rci_asset_properties_gral()
        except Exception as excep:
            write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by,"cr_rci_asset_properties_gral", "ERROR:%s" % (excep))
            raise Exception("Exception: " + str(excep))
        write_processed_sources(ctl_eid, source_id, source_table_name_str, created_by, "cr_rci_asset_properties_gral","END")

        #Fill table cr_rci_asset_identifiers_gral
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
        delete_path(spark, source_clean[0], "%s_clean_%s"%(source_clean[1],eid_tid))
    except:
        pass

    print "Invocar funcion para enviar correo"

    mail_type="end" #Manda correo notificando el fin de la ejecución
    mail_err="NA" #Para enviar un archivo adjunto setear la ruta del HDFS en esta variable ie: /user/raw_rci/attdlkrci/tmp/dev_tx_fixed_asset.txt, para no enviar nada poner como NA
    mail_type_flow="asset"
    send_notification(mail_environment, mail_type, source_database, source_table, mail_err, mail_type_flow)

    spark.stop()

if __name__ == "__main__":

    listArgs = sys.argv

    if len(listArgs) > 0:

        prefix = listArgs[1]
        subfix = listArgs[2]
        source_database = listArgs[3]
        source_table = listArgs[4]
        ctl_eid = listArgs[5]
        created_by = listArgs[6]

        if prefix == "dev_":
            mail_environment='dev'
        else:
            mail_environment='prd'
        
        version = subfix
        cr_rci_asset_identifiers_str = "%s.%scr_rci_asset_identifiers_count_bysrc%s" % (source_database, prefix, version)
        cr_rci_asset_properties_str = "%s.%scr_rci_asset_properties_count_bysrc%s" % (source_database, prefix, version)
        cr_rci_asset_identifiers_gral_str = "%s.%scr_rci_asset_identifiers_count_gral%s" % (source_database, prefix, version)
        cr_rci_asset_properties_gral_str = "%s.%scr_rci_asset_properties_count_gral%s" % (source_database, prefix, version)
        cr_rci_asset_events_str = "%s.%scr_rci_asset_events%s" % (source_database, prefix, version)
        cr_rci_processed_records_str = "%s.%scr_rci_processed_records%s" % (source_database, prefix, version)
        cr_rci_asset_group_str = "%s.%scr_rci_asset_group%s" % (source_database, prefix, version)
        cg_rci_asset_master_str = "%s.%scg_rci_asset_master%s" % (source_database, prefix, version)
        cr_rci_acn_mapping_str = "%s.%scr_rci_acn_mapping%s" % (source_database, prefix, version)
        asset_trace_table_str = '%s.%scr_asset_trace%s' % (source_database, prefix, version)
        cr_rci_anomalies_str = "%s.%scr_rci_anomalies%s" % (source_database, prefix, version)
        cr_rci_ae_processed_sources_str = '%s.%scr_rci_ae_processed_sources%s' % (source_database, prefix, version)
        source_table_name_str = '%s.%s' % (source_database, source_table)

        main()

    else:
        print("Not enough arguments")