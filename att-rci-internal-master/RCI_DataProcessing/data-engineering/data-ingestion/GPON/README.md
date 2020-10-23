![EncabezadoAxity][img1]

# Documentación Data Ingestion para la fuente ATT **U2000 GPON**

La ingesta de la fuente U2000 GPON requirió la construcción de varios flujos de NiFi debido a que en el repositorio de origen existen archivos con estructuras distintas y que deben de guardarse en tablas separadas. Debido a la naturaleza de los datos se han creado dos grupos:

![Grupo GPON][img4]

Vista general de **G - U200 GPON**

 Esta fuente se compone de quince flujos de NiFi y se separan de la siguiente manera:

 <a name="main"></a>

1. **inventoryDump**
    * [Board_Report](#board)
    * [Port_Report](#port)
    * [NE_Report](#ne)
    * [CMC_Information](#cmc)
    * [Subcard_Report](#subcard)
    * [Subrack_Report](#subrack)

![Grupo inventoryDump][img2]

Vista general de **G - INVENTORYDUMP** 

2. **pfm_output**
    * [PM_IG80034](#80034)
    * [PM_IG80097](#80097)
    * [PM_IG80099](#80099)
    * [PM_IG80115](#80115)
    * [PM_IG80123](#80123)
    * [PM_IG80232](#80307)
    * [PM_IG80307](#80307)
    * [PM_IG80333](#80307)
    * [PM_IG80372](#80307)

![Grupo pfm_output][img3]

Vista general de **G - PFM OUTPUT**

<a name="cmc"></a>
<a name="subcard"></a>
<a name="80372"></a>

Los archivos de las fuentes `CMC_Information`, `Subcard_Report`, `Port Report` e `IG80372` no se han cargado en el Data Lake debido a que los archivos en el SFTP no contienen datos aunque sus flujos si fueron construidos y probados, estos existen dentro del flujo de NiFi esperando a que las fuentes contengan datos.

El detalle de cada uno de los flujos será explicado con mas detalle en los siguientes apartados.

## Descripcion del `FTP`

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14481174), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

En el directorio del SFTP todos los archivos de U2000 GPON viven en un misma carpeta, por lo que el flujo esta configurado para buscar los archivos de forma recursiva usando la siguiente expresión regular en el procesador GetSFTP:

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
A continuación se detalla el estado de la tabla de Hive `tx_gpon_u2000_board`, en la cual se depositan los datos:

| name              | type   | comment                                       |
|-------------------|--------|-----------------------------------------------|
| ne                | string | Type inferred from 'MXSINHOM0552OLT01'        |
| board_name        | string | Type inferred from 'Frame:0/Slot:1/Subslot:0' |
| board_type        | string | Type inferred from 'H801NH1A'                 |
| ne_type           | string | Type inferred from 'MA5608T'                  |
| subrack_id        | string | Type inferred from '0'                        |
| slot_id           | string | Type inferred from '1'                        |
| hardware_version  | string | Type inferred from 'H801NH1A VER A'           |
| software_version  | string | Type inferred from '--'                       |
| snbar_code        | string | Type inferred from '020EJHD0B8000051'         |
| alias             | string | Type inferred from '-'                        |
| remarks           | string | Type inferred from '-'                        |
| customized_column | string | Type inferred from '-'                        |
| subrack_type      | string | Type inferred from 'H801MABR'                 |
| ne_id             | string | Type inferred from '--'                       |
| bios_version      | string | Type inferred from '--'                       |
| fpga_version      | string | Type inferred from '--'                       |
| board_status      | string | Type inferred from 'Normal'                   |
| pnbom_codeitem    | string | Type inferred from '--'                       |
| model             | string | Type inferred from '--'                       |
| rev_issue_number  | string | Type inferred from '--'                       |
| management        | string | Type inferred from 'Managed'                  |
| description       | string | Type inferred from '--'                       |
| manufacture_date  | string | Type inferred from '--'                       |
| create_time       | string | Type inferred from '--'                       |

Las siguientes columnas son datos de control que se insertan al momento de la ingesta para identificar a la fuente, el archivo original no las incluye. Por ser las mismas columnas para todos los flujos de NiFi de GPON solo se listarán una vez aunque todas las tablas de GPON los llevan:

| name               | type   | comment                                                   |
|--------------------|--------|-----------------------------------------------------------|
| filedate           | bigint | Type inferred from '20190722'                             |
| filename           | string | Type inferred from 'Board_Report_2019-07-22_06-00-07.csv' |
| fileip             | string | Type inferred from '10.105.100.2'                         |
| hash_id            | string | Type inferred from 'null'                                 |
| sourceid           | string | Type inferred from 'Gestores-U2000-GPON'                  |
| registry_state     | string | Type inferred from 'null'                                 |
| datasetname        | string | Type inferred from 'Board_Report'                         |
| timestamp          | bigint | Type inferred from '20191128'                             |
| transaction_status | string | Type inferred from 'null'                                 |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_gpon_u2000_board** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_gpon_u2000_board`:

| year | month | day | #Rows | #Files | Size   | Format | Location                                                                                    |
|------|-------|-----|-------|--------|--------|--------|---------------------------------------------------------------------------------------------|
| 2018 | 12    | 2   | 3900  | 1      | 1.65MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/board/year=2018/month=12/day=2  |
| 2018 | 12    | 3   | 3900  | 1      | 1.65MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/board/year=2018/month=12/day=3  |
| 2018 | 12    | 4   | 3900  | 1      | 1.65MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/board/year=2018/month=12/day=4  |
| 2018 | 12    | 5   | 3900  | 1      | 1.65MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/board/year=2018/month=12/day=5  |
| 2018 | 12    | 6   | 3901  | 1      | 1.65MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/board/year=2018/month=12/day=6  |
| 2018 | 12    | 7   | 3901  | 1      | 1.65MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/board/year=2018/month=12/day=7  |
| 2018 | 12    | 8   | 3900  | 1      | 1.65MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/board/year=2018/month=12/day=8  |
| 2018 | 12    | 9   | 3900  | 1      | 1.65MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/board/year=2018/month=12/day=9  |
| 2018 | 12    | 10  | 3900  | 1      | 1.65MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/board/year=2018/month=12/day=10 |
| 2018 | 12    | 11  | 3883  | 1      | 1.64MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/board/year=2018/month=12/day=11 |

<a name="ne"></a>
## NE Report

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_gpon_u2000_ne`, en la cual se depositan los datos:

| name               | type   | comment                                                |
|--------------------|--------|--------------------------------------------------------|
| ne_name            | string | Type inferred from 'MXJALGDL0707OLT01'                 |
| ne_type            | string | Type inferred from 'MA5608T'                           |
| ne_ip_address      | string | Type inferred from '10.105.51.228'                     |
| ne_mac_address     | string | Type inferred from 'D4-94-E8-00-50-02'                 |
| ne_id              | string | Type inferred from '--'                                |
| software_version   | string | Type inferred from 'MA5600V800R015C10'                 |
| physical_location  | string | Type inferred from 'REGION R5 - GDL'                   |
| create_time        | string | Type inferred from '03/10/2016 21:53:22'               |
| fibercable_count   | string | Type inferred from '0'                                 |
| running_status     | string | Type inferred from 'Normal'                            |
| subnet             | string | Type inferred from 'ORIENTE_AT&T'                      |
| subnet_path        | string | Type inferred from 'Physical Root/R5/GDL/ORIENTE_AT&T' |
| alias              | string | Type inferred from '--'                                |
| remarks            | string | Type inferred from 'null'                              |
| patch_version_list | string | Type inferred from 'SPC101 HP1006'                     |
| customized_column  | string | Type inferred from '-'                                 |
| lsr_id             | string | Type inferred from '--'                                |
| maintenance_status | string | Type inferred from 'Normal'                            |
| gateway_type       | string | Type inferred from '--'                                |
| gateway            | string | Type inferred from '--'                                |
| optical_ne         | string | Type inferred from '--'                                |
| subrack_type       | string | Type inferred from '--'                                |
| conference_call    | string | Type inferred from '--'                                |
| orderwire_phone    | string | Type inferred from '--'                                |
| ne_subtype         | string | Type inferred from 'MA5608T'                           |
| filedate           | bigint | Type inferred from '20190611'                          |
| filename           | string | Type inferred from 'NE_Report_2019-06-11_06-00-06.csv' |
| fileip             | string | Type inferred from '10.105.100.2'                      |
| hash_id            | string | Type inferred from 'null'                              |
| sourceid           | string | Type inferred from 'Gestores-U2000-GPON'               |
| registry_state     | string | Type inferred from 'null'                              |
| datasetname        | string | Type inferred from 'NE_Report'                         |
| timestamp          | bigint | Type inferred from '20191128'                          |
| transaction_status | string | Type inferred from 'null'                              |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_gpon_u2000_ne** se generan de forma diaria usando el campo de auditoría **filedate**. La tabla contiene 359 particiones,  algunas de las particiones son:

    Sentencia `show partitions tx_gpon_u2000_ne`:

| year | month | day | #Rows | #Files | Size     | Format | Location                                                                                 |
|------|-------|-----|-------|--------|----------|--------|------------------------------------------------------------------------------------------|
| 2018 | 12    | 2   | 1126  | 1      | 586.75KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=2  |
| 2018 | 12    | 3   | 1126  | 1      | 586.75KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=3  |
| 2018 | 12    | 4   | 1126  | 1      | 586.75KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=4  |
| 2018 | 12    | 5   | 1126  | 1      | 586.75KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=5  |
| 2018 | 12    | 6   | 1126  | 1      | 586.72KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=6  |
| 2018 | 12    | 7   | 1126  | 1      | 586.72KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=7  |
| 2018 | 12    | 8   | 1126  | 1      | 586.71KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=8  |
| 2018 | 12    | 9   | 1126  | 1      | 586.70KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=9  |
| 2018 | 12    | 10  | 1126  | 1      | 586.70KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=10 |
| 2018 | 12    | 11  | 1124  | 1      | 585.45KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=11 |
| 2018 | 12    | 12  | 1114  | 1      | 580.38KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=12 |
| 2018 | 12    | 13  | 1116  | 1      | 581.39KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=13 |
| 2018 | 12    | 14  | 1118  | 1      | 582.34KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=14 |
| 2018 | 12    | 15  | 1118  | 1      | 582.35KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=15 |
| 2018 | 12    | 16  | 1118  | 1      | 582.35KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=16 |
| 2018 | 12    | 17  | 1117  | 1      | 581.77KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=17 |
| 2018 | 12    | 18  | 1117  | 1      | 581.84KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=18 |
| 2018 | 12    | 19  | 1117  | 1      | 581.84KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=19 |
| 2018 | 12    | 20  | 1117  | 1      | 581.83KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=20 |
| 2018 | 12    | 21  | 1116  | 1      | 581.22KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=21 |
| 2018 | 12    | 22  | 1117  | 1      | 581.77KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=22 |
| 2018 | 12    | 23  | 1117  | 1      | 581.69KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=23 |
| 2018 | 12    | 24  | 1117  | 1      | 581.69KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=24 |
| 2018 | 12    | 25  | 1117  | 1      | 581.70KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=25 |
| 2018 | 12    | 26  | 1117  | 1      | 581.70KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=26 |
| 2018 | 12    | 27  | 1117  | 1      | 581.69KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ne/year=2018/month=12/day=27 |

<a name="subrack"></a>
## Subrack Report

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_gpon_u2000_subrack`, en la cual se depositan los datos:

| name                    | type   | comment                                                     |
|-------------------------|--------|-------------------------------------------------------------|
| ne                      | string | Type inferred from 'MXJALGDL0707OLT01'                      |
| subrack_name            | string | Type inferred from 'Frame:0'                                |
| subrack_type            | string | Type inferred from 'H801MABR'                               |
| subrack_id              | string | Type inferred from '0'                                      |
| software_version        | string | Type inferred from '--'                                     |
| ne_id                   | string | Type inferred from '--'                                     |
| alias                   | string | Type inferred from 'H801MABR_0'                             |
| subrack_status          | string | Type inferred from 'Normal'                                 |
| snbar_code              | string | Type inferred from '021RSTW0F7000511'                       |
| telecommunications_room | string | Type inferred from '-'                                      |
| rack                    | string | Type inferred from '-'                                      |
| subrack_no              | string | Type inferred from '--'                                     |
| pnbom_codeitem          | string | Type inferred from '--'                                     |
| description             | string | Type inferred from '--'                                     |
| manufacture_date        | string | Type inferred from '2015-07-25'                             |
| subnet                  | string | Type inferred from 'ORIENTE_AT&T'                           |
| subnet_path             | string | Type inferred from 'Physical Root/R5/GDL/ORIENTE_AT&T'      |
| equipment_no            | string | Type inferred from '-'                                      |
| remarks                 | string | Type inferred from '-'                                      |
| customized_column       | string | Type inferred from '-'                                      |
| filedate                | bigint | Type inferred from '20190722'                               |
| filename                | string | Type inferred from 'Subrack_Report_2019-07-22_06-00-07.csv' |
| fileip                  | string | Type inferred from '10.105.100.2'                           |
| hash_id                 | string | Type inferred from 'null'                                   |
| sourceid                | string | Type inferred from 'Gestores-U2000-GPON'                    |
| registry_state          | string | Type inferred from 'null'                                   |
| datasetname             | string | Type inferred from 'Subrack_report'                         |
| timestamp               | bigint | Type inferred from '20191128'                               |
| transaction_status      | string | Type inferred from 'null'                                   |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_gpon_u2000_subrack** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_gpon_u2000_subrack`:

| year | month | day | #Rows | #Files | Size     | Format | Location                                                                                      |
|------|-------|-----|-------|--------|----------|--------|-----------------------------------------------------------------------------------------------|
| 2018 | 12    | 2   | 1096  | 1      | 469.53KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=2  |
| 2018 | 12    | 3   | 1096  | 1      | 469.53KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=3  |
| 2018 | 12    | 4   | 1096  | 1      | 469.53KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=4  |
| 2018 | 12    | 5   | 1096  | 1      | 469.53KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=5  |
| 2018 | 12    | 6   | 1097  | 1      | 469.95KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=6  |
| 2018 | 12    | 7   | 1097  | 1      | 469.95KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=7  |
| 2018 | 12    | 8   | 1098  | 1      | 470.63KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=8  |
| 2018 | 12    | 9   | 1098  | 1      | 470.63KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=9  |
| 2018 | 12    | 10  | 1098  | 1      | 470.63KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=10 |
| 2018 | 12    | 11  | 1095  | 1      | 469.42KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=11 |
| 2018 | 12    | 12  | 1085  | 1      | 465.62KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=12 |
| 2018 | 12    | 13  | 1086  | 1      | 466.06KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=13 |
| 2018 | 12    | 14  | 1086  | 1      | 466.06KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=14 |
| 2018 | 12    | 15  | 1086  | 1      | 466.06KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=15 |
| 2018 | 12    | 16  | 1086  | 1      | 466.06KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=16 |
| 2018 | 12    | 17  | 1085  | 1      | 465.87KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=17 |
| 2018 | 12    | 18  | 1086  | 1      | 466.47KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=18 |
| 2018 | 12    | 19  | 1086  | 1      | 466.47KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=19 |
| 2018 | 12    | 20  | 1086  | 1      | 466.47KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=20 |
| 2018 | 12    | 21  | 1085  | 1      | 466.15KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=21 |
| 2018 | 12    | 22  | 1087  | 1      | 467.00KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=22 |
| 2018 | 12    | 23  | 1087  | 1      | 466.93KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/subrack/year=2018/month=12/day=23 |

<a name="80034"></a>
## PM_IG80034

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_gpon_u2000_ig80034`, en la cual se depositan los datos:

| name                               | type   | comment                                                      |
|------------------------------------|--------|--------------------------------------------------------------|
| deviceid                           | string | Type inferred from '7340225'                                 |
| devicename                         | string | Type inferred from 'MXNLEMTY0832OLT01'                       |
| resourcename                       | string | Type inferred from 'MXNLEMTY0832OLT01/Frame:0/Slot:2/Port:0' |
| collectiontime                     | string | Type inferred from '2019-11-25 10:00:00'                     |
| granularityperiod                  | string | Type inferred from '15'                                      |
| downstream_bandwidth_occupancy     | string | Type inferred from 'null'                                    |
| upstream_bandwidth_occupancy       | string | Type inferred from 'null'                                    |
| tx_octets_during_collection_period | string | Type inferred from 'null'                                    |
| rx_octets_during_collection_period | string | Type inferred from 'null'                                    |
| total_number_of_rx_frames          | string | Type inferred from 'null'                                    |
| total_number_of_tx_frames          | string | Type inferred from 'null'                                    |
| the_upstream_discarded_packets     | string | Type inferred from 'null'                                    |
| the_downstream_discarded_packets   | string | Type inferred from 'null'                                    |
| tx_rate                            | string | Type inferred from '0.0'                                     |
| rx_rate                            | string | Type inferred from '0.0'                                     |
| total_number_of_tx_octets          | string | Type inferred from 'null'                                    |
| total_number_of_rx_octets          | string | Type inferred from 'null'                                    |
| filedate                           | bigint | Type inferred from '20191125'                                |
| filename                           | string | Type inferred from 'PM_IG80034_15_201911251000_01.csv'       |
| filetime                           | string | Type inferred from '1000'                                    |
| hash_id                            | string | Type inferred from 'null'                                    |
| sourceid                           | string | Type inferred from 'Gestores-U2000-GPON'                     |
| registry_state                     | string | Type inferred from 'null'                                    |
| datasetname                        | string | Type inferred from 'PM_IG80034'                              |
| timestamp                          | bigint | Type inferred from '20191129'                                |
| transaction_status                 | string | Type inferred from 'null'                                    |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_gpon_u2000_ig80034** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_gpon_u2000_ig80034`:

| year  | month | day | #Rows  | #Files | Size    | Format | Location                                                                                      |
|-------|-------|-----|--------|--------|---------|--------|-----------------------------------------------------------------------------------------------|
| 2019  | 11    | 24  | 125067 | 1      | 46.34MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80034/year=2019/month=11/day=24 |
| 2019  | 11    | 25  | 125152 | 1      | 46.37MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80034/year=2019/month=11/day=25 |
| Total |      |    | 250219 | 2      | 92.71MB |       |                                                                                              |

<a name="80097"></a>
## PM_IG80097

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_gpon_u2000_ig80097`, en la cual se depositan los datos:

| name                                                                            | type   | comment                                                |
|---------------------------------------------------------------------------------|--------|--------------------------------------------------------|
| deviceid                                                                        | string | Type inferred from '7340505'                           |
| devicename                                                                      | string | Type inferred from 'MXJALPTL0819OLT01'                 |
| resourcename                                                                    | string | Type inferred from 'TLAQUEPAQUE_AT&T/VLANID=395'       |
| collectiontime                                                                  | string | Type inferred from '2019-11-23 19:30:00'               |
| granularityperiod                                                               | string | Type inferred from '15'                                |
| vlan_upstream_account_of_network_interface_by_packet_during_collection_period   | string | Type inferred from '0.0'                               |
| vlan_downstream_account_of_network_interface_by_packet_during_collection_period | string | Type inferred from '0.0'                               |
| vlan_upstream_account_of_network_interface_by_packet                            | string | Type inferred from '0.0'                               |
| vlan_downstream_account_of_network_interface_by_packet                          | string | Type inferred from '0.0'                               |
| upstream_bandwidth_occupancy                                                    | string | Type inferred from 'null'                              |
| downstream_bandwidth_occupancy                                                  | string | Type inferred from 'null'                              |
| filedate                                                                        | bigint | Type inferred from '20191123'                          |
| filename                                                                        | string | Type inferred from 'PM_IG80097_15_201911231930_01.csv' |
| filetime                                                                        | string | Type inferred from '1930'                              |
| hash_id                                                                         | string | Type inferred from 'null'                              |
| sourceid                                                                        | string | Type inferred from 'Gestores-U2000-GPON'               |
| registry_state                                                                  | string | Type inferred from 'null'                              |
| datasetname                                                                     | string | Type inferred from 'PM_IG80097'                        |
| timestamp                                                                       | bigint | Type inferred from '20191129'                          |
| transaction_status                                                              | string | Type inferred from 'null'                              |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_gpon_u2000_ig80097** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_gpon_u2000_ig80097`:

| year  | month | day | #Rows | #Files | Size     | Format | Location                                                                                      |
|-------|-------|-----|-------|--------|----------|--------|-----------------------------------------------------------------------------------------------|
| 2019  | 11    | 20  | 96    | 1      | 34.96KB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80097/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 96    | 1      | 34.96KB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80097/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 96    | 1      | 34.96KB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80097/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 96    | 1      | 34.96KB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80097/year=2019/month=11/day=23 |
| Total | .     | .   | 384   | 4      | 139.82KB | .      | .                                                                                             |

<a name="80099"></a>
## PM_IG80099

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_gpon_u2000_ig80099`, en la cual se depositan los datos:

| name                                     | type   | comment                                                      |
|------------------------------------------|--------|--------------------------------------------------------------|
| deviceid                                 | string | Type inferred from '7341307'                                 |
| devicename                               | string | Type inferred from 'MXDIFXCH0950OLT01'                       |
| resourcename                             | string | Type inferred from 'MXDIFXCH0950OLT01/Frame:0/Slot:2/Port:2' |
| collectiontime                           | string | Type inferred from '2019-11-25 03:00:00'                     |
| granularityperiod                        | string | Type inferred from '15'                                      |
| total_number_of_tx_discarded_packets     | string | Type inferred from 'null'                                    |
| total_number_of_tx_error_packets         | string | Type inferred from 'null'                                    |
| total_number_of_tx_broadcast_packets     | string | Type inferred from 'null'                                    |
| tx_power                                 | string | Type inferred from '-2.29'                                   |
| rx_power                                 | string | Type inferred from '-2.32'                                   |
| total_number_of_rx_unicast_packets       | string | Type inferred from 'null'                                    |
| total_number_of_rx_multicast_packets     | string | Type inferred from 'null'                                    |
| total_number_of_rx_broadcast_packets     | string | Type inferred from 'null'                                    |
| total_number_of_tx_unicast_packets       | string | Type inferred from 'null'                                    |
| total_number_of_tx_multicast_packets     | string | Type inferred from 'null'                                    |
| total_number_of_tx_nonunicast_packets    | string | Type inferred from 'null'                                    |
| total_number_of_rx_nonunicast_packets    | string | Type inferred from 'null'                                    |
| total_number_of_rx_discarded_packets     | string | Type inferred from 'null'                                    |
| total_number_of_rx_error_packets         | string | Type inferred from 'null'                                    |
| total_number_of_rx_unknownprotos_packets | string | Type inferred from 'null'                                    |
| filedate                                 | bigint | Type inferred from '20191125'                                |
| filename                                 | string | Type inferred from 'PM_IG80099_15_201911250300_01.csv'       |
| filetime                                 | string | Type inferred from '300'                                     |
| hash_id                                  | string | Type inferred from 'null'                                    |
| sourceid                                 | string | Type inferred from 'Gestores-U2000-GPON'                     |
| registry_state                           | string | Type inferred from 'null'                                    |
| datasetname                              | string | Type inferred from 'PM_IG80099'                              |
| timestamp                                | bigint | Type inferred from '20191129'                                |
| transaction_status                       | string | Type inferred from 'null'                                    |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_gpon_u2000_ig80099** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_gpon_u2000_ig80099`:

| year  | month | day | #Rows | #Files | Size    | Format | Location                                                                                      |
|-------|-------|-----|-------|--------|---------|--------|-----------------------------------------------------------------------------------------------|
| 2019  | 11    | 20  | 10848 | 1      | 3.88MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80099/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 10848 | 1      | 3.88MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80099/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 10848 | 1      | 3.88MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80099/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 10848 | 1      | 3.88MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80099/year=2019/month=11/day=23 |
| 2019  | 11    | 25  | 10848 | 1      | 3.88MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80099/year=2019/month=11/day=25 |
| Total | .     | .   | 54240 | 5      | 19.41MB | .      | .                                                                                             |

<a name="80115"></a>
## PM_IG80115

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_gpon_u2000_ig80115`, en la cual se depositan los datos:

| name                                             | type   | comment                                                               |
|--------------------------------------------------|--------|-----------------------------------------------------------------------|
| deviceid                                         | string | Type inferred from '7340188'                                          |
| devicename                                       | string | Type inferred from 'MXMORCVA0223OLT01'                                |
| resourcename                                     | string | Type inferred from 'MXMORCVA0223OLT01/Frame:0/Slot:0/Port:0/ONU ID:0' |
| collectiontime                                   | string | Type inferred from '2019-11-25 05:00:00'                              |
| granularityperiod                                | string | Type inferred from '15'                                               |
| ont_optics_temperature_selector                  | string | Type inferred from 'null'                                             |
| ont_optics_bias_current_selector                 | string | Type inferred from 'null'                                             |
| ont_optics_txpower_selector                      | string | Type inferred from '2.29'                                             |
| ont_optics_rxpower_selector                      | string | Type inferred from 'null'                                             |
| ont_optics_supply_voltage                        | string | Type inferred from 'null'                                             |
| the_olt_received_onu_power_of_the_optical_module | string | Type inferred from 'null'                                             |
| filedate                                         | bigint | Type inferred from '20191125'                                         |
| filename                                         | string | Type inferred from 'PM_IG80115_15_201911250500_01.csv'                |
| filetime                                         | string | Type inferred from '500'                                              |
| hash_id                                          | string | Type inferred from 'null'                                             |
| sourceid                                         | string | Type inferred from 'Gestores-U2000-GPON'                              |
| registry_state                                   | string | Type inferred from 'null'                                             |
| datasetname                                      | string | Type inferred from 'PM_IG80115'                                       |
| timestamp                                        | bigint | Type inferred from '20191129'                                         |
| transaction_status                               | string | Type inferred from 'null'                                             |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_gpon_u2000_ig80115** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_gpon_u2000_ig80115`:

| year  | month | day | #Rows | #Files | Size    | Format | Location                                                                                      |
|-------|-------|-----|-------|--------|---------|--------|-----------------------------------------------------------------------------------------------|
| 2019  | 11    | 20  | 9696  | 1      | 3.33MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80115/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 9696  | 1      | 3.33MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80115/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 9696  | 1      | 3.33MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80115/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 9696  | 1      | 3.33MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80115/year=2019/month=11/day=23 |
| 2019  | 11    | 25  | 9696  | 1      | 3.34MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80115/year=2019/month=11/day=25 |
| Total | .     | .   | 48480 | 5      | 16.65MB | .      | .                                                                                             |

<a name="80123"></a>
## PM_IG80123

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_gpon_u2000_ig80123`, en la cual se depositan los datos:

| name                                                                                      | type   | comment                                                                 |
|-------------------------------------------------------------------------------------------|--------|-------------------------------------------------------------------------|
| deviceid                                                                                  | string | Type inferred from '7340399'                                            |
| devicename                                                                                | string | Type inferred from 'MXYUCMER0426OLT01'                                  |
| resourcename                                                                              | string | Type inferred from 'MXYUCMER0426OLT01/Frame:0/Slot:0/Port:1/ONU ID:1/U' |
| collectiontime                                                                            | string | Type inferred from '2019-11-25 12:45:00'                                |
| granularityperiod                                                                         | string | Type inferred from '15'                                                 |
| count_of_the_mac_sublayer_receiving_errors                                                | string | Type inferred from 'null'                                               |
| count_of_filtered_pppoe_frames                                                            | string | Type inferred from 'null'                                               |
| count_of_sent_frames                                                                      | string | Type inferred from 'null'                                               |
| count_of_discarded_frames_due_to_delay                                                    | string | Type inferred from 'null'                                               |
| count_of_received_unicast_frames                                                          | string | Type inferred from 'null'                                               |
| count_of_sent_unicast_frames                                                              | string | Type inferred from 'null'                                               |
| count_of_sent_broadcast_frames                                                            | string | Type inferred from 'null'                                               |
| count_of_sent_multicast_frames                                                            | string | Type inferred from 'null'                                               |
| count_of_received_pause_flow_control_frames                                               | string | Type inferred from 'null'                                               |
| count_of_sent_pause_flow_control_frames                                                   | string | Type inferred from 'null'                                               |
| count_of_received_1519_oversizeoctet_frames                                               | string | Type inferred from 'null'                                               |
| the_total_number_of_packets_received                                                      | string | Type inferred from 'null'                                               |
| the_total_number_of_packets_received_that_were_less_than_64_octets_long                   | string | Type inferred from 'null'                                               |
| the_total_number_of_received_packets_including_bad_packets_that_were_64_octets_long       | string | Type inferred from 'null'                                               |
| the_total_number_of_received_packets_including_bad_packets_that_were_65127_octets_long    | string | Type inferred from 'null'                                               |
| the_total_number_of_packets_including_bad_packets_received_that_were_128255_octets_long   | string | Type inferred from 'null'                                               |
| the_total_number_of_packets_including_bad_packets_received_that_were_256511_octets_long   | string | Type inferred from 'null'                                               |
| the_total_number_of_packets_including_bad_packets_received_that_were_5121023_octets_long  | string | Type inferred from 'null'                                               |
| the_total_number_of_packets_including_bad_packets_received_that_were_10241518_octets_long | string | Type inferred from 'null'                                               |
| count_of_fcs_errors                                                                       | string | Type inferred from 'null'                                               |
| count_of_excessive_collisions                                                             | string | Type inferred from 'null'                                               |
| count_of_collisions_in_the_512bittimes_range                                              | string | Type inferred from 'null'                                               |
| count_of_overlong_frames                                                                  | string | Type inferred from 'null'                                               |
| count_of_buffer_rx_overflows                                                              | string | Type inferred from 'null'                                               |
| count_of_buffer_tx_overflows                                                              | string | Type inferred from 'null'                                               |
| count_of_singlecollision_frames                                                           | string | Type inferred from 'null'                                               |
| count_of_multiplecollisions_frames                                                        | string | Type inferred from 'null'                                               |
| count_of_sqe_synchronized_queue_element_test_error_messages                               | string | Type inferred from 'null'                                               |
| count_of_deferred_frames                                                                  | string | Type inferred from 'null'                                               |
| count_of_the_mac_sublayer_transmission_errors                                             | string | Type inferred from 'null'                                               |
| count_of_carrier_sense_errors                                                             | string | Type inferred from 'null'                                               |
| count_of_frame_alignment_errors                                                           | string | Type inferred from 'null'                                               |
| count_of_received_bad_frames_octets                                                       | string | Type inferred from 'null'                                               |
| count_of_sent_bad_frames_octets                                                           | string | Type inferred from 'null'                                               |
| upstream_rate                                                                             | string | Type inferred from '0.0'                                                |
| downstream_rate                                                                           | string | Type inferred from '0.0'                                                |
| filedate                                                                                  | bigint | Type inferred from '20191125'                                           |
| filename                                                                                  | string | Type inferred from 'PM_IG80123_15_201911251245_01.csv'                  |
| filetime                                                                                  | string | Type inferred from '1245'                                               |
| hash_id                                                                                   | string | Type inferred from 'null'                                               |
| sourceid                                                                                  | string | Type inferred from 'Gestores-U2000-GPON'                                |
| registry_state                                                                            | string | Type inferred from 'null'                                               |
| datasetname                                                                               | string | Type inferred from 'PM_IG80123'                                         |
| timestamp                                                                                 | bigint | Type inferred from '20191129'                                           |
| transaction_status                                                                        | string | Type inferred from 'null'                                               |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_gpon_u2000_ig80123** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_gpon_u2000_ig80123`:

| year  | month | day | #Rows | #Files | Size    | Format | Location                                                                                      |
|-------|-------|-----|-------|--------|---------|--------|-----------------------------------------------------------------------------------------------|
| 2019  | 11    | 20  | 7584  | 1      | 3.29MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80123/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 7584  | 1      | 3.29MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80123/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 7583  | 1      | 3.29MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80123/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 7584  | 1      | 3.29MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80123/year=2019/month=11/day=23 |
| 2019  | 11    | 25  | 7584  | 1      | 3.28MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80123/year=2019/month=11/day=25 |
| Total | .     | .   | 37919 | 5      | 16.43MB | .      | .                                                                                             |

<a name="80232"></a>
## PM_IG80232

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_gpon_u2000_ig80232`, en la cual se depositan los datos:

| name                                    | type   | comment                                                      |
|-----------------------------------------|--------|--------------------------------------------------------------|
| deviceid                                | string | Type inferred from '7340232'                                 |
| devicename                              | string | Type inferred from 'MXJALGDL0714OLT01'                       |
| resourcename                            | string | Type inferred from 'MXJALGDL0714OLT01/Frame:0/Slot:0/Port:0' |
| collectiontime                          | string | Type inferred from '2019-11-21 21:30:00'                     |
| granularityperiod                       | string | Type inferred from '15'                                      |
| upstream_rate                           | string | Type inferred from '8207.45'                                 |
| downstream_rate                         | string | Type inferred from '39165.61'                                |
| gpon_uni_upstream_bandwidth_occupancy   | string | Type inferred from 'null'                                    |
| gpon_uni_downstream_bandwidth_occupancy | string | Type inferred from 'null'                                    |
| filedate                                | bigint | Type inferred from '20191121'                                |
| filename                                | string | Type inferred from 'PM_IG80232_15_201911212130_01.csv'       |
| filetime                                | string | Type inferred from '2130'                                    |
| hash_id                                 | string | Type inferred from 'null'                                    |
| sourceid                                | string | Type inferred from 'Gestores-U2000-GPON'                     |
| registry_state                          | string | Type inferred from 'null'                                    |
| datasetname                             | string | Type inferred from 'PM_IG80232'                              |
| timestamp                               | bigint | Type inferred from '20191129'                                |
| transaction_status                      | string | Type inferred from 'null'                                    |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_gpon_u2000_ig80232** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_gpon_u2000_ig80232`:

| year  | month | day | #Rows  | #Files | Size     | Format | Location                                                                                      |
|-------|-------|-----|--------|--------|----------|--------|-----------------------------------------------------------------------------------------------|
| 2019  | 11    | 20  | 74496  | 2      | 25.07MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80232/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 74496  | 2      | 25.07MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80232/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 74496  | 2      | 25.07MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80232/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 74496  | 2      | 25.07MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80232/year=2019/month=11/day=23 |
| Total | .     | .   | 297984 | 8      | 100.27MB | .      | .                                                                                             |

<a name="80307"></a>
## PM_IG80307

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_gpon_u2000_ig80307`, en la cual se depositan los datos:

| name                               | type   | comment                                                               |
|------------------------------------|--------|-----------------------------------------------------------------------|
| deviceid                           | string | Type inferred from '7340169'                                          |
| devicename                         | string | Type inferred from 'MXJALZAP1015OLT01'                                |
| resourcename                       | string | Type inferred from 'MXJALZAP1015OLT01/Frame:0/Slot:0/Port:0/ONU ID:0' |
| collectiontime                     | string | Type inferred from '2019-11-25 16:15:00'                              |
| granularityperiod                  | string | Type inferred from '15'                                               |
| ont_upstream_rate                  | string | Type inferred from '14732.01'                                         |
| ont_downstream_rate                | string | Type inferred from '68055.31'                                         |
| ont_upstream_bandwidth_occupancy   | string | Type inferred from '0.0'                                              |
| ont_downstream_bandwidth_occupancy | string | Type inferred from '0.0'                                              |
| filedate                           | bigint | Type inferred from '20191125'                                         |
| filename                           | string | Type inferred from 'PM_IG80307_15_201911251615_01.csv'                |
| filetime                           | string | Type inferred from '1615'                                             |
| hash_id                            | string | Type inferred from 'null'                                             |
| sourceid                           | string | Type inferred from 'Gestores-U2000-GPON'                              |
| registry_state                     | string | Type inferred from 'null'                                             |
| datasetname                        | string | Type inferred from 'PM_IG80307'                                       |
| timestamp                          | bigint | Type inferred from '20191129'                                         |
| transaction_status                 | string | Type inferred from 'null'                                             |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_gpon_u2000_ig80307** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_gpon_u2000_ig80307`:

| year  | month | day | #Rows | #Files | Size    | Format | Location                                                                                      |
|-------|-------|-----|-------|--------|---------|--------|-----------------------------------------------------------------------------------------------|
| 2019  | 11    | 20  | 6336  | 1      | 2.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80307/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 6333  | 1      | 2.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80307/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 6336  | 1      | 2.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80307/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 6333  | 2      | 2.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80307/year=2019/month=11/day=23 |
| 2019  | 11    | 25  | 6335  | 2      | 2.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80307/year=2019/month=11/day=25 |
| Total | .     | .   | 31673 | 7      | 11.06MB | .      | .                                                                                             |

<a name="80333"></a>
## PM_IG80333

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_gpon_u2000_ig80333`, en la cual se depositan los datos:

| name                                  | type   | comment                                                      |
|---------------------------------------|--------|--------------------------------------------------------------|
| deviceid                              | string | Type inferred from '7340576'                                 |
| devicename                            | string | Type inferred from 'MXMORCVA0220OLT01'                       |
| resourcename                          | string | Type inferred from 'MXMORCVA0220OLT01/Frame:0/Slot:0/Port:0' |
| collectiontime                        | string | Type inferred from '2019-11-25 21:45:00'                     |
| granularityperiod                     | string | Type inferred from '15'                                      |
| uni_port_optics_temperature_selector  | bigint | Type inferred from '36'                                      |
| uni_port_optics_bias_current_selector | string | Type inferred from 'null'                                    |
| uni_port_optics_supply_voltage        | string | Type inferred from 'null'                                    |
| uni_port_optics_txpower_selector      | string | Type inferred from '3.83'                                    |
| filedate                              | bigint | Type inferred from '20191125'                                |
| filename                              | string | Type inferred from 'PM_IG80333_15_201911252145_01.csv'       |
| filetime                              | string | Type inferred from '2145'                                    |
| hash_id                               | string | Type inferred from 'null'                                    |
| sourceid                              | string | Type inferred from 'Gestores-U2000-GPON'                     |
| registry_state                        | string | Type inferred from 'null'                                    |
| datasetname                           | string | Type inferred from 'PM_IG80333'                              |
| timestamp                             | bigint | Type inferred from '20191129'                                |
| transaction_status                    | string | Type inferred from 'null'                                    |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_gpon_u2000_ig80333** se generan de forma diaria usando el campo de auditoría **filedate**. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_gpon_u2000_ig80333`:

| year  | month | day | #Rows  | #Files | Size     | Format | Location                                                                                      |
|-------|-------|-----|--------|--------|----------|--------|-----------------------------------------------------------------------------------------------|
| 2019  | 11    | 20  | 74496  | 2      | 24.59MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80333/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 74496  | 2      | 24.59MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80333/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 74496  | 2      | 24.59MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80333/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 74496  | 2      | 24.59MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80333/year=2019/month=11/day=23 |
| 2019  | 11    | 25  | 74496  | 1      | 24.58MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/U2000/GPON/ig80333/year=2019/month=11/day=25 |
| Total | .     | .   | 372480 | 9      | 122.93MB | .      | .                                                                                             |

## Componentes del procesos de ingestion:

### 1. Ingestion y Serialización via NiFi

Los datos son ingestados al Data Lake usando los siguientes flujos de NiFi:

- Para las fuentes que se encuentran dentro del grupo **G - INVENTORYDUMP**:

| Flujo NiFi              | Fuente ingestada     |
|-------------------------|----------------------|
| G – BOARD REPORT        | Board_Report…        |
| G – PORT REPORT         | Port_Report…         |
| G – NE REPORT           | NE_Report…           |
| G – CMC INFORMATION     | CMC_Information…     |
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
| G - PM_IG80307 | PM_IG80307_15_…  |
| G - PM_IG80333 | PM_IG80333_15_…  |
| G - PM_IG80372 | PM_IG80372_15_…  |

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

El comando necesita un parámetro para funcionar, el cual contiene el valor que identifica a la fuente en  la documentación de Kite:[AX_IM_FrameworkIngestion_CommandExecutionV2.xlsx](http://10.103.133.122/app/owncloud/f/14481174). Es único para cada flujo de NiFi como se especifica en la siguiente tabla:

| Flujo NiFi              | Archivo a ingestar   | Valor | Ejemplo                             |
|-------------------------|----------------------|:-----:|-------------------------------------|
| G – BOARD REPORT        | Board_Report…        | 38    | ./rci_ingesta_generacion_avro.sh 38 |
| G – PORT REPORT         | Port_Report…         | 39    | ./rci_ingesta_generacion_avro.sh 39 |
| G – NE REPORT           | NE_Report…           | 40    | ./rci_ingesta_generacion_avro.sh 40 |
| G – CMC INFORMATION     | CMC_Information…     | 41    | ./rci_ingesta_generacion_avro.sh 41 |
| G – SUBCARD INFORMATION | Subcard_Information… | 42    | ./rci_ingesta_generacion_avro.sh 42 |
| G – SUBRACK INFORMATION | Subrack_Information… | 43    | ./rci_ingesta_generacion_avro.sh 43 |
| G - PM_IG80034          | PM_IG80034_15_…      | 29    | ./rci_ingesta_generacion_avro.sh 29 |
| G - PM_IG80097          | PM_IG80097_15_…      | 30    | ./rci_ingesta_generacion_avro.sh 30 |
| G - PM_IG80099          | PM_IG80099_15_…      | 31    | ./rci_ingesta_generacion_avro.sh 31 |
| G - PM_IG80115          | PM_IG80115_15_…      | 32    | ./rci_ingesta_generacion_avro.sh 32 |
| G - PM_IG80123          | PM_IG80123_15_…      | 33    | ./rci_ingesta_generacion_avro.sh 33 |
| G - PM_IG80232          | PM_IG80232_15_…      | 34    | ./rci_ingesta_generacion_avro.sh 34 |
| G - PM_IG80307          | PM_IG80307_15_…      | 35    | ./rci_ingesta_generacion_avro.sh 35 |
| G - PM_IG80333          | PM_IG80333_15_…      | 36    | ./rci_ingesta_generacion_avro.sh 36 |
| G - PM_IG80372          | PM_IG80372_15_…      | 37    | ./rci_ingesta_generacion_avro.sh 37 |

Ejemplo para el flujo NiFi `G - PM_IG80333`:

```
./rci_ingesta_generacion_avro.sh 36
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

Los siguientes parámetros son distintos para cada uno de los flujos de NiFi que componen GPON:

- parametro3
- parametro7
- parametro8
- parametro11
- parametro12
- parametro13

El valor que debe de tomar cada uno de estos parámetros por flujo de NiFi se indica en la siguiente tabla:

| Flujo NiFi              | Archivo a ingestar   | Valor de `parametro3`             | Valor de `parametro7`                          | Valor de `parametro8` | Valor de `parametro11`                                                | Valor de `parametro12`                                      | Valor de `parametro13`                                          |
|-------------------------|----------------------|-----------------------------------|------------------------------------------------|-----------------------|-----------------------------------------------------------------------|-------------------------------------------------------------|-----------------------------------------------------------------|
| G – BOARD REPORT        | Board_Report…        | 'Delta Spark Board Report'        | /data/RCI/raw/Gestores/U2000/GPON/data/board   | tx_gpon_u2000_board   | NE,Board_Type,Subrack_ID,Slot_ID,SNBar_Code,Alias                     |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_board.avro   | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_board/20191128   |
| G – PORT REPORT         | Port_Report…         | 'Delta Spark Port Report'         | /data/RCI/raw/Gestores/U2000/GPON/data/port    | tx_gpon_u2000_port    | NE_Name,Shelf_No,Slot_No,SubSlot_No,Port_No,Port_Level,Management     |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_port.avro    | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_port/20191128    |
| G – NE REPORT           | NE_Report…           | 'Delta Spark NE Report'           | /data/RCI/raw/Gestores/U2000/GPON/data/ne      | tx_gpon_u2000_ne      | NE_Name,NE_IP_Address,NE_MAC_Address,Create_Time,Running_Status,Alias |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_ne.avro      | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_ne/20191128      |
| G – CMC INFORMATION     | CMC_Information…     | 'Delta Spark CMC Information'     | /data/RCI/raw/Gestores/U2000/GPON/data/cmc     | tx_gpon_u2000_cmc     |                                                                       |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_cmc.avro     | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_cmc/20191128     |
| G – SUBCARD INFORMATION | Subcard_Information… | 'Delta Spark Subcard Information' | /data/RCI/raw/Gestores/U2000/GPON/data/subcard | tx_gpon_u2000_subcard | NE,Subboard_Name,Subboard_Type,Subboard_Status,SNBar_Code,Alias       |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_subcard.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_subcard/20191128 |
| G – SUBRACK INFORMATION | Subrack_Information… | 'Delta Spark Subrack Information' | /data/RCI/raw/Gestores/U2000/GPON/data/subrack | tx_gpon_u2000_subrack | NE,NE_ID,SNBar_Code,Manufacture_Date                                  |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_subrack.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_subrack/20191128 |
| G - PM_IG80034          | PM_IG80034_15_…      | 'Delta Spark PM IG80034'          | /data/RCI/raw/Gestores/U2000/GPON/data/ig80034 | tx_gpon_u2000_ig80034 | DeviceID,DeviceName,ResourceName,filedate                             |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_ig80034.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_ig80034/20191128 |
| G - PM_IG80097          | PM_IG80097_15_…      | 'Delta Spark PM IG80097'          | /data/RCI/raw/Gestores/U2000/GPON/data/ig80097 | tx_gpon_u2000_ig80097 | DeviceID,DeviceName,ResourceName,filedate                             |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_ig80097.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_ig80097/20191128 |
| G - PM_IG80099          | PM_IG80099_15_…      | 'Delta Spark PM IG80099'          | /data/RCI/raw/Gestores/U2000/GPON/data/ig80099 | tx_gpon_u2000_ig80099 | DeviceID,DeviceName,ResourceName,filedate                             |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_ig80099.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_ig80099/20191128 |
| G - PM_IG80115          | PM_IG80115_15_…      | 'Delta Spark PM IG80115'          | /data/RCI/raw/Gestores/U2000/GPON/data/ig80115 | tx_gpon_u2000_ig80115 | DeviceID,DeviceName,ResourceName,filedate                             |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_ig80115.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_ig80115/20191128 |
| G - PM_IG80123          | PM_IG80123_15_…      | 'Delta Spark PM IG80123'          | /data/RCI/raw/Gestores/U2000/GPON/data/ig80123 | tx_gpon_u2000_ig80123 | DeviceID,DeviceName,ResourceName,filedate                             |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_ig80123.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_ig80123/20191128 |
| G - PM_IG80232          | PM_IG80232_15_…      | 'Delta Spark PM IG80232'          | /data/RCI/raw/Gestores/U2000/GPON/data/ig80232 | tx_gpon_u2000_ig80232 | DeviceID,DeviceName,ResourceName,filedate                             |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_ig80232.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_ig80232/20191128 |
| G - PM_IG80307          | PM_IG80307_15_…      | 'Delta Spark PM IG80307'          | /data/RCI/raw/Gestores/U2000/GPON/data/ig80307 | tx_gpon_u2000_ig80307 | DeviceID,DeviceName,ResourceName,filedate                             |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_ig80307.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_ig80307/20191128 |
| G - PM_IG80333          | PM_IG80333_15_…      | 'Delta Spark PM IG80333'          | /data/RCI/raw/Gestores/U2000/GPON/data/ig80333 | tx_gpon_u2000_ig80333 | DeviceID,DeviceName,ResourceName,filedate                             |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_ig80333.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_ig80333/20191128 |
| G - PM_IG80372          | PM_IG80372_15_…      | 'Delta Spark PM IG80372'          | /data/RCI/raw/Gestores/U2000/GPON/data/ig80372 | tx_gpon_u2000_ig80372 | DeviceID,DeviceName,ResourceName,filedate                             |  /data/RCI/stg/hive/work/ctl/ctl_tx_gpon_u2000_ig80372.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_gpon_u2000_ig80372/20191128 |

Los demás parametros se configuran igual para todos los flujos de NiFi de GPON.

Ejemplo:

```
spark-submit --master yarn-cluster --deploy-mode cluster --name 'Delta SPARK' --queue=root.rci --class com.axity.DataFlowIngestion /home/fh967x/SparkNew/spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-dependencies.jar /data/RCI/raw/AF/data/ tx_fixed_asset hash_id hive ACTIVO,ETIQUETA,SERIE,LOCATION,filedate /data/RCI/stg/hive/work/ctl/ctrl_tx_fixed_asset.avro /data/RCI/stg/hive/work/ctl/ctrl_tx_fixed_asset/20191126 full 1
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



[img1]: images/U2000GPON-nifi-01.png "Logo Axity"
[img2]: images/U2000GPON-nifi-02.png "Grupo PFM OUTPUT"
[img3]: images/U2000GPON-nifi-03.png "Grupo INVENTORY DUMP"
[img4]: images/U2000GPON-nifi-04.png "Grupo GPON"
[img5]: images/U2000GPON-nifi-05.png "Procesador GetSFTP"
[img6]: images/U2000GPON-nifi-06.png "Vista general del flujo"
[img7]: images/U2000GPON-nifi-07.png "Detalle del flujo NiFi"

