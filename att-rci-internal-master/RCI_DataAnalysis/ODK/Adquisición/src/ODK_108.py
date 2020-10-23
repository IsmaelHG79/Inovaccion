#!/usr/bin/env python
# coding: utf-8

# # Adquisición de datos ODK 108

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
import re
from functools import partial 
from pyspark.sql.functions import substring, length, col, expr


# In[4]:


conf = SparkConf().setAppName('odk_118')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[6]:


#Cargando el diccionario de elementos
#path = "/user/eg2202/Docs/MFO.csv"
#df_mfo = spark.read.format("csv").option("header", "true").load(path)
df_108 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type = 'MFO' AND substr(registry_state,1,10) = '2020-02-04' ")


# In[8]:


#Se hace una limpieza de los datos
df108_1 = df_108.withColumn("map",regexp_replace('map', '::', ''))
df108_1 = df108_1.withColumn('map', trim(df108_1.map))


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


df108_2 = df108_1.withColumn("m_key",split(df108_1['map'],':').getItem(0)).withColumn("m_value",split(df108_1['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df108_1['map'],':').getItem(1)))


# In[15]:


df108_3 = df108_2.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[18]:


##Lista de elementos únicos en este tipo de ODK
global lista
lista=['RF','RTU','FWDM']


# In[19]:


#Se realiza la función que busca el elemento dentro de la agrupación
def find_word(array):
    for i in lista:
        if i in array:
            word=i
            break
        else:
            word='root'
    return word


# In[20]:


def search(grupo,array):
    if len(array)>0:
        if (grupo.find("View")!=-1):
            word='Vista'
        elif (grupo.find("Equi")!=-1):
            word = grupo.split('Equi')[1]
        else:
            for i in array:
                key=i.split(':')[0]
                value=i.split(':')[1]
                if(key!='' and value!=''):
                    if key=='Elemento':
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
search_element = udf(find_word, StringType())


# In[22]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df108_4=df108_3.withColumn("tipo_elemento", search_element('value'))


# In[23]:


#Se muestra el nuevo dataframe con la transformación
#mfo_4.show(truncate=False)


# In[24]:


#Se realiza un explode de los array
df108_5 = df108_4.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[26]:


#Se seleccionan todas las columnas
df108_5 = df108_5.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[28]:


#Se filtra por los hijos del key_dad y se elimina la columna
df108_6 = df108_5.where(F.col("validate_key") == False).drop("validate_key")


# In[29]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","")
    str_clean_3 = str_clean_2.replace(" ","_").replace("-","_").replace("¿","").replace("?","").replace(".","").replace("/","").replace("activo_fijo","activo")
    return str_clean_3
    
clean_str_udf = udf(clean_str, StringType())


# In[30]:


df108_7 = df108_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[32]:


df108_8 = df108_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value") ))


# In[33]:


df108_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_108")


# In[34]:


sc.stop()
spark.stop()


# In[ ]:




