![EncabezadoAxity][imgEncabezado]

# Documentación Data Ingestion para la fuente ATT **TELLABS**

## Descripción del `FTP`  

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

## Descripción de la fuentes de datos
- **Descripción**
  [TELLABS Finanzas EDA](../../../../RCI_DataAnalysis/eda/TELLABS/EDA_Tellabs.md#descripci%C3%B3n)

- **Diccionario de Datos**
     La siguiente tabla muestra el resultado de ejecutar el siguiente comando:

    `describe formatted rci_network_db.tx_tellabs;`

  | Id 	| Nombre de Columna  	| Tipo de Dato 	| Comentario                                                	|
  |----	|--------------------	|--------------	|-----------------------------------------------------------	|
  | 1  	| out1_in0           	| string       	| Type inferred from '1'                                    	|
  | 2  	| id                 	| string       	| Type inferred from '1'                                    	|
  | 3  	| name               	| string       	| Type inferred from 'MSO I 6340 REVOLUCION'                	|
  | 4  	| type               	| string       	| Type inferred from '6340 Switch'                          	|
  | 5  	| locationid         	| string       	| Type inferred from '100'                                  	|
  | 6  	| subtype            	| string       	| Type inferred from 'FP 3.3'                               	|
  | 7  	| network            	| string       	| Type inferred from 'null'                                 	|
  | 8  	| site               	| string       	| Type inferred from 'null'                                 	|
  | 9  	| role               	| string       	| Type inferred from 'null'                                 	|
  | 10 	| customer           	| string       	| Type inferred from 'NEXTEL MSO I'                         	|
  | 11 	| state              	| string       	| Type inferred from 'In Use'                               	|
  | 12 	| area               	| string       	| Type inferred from 'NEXTEL-MEXICO'                        	|
  | 13 	| ospfarea           	| string       	| Type inferred from 'null'                                 	|
  | 14 	| routerid           	| string       	| Type inferred from 'null'                                 	|
  | 15 	| mgmtip             	| string       	| Type inferred from 'null'                                 	|
  | 16 	| testloopbackaddr   	| string       	| Type inferred from 'null'                                 	|
  | 17 	| label              	| string       	| Type inferred from 'null'                                 	|
  | 18 	| alias_nsap_sid_tid 	| string       	| Type inferred from '49001000a0822e0aed01'                 	|
  | 19 	| commrole           	| string       	| Type inferred from 'null'                                 	|
  | 20 	| getcommunity       	| string       	| Type inferred from 'null'                                 	|
  | 21 	| setcommunity       	| string       	| Type inferred from 'null'                                 	|  

    Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestión.

  | Id 	| Nombre de Columna  	| Tipo de Dato 	| Comentario                                                	|
  |----	|--------------------	|--------------	|-----------------------------------------------------------	|
  | 22 	| filedate           	| bigint       	| Type inferred from '20191019'                             	|
  | 23 	| filename           	| string       	| Type inferred from 'ATT_Naranja_Nodos_191019-TELLABS.csv' 	|
  | 24 	| hash_id            	| string       	| Type inferred from 'null'                                 	|
  | 25 	| sourceid           	| string       	| Type inferred from 'TELLABS'                              	|
  | 26 	| registry_state     	| string       	| Type inferred from 'null'                                 	|
  | 27 	| datasetname        	| string       	| Type inferred from 'tellabs'                              	|
  | 28 	| timestamp          	| bigint       	| Type inferred from '20191230'                             	|
  | 29 	| transaction_status 	| string       	| Type inferred from 'null'                                 	|


- **Particiones**

  A continuación se presentan las particiones creadas de la tabla **tx_tellabs**.

  Sentencia: ```show partitions rci_network_db.tx_tellabs;```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Location                                                                      	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------------------------------------------------------------------	|
  | 2019 	| 10     	| 19   	| 810     	| 1      	| 276.42KB 	| AVRO   	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/tellabs/year=2019/month=10/day=19  	|

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:
  ```
  select * from rci_metadata_db.tx_rci_executions
  where table_name = 'tx_tellabs';
  ```

  | id_execution | table_name | dateload | avro_name | start_execution | end_execution | status | attempts |
  |--------------|------------|----------|---------------------------------------------------------|---------------------|---------------------|--------|----------|
  | 1 | tx_tellabs | 20191231 | /data/RCI/raw/tellabs/data/20191019_ATT_Naranja_Nodos_191019-TELLABS.avro | 2019-12-31 13:22:18 | 2019-12-31 13:23:56 | 1 | 0 |

- **Cifras de control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_tellabs'
  and dateload = 20191231
  order by filedate asc;
  ```

  | uuid | rowprocessed | datasetname | filedate | filename | sourceid | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|-------------|----------|-----------------------|----------------|----------|------------|--------------|--------------|--------------|
  | ec0feb9a-59a4-4091-83a8-dda2ea54db6e | 810 | tx_tellabs | 20191019 | ATT_Naranja_Nodos_191019-TELLABS.csv	 | TELLABS | 20191231 | 810 | 810 | 0 | 0 |

  ## Componentes del procesos de ingestion

  1. **Ingestion y Serialización via NiFi**

    ![TELLABS NiFi Vista General][img1]

    Pipeline Principal __Flujo Principal__

    ![TELLABS NiFi Vista Subproceso][img2]

    Pipeline Subproceso __Flujo de Subproceso__

    ![TELLABS NiFi Vista Lectura de Archivos][img3]

    Pipeline Lectura de Archivos __Lectura de Archivos__

    ![TELLABS NiFi Vista Procesamiento][img4]

    Pipeline Lectura de Archivos __Procesamiento de Archivos__

  2. __Reglas de Estandarización del Esquema `Kite`__

    Las siguientes reglas se aplicarón para estandarizar el esquema:

    - Remover Caracteres especiales en el header.
    - Reemplazo de caracter _ por " " en el nombre del archivo.

  3. __Framework de Ingestión Automatizado__

    - Especificar parámetros del proceso kite:

      | Parámetro | Valor | Descripción|
      | ---------- | ---------- | ---------- |
      | parametro_01   | 88   | Valor de correspondiente al flujo TELLABS   |

      Sentencia kite:

      ```
      ./rci_ingesta_generacion_avro.sh {parametro_01}
      ```

      Ejemplo:

      ```
      ./rci_ingesta_generacion_avro.sh 88
      ```

## Referencias al Framework de Ingestion

- [Framework de Ingestion](../Globales/ArquitecturaFrameworkIngestion/readme.md)

## Código Fuente Local

- [Codigo NiFi - NFR](NFR/)

## Código Fuente Globales

- [Codigo NiFi](../Globales/NIFICustomProcessorXLSX)
- [Codigo Spark](../Globales/SparkAxity)
- [Codigo Kite](../Globales/attdlkrci/readme.md)

[img1]: images/TELLABS-nifi-00.png "TELLABS NiFi vista general"
[img2]: images/TELLABS-nifi-01.png "TELLABS NiFi vista subproceso"
[img3]: images/TELLABS-nifi-02.png "TELLABS NiFi Lectura de Archivos"
[img4]: images/TELLABS-nifi-03.png "TELLABS NiFi Lectura de Archivos"


[imgEncabezado]:../Globales/ArquitecturaFrameworkIngestion/images/encabezado.png ""
