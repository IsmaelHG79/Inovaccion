#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


conf = SparkConf().setAppName('odk_61')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


df_61 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type in ('AVGI','SEFOP') AND substr(registry_state,1,10) = '2020-02-04'")


# In[4]:


#Se borran columnas que no se usaran en el analisis
columns_to_drop = ['no_informe', 'sourceid','registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month','day', 'filename', 'filedate', 'hash_id']
df_61 = df_61.drop(*columns_to_drop)


# In[6]:


#Función para validar el key_dad
def validate_key_dad(string):
    res = False
    if string == '':
        res =True
    return res


# In[7]:


validate_key_dad_udf = udf(validate_key_dad, BooleanType())


# In[8]:


df_61_1 = df_61.withColumn("m_key",split(df_61['map'],':').getItem(0)).withColumn("m_value",split(df_61['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_61['map'],':').getItem(1)))


# In[10]:


df_61_2 = df_61_1.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("map"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[12]:


def search(grupo,subgrupos,dictionary, keys, values):
    word='Not Found'
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root'
    else:
        if (grupo.find('VerificationInterconnection')!=-1):    
            word='Router' + grupo[-1]
        else:
            word='Not Found'
    return word
            


# In[13]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(search, StringType())


# In[14]:


df_61_3=df_61_2.withColumn("tipo_elemento", search_element('groups','sub_group','map','key','value'))


# In[16]:


df_61_4 = df_61_3.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[17]:


df_61_5 = df_61_4.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[18]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_61_6 = df_61_5.where(F.col("validate_key") == False).drop("validate_key")


# In[19]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace(" ","_").replace("-","_")
    str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_3 = str_clean_2.replace("/","_").replace("*","").replace("keymodel","modelo").replace("strmanualassetmode","activo")
    str_clean_4 = str_clean_3.replace("strmanualserialmode","serie").replace("strmodeloth","modelo")
    return str_clean_4
    
clean_str_udf = udf(clean_str, StringType())


# In[20]:


df_61_7 = df_61_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[21]:


df_61_8 = df_61_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[23]:


df_61_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_61")


# In[24]:


sc.stop()
spark.stop()


# In[ ]:




