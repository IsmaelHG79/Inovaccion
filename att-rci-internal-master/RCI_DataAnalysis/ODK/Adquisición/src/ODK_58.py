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


conf = SparkConf().setAppName('odk_58')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


df_58 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type in ('ARFCS','ATPSA','CSRAN') AND substr(registry_state,1,10) = '2020-02-04'")


# In[4]:


#Se hace una limpieza de los datos
df_58 = df_58.withColumn("map",regexp_replace('map', '::', ''))
df_58 = df_58.withColumn('map', trim(df_58.map))


# In[5]:


#Se borran columnas que no se usaran en el analisis
columns_to_drop = ['no_informe', 'sourceid','registry_state', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month','day', 'filename', 'filedate', 'hash_id']
df_58 = df_58.drop(*columns_to_drop)


# In[7]:


#Función para validar el key_dad
def validate_key_dad(string):
    res = False
    if string == '':
        res =True
    return res


# In[8]:


validate_key_dad_udf = udf(validate_key_dad, BooleanType())


# In[9]:


df_58_1 = df_58.withColumn("m_key",split(df_58['map'],':').getItem(0)).withColumn("m_value",split(df_58['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_58['map'],':').getItem(1)))


# In[11]:


df_58_2 = df_58_1.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("map"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[13]:


global elementos1
elementos1=[{'Sectores':'Sector'},{'SectoresPhoto':'Fotos'},{'ElemInvPhoto':'Fotos Inventario'},{'HeightChange':'Cambio de altura'},{'AntennaChange':'Antena'},{'AzimuthTilt':'Azimut'},{'AdSector':'Sector'},{'Antenna':'Antenna'},{'Rrus':'Rru'},{'Rcus':'Rcu'},{'Boards':'Tarjeta'},{'Cards':'Tarjeta'},{'SectorData':'Sector'},{'Secscr':'Pantalla Sector'},{'Comm':'Comisionamiento'},{'Shelter':'Shelter'},{'Azimuts':'Vista azimut'},{'Sectors':'Sector'},{'Antenas':'Antena'},{'Rrus':'Rru'},{'Paths':'Trayectoria'},{'Cabinet':'Gabinete'},{'Nodeb':'Nodo b'},{'Baterry':'Bateria'}]


# In[14]:


def search(grupo,subgrupos,dictionary, keys, values):
    word='Not Found'
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root'
    elif (len(groups)==3):
        if groups[2].find('Inventario')!=-1:
            if (len(subgrupos))>0:
                for i in subgrupos:
                    if(i.find('keyElemInv')!=-1):
                        indexx=subgrupos.index(i)
                        word=values[indexx]
                        break
                    else:
                        word='Inventario'
            else:
                word='Not Found'
        else:
            for i in elementos1:
                if groups[2].find(i.keys()[0])!=-1:
                    word=i.values()[0]
                    break
                else:
                    word='Not Found'
        
    elif (len(groups)==4):
        if groups[3].find('ElemInv')!=-1:
            if (len(subgrupos))>0:
                for i in subgrupos:
                    if(i.find('keyElemInv')!=-1):
                        indexx=subgrupos.index(i)
                        word=values[indexx]
                        break
                    else:
                        word='Not Found'
            else:
                word='Not Found'
        else:
            for i in elementos1:
                if groups[3].find(i.keys()[0])!=-1:
                    word=i.values()[0]
                    break
                else:
                    word='Not Found'
    else:
        word='root'
    return word
            


# In[15]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(search, StringType())


# In[16]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df_58_3=df_58_2.withColumn("tipo_elemento", search_element('groups','sub_group','map','key','value'))


# In[18]:


df_58_4 = df_58_3.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[19]:


df_58_5 = df_58_4.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[20]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_58_6 = df_58_5.where(F.col("validate_key") == False).drop("validate_key")


# In[21]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace(" ","_").replace("-","_")
    str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_3 = str_clean_2.replace("âº","")
    activos=['activo_fijo_escaner','activo_fijo_manual','numero_de_activo_fijo_de_antena_retirada_escaner','numero_de_activo_fijo_de_antena_retirada_manual','numero_de_activo_fijo_escaner','numero_de_activo_fijo_manual']
    for i in activos:
        str_clean_3=str_clean_3.replace(i,'activo')
    str_clean_4=str_clean_3.replace("longitud_de_lineas_de_fo","longitud").replace("longitud_de_lineas_de_fo/hibrido","longitud")
    str_clean_5=str_clean_4.replace("marca","marca").replace("marca_de_fo","marca").replace("marca_de_fo/hibrido","marca")
    str_clean_6=str_clean_5.replace("modelo_de_antena_retirada","modelo").replace("numero_de_serie_de_antena_retirada_escaner","serie").replace("numero_de_serie_de_antena_retirada_manual","serie").replace("numero_de_serie_manual","serie").replace("numero_de_serie_escaner","serie")
    str_clean_7 = str_clean_6.replace("/","").replace("°","").replace("numero_de_","")
    return str_clean_6
    
clean_str_udf = udf(clean_str, StringType())


# In[22]:


df_58_7 = df_58_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[23]:


df_58_8 = df_58_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[25]:


df_58_8.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_58")


# In[26]:


sc.stop()
spark.stop()


# In[ ]:




