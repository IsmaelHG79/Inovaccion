
<div style="width: 100%; clear: both; font-family: Verdana;">
<div style="float: left; width: 50%;font-family: Verdana;">
<img src="https://github.com/Eligoze/att-rci-internal/blob/qa/RCI_DataAnalysis/eda/doc/att-logo1.png" align="left">
</div>
<div style="float: right; width: 200%;">
<p style="margin: 0; padding-top: 20px; text-align:right;color:rgb(193, 38, 184)"><strong>Axity - AT&T.
    Ciclo de vida de elementos de inventario</strong></p>
</div>
</div>
<div style="width:100%;">&nbsp;</div>

# Exploratory Data Analysis

## ODK 12 (ATP Instalación MW)

## Descripción

Analizaremos los datos de la fuente **ODK 12** que corresponde a los elementos que se encuentran en instalación de AT&T con un tratamiento estadístico descriptivo para la exploración, explotación y descubrimiento de los datos para un correcto tracking del ciclo de vida de los elementos de red. 
Para esta fuente en particular tenemos 10 formularios diferentes:

- **ATPMW**: ATP Instalación MW
- **MWITX**: ATP Instalación MW (Nuevo enlace Tx) Obsolete
- **MWIN2**: ATP Instalación MW (Nuevo Enlace)
- **AMWIN**: ATP Instalación MW (Nuevo Enlace) Obsolete
- **RFE80**: ATP Instalación MW (Nuevo enlace, MWS)
- **WITX2**: ATP Instalación MW (Nuevo enlace, Tx) 
- **AOP2**: ATP Optimización MW
- **MTX2**: ATP Optimización MW (Tx)
- **MWOTX**: ATP Optimización MW (Tx)-Obsolete
- **AMWOP**: ATP Optimización MW-Obsolete

Nos centraremos en las claves de ATPMW, WITX2, MWITX y MWIN2 que son los tipos de formulario que se encuentran en el datalake.

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
conf = SparkConf().setAppName('ODK_12')  \
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

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/fuzzywuzzy/fuzz.py:11: UserWarning: Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning
      warnings.warn('Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning')




    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="40846c39-71f6-4a14-92a0-73e7944b6296">Loading BokehJS ...</span>
    </div>




## 1. ODK 12
### 1. Recolección de los datos: 

Se crea el dataframe de spark con el universo de datos crudos.


```python
df = spark.sql("SELECT * FROM tx_stg_06_tabular_odk_12").cache().toPandas()
```


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>102341</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1519779261882.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>103636</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1521213704361.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>104237</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1522270194317.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>110042</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1529637323382.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>111650</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1532990550837.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>16089</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1450378225292.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>22410</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1458087131765.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>7</th>
      <td>33027</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1465578436201.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>8</th>
      <td>35255</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1468292677107.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>9</th>
      <td>38728</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1470936860504.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>10</th>
      <td>52562</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1482293070624.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>11</th>
      <td>59755</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1487865751088.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>12</th>
      <td>64107</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1491083675568.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>13</th>
      <td>67500</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1494280047539.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>14</th>
      <td>68682</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1495379343016.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>15</th>
      <td>71416</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1497818810101.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>16</th>
      <td>8224</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1430941420856.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>17</th>
      <td>8262</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1430640438481.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>18</th>
      <td>8556</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1435009206281.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>19</th>
      <td>90591</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1508963966834.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>20</th>
      <td>94009</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1511461642926.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>21</th>
      <td>99584</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1516374128215.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>22</th>
      <td>102615</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1518816187625.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>23</th>
      <td>103895</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1520875644122.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>24</th>
      <td>104211</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1522246661003.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>25</th>
      <td>12508</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1445597218125.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>26</th>
      <td>23025</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1458431638791.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>27</th>
      <td>29303</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1462676722731.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>28</th>
      <td>38928</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1471635408455.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>29</th>
      <td>39387</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1471632209970.jpg (image/jpeg)</td>
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
    </tr>
    <tr>
      <th>75558</th>
      <td>107362</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>201607</td>
    </tr>
    <tr>
      <th>75559</th>
      <td>89889</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>01071089</td>
    </tr>
    <tr>
      <th>75560</th>
      <td>108715</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102310BES10DC000281</td>
    </tr>
    <tr>
      <th>75561</th>
      <td>104063</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102113821N0F9001918</td>
    </tr>
    <tr>
      <th>75562</th>
      <td>105118</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102120762N0F9001934</td>
    </tr>
    <tr>
      <th>75563</th>
      <td>100957</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102310BES10F1000357</td>
    </tr>
    <tr>
      <th>75564</th>
      <td>103485</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102113821N0FA000100</td>
    </tr>
    <tr>
      <th>75565</th>
      <td>99263</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>MDP-400MB-1BB</td>
    </tr>
    <tr>
      <th>75566</th>
      <td>99263</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>NWA-063847-001</td>
    </tr>
    <tr>
      <th>75567</th>
      <td>99263</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>0000045107</td>
    </tr>
    <tr>
      <th>75568</th>
      <td>99263</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>201606</td>
    </tr>
    <tr>
      <th>75569</th>
      <td>91029</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>E275J02208</td>
    </tr>
    <tr>
      <th>75570</th>
      <td>104001</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102113821N0F8002736</td>
    </tr>
    <tr>
      <th>75571</th>
      <td>107358</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>BS-0278-0</td>
    </tr>
    <tr>
      <th>75572</th>
      <td>105277</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>MDP-400MB-1BB</td>
    </tr>
    <tr>
      <th>75573</th>
      <td>105277</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>NWA-063847-001</td>
    </tr>
    <tr>
      <th>75574</th>
      <td>105277</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>0000044413</td>
    </tr>
    <tr>
      <th>75575</th>
      <td>105277</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>201607</td>
    </tr>
    <tr>
      <th>75576</th>
      <td>97350</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>21021131746TB7906070</td>
    </tr>
    <tr>
      <th>75577</th>
      <td>96089</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>00887432</td>
    </tr>
    <tr>
      <th>75578</th>
      <td>91279</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>3G010100</td>
    </tr>
    <tr>
      <th>75579</th>
      <td>94657</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102352307P0D7000279</td>
    </tr>
    <tr>
      <th>75580</th>
      <td>115574</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>210235257110D8000162</td>
    </tr>
    <tr>
      <th>75581</th>
      <td>99522</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>MDP-400MB-1BB</td>
    </tr>
    <tr>
      <th>75582</th>
      <td>99522</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>NWA-063847-001</td>
    </tr>
    <tr>
      <th>75583</th>
      <td>99522</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>0000044997</td>
    </tr>
    <tr>
      <th>75584</th>
      <td>99522</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>201606</td>
    </tr>
    <tr>
      <th>75585</th>
      <td>103636</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>21021138216TF8904900</td>
    </tr>
    <tr>
      <th>75586</th>
      <td>101386</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>BS-0278-0</td>
    </tr>
    <tr>
      <th>75587</th>
      <td>94736</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>21021138216TG3902365</td>
    </tr>
  </tbody>
</table>
<p>75588 rows × 7 columns</p>
</div>



Para las fuentes de los ODK's nos interesa conocer todos los elementos en sitio, por lo que haremos una limpieza en los campos que contengan características de los mismos.
Creamos una función para el tratamiento del campo de sitio en spark el cual contiene ciertas reglas definidas para su limpieza.

### Una muestra del ODK 12:


```python
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>102341</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1519779261882.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>103636</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1521213704361.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>104237</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1522270194317.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>110042</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1529637323382.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>111650</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1532990550837.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>16089</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1450378225292.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>22410</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1458087131765.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>7</th>
      <td>33027</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1465578436201.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>8</th>
      <td>35255</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1468292677107.jpg (image/jpeg)</td>
    </tr>
    <tr>
      <th>9</th>
      <td>38728</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1470936860504.jpg (image/jpeg)</td>
    </tr>
  </tbody>
</table>
</div>



### 2. Descripción de las fuentes.

En este apartado se describe a detalle el tipo información de la fuente para una mejor comprensión de los datos. Se mostrarán los tipos de datos, tamaño de la fuente, es decir, su dimensionalidad y una estadística descriptiva, en ese orden.


```python
print 'renglones = ',df.shape[0],' columnas = ',df.shape[1]
```

    renglones =  75588  columnas =  7


#### Una breve descripción de los campos:
* **id_form**: Número de formulario en *Panda*.
* **clave_form**: Clave de identificación del ODK.
* **element_group**: Element group.
* **element**: Hijo del element group.
* **exist**: Campo diseñado durante la extracción de los datos para identificar que el campo buscado se encuentra existente.
* **TipoElemento_key**: Nombre del campo.
* **TipoElemento_value**: Atributo del campo.

Con la transformación que se llevo a cabo previamente, los campos **id_form, clave_form, element_group, element, exist** sirven para tener un control y mejor manejo del odk. Los campos **TipoElemento_key y TipoElemento_value** son los que se utilizarán para sacar indicadores.
A continuación se muestran los datos únicos en el campo **TipoElemento_Key**

Se muestra la información de campos únicos que se encuentran en **TipoElemento_Key** de nuestra tabla que vamos a considerar para los cálculos.


```python
df.TipoElemento_key.unique().tolist()
```




    [u'Barra de Tierra',
     u'Barra de Tierra en Torre',
     u'Segunda Barra de Tierra en Torre',
     u'N\xfamero de serie (manual)',
     None,
     u'Modelo de la antena de MW',
     u'Modelo de ODU',
     u'Modelo',
     u'Modelo de IDU',
     u'N\xfamero de activo fijo (manual)',
     u'Fabricante / Modelo de antena de MW',
     u'N\xfamero de serie (esc\xe1ner)',
     u'Fabricante',
     u'N\xfamero de activo fijo (esc\xe1ner)',
     u'Atizador',
     u'PTR',
     u'Fabricante / Modelo IDU']



Podemos observar que algunos de los campos contienen caractéres especiales que posteriormente se hará una limpieza.
A continuación se muestran un conteo de los campos que se obtuvieron de la transformación en el notebook Adquisición_Datos_ODK_12.


```python
pandasql.sqldf("SELECT tipoelemento_key, count(*) as conteo FROM df group by tipoelemento_key;", locals())
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_key</th>
      <th>conteo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>None</td>
      <td>597</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Atizador</td>
      <td>937</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Barra de Tierra</td>
      <td>6983</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Barra de Tierra en Torre</td>
      <td>6982</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Fabricante</td>
      <td>6337</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Fabricante / Modelo IDU</td>
      <td>1254</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Fabricante / Modelo de antena de MW</td>
      <td>2356</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Modelo</td>
      <td>9375</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Modelo de IDU</td>
      <td>6986</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Modelo de ODU</td>
      <td>7918</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Modelo de la antena de MW</td>
      <td>7918</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Número de activo fijo (escáner)</td>
      <td>2212</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Número de activo fijo (manual)</td>
      <td>5368</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Número de serie (escáner)</td>
      <td>1846</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Número de serie (manual)</td>
      <td>5734</td>
    </tr>
    <tr>
      <th>15</th>
      <td>PTR</td>
      <td>937</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Segunda Barra de Tierra en Torre</td>
      <td>1848</td>
    </tr>
  </tbody>
</table>
</div>



Para el cálculo de indicadores que se va a realizar mas adelante, nos vamos a enfocar en el campo Número de Serie (manual) y Serie (escáner) los cuales son campos identificados que contienen números de serie.


```python
dfSerie = pandasql.sqldf("SELECT tipoelemento_value FROM df WHERE tipoelemento_key IN ('Número de serie (manual)', 'Número de serie (escáner)');", locals())
dfSerie.describe(include='all')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>7580</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>5806</td>
    </tr>
    <tr>
      <th>top</th>
      <td>N/A</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>180</td>
    </tr>
  </tbody>
</table>
</div>



Podemos observar que en la tabla tenemos el total del número de serie con el **count**, los campos únicos con **unique** y el valor que más se repite con el **top** y cuántas veces se retipe con el **freq**.

Debemos de tener en cuenta que el número de renglones no representa el número de elementos sino que es la información al nivel más bajo de cada formulario. Es decir, debemos considerar que para cada id_form hay diferente número de registros.

### Tamaño de la fuente


```python
print('rows = ',df.shape[0],' columnas = ',df.shape[1])
```

    ('rows = ', 75588, ' columnas = ', 7)


### 3. Exploración de los datos.

De acuerdo al análisis anterior, procederemos a observar algunos detalles de la fuente:


```python
print 'Los atributos priority que encontramos en este ODK en los distintos element groups son:'
Freq_Atributos=pd.DataFrame(df.TipoElemento_key.value_counts())
Freq_Atributos
```

    Los atributos priority que encontramos en este ODK en los distintos element groups son:





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_key</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Modelo</th>
      <td>9375</td>
    </tr>
    <tr>
      <th>Modelo de ODU</th>
      <td>7918</td>
    </tr>
    <tr>
      <th>Modelo de la antena de MW</th>
      <td>7918</td>
    </tr>
    <tr>
      <th>Modelo de IDU</th>
      <td>6986</td>
    </tr>
    <tr>
      <th>Barra de Tierra</th>
      <td>6983</td>
    </tr>
    <tr>
      <th>Barra de Tierra en Torre</th>
      <td>6982</td>
    </tr>
    <tr>
      <th>Fabricante</th>
      <td>6337</td>
    </tr>
    <tr>
      <th>Número de serie (manual)</th>
      <td>5734</td>
    </tr>
    <tr>
      <th>Número de activo fijo (manual)</th>
      <td>5368</td>
    </tr>
    <tr>
      <th>Fabricante / Modelo de antena de MW</th>
      <td>2356</td>
    </tr>
    <tr>
      <th>Número de activo fijo (escáner)</th>
      <td>2212</td>
    </tr>
    <tr>
      <th>Segunda Barra de Tierra en Torre</th>
      <td>1848</td>
    </tr>
    <tr>
      <th>Número de serie (escáner)</th>
      <td>1846</td>
    </tr>
    <tr>
      <th>Fabricante / Modelo IDU</th>
      <td>1254</td>
    </tr>
    <tr>
      <th>PTR</th>
      <td>937</td>
    </tr>
    <tr>
      <th>Atizador</th>
      <td>937</td>
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




![png](output_29_1.png)


#### Se hará una limpieza para homologar los campos de serie y activo:



```python
stoppers=[u'numero de',u'número de',u'escaner',u'manual',u' fijo',u'escáner',u'scanner']
df['TipoElemento_Key_Clean']=df.TipoElemento_key

