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


conf = SparkConf().setAppName('ARGD')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


df_85 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type = 'ARGD' AND substr(registry_state,1,10) = '2020-02-04'")


# In[15]:


#Se hace una limpieza de los datos
df_85 = df_85.withColumn("map",regexp_replace('map', '::', ''))
df_85 = df_85.withColumn('map', trim(df_85.map))


# In[16]:


#Función para validar el key_dad
def validate_key_dad(string):
    res = False
    if string == '':
        res =True
    return res


# In[17]:


validate_key_dad_udf = udf(validate_key_dad, BooleanType())


# In[18]:


df_85_1 = df_85.withColumn("m_key",split(df_85['map'],':').getItem(0)).withColumn("m_value",split(df_85['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_85['map'],':').getItem(1)))


# In[19]:


df_85_2 = df_85_1.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("ma"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[21]:


global elementos1
elementos1=[{'retirogenerador':'Vista'}]


# In[22]:


def search(grupo,subgrupos,dictionary, keys, values):
    word='Not Found'
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root'
    elif (len(groups)==3):
        if groups[2].lower().find('inventory')!=-1:
            for i in subgrupos:
                if i.lower().find('strelement')!=-1:
                    indexx=subgrupos.index(i)
                    word=values[indexx]
                    break
                else:
                    word='Equipo'
        else:
            for i in elementos1:
                if groups[2].lower().find(i.keys()[0])!=-1:
                    word=i.values()[0]
                    break
                else:
                    word='Not Found'
                
    else:
        word='root'
    return word
            


# In[23]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(search, StringType())


# In[24]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df_85_3=df_85_2.withColumn("tipo_elemento", search_element('groups','sub_group','ma','key','value'))


# In[26]:


df_85_4 = df_85_3.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[27]:


df_85_5 = df_85_4.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[28]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_85_6 = df_85_5.where(F.col("validate_key") == False).drop("validate_key")


# In[29]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace(" ","_").replace("-","_")
    str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_3 = str_clean_2.replace("numero_de_","").replace("_escaner","").replace("_fijo","").replace("_manual","").replace("_scanner","")
    return str_clean_3
    
clean_str_udf = udf(clean_str, StringType())


# In[30]:


df_85_7 = df_85_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[31]:


df_85_8 = df_85_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[33]:


df_85_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_85")


# In[4]:


sc.stop()
spark.stop()


# In[ ]:




