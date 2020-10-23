|                                        	|| |
|--------------------------------------	|-----------------------------------------	|-------------------------------------------------------------------------|
| ![EncabezadoAxity][img_axity]       || ![EncabezadoATT][img_att] |

# Arquitectura general del Framework de ingestión: __Repositorio Central de Información.__

___

__1.__ Descripción general del requerimiento
AT&T México busca tener una visión conciliada del Inventario de Red, que contenga información fiel de todos y cada uno de los elementos que conforman la Red de Telecomunicaciones, disgregados en los múltiples dominios (TX, RAN, CORE) y fases del ciclo de vida (Plan, Adquisición, Instalación, Decomiso, etc) por lo que AT&T, ha adjudicado dos RFPs a Axity, uno para Gestión de datos y el otro para el desarrollo de App Móvil.


__2.__ Solución al requerimiento
Axity tiene el objetivo de realizar la integración de la información en el Repositorio Central de Inventario (RCI), que incluye el alcance como el reforzamiento en el desarrollo, integración y la ejecución sobre la estructura de los modelos de datos, la integración de las fuentes de información, desarrollo de queries, store procedures y scripts de automatización, esto para el proyecto Data Management


__3.__ Diagrama de la arquitectura propuesta
<br>
![FrameworkIngestion][img_framework_ingestion]

<br><br>
__3.1__ Descripción de los componentes que integran la solución

__3.1.1__ Rutas de FTP
Servidor FTP en el cuál serán depositadas las fuentes a ingestar por parte de AT&T, en diferentes rutas dependiendo del tipo de fuente. Las rutas del FTP de donde se leerán los archivos a ingestar se pueden encontrar en el documento "[ATT-DataLake-Security Level Strategy v1.8](http://10.103.133.122/app/owncloud/f/14481184)", este archivo concentra los diferentes servidores, carpetas y sub carpetas que nos proporcionó ATT en la fase de análisis.


|Entrada:|Salida:|
|-	|-|
|Fuentes a ingestar|No genera salida|

<br>

__3.1.2__ Flujo maestro de Nifi
Es el flujo de datos principal que tiene como objetivo leer las fuentes depositadas en las diferentes rutas del servidor Ftp, el proceso tomará las fuentes una a una (archivos de Excel con extensión xlsx) y procesará las hojas especificadas en la columna Sheet/Path del documento de análisis “[Data Model Analisys_2019.11.05_v5](http://10.103.133.122/app/owncloud/f/14481184)”, una vez leída la información del sheet el procesador implementado con Nifi infiere el esquema definido en la hoja de Excel a procesar, generando el archivo final con el esquema.
El componente fue desarrollado de forma genérica para que todas las fuentes fueran procesadas con el mismo flujo, se utilizaron componentes propios de Nifi y se desarrolló un procesador genérico para poder leer las diferentes estructuras que se envían.
Este componente es generado en un archivo empaquetado con extensión NAR (Nifi Application Archive) y debe ser deployado en todos los nodos de Nifi. A continuación, se muestra en la Figura 1 la estructura general de un archivo con extensión NAR.

|Entrada:|Salida:|
|-	|-|
|Fuentes a ingestar (archivos en formato Excel)|Archivo con el esquema inferido de la hoja de Excel (Archivo con extensión avsc).|

<br>

||![EstructuraNar][img_estructura_nar]|
|-|-|
||__Figura 1.__ Estructura general de un archivo con extensión NAR.|

<br>

__3.1.3__ Flujo maestro de Kite
Este componente se encargará de generar el dataset correspondiente a la fuente a ingestar por medio del framework Kite tomando como parámetros la ruta donde se estará creando la estructura y el esquema generado por el componente de Nifi, la tabla será particionada por el año, mes y día de la ejecución.
La estructura de carpetas que contiene este componente se muestra en la Figura 2.


||![EstructuraCarpetas][img_estructura_carpetas]|
|-|-|
||__Figura 2.__ Estructura del componente de kite|


* __config:__ Contiene los archivos de configuración donde se especifican las rutas de los esquemas a leer y la configuración de la partición a crear.
logs: Contiene el log de ejecuciones del componente
* __schemas:__ Contiene los esquemas para realizar las pruebas en ambiente local, esta carpeta no interfiere para ejecutar el flujo productivo.
* __shell:__ Contiene el script principal “rci_ingesta_generacion_avro.sh” que ejecuta el flujo de kite, la forma de ejecutar es la siguiente:
rci_ingesta_generacion_avro.sh numero_flujo
* __numero_flujo:__ Es un numero entre 1 y N donde los valores corresponden a la columna "Parámetro en shell" del archivo [AX_IM_FrameworkIngestion_CommandExecutionV2.xls](http://10.103.133.122/app/owncloud/f/14481184)

<br>

|Entrada:|Salida:|
|-	|-|
|Archivo con el esquema generado por el flujo de Nifi (archivo avsc).|Esquema de la fuente procesada en el HDFS de Hadoop.|

<br>

Para mas detalle del componente consultar la documentación de este [componente de kite](../attdlkrci/readme.md)

<br>

__3.1.4__ Componente Spark
Se encargará de leer la información de la fuente procesada y de cargarla al dataset creada por el flujo de kite leyendo la partición definida en el archivo /config/json_partition_date.json, este componente controlará la incrementalidad de los deltas procesados. Para mas información revisar el documento del componente [Spark](../SparkAxity/README.md).


[img_axity]: images/axity.png "Axity"
[img_att]: images/att.png "ATT"
[img_framework_ingestion]: images/framework_ingestion.png "Ingesta de datos"
[img_estructura_nar]: images/estructura_nar.png "Estructura general de un archivo con extensión NAR."
[img_estructura_carpetas]: images/estructura_carpetas.png "Estructura del componente de kite"
