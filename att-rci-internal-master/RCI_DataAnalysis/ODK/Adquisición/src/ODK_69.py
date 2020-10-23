#!/usr/bin/env python
# coding: utf-8

# # Adquisición de datos ODK 69

# Se importan las librerías necesarias:

# In[1]:



from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import HiveContext
from pyspark.sql.types import *
from pyspark.sql.functions import lit
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
import re
from functools import partial 
from pyspark.sql.functions import substring, length, col, expr


# In[2]:


conf = SparkConf().setAppName('RRFM')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# Consulta para importar los datos del ODK: 

# In[190]:


#Cargando el diccionario de elementos
df_69 = spark.sql("select * from rci_network_db.tx_odk WHERE cve_type = 'RRFM' AND substr(registry_state,1,10) = '2020-02-04'")


# In[191]:


#Se hace una limpieza de los datos
df69_1 = df_69.withColumn("map",regexp_replace('map', '::', ''))
df69_2 = df69_1.withColumn("map",regexp_replace('map', ':::', ''))
df69_3 = df69_2.withColumn("map",regexp_replace('map', '(?<=\d{2}):(?=[0-9])', ''))
df69_1 = df69_3.withColumn('map', trim(df69_3.map))


# In[192]:


#Función para validar el key_dad
def validate_key_dad(string):
    res = False
    if string == '':
        res =True
    return res


# In[193]:


validate_key_dad_udf = udf(validate_key_dad, BooleanType())


# In[194]:


df69_2 = df69_1.withColumn("m_key",split(df69_1['map'],':').getItem(0)).withColumn("m_value",split(df69_1['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df69_1['map'],':').getItem(1)))


# In[195]:


df69_3 = df69_2.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[196]:


##Lista de elementos únicos en este tipo de ODK
global lista
lista=['DCDU', 'UPEU', 'WBBP', 'UMPT', 'BBU', 'FAN']


# In[197]:


#Se realiza la función que busca el elemento dentro de la agrupación
def find_word(array):
    for i in lista:
        if i in array:
            word=i
            break
        else:
            word='root'
    return word


# In[211]:


def search(grupo,subgrupos, keys, values):
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root'
    elif (len(groups)==3):
           word = 'Vista'
    elif (len(groups)==5):
        if (len(subgrupos))>0:
            for i in subgrupos:
                if(i.find('keyEquipmentTunel')!=-1):
                    indexx=subgrupos.index(i)
                    word=values[indexx]
                    break
                else:
                    word = 'Not Found'
        else:
            word = 'test'
    elif (len(groups)==4):
        for i in subgrupos:
            if(i.find('keyEquipment')!=-1):
                indexx=subgrupos.index(i)
                word=values[indexx]
                break
            elif(i.find('keyEquipmentDAS')!=-1):
                indexx=subgrupos.index(i)
                word=values[indexx]
                break
            elif(i.find('keyEquipmentTunel')!=-1):
                indexx=subgrupos.index(i)
                word=values[indexx]
                break
            else:
                word = 'Pantalla'     
        
    else:
        word = 'Not Found'
    return word


# In[212]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(search, StringType())


# In[213]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df69_4 = df69_3.withColumn("tipo_elemento", search_element('groups','sub_group', 'key','value'))


# In[216]:


#Se realiza un explode de los array
df69_5 = df69_4.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[217]:


#Se seleccionan todas las columnas
df69_5 = df69_5.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[218]:


#Se filtra por los hijos del key_dad y se elimina la columna
df69_6 = df69_5.where(F.col("validate_key") == False).drop("validate_key")


# In[219]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","")
    str_clean_3 = str_clean_2.replace(" ","_").replace("-","_") 
    str_clean_4 = str_clean_3.replace(".","").replace('"','').replace("activo_fijo","activo")
    return str_clean_4
    
clean_str_udf = udf(clean_str, StringType())


# In[220]:


df69_7 = df69_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[221]:


df69_8 = df69_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value") ))


# In[222]:


df69_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_69")


# In[223]:


sc.stop()
spark.stop()

