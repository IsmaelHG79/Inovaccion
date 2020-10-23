![EncabezadoAxity][imgEncabezado]


# Documentación Data Ingestion para la fuente ATT **U2000 RAN**

Para esta fuente se documentan diferentes flujos de una sola fuente, esto debido a que existen diferentes tablas para su consumo.

## Descripción del `Orígen de Datos`  
Los datos de conexión son los siguientes:
```
Tecnología:       Excel
IP:               10.150.25.149
Directorio:       /FILES_SPLUNK/INVENTARIO/U2000_RAN/Inventario_RAN_{DDMMYYYY}/
USR:              raw_rci
Nombre Archivo:   Inventory_Antenna_{DDMMYYYY}_112230.csv
                  Inventory_Board_{DDMMYYYY}_112230.csv
                  Inventory_Cabinet_{DDMMYYYY}_112230.csv
                  Inventory_Slot_{DDMMYYYY}_112230.csv
                  Inventory_Port_{DDMMYYYY}_112230.csv                                                      
                  Inventory_Subrack_{DDMMYYYY}_112230.csv                  
                  Inventory_RRN_{DDMMYYYY}_112230.csv
                  Inventory_Hostver_{DDMMYYYY}_112230.csv                  

```
## Componentes del procesos de ingestión (Flujo General):

__Ingestión y Serialización via NiFi__

__Flujo Principal__

![FlujoPrincipal][img1]

__Flujo de Subproceso__

![FlujoSubproceso][img2]

__Flujo General Antenna__

![Flujo Principal Antenna][img4]

__SFTP Process__

![SFTP Process][img3]

__File Process__

![File Process][img5]

__Cifra Control__

![Cifra Control][img6]

__Process Avro Schema__

![Process Avro Schema][img7]



[img1]: images/u2000ran-nifi-00.png ""
[img2]: images/u2000ran-nifi-01.png ""
[img3]: images/u2000ran-nifi-02.png ""
[img4]: images/u2000ran-nifi-03.png ""
[img5]: images/u2000ran-nifi-04.png ""
[img6]: images/u2000ran-nifi-05.png ""
[img7]: images/u2000ran-nifi-06.png ""



## Listado de Tablas  

