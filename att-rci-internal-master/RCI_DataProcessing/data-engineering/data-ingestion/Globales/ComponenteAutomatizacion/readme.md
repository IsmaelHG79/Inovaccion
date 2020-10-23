|                                        	|| |
|--------------------------------------	|-----------------------------------------	|-------------------------------------------------------------------------|
| ![EncabezadoAxity][img_axity]       || ![EncabezadoATT][img_att] |

# Componente: __Automatización de ingesta__

___

#### __1.__ Descripción general del componente.
Para ejecutar el flujo completo de la ingesta de información por fuente, se creo el componente de automatización, el cual integra las diferentes herramientas utilizadas por el Framework de ingestión (Apache Nifi, Kite y Spark) para la ejecución automática de la ingesta. En primera instancia el proceso validará si existe información en la ruta definida para la fuente a ingestar, en caso de no existir información el componente generará una alerta por correo electrónico indicando que no hay insumos a procesar. En caso de que exista información el proceso ejecutará los siguientes pasos:
* Ejecutar el flujo de Nifi (play al process group)
* Esperar N segundos para que el flujo de Nifi consuma la información
* Obtener el estatus general del componente para leer el número de archivos que entran al procesador
* Esperar N minutos para que el procesador termine de procesar los archivos
* Comparar el número de archivos de salida contra el número de archivos de entrada.
* Una vez que el conteo coincide el componente apagará el procesador de Nifi.
* El componente invocará al Framework de ingestion para realizar la creación o actualización de la tabla, el registro del esquema e inserción de los datos.


<br>

#### __2.__ Ejecución del componente.
El shell está deployado en el servidor 10.150.25.146, en la siguiente ruta: __/home/raw_rci/attdlkrci/shells__ y debe ejecutarse con el usuario __raw_rci__. La forma de ejecutarlo es con la siguiente línea:

<br>

__./rci_execute_ingestion_flow.sh Numero_de_fuente Frecuencia_ejecucion__

Donde:
__Numero_de_fuente:__ Es el id de la fuente definida en la tabla de configuración (rci_metadata_db.tx_config)"
__Frecuencia_ejecucion:__	Indica la frecuencia con la que se ingestara la fuente, d=diaria, s=semanal, m=mensual"

Por ejemplo la siguiente línea __./rci_execute_ingestion_flow.sh 1 m__ iniciará la ejecución del flujo de ingestión de la fuente, __tx_finance_cip__ con periodicidad mensual.


#### __3.__ Alertas:
Es el componente encargado de notificar vía correo electrónico si el proceso se ejecutará o no, dependiendo de los insumos encontrados en la ruta configurada en la fuente.

[img_axity]: ../ArquitecturaFrameworkIngestion/images/axity.png "Axity"
[img_att]: ../ArquitecturaFrameworkIngestion/images/att.png "ATT"
