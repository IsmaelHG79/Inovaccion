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
from pyspark.sql.functions import when, sum, avg, col,lower
import re
from functools import partial 
from pyspark.sql.functions import substring, length, col, expr


# In[2]:


conf = SparkConf().setAppName('IESAU')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


#Cargando el diccionario de elementos
df = spark.sql("select * from rci_network_db.tx_odk WHERE cve_type = 'IESAU' AND substr(registry_state,1,10) = '2020-02-04'")


# In[4]:


df_1 = df.withColumn('map', trim(df.ma))


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


df2 = df_1.withColumn("m_key",split(df_1['map'],':').getItem(0)).withColumn("m_value",split(df_1['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_1['map'],':').getItem(1)))


# In[8]:


df3 = df2.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[9]:


##Lista de elementos únicos en este tipo de ODK
global lista
lista=['C9CN', 'OTH', 'CAT6', 'C16CN', 'C9CB', 'Vista']


# In[1]:


def search(grupo,subgrupos, keys, values):
    groups=grupo.split(':')
    if len(groups)>3:
        if (groups[2].find("SondaChange")!=-1):
            word='Vista'
        else:
            for i in subgrupos:
                if len(subgrupos.split(':'))>2:
                    key=i.split(':')[0]
                    value=i.split(':')[1]
                    if(key!='' and value!=''):
                        if key=='strElementoInventarioOth':
                            word=value
                            break
                        else:
                            word='root'
                    else:
                        word='not found'
                else:
                    word='not found'
    else:
        word='not found'
    return word


# In[12]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(search, StringType())


# In[13]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df4=df3.withColumn("tipo_elemento", search_element('groups','sub_group', 'key','value'))


# In[14]:


#Se realiza un explode de los array
df5 = df4.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[15]:


#Se seleccionan todas las columnas
df5 = df5.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[16]:


#Se filtra por los hijos del key_dad y se elimina la columna
df6 = df5.where(F.col("validate_key") == False).drop("validate_key")


# In[17]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","")
    str_clean_3 = str_clean_2.replace(" ","_").replace("-","_") 
    return str_clean_3
    
clean_str_udf = udf(clean_str, StringType())


# In[18]:


df7 = df6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[19]:


df8 = df7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value") ))


# In[20]:


df8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_60")


# In[ ]:


sc.stop()
spark.stop()

