|                                        	|| |
|--------------------------------------	|-----------------------------------------	|-------------------------------------------------------------------------|
| ![EncabezadoAxity][img_axity]       || ![EncabezadoATT][img_att] |

# Componente: __Compactación__

___

#### __1.__ Descripción general del componente.
Dado que se cuentan con fuentes de periodicidad diaria que se deben ingestar el proceso de Spark genera un archivo por cada día de tamaño variable y que no cumple la cuota minima de 100 MB para almacenamiento en HDFS, un ejemplo es WLOG. Para poder garantizar el cumplimiento del lineamiento de almacenamiento se creo el componente de compactación el cuál se encarga de recorrer las diferentes particiones de una tabla y compactar la información.


<br>

#### __2.__ Ejecución del componente.
El shell está deployado en el servidor 10.150.25.146, en la siguiente ruta: __/home/raw_rci/attdlkrci/shells/rci_compactation_table.sh__ y debe ejecutarse con el usuario __raw_rci__. La forma de ejecutarlo es con la siguiente línea:

<br>

__./rci_compactation_table.sh Numero_de_fuente Tipo_de_particion__

<br>

Por ejemplo la siguiente línea __./rci_compactation_table.sh 1 m__ ejecutara el shell compactando las particiones mensuales de la tabla, __tx_finance_cip__.

si el segundo parámetro es:
* __m__ = Se compactan particiones mensuales
* __d__ = Se compactan particiones diarias

<br>

Si se quiere compactar un partición única es necesario ejecutar el comando de la siguiente manera:

__./rci_compactation_table.sh Numero_de_fuente Tipo_de_particion Particion__

<br>

Por ejemplo la siguiente línea __./rci_compactation_table.sh 1 m 2019,8__ ejecutara el shell compactando la partición de Agosto del 2019 de la tabla, __tx_finance_cip__.

Para compactar la partición del 1 de Julio del 2019 debemos invocar el componente de la siguiente manera __./rci_compactation_table.sh 1 d 2019,7,1__ ejecutara el shell compactando la partición de Agosto del 2019 de la tabla, __tx_finance_cip__.

Es importante mencionar que si el día del mes es solo de un dígito, el componente debe invocarse solo con el dígito, no anteponer un 0. Lo mismo sucede con el dígito de la partición del día.

[img_axity]: ../ArquitecturaFrameworkIngestion/images/axity.png "Axity"
[img_att]: ../ArquitecturaFrameworkIngestion/images/att.png "ATT"
