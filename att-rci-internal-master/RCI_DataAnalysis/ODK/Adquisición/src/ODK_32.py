#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import HiveContext
from pyspark.sql.functions import lower,arrays_zip,explode,explode_outer, col, split, regexp_extract, array_contains, regexp_replace,concat_ws, create_map, create_map, lit
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
from pyspark.sql.functions import when, sum, avg, col,lower
from pyspark.sql import types as T
import re
from functools import partial 
from pyspark.sql.functions import substring, length, col, expr


# In[2]:


conf = SparkConf().setAppName('odk_32')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


df_114 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type = 'AIATP' AND substr(registry_state,1,10) = '2020-02-04'")


# In[4]:


#Se hace una limpieza de los datos
df_114 = df_114.withColumn('map', trim(df_114.map))
df_114 = df_114.withColumn("map",regexp_replace('map', 'Numero de Serie (Escanner)', 'serie esc'))
df_114 = df_114.withColumn("map",regexp_replace('map', 'Número de Serie (Manual)', 'serie man'))
df_114 = df_114.withColumn("map",regexp_replace('map', 'Número de Serie Manual', 'serie man'))
df_114 = df_114.withColumn("map",regexp_replace('map', 'Número de serie (escáner)', 'serie'))
df_114 = df_114.withColumn("map",regexp_replace('map', '::', ''))
df_114 = df_114.withColumn('map', trim(df_114.map))


# In[5]:


#Función para validar el key_dad
def validate_key_dad(string):
    res = False
    if string == '':
        res =True
    return res


# In[6]:


validate_key_dad_udf = udf(validate_key_dad, BooleanType())


# In[7]:


df_114_1 = df_114.withColumn("m_key",split(df_114['map'],':').getItem(0)).withColumn("m_value",split(df_114['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_114['map'],':').getItem(1)))


# In[9]:


df_114_2 = df_114_1.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("map"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[11]:


global elementos1
elementos1=[{'Azimuts':'Azimut'},{'Sectors':'Sector'},{'Paths':'Vista'},{'Shettler':'Shettler'},{'Cabinet':'Gabinete'},{'Brushidden':'Brushidden'},{'Bbus':'Bbus'},{'Inventory':'Equipo'},{'Antenna':'Antena'},{'Cards':'Cards'},{'Rrus':'Rrus'},{'Antenas':'Antena'}]


# In[12]:


def search(grupo,subgrupos,dictionary, keys, values):
    word='Not Found'
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root'
    elif (len(groups)==3):
        ln = len(groups[2]) - 3
        #word = groups[2][5:ln]
        if (groups[2][5:ln] == 'Com'):
            word = 'Comisionamiento'
        else:
            word = groups[2][5:ln]
    elif (len(groups)==4):
        ln = len(groups[3]) - 3
        word = groups[3][5:ln]
    else:
        word='root'
    return word
            


# In[13]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(search, StringType())


# In[14]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df_114_3=df_114_2.withColumn("tipo_elemento", search_element('groups','sub_group','map','key','value'))


# In[16]:


df_114_4 = df_114_3.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[17]:


df_114_5 = df_114_4.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[18]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_114_6 = df_114_5.where(F.col("validate_key") == False).drop("validate_key")


# In[19]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace(" ","_").replace("-","_")
    str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_3 = str_clean_2.replace("numero_de_","").replace("_escanner","_esc").replace("_manual","_man").replace("_escaner","")
    str_clean_4 = str_clean_3.replace("'","").replace("_bbu_m","").replace("_esc","").replace("_man","").replace("_fijo","").replace("_manual","").replace("_fijo_manual","")
    return str_clean_4
    
clean_str_udf = udf(clean_str, StringType())


# In[20]:


df_114_7 = df_114_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[21]:


df_114_8 = df_114_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[23]:


df_114_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_32")


# In[ ]:


sc.stop()
spark.stop()

