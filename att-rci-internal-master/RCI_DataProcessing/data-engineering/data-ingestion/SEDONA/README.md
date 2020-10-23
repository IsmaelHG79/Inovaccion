<a name="main"></a>  ![Encabezado](./images/encabezado.png)

----

# Documentación Data Ingestion para la fuente ATT **SEDONA**

Para esta fuente se documentan diferentes flujos de una sola fuente, esto debido a que existen diferentes archivos generados los cuales son los siguientes:

1. [NetworkElementSummary](#network)
2. [Inventory_report_Huawei](#huawei)
3. [Inventory_report_Nokia](#nokia)

En total son 3 diferentes tipos de archivos que se tienen que procesar y sera explicados con mas detalle en los siguientes apartados.

* __Vista Principal de Nifi para SEDONA__

    ![Sedona NiFi Main View][img1]
    *Pipeline General de __SEDONA__*

* __Vista Principal Flujo de Nifi para SEDONA__

    ![Sedona NiFi All Inventory View][img2]                        
    *Vista Flujo Principal Nifi __SEDONA__*

* __Vista Flujo de Nifi para SEDONA (Network, Huawei, Nokia)__

    ![Sedona NiFi All Inventory View][img3]                        
    *Vista Flujo de Detalle Principal Nifi __SEDONA__*

## Descripcion del *`FTP`*

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

<<<<<<< HEAD
Las rutas donde se hara un backup de los archivos que se procesaran para cada tema de la fuente SEDONA para despues procesarlos son las siguientes:

``` /FILES_SPLUNK/SEDONA/ingested/ ```

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481174)
=======
- El directorio de HDFS en donde se colocan los datos ingestados.
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

##### [Ir a Inicio](#main)

## <a name="network"></a> Network Element Summary

### Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA Sedona](/RCI_DataAnalysis/eda/Gestor_Sedona/README.md#descripcion)**

- **[dicciorario de datos]** La siguiente tabla muestra el resultado de ejecutar el siguiente comando: 
    
    ```
    describe formatted rci_network_db.tx_sedona_ne;
    ```

| col_name | data_type | comment |
|--------------------|-----------|-------------------------------------------------------------------------|
| system_name | string | Type inferred from 'kite' |
| ip_address | string | Type inferred from 'kite' |
| vendor | string | Type inferred from 'kite' |
| device_type | string | Type inferred from 'kite' |
| software_version | string | Type inferred from 'kite' |
| site_id | string | Type inferred from 'kite' |
| serial_number | string | Type inferred from 'kite' |

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

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA Sedona](/RCI_DataAnalysis/eda/Gestor_Sedona/README.md)
    
- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:
    
    ```
    show partitions rci_network_db.tx_sedona_ne;
    ```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|-------|--------|----------|--------|----------------------------------------------------------------------------------------------------|
| 2019 | 7 | 31 | 1288 | 1 | 413.28KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=7/day=31 |
| 2019 | 8 | 1 | 1288 | 1 | 413.28KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=8/day=1 |
| 2019 | 8 | 2 | 1288 | 1 | 413.28KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=8/day=2 |
| 2019 | 8 | 3 | 1288 | 1 | 413.28KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=8/day=3 |
| 2019 | 8 | 4 | 1288 | 1 | 413.28KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=8/day=4 |
| 2019 | 8 | 13 | 1288 | 1 | 413.28KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=8/day=13 |
| 2019 | 8 | 29 | 1288 | 1 | 413.33KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=8/day=29 |
| 2019 | 8 | 30 | 1288 | 1 | 413.34KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=8/day=30 |
| 2019 | 8 | 31 | 1288 | 1 | 413.34KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=8/day=31 |
| 2019 | 9 | 1 | 1288 | 1 | 413.34KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=1 |
| 2019 | 9 | 2 | 1288 | 1 | 413.34KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=2 |
| 2019 | 9 | 3 | 1288 | 1 | 413.34KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=3 |
| 2019 | 9 | 4 | 1288 | 1 | 413.34KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=4 |
| 2019 | 9 | 5 | 1288 | 1 | 413.35KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=5 |
| 2019 | 9 | 6 | 1288 | 1 | 413.37KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=6 |
| 2019 | 9 | 7 | 1288 | 1 | 413.38KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=7 |
| 2019 | 9 | 8 | 1288 | 1 | 413.40KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=8 |
| 2019 | 9 | 9 | 1288 | 1 | 413.40KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=9 |
| 2019 | 9 | 14 | 1288 | 1 | 413.43KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=14 |
| 2019 | 9 | 15 | 1288 | 1 | 413.43KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=15 |
| 2019 | 9 | 16 | 1288 | 1 | 413.43KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=16 |
| 2019 | 9 | 17 | 1288 | 1 | 413.40KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=17 |
| 2019 | 9 | 18 | 1288 | 1 | 413.43KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=18 |
| 2019 | 9 | 19 | 1288 | 1 | 413.43KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=19 |
| 2019 | 9 | 20 | 1288 | 1 | 413.45KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=9/day=20 |
| 2019 | 10 | 2 | 1288 | 1 | 413.52KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=2 |
| 2019 | 10 | 3 | 1288 | 1 | 413.52KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=3 |
| 2019 | 10 | 4 | 1288 | 1 | 413.52KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=4 |
| 2019 | 10 | 5 | 1288 | 1 | 413.52KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=5 |
| 2019 | 10 | 6 | 1288 | 1 | 413.52KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=6 |
| 2019 | 10 | 7 | 1288 | 1 | 413.52KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=7 |
| 2019 | 10 | 8 | 1288 | 1 | 413.52KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=8 |
| 2019 | 10 | 9 | 1288 | 1 | 413.52KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=9 |
| 2019 | 10 | 10 | 1288 | 1 | 413.52KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=10 |
| 2019 | 10 | 11 | 1288 | 1 | 413.54KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=11 |
| 2019 | 10 | 12 | 1288 | 1 | 413.57KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=12 |
| 2019 | 10 | 13 | 1288 | 1 | 413.57KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=13 |
| 2019 | 10 | 14 | 1288 | 1 | 413.57KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=14 |
| 2019 | 10 | 15 | 1288 | 1 | 413.57KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=15 |
| 2019 | 10 | 16 | 1288 | 1 | 413.57KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=16 |
| 2019 | 10 | 18 | 1288 | 1 | 413.58KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=18 |
| 2019 | 10 | 19 | 1288 | 1 | 413.58KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=19 |
| 2019 | 10 | 20 | 1288 | 1 | 413.58KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=20 |
| 2019 | 10 | 21 | 1288 | 1 | 413.58KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=10/day=21 |
| 2019 | 11 | 26 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=11/day=26 |
| 2019 | 11 | 27 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=11/day=27 |
| 2019 | 11 | 28 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=11/day=28 |
| 2019 | 11 | 29 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=11/day=29 |
| 2019 | 11 | 30 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=11/day=30 |
| 2019 | 12 | 1 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=1 |
| 2019 | 12 | 2 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=2 |
| 2019 | 12 | 10 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=10 |
| 2019 | 12 | 11 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=11 |
| 2019 | 12 | 12 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=12 |
| 2019 | 12 | 13 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=13 |
| 2019 | 12 | 14 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=14 |
| 2019 | 12 | 15 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=15 |
| 2019 | 12 | 16 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=16 |
| 2019 | 12 | 17 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=17 |
| 2019 | 12 | 18 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=18 |
| 2019 | 12 | 19 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=19 |
| 2019 | 12 | 20 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=20 |
| 2019 | 12 | 21 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=21 |
| 2019 | 12 | 22 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=22 |
| 2019 | 12 | 23 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=23 |
| 2019 | 12 | 24 | 1288 | 1 | 413.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/network/year=2019/month=12/day=24 |
| Total |  |  | 85008 | 66 | 26.65MB |  |  |

### Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Sedona NE NiFi General View][img4]             
    *Pipeline General View __SEDONA Network__*

    ![Sedona NE NiFi Flow General View][img0]      
    *Pipeline General Flow View __SEDONA Network__*

    ![Sedona NE NiFi Detail View][img5]      
    *Pipeline Detail View __SEDONA Network__*

2. **Reglas de estandarizacion del esquema**

    * Sobre el esquema se eliminaron caracteres para que se generara correctamente el esquema del archivo avro con la siguiente expresion regular:
    
     ```
     Valor de Busqueda: (?s)(^[^\n]*)(.*$)
     Expresion regular a ejecutar: ${'$1':replace(",\"1",",\"F_1"):replace(" ","_"):replace("[",""):replace("]",""):replace("-","")}$2
     ```

3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 12   | Valor de correspondiente al flujo de SEDONA NE  |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización: 
    
     ```
     sh rci_ingesta_generacion_avro.sh 12
     ```

##### [Ir a Inicio](#main)

## <a name="huawei"></a> Inventory Report Huawei

### Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA Sedona](/RCI_DataAnalysis/eda/Gestor_Sedona/README.md#descripcion)**

- **[dicciorario de datos]** La siguiente tabla muestra el resultado de ejecutar el siguiente comando: 
    
    ```
    describe formatted rci_network_db.tx_sedona_huawei;
    ``` 

| col_name | data_type | comment |
|--------------------|-----------|-------------------------------------------------------------------------|
| inventory_type | string | Type inferred from 'kite' |
| vendor | string | Type inferred from 'kite' |
| device_type | string | Type inferred from 'kite' |
| software_version | string | Type inferred from 'kite' |
| system_name | string | Type inferred from 'kite' |
| ip | string | Type inferred from 'kite' |
| site_id | string | Type inferred from 'kite' |
| longitude | string | Type inferred from 'kite' |
| latitude | string | Type inferred from 'kite' |
| shelf | string | Type inferred from 'kite' |
| card | string | Type inferred from 'kite' |
| sub_card | string | Type inferred from 'kite' |
| port | string | Type inferred from 'kite' |
| description | string | Type inferred from 'kite' |
| serial_number | string | Type inferred from 'kite' |
| part_number | string | Type inferred from 'kite' |
| speed | string | Type inferred from 'kite' |
| f_1g | string | Type inferred from 'kite' |
| f_10g | string | Type inferred from 'kite' |
| f_100g | string | Type inferred from 'kite' |
| l1 | string | Type inferred from 'kite' |
| summary | string | Type inferred from 'kite' |

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

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA Sedona](/RCI_DataAnalysis/eda/Gestor_Sedona/README.md)
    
- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:
    
    ```
    show partitions rci_network_db.tx_sedona_huawei;
    ```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|---------|--------|---------|--------|--------------------------------------------------------------------------------------------------|
| 2019 | 7 | 31 | 45969 | 1 | 17.79MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=7/day=31 |
| 2019 | 8 | 1 | 45993 | 1 | 17.80MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=8/day=1 |
| 2019 | 8 | 2 | 45968 | 1 | 17.79MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=8/day=2 |
| 2019 | 8 | 3 | 46015 | 1 | 17.81MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=8/day=3 |
| 2019 | 8 | 4 | 45972 | 1 | 17.79MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=8/day=4 |
| 2019 | 8 | 13 | 45962 | 1 | 17.79MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=8/day=13 |
| 2019 | 8 | 29 | 46312 | 1 | 17.93MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=8/day=29 |
| 2019 | 8 | 30 | 46314 | 1 | 17.93MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=8/day=30 |
| 2019 | 8 | 31 | 46314 | 1 | 17.93MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=8/day=31 |
| 2019 | 9 | 1 | 46314 | 1 | 17.93MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=1 |
| 2019 | 9 | 2 | 46314 | 1 | 17.93MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=2 |
| 2019 | 9 | 3 | 46314 | 1 | 17.93MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=3 |
| 2019 | 9 | 4 | 46313 | 1 | 17.93MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=4 |
| 2019 | 9 | 5 | 46372 | 1 | 17.95MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=5 |
| 2019 | 9 | 6 | 46371 | 1 | 17.95MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=6 |
| 2019 | 9 | 7 | 46432 | 1 | 17.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=7 |
| 2019 | 9 | 8 | 46432 | 1 | 17.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=8 |
| 2019 | 9 | 9 | 46432 | 1 | 17.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=9 |
| 2019 | 9 | 14 | 46552 | 1 | 18.03MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=14 |
| 2019 | 9 | 15 | 46551 | 1 | 18.03MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=15 |
| 2019 | 9 | 16 | 46551 | 1 | 18.03MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=16 |
| 2019 | 9 | 17 | 46551 | 1 | 18.03MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=17 |
| 2019 | 9 | 18 | 46582 | 1 | 18.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=18 |
| 2019 | 9 | 19 | 46655 | 1 | 18.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=19 |
| 2019 | 9 | 20 | 46683 | 1 | 18.08MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=9/day=20 |
| 2019 | 10 | 2 | 46657 | 1 | 18.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=2 |
| 2019 | 10 | 3 | 46659 | 1 | 18.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=3 |
| 2019 | 10 | 4 | 46659 | 1 | 18.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=4 |
| 2019 | 10 | 5 | 46660 | 1 | 18.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=5 |
| 2019 | 10 | 6 | 46661 | 1 | 18.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=6 |
| 2019 | 10 | 7 | 46662 | 1 | 18.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=7 |
| 2019 | 10 | 8 | 46661 | 1 | 18.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=8 |
| 2019 | 10 | 9 | 46659 | 1 | 18.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=9 |
| 2019 | 10 | 10 | 46652 | 1 | 18.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=10 |
| 2019 | 10 | 11 | 46652 | 1 | 18.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=11 |
| 2019 | 10 | 12 | 46655 | 1 | 18.08MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=12 |
| 2019 | 10 | 13 | 46655 | 1 | 18.08MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=13 |
| 2019 | 10 | 14 | 46658 | 1 | 18.08MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=14 |
| 2019 | 10 | 15 | 46657 | 1 | 18.08MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=15 |
| 2019 | 10 | 16 | 46656 | 1 | 18.08MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=16 |
| 2019 | 10 | 18 | 46649 | 1 | 18.08MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=18 |
| 2019 | 10 | 19 | 46680 | 1 | 18.09MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=19 |
| 2019 | 10 | 20 | 46690 | 1 | 18.09MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=20 |
| 2019 | 10 | 21 | 46692 | 1 | 18.09MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=10/day=21 |
| 2019 | 11 | 26 | 46795 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=11/day=26 |
| 2019 | 11 | 27 | 46794 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=11/day=27 |
| 2019 | 11 | 28 | 46792 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=11/day=28 |
| 2019 | 11 | 29 | 46792 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=11/day=29 |
| 2019 | 11 | 30 | 46793 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=11/day=30 |
| 2019 | 12 | 1 | 46792 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=1 |
| 2019 | 12 | 2 | 46792 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=2 |
| 2019 | 12 | 10 | 46791 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=10 |
| 2019 | 12 | 11 | 46790 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=11 |
| 2019 | 12 | 12 | 46793 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=12 |
| 2019 | 12 | 13 | 46792 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=13 |
| 2019 | 12 | 14 | 46793 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=14 |
| 2019 | 12 | 15 | 46794 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=15 |
| 2019 | 12 | 16 | 46794 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=16 |
| 2019 | 12 | 17 | 46796 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=17 |
| 2019 | 12 | 18 | 46796 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=18 |
| 2019 | 12 | 19 | 46794 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=19 |
| 2019 | 12 | 20 | 46793 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=20 |
| 2019 | 12 | 21 | 46796 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=21 |
| 2019 | 12 | 22 | 46795 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=22 |
| 2019 | 12 | 23 | 46795 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=23 |
| 2019 | 12 | 24 | 46795 | 1 | 18.13MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/nokia/year=2019/month=12/day=24 |
| Total |  |  | 3074269 | 66 | 1.16GB |  |  |

### Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Sedona HW NiFi General View][img6]             
    *Pipeline General View __SEDONA Huawei__*

    ![Sedona HW NiFi Flow General View][img0]      
    *Pipeline General Flow View __SEDONA Huawei__*

    ![Sedona HW NiFi Detail View][img7]      
    *Pipeline Detail View __SEDONA Huawei__*

2. **Reglas de estandarizacion del esquema**

    * Sobre el esquema se eliminaron caracteres para que se generara correctamente el esquema del archivo avro con la siguiente expresion regular:
    
     ```
     Valor de Busqueda: (?s)(^[^\n]*)(.*$)
     Expresion regular a ejecutar: ${'$1':replace(",\"1",",\"F_1"):replace(" ","_"):replace("[",""):replace("]",""):replace("-","")}$2
     ```

3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 14   | Valor de correspondiente al flujo de SEDONA Huawei  |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización: 
    
     ```
     sh rci_ingesta_generacion_avro.sh 14
     ```

##### [Ir a Inicio](#main)

## <a name="nokia"></a> Inventory Report Nokia

### Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA Sedona](/RCI_DataAnalysis/eda/Gestor_Sedona/README.md#descripcion)**

- **[dicciorario de datos]** La siguiente tabla muestra el resultado de ejecutar el siguiente comando: 
    
    ```
    describe formatted rci_network_db.tx_sedona_nokia;
    ``` 

