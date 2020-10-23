#!/usr/bin/env python
# coding: utf-8

# <div style="width: 100%; clear: both; font-family: Verdana;">
# <div style="float: left; width: 50%;font-family: Verdana;">
# <img src="https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/doc/att-logo1.png" align="left">
# </div>
# <div style="float: right; width: 200%;">
# <p style="margin: 0; padding-top: 20px; text-align:right;color:rgb(193, 38, 184)"><strong>Axity - AT&T.
#     Ciclo de vida de elementos de inventario</strong></p>
# </div>
# </div>
# <div style="width:100%;">&nbsp;</div>

# # Exploratory Data Analysis
# ## Ciclo de vida de elementos de inventario.
# ### Axity - AT&T.

# ## Descripción
# Analizaremos los datos de las fuentes de inventarios de AT&T con un tratamiento estadístico descriptivo para hacer el tracking del ciclo de vida de los elementos de red. Se creará un EDA enfocado al gestor Sedona. Serán documentados los catálogos propuestos junto a su respectivo tratamiento de datos. La fuente que corresponde a este análisis es el:
# 
# * **Gestor Sedona**
# 
# Primero cargamos las librerías necesarias.

# #### Conectando al Datalake

# In[4]:


import os
os.environ['JAVA_HOME'] = '/usr/java/jdk1.8.0_162'
os.environ['SPARK_HOME'] = '/opt/cloudera/parcels/CDH-6.2.0-1.cdh6.2.0.p0.967373/lib/spark'
import findspark
findspark.init()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import HiveContext


# In[5]:


conf = SparkConf().setAppName('Sedona')      .setMaster('yarn').set("spark.yarn.queue","root.eda")      .set("spark.kryoserializer.buffer.mb","128").set("spark.yarn.executor.memoryOverhead","409")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)


# In[6]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import re

from pyspark.sql.functions import udf ,col
from pyspark.sql.types import IntegerType,StringType

get_ipython().magic(u'matplotlib inline')

from bokeh.io import show, output_notebook, output_file 
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20_9,Category20c_7,Category10_5,Category10_6,Category20c_8,Plasma256
output_notebook()


# ---
# ### 1.1 Recolección de los datos: 

# *IMPORTANTE*: Si se requieren ver datos de otro periódo, se debe cambiar los filtros ```year = <año-a-ejecutar>```, ```month = <mes-a-ejecutar>```, ```day = <día-a-ejecutar>``` de las tablas en la siguiente celda:

# In[7]:


# reglas para serie con pyspark
#sobre el df que se carga con pysaprk, se le agrega una columna 
#con el nombre de serie_cleaned. el cual contiene valores 0 y 1


# Se crea el dataframe de spark

# In[8]:


df_load1 = spark.sql("SELECT inventory_type,serial_number,system_name,site_id,ip,longitude,latitude FROM tx_sedona_huawei").cache()#.toPandas() 


# Creamos una función para el tratamiento de datos en spark el cual contiene la reglas definidas para la columna serie:

# In[9]:


def validate_rule(string):    
    search_list=[" ",'!','%','$',"<",">","^",'¡',"+","N/A",u'¿','~','#','Ñ',"Ã","Åƒ","Ã‹","Ã³",'Ë','*','?',"ILEGIBLE", "VICIBLE","VISIBLE","INCOMPLETO"]
    str_temp = string.encode('utf-8')
    if str_temp.upper() == "BORRADO":
      return 1
    elif len(str_temp) < 6:
      return 1
    elif any(ext in str_temp.upper()for ext in search_list):
      return 1
    else:
      return 0


# Se crea un udf en spark sobre la función ya creada.

# In[10]:


validate_rule_udf = udf(validate_rule, IntegerType())


# Se le agrega una nueva columna al dataframe de spark; la nueva columna es la validacion de la columna serie con respecto al udf que creamos.

# In[11]:


df_serie1 = df_load1.withColumn("serie_cleaned",validate_rule_udf(col("serial_number"))).cache()


# In[12]:


def coding_rule(string):
    test = u'%s' % (string)
    str_temp = test.encode('utf-8')
    return str_temp
coding_str_udf = udf(coding_rule, StringType())


# In[13]:


