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


conf = SparkConf().setAppName('DITPE')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


df_46 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type = 'DITPE' AND substr(registry_state,1,10) = '2020-02-04'")


# In[5]:


#Se borran columnas que no se usaran en el analisis
columns_to_drop = ['no_informe', 'sourceid','registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month','day', 'filename', 'filedate', 'hash_id']
df_46 = df_46.drop(*columns_to_drop)


# In[7]:


#Función para validar el key_dad
def validate_key_dad(string):
    res = False
    if string == '':
        res =True
    return res


# In[8]:


validate_key_dad_udf = udf(validate_key_dad, BooleanType())


# In[9]:


df_46_1 = df_46.withColumn("m_key",split(df_46['map'],':').getItem(0)).withColumn("m_value",split(df_46['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_46['map'],':').getItem(1)))


# In[10]:


df_46_2 = df_46_1.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("map"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[12]:


global elementos1
elementos1=[{'Pow':'Vista'},{'Ind':'Vista'},{'Inv':'Vista Inventario'}]


# In[13]:


def search(grupo,subgrupos,dictionary, keys, values):
    word='Not Found'
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root'
    elif (len(groups)==3):
        if groups[2].find('WdEqpt')!=-1:
            if (len(subgrupos))>0:
                for i in subgrupos:
                    if(i.find('keyEqpt')!=-1):
                        for j in subgrupos:
                            if(j.find('strEqptOth')!=-1):
                                indexx=subgrupos.index(j)
                                word=values[indexx]
                                break
                            else:
                                indexx=subgrupos.index(i)
                                word=values[indexx]
                        break
                    else:
                        word='Not Found'
            else:
                word='Not Found'
    else:
        word='root'
    return word
            


# In[14]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(search, StringType())


# In[15]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df_46_3=df_46_2.withColumn("tipo_elemento", search_element('groups','sub_group','map','key','value'))


# In[17]:


df_46_4 = df_46_3.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[18]:


df_46_5 = df_46_4.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[19]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_46_6 = df_46_5.where(F.col("validate_key") == False).drop("validate_key")


# In[20]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_2 = str_clean_1.replace("Numero de ","").replace(" manual","").replace(" escaner","")
    str_clean_3 = str_clean_2.replace(" ","_").replace("-","_")
    str_clean_4 = str_clean_3.replace("?","")
    return str_clean_4
clean_str_udf = udf(clean_str, StringType())


# In[21]:


df_46_7 = df_46_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[22]:


df_46_8 = df_46_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[24]:


df_46_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_46")


# In[25]:


sc.stop()
spark.stop()


# In[ ]:




