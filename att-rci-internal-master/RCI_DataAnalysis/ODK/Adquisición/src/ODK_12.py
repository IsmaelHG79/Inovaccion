#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
os.environ['JAVA_HOME'] = '/usr/java/jdk1.8.0_162'
os.environ['SPARK_HOME'] = '/opt/cloudera/parcels/CDH-6.2.0-1.cdh6.2.0.p0.967373/lib/spark'
import findspark
findspark.init()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import HiveContext
import pandasql
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


conf = SparkConf().setAppName('odk_12')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[3]:


df_12 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type in ('ATPMW','WITX2','MWIN2','MWITX','RFE80','AMWIN','AOP2','MTX2','MWOTX','AMWOP') AND substr(registry_state,1,10) = '2020-02-04'")


# In[4]:


#df_12.show(truncate=False)


# In[5]:


#Se hace una limpieza de los datos
df_12 = df_12.withColumn("map",regexp_replace('map', '::', ''))
df_12 = df_12.withColumn('map', trim(df_12.map))


# In[6]:


#Se borran columnas que no se usaran en el analisis
columns_to_drop = ['no_informe', 'sourceid','filedate', 'datasetname', 'timestamp', 'transaction_status', 'year', 'month','day', 'filename','hash_id']
df_12= df_12.drop(*columns_to_drop)


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