df_carga = df_load1.withColumn("inventory_type_Cod",coding_str_udf(col("inventory_type")))                     .withColumn("longitude_Cod",coding_str_udf(col("longitude")))                     .withColumn("latitude_Cod",coding_str_udf(col("latitude")))                     .withColumn("system_name_Cod",coding_str_udf(col("system_name")))                     .withColumn("serial_number_Cod",coding_str_udf(col("serial_number")))                     .withColumn("site_id_Cod",coding_str_udf(col("site_id")))                     .withColumn("ip_Cod",coding_str_udf(col("ip")))
                    #.withColumn("serie_cleaned_Cod",coding_str_udf(col("serie_cleaned"))) \


# Se convierte el dataframe de spark a un dataframe de pandas.

# In[14]:


Sedona_hwi = df_load1.toPandas()


# Hemos recolectado los campos a analizar de la fuente Sedona_huawei.

# Por razones técnicas, se creará la bandera *serie_cleaned* desde python para este caso.

# In[15]:


search_list=[" ",'!','%','$',"<",">","^",'¡',"+","N/A",u'¿','~','#',
             'Ñ',"Ã","Åƒ","Ã‹","Ã³",'Ë','*','?',"ILEGIBLE", "VICIBLE",
             "VISIBLE","INCOMPLETO","BORRADO"]

Sedona_hwi['serie_cleaned']=0
Sedona_hwi.serie_cleaned.loc[(Sedona_hwi.serial_number.isin(search_list)) |
                            (Sedona_hwi.serial_number.str.len<6)]=1


# ## Gestor Sedona Huawei
# Una muestra de la fuente Sedona Huawei.

# In[16]:


Sedona_hwi.head()


# ### Diccionario de datos.
# A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  
# 
# * **inventory_type**: Tipo de elemento del inventario.
# * **serial_number**: Número de serie.
# * **system_name**: Nombre del sistema.
# * **site_id**: Código de sitio.
# * **ip**: Dirección IP.
# * **longitude**: Coordenada Longitud.
# * **latitude**: Coordenada Latitud.
# * **serie_cleaned**: Bandera que indica el estado del número de serie, 0 implica buen estado, 1 implica mal estado.

# ---
# ### 1.2 Recolección de los datos:

# In[17]:


df_load2 = spark.sql("SELECT system_name,ip_address,vendor,serial_number,site_id FROM tx_sedona_ne").cache()#.toPandas() 


# In[18]:


df_serie2 = df_load2.withColumn("serie_cleaned",validate_rule_udf(col("serial_number"))).cache()


# In[19]:


Sedona_ne = df_serie2.toPandas()


# Hemos recolectado los campos a analizar de la fuente Sedona_ne.

# ## Gestor Sedona NE
# Una muestra de la fuente Sedona NE.

# In[20]:


Sedona_ne.head()


# ### Diccionario de datos.
# A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  
# 
# * **system_name**: Nombre del sistema.
# * **ip_address**: Dirección IP.
# * **vendor**: Proveedor.
# * **serial_number**: Número de serie.
# * **site_id**: Sitio.
# * **serie_cleaned**: Bandera que indica el estado del número de serie, 0 implica buen estado, 1 implica mal estado.

# ---
# ### 1.3 Recolección de los datos:

# In[21]:


df_load3 = spark.sql("SELECT vendor,inventory_type,ip,site_id,longitude,latitude,serial_number,system_name FROM tx_sedona_nokia").cache()#.toPandas() 


# In[22]:


df_serie3 = df_load3.withColumn("serie_cleaned",validate_rule_udf(col("serial_number"))).cache()


# In[23]:


Sedona_Nokia = df_serie3.toPandas()


# Hemos recolectado los campos a analizar de la fuente Sedona_nokia.

# ### Gestor Sedona Nokia
# Una muestra de la fuente Sedona Nokia.

# In[24]:


Sedona_Nokia.head()


