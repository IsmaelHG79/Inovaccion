#!/usr/bin/env python
# coding: utf-8

# # Adquisición de datos ODK 84

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


# In[2]:


conf = SparkConf().setAppName('odk_84')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


#Cargando el diccionario de elementos
#path = "/user/eg2202/Docs/MFO.csv"
#df_mfo = spark.read.format("csv").option("header", "true").load(path)
df_84 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type = 'ASMGD' AND substr(registry_state,1,10) = '2020-02-04' ")


# In[4]:


#Se hace una limpieza de los datos
df84_1 = df_84.withColumn("map",regexp_replace('map', '::', ''))
df84_1 = df84_1.withColumn('map', trim(df84_1.map)).withColumn("map",lower(col("map")))
df84_1 = df84_1.withColumn("map",regexp_replace('map', 'á', 'a')).withColumn("map",regexp_replace('map', 'é', 'e')).withColumn("map",regexp_replace('map', 'í', 'i')).withColumn("map",regexp_replace('map', 'ó', 'o')).withColumn("map",regexp_replace('map', 'ú', 'u'))


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


df84_2 = df84_1.withColumn("m_key",split(df84_1['map'],':').getItem(0)).withColumn("m_value",split(df84_1['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df84_1['map'],':').getItem(1)))


# In[8]:


df84_3 = df84_2.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[9]:


##Lista de elementos únicos en este tipo de ODK
global lista
lista=['suministro de diesel', 'erl145', 'generador movil de 30 kw', 'erl1', 'erl126', 'generador movil de 50 kw', 'planta electrica erl67', 'generador movilno. de identificacion: 9modelo: 4bt3.3g5', 'generador electrico  movil', 'generador en uso continuo', 'generador electrico', 'suministro de diesel', 'generador electrico movil', '01327136 transfer', 'generador', '01327136 generador', 'generador electrico movil']


# In[10]:


#Se realiza la función que busca el elemento dentro de la agrupación
def find_word(array):
    for i in lista:
        if i in array:
            word=i
            break
        else:
            word='root'
    return word


# In[11]:


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


# In[12]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(find_word, StringType())


# In[13]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df84_4=df84_3.withColumn("tipo_elemento", search_element('value'))


# In[ ]:


#Se muestra el nuevo dataframe con la transformación
#mfo_4.show(truncate=False)


# In[14]:


#Se realiza un explode de los array
df84_5 = df84_4.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[17]:


#Se seleccionan todas las columnas
df84_5 = df84_5.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[18]:


#Se filtra por los hijos del key_dad y se elimina la columna
df84_6 = df84_5.where(F.col("validate_key") == False).drop("validate_key")


# In[19]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","").replace(" scanner","")
    str_clean_3 = str_clean_2.replace(" ","_").replace("-","_")
    return str_clean_3
    
clean_str_udf = udf(clean_str, StringType())


# In[21]:


df84_7 = df84_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[22]:


df84_8 = df84_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value") ))


# In[24]:


df84_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_84")


# In[ ]:


sc.stop()
spark.stop()


# In[ ]:




