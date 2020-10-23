![EncabezadoAxity][imgEncabezado]


# Documentación Data Ingestion para la fuente ATT **ALCATEL**

Para esta fuente se documentan diferentes flujos de una sola fuente, esto debido a que existen diferentes archivos generados los cuales son los siguientes:

* [Elementos T7 Naranja](#elementost7_naranja_alu)
* [Elementos T7 Rojo](#elementost7_rojo_alu)

## <a name="elementost7_naranja_alu"></a> Elementos T7 Naranja

## Descripción del `FTP`  

  El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

  - El servidor y la ruta en donde se encontrarán los archivos a ingestar.

  - La ruta en donde se coloca el respaldo de los archivos ingestados.

  - El directorio de HDFS en donde se colocan los datos ingestados.

## Descripción de la fuentes de datos
- **Descripción**
  [Elementos T7 Naranja EDA](../../../../RCI_DataAnalysis/eda/Alcatel/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Alcatel/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_elementost7_naranja_alu;```

  | Id 	| Nombre de Columna  	| Tipo de Dato 	| Comentario                                                              	|
  |----	|--------------------	|--------------	|-------------------------------------------------------------------------	|
  | 1  	| emlim              	| string       	| Type inferred from '160'                                                	|
  | 2  	| userlabel          	| string       	| Type inferred from 'ML5107-ML5259_AWY_101_2_36_46'                      	|
  | 3  	| type               	| string       	| Type inferred from 'ULS'                                                	|
  | 4  	| version            	| string       	| Type inferred from '2'                                                  	|
  | 5  	| address            	| string       	| Type inferred from '101.2.36.46:161'                                    	|
  | 6  	| interface          	| string       	| Type inferred from 'alcatel_2'                                          	|
  | 7  	| id                 	| string       	| Type inferred from '24'                                                 	|
  | 8  	| status             	| string       	| Type inferred from 'supervised'                                         	|

  Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestión.

  | Id 	| Nombre de Columna  	| Tipo de Dato 	| Comentario                                                              	|
  |----	|--------------------	|--------------	|-------------------------------------------------------------------------	|  
  | 9  	| filedate           	| bigint       	| Type inferred from '20191231'                                           	|
  | 10 	| filename           	| string       	| Type inferred from 'elementosT7_NaranjaALU-1353-NARANJA_elementosT7_Na' 	|
  | 11 	| hash_id            	| string       	| Type inferred from 'null'                                               	|
  | 12 	| sourceid           	| string       	| Type inferred from 'elementost7_naranja_alu'                            	|
  | 13 	| registry_state     	| string       	| Type inferred from 'null'                                               	|
  | 14 	| datasetname        	| string       	| Type inferred from 'tx_elementost7_naranja_alu'                         	|
  | 15 	| timestamp          	| bigint       	| Type inferred from '20191231'                                           	|
  | 16 	| transaction_status 	| string       	| Type inferred from 'null'                                               	|   



- **Particiones**

    A continuación se presentan las particiones creadas de la tabla **tx_elementost7_naranja_alu**.

    Sentencia: ```show partitions rci_network_db.tx_elementost7_naranja_alu```

    | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Location                                                                                 	|
    |------	|-------	|-----	|-------	|--------	|----------	|--------	|------------------------------------------------------------------------------------------	|
    | 2019 	| 12     	| 31  	| 752  	| 1      	| 268.00KB 	| AVRO   	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/alcatel/tx_elementost7_naranja_alu/year=2019/month=12/day=31 	|

- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:
    ```
    select * from rci_metadata_db.tx_rci_executions
    where table_name = 'tx_elementost7_naranja_alu';
    ```

    | id_execution | table_name | dateload | avro_name | start_execution | end_execution | status | attempts |
    |--------------|------------|----------|---------------------------------------------------------|---------------------|---------------------|--------|----------|
    | 1 | tx_elementost7_naranja_alu | 20191231 | /data/RCI/raw/alcatel/elementost7_naranja_alu/data/20191231_elementosT7_NaranjaALU-1353-NARANJA_elementosT7_Naranja.avro | 2019-12-31 15:47:37 | 2019-12-31 15:48:38 | 1 | 0 |

- **Cifras de control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_elementost7_naranja_alu'
    and dateload = 20191231
    order by filedate asc;
    ```

    | uuid | rowprocessed | datasetname | filedate | filename | sourceid | dateload | read_count | insert_count | update_count | delete_count |
    |--------------------------------------|--------------|-------------|----------|-----------------------|----------------|----------|------------|--------------|--------------|--------------|
    | 0c042750-65df-4856-b644-a7a1c686fb6e | 752 | tx_elementost7_naranja_alu | 20191231 | elementosT7_NaranjaALU-1353-NARANJA_elementosT7_Naranja.csv | elementost7_naranja_alu | 20191231 | 752 | 752 | 0 | 0 |    


## Componentes del procesos de ingestión:

1 __Ingestión y Serialización via NiFi__

  ![NiFi Vista General][imgEM1]

  Pipeline Principal __Flujo Principal__

  ![EM NiFi Vista Subproceso][imgEM2]

  Pipeline Subproceso __Flujo de Subproceso__

  ![EM NiFi Vista Lectura de Archivos][imgEM3]

  Pipeline Lectura de Archivos __Lectura de Archivos__

  ![EM NiFi Vista Procesamiento][imgEM4]

  [imgEM1]: images/Elementost7_Naranja-nifi-00.png "EM NiFi vista general"
  [imgEM2]: images/Elementost7_Naranja-nifi-01.png "EM NiFi vista subproceso"
  [imgEM3]: images/Elementost7_Naranja-nifi-02.png "EM NiFi Lectura de Archivos"
  [imgEM4]: images/Elementost7_Naranja-nifi-03.png "EM NiFi Lectura de Archivos"

  Pipeline Lectura de Archivos __Procesamiento de Archivos__

2 __Reglas de Estandarización del Esquema `Kite`__

Las siguientes reglas se aplicarón para estandarizar el esquema:

- Remover Caracteres especiales en el header.
- Reemplazo de caracter _ por " " en el nombre del archivo.

3 __Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 89   | Valor de correspondiente al flujo Elementos T7 Naranja   |


  Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```

  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 89
  ```

## Referencias al Framework de Ingestion

[Framework de Ingestion](../Globales/ArquitecturaFrameworkIngestion/readme.md)

## Código Fuente Local

- [Código NiFi - NFR](NFR/)

## Código Fuente Globales

- [Código NiFi](/Globales/NIFICustomProcessorXLSX)
- [Código Spark](/Globales/SparkAxity)
- [Código Kite](/Globales/attdlkrci/readme.md)

***

## <a name="elementost7_rojo_alu"></a> Elementos T7 Rojo

## Descripción del `FTP`

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

## Descripción de la fuentes de datos
- **Descripción**
  [Elementos T7 Rojo EDA](../../../../RCI_DataAnalysis/eda/Alcatel/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Alcatel/README.md)

     Sentencia: ```describe formatted tx_elementost7_rojo_alu```

  | Id 	| Nombre de Columna  	| Tipo de Dato 	| Comentario                                                              	|
  |----	|--------------------	|--------------	|-------------------------------------------------------------------------	|
  | 1  	| emlim              	| string       	| Type inferred from '119'                                                	|
  | 2  	| userlabel          	| string       	| Type inferred from 'Tepeyac-MEXICO_68'                                  	|
  | 3  	| tipo               	| string       	| Type inferred from 'ULS'                                                	|
  | 4  	| version            	| string       	| Type inferred from '2.0'                                                	|
  | 5  	| direccion          	| string       	| Type inferred from '10.197.51.103:161'                                  	|
  | 6  	| interface          	| string       	| Type inferred from 'iusanmm1_0'                                         	|
  | 7  	| id                 	| string       	| Type inferred from '3'                                                  	|
  | 8  	| status             	| string       	| Type inferred from 'declared'                                           	|
  | 9  	| locationname       	| string       	| Type inferred from 'REG_7_PUEB'                                         	|
  | 10 	| aligned            	| string       	| Type inferred from 'misaligned'                                         	|

  Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestión.

  | Id 	| Nombre de Columna  	| Tipo de Dato 	| Comentario                                                              	|
  |----	|--------------------	|--------------	|-------------------------------------------------------------------------	|
  | 11 	| filedate           	| bigint       	| Type inferred from '20191231'                                           	|
  | 12 	| filename           	| string       	| Type inferred from 'ElementosT7_Rojo-ALU-1353-ROJO_elementosT7_Rojo.cs' 	|
  | 13 	| hash_id            	| string       	| Type inferred from 'null'                                               	|
  | 14 	| sourceid           	| string       	| Type inferred from 'elementost7_rojo_alu'                               	|
  | 15 	| registry_state     	| string       	| Type inferred from 'null'                                               	|
  | 16 	| datasetname        	| string       	| Type inferred from 'tx_elementost7_rojo_alu'                            	|
  | 17 	| timestamp          	| bigint       	| Type inferred from '20191231'                                           	|
  | 18 	| transaction_status 	| string       	| Type inferred from 'null'                                               	|

- **Particiones**

    A continuación se presentan las particiones creadas de la tabla **tx_elementost7_rojo_alu**.

    Sentencia: ```show partitions rci_network_db.tx_elementost7_rojo_alu```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Location                                                                                 	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|------------------------------------------------------------------------------------------	|
  | 2019 	| 12     	| 31  	| 393     	| 1      	| 278.07KB 	| AVRO   	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/alcatel/tx_elementost7_rojo_alu/year=2019/month=12/day=31 	|

- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:
    ```
    select * from rci_metadata_db.tx_rci_executions
    where table_name = 'tx_elementost7_rojo_alu';
    ```

    | id_execution | table_name | dateload | avro_name | start_execution | end_execution | status | attempts |
    |--------------|------------|----------|---------------------------------------------------------|---------------------|---------------------|--------|----------|
    | 1 | tx_elementost7_rojo_alu | 20191231 | /data/RCI/raw/alcatel/elementost7_rojo_alu/data/20191231_ElementosT7_Rojo-ALU-1353-ROJO_elementosT7_Rojo.avro | 2019-12-31 16:12:05 | 2019-12-31 16:14:01 | 1 | 0 |

- **Cifras de control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_elementost7_rojo_alu'
    and dateload = 20191231
    order by filedate asc;
    ```

    | uuid | rowprocessed | datasetname | filedate | filename | sourceid | dateload | read_count | insert_count | update_count | delete_count |
    |--------------------------------------|--------------|-------------|----------|-----------------------|----------------|----------|------------|--------------|--------------|--------------|
    | 0629aadd-3847-40e5-a0c5-e03fe0b3b233 | 393 | tx_elementost7_rojo_alu | 20191231 | ElementosT7_Rojo-ALU-1353-ROJO_elementosT7_Rojo.csv | elementost7_rojo_alu | 20191231 | 393 | 393 | 0 | 0 |     

## Componentes del procesos de ingestión:

1 __Ingestión y Serialización via NiFi__

  ![NiFi Vista General][imgEM1]

  Pipeline Principal __Flujo Principal__

  ![EM NiFi Vista Subproceso][imgEM2]

  Pipeline Subproceso __Flujo de Subproceso__

  ![EM NiFi Vista Lectura de Archivos][imgEM3]

  Pipeline Lectura de Archivos __Lectura de Archivos__

  ![EM NiFi Vista Procesamiento][imgEM4]

  [imgEM1]: images/Elementost7_Rojo-nifi-00.png "EM NiFi vista general"
  [imgEM2]: images/Elementost7_Rojo-nifi-01.png "EM NiFi vista subproceso"
  [imgEM3]: images/Elementost7_Rojo-nifi-02.png "EM NiFi Lectura de Archivos"
  [imgEM4]: images/Elementost7_Rojo-nifi-03.png "EM NiFi Lectura de Archivos"

  Pipeline Lectura de Archivos __Procesamiento de Archivos__

  2 __Reglas de Estandarización del Esquema `Kite`__

  Las siguientes reglas se aplicarón para estandarizar el esquema:

  - Remover Caracteres especiales en el header.
  - Reemplazo de caracter _ por " " en el nombre del archivo.

3 __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 90   | Valor de correspondiente al flujo Elementos T7 Rojo|


  Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```

  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 90
  ```

## Referencias al Framework de Ingestion

  [Framework de Ingestion](../Globales/ArquitecturaFrameworkIngestion/readme.md)

## Código Fuente Local

  - [Código NiFi - NFR](NFR/)

## Código Fuente Globales

  - [Código NiFi](/Globales/NIFICustomProcessorXLSX)
  - [Código Spark](/Globales/SparkAxity)
  - [Código Kite](/Globales/attdlkrci/readme.md)


***



[imgLogoAxity]:../Globales/ArquitecturaFrameworkIngestion/images/axity.png ""
[imgLogoAtt]:../Globales/ArquitecturaFrameworkIngestion/images/att.png ""
[imgEncabezado]:../Globales/ArquitecturaFrameworkIngestion/images/encabezado.png ""
