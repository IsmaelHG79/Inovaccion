#!/usr/bin/env python
# coding: utf-8

# # Adquisición de datos ODK 72

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
from pyspark.sql.functions import substring, length, col, expr, lower


# In[2]:


conf = SparkConf().setAppName('odk_72')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


#Cargando el diccionario de elementos
#path = "/user/eg2202/Docs/MFO.csv"
#df_mfo = spark.read.format("csv").option("header", "true").load(path)
df_72 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type in ('ATPGA','ATPPO') AND substr(registry_state,1,10) = '2020-02-04'")


# In[5]:


#Se hace una limpieza de los datos
df72_1 = df_72.withColumn("map",regexp_replace('map', '::', ''))
df72_1 = df72_1.withColumn('map', trim(df72_1.map)).withColumn("map",lower(col("map")))
df72_1 = df72_1.withColumn("map",regexp_replace('map', 'á', 'a')).withColumn("map",regexp_replace('map', 'é', 'e')).withColumn("map",regexp_replace('map', 'í', 'i')).withColumn("map",regexp_replace('map', 'ó', 'o')).withColumn("map",regexp_replace('map', 'ú', 'u'))


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


df72_2 = df72_1.withColumn("m_key",split(df72_1['map'],':').getItem(0)).withColumn("m_value",split(df72_1['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df72_1['map'],':').getItem(1)))


# In[11]:


df72_3 = df72_2.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[14]:


##Lista de elementos únicos en este tipo de ODK
global lista
lista=['fuerza', 'rack', 'card', 'oth', 'slprnc11']


# In[15]:


#Se realiza la función que busca el elemento dentro de la agrupación
def find_word(array):
    for i in lista:
        if i in array:
            word=i
            break
        else:
            word='root'
    return word


# In[16]:


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


# In[17]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(find_word, StringType())


# In[18]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df72_4=df72_3.withColumn("tipo_elemento", search_element('value'))


# In[20]:


#Se realiza un explode de los array
df72_5 = df72_4.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[22]:


#Se seleccionan todas las columnas
df72_5 = df72_5.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[24]:


#Se filtra por los hijos del key_dad y se elimina la columna
df72_6 = df72_5.where(F.col("validate_key") == False).drop("validate_key")


# In[25]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","").replace(" scanner","").replace("numero ","")
    str_clean_3 = str_clean_2.replace(" ","_").replace("-","_") 
    str_clean_4 = str_clean_3.replace("?","").replace("¿","").replace("*","").replace("activo_fijo","activo").replace("/","")
    str_clean_5 = str_clean_4.replace("marca_del_equipo","marca").replace("marca_del_equipo_otra","marca").replace("modelo_del_equipo","modelo").replace("modelo_del_equipo_otro","modelo")
    return str_clean_5
    
clean_str_udf = udf(clean_str, StringType())


# In[26]:


df72_7 = df72_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[28]:


df72_8 = df72_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value") ))


# In[30]:


df72_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_72")


# In[31]:


sc.stop()
spark.stop()


# In[ ]:




