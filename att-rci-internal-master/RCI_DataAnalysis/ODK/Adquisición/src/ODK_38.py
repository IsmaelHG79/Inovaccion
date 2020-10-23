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


conf = SparkConf().setAppName('DECOR')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


df_38 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type = 'DECOR' AND substr(registry_state,1,10) = '2020-02-04'")


# In[5]:


#Se borran columnas que no se usaran en el analisis
columns_to_drop = ['no_informe', 'sourceid','registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month','day', 'filename', 'filedate', 'hash_id']
df_38 = df_38.drop(*columns_to_drop)


# In[6]:


def transform(grupo):
    groups=grupo.split(':')
    if (len(groups)==5):
        col=groups[0]+':'+groups[1]+':'+groups[2]+':'+groups[3]
    elif(len(groups)==4):
        col=groups[0]+':'+groups[1]+':'+groups[2]
    else:
        col=grupo
    return col


# In[7]:


transform_group = udf(transform, StringType())


# In[8]:


df_38_1=df_38.withColumn('form_elementos',transform_group('groups')).drop('groups')


# In[9]:


df_38_1 = df_38_1.select(col("id_form").alias("id_form"), col("cve_type").alias("clave_form"),col("form_elementos").alias("form_element"),col("sub_group").alias("atributo"),col("map").alias("ma"))


# In[11]:


#Función para validar el key_dad
def validate_key_dad(string):
    res = False
    if string == '':
        res =True
    return res


# In[12]:


validate_key_dad_udf = udf(validate_key_dad, BooleanType())


# In[13]:


df_38_2 = df_38_1.withColumn("m_key",split(df_38_1['ma'],':').getItem(0)).withColumn("m_value",split(df_38_1['ma'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_38_1['ma'],':').getItem(1)))


# In[14]:


df_38_3 = df_38_2.groupBy("clave_form","id_form","form_element").agg(F.collect_list("atributo").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("ma").alias("ma"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[16]:


global elementos1
elementos1=[{'AntennaRRU':'RRu'},{'CabinetRack':'Gabinete'},{'BatteryBank':'Banco de baterias'},{'Shelter':'Shelter'},{'Pwr':'Planta de fuerza'},{'Transfers':'Transferencias'},{'Towers':'Torre'},{'Supports':'Soportes'},{'Materials':'Materiales'}]


# In[17]:


def search(grupo,subgrupos,dictionary, keys, values):
    word='Not Found'
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root1'
    elif (len(groups)==3):
        if grupo.find('Vw')!=-1:
            word='Vista'
        else:
            if (len(subgrupos))>0:
                for i in subgrupos:
                    if(i.find('keyType')!=-1):
                        indexx=subgrupos.index(i)
                        word=values[indexx]
                        break
                    else:
                        word='Not Found'
            else:
                word='Not Found'
        if word=='Not Found':
            for i in elementos1:
                if groups[2].find(i.keys()[0])!=-1:
                    word=i.values()[0]
                    break
                else:
                    word='Not Found' 
        
    elif (len(groups)==4):
        for i in elementos1:
            if groups[3].find(i.keys()[0])!=-1:
                word=i.values()[0]
                break
            else:
                word='Not Found'
    else:
        word='root2'
    return word
            


# In[18]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(search, StringType())


# In[19]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df_38_4=df_38_3.withColumn("tipo_elemento", search_element('form_element','sub_group','ma','key','value'))


# In[21]:


df_38_5 = df_38_4.select("clave_form","id_form","form_element","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[22]:


df_38_6 = df_38_5.select("clave_form","id_form","form_element","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[23]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_38_7 = df_38_6.where(F.col("validate_key") == False).drop("validate_key")


# In[32]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace(" ","_").replace("-","_")
    str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_3 = str_clean_2.replace("marca_OTH","marca").replace("numero_de_activo","activo").replace("numero_de_activoescaner","activo").replace("numero_de_activomanua","activo")
    str_clean_4 = str_clean_3.replace("numero_de_serie_escaner","serie").replace("numero_de_serie_manual","serie").replace("activoescaner","activo").replace("activomanual","activo")

    return str_clean_4
    
clean_str_udf = udf(clean_str, StringType())


# In[33]:


df_38_8 = df_38_7.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[34]:


df_38_9 = df_38_8.groupBy("clave_form","id_form","form_element","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[36]:


df_38_9.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_38")


# In[ ]:


sc.stop()
spark.stop()