* [Antenna](#Antenna)
* [Board](#Board)
* [Cabinet](#Cabinet)
* [HostVer](#HostVer)
* [Slot](#Slot)
* [Port](#Port)
* [Subrack](#Subrack)
* [RRN](#RRN)


## <a name="Antenna"></a>Antenna

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Antenna](../../../../RCI_DataAnalysis/eda/RAN/README.md)

- **Diccionario de Datos**
  [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/RAN/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_u2000ran_antenna```

  | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                           |
  |----|----------------------|--------------|----------------------------------------------------------------------|
  | 1  | netype               | string       | Type inferred from 'NodeB'                                           |
  | 2  | nefdn                | string       | Type inferred from 'NE=5274'                                         |
  | 3  | nename               | string       | Type inferred from 'HMEX0729'                                        |
  | 4  | antennadeviceid      | string       | Type inferred from '0'                                               |
  | 5  | antennadevicetype    | string       | Type inferred from 'SINGLE_RET'                                      |
  | 6  | dateoflastservice    | string       | Type inferred from 'null'                                            |
  | 7  | dateofmanufacture    | string       | Type inferred from 'null'                                            |
  | 8  | extinfo              | string       | Type inferred from 'null'                                            |
  | 9  | inventoryunitid      | string       | Type inferred from '0'                                               |
  | 10 | inventoryunittype    | string       | Type inferred from 'Hardware'                                        |
  | 11 | revissuenumber       | string       | Type inferred from 'null'                                            |
  | 12 | pnbomcodeitem        | string       | Type inferred from 'null'                                            |
  | 13 | manufacturerdata     | string       | Type inferred from 'ATM3-1'                                          |
  | 14 | model                | string       | Type inferred from 'null'                                            |
  | 15 | antennamodel         | string       | Type inferred from 'ATM3'                                            |
  | 16 | snbarcode            | string       | Type inferred from '0000CN10123648181'                               |
  | 17 | serialnumberex       | string       | Type inferred from 'null'                                            |
  | 18 | sharemode            | string       | Type inferred from 'null'                                            |
  | 19 | unitposition         | string       | Type inferred from 'AntennaDeviceName=RCU1-R-UMTS,AntennaDeviceNo=0' |
  | 20 | vendorname           | string       | Type inferred from 'AN'                                              |
  | 21 | vendorunitfamilytype | string       | Type inferred from 'SINGLE_RET'                                      |
  | 22 | vendorunittypenumber | string       | Type inferred from '0'                                               |
  | 23 | hardwareversion      | string       | Type inferred from '2.0'                                             |

  Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestión.

  | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
  |----|----------------------|--------------|-------------------------------------------------------------------------|
  | 24 | filedate             | bigint       | Type inferred from '20200121'                                           |
  | 25 | filename             | string       | Type inferred from '/home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_' |
  | 26 | hash_id              | string       | Type inferred from 'null'                                               |
  | 27 | sourceid             | string       | Type inferred from 'U2000RAN'                                           |
  | 28 | registry_state       | string       | Type inferred from 'null'                                               |
  | 29 | datasetname          | string       | Type inferred from 'tx_u2000ran_antenna'                                |
  | 30 | timestamp            | bigint       | Type inferred from '20200124'                                           |
  | 31 | transaction_status   | string       | Type inferred from 'null'                                               |    



- **Particiones**

    A continuación se presentan las particiones creadas de la tabla **tx_u2000ran_antenna**.

    Sentencia: ```show partitions rci_network_db.tx_u2000ran_antenna```

    | year | month | #Rows  | #Files | Size    | Format | Incremental stats | Location                                                                                       |
    |------|-------|--------|--------|---------|--------|-------------------|------------------------------------------------------------------------------------------------|
    | 2019 | 11    | 102069 | 5      | 49.56MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/antenna/year=2019/month=11 |
    | 2020 | 1     | 204276 | 10     | 99.01MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/antenna/year=2020/month=1  |


- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_u2000ran_antenna';
    ```    

    | id_execution | table_name          | dateload | avro_name                                                                                     | start_execution  | end_execution    | status |
    |--------------|---------------------|----------|-----------------------------------------------------------------------------------------------|------------------|------------------|--------|
    | 1            | tx_u2000ran_antenna | 20200123 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200114_Inventory_Antenna_20200114_112005.avro | 23/01/2020 12:52 | 23/01/2020 12:53 | 1      |
    | 1            | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20191125_Inventory_Antenna_20191125_161826.avro | 24/01/2020 15:04 | 24/01/2020 15:05 | 1      |
    | 2            | tx_u2000ran_antenna | 20200123 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200114_Inventory_Antenna_20200114_112230.avro | 23/01/2020 12:53 | 23/01/2020 12:54 | 1      |
    | 2            | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20191125_Inventory_Antenna_20191125_162140.avro | 24/01/2020 15:06 | 24/01/2020 15:07 | 1      |
    | 3            | tx_u2000ran_antenna | 20200123 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200114_Inventory_Antenna_20200114_112306.avro | 23/01/2020 12:55 | 23/01/2020 12:56 | 1      |
    | 3            | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20191125_Inventory_Antenna_20191125_162229.avro | 24/01/2020 15:07 | 24/01/2020 15:08 | 1      |
    | 4            | tx_u2000ran_antenna | 20200123 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200114_Inventory_Antenna_20200114_112327.avro | 23/01/2020 12:56 | 23/01/2020 12:57 | 1      |
    | 4            | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20191125_Inventory_Antenna_20191125_162416.avro | 24/01/2020 15:08 | 24/01/2020 15:09 | 1      |
    | 5            | tx_u2000ran_antenna | 20200123 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200114_Inventory_Antenna_20200114_112358.avro | 23/01/2020 13:13 | 23/01/2020 13:14 | 1      |
    | 5            | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20191125_Inventory_Antenna_20191125_162421.avro | 24/01/2020 15:10 | 24/01/2020 15:11 | 1      |
    | 6            | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200114_Inventory_Antenna_20200114_112005.avro | 24/01/2020 15:11 | 24/01/2020 15:12 | 1      |
    | 7            | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200114_Inventory_Antenna_20200114_112230.avro | 24/01/2020 15:12 | 24/01/2020 15:13 | 1      |
    | 8            | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200114_Inventory_Antenna_20200114_112306.avro | 24/01/2020 15:14 | 24/01/2020 15:15 | 1      |
    | 9            | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200114_Inventory_Antenna_20200114_112327.avro | 24/01/2020 15:15 | 24/01/2020 15:16 | 1      |
    | 10           | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200114_Inventory_Antenna_20200114_112358.avro | 24/01/2020 15:17 | 24/01/2020 15:18 | 1      |
    | 11           | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200121_Inventory_Antenna_20200121_110442.avro | 24/01/2020 15:18 | 24/01/2020 15:19 | 1      |
    | 12           | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200121_Inventory_Antenna_20200121_110720.avro | 24/01/2020 15:19 | 24/01/2020 15:20 | 1      |
    | 13           | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200121_Inventory_Antenna_20200121_110745.avro | 24/01/2020 15:21 | 24/01/2020 15:22 | 1      |
    | 14           | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200121_Inventory_Antenna_20200121_110751.avro | 24/01/2020 15:22 | 24/01/2020 15:24 | 1      |
    | 15           | tx_u2000ran_antenna | 20200124 | /data/RCI/raw/gestores/u2000/ran/antenna/data/20200121_Inventory_Antenna_20200121_110801.avro | 24/01/2020 15:24 | 24/01/2020 15:25 | 1      |

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_u2000ran_antenna'
    and dateload = 20200124
    order by filedate asc;
    ```    

    | uuid                                 | rowprocessed | datasetname         | filedate | filename                                                                                                          | sourceid | dateload | read_count | insert_count | update_count | delete_count |
    |--------------------------------------|--------------|---------------------|----------|-------------------------------------------------------------------------------------------------------------------|----------|----------|------------|--------------|--------------|--------------|
    | 2ed98490-53d0-45fd-b2a1-9569883263ba | 29987        | tx_u2000ran_antenna | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/39/20200114_Inventory_Antenna_20200114_112306.csv  | U2000RAN | 20200124 | 29987      | 29987        | 0            | 0            |
    | addf5e56-92f1-4fae-b4f1-bd9e415f1c95 | 8086         | tx_u2000ran_antenna | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/197/20200121_Inventory_Antenna_20200121_110720.csv | U2000RAN | 20200124 | 8086       | 8086         | 0            | 0            |
    | d7d448cb-ffdb-4dd9-83a1-b911a43bd69e | 8062         | tx_u2000ran_antenna | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/197/20200114_Inventory_Antenna_20200114_112230.csv | U2000RAN | 20200124 | 8062       | 8062         | 0            | 0            |
    | 23235286-0bf3-415c-8869-846f92995467 | 22746        | tx_u2000ran_antenna | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/7/20200114_Inventory_Antenna_20200114_112358.csv   | U2000RAN | 20200124 | 22746      | 22746        | 0            | 0            |
    | b2b2d096-b628-40e3-a90f-1402870db604 | 34064        | tx_u2000ran_antenna | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/23/20200114_Inventory_Antenna_20200114_112327.csv  | U2000RAN | 20200124 | 34064      | 34064        | 0            | 0            |
    | 32d961bd-996e-4646-be37-b8d97493f0e5 | 8351         | tx_u2000ran_antenna | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/54/20200114_Inventory_Antenna_20200114_112005.csv  | U2000RAN | 20200124 | 8351       | 8351         | 0            | 0            |
    | aaaa17bb-7baa-4349-aa56-26a7bb314950 | 34259        | tx_u2000ran_antenna | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/23/20191125_Inventory_Antenna_20191125_162229.csv  | U2000RAN | 20200124 | 34259      | 34259        | 0            | 0            |
    | 2911916d-8328-470f-ae19-ebbf5b2d9bd4 | 8303         | tx_u2000ran_antenna | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/54/20191125_Inventory_Antenna_20191125_161826.csv  | U2000RAN | 20200124 | 8303       | 8303         | 0            | 0            |
    | fd54ff79-988a-4ef3-99e8-bb4296e0a397 | 29986        | tx_u2000ran_antenna | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/39/20191125_Inventory_Antenna_20191125_162421.csv  | U2000RAN | 20200124 | 29986      | 29986        | 0            | 0            |
    | 89d36f33-f961-4492-85ee-c2dd81fbac21 | 29970        | tx_u2000ran_antenna | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/39/20200121_Inventory_Antenna_20200121_110801.csv  | U2000RAN | 20200124 | 29970      | 29970        | 0            | 0            |
    | d4575d77-722b-49a2-ac32-9812a34ec33b | 34110        | tx_u2000ran_antenna | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/23/20200121_Inventory_Antenna_20200121_110745.csv  | U2000RAN | 20200124 | 34110      | 34110        | 0            | 0            |
    | b88a381e-da09-45b0-8087-a32ba98b8457 | 22797        | tx_u2000ran_antenna | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/7/20191125_Inventory_Antenna_20191125_162416.csv   | U2000RAN | 20200124 | 22797      | 22797        | 0            | 0            |
    | 8abd2f91-0098-48c3-86b4-9199d04bb591 | 8060         | tx_u2000ran_antenna | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/197/20191125_Inventory_Antenna_20191125_162140.csv | U2000RAN | 20200124 | 8060       | 8060         | 0            | 0            |
    | 249a8420-c74c-48f9-b445-67891da1e77c | 8357         | tx_u2000ran_antenna | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/54/20200121_Inventory_Antenna_20200121_110442.csv  | U2000RAN | 20200124 | 8357       | 8357         | 0            | 0            |
    | 29117116-be7d-4ef7-bb1f-b1914baed955 | 22764        | tx_u2000ran_antenna | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/7/20200121_Inventory_Antenna_20200121_110751.csv   |

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

Especificar parámetros del proceso kite:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 132   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 132
```


## <a name="Board"></a>Board

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Board](../../../../RCI_DataAnalysis/eda/RAN/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/RAN/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_u2000ran_board```

  | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
  |----|----------------------|--------------|-------------------------------------------------------------------------|
  | 1  | netype               | string       | Type inferred from 'NodeB'                                              |
  | 2  | nefdn                | string       | Type inferred from 'NE=5274'                                            |
  | 3  | nename               | string       | Type inferred from 'HMEX0729'                                           |
  | 4  | wifideviceinfo       | string       | Type inferred from 'null'                                               |
  | 5  | biosver              | string       | Type inferred from '18.325.10.017'                                      |
  | 6  | biosverex            | string       | Type inferred from '18.325.10.017'                                      |
  | 7  | boardname            | string       | Type inferred from 'PMU'                                                |
  | 8  | boardtype            | string       | Type inferred from 'WD2M1EPM'                                           |
  | 9  | dateoflastservice    | string       | Type inferred from 'null'                                               |
  | 10 | dateofmanufacture    | string       | Type inferred from '2011-03-28'                                         |
  | 11 | extinfo              | string       | Type inferred from 'null'                                               |
  | 12 | subrackno            | string       | Type inferred from '7'                                                  |
  | 13 | inventoryunitid      | string       | Type inferred from '0'                                                  |
  | 14 | inventoryunittype    | string       | Type inferred from 'Hardware'                                           |
  | 15 | revissuenumber       | string       | Type inferred from '00'                                                 |
  | 16 | pnbomcodeitem        | string       | Type inferred from '02317275'                                           |
  | 17 | lanver               | string       | Type inferred from 'null'                                               |
  | 18 | logicver             | string       | Type inferred from '0'                                                  |
  | 19 | mbusver              | string       | Type inferred from 'null'                                               |
  | 20 | manufacturerdata     | string       | Type inferred from 'Function Module,HERT MPE,WD2M1EPM,Power System Mon' |
  | 21 | model                | string       | Type inferred from 'null'                                               |
  | 22 | moduleno             | string       | Type inferred from '-1'                                                 |
  | 23 | portno               | string       | Type inferred from '-1'                                                 |
  | 24 | cabinetno            | string       | Type inferred from '0'                                                  |
  | 25 | snbarcode            | string       | Type inferred from '21023172756TB3002443'                               |
  | 26 | sharemode            | string       | Type inferred from 'null'                                               |
  | 27 | slotno               | string       | Type inferred from '0'                                                  |
  | 28 | slotpos              | string       | Type inferred from '0'                                                  |
  | 29 | softwareversion      | string       | Type inferred from '128'                                                |
  | 30 | subslotno            | string       | Type inferred from '-1'                                                 |
  | 31 | unitposition         | string       | Type inferred from 'RackNo=0,FrameNo=7,SlotNo=0,SlotPos=0,SubSlotNo=-1' |
  | 32 | userlabel            | string       | Type inferred from 'null'                                               |
  | 33 | vendorname           | string       | Type inferred from 'Huawei'                                             |
  | 34 | vendorunitfamilytype | string       | Type inferred from 'PMU'                                                |
  | 35 | vendorunittypenumber | string       | Type inferred from '0'                                                  |
  | 36 | hardwareversion      | string       | Type inferred from 'PMU.4'                                              |
  | 37 | workmode             | string       | Type inferred from 'null'                                               |

     Las siguientes columnas son creadas para la identidad de la fuente:

  | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
  |----|----------------------|--------------|-------------------------------------------------------------------------|
  | 38 | filedate             | bigint       | Type inferred from '20200121'                                           |
  | 39 | filename             | string       | Type inferred from '/home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_' |
  | 40 | hash_id              | string       | Type inferred from 'null'                                               |
  | 41 | sourceid             | string       | Type inferred from 'U2000RAN'                                           |
  | 42 | registry_state       | string       | Type inferred from 'null'                                               |
  | 43 | datasetname          | string       | Type inferred from 'tx_u2000ran_board'                                  |
  | 44 | timestamp            | bigint       | Type inferred from '20200124'                                           |
  | 45 | transaction_status   | string       | Type inferred from 'null'                                               |


- **Particiones**

  A continuación se presentan las particiones creadas de la tabla **tx_u2000ran_board**.

  Sentencia: ```show partitions rci_network_db.tx_u2000ran_board```

  | year | month | #Rows   | #Files | Size     | Format | Incremental stats | Location                                                                                     |
  |------|-------|---------|--------|----------|--------|-------------------|----------------------------------------------------------------------------------------------|
  | 2019 | 11    | 501914  | 5      | 265.04MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/board/year=2019/month=11 |
  | 2020 | 1     | 1002619 | 10     | 528.15MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/board/year=2020/month=1  |

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_u2000ran_board';
  ```

  | id_execution | table_name        | dateload | avro_name                                                                                 | start_execution  | end_execution    | status |
  |--------------|-------------------|----------|-------------------------------------------------------------------------------------------|------------------|------------------|--------|
  | 1            | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20191125_Inventory_Board_20191125_161826.avro | 24/01/2020 16:17 | 24/01/2020 16:18 | 1      |
  | 2            | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20191125_Inventory_Board_20191125_162140.avro | 24/01/2020 16:19 | 24/01/2020 16:20 | 1      |
  | 3            | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20191125_Inventory_Board_20191125_162229.avro | 24/01/2020 16:20 | 24/01/2020 16:22 | 1      |
  | 4            | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20191125_Inventory_Board_20191125_162416.avro | 24/01/2020 16:22 | 24/01/2020 16:24 | 1      |
  | 5            | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20191125_Inventory_Board_20191125_162421.avro | 24/01/2020 16:24 | 24/01/2020 16:26 | 1      |
  | 6            | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20200114_Inventory_Board_20200114_112005.avro | 24/01/2020 16:26 | 24/01/2020 16:27 | 1      |
  | 7            | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20200114_Inventory_Board_20200114_112230.avro | 24/01/2020 16:28 | 24/01/2020 16:29 | 1      |
  | 8            | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20200114_Inventory_Board_20200114_112306.avro | 24/01/2020 16:29 | 24/01/2020 16:31 | 1      |
  | 9            | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20200114_Inventory_Board_20200114_112327.avro | 24/01/2020 16:31 | 24/01/2020 16:33 | 1      |
  | 10           | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20200114_Inventory_Board_20200114_112358.avro | 24/01/2020 16:33 | 24/01/2020 16:35 | 1      |
  | 11           | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20200121_Inventory_Board_20200121_110442.avro | 24/01/2020 16:35 | 24/01/2020 16:37 | 1      |
  | 12           | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20200121_Inventory_Board_20200121_110720.avro | 24/01/2020 16:37 | 24/01/2020 16:39 | 1      |
  | 13           | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20200121_Inventory_Board_20200121_110745.avro | 24/01/2020 16:39 | 24/01/2020 16:41 | 1      |
  | 14           | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20200121_Inventory_Board_20200121_110751.avro | 24/01/2020 16:41 | 24/01/2020 16:43 | 1      |
  | 15           | tx_u2000ran_board | 20200124 | /data/RCI/raw/gestores/u2000/ran/board/data/20200121_Inventory_Board_20200121_110801.avro | 24/01/2020 16:43 | 24/01/2020 16:45 | 1      |

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_u2000ran_board'
  and dateload = 20200124
  order by filedate asc;
  ```      
  | uuid                                 | rowprocessed | datasetname       | filedate | filename                                                                                                        | sourceid | dateload | read_count | insert_count | update_count | delete_count |   |
  |--------------------------------------|--------------|-------------------|----------|-----------------------------------------------------------------------------------------------------------------|----------|----------|------------|--------------|--------------|--------------|---|
  | 1d65eeca-9fa2-4076-aa4d-bc669115b4a2 | 139078       | tx_u2000ran_board | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/23/20200121_Inventory_Board_20200121_110745.csv  | U2000RAN | 20200124 | 139078     | 139078       | 0            | 0            |   |
  | 1a1e7353-c076-4a93-92f5-10698abb28a0 | 46178        | tx_u2000ran_board | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/197/20191125_Inventory_Board_20191125_162140.csv | U2000RAN | 20200124 | 46178      | 46178        | 0            | 0            |   |
  | 25714a00-a51f-4998-a0d4-33c70d48ea8b | 131778       | tx_u2000ran_board | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/7/20200114_Inventory_Board_20200114_112358.csv   | U2000RAN | 20200124 | 131778     | 131778       | 0            | 0            |   |
  | 34c53e10-2ba9-4a87-9c0c-b6fdfcd83958 | 138650       | tx_u2000ran_board | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/23/20191125_Inventory_Board_20191125_162229.csv  | U2000RAN | 20200124 | 138650     | 138650       | 0            | 0            |   |
  | 1d61fe08-8159-4940-956a-8d2d35910084 | 47918        | tx_u2000ran_board | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/54/20191125_Inventory_Board_20191125_161826.csv  | U2000RAN | 20200124 | 47918      | 47918        | 0            | 0            |   |
  | 8144879c-f585-4150-a073-dd7ee6bfb6df | 46318        | tx_u2000ran_board | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/197/20200114_Inventory_Board_20200114_112230.csv | U2000RAN | 20200124 | 46318      | 46318        | 0            | 0            |   |
  | 6d385144-c2bf-4441-a45d-50d1d7617764 | 132079       | tx_u2000ran_board | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/7/20191125_Inventory_Board_20191125_162416.csv   | U2000RAN | 20200124 | 132079     | 132079       | 0            | 0            |   |
  | 2751047c-8ec9-41f4-9204-8a7c3cdfb32e | 48537        | tx_u2000ran_board | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/54/20200121_Inventory_Board_20200121_110442.csv  | U2000RAN | 20200124 | 48537      | 48537        | 0            | 0            |   |
  | 02155e91-4d7e-4a4a-8abf-43999bf7f967 | 46375        | tx_u2000ran_board | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/197/20200121_Inventory_Board_20200121_110720.csv | U2000RAN | 20200124 | 46375      | 46375        | 0            | 0            |   |
  | dbb08969-2d7e-4ccf-9b95-af45d66d869a | 148497       | tx_u2000ran_board | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/39/20200114_Inventory_Board_20200114_112306.csv  | U2000RAN | 20200124 | 148497     | 148497       | 0            | 0            |   |
  | 01c044be-8bef-44ee-900c-8e692a59c44e | 138709       | tx_u2000ran_board | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/23/20200114_Inventory_Board_20200114_112327.csv  | U2000RAN | 20200124 | 138709     | 138709       | 0            | 0            |   |
  | 1f90287e-cb64-4817-ae34-cad81cdf37de | 149660       | tx_u2000ran_board | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/39/20191125_Inventory_Board_20191125_162421.csv  | U2000RAN | 20200124 | 149660     | 149660       | 0            | 0            |   |
  | 749a1ffd-0d9c-45e6-b45d-e1cc83b6bf9f | 148529       | tx_u2000ran_board | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/39/20200121_Inventory_Board_20200121_110801.csv  | U2000RAN | 20200124 | 148529     | 148529       | 0            | 0            |   |
  | a09fd778-8de8-4a27-bd21-b138927bd284 | 48502        | tx_u2000ran_board | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/54/20200114_Inventory_Board_20200114_112005.csv  | U2000RAN | 20200124 | 48502      | 48502        | 0            | 0            |   |
  | 937448ed-51b6-4804-9bc8-c81e60a40b94 | 131661       | tx_u2000ran_board | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/7/20200121_Inventory_Board_20200121_110751.csv   | U2000RAN | 20200124 | 131661     | 131661       | 0            | 0            |   |

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 133   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 133
```


## <a name="Cabinet"></a>Cabinet

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Cabinet](../../../../RCI_DataAnalysis/eda/RAN/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/RAN/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_u2000ran_cabinet```

  | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
  |----|----------------------|--------------|-------------------------------------------------------------------------|
  | 1  | netype               | string       | Type inferred from 'NodeB'                                              |
  | 2  | nefdn                | string       | Type inferred from 'NE=5274'                                            |
  | 3  | nename               | string       | Type inferred from 'HMEX0729'                                           |
  | 4  | bomracktype          | string       | Type inferred from 'WD2B30OPC'                                          |
  | 5  | dateoflastservice    | string       | Type inferred from 'null'                                               |
  | 6  | dateofmanufacture    | string       | Type inferred from '2011-03-31'                                         |
  | 7  | extinfo              | string       | Type inferred from 'Heat Dissipation Parts.Panasonic'                   |
  | 8  | inventoryunitid      | string       | Type inferred from '0'                                                  |
  | 9  | inventoryunittype    | string       | Type inferred from 'Hardware'                                           |
  | 10 | revissuenumber       | bigint       | Type inferred from '0'                                                  |
  | 11 | pnbomcodeitem        | bigint       | Type inferred from '1071089'                                            |
  | 12 | manufacturerdata     | string       | Type inferred from 'APM30H,WD2B30OPC,110VAC Dual-line,Bottom Cabling,6' |
  | 13 | model                | string       | Type inferred from 'null'                                               |
  | 14 | cabinetno            | string       | Type inferred from '0'                                                  |
  | 15 | racktype             | string       | Type inferred from 'APM30'                                              |
  | 16 | snbarcode            | string       | Type inferred from '21010710896TB3000917'                               |
  | 17 | sharemode            | string       | Type inferred from 'null'                                               |
  | 18 | unitposition         | string       | Type inferred from 'RackNo=0'                                           |
  | 19 | userlabel            | string       | Type inferred from 'null'                                               |
  | 20 | vendorname           | string       | Type inferred from 'Huawei'                                             |
  | 21 | vendorunitfamilytype | string       | Type inferred from 'Rack'                                               |
  | 22 | vendorunittypenumber | string       | Type inferred from '0'                                                  |
  | 23 | hardwareversion      | string       | Type inferred from 'null'                                               |

     Las siguientes columnas son creadas para la identidad de la fuente:

  | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
  |----|----------------------|--------------|-------------------------------------------------------------------------|
  | 24 | filedate             | bigint       | Type inferred from '20200121'                                           |
  | 25 | filename             | string       | Type inferred from '/home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_' |
  | 26 | hash_id              | string       | Type inferred from 'null'                                               |
  | 27 | sourceid             | string       | Type inferred from 'U2000RAN'                                           |
  | 28 | registry_state       | string       | Type inferred from 'null'                                               |
  | 29 | datasetname          | string       | Type inferred from 'tx_u2000ran_cabinet'                                |
  | 30 | timestamp            | bigint       | Type inferred from '20200125'                                           |
  | 31 | transaction_status   | string       | Type inferred from 'null'                                               |   


- **Particiones**

  A continuación se presentan las particiones creadas de la tabla **tx_u2000ran_cabinet**.

  Sentencia: ```show partitions rci_network_db.tx_u2000ran_cabinet```

  | year | month | #Rows | #Files | Size    | Format | Incremental stats | Location                                                                                       |
  |------|-------|-------|--------|---------|--------|-------------------|------------------------------------------------------------------------------------------------|
  | 2019 | 11    | 24439 | 5      | 10.24MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/cabinet/year=2019/month=11 |
  | 2020 | 1     | 48234 | 10     | 20.19MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/cabinet/year=2020/month=1  |

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_u2000ran_cabinet';
  ```

  | id_execution | table_name          | dateload | avro_name                                                                                     | start_execution  | end_execution    | status |
  |--------------|---------------------|----------|-----------------------------------------------------------------------------------------------|------------------|------------------|--------|
  | 1            | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20191125_Inventory_Cabinet_20191125_161826.avro | 24/01/2020 23:10 | 24/01/2020 23:11 | 1      |
  | 2            | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20191125_Inventory_Cabinet_20191125_162140.avro | 24/01/2020 23:12 | 24/01/2020 23:13 | 1      |
  | 3            | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20191125_Inventory_Cabinet_20191125_162229.avro | 24/01/2020 23:13 | 24/01/2020 23:14 | 1      |
  | 4            | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20191125_Inventory_Cabinet_20191125_162416.avro | 24/01/2020 23:14 | 24/01/2020 23:15 | 1      |
  | 5            | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20191125_Inventory_Cabinet_20191125_162421.avro | 24/01/2020 23:15 | 24/01/2020 23:16 | 1      |
  | 6            | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20200114_Inventory_Cabinet_20200114_112005.avro | 24/01/2020 23:17 | 24/01/2020 23:18 | 1      |
  | 7            | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20200114_Inventory_Cabinet_20200114_112230.avro | 24/01/2020 23:18 | 24/01/2020 23:19 | 1      |
  | 8            | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20200114_Inventory_Cabinet_20200114_112306.avro | 24/01/2020 23:19 | 24/01/2020 23:20 | 1      |
  | 9            | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20200114_Inventory_Cabinet_20200114_112327.avro | 24/01/2020 23:21 | 24/01/2020 23:22 | 1      |
  | 10           | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20200114_Inventory_Cabinet_20200114_112358.avro | 24/01/2020 23:22 | 24/01/2020 23:24 | 1      |
  | 11           | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20200121_Inventory_Cabinet_20200121_110442.avro | 24/01/2020 23:25 | 24/01/2020 23:26 | 1      |
  | 12           | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20200121_Inventory_Cabinet_20200121_110720.avro | 24/01/2020 23:26 | 24/01/2020 23:27 | 1      |
  | 13           | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20200121_Inventory_Cabinet_20200121_110745.avro | 24/01/2020 23:28 | 24/01/2020 23:29 | 1      |
  | 14           | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20200121_Inventory_Cabinet_20200121_110751.avro | 24/01/2020 23:30 | 24/01/2020 23:31 | 1      |
  | 15           | tx_u2000ran_cabinet | 20200124 | /data/RCI/raw/gestores/u2000/ran/cabinet/data/20200121_Inventory_Cabinet_20200121_110801.avro | 24/01/2020 23:31 | 24/01/2020 23:32 | 1      |

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_u2000ran_cabinet'
  and dateload = 20200125
  order by filedate asc;
  ```

  | uuid                                 | rowprocessed | datasetname         | filedate | filename                                                                                                          | sourceid | dateload | read_count | insert_count | update_count | delete_count |   |
  |--------------------------------------|--------------|---------------------|----------|-------------------------------------------------------------------------------------------------------------------|----------|----------|------------|--------------|--------------|--------------|---|
  | 65aa0d1d-18c0-41a0-81b0-912c9aa16dc1 | 6346         | tx_u2000ran_cabinet | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/7/20200114_Inventory_Cabinet_20200114_112358.csv   | U2000RAN | 20200125 | 6346       | 6346         | 0            | 0            |   |
  | 367efd66-deef-4113-be42-b19ea75b6848 | 7006         | tx_u2000ran_cabinet | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/39/20191125_Inventory_Cabinet_20191125_162421.csv  | U2000RAN | 20200125 | 7006       | 7006         | 0            | 0            |   |
  | c9243c39-a36e-4613-9087-869c1150a924 | 2511         | tx_u2000ran_cabinet | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/54/20191125_Inventory_Cabinet_20191125_161826.csv  | U2000RAN | 20200125 | 2511       | 2511         | 0            | 0            |   |
  | 425ecbd5-f338-4e5f-8b43-f40ed0731b73 | 7839         | tx_u2000ran_cabinet | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/23/20200121_Inventory_Cabinet_20200121_110745.csv  | U2000RAN | 20200125 | 7839       | 7839         | 0            | 0            |   |
  | ded4b5b2-f3c7-402f-b947-82b5597ba39c | 2254         | tx_u2000ran_cabinet | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/197/20191125_Inventory_Cabinet_20191125_162140.csv | U2000RAN | 20200125 | 2254       | 2254         | 0            | 0            |   |
  | acc3c0d1-571b-44b2-b8da-c3540b15fc52 | 6896         | tx_u2000ran_cabinet | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/39/20200121_Inventory_Cabinet_20200121_110801.csv  | U2000RAN | 20200125 | 6896       | 6896         | 0            | 0            |   |
  | 97d8e351-0701-4356-bcbb-8611d580d643 | 2265         | tx_u2000ran_cabinet | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/197/20200114_Inventory_Cabinet_20200114_112230.csv | U2000RAN | 20200125 | 2265       | 2265         | 0            | 0            |   |
  | 46dbbdf6-f8a7-4cf5-8e48-24c2404a94a6 | 8124         | tx_u2000ran_cabinet | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/23/20191125_Inventory_Cabinet_20191125_162229.csv  | U2000RAN | 20200125 | 8124       | 8124         | 0            | 0            |   |
  | 012a1b0a-5121-49e5-8cf7-4710cff47674 | 2545         | tx_u2000ran_cabinet | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/54/20200114_Inventory_Cabinet_20200114_112005.csv  | U2000RAN | 20200125 | 2545       | 2545         | 0            | 0            |   |
  | d75f2a3a-62d3-41ef-8da9-f9213b1bd448 | 6898         | tx_u2000ran_cabinet | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/39/20200114_Inventory_Cabinet_20200114_112306.csv  | U2000RAN | 20200125 | 6898       | 6898         | 0            | 0            |   |
  | 20afb7e1-a7a6-4d62-bafa-fea03efde3d7 | 6364         | tx_u2000ran_cabinet | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/7/20191125_Inventory_Cabinet_20191125_162416.csv   | U2000RAN | 20200125 | 6364       | 6364         | 0            | 0            |   |
  | 82c7b438-cc44-406e-9fd6-4db1036a64fc | 2269         | tx_u2000ran_cabinet | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/197/20200121_Inventory_Cabinet_20200121_110720.csv | U2000RAN | 20200125 | 2269       | 2269         | 0            | 0            |   |
  | cb3d0466-0145-4b9e-afa5-a8ddb7d749cd | 6347         | tx_u2000ran_cabinet | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/7/20200121_Inventory_Cabinet_20200121_110751.csv   | U2000RAN | 20200125 | 6347       | 6347         | 0            | 0            |   |
  | 885a920f-aed6-4c89-a866-ee25ef0e007c | 7832         | tx_u2000ran_cabinet | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/23/20200114_Inventory_Cabinet_20200114_112327.csv  | U2000RAN | 20200125 | 7832       | 7832         | 0            | 0            |   |
  | f955d274-386c-4861-8ccf-76ded03fe165 | 2550         | tx_u2000ran_cabinet | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/54/20200121_Inventory_Cabinet_20200121_110442.csv  |

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

      | Parámetro | Valor | Descripción|
      | ---------- | ---------- | ---------- |
      | parametro_01   | 134   | Valor de correspondiente al flujo|

       Sentencia kite:

      ```
      ./rci_ingesta_generacion_avro.sh {parametro_01}
      ```
      Ejemplo:

      ```
      ./rci_ingesta_generacion_avro.sh 134
      ```

## <a name="HostVer"></a>HostVer

  Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
  - **Descripción**
    [HostVer](../../../../RCI_DataAnalysis/eda/RAN/README.md)

  - **Diccionario de Datos**
       [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/RAN/README.md)

       Sentencia: ```describe formatted rci_network_db.tx_u2000ran_hostver```

       | Id | Nombre de la Columna | Tipo de Dato | Comentario                                          |
       |----|----------------------|--------------|-----------------------------------------------------|
       | 1  | netype               | string       | Type inferred from 'NodeB'                          |
       | 2  | nefdn                | string       | Type inferred from 'NE=5274'                        |
       | 3  | nename               | string       | Type inferred from 'HMEX0729'                       |
       | 4  | hostver              | string       | Type inferred from 'BTS3900_5900 V100R013C10SPC180' |
       | 5  | hostvernetype        | string       | Type inferred from 'null'                           |
       | 6  | hostvertype          | string       | Type inferred from 'BACKVER'                        |
       | 7  | sdesc                | string       | Type inferred from 'BACK SOFTWARE VERSION'          |

       Las siguientes columnas son creadas para la identidad de la fuente:

       | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
       |----|----------------------|--------------|-------------------------------------------------------------------------|
       | 8  | filedate             | bigint       | Type inferred from '20200121'                                           |
       | 9  | filename             | string       | Type inferred from '/home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_' |
       | 10 | hash_id              | string       | Type inferred from 'null'                                               |
       | 11 | sourceid             | string       | Type inferred from 'U2000RAN'                                           |
       | 12 | registry_state       | string       | Type inferred from 'null'                                               |
       | 13 | datasetname          | string       | Type inferred from 'tx_u2000ran_hostver'                                |
       | 14 | timestamp            | bigint       | Type inferred from '20200125'                                           |
       | 15 | transaction_status   | string       | Type inferred from 'null'                                               |

  - **Particiones**

    A continuación se presentan las particiones creadas de la tabla **tx_u2000ran_hostver**.

    Sentencia: ```show partitions rci_network_db.tx_u2000ran_hostver```

    | year | month | #Rows | #Files | Size    | Format | Incremental stats | Location                                                                                       |
    |------|-------|-------|--------|---------|--------|-------------------|------------------------------------------------------------------------------------------------|
    | 2019 | 11    | 47648 | 5      | 15.26MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/hostver/year=2019/month=11 |
    | 2020 | 1     | 91791 | 10     | 29.29MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/hostver/year=2020/month=1  |

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_u2000ran_hostver';
  ```

  | id_execution | table_name          | dateload | avro_name                                                                                     | start_execution  | end_execution    | status |
  |--------------|---------------------|----------|-----------------------------------------------------------------------------------------------|------------------|------------------|--------|
  | 1            | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20191125_Inventory_HostVer_20191125_161826.avro | 24/01/2020 23:42 | 24/01/2020 23:43 | 1      |
  | 2            | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20191125_Inventory_HostVer_20191125_162140.avro | 24/01/2020 23:44 | 24/01/2020 23:44 | 1      |
  | 3            | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20191125_Inventory_HostVer_20191125_162229.avro | 24/01/2020 23:45 | 24/01/2020 23:46 | 1      |
  | 4            | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20191125_Inventory_HostVer_20191125_162416.avro | 24/01/2020 23:46 | 24/01/2020 23:47 | 1      |
  | 5            | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20191125_Inventory_HostVer_20191125_162421.avro | 24/01/2020 23:47 | 24/01/2020 23:48 | 1      |
  | 6            | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20200114_Inventory_HostVer_20200114_112005.avro | 24/01/2020 23:49 | 24/01/2020 23:50 | 1      |
  | 7            | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20200114_Inventory_HostVer_20200114_112230.avro | 24/01/2020 23:50 | 24/01/2020 23:51 | 1      |
  | 8            | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20200114_Inventory_HostVer_20200114_112306.avro | 24/01/2020 23:51 | 24/01/2020 23:52 | 1      |
  | 9            | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20200114_Inventory_HostVer_20200114_112327.avro | 24/01/2020 23:52 | 24/01/2020 23:54 | 1      |
  | 10           | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20200114_Inventory_HostVer_20200114_112358.avro | 24/01/2020 23:54 | 24/01/2020 23:55 | 1      |
  | 11           | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20200121_Inventory_HostVer_20200121_110442.avro | 24/01/2020 23:55 | 24/01/2020 23:56 | 1      |
  | 12           | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20200121_Inventory_HostVer_20200121_110720.avro | 24/01/2020 23:57 | 24/01/2020 23:57 | 1      |
  | 13           | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20200121_Inventory_HostVer_20200121_110745.avro | 24/01/2020 23:58 | 24/01/2020 23:59 | 1      |
  | 14           | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20200121_Inventory_HostVer_20200121_110751.avro | 24/01/2020 23:59 | 25/01/2020 00:00 | 1      |
  | 15           | tx_u2000ran_hostver | 20200124 | /data/RCI/raw/gestores/u2000/ran/hostver/data/20200121_Inventory_HostVer_20200121_110801.avro | 25/01/2020 00:01 | 25/01/2020 00:02 | 1      |

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_u2000ran_hostver'
  and dateload = 20200125
  order by filedate asc;
  ```
  | uuid                                 | rowprocessed | datasetname         | filedate | filename                                                                                                          | sourceid | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|---------------------|----------|-------------------------------------------------------------------------------------------------------------------|----------|----------|------------|--------------|--------------|--------------|
  | 228ff629-6a3a-4077-9334-58cdc286f618 | 22067        | tx_u2000ran_hostver | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/39/20191125_Inventory_HostVer_20191125_162421.csv  | U2000RAN | 20200125 | 22067      | 22067        | 0            | 0            |
  | d2df5970-5db6-4e28-b74f-4c4adf84957b | 18604        | tx_u2000ran_hostver | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/7/20191125_Inventory_HostVer_20191125_162416.csv   | U2000RAN | 20200125 | 18604      | 18604        | 0            | 0            |
  | 3d7a30c9-97b9-4efb-9544-faa4136b166d | 6411         | tx_u2000ran_hostver | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/197/20191125_Inventory_HostVer_20191125_162140.csv | U2000RAN | 20200125 | 6411       | 6411         | 0            | 0            |
  | 2810df24-a59e-4beb-b34a-c79d02e85ffc | 21462        | tx_u2000ran_hostver | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/39/20200121_Inventory_HostVer_20200121_110801.csv  | U2000RAN | 20200125 | 21462      | 21462        | 0            | 0            |
  | 3b48395d-f64b-4130-9132-f6ef62bf3e0b | 25706        | tx_u2000ran_hostver | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/23/20200114_Inventory_HostVer_20200114_112327.csv  | U2000RAN | 20200125 | 25706      | 25706        | 0            | 0            |
  | 78ab4bb7-8fe1-4fa4-adca-0903b2269151 | 18459        | tx_u2000ran_hostver | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/7/20200114_Inventory_HostVer_20200114_112358.csv   | U2000RAN | 20200125 | 18459      | 18459        | 0            | 0            |
  | f1c44823-b97d-4542-8886-48bbe33f732f | 18444        | tx_u2000ran_hostver | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/7/20200121_Inventory_HostVer_20200121_110751.csv   | U2000RAN | 20200125 | 18444      | 18444        | 0            | 0            |
  | 0428bbd8-b05e-44df-9c91-49b65cb94368 | 6711         | tx_u2000ran_hostver | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/54/20191125_Inventory_HostVer_20191125_161826.csv  | U2000RAN | 20200125 | 6711       | 6711         | 0            | 0            |
  | 8c40893e-3513-4d77-ad9a-ebd8221cf6bb | 6441         | tx_u2000ran_hostver | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/197/20200121_Inventory_HostVer_20200121_110720.csv | U2000RAN | 20200125 | 6441       | 6441         | 0            | 0            |
  | 7ce8f3d4-674a-41b3-8470-a04be62ad0a2 | 6432         | tx_u2000ran_hostver | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/197/20200114_Inventory_HostVer_20200114_112230.csv | U2000RAN | 20200125 | 6432       | 6432         | 0            | 0            |
  | 417189c8-6553-4810-b1cf-78bb081c2f87 | 25653        | tx_u2000ran_hostver | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/23/20200121_Inventory_HostVer_20200121_110745.csv  | U2000RAN | 20200125 | 25653      | 25653        | 0            | 0            |
  | 4993b4a7-e394-473a-b8b4-975a5081ef19 | 6771         | tx_u2000ran_hostver | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/54/20200121_Inventory_HostVer_20200121_110442.csv  | U2000RAN | 20200125 | 6771       | 6771         | 0            | 0            |
  | 5dccfcb2-27d9-4013-986a-daafa42e4852 | 6762         | tx_u2000ran_hostver | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/54/20200114_Inventory_HostVer_20200114_112005.csv  | U2000RAN | 20200125 | 6762       | 6762         | 0            | 0            |
  | 97884dc4-4a7d-4679-8e7f-67a0ae957a4d | 21507        | tx_u2000ran_hostver | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/39/20200114_Inventory_HostVer_20200114_112306.csv  | U2000RAN | 20200125 | 21507      | 21507        | 0            | 0            |
  | f577b790-6c04-4638-adb0-cf89f8d9cbb8 | 27620        | tx_u2000ran_hostver | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/23/20191125_Inventory_HostVer_20191125_162229.csv  |

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

       | Parámetro | Valor | Descripción|
       | ---------- | ---------- | ---------- |
       | parametro_01   | 135   | Valor de correspondiente al flujo|

      Sentencia kite:

       ```
       ./rci_ingesta_generacion_avro.sh {parametro_01}
       ```
       Ejemplo:

       ```
       ./rci_ingesta_generacion_avro.sh 135
       ```

## <a name="Slot"></a>Slot

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Slot](../../../../RCI_DataAnalysis/eda/RAN/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/RAN/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_u2000ran_slot```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                 |
     |----|----------------------|--------------|------------------------------------------------------------|
     | 1  | netype               | string       | Type inferred from 'NodeB'                                 |
     | 2  | nefdn                | string       | Type inferred from 'NE=5274'                               |
     | 3  | nename               | string       | Type inferred from 'HMEX0729'                              |
     | 4  | dateoflastservice    | string       | Type inferred from 'null'                                  |
     | 5  | dateofmanufacture    | string       | Type inferred from 'null'                                  |
     | 6  | subrackno            | string       | Type inferred from '0'                                     |
     | 7  | inventoryunitid      | string       | Type inferred from '0'                                     |
     | 8  | inventoryunittype    | string       | Type inferred from 'Hardware'                              |
     | 9  | manufacturerdata     | string       | Type inferred from 'null'                                  |
     | 10 | cabinetno            | string       | Type inferred from '0'                                     |
     | 11 | snbarcode            | string       | Type inferred from 'null'                                  |
     | 12 | sharemode            | string       | Type inferred from 'null'                                  |
     | 13 | slotno               | string       | Type inferred from '0'                                     |
     | 14 | slotpos              | string       | Type inferred from '0'                                     |
     | 15 | unitposition         | string       | Type inferred from 'RackNo=0,FrameNo=0,SlotNo=0,SlotPos=0' |
     | 16 | vendorname           | string       | Type inferred from 'Huawei'                                |
     | 17 | vendorunitfamilytype | string       | Type inferred from 'Slot'                                  |
     | 18 | vendorunittypenumber | string       | Type inferred from '0'                                     |
     | 19 | hardwareversion      | string       | Type inferred from 'null'                                  |

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 20 | filedate             | bigint       | Type inferred from '20200121'                                           |
     | 21 | filename             | string       | Type inferred from '/home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_' |
     | 22 | hash_id              | string       | Type inferred from 'null'                                               |
     | 23 | sourceid             | string       | Type inferred from 'U2000RAN'                                           |
     | 24 | registry_state       | string       | Type inferred from 'null'                                               |
     | 25 | datasetname          | string       | Type inferred from 'tx_u2000ran_slot'                                   |
     | 26 | timestamp            | bigint       | Type inferred from '20200125'                                           |
     | 27 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_u2000ran_slot**.

 Sentencia: ```show partitions rci_network_db.tx_u2000ran_slot```

  | year | month | #Rows | #Files | Size   | Format | Incremental stats | Location                                                                                    |
  |------|-------|-------|--------|--------|--------|-------------------|---------------------------------------------------------------------------------------------|
  | 2019 | 11    | 10261 | 5      | 3.53MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/slot/year=2019/month=11 |
  | 2020 | 1     | 19303 | 10     | 6.61MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/slot/year=2020/month=1  |

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_u2000ran_slot';
   ```

  | id_execution | table_name       | dateload | avro_name                                                                               | start_execution  | end_execution    | status |
  |--------------|------------------|----------|-----------------------------------------------------------------------------------------|------------------|------------------|--------|
  | 1            | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20191125_Inventory_Slot_20191125_161826.avro | 25/01/2020 01:45 | 25/01/2020 01:46 | 1      |
  | 2            | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20191125_Inventory_Slot_20191125_162140.avro | 25/01/2020 01:46 | 25/01/2020 01:47 | 1      |
  | 3            | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20191125_Inventory_Slot_20191125_162229.avro | 25/01/2020 01:47 | 25/01/2020 01:48 | 1      |
  | 4            | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20191125_Inventory_Slot_20191125_162416.avro | 25/01/2020 01:49 | 25/01/2020 01:50 | 1      |
  | 5            | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20191125_Inventory_Slot_20191125_162421.avro | 25/01/2020 01:50 | 25/01/2020 01:51 | 1      |
  | 6            | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20200114_Inventory_Slot_20200114_112005.avro | 25/01/2020 01:52 | 25/01/2020 01:53 | 1      |
  | 7            | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20200114_Inventory_Slot_20200114_112230.avro | 25/01/2020 01:53 | 25/01/2020 01:54 | 1      |
  | 8            | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20200114_Inventory_Slot_20200114_112306.avro | 25/01/2020 01:54 | 25/01/2020 01:56 | 1      |
  | 9            | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20200114_Inventory_Slot_20200114_112327.avro | 25/01/2020 01:56 | 25/01/2020 01:57 | 1      |
  | 10           | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20200114_Inventory_Slot_20200114_112358.avro | 25/01/2020 01:57 | 25/01/2020 01:59 | 1      |
  | 11           | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20200121_Inventory_Slot_20200121_110442.avro | 25/01/2020 01:59 | 25/01/2020 02:00 | 1      |
  | 12           | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20200121_Inventory_Slot_20200121_110720.avro | 25/01/2020 02:00 | 25/01/2020 02:01 | 1      |
  | 13           | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20200121_Inventory_Slot_20200121_110745.avro | 25/01/2020 02:02 | 25/01/2020 02:03 | 1      |
  | 14           | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20200121_Inventory_Slot_20200121_110751.avro | 25/01/2020 02:03 | 25/01/2020 02:04 | 1      |
  | 15           | tx_u2000ran_slot | 20200125 | /data/RCI/raw/gestores/u2000/ran/slot/data/20200121_Inventory_Slot_20200121_110801.avro | 25/01/2020 02:05 | 25/01/2020 02:06 | 1      |

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_u2000ran_slot'
   and dateload = 20200125
   order by filedate asc;
   ```

  | uuid                                 | rowprocessed | datasetname      | filedate | filename                                                                                                   | sourceid | dateload | read_count | insert_count | update_count | delete_count |   |
  |--------------------------------------|--------------|------------------|----------|------------------------------------------------------------------------------------------------------------|----------|----------|------------|--------------|--------------|--------------|---|
  | 39fde53d-dce7-4ba0-b325-ad9e4bebb918 | 127777       | tx_u2000ran_slot | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/20191125_Inventory_Slot_20191125_162421.csv | U2000RAN | 20200125 | 127777     | 127777       | 0            | 0            |   |
  | ba001047-eaf2-4998-a481-1857112ffc2f | 116487       | tx_u2000ran_slot | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/20191125_Inventory_Slot_20191125_162416.csv | U2000RAN | 20200125 | 116487     | 116487       | 0            | 0            |   |
  | aad81eb4-b864-4e71-ab7e-974bfefc72af | 134681       | tx_u2000ran_slot | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/20200121_Inventory_Slot_20200121_110745.csv | U2000RAN | 20200125 | 134681     | 134681       | 0            | 0            |   |
  | 86aeda99-e4b5-4478-8435-6cf594ecfef7 | 116127       | tx_u2000ran_slot | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/20200121_Inventory_Slot_20200121_110751.csv | U2000RAN | 20200125 | 116127     | 116127       | 0            | 0            |   |
  | 41463e4b-882f-4b81-a386-7a5b4f066c37 | 116224       | tx_u2000ran_slot | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/20200114_Inventory_Slot_20200114_112358.csv | U2000RAN | 20200125 | 116224     | 116224       | 0            | 0            |   |
  | 596454ab-84b3-46fe-9192-c5198acb4c4a | 126354       | tx_u2000ran_slot | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/20200121_Inventory_Slot_20200121_110801.csv | U2000RAN | 20200125 | 126354     | 126354       | 0            | 0            |   |
  | 733edd5a-59c2-471e-bb95-3a14585f4370 | 134473       | tx_u2000ran_slot | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/20200114_Inventory_Slot_20200114_112327.csv | U2000RAN | 20200125 | 134473     | 134473       | 0            | 0            |   |
  | 000ed913-e40d-44c7-9b0e-f67a82a646fd | 44852        | tx_u2000ran_slot | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/20200114_Inventory_Slot_20200114_112005.csv | U2000RAN | 20200125 | 44852      | 44852        | 0            | 0            |   |
  | 0c921544-6899-4c45-9b3d-54aadfc5c56f | 44244        | tx_u2000ran_slot | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/20191125_Inventory_Slot_20191125_161826.csv | U2000RAN | 20200125 | 44244      | 44244        | 0            | 0            |   |
  | 642c9aba-30cd-47e8-9173-7fb7b246c9b7 | 44914        | tx_u2000ran_slot | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/20200121_Inventory_Slot_20200121_110442.csv | U2000RAN | 20200125 | 44914      | 44914        | 0            | 0            |   |
  | 8d122849-8ef9-423e-a128-f5fe29146165 | 42429        | tx_u2000ran_slot | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/20200114_Inventory_Slot_20200114_112230.csv | U2000RAN | 20200125 | 42429      | 42429        | 0            | 0            |   |
  | 81ab75fe-3239-4495-ac94-dd068e5f2ea3 | 126372       | tx_u2000ran_slot | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/20200114_Inventory_Slot_20200114_112306.csv | U2000RAN | 20200125 | 126372     | 126372       | 0            | 0            |   |
  | 2bd17d4f-e552-4600-828a-5b5ccab69fc5 | 42263        | tx_u2000ran_slot | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/20191125_Inventory_Slot_20191125_162140.csv | U2000RAN | 20200125 | 42263      | 42263        | 0            | 0            |   |
  | ffa59b63-92c8-4453-b8e1-e50e42a8f723 | 137546       | tx_u2000ran_slot | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/20191125_Inventory_Slot_20191125_162229.csv | U2000RAN | 20200125 | 137546     | 137546       | 0            | 0            |   |
  | a0feeee3-2cec-4c3c-8180-ce15681e5569 | 42500        | tx_u2000ran_slot | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/20200121_Inventory_Slot_20200121_110720.csv | U2000RAN | 20200125 | 42500      | 42500        | 0            | 0            |   |

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 136   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 136
```


## <a name="Port"></a>Port

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Port](../../../../RCI_DataAnalysis/eda/RAN/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/RAN/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_u2000ran_port```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 1  | netype               | string       | Type inferred from 'NodeB'                                              |
     | 2  | nefdn                | string       | Type inferred from 'NE=5274'                                            |
     | 3  | nename               | string       | Type inferred from 'HMEX0729'                                           |
     | 4  | dateoflastservice    | string       | Type inferred from 'null'                                               |
     | 5  | dateofmanufacture    | string       | Type inferred from 'null'                                               |
     | 6  | subrackno            | string       | Type inferred from '60'                                                 |
     | 7  | inventoryunitid      | string       | Type inferred from '0'                                                  |
     | 8  | inventoryunittype    | string       | Type inferred from 'Hardware'                                           |
     | 9  | macaddr              | string       | Type inferred from '4C1F-CCE1-CB7A'                                     |
     | 10 | manufacturerdata     | string       | Type inferred from 'null'                                               |
     | 11 | portno               | string       | Type inferred from '0'                                                  |
     | 12 | cabinetno            | string       | Type inferred from '0'                                                  |
     | 13 | snbarcode            | string       | Type inferred from 'null'                                               |
     | 14 | sharemode            | string       | Type inferred from 'null'                                               |
     | 15 | slotno               | string       | Type inferred from '0'                                                  |
     | 16 | slotpos              | string       | Type inferred from '0'                                                  |
     | 17 | subslotno            | string       | Type inferred from '-1'                                                 |
     | 18 | unitposition         | string       | Type inferred from 'RackNo=0,FrameNo=60,SlotNo=0,SlotPos=0,SubSlotNo=-' |
     | 19 | vendorname           | string       | Type inferred from 'Huawei'                                             |
     | 20 | vendorunitfamilytype | string       | Type inferred from 'CPRIPort_SFP'                                       |
     | 21 | vendorunittypenumber | string       | Type inferred from '0'                                                  |
     | 22 | hardwareversion      | string       | Type inferred from 'null'                                               |

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 23 | filedate             | bigint       | Type inferred from '20200121'                                           |
     | 24 | filename             | string       | Type inferred from '/home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_' |
     | 25 | hash_id              | string       | Type inferred from 'null'                                               |
     | 26 | sourceid             | string       | Type inferred from 'U2000RAN'                                           |
     | 27 | registry_state       | string       | Type inferred from 'null'                                               |
     | 28 | datasetname          | string       | Type inferred from 'tx_u2000ran_port'                                   |
     | 29 | timestamp            | bigint       | Type inferred from '20200125'                                           |
     | 30 | transaction_status   | string       | Type inferred from 'null'                                               |


   - **Particiones**

     A continuación se presentan las particiones creadas de la tabla **tx_u2000ran_port**.

     Sentencia: ```show partitions rci_network_db.tx_u2000ran_port```

     | year | month | #Rows  | #Files | Size    | Format | Incremental stats | Location                                                                                    |
     |------|-------|--------|--------|---------|--------|-------------------|---------------------------------------------------------------------------------------------|
     | 2019 | 11    | 90973  | 5      | 34.83MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/port/year=2019/month=11 |
     | 2020 | 1     | 180873 | 10     | 69.01MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/port/year=2020/month=1  |

   - **Ejecuciones**

      En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

      ```
      select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_u2000ran_port';
      ```

      | id_execution | table_name       | dateload | avro_name                                                                               | start_execution  | end_execution    | status |
      |--------------|------------------|----------|-----------------------------------------------------------------------------------------|------------------|------------------|--------|
      | 1            | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20191125_Inventory_Port_20191125_161826.avro | 25/01/2020 02:17 | 25/01/2020 02:18 | 1      |
      | 2            | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20191125_Inventory_Port_20191125_162140.avro | 25/01/2020 02:19 | 25/01/2020 02:19 | 1      |
      | 3            | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20191125_Inventory_Port_20191125_162229.avro | 25/01/2020 02:20 | 25/01/2020 02:21 | 1      |
      | 4            | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20191125_Inventory_Port_20191125_162416.avro | 25/01/2020 02:21 | 25/01/2020 02:23 | 1      |
      | 5            | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20191125_Inventory_Port_20191125_162421.avro | 25/01/2020 02:23 | 25/01/2020 02:24 | 1      |
      | 6            | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20200114_Inventory_Port_20200114_112005.avro | 25/01/2020 02:24 | 25/01/2020 02:25 | 1      |
      | 7            | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20200114_Inventory_Port_20200114_112230.avro | 25/01/2020 02:26 | 25/01/2020 02:27 | 1      |
      | 8            | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20200114_Inventory_Port_20200114_112306.avro | 25/01/2020 02:27 | 25/01/2020 02:28 | 1      |
      | 9            | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20200114_Inventory_Port_20200114_112327.avro | 25/01/2020 02:29 | 25/01/2020 02:30 | 1      |
      | 10           | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20200114_Inventory_Port_20200114_112358.avro | 25/01/2020 02:30 | 25/01/2020 02:32 | 1      |
      | 11           | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20200121_Inventory_Port_20200121_110442.avro | 25/01/2020 02:32 | 25/01/2020 02:33 | 1      |
      | 12           | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20200121_Inventory_Port_20200121_110720.avro | 25/01/2020 02:33 | 25/01/2020 02:34 | 1      |
      | 13           | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20200121_Inventory_Port_20200121_110745.avro | 25/01/2020 02:35 | 25/01/2020 02:36 | 1      |
      | 14           | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20200121_Inventory_Port_20200121_110751.avro | 25/01/2020 02:36 | 25/01/2020 02:37 | 1      |
      | 15           | tx_u2000ran_port | 20200125 | /data/RCI/raw/gestores/u2000/ran/port/data/20200121_Inventory_Port_20200121_110801.avro | 25/01/2020 02:38 | 25/01/2020 02:39 | 1      |

   - **Cifras de Control**

      En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

      ```
      select * from rci_network_db.tx_cifras_control
      where datasetname = 'tx_u2000ran_port'
      and dateload = 20200125
      order by filedate asc;
      ```

  | uuid                                 | rowprocessed | datasetname      | filedate | filename                                                                                                       | sourceid | dateload | read_count | insert_count | update_count | delete_count |   |
  |--------------------------------------|--------------|------------------|----------|----------------------------------------------------------------------------------------------------------------|----------|----------|------------|--------------|--------------|--------------|---|
  | 0596ac83-a297-4ad2-82d6-04992fbb289c | 122514       | tx_u2000ran_port | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/7/20191125_Inventory_Port_20191125_162416.csv   | U2000RAN | 20200125 | 122514     | 122514       | 0            | 0            |   |
  | 2d4757cc-aa4c-4031-a80e-db7fa5182760 | 138476       | tx_u2000ran_port | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/23/20191125_Inventory_Port_20191125_162229.csv  | U2000RAN | 20200125 | 138476     | 138476       | 0            | 0            |   |
  | 263cbda0-4ab9-4435-85ea-772d33d87132 | 144431       | tx_u2000ran_port | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/39/20200121_Inventory_Port_20200121_110801.csv  | U2000RAN | 20200125 | 144431     | 144431       | 0            | 0            |   |
  | d7616c56-bda2-4aa5-a616-ade94dc0c966 | 146229       | tx_u2000ran_port | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/39/20191125_Inventory_Port_20191125_162421.csv  | U2000RAN | 20200125 | 146229     | 146229       | 0            | 0            |   |
  | cff656b0-a6a3-459d-9703-caa6df94ea8f | 42493        | tx_u2000ran_port | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/197/20191125_Inventory_Port_20191125_162140.csv | U2000RAN | 20200125 | 42493      | 42493        | 0            | 0            |   |
  | 22546434-ab6b-4e95-9205-fce2281cf107 | 137242       | tx_u2000ran_port | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/23/20200114_Inventory_Port_20200114_112327.csv  | U2000RAN | 20200125 | 137242     | 137242       | 0            | 0            |   |
  | 8cd6c2a0-8fd4-444b-9ef6-0ecd10b952e9 | 43389        | tx_u2000ran_port | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/54/20200114_Inventory_Port_20200114_112005.csv  | U2000RAN | 20200125 | 43389      | 43389        | 0            | 0            |   |
  | b23c66d6-22d4-46af-abaa-7a83c5184b9f | 42968        | tx_u2000ran_port | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/54/20191125_Inventory_Port_20191125_161826.csv  | U2000RAN | 20200125 | 42968      | 42968        | 0            | 0            |   |
  | 43b8210f-ae91-4444-8fb2-07f9dd1e6a80 | 144418       | tx_u2000ran_port | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/39/20200114_Inventory_Port_20200114_112306.csv  | U2000RAN | 20200125 | 144418     | 144418       | 0            | 0            |   |
  | ba478c9b-9c61-4698-be22-f212d7c4e581 | 137591       | tx_u2000ran_port | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/23/20200121_Inventory_Port_20200121_110745.csv  | U2000RAN | 20200125 | 137591     | 137591       | 0            | 0            |   |
  | 9223dbef-25fe-4382-a207-fc1c1fc0aed1 | 121822       | tx_u2000ran_port | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/7/20200121_Inventory_Port_20200121_110751.csv   | U2000RAN | 20200125 | 121822     | 121822       | 0            | 0            |   |
  | a5518194-1bcd-49b0-8fcf-ed2921856c34 | 42580        | tx_u2000ran_port | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/197/20200114_Inventory_Port_20200114_112230.csv | U2000RAN | 20200125 | 42580      | 42580        | 0            | 0            |   |
  | 4d906e17-1b07-4087-8006-d90d616d5261 | 43391        | tx_u2000ran_port | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/54/20200121_Inventory_Port_20200121_110442.csv  | U2000RAN | 20200125 | 43391      | 43391        | 0            | 0            |   |
  | 80454fa7-a4fc-483f-9378-fe84709eacff | 42629        | tx_u2000ran_port | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/197/20200121_Inventory_Port_20200121_110720.csv | U2000RAN | 20200125 | 42629      | 42629        | 0            | 0            |   |
  | 2d31fad0-39f1-43a0-bdd5-1b26851444ad | 122058       | tx_u2000ran_port | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/7/20200114_Inventory_Port_20200114_112358.csv   | U2000RAN | 20200125 | 122058     | 122058       | 0            | 0            |   |

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 137   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 137
```


## <a name="Subrack"></a>Subrack

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Subrack](../../../../RCI_DataAnalysis/eda/RAN/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/RAN/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_u2000ran_subrack```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                          |
     |----|----------------------|--------------|-----------------------------------------------------|
     | 1  | netype               | string       | Type inferred from 'NodeB'                          |
     | 2  | nefdn                | string       | Type inferred from 'NE=5274'                        |
     | 3  | nename               | string       | Type inferred from 'HMEX0729'                       |
     | 4  | bomframetype         | string       | Type inferred from 'WD2BBBUC'                       |
     | 5  | dateoflastservice    | string       | Type inferred from 'null'                           |
     | 6  | dateofmanufacture    | string       | Type inferred from '2011-06-12'                     |
     | 7  | extinfo              | string       | Type inferred from 'null'                           |
     | 8  | subrackno            | string       | Type inferred from '0'                              |
     | 9  | frametype            | string       | Type inferred from 'BBU3900'                        |
     | 10 | inventoryunitid      | string       | Type inferred from '0'                              |
     | 11 | inventoryunittype    | string       | Type inferred from 'Hardware'                       |
     | 12 | revissuenumber       | string       | Type inferred from '00'                             |
     | 13 | pnbomcodeitem        | string       | Type inferred from '02112722'                       |
     | 14 | manufacturerdata     | string       | Type inferred from 'HERT BBU,WD2BBBUC,HERT BBU Box' |
     | 15 | model                | string       | Type inferred from 'null'                           |
     | 16 | moduleno             | string       | Type inferred from '-1'                             |
     | 17 | rackframeno          | string       | Type inferred from '0'                              |
     | 18 | cabinetno            | string       | Type inferred from '0'                              |
     | 19 | snbarcode            | string       | Type inferred from '2102112722P0B6000161'           |
     | 20 | sharemode            | string       | Type inferred from 'null'                           |
     | 21 | unitposition         | string       | Type inferred from 'RackNo=0,FrameNo=0'             |
     | 22 | userlabel            | string       | Type inferred from 'null'                           |
     | 23 | vendorname           | string       | Type inferred from 'Huawei'                         |
     | 24 | vendorunitfamilytype | string       | Type inferred from 'Frame'                          |
     | 25 | vendorunittypenumber | string       | Type inferred from '0'                              |
     | 26 | hardwareversion      | string       | Type inferred from 'null'                           |

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 27 | filedate             | bigint       | Type inferred from '20200121'                                           |
     | 28 | filename             | string       | Type inferred from '/home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_' |
     | 29 | hash_id              | string       | Type inferred from 'null'                                               |
     | 30 | sourceid             | string       | Type inferred from 'U2000RAN'                                           |
     | 31 | registry_state       | string       | Type inferred from 'null'                                               |
     | 32 | datasetname          | string       | Type inferred from 'tx_u2000ran_subrack'                                |
     | 33 | timestamp            | bigint       | Type inferred from '20200125'                                           |
     | 34 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_u2000ran_subrack**.

 Sentencia: ```show partitions rci_network_db.tx_u2000ran_subrack```

  | year | month | #Rows  | #Files | Size    | Format | Incremental stats | Location                                                                                       |
  |------|-------|--------|--------|---------|--------|-------------------|------------------------------------------------------------------------------------------------|
  | 2019 | 11    | 109927 | 5      | 42.57MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/subrack/year=2019/month=11 |
  | 2020 | 1     | 217133 | 10     | 83.86MB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/u2000/ran/subrack/year=2020/month=1  |

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_u2000ran_subrack';
  ```

  | id_execution | table_name          | dateload | avro_name                                                                                     | start_execution  | end_execution    | status |
  |--------------|---------------------|----------|-----------------------------------------------------------------------------------------------|------------------|------------------|--------|
  | 1            | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20191125_Inventory_Subrack_20191125_161826.avro | 25/01/2020 02:51 | 25/01/2020 02:51 | 1      |
  | 2            | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20191125_Inventory_Subrack_20191125_162140.avro | 25/01/2020 02:52 | 25/01/2020 02:53 | 1      |
  | 3            | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20191125_Inventory_Subrack_20191125_162229.avro | 25/01/2020 02:53 | 25/01/2020 02:54 | 1      |
  | 4            | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20191125_Inventory_Subrack_20191125_162416.avro | 25/01/2020 02:54 | 25/01/2020 02:55 | 1      |
  | 5            | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20191125_Inventory_Subrack_20191125_162421.avro | 25/01/2020 02:56 | 25/01/2020 02:57 | 1      |
  | 6            | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20200114_Inventory_Subrack_20200114_112005.avro | 25/01/2020 02:57 | 25/01/2020 02:58 | 1      |
  | 7            | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20200114_Inventory_Subrack_20200114_112230.avro | 25/01/2020 02:59 | 25/01/2020 03:00 | 1      |
  | 8            | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20200114_Inventory_Subrack_20200114_112307.avro | 25/01/2020 03:00 | 25/01/2020 03:01 | 1      |
  | 9            | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20200114_Inventory_Subrack_20200114_112327.avro | 25/01/2020 03:01 | 25/01/2020 03:02 | 1      |
  | 10           | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20200114_Inventory_Subrack_20200114_112358.avro | 25/01/2020 03:03 | 25/01/2020 03:04 | 1      |
  | 11           | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20200121_Inventory_Subrack_20200121_110442.avro | 25/01/2020 03:04 | 25/01/2020 03:05 | 1      |
  | 12           | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20200121_Inventory_Subrack_20200121_110720.avro | 25/01/2020 03:05 | 25/01/2020 03:06 | 1      |
  | 13           | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20200121_Inventory_Subrack_20200121_110745.avro | 25/01/2020 03:07 | 25/01/2020 03:08 | 1      |
  | 14           | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20200121_Inventory_Subrack_20200121_110751.avro | 25/01/2020 03:08 | 25/01/2020 03:09 | 1      |
  | 15           | tx_u2000ran_subrack | 20200125 | /data/RCI/raw/gestores/u2000/ran/subrack/data/20200121_Inventory_Subrack_20200121_110801.avro | 25/01/2020 03:10 | 25/01/2020 03:11 | 1      |

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_u2000ran_subrack'
  and dateload = 20200125
  order by filedate asc;
  ```
  | uuid                                 | rowprocessed | datasetname         | filedate | filename                                                                                                          | sourceid | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|---------------------|----------|-------------------------------------------------------------------------------------------------------------------|----------|----------|------------|--------------|--------------|--------------|
  | 0ccb35d0-5e9e-45bc-9178-9f96ec62c798 | 35278        | tx_u2000ran_subrack | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/23/20191125_Inventory_Subrack_20191125_162229.csv  | U2000RAN | 20200125 | 35278      | 35278        | 0            | 0            |
  | ce369ba3-127a-402d-8efa-9f8454ea6df5 | 10716        | tx_u2000ran_subrack | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/197/20200121_Inventory_Subrack_20200121_110720.csv | U2000RAN | 20200125 | 10716      | 10716        | 0            | 0            |
  | 1a03ad30-1bdc-4185-a1fc-74887fcd6681 | 34505        | tx_u2000ran_subrack | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/23/20200114_Inventory_Subrack_20200114_112327.csv  | U2000RAN | 20200125 | 34505      | 34505        | 0            | 0            |
  | 96f4b6ad-3204-4b3a-8c22-18052bdf3b94 | 34551        | tx_u2000ran_subrack | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/23/20200121_Inventory_Subrack_20200121_110745.csv  | U2000RAN | 20200125 | 34551      | 34551        | 0            | 0            |
  | 42f579cf-0fb2-41f5-88fd-bf4f45167173 | 36568        | tx_u2000ran_subrack | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/39/20200121_Inventory_Subrack_20200121_110801.csv  | U2000RAN | 20200125 | 36568      | 36568        | 0            | 0            |
  | 00748331-4a28-45b5-aa02-86f54bf22e2a | 36583        | tx_u2000ran_subrack | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/39/20200114_Inventory_Subrack_20200114_112307.csv  | U2000RAN | 20200125 | 36583      | 36583        | 0            | 0            |
  | 6a2b1d08-6d69-4316-a59b-9080b500c158 | 30062        | tx_u2000ran_subrack | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/7/20191125_Inventory_Subrack_20191125_162416.csv   | U2000RAN | 20200125 | 30062      | 30062        | 0            | 0            |
  | 9f9b51e6-5107-4882-b52f-78726b0e03c1 | 36983        | tx_u2000ran_subrack | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/39/20191125_Inventory_Subrack_20191125_162421.csv  | U2000RAN | 20200125 | 36983      | 36983        | 0            | 0            |
  | 2b990811-3f82-49d0-8d5e-6a226a5afb32 | 11188        | tx_u2000ran_subrack | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/54/20200121_Inventory_Subrack_20200121_110442.csv  | U2000RAN | 20200125 | 11188      | 11188        | 0            | 0            |
  | e12fcf02-7bb6-4759-ab9b-374dd0352a53 | 10699        | tx_u2000ran_subrack | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/197/20200114_Inventory_Subrack_20200114_112230.csv | U2000RAN | 20200125 | 10699      | 10699        | 0            | 0            |
  | 966dfaf5-1b7b-4a5b-b058-aba04a5c2cd1 | 11044        | tx_u2000ran_subrack | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/54/20191125_Inventory_Subrack_20191125_161826.csv  | U2000RAN | 20200125 | 11044      | 11044        | 0            | 0            |
  | 9092b537-85eb-41dd-bb0d-e4eb11372fdd | 10665        | tx_u2000ran_subrack | 20191125 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_25112019/197/20191125_Inventory_Subrack_20191125_162140.csv | U2000RAN | 20200125 | 10665      | 10665        | 0            | 0            |
  | 81b19009-1e55-4676-8fbd-4851b85a3fa1 | 29965        | tx_u2000ran_subrack | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/7/20200114_Inventory_Subrack_20200114_112358.csv   | U2000RAN | 20200125 | 29965      | 29965        | 0            | 0            |
  | 507099ca-9061-4e4c-8440-751e85ec8f72 | 29913        | tx_u2000ran_subrack | 20200121 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_21012020/7/20200121_Inventory_Subrack_20200121_110751.csv   | U2000RAN | 20200125 | 29913      | 29913        | 0            | 0            |
  | aa901769-95c5-4c29-8552-8b0027769a46 | 11178        | tx_u2000ran_subrack | 20200114 | /home/raw_rci/pruebas_id014h/U2000_RAN/Inventario_RAN_14012020/54/20200114_Inventory_Subrack_20200114_112005.csv  | U2000RAN | 20200125 | 11178      | 11178        | 0            | 0            |

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 138   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 138
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

[imgEncabezado]:../Globales/ArquitecturaFrameworkIngestion/images/encabezado.png ""