df_12_1 = df_12.withColumn("m_key",split(df_12['map'],':').getItem(0)).withColumn("m_value",split(df_12['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_12['map'],':').getItem(1)))


# In[10]:


df_12_2 = df_12_1.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("ma"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[11]:


#df_99_2.show(truncate=False)


# In[12]:


global elementos1
elementos1=[{'mw':'AntenaMW'},{'vertical':'Vista'},{'horizontal':'Vista'},{'floor':'Vista'},{'config':'Configuraciones'},{'test':'Pruebas'},{'cambioantena':'Antena'},{'cambioodu':'ODU'},{'chidu':'IDU'},{'wires':'Cable'},{'certrfc':'Equipo de medicion'},{'fotografico':'Vista'},{'testing':'Pruebas'},{'polari':'Vista'},{'side':'Sitio'},{'aligment':'Vista'},{'tarjetas':'Tarjeta'},{'install':'Vista'},{'before':'Vista'},{'after':'Vista'},{'commisioning':'Vista'},{'soporte':'soporte'}]


# In[13]:


global search_dic
path = "/user/eg2202/Docs/ATPMW_patron_search.csv"
searchs = spark.read.format("csv").option("header", "true").load(path)
search_collect_12=searchs.collect()
search_dic = list(map(lambda x : {"atributo":x[0], "elemento":x[1]},search_collect_12))


# In[14]:


def searchATPMW(subgrupo):
    for i in search_dic:
        if i['atributo'].find(subgrupo)!=-1:
            word=i['elemento']
            break
        else:
            word='Not Found'
    return word
    


# In[15]:


#searchATPMW = udf(search_ATPMW, StringType())


# In[16]:


def search(grupo,subgrupos,dictionary, keys, values):
    word='Not Found'
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root'
    elif (len(groups)==3):
        if groups[2].lower().find('inventory')!=-1:
            for k in subgrupos:
                if k.lower().find('element')!=-1:
                    indexx=subgrupos.index(k)
                    word=values[indexx]
                    break
                else:
                    word='Not Found'
        else:
            for i in elementos1:
                if groups[2].lower().find(i.keys()[0])!=-1:
                    word=i.values()[0]
                    break
                else:
                    word='Not Found'

    elif (len(groups)==4):
        if groups[3].lower().find('inventory')!=-1:
            for k in subgrupos:
                if k.lower().find('element')!=-1:
                    indexx=subgrupos.index(k)
                    word=values[indexx]
                    break
                else:
                    word='Not Found'
        else:
            for i in elementos1:
                if groups[3].lower().find(i.keys()[0])!=-1:
                    word=i.values()[0]
                    break
                else:
                    word='Not Found'
                    
    elif(len(groups)==5):
        if groups[4].lower().find('inventory')!=-1:
            for k in subgrupos:
                if k.lower().find('element')!=-1:
                    indexx=subgrupos.index(k)
                    word=values[indexx]
                    break
                else:
                    word='Not Found'
        else:
            for i in elementos1:
                if groups[4].lower().find(i.keys()[0])!=-1:
                    word=i.values()[0]
                    break
                else:
                    word='Not Found'

    return word
            


# In[17]:


#Se convierne la función a una UDF(User-Defined Function)
#search_element = udf(search, StringType())


# In[18]:


def searchGeneral(clave_form,grupo,subgrupos,dictionary, keys, values):
    if (clave_form=='WITX2' or clave_form=='MWITX' or clave_form=='MWIN2' or clave_form=='RFE80' or clave_form=='AMWIN' or clave_form=='AOP2' or clave_form=='MTX2' or clave_form=='MWOTX' or clave_form=='AMWOP'):
        elemento=search(grupo,subgrupos,dictionary, keys, values)
    elif clave_form=='ATPMW':
        elemento=searchATPMW(subgrupos)
    else:
        elemento='No encontrado'
    return elemento


# In[19]:


search_general = udf(searchGeneral, StringType())


# In[20]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df_12_3=df_12_2.withColumn("tipo_elemento", search_general('cve_type','groups','sub_group','ma','key','value'))


# In[21]:


#df_12_3.show(truncate=False)


# In[22]:


df_12_4 = df_12_3.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[23]:


df_12_5 = df_12_4.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[24]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_12_6 = df_12_5.where(F.col("validate_key") == False).drop("validate_key")


# In[166]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","")
    str_clean_3 = str_clean_2.replace(" ","_").replace("-","_")
   #str_clean_4 = str_clean_3.replace("Activo_Fijo_Manual","Activo").replace("Activo_Manual","Activo").replace("Serie_Manual","Serie").replace("Marca_Manual","Marca")
    str_clean_4 = str_clean_3.replace("activo_fijo","activo").replace("activo_fijo_scanner","activo").replace("activo_scanner","activo").replace('*','')
    str_clean_5 = str_clean_4.replace("_a","").replace("_b","").replace("_del_equipo_de_medicion","")
    str_clean_6 = str_clean_5.replace("strmodel","modelo").replace("strmodelidua", "modelo").replace("strmodelidub","modelo").replace("strmodeltowerb","modelo")
    str_clean_7 = str_clean_6.replace("modeloidua","modelo").replace("modeloidub","modelo").replace("modelotowerb","modelo")
    str_clean_8 = str_clean_7.replace("decazimuthreala","decazimuthreal").replace("decazimuthrealb","decazimuthreal")
    str_clean_9 = str_clean_8.replace("decantennahtfloora","decantennahtfloor").replace("decantennahtfloorb","decantennahtfloor")
    str_clean_10 = str_clean_9.replace("decantennahttwra","decantennahttwr").replace("decantennahttwrb","decantennahttwr")
    str_clean_11 = str_clean_10.replace("decdiameterantennaa","decdiameterantenna").replace("decdiameterantennab","decdiameterantenna")
    str_clean_12 = str_clean_11.replace("_inventariar","").replace("decazimuthreal","azimuth_real")
    str_clean_13 = str_clean_12.replace("imgalarmsaa","imgalarms").replace("imgalarmsab","imgalarms").replace("imgalarmsba","imgalarms").replace("imgalarmsbb","imgalarms")
    str_clean_14 = str_clean_13.replace("imglinkconfigaa","imglinkconfig").replace("imglinkconfigab","imglinkconfig").replace("imglinkconfigba","imglinkconfig").replace("imglinkconfigbb","imglinkconfig")
    str_clean_15 = str_clean_14.replace("keyelement","elemento").replace("strelement","elemento").replace("strelementidua","elemento").replace("strelementidub","elemento").replace("strelementtowerb","elemento")
    str_clean_16 = str_clean_15.replace("elementoidua","elemento").replace("elementoidub","elemento").replace("elementotowerb","elemento").replace("/","")
    str_clean_17 = str_clean_16.decode("utf-8").replace(u"cÃ£Â³digo_de_sitio", "codigo_de_sitio").encode("utf-8")
    return str_clean_16
clean_str_udf = udf(clean_str, StringType())


# In[167]:


df_12_7 = df_12_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[168]:


df_12_8 = df_12_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[178]:


print len(df_12_9.columns)


# In[174]:


df_12_9 = df_12_8.withColumn('codigo_sitio', 
                    F.concat(F.col('codigo_de_sitio'),F.lit(''), F.col('cÃ£Â³digo_de_sitio'))).drop('codigo_de_sitio').drop('cÃ£Â³digo_de_sitio')


# In[175]:


#df_12_8.show(truncate=False)


# In[176]:


df_12_9.printSchema()


# In[185]:


df_12_9.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_12")


# In[65]:


sc.stop()
spark.stop()