# ### Diccionario de datos.
# A continuación se enlistan los campos de la fuente con una breve descripción de negocio.  
# 
# * **vendor**: Proveedor.
# * **inventory_type**: Tipo de elemento del inventario.
# * **ip**: Dirección IP.
# * **site_id**: Código de sitio.
# * **longitude**: Coordenada Longitud.
# * **latitude**: Coordenada Latitud.
# * **serial_number**: Número de serie.
# * **system_name**: Nombre del sistema.
# * **serie_cleaned**: Bandera que indica el estado del número de serie, 0 implica buen estado, 1 implica mal estado.

# ---
# ### 2.1 Descripción de las fuentes.
# En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.

# In[25]:


campos=Sedona_hwi.columns
print 'Columnas de la fuente Sedona_NE son: ',list(campos)
pd.DataFrame(Sedona_hwi.dtypes,columns=['Tipo de objeto Sedona_hwi'])


# In[26]:


print 'renglones = ',Sedona_hwi.shape[0],' columnas = ',Sedona_hwi.shape[1]


# In[27]:


#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes=[v for v in Sedona_hwi.columns if v not in NOrelevantes]

Sedona_hwi[relevantes].describe(include='all')


# #### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

# * Como posibles catálogos se tienen: *inventory_type*, y *site_id*.
# * Se observa que existen campos en blanco en varios campos.

# #### Se proponen catálogos derivados de la fuente Sedona_hwi con los siguientes campos:
#     
# * **inventory_type**: Tipo de elemento del inventario..
# * **site_id**: Código de sitio.  
# 
# Estos catálogos nos ayudarán a mapear todos los diferentes proyectos que existen en los cuales hay un activo.
# 

# ---
# ### 2.2 Descripción de las fuentes.
# En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.

# In[28]:


campos=Sedona_ne.columns
print 'Columnas de la fuente Sedona_NE son: ',list(campos)
pd.DataFrame(Sedona_ne.dtypes,columns=['Tipo de objeto Sedona_NE'])


# In[29]:


print 'renglones = ',Sedona_ne.shape[0],' columnas = ',Sedona_ne.shape[1]


# In[30]:


#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes=[v for v in Sedona_ne.columns if v not in NOrelevantes]

Sedona_ne[relevantes].describe(include='all')


# #### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

# * Tenemos dos únicos vendors, donde predomina **ALU**.
# * Esta tabla contiene más sites id que la anterior.

# #### Se proponen catálogos derivados de la fuente Sedona_ne con los siguientes campos:
#     
# * **site_id**: Código de sitio.
# 
# Estos catálogos nos ayudarán a mapear todos los diferentes proyectos que existen en los cuales hay un activo.

# ---
# ### 2.3 Descripción de las fuentes.
# En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.

# In[31]:


campos=Sedona_Nokia.columns
print 'Columnas de la fuente Sedona_Nokia son: ',list(campos)
pd.DataFrame(Sedona_Nokia.dtypes,columns=['Tipo de objeto Sedona_Nokia'])


# In[32]:


print 'renglones = ',Sedona_Nokia.shape[0],' columnas = ',Sedona_Nokia.shape[1]


# In[33]:


#Pasamos las columnas que queremos ver en nuestro describe:
NOrelevantes=['filedate', 'filename', 'hash_id', 'sourceid',
              'registry_state', 'datasetname', 'timestamp',
              'transaction_status', 'year', 'month', 'day']
relevantes=[v for v in Sedona_Nokia.columns if v not in NOrelevantes]

Sedona_Nokia[relevantes].describe(include='all')


# #### Haremos anotaciones sobre lo que se puede observar de la tabla describe:

# * Existe un único *vendor* que es **ALU**.
# * Se encuentran muchos registros en blanco.
# * También tiene sites id, será revisado este campo junto a los catálogos de las tablas anteriores. 

# #### Se proponen catálogos derivados de la fuente Sedona_Nokia con los siguientes campos:
#     
# * **site_id**: Código de sitio.
# 
# Estos catálogos nos ayudarán a mapear todos los diferentes proyectos que existen en los cuales hay un activo.

# ---
# ### 3.1 Exploración de los datos.
# De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los catálogos.

# #### Para empezar, se hará una limpieza general a los datos:

# In[34]:


Sedona_hwi.replace('null',np.NaN,inplace=True)
Sedona_hwi.replace(r'^\s*$',np.NaN,regex=True,inplace=True)


# ### Primer catálogo: *inventory_type*

