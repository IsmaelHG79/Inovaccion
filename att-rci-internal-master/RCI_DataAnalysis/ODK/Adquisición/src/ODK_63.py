#!/usr/bin/env python
# coding: utf-8

# # Adquisición de datos ODK 63

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


conf = SparkConf().setAppName('AIEC')      .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# Se importan los datos del ODK: 

# In[3]:


#Cargando el diccionario de elementos
df_63 = spark.sql("select * from rci_network_db.tx_odk WHERE cve_type in ('AIEC','IECV2') AND substr(registry_state,1,10) = '2020-02-04'")


# In[4]:


#Se hace una limpieza de los datos
df63_1 = df_63.withColumn("map",regexp_replace('map', '(?<=\d{2}):(?=[0-9])', ''))
#df63_2 = df63_1.withColumn("map",regexp_replace('map', ':::', ''))
#df63_1 = df63_1.withColumn("map",regexp_replace('map', '(?<=\d{2}):(?=[0-9])', ''))
df63_1 = df63_1.withColumn('map', trim(df63_1.map))


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


df63_2 = df63_1.withColumn("m_key",split(df63_1['map'],':').getItem(0)).withColumn("m_value",split(df63_1['map'],':').getItem(1)).withColumn("validate_key_dad",validate_key_dad_udf(split(df63_1['map'],':').getItem(1)))


# In[11]:


df63_3 = df63_2.groupBy("cve_type","id_form","groups").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"),F.collect_list("m_value").alias("value"),F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True,F.col("m_key").cast("string")).otherwise("root")).alias("key_dad"))


# In[14]:


##Lista de elementos únicos en este tipo de ODK
global lista
lista=['PATCH PANEL', 'Si Edge II-C Capricorn Pro', 'Raisecon RAX700', 'ETX-205A', '417040008', 'AR1220', '3430', 'RAX700', 'Asr920', '3903', 'ASR-920-4SZ-D', 'ASR920', 'Asr920-4sz-D V01', '1800II', 'Etc', 'RAX711B', 'Rax711-B', 'Att', '5508', 'Rax700', 'RAISECOM RAX700', 'DFO', 'ASR-920-4SZ-D V01', 'ODF', 'Ciena 3930', 'ASR-920-4SZ-D-V01', 'Asr-920-4sz-Dv01', 'Metro NID', 'AR1220E', 'RAX711', '5142', 'SKYEDGE II CAPRICORN PRO', 'Rax711', 'BUC NJT5193', '3930', 'Gilat', 'ASR-920-4SZ-DV01', 'Asr-920-4sz-D V01', '3039', 'Ciena3930', 'SKYEDGE II-C / CAPRICORN PRO', 'LT-S', 'Asr-920-4sz-d', 'ETX-203AX', 'PANEL DE PARCHEO 12 POSICIONES', 'CIENA 3930', 'ASÍ 920 4SZ D V01', 'RAISECOM RAX711', 'Raz700', 'Capricorn pro DC2/2ps/24vodu', '3939']


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
        if (grupo.find("Pic")!=-1):
            word='Vista'
        else:
            for i in array:
                key=i.split(':')[0]
                value=i.split(':')[1]
                if(key!='' and value!=''):
                    if key=='Modelo':
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
df63_4=df63_3.withColumn("tipo_elemento", search_element('value'))


# In[20]:


#Se realiza un explode de los array
df63_5 = df63_4.select("cve_type","id_form","groups","key_dad","tipo_elemento",explode_outer(arrays_zip("sub_group","key","value","validate_key")))


# In[22]:


#Se seleccionan todas las columnas
df63_5 = df63_5.select("cve_type","id_form","groups","key_dad","tipo_elemento","col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key")


# In[24]:


#Se filtra por los hijos del key_dad y se elimina la columna
df63_6 = df63_5.where(F.col("validate_key") == False).drop("validate_key")


# In[25]:


def clean_str(string):
    str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
    str_clean_1 = str_clean.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","")
    str_clean_3 = str_clean_2.replace(" ","_").replace("-","_").replace("activo_fijo","activo")
    
    return str_clean_3
    
clean_str_udf = udf(clean_str, StringType())


# In[26]:


df63_7 = df63_6.withColumn("key_clean",clean_str_udf("key")).drop("key")


# In[28]:


df_63_8 = df63_7.groupBy("cve_type","id_form","groups","key_dad","tipo_elemento").pivot("key_clean").agg(concat_ws("|",F.collect_list("value") ))


# In[1]:


columnas=['vista_fo_a_amp_301514997115153.jpg_image/jpeg',
       'vista_fo_a_amp_301515177291552.jpg_image/jpeg',
       'vista_fo_a_amp_301515539539064.jpg_image/jpeg',
       'vista_fo_a_amp_301515623798381.jpg_image/jpeg',
       'vista_fo_a_amp_301515686498430.jpg_image/jpeg',
       'vista_fo_a_amp_301515694044038.jpg_image/jpeg',
       'vista_fo_a_amp_301515710237852.jpg_image/jpeg',
       'vista_fo_a_amp_301516295980083.jpg_image/jpeg',
       'vista_fo_a_amp_301516305385747.jpg_image/jpeg',
       'vista_fo_a_amp_301516320004859.jpg_image/jpeg',
       'vista_fo_a_amp_301516385435659.jpg_image/jpeg',
       'vista_fo_a_amp_301516646406619.jpg_image/jpeg',
       'vista_fo_a_amp_301516651051267.jpg_image/jpeg',
       'vista_fo_a_amp_301516722751823.jpg_image/jpeg',
       'vista_fo_a_amp_301516726752385.jpg_image/jpeg',
       'vista_fo_a_amp_301516742298468.jpg_image/jpeg',
       'vista_fo_a_amp_301516750177434.jpg_image/jpeg',
       'vista_fo_a_amp_301516820122611.jpg_image/jpeg',
       'vista_fo_a_amp_301516823748285.jpg_image/jpeg',
       'vista_fo_a_amp_301516827606570.jpg_image/jpeg',
       'vista_fo_a_amp_301516830561480.jpg_image/jpeg',
       'vista_fo_a_amp_301516906325141.jpg_image/jpeg',
       'vista_fo_a_amp_301516986331486.jpg_image/jpeg',
       'vista_fo_a_amp_301516993823224.jpg_image/jpeg',
       'vista_fo_a_amp_301517007943430.jpg_image/jpeg',
       'vista_fo_a_amp_301517266946566.jpg_image/jpeg',
       'vista_fo_a_amp_301517368200005.jpg_image/jpeg',
       'vista_fo_a_amp_301517425779845.jpg_image/jpeg',
       'vista_fo_a_amp_301517539992602.jpg_image/jpeg',
       'vista_fo_a_amp_301517542855603.jpg_image/jpeg',
       'vista_fo_a_amp_301517544006003.jpg_image/jpeg',
       'vista_fo_a_amp_301517545572123.jpg_image/jpeg',
       'vista_fo_a_amp_301517546977764.jpg_image/jpeg',
       'vista_fo_a_amp_301517548137290.jpg_image/jpeg',
       'vista_fo_a_amp_301517549068304.jpg_image/jpeg',
       'vista_fo_a_amp_301518109467327.jpg_image/jpeg',
       'vista_fo_a_amp_301518115497403.jpg_image/jpeg',
       'vista_fo_a_amp_301518116159669.jpg_image/jpeg',
       'vista_fo_a_amp_301518123502314.jpg_image/jpeg',
       'vista_fo_a_amp_301518126939455.jpg_image/jpeg',
       'vista_fo_a_amp_301518136062509.jpg_image/jpeg',
       'vista_fo_a_amp_301518190696450.jpg_image/jpeg',
       'vista_fo_a_amp_301518204138362.jpg_image/jpeg',
       'vista_fo_a_amp_301518207933830.jpg_image/jpeg',
       'vista_fo_a_amp_301518211639856.jpg_image/jpeg',
       'vista_fo_a_amp_301518558857725.jpg_image/jpeg',
       'vista_fo_a_amp_301518566245355.jpg_image/jpeg',
       'vista_fo_a_amp_301518633927936.jpg_image/jpeg',
       'vista_fo_a_amp_301518817181688.jpg_image/jpeg',
       'vista_fo_a_amp_301518828201976.jpg_image/jpeg',
       'vista_fo_a_amp_301519128297359.jpg_image/jpeg',
       'vista_fo_a_amp_301519403929061.jpg_image/jpeg',
       'vista_fo_a_amp_301519409836263.jpg_image/jpeg',
       'vista_fo_a_amp_301519418358051.jpg_image/jpeg',
       'vista_fo_a_amp_301519424496533.jpg_image/jpeg',
       'vista_fo_a_amp_301519668993974.jpg_image/jpeg',
       'vista_fo_a_amp_301519752812089.jpg_image/jpeg',
       'vista_fo_a_amp_301519753684525.jpg_image/jpeg',
       'vista_fo_a_amp_301519757006397.jpg_image/jpeg',
       'vista_fo_a_amp_301519764003071.jpg_image/jpeg',
       'vista_fo_a_amp_301519851131583.jpg_image/jpeg',
       'vista_fo_a_amp_301519860901767.jpg_image/jpeg',
       'vista_fo_a_amp_301519925863319.jpg_image/jpeg',
       'vista_fo_a_amp_301519936382645.jpg_image/jpeg',
       'vista_fo_a_amp_301520011352189.jpg_image/jpeg',
       'vista_fo_a_amp_301520014165645.jpg_image/jpeg',
       'vista_fo_a_amp_301520268622514.jpg_image/jpeg',
       'vista_fo_a_amp_301520276160652.jpg_image/jpeg',
       'vista_fo_a_amp_301520282009368.jpg_image/jpeg',
       'vista_fo_a_amp_301520287496719.jpg_image/jpeg',
       'vista_fo_a_amp_301520359243120.jpg_image/jpeg',
       'vista_fo_a_amp_301520362616360.jpg_image/jpeg',
       'vista_fo_a_amp_301520375605544.jpg_image/jpeg',
       'vista_fo_a_amp_301520379313428.jpg_image/jpeg',
       'vista_fo_a_amp_301520440516799.jpg_image/jpeg',
       'vista_fo_a_amp_301520443932941.jpg_image/jpeg',
       'vista_fo_a_amp_301520446723208.jpg_image/jpeg',
       'vista_fo_a_amp_301520448748700.jpg_image/jpeg',
       'vista_fo_a_amp_301520451901126.jpg_image/jpeg',
       'vista_fo_a_amp_301520457131940.jpg_image/jpeg',
       'vista_fo_a_amp_301520458713412.jpg_image/jpeg',
       'vista_fo_a_amp_301520470603433.jpg_image/jpeg',
       'vista_fo_a_amp_301520521988137.jpg_image/jpeg',
       'vista_fo_a_amp_301520524196056.jpg_image/jpeg',
       'vista_fo_a_amp_301520527497362.jpg_image/jpeg',
       'vista_fo_a_amp_301520532256224.jpg_image/jpeg',
       'vista_fo_a_amp_301520549489989.jpg_image/jpeg',
       'vista_fo_a_amp_301521048755629.jpg_image/jpeg',
       'vista_fo_a_amp_301521058989730.jpg_image/jpeg',
       'vista_fo_a_amp_301521674449086.jpg_image/jpeg',
       'vista_fo_a_amp_301521832816377.jpg_image/jpeg',
       'vista_fo_a_amp_301521840311754.jpg_image/jpeg',
       'vista_fo_a_amp_301522173373152.jpg_image/jpeg',
       'vista_fo_a_amp_301522263895213.jpg_image/jpeg',
       'vista_fo_a_amp_301522775052787.jpg_image/jpeg',
       'vista_fo_a_amp_301522785780573.jpg_image/jpeg',
       'vista_fo_a_amp_301522792853356.jpg_image/jpeg',
       'vista_fo_a_amp_301523131987414.jpg_image/jpeg',
       'vista_fo_a_amp_301523293302637.jpg_image/jpeg',
       'vista_fo_a_amp_301523556097315.jpg_image/jpeg',
       'vista_fo_a_amp_301523562995936.jpg_image/jpeg',
       'vista_fo_a_amp_301523573591073.jpg_image/jpeg',
       'vista_fo_a_amp_301523896911058.jpg_image/jpeg',
       'vista_fo_a_amp_301524082299130.jpg_image/jpeg',
       'vista_fo_a_amp_301524087967284.jpg_image/jpeg',
       'vista_fo_a_amp_301524595106854.jpg_image/jpeg',
       'vista_fo_a_amp_301524600974850.jpg_image/jpeg',
       'vista_fo_a_amp_301524610641643.jpg_image/jpeg',
       'vista_fo_a_amp_301525117360278.jpg_image/jpeg',
       'vista_fo_a_amp_301525286146777.jpg_image/jpeg',
       'vista_fo_a_amp_301525288539882.jpg_image/jpeg',
       'vista_fo_a_amp_301525369473330.jpg_image/jpeg',
       'vista_fo_a_amp_301525457430206.jpg_image/jpeg',
       'vista_fo_a_amp_301525971176761.jpg_image/jpeg',
       'vista_fo_a_amp_301526054498258.jpg_image/jpeg',
       'vista_fo_a_amp_301526501535534.jpg_image/jpeg',
       'vista_fo_a_amp_301526578429978.jpg_image/jpeg',
       'vista_fo_a_amp_301526580328830.jpg_image/jpeg',
       'vista_fo_a_amp_301526589477754.jpg_image/jpeg',
       'vista_fo_a_amp_301526657290479.jpg_image/jpeg',
       'vista_fo_a_amp_301526666023168.jpg_image/jpeg',
       'vista_fo_a_amp_301526666546337.jpg_image/jpeg',
       'vista_fo_a_amp_301526671391236.jpg_image/jpeg',
       'vista_fo_a_amp_301526682865309.jpg_image/jpeg',
       'vista_fo_a_amp_301526931022403.jpg_image/jpeg',
       'vista_fo_a_amp_301527012560713.jpg_image/jpeg',
       'vista_fo_a_amp_301527179636762.jpg_image/jpeg',
       'vista_fo_a_amp_301527189307113.jpg_image/jpeg',
       'vista_fo_a_amp_301527190050845.jpg_image/jpeg',
       'vista_fo_a_amp_301527267223703.jpg_image/jpeg',
       'vista_fo_a_amp_301527277660245.jpg_image/jpeg',
       'vista_fo_a_amp_301527279168976.jpg_image/jpeg',
       'vista_fo_a_amp_301527283707399.jpg_image/jpeg',
       'vista_fo_a_amp_301527875277631.jpg_image/jpeg',
       'vista_fo_a_amp_301528326120693.jpg_image/jpeg',
       'vista_fo_a_amp_301528408187896.jpg_image/jpeg',
       'vista_fo_a_amp_301528743284112.jpg_image/jpeg',
       'vista_fo_a_amp_301528753003421.jpg_image/jpeg',
       'vista_fo_a_amp_301528765557671.jpg_image/jpeg',
       'vista_fo_a_amp_301528820170399.jpg_image/jpeg',
       'vista_fo_a_amp_301528831291116.jpg_image/jpeg',
       'vista_fo_a_amp_301528836121138.jpg_image/jpeg',
       'vista_fo_a_amp_301529086358114.jpg_image/jpeg',
       'vista_fo_a_amp_301529616605468.jpg_image/jpeg',
       'vista_fo_a_amp_301529701043945.jpg_image/jpeg',
       'vista_fo_a_amp_301529710022664.jpg_image/jpeg',
       'vista_fo_a_amp_301530042398578.jpg_image/jpeg',
       'vista_fo_a_amp_301530112299578.jpg_image/jpeg',
       'vista_fo_a_amp_301530122882879.jpg_image/jpeg',
       'vista_fo_a_amp_301530128937585.jpg_image/jpeg',
       'vista_fo_a_amp_301530198207098.jpg_image/jpeg',
       'vista_fo_a_amp_301530561133673.jpg_image/jpeg',
       'vista_fo_a_amp_301531234169662.jpg_image/jpeg',
       'vista_fo_a_amp_301531238249973.jpg_image/jpeg',
       'vista_fo_a_amp_301531269626825.jpg_image/jpeg',
       'vista_fo_a_amp_301533325861403.jpg_image/jpeg',
       'vista_fo_a_amp_301533572778776.jpg_image/jpeg',
       'vista_fo_a_amp_301533589692529.jpg_image/jpeg',
       'vista_fo_a_amp_301533659072408.jpg_image/jpeg',
       'vista_fo_a_amp_301533671200429.jpg_image/jpeg',
       'vista_fo_a_amp_301533745137478.jpg_image/jpeg',
       'vista_fo_a_amp_301533754311405.jpg_image/jpeg',
       'vista_fo_a_amp_301533756252400.jpg_image/jpeg',
       'vista_fo_a_amp_301533759466775.jpg_image/jpeg',
       'vista_fo_a_amp_301533836235086.jpg_image/jpeg',
       'vista_fo_a_amp_301533837627502.jpg_image/jpeg',
       'vista_fo_a_amp_301533845232535.jpg_image/jpeg',
       'vista_fo_a_amp_301533912602737.jpg_image/jpeg',
       'vista_fo_a_amp_301534266091308.jpg_image/jpeg',
       'vista_fo_a_amp_301534279844304.jpg_image/jpeg',
       'vista_fo_a_amp_301534345959720.jpg_image/jpeg',
       'vista_fo_a_amp_301534520895388.jpg_image/jpeg',
       'vista_fo_a_amp_301534532679019.jpg_image/jpeg',
       'vista_fo_a_amp_301535142612880.jpg_image/jpeg',
       'vista_fo_a_amp_301535575202255.jpg_image/jpeg',
       'vista_fo_a_amp_301535646444738.jpg_image/jpeg',
       'vista_fo_a_amp_301535652352336.jpg_image/jpeg',
       'vista_fo_a_amp_301535652728811.jpg_image/jpeg',
       'vista_fo_a_amp_301535659432511.jpg_image/jpeg',
       'vista_fo_a_amp_301535666512588.jpg_image/jpeg',
       'vista_fo_a_amp_301535729658979.jpg_image/jpeg',
       'vista_fo_a_amp_301535736348506.jpg_image/jpeg',
       'vista_fo_a_amp_301535755550838.jpg_image/jpeg',
       'vista_fo_a_amp_301536073924762.jpg_image/jpeg',
       'vista_fo_a_amp_301536087541677.jpg_image/jpeg',
       'vista_fo_a_amp_301536095205184.jpg_image/jpeg',
       'vista_fo_a_amp_301536166079457.jpg_image/jpeg',
       'vista_fo_a_amp_301536178398252.jpg_image/jpeg',
       'vista_fo_a_amp_301536245628856.jpg_image/jpeg',
       'vista_fo_a_amp_301536250220576.jpg_image/jpeg',
       'vista_fo_a_amp_301536252469942.jpg_image/jpeg',
       'vista_fo_a_amp_301536258790333.jpg_image/jpeg',
       'vista_fo_a_amp_301536260591679.jpg_image/jpeg',
       'vista_fo_a_amp_301536262261980.jpg_image/jpeg',
       'vista_fo_a_amp_301536337938423.jpg_image/jpeg',
       'vista_fo_a_amp_301536345688921.jpg_image/jpeg',
       'vista_fo_a_amp_301536615579131.jpg_image/jpeg',
       'vista_fo_a_amp_301536682728221.jpg_image/jpeg',
       'vista_fo_a_amp_301536683280101.jpg_image/jpeg',
       'vista_fo_a_amp_301536686594741.jpg_image/jpeg',
       'vista_fo_a_amp_301536688367048.jpg_image/jpeg',
       'vista_fo_a_amp_301536691179661.jpg_image/jpeg',
       'vista_fo_a_amp_301536698452873.jpg_image/jpeg',
       'vista_fo_a_amp_301536728941412.jpg_image/jpeg',
       'vista_fo_a_amp_301536771316360.jpg_image/jpeg',
       'vista_fo_a_amp_301536779812870.jpg_image/jpeg',
       'vista_fo_a_amp_301536781404960.jpg_image/jpeg',
       'vista_fo_a_amp_301536782870541.jpg_image/jpeg',
       'vista_fo_a_amp_301536788376525.jpg_image/jpeg',
       'vista_fo_a_amp_301536858054059.jpg_image/jpeg',
       'vista_fo_a_amp_301536861681030.jpg_image/jpeg',
       'vista_fo_a_amp_301536868576517.jpg_image/jpeg',
       'vista_fo_a_amp_301536869904308.jpg_image/jpeg',
       'vista_fo_a_amp_301536873259690.jpg_image/jpeg',
       'vista_fo_a_amp_301536875738998.jpg_image/jpeg',
       'vista_fo_a_amp_301536948002034.jpg_image/jpeg',
       'vista_fo_a_amp_301536954119781.jpg_image/jpeg',
       'vista_fo_a_amp_301537222193038.jpg_image/jpeg',
       'vista_fo_a_amp_301537383583520.jpg_image/jpeg',
       'vista_fo_a_amp_301537417274256.jpg_image/jpeg',
       'vista_fo_a_amp_301537551359393.jpg_image/jpeg',
       'vista_fo_a_amp_301537557301939.jpg_image/jpeg',
       'vista_fo_a_amp_301537560979750.jpg_image/jpeg',
       'vista_fo_a_amp_301538091421540.jpg_image/jpeg',
       'vista_fo_a_amp_301538163808275.jpg_image/jpeg',
       'vista_fo_a_amp_301538424385889.jpg_image/jpeg',
       'vista_fo_a_amp_301538430663629.jpg_image/jpeg',
       'vista_fo_a_amp_301538501432804.jpg_image/jpeg',
       'vista_fo_a_amp_301538508680197.jpg_image/jpeg',
       'vista_fo_a_amp_301538588261692.jpg_image/jpeg',
       'vista_fo_a_amp_301538590342736.jpg_image/jpeg',
       'vista_fo_a_amp_301538642368413.jpg_image/jpeg',
       'vista_fo_a_amp_301538674030450.jpg_image/jpeg',
       'vista_fo_a_amp_301538685873913.jpg_image/jpeg',
       'vista_fo_a_amp_301538692678771.jpg_image/jpeg',
       'vista_fo_a_amp_301538695091617.jpg_image/jpeg',
       'vista_fo_a_amp_301538719040686.jpg_image/jpeg',
       'vista_fo_a_amp_301539096683179.jpg_image/jpeg',
       'vista_fo_a_amp_301539104764900.jpg_image/jpeg',
       'vista_fo_a_amp_301539112108154.jpg_image/jpeg',
       'vista_fo_a_amp_301539113194520.jpg_image/jpeg',
       'vista_fo_a_amp_301539119813074.jpg_image/jpeg',
       'vista_fo_a_amp_301539123552777.jpg_image/jpeg',
       'vista_fo_a_amp_301539183625271.jpg_image/jpeg',
       'vista_fo_a_amp_301539193146654.jpg_image/jpeg',
       'vista_fo_a_amp_301539193147298.jpg_image/jpeg',
       'vista_fo_a_amp_301539224055380.jpg_image/jpeg',
       'vista_fo_a_amp_301539380926328.jpg_image/jpeg',
       'vista_fo_a_amp_301539392103071.jpg_image/jpeg',
       'vista_fo_a_amp_301539648614279.jpg_image/jpeg',
       'vista_fo_a_amp_301539669857705.jpg_image/jpeg',
       'vista_fo_a_amp_301539706326352.jpg_image/jpeg',
       'vista_fo_a_amp_301539707685839.jpg_image/jpeg',
       'vista_fo_a_amp_301539711653692.jpg_image/jpeg',
       'vista_fo_a_amp_301539712855037.jpg_image/jpeg',
       'vista_fo_a_amp_301539716451753.jpg_image/jpeg',
       'vista_fo_a_amp_301539716872832.jpg_image/jpeg',
       'vista_fo_a_amp_301539718135203.jpg_image/jpeg',
       'vista_fo_a_amp_301539721263958.jpg_image/jpeg',
       'vista_fo_a_amp_301539724861733.jpg_image/jpeg',
       'vista_fo_a_amp_301539725252217.jpg_image/jpeg',
       'vista_fo_a_amp_301539798278046.jpg_image/jpeg',
       'vista_fo_a_amp_301539800550282.jpg_image/jpeg',
       'vista_fo_a_amp_301539801360324.jpg_image/jpeg',
       'vista_fo_a_amp_301539804594628.jpg_image/jpeg',
       'vista_fo_a_amp_301539805225054.jpg_image/jpeg',
       'vista_fo_a_amp_301539805947610.jpg_image/jpeg',
       'vista_fo_a_amp_301539813466020.jpg_image/jpeg',
       'vista_fo_a_amp_301539816076620.jpg_image/jpeg',
       'vista_fo_a_amp_301539826717221.jpg_image/jpeg',
       'vista_fo_a_amp_301539828667710.jpg_image/jpeg',
       'vista_fo_a_amp_301539831151317.jpg_image/jpeg',
       'vista_fo_a_amp_301539880767434.jpg_image/jpeg',
       'vista_fo_a_amp_301539889060931.jpg_image/jpeg',
       'vista_fo_a_amp_301539981865643.jpg_image/jpeg',
       'vista_fo_a_amp_301540233376082.jpg_image/jpeg',
       'vista_fo_a_amp_301540239636699.jpg_image/jpeg',
       'vista_fo_a_amp_301540320297279.jpg_image/jpeg',
       'vista_fo_a_amp_301540328990615.jpg_image/jpeg',
       'vista_fo_a_amp_301540329099523.jpg_image/jpeg',
       'vista_fo_a_amp_301540330845158.jpg_image/jpeg',
       'vista_fo_a_amp_301540333468948.jpg_image/jpeg',
       'vista_fo_a_amp_301540335256446.jpg_image/jpeg',
       'vista_fo_a_amp_301540338763848.jpg_image/jpeg',
       'vista_fo_a_amp_301540395292000.jpg_image/jpeg',
       'vista_fo_a_amp_301540405491696.jpg_image/jpeg',
       'vista_fo_a_amp_301540407446082.jpg_image/jpeg',
       'vista_fo_a_amp_301540415360709.jpg_image/jpeg',
       'vista_fo_a_amp_301540419194193.jpg_image/jpeg',
       'vista_fo_a_amp_301540424197461.jpg_image/jpeg',
       'vista_fo_a_amp_301540488982620.jpg_image/jpeg',
       'vista_fo_a_amp_301541012402683.jpg_image/jpeg',
       'vista_fo_a_amp_301541037136154.jpg_image/jpeg',
       'vista_fo_a_amp_301541525014340.jpg_image/jpeg',
       'vista_fo_a_amp_301542138069755.jpg_image/jpeg',
       'vista_fo_a_amp_301542220677853.jpg_image/jpeg',
       'vista_fo_a_amp_301542309172850.jpg_image/jpeg',
       'vista_fo_a_amp_301542395925313.jpg_image/jpeg',
       'vista_fo_a_amp_301542410589654.jpg_image/jpeg',
       'vista_fo_a_amp_301542982799962.jpg_image/jpeg',
       'vista_fo_a_amp_301543007175641.jpg_image/jpeg',
       'vista_fo_a_amp_301543340307151.jpg_image/jpeg',
       'vista_fo_a_amp_301543517260024.jpg_image/jpeg',
       'vista_fo_a_amp_301544559794990.jpg_image/jpeg',
       'vista_fo_a_amp_301544568325449.jpg_image/jpeg',
       'vista_fo_a_amp_301544724730607.jpg_image/jpeg',
       'vista_fo_a_amp_301544737638392.jpg_image/jpeg',
       'vista_fo_a_amp_301544826378563.jpg_image/jpeg',
       'vista_fo_a_amp_301545090843188.jpg_image/jpeg',
       'vista_fo_a_amp_301546483049815.jpg_image/jpeg',
       'vista_fo_a_amp_301546540476287.jpg_image/jpeg',
       'vista_fo_a_amp_301546553542964.jpg_image/jpeg',
       'vista_fo_a_amp_301546558786908.jpg_image/jpeg',
       'vista_fo_a_amp_301546564140296.jpg_image/jpeg',
       'vista_fo_a_amp_301547168258025.jpg_image/jpeg',
       'vista_fo_a_amp_301547232543073.jpg_image/jpeg',
       'vista_fo_a_amp_301547751706056.jpg_image/jpeg',
       'vista_fo_a_amp_301547764602215.jpg_image/jpeg',
       'vista_fo_a_amp_301547767053233.jpg_image/jpeg',
       'vista_fo_a_amp_301548173981760.jpg_image/jpeg',
       'vista_fo_a_amp_301548439560249.jpg_image/jpeg',
       'vista_fo_a_amp_301548444819823.jpg_image/jpeg',
       'vista_fo_a_amp_301548449632198.jpg_image/jpeg',
       'vista_fo_a_amp_301548799263869.jpg_image/jpeg',
       'vista_fo_a_amp_301549568790880.jpg_image/jpeg',
       'vista_fo_a_amp_301549654907905.jpg_image/jpeg',
       'vista_fo_a_amp_301550176468698.jpg_image/jpeg',
       'vista_fo_a_amp_301550260400832.jpg_image/jpeg',
       'vista_fo_a_amp_301550518475353.jpg_image/jpeg',
       'vista_fo_a_amp_301550524606988.jpg_image/jpeg',
       'vista_fo_a_amp_301550531328565.jpg_image/jpeg',
       'vista_fo_a_amp_301550701168344.jpg_image/jpeg',
       'vista_fo_a_amp_301550791950110.jpg_image/jpeg',
       'vista_fo_a_amp_301551135556623.jpg_image/jpeg',
       'vista_fo_a_amp_301551159516415.jpg_image/jpeg',
       'vista_fo_a_amp_301551474549588.jpg_image/jpeg',
       'vista_fo_a_amp_301551810447472.jpg_image/jpeg',
       'vista_fo_a_amp_301551904261372.jpg_image/jpeg',
       'vista_fo_a_amp_301552031197058.jpg_image/jpeg',
       'vista_fo_a_amp_301552505042432.jpg_image/jpeg',
       'vista_fo_a_amp_301552590577143.jpg_image/jpeg',
       'vista_fo_a_amp_301552674311542.jpg_image/jpeg',
       'vista_fo_a_amp_301553206092336.jpg_image/jpeg',
       'vista_fo_a_amp_301553274652562.jpg_image/jpeg',
       'vista_fo_a_amp_301553303135515.jpg_image/jpeg',
       'vista_fo_a_amp_301553645980054.jpg_image/jpeg',
       'vista_fo_a_amp_301553648914091.jpg_image/jpeg',
       'vista_fo_a_amp_301553894729177.jpg_image/jpeg',
       'vista_fo_a_amp_301554321280130.jpg_image/jpeg',
       'vista_fo_a_amp_301554346469260.jpg_image/jpeg',
       'vista_fo_a_amp_301554404591600.jpg_image/jpeg',
       'vista_fo_a_amp_301554426152926.jpg_image/jpeg',
       'vista_fo_a_amp_301554921632751.jpeg_image/jpeg',
       'vista_fo_a_amp_301556568120756.jpg_image/jpeg',
       'vista_fo_a_amp_301556572055982.jpg_image/jpeg',
       'vista_fo_a_amp_301556576174663.jpg_image/jpeg',
       'vista_fo_a_amp_301556612764344.jpg_image/jpeg',
       'vista_fo_a_amp_301556668925500.jpg_image/jpeg',
       'vista_fo_a_amp_301557620377043.jpg_image/jpeg',
       'vista_fo_a_amp_301558390942081.jpg_image/jpeg',
       'vista_fo_a_amp_301558506568547.jpg_image/jpeg',
       'vista_fo_a_amp_301562181620300null_application/octet_stream',
       'vista_fo_a_amp_301562963489099.jpg_image/jpeg',
       'vista_fo_a_amp_301564029384859.jpg_image/jpeg',
       'vista_l3_vlan1_resultado', 'vista_l3_vlan2_resultado',
       'vista_l3_vlan4_resultado', 'vista_l3_vlan5_resultado',
       'vista_l3_vlan6_resultado']


# In[ ]:


df_63_9 = df_63_8.drop(*columnas)


# In[30]:


df_63_9.write.format("parquet").mode("overwrite").saveAsTable("rci_network_db.tx_stg_tabla_columnar_odk_63")


# In[31]:


sc.stop()
spark.stop()


# In[ ]:




