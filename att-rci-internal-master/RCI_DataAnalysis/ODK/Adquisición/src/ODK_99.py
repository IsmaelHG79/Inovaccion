#!/usr/bin/env python
# coding: utf-8

# In[2]:
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


# In[3]:


conf = SparkConf().setAppName('odk_99')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[5]:


df_99 = spark.sql("SELECT * FROM rci_network_db.tx_odk WHERE cve_type in ('SINV','SINR') AND substr(registry_state,1,10) = '2020-02-04'")


# In[6]:


df_99.show(truncate=False)


# In[5]:


#Se hace una limpieza de los datos
#df_38 = df_38.withColumn("ma",regexp_replace('ma', '::', ''))
#df_38 = df_38.withColumn('ma', trim(df_58.ma))


# In[7]:


#Se borran columnas que no se usaran en el analisis
columns_to_drop = ['no_informe', 'sourceid','filedate', 'datasetname', 'timestamp', 'transaction_status', 'filename','hash_id']
df_99 = df_99.drop(*columns_to_drop)


# In[8]:


#Función para validar el key_dad
def validate_key_dad(string):
    res = False
    if string == '':
        res =True
    return res


# In[9]:


validate_key_dad_udf = udf(validate_key_dad, BooleanType())


# In[10]:


df_99_1 = df_99.withColumn("m_key",split(df_99['map'],':').getItem(0)).withColumn("m_value",split(df_99['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df_99['map'],':').getItem(1)))


# In[12]:


df_99_2 = df_99_1.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("map").alias("ma"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[13]:


global elementos1,elementos2
elementos1=[{'cabinet':'Gabinete'},{'struct':'Estructura'},{'shelter':'shelter'},{'cbbattery':'Banco de baterias'},{'cbattery':'Bateria'},{'srack':'Rack'},{'sbattery':'Bateria'},{'sbbank':'Banco de baterias'}]
elementos2=[{'twelement':'keytelement'},{'irack':'ertype'},{'lrack':'ertype'},{'powerdc':'dcetype'},{'hvac':'hvactype'},{'other':'othtype'},{'ecabinet':'ecabtype'},{'gen':'gentype'}]


# In[14]:


def search(grupo,subgrupos,dictionary, keys, values):
    word='Not Found'
    groups=grupo.split(':')
    if (len(groups)<=2):
        word='root'
    elif (len(groups)==3):
        for i in elementos1:
            if groups[2].lower().find(i.keys()[0])!=-1:
                word=i.values()[0]
                break
            else:
                word='Not Found'
        if word=='Not Found':
            for j in elementos2:
                if groups[2].lower().find(j.keys()[0])!=-1:
                    for k in subgrupos:
                        if k.lower().find(j.values()[0])!=-1:
                            indexx=subgrupos.index(k)
                            word=values[indexx]
                            bandera=True
                            break
                        else:
                            bandera=False
                            word='Not found'
                    if bandera:
                        break
                    
    elif(len(groups)==4):
        for i in elementos1:
            if groups[3].lower().find(i.keys()[0])!=-1:
                word=i.values()[0]
                break
            else:
                word='Not Found'
        if word=='Not Found':
            for j in elementos2:
                if groups[3].lower().find(j.keys()[0])!=-1:
                    for k in subgrupos:
                        if k.lower().find(j.values()[0])!=-1:
                            indexx=subgrupos.index(k)
                            word=values[indexx]
                            bandera=True
                            break
                        else:
                            bandera=False
                            word='Not found'
                    if bandera:
                        break
    elif(len(groups)==5):
        for i in elementos1:
            if groups[4].lower().find(i.keys()[0])!=-1:
                word=i.values()[0]
                break
            else:
                word='Not Found'
        if word=='Not Found':
            for j in elementos2:
                if groups[4].lower().find(j.keys()[0])!=-1:
                    for k in subgrupos:
                        if k.lower().find(j.values()[0])!=-1:
                            indexx=subgrupos.index(k)
                            word=values[indexx]
                            bandera=True
                            break
                        else:
                            bandera=False
                            word='Not found'
                    if bandera:
                        break
    return word
            


# In[15]:


#Se convierne la función a una UDF(User-Defined Function)
search_element = udf(search, StringType())


# In[16]:


#Se agrega la nueva columna con el tipo de elemento que tiene la agrupación
df_99_3=df_99_2.withColumn("Elemento", search_element('groups','sub_group','ma','key','value'))


# In[17]:


df_99_4 = df_99_3.select("cve_type","id_form","groups","key_dad","Elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[18]:


df_99_5 = df_99_4.select("cve_type","id_form","groups","key_dad","Elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[19]:


#Se filtra por los hijos del key_dad y se elimina la columna
df_99_6 = df_99_5.where(F.col("validate_key") == False).drop("validate_key")


# In[20]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
    str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","")
    str_clean_3 = str_clean_2.replace(" ","_").replace("-","_")
    str_clean_4 = str_clean_3.replace("activo_fijo_manual","activo").replace("activo_manual","activo").replace("serie_manual","serie").replace("marca_manual","marca")
    str_clean_5 = str_clean_4.replace("tipo_de_elemento","tipo_elemento").replace("tipo_de_equipo","tipo_equipo").replace("?","").replace("¿","")
    return str_clean_5
clean_str_udf = udf(clean_str, StringType())


# In[21]:


df_99_7 = df_99_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[22]:


df_99_8 = df_99_7.groupBy("cve_type","id_form",'groups',"key_dad","Elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value")))


# In[23]:


cols_to="Irving.garcia@wfinet.com.mx|Fernando.mendoza@wfinet.com.mx|cesar.uribe@wfinet.com.mx|claudia.resendiz@wfinet.com.mx|eduardo.torres.1@huawei.com|eduardo.torres1@huawei.com|eduardo.torres@Huawei.com|eduardo.torres@huawei.com|emmanuel.estrada.ortiz@huawei.com|fernando.martinez@wfinet.com.mx|fralvarezh@gmail.com|irving.garcia@wfinet.com.mx|jafet.vera@wfinet.com.mx|javiair.jjr@gmail.com|jmgalvanv@hotmail.com|jose.morales@wfinet.com.mx|josue.jimenez@wfinet.com.mx|luis.quintero@tinnova.mx|luis.rodriguez@wfinet.com.mx|mauroF.Diaz@huawei.com|maurof.diaz@huawei.com|miguel.acosta@huawei.com|pedro.montalvo@wfinet.com.mx|raul.perez810823@gmail.com|sergio.paz@huawei.com"
columns_a_borrar=cols_to.split('|')


# In[24]:


df_99_9 = df_99_8.drop(*columns_a_borrar)


# In[25]:


df_99_9.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_99")


# In[24]:


sc.stop()


# In[25]:


spark.stop()

