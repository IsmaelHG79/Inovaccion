![EncabezadoAxity][img1]

# Documentación Data Ingestion para la fuente ATT **U2000-FBB-TX**

La ingesta de la fuente U2000 TX requirió la construcción de varios flujos de NiFi debido a que en el repositorio de origen existen archivos con estructuras distintas y que deben de guardarse en tablas separadas:

![Flujo NiFi U2000 TX][img2]

Vista general de **G - U2000 TX**

 Esta fuente se compone de catorce flujos de NiFi y se separan de la siguiente manera:

 <a name="main"></a>

1. **inventoryDump**
    * [Board_Report](#board)
    * [Port_Report](#port)
    * [NE_Report](#ne)
    * [SFP_Information](#sfp)
    * [Subcard_Report](#subcard)
    * [Subrack_Report](#subrack)
    * [OpticalModule](#optical)
    * [Microwave Link Report](#microwave)

![Grupo inventoryDump][img3]

Vista general de **G - INVENTORYDUMP**

2. **pfm_output**
    * [PM_IG1](#ig1)
    * [PM_IG27](#ig27)
    * [PM_IG56](#ig56)
    * [PM_IG60003](#ig60003)
    * [PM_IG60008](#ig60008)
    * [PM_IG64](#ig64)

![Grupo pfm_output][img4]

Vista general de **G - PFM OUTPUT**

3. **RTNLinkDump**
    * [RTNLinkDump](#microwave)

![Grupo pfm_output][img5]

Vista general de **G - RTNLinkDump**

<a name="ig1"></a>
<a name="ig27"></a>
<a name="ig56"></a>
<a name="ig60003"></a>
<a name="ig60008"></a>
<a name="ig64"></a>
<a name="cmc"></a>
<a name="subcard"></a>

Los archivos de las fuentes `CMC_Information`, `Subcard_Report`, `PM_IG64`, `PM_IG60003` y `PM_IG60008` no se han cargado en el Data Lake debido a que los archivos en el SFTP no contienen datos aunque sus flujos si fueron construidos y probados, estos existen dentro del flujo de NiFi esperando a que las fuentes contengan datos.

El detalle de cada uno de los flujos será explicado con mas detalle en los siguientes apartados.

## Descripcion del `FTP`

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14481174), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

En el directorio del SFTP todos los archivos de U2000 TX viven en un misma carpeta, por lo que el flujo esta configurado para buscar los archivos de forma recursiva usando la siguiente expresión regular en el procesador GetSFTP:

```
(?=<archivo>).*.csv$
```

En esta expresion se buscan las primeras palabras con las que inicia el nombre del archivo a cargar y que aparecen como `<archivo>`, además la expresión confirma que el archivo tenga una extension `.csv`.

![Procesador GetSFTP][img5]

Vista del procesador **GetSFTP**

<a name="board"></a>
## Board Report

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_fbb_u2000_board`, en la cual se depositan los datos:

| name               | type   | comment                                                        |
|--------------------|--------|----------------------------------------------------------------|
| ne                 | string | Type inferred from 'MXCMXM01RTCOREBH01'                        |
| board_name         | string | Type inferred from 'LPU 1'                                     |
| board_type         | string | Type inferred from 'DEVLPUF-21'                                |
| ne_type            | string | Type inferred from 'CX600'                                     |
| subrack_id         | string | Type inferred from '1'                                         |
| slot_id            | string | Type inferred from '1'                                         |
| hardware_version   | string | Type inferred from 'CR52LPUK REV D'                            |
| software_version   | string | Type inferred from 'FSU ver Version 2.1                        |
| snbar_code         | string | Type inferred from '210305253310B2000065'                      |
| alias              | string | Type inferred from '-'                                         |
| remarks            | string | Type inferred from '-'                                         |
| customized_column  | string | Type inferred from '-'                                         |
| subrack_type       | string | Type inferred from '--'                                        |
| ne_id              | string | Type inferred from '0-0'                                       |
| bios_version       | string | Type inferred from '--'                                        |
| fpga_version       | string | Type inferred from '--'                                        |
| board_status       | string | Type inferred from 'Normal'                                    |
| pnbom_codeitem     | string | Type inferred from '03052533'                                  |
| model              | string | Type inferred from '--'                                        |
| rev_issue_number   | string | Type inferred from '00'                                        |
| management         | string | Type inferred from 'Managed'                                   |
| description        | string | Type inferred from 'Flexible Card Line Processing Unit(LPUF-21 |
| manufacture_date   | string | Type inferred from '2011-02-13'                                |
| create_time        | string | Type inferred from '--'                                        |

Las siguientes columnas son datos de control que se insertan al momento de la ingesta para identificar a la fuente, el archivo original no las incluye. Por ser las mismas columnas para todos los flujos de NiFi solo se listarán una vez aunque todas las tablas de U2000 TX los llevan:

| name               | type   | comment                                                        |
|--------------------|--------|----------------------------------------------------------------|
| filedate           | bigint | Type inferred from '20191124'                                  |
| filename           | string | Type inferred from 'Board_Report_2019-11-24_07-00-22.csv'      |
| fileip             | string | Type inferred from '10.32.233.36'                              |
| hash_id            | string | Type inferred from 'null'                                      |
| sourceid           | string | Type inferred from 'Gestores-U2000-FBB-TX'                     |
| registry_state     | string | Type inferred from 'null'                                      |
| datasetname        | string | Type inferred from 'Board_Report'                              |
| timestamp          | bigint | Type inferred from '20191129'                                  |
| transaction_status | string | Type inferred from 'null'                                      |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_fbb_u2000_board** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_fbb_u2000_board`:

| year  | month | day | #Rows   | #Files | Size     | Format | Location                                                                                  |
|-------|-------|-----|---------|--------|----------|--------|-------------------------------------------------------------------------------------------|
| 2019  | 11    | 13  | 107509  | 4      | 54.74MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=13 |
| 2019  | 11    | 14  | 107468  | 4      | 54.71MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=14 |
| 2019  | 11    | 15  | 107523  | 4      | 54.73MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=15 |
| 2019  | 11    | 16  | 107523  | 5      | 54.73MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=16 |
| 2019  | 11    | 17  | 107523  | 5      | 54.73MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=17 |
| 2019  | 11    | 18  | 107523  | 5      | 54.73MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=18 |
| 2019  | 11    | 19  | 107524  | 4      | 54.73MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=19 |
| 2019  | 11    | 20  | 107531  | 4      | 54.72MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 107510  | 4      | 54.71MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 107494  | 4      | 54.70MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 107487  | 4      | 54.69MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=23 |
| 2019  | 11    | 24  | 107487  | 5      | 54.69MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=24 |
| 2019  | 11    | 25  | 107487  | 4      | 54.69MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/board/year=2019/month=11/day=25 |
| Total | .     | .   | 1397589 | 56     | 711.28MB | .      | .                                                                                         |

<a name="ne"></a>
## NE Report

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_fbb_u2000_ne`, en la cual se depositan los datos:

| name               | type   | comment                                                        |
|--------------------|--------|----------------------------------------------------------------|
| ne_name            | string | Type inferred from 'MXCMXM01RTCOREBH01'                        |
| ne_type            | string | Type inferred from 'CX600'                                     |
| ne_ip_address      | string | Type inferred from '10.33.79.9'                                |
| ne_mac_address     | string | Type inferred from '78:1D:BA:56:8F:C7'                         |
| ne_id              | string | Type inferred from '0-0'                                       |
| software_version   | string | Type inferred from 'VRP5.160 V600R008C10'                      |
| physical_location  | string | Type inferred from 'Beijing China'                             |
| create_time        | string | Type inferred from '10/31/2016 17:06:34'                       |
| fibercable_count   | string | Type inferred from '0'                                         |
| running_status     | string | Type inferred from 'Normal'                                    |
| subnet             | string | Type inferred from 'MSO-REV-M2'                                |
| subnet_path        | string | Type inferred from 'Physical Root/DATACOMM/MX-REV/MSO-REV-M2'  |
| alias              | string | Type inferred from '10.38.217.159'                             |
| remarks            | string | Type inferred from 'The NE is created through auto discovery.' |
| patch_version_list | string | Type inferred from 'SPC300 SPH111'                             |
| customized_column  | string | Type inferred from '-'                                         |
| lsr_id             | string | Type inferred from '10.33.78.9'                                |
| maintenance_status | string | Type inferred from 'Normal'                                    |
| gateway_type       | string | Type inferred from 'Non-gateway'                               |
| gateway            | string | Type inferred from '--'                                        |
| optical_ne         | string | Type inferred from '--'                                        |
| subrack_type       | string | Type inferred from 'Enhanced Subrack'                          |
| conference_call    | string | Type inferred from '--'                                        |
| orderwire_phone    | string | Type inferred from '--'                                        |
| ne_subtype         | string | Type inferred from 'CX600-X3'                                  |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_fbb_u2000_ne** se generan de forma diaria usando el campo de auditoría **filedate**. La tabla contiene 359 particiones,  algunas de las particiones son:

    Sentencia `show partitions tx_fbb_u2000_ne`:

| year  | month | day | #Rows  | #Files | Size    | Format | Location                                                                               |
|-------|-------|-----|--------|--------|---------|--------|----------------------------------------------------------------------------------------|
| 2019  | 11    | 13  | 8219   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=13 |
| 2019  | 11    | 14  | 8218   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=14 |
| 2019  | 11    | 15  | 8226   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=15 |
| 2019  | 11    | 16  | 8226   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=16 |
| 2019  | 11    | 17  | 8226   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=17 |
| 2019  | 11    | 18  | 8226   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=18 |
| 2019  | 11    | 19  | 8226   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=19 |
| 2019  | 11    | 20  | 8226   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 8225   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 8224   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 8228   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=23 |
| 2019  | 11    | 24  | 8228   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=24 |
| 2019  | 11    | 25  | 8228   | 2      | 4.50MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/ne/year=2019/month=11/day=25 |
| Total | .     | .   | 106926 | 26     | 58.52MB | .      | .                                                                                      |

<a name="optical"></a>
## Optical Module Information

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_fbb_u2000_optical_module`, en la cual se depositan los datos:

| name                                          | type   | comment                                            |
|-----------------------------------------------|--------|----------------------------------------------------|
| serial_no                                     | string | Type inferred from 'HA11040121534'                 |
| opticalelectrical_type                        | string | Type inferred from 'ESFP'                          |
| ne_name                                       | string | Type inferred from 'MXCMXM01RTCOREBH01'            |
| port_name                                     | string | Type inferred from 'GigabitEthernet1/1/1'          |
| port_description                              | string | Type inferred from 'To-MXCMXM01RTCOREBH02-GE1/1/1' |
| port_type                                     | string | Type inferred from 'Ethernet'                      |
| receive_optical_powerdbm                      | string | Type inferred from '-6.11'                         |
| reference_receive_optical_powerdbm            | string | Type inferred from 'null'                          |
| reference_receive_time                        | string | Type inferred from 'null'                          |
| receive_status                                | string | Type inferred from 'Normal'                        |
| upper_threshold_for_receive_optical_powerdbm  | string | Type inferred from '-3'                            |
| low_threshold_for_receive_optical_powerdbm    | string | Type inferred from '-19'                           |
| transmit_optical_powerdbm                     | string | Type inferred from '-5.52'                         |
| reference_transmit_optical_powerdbm           | string | Type inferred from 'null'                          |
| reference_transmit_time                       | string | Type inferred from 'null'                          |
| transmit_status                               | string | Type inferred from 'Normal'                        |
| upper_threshold_for_transmit_optical_powerdbm | string | Type inferred from '-3.52'                         |
| low_threshold_for_transmit_optical_powerdbm   | string | Type inferred from '-7.52'                         |
| singlemodemultimode                           | string | Type inferred from 'SingleMode'                    |
| speedmbs                                      | string | Type inferred from '1000'                          |
| wave_lengthnm                                 | string | Type inferred from '1310'                          |
| transmission_distancem                        | string | Type inferred from '10000'                         |
| fiber_type                                    | string | Type inferred from 'LC'                            |
| pmanufacturer                                 | string | Type inferred from 'HG GENUINE'                    |
| optical_mode_authentication                   | string | Type inferred from 'Authenticated'                 |
| port_remark                                   | string | Type inferred from 'null'                          |
| port_custom_column                            | string | Type inferred from 'null'                          |
| opticaldirectiontype                          | string | Type inferred from 'twoFiberBidirection'           |
| vendor_pn                                     | string | Type inferred from 'MXPD-243S'                     |
| model                                         | string | Type inferred from '--'                            |
| revissue_number                               | string | Type inferred from '--'                            |
| pnbom_codeitem                                | string | Type inferred from '--'                            |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_fbb_u2000_optical_module** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_fbb_u2000_optical_module`:

| year  | month | day | #Rows  | #Files | Size    | Format | Location                                                                                           |
|-------|-------|-----|--------|--------|---------|--------|----------------------------------------------------------------------------------------------------|
| 2019  | 11    | 13  | 12352  | 1      | 6.22MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=13 |
| 2019  | 11    | 14  | 12352  | 1      | 6.22MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=14 |
| 2019  | 11    | 15  | 12351  | 1      | 6.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=15 |
| 2019  | 11    | 16  | 12351  | 1      | 6.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=16 |
| 2019  | 11    | 17  | 12351  | 1      | 6.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=17 |
| 2019  | 11    | 18  | 12351  | 2      | 6.22MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=18 |
| 2019  | 11    | 19  | 12341  | 1      | 6.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=19 |
| 2019  | 11    | 20  | 12341  | 1      | 6.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 12342  | 1      | 6.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 12342  | 1      | 6.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 12342  | 1      | 6.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=23 |
| 2019  | 11    | 24  | 12342  | 1      | 6.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=24 |
| 2019  | 11    | 25  | 12342  | 1      | 6.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/optical_module/year=2019/month=11/day=25 |
| Total | .     | .   | 160500 | 14     | 80.77MB | .      | .                                                                                                  |

<a name="port"></a>
## Port Report

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_fbb_u2000_port`, en la cual se depositan los datos:

| name              | type   | comment                                              |
|-------------------|--------|------------------------------------------------------|
| ne_name           | string | Type inferred from 'MXCMXM01RTCOREBH01'              |
| ne_type           | string | Type inferred from 'CX600'                           |
| shelf_no          | string | Type inferred from '1'                               |
| slot_no           | string | Type inferred from '1'                               |
| subslot_no        | string | Type inferred from '0'                               |
| port_no           | string | Type inferred from '0'                               |
| port_name         | string | Type inferred from 'GigabitEthernet1/0/0'            |
| port_type         | string | Type inferred from 'Ethernet'                        |
| port_rate_bits    | string | Type inferred from '1000000000'                      |
| port_level        | string | Type inferred from '--'                              |
| management        | string | Type inferred from 'Up'                              |
| alias             | string | Type inferred from 'To-DIFBEJ6020-ETAA000198312-1st' |
| remarks           | string | Type inferred from '--'                              |
| customized_column | string | Type inferred from '-'                               |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_fbb_u2000_port** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_fbb_u2000_port`:

| year  | month | day | #Rows   | #Files | Size      | Format | Location                                                                                 |
|-------|-------|-----|---------|--------|-----------|--------|------------------------------------------------------------------------------------------|
| 2019  | 11    | 13  | 236622  | 4      | 78.28MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=13 |
| 2019  | 11    | 14  | 236534  | 4      | 78.25MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=14 |
| 2019  | 11    | 15  | 236670  | 5      | 78.30MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=15 |
| 2019  | 11    | 16  | 236670  | 4      | 78.30MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=16 |
| 2019  | 11    | 17  | 236670  | 4      | 78.30MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=17 |
| 2019  | 11    | 18  | 236670  | 3      | 78.29MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=18 |
| 2019  | 11    | 19  | 236648  | 4      | 78.29MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=19 |
| 2019  | 11    | 20  | 236658  | 5      | 78.29MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 236632  | 3      | 78.28MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 236604  | 4      | 78.27MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 236590  | 4      | 78.27MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=23 |
| 2019  | 11    | 24  | 236590  | 4      | 78.27MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=24 |
| 2019  | 11    | 25  | 236590  | 4      | 78.27MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/port/year=2019/month=11/day=25 |
| Total | .     | .   | 3076148 | 52     | 1017.66MB | .      | .                                                                                        |

<a name="sfp"></a>
## SFP Information

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_fbb_u2000_sfp_information`, en la cual se depositan los datos:

| name                | type   | comment                                                |
|---------------------|--------|--------------------------------------------------------|
| port                | string | Type inferred from 'MXNAYTPI1282MW01-7-CSHO-1(port-1)' |
| sfp_type            | string | Type inferred from '-'                                 |
| fibercable_type     | string | Type inferred from '-'                                 |
| logical_type        | string | Type inferred from '-'                                 |
| physical_type       | string | Type inferred from '-'                                 |
| sn_bar_code         | string | Type inferred from '-'                                 |
| clei_code           | string | Type inferred from '-'                                 |
| pn_bom_codeitem     | string | Type inferred from '-'                                 |
| rev_issue_number    | string | Type inferred from '-'                                 |
| model               | string | Type inferred from '--'                                |
| manufacturer        | string | Type inferred from '--'                                |
| date_of_manufacture | string | Type inferred from '-'                                 |
| user_label          | string | Type inferred from '-'                                 |
| description         | string | Type inferred from '-'                                 |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_fbb_u2000_sfp_information** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_fbb_u2000_sfp_information`:

| year  | month | day | #Rows | #Files | Size     | Format | Location                                                                                            |
|-------|-------|-----|-------|--------|----------|--------|-----------------------------------------------------------------------------------------------------|
| 2019  | 11    | 13  | 2820  | 1      | 962.46KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=13 |
| 2019  | 11    | 14  | 659   | 1      | 222.51KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=14 |
| 2019  | 11    | 15  | 904   | 1      | 305.07KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=15 |
| 2019  | 11    | 16  | 659   | 1      | 222.51KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=16 |
| 2019  | 11    | 17  | 659   | 1      | 222.51KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=17 |
| 2019  | 11    | 18  | 92    | 1      | 33.05KB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=18 |
| 2019  | 11    | 19  | 1033  | 1      | 348.15KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=19 |
| 2019  | 11    | 20  | 2277  | 1      | 788.35KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 659   | 1      | 222.51KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 3572  | 1      | 1.19MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 1970  | 1      | 664.23KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=23 |
| 2019  | 11    | 24  | 2023  | 1      | 692.56KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=24 |
| 2019  | 11    | 25  | 1610  | 1      | 542.07KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/sfp_information/year=2019/month=11/day=25 |
| Total | .     | .   | 18937 | 13     | 6.30MB   | .      | .                                                                                                   |

<a name="subcard"></a>
## Subcard Report

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_fbb_u2000_subcard`, en la cual se depositan los datos:

| name                      | type   | comment                                 |
|---------------------------|--------|-----------------------------------------|
| ne                        | string | Type inferred from 'MXCMXM01RTCOREBH01' |
| subboard_name             | string | Type inferred from 'CR52EBGE 1/0'       |
| subboard_type             | string | Type inferred from 'ETH_12XGE_CARD'     |
| subrack_id                | string | Type inferred from '1'                  |
| slot_number               | string | Type inferred from '1'                  |
| subslot_number            | string | Type inferred from '0'                  |
| subboard_status           | string | Type inferred from 'Normal'             |
| hardware_version          | string | Type inferred from 'CR52EBGE REV A'     |
| software_version          | string | Type inferred from '--'                 |
| snbar_code                | string | Type inferred from '030GSG10B1000130'   |
| alias                     | string | Type inferred from '-'                  |
| subboard_description      | string | Type inferred from 'CX600               |
| remarks                   | string | Type inferred from '-'                  |
| customized_column         | string | Type inferred from '-'                  |
| pnbom_codeitem            | string | Type inferred from '03030GSG'           |
| subboard_manufacture_date | string | Type inferred from '2011-01-11'         |
| model                     | string | Type inferred from '--'                 |
| rev_issue_number          | string | Type inferred from '00'                 |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_fbb_u2000_subcard** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_fbb_u2000_subcard`:

| year  | month | day | #Rows | #Files | Size    | Format | Location                                                                                    |
|-------|-------|-----|-------|--------|---------|--------|---------------------------------------------------------------------------------------------|
| 2019  | 11    | 13  | 5162  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=13 |
| 2019  | 11    | 14  | 5162  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=14 |
| 2019  | 11    | 15  | 5162  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=15 |
| 2019  | 11    | 16  | 5162  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=16 |
| 2019  | 11    | 17  | 5162  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=17 |
| 2019  | 11    | 18  | 5162  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=18 |
| 2019  | 11    | 19  | 5161  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=19 |
| 2019  | 11    | 20  | 5161  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 5161  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 5161  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 5161  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=23 |
| 2019  | 11    | 24  | 5161  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=24 |
| 2019  | 11    | 25  | 5161  | 2      | 2.09MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subcard/year=2019/month=11/day=25 |
| Total | .     | .   | 67099 | 26     | 27.22MB | .      | .                                                                                           |

<a name="subrack"></a>
## Subrack Report

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_fbb_u2000_subrack`, en la cual se depositan los datos:

| name                    | type   | comment                                                       |
|-------------------------|--------|---------------------------------------------------------------|
| ne                      | string | Type inferred from 'MXCMXM01RTCOREBH01'                       |
| subrack_name            | string | Type inferred from 'CX600-X3 frame'                           |
| subrack_type            | string | Type inferred from 'CX600-X3'                                 |
| subrack_id              | string | Type inferred from '1'                                        |
| software_version        | string | Type inferred from 'VRP (R) software                          |
| ne_id                   | string | Type inferred from '0-0'                                      |
| alias                   | string | Type inferred from '-'                                        |
| subrack_status          | string | Type inferred from 'Normal'                                   |
| snbar_code              | string | Type inferred from '--'                                       |
| telecommunications_room | string | Type inferred from '-'                                        |
| rack                    | string | Type inferred from '-'                                        |
| subrack_no              | string | Type inferred from '--'                                       |
| pnbom_codeitem          | string | Type inferred from '--'                                       |
| description             | string | Type inferred from 'CX600-X3 frame'                           |
| manufacture_date        | string | Type inferred from '--'                                       |
| subnet                  | string | Type inferred from 'MSO-REV-M2'                               |
| subnet_path             | string | Type inferred from 'Physical Root/DATACOMM/MX-REV/MSO-REV-M2' |
| equipment_no            | string | Type inferred from '-'                                        |
| remarks                 | string | Type inferred from '-'                                        |
| customized_column       | string | Type inferred from '-'                                        |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_fbb_u2000_subrack** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_fbb_u2000_subrack`:

| year  | month | day | #Rows  | #Files | Size    | Format | Location                                                                                    |
|-------|-------|-----|--------|--------|---------|--------|---------------------------------------------------------------------------------------------|
| 2019  | 11    | 13  | 8134   | 2      | 3.90MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=13 |
| 2019  | 11    | 14  | 8133   | 2      | 3.90MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=14 |
| 2019  | 11    | 15  | 8141   | 2      | 3.90MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=15 |
| 2019  | 11    | 16  | 8141   | 2      | 3.90MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=16 |
| 2019  | 11    | 17  | 8141   | 1      | 3.90MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=17 |
| 2019  | 11    | 18  | 8141   | 1      | 3.90MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=18 |
| 2019  | 11    | 19  | 8141   | 2      | 3.90MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=19 |
| 2019  | 11    | 20  | 8141   | 2      | 3.90MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 8140   | 1      | 3.90MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 8139   | 2      | 3.90MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 8143   | 2      | 3.91MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=23 |
| 2019  | 11    | 24  | 8143   | 2      | 3.91MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=24 |
| 2019  | 11    | 25  | 8143   | 2      | 3.91MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/subrack/year=2019/month=11/day=25 |
| Total | .     | .   | 105821 | 23     | 50.75MB | .      | .                                                                                           |

<a name="microwave"></a>
## Microwave Link Report

Los archivos de las fuente  `Microwave_link_report` no se cargaron en el Data Lake de forma completa debido a que los archivos en el SFTP presentan inconsistencias en la información que impiden su completa ingestión:

1. Hay filas erróneas en el archivo, por regla general la última fila del archivo no tiene todas las columnas en el archivo `.csv`.

![Registros incompletos en el archivo original][img9]

2. Parece que los archivos están incompletos si se toma como referencia el data de número de registros que aparece en la aprte superior de los archivos, este difícilmente coincide con el número de filas reales.

![No conciden los números de filas][img10]

Los registros que si se cargaron tienen las siguientes características:

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_fbb_u2000_microwave_link_report`, en la cual se depositan los datos:

| name                                               | type   | comment                               |
|----------------------------------------------------|--------|---------------------------------------|
| link_name                                          | string | Type inferred from 'PT'               |
| source_physical_location                           | string | Type inferred from 'null'             |
| source_ne_name                                     | string | Type inferred from 'MXHORI9001MW01'   |
| source_ne_id                                       | string | Type inferred from '8-192'            |
| source_board                                       | string | Type inferred from '10-ISU2'          |
| source_port                                        | string | Type inferred from '1(RTNIF-1)'       |
| sink_physical_location                             | string | Type inferred from 'null'             |
| sink_ne_name                                       | string | Type inferred from 'MXVERCMM0484MW01' |
| sink_ne_id                                         | string | Type inferred from '8-193'            |
| sink_board                                         | string | Type inferred from '5-ISU2'           |
| sink_port                                          | string | Type inferred from '1(RTNIF-1)'       |
| level                                              | string | Type inferred from 'Hybrid(84Mbit/s)' |
| up_and_down_rate_ratiotxrx                         | string | Type inferred from '-'                |
| source_protect_type                                | string | Type inferred from '1+1(HSB)'         |
| sink_protect_type                                  | string | Type inferred from '1+1(HSB)'         |
| source_protection_group_id                         | string | Type inferred from '2'                |
| sink_protection_group_id                           | string | Type inferred from '1'                |
| source_protect_unit_type                           | string | Type inferred from 'Protect Unit'     |
| sink_protect_unit_type                             | string | Type inferred from 'Protect Unit'     |
| source_revertive_mode                              | string | Type inferred from 'Non-Revertive'    |
| sink_revertive_mode                                | string | Type inferred from 'Non-Revertive'    |
| source_protection_group_active_work_unit           | string | Type inferred from 'Protect Unit'     |
| sink_protection_group_active_work_unit             | string | Type inferred from 'Protect Unit'     |
| source_xpic_group_id                               | string | Type inferred from '-'                |
| sink_xpic_group_id                                 | string | Type inferred from '-'                |
| source_xpic_group_capacity_mbits                   | string | Type inferred from '-'                |
| sink_xpic_group_capacity_mbits                     | string | Type inferred from '-'                |
| source_xpic_polarization_direction                 | string | Type inferred from '-'                |
| sink_xpic_polarization_direction                   | string | Type inferred from '-'                |
| source_xpic_adjoin_neid                            | string | Type inferred from '-'                |
| sink_xpic_adjoin_neid                              | string | Type inferred from '-'                |
| source_xpic_adjoin_linkid                          | string | Type inferred from '-'                |
| sink_xpic_adjoin_linkid                            | string | Type inferred from '-'                |
| source_frequencyghz                                | string | Type inferred from '15'               |
| sink_frequencyghz                                  | string | Type inferred from '15'               |
| source_odu_frequency_rangemhz                      | string | Type inferred from '[15228.000        |
| sink_odu_frequency_rangemhz                        | string | Type inferred from '[14500.000        |
| source_equipment_infomation                        | string | Type inferred from 'XMC-2'            |
| sink_equipment_infomation                          | string | Type inferred from 'XMC-2'            |
| source_station_type                                | string | Type inferred from 'TX high'          |
| sink_station_type                                  | string | Type inferred from 'TX low'           |
| source_ne_frequency_mhz                            | string | Type inferred from '15299.0'          |
| sink_ne_frequency_mhz                              | string | Type inferred from '14571.0'          |
| source_ne_radio_work_mode                          | string | Type inferred from '0E1               |
| sink_ne_radio_work_mode                            | string | Type inferred from '0E1               |
| source_ne_preset_value_of_transmit_power           | string | Type inferred from '22.0'             |
| sink_ne_preset_value_of_transmit_power             | string | Type inferred from '22.0'             |
| source_ne_current_value_of_transmit_power          | string | Type inferred from '-55.0'            |
| sink_ne_current_value_of_transmit_power            | string | Type inferred from '-55.0'            |
| source_ne_preset_value_of_receive_power            | string | Type inferred from '-10'              |
| sink_ne_preset_value_of_receive_power              | string | Type inferred from '-10.0'            |
| source_ne_current_value_of_receive_power           | string | Type inferred from '-47.2'            |
| sink_ne_current_value_of_receive_power             | string | Type inferred from '-46.9'            |
| source_ne_max_value_of_transmit_power_of_24hour_pm | string | Type inferred from '-55.0'            |
| sink_ne_max_value_of_transmit_power_of_24hour_pm   | string | Type inferred from '-55.0'            |
| source_ne_min_value_of_transmit_power_of_24hour_pm | string | Type inferred from '-55.0'            |
| sink_ne_min_value_of_transmit_power_of_24hour_pm   | string | Type inferred from '-55'              |
| source_ne_max_value_of_receive_power_of_24hour_pm  | string | Type inferred from '-47.0'            |
| sink_ne_max_value_of_receive_power_of_24hour_pm    | string | Type inferred from '-46.8'            |
| source_ne_min_value_of_receive_power_of_24hour_pm  | string | Type inferred from '-47.4'            |
| sink_ne_min_value_of_receive_power_of_24hour_pm    | string | Type inferred from '-47.2'            |
| source_ne_guaranteed_e1_capacity                   | string | Type inferred from '0'                |
| sink_ne_guaranteed_e1_capacity                     | string | Type inferred from '0'                |
| source_ne_occupied_e1_capacity                     | string | Type inferred from '0'                |
| sink_ne_occupied_e1_capacity                       | string | Type inferred from '0'                |
| source_ne_e1_capacity_usage_                       | string | Type inferred from '-'                |
| sink_ne_e1_capacity_usage_                         | string | Type inferred from '-'                |
| source_ne_ethernet_capacity_mbits                  | string | Type inferred from '83.273'           |
| sink_ne_ethernet_capacity_mbits                    | string | Type inferred from '83.273'           |
| source_ne_max_ethernet_throughput_kbps             | string | Type inferred from '81203'            |
| sink_ne_max_ethernet_throughput_kbps               | string | Type inferred from '94356'            |
| source_ne_min_ethernet_throughput_kbps             | string | Type inferred from '0'                |
| sink_ne_min_ethernet_throughput_kbps               | string | Type inferred from '0'                |
| source_ne_average_ethernet_throughput_kbps         | string | Type inferred from '17420'            |
| sink_ne_average_ethernet_throughput_kbps           | string | Type inferred from '69425'            |
| source_ne_atpc_enable_status                       | string | Type inferred from 'Disabled'         |
| sink_ne_atpc_enable_status                         | string | Type inferred from 'Disabled'         |
| source_ne_atpc_upper_threshold                     | string | Type inferred from '-'                |
| sink_ne_atpc_upper_threshold                       | string | Type inferred from '-'                |
| source_ne_atpc_lower_threshold                     | string | Type inferred from '-'                |
| sink_ne_atpc_lower_threshold                       | string | Type inferred from '-'                |
| source_ne_atpc_automatic_threshold_enable_status   | string | Type inferred from 'Disabled'         |
| sink_ne_atpc_automatic_threshold_enable_status     | string | Type inferred from 'Disabled'         |
| source_ne_atpc_upper_automatic_threshold           | string | Type inferred from '-'                |
| sink_ne_atpc_upper_automatic_threshold             | string | Type inferred from '-'                |
| source_ne_atpc_lower_automatic_threshold           | string | Type inferred from '-'                |
| sink_ne_atpc_lower_automatic_threshold             | string | Type inferred from '-'                |
| source_ne_am_status                                | string | Type inferred from 'Disabled'         |
| sink_ne_am_status                                  | string | Type inferred from 'Disabled'         |
| source_am_full_capacity_modulation_format          | string | Type inferred from '/'                |
| sink_am_full_capacity_modulation_format            | string | Type inferred from '/'                |
| source_am_guaranteed_capacity_modulation_format    | string | Type inferred from '/'                |
| sink_am_guaranteed_capacity_modulation_format      | string | Type inferred from '/'                |
| highestorder_am_scheme_for_source_ne               | string | Type inferred from '256QAM'           |
| highestorder_am_scheme_for_sink_ne                 | string | Type inferred from '256QAM'           |
| lowestorder_am_scheme_for_source_ne                | string | Type inferred from 'QPSK'             |
| lowestorder_am_scheme_for_sink_ne                  | string | Type inferred from 'QPSK'             |
| link_id                                            | string | Type inferred from '2763'             |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_fbb_u2000_port** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_fbb_u2000_microwave_link_report`:

| year  | month | day | #Rows  | #Files | Size     | Format | Location                                                                                                  |
|-------|-------|-----|--------|--------|----------|--------|-----------------------------------------------------------------------------------------------------------|
| 2019  | 11    | 12  | 4354   | 2      | 3.89MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=12 |
| 2019  | 11    | 13  | 10312  | 2      | 9.26MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=13 |
| 2019  | 11    | 14  | 7639   | 2      | 6.86MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=14 |
| 2019  | 11    | 15  | 6098   | 2      | 5.51MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=15 |
| 2019  | 11    | 16  | 6317   | 2      | 5.66MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=16 |
| 2019  | 11    | 17  | 11684  | 2      | 10.48MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=17 |
| 2019  | 11    | 18  | 7891   | 2      | 7.09MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=18 |
| 2019  | 11    | 19  | 7713   | 2      | 6.92MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=19 |
| 2019  | 11    | 20  | 5359   | 2      | 4.82MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 12676  | 2      | 11.41MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 5523   | 2      | 4.97MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 7261   | 2      | 6.54MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=23 |
| 2019  | 11    | 24  | 12246  | 2      | 11.00MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=24 |
| 2019  | 11    | 25  | 18047  | 2      | 16.18MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=25 |
| 2019  | 11    | 26  | 6194   | 2      | 5.62MB   | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/TX/microwave_link_report/year=2019/month=11/day=26 |
| Total | .     | .   | 129314 | 30     | 116.22MB | .      | .                                                                                                         |

## Componentes del procesos de ingestion:

### 1. Ingestion y Serialización via NiFi

Los datos son ingestados al Data Lake usando los siguientes flujos de NiFi:

- Para las fuentes que se encuentran dentro del grupo **G - INVENTORYDUMP**:

| Flujo NiFi              | Fuente ingestada     |
|-------------------------|----------------------|
| G – BOARD REPORT        | Board_Report…        |
| G – NE REPORT           | NE_Report…           |
| G – OPTICAL MODULE      | Optical_Module…      |
| G – PORT REPORT         | Port_Report…         |
| G – SFP INFORMATION     | SFP_Information…     |
| G – SUBCARD INFORMATION | Subcard_Information… |
| G – SUBRACK INFORMATION | Subrack_Information… |

- Para las fuentes que se encuentran dentro del grupo **G - PFM OUTPUT**:

| Flujo NiFi     | Fuente ingestada |
|----------------|------------------|
| G - PM_IG80034 | PM_IG80034_15_…  |
| G - PM_IG80097 | PM_IG80097_15_…  |
| G - PM_IG80099 | PM_IG80099_15_…  |
| G - PM_IG80115 | PM_IG80115_15_…  |
| G - PM_IG80123 | PM_IG80123_15_…  |
| G - PM_IG80232 | PM_IG80232_15_…  |

- Para las fuentes que se encuentran dentro del grupo **G - RTNLINKDUMP**:

| Flujo NiFi              | Fuente ingestada     |
|-------------------------|----------------------|
| G – RTNLINKDUMP         | Microwave_Link…      |

Todos los flujos tienen la misma estructura generaL:

![Activo Fijo NiFi General View][img6]

Pipeline General NiFi

Los flujos varian entre ellos en los siguientes aspectos:
- El filtro del archivo a ingestar en el procesador GetSFTP como se describe en el apartado [Descripcion del FTP]().
- El campo `datasetName` que tiene que referenciar a su fuente de acuerdo a la lista que aparece al [inicio](#main) de este documento.
- El nombre del esquema de avro que se escribe en el SFTP (parámetro `var_HPathLogSchema`).
- La ruta de HDFS en donde se depositan los datos al final del proceso (parámetro `var_HPathData`).

![Activo Fijo NiFi Detail View][img7]

Detalle del Pipeline.

### 2. Aplicación de Reglas de Estandarización del Esquema `Kite`

Las siguientes reglas se aplicarón para estandarizar el esquema de los datos que se genera al convertir los datos al formato Avro para todos los flujos de GPON:

- Eliminado de caracteres especiales en el encabezado del archivo inestado.

```
${'$1':replace("-",""):replace("[",""):replace("]",""):replace(" ","_"):replace("ñ","n"):replace("#","Num"):replace("Í","I"):replace("(",""):replace(")","")}$2
```

- Remplazo de espacios por guiones bajos ( _ ) en el encabezado del archivo ingestado.

```
${'$1':replace(" ","_")}$2
```

### 3. Generación de la Evolución del Esquema via `Kite`

La generación del esquema con Kite se invoca a través del siguiente comando:

```
./rci_ingesta_generacion_avro.sh {parametro0} 
```

El comando necesita un parámetro para funcionar, el cual contiene el valor que identifica a la fuente en  la documentación de Kite: [AX_IM_FrameworkIngestion_CommandExecutionV2.xlsx](http://10.103.133.122/app/owncloud/f/14481174). Es único para cada flujo de NiFi como se especifica en la siguiente tabla:

| Flujo NiFi              | Archivo a ingestar   | Valor | Ejemplo                             |
|-------------------------|----------------------|:-----:|-------------------------------------|
| G – BOARD REPORT        | Board_Report…        | 21    | ./rci_ingesta_generacion_avro.sh 21 |
| G – NE REPORT           | NE_Report…           | 22    | ./rci_ingesta_generacion_avro.sh 22 |
| G - OPTICAL MODULE      | Optical_Module…      | 23    | ./rci_ingesta_generacion_avro.sh 23 |
| G – PORT REPORT         | Port_Report…         | 24    | ./rci_ingesta_generacion_avro.sh 24 |
| G – SFP INFORMATION     | SFP_Information…     | 25    | ./rci_ingesta_generacion_avro.sh 25 |
| G – SUBCARD INFORMATION | Subcard_Information… | 26    | ./rci_ingesta_generacion_avro.sh 26 |
| G – SUBRACK INFORMATION | Subrack_Information… | 27    | ./rci_ingesta_generacion_avro.sh 27 |
| G – RTNLINKDUMP         | Microwave_Link…      | 28    | ./rci_ingesta_generacion_avro.sh 28 |

Ejemplo para el flujo NiFi `G – NE REPORT `:

```
./rci_ingesta_generacion_avro.sh 22
```

__3. Estrategia Incremental vía `Spark`__

Debido a la naturaleza de los datos la fuente no requiere hacer cálculo de incrementales, por lo tanto, cada ingestión se inserta de forma completa. Este proceso se realiza mediante un script de [Spark](../Globales/SparkAxity), el cual se invoca mediante una linea de ejecución que necesita 15 parámetros:

```
spark-submit --master {parametro1} --deploy-mode {parametro2} --name {parametro3} --queue={parametro4} -class {parametro5} {parametro6} {parametro7} {parametro8} {parametro9} {parametro10} {parametr11} {parametro12} {parametro13} {parametro14} {parametro15}
```

- Especificación de parámetros del proceso Spark:

| Parámetro     |  Descripción del Parámetro                               |
|---------------|----------------------------------------------------------|
|  parametro1   |   Modo de ejecución de aplicación spark.                 |
|  parametro2   |   Modo en que se despliega la aplicación.                |
|  parametro3   |   Nombre de la aplicación spark.                         |
|  parametro4   |   Nombre del recurso queue.                              |
|  parametro5   |   Nombre de la clase.                                    |
|  parametro6   |   Ruta del archivo jar.                                  |
|  parametro7   |   Directorio de área stage de datos.                     |
|  parametro8   |   Nombre de la tabla destino.                            |
|  parametro9   |   Nombre del atributo hash_id.                           |
|  parametro10  |   Formato de registro de almacenamiento.                 |
|  parametro11  |   Campos de cálculo para llave Hash.                     |
|  parametro12  |   Ruta del archivo avro de cifra de control.             |
|  parametro13  |   Directorio de salida de cifra control.                 |
|  parametro14  |   Indicador de tipo de incrementalidad: full ó nofull.   |
|  parametro15  |   Número de compactación de coalesce.                    |

Los siguientes parámetros son distintos para cada uno de los flujos de NiFi que componen FBB-TX:

- parametro3
- parametro7
- parametro8
- parametro11
- parametro12
- parametro13

El valor que debe de tomar cada uno de estos parámetros por flujo de NiFi se indica en la siguiente tabla:

| Flujo NiFi                |  Archivo a ingestar    |  Valor de `parametro3`                      |  Valor de `parametro7`                                     |  Valor de `parametro8`             |  Valor de `parametro11`                                                        |  Valor de `parametro12`                                                  |  Valor de `parametro13`                                                      |
|---------------------------|------------------------|---------------------------------------------|------------------------------------------------------------|------------------------------------|--------------------------------------------------------------------------------|--------------------------------------------------------------------------|------------------------------------------------------------------------------|
| G – BOARD REPORT          | Board_Report…          |  'Delta Spark Board Report TX'              | /data/RCI/raw/Gestores/U2000/TX/data/board                 | tx_fbb_u2000_board                 | NE,Board_Type,Subrack_ID,Slot_ID,SNBar_Code,Alias,filedate                     | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_board.avro                 | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_board/20191126_5               |
|  G – NE REPORT            | NE_Report…             |  'Delta Spark NE Report TX'                 | /data/RCI/raw/Gestores/U2000/TX/data/ne                    | tx_fbb_u2000_ne                    | NE_Name,NE_IP_Address,NE_MAC_Address,Create_Time,Running_Status,Alias,filedate | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_ne.avro                    | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_ne/20191126                    |
| G - OPTICALMODULE         | Optical_Module…        |  'Delta Spark Optical Module TX'            | /data/RCI/raw/Gestores/U2000/TX/data/optical_module        | tx_fbb_u2000_optical_module        | Serial_No,NE_Name,Port_Name,Receive_Status,Transmit_Status,filedate            | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_optical_module.avro        | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_optical_module/20191126        |
|  G – PORT REPORT          | Port_Report…           |  'Delta Spark Port Report TX'               | /data/RCI/raw/Gestores/U2000/TX/data/port                  | tx_fbb_u2000_port                  | NE_Name,Shelf_No,Slot_No,SubSlot_No,Port_No,Port_Level,Management,filedate     | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_port.avro                  | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_port/20191126_2                |
|  G – SFP INFORMATION      | SFP_Information…       |  'Delta Spark SFP Information TX'           | /data/RCI/raw/Gestores/U2000/TX/data/sfp_information       | tx_fbb_u2000_sfp_information       | Port,SFP_Type,SN_Bar_Code,Rev_Issue_Number,filedate                            | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_sfp_information.avro       | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_sfp_information/20191126       |
|  G – SUBCARD INFORMATION  | Subcard_Information…   |  'Delta Spark Subcard Information TX'       | /data/RCI/raw/Gestores/U2000/TX/data/subcard               | tx_fbb_u2000_subcard               | NE,Subboard_Name,Subboard_Type,Subboard_Status,SNBar_Code,Alias,filedate       | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_subcard.avro               | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_subcard/20191126               |
|  G – SUBRACK INFORMATION  | Subrack_Information…   |  'Delta Spark Subrack Information TX'       | /data/RCI/raw/Gestores/U2000/TX/data/subrack               | tx_fbb_u2000_subrack               | NE,NE_ID,SNBar_Code,Manufacture_Date,filedate                                  | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_subrack.avro               | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_subrack/20191126_1             |
| G – RTNLINKDUMP           | Microwave_Link…        |  'Delta Spark Microwave'                    | /data/RCI/raw/Gestores/U2000/TX/data/microwave_link_report | tx_fbb_u2000_microwave_link_report | Link_Name,Source_NE_Name,Sink_NE_Name,Link_ID,filedate                         | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_microwave_link_report.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_Microwave_Link_Report/20191126 |

Los demás parametros se configuran igual para todos los flujos de NiFi de FBB-TX.

Ejemplo para el flujo `G - BOARD REPORT`:

```
spark-submit --master yarn-cluster --deploy-mode cluster --name 'Delta SPARK' --queue=root.rci --class com.axity.DataFlowIngestion /home/fh967x/SparkNew/spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-dependencies.jar /data/RCI/raw/Gestores/U2000/TX/data/board tx_fbb_u2000_board hash_id hive NE,Board_Type,Subrack_ID,Slot_ID,SNBar_Code,Alias,filedate /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_board.avro /data/RCI/stg/hive/work/ctl/ctrl_tx_fbb_u2000_board/20191126 full 1

```
El valor de `parametro 15` puede variar dependiendo de la cantidad de archivos que se van a ingestar pero en flujo de trabajo ordinario este debe de estar configurado con el valor `1`.


## Referencias al Framework de Ingestión

- [Framework de Ingestion](../Globales/)

## Código Fuente Local

- [Codigo NiFi - NFR](NFR/)

## Código Fuente Globales

- [Codigo NiFi](../Globales/NIFICustomProcessorXLSX)
- [Codigo Spark](../Globales/SparkAxity)
- [Codigo Kite](../Globales/attdlkrci)



[img1]: images/FBBTX-nifi-01.png "Logo Axity"
[img2]: images/FBBTX-nifi-02.png "Grupo U2000TX"
[img3]: images/FBBTX-nifi-03.png "Grupo INVENTORY DUMP"
[img4]: images/FBBTX-nifi-04.png "Grupo PFM OUTPUT"
[img5]: images/FBBTX-nifi-05.png "Grupo RTNLINKDUMP"
[img6]: images/FBBTX-nifi-06.png "Vista general del flujo"
[img7]: images/FBBTX-nifi-07.png "Detalle del flujo NiFi"
[img8]: images/FBBTX-nifi-08.png "Procesador GetSFTP"
[img9]: images/FBBTX-nifi-09.png "La última fila del archivo generalmente no tiene todas las columnas"
[img10]: images/FBBTX-nifi-10.png "Se indican 3,901 registros pero solo hay 342"