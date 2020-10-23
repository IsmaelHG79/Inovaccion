
![Encabezado](image/encabezado.png)

# Exploratory Data Analysis

## ODK 32 - Instalación y Comisionamiento

## Descripción

Analizaremos los datos de la fuente **ODK 32** que corresponde a los elementos que se encuentran en Instalacion y Comisionamiento en AT&T con un tratamiento estadístico descriptivo para la exploración, explotación y descubrimiento de los datos para un correcto tracking del ciclo de vida de los elementos de red. 

Primero cargamos las librerías necesarias.

#### Conectando al Datalake


```python
import os
os.environ['JAVA_HOME'] = '/usr/java/jdk1.8.0_162'
os.environ['SPARK_HOME'] = '/opt/cloudera/parcels/CDH-6.2.0-1.cdh6.2.0.p0.967373/lib/spark'
import findspark
findspark.init()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import HiveContext
```


```python
conf = SparkConf().setAppName('EDA_ODK_32')  \
    .setMaster('yarn').set("spark.yarn.queue","root.eda")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
sqlContext = HiveContext(sc)
```


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import re
import pandasql


import nltk
from nltk.probability import FreqDist
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#from pyspark.sql.functions import udf ,col
#from pyspark.sql.types import IntegerType,StringType

%matplotlib inline

from bokeh.io import show, output_notebook, output_file 
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20_11, Category20c_20, Category10_5,Category10_6, Category20_20, Plasma256
output_notebook()
```

### 1. Recolección de los datos: 

Se crea el dataframe de spark con el universo de datos crudos.  

Los datos se van a recolectar de la tabla ```default.tx_stg_06_tabular_odk_32``` obtenida previamente en el notebook *Adquisicion_Datos_ODK_32*.


```python
df_load = spark.sql("SELECT * FROM tx_stg_06_tabular_odk_32").cache().toPandas()
```

Para las fuentes de los ODK's nos interesa conocer todos los elementos en sitio, por lo que haremos una limpieza en los campos que contengan características de los mismos.
Creamos una funcion para el tratamiento del campo de sitio en spark el cual contiene ciertas reglas definidas para su limpieza.

Hemos recolectado los campos a analizar de la fuente **ODK 32**.

### Una muestra del ODK 32:


```python
df=df_load.copy()
#Sólamente se usa lo siguiente en caso de querer filtrar el universo limpio en el campo TipoElemento_key
#df=df.loc[df.exist==True] 
df.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_form</th>
      <th>clave_form</th>
      <th>element_group</th>
      <th>element</th>
      <th>exist</th>
      <th>TipoElemento_key</th>
      <th>TipoElemento_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>100079</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022HEM4MG6000531</td>
    </tr>
    <tr>
      <th>1</th>
      <td>101025</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupBbus-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102310WYGN0G7014852</td>
    </tr>
    <tr>
      <th>2</th>
      <td>101350</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022HEM9WGA110408</td>
    </tr>
    <tr>
      <th>3</th>
      <td>101491</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-4</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>21023198974MD9029272</td>
    </tr>
    <tr>
      <th>4</th>
      <td>102228</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-3</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022HEM4MF8018167</td>
    </tr>
    <tr>
      <th>5</th>
      <td>102565</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022HEM6TFB603528</td>
    </tr>
    <tr>
      <th>6</th>
      <td>105936</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-2</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022HEM4MG4013730</td>
    </tr>
    <tr>
      <th>7</th>
      <td>106335</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-0</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102311CHKN0G2014076</td>
    </tr>
    <tr>
      <th>8</th>
      <td>107818</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022HEM10H8009411</td>
    </tr>
    <tr>
      <th>9</th>
      <td>107833</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022HEM4MG6002133</td>
    </tr>
  </tbody>
</table>
</div>



### 2. Descripción de las fuentes.
En este apartado se hará una descripción a detalle de las fuentes para una mejor comprensión de los datos. Por cada fuente se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
print 'renglones = ',df.shape[0],' columnas = ',df.shape[1]
```

    renglones =  421495  columnas =  7


#### Una breve descripción de los campos:
* **id_form**: Número de formulario en *Panda*.
* **clave_form**: Clave de identificación del ODK.
* **element_group**: Element group.
* **element**: Hijo del element group.
* **exist**: Campo diseñado durante la extracción de los datos para identificar que el campo buscado se encuentra existente.
* **TipoElemento_key**: Nombre del campo.
* **TipoElemento_value**: Atributo del campo.

Con la transformación que se llevo a cabo previamente, los campos id_form, clave_form, element_group, element, exist sirven para tener un control y mejor manejo del odk. Los campos TipoElemento_key y TipoElemento_value son los que se utilizarán para sacar indicadores.

### 3. Exploración de los datos.
De acuerdo al análisis anterior, procederemos a observar algunos detalles de la fuente:


```python
print 'Los atributos priority que encontramos en este ODK en los distintos element groups son:'
Freq_Atributos=pd.DataFrame(df.TipoElemento_key.value_counts())
Freq_Atributos
```

    Los atributos priority que encontramos en este ODK en los distintos element groups son:





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_key</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Modelo Tarjeta</th>
      <td>73238</td>
    </tr>
    <tr>
      <th>Numero de Serie (Escanner)</th>
      <td>68001</td>
    </tr>
    <tr>
      <th>Número de Serie (Manual)</th>
      <td>51938</td>
    </tr>
    <tr>
      <th>Modelo Antenna RF</th>
      <td>37916</td>
    </tr>
    <tr>
      <th>Etiqueta RCU RET</th>
      <td>37910</td>
    </tr>
    <tr>
      <th>Etiqueta RCU RET 2 (Si aplica)</th>
      <td>25757</td>
    </tr>
    <tr>
      <th>RRU 01</th>
      <td>21512</td>
    </tr>
    <tr>
      <th>RRU 02</th>
      <td>21110</td>
    </tr>
    <tr>
      <th>RRU 03</th>
      <td>17578</td>
    </tr>
    <tr>
      <th>Marca y Modelo Antena RF</th>
      <td>15034</td>
    </tr>
    <tr>
      <th>Tipo de Gabinete</th>
      <td>7610</td>
    </tr>
    <tr>
      <th>Modelo de Gabinete</th>
      <td>7610</td>
    </tr>
    <tr>
      <th>TS Finalización</th>
      <td>7218</td>
    </tr>
    <tr>
      <th>Tipo de Instalación</th>
      <td>7209</td>
    </tr>
    <tr>
      <th>Serie BBU (M)</th>
      <td>5026</td>
    </tr>
    <tr>
      <th>Número de activo fijo (manual)</th>
      <td>4176</td>
    </tr>
    <tr>
      <th>Número de serie (manual)</th>
      <td>4079</td>
    </tr>
    <tr>
      <th>Código de Sitio</th>
      <td>3900</td>
    </tr>
    <tr>
      <th>SHELTER 01</th>
      <td>2150</td>
    </tr>
    <tr>
      <th>RACK 01</th>
      <td>2058</td>
    </tr>
    <tr>
      <th>RACK 02</th>
      <td>45</td>
    </tr>
    <tr>
      <th>SHELTER 02</th>
      <td>21</td>
    </tr>
  </tbody>
</table>
</div>




```python
Freq_Atributos.plot(kind='bar',figsize=(10,6),rot=90,colormap='summer')

plt.title('Histograma de los atributos del ODK')
plt.ylabel('Frequencia del atributo')
plt.xlabel('Atributos')
```




    Text(0.5,0,'Atributos')




![Grafica_01](image/output_19_1.png)


#### Se hará una limpieza para homologar los campos de serie y activo:


```python
stoppers=[u'numero de',u'escaner',u'manual', u'bbu m', u'escanner', u'fijo']
df['TipoElemento_Key_Clean']=df.TipoElemento_key

