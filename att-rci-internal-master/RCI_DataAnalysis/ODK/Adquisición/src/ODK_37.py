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


conf = SparkConf().setAppName('odk_37')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


df_37 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type IN ('IPBV3', 'AIIPB', 'IPBV2') AND substr(registry_state,1,10) = '2020-02-04'")


# In[5]:


#Se borran columnas que no se usaran en el analisis
columns_to_drop = ['no_informe', 'sourceid','registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month','day', 'filename', 'filedate', 'hash_id']
df_37 = df_37.drop(*columns_to_drop)


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


df_37_1 = df_37.withColumn("m_key",split(df_37['map'],':').getItem(0)).withColumn("m_value",split(df_37['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_37['map'],':').getItem(1)))


# In[10]:


df_37_2 = df_37_1.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("map"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


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
        if groups[2].find('Ixn')!=-1:
            if (len(subgrupos))>0:
                for i in subgrupos:
                    if(i.find('strIxnoEqu')!=-1):
                        indexx=subgrupos.index(i)
                        word=values[indexx]
                        break
                    else:
                        word='Inventario'
            else:
                word='Not Found'
        else:
            for i in elementos1:
                if groups[2].find(i.keys()[0])!=-1:
                    word=i.values()[0]
                    break
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
df_37_3=df_37_2.withColumn("tipo_elemento", search_element('groups','sub_group','map','key','value'))


# In[17]:


df_37_4 = df_37_3.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[18]:


df_37_5 = df_37_4.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[19]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_37_6 = df_37_5.where(F.col("validate_key") == False).drop("validate_key")


# In[27]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace(" ","_").replace("-","_")
    str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_3 = str_clean_2.replace("numero_","").replace("_manual","").replace("_fijo","")
    str_clean_4 = str_clean_3.replace("?","").replace(".","").replace("'","").replace("&","").replace("numero_","").replace("_fijo","").replace("_fijo_manual","").replace("_manual","")
    series=['modelo','modelo_equipo_destino','modelo_equipo_origen','modelo_otro']
    for i in series:
        str_clean_4 = str_clean_4.replace(i,"modelo")
   
    return str_clean_4 
    
clean_str_udf = udf(clean_str, StringType())


# In[28]:


df_37_7 = df_37_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[29]:


df_37_8 = df_37_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[31]:


df_37_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_37")


# In[32]:


sc.stop()
spark.stop()


# In[ ]:




