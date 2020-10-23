![EncabezadoAxity][imgEncabezado]

# Documentación Data Ingestion para la fuente ATT **CIP Finanzas**

## Descripción del `FTP`  

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
=======
- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [CIP Finanzas EDA](../../../../RCI_DataAnalysis/eda/CIP_Finanzas/EDA_CIP_Finanzas.md#descripci%C3%B3n)

- **Diccionario de Datos**
     La siguiente tabla muestra el resultado de ejecutar el siguiente comando:

    `describe formatted rci_network_db.tx_finance_cip;`

  | Id | Nombre de Columna           | Tipo de Dato | Comentario                                                              |
  |----|-----------------------------|--------------|-------------------------------------------------------------------------|
  | 1  | idnf                        | string       | Type inferred from 'ALPMX1'                                             |
  | 2  | id                          | string       | Type inferred from '1'                                                  |
  | 3  | origen                      | string       | Type inferred from 'M.dulo'                                             |
  | 4  | activo                      | string       | Type inferred from '1398036'                                            |
  | 5  | legalentity                 | string       | Type inferred from '16'                                                 |
  | 6  | libro                       | string       | Type inferred from 'MXCOR 02-TELE'                                      |
  | 7  | consecpapeldetrabajo        | string       | Type inferred from '1'                                                  |
  | 8  | notransaccion               | string       | Type inferred from '-'                                                  |
  | 9  | nofactura                   | string       | Type inferred from '-'                                                  |
  | 10 | categoria_1                 | string       | Type inferred from '86-1723 787 3G WIRELESS MICROONDAS'                 |
  | 11 | proyecto                    | string       | Type inferred from '10MWL00400'                                         |
  | 12 | nombreproyecto              | string       | Type inferred from 'NA'                                                 |
  | 13 | tarea                       | string       | Type inferred from '-'                                                  |
  | 14 | descripcion                 | string       | Type inferred from 'RTN 605 SYSTEM 3*FE+1*GE+16*E1+2*IF IDU UNIT (-48V' |
  | 15 | units_assigned              | string       | Type inferred from '1'                                                  |
  | 16 | unidades                    | string       | Type inferred from '1'                                                  |
  | 17 | articulo                    | string       | Type inferred from 'W.0913619'                                          |
  | 18 | cuenta                      | string       | Type inferred from '1763-787'                                           |
  | 19 | sub_cta                     | string       | Type inferred from '787'                                                |
  | 20 | mxn                         | string       | Type inferred from '4 398.39'                                           |
  | 21 | usd                         | string       | Type inferred from '227.18'                                             |
  | 22 | tc                          | string       | Type inferred from '19.3612'                                            |
  | 23 | column_000                  | string       | Type inferred from '0.23'                                               |
  | 24 | ubicacionconfirmada         | string       | Type inferred from 'ALPMX1'                                             |
  | 25 | tipoubicacion               | string       | Type inferred from 'Network'                                            |
  | 26 | tipografica                 | string       | Type inferred from 'null'                                               |
  | 27 | tipodeubicacionresumgrafica | string       | Type inferred from 'Sites'                                              |
  | 28 | tipodeubicacionresum        | string       | Type inferred from 'Warehouse'                                          |
  | 29 | mesdeingreso                | string       | Type inferred from '7/1/10'                                             |
  | 30 | mes                         | string       | Type inferred from 'nov-19'                                             |
  | 31 | tec                         | string       | Type inferred from 'Sitios'                                             |
  | 32 | tipo                        | string       | Type inferred from '3G / LTE'                                           |
  | 33 | ref                         | string       | Type inferred from 'M.dulo'                                             |
  | 34 | conspolsaldocuentas         | string       | Type inferred from 'M.dulo'                                             |
  | 35 | concepto                    | string       | Type inferred from 'Microondas'                                         |
  | 36 | column_year                 | string       | Type inferred from '2010'                                               |
  | 37 | dias                        | string       | Type inferred from '3439'                                               |
  | 38 | days                        | string       | Type inferred from 'DAYS>361'                                           |
  | 39 | parametrosdays              | string       | Type inferred from 'Days > 1 461'                                       |
  | 40 | tipocuenta                  | string       | Type inferred from 'CIP'                                                |
  | 41 | ordendecompra               | string       | Type inferred from '220100881'                                          |
  | 42 | proveedor                   | string       | Type inferred from 'HUAWEI TECHNOLOGIES DE MEXICO SA DE CV'             |
  | 43 | numeroetiqueta              | string       | Type inferred from '302125'                                             |
  | 44 | numeroserie                 | string       | Type inferred from '210231699810B2000083'                               |
  | 45 | obsv                        | string       | Type inferred from 'null'                                               |
  | 46 | valid                       | string       | Type inferred from 'null'                                               |
  | 47 | polizacap                   | string       | Type inferred from 'null'                                               |
  | 48 | tc20                        | string       | Type inferred from '219.92'                                             |
  | 49 | tc18                        | string       | Type inferred from '244.36'                                             |
  | 50 | ubicado                     | string       | Type inferred from '219.92'                                             |
  | 51 | noubicado                   | string       | Type inferred from 'null'                                               |
  | 52 | column_ampersand            | string       | Type inferred from '10MWL00400220100881'                                |
  | 53 | areaok                      | string       | Type inferred from 'Tx Eng.'                                            |
  | 54 | categoria_budget1_jc        | string       | Type inferred from '0'                                                  |
  | 55 | categoria_budget2_jc        | string       | Type inferred from '0'                                                  |
  | 56 | categoriamastplann          | string       | Type inferred from '0'                                                  |
  | 57 | categoriamastercipbudget    | string       | Type inferred from 'Transport MW'                                       |
  | 58 | column_idsitio              | string       | Type inferred from 'ALPMX1'                                             |
  | 59 | oracle                      | string       | Type inferred from 'ALPMX1'                                             |
  | 60 | nombredelsitio              | string       | Type inferred from 'ALMACEN'                                            |
  | 61 | subarea                     | string       | Type inferred from 'TX MW'                                              |
  | 62 | ubicacionconfirmada_2       | string       | Type inferred from 'ALMACEN'                                            |
  | 63 | nuevooenproceso             | string       | Type inferred from 'EN PROCESO'                                         |
  | 64 | idpm                        | string       | Type inferred from '-'                                                  |
  | 65 | pm                          | string       | Type inferred from '-'                                                  |
  | 66 | projectpm                   | string       | Type inferred from '-'                                                  |
  | 67 | id_programa                 | string       | Type inferred from '-'                                                  |
  | 68 | nombreprograma              | string       | Type inferred from '-'                                                  |
  | 69 | solicitante                 | string       | Type inferred from '-'                                                  |
  | 70 | director                    | string       | Type inferred from '-'                                                  |
  | 71 | responsable                 | string       | Type inferred from '-'                                                  |
  | 72 | notaalcomprador             | string       | Type inferred from '-'                                                  |
  | 73 | categoria                   | string       | Type inferred from '-'                                                  |
  | 74 | areahomologada              | string       | Type inferred from '-'                                                  |
  | 75 | ocdescripcion               | string       | Type inferred from '0'                                                  |
  | 76 | clasificacion               | string       | Type inferred from 'Network'                                            |
  | 77 | avp                         | string       | Type inferred from 'HECTOR VAZQUEZ'                                     |
  | 78 | disponiblesgermanluna       | string       | Type inferred from '0'                                                  |
  | 79 | controldecambiosenproceso   | string       | Type inferred from '0'                                                  |

    Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestión.

  | Id 	| Nombre de Columna           	| Tipo de Dato 	| Comentario                                                       	|
  |----	|-----------------------------	|--------------	|------------------------------------------------------------------	|
  | 80 	| filedate                    	| bigint       	| Type inferred from '20190801'                                    	|
  | 81 	| filename                    	| string       	| Type inferred from 'Integracion CIP + Ago 19 + TC20 +vfu_BD.csv' 	|
  | 82 	| hash_id                     	| string       	| Type inferred from 'null'                                        	|
  | 83 	| sourceid                    	| string       	| Type inferred from 'CIP'                                         	|
  | 84 	| registry_state              	| string       	| Type inferred from 'null'                                        	|
  | 85 	| datasetname                 	| string       	| Type inferred from 'cip_finance_cip'                             	|
  | 86 	| timestamp                   	| bigint       	| Type inferred from '20191226'                                    	|
  | 87 	| transaction_status          	| string       	| Type inferred from 'null'                                        	|


- **Particiones**

  A continuación se presentan las particiones creadas de la tabla **tx_finance_cip**.

  Sentencia: ```show partitions rci_network_db.tx_finance_cip;```

  | year 	| month 	| day 	| #Rows  	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                      	|
  |------	|-------	|-----	|--------	|--------	|----------	|--------	|-------------------	|-------------------------------------------------------------------------------	|
  | 2019 	| 7     	| 1   	| 189563 	| 1      	| 194.55MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/cip/year=2019/month=7/day=1  	|
  | 2019 	| 8     	| 1   	| 190665 	| 1      	| 189.20MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/cip/year=2019/month=8/day=1  	|
  | 2019 	| 9     	| 1   	| 193896 	| 1      	| 221.99MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/cip/year=2019/month=9/day=1  	|
  | 2019 	| 10    	| 1   	| 203210 	| 1      	| 229.32MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/cip/year=2019/month=10/day=1 	|
  | 2019 	| 11    	| 1   	| 211219 	| 1      	| 239.31MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/cip/year=2019/month=11/day=1 	|
  | 2019 	| 12    	| 1   	| 213107 	| 1      	| 241.11MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/cip/year=2019/month=12/day=1 	|

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:
  ```
  select * from rci_metadata_db.tx_rci_executions where
  table_name = 'tx_finance_cip'
  and status = 1
  and dateload = 20200114;
  ```

  | id_execution | table_name     | dateload | avro_name                                                                         | start_execution     | end_execution       | status | id_application | attempts |
  |--------------|----------------|----------|-----------------------------------------------------------------------------------|---------------------|---------------------|--------|----------------|----------|
  | 1            | tx_finance_cip | 20200114 | /data/RCI/raw/cip/data/20190701_Integracion_CIP_+_Jul_19_+_TC20_+vfu_NETWORK.avro | 2020-01-14 18:14:04 | 2020-01-14 18:16:01 | 1      |                | 0        |
  | 2            | tx_finance_cip | 20200114 | /data/RCI/raw/cip/data/20190801_Integracion_CIP_+_Ago_19_+_TC20_+vfu_BD.avro      | 2020-01-14 18:16:25 | 2020-01-14 18:18:33 | 1      |                | 0        |
  | 3            | tx_finance_cip | 20200114 | /data/RCI/raw/cip/data/20190901_Integracion_CIP_+_Sep_19_+_TC20_+vfu_Network.avro | 2020-01-14 18:18:56 | 2020-01-14 18:21:17 | 1      |                | 0        |
  | 4            | tx_finance_cip | 20200114 | /data/RCI/raw/cip/data/20191001_Integracion_CIP_+_Oct_19_+_TC20_+vfu_BD.avro      | 2020-01-14 18:21:40 | 2020-01-14 18:24:12 | 1      |                | 0        |
  | 5            | tx_finance_cip | 20200114 | /data/RCI/raw/cip/data/20191101_Integracion_CIP_+_Nov_19_+_TC20_+vfu_BD.avro      | 2020-01-14 18:24:36 | 2020-01-14 18:27:12 | 1      |                | 0        |
  | 6            | tx_finance_cip | 20200114 | /data/RCI/raw/cip/data/20191201_Integracion_CIP_+_Dic_19_+_TC20_+vfu_BD.avro      | 2020-01-14 18:27:35 | 2020-01-14 18:30:13 | 1      |                | 0        |


- **Cifras de control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_finance_cip'
  and dateload = 20200115
  order by filedate asc;
  ```

  | uuid                                 | rowprocessed | datasetname    | filedate | filename                                         | sourceid | dateload | read_count | insert_count | update_count | delete_count |   |
  |--------------------------------------|--------------|----------------|----------|--------------------------------------------------|----------|----------|------------|--------------|--------------|--------------|---|
  | 1f76042e-a3f4-4a01-937a-88a140b4df79 | 189563       | tx_finance_cip | 20190701 | Integracion CIP + Jul 19 + TC20 +vfu_NETWORK.csv | CIP      | 20200115 | 189563     | 189563       | 0            | 0            |   |
  | 4c8884d7-4be6-4e3e-8d29-d3233dc8313e | 190665       | tx_finance_cip | 20190801 | Integracion CIP + Ago 19 + TC20 +vfu_BD.csv      | CIP      | 20200115 | 190665     | 190665       | 0            | 0            |   |
  | e9d6fa4e-274d-436f-86c6-bc62609bef57 | 193896       | tx_finance_cip | 20190901 | Integracion CIP + Sep 19 + TC20 +vfu_Network.csv | CIP      | 20200115 | 193896     | 193896       | 0            | 0            |   |
  | 0055a4ac-f5de-43ca-a0c3-2b5bb60d1216 | 203210       | tx_finance_cip | 20191001 | Integracion CIP + Oct 19 + TC20 +vfu_BD.csv      | CIP      | 20200115 | 203210     | 203210       | 0            | 0            |   |
  | 136b7156-307c-429b-a7d2-a7537592d2ca | 211219       | tx_finance_cip | 20191101 | Integracion CIP + Nov 19 + TC20 +vfu_BD.csv      | CIP      | 20200115 | 211219     | 211219       | 0            | 0            |   |
  | 05a1c18d-6001-4c8c-b55a-ad6ed1b83b50 | 213107       | tx_finance_cip | 20191201 | Integracion CIP + Dic 19 + TC20 +vfu_BD.csv      | CIP      | 20200115 | 213107     | 213107       | 0            | 0            |   |

## Componentes del procesos de ingestion

  1. **Ingestion y Serialización via NiFi**

  ![CIP Finanzas NiFi Vista General][img1]

  Pipeline Principal __Flujo Principal__

  ![CIP Finanzas NiFi Vista Subproceso][img2]

  Pipeline Subproceso __Flujo de Subproceso__

  ![CIP Finanzas NiFi Vista Lectura de Archivos][img3]

  Pipeline Lectura de Archivos __Lectura de Archivos__

  2. **Reglas de Estandarización del Esquema `Kite`**

    Las siguientes reglas se aplicarón para estandarizar el esquema:

    - Remover Caracteres especiales en el header.
    - Reemplazo de caracter _ por "" en el nombre del archivo.

3. **Framework de Ingestión Automatizado**

  - Especificar parámetros del proceso kite:

    | Parámetro | Valor | Descripción|
    | ---------- | ---------- | ---------- |
    | parametro_01   | 1   | Valor de correspondiente al flujo CIP Finanzas   |

    Sentencia kite:

    ```
    ./rci_ingesta_generacion_avro.sh {parametro_01}
    ```

    Ejemplo:

    ```
    ./rci_ingesta_generacion_avro.sh 1
    ```

## Referencias al Framework de Ingestion

- [Framework de Ingestion](../Globales/ArquitecturaFrameworkIngestion/readme.md)

## Código Fuente Local

- [Codigo NiFi - NFR](NFR/)

## Código Fuente Globales

- [Codigo NiFi](../Globales/NIFICustomProcessorXLSX)
- [Codigo Spark](../Globales/SparkAxity)
- [Codigo Kite](../Globales/attdlkrci/readme.md)

[img1]: images/IntegracionCIP-nifi-00.png "CIP Finanzas NiFi vista general"
[img2]: images/IntegracionCIP-nifi-01.png "CIP Finanzas NiFi vista subproceso"
[img3]: images/IntegracionCIP-nifi-02.png "CIP Finanzas NiFi Lectura de Archivos"
[img5]: images/IntegracionCIP-nifi-04.png "CIP Finanzas NiFi Lectura de Archivos"


[imgEncabezado]:../Globales/ArquitecturaFrameworkIngestion/images/encabezado.png ""