# Empezaremos con el catálogo de inventory_type. Nuestra intención por el momento es simplemente explorar los datos.

# In[35]:


pd.DataFrame(Sedona_hwi.inventory_type.value_counts())


# In[36]:


#Revisamos frecuencias:
inventory_type=pd.DataFrame(Sedona_hwi.inventory_type.value_counts())

#Visualización:
fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Subplot1: Bar chart
inventory_type.plot(kind='bar',figsize=(10,6),colormap='rainbow_r',ax=ax0)
ax0.set_xlabel(u'inventory_type')
ax0.set_ylabel('Frecuencia')
ax0.set_title(u'Distribuciones de los tipos de elemento en inventario')

#Subplot2: Pie chart
#La lista explode debe ser ajustada manualmente contra el número de elementos del catálogo
explode_list=[.2,0,0,0,0.1] #Cada entrada corresponde a un registro del catálogo

color_list=['royalblue','lightcoral','springgreen','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','silver','mediumaquamarine',
            'mediumblue','mediumorchid','turquoise','powderblue','oldlace','palegoldenrod',
            'peachpuff','rebeccapurple','tomato','slateblue','powderblue']

inventory_type['inventory_type'].plot(kind='pie',         
                    figsize=(15,8),
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True,
                    labels=None,
                    pctdistance=1.14,
                    colors=color_list,
                               ax=ax1,
                    explode=explode_list)
ax1.set_title(u'Distribuciones de los tipos de elemento en inventario',y=1.12)
ax1.axis('equal')
ax1.legend(labels=inventory_type.index,loc='upper left')

plt.show()


# Parece un campo limpio, sin embargo no sabemos qué tipo de Router son los que sólo vienen con esta categoría.
# Se encontrará el catálogo en el apartado **Catálogos**.

# ### Segundo catálogo *site_id*

# In[37]:


Sedona_hwi.site_id.value_counts().count()


# In[38]:


pd.DataFrame(Sedona_hwi.site_id.value_counts()).head(20)


# #### Para este catálogo se hará un cruce los los catálogos del mismo campo en las demás tablas, se buscará obtener un catálogo completo.
# Pueden observarse registros con formato irregular, sin embargo por la frequencia de los mismos, no se tomarán como sucios.

# #### Visualización de los datos de trazabilidad: 

# In[39]:


pd.DataFrame(Sedona_hwi.serial_number.value_counts()[:15])


# In[40]:


pd.DataFrame(Sedona_hwi.serie_cleaned.value_counts()).plot(kind='barh',
                                                           figsize=(8,5),
                                                           title='Estado del campo serie',
                                                          colormap='coolwarm')


# #### Es de interés haber observado los datos que se usaran para la trazabilidad.
# Se nota que el campo serie mantiene un formato estándar y según los datos que nos muestra el plot, también son datos saludables.

# ---
# ### 3.2 Exploración de los datos.

# #### Para empezar, se hará una limpieza general a los datos:

# In[41]:


Sedona_ne.replace('null',np.NaN,inplace=True)
Sedona_ne.replace(r'^\s*$', np.NaN,regex=True,inplace=True)


# ### Catálogo: *site_id*

# Para este campo, se buscará ver si hay relación con los registros únicos encontrados en el catálogo de la tabla anterior y los de la tabla Sedona NE.

# In[42]:


Sedona_ne.site_id.value_counts().count()


# In[43]:


Cat_site_id=list(Sedona_ne.site_id.unique())
Cat_site_id[:15]


# No son el mismo tipo de registros. Se tratarán como catálogos distintos.
# Se llamará al catálogo limpio en el apartado de catálogos.

# #### Visualización de los datos de trazabilidad: 

# In[44]:


pd.DataFrame(Sedona_ne.serial_number.value_counts()[:15])


# In[45]:


pd.DataFrame(Sedona_ne.serie_cleaned.value_counts()).plot(kind='barh',
                                                          figsize=(8,5),
                                                          title='Estado del campo serie',
                                                          colormap='Spectral')


# #### Es de interés haber observado los datos que se usaran para la trazabilidad, parece que el campo serie se encuentra con buena salud. 

