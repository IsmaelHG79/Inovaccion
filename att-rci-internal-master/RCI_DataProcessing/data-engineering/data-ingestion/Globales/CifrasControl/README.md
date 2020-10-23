|                                        	|| |
|--------------------------------------	|-----------------------------------------	|-------------------------------------------------------------------------|
| ![EncabezadoAxity][img_axity]       || ![EncabezadoATT][img_att] |

# Cifras control

___

#### __1.__ Descripción general.
Para poder verificar el número de registros que se estan ingestando por fuente y fecha de archivo, se creó una tabla externa que contiene las siguientes columnas, el nombre de la tabla es: __tx_cifras_control__.

__1.1__ __Columnas de la tabla: tx_cifras_control__
|-- uuid: string (nullable = true)
|-- rowprocessed: long (nullable = true)
|-- datasetName: string (nullable = true)
|-- filedate: long (nullable = true)
|-- filename: string (nullable = true)
|-- sourceid: string (nullable = true)
|-- dateload: long (nullable = true)
|-- READ_COUNT: long (nullable = true)
|-- INSERT_COUNT: long (nullable = true)
|-- UPDATE_COUNT: long (nullable = true)
|-- DELETE_COUNT: long (nullable = true)

__1.1.1__ **Columna uuid:** Es un identificar único generado a partir de los campos definidos como llave en cada fuente, estas llaves pueden consultarse en el archivo "[Data Model Analysis_2019.11.21_v6](http://10.103.133.122/app/owncloud/f/14481184)".
<br>
__1.1.1__ **Columna rowprocessed:** Indica el número de registros procesados en cada ejecución .
<br>
__1.1.2__ **Columna datasetName:** Es el nombre de la fuente que se proceso.
<br>
__1.1.3__ **Columna filedate:** Es la fecha recuperada del nombre del archivo procesado.
<br>
__1.1.4__ **Columna filename:** Es el nombre del archivo que se proceso en la ejecución.
<br>
__1.1.5__ **Columna sourceid:** Es el nombre con el que se identifica la fuente ingestada.
<br>
__1.1.6__ **Columna dateload:** Es la fecha en que se realizó la carga de la fuente.
<br>
__1.1.7__ **Columna READ_COUNT:** Es el número de registros leidos de la fuente procesada.
<br>
__1.1.8__ **Columna INSERT_COUNT:** Es el número de registros insertados en la tabla.
<br>
__1.1.9__ **Columna UPDATE_COUNT:** Es el número de registros identificados con cambios, es decir, existe ya en la tabla y en el archivo que se esta ingestando viene nuevamente pero con una actualización de información.
<br>
__1.1.10__ **Columna DELETE_COUNT:** Es el número de registros identificados como eliminados, es decir, existen en la tabla, pero en el archivo que se esta ingestando ya no existe.
<br>

__1.2__ __Esquema de la tabla__
El esquema con el que se creó la tabla es el siguiente [tx_cifras_control.avsc](schema/tx_cifras_control.avsc), fue definido en base a las columnas propuestas para aportar la mayor información posible.

__1.2__ __Definición de la tabla__
La tabla que contiene las cifras control, fue definida como external, usando el esquema mencionado en el punto __1.2__, y la definición puede consultarse en la siguiente [Definición](sql/dll_tx_cifras_control.sql), esta definición se ejecuta en Hive.

__1.3__ __Ruta en HDFS con los archivos .avro__
La tabla external es creada con un location que existe en el hdfs, esta ruta es dónde se irán depositando los archivos .avro en cada ejecución y que contienen las cifras control generadas por el componente de [Spark](../SparkAxity/README.md), la ruta es: __/data/RCI/stg/hive/staging/cifras_control/data__.

__1.4__ __Ruta en HDFS del esquema__
De igual manera la tabla external utiliza el esquema mencionado en el punto __1.2__ y el esquema se encuentra en la siguiente ruta del hdfs __/data/RCI/stg/hive/staging/cifras_control/schemas/tx_cifras_control.avsc__.


[img_axity]: ../ArquitecturaFrameworkIngestion/images/axity.png "Axity"
[img_att]: ../ArquitecturaFrameworkIngestion/images/att.png "ATT"