df.TipoElemento_Key_Clean=df.TipoElemento_Key_Clean.str.lower()
df.TipoElemento_Key_Clean=df.TipoElemento_Key_Clean.str.replace("\)",'')
df.TipoElemento_Key_Clean=df.TipoElemento_Key_Clean.str.replace("\(",'')
df.TipoElemento_Key_Clean.replace(u'á',u'a',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'é',u'e',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'í',u'i',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'ó',u'o',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'ú',u'u',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(u'ú',u'u',regex=True,inplace=True)
df.TipoElemento_Key_Clean.replace(stoppers,u'',regex=True,inplace=True)
df.TipoElemento_Key_Clean=df.TipoElemento_Key_Clean.str.strip()
```

#### Después de haber pasado una limpieza, podemos tener homologados los campos:


```python
#Se debe observar que serie y activo han quedado homologados
pd.DataFrame(df.TipoElemento_Key_Clean.value_counts())
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_Key_Clean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>modelo</th>
      <td>9375</td>
    </tr>
    <tr>
      <th>modelo de odu</th>
      <td>7918</td>
    </tr>
    <tr>
      <th>modelo de la antena de mw</th>
      <td>7918</td>
    </tr>
    <tr>
      <th>serie</th>
      <td>7580</td>
    </tr>
    <tr>
      <th>activo</th>
      <td>7580</td>
    </tr>
    <tr>
      <th>modelo de idu</th>
      <td>6986</td>
    </tr>
    <tr>
      <th>barra de tierra</th>
      <td>6983</td>
    </tr>
    <tr>
      <th>barra de tierra en torre</th>
      <td>6982</td>
    </tr>
    <tr>
      <th>fabricante</th>
      <td>6337</td>
    </tr>
    <tr>
      <th>fabricante / modelo de antena de mw</th>
      <td>2356</td>
    </tr>
    <tr>
      <th>segunda barra de tierra en torre</th>
      <td>1848</td>
    </tr>
    <tr>
      <th>fabricante / modelo idu</th>
      <td>1254</td>
    </tr>
    <tr>
      <th>ptr</th>
      <td>937</td>
    </tr>
    <tr>
      <th>atizador</th>
      <td>937</td>
    </tr>
  </tbody>
</table>
</div>



Hacemos una descripción del campo homologado con serie.


```python
#pd.DataFrame(df.TipoElemento_Key_Clean.loc[df.TipoElemento_Key_Clean=='serie'].describe())
pd.DataFrame(df.TipoElemento_value.loc[df.TipoElemento_Key_Clean=='serie'].describe())
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>7580</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>5806</td>
    </tr>
    <tr>
      <th>top</th>
      <td>N/A</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>180</td>
    </tr>
  </tbody>
</table>
</div>



Hacemos una descripción del campo homologado con activo.


```python
#pd.DataFrame(df.TipoElemento_Key_Clean.loc[df.TipoElemento_Key_Clean=='activo'].describe())
pd.DataFrame(df.TipoElemento_value.loc[df.TipoElemento_Key_Clean=='activo'].describe())
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>7580</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>4706</td>
    </tr>
    <tr>
      <th>top</th>
      <td>N/A</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>392</td>
    </tr>
  </tbody>
</table>
</div>



#### Campo Fabricante


```python
Cat_Fabricante=pd.DataFrame(df.TipoElemento_value.loc[df.TipoElemento_Key_Clean=='fabricante']).drop_duplicates().reset_index(drop=True)
Cat_Fabricante.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>CERAGON</td>
    </tr>
    <tr>
      <th>1</th>
      <td>OTH</td>
    </tr>
    <tr>
      <th>2</th>
      <td>N/A</td>
    </tr>
    <tr>
      <th>3</th>
      <td>RadioFrecunciaSistems</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Ceragon</td>
    </tr>
  </tbody>
</table>
</div>




```python
dirt=['no visible','n/v','nv','ilegible',u'n/a','na','no legible','N/A',
      'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene','No visble','no visble',u'versió',
      'No viaible','noisible','no aplica','n /v','finizar','no bisible','finisar','finsar',u'ftlfpbnl',u'ñ/a',u'ñ']

#En caso de que se requieran eliminar los números se utilizará la siguiente lista:
nums=['1','2','3','4','5','6','7','8','9','0']

Cat_Fabricante.TipoElemento_value=Cat_Fabricante.TipoElemento_value.str.lower()
Cat_Fabricante.TipoElemento_value=Cat_Fabricante.TipoElemento_value.str.replace('.','')
Cat_Fabricante.TipoElemento_value.fillna(np.NaN,inplace=True)
Cat_Fabricante.replace(u'inc.','',regex=True,inplace=True)
Cat_Fabricante.TipoElemento_value.replace(dirt,'',regex=True,inplace=True)
Cat_Fabricante.head(20)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>ceragon</td>
    </tr>
    <tr>
      <th>1</th>
      <td>oth</td>
    </tr>
    <tr>
      <th>2</th>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>radiofrecunciasistems</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ceragon</td>
    </tr>
    <tr>
      <th>5</th>
      <td>nec</td>
    </tr>
    <tr>
      <th>6</th>
      <td>nec</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ceragon</td>
    </tr>
    <tr>
      <th>8</th>
      <td>hwi</td>
    </tr>
    <tr>
      <th>9</th>
      <td>nec</td>
    </tr>
    <tr>
      <th>10</th>
      <td>nec</td>
    </tr>
    <tr>
      <th>11</th>
      <td>radio frequency systems</td>
    </tr>
    <tr>
      <th>12</th>
      <td>oth</td>
    </tr>
    <tr>
      <th>13</th>
      <td></td>
    </tr>
    <tr>
      <th>14</th>
      <td>ceragon</td>
    </tr>
    <tr>
      <th>15</th>
      <td>nec pasolink</td>
    </tr>
    <tr>
      <th>16</th>
      <td>nec pasolink</td>
    </tr>
    <tr>
      <th>17</th>
      <td></td>
    </tr>
    <tr>
      <th>18</th>
      <td></td>
    </tr>
    <tr>
      <th>19</th>
      <td>atel</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Similitud de palabras se usarán las librerías fuzzywuzzy y nltk:
fdist=FreqDist(Cat_Fabricante.TipoElemento_value)
fdist.most_common(100)
```




    [(u' ', 9),
     (u'  ', 9),
     (u'  seniortek', 5),
     (u' nec pasolink', 5),
     (u' nec ipasolink', 5),
     (u'  nec pasolink', 4),
     (u' ceragon', 4),
     (u' ipasolink', 3),
     (u'  universal microwave technology', 3),
     (u' commscope', 3),
     (u' nec paso link', 3),
     (u'  senior tek', 3),
     (u' radio frequency systems', 3),
     (u'  ceragon', 3),
     (u' ceragon ip20c', 3),
     (u' nec', 3),
     (u'  universal microwave tecnology', 2),
     (u'  nec', 2),
     (u' rfs', 2),
     (u'  commscope', 2),
     (u' atel', 2),
     (u' chatsworth', 2),
     (u'  rfs', 2),
     (u'  no lleva acoplador', 2),
     (u' comscope', 2),
     (u'  andrew', 2),
     (u' radio frecuency systems', 2),
     (u' ericsson', 2),
     (u'  (omt) universal microwave technologyseniortek', 2),
     (u' rack', 2),
     (u' ipasolink nec', 2),
     (u' seragon', 2),
     (u' huawei', 2),
     (u'  ipasolink', 2),
     (u' ip20c', 2),
     (u'  nec ipasolink', 2),
     (u' andrew', 2),
     (u'  hwi', 1),
     (u' nec pasolinik', 1),
     (u' apm30h', 1),
     (u' rfc', 1),
     (u' x', 1),
     (u' ip-20c-hp', 1),
     (u' nec ipaso link', 1),
     (u' chatsworth producs inc', 1),
     (u'  no/a', 1),
     (u' rak', 1),
     (u' ipasolink 20n', 1),
     (u'  seniorterk', 1),
     (u'  nec passolink', 1),
     (u' nec 64', 1),
     (u' existen', 1),
     (u'  commscope nec', 1),
     (u' ip 20c hp 10 350b', 1),
     (u' ip 20 ceragon', 1),
     (u'  n/d', 1),
     (u' 0', 1),
     (u' no trae', 1),
     (u'  hybrid coupler', 1),
     (u'  seragon', 1),
     (u' commscope-andrew', 1),
     (u' nec- ipasolink1000', 1),
     (u' chats worth products', 1),
     (u' commscope adrew', 1),
     (u' cergon', 1),
     (u' ip-20c-f-23-h-l-esx', 1),
     (u'  c112mnsg', 1),
     (u' commscope nec', 1),
     (u' ip-20c-hp-10-350b-1w5-h-esx', 1),
     (u' commscop', 1),
     (u' ipasolink nec 1000', 1),
     (u' seniortek', 1),
     (u' ceragon ip20n', 1),
     (u'  evidencia de cambio de ante', 1),
     (u'  technology inc', 1),
     (u' ip-20c-f23-h-h-esx', 1),
     (u' radiofrecunciasistems', 1),
     (u' radio frecuncy systems', 1),
     (u' nec pasoling', 1),
     (u' nec  pasolink', 1),
     (u' radio frecueny systems', 1),
     (u' standart tipo newton', 1),
     (u'  oth', 1),
     (u' nec pazolink', 1),
     (u'  universal microwave technology inc', 1),
     (u'  pasolink', 1),
     (u' tipo newton', 1),
     (u' nec-pasolink', 1),
     (u' commscope andrew', 1),
     (u'  ceragon seniortek', 1),
     (u' nextel', 1),
     (u' newton', 1),
     (u' radiofrecuenciasistems', 1),
     (u' nek', 1),
     (u'  ipasolink nec', 1),
     (u' nec ipasoling', 1),
     (u' mec', 1),
     (u' commacope', 1),
     (u' compscop', 1),
     (u' paso link 400', 1)]




```python
len(fdist)
```




    150




```python
Clean_Fabricante=[v for v,k in fdist.items() if k>2]

#En caso de querer agregar elementos:
#Clean_CAMPO.append(u'ELEMENTO')

#En caso de querer eliminar elementos:
#Clean_CAMPO.remove(u'ELEMENTO')

Clean_Fabricante
```




    [u'  nec pasolink',
     u' ',
     u' ipasolink',
     u'  ',
     u'  seniortek',
     u'  universal microwave technology',
     u' commscope',
     u' nec pasolink',
     u' nec paso link',
     u' ceragon',
     u'  senior tek',
     u' nec ipasolink',
     u' radio frequency systems',
     u'  ceragon',
     u' ceragon ip20c',
     u' nec']




```python
Cat_Fabricante['Clean']=1
for v in range(0,Cat_Fabricante.shape[0]):
    Cat_Fabricante.Clean[v]=process.extractOne(Cat_Fabricante.TipoElemento_value[v],
                                            Clean_Fabricante,
                                            scorer=fuzz.partial_ratio,
                                            score_cutoff=67)
    if Cat_Fabricante.Clean[v] is None:
        Cat_Fabricante.Clean[v]=Cat_Fabricante.TipoElemento_value[v]
    else:
        Cat_Fabricante.Clean[v]=Cat_Fabricante.Clean[v][0]

Cat_Fabricante.head(15)
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/ipykernel_launcher.py:6: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      
    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/pandas/core/indexing.py:189: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self._setitem_with_indexer(indexer, value)
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: '  ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: '  ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: '  ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: '  ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: '  ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: '  ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: '  ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: '  ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: '  ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_value</th>
      <th>Clean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ceragon</td>
      <td>ceragon</td>
    </tr>
    <tr>
      <th>1</th>
      <td>oth</td>
      <td>seniortek</td>
    </tr>
    <tr>
      <th>2</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>radiofrecunciasistems</td>
      <td>radio frequency systems</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ceragon</td>
      <td>ceragon</td>
    </tr>
    <tr>
      <th>5</th>
      <td>nec</td>
      <td>nec pasolink</td>
    </tr>
    <tr>
      <th>6</th>
      <td>nec</td>
      <td>nec pasolink</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ceragon</td>
      <td>ceragon</td>
    </tr>
    <tr>
      <th>8</th>
      <td>hwi</td>
      <td>hwi</td>
    </tr>
    <tr>
      <th>9</th>
      <td>nec</td>
      <td>nec pasolink</td>
    </tr>
    <tr>
      <th>10</th>
      <td>nec</td>
      <td>nec pasolink</td>
    </tr>
    <tr>
      <th>11</th>
      <td>radio frequency systems</td>
      <td>radio frequency systems</td>
    </tr>
    <tr>
      <th>12</th>
      <td>oth</td>
      <td>seniortek</td>
    </tr>
    <tr>
      <th>13</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>14</th>
      <td>ceragon</td>
      <td>ceragon</td>
    </tr>
  </tbody>
</table>
</div>



Mostramos los primeros registros del catálogo terminado:


```python
#Una vez listo el catálogo, podemos tirar la columna TipoElemento_value:
Cat_Fabricante.drop(columns=['TipoElemento_value'],inplace=True)
Cat_Fabricante.columns=['Atributos']
Cat_Fabricante.drop_duplicates(inplace=True)
Cat_Fabricante.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>ceragon</td>
    </tr>
    <tr>
      <th>1</th>
      <td>seniortek</td>
    </tr>
    <tr>
      <th>2</th>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>radio frequency systems</td>
    </tr>
    <tr>
      <th>5</th>
      <td>nec pasolink</td>
    </tr>
    <tr>
      <th>8</th>
      <td>hwi</td>
    </tr>
    <tr>
      <th>19</th>
      <td>atel</td>
    </tr>
    <tr>
      <th>20</th>
      <td>huawei</td>
    </tr>
    <tr>
      <th>21</th>
      <td>hwi</td>
    </tr>
    <tr>
      <th>22</th>
      <td>commscope</td>
    </tr>
  </tbody>
</table>
</div>



#### Campo Modelo de la Antena de MW


```python
Cat_Modelo_AMW=pd.DataFrame(df.TipoElemento_value.loc[df.TipoElemento_Key_Clean=='modelo de la antena de mw']).drop_duplicates().reset_index(drop=True)
Cat_Modelo_AMW.head(16)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>COMM</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MWA41</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MWA31</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MWA29</td>
    </tr>
    <tr>
      <th>4</th>
      <td>OTH</td>
    </tr>
    <tr>
      <th>5</th>
      <td>MWA23</td>
    </tr>
    <tr>
      <th>6</th>
      <td>MWA5</td>
    </tr>
    <tr>
      <th>7</th>
      <td>MWA47</td>
    </tr>
    <tr>
      <th>8</th>
      <td>MWA28</td>
    </tr>
    <tr>
      <th>9</th>
      <td>MWA16</td>
    </tr>
    <tr>
      <th>10</th>
      <td>MWA33</td>
    </tr>
    <tr>
      <th>11</th>
      <td>MWA22</td>
    </tr>
    <tr>
      <th>12</th>
      <td>MWA45</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MWA38</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MWA24</td>
    </tr>
    <tr>
      <th>15</th>
      <td>MWA21</td>
    </tr>
  </tbody>
</table>
</div>




```python
dirt=['no visible','n/v','nv','ilegible',u'n/a','na','no legible','N/A',
      'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene','No visble','no visble',u'versió',
      'No viaible','noisible','no aplica','n /v','finizar','no bisible','finisar','finsar',u'ftlfpbnl',u'ñ/a',u'ñ']

#En caso de que se requieran eliminar los números se utilizará la siguiente lista:
nums=['1','2','3','4','5','6','7','8','9','0']

Cat_Modelo_AMW.TipoElemento_value=Cat_Modelo_AMW.TipoElemento_value.str.lower()
Cat_Modelo_AMW.TipoElemento_value=Cat_Modelo_AMW.TipoElemento_value.str.replace('.','')
Cat_Modelo_AMW.TipoElemento_value.fillna(np.NaN,inplace=True)
Cat_Modelo_AMW.replace(u'inc.','',regex=True,inplace=True)
Cat_Modelo_AMW.TipoElemento_value.replace(dirt,'',regex=True,inplace=True)
Cat_Modelo_AMW.head(20)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>comm</td>
    </tr>
    <tr>
      <th>1</th>
      <td>mwa41</td>
    </tr>
    <tr>
      <th>2</th>
      <td>mwa31</td>
    </tr>
    <tr>
      <th>3</th>
      <td>mwa29</td>
    </tr>
    <tr>
      <th>4</th>
      <td>oth</td>
    </tr>
    <tr>
      <th>5</th>
      <td>mwa23</td>
    </tr>
    <tr>
      <th>6</th>
      <td>mwa5</td>
    </tr>
    <tr>
      <th>7</th>
      <td>mwa47</td>
    </tr>
    <tr>
      <th>8</th>
      <td>mwa28</td>
    </tr>
    <tr>
      <th>9</th>
      <td>mwa16</td>
    </tr>
    <tr>
      <th>10</th>
      <td>mwa33</td>
    </tr>
    <tr>
      <th>11</th>
      <td>mwa22</td>
    </tr>
    <tr>
      <th>12</th>
      <td>mwa45</td>
    </tr>
    <tr>
      <th>13</th>
      <td>mwa38</td>
    </tr>
    <tr>
      <th>14</th>
      <td>mwa24</td>
    </tr>
    <tr>
      <th>15</th>
      <td>mwa21</td>
    </tr>
    <tr>
      <th>16</th>
      <td>mwa49</td>
    </tr>
    <tr>
      <th>17</th>
      <td>mwa17</td>
    </tr>
    <tr>
      <th>18</th>
      <td>mwa20</td>
    </tr>
    <tr>
      <th>19</th>
      <td>mwa2</td>
    </tr>
  </tbody>
</table>
</div>



#### Campo Modelo


```python
Cat_Modelo=pd.DataFrame(df.TipoElemento_value.loc[df.TipoElemento_Key_Clean=='modelo']).drop_duplicates().reset_index(drop=True)
Cat_Modelo.head(16)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>VHLPX4-7W-3WH/E</td>
    </tr>
    <tr>
      <th>1</th>
      <td>OTH</td>
    </tr>
    <tr>
      <th>2</th>
      <td>RTN XMC 7G-3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>OTH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>VHLPX6-7W3/WH</td>
    </tr>
    <tr>
      <th>5</th>
      <td>RTN-XMC-7G-2</td>
    </tr>
    <tr>
      <th>6</th>
      <td>N/A</td>
    </tr>
    <tr>
      <th>7</th>
      <td>HSX4-71-B3A/A</td>
    </tr>
    <tr>
      <th>8</th>
      <td>TRP-7G-1E</td>
    </tr>
    <tr>
      <th>9</th>
      <td>CBG-020276-002</td>
    </tr>
    <tr>
      <th>10</th>
      <td>VHLPX2-15-3WH/A</td>
    </tr>
    <tr>
      <th>11</th>
      <td>RTN-XMC-15G-2</td>
    </tr>
    <tr>
      <th>12</th>
      <td>C15U06RRC</td>
    </tr>
    <tr>
      <th>13</th>
      <td>VHLP6-7W-CR-4C</td>
    </tr>
    <tr>
      <th>14</th>
      <td>IP-20C-HP-7-161A-1W2</td>
    </tr>
    <tr>
      <th>15</th>
      <td>No visible</td>
    </tr>
  </tbody>
</table>
</div>



#### Campo Modelo de la Antena de MW


```python
Cat_Modelo_AMW=pd.DataFrame(df.TipoElemento_value.loc[df.TipoElemento_Key_Clean=='modelo de la antena de mw']).drop_duplicates().reset_index(drop=True)
Cat_Modelo_AMW.head(16)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>COMM</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MWA41</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MWA31</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MWA29</td>
    </tr>
    <tr>
      <th>4</th>
      <td>OTH</td>
    </tr>
    <tr>
      <th>5</th>
      <td>MWA23</td>
    </tr>
    <tr>
      <th>6</th>
      <td>MWA5</td>
    </tr>
    <tr>
      <th>7</th>
      <td>MWA47</td>
    </tr>
    <tr>
      <th>8</th>
      <td>MWA28</td>
    </tr>
    <tr>
      <th>9</th>
      <td>MWA16</td>
    </tr>
    <tr>
      <th>10</th>
      <td>MWA33</td>
    </tr>
    <tr>
      <th>11</th>
      <td>MWA22</td>
    </tr>
    <tr>
      <th>12</th>
      <td>MWA45</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MWA38</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MWA24</td>
    </tr>
    <tr>
      <th>15</th>
      <td>MWA21</td>
    </tr>
  </tbody>
</table>
</div>



#### Campo Fabricante / Modelo de Antena de MW


```python
Cat_Fab_AMW=pd.DataFrame(df.TipoElemento_value.loc[df.TipoElemento_Key_Clean=='fabricante / modelo de antena de mw']).drop_duplicates().reset_index(drop=True)
Cat_Fab_AMW.head(16)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>Andrew / VHLPX4-11W</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ANDREW VHLPX4-7W-HW1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ANDREW-VHLPX4-7W-3WH/E</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Commscope SPHX3-23-2wh</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ANDREW-VHLPX4-15-3WH/C</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Commscope VHLP2-23-HW1A</td>
    </tr>
    <tr>
      <th>6</th>
      <td>ANDREW VHLPX6-7W-3WH/B</td>
    </tr>
    <tr>
      <th>7</th>
      <td>RFS SC2 W71BIPN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>RFS SC2-W71BIPN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>ANDREW-SU2-71</td>
    </tr>
    <tr>
      <th>10</th>
      <td>A07D12HS</td>
    </tr>
    <tr>
      <th>11</th>
      <td>N/A</td>
    </tr>
    <tr>
      <th>12</th>
      <td>HUAWEI - MODELO</td>
    </tr>
    <tr>
      <th>13</th>
      <td>HUAWEI-A07D12HS</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Huawei/A07D18HS</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Andrew VHLP4-7W-HW1</td>
    </tr>
  </tbody>
</table>
</div>




```python
dirt=['no visible','n/v','nv','ilegible',u'n/a','na','no legible','N/A',
      'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene','No visble','no visble',u'versió',
      'No viaible','noisible','no aplica','n /v','finizar','no bisible','finisar','finsar',u'ftlfpbnl',u'ñ/a',u'ñ']

#En caso de que se requieran eliminar los números se utilizará la siguiente lista:
nums=['1','2','3','4','5','6','7','8','9','0']

Cat_Fab_AMW.TipoElemento_value=Cat_Fab_AMW.TipoElemento_value.str.lower()
Cat_Fab_AMW.TipoElemento_value=Cat_Fab_AMW.TipoElemento_value.str.replace('.','')
Cat_Fab_AMW.TipoElemento_value.fillna(np.NaN,inplace=True)
Cat_Fab_AMW.replace(u'inc.','',regex=True,inplace=True)
Cat_Fab_AMW.TipoElemento_value.replace(dirt,'',regex=True,inplace=True)
Cat_Fab_AMW.head(20)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>andrew / vhlpx4-11w</td>
    </tr>
    <tr>
      <th>1</th>
      <td>andrew vhlpx4-7w-hw1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>andrew-vhlpx4-7w-3wh/e</td>
    </tr>
    <tr>
      <th>3</th>
      <td>commscope sphx3-23-2wh</td>
    </tr>
    <tr>
      <th>4</th>
      <td>andrew-vhlpx4-15-3wh/c</td>
    </tr>
    <tr>
      <th>5</th>
      <td>commscope vhlp2-23-hw1a</td>
    </tr>
    <tr>
      <th>6</th>
      <td>andrew vhlpx6-7w-3wh/b</td>
    </tr>
    <tr>
      <th>7</th>
      <td>rfs sc2 w71bipn</td>
    </tr>
    <tr>
      <th>8</th>
      <td>rfs sc2-w71bipn</td>
    </tr>
    <tr>
      <th>9</th>
      <td>andrew-su2-71</td>
    </tr>
    <tr>
      <th>10</th>
      <td>a07d12hs</td>
    </tr>
    <tr>
      <th>11</th>
      <td></td>
    </tr>
    <tr>
      <th>12</th>
      <td>huawei - modelo</td>
    </tr>
    <tr>
      <th>13</th>
      <td>huawei-a07d12hs</td>
    </tr>
    <tr>
      <th>14</th>
      <td>huawei/a07d18hs</td>
    </tr>
    <tr>
      <th>15</th>
      <td>andrew vhlp4-7w-hw1</td>
    </tr>
    <tr>
      <th>16</th>
      <td>andrew vhlp2-23-nc3</td>
    </tr>
    <tr>
      <th>17</th>
      <td>ceragon/ip20b-23-c28x</td>
    </tr>
    <tr>
      <th>18</th>
      <td>commscope / andrew - 23 - nc3</td>
    </tr>
    <tr>
      <th>19</th>
      <td>shpx-23-2wh</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Similitud de palabras se usarán las librerías fuzzywuzzy y nltk:
fdist2=FreqDist(Cat_Fab_AMW.TipoElemento_value)
fdist2.most_common(100)
```




    [(u' ', 5),
     (u' commscope vhlpx4-11w-3wh/a', 4),
     (u' andrew shp3-15-cr4', 4),
     (u' commscope vhlpx6-7w-3wh/b', 4),
     (u' commscope vhlpx2-15-3wh/a', 3),
     (u' andrew vhlpx4-15-3wh/c', 3),
     (u' commscope vhlpx2-23-3wh/b', 3),
     (u' huahuei  a07d18hs', 3),
     (u' andrew shp2-15-cr4', 3),
     (u' andrew', 3),
     (u' rfs sc2-142bipn', 3),
     (u' commscope vhlp2-23-hw1a', 3),
     (u' huawei modelo', 3),
     (u' commscope vhlp3-15-hw1', 3),
     (u' huawey a07d12hs', 3),
     (u' andrew vhlpx4-11w-3wh/a', 3),
     (u' andrew vhlp4-15-hw1a', 2),
     (u' commscope vhlpx4-11w', 2),
     (u' andrew hpx10-71w-r1a', 2),
     (u' andrew hsx4-71-b3a/a', 2),
     (u' commscope/vhlp4-7w-cr4e', 2),
     (u' andrew/shp2-38-cr4', 2),
     (u' commscope vhlp3-23-hw1', 2),
     (u' commscope vhlp4-11w-hw1a', 2),
     (u' vhlp4-7w-cr4e', 2),
     (u' huawei - a07d12hs', 2),
     (u' andrew shpx3-11w-4wh', 2),
     (u' andr\xe9w vhlp4-7w-cr4e', 2),
     (u' commscope hsx4-71-b3a/a', 2),
     (u' andrew - vhlpx6-7w-3wh/b', 2),
     (u' commscopevhlpx6-7w-3wh/b', 2),
     (u' commscope vhlp3-11w-hw1', 2),
     (u' comscope shp3-23-cr4', 2),
     (u' commscope/vhlpx4-11w-3wh/a', 2),
     (u' andrew modelo ', 2),
     (u' commscope/vhlpx6-7w-3wh/b', 2),
     (u' andrew/ vhlpx4-11w-3wh/a', 2),
     (u' vhlpx4-15-3wh/c', 2),
     (u' andr\xe9s vhlpx3-23-3wh', 2),
     (u' commscope shpx2-15-2wh', 2),
     (u' andrew vhlp4-7w-cr4e', 2),
     (u' andrew vhlpx6-7w-3wh/b', 2),
     (u' andrew vhlpx4-7w-3wh/e', 2),
     (u' commscope vhlp1-38-hw1a', 2),
     (u' andrew/vhlp4-7w-cr4e', 2),
     (u' andrew - vhlpx4-7w-3wh/e', 2),
     (u' hsx4-71-b3a', 2),
     (u' rfs sc2-220-bipn', 2),
     (u' huawei ao7d18hs', 2),
     (u' commscope vhlp4-15-hw1a', 2),
     (u' andrew shpx3-23-2wh', 2),
     (u' andrew vhlp2-23-nc3', 2),
     (u' huawei ao7d12hs', 2),
     (u' ceragon ip20c-15-m14', 2),
     (u' andrew / vhlpx4-15-3wh/c', 2),
     (u' andrew shp2-38-cr4', 2),
     (u' huawei / a07d18hs', 2),
     (u' commscope shp3-11w-cr4', 2),
     (u' huawei/ a07d12hs', 2),
     (u' andrew/vhlpx4-11w-3wh/a', 2),
     (u' andrew-vhlpx3-15-3wh', 2),
     (u' commscope shp2-15-cr4', 2),
     (u' a07d12hls 7g', 2),
     (u' commscope shp3-23-cr4', 2),
     (u' huawei a07d12hs', 2),
     (u' huawei/a07d18hs', 2),
     (u' commscope shpx3-15-2wh', 2),
     (u' andrew vhpx8-7w-6gr', 2),
     (u' huawei a07d18hs', 2),
     (u' vhlpx4 - 11w - 3wh/a', 2),
     (u' andrew commscope shp3-23-cr4', 2),
     (u' commcope shpx2-38-2wh', 2),
     (u' andrew/shp3-11w-cr4', 2),
     (u' huahuei a07d12hs', 2),
     (u' commscope shpx2-38-2wh', 2),
     (u' andrew/vhlpx4-7w-3wh/e', 2),
     (u' andrew-vhlpx3-23-3wh', 2),
     (u' andrew vhlp6-11w-cr4c', 2),
     (u' commscope shp3 - 23 - cr4', 2),
     (u' commscope', 2),
     (u' commscope vhlpx4-7w-3wh/e', 2),
     (u' commscope shpx3-11w-4wh', 2),
     (u' andrew shp3-11w-cr4', 2),
     (u' huawei/a07d12hs', 2),
     (u' atel sc2-142bipn', 2),
     (u' huaweimodelo', 2),
     (u' huawei - modelo', 2),
     (u' huawei  a07d12hs', 2),
     (u' andrew vhlp2-15-hw1c', 2),
     (u' andrew shp3-23-cr4', 2),
     (u' andrew/vhlpx4-15-3wh/c', 2),
     (u' shpx3-15-2wh', 2),
     (u' andrew shpx3-15-2wh', 2),
     (u' commscope   shpx2-15-2wh', 2),
     (u' andrew vhlpx3-23-3wh', 2),
     (u' andrew vhlp3-23-hw1', 2),
     (u' huawei', 2),
     (u' andrew / vhlp4-7w-cr4e', 2),
     (u' shp3-11w-cr4', 2),
     (u' commscope vlpp2-23-nec3', 1)]




```python
len(fdist2)
```




    775




```python
Clean_Fab_AMW=[v for v,k in fdist2.items() if k>2]

#En caso de querer agregar elementos:
#Clean_CAMPO.append(u'ELEMENTO')

#En caso de querer eliminar elementos:
#Clean_CAMPO.remove(u'ELEMENTO')

Clean_Fab_AMW
```




    [u' commscope vhlpx4-11w-3wh/a',
     u' ',
     u' commscope vhlpx2-15-3wh/a',
     u' andrew vhlpx4-15-3wh/c',
     u' commscope vhlpx2-23-3wh/b',
     u' huahuei  a07d18hs',
     u' andrew shp3-15-cr4',
     u' andrew shp2-15-cr4',
     u' andrew',
     u' rfs sc2-142bipn',
     u' commscope vhlpx6-7w-3wh/b',
     u' commscope vhlp2-23-hw1a',
     u' huawei modelo',
     u' commscope vhlp3-15-hw1',
     u' huawey a07d12hs',
     u' andrew vhlpx4-11w-3wh/a']




```python
Cat_Fab_AMW['Clean']=1
for v in range(0,Cat_Fab_AMW.shape[0]):
    Cat_Fab_AMW.Clean[v]=process.extractOne(Cat_Fab_AMW.TipoElemento_value[v],
                                            Clean_Fab_AMW,
                                            scorer=fuzz.partial_ratio,
                                            score_cutoff=67)
    if Cat_Fab_AMW.Clean[v] is None:
        Cat_Fab_AMW.Clean[v]=Cat_Fab_AMW.TipoElemento_value[v]
    else:
        Cat_Fab_AMW.Clean[v]=Cat_Fab_AMW.Clean[v][0]

Cat_Fab_AMW.head(15)
```

    /opt/cloudera/parcels/Anaconda-5.3.1/lib/python2.7/site-packages/ipykernel_launcher.py:6: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']
    WARNING:root:Applied processor reduces input query to empty string, all comparisons will have score 0. [Query: ' ']





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TipoElemento_value</th>
      <th>Clean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>andrew / vhlpx4-11w</td>
      <td>andrew</td>
    </tr>
    <tr>
      <th>1</th>
      <td>andrew vhlpx4-7w-hw1</td>
      <td>andrew</td>
    </tr>
    <tr>
      <th>2</th>
      <td>andrew-vhlpx4-7w-3wh/e</td>
      <td>andrew</td>
    </tr>
    <tr>
      <th>3</th>
      <td>commscope sphx3-23-2wh</td>
      <td>commscope vhlpx2-23-3wh/b</td>
    </tr>
    <tr>
      <th>4</th>
      <td>andrew-vhlpx4-15-3wh/c</td>
      <td>andrew vhlpx4-15-3wh/c</td>
    </tr>
    <tr>
      <th>5</th>
      <td>commscope vhlp2-23-hw1a</td>
      <td>commscope vhlp2-23-hw1a</td>
    </tr>
    <tr>
      <th>6</th>
      <td>andrew vhlpx6-7w-3wh/b</td>
      <td>andrew</td>
    </tr>
    <tr>
      <th>7</th>
      <td>rfs sc2 w71bipn</td>
      <td>rfs sc2-142bipn</td>
    </tr>
    <tr>
      <th>8</th>
      <td>rfs sc2-w71bipn</td>
      <td>rfs sc2-142bipn</td>
    </tr>
    <tr>
      <th>9</th>
      <td>andrew-su2-71</td>
      <td>andrew</td>
    </tr>
    <tr>
      <th>10</th>
      <td>a07d12hs</td>
      <td>huawey a07d12hs</td>
    </tr>
    <tr>
      <th>11</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>12</th>
      <td>huawei - modelo</td>
      <td>huawei modelo</td>
    </tr>
    <tr>
      <th>13</th>
      <td>huawei-a07d12hs</td>
      <td>huawey a07d12hs</td>
    </tr>
    <tr>
      <th>14</th>
      <td>huawei/a07d18hs</td>
      <td>huahuei  a07d18hs</td>
    </tr>
  </tbody>
</table>
</div>



Mostramos los primeros registros del catálogo terminado:


```python
#Una vez listo el catálogo, podemos tirar la columna TipoElemento_value:
Cat_Fab_AMW.drop(columns=['TipoElemento_value'],inplace=True)
Cat_Fab_AMW.columns=['Atributos']
Cat_Fab_AMW.drop_duplicates(inplace=True)
Cat_Fab_AMW.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>andrew</td>
    </tr>
    <tr>
      <th>3</th>
      <td>commscope vhlpx2-23-3wh/b</td>
    </tr>
    <tr>
      <th>4</th>
      <td>andrew vhlpx4-15-3wh/c</td>
    </tr>
    <tr>
      <th>5</th>
      <td>commscope vhlp2-23-hw1a</td>
    </tr>
    <tr>
      <th>7</th>
      <td>rfs sc2-142bipn</td>
    </tr>
    <tr>
      <th>10</th>
      <td>huawey a07d12hs</td>
    </tr>
    <tr>
      <th>11</th>
      <td></td>
    </tr>
    <tr>
      <th>12</th>
      <td>huawei modelo</td>
    </tr>
    <tr>
      <th>14</th>
      <td>huahuei  a07d18hs</td>
    </tr>
    <tr>
      <th>17</th>
      <td>ceragon/ip20b-23-c28x</td>
    </tr>
  </tbody>
</table>
</div>



#### Hacemos más limpieza para poder eliminar basura.
Esta limpieza se sigue tomando del catálogo que se encuentra en Hive *regex_cat_cleanup*.


```python
dirt=['no visible','n/v','nv','ilegible','n/a','na','no legible',
      'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene','No visble','no visble',
      'No viaible','noisible','no aplica','n /v','finizar','no bisible','finisar','finsar','ftlfpbnl']

df.TipoElemento_value=df.TipoElemento_value.str.lower()
df.TipoElemento_value.replace(dirt,np.NaN,regex=True,inplace=True)
df.TipoElemento_value=df.TipoElemento_value.str.strip()
```

Crearemos una bandera para visualizar atributos de trazabilidad:


```python
df['Trazabilidad']='No Trazable'

df['Trazabilidad'].loc[((df.TipoElemento_Key_Clean=='serie') | 
                        (df.TipoElemento_Key_Clean=='activo')) & 
                       (df.TipoElemento_value is not np.NaN)
                      ]='Trazable'
```


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>102341</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1519779261882.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>1</th>
      <td>103636</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1521213704361.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>2</th>
      <td>104237</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1522270194317.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>3</th>
      <td>110042</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1529637323382.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>4</th>
      <td>111650</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1532990550837.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>5</th>
      <td>16089</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1450378225292.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>6</th>
      <td>22410</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1458087131765.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>7</th>
      <td>33027</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1465578436201.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>8</th>
      <td>35255</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1468292677107.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>9</th>
      <td>38728</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1470936860504.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>10</th>
      <td>52562</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1482293070624.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>11</th>
      <td>59755</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1487865751088.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>12</th>
      <td>64107</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1491083675568.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>13</th>
      <td>67500</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1494280047539.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>14</th>
      <td>68682</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1495379343016.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>15</th>
      <td>71416</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1497818810101.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>16</th>
      <td>8224</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1430941420856.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>17</th>
      <td>8262</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1430640438481.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>18</th>
      <td>8556</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1435009206281.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>19</th>
      <td>90591</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1508963966834.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>20</th>
      <td>94009</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1511461642926.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>21</th>
      <td>99584</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1516374128215.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>22</th>
      <td>102615</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1518816187625.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>23</th>
      <td>103895</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1520875644122.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>24</th>
      <td>104211</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1522246661003.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>25</th>
      <td>12508</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1445597218125.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>26</th>
      <td>23025</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1458431638791.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>27</th>
      <td>29303</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1462676722731.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>28</th>
      <td>38928</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1471635408455.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>29</th>
      <td>39387</td>
      <td>ATPMW</td>
      <td>groupHorizontalB-0</td>
      <td>groupHorizontalB-0</td>
      <td>True</td>
      <td>Barra de Tierra</td>
      <td>1471632209970.jpg (image/jpeg)</td>
      <td>barra de tierra</td>
      <td>No Trazable</td>
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
      <th>75558</th>
      <td>107362</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>201607</td>
      <td>None</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>75559</th>
      <td>89889</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>01071089</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75560</th>
      <td>108715</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102310bes10dc000281</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75561</th>
      <td>104063</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102113821n0f9001918</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75562</th>
      <td>105118</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102120762n0f9001934</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75563</th>
      <td>100957</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102310bes10f1000357</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75564</th>
      <td>103485</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102113821n0fa000100</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75565</th>
      <td>99263</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>mdp-400mb-1bb</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75566</th>
      <td>99263</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>nwa-063847-001</td>
      <td>None</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>75567</th>
      <td>99263</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>0000045107</td>
      <td>None</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>75568</th>
      <td>99263</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>201606</td>
      <td>None</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>75569</th>
      <td>91029</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>e275j02208</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75570</th>
      <td>104001</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102113821n0f8002736</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75571</th>
      <td>107358</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>bs-0278-0</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75572</th>
      <td>105277</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>mdp-400mb-1bb</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75573</th>
      <td>105277</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>nwa-063847-001</td>
      <td>None</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>75574</th>
      <td>105277</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>0000044413</td>
      <td>None</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>75575</th>
      <td>105277</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>201607</td>
      <td>None</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>75576</th>
      <td>97350</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>21021131746tb7906070</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75577</th>
      <td>96089</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>00887432</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75578</th>
      <td>91279</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>3g010100</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75579</th>
      <td>94657</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>2102352307p0d7000279</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75580</th>
      <td>115574</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>210235257110d8000162</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75581</th>
      <td>99522</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>mdp-400mb-1bb</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75582</th>
      <td>99522</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>nwa-063847-001</td>
      <td>None</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>75583</th>
      <td>99522</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>0000044997</td>
      <td>None</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>75584</th>
      <td>99522</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>None</td>
      <td>201606</td>
      <td>None</td>
      <td>No Trazable</td>
    </tr>
    <tr>
      <th>75585</th>
      <td>103636</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>21021138216tf8904900</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75586</th>
      <td>101386</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>bs-0278-0</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
    <tr>
      <th>75587</th>
      <td>94736</td>
      <td>ATPMW</td>
      <td>groupFloorB-0</td>
      <td>groupFloorB-0</td>
      <td>True</td>
      <td>Número de serie (escáner)</td>
      <td>21021138216tg3902365</td>
      <td>serie</td>
      <td>Trazable</td>
    </tr>
  </tbody>
</table>
<p>75588 rows × 9 columns</p>
</div>



### 4. Calidad de los datos

En el parseo de nuestra fuente de ODK se creo el campo de *exist* que corresponde a la limpieza de los atributos que se encuentran en el formulario, con esto eliminando missing values.

### 5. Catálogos

Del resultado de la exploración se proponen los catalogos:

- Modelo de la Antena MW
- Modelo
- Fabricante
- Fabricante / Modelo de la Antena MW

### 6. Preparación de los datos

Para la preparación de los datos se propondrán en el modelo lógico para hacer sentido a la información de la fuente.

### 7. Métricas KPI.

Se mostrarán los KPIs generados. Se considerará el conteo sobre el *Número de serie (manual)* más el *Número de serie (escáner)*.
Primero reemplazamos nulos por la palabra vacío.


```python
df.fillna('vacio',inplace=True)
```

#### Total de elementos


```python
Total_Elementos=spark.sql("SELECT count(*) AS Total FROM default.tx_stg_06_1_odk WHERE odk_no = '0012'").cache().toPandas()
Total_Elementos
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>45615</td>
    </tr>
  </tbody>
</table>
</div>



#### Total de elementos Trazables


```python
Total_Tr=pandasql.sqldf("SELECT count(tipoelemento_value) as Trazables FROM df WHERE tipoelemento_Key_Clean = 'serie' OR tipoelemento_Key_Clean = 'activo'", locals())
Total_Tr
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Trazables</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>15160</td>
    </tr>
  </tbody>
</table>
</div>



#### Elementos No Trazables Identificados (Barra de Tierra, Atizador , Barra de Tierra en Torre , Segunda Barra de Tierra en Torre , PTR)


```python
Total_Elementos_NOTr=pandasql.sqldf("SELECT count(tipoelemento_value) as No_Trazables FROM df WHERE tipoelemento_key IN ('Barra de Tierra','Atizador','Barra de Tierra en Torre','Segunda Barra de Tierra en Torre','PTR')", locals())
Total_Elementos_NOTr
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>No_Trazables</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>17687</td>
    </tr>
  </tbody>
</table>
</div>



#### Total de Elementos No Trazables


```python
Total_NOTr=Total_Elementos.iloc[0,0]-Total_Tr.iloc[0,0]
Total_NOTr
```




    30455



#### Total Elementos Trazables Únicos


```python
Total_Tr_Unic=pandasql.sqldf("SELECT count(distinct(tipoelemento_value)) as Trazables_Únicos FROM df WHERE tipoelemento_value <> 'vacio' AND TipoElemento_Key_Clean = 'serie' OR TipoElemento_Key_Clean = 'activo'", locals())
Total_Tr_Unic
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Trazables_Únicos</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10068</td>
    </tr>
  </tbody>
</table>
</div>



#### Total de elementos trazables duplicados


```python
Total_Tr_Dupli = Total_Tr.iloc[0,0] - Total_Tr_Unic.iloc[0,0]
Total_Tr_Dupli
```




    5092



#### Total Elementos Trazables Únicos Con Serie Con Activo


```python
Total_Tr_Unic_CS_CA=pandasql.sqldf("SELECT count(distinct(tipoelemento_value)) as Trazables_Únicos_CS_CA FROM df WHERE tipoelemento_value <> 'vacio' AND TipoElemento_Key_Clean IN ('serie','activo')", locals())
Total_Tr_Unic_CS_CA
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Trazables_Únicos_CS_CA</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10067</td>
    </tr>
  </tbody>
</table>
</div>



#### Total Elementos Trazables Únicos Con Serie Sin Activo


```python
Total_Tr_Unic_CS_SA=pandasql.sqldf("SELECT count(distinct(tipoelemento_value)) as Trazables_Únicos_CS_CA FROM df WHERE tipoelemento_value <> 'vacio' AND TipoElemento_Key_Clean IN ('serie')", locals())
Total_Tr_Unic_CS_SA
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Trazables_Únicos_CS_CA</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5684</td>
    </tr>
  </tbody>
</table>
</div>



#### Total Elementos Trazables Únicos Sin Serie Con Activo


```python
Total_Tr_Unic_SS_CA=pandasql.sqldf("SELECT count(distinct(tipoelemento_value)) as Trazables_Únicos_CS_CA FROM df WHERE tipoelemento_value <> 'vacio' AND TipoElemento_Key_Clean IN ('activo')", locals())
Total_Tr_Unic_SS_CA
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Trazables_Únicos_CS_CA</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4524</td>
    </tr>
  </tbody>
</table>
</div>



### Otros KPIS

En este apartado se muestra algunos de los hayazgos vistos en la exploración.


```python

KPIs=pd.DataFrame({'KPI':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados'],
                  'Resultado':[Total_Elementos_Fuente.iloc[0,0],Total_Tr.iloc[0,0],Total_NOTr.iloc[0,0],
                              Total_Tr_Unic.iloc[0,0],Total_Tr_Dupli]})

KPIs
```


```python

KPIs=pd.DataFrame({'KPI':['Total Elementos','Total Elementos Trazables',
                         'Total NO Trazables Identificados','Total NO Trazables','Total Trazables Unicos',
                         'Total Trazables Duplicados','Total Trazables Unicos Con Serie Con Activo',
                         'Total Trazables Unicos Con Serie Sin Activo','Total Trazables Unicos Sin Serie Con Activo'],
                  'Resultado':[Total_Elementos.iloc[0,0],Total_Tr.iloc[0,0],Total_Elementos_NOTr.iloc[0,0],
                               Total_NOTr,Total_Tr_Unic.iloc[0,0],Total_Tr_Dupli,
                               Total_Tr_Unic_CS_CA.iloc[0,0],Total_Tr_Unic_CS_SA.iloc[0,0],Total_Tr_Unic_SS_CA.iloc[0,0]
                              ]})

KPIs
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>45615</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total Elementos Trazables</td>
      <td>15160</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Total NO Trazables Identificados</td>
      <td>17687</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Total NO Trazables</td>
      <td>30455</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Total Trazables Unicos</td>
      <td>10068</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Total Trazables Duplicados</td>
      <td>5092</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Total Trazables Unicos Con Serie Con Activo</td>
      <td>10067</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Total Trazables Unicos Con Serie Sin Activo</td>
      <td>5684</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Total Trazables Unicos Sin Serie Con Activo</td>
      <td>4524</td>
    </tr>
  </tbody>
</table>
</div>



Se generan las tablas en Hive de la exploración ***default.eda_odk_12** y los resultados de los KPI's **default.kpi_odk_12**. 


```python
df_hive_eda = spark.createDataFrame(KPIs)
df_hive_eda.write.mode("overwrite").saveAsTable("default.eda_odk_12")

df_hive_kpis = spark.createDataFrame(KPIs)
df_hive_kpis.write.mode("overwrite").saveAsTable("default.kpi_odk_12")
```


```python

```