df.TipoElemento_Key_Clean=df.TipoElemento_Key_Clean.str.lower()
df.TipoElemento_Key_Clean=df.TipoElemento_Key_Clean.str.replace("\)",'')
df.TipoElemento_Key_Clean=df.TipoElemento_Key_Clean.str.replace("\(",'')
df.TipoElemento_Key_Clean.replace(u'á',u'a',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'é',u'e',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'í',u'i',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'ó',u'o',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'ú',u'u',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'0',u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'1',u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'2',u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'3',u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'4',u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'5',u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'6',u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'7',u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'8',u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'9',u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(stoppers,u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean=df.TipoElemento_Key_Clean.str.strip()
```

#### Después de haber pasado una limpieza, podemos tener homologados los campos:


```python
#Se debe observar que serie y activo han quedado homologados
pd.DataFrame(df.TipoElemento_Key_Clean.value_counts())
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_Key_Clean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>serie</th>
      <td>129044</td>
    </tr>
    <tr>
      <th>modelo tarjeta</th>
      <td>73238</td>
    </tr>
    <tr>
      <th>rru</th>
      <td>60200</td>
    </tr>
    <tr>
      <th>modelo antenna rf</th>
      <td>37916</td>
    </tr>
    <tr>
      <th>etiqueta rcu ret</th>
      <td>37910</td>
    </tr>
    <tr>
      <th>etiqueta rcu ret  si aplica</th>
      <td>25757</td>
    </tr>
    <tr>
      <th>marca y modelo antena rf</th>
      <td>15034</td>
    </tr>
    <tr>
      <th>modelo de gabinete</th>
      <td>7610</td>
    </tr>
    <tr>
      <th>tipo de gabinete</th>
      <td>7610</td>
    </tr>
    <tr>
      <th>ts finalizacion</th>
      <td>7218</td>
    </tr>
    <tr>
      <th>tipo de instalacion</th>
      <td>7209</td>
    </tr>
    <tr>
      <th>activo</th>
      <td>4176</td>
    </tr>
    <tr>
      <th>codigo de sitio</th>
      <td>3900</td>
    </tr>
    <tr>
      <th>shelter</th>
      <td>2171</td>
    </tr>
    <tr>
      <th>rack</th>
      <td>2103</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.DataFrame(df.TipoElemento_Key_Clean.loc[df.TipoElemento_Key_Clean=='serie'].describe())
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_Key_Clean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>129044</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>1</td>
    </tr>
    <tr>
      <th>top</th>
      <td>serie</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>129044</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.DataFrame(df.TipoElemento_Key_Clean.loc[df.TipoElemento_Key_Clean=='activo'].describe())
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_Key_Clean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>4176</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>1</td>
    </tr>
    <tr>
      <th>top</th>
      <td>activo</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>4176</td>
    </tr>
  </tbody>
</table>
</div>



#### Campo *Modelo Tarjeta*


```python
Cat_ModeloTarjeta=pd.DataFrame(df.TipoElemento_value.loc[df.TipoElemento_Key_Clean=='modelo tarjeta']).drop_duplicates().reset_index(drop=True)
Cat_ModeloTarjeta
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>UBBPd6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WD22UMPTb1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>WD2MUPEUC</td>
    </tr>
    <tr>
      <th>3</th>
      <td>OTH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>FANd</td>
    </tr>
    <tr>
      <th>5</th>
      <td>QWL1WBBPD2</td>
    </tr>
    <tr>
      <th>6</th>
      <td>QWL3WBBPF3</td>
    </tr>
    <tr>
      <th>7</th>
      <td>GTMUb</td>
    </tr>
    <tr>
      <th>8</th>
      <td>WD2E1FANC</td>
    </tr>
    <tr>
      <th>9</th>
      <td>QWL1WBBPB2</td>
    </tr>
    <tr>
      <th>10</th>
      <td>QWL2WBBPB3</td>
    </tr>
    <tr>
      <th>11</th>
      <td>WD2E1FAN</td>
    </tr>
    <tr>
      <th>12</th>
      <td>WD22LBBPD3</td>
    </tr>
    <tr>
      <th>13</th>
      <td>UBBPd2</td>
    </tr>
    <tr>
      <th>14</th>
      <td>GTMU1</td>
    </tr>
    <tr>
      <th>15</th>
      <td>WD23LBBPD1</td>
    </tr>
    <tr>
      <th>16</th>
      <td>QWL1WBBPD1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>QWL2WBBPB2</td>
    </tr>
    <tr>
      <th>18</th>
      <td>QWL1WBBPF4</td>
    </tr>
    <tr>
      <th>19</th>
      <td>WD2M1UEIU</td>
    </tr>
    <tr>
      <th>20</th>
      <td>WD2MUPEUA</td>
    </tr>
    <tr>
      <th>21</th>
      <td>WD22UMPTa2</td>
    </tr>
    <tr>
      <th>22</th>
      <td>WD22WMPT</td>
    </tr>
    <tr>
      <th>23</th>
      <td>LBBPD2</td>
    </tr>
    <tr>
      <th>24</th>
      <td>WD22LBBPD1</td>
    </tr>
  </tbody>
</table>
</div>



Podemos encontrar un campo no homologado. Se hará un esfuerzo para limpiar el campo y crear un catálogo.


```python
dirt=['no visible','n/v','nv','ilegible','n/a','na','no legible',
      'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene','No visble','no visble',
      'No viaible']

Cat_ModeloTarjeta.TipoElemento_value=Cat_ModeloTarjeta.TipoElemento_value.str.upper()
#Cat_ModeloTarjeta.TipoElemento_value=Cat_ModeloTarjeta.TipoElemento_value.str.replace('.',inplace=True)
Cat_ModeloTarjeta.replace(u'inc.','',regex=True,inplace=True)
Cat_ModeloTarjeta.replace(u'inc.','',regex=True,inplace=True)
Cat_ModeloTarjeta.replace(dirt,'',regex=True,inplace=True)
Cat_ModeloTarjeta.dropna(inplace=True)
Cat_ModeloTarjeta.rename(columns={'TipoElemento_value': 'Atributos'}, inplace=True)
```

#### Campo *Modelo Antena RF*


```python
Cat_ModeloAntenaRF=pd.DataFrame(df.TipoElemento_value.loc[df.TipoElemento_Key_Clean=='modelo antenna rf']).drop_duplicates().reset_index(drop=True)
Cat_ModeloAntenaRF
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HBXX-6516DS-A2M</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ODV-065R17E18K-G</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ADU4518R1V01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>80010765V01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ADU4518R0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ODV2-065R18K-G-V1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>ODI2-065R18K-GQ</td>
    </tr>
    <tr>
      <th>7</th>
      <td>OTH</td>
    </tr>
    <tr>
      <th>8</th>
      <td>DBXLH-6565EC-A2M</td>
    </tr>
    <tr>
      <th>9</th>
      <td>80010622V01</td>
    </tr>
    <tr>
      <th>10</th>
      <td>5NPX1006F</td>
    </tr>
    <tr>
      <th>11</th>
      <td>OPA65R-W4</td>
    </tr>
    <tr>
      <th>12</th>
      <td>ADU4518R0V01</td>
    </tr>
    <tr>
      <th>13</th>
      <td>DBXLH-6565B-A2M</td>
    </tr>
    <tr>
      <th>14</th>
      <td>742-266V02</td>
    </tr>
    <tr>
      <th>15</th>
      <td>742-236V01</td>
    </tr>
    <tr>
      <th>16</th>
      <td>ADU4518R1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>80010510V01</td>
    </tr>
    <tr>
      <th>18</th>
      <td>AQU4518R21</td>
    </tr>
    <tr>
      <th>19</th>
      <td>ODI-065R17E18K-GQ</td>
    </tr>
    <tr>
      <th>20</th>
      <td>ADU4518R1V06</td>
    </tr>
    <tr>
      <th>21</th>
      <td>ADU4518R0V06</td>
    </tr>
    <tr>
      <th>22</th>
      <td>80010766V01</td>
    </tr>
    <tr>
      <th>23</th>
      <td>DBXLH-6565EC-VTM</td>
    </tr>
    <tr>
      <th>24</th>
      <td>CMAX-DM60-CPUSEI</td>
    </tr>
    <tr>
      <th>25</th>
      <td>DXX-1710-2170/1710-2170-65/65-18I/18I-M/M</td>
    </tr>
    <tr>
      <th>26</th>
      <td>DXX-790-960/1710-2180/1710-2180-65/65/65-17.5I...</td>
    </tr>
    <tr>
      <th>27</th>
      <td>742266V02</td>
    </tr>
    <tr>
      <th>28</th>
      <td>ODI3-065R18K-GQ</td>
    </tr>
    <tr>
      <th>29</th>
      <td>AAU3940</td>
    </tr>
    <tr>
      <th>30</th>
      <td>HBXX-3817TB1-VTM</td>
    </tr>
    <tr>
      <th>31</th>
      <td>ODV2-065R18K</td>
    </tr>
    <tr>
      <th>32</th>
      <td>DBXLH-6565B-VTM</td>
    </tr>
    <tr>
      <th>33</th>
      <td>80010727</td>
    </tr>
    <tr>
      <th>34</th>
      <td>5NPX1006F-1</td>
    </tr>
    <tr>
      <th>35</th>
      <td>742236V01</td>
    </tr>
    <tr>
      <th>36</th>
      <td>HBX-6516DS-A1M</td>
    </tr>
    <tr>
      <th>37</th>
      <td>HBX-3319DS-VTM</td>
    </tr>
    <tr>
      <th>38</th>
      <td>HBX-6516DS-VTM</td>
    </tr>
    <tr>
      <th>39</th>
      <td>HBX-3319DS-A1M</td>
    </tr>
    <tr>
      <th>40</th>
      <td>HBXX-6513DS-VTM</td>
    </tr>
    <tr>
      <th>41</th>
      <td>HBXX-6516DS-VTM</td>
    </tr>
    <tr>
      <th>42</th>
      <td>ODV3-065R18K-G</td>
    </tr>
    <tr>
      <th>43</th>
      <td>DXX-824-960/1710-2170-65/65-17.5I/18I-M/M</td>
    </tr>
    <tr>
      <th>44</th>
      <td>AMB4520R6V06</td>
    </tr>
    <tr>
      <th>45</th>
      <td>DXX-824-960/1710-2170/1710-2170-65/65/65-17.5I...</td>
    </tr>
    <tr>
      <th>46</th>
      <td>RVV-33B-R3</td>
    </tr>
    <tr>
      <th>47</th>
      <td>DXX-824-960/1710-2170-65/65-15I/18I-M/M</td>
    </tr>
    <tr>
      <th>48</th>
      <td>ODV-065R15B17K17K</td>
    </tr>
    <tr>
      <th>49</th>
      <td>ODV3-065R18K-G-V1</td>
    </tr>
  </tbody>
</table>
</div>



Podemos encontrar un campo no homologado. Se hará un esfuerzo para limpiar el campo y crear un catálogo.


```python
dirt=['no visible','n/v','nv','ilegible','n/a','na','no legible',
      'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene','No visble','no visble',
      'No viaible']

Cat_ModeloAntenaRF.TipoElemento_value=Cat_ModeloAntenaRF.TipoElemento_value.str.upper()
Cat_ModeloAntenaRF.replace(u'inc.','',regex=True,inplace=True)
Cat_ModeloAntenaRF.replace(u'inc.','',regex=True,inplace=True)
Cat_ModeloAntenaRF.replace(dirt,'',regex=True,inplace=True)
Cat_ModeloAntenaRF.dropna(inplace=True)
Cat_ModeloAntenaRF.rename(columns={'TipoElemento_value': 'Atributos'}, inplace=True)
```

#### Hacemos más limpieza para poder eliminar basura.
Esta limpieza se sigue tomando del catálogo que se encuentra en Hive *regex_cat_cleanup* y adicional, se aregan a la lista campos que salieron de acuerdo al análisis.


```python
dirt=['no visible','n/v','nv','ilegible','n/a', 's/a', 'na','no legible',
      'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene','no visble','no visble',
      'no viaible', '.fhy', 'bxfj', 'cambiar la foto', 'hdjdjjdjfjfj', 'hdjrnnfjfjf', 'hffhthjih', 'hhyhigch',
      'hswkwjj', 'no aplica', 'no pude borrar elemnto', 'ns no visible', 'sin serie', 'sitio ibs no aplica', 'tutj',
      'uflp serie no visible', 'xxxxxxx', 'hsid# djdncg', 'sin información disponible', 'no tiene número de serie',
      'hdkoe kg udkke' 'no se ve', 'ninguna', 'no tiene etiqueta y no se alcnaza a ver.', 'fue un error',
      'no legible', 'sin etiqueta', 'no disponible', 'no tiene', 'sin datos', 'num de serie no legible', 'etiqueta no legible', 'no cuenta con número de serie',
      'no aplica por error se selecciona una tarjeta más', 'enviado ya en reporte anterior', 'hlk', 'ninguno', 'la antena no tiene etiqueta por lo tanto tampoco número de serie', 'no leguible',
      'sin targeta (por equivocacion se agrego este eslot 18 )', 'no cuenta con numeros de serie', 'enviados en reporte anterior .', 'sin etiqueta de numero de serie',
      'sin numero', 'sin informacion disponible', 'sin acceso a la antena', 'no tiene serie', 'sin acceso', 'no se pudo sacar ya que esta clausurado el sitio',
      'no se hizo por que no tenemos tarjeta se las llevo el ing de huawei gabriel lopez', 'sin informacion disponible', 'no aplica ta este segmento',
      'sin numero de serie visible', 'enviada en reporte  anterior', 'no hay antena', 'no se pudo sacar ya que esta clausurado y nos sacaron de sitio',
      'sin serie falta etiqueta', 'sin numero de serie no cuenta con la etiqueta', 'no tiene etiqueta', 'no existe', 'no serie visible', 'no hay bbu esta en resguardo por el ing gabriel lopez',
      'no legible', 'na', 'na hay  tarjeta', 'sin acceso al numero de serie', 'no visibles', 'uelp serie no visible', 'sin informacion disponible', 'sin tarjeta', 'fue un error de dedo no ay mas slot',
      'codigo no visible', 'num de serie no visible', 'sin informacion', 'no se aprecia el codigo', 'sin numero de serie', 'no trae la etiketa de numero de serie',
      'no aplica.', 'no se pudo sacar el numero  de serie ya q nos sacaron del sitio ya q esta clausurado', 'no tiene serie visible', 'no tiene serial ala vista',
      'no se tiene acceso a la antena', 'etiqueta no visible', 'no se puede tomar la foto porque tenemos la fan', 'n/a  no se instalan antenas', 'no aplica sitio ibs',
      'sin numero', 'no visible', 'kcuvicuv', 'error no hay mas', 'no se puede apreciar el codigo', 'no aplica es ibs.', 'no  cuenta con etiquetas de n/s', 'esta ultima no vale',
      'no hay tarjeta', 'esta no vale', 'falta']
```


```python
df.TipoElemento_value=df.TipoElemento_value.str.lower()
df.TipoElemento_value=df.TipoElemento_value.str.strip()
df.TipoElemento_value.replace(dirt,np.NaN,regex=True,inplace=True)
```


```python
df['Trazabilidad']='No Trazable'
```


```python
df['Trazabilidad'].loc[((df.TipoElemento_Key_Clean=='serie') | (df.TipoElemento_Key_Clean=='activo')) & (df.TipoElemento_value is not np.NaN)]='Trazable'
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/pandas/core/indexing.py:189: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self._setitem_with_indexer(indexer, value)



```python
df.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_form</th>
      <th>clave_form</th>
      <th>element_group</th>
      <th>element</th>
      <th>exist</th>
      <th>TipoElemento_key</th>
      <th>TipoElemento_value</th>
      <th>TipoElemento_Key_Clean</th>
      <th>Trazabilidad</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>100079</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mg6000531</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>1</th>
      <td>101025</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupBbus-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102310wygn0g7014852</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>2</th>
      <td>101350</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem9wga110408</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>3</th>
      <td>101491</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-4</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>21023198974md9029272</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>4</th>
      <td>102228</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-3</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mf8018167</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>5</th>
      <td>102565</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem6tfb603528</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>6</th>
      <td>105936</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-2</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mg4013730</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>7</th>
      <td>106335</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-0</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102311chkn0g2014076</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>8</th>
      <td>107818</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem10h8009411</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>9</th>
      <td>107833</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mg6002133</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
  </tbody>
</table>
</div>



### 4. Calidad de los datos.
En el parseo de nuestra fuente de ODK se creo el campo de *exist* que corresponde a la limpieza de los atributos que se encuentran en el formulario, con esto eliminando missing values.

### 5. Catálogos.
Se enlistan los catálogos que surgieron de la exploración. 

#### Catálogo Modelo de Tarjeta


```python
Cat_ModeloTarjeta
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Atributos</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>UBBPD6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WD22UMPTB1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>WD2MUPEUC</td>
    </tr>
    <tr>
      <th>3</th>
      <td>OTH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>FAND</td>
    </tr>
    <tr>
      <th>5</th>
      <td>QWL1WBBPD2</td>
    </tr>
    <tr>
      <th>6</th>
      <td>QWL3WBBPF3</td>
    </tr>
    <tr>
      <th>7</th>
      <td>GTMUB</td>
    </tr>
    <tr>
      <th>8</th>
      <td>WD2E1FANC</td>
    </tr>
    <tr>
      <th>9</th>
      <td>QWL1WBBPB2</td>
    </tr>
    <tr>
      <th>10</th>
      <td>QWL2WBBPB3</td>
    </tr>
    <tr>
      <th>11</th>
      <td>WD2E1FAN</td>
    </tr>
    <tr>
      <th>12</th>
      <td>WD22LBBPD3</td>
    </tr>
    <tr>
      <th>13</th>
      <td>UBBPD2</td>
    </tr>
    <tr>
      <th>14</th>
      <td>GTMU1</td>
    </tr>
    <tr>
      <th>15</th>
      <td>WD23LBBPD1</td>
    </tr>
    <tr>
      <th>16</th>
      <td>QWL1WBBPD1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>QWL2WBBPB2</td>
    </tr>
    <tr>
      <th>18</th>
      <td>QWL1WBBPF4</td>
    </tr>
    <tr>
      <th>19</th>
      <td>WD2M1UEIU</td>
    </tr>
    <tr>
      <th>20</th>
      <td>WD2MUPEUA</td>
    </tr>
    <tr>
      <th>21</th>
      <td>WD22UMPTA2</td>
    </tr>
    <tr>
      <th>22</th>
      <td>WD22WMPT</td>
    </tr>
    <tr>
      <th>23</th>
      <td>LBBPD2</td>
    </tr>
    <tr>
      <th>24</th>
      <td>WD22LBBPD1</td>
    </tr>
  </tbody>
</table>
</div>



#### Catálogo Modelo de Antena RF


```python
Cat_ModeloAntenaRF
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Atributos</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HBXX-6516DS-A2M</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ODV-065R17E18K-G</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ADU4518R1V01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>80010765V01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ADU4518R0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ODV2-065R18K-G-V1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>ODI2-065R18K-GQ</td>
    </tr>
    <tr>
      <th>7</th>
      <td>OTH</td>
    </tr>
    <tr>
      <th>8</th>
      <td>DBXLH-6565EC-A2M</td>
    </tr>
    <tr>
      <th>9</th>
      <td>80010622V01</td>
    </tr>
    <tr>
      <th>10</th>
      <td>5NPX1006F</td>
    </tr>
    <tr>
      <th>11</th>
      <td>OPA65R-W4</td>
    </tr>
    <tr>
      <th>12</th>
      <td>ADU4518R0V01</td>
    </tr>
    <tr>
      <th>13</th>
      <td>DBXLH-6565B-A2M</td>
    </tr>
    <tr>
      <th>14</th>
      <td>742-266V02</td>
    </tr>
    <tr>
      <th>15</th>
      <td>742-236V01</td>
    </tr>
    <tr>
      <th>16</th>
      <td>ADU4518R1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>80010510V01</td>
    </tr>
    <tr>
      <th>18</th>
      <td>AQU4518R21</td>
    </tr>
    <tr>
      <th>19</th>
      <td>ODI-065R17E18K-GQ</td>
    </tr>
    <tr>
      <th>20</th>
      <td>ADU4518R1V06</td>
    </tr>
    <tr>
      <th>21</th>
      <td>ADU4518R0V06</td>
    </tr>
    <tr>
      <th>22</th>
      <td>80010766V01</td>
    </tr>
    <tr>
      <th>23</th>
      <td>DBXLH-6565EC-VTM</td>
    </tr>
    <tr>
      <th>24</th>
      <td>CMAX-DM60-CPUSEI</td>
    </tr>
    <tr>
      <th>25</th>
      <td>DXX-1710-2170/1710-2170-65/65-18I/18I-M/M</td>
    </tr>
    <tr>
      <th>26</th>
      <td>DXX-790-960/1710-2180/1710-2180-65/65/65-17.5I...</td>
    </tr>
    <tr>
      <th>27</th>
      <td>742266V02</td>
    </tr>
    <tr>
      <th>28</th>
      <td>ODI3-065R18K-GQ</td>
    </tr>
    <tr>
      <th>29</th>
      <td>AAU3940</td>
    </tr>
    <tr>
      <th>30</th>
      <td>HBXX-3817TB1-VTM</td>
    </tr>
    <tr>
      <th>31</th>
      <td>ODV2-065R18K</td>
    </tr>
    <tr>
      <th>32</th>
      <td>DBXLH-6565B-VTM</td>
    </tr>
    <tr>
      <th>33</th>
      <td>80010727</td>
    </tr>
    <tr>
      <th>34</th>
      <td>5NPX1006F-1</td>
    </tr>
    <tr>
      <th>35</th>
      <td>742236V01</td>
    </tr>
    <tr>
      <th>36</th>
      <td>HBX-6516DS-A1M</td>
    </tr>
    <tr>
      <th>37</th>
      <td>HBX-3319DS-VTM</td>
    </tr>
    <tr>
      <th>38</th>
      <td>HBX-6516DS-VTM</td>
    </tr>
    <tr>
      <th>39</th>
      <td>HBX-3319DS-A1M</td>
    </tr>
    <tr>
      <th>40</th>
      <td>HBXX-6513DS-VTM</td>
    </tr>
    <tr>
      <th>41</th>
      <td>HBXX-6516DS-VTM</td>
    </tr>
    <tr>
      <th>42</th>
      <td>ODV3-065R18K-G</td>
    </tr>
    <tr>
      <th>43</th>
      <td>DXX-824-960/1710-2170-65/65-17.5I/18I-M/M</td>
    </tr>
    <tr>
      <th>44</th>
      <td>AMB4520R6V06</td>
    </tr>
    <tr>
      <th>45</th>
      <td>DXX-824-960/1710-2170/1710-2170-65/65/65-17.5I...</td>
    </tr>
    <tr>
      <th>46</th>
      <td>RVV-33B-R3</td>
    </tr>
    <tr>
      <th>47</th>
      <td>DXX-824-960/1710-2170-65/65-15I/18I-M/M</td>
    </tr>
    <tr>
      <th>48</th>
      <td>ODV-065R15B17K17K</td>
    </tr>
    <tr>
      <th>49</th>
      <td>ODV3-065R18K-G-V1</td>
    </tr>
  </tbody>
</table>
</div>



### 6. Preparación de los datos.
Para la preparación de los datos se propondrán en el modelo lógico para hacer sentido a la información de la fuente. 

#### Reglas utilizadas:
* Se eliminan todos los registros: ('no visible','n/v','nv','ilegible','n/a','na','no legible',
    'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene',  
    'No visble','no visble','No viaible', etc...).      
* Se pasa lower case todos los atributos (La columna **TipoElemento_value**).
* Se eliminan espacios sobrantes.
* Se eliminan los strings 'NA'.
* Se eliminan las palabras: 'numero de', 'escaner', 'manual' en la columna **TipoElemento_key**.
* Se pasa lower case todos los campos key (La columna **TipoElemento_key**).
* Se eliminan acentos y caracteres '/\'

### 7. Métricas KPI.
Se mostrarán los KPIs generados. 


```python
df.fillna('vacio',inplace=True)
```

*Aqui se hace el filtro por id_form para hacer ejercicios muestra*


```python
aux=df.copy()
```

Se documenta el query donde se hace el chequeo con la tabla *parsed_odk* del odk correspondiente:  

``SELECT COUNT(*) FROM inventario.parsed_odk_ WHERE id_form=='37605';
``

Para asegurarnos que estamos tomando los campos correctos y no duplicar información, no se tomarán en cuenta los registros que contengan dentro del campo **TipoElemento_Key**: 'modelo antena rf', 'ts finalizacion', 'modelo tarjeta' y 'tipo de instalacion'.


```python
aux = aux.loc[(aux.TipoElemento_Key_Clean=='serie') | (aux.TipoElemento_Key_Clean=='activo') | (aux.TipoElemento_Key_Clean=='etiqueta rcu ret')  | (aux.TipoElemento_Key_Clean=='etiqueta rcu ret si aplica') | (aux.TipoElemento_Key_Clean=='shelter') | (aux.TipoElemento_Key_Clean=='rack')]
```

#### Total de elementos


```python
Total_Elementos=aux.loc[(aux.TipoElemento_Key_Clean!=u'activo')].shape[0]
Total_Elementos
```




    171228




```python
aux.loc[(aux.TipoElemento_Key_Clean!=u'activo')]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_form</th>
      <th>clave_form</th>
      <th>element_group</th>
      <th>element</th>
      <th>exist</th>
      <th>TipoElemento_key</th>
      <th>TipoElemento_value</th>
      <th>TipoElemento_Key_Clean</th>
      <th>Trazabilidad</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>100079</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mg6000531</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>1</th>
      <td>101025</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupBbus-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102310wygn0g7014852</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>2</th>
      <td>101350</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem9wga110408</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>3</th>
      <td>101491</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-4</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>21023198974md9029272</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>4</th>
      <td>102228</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-3</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mf8018167</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>5</th>
      <td>102565</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem6tfb603528</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>6</th>
      <td>105936</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-2</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mg4013730</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>7</th>
      <td>106335</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-0</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102311chkn0g2014076</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>8</th>
      <td>107818</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem10h8009411</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>9</th>
      <td>107833</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mg6002133</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>10</th>
      <td>108225</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-2</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mg4049033</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>11</th>
      <td>111637</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-8</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102319897d0fc000680</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>12</th>
      <td>114606</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-4</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102310sfmhvfb025988</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>13</th>
      <td>118742</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-9</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102310sfmbtg3011712</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>14</th>
      <td>118746</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-7</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>210305488510hb000441</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>15</th>
      <td>121017</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mg3034742</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>16</th>
      <td>133291</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-2</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mfb013338</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>17</th>
      <td>154368</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-2</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem10h8003827</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>18</th>
      <td>171907</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-3</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>210305488510g4013548</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>19</th>
      <td>179872</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupBbus-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102112722p0f3004270</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>20</th>
      <td>19192</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-4</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>030lpm4md1004235</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>21</th>
      <td>19356</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-4</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102311chkn0fa017095</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>22</th>
      <td>19897</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-2</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>021hpr10f3002000</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>23</th>
      <td>19905</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupBbus-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>21021127229tb3007440</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>24</th>
      <td>20038</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupBbus-0</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>21021127226td2913324</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>25</th>
      <td>20251</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>020qyr4md9014807</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>26</th>
      <td>20619</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-1</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>020lajw0a3000336</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>27</th>
      <td>20792</td>
      <td>AIATP</td>
      <td>groupBbus-0</td>
      <td>groupCards-2</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>022hem4mf9011179</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>28</th>
      <td>20792</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-3</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>210305488510fb011982</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>29</th>
      <td>21139</td>
      <td>AIATP</td>
      <td>groupBbus-1</td>
      <td>groupCards-0</td>
      <td>True</td>
      <td>Numero de Serie (Escanner)</td>
      <td>2102311chk6tf8901529</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>421465</th>
      <td>100879</td>
      <td>AIATP</td>
      <td>groupShelter-0</td>
      <td>groupRack-1</td>
      <td>True</td>
      <td>RACK 02</td>
      <td></td>
      <td>rack</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421466</th>
      <td>30649</td>
      <td>AIATP</td>
      <td>groupShelter-0</td>
      <td>groupRack-1</td>
      <td>True</td>
      <td>RACK 02</td>
      <td></td>
      <td>rack</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421467</th>
      <td>100910</td>
      <td>AIATP</td>
      <td>groupShelter-0</td>
      <td>groupRack-1</td>
      <td>True</td>
      <td>RACK 02</td>
      <td></td>
      <td>rack</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421468</th>
      <td>35315</td>
      <td>AIATP</td>
      <td>groupShelter-0</td>
      <td>groupRack-1</td>
      <td>True</td>
      <td>RACK 02</td>
      <td></td>
      <td>rack</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421469</th>
      <td>21681</td>
      <td>AIATP</td>
      <td>groupShelter-0</td>
      <td>groupRack-1</td>
      <td>True</td>
      <td>RACK 02</td>
      <td></td>
      <td>rack</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421470</th>
      <td>22733</td>
      <td>AIATP</td>
      <td>groupShelter-0</td>
      <td>groupRack-1</td>
      <td>True</td>
      <td>RACK 02</td>
      <td></td>
      <td>rack</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421471</th>
      <td>21932</td>
      <td>AIATP</td>
      <td>groupShelter-0</td>
      <td>groupRack-1</td>
      <td>True</td>
      <td>RACK 02</td>
      <td></td>
      <td>rack</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421472</th>
      <td>36042</td>
      <td>AIATP</td>
      <td>groupShelter-0</td>
      <td>groupRack-1</td>
      <td>True</td>
      <td>RACK 02</td>
      <td></td>
      <td>rack</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421473</th>
      <td>21013</td>
      <td>AIATP</td>
      <td>groupShelter-0</td>
      <td>groupRack-1</td>
      <td>True</td>
      <td>RACK 02</td>
      <td></td>
      <td>rack</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421474</th>
      <td>22632</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421475</th>
      <td>35637</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421476</th>
      <td>30081</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421477</th>
      <td>30696</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421478</th>
      <td>29813</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421479</th>
      <td>35088</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421480</th>
      <td>36522</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421481</th>
      <td>36477</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421482</th>
      <td>29816</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421483</th>
      <td>34794</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421484</th>
      <td>27541</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421485</th>
      <td>30324</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421486</th>
      <td>21670</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421487</th>
      <td>21629</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421488</th>
      <td>62377</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421489</th>
      <td>59993</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421490</th>
      <td>32200</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421491</th>
      <td>30067</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421492</th>
      <td>30353</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421493</th>
      <td>31984</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>421494</th>
      <td>31154</td>
      <td>AIATP</td>
      <td>groupShelter-1</td>
      <td>groupShelter-1</td>
      <td>True</td>
      <td>SHELTER 02</td>
      <td></td>
      <td>shelter</td>
      <td>No Trazable</td>
    </tr>
  </tbody>
</table>
<p>171228 rows × 9 columns</p>
</div>



#### Total Elementos Trazables

Para el total de elementos trazables haremos una extracción del campo **TipoElemento_Key_Clean**  sea igual a **serie** o **activo**, esto nos servirá para poder hacer el calculado de los indicadores con serie con activo, con serie sin activo, sin serie con activo.  


```python
dfTrazables = pandasql.sqldf("WITH serie as (SELECT id_form, element_group, element, TipoElemento_Key_Clean as serie, tipoelemento_value as valor_serie FROM aux WHERE lower(TipoElemento_Key_Clean) = 'serie'), activo as ( SELECT id_form, element_group, element, TipoElemento_Key_Clean as activo, tipoelemento_value as valor_activo FROM aux WHERE lower(TipoElemento_Key_Clean) = 'activo') SELECT a.id_form, a.element, a.element_group, serie, valor_serie, activo, valor_activo FROM serie a LEFT JOIN activo b ON a.id_form = b.id_form AND a.element = b.element AND a.element_group = b.element_group;", locals())
```


```python
dfTrazables.activo.replace(to_replace=[None], value='activo', inplace=True)
dfTrazables.valor_activo.replace(to_replace=[None], value=np.nan, inplace=True)
dfTrazables.valor_activo.fillna('vacio',inplace=True)
```


```python
Total_Tr=dfTrazables.loc[(dfTrazables.valor_serie!='vacio') | (dfTrazables.valor_activo!='vacio')].shape[0]
Total_Tr
```




    127770



#### Total Elementos NO Trazables


```python
Total_NOTr=Total_Elementos-Total_Tr
Total_NOTr
```




    43458



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=dfTrazables[['valor_serie','valor_activo']].loc[(dfTrazables.valor_serie!='vacio') | (dfTrazables.valor_activo!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic
```




    96328



#### Total Elementos Trazables Duplicados


```python
Total_Tr_Dupli=Total_Tr-Total_Tr_Unic
Total_Tr_Dupli
```




    31442



#### Total Elementos Trazables Únicos Con Serie Con Activo


```python
Total_Tr_Unic_CS_CA=dfTrazables[['valor_serie','valor_activo']].loc[(dfTrazables.valor_serie!='vacio') & (dfTrazables.valor_activo!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_CS_CA
```




    2561



#### Total Elementos Trazables Únicos Con Serie Sin Activo


```python
Total_Tr_Unic_CS_SA=dfTrazables[['valor_serie','valor_activo']].loc[(dfTrazables.valor_serie!='vacio') & (dfTrazables.valor_activo=='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_CS_SA
```




    93640



#### Total Elementos Trazables Únicos Sin Serie Con Activo


```python
Total_Tr_Unic_SS_CA=dfTrazables[['valor_serie','valor_activo']].loc[(dfTrazables.valor_serie=='vacio') & (dfTrazables.valor_activo!='vacio')].drop_duplicates().shape[0]
Total_Tr_Unic_SS_CA
```




    127




```python
KPIs=pd.DataFrame({'KPI':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados',
                          'Total CS CA','Total CS SA','Total SS CA'],
                  'Resultado':[Total_Elementos,Total_Tr,Total_NOTr,
                              Total_Tr_Unic,Total_Tr_Dupli,
                               Total_Tr_Unic_CS_CA,Total_Tr_Unic_CS_SA,
                              Total_Tr_Unic_SS_CA]})

KPIs
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>KPI</th>
      <th>Resultado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Total Elementos</td>
      <td>171228</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>127770</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables</td>
      <td>43458</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total Trazables Unicos</td>
      <td>96328</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Duplicados</td>
      <td>31442</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Total CS CA</td>
      <td>2561</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Total CS SA</td>
      <td>93640</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Total SS CA</td>
      <td>127</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_hive_kpi = spark.createDataFrame(KPIs)
```


```python
#Se sube la tabla a Hive
df_hive_kpi.write.mode("overwrite").saveAsTable("default.kpi_odk_32")
```