# ---
# ### 3.3 Exploración de los datos.
# De acuerdo al análisis anterior, procedemos a hacer una exploración de los datos con gráficas, de manera particular nos enfocaremos en los catálogos.

# #### Para empezar, se hará una limpieza general a los datos:

# In[46]:


Sedona_Nokia.replace('null',np.NaN,inplace=True)
Sedona_Nokia.replace(r'^\s*$', np.NaN,regex=True,inplace=True)


# ### Catálogo: *site_id*

# Se buscará saber con qué tabla tiene relación este campo. Una vez encontrada, se cruzará para generar un catálogo completo.

# In[47]:


Sedona_Nokia.site_id.value_counts()[:15]


# Podemos ver que es el mismo campo que en la tabla **Sedona_hwi**.

# In[48]:


Cat_sitios=set(list(Sedona_hwi.site_id.unique())+list(Sedona_Nokia.site_id.unique()))
Cat_sitios=list(Cat_sitios)
Cat_sitios[:15]


# Tenemos el catálogo completo.

# #### Visualización de los datos de trazabilidad: 

# In[49]:


pd.DataFrame(Sedona_Nokia.serial_number.value_counts()[:15])


# In[50]:


pd.DataFrame(Sedona_Nokia.serie_cleaned.value_counts()).plot(kind='barh',
                                                          figsize=(8,5),
                                                          title='Estado del campo serie',
                                                          colormap='Accent')


# #### Es de interés haber observado los datos que se usaran para la trazabilidad, se encontró un campo saludable.
# Se pasarán algunas reglas de limpieza.

# ---
# ### 4.1 Calidad de los datos
# Se documentará la calidad de los datos y analizarán las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

# ### Missings Values
# Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

# Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.

# In[51]:


Sedona_hwi.shape


# In[52]:


nas=Sedona_hwi.isna().sum()
porcentaje_nas=nas/Sedona_hwi.isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_8))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])


# #### Visualización de datos NOT NULL: 

# In[53]:


notmiss=(1-porcentaje_nas)*100

columnas=list(notmiss.keys())
counts_nas=list(notmiss.values)

#Mismo aplica aquí para color
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20c_8))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])


# Los missings se centran en los campos de longitud, latitud y site_id.

# ---
# ### 4.2 Calidad de los datos
# Se documentará la calidad de los datos y analizarán las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

# ### Missings Values
# Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

# Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.

# In[54]:


Sedona_ne.shape


# In[55]:


nas=Sedona_ne.isna().sum()
porcentaje_nas=nas/Sedona_ne.isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category10_6))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])


# #### Visualización de datos NOT NULL: 

# In[56]:


notmiss=(1-porcentaje_nas)*100

columnas=list(notmiss.keys())
counts_nas=list(notmiss.values)

#Mismo aplica aquí para color
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category10_6))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])


# Esta tabla se encuentra en perfecto estado.

# ---

# ### 4.3 Calidad de los datos
# Se documentará la calidad de los datos y analizarán las variables que necesitan tratamiento con la ayuda de visualizaciones y tablas.

# ### Missings Values
# Los missings values son los valores faltantes en el conjunto de datos que se refieren a aquellos campos que están vacíos o no tienen valores asignados, estos generalmente ocurren debido a errores de entrada de datos, fallas que ocurren con los procesos de recopilación de datos y, a menudo, al unir varias columnas de diferentes tablas encontramos una condición que conduce a valores faltantes. Existen numerosas formas de tratar los valores perdidos, los más fáciles son reemplazar el valor perdido con la media, la mediana, la moda o un valor constante (llegamos a un valor basado en el conocimiento del dominio) y otra alternativa es eliminar la entrada desde el conjunto de datos en sí.

# Calculamos el porcentaje de NA's que tiene la fuente por columna y el porcentaje de los missings.

# In[57]:


Sedona_Nokia.shape


# In[58]:


nas=Sedona_Nokia.isna().sum()
porcentaje_nas=nas/Sedona_Nokia.isna().count()

columnas=list(porcentaje_nas.keys())
counts_nas=list(porcentaje_nas.values)

#Para el siguiente comando, en el parámetro "color":
#Dependiendo el número de columnas se escoge un pallete, este debe ser cargado en la sección de librerías,
#Sólo se añade a la parte from bokeh.palettes import Category20c_20  colocando una ","
#http://docs.bokeh.org/en/1.3.2/docs/reference/palettes.html
#Se recomienda no poner más de 20 columnas. 
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20_9))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,1), title='Porcentaje de nas por columna')
p.vbar(x='columnas',top='counts_nas',width=.7, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
pd.DataFrame(porcentaje_nas*100,columns=['Porcentaje de NAs'])


# #### Visualización de datos NOT NULL: 

# In[59]:


notmiss=(1-porcentaje_nas)*100

columnas=list(notmiss.keys())
counts_nas=list(notmiss.values)

#Mismo aplica aquí para color
source=ColumnDataSource(dict(columnas=columnas, counts_nas=counts_nas, color=Category20_9))

p=figure(x_range=columnas, plot_height=300, plot_width=850, y_range=(0,100), 
         title='Porcentaje de not-nulls por columna')
p.vbar(x='columnas',top='counts_nas',width=.5, color='color', legend='columnas', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

pd.DataFrame(notmiss,columns=['Porcentaje de Not nulls'])


# En esta tabla los missings matienen una distribución parecida a la de la tabla **Sedona_hwi**.

# Según lo observado en los campos *serial_number* se hará una limpieza para estos campos:

# In[60]:


Sedona_Nokia.serial_number.fillna(np.NaN,inplace=True)


# ---
# ### 5 Catálogos.

# #### Catálogo *inventory_type*:

# In[61]:


Cat_inventory_type=pd.DataFrame(Sedona_hwi.inventory_type.unique())
Cat_inventory_type.columns=['inventory_type']
Cat_inventory_type.sort_values(by='inventory_type').head(10)


# #### Catálogo *Site_code*:

# In[62]:


Cat_site_codes=pd.DataFrame(Cat_sitios)
Cat_site_codes.columns=['Site_codes']
Cat_site_codes.replace(u'nan',np.NaN,regex=True,inplace=True)
Cat_site_codes.replace(u'N/A',np.NaN,regex=True,inplace=True)
Cat_site_codes.replace(u'ST/','',regex=True,inplace=True)
Cat_site_codes.dropna(inplace=True)
Cat_site_codes.reset_index(inplace=True,drop=True)
Cat_site_codes.head()


# #### Catálogo *Sites*: 

# In[63]:


Cat_sitios=pd.DataFrame(Sedona_ne.site_id.unique(),columns=['Sitios'])
Cat_sitios.head()


# ---
# ### 6. Preparación de los datos.
# Para la preparación de los datos crearemos las reglas de calidad o estándares observados en el apartado anterior de acuerdo a la calidad de datos obtenidos: 

# * **Reglas generales**:
#     * Eliminar registros en blanco.
#     * Eliminar registros 'nan'.
#     * Eliminar iniciales 'ST/' para site_codes.
#     * Eliminar registros None.

# ---
# ### 7.1 Métricas KPI.
# Se mostrarán los KPIs generados. 

# In[64]:


Sedona_hwi.replace(np.NaN,'vacio',inplace=True)


# #### Total de elementos

# In[65]:


Total_Elementos_hwi=Sedona_hwi.shape[0]
Total_Elementos_hwi


# #### Total Elementos Trazables

# In[66]:


Total_Tr_hwi=Sedona_hwi.loc[(Sedona_hwi.serie_cleaned==0) & (Sedona_hwi.serial_number!='vacio')].shape[0]
Total_Tr_hwi


# #### Total Elementos NO Trazables

# In[67]:


Total_NOTr_hwi=Total_Elementos_hwi-Total_Tr_hwi
Total_NOTr_hwi


# #### Total Elementos Trazables Únicos

# In[68]:


Total_Tr_Unic_hwi=Sedona_hwi['serial_number'].loc[(Sedona_hwi.serie_cleaned==0) &
                                              (Sedona_hwi.serial_number!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_hwi


# #### Total de elementos trazables duplicados

# In[69]:


Total_Tr_Dupli_hwi=Total_Tr_hwi-Total_Tr_Unic_hwi
Total_Tr_Dupli_hwi


# In[70]:


print '        KPIs Sedona_hwi'
KPIs=pd.DataFrame({'KPIs Sedona_hwi':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos_hwi,Total_Tr_hwi,Total_NOTr_hwi,
                              Total_Tr_Unic_hwi,Total_Tr_Dupli_hwi]})

KPIs


# In[71]:


#df_hive_kpi = spark.createDataFrame(KPIs)


# In[72]:


#df_hive_kpi.write.mode("overwrite").saveAsTable("default.kpi_odk_38") #hdfs://attdatalakehdfs/user/hive/warehouse/eda_odk_99


# ---
# ### 7.2 Métricas KPI.
# Se mostrarán los KPIs generados. 

# In[73]:


Sedona_ne.replace(np.NaN,'vacio',inplace=True)


# #### Total de elementos

# In[74]:


Total_Elementos_ne=Sedona_ne.shape[0]
Total_Elementos_ne


# #### Total Elementos Trazables

# In[75]:


Total_Tr_ne=Sedona_ne.loc[(Sedona_ne.serie_cleaned==0) & (Sedona_ne.serial_number!='vacio')].shape[0]
Total_Tr_ne


# #### Total Elementos NO Trazables

# In[76]:


Total_NOTr_ne=Total_Elementos_ne-Total_Tr_ne
Total_NOTr_ne


# #### Total Elementos Trazables Únicos

# In[77]:


Total_Tr_Unic_ne=Sedona_ne['serial_number'].loc[(Sedona_ne.serie_cleaned==0) &
                                                (Sedona_ne.serial_number!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_ne


# #### Total de elementos trazables duplicados

# In[78]:


Total_Tr_Dupli_ne=Total_Tr_ne-Total_Tr_Unic_ne
Total_Tr_Dupli_ne


# In[79]:


print '          KPIs Sedona_ne'

KPIs=pd.DataFrame({'KPIs Sedona_ne':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos_ne,Total_Tr_ne,Total_NOTr_ne,
                              Total_Tr_Unic_ne,Total_Tr_Dupli_ne]})

KPIs


# In[80]:


#df_hive_kpi = spark.createDataFrame(KPIs)


# In[81]:


#df_hive_kpi.write.mode("overwrite").saveAsTable("default.kpi_odk_38") #hdfs://attdatalakehdfs/user/hive/warehouse/eda_odk_99


# ---
# ### 7.3 Métricas KPI.
# Se mostrarán los KPIs generados. 

# In[82]:


Sedona_Nokia.replace(np.NaN,'vacio',inplace=True)


# #### Total de elementos

# In[83]:


Total_Elementos_nk=Sedona_Nokia.shape[0]
Total_Elementos_nk


# #### Total Elementos Trazables

# In[84]:


Total_Tr_nk=Sedona_Nokia.loc[(Sedona_Nokia.serie_cleaned==0) & (Sedona_Nokia.serial_number!='vacio')].shape[0]
Total_Tr_nk


# #### Total Elementos NO Trazables

# In[85]:


Total_NOTr_nk=Total_Elementos_nk-Total_Tr_nk
Total_NOTr_nk


# #### Total Elementos Trazables Únicos

# In[86]:


Total_Tr_Unic_nk=Sedona_Nokia['serial_number'].loc[(Sedona_Nokia.serie_cleaned==0) &
                                                   (Sedona_Nokia.serial_number!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_nk


# #### Total de elementos trazables duplicados

# In[87]:


Total_Tr_Dupli_nk=Total_Tr_nk-Total_Tr_Unic_nk
Total_Tr_Dupli_nk


# In[88]:


print '         KPIs Sedona_Nokia'

KPIs=pd.DataFrame({'KPIs Sedona_Nokia':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos_nk,Total_Tr_nk,Total_NOTr_nk,
                              Total_Tr_Unic_nk,Total_Tr_Dupli_nk]})

KPIs


# #### Se suben las tablas a Hive:

# In[89]:


#df_hive_kpi = spark.createDataFrame(KPIs)


# In[90]:


#df_hive_kpi.write.mode("overwrite").saveAsTable("default.kpi_odk_38") #hdfs://attdatalakehdfs/user/hive/warehouse/eda_odk_99


# In[91]:


sc.stop()


# In[ ]:




