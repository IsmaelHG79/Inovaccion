<a name="main"></a>  ![Encabezado](./images/encabezado.png)

----

# Documentación Data Ingestion para la fuente ATT **NetCM**

Para esta fuente se documentan diferentes tres vertientes del gestor NETCM, para los cuales se obtienen diferentes reportes los cuales se ingestaron y son los siguientes:

1. __[NetCM CISCO](#cisco)__
    * Cisco EPNM - BackHaul Sites MAN
    * Cisco EPNM - Audit Specific Sit
    * Cisco EPNM - Node Inventory wit
    * Cisco EPNM - Inventory Site Rep
    * Cisco EPNM - Audit ALL Sites MA
    * Cisco EPNM - Audit BackHaul All
    * Cisco EPNM - Audit ALL sites NO
    * Cisco SPGW - ASR hardware inven
2. __[NetCM ERICSSON](#ericsson)__
    * Ericsson BTS - Antenna Serial N
    * Ericsson UMTS - NODEB Serial Un
    * Ericsson UMTS - RNC Serial Numb
    * Ericsson LTE - ENODEB Board Ser
    * Ericsson GSM - BTS Board Serial
    * Ericsson MME - HW Status
3. __[NetCM HUAWEI](#huawei)__
    * Huawei - Antenna Serial Number
    * Huawei LTE - ENODEB Board Seria
    * Huawei UMTS - RNC Elabel Board
    * Huawei UMTS - NODEB Board Seria
    * Huawei MME  Platform Inventory
    * Huawei MME - Inventory Board
    * Huawei UMTS - Cell State Audit
    * Huawei BTS - Antenna Serial Num
    * Huawei CO MPT BTS - MBTS Board

En la siguiente tabla se muestra la relacion de archivos, reportes y tabla a ingestar.

| Tabla                    | Hoja de Cálculo                 | Archivo Excel                                                |
|--------------------------|---------------------------------|--------------------------------------------------------------|
| tx_netcm_cisco_epn       | Cisco EPNM - Audit ALL Sites MA | Email - Cisco EPN Node Inventory.xlsx                        |
| tx_netcm_cisco_epn       | Cisco EPNM - Audit ALL Sites MA | Email - Cisco EPN Node Inventory_DD-MM-YYYY_NNNNNN.xlsx      |
| tx_netcm_cisco_epn       | Cisco EPNM - Audit ALL sites NO | Email - Cisco EPN Node Inventory.xlsx                        |
| tx_netcm_cisco_epn       | Cisco EPNM - Audit ALL sites NO | Email - Cisco EPN Node Inventory_DD-MM-YYYY_NNNNNN.xlsx      |
| tx_netcm_cisco_epn       | Cisco EPNM - Audit BackHaul All | Email - Cisco EPN Node Inventory.xlsx                        |
| tx_netcm_cisco_epn       | Cisco EPNM - Audit BackHaul All | Email - Cisco EPN Node Inventory_DD-MM-YYYY_NNNNNN.xlsx      |
| tx_netcm_cisco_epn       | Cisco EPNM - Audit Specific Sit | Email - Cisco EPN Node Inventory.xlsx                        |
| tx_netcm_cisco_epn       | Cisco EPNM - Audit Specific Sit | Email - Cisco EPN Node Inventory_DD-MM-YYYY_NNNNNN.xlsx      |
| tx_netcm_cisco_epn       | Cisco EPNM - BackHaul Sites MAN | Email - Cisco EPN Node Inventory.xlsx                        |
| tx_netcm_cisco_epn       | Cisco EPNM - BackHaul Sites MAN | Email - Cisco EPN Node Inventory_DD-MM-YYYY_NNNNNN.xlsx      |
| tx_netcm_cisco_epn       | Cisco EPNM - Node Inventory wit | Email - Cisco EPN Node Inventory.xlsx                        |
| tx_netcm_cisco_epn       | Cisco EPNM - Node Inventory wit | Email - Cisco EPN Node Inventory_DD-MM-YYYY_NNNNNN.xlsx      |
| tx_netcm_cisco_inv       | Cisco EPNM - Inventory Site Rep | Email - Cisco EPN Node Inventory.xlsx                        |
| tx_netcm_cisco_inv       | Cisco EPNM - Inventory Site Rep | Email - Cisco EPN Node Inventory_DD-MM-YYYY_NNNNNN.xlsx      |
| tx_netcm_cisco_asr       | Cisco SPGW - ASR hardware inven | EMAIL-PS CORE.xlsx                                           |
| tx_netcm_cisco_asr       | Cisco SPGW - ASR hardware inven | Email - All Inventory Send DD-MM-YYYY NNNNNN.xlsx            |
| tx_netcm_huawei_antena   | Huawei - Antenna Serial Number  | Email - Huawei Antenna Inventory Information.xlsx            |
| tx_netcm_huawei_enodeb   | Huawei LTE - ENODEB Board Seria | Email - Huawei UMTS and LTE Inventory Information.xlsx       |
| tx_netcm_huawei_enodeb   | Huawei LTE - ENODEB Board Seria | Email - All Inventory Send DD-MM-YYYY NNNNNN.xlsx            |
| tx_netcm_huawei_nodeb    | Huawei UMTS - NODEB Board Seria | Email - Huawei UMTS and LTE Inventory Information.xlsx       |
| tx_netcm_huawei_rnc      | Huawei UMTS - RNC Elabel Board  | Email - Huawei UMTS and LTE Inventory Information.xlsx       |
| tx_netcm_huawei_rnc      | Huawei UMTS - RNC Elabel Board  | Email - All Inventory Send DD-MM-YYYY NNNNNN.xlsx            |
| tx_netcm_huawei_bts      | Huawei BTS - Antenna Serial Num | Email - All Inventory Send DD-MM-YYYY NNNNNN.xlsx            |
| tx_netcm_huawei_mmepi    | Huawei MME  Platform Inventory  | EMAIL-PS CORE.xlsx                                           |
| tx_netcm_huawei_mmepi    | Huawei MME  Platform Inventory  | Email - All Inventory Send DD-MM-YYYY NNNNNN.xlsx            |
| tx_netcm_huawei_mmeib    | Huawei MME - Inventory Board    | EMAIL-PS CORE.xlsx                                           |
| tx_netcm_huawei_mmeib    | Huawei MME - Inventory Board    | Email - All Inventory Send DD-MM-YYYY NNNNNN.xlsx            |
| tx_netcm_huawei_cell     | Huawei UMTS - Cell State Audit  | Email - All Inventory Send 3 DD-MM-YYYY NNNNNN.xlsx          |
| tx_netcm_huawei_mbts     | Huawei CO MPT BTS - MBTS Board  | Email - Huawei CO MPT BTS Board Serial Number.xlsx           |
| tx_netcm_ericsson_antena | Ericsson BTS - Antenna Serial N | Email - Ericsson UMTS Antenna Serial Number Information.xlsx |
| tx_netcm_ericsson_antena | Ericsson BTS - Antenna Serial N | Email - All Inventory Send 2 DD-MM-YYYY NNNNNN.xlsx          |
| tx_netcm_ericsson_board  | Ericsson GSM - BTS Board Serial | Email - Ericsson GSM Inventory Information.xlsx              |
| tx_netcm_ericsson_board  | Ericsson GSM - BTS Board Serial | Email - All Inventory Send 2 DD-MM-YYYY NNNNNN.xlsx          |
| tx_netcm_ericsson_enodeb | Ericsson LTE - ENODEB Board Ser | Email - Ericsson UMTS and LTE Inventory Information.xlsx     |
| tx_netcm_ericsson_enodeb | Ericsson LTE - ENODEB Board Ser | Email - All Inventory Send 2 DD-MM-YYYY NNNNNN.xlsx          |
| tx_netcm_ericsson_nodeb  | Ericsson UMTS - NODEB Serial Un | Email - Ericsson UMTS and LTE Inventory Information.xlsx     |
| tx_netcm_ericsson_rnc    | Ericsson UMTS - RNC Serial Numb | Email - Ericsson UMTS and LTE Inventory Information.xlsx     |
| tx_netcm_ericsson_hw     | Ericsson MME - HW Status        | EMAIL-PS CORE.xlsx                                           |
| tx_netcm_ericsson_hw     | Ericsson MME - HW Status        | Email - All Inventory Send 2 DD-MM-YYYY NNNNNN.xlsx          |

* __Vista Principal de Nifi para NetCM__

    ![NetCM NiFi Main View][img01]       
    *Vista Principal __NetCM__*

* __Vista General de Nifi para NetCM__

    ![NetCM NiFi All General View][img02]          
    *Vista Principal __NetCM__*

## Descripcion del *`FTP`*

El diseño del Data Lake se detalla en el documento __[Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776)__, en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

<<<<<<< HEAD
* Cisco EPN : ``` /FILES_SPLUNK/INVENTARIO/netcm/netcmexcel/Cisco_EPN/ingested/ ```
* All Inventory : ``` /FILES_SPLUNK/INVENTARIO/netcm/netcmexcel/All_Inventory/ingested/```
* Huawei : ``` /FILES_SPLUNK/INVENTARIO/netcm/netcmexcel/Huawei/ingested/```

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
=======
- El directorio de HDFS en donde se colocan los datos ingestados.
>>>>>>> f17ccfc48c11b46af8c37c2b5c513a6316537378

##### [Ir a Inicio](#main)

## <a name="cisco"></a> NetCM Cisco

### Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA NETCM](/RCI_DataAnalysis/eda/Gestor_NETCM/README.md#descripcion)**

- **[dicciorario de datos]** La siguientes tablas muestran el resultado de ejecutar el siguiente comando: 

    * __tx_netcm_cisco_epn__
    
    ```
    describe formatted rci_network_db.tx_netcm_cisco_epn;
    ```
    
    | col_name            | data_type | comment                   |
    |---------------------|-----------|---------------------------|
    | location            | string    | Type inferred from 'kite' |
    | devicename          | string    | Type inferred from 'kite' |
    | adminstatus         | string    | Type inferred from 'kite' |
    | ipaddress           | string    | Type inferred from 'kite' |
    | softwaretype        | string    | Type inferred from 'kite' |
    | managementstatus10  | string    | Type inferred from 'kite' |
    | sheet_name          | string    | Type inferred from 'kite' |
    | managementstatus    | string    | Type inferred from 'kite' |
    | devicetypeparameter | string    | Type inferred from 'kite' |
    | creationtime        | string    | Type inferred from 'kite' |
    | reachability        | string    | Type inferred from 'kite' |
    | productfamily       | string    | Type inferred from 'kite' |
    
    * __tx_netcm_cisco_inv__
    
    ```
    describe formatted rci_network_db.tx_netcm_cisco_inv;
    ```
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | nodename           | string    | Type inferred from 'kite' |
    | technology         | string    | Type inferred from 'kite' |
    | omip               | string    | Type inferred from 'kite' |
    | manufacturerpartnr | string    | Type inferred from 'kite' |
    | serial_number      | string    | Type inferred from 'kite' |
    | sheet_name         | string    | Type inferred from 'kite' |
    
    * __tx_netcm_cisco_asr__
    
    ```
    describe formatted rci_network_db.tx_netcm_cisco_asr;
    ```
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | node               | string    | Type inferred from 'kite' |
    | slot               | string    | Type inferred from 'kite' |
    | type               | string    | Type inferred from 'kite' |
    | part_number        | string    | Type inferred from 'kite' |
    | product_id         | string    | Type inferred from 'kite' |
    | version_id         | string    | Type inferred from 'kite' |
    | serial_num         | string    | Type inferred from 'kite' |
    | clei_code          | string    | Type inferred from 'kite' |
    | date               | string    | Type inferred from 'kite' |
    | sheet_name         | string    | Type inferred from 'kite' |
    
    * Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestion.
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | filedate           | bigint    | Type inferred from 'kite' |
    | filename           | string    | Type inferred from 'kite' |
    | hash_id            | string    | Type inferred from 'kite' |
    | sourceid           | string    | Type inferred from 'kite' |
    | registry_state     | string    | Type inferred from 'kite' |
    | datasetname        | string    | Type inferred from 'kite' |
    | timestamp          | bigint    | Type inferred from 'kite' |
    | transaction_status | string    | Type inferred from 'kite' |
    
    * Para mas informacion consultar la siguiente documentacion: __[Documentacion EDA NETCM](/RCI_DataAnalysis/eda/Gestor_NETCM/README.md)__
    
- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:

    * __tx_netcm_cisco_epn__
    
    ```
    show partitions rci_network_db.tx_netcm_cisco_epn;
    ```
    
    | year  | month | #Rows  | #Files | Size     | Format | Location                                                                                     |
    |-------|-------|--------|--------|----------|--------|----------------------------------------------------------------------------------------------|
    | 2019  | 9     | 62442  | 1      | 24.16MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/cisco/epn/year=2019/month=9  |
    | 2019  | 10    | 91524  | 1      | 35.42MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/cisco/epn/year=2019/month=10 |
    | 2019  | 11    | 96560  | 1      | 39.28MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/cisco/epn/year=2019/month=11 |
    | 2019  | 12    | 131034 | 1      | 53.89MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/cisco/epn/year=2019/month=12 |
    | 2020  | 1     | 91940  | 1      | 36.63MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/cisco/epn/year=2020/month=1  |
    | Total |       | 473500 | 5      | 189.39MB |        |                                                                                              |
    
    * __tx_netcm_cisco_inv__
    
    ```
    show partitions rci_network_db.tx_netcm_cisco_inv;
    ```
    
    | year  | month | #Rows  | #Files | Size    | Format | Location                                                                                     |
    |-------|-------|--------|--------|---------|--------|----------------------------------------------------------------------------------------------|
    | 2019  | 9     | 5690   | 1      | 1.65MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/cisco/inv/year=2019/month=9  |
    | 2019  | 10    | 33002  | 1      | 9.59MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/cisco/inv/year=2019/month=10 |
    | 2019  | 11    | 16106  | 1      | 4.67MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/cisco/inv/year=2019/month=11 |
    | 2019  | 12    | 39044  | 1      | 11.31MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/cisco/inv/year=2019/month=12 |
    | 2020  | 1     | 26927  | 1      | 7.45MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/cisco/inv/year=2020/month=1  |
    | Total |       | 120769 | 5      | 34.68MB |        |                                                                                              |
    
    * __tx_netcm_cisco_asr__
    
    ```
    show partitions rci_network_db.tx_netcm_cisco_asr;
    ```
    
    | year  | month | #Rows | #Files | Size    | Format | Location                                                                            |
    |-------|-------|-------|--------|---------|--------|-------------------------------------------------------------------------------------|
    | 2019  | 9     | 6580  | 1      | 1.97MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/cisco/asr/year=2019/month=9  |
    | 2019  | 10    | 9569  | 1      | 2.86MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/cisco/asr/year=2019/month=10 |
    | 2019  | 11    | 8802  | 1      | 2.63MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/cisco/asr/year=2019/month=11 |
    | 2019  | 12    | 10198 | 1      | 3.04MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/cisco/asr/year=2019/month=12 |
    | 2020  | 1     | 9240  | 1      | 2.76MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/cisco/asr/year=2020/month=1  |
    | Total |       | 36469 | 5      | 13.25MB |        |                                                                                     |
    
### Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Cisco NiFi General View][img05]                  
    *Pipeline General __NetCM Cisco__*

    ![Cisco NiFi Detail View][img06]      
    *Pipeline Detalle __NetCM Cisco__*

2. **Reglas de estandarizacion del esquema**

    * Sobre el esquema se eliminaron caracteres para que se generara correctamente el esquema del archivo avro con la siguiente expresion regular:
    
    ```
    Valor de Busqueda: (?s)(^[^\n]*)(.*$)
    Expresion regular a ejecutar: ${'$1':replace("[",""):replace("]",""):replace("-",""):replace(".","")}$2
    ```

3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

    | Parámetro | Valor | Descripción|
    | ---------- | ---------- | ---------- |
    | parametro_01   | 99    | Valor de correspondiente al flujo NETCM Cisco ASR  |
    | parametro_01   | 100   | Valor de correspondiente al flujo NETCM Cisco EPN  |
    | parametro_01   | 101   | Valor de correspondiente al flujo NETCM Cisco INV  |

    * Sintaxis del comando de ejecucion del proceso de automatización:
   
    ```
    sh rci_ingesta_generacion_avro.sh {parametro_01}
    ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización : 
    
    ```
    sh rci_ingesta_generacion_avro.sh 99
    sh rci_ingesta_generacion_avro.sh 100
    sh rci_ingesta_generacion_avro.sh 101
    ```

##### [Ir a Inicio](#main)

## <a name="ericsson"></a> NetCM ERICSSON

### Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA NETCM](/RCI_DataAnalysis/eda/Gestor_NETCM/README.md#descripcion)**

- **[dicciorario de datos]** La siguientes tablas muestran el resultado de ejecutar el siguiente comando: 

    * __tx_netcm_ericsson_antena__
    
    ```
    describe formatted rci_network_db.tx_netcm_ericsson_antena;
    ```
    
    | col_name                   | data_type | comment                   |
    |----------------------------|-----------|---------------------------|
    | rnc                        | string    | Type inferred from 'kite' |
    | nodeb                      | string    | Type inferred from 'kite' |
    | electricalantennatilt      | string    | Type inferred from 'kite' |
    | antennamodelnumber         | string    | Type inferred from 'kite' |
    | antennaserialnumber        | string    | Type inferred from 'kite' |
    | maxsupportedelectricaltilt | string    | Type inferred from 'kite' |
    | minsupportedelectricaltilt | string    | Type inferred from 'kite' |
    | sheet_name                 | string    | Type inferred from 'kite' |
    
    * __tx_netcm_ericsson_nodeb__
    
    ```
    describe formatted rci_network_db.tx_netcm_ericsson_nodeb;
    ```
    
    | col_name            | data_type | comment                   |
    |---------------------|-----------|---------------------------|
    | nodeb               | string    | Type inferred from 'kite' |
    | serialnumber        | string    | Type inferred from 'kite' |
    | productname         | string    | Type inferred from 'kite' |
    | productnumber       | string    | Type inferred from 'kite' |
    | productrevision     | string    | Type inferred from 'kite' |
    | productiondate      | string    | Type inferred from 'kite' |
    | administrativestate | string    | Type inferred from 'kite' |
    | availabilitystatus  | string    | Type inferred from 'kite' |
    | operationalstate    | string    | Type inferred from 'kite' |
    | pluginunitref1      | string    | Type inferred from 'kite' |
    | positionref         | string    | Type inferred from 'kite' |
    | unittype            | string    | Type inferred from 'kite' |
    | sheet_name          | string    | Type inferred from 'kite' |
    
    * __tx_netcm_ericsson_enodeb__
    
    ```
    describe formatted rci_network_db.tx_netcm_ericsson_enodeb;
    ```
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | enodeb             | string    | Type inferred from 'kite' |
    | serialnumber       | string    | Type inferred from 'kite' |
    | productname        | string    | Type inferred from 'kite' |
    | productnumber      | string    | Type inferred from 'kite' |
    | productrevision    | string    | Type inferred from 'kite' |
    | productiondate     | string    | Type inferred from 'kite' |
    | sheet_name         | string    | Type inferred from 'kite' |
    
    * __tx_netcm_ericsson_board__
    
    ```
    describe formatted rci_network_db.tx_netcm_ericsson_board;
    ```
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | bsc                | string    | Type inferred from 'kite' |
    | site               | string    | Type inferred from 'kite' |
    | ruserialno         | string    | Type inferred from 'kite' |
    | ruserialno_count   | string    | Type inferred from 'kite' |
    | rulogicalid        | string    | Type inferred from 'kite' |
    | rurevision         | string    | Type inferred from 'kite' |
    | tg                 | string    | Type inferred from 'kite' |
    | tg_count           | string    | Type inferred from 'kite' |
    | mo                 | string    | Type inferred from 'kite' |
    | btsswver           | string    | Type inferred from 'kite' |
    | ru                 | string    | Type inferred from 'kite' |
    | state              | string    | Type inferred from 'kite' |
    | sheet_name         | string    | Type inferred from 'kite' |
    
    * __tx_netcm_ericsson_rnc__
    
    ```
    describe formatted rci_network_db.tx_netcm_ericsson_rnc;
    ```
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | rnc                | string    | Type inferred from 'kite' |
    | serialnumber       | string    | Type inferred from 'kite' |
    | productname        | string    | Type inferred from 'kite' |
    | productnumber      | string    | Type inferred from 'kite' |
    | productrevision    | string    | Type inferred from 'kite' |
    | productiondate     | string    | Type inferred from 'kite' |
    | mtni_product_code  | string    | Type inferred from 'kite' |
    | sheet_name         | string    | Type inferred from 'kite' |

    * __tx_netcm_ericsson_hw__
    
    ```
    describe formatted rci_network_db.tx_netcm_ericsson_hw;
    ```
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | node               | string    | Type inferred from 'kite' |
    | eq                 | string    | Type inferred from 'kite' |
    | eq_class           | string    | Type inferred from 'kite' |
    | type               | string    | Type inferred from 'kite' |
    | adminstate         | string    | Type inferred from 'kite' |
    | operstate          | string    | Type inferred from 'kite' |
    | powerstate         | string    | Type inferred from 'kite' |
    | revision           | string    | Type inferred from 'kite' |
    | bootrom            | string    | Type inferred from 'kite' |
    | prodno             | string    | Type inferred from 'kite' |
    | prodname           | string    | Type inferred from 'kite' |
    | manweek            | string    | Type inferred from 'kite' |
    | serialno           | string    | Type inferred from 'kite' |
    | fsbrole            | string    | Type inferred from 'kite' |
    | f_timestamp        | string    | Type inferred from 'kite' |
    | sheet_name         | string    | Type inferred from 'kite' |
    
    * Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestion.

    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | filedate           | bigint    | Type inferred from 'kite' |
    | filename           | string    | Type inferred from 'kite' |
    | hash_id            | string    | Type inferred from 'kite' |
    | sourceid           | string    | Type inferred from 'kite' |
    | registry_state     | string    | Type inferred from 'kite' |
    | datasetname        | string    | Type inferred from 'kite' |
    | timestamp          | bigint    | Type inferred from 'kite' |
    | transaction_status | string    | Type inferred from 'kite' |
    
    * Para mas informacion consultar la siguiente documentacion: __[Documentacion EDA NETCM](/RCI_DataAnalysis/eda/Gestor_NETCM/README.md)__
        
- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:

    * __tx_netcm_ericsson_antena__
    
    ```
    show partitions rci_network_db.tx_netcm_ericsson_antena;
    ```
    
    | year  | month | #Rows  | #Files | Size     | Format | Location                                                                                           |
    |-------|-------|--------|--------|----------|--------|----------------------------------------------------------------------------------------------------|
    | 2019  | 9     | 105254 | 1      | 29.49MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/antena/year=2019/month=9  |
    | 2019  | 10    | 157992 | 1      | 44.26MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/antena/year=2019/month=10 |
    | 2019  | 11    | 142934 | 1      | 39.24MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/antena/year=2019/month=11 |
    | 2019  | 12    | 165045 | 1      | 45.14MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/antena/year=2019/month=12 |
    | 2020  | 1     | 37280  | 1      | 10.38MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/antena/year=2020/month=1  |
    | Total |       | 608505 | 5      | 168.51MB |        |                                                                                                    |
    
    * __tx_netcm_ericsson_nodeb__
    
    ```
    show partitions rci_network_db.tx_netcm_ericsson_nodeb;
    ```
    
    | year  | month | #Rows | #Files | Size   | Format | Location                                                                                         |
    |-------|-------|-------|--------|--------|--------|--------------------------------------------------------------------------------------------------|
    | 2020  | 1     | 21195 | 1      | 6.17MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/nodeb/year=2020/month=1 |
    | Total |       | -1    | 1      | 6.17MB |        |                                                                                                  |
    
    * __tx_netcm_ericsson_enodeb__
    
    ```
    show partitions rci_network_db.tx_netcm_ericsson_enodeb;
    ```
    
    | year  | month | #Rows  | #Files | Size     | Format | Location                                                                                           |
    |-------|-------|--------|--------|----------|--------|----------------------------------------------------------------------------------------------------|
    | 2019  | 9     | 105103 | 1      | 29.31MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/enodeb/year=2019/month=9  |
    | 2019  | 10    | 157794 | 1      | 44.01MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/enodeb/year=2019/month=10 |
    | 2019  | 11    | 141991 | 1      | 39.14MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/enodeb/year=2019/month=11 |
    | 2019  | 12    | 163028 | 1      | 44.85MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/enodeb/year=2019/month=12 |
    | 2020  | 1     | 36803  | 1      | 10.22MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/enodeb/year=2020/month=1  |
    | Total |       | 588952 | 5      | 167.52MB |        |                                                                                                    |
    
    * __tx_netcm_ericsson_board__
    
    ```
    show partitions rci_network_db.tx_netcm_ericsson_board;
    ```
    
    | year  | month | #Rows  | #Files | Size    | Format | Location                                                                                        |
    |-------|-------|--------|--------|---------|--------|-------------------------------------------------------------------------------------------------|
    | 2019  | 9     | 24860  | 1      | 10.41MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/gsm/year=2019/month=9  |
    | 2019  | 10    | 37290  | 1      | 15.61MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/gsm/year=2019/month=10 |
    | 2019  | 11    | 33561  | 1      | 13.84MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/gsm/year=2019/month=11 |
    | 2019  | 12    | 38533  | 1      | 15.85MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/gsm/year=2019/month=12 |
    | 2020  | 1     | 8701   | 1      | 3.57MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/gsm/year=2020/month=1  |
    | Total |       | 139216 | 5      | 59.28MB |        |                                                                                                 |
    
    * __tx_netcm_ericsson_rnc__
    
    ```
    show partitions rci_network_db.tx_netcm_ericsson_rnc;
    ```
    
    | year  | month | #Rows | #Files | Size     | Format | Location                                                                                       |
    |-------|-------|-------|--------|----------|--------|------------------------------------------------------------------------------------------------|
    | 2020  | 1     | 1506  | 1      | 431.37KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/ericsson/rnc/year=2020/month=1 |
    | Total |       | -1    | 1      | 431.37KB |        |                                                                                                |

    * __tx_netcm_ericsson_hw__
    
    ```
    show partitions rci_network_db.tx_netcm_ericsson_hw;
    ```
    
    | year  | month | #Rows | #Files | Size     | Format | Location                                                                              |
    |-------|-------|-------|--------|----------|--------|---------------------------------------------------------------------------------------|
    | 2019  | 9     | 1680  | 1      | 596.08KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/ericsson/hw/year=2019/month=9  |
    | 2019  | 10    | 2520  | 1      | 892.96KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/ericsson/hw/year=2019/month=10 |
    | 2019  | 11    | 2289  | 1      | 796.28KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/ericsson/hw/year=2019/month=11 |
    | 2019  | 12    | 2604  | 1      | 902.60KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/ericsson/hw/year=2019/month=12 |
    | 2020  | 1     | 2163  | 1      | 750.13KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/ericsson/hw/year=2020/month=1  |
    | Total |       | 11256 | 5      | 3.85MB   |        |                                                                                       |    

### Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Ericsson NiFi General View][img04]              
    *Pipeline General __NetCM All Inventory Send 2__*

    ![Ericsson NiFi Detail View][img07]           
    *Pipeline Detalle __NetCM All Inventory Send 2__*

2. **Reglas de estandarizacion del esquema**

    * Sobre el esquema se eliminaron caracteres para que se generara correctamente el esquema del archivo avro con la siguiente expresion regular:
    
     ```
     Valor de Busqueda: (?s)(^[^\n]*)(.*$)
     Expresion regular a ejecutar: ${'$1':replace("[",""):replace("]",""):replace("-",""):replace(".","")}$2
     ```

3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

    | Parámetro | Valor | Descripción|
    | ---------- | ---------- | ---------- |
    | parametro_01   | 102   | Valor de correspondiente al flujo NETCM Ericsson ANTENA  |
    | parametro_01   | 103   | Valor de correspondiente al flujo NETCM Ericsson NODEB   |
    | parametro_01   | 104   | Valor de correspondiente al flujo NETCM Ericsson RNC     |
    | parametro_01   | 105   | Valor de correspondiente al flujo NETCM Ericsson ENODEB  |
    | parametro_01   | 106   | Valor de correspondiente al flujo NETCM Ericsson BOARD   |
    | parametro_01   | 140   | Valor de correspondiente al flujo NETCM Ericsson HW      |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
   ```
   sh rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización : 
    
   ```
   sh rci_ingesta_generacion_avro.sh 102
   sh rci_ingesta_generacion_avro.sh 103
   sh rci_ingesta_generacion_avro.sh 104
   sh rci_ingesta_generacion_avro.sh 105
   sh rci_ingesta_generacion_avro.sh 106
   sh rci_ingesta_generacion_avro.sh 140
   ```

##### [Ir a Inicio](#main)

## <a name="huawei"></a> NetCM Huawei

### Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA NETCM](/RCI_DataAnalysis/eda/Gestor_NETCM/README.md#descripcion)**

- **[dicciorario de datos]** La siguientes tablas muestran el resultado de ejecutar el siguiente comando: 

    * __tx_netcm_huawei_antena__
    
    ```
    describe formatted rci_network_db.tx_netcm_huawei_antena;
    ```
    
    | col_name                  | data_type | comment                   |
    |---------------------------|-----------|---------------------------|
    | node_name                 | string    | Type inferred from 'kite' |
    | aisg_sector_id            | string    | Type inferred from 'kite' |
    | antenna_model_number      | string    | Type inferred from 'kite' |
    | antenna_serial_no         | string    | Type inferred from 'kite' |
    | band1                     | string    | Type inferred from 'kite' |
    | band2                     | string    | Type inferred from 'kite' |
    | band3                     | string    | Type inferred from 'kite' |
    | band4                     | string    | Type inferred from 'kite' |
    | max_tilt                  | string    | Type inferred from 'kite' |
    | min_tilt                  | string    | Type inferred from 'kite' |
    | beamwidth1                | string    | Type inferred from 'kite' |
    | beamwidth2                | string    | Type inferred from 'kite' |
    | beamwidth3                | string    | Type inferred from 'kite' |
    | beamwidth4                | string    | Type inferred from 'kite' |
    | device_name               | string    | Type inferred from 'kite' |
    | device_no                 | string    | Type inferred from 'kite' |
    | gain1                     | string    | Type inferred from 'kite' |
    | gain2                     | string    | Type inferred from 'kite' |
    | gain3                     | string    | Type inferred from 'kite' |
    | gain4                     | string    | Type inferred from 'kite' |
    | installed_mechanical_tilt | string    | Type inferred from 'kite' |
    | subunit_name              | string    | Type inferred from 'kite' |
    | sheet_name                | string    | Type inferred from 'kite' |
    
    * __tx_netcm_huawei_nodeb__
    
    ```
    describe formatted rci_network_db.tx_netcm_huawei_nodeb;
    ```
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | rnc                | string    | Type inferred from 'kite' |
    | nodeb              | string    | Type inferred from 'kite' |
    | serial_number      | string    | Type inferred from 'kite' |
    | description        | string    | Type inferred from 'kite' |
    | manufacture_date   | string    | Type inferred from 'kite' |
    | issue_number       | string    | Type inferred from 'kite' |
    | type               | string    | Type inferred from 'kite' |
    | cabinet_number     | string    | Type inferred from 'kite' |
    | subrack_number     | string    | Type inferred from 'kite' |
    | slot_number        | string    | Type inferred from 'kite' |
    | mtni_product_code  | string    | Type inferred from 'kite' |
    | sheet_name         | string    | Type inferred from 'kite' |
    
    * __tx_netcm_huawei_enodeb__
    
    ```
    describe formatted rci_network_db.tx_netcm_huawei_enodeb;
    ```
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | enodeb             | string    | Type inferred from 'kite' |
    | serial_number      | string    | Type inferred from 'kite' |
    | description        | string    | Type inferred from 'kite' |
    | manufacture_date   | string    | Type inferred from 'kite' |
    | issue_number       | string    | Type inferred from 'kite' |
    | type               | string    | Type inferred from 'kite' |
    | cabinet_number     | string    | Type inferred from 'kite' |
    | subrack_number     | string    | Type inferred from 'kite' |
    | slot_number        | string    | Type inferred from 'kite' |
    | sheet_name         | string    | Type inferred from 'kite' |
    
    * __tx_netcm_huawei_rnc__
    
    ```
    describe formatted rci_network_db.tx_netcm_huawei_rnc;
    ```
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | rnc                | string    | Type inferred from 'kite' |
    | subrack_no         | string    | Type inferred from 'kite' |
    | slot_no            | string    | Type inferred from 'kite' |
    | boardtype          | string    | Type inferred from 'kite' |
    | barcode            | string    | Type inferred from 'kite' |
    | description        | string    | Type inferred from 'kite' |
    | manufactured       | string    | Type inferred from 'kite' |
    | daughter_board     | string    | Type inferred from 'kite' |
    | port               | string    | Type inferred from 'kite' |
    | sheet_name         | string    | Type inferred from 'kite' |

    * __tx_netcm_huawei_bts__
    
    ```
    describe formatted rci_network_db.tx_netcm_huawei_bts;
    ```
    
    | col_name             | data_type | comment                   |
    |----------------------|-----------|---------------------------|
    | site                 | string    | Type inferred from 'kite' |
    | antennadevicetype    | string    | Type inferred from 'kite' |
    | dateofmanufacture    | string    | Type inferred from 'kite' |
    | inventoryunitid      | string    | Type inferred from 'kite' |
    | inventoryunittype    | string    | Type inferred from 'kite' |
    | manufacturerdata     | string    | Type inferred from 'kite' |
    | prodnr               | string    | Type inferred from 'kite' |
    | serialnumber         | string    | Type inferred from 'kite' |
    | unitposition         | string    | Type inferred from 'kite' |
    | vendorname           | string    | Type inferred from 'kite' |
    | vendorunitfamilytype | string    | Type inferred from 'kite' |
    | vendorunittypenumber | string    | Type inferred from 'kite' |
    | versionnumber        | string    | Type inferred from 'kite' |
    | sheet_name           | string    | Type inferred from 'kite' |
    
    * __tx_netcm_huawei_mbts__
    
    ```
    describe formatted rci_network_db.tx_netcm_huawei_mbts;
    ```
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | mbts               | string    | Type inferred from 'kite' |
    | serialnumber       | string    | Type inferred from 'kite' |
    | boardname          | string    | Type inferred from 'kite' |
    | boardtype          | string    | Type inferred from 'kite' |
    | manufacturerdata   | string    | Type inferred from 'kite' |
    | sheet_name         | string    | Type inferred from 'kite' |

    * __tx_netcm_huawei_mmeib__
    
    ```
    describe formatted rci_network_db.tx_netcm_huawei_mmeib;
    ```
    
    | col_name             | data_type | comment                   |
    |----------------------|-----------|---------------------------|
    | mme                  | string    | Type inferred from 'kite' |
    | boardname            | string    | Type inferred from 'kite' |
    | boardtype            | string    | Type inferred from 'kite' |
    | dateoflastservice    | string    | Type inferred from 'kite' |
    | frameno              | string    | Type inferred from 'kite' |
    | inventoryunitid      | string    | Type inferred from 'kite' |
    | serialnumber         | string    | Type inferred from 'kite' |
    | rackno               | string    | Type inferred from 'kite' |
    | slotno               | string    | Type inferred from 'kite' |
    | slotpos              | string    | Type inferred from 'kite' |
    | unitposition         | string    | Type inferred from 'kite' |
    | softver              | string    | Type inferred from 'kite' |
    | vendorname           | string    | Type inferred from 'kite' |
    | vendorunitfamilytype | string    | Type inferred from 'kite' |
    | node_type            | string    | Type inferred from 'kite' |
    | sheet_name           | string    | Type inferred from 'kite' |
    
    * __tx_netcm_huawei_mmepi__
    
    ```
    describe formatted rci_network_db.tx_netcm_huawei_mmepi;
    ```
    
    | col_name             | data_type | comment                   |
    |----------------------|-----------|---------------------------|
    | mme                  | string    | Type inferred from 'kite' |
    | boardname            | string    | Type inferred from 'kite' |
    | boardtype            | string    | Type inferred from 'kite' |
    | dateoflastservice    | string    | Type inferred from 'kite' |
    | frameno              | string    | Type inferred from 'kite' |
    | inventoryunitid      | string    | Type inferred from 'kite' |
    | serialnumber         | string    | Type inferred from 'kite' |
    | rackno               | string    | Type inferred from 'kite' |
    | slotno               | string    | Type inferred from 'kite' |
    | slotpos              | string    | Type inferred from 'kite' |
    | unitposition         | string    | Type inferred from 'kite' |
    | softver              | string    | Type inferred from 'kite' |
    | vendorname           | string    | Type inferred from 'kite' |
    | vendorunitfamilytype | string    | Type inferred from 'kite' |
    | node_type            | string    | Type inferred from 'kite' |
    | sheet_name           | string    | Type inferred from 'kite' |
    
    * __tx_netcm_huawei_cell__
    
    ```
    describe formatted rci_network_db.tx_netcm_huawei_cell;
    ```
    
    | col_name                  | data_type | comment                   |
    |---------------------------|-----------|---------------------------|
    | rnc                       | string    | Type inferred from 'kite' |
    | ucell                     | string    | Type inferred from 'kite' |
    | ucell_created_date        | string    | Type inferred from 'kite' |
    | cell_administrative_state | string    | Type inferred from 'kite' |
    | validation_indication     | string    | Type inferred from 'kite' |
    | blocked_count             | string    | Type inferred from 'kite' |
    | blocked_dates             | string    | Type inferred from 'kite' |
    | deactivated_count         | string    | Type inferred from 'kite' |
    | deactivated_dates         | string    | Type inferred from 'kite' |
    | sheet_name                | string    | Type inferred from 'kite' |
    
    * Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestion.
    
    | col_name           | data_type | comment                   |
    |--------------------|-----------|---------------------------|
    | filedate           | bigint    | Type inferred from 'kite' |
    | filename           | string    | Type inferred from 'kite' |
    | hash_id            | string    | Type inferred from 'kite' |
    | sourceid           | string    | Type inferred from 'kite' |
    | registry_state     | string    | Type inferred from 'kite' |
    | datasetname        | string    | Type inferred from 'kite' |
    | timestamp          | bigint    | Type inferred from 'kite' |
    | transaction_status | string    | Type inferred from 'kite' |
    
    * Para mas informacion consultar la siguiente documentacion: __[Documentacion EDA NETCM](/RCI_DataAnalysis/eda/Gestor_NETCM/README.md)__
        
- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:

    * __tx_netcm_huawei_antena__
    
    ```
    show partitions rci_network_db.tx_netcm_huawei_antena;
    ```
    
    | year  | month | #Rows  | #Files | Size     | Format | Location                                                                                        |
    |-------|-------|--------|--------|----------|--------|-------------------------------------------------------------------------------------------------|
    | 2020  | 1     | 576225 | 2      | 208.88MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/antena/year=2020/month=1 |
    | Total |       | 576225 | 2      | 208.88MB |        |                                                                                                 |
    
    * __tx_netcm_huawei_nodeb__
    
    ```
    show partitions rci_network_db.tx_netcm_huawei_nodeb;
    ```
    
    | year  | month | #Rows  | #Files | Size    | Format | Location                                                                                       |
    |-------|-------|--------|--------|---------|--------|------------------------------------------------------------------------------------------------|
    | 2020  | 1     | 118413 | 1      | 44.43MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/nodeb/year=2020/month=1 |
    | Total |       | 118413 | 1      | 44.43MB |        |                                                                                                |
    
    * __tx_netcm_huawei_enodeb__
    
    ```
    show partitions rci_network_db.tx_netcm_huawei_enodeb;
    ```
    
    | year  | month | #Rows | #Files | Size     | Format | Location                                                                                         |
    |-------|-------|-------|--------|----------|--------|--------------------------------------------------------------------------------------------------|
    | 2019  | 9     | 6060  | 1      | 1.96MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/enodeb/year=2019/month=9  |
    | 2019  | 10    | 9090  | 1      | 2.93MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/enodeb/year=2019/month=10 |
    | 2019  | 11    | 8181  | 1      | 2.62MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/enodeb/year=2019/month=11 |
    | 2019  | 12    | 9393  | 1      | 3.00MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/enodeb/year=2019/month=12 |
    | 2020  | 1     | 2121  | 1      | 701.10KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/enodeb/year=2020/month=1  |
    | Total |       | 34845 | 5      | 11.20MB  |        |                                                                                                  |
    
    * __tx_netcm_huawei_rnc__
    
    ```
    show partitions rci_network_db.tx_netcm_huawei_rnc;
    ```
    
    | year  | month | #Rows  | #Files | Size     | Format | Location                                                                                      |
    |-------|-------|--------|--------|----------|--------|-----------------------------------------------------------------------------------------------|
    | 2019  | 9     | 105480 | 1      | 35.23MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/rnc/year=2019/month=9  |
    | 2019  | 10    | 158220 | 1      | 52.85MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/rnc/year=2019/month=10 |
    | 2019  | 11    | 142398 | 1      | 46.03MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/rnc/year=2019/month=11 |
    | 2019  | 12    | 163494 | 1      | 52.44MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/rnc/year=2019/month=12 |
    | 2020  | 1     | 36918  | 1      | 11.93MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/netcm/huawei/rnc/year=2020/month=1  |
    | Total |       | 606510 | 5      | 198.48MB |        |                                                                                               |

    * __tx_netcm_huawei_bts__
    
    ```
    show partitions rci_network_db.tx_netcm_huawei_bts;
    ```
    
    | year  | month | #Rows    | #Files | Size     | Format | Location                                                                             |
    |-------|-------|----------|--------|----------|--------|--------------------------------------------------------------------------------------|
    | 2019  | 9     | 1990955  | 7      | 846.82MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/bts/year=2019/month=9  |
    | 2019  | 10    | 2950433  | 7      | 1.23GB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/bts/year=2019/month=10 |
    | 2019  | 11    | 2708823  | 6      | 1.12GB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/bts/year=2019/month=11 |
    | 2019  | 12    | 2922279  | 9      | 1.21GB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/bts/year=2019/month=12 |
    | 2020  | 1     | 2723677  | 8      | 1.12GB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/bts/year=2020/month=1  |
    | Total |       | 13296167 | 37     | 5.50GB   |        |                                                                                      |

    * __tx_netcm_huawei_mbts__
    
    ```
    show partitions rci_network_db.tx_netcm_huawei_mbts;
    ```
    
    | year  | month | #Rows  | #Files | Size     | Format | Location                                                                             |
    |-------|-------|--------|--------|----------|--------|--------------------------------------------------------------------------------------|
    | 2020  | 1     | 953530 | 3      | 305.90MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/mbts/year=2020/month=1 |
    | Total |       | 953530 | 3      | 305.90MB |        |                                                                                      |

    * __tx_netcm_huawei_mmeib__
    
    ```
    show partitions rci_network_db.tx_netcm_huawei_mmeib;
    ```
    
    | year  | month | #Rows  | #Files | Size    | Format | Location                                                                               |
    |-------|-------|--------|--------|---------|--------|----------------------------------------------------------------------------------------|
    | 2019  | 9     | 29565  | 1      | 11.62MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/mmeib/year=2019/month=9  |
    | 2019  | 10    | 44888  | 1      | 17.64MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/mmeib/year=2019/month=10 |
    | 2019  | 11    | 41458  | 1      | 15.85MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/mmeib/year=2019/month=11 |
    | 2019  | 12    | 47802  | 1      | 18.15MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/mmeib/year=2019/month=12 |
    | 2020  | 1     | 38544  | 1      | 14.64MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/mmeib/year=2020/month=1  |
    | Total |       | 169881 | 5      | 77.90MB |        |                                                                                        |

    * __tx_netcm_huawei_mmepi__
    
    ```
    show partitions rci_network_db.tx_netcm_huawei_mmepi;
    ```
    
    | year  | month | #Rows  | #Files | Size     | Format | Location                                                                               |
    |-------|-------|--------|--------|----------|--------|----------------------------------------------------------------------------------------|
    | 2019  | 9     | 57699  | 1      | 22.48MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/mmepi/year=2019/month=9  |
    | 2019  | 10    | 84384  | 1      | 32.87MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/mmepi/year=2019/month=10 |
    | 2019  | 11    | 79461  | 1      | 30.19MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/mmepi/year=2019/month=11 |
    | 2019  | 12    | 91357  | 1      | 34.51MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/mmepi/year=2019/month=12 |
    | 2020  | 1     | 82922  | 1      | 31.32MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/mmepi/year=2020/month=1  |
    | Total |       | 324689 | 5      | 151.37MB |        |                                                                                        |

    * __tx_netcm_huawei_cell__
    
    ```
    show partitions rci_network_db.tx_netcm_huawei_cell;
    ```
    
    | year  | month | #Rows | #Files | Size    | Format | Location                                                                              |
    |-------|-------|-------|--------|---------|--------|---------------------------------------------------------------------------------------|
    | 2019  | 9     | 20    | 1      | 7.88KB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/cell/year=2019/month=9  |
    | 2019  | 10    | 29    | 1      | 10.71KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/cell/year=2019/month=10 |
    | 2019  | 11    | 26    | 1      | 9.68KB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/cell/year=2019/month=11 |
    | 2019  | 12    | 30    | 1      | 10.86KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/cell/year=2019/month=12 |
    | 2020  | 1     | 28    | 1      | 10.26KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/netcm/huawei/cell/year=2020/month=1  |
    | Total |       | 133   | 5      | 49.38KB |        |                                                                                       |

### Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Huawei NiFi General View][img03]              
    *Pipeline General __NetCM All Inventory Send__*

    ![Huawei NiFi Detail View][img08]           
    *Pipeline Detalle __NetCM All Inventory Send__*

    ![Huawei NiFi General View][img09]              
    *Pipeline General __NetCM All Inventory Send 3__*

    ![Huawei NiFi Detail View][img10]           
    *Pipeline Detalle __NetCM All Inventory Send 3__*
    
2. **Reglas de estandarizacion del esquema**

    * Sobre el esquema se eliminaron caracteres para que se generara correctamente el esquema del archivo avro con la siguiente expresion regular:
    
     ```
     Valor de Busqueda: (?s)(^[^\n]*)(.*$)
     Expresion regular a ejecutar: ${'$1':replace("[",""):replace("]",""):replace("-",""):replace(".","")}$2
     ```

3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

    | Parámetro | Valor | Descripción|
    | ---------- | ---------- | ---------- |
    | parametro_01   | 107   | Valor de correspondiente al flujo NETCM Huawei ANTENA  |
    | parametro_01   | 109   | Valor de correspondiente al flujo NETCM Huawei NODEB   |
    | parametro_01   | 110   | Valor de correspondiente al flujo NETCM Huawei RNC     |
    | parametro_01   | 108   | Valor de correspondiente al flujo NETCM Huawei ENODEB  |
    | parametro_01   | 141   | Valor de correspondiente al flujo NETCM Huawei BTS     |
    | parametro_01   | 143   | Valor de correspondiente al flujo NETCM Huawei MBTS    |
    | parametro_01   | 145   | Valor de correspondiente al flujo NETCM Huawei MMEIB   |
    | parametro_01   | 144   | Valor de correspondiente al flujo NETCM Huawei MMEPI   |
    | parametro_01   | 142   | Valor de correspondiente al flujo NETCM Huawei CELL    |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
    ```
    sh rci_ingesta_generacion_avro.sh {parametro_01}
    ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización : 
    
    ```
    sh rci_ingesta_generacion_avro.sh 107
    sh rci_ingesta_generacion_avro.sh 109
    sh rci_ingesta_generacion_avro.sh 110
    sh rci_ingesta_generacion_avro.sh 108
    sh rci_ingesta_generacion_avro.sh 141
    sh rci_ingesta_generacion_avro.sh 143
    sh rci_ingesta_generacion_avro.sh 145
    sh rci_ingesta_generacion_avro.sh 144
    sh rci_ingesta_generacion_avro.sh 142
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

[img01]: images/netcm-nifi-01.png "Netcm NiFi Main View"
[img02]: images/netcm-nifi-02.png "Netcm NiFi General View"
[img03]: images/netcm-nifi-03.png "Netcm NiFi Cisco EPN Main Flow View"
[img04]: images/netcm-nifi-04.png "Netcm NiFi Ericsson Main Flows View"
[img05]: images/netcm-nifi-05.png "Netcm NiFi Huawei Main Flow View"
[img06]: images/netcm-nifi-06.png "Netcm NiFi Cisco EPN Detail Flow View"
[img07]: images/netcm-nifi-07.png "Netcm NiFi Ericsson Detail Flow View"
[img08]: images/netcm-nifi-08.png "Netcm NiFi Huawei Detail Flow View"
[img09]: images/netcm-nifi-09.png "Netcm NiFi Huawei Main Flow View"
[img10]: images/netcm-nifi-10.png "Netcm NiFi Huawei Detail Flow View"