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


conf = SparkConf().setAppName('odk_64')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[4]:


df_64 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type in ('NRWRF','NRWRI','NRWRM','NRWRN') AND substr(registry_state,1,10) = '2020-02-04'")


# In[6]:


#Se borran columnas que no se usaran en el analisis
columns_to_drop = ['no_informe', 'sourceid','filedate', 'datasetname', 'timestamp', 'transaction_status', 'filename','hash_id']
df_64 = df_64.drop(*columns_to_drop)


# In[10]:


#Función para validar el key_dad
def validate_key_dad(string):
    res = False
    if string == '':
        res =True
    return res


# In[11]:


validate_key_dad_udf = udf(validate_key_dad, BooleanType())


# In[12]:


df_64_1 = df_64.withColumn("m_key",split(df_64['map'],':').getItem(0)).withColumn("m_value",split(df_64['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_64['map'],':').getItem(1)))


# In[18]:


df_64_2 = df_64_1.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("ma"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[20]:


def search(grupo,array):
    if len(array)>0:
        if (grupo.find("View")!=-1):
            word='Vista'
        elif (grupo.find("Equi")!=-1):
            word = 'Equipo'+ grupo.split('Equi')[1]
        else:
            for i in array:
                key=i.split(':')[0]
                value=i.split(':')[1]
                if(key!='' and value!=''):
                    if key=='Elemento(s) de Trabajo':
                        word=value
                        break
                    else:
                        word='root'
                else:
                    word='not found'
    else:
        word='not found'
    return word
        


# In[21]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(search, StringType())


# In[22]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df_64_3=df_64_2.withColumn("tipo_elemento", search_element('groups','ma'))


# In[24]:


#Se realiza un explode de los array
df_64_4 = df_64_3.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[26]:


df_64_5 = df_64_4.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[27]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_64_6 = df_64_5.where(F.col("validate_key") == False).drop("validate_key")


# In[33]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","")
    str_clean_3 = str_clean_2.replace(" ","_").replace("-","_")
    str_clean_4 = str_clean_3.replace("?","").replace("¿","").replace("numero_activo_fijo","activo").replace("serie_manual","serie").replace("_fijo","")
    return str_clean_4
clean_str_udf = udf(clean_str, StringType())


# In[34]:


df_64_7 = df_64_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[35]:


df_64_8 = df_64_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[37]:


df_64_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_64")


# In[38]:


sc.stop()
spark.stop()


# In[ ]:




