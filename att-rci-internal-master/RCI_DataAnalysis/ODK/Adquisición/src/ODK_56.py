#!/usr/bin/env python
# coding: utf-8

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


conf = SparkConf().setAppName('ATPCG')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


#Cargando el diccionario de elementos
df = spark.sql("select * from rci_network_db.tx_odk WHERE cve_type = 'ATPCG' AND substr(registry_state,1,10) = '2020-02-04'")


# In[4]:


#Se hace una limpieza de los datos
df_1 = df.withColumn('map',regexp_replace('map', '(?<=\d{2}):(?=[0-9])', ''))
df_2 = df_1.withColumn('map',regexp_replace('map', '::', ''))
df1 = df_2.withColumn('map', trim(df_2.map))


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


df2 = df1.withColumn("m_key",split(df1['map'],':').getItem(0)).withColumn("m_value",split(df1['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df1['map'],':').getItem(1)))


# In[11]:


df3 = df2.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[14]:


##Lista de elementos únicos en este tipo de ODK
global lista
lista=['DUW', 'TTCU', 'SPD', 'BAT', 'DUS', 'TPSU', 'TPDU', 'TBF', 'DUG']


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


def find_word(grupo,subgrupos):
    word='Not Found'
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root'
    elif (len(groups)==3):
        ln = len(groups[2]) - 3
        #word = groups[2][5:ln]
        if (groups[2][5:8] == 'Mod'):
            word = 'Vista'
        elif (groups[2][5:8] == 'Gab'):
            word = 'Gabinete'
        elif (groups[2][5:8] == 'Cab'):
            word = 'Cable'
        elif (groups[2][5:8] == 'Ban'):
            word = 'Banco de Baterias'
        elif (groups[2][5:8] == 'Inv'):
            for i in subgrupos:
                if (i.find('keyElementoInv')!=-1):
                    indexx=subgrupos.index(i)
                    word=lista[indexx]
                    break
                else:
                    word='Not Found'
        else:
            word = 'Not Found'           
    elif (len(groups)==4):
        word = groups[3][5:8]
    else:
        word='root'
    return word


# In[17]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(find_word, StringType())


# In[18]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df4=df3.withColumn("tipo_elemento", search_element('groups', 'sub_group'))


# In[20]:


#Se realiza un explode de los array
df5 = df4.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[22]:


#Se seleccionan todas las columnas
df5 = df5.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[24]:


#Se filtra por los hijos del key_dad y se elimina la columna
df6 = df5.where(F.col("validate_key") == False).drop("validate_key")


# In[25]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","")
    str_clean_3 = str_clean_2.replace(" ","_").replace("-","_") 
    return str_clean_3
    
clean_str_udf = udf(clean_str, StringType())


# In[26]:


df7 = df6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[28]:


df8 = df7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value") ))


# In[30]:


df8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_56")


# In[31]:


sc.stop()
spark.stop()