| col_name | data_type | comment |
|--------------------|-----------|-------------------------------------------------------------------------|
| inventory_type | string | Type inferred from 'kite' |
| vendor | string | Type inferred from 'kite' |
| device_type | string | Type inferred from 'kite' |
| software_version | string | Type inferred from 'kite' |
| system_name | string | Type inferred from 'kite' |
| ip | string | Type inferred from 'kite' |
| site_id | string | Type inferred from 'kite' |
| longitude | string | Type inferred from 'kite' |
| latitude | string | Type inferred from 'kite' |
| shelf | string | Type inferred from 'kite' |
| card | string | Type inferred from 'kite' |
| sub_card | string | Type inferred from 'kite' |
| port | string | Type inferred from 'kite' |
| description | string | Type inferred from 'kite' |
| serial_number | string | Type inferred from 'kite' |
| part_number | string | Type inferred from 'kite' |
| speed | string | Type inferred from 'kite' |
| f_1g | string | Type inferred from 'kite' |
| f_10g | string | Type inferred from 'kite' |
| f_100g | string | Type inferred from 'kite' |
| l1 | string | Type inferred from 'kite' |
| summary | string | Type inferred from 'kite' |

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

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA Sedona](/RCI_DataAnalysis/eda/Gestor_Sedona/README.md)
    
- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:
    
    ```
    show partitions rci_network_db.tx_sedona_nokia;
    ```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|---------|--------|----------|--------|---------------------------------------------------------------------------------------------------|
| 2019 | 7 | 31 | 28228 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=7/day=31 |
| 2019 | 8 | 1 | 28228 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=8/day=1 |
| 2019 | 8 | 2 | 28228 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=8/day=2 |
| 2019 | 8 | 3 | 28227 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=8/day=3 |
| 2019 | 8 | 4 | 28227 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=8/day=4 |
| 2019 | 8 | 13 | 28226 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=8/day=13 |
| 2019 | 8 | 29 | 28223 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=8/day=29 |
| 2019 | 8 | 30 | 28223 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=8/day=30 |
| 2019 | 8 | 31 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=8/day=31 |
| 2019 | 9 | 1 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=1 |
| 2019 | 9 | 2 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=2 |
| 2019 | 9 | 3 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=3 |
| 2019 | 9 | 4 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=4 |
| 2019 | 9 | 5 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=5 |
| 2019 | 9 | 6 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=6 |
| 2019 | 9 | 7 | 28176 | 1 | 11.02MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=7 |
| 2019 | 9 | 8 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=8 |
| 2019 | 9 | 9 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=9 |
| 2019 | 9 | 14 | 28222 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=14 |
| 2019 | 9 | 15 | 28222 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=15 |
| 2019 | 9 | 16 | 28222 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=16 |
| 2019 | 9 | 18 | 28222 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=18 |
| 2019 | 9 | 19 | 28232 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=19 |
| 2019 | 9 | 20 | 28232 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=9/day=20 |
| 2019 | 10 | 2 | 28234 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=2 |
| 2019 | 10 | 3 | 28234 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=3 |
| 2019 | 10 | 4 | 28233 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=4 |
| 2019 | 10 | 5 | 28233 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=5 |
| 2019 | 10 | 6 | 28232 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=6 |
| 2019 | 10 | 7 | 28232 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=7 |
| 2019 | 10 | 8 | 28232 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=8 |
| 2019 | 10 | 9 | 28233 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=9 |
| 2019 | 10 | 10 | 28233 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=10 |
| 2019 | 10 | 11 | 28234 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=11 |
| 2019 | 10 | 12 | 28234 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=12 |
| 2019 | 10 | 13 | 28235 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=13 |
| 2019 | 10 | 14 | 28235 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=14 |
| 2019 | 10 | 15 | 28235 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=15 |
| 2019 | 10 | 16 | 28235 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=16 |
| 2019 | 10 | 18 | 28235 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=18 |
| 2019 | 10 | 19 | 28235 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=19 |
| 2019 | 10 | 20 | 28235 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=20 |
| 2019 | 10 | 21 | 28235 | 1 | 11.05MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=10/day=21 |
| 2019 | 11 | 26 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=11/day=26 |
| 2019 | 11 | 27 | 28223 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=11/day=27 |
| 2019 | 11 | 28 | 28223 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=11/day=28 |
| 2019 | 11 | 29 | 28223 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=11/day=29 |
| 2019 | 11 | 30 | 28223 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=11/day=30 |
| 2019 | 12 | 1 | 28223 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=1 |
| 2019 | 12 | 2 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=2 |
| 2019 | 12 | 10 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=10 |
| 2019 | 12 | 11 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=11 |
| 2019 | 12 | 12 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=12 |
| 2019 | 12 | 13 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=13 |
| 2019 | 12 | 14 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=14 |
| 2019 | 12 | 15 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=15 |
| 2019 | 12 | 16 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=16 |
| 2019 | 12 | 17 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=17 |
| 2019 | 12 | 18 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=18 |
| 2019 | 12 | 19 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=19 |
| 2019 | 12 | 20 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=20 |
| 2019 | 12 | 21 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=21 |
| 2019 | 12 | 22 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=22 |
| 2019 | 12 | 23 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=23 |
| 2019 | 12 | 24 | 28224 | 1 | 11.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/sedona/huawei/year=2019/month=12/day=24 |
| Total |  |  | 1834721 | 65 | 717.83MB |  |  |

### Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Sedona NK NiFi General View][img8]             
    *Pipeline General View __SEDONA Nokia__*

    ![Sedona NK NiFi Flow General View][img0]      
    *Pipeline General Flow View __SEDONA Nokia__*

    ![Sedona NK NiFi Detail View][img9]      
    *Pipeline Detail View __SEDONA Nokia__*

2. **Reglas de estandarizacion del esquema**

    * Sobre el esquema se eliminaron caracteres para que se generara correctamente el esquema del archivo avro con la siguiente expresion regular:
    
     ```
     Valor de Busqueda: (?s)(^[^\n]*)(.*$)
     Expresion regular a ejecutar: ${'$1':replace(",\"1",",\"F_1"):replace(" ","_"):replace("[",""):replace("]",""):replace("-","")}$2
     ```

3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 13   | Valor de correspondiente al flujo de SEDONA Nokia  |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización: 
    
     ```
     sh rci_ingesta_generacion_avro.sh 13
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
[img0]: images/sedona-nifi-00.png "Sedona NiFi General Flow View"
[img1]: images/sedona-nifi-01.png "Sedona NiFi Principal View"
[img2]: images/sedona-nifi-02.png "Sedona NiFi Main Flow View"
[img3]: images/sedona-nifi-03.png "Sedona NiFi Flows View"
[img4]: images/sedona-network-nifi-01.png "Sedona NiFi NE Main View"
[img5]: images/sedona-network-nifi-02.png "Sedona NiFi NE Detail View"
[img6]: images/sedona-huawei-nifi-01.png "Sedona NiFi HW Main View"
[img7]: images/sedona-huawei-nifi-02.png "Sedona NiFi HW Detail View"
[img8]: images/sedona-nokia-nifi-01.png "Sedona NiFi SW Main View"
[img9]: images/sedona-nokia-nifi-02.png "Sedona NiFi SW Detail View"