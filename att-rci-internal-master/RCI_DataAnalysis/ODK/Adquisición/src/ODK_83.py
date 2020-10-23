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


conf = SparkConf().setAppName('odk_83')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


df_83 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type = 'AIGD' AND substr(registry_state,1,10) = '2020-02-04'")


# In[5]:


#Se borran columnas que no se usaran en el analisis
columns_to_drop = ['no_informe', 'sourceid','registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month','day', 'filename', 'filedate', 'hash_id']
df_83 = df_83.drop(*columns_to_drop)


# In[7]:


#Se hace una limpieza de los datos
df_83 = df_83.withColumn("map",regexp_replace('map', '::', ''))
df_83_1 = df_83.withColumn('map', trim(df_83.map))


# In[9]:


#Función para validar el key_dad
def validate_key_dad(string):
    res = False
    if string == '':
        res =True
    return res


# In[10]:


validate_key_dad_udf = udf(validate_key_dad, BooleanType())


# In[11]:


df_83_2 = df_83_1.withColumn("m_key",split(df_83_1['map'],':').getItem(0)).withColumn("m_value",split(df_83_1['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_83_1['map'],':').getItem(1)))


# In[14]:


df_83_3 = df_83_2.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("map"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[1]:


def search(grupo,subgrupos,dictionary, keys, values):
    word='Not Found'
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root'
    else:
        if (grupo.find('Inventory')!=-1):    
            if len(subgrupos)>0:
                for i in subgrupos:
                    if (i.find('strElement')!=-1):
                        indexx=subgrupos.index(i)
                        word=values[indexx]
                        break
                    else:
                        word='Not found'
            else:
                word='Not found'
        else:
            if len(subgrupos)>0:
                for i in subgrupos:
                    if (i.find('pic')!=-1):
                        word='Vista'
                        break
                    else:
                        word='Not Found'
            else:
                word='Not Found'
    return word
            
    


# In[17]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(search, StringType())


# In[18]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df_83_4=df_83_3.withColumn("tipo_elemento", search_element('groups','sub_group','map','key','value'))


# In[20]:


#Se realiza un explode de los array
df_83_5 = df_83_4.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[22]:


df_83_6 = df_83_5.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[23]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_83_7 = df_83_6.where(F.col("validate_key") == False).drop("validate_key")


# In[25]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace(" ","_").replace("-","_")
    str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_3 = str_clean_2.replace("numero_de_","").replace("_escaner","").replace("_fijo","").replace("_manual","").replace("_scanner","")
    str_clean_4 = str_clean_3.replace("/","")
    return str_clean_3
    
clean_str_udf = udf(clean_str, StringType())


# In[26]:


df_83_8 = df_83_7.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[27]:


df_83_9 = df_83_8.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[29]:


df_83_9.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_83")


# In[30]:


sc.stop()
spark.stop()


# In[ ]:




