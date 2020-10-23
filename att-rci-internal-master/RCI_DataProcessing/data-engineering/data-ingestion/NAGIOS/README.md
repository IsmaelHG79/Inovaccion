<a name="main"></a>  ![Encabezado](./images/encabezado.png)

----

# Documentación Data Ingestion para la fuente ATT **NAGIOS**

Para esta fuente se documentan diferentes flujos de una sola fuente, esto debido a que existen diferentes archivos generados los cuales son los siguientes:

1. [Hosts](#hots)
2. [Hosts Status](#status)

En total son 2 diferentes tipos de archivos que se tienen que procesar y sera explicados con mas detalle en los siguientes apartados.

* __Vista Principal de Nifi para NAGIOS__

    ![Nagios NiFi Main View][img1]    
    *Pipeline General de __NAGIOS__*

* __Vista Principal Flujo de Nifi para NAGIOS__

    ![Nagios NiFi All Inventory View][img2]                        
    *Vista Flujo Principal Nifi __NAGIOS__*


## Descripcion del *`FTP`*

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

##### [Ir a Inicio](#main)

## <a name="hots"></a> Archivo Host

### Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA NAGIOS](/RCI_DataAnalysis/eda/NAGIOS/README.md#descripcion)**

- **[dicciorario de datos]** La siguiente tabla muestra el resultado de ejecutar el siguiente comando: 
    
    ```
    describe formatted rci_network_db.tx_nagios_host;
    ``` 

| col_name | data_type | comment |
|--------------------|-----------|-------------------------------------------------------------------------|
| attributes_id | string | Type inferred from 'kite' |
| active_checks_enabled | string | Type inferred from 'kite' |
| address | string | Type inferred from 'kite' |
| alias | string | Type inferred from 'kite' |
| check_interval | string | Type inferred from 'kite' |
| config_type | string | Type inferred from 'kite' |
| display_name | string | Type inferred from 'kite' |
| first_notification_delay | string | Type inferred from 'kite' |
| host_name | string | Type inferred from 'kite' |
| icon_image | string | Type inferred from 'kite' |
| instance_id | string | Type inferred from 'kite' |
| is_active | string | Type inferred from 'kite' |
| max_check_attempts | string | Type inferred from 'kite' |
| notification_interval | string | Type inferred from 'kite' |
| notifications_enabled | string | Type inferred from 'kite' |
| passive_checks_enabled | string | Type inferred from 'kite' |
| retry_interval | string | Type inferred from 'kite' |
| statusmap_image | string | Type inferred from 'kite' |

Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestion.

| col_name | data_type | comment |
|--------------------|-----------|-------------------------------------------------------------------------|
| filedate | bigint | Type inferred from 'kite' |
| filename | string | Type inferred from 'kite' |
| hash_id | string | Type inferred from 'kite' |
| sourceid | string | Type inferred from 'kite' |
| registry_state | string | Type inferred from 'kite' |
| datasetname | string | Type inferred from 'kite' |
| timestamp | bigint | Type inferred from 'kite' |
| transaction_status | string | Type inferred from 'kite' |

Para mas informacion consultar la siguiente documentacion: **[Documentacion EDA NAGIOS](/RCI_DataAnalysis/eda/NAGIOS/README.md)**
    
- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:
    
    ```
    show partitions rci_network_db.tx_nagios_host;
    ```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|-------|--------|----------|--------|----------------------------------------------------------------------------------------|
| 2019 | 10 | 30 | 764 | 1 | 254.48KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/host/year=2019/month=10/day=30 |
| 2019 | 11 | 14 | 2 | 2 | 5.94KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/host/year=2019/month=11/day=14 |
| 2019 | 12 | 10 | 2 | 2 | 5.90KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/host/year=2019/month=12/day=10 |
| 2019 | 12 | 14 | 4 | 2 | 6.58KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/host/year=2019/month=12/day=14 |
| 2019 | 12 | 20 | 69 | 6 | 39.34KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/host/year=2019/month=12/day=20 |
| 2019 | 12 | 24 | 4 | 4 | 11.88KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/host/year=2019/month=12/day=24 |
| Total |  |  | 845 | 17 | 324.11KB |  |  |


### Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Nagios Host NiFi General View][img4]             
    *Pipeline General View __NAGIOS HOST__*

    ![Nagios Host NiFi Detail View][img5]      
    *Pipeline Detail View __NAGIOS HOST__*

2. **Reglas de estandarizacion del esquema**

    * Sobre el esquema se eliminaron caracteres para que se generara correctamente el esquema del archivo avro con la siguiente expresion regular:
    
     ```
     Valor de Busqueda: (?s)(^[^\n]*)(.*$)
     Expresion regular a ejecutar: ${'$1':replace(" ","_"):replace(" ","_"):replace("[",""):replace("]",""):replace("-",""):replace("\"_","\""):replace("@","")}$2
     ```

3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 92   | Valor de correspondiente al flujo de NAGIOS Host  |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización : 
    
     ```
     sh rci_ingesta_generacion_avro.sh 92
     ```

##### [Ir a Inicio](#main)

## <a name="status"></a> Archivo Host Status

### Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA NAGIOS](/RCI_DataAnalysis/eda/NAGIOS/README.md#descripcion)**

- **[dicciorario de datos]** La siguiente tabla muestra el resultado de ejecutar el siguiente comando: 
    
    ```
    describe formatted rci_network_db.tx_nagios_status;
    ``` 

| col_name | data_type | comment |
|---------------------|-----------|-------------------------------------------------------------------------|
| attributes_id | string | Type inferred from 'kite' |
| acknowledgement_type | string | Type inferred from 'kite' |
| active_checks_enabled | string | Type inferred from 'kite' |
| address | string | Type inferred from 'kite' |
| alias | string | Type inferred from 'kite' |
| check_command | string | Type inferred from 'kite' |
| check_timeperiod_id | string | Type inferred from 'kite' |
| check_type | string | Type inferred from 'kite' |
| current_check_attempt | string | Type inferred from 'kite' |
| current_notification_number | string | Type inferred from 'kite' |
| current_state | string | Type inferred from 'kite' |
| display_name | string | Type inferred from 'kite' |
| event_handler_enabled | string | Type inferred from 'kite' |
| execution_time | string | Type inferred from 'kite' |
| flap_detection_enabled | string | Type inferred from 'kite' |
| has_been_checked | string | Type inferred from 'kite' |
| host_id | string | Type inferred from 'kite' |
| icon_image | string | Type inferred from 'kite' |
| instance_id | string | Type inferred from 'kite' |
| is_flapping | string | Type inferred from 'kite' |
| last_check | string | Type inferred from 'kite' |
| last_hard_state | string | Type inferred from 'kite' |
| last_hard_state_change | string | Type inferred from 'kite' |
| last_notification | string | Type inferred from 'kite' |
| last_state_change | string | Type inferred from 'kite' |
| last_time_down | string | Type inferred from 'kite' |
| last_time_unreachable | string | Type inferred from 'kite' |
| last_time_up | string | Type inferred from 'kite' |
| latency | string | Type inferred from 'kite' |
| max_check_attempts | string | Type inferred from 'kite' |
| modified_host_attributes | string | Type inferred from 'kite' |
| name | string | Type inferred from 'kite' |
| next_check | string | Type inferred from 'kite' |
| next_notification | string | Type inferred from 'kite' |
| no_more_notifications | string | Type inferred from 'kite' |
| normal_check_interval | string | Type inferred from 'kite' |
| notifications_enabled | string | Type inferred from 'kite' |
| obsess_over_host | string | Type inferred from 'kite' |
| passive_checks_enabled | string | Type inferred from 'kite' |
| percent_state_change | string | Type inferred from 'kite' |
| performance_data | string | Type inferred from 'kite' |
| problem_acknowledged | string | Type inferred from 'kite' |
| process_performance_data | string | Type inferred from 'kite' |
| retry_check_interval | string | Type inferred from 'kite' |
| scheduled_downtime_depth | string | Type inferred from 'kite' |
| should_be_scheduled | string | Type inferred from 'kite' |
| state_type | string | Type inferred from 'kite' |
| status_text | string | Type inferred from 'kite' |
| status_update_time | string | Type inferred from 'kite' |

Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestion.

| col_name | data_type | comment |
|--------------------|-----------|-------------------------------------------------------------------------|
| filedate | bigint | Type inferred from 'kite' |
| filename | string | Type inferred from 'kite' |
| hash_id | string | Type inferred from 'kite' |
| sourceid | string | Type inferred from 'kite' |
| registry_state | string | Type inferred from 'kite' |
| datasetname | string | Type inferred from 'kite' |
| timestamp | bigint | Type inferred from 'kite' |
| transaction_status | string | Type inferred from 'kite' |

Para mas informacion consultar la siguiente documentacion: **[Documentacion EDA NAGIOS](/RCI_DataAnalysis/eda/NAGIOS/README.md)**
    
- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:
    
    ```
    show partitions rci_network_db.tx_nagios_status;
    ```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|-------|--------|----------|--------|------------------------------------------------------------------------------------------|
| 2019 | 10 | 30 | 764 | 1 | 582.12KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=10/day=30 |
| 2019 | 10 | 31 | 764 | 6 | 612.77KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=10/day=31 |
| 2019 | 11 | 14 | 2294 | 6 | 1.73MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=14 |
| 2019 | 11 | 15 | 1532 | 6 | 1.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=15 |
| 2019 | 11 | 16 | 1532 | 6 | 1.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=16 |
| 2019 | 11 | 17 | 765 | 6 | 612.17KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=17 |
| 2019 | 11 | 18 | 765 | 6 | 612.20KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=18 |
| 2019 | 11 | 19 | 766 | 6 | 614.45KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=19 |
| 2019 | 11 | 20 | 3828 | 6 | 2.86MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=20 |
| 2019 | 11 | 21 | 1532 | 6 | 1.17MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=21 |
| 2019 | 11 | 22 | 765 | 6 | 613.79KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=22 |
| 2019 | 11 | 23 | 766 | 6 | 613.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=23 |
| 2019 | 11 | 24 | 765 | 6 | 612.28KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=24 |
| 2019 | 11 | 25 | 765 | 6 | 612.27KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=25 |
| 2019 | 11 | 26 | 765 | 6 | 612.25KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=26 |
| 2019 | 11 | 27 | 765 | 6 | 612.22KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=27 |
| 2019 | 11 | 28 | 765 | 6 | 612.28KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=28 |
| 2019 | 11 | 29 | 765 | 6 | 613.78KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=29 |
| 2019 | 11 | 30 | 7653 | 6 | 5.68MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=11/day=30 |
| 2019 | 12 | 1 | 765 | 6 | 612.20KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=1 |
| 2019 | 12 | 2 | 765 | 6 | 612.22KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=2 |
| 2019 | 12 | 3 | 3062 | 6 | 2.29MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=3 |
| 2019 | 12 | 4 | 1532 | 6 | 1.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=4 |
| 2019 | 12 | 5 | 1532 | 6 | 1.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=5 |
| 2019 | 12 | 6 | 1532 | 6 | 1.17MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=6 |
| 2019 | 12 | 7 | 765 | 6 | 613.74KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=7 |
| 2019 | 12 | 8 | 766 | 6 | 612.96KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=8 |
| 2019 | 12 | 9 | 765 | 6 | 612.18KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=9 |
| 2019 | 12 | 10 | 3830 | 6 | 2.86MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=10 |
| 2019 | 12 | 11 | 1536 | 6 | 1.17MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=11 |
| 2019 | 12 | 12 | 768 | 6 | 615.81KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=12 |
| 2019 | 12 | 13 | 771 | 6 | 617.90KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=13 |
| 2019 | 12 | 14 | 3079 | 6 | 2.30MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=14 |
| 2019 | 12 | 15 | 771 | 6 | 616.57KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=15 |
| 2019 | 12 | 16 | 771 | 6 | 616.54KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=16 |
| 2019 | 12 | 17 | 3086 | 6 | 2.31MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=17 |
| 2019 | 12 | 18 | 1544 | 6 | 1.17MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=18 |
| 2019 | 12 | 19 | 1544 | 6 | 1.17MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=19 |
| 2019 | 12 | 20 | 1613 | 6 | 1.22MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=20 |
| 2019 | 12 | 21 | 841 | 6 | 670.35KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=21 |
| 2019 | 12 | 22 | 840 | 6 | 669.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=22 |
| 2019 | 12 | 23 | 840 | 6 | 669.64KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=23 |
| 2019 | 12 | 24 | 4207 | 6 | 3.14MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=24 |
| 2019 | 12 | 25 | 1690 | 6 | 1.28MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=25 |
| 2019 | 12 | 26 | 844 | 6 | 672.61KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=26 |
| 2019 | 12 | 27 | 844 | 6 | 672.62KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/nagios/status/year=2019/month=12/day=27 |
| Total |  |  | 69219 | 271 | 52.59MB |  |  |


### Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Nagios Status NiFi General View][img6]             
    *Pipeline General View __NAGIOS Status__*

    ![Nagios Status NiFi Detail View][img7]      
    *Pipeline Detail View __NAGIOS Status__*

2. **Reglas de estandarizacion del esquema**

    * Sobre el esquema se eliminaron caracteres para que se generara correctamente el esquema del archivo avro con la siguiente expresion regular:
    
     ```
     Valor de Busqueda: (?s)(^[^\n]*)(.*$)
     Expresion regular a ejecutar: ${'$1':replace(" ","_"):replace(" ","_"):replace("[",""):replace("]",""):replace("-",""):replace("\"_","\""):replace("@","")}$2
     ```

3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 93   | Valor de correspondiente al flujo de NAGIOS Status  |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización : 
    
     ```
     sh rci_ingesta_generacion_avro.sh 93
     ```

##### [Ir a Inicio](#main)

## Referencias al Framework de Ingestion

[Framework de Ingestion](../Globales/ArquitecturaFrameworkIngestion/readme.md)

## Codigo Fuente Local

- [Codigo NiFi - NFR](NFR/)

## Codigo Fuente Globales

- [Codigo NiFi](../Globales/NIFICustomProcessorXLSX/README.md)
- [Codigo Spark](../Globales/SparkAxity/README.md)
- [Codigo Kite](../Globales/attdlkrci/readme.md)
---
[img1]: images/nagios-nifi-01.png "Nagios NiFi Principal View"
[img2]: images/nagios-nifi-02.png "Nagios NiFi Main Flow View"
[img4]: images/nagios-nifi-host-01.png "Nagios NiFi Host Main View"
[img5]: images/nagios-nifi-host-02.png "Nagios NiFi Host Detail View"
[img6]: images/nagios-nifi-status-01.png "Nagios NiFi Status Main View"
[img7]: images/nagios-nifi-status-02.png "Nagios NiFi Status Detail View"

