|                                        	|| |
|--------------------------------------	|-----------------------------------------	|-------------------------------------------------------------------------|
| ![EncabezadoAxity][img_axity]       || ![EncabezadoATT][img_att] |

# Componente: __Adquisición ODK'S__

___

#### __1.__ Descripción general del componente.

Este orquestador es un workflow diseñado en el sistema de programación de flujo Apache Oozie. Este flujo es encargado de correr scripts de Spark individuales para cada ODK, estos scripts ejecutan funciones de busqueda unicas por cada ODK buscando los diferentes tipos de elemento de red.

Cada script ejecutado es para un ODK, incluyendo en este los subtipos del mismo. Cada script escribe en la base de datos rci_network_db una tabla con la siguiente nomenclatura "tx_stg_tabla_columnar_odk_(número de ODK)".

<br>

#### __2.__ Ejecución del componente.
El flujo está diseñado en la herramienta Oozie en el servidor 10.150.25.146, en la siguiente ruta:

Cada script de spark es ejecutado en serie, es decir cuando acabe de ejecutar uno, inicia el otro, y aunque falle uno se pasa a la siguiente ejecución sin cancelar el flujo.

<br>


#### __3.__ Operaciones realizadas por el componente para cada script.
__1.__ Limpieza: Se hace una limpieza a los campos de la tabla del ODK eliminando caracteres especiales y signos que no sirven para la adquisición y busqueda del tipo de elemento.

__2.__ Obtener key y value: Se hacen dos columnas nuevas haciendo un split por el carácter (':') al campo "ma" para obtener el key y el value que nos va a ayudar a obtener las propiedas del elemento.

__3.__ Agrupación: Se hace un agrupación por el campo "clave_form","id_form","form_element" que es el grupo que describe el tipo de elemento que se esta tratando.

__4.__ Busqueda: Se ejecuta una función de busqueda derivada de un analisis previo al tipo de ODK para encontrar los tipos de elementos de red para cada "form_element".

__5.__ Explode y pivot: Se hace un explode de los campos, se vuelve a agrupar y se hace un pivoteo sobre la columna "key", concatenando como valores la columna "value".

__6.__ homologación: Se hace una limpieza final y homologación de campos.

__7.__ Escritura: Se hace una escritura de la tabla columnar con la siguiente nomenclatura "tx_stg_tabla_columnar_odk_(número de ODK)".

|Entrada:|Salida:|
|-	|-|
|Tabla del ODK|Tabla columnar del ODK en hive|



[img_axity]: images/axity.png "Axity"
[img_att]: images/att.png "ATT"
