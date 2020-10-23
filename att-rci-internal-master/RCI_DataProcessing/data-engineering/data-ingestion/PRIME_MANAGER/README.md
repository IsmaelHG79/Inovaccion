![EncabezadoAxity][imgEncabezado]

# Documentación Data Ingestion para la fuente ATT **Prime Manager**

## Descripción del `FTP`  

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

## Descripción de la fuentes de datos
- **Descripción**
  [Prime Manager Finanzas EDA](../../../../RCI_DataAnalysis/eda/PRIME_MANAGER/EDA_Prime_Manager.md#descripci%C3%B3n)

- **Diccionario de Datos**
     La siguiente tabla muestra el resultado de ejecutar el siguiente comando:

    `describe formatted rci_network_db.tx_prime_manager;`

    | Id 	| Nombre de Columna   	| Tipo de Dato 	| Comentario                                            	|
    |----	|---------------------	|--------------	|-------------------------------------------------------	|
    | 1  	| name                	| string       	| Type inferred from 'MX-TIJ-M5-ISP-NEXUS-7702-2'       	|
    | 2  	| ip_address          	| string       	| Type inferred from '10.38.2.82'                       	|
    | 3  	| communication_state 	| string       	| Type inferred from 'Device Reachable'                 	|
    | 4  	| investigation_state 	| string       	| Type inferred from 'Operational'                      	|
    | 5  	| product             	| string       	| Type inferred from 'Eth-Switch'                       	|
    | 6  	| device_series       	| string       	| Type inferred from 'Cisco Nexus 7000 Series Switches' 	|
    | 7  	| element_type        	| string       	| Type inferred from 'Cisco_Nexus_7702_Switch'          	|
    | 8  	| software_version    	| string       	| Type inferred from '8.2(3)'                           	|
    | 9  	| location            	| string       	| Type inferred from 'Tijuana ISP'                      	|
    | 10 	| up_since            	| string       	| Type inferred from 'Sun Sep 01 03:59:32 CDT 2019'     	|

    Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestión.

    | Id 	| Nombre de Columna  	| Tipo de Dato 	| Comentario                                                	|
    |----	|--------------------	|--------------	|-----------------------------------------------------------	|
    | 11 	| filedate            	| bigint       	| Type inferred from '20191016'                         	|
    | 12 	| filename            	| string       	| Type inferred from 'CPN_DeviceList_20191016_0559.csv' 	|
    | 13 	| hash_id             	| string       	| Type inferred from 'null'                             	|
    | 14 	| sourceid            	| string       	| Type inferred from 'prime_manager'                    	|
    | 15 	| registry_state      	| string       	| Type inferred from 'null'                             	|
    | 16 	| datasetname         	| string       	| Type inferred from 'tx_prime_manager'                 	|
    | 17 	| timestamp           	| bigint       	| Type inferred from '20200102'                         	|
    | 18 	| transaction_status  	| string       	| Type inferred from 'null'                             	|


- **Particiones**

  A continuación se presentan las particiones creadas de la tabla **tx_prime_manager**.

  Sentencia: ```show partitions rci_network_db.tx_prime_manager;```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size    	| Format 	| Incremental stats 	| Location                                                                                 	|
  |------	|-------	|-----	|-------	|--------	|---------	|--------	|-------------------	|------------------------------------------------------------------------------------------	|
  | 2019 	| 10    	| 16  	| 197   	| 1      	| 81.56KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=16 	|
  | 2019 	| 10    	| 17  	| 20    	| 1      	| 9.96KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=17 	|
  | 2019 	| 10    	| 18  	| 14    	| 1      	| 7.56KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=18 	|
  | 2019 	| 10    	| 19  	| 14    	| 1      	| 7.56KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=19 	|
  | 2019 	| 10    	| 20  	| 2     	| 1      	| 2.66KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=20 	|
  | 2019 	| 10    	| 22  	| 11    	| 1      	| 6.36KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=22 	|
  | 2019 	| 10    	| 23  	| 10    	| 1      	| 5.93KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=23 	|
  | 2019 	| 10    	| 24  	| 7     	| 1      	| 4.65KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=24 	|
  | 2019 	| 10    	| 25  	| 2     	| 1      	| 2.65KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=25 	|
  | 2019 	| 10    	| 26  	| 2     	| 1      	| 2.66KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=26 	|
  | 2019 	| 10    	| 27  	| 4     	| 1      	| 3.48KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=27 	|
  | 2019 	| 10    	| 28  	| 2     	| 1      	| 2.66KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=28 	|
  | 2019 	| 10    	| 29  	| 15    	| 1      	| 7.96KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=29 	|
  | 2019 	| 10    	| 30  	| 13    	| 1      	| 7.16KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=30 	|
  | 2019 	| 10    	| 31  	| 12    	| 1      	| 6.74KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=10/day=31 	|
  | 2019 	| 11    	| 1   	| 12    	| 1      	| 6.74KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=1  	|
  | 2019 	| 11    	| 2   	| 5     	| 1      	| 3.88KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=2  	|
  | 2019 	| 11    	| 4   	| 2     	| 1      	| 2.66KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=4  	|
  | 2019 	| 11    	| 5   	| 5     	| 1      	| 3.88KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=5  	|
  | 2019 	| 11    	| 6   	| 10    	| 1      	| 5.93KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=6  	|
  | 2019 	| 11    	| 7   	| 4     	| 1      	| 3.49KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=7  	|
  | 2019 	| 11    	| 13  	| 18    	| 1      	| 9.18KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=13 	|
  | 2019 	| 11    	| 14  	| 4     	| 1      	| 3.49KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=14 	|
  | 2019 	| 11    	| 15  	| 8     	| 1      	| 4.95KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=15 	|
  | 2019 	| 11    	| 16  	| 64    	| 1      	| 28.02KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=16 	|
  | 2019 	| 11    	| 19  	| 2     	| 1      	| 2.65KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=19 	|
  | 2019 	| 11    	| 20  	| 4     	| 1      	| 3.48KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=20 	|
  | 2019 	| 11    	| 21  	| 3     	| 1      	| 3.05KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=21 	|
  | 2019 	| 11    	| 22  	| 17    	| 1      	| 8.91KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=22 	|
  | 2019 	| 11    	| 23  	| 17    	| 1      	| 8.87KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=23 	|
  | 2019 	| 11    	| 24  	| 3     	| 1      	| 3.10KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=24 	|
  | 2019 	| 11    	| 25  	| 4     	| 1      	| 3.48KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=25 	|
  | 2019 	| 11    	| 26  	| 3     	| 1      	| 3.06KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=26 	|
  | 2019 	| 11    	| 27  	| 5     	| 1      	| 3.91KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=27 	|
  | 2019 	| 11    	| 28  	| 3     	| 1      	| 3.04KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=28 	|
  | 2019 	| 11    	| 29  	| 5     	| 1      	| 3.82KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=29 	|
  | 2019 	| 11    	| 30  	| 4     	| 1      	| 3.49KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=11/day=30 	|
  | 2019 	| 12    	| 1   	| 1     	| 1      	| 2.25KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=1  	|
  | 2019 	| 12    	| 2   	| 1     	| 1      	| 2.25KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=2  	|
  | 2019 	| 12    	| 3   	| 3     	| 1      	| 3.06KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=3  	|
  | 2019 	| 12    	| 4   	| 13    	| 1      	| 7.17KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=4  	|
  | 2019 	| 12    	| 5   	| 11    	| 1      	| 6.40KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=5  	|
  | 2019 	| 12    	| 6   	| 6     	| 1      	| 4.27KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=6  	|
  | 2019 	| 12    	| 7   	| 4     	| 1      	| 3.49KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=7  	|
  | 2019 	| 12    	| 8   	| 3     	| 1      	| 3.07KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=8  	|
  | 2019 	| 12    	| 9   	| 12    	| 1      	| 6.74KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=9  	|
  | 2019 	| 12    	| 10  	| 14    	| 1      	| 7.57KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=10 	|
  | 2019 	| 12    	| 11  	| 6     	| 1      	| 4.33KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=11 	|
  | 2019 	| 12    	| 12  	| 4     	| 1      	| 3.52KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=12 	|
  | 2019 	| 12    	| 13  	| 5     	| 1      	| 3.88KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=13 	|
  | 2019 	| 12    	| 16  	| 20    	| 1      	| 10.04KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=16 	|
  | 2019 	| 12    	| 17  	| 2     	| 1      	| 2.66KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=17 	|
  | 2019 	| 12    	| 18  	| 3     	| 1      	| 3.09KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=18 	|
  | 2019 	| 12    	| 19  	| 2     	| 1      	| 2.66KB  	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/prime_manager/year=2019/month=12/day=19 	|

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:
  ```
  select * from rci_metadata_db.tx_rci_executions
  where table_name = 'tx_prime_manager';
  ```

  | id_execution 	| table_name       	| dateload 	| avro_name                                                                   	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|
  |--------------	|------------------	|----------	|-----------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|
  | 1            	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191016_CPN_DeviceList_20191016_0559.avro 	| 2020-01-03 11:54:26 	| 2020-01-03 11:55:11 	| 1      	|         	|                	| 0        	|
  | 2            	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191017_CPN_DeviceList_20191017_0559.avro 	| 2020-01-03 11:55:15 	| 2020-01-03 11:56:52 	| 1      	|         	|                	| 0        	|
  | 3            	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191018_CPN_DeviceList_20191018_0559.avro 	| 2020-01-03 11:56:56 	| 2020-01-03 11:58:32 	| 1      	|         	|                	| 0        	|
  | 4            	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191019_CPN_DeviceList_20191019_0559.avro 	| 2020-01-03 11:58:36 	| 2020-01-03 12:00:11 	| 1      	|         	|                	| 0        	|
  | 5            	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191020_CPN_DeviceList_20191020_0559.avro 	| 2020-01-03 12:00:15 	| 2020-01-03 12:01:51 	| 1      	|         	|                	| 0        	|
  | 6            	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191021_CPN_DeviceList_20191021_0559.avro 	| 2020-01-03 12:01:55 	| 2020-01-03 12:03:25 	| 1      	|         	|                	| 0        	|
  | 7            	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191022_CPN_DeviceList_20191022_0559.avro 	| 2020-01-03 12:03:29 	| 2020-01-03 12:04:59 	| 1      	|         	|                	| 0        	|
  | 8            	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191023_CPN_DeviceList_20191023_0559.avro 	| 2020-01-03 12:05:03 	| 2020-01-03 12:06:41 	| 1      	|         	|                	| 0        	|
  | 9            	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191024_CPN_DeviceList_20191024_0559.avro 	| 2020-01-03 12:06:45 	| 2020-01-03 12:08:26 	| 1      	|         	|                	| 0        	|
  | 10           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191025_CPN_DeviceList_20191025_0559.avro 	| 2020-01-03 12:08:30 	| 2020-01-03 12:10:04 	| 1      	|         	|                	| 0        	|
  | 11           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191026_CPN_DeviceList_20191026_0559.avro 	| 2020-01-03 12:10:08 	| 2020-01-03 12:11:50 	| 1      	|         	|                	| 0        	|
  | 12           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191027_CPN_DeviceList_20191027_0559.avro 	| 2020-01-03 12:11:54 	| 2020-01-03 12:13:23 	| 1      	|         	|                	| 0        	|
  | 13           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191028_CPN_DeviceList_20191028_0559.avro 	| 2020-01-03 12:13:27 	| 2020-01-03 12:14:56 	| 1      	|         	|                	| 0        	|
  | 14           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191029_CPN_DeviceList_20191029_0559.avro 	| 2020-01-03 12:15:00 	| 2020-01-03 12:16:30 	| 1      	|         	|                	| 0        	|
  | 15           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191030_CPN_DeviceList_20191030_0559.avro 	| 2020-01-03 12:16:34 	| 2020-01-03 12:18:14 	| 1      	|         	|                	| 0        	|
  | 16           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191031_CPN_DeviceList_20191031_0559.avro 	| 2020-01-03 12:18:18 	| 2020-01-03 12:19:59 	| 1      	|         	|                	| 0        	|
  | 17           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191101_CPN_DeviceList_20191101_0559.avro 	| 2020-01-03 12:20:04 	| 2020-01-03 12:21:46 	| 1      	|         	|                	| 0        	|
  | 18           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191102_CPN_DeviceList_20191102_0559.avro 	| 2020-01-03 12:21:51 	| 2020-01-03 12:23:32 	| 1      	|         	|                	| 0        	|
  | 19           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191103_CPN_DeviceList_20191103_0559.avro 	| 2020-01-03 12:23:36 	| 2020-01-03 12:25:15 	| 1      	|         	|                	| 0        	|
  | 20           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191104_CPN_DeviceList_20191104_0559.avro 	| 2020-01-03 12:25:19 	| 2020-01-03 12:27:00 	| 1      	|         	|                	| 0        	|
  | 21           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191105_CPN_DeviceList_20191105_0559.avro 	| 2020-01-03 12:27:03 	| 2020-01-03 12:28:28 	| 1      	|         	|                	| 0        	|
  | 22           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191106_CPN_DeviceList_20191106_0559.avro 	| 2020-01-03 12:28:32 	| 2020-01-03 12:30:03 	| 1      	|         	|                	| 0        	|
  | 23           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191107_CPN_DeviceList_20191107_0559.avro 	| 2020-01-03 12:30:07 	| 2020-01-03 12:31:50 	| 1      	|         	|                	| 0        	|
  | 24           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191113_CPN_DeviceList_20191113_0559.avro 	| 2020-01-03 12:31:54 	| 2020-01-03 12:33:37 	| 1      	|         	|                	| 0        	|
  | 25           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191114_CPN_DeviceList_20191114_0559.avro 	| 2020-01-03 12:33:41 	| 2020-01-03 12:35:24 	| 1      	|         	|                	| 0        	|
  | 26           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191115_CPN_DeviceList_20191115_0559.avro 	| 2020-01-03 12:35:28 	| 2020-01-03 12:37:17 	| 1      	|         	|                	| 0        	|
  | 27           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191116_CPN_DeviceList_20191116_0559.avro 	| 2020-01-03 12:37:21 	| 2020-01-03 12:39:04 	| 1      	|         	|                	| 0        	|
  | 28           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191117_CPN_DeviceList_20191117_0559.avro 	| 2020-01-03 12:39:08 	| 2020-01-03 12:40:53 	| 1      	|         	|                	| 0        	|
  | 29           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191118_CPN_DeviceList_20191118_0559.avro 	| 2020-01-03 12:40:57 	| 2020-01-03 12:42:42 	| 1      	|         	|                	| 0        	|
  | 30           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191119_CPN_DeviceList_20191119_0559.avro 	| 2020-01-03 12:42:47 	| 2020-01-03 12:44:18 	| 1      	|         	|                	| 0        	|
  | 31           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191120_CPN_DeviceList_20191120_0559.avro 	| 2020-01-03 12:44:22 	| 2020-01-03 12:46:05 	| 1      	|         	|                	| 0        	|
  | 32           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191121_CPN_DeviceList_20191121_0559.avro 	| 2020-01-03 12:46:09 	| 2020-01-03 12:47:52 	| 1      	|         	|                	| 0        	|
  | 33           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191122_CPN_DeviceList_20191122_0559.avro 	| 2020-01-03 12:47:56 	| 2020-01-03 12:49:32 	| 1      	|         	|                	| 0        	|
  | 34           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191123_CPN_DeviceList_20191123_0559.avro 	| 2020-01-03 12:49:37 	| 2020-01-03 12:51:23 	| 1      	|         	|                	| 0        	|
  | 35           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191124_CPN_DeviceList_20191124_0559.avro 	| 2020-01-03 12:51:27 	| 2020-01-03 12:52:59 	| 1      	|         	|                	| 0        	|
  | 36           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191125_CPN_DeviceList_20191125_0559.avro 	| 2020-01-03 12:53:03 	| 2020-01-03 12:54:48 	| 1      	|         	|                	| 0        	|
  | 37           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191126_CPN_DeviceList_20191126_0559.avro 	| 2020-01-03 12:54:52 	| 2020-01-03 12:56:36 	| 1      	|         	|                	| 0        	|
  | 38           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191127_CPN_DeviceList_20191127_0559.avro 	| 2020-01-03 12:56:49 	| 2020-01-03 12:58:31 	| 1      	|         	|                	| 0        	|
  | 39           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191128_CPN_DeviceList_20191128_0559.avro 	| 2020-01-03 12:58:36 	| 2020-01-03 13:00:24 	| 1      	|         	|                	| 0        	|
  | 40           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191129_CPN_DeviceList_20191129_0559.avro 	| 2020-01-03 13:00:28 	| 2020-01-03 13:02:19 	| 1      	|         	|                	| 0        	|
  | 41           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191130_CPN_DeviceList_20191130_0559.avro 	| 2020-01-03 13:02:23 	| 2020-01-03 13:03:55 	| 1      	|         	|                	| 0        	|
  | 42           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191201_CPN_DeviceList_20191201_0559.avro 	| 2020-01-03 13:03:59 	| 2020-01-03 13:05:46 	| 1      	|         	|                	| 0        	|
  | 43           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191202_CPN_DeviceList_20191202_0559.avro 	| 2020-01-03 13:05:50 	| 2020-01-03 13:07:19 	| 1      	|         	|                	| 0        	|
  | 44           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191203_CPN_DeviceList_20191203_0559.avro 	| 2020-01-03 13:07:23 	| 2020-01-03 13:09:05 	| 1      	|         	|                	| 0        	|
  | 45           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191204_CPN_DeviceList_20191204_0559.avro 	| 2020-01-03 13:09:10 	| 2020-01-03 13:11:07 	| 1      	|         	|                	| 0        	|
  | 46           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191205_CPN_DeviceList_20191205_0559.avro 	| 2020-01-03 13:11:11 	| 2020-01-03 13:13:18 	| 1      	|         	|                	| 0        	|
  | 47           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191206_CPN_DeviceList_20191206_0559.avro 	| 2020-01-03 13:13:22 	| 2020-01-03 13:17:29 	| 1      	|         	|                	| 0        	|
  | 48           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191207_CPN_DeviceList_20191207_0559.avro 	| 2020-01-03 13:17:34 	| 2020-01-03 13:21:13 	| 1      	|         	|                	| 0        	|
  | 49           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191208_CPN_DeviceList_20191208_0559.avro 	| 2020-01-03 13:21:17 	| 2020-01-03 13:24:22 	| 1      	|         	|                	| 0        	|
  | 50           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191209_CPN_DeviceList_20191209_0559.avro 	| 2020-01-03 13:24:27 	| 2020-01-03 13:26:04 	| 1      	|         	|                	| 0        	|
  | 51           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191210_CPN_DeviceList_20191210_0559.avro 	| 2020-01-03 13:26:08 	| 2020-01-03 13:28:31 	| 1      	|         	|                	| 0        	|
  | 52           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191211_CPN_DeviceList_20191211_0559.avro 	| 2020-01-03 13:28:35 	| 2020-01-03 13:31:10 	| 1      	|         	|                	| 0        	|
  | 53           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191212_CPN_DeviceList_20191212_0559.avro 	| 2020-01-03 13:31:14 	| 2020-01-03 13:35:22 	| 1      	|         	|                	| 0        	|
  | 54           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191213_CPN_DeviceList_20191213_0559.avro 	| 2020-01-03 13:35:26 	| 2020-01-03 13:39:16 	| 1      	|         	|                	| 0        	|
  | 55           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191214_CPN_DeviceList_20191214_0559.avro 	| 2020-01-03 13:39:20 	| 2020-01-03 13:42:38 	| 1      	|         	|                	| 0        	|
  | 56           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191215_CPN_DeviceList_20191215_0559.avro 	| 2020-01-03 13:42:42 	| 2020-01-03 13:44:15 	| 1      	|         	|                	| 0        	|
  | 57           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191216_CPN_DeviceList_20191216_0559.avro 	| 2020-01-03 13:44:19 	| 2020-01-03 13:46:12 	| 1      	|         	|                	| 0        	|
  | 58           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191217_CPN_DeviceList_20191217_0559.avro 	| 2020-01-03 13:46:16 	| 2020-01-03 13:48:13 	| 1      	|         	|                	| 0        	|
  | 59           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191218_CPN_DeviceList_20191218_0559.avro 	| 2020-01-03 13:48:18 	| 2020-01-03 13:50:01 	| 1      	|         	|                	| 0        	|
  | 60           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191219_CPN_DeviceList_20191219_0559.avro 	| 2020-01-03 13:50:05 	| 2020-01-03 13:51:47 	| 1      	|         	|                	| 0        	|
  | 61           	| tx_prime_manager 	| 20200103 	| /data/RCI/raw/prime_manager/data/20191220_CPN_DeviceList_20191220_0559.avro 	| 2020-01-03 13:51:51 	| 2020-01-03 13:53:30 	| 1      	|         	|                	| 0        	|

- **Cifras de control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_prime_manager'
  and dateload = 20200103
  order by filedate asc;
  ```

  | uuid                                 	| rowprocessed 	| datasetname      	| filedate 	| filename                         	| sourceid      	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |--------------------------------------	|--------------	|------------------	|----------	|----------------------------------	|---------------	|----------	|------------	|--------------	|--------------	|--------------	|
  | af6335bd-bbba-42e7-8095-8b0010a47e5e 	| 197          	| tx_prime_manager 	| 20191016 	| CPN_DeviceList_20191016_0559.csv 	| prime_manager 	| 20200103 	| 197        	| 197          	| 0            	| 0            	|
  | 1c22b396-7457-4160-8fd5-fc2977cc77a1 	| 196          	| tx_prime_manager 	| 20191017 	| CPN_DeviceList_20191017_0559.csv 	| prime_manager 	| 20200103 	| 196        	| 0            	| 19           	| 1            	|
  | 2a9d27cb-eb99-4d54-b9f2-a5b4ff66fe47 	| 195          	| tx_prime_manager 	| 20191018 	| CPN_DeviceList_20191018_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 25           	| 1            	|
  | 3eb62d50-6009-4175-b7a4-69257b59e669 	| 195          	| tx_prime_manager 	| 20191019 	| CPN_DeviceList_20191019_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 38           	| 0            	|
  | ad5532eb-75a1-430b-8f94-1049e84ace12 	| 195          	| tx_prime_manager 	| 20191020 	| CPN_DeviceList_20191020_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 2            	| 0            	|
  | d37ca13e-8499-40ad-8dbf-7b51be4788f9 	| 195          	| tx_prime_manager 	| 20191021 	| CPN_DeviceList_20191021_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 0            	| 0            	|
  | 07c4ed5c-360e-4d66-bbde-8c5f14171676 	| 195          	| tx_prime_manager 	| 20191022 	| CPN_DeviceList_20191022_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 11           	| 0            	|
  | 29f85735-4e78-4004-9713-87953148a335 	| 195          	| tx_prime_manager 	| 20191023 	| CPN_DeviceList_20191023_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 18           	| 0            	|
  | fa44c47c-5e82-47f4-a8ea-6a4ab7e160e1 	| 195          	| tx_prime_manager 	| 20191024 	| CPN_DeviceList_20191024_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 1            	| 5            	| 1            	|
  | 899d3fa2-f140-41d5-bf0c-e663d1029a3a 	| 195          	| tx_prime_manager 	| 20191025 	| CPN_DeviceList_20191025_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 2            	| 0            	|
  | c44aa926-068a-45ef-a927-168f0cb4bb01 	| 195          	| tx_prime_manager 	| 20191026 	| CPN_DeviceList_20191026_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 3            	| 0            	|
  | 1ef0975f-101c-429b-8057-e71f50f81a8f 	| 195          	| tx_prime_manager 	| 20191027 	| CPN_DeviceList_20191027_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 6            	| 0            	|
  | 18a47140-23a0-47c5-a12e-e0cb5f42ce8f 	| 195          	| tx_prime_manager 	| 20191028 	| CPN_DeviceList_20191028_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 4            	| 0            	|
  | d09268b0-6b2d-4d01-af82-cd37a21d8e00 	| 195          	| tx_prime_manager 	| 20191029 	| CPN_DeviceList_20191029_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 50           	| 0            	|
  | adf85973-52bc-4c19-8038-b00ea08fb79a 	| 195          	| tx_prime_manager 	| 20191030 	| CPN_DeviceList_20191030_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 57           	| 0            	|
  | a246ec62-0cd3-4195-bee3-a6db172f1a02 	| 195          	| tx_prime_manager 	| 20191031 	| CPN_DeviceList_20191031_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 67           	| 0            	|
  | 7aed81ef-f7c0-4b61-b49a-1af51bc2f0e3 	| 195          	| tx_prime_manager 	| 20191101 	| CPN_DeviceList_20191101_0559.csv 	| prime_manager 	| 20200103 	| 195        	| 0            	| 79           	| 0            	|
  | f6351c25-de16-4408-8d80-29beee02cc7c 	| 194          	| tx_prime_manager 	| 20191102 	| CPN_DeviceList_20191102_0559.csv 	| prime_manager 	| 20200103 	| 194        	| 0            	| 6            	| 1            	|
  | 0e066236-73bf-456b-a259-d1b704898c86 	| 194          	| tx_prime_manager 	| 20191103 	| CPN_DeviceList_20191103_0559.csv 	| prime_manager 	| 20200103 	| 194        	| 0            	| 0            	| 0            	|
  | 9aac92df-4061-448f-a9da-5b2b0e8b68d5 	| 194          	| tx_prime_manager 	| 20191104 	| CPN_DeviceList_20191104_0559.csv 	| prime_manager 	| 20200103 	| 194        	| 0            	| 2            	| 0            	|
  | b11fad7d-bf54-4191-aa1a-68c3423bf77e 	| 194          	| tx_prime_manager 	| 20191105 	| CPN_DeviceList_20191105_0559.csv 	| prime_manager 	| 20200103 	| 194        	| 0            	| 9            	| 0            	|
  | c46ee54e-1a0b-47b7-ad44-0256911443d1 	| 194          	| tx_prime_manager 	| 20191106 	| CPN_DeviceList_20191106_0559.csv 	| prime_manager 	| 20200103 	| 194        	| 0            	| 14           	| 0            	|
  | 8a4ea17f-9601-4f3b-a33e-2357ab54f333 	| 194          	| tx_prime_manager 	| 20191107 	| CPN_DeviceList_20191107_0559.csv 	| prime_manager 	| 20200103 	| 194        	| 0            	| 9            	| 0            	|
  | ac7e183d-7a4d-4654-a89b-51adaf07d990 	| 192          	| tx_prime_manager 	| 20191113 	| CPN_DeviceList_20191113_0559.csv 	| prime_manager 	| 20200103 	| 192        	| 1            	| 20           	| 4            	|
  | faaf7109-3cc1-44d2-941d-01d256897b9d 	| 192          	| tx_prime_manager 	| 20191114 	| CPN_DeviceList_20191114_0559.csv 	| prime_manager 	| 20200103 	| 192        	| 0            	| 4            	| 0            	|
  | a7cfd5c8-c367-4847-ad1c-fe43369442ca 	| 192          	| tx_prime_manager 	| 20191115 	| CPN_DeviceList_20191115_0559.csv 	| prime_manager 	| 20200103 	| 192        	| 3            	| 2            	| 4            	|
  | 384da8d5-50fb-40b1-9745-e7109da20bcb 	| 192          	| tx_prime_manager 	| 20191116 	| CPN_DeviceList_20191116_0559.csv 	| prime_manager 	| 20200103 	| 192        	| 0            	| 192          	| 0            	|
  | 7cc34336-6ded-4e92-ba72-59582b84d12b 	| 192          	| tx_prime_manager 	| 20191117 	| CPN_DeviceList_20191117_0559.csv 	| prime_manager 	| 20200103 	| 192        	| 0            	| 0            	| 0            	|
  | 03082c5e-ae6c-48fd-9abe-609040f59f07 	| 192          	| tx_prime_manager 	| 20191118 	| CPN_DeviceList_20191118_0559.csv 	| prime_manager 	| 20200103 	| 192        	| 0            	| 0            	| 0            	|
  | 16923e82-ee51-4253-91fd-ebff75a9c251 	| 192          	| tx_prime_manager 	| 20191119 	| CPN_DeviceList_20191119_0559.csv 	| prime_manager 	| 20200103 	| 192        	| 0            	| 5            	| 0            	|
  | eefa4fe3-3cef-4282-96ba-ec15be3019c7 	| 190          	| tx_prime_manager 	| 20191120 	| CPN_DeviceList_20191120_0559.csv 	| prime_manager 	| 20200103 	| 190        	| 0            	| 3            	| 3            	|
  | 084cc940-dbdd-4b79-91c5-2f07a59c4b34 	| 190          	| tx_prime_manager 	| 20191121 	| CPN_DeviceList_20191121_0559.csv 	| prime_manager 	| 20200103 	| 190        	| 0            	| 5            	| 0            	|
  | 11e3b403-237f-41f6-aa77-0ecdefac40ad 	| 190          	| tx_prime_manager 	| 20191122 	| CPN_DeviceList_20191122_0559.csv 	| prime_manager 	| 20200103 	| 190        	| 0            	| 37           	| 0            	|
  | 9d7b57e9-d6f7-437d-be14-3a64e9bb39e1 	| 190          	| tx_prime_manager 	| 20191123 	| CPN_DeviceList_20191123_0559.csv 	| prime_manager 	| 20200103 	| 190        	| 0            	| 43           	| 0            	|
  | 14b90d46-87cb-4c7b-b44e-41a6d48b41c1 	| 190          	| tx_prime_manager 	| 20191124 	| CPN_DeviceList_20191124_0559.csv 	| prime_manager 	| 20200103 	| 190        	| 0            	| 9            	| 0            	|
  | c7c76b6d-0b3a-4b40-8820-5e81138a235a 	| 190          	| tx_prime_manager 	| 20191125 	| CPN_DeviceList_20191125_0559.csv 	| prime_manager 	| 20200103 	| 190        	| 0            	| 8            	| 0            	|
  | 43fa439f-a8de-4fc2-b0ac-c9b3d53916b9 	| 190          	| tx_prime_manager 	| 20191126 	| CPN_DeviceList_20191126_0559.csv 	| prime_manager 	| 20200103 	| 190        	| 0            	| 9            	| 0            	|
  | 56828b3f-d5a9-4590-ba80-538f30339739 	| 190          	| tx_prime_manager 	| 20191127 	| CPN_DeviceList_20191127_0559.csv 	| prime_manager 	| 20200103 	| 190        	| 0            	| 18           	| 0            	|
  | 31e2bbd9-ce02-43d7-992e-ca752e46834c 	| 189          	| tx_prime_manager 	| 20191128 	| CPN_DeviceList_20191128_0559.csv 	| prime_manager 	| 20200103 	| 189        	| 0            	| 5            	| 1            	|
  | f1cae642-ab6f-4cd8-a901-51c8135f5ceb 	| 189          	| tx_prime_manager 	| 20191129 	| CPN_DeviceList_20191129_0559.csv 	| prime_manager 	| 20200103 	| 189        	| 0            	| 15           	| 0            	|
  | 2c0d0f6b-e6fe-442c-bc0d-950020b21285 	| 189          	| tx_prime_manager 	| 20191130 	| CPN_DeviceList_20191130_0559.csv 	| prime_manager 	| 20200103 	| 189        	| 0            	| 7            	| 0            	|
  | 34614f67-9124-4152-92f1-c5b0bc488e10 	| 189          	| tx_prime_manager 	| 20191201 	| CPN_DeviceList_20191201_0559.csv 	| prime_manager 	| 20200103 	| 189        	| 0            	| 2            	| 0            	|
  | 837bbfe3-1e22-425b-86a3-c3315ae7707e 	| 189          	| tx_prime_manager 	| 20191202 	| CPN_DeviceList_20191202_0559.csv 	| prime_manager 	| 20200103 	| 189        	| 0            	| 3            	| 0            	|
  | 30847f6f-1190-4eaf-a707-2fbe16f059f9 	| 189          	| tx_prime_manager 	| 20191203 	| CPN_DeviceList_20191203_0559.csv 	| prime_manager 	| 20200103 	| 189        	| 0            	| 5            	| 0            	|
  | a4a57e0a-86f6-461d-aacf-f62b315af6e2 	| 189          	| tx_prime_manager 	| 20191204 	| CPN_DeviceList_20191204_0559.csv 	| prime_manager 	| 20200103 	| 189        	| 0            	| 39           	| 0            	|
  | 23c237f3-822a-471b-a313-349adea6152b 	| 188          	| tx_prime_manager 	| 20191205 	| CPN_DeviceList_20191205_0559.csv 	| prime_manager 	| 20200103 	| 188        	| 0            	| 17           	| 4            	|
  | 6be33b0b-b615-4cb3-8331-9a226fb0774b 	| 188          	| tx_prime_manager 	| 20191206 	| CPN_DeviceList_20191206_0559.csv 	| prime_manager 	| 20200103 	| 188        	| 1            	| 12           	| 1            	|
  | 1e703787-9ceb-42db-acc2-96e777d88bbd 	| 188          	| tx_prime_manager 	| 20191207 	| CPN_DeviceList_20191207_0559.csv 	| prime_manager 	| 20200103 	| 188        	| 0            	| 12           	| 0            	|
  | 2ba7b83c-007f-4d96-8c12-4460ce90c450 	| 188          	| tx_prime_manager 	| 20191208 	| CPN_DeviceList_20191208_0559.csv 	| prime_manager 	| 20200103 	| 188        	| 0            	| 13           	| 0            	|
  | c58cffdc-28fc-429e-90f2-1587d1868853 	| 188          	| tx_prime_manager 	| 20191209 	| CPN_DeviceList_20191209_0559.csv 	| prime_manager 	| 20200103 	| 188        	| 0            	| 102          	| 0            	|
  | 6ad5e9c8-b278-48eb-af45-6c74a04ddec9 	| 187          	| tx_prime_manager 	| 20191210 	| CPN_DeviceList_20191210_0559.csv 	| prime_manager 	| 20200103 	| 187        	| 0            	| 113          	| 2            	|
  | 8abc7ad5-ff6d-4af8-aec5-5d1bc294bf2e 	| 187          	| tx_prime_manager 	| 20191211 	| CPN_DeviceList_20191211_0559.csv 	| prime_manager 	| 20200103 	| 187        	| 0            	| 19           	| 0            	|
  | 9be2d0f8-8758-49c7-97db-5ed54c2d7259 	| 187          	| tx_prime_manager 	| 20191212 	| CPN_DeviceList_20191212_0559.csv 	| prime_manager 	| 20200103 	| 187        	| 0            	| 14           	| 0            	|
  | f5166032-d2f6-4891-b80f-3e6a13a5aae9 	| 186          	| tx_prime_manager 	| 20191213 	| CPN_DeviceList_20191213_0559.csv 	| prime_manager 	| 20200103 	| 186        	| 0            	| 12           	| 1            	|
  | 22a375e1-d0ed-4460-a797-8b372a23c1d3 	| 186          	| tx_prime_manager 	| 20191214 	| CPN_DeviceList_20191214_0559.csv 	| prime_manager 	| 20200103 	| 186        	| 0            	| 0            	| 0            	|
  | e1128b89-e649-47ab-985a-d5e59ea26c5b 	| 186          	| tx_prime_manager 	| 20191215 	| CPN_DeviceList_20191215_0559.csv 	| prime_manager 	| 20200103 	| 186        	| 0            	| 0            	| 0            	|
  | fee011f2-08b4-4bd6-bc58-87dc844deacb 	| 186          	| tx_prime_manager 	| 20191216 	| CPN_DeviceList_20191216_0559.csv 	| prime_manager 	| 20200103 	| 186        	| 0            	| 76           	| 0            	|
  | f1ce1905-4b45-4adc-ba6d-ba2be570062f 	| 186          	| tx_prime_manager 	| 20191217 	| CPN_DeviceList_20191217_0559.csv 	| prime_manager 	| 20200103 	| 186        	| 0            	| 12           	| 0            	|
  | 86372ef5-b908-4e2e-9af3-a40efd809db0 	| 186          	| tx_prime_manager 	| 20191218 	| CPN_DeviceList_20191218_0559.csv 	| prime_manager 	| 20200103 	| 186        	| 0            	| 12           	| 0            	|
  | f54d8825-61d8-434a-b77f-a72d0e5fbbf3 	| 186          	| tx_prime_manager 	| 20191219 	| CPN_DeviceList_20191219_0559.csv 	| prime_manager 	| 20200103 	| 186        	| 0            	| 6            	| 0            	|
  | 51febc83-5fd9-4982-b8cf-995d0e5698c3 	| 186          	| tx_prime_manager 	| 20191220 	| CPN_DeviceList_20191220_0559.csv 	| prime_manager 	| 20200103 	| 186        	| 0            	| 0            	| 0            	|

  ## Componentes del procesos de ingestion

  1. **Ingestion y Serialización via NiFi**

    ![Prime Manager NiFi Vista General][img1]

    Pipeline Principal __Flujo Principal__

    ![Prime Manager NiFi Vista Subproceso][img2]

    Pipeline Subproceso __Flujo de Subproceso__

    ![Prime Manager NiFi Vista Lectura de Archivos][img3]

    Pipeline Lectura de Archivos __Lectura de Archivos__

    ![Prime Manager NiFi Vista Procesamiento][img4]

    Pipeline Lectura de Archivos __Procesamiento de Archivos__

  2. __Reglas de Estandarización del Esquema `Kite`__

    Las siguientes reglas se aplicarón para estandarizar el esquema:

    - Remover Caracteres especiales en el header.
    - Reemplazo de caracter _ por " " en el nombre del archivo.

  3. __Framework de Ingestión Automatizado__

    - Especificar parámetros del proceso kite:

      | Parámetro | Valor | Descripción|
      | ---------- | ---------- | ---------- |
      | parametro_01   | 91   | Valor de correspondiente al flujo Prime Manager   |

      Sentencia kite:

      ```
      ./rci_ingesta_generacion_avro.sh {parametro_01}
      ```

      Ejemplo:

      ```
      ./rci_ingesta_generacion_avro.sh 91
      ```

## Referencias al Framework de Ingestion

- [Framework de Ingestion](../Globales/ArquitecturaFrameworkIngestion/readme.md)

## Código Fuente Local

- [Codigo NiFi - NFR](NFR/)

## Código Fuente Globales

- [Codigo NiFi](../Globales/NIFICustomProcessorXLSX)
- [Codigo Spark](../Globales/SparkAxity)
- [Codigo Kite](../Globales/attdlkrci/readme.md)

[img1]: images/PRIME_MANAGER-nifi-00.png "Prime Manager NiFi vista general"
[img2]: images/PRIME_MANAGER-nifi-01.png "Prime Manager NiFi vista subproceso"
[img3]: images/PRIME_MANAGER-nifi-02.png "Prime Manager NiFi Lectura de Archivos"
[img4]: images/PRIME_MANAGER-nifi-03.png "Prime Manager NiFi Lectura de Archivos"


[imgEncabezado]:../Globales/ArquitecturaFrameworkIngestion/images/encabezado.png ""
