#!/usr/bin/env python
# coding: utf-8

# In[3]:


from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import HiveContext
from pyspark.sql.functions import arrays_zip,explode,explode_outer, col, split, regexp_extract, array_contains, regexp_replace,concat_ws, create_map, create_map, lit
import pyspark.sql.functions as f
from pyspark.sql.functions import size
from pyspark.sql.functions import concat_ws
from pyspark.sql.functions import split, trim
from pyspark.sql import functions as F
from pyspark.sql.functions import first
from pyspark.sql.functions import udf
from pyspark.sql.types import LongType
from pyspark.sql.types import StringType ,BooleanType
from pyspark.sql.functions import map_keys,map_values
from pyspark.sql.functions import when, sum, avg, col, lower
from pyspark.sql import types as T
import re
from functools import partial 
from pyspark.sql.functions import substring, length, col, expr


# In[4]:


conf = SparkConf().setAppName('ATPMW')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[5]:


df_12 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type = 'ATPMW' AND substr(registry_state,1,10) = '2020-02-04'")


# In[6]:


#Se borran columnas que no se usaran en el analisis
columns_to_drop = ['no_informe', 'sourceid','filedate', 'datasetname', 'timestamp', 'transaction_status', 'filename','hash_id']
df_12 = df_12.drop(*columns_to_drop)


# In[7]:


#Función para validar el key_dad
def validate_key_dad(string):
    res = False
    if string == '':
        res =True
    return res


# In[8]:


validate_key_dad_udf = udf(validate_key_dad, BooleanType())


# In[10]:


df_12_1 = df_12.withColumn("m_key",split(df_12['map'],':').getItem(0)).withColumn("m_value",split(df_12['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_12['map'],':').getItem(1)))


# In[12]:


path = "/user/raw_rci/attdlkrci/spark/ATPMW_patron_search.csv"


# In[41]:


search = spark.read.format("csv").option("header", "true").load(path)


# In[15]:


search_collect=search.collect()


# In[25]:


global search_dic
search_dic = list(map(lambda x : {"atributo":x[0], "elemento":x[1]},search_collect))


# In[50]:


def search_ATPMW(subgrupo):
    for i in search_dic:
        if i['atributo'].find(subgrupo)!=-1:
            word=i['elemento']
            break
        else:
            word='Not Found'
    return word
    


# In[51]:


search = udf(search_elemento, StringType())


# In[52]:


df_12_2=df_12_1.withColumn("tipo_elemento", search('sub_group'))


# In[54]:


df_12_3 = df_12_2.groupBy("cve_type","id_form","groups","tipo_elemento").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("ma"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[56]:


df_12_4 = df_12_3.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[58]:


df_12_5 = df_12_4.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[59]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_12_6 = df_12_5.where(F.col("validate_key") == False).drop("validate_key")


# In[69]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_2 = str_clean_1.replace(" ","_").replace("-","_")
    str_clean_3 = str_clean_2.replace("numero_de_activo_fijo_escaner","activo").replace("numero_de_activo_fijo_manual","activo").replace("numero_de_serie_escaner","serie").replace("numero_de_serie_manual","serie")
    return str_clean_3
clean_str_udf = udf(clean_str, StringType())


# In[70]:


df_12_7 = df_12_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[71]:


df_12_8 = df_12_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[73]:


df_12_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_12_ATPMW")


# In[ ]:


sc.stop()
spark.stop()

