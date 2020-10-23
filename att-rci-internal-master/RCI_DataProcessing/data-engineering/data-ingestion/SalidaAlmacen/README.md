<a name="main"></a>  ![Encabezado](./images/encabezado.png)

----

# Documentación Data Ingestion para la fuente ATT **Salida de Almacen**

## Descripción del *`FTP`*

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

## Descripción de la fuentes de datos

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: **[Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)**

## Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA Salida Almacen](/RCI_DataAnalysis/eda/Salida_Almacen/README.md#descripcion)**
=======
- **[descripción]** Descripción basada en la documentación del EDA para esta fuente se encuentra descrita aqui **[Descripción EDA Salida Almacen](/RCI_DataAnalysis/eda/Salida_Almacen/README.md#descripcion)**
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

- **[dicciorario de datos]** La siguiente tabla muestra el resultado de ejecutar el siguiente comando: 
    
    `describe formatted rci_network_db.tx_wlog;` 
    
| col_name | data_type | comment |
|--------------------|-----------|------------------------------------------|
| id | string | Type inferred from 'kite' |
| organizacion | string | Type inferred from 'kite' |
| lpn_salida | string | Type inferred from 'kite' |
| num_pedido_att | string | Type inferred from 'kite' |
| num_pedido | string | Type inferred from 'kite' |
| sku_oracle | string | Type inferred from 'kite' |
| sku_descripcion | string | Type inferred from 'kite' |
| serie | string | Type inferred from 'kite' |
| activo | string | Type inferred from 'kite' |
| parte | string | Type inferred from 'kite' |
| cantidad | string | Type inferred from 'kite' |
| units | string | Type inferred from 'kite' |
| area_usuaria | string | Type inferred from 'kite' |
| control_serie | string | Type inferred from 'kite' |
| control_activo | string | Type inferred from 'kite' |
| site_name | string | Type inferred from 'kite' |
| site_id | string | Type inferred from 'kite' |
| proyecto | string | Type inferred from 'kite' |
| orden_compra | string | Type inferred from 'kite' |
| tipo_transporte | string | Type inferred from 'kite' |
| audit_cierre_embarque | string | Type inferred from 'kite' |

Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestión.

| col_name | data_type | comment |
|--------------------|-----------|------------------------------------------|
| filedate | bigint | Type inferred from 'kite' |
| filename | string | Type inferred from 'kite' |
| hash_id | string | Type inferred from 'kite' |
| sourceid | string | Type inferred from 'kite' |
| registry_state | string | Type inferred from 'kite' |
| datasetname | string | Type inferred from 'kite' |
| timestamp | bigint | Type inferred from 'kite' |
| transaction_status | string | Type inferred from 'kite' |

Para mas información consultar la siguiente documentación: **[Documentación EDA Salida Almacen](/RCI_DataAnalysis/eda/Salida_Almacen/README.md)**

- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:
    
    `show partitions rci_network_db.tx_wlog;`

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|-------|--------|----------|--------|---------------------------------------------------------------------------------|
| 2019 | 12 | 6 | 1955 | 1 | 882.46KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=6 |
| 2019 | 12 | 7 | 680 | 6 | 320.16KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=7 |
| 2019 | 12 | 8 | 2242 | 6 | 1.01MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=8 |
| 2019 | 12 | 9 | 733 | 6 | 345.40KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=9 |
| 2019 | 12 | 10 | 2716 | 6 | 1.21MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=10 |
| 2019 | 12 | 11 | 495 | 6 | 242.70KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=11 |
| 2019 | 12 | 12 | 2415 | 6 | 1.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=12 |
| 2019 | 12 | 13 | 1155 | 6 | 540.14KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=13 |
| 2019 | 12 | 14 | 1475 | 6 | 675.04KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=14 |
| 2019 | 12 | 15 | 907 | 6 | 426.24KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=15 |
| 2019 | 12 | 16 | 665 | 6 | 318.33KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=16 |
| 2019 | 12 | 17 | 412 | 6 | 204.80KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=17 |
| 2019 | 12 | 18 | 506 | 6 | 245.24KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=18 |
| 2019 | 12 | 19 | 997 | 6 | 470.42KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=19 |
| 2019 | 12 | 20 | 283 | 6 | 147.03KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=20 |
| 2019 | 12 | 21 | 1050 | 6 | 495.21KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=21 |
| 2019 | 12 | 22 | 162 | 6 | 90.67KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/wlog/year=2019/month=12/day=22 |
| Total |  |  | 18848 | 97 | 8.56MB |  |  |

- **[ejecuciones]**
    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:
    ```
    select * from rci_metadata_db.tx_rci_executions
    where table_name = 'tx_wlog';
    ```

| id_execution | table_name | dateload | avro_name | start_execution | end_execution | status | attempts |
|--------------|------------|----------|---------------------------------------------------------|---------------------|---------------------|--------|----------|
| 1 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191206_Report_06-12-2019.avro | 2019-12-23 19:38:45 | 2019-12-23 19:39:28 | 1 | 0 |
| 2 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191207_Report_07-12-2019.avro | 2019-12-23 19:39:33 | 2019-12-23 19:41:11 | 1 | 0 |
| 3 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191208_Report_08-12-2019.avro | 2019-12-23 19:41:15 | 2019-12-23 19:42:54 | 1 | 0 |
| 4 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191209_Report_09-12-2019.avro | 2019-12-23 19:42:59 | 2019-12-23 19:44:47 | 1 | 0 |
| 5 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191210_Report_10-12-2019.avro | 2019-12-23 19:44:52 | 2019-12-23 19:46:51 | 1 | 0 |
| 6 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191211_Report_11-12-2019.avro | 2019-12-23 19:46:56 | 2019-12-23 19:49:01 | 1 | 0 |
| 7 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191212_Report_12-12-2019.avro | 2019-12-23 19:49:05 | 2019-12-23 19:51:19 | 1 | 0 |
| 8 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191213_Report_13-12-2019.avro | 2019-12-23 19:51:24 | 2019-12-23 19:53:00 | 1 | 0 |
| 9 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191214_Report_14-12-2019.avro | 2019-12-23 19:53:05 | 2019-12-23 19:55:15 | 1 | 0 |
| 10 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191215_Report_15-12-2019.avro | 2019-12-23 19:55:20 | 2019-12-23 19:57:36 | 1 | 0 |
| 11 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191216_Report_16-12-2019.avro | 2019-12-23 19:57:40 | 2019-12-23 20:00:25 | 1 | 0 |
| 12 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191217_Report_17-12-2019.avro | 2019-12-23 20:00:30 | 2019-12-23 20:02:51 | 1 | 0 |
| 13 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191218_Report_18-12-2019.avro | 2019-12-23 20:02:56 | 2019-12-23 20:04:38 | 1 | 0 |
| 14 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191219_Report_19-12-2019.avro | 2019-12-23 20:04:43 | 2019-12-23 20:06:37 | 1 | 0 |
| 15 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191220_Report_20-12-2019.avro | 2019-12-23 20:06:41 | 2019-12-23 20:09:14 | 1 | 0 |
| 16 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191221_Report_21-12-2019.avro | 2019-12-23 20:09:18 | 2019-12-23 20:11:38 | 1 | 0 |
| 17 | tx_wlog | 20191223 | /data/RCI/raw/wlog/data/20191222_Report_22-12-2019.avro | 2019-12-23 20:11:43 | 2019-12-23 20:13:29 | 1 | 0 |

- **[cifras de control]**
    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    
    
    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_wlog'
    and dateload = 20191224
    order by filedate asc;
    ```

| uuid | rowprocessed | datasetname | filedate | filename | sourceid | dateload | read_count | insert_count | update_count | delete_count |
|--------------------------------------|--------------|-------------|----------|-----------------------|----------------|----------|------------|--------------|--------------|--------------|
| 434a331f-f61e-4701-aaec-9e0b60b8db22 | 1955 | tx_wlog | 20191206 | Report_06-12-2019.csv | Salida Almacen | 20191224 | 1955 | 1955 | 0 | 0 |
| 18cae7fd-38c6-4f1d-bfe9-f60306faafbc | 1275 | tx_wlog | 20191207 | Report_07-12-2019.csv | Salida Almacen | 20191224 | 1275 | 0 | 0 | 680 |
| 4b9d438c-91f0-4f6e-86cf-01bf3e7607e4 | 2019 | tx_wlog | 20191208 | Report_08-12-2019.csv | Salida Almacen | 20191224 | 2019 | 1493 | 0 | 749 |
| a6d9f606-e49f-4012-b21c-b835ee1963e4 | 1700 | tx_wlog | 20191209 | Report_09-12-2019.csv | Salida Almacen | 20191224 | 1700 | 207 | 0 | 526 |
| 51b30143-2c0c-46ec-ae56-0109b3f47fe0 | 1430 | tx_wlog | 20191210 | Report_10-12-2019.csv | Salida Almacen | 20191224 | 1430 | 1223 | 0 | 1493 |
| 0baaa870-0ae5-4a22-8111-2c4c8e9e464a | 1511 | tx_wlog | 20191211 | Report_11-12-2019.csv | Salida Almacen | 20191224 | 1511 | 288 | 0 | 207 |
| 2cd6292c-2a28-4331-8194-049d4ce2b7bc | 1614 | tx_wlog | 20191212 | Report_12-12-2019.csv | Salida Almacen | 20191224 | 1614 | 1259 | 0 | 1156 |
| 9c17b570-8a94-4723-a96e-5e8e4c8e2c5d | 2059 | tx_wlog | 20191213 | Report_13-12-2019.csv | Salida Almacen | 20191224 | 2059 | 800 | 0 | 355 |
| 55a048b7-0df5-43f1-8b17-3191753fb4ed | 1016 | tx_wlog | 20191214 | Report_14-12-2019.csv | Salida Almacen | 20191224 | 1016 | 216 | 0 | 1259 |
| 9c6f3bb0-f80f-4869-b1fa-1d0ea494dec3 | 323 | tx_wlog | 20191215 | Report_15-12-2019.csv | Salida Almacen | 20191224 | 323 | 107 | 0 | 800 |
| c56656c7-4c43-4370-87e7-2fa793033f6f | 556 | tx_wlog | 20191216 | Report_16-12-2019.csv | Salida Almacen | 20191224 | 556 | 449 | 0 | 216 |
| 24a3c711-a19f-4855-a282-be159fe17be1 | 754 | tx_wlog | 20191217 | Report_17-12-2019.csv | Salida Almacen | 20191224 | 754 | 305 | 0 | 107 |
| 07628d0a-145a-42e4-ad90-9b4d0699f5f4 | 362 | tx_wlog | 20191218 | Report_18-12-2019.csv | Salida Almacen | 20191224 | 362 | 57 | 0 | 449 |
| 988a08fa-f4a4-44d6-a0d9-37b607ef2181 | 1127 | tx_wlog | 20191219 | Report_19-12-2019.csv | Salida Almacen | 20191224 | 1127 | 881 | 0 | 116 |
| cda6945e-62a7-4984-b265-18320f5a08e5 | 1028 | tx_wlog | 20191220 | Report_20-12-2019.csv | Salida Almacen | 20191224 | 1028 | 92 | 0 | 191 |
| 6c82f8e2-9cf1-4e56-b8cb-4ebca27f4861 | 358 | tx_wlog | 20191221 | Report_21-12-2019.csv | Salida Almacen | 20191224 | 358 | 190 | 0 | 860 |
| 8f3c3258-aef2-4e0a-b745-b0c0f6eba52e | 196 | tx_wlog | 20191222 | Report_22-12-2019.csv | Salida Almacen | 20191224 | 196 | 0 | 0 | 162 |    


## Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Wlog NiFi General View][img1]
    *Pipeline General __Salida Almacen__*

    ![Wlog NiFi Main View][img2]                             
    *Pipeline Main __Salida Almacen__*

    ![Wlog NiFi Flow View][img3]      
    *Pipeline Flow __Salida Almacen__*

    ![Wlog NiFi Detail View][img4]      
    *Pipeline Detalle __Salida Almacen__*

2. **Reglas de estandarización del esquema**

    * Sobre el esquema se eliminaron caracteres para que se generara correctamente el esquema del archivo avro con la siguiente expresion regular:
    
     ```
     Valor de Busqueda: (?s)(^[^\n]*)(.*$)
     Expresion regular a ejecutar: ${'$1':replace(" ","_"):replace("[",""):replace("]",""):replace("-","")}$2
     ```

3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 44   | Valor de correspondiente al flujo de Salida Almacen (wlog)  |

   * Sintaxis del comando de ejecución del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización : 
    
     ```
     sh rci_ingesta_generacion_avro.sh 44
     ```

## Referencias al Framework de Ingestion

[Framework de Ingestion](../Globales/ArquitecturaFrameworkIngestion/readme.md)

## Codigo Fuente Local

- [Codigo NiFi - NFR](NFR/)

## Codigo Fuente Globales

- [Codigo NiFi](../Globales/NIFICustomProcessorXLSX/README.md)
- [Codigo Spark](../Globales/SparkAxity/README.md)
- [Codigo Kite](../Globales/attdlkrci/readme.md)

##### [Ir a Inicio](#main)

---

 [img1]: images/wlog-nifi-01.png "WLOG NiFi General View"
 [img2]: images/wlog-nifi-02.png "WLOG NiFi Main View"
 [img3]: images/wlog-nifi-03.png "WLOG NiFi Flow View"
 [img4]: images/wlog-nifi-04.png "WLOG NiFi Detail View"
 