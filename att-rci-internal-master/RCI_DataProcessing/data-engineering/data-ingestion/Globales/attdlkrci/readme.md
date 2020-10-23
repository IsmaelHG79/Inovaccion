|                                        	|| |
|--------------------------------------	|-----------------------------------------	|-------------------------------------------------------------------------|
| ![EncabezadoAxity][img_axity]       || ![EncabezadoATT][img_att] |

# Componente: __Shell-Kite__

___

#### __1.__ Descripción general del componente.
Este shell tiene la función de crear una dataset (tabla) y/o actualizar su definición en base a un esquema inferido de una fuente procesada (primera fase de ejecución del "[Framework de Ingestion](../ArquitecturaFrameworkIngestion/readme.md)"). El componente identifica el tipo de operación a realizar (create o update) en base al esquema que se está procesando y comparandolo con el historial de esquemas ya procesados por este componente. El registro del esquema lo realiza Apache kite en el metastore de hive, y es hive quien hace uso de esos esquemas para poder consultar la información de las fuentes ingestadas.


<br>

#### __2.__ Ejecución del componente.
El shell está deployado en el servidor 10.150.25.146, en la siguiente ruta: __/home/raw_rci/attdlkrci/shells__ y debe ejecutarse con el usuario __raw_rci__. La forma de ejecutarlo es con la siguiente línea:

<br>

__./rci_ingesta_generacion_avro.sh Numero_de_fuente__

<br>

Por ejemplo la siguiente línea __./rci_ingesta_generacion_avro.sh 1__ ejecutara el shell ingestando la fuente identificada con el id número 1, __tx_finance_cip__.

<br>

<<<<<<< HEAD
<<<<<<< HEAD
Para identificar el número de la fuente a ingestar consultar el documento "[AX_IM_FrameworkIngestion_CommandExecutionV2](http://10.103.133.122/app/owncloud/f/14481184)" que contiene el listado de fuentes a ingestar y el valor de los parámetros necesarios para ejecutar el [componente de Spark](../SparkAxity/README.md).
=======
Para identificar el número de la fuente a ingestar consultar el documento "[AX_IM_FrameworkIngestion_CommandExecutionV2](http://10.103.133.122/app/owncloud/f/14480776)" que contiene el listado de fuentes a ingestar y el valor de los parámetros necesarios para ejecutar el [componente de Spark](../SparkAxity/README.md).
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596
=======
Para identificar el número de la fuente a ingestar consultar la tabla __rci_network_db.tx_rci_config__ en la columna __id_source__ que contiene el listado de fuentes a ingestar y el valor de los parámetros necesarios para ejecutar el [componente de Spark](../SparkAxity/README.md).
>>>>>>> f17ccfc48c11b46af8c37c2b5c513a6316537378

<br>

#### __3.__ Archivo de propiedades _pro_rci_ingesta_generacion_avro.properties_
Para la correcta ejecución del componente shell-kite se cuenta con un archivo de propiedades, donde se especifican las rutas y parámetros para poder registrar el esquema en el metastore y crear la tabla. Este archivo se encuentra en la carpeta __/home/raw_rci/attdlkrci/config__

__3.1__ Propiedades del archivo de configuración.
En las siguientes descripciones se usa la palabra __"NombreTabla"__ para describir el nombre de las varaibles, sin embargo el valor real es el nombre de la fuente a configurar, por ejemplo:
* __esquema_tablas_rci__ Esquema donde se almacenan las tablas ingestadas.
* __esquema_tablas_config__ Esquema donde se almacenan las tablas de configuración del componente.
* __tabla_ejecuciones__ Tabla donde se registran las ejecuciones de carga.
* __tabla_config__ Tabla donde se insertan las configuraciones de las fuentes a ingestar.
* __tabla_cifras__ Tabla donde se almacenan las cifras de control.
* __path_cifras__ Ruta en el HDFS donde se almacenan los archivos avro de las cifras de control.
* __tabla_processors__ Tabla que contiene la configuración de los procesadores para poder ejecutar la automatización.


#### __4.__ Operaciones realizadas por el componente.
__1.__ create: La primera vez que se ejecuta el componente para ingestar una fuente, siempre realiza la operación de create, a continuación se describen los pasos.


__1.1__ El shell es ejecutado y lee los parámetros del archivo de configuración, lee la propiedad NombreTabla_avsc para obtener la ruta del esquema a procesar.

__1.2__ Se compara el esquema a procesar contra el esquema ubicado en la ruta que tiene la variable __schemas_bck_NombreTabla__ y que coincide con el nombre de la fuente a ingestar, por ejemplo: __tx_finance_cip.avsc__. La primera vez no existe ningún esquema en la carpeta de procesados, por lo cual al hacer la comparación regresa vacio y el shell lo identifica como __sin cambios__ por lo cual el comando será __create__.

__1.3__ Se ejecuta el comando __kite-dataset create dataset:hive:default/table_NombreTabla --location location_NombreTabla --schema NombreTabla_avsc --partition-by json_partition_config__

__2.__ update: En la segunda ejecución del componente y previamente la ejecución correcta la primera vez, el componente ya encontrará un esquema procesado en la ruta definida por la variable __schemas_bck_NombreTabla__ y realizará la comparación entre el esquema a procesar y el esquema procesado, en este caso si son diferentes el shell ejecutara el siguiente comando: __kite-dataset update dataset:hive:default/table_NombreTabla --schema NombreTabla_avsc__


|Entrada:|Salida:|
|-	|-|
|Esquema de la fuente a ingestar|Tabla en hive|


#### __5.__ Diagrama de la arquitectura automatizada
<br>

![FrameworkIngestion][img_framework_ingestion_automatizada]

<br><br>
__5.1__ Descripción de los componentes que integran la solución automatizada.

__5.1.1__ __Shell__: rci_ingesta_generacion_avro.sh
Componente principal que es invocado con un id numérico asociado a una fuente única.

__5.1.2__ __Archivo .properties__: pro_rci_ingesta_generacion_avro.properties
Archivo que contiene las propiedades generales de ejecución como son: lista de correo para notificar las cifras de control, work space de oozie para el notificador, esquema donde se encuentran las tablas con la información, esquema para las tablas de configuración y nombre de las tablas de configuración y cifras de control.

__5.1.3__ __Tabla__: rci_metadata_db.tx_rci_config
Tabla Impala-Kudu que contiene los parámetros de configuración para cada fuente a ingestar.

|Campo|Tipo dato|Comentario|
|-	|-|-|
|id_source			|int			|'Identificador numerico de la fuente.'|
|table_name			|string			|'Nombre de la tabla asociada a la ejecución'|
|status				|int			|'Bandera para controlar el cambio de versiones, 1=Activo, 0=Inactivo.'|
|date_insert		|int			|'Fecha en la que se registro el cambio.'|
|path_avsc			|string			|'Ruta donde se encontrara el esquema a procesar en modo cliente.'|
|path_hdfs			|string			|'Ruta del HDFS donde se depositaran los datos insertados en la tabla.'|
|path_backup		|string			|'Ruta del file system donde se depositaran los esquemas procesados.'|
|ban_process_all	|int			|'Bandera para indicar si el procesamiento es masivo o archivo por archivo, 0=Archivo, 1=Mascivo.'|
|path_avsc_all		|string			|'Ruta donde se encuentran todos los esquemas a procesar, se lee cuando la ban_process_all es igual a 1.'|
|path_avro_all		|string			|'Ruta donde se encuentran todos los avros a procesar, se lee cuando la ban_process_all es igual a 1.'|
|schema_database	|string			|'Esquema de la base de datos en donde se creara la tabla.'|
|json_partition		|string			|'Ruta en donde estará el json que definira la particion de la tabla.'|
|command_kite		|string			|'Comando que ejecutara el shell de kite para crear la tabla.'|
|path_data_spark	|string			|'Ruta de donde el componente de spark leera los archivos avros (datos) a ingestar.'|
|key_columns		|string			|'Columnas para definir la llave (hash_id) que generara el componente de spark.'|
|path_avro_cifras	|string			|'Ruta de donde leeremos el archivo avro generado por Nifi que contiene las cifras de control.'|
|path_write_cifras	|string			|'Ruta en donde se escribiran las cifras de conttrol homologadas.'|
|type_load			|string			|'Indica el tipo de carga que se realizara, full=carga todo, nofull=carga incremental. nofull, puede ser cualquier otra palabra.'|
|number_partitions	|int			|'Valor que indica el numero de particiones que se creara para la comprension.'|
|command_spark		|string			|'Comando para invocar el componente de Spark.'|

__5.1.4__ __Tabla__: rci_metadata_db.tx_rci_executions
Tabla Impala-Kudu que contiene las ejecuciones creadas por el orquestador y que son necesarias para ingestar las diferentes fuentes.

|Campo|Tipo dato|Comentario|
|-	|-|-|
|id_execution		|int			|'Identificador de la ejecución'|
|table_name			|string			|'Nombre de la tabla asociada a la ejecución'|
|dateload			|int			|'Fecha de la ejecución'|
|avro_name			|string			|'Nombre del avro procesado'|
|start_execution	|timestamp		|'Hora de inicio de la ejecución'|
|end_execution		|timestamp		|'Hora de fin de la ejecución'|
|status				|int			|'Estatus de la ejecucion, 0=Pendiente, 1=Ejecutada'|
|command			|string			|'Comando de Spark con el que fue creada la ejecución'|
|id_application		|string			|'Id generado por yarn para la ejecución de Spark'|
|attempts			|int			|'Número de intentos para realizar la ejecución'|

__5.1.5__ __Generador de ejecuciones__:
Código encargado de leer la ruta configurada en la tabla rci_metadata_db.tx_rci_config, columna: path_avro_all y obtener el número de archivos depositados en esa ruta, con esa lista de archivos se insertan los N registros (ejecuciones) en la tabla rci_metadata_db.tx_rci_executions, de inicio, todas las ejecuciones se generan con status 0 (Pendiente), y con hora de inicio y fin en NULL.
Los campos command, id_application permaneceran con el valor vacio en el todo el ciclo de vida de la ejecución.

__5.1.6__ __Orquestador de ejecuciones__:
Código encargado de leer la tabla rci_metadata_db.tx_rci_executions filtrando por el nombre de la tabla y fecha de ejecución para obtener el número de ejecuciones a lanzar en el proceso de ingesta. Para obtener la primer ejecución se consulta por el mínimo número de ejecución que tenga el estatus 0 y se almacena el valor en un contador, que será encargado de ir controlando el número de ejecución a procesar, posteriormente se actualiza la fecha de inicio de ejecución y se procesa el primer esquema de la lista, una vez procesado el esquema se invoca el componente de spark para realizar la inserción de los datos en la tabla.
Se espera a que se finalice con exito la operación de carga, para poder mover el avro de cifras de control actualizado por el componente de Spark a la ruta configurada en la propiedad path_cifras del archivo properties, eliminar el archivo avro procesado (información insertada en la tabla de hive), actualizar el la hora de fin de la ejecución y establecer en 1 el valor del campo estatus de la tabla de ejecuciones para indicar que la ejecución fue terminada correctamente. Por último se incrementa en 1 el valor del contador de ejecuciones para seguir procesando el siguiente registro.
En caso de que la ejecución en curso finalice con error, la fecha de fin de ejecución no se actualiza (se queda con valor NULL), la columna que se actualiza es attempts (attempts + 1), para indicar que en hubo en error en el procesamiento, y la ejecución terminará para que el operador revise la causa de la falla.
Una vez identificada y corregida la causa que originó el error en la ejecuión, el operador tendrá que volver a invocar el componente "Framework de ingestion" con el mismo parámetro de la fuente, el orquestador de ejecuciones identificará el número de ejecución en la que se abortó el proceso en el intento anterior y procederá a lanzarla.
Se validará el número de intentos de la ejecución para decidir si se debe procesar el esquema o no. Cada ejecución va referenciada con un esquema_tabla-avro_de_datos, esto para garantizar la integridad del esquema y la información.
Al finalizar de procesar todas las ejecuciones se procedera a obtener las cifras de control generadas para enviarlas por correo electrónico y esa será la notificación de fin de carga de la fuente.

__5.1.7__ __Notificador de cifras de control__:
Es el componente encargado de consultar la tabla rci_network_db.tx_cifras_control para filtar la información por nombre de la tabla y fecha de carga, y obtener las cifras de control generadas, posteriormente son enviadas por correo electrónico.

[img_axity]: images/axity.png "Axity"
[img_att]: images/att.png "ATT"
[img_framework_ingestion_automatizada]: images/framework-ingestion_automatization.png "Ingesta de datos automatizada"
