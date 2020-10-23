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
from pyspark.sql.functions import when, sum, avg, col, lower
from pyspark.sql import types as T
import re
from functools import partial 
from pyspark.sql.functions import substring, length, col, expr


# In[2]:


conf = SparkConf().setAppName('ATPLT')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


df_114 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type = 'ATPLT' AND substr(registry_state,1,10) = '2020-02-04' ")


# In[5]:


#Se hace una limpieza de los datos
df_114 = df_114.withColumn("map",regexp_replace('map', '::', ''))
df_114 = df_114.withColumn('map', trim(df_114.map))


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


df_114_1 = df_114.withColumn("m_key",split(df_114['map'],':').getItem(0)).withColumn("m_value",split(df_114['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_114['map'],':').getItem(1)))


# In[10]:


df_114_2 = df_114_1.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("ma"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[12]:


global elementos1
elementos1=[{'Azimuts':'Vista Azimut'},{'Sectors':'Sector'},{'Paths':'Vista trayectoria'},{'Shettler':'Shettler'},{'Cabinet':'Gabinete'},{'Bbus':'Bbus'},{'Brushidden':'Brushidden'},{'Bbus':'Bbus'},{'Inventory':'Equipo'},{'Antenna':'Antena'},{'Cards':'Cards'},{'Rrus':'Rrus'},{'Antenas':'Antena'}]


# In[13]:


def search(grupo,subgrupos,dictionary, keys, values):
    word='Not Found'
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root'
    elif (len(groups)==3):
        for i in elementos1:
            if groups[2].find(i.keys()[0])!=-1:
                word=i.values()[0] + groups[2][-1]
                break
            else:
                word='Not Found'
    elif (len(groups)==4):
        for i in elementos1:
            if groups[3].find(i.keys()[0])!=-1:
                word=i.values()[0] + groups[3][-1]
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
df_114_3=df_114_2.withColumn("tipo_elemento", search_element('groups','sub_group','ma','key','value'))


# In[17]:


df_114_4 = df_114_3.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[18]:


df_114_5 = df_114_4.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[19]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_114_6 = df_114_5.where(F.col("validate_key") == False).drop("validate_key")


# In[20]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace(" ","_").replace("-","_")
    str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_3 = str_clean_2.replace("numero_de_","").replace("_escaner","").replace("_fijo","").replace("_manual","").replace("_scanner","")
    str_clean_4 = str_clean_3.replace(".","").replace("/","").replace("'","").replace("*","").replace("_escanner","")
    series=['strbbuserialnumbermanual','strbbuserialnumberscan','strcardserialnumbermanual','strcardserialnumberscan','strmanualmodeu','strserialnumbervwu']
    for i in series:
        str_clean_4 = str_clean_4.replace(i,"serie")
    activos=['strbbuassetmanual','strbbuassetscan','strcardassetmanual','strcardassetscan','strmanualmodeafu','strserialnumberafu']
    for i in activos:
        str_clean_4 = str_clean_4.replace(i,"activo")
    return str_clean_4
    
clean_str_udf = udf(clean_str, StringType())


# In[21]:


df_114_7 = df_114_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[22]:


df_114_8 = df_114_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[24]:


df_114_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_114")


# In[ ]:


sc.stop()
spark.stop()

