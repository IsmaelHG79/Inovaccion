![EncabezadoAxity][imgEncabezado]


# Documentación Data Ingestion para la fuente ATT **Smallworld**

Para esta fuente se documentan diferentes flujos de una sola fuente, esto debido a que existen diferentes tablas para su consumo.

## Descripción del `Orígen de Datos`  
Los datos de conexión son los siguientes:
```
Tecnología:       Excel
IP:               10.150.25.149
USR:              raw_rci
Nombre Archivo:   ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx
```
__Estructura Archivo__

| Nombre Archivo                            |#Pestaña| Pestaña Archivo                 | Esquema        | Tabla Target                          |
|-------------------------------------------|----------|---------------------------------|----------------|---------------------------------------|
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 1        | Pole                            | rci_network_db | tx_sw_pole                            |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 2        | Access Point                    | rci_network_db | tx_sw_accesspoint                     |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 3        | Bay                             | rci_network_db | tx_sw_bay                             |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 4        | Riser                           | rci_network_db | tx_sw_riser                           |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 5        | Building Structure              | rci_network_db | tx_sw_building_structure              |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 6        | Sheath Splice                   | rci_network_db | tx_sw_sheath_splice                   |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 7        | Underground Route               | rci_network_db | tx_sw_underground_route               |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 8        | Conduit                         | rci_network_db | tx_sw_conduit                         |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 9        | Container                       | rci_network_db | tx_sw_container                       |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 10       | Point Of Attachment             | rci_network_db | tx_sw_point_of_attachment             |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 11       | Sheath (LOC)                    | rci_network_db | tx_sw_sheath                          |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 12       | Floor                           | rci_network_db | tx_sw_floor                           |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 13       | Fibre Figure Eight              | rci_network_db | tx_sw_fibre_figure_eight              |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 14       | Aerial Route                    | rci_network_db | tx_sw_aerial_route                    |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 15       | Port                            | rci_network_db | tx_sw_port                            |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 16       | Underground Utility Box         | rci_network_db | tx_sw_underground_utility_box         |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 17       | Anchor                          | rci_network_db | tx_sw_anchor                          |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 18       | Room                            | rci_network_db | tx_sw_room                            |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 19       | Shelf                           | rci_network_db | tx_sw_shelf                           |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 20       | Building                        | rci_network_db | tx_sw_building                        |
| ELEMENTOS_CARGADOS_EN_PNI_Julio_2019.xlsx | 21       | Structural Wiring Connection Po | rci_network_db | tx_sw_structural_wiring_connection_po |

## Componentes del procesos de ingestión (Flujo General):

__Ingestión y Serialización via NiFi__

__Flujo Principal__

![FlujoPrincipal][img1]

__Flujo de Subproceso__

![FlujoSubproceso][img2]

__SFTP Process__

![SFTP Process][img3]

__Flujo General__

__Pole__

![Flujo Principal Pole][img4]

__File Process__

![File Process][img5]

__Cifra Control__

![Cifra Control][img6]

__Process Avro Schema__

![Process Avro Schema][img7]



[img1]: images/smallworld-nifi-00.png ""
[img2]: images/smallworld-nifi-01.png ""
[img3]: images/smallworld-nifi-02.png ""
[img4]: images/smallworld-nifi-03.png ""
[img5]: images/smallworld-nifi-04.png ""
[img6]: images/smallworld-nifi-05.png ""
[img7]: images/smallworld-nifi-06.png ""



## Listado de Tablas  

* [Pole](#Pole)
* [Access Point](#AccessPoint)
* [Bay](#Bay)
* [Riser](#Riser)
* [Building Structure](#BuildingStructure)
* [Sheath Splice](#SheathSplice)
* [Underground Route](#UndergroundRoute)
* [Conduit](#Conduit)
* [Container](#Container)
* [Point Of Attachment](#PointOfAttachment)
* [Sheath (LOC)](#SheathLOC)
* [Floor](#Floor)
* [Fibre Figure Eight](#FibreFigureEight)
* [Aerial Route](#AerialRoute)
* [Port](#Port)
* [Underground Utility Box](#UndergroundUtilityBox)
* [Anchor](#Anchor)
* [Room](#Room)
* [Shelf](#Shelf)
* [Building](#Building)
* [Structural Wiring Connection Po](#StructuralWiringConnectionPo)





## <a name="Pole"></a>Pole

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Pole](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
  [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_pole```

  | Id | Nombre de la Columna     | Tipo de Dato | Comentario                               |
  |----|--------------------------|--------------|------------------------------------------|
  | 1  | id                       | string       | Type inferred from '4894712882786520000' |
  | 2  | usage                    | string       | Type inferred from 'Power'               |
  | 3  | catvpoletag              | string       | Type inferred from '9'                   |
  | 4  | constructionstatus       | string       | Type inferred from 'In Service'          |
  | 5  | catvriserheight          | string       | Type inferred from '1000.0 mm'           |
  | 6  | estadofisico             | string       | Type inferred from 'BUENO'               |
  | 7  | tipodesuelo              | string       | Type inferred from 'BANQUETA'            |
  | 8  | codigodeobjeto           | string       | Type inferred from 'CFE'                 |
  | 9  | bajadaenergiafibraoptica | string       | Type inferred from 'DESCONOCIDO'         |
  | 10 | elementoaterrizado       | string       | Type inferred from 'DESCONOCIDO'         |
  | 11 | infraestructura          | string       | Type inferred from 'DESCONOCIDO'         |
  | 12 | nocarriersflejes         | string       | Type inferred from '3'                   |
  | 13 | herraje                  | string       | Type inferred from 'TENSION'             |

  Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestión.

  | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
  |----|----------------------|--------------|-------------------------------------------------------------------------|
  | 14 | hash_id              | string       | Type inferred from 'null'                                               |
  | 15 | datasetname          | string       | Type inferred from 'tx_sw_pole'                                         |
  | 16 | timestamp            | bigint       | Type inferred from '20200122'                                           |
  | 17 | transaction_status   | string       | Type inferred from 'null'                                               |
  | 18 | filedate             | bigint       | Type inferred from '20190701'                                           |
  | 19 | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Pole.c' |
  | 20 | sourceid             | string       | Type inferred from 'smallworld'                                         |
  | 21 | registry_state       | string       | Type inferred from 'null'                                               |    



- **Particiones**

    A continuación se presentan las particiones creadas de la tabla **tx_sw_pole**.

    Sentencia: ```show partitions rci_network_db.tx_sw_pole```

    | year | month | #Rows | #Files | Size     | Format | Incremental stats | Location                                                                           |
    |------|-------|-------|--------|----------|--------|-------------------|------------------------------------------------------------------------------------|
    | 2019 | 7     | 636   | 1      | 183.36KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/pole/year=2019/month=7 |


- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_pole';
    ```    

    | id_execution | table_name | dateload | avro_name                                                                                | start_execution  | end_execution    | status |
    |--------------|------------|----------|------------------------------------------------------------------------------------------|------------------|------------------|--------|
    | 1            | tx_sw_pole | 20200123 | /data/RCI/raw/smallworld/pole/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Pole.avro | 23/01/2020 15:57 | 23/01/2020 15:58 | 1      |

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_sw_pole'
    and dateload = 20200122
    order by filedate asc;
    ```    

  | uuid                                 | rowprocessed | datasetname | filedate | filename                                             | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|-------------|----------|------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
  | 44510c92-bb4d-4d9e-9c21-49d9e9fa11d5 | 118208       | tx_sw_pole  | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Pole.csv | smallworld | 20200122 | 118208     | 118208       | 0            | 0            |

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

Especificar parámetros del proceso kite:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 111   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 111
```


## <a name="Access Point"></a>AccessPoint

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [AccessPoint](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_accesspoint```

  | Id | Nombre de la Columna | Tipo de Dato | Comentario                               |
  |----|----------------------|--------------|------------------------------------------|
  | 1  | id                   | string       | Type inferred from '4894712882786520000' |
  | 2  | specification        | string       | Type inferred from 'Building Entry'      |
  | 3  | type                 | string       | Type inferred from 'Conduit Terminus'    |

     Las siguientes columnas son creadas para la identidad de la fuente:

  | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
  |----|----------------------|--------------|-------------------------------------------------------------------------|
  | 4  | filedate             | bigint       | Type inferred from '20190701'                                           |
  | 5  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Access' |
  | 6  | hash_id              | string       | Type inferred from 'null'                                               |
  | 7  | sourceid             | string       | Type inferred from 'smallworld'                                         |
  | 8  | registry_state       | string       | Type inferred from 'null'                                               |
  | 9  | datasetname          | string       | Type inferred from 'tx_sw_accesspoint'                                  |
  | 10 | timestamp            | bigint       | Type inferred from '20200122'                                           |
  | 11 | transaction_status   | string       | Type inferred from 'null'                                               |


- **Particiones**

  A continuación se presentan las particiones creadas de la tabla **tx_sw_accesspoint**.

  Sentencia: ```show partitions rci_network_db.tx_sw_accesspoint```

  | year | month | #Rows | #Files | Size    | Format | Incremental stats | Location                                                                                  |
  |------|-------|-------|--------|---------|--------|-------------------|-------------------------------------------------------------------------------------------|
  | 2019 | 7     | 385   | 1      | 92.58KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/accesspoint/year=2019/month=7 |

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_accesspoint';
  ```

  | id_execution | table_name        | dateload | avro_name                                                                                               | start_execution  | end_execution    | status |
  |--------------|-------------------|----------|---------------------------------------------------------------------------------------------------------|------------------|------------------|--------|
  | 1            | tx_sw_accesspoint | 20200123 | /data/RCI/raw/smallworld/accesspoint/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Access_Point.avro | 23/01/2020 16:02 | 23/01/2020 16:03 | 1      |  

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_sw_accesspoint'
  and dateload = 20200122
  order by filedate asc;
  ```      
  | uuid                                 | rowprocessed | datasetname       | filedate | filename                                                     | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|-------------------|----------|--------------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
  | cb309773-3294-4c18-9db8-5fa6026226a6 | 1772         | tx_sw_accesspoint | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Access Point.csv | smallworld | 20200122 | 1772       | 1772         | 0            | 0            |

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 112   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 112
```


## <a name="Bay"></a>Bay

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Bay](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_bay```

  | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                   |
  |----|----------------------|--------------|--------------------------------------------------------------|
  | 1  | description          | string       | Type inferred from 'HCUE0010 DOMINGO DIEZ'                   |
  | 2  | number               | string       | Type inferred from '1'                                       |
  | 3  | constructionstatus   | string       | Type inferred from 'In Service'                              |
  | 4  | accountcode          | string       | Type inferred from 'null'                                    |
  | 5  | installedcost        | string       | Type inferred from 'null'                                    |
  | 6  | dateinstalled        | string       | Type inferred from 'null'                                    |
  | 7  | installername        | string       | Type inferred from 'null'                                    |
  | 8  | barcodenumber        | string       | Type inferred from 'null'                                    |
  | 9  | serialnumber         | string       | Type inferred from 'null'                                    |
  | 10 | acceptancedate       | string       | Type inferred from 'null'                                    |
  | 11 | acceptancename       | string       | Type inferred from 'null'                                    |
  | 12 | shortname            | string       | Type inferred from 'HCUE0010 DOMINGO DIEZ'                   |
  | 13 | mediumname           | string       | Type inferred from 'Bay(HCUE0010 DOMINGO DIEZ), Number = 1'  |
  | 14 | longname             | string       | Type inferred from 'HCUE0010 DOMINGO DIEZ,In Service'        |
  | 15 | shortdescription     | string       | Type inferred from 'HCUE0010 DOMINGO DIEZ 1'                 |
  | 16 | mediumdescription    | string       | Type inferred from 'Bay : HCUE0010 DOMINGO DIEZ, Number - 1' |
  | 17 | longdescription      | string       | Type inferred from 'Room : 1, HCUE0010 DOMINGO DIEZ 1'       |

     Las siguientes columnas son creadas para la identidad de la fuente:

  | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
  |----|----------------------|--------------|-------------------------------------------------------------------------|
  | 18 | filedate             | bigint       | Type inferred from '20190701'                                           |
  | 19 | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Bay.cs' |
  | 20 | hash_id              | string       | Type inferred from 'null'                                               |
  | 21 | sourceid             | string       | Type inferred from 'smallworld'                                         |
  | 22 | registry_state       | string       | Type inferred from 'null'                                               |
  | 23 | datasetname          | string       | Type inferred from 'tx_sw_bay'                                          |
  | 24 | timestamp            | bigint       | Type inferred from '20200122'                                           |
  | 25 | transaction_status   | string       | Type inferred from 'null'                                               |    


- **Particiones**

  A continuación se presentan las particiones creadas de la tabla **tx_sw_bay**.

  Sentencia: ```show partitions rci_network_db.tx_sw_bay```

  | year | month | #Rows | #Files | Size   | Format | Incremental stats | Location                                                                          |
  |------|-------|-------|--------|--------|--------|-------------------|-----------------------------------------------------------------------------------|
  | 2019 | 7     | 1     | 1      | 3.17KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/bay/year=2019/month=7 |

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_bay';
  ```

  | id_execution | table_name | dateload | avro_name                                                                              | start_execution  | end_execution    | status |
  |--------------|------------|----------|----------------------------------------------------------------------------------------|------------------|------------------|--------|
  | 1            | tx_sw_bay  | 20200123 | /data/RCI/raw/smallworld/bay/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Bay.avro | 23/01/2020 17:13 | 23/01/2020 17:14 | 1      |

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_sw_bay'
  and dateload = 20200122
  order by filedate asc;
  ```

  | uuid                                 | rowprocessed | datasetname | filedate | filename                                            | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|-------------|----------|-----------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
  | 8f2d8e7c-2241-4df6-85e9-90e1f9a827e6 | 69           | tx_sw_bay   | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Bay.csv | smallworld | 20200122 | 69         | 69           | 0            | 0            |   

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

      | Parámetro | Valor | Descripción|
      | ---------- | ---------- | ---------- |
      | parametro_01   | 113   | Valor de correspondiente al flujo|

       Sentencia kite:

      ```
      ./rci_ingesta_generacion_avro.sh {parametro_01}
      ```
      Ejemplo:

      ```
      ./rci_ingesta_generacion_avro.sh 113
      ```

## <a name="Riser"></a>Riser

  Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
  - **Descripción**
    [Riser](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

  - **Diccionario de Datos**
       [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

       Sentencia: ```describe formatted rci_network_db.tx_sw_riser```

       | Id | Nombre de la Columna | Tipo de Dato | Comentario                      |
       |----|----------------------|--------------|---------------------------------|
       | 1  | constructionstatus   | string       | Type inferred from 'In Service' |
       | 2  | ownership            | string       | Type inferred from 'Cable'      |
       | 3  | length               | string       | Type inferred from '1.000 m'    |
       | 4  | accountcode          | string       | Type inferred from 'null'       |
       | 5  | installedcost        | string       | Type inferred from 'null'       |

       Las siguientes columnas son creadas para la identidad de la fuente:

       | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
       |----|----------------------|--------------|-------------------------------------------------------------------------|
       | 6  | filedate             | bigint       | Type inferred from '20190701'                                           |
       | 7  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Riser.' |
       | 8  | hash_id              | string       | Type inferred from 'null'                                               |
       | 9  | sourceid             | string       | Type inferred from 'smallworld'                                         |
       | 10 | registry_state       | string       | Type inferred from 'null'                                               |
       | 11 | datasetname          | string       | Type inferred from 'tx_sw_riser'                                        |
       | 12 | timestamp            | bigint       | Type inferred from '20200122'                                           |
       | 13 | transaction_status   | string       | Type inferred from 'null'                                               |

  - **Particiones**

    A continuación se presentan las particiones creadas de la tabla **tx_sw_riser**.

    Sentencia: ```show partitions rci_network_db.tx_sw_riser```

    | year | month | #Rows | #Files | Size   | Format | Incremental stats | Location                                                                            |
    |------|-------|-------|--------|--------|--------|-------------------|-------------------------------------------------------------------------------------|
    | 2019 | 7     | 14    | 1      | 4.26KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/riser/year=2019/month=7 |

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_riser';
  ```

  | id_execution | table_name  | dateload | avro_name                                                                                  | start_execution     | end_execution       | status | id_application | attempts |
  |--------------|-------------|----------|--------------------------------------------------------------------------------------------|---------------------|---------------------|--------|----------------|----------|
  | 1            | tx_sw_riser | 20200123 | /data/RCI/raw/smallworld/riser/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Riser.avro | 2020-01-23 17:20:26 | 2020-01-23 17:21:10 | 1      |                | 0        |

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_sw_riser'
  and dateload = 20200122
  order by filedate asc;
  ```
  | uuid                                 | rowprocessed | datasetname | filedate | filename                                              | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|-------------|----------|-------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
  | ee3486b8-bc07-40ba-ad40-e506227e98bf | 8951         | tx_sw_riser | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Riser.csv | smallworld | 20200122 | 8951       | 8951         | 0            | 0            |

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

       | Parámetro | Valor | Descripción|
       | ---------- | ---------- | ---------- |
       | parametro_01   | 114   | Valor de correspondiente al flujo|

      Sentencia kite:

       ```
       ./rci_ingesta_generacion_avro.sh {parametro_01}
       ```
       Ejemplo:

       ```
       ./rci_ingesta_generacion_avro.sh 114
       ```

## <a name="BuildingStructure"></a>Building Structure

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [BuildingStructure](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_building_structure```

     | Id | Nombre de la Columna  | Tipo de Dato | Comentario                      |
     |----|-----------------------|--------------|---------------------------------|
     | 1  | numberoffloors        | string       | Type inferred from '1'          |
     | 2  | undergroundfloors     | string       | Type inferred from '0'          |
     | 3  | floordimensionlength  | string       | Type inferred from '6.000 m'    |
     | 4  | floordimensionwidth   | string       | Type inferred from '6.000 m'    |
     | 5  | numberofroomslength   | string       | Type inferred from '1'          |
     | 6  | numberofroomswidth    | string       | Type inferred from '0'          |
     | 7  | defaultroomtype       | string       | Type inferred from 'Commercial' |
     | 8  | defaultservicetype    | string       | Type inferred from 'Unknown'    |
     | 9  | defaultriserlength    | string       | Type inferred from '0.010 m'    |
     | 10 | defaultriserownership | string       | Type inferred from 'Cable'      |

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 11 | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 12 | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Buildi' |
     | 13 | hash_id              | string       | Type inferred from 'null'                                               |
     | 14 | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 15 | registry_state       | string       | Type inferred from 'null'                                               |
     | 16 | datasetname          | string       | Type inferred from 'tx_sw_building_structure'                           |
     | 17 | timestamp            | bigint       | Type inferred from '20200122'                                           |
     | 18 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_building_structure**.

 Sentencia: ```show partitions rci_network_db.tx_sw_building_structure```

  | year | month | #Rows | #Files | Size   | Format | Incremental stats | Location                                                                                         |
  |------|-------|-------|--------|--------|--------|-------------------|--------------------------------------------------------------------------------------------------|
  | 2019 | 7     | 1     | 1      | 2.24KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/building_structure/year=2019/month=7 |

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_building_structure';
   ```

   | id_execution | table_name               | dateload | avro_name                                                                                                            | start_execution     | end_execution       | status |
   |--------------|--------------------------|----------|----------------------------------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
   | 1            | tx_sw_building_structure | 20200123 | /data/RCI/raw/smallworld/building_structure/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Building_Structure.avro | 2020-01-23 17:25:49 | 2020-01-23 17:26:35 | 1      |

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_sw_building_structure'
   and dateload = 20191225
   order by filedate asc;
   ```

   | uuid                                 | rowprocessed | datasetname              | filedate | filename                                                           | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
   |--------------------------------------|--------------|--------------------------|----------|--------------------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
   | a1c6ddcb-bdb2-4206-9885-10e51407a9c0 | 71           | tx_sw_building_structure | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Building Structure.csv | smallworld | 20200122 | 71         | 71           | 0            | 0            |

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 115   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 115
```


## <a name="SheathSplice"></a>Sheath Splice

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Sheath Splice](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_sheath_splice```

     | Id | Nombre de la Columna       | Tipo de Dato | Comentario                               |
     |----|----------------------------|--------------|------------------------------------------|
     | 1  | id                         | string       | Type inferred from '4894712882786520000' |
     | 2  | name                       | string       | Type inferred from 'FO-CHI-03'           |
     | 3  | specification              | string       | Type inferred from 'Splice 1'            |
     | 4  | constructionstatus         | string       | Type inferred from 'In Service'          |
     | 5  | splicetype                 | string       | Type inferred from 'breaking'            |
     | 6  | method                     | string       | Type inferred from 'Fusion'              |
     | 7  | availablemountingpositions | string       | Type inferred from '6'                   |
     | 8  | estadofisico               | string       | Type inferred from 'BUENO'               |
     | 9  | distanciaaposte            | string       | Type inferred from '3.000 m'             |
     | 10 | puntasdecable              | string       | Type inferred from '3'                   |

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 11 | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 12 | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Sheath' |
     | 13 | hash_id              | string       | Type inferred from 'null'                                               |
     | 14 | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 15 | registry_state       | string       | Type inferred from 'null'                                               |
     | 16 | datasetname          | string       | Type inferred from 'tx_sw_sheath_splice'                                |
     | 17 | timestamp            | bigint       | Type inferred from '20200122'                                           |
     | 18 | transaction_status   | string       | Type inferred from 'null'                                               |


   - **Particiones**

     A continuación se presentan las particiones creadas de la tabla **tx_sw_sheath_splice**.

     Sentencia: ```show partitions rci_network_db.tx_sw_sheath_splice```

     | year | month | #Rows | #Files | Size     | Format | Incremental stats | Location                                                                                    |
     |------|-------|-------|--------|----------|--------|-------------------|---------------------------------------------------------------------------------------------|
     | 2019 | 7     | 588   | 1      | 168.20KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/sheath_splice/year=2019/month=7 |

   - **Ejecuciones**

      En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

      ```
      select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_sheath_splice';
      ```

      | id_execution | table_name          | dateload | avro_name                                                                                                  | start_execution     | end_execution       | status |
      |--------------|---------------------|----------|------------------------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
      | 1            | tx_sw_sheath_splice | 20200123 | /data/RCI/raw/smallworld/sheath_splice/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Sheath_Splice.avro | 2020-01-23 17:29:03 | 2020-01-23 17:29:56 | 1      |

   - **Cifras de Control**

      En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

      ```
      select * from rci_network_db.tx_cifras_control
      where datasetname = 'tx_sw_sheath_splice'
      and dateload = 20200122
      order by filedate asc;
      ```

      | uuid                                 | rowprocessed | datasetname         | filedate | filename                                                      | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
      |--------------------------------------|--------------|---------------------|----------|---------------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
      | 55ade7a4-7120-4326-a5de-74c93e488ac0 | 12595        | tx_sw_sheath_splice | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Sheath Splice.csv | smallworld | 20200122 | 12595      | 12595        | 0            | 0            |

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 116   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 116
```


## <a name="UndergroundRoute"></a>Underground Route

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Underground Route](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_underground_route```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                               |
     |----|----------------------|--------------|------------------------------------------|
     | 1  | id                   | string       | Type inferred from '4894712882786820000' |
     | 2  | name                 | string       | Type inferred from 'CANALIZACION'        |
     | 3  | constructionstatus   | string       | Type inferred from 'In Service'          |
     | 4  | undergroundroutetype | string       | Type inferred from 'Unknown'             |
     | 5  | calculatedlength     | string       | Type inferred from '39.265 m'            |
     | 6  | measuredlength       | string       | Type inferred from '39.000 m'            |
     | 7  | surfacematerial      | string       | Type inferred from 'Asphalt'             |
     | 8  | surroundingmaterial  | string       | Type inferred from 'Asphalt'             |
     | 9  | diameter             | string       | Type inferred from '400 mm'              |
     | 10 | centrepointdepth     | string       | Type inferred from '800 mm'              |
     | 11 | width                | string       | Type inferred from 'null'                |
     | 12 | basematerial         | string       | Type inferred from 'null'                |
     | 13 | basematerialdepth    | string       | Type inferred from 'null'                |
     | 14 | corematerial         | string       | Type inferred from 'null'                |
     | 15 | corematerialdepth    | string       | Type inferred from 'null'                |
     | 16 | uppermaterial        | string       | Type inferred from 'null'                |
     | 17 | uppermaterialdepth   | string       | Type inferred from 'null'                |
     | 18 | installedcost        | string       | Type inferred from 'null'                |

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 19 | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 20 | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Underg' |
     | 21 | hash_id              | string       | Type inferred from 'null'                                               |
     | 22 | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 23 | registry_state       | string       | Type inferred from 'null'                                               |
     | 24 | datasetname          | string       | Type inferred from 'tx_sw_underground_route'                            |
     | 25 | timestamp            | bigint       | Type inferred from '20200122'                                           |
     | 26 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_underground_route**.

 Sentencia: ```show partitions rci_network_db.tx_sw_underground_route```

 | year | month | #Rows | #Files | Size    | Format | Incremental stats | Location                                                                                        |
 |------|-------|-------|--------|---------|--------|-------------------|-------------------------------------------------------------------------------------------------|
 | 2019 | 7     | 291   | 1      | 95.42KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/underground_route/year=2019/month=7 |

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_underground_route';
  ```

  | id_execution | table_name              | dateload | avro_name                                                                                                          | start_execution     | end_execution       | status |
  |--------------|-------------------------|----------|--------------------------------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
  | 1            | tx_sw_underground_route | 20200123 | /data/RCI/raw/smallworld/underground_route/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Underground_Route.avro | 2020-01-23 17:33:00 | 2020-01-23 17:33:50 | 1      |

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_sw_underground_route'
  and dateload = 20200122
  order by filedate asc;
  ```
  | uuid                                 | rowprocessed | datasetname             | filedate | filename                                                          | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|-------------------------|----------|-------------------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
  | 98f3bee5-387d-431d-9d0a-488cb32e7f04 | 1567         | tx_sw_underground_route | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Underground Route.csv | smallworld | 20200122 | 1567       | 1567         | 0            | 0            |

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 117   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 117
```


## <a name="Conduit"></a>Conduit

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Conduit](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_conduit```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                       |
     |----|----------------------|--------------|----------------------------------|
     | 1  | id                   | string       | Type inferred from '21497'       |
     | 2  | name                 | string       | Type inferred from '1'           |
     | 3  | specification        | string       | Type inferred from 'PVC 40.0 mm' |
     | 4  | constructionstatus   | string       | Type inferred from 'In Service'  |
     | 5  | owner                | string       | Type inferred from 'null'        |
     | 6  | usage                | string       | Type inferred from 'Fibre Only'  |

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 7  | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 8  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Condui' |
     | 9  | hash_id              | string       | Type inferred from 'null'                                               |
     | 10 | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 11 | registry_state       | string       | Type inferred from 'null'                                               |
     | 12 | datasetname          | string       | Type inferred from 'tx_sw_conduit'                                      |
     | 13 | timestamp            | bigint       | Type inferred from '20200122'                                           |
     | 14 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_conduit**.

 Sentencia: ```show partitions rci_network_db.tx_sw_conduit```

  | year | month | #Rows | #Files | Size    | Format | Incremental stats | Location                                                                              |
  |------|-------|-------|--------|---------|--------|-------------------|---------------------------------------------------------------------------------------|
  | 2019 | 7     | 407   | 1      | 91.57KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/conduit/year=2019/month=7 |

- **Ejecuciones**

 En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

 ```
 select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_conduit';
 ```

   | id_execution | table_name    | dateload | avro_name                                                                                      | start_execution  | end_execution    | status |
   |--------------|---------------|----------|------------------------------------------------------------------------------------------------|------------------|------------------|--------|
   | 1            | tx_sw_conduit | 20200123 | /data/RCI/raw/smallworld/conduit/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Conduit.avro | 23/01/2020 17:39 | 23/01/2020 17:40 | 1      |

- **Cifras de Control**

 En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

 ```
 select * from rci_network_db.tx_cifras_control
 where datasetname = 'tx_sw_conduit'
 and dateload = 20200122
 order by filedate asc;
 ```

  | id_execution | table_name    | dateload | avro_name                                                                                      | start_execution     | end_execution       | status |
  |--------------|---------------|----------|------------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
  | 1            | tx_sw_conduit | 20200123 | /data/RCI/raw/smallworld/conduit/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Conduit.avro | 2020-01-23 17:39:29 | 2020-01-23 17:40:20 | 1      |

## Componentes del procesos de ingestión:

 __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 118   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 118
```

## <a name="Container"></a>Container

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Container](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_container```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                          |
     |----|----------------------|--------------|-----------------------------------------------------|
     | 1  | specid               | string       | Type inferred from 'Alcatel generic bay (2500x600)' |

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 2  | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 3  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Contai' |
     | 4  | hash_id              | string       | Type inferred from 'null'                                               |
     | 5  | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 6  | registry_state       | string       | Type inferred from 'null'                                               |
     | 7  | datasetname          | string       | Type inferred from 'tx_sw_container'                                    |
     | 8  | timestamp            | bigint       | Type inferred from '20200122'                                           |
     | 9  | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_container**.

 Sentencia: ```show partitions rci_network_db.tx_sw_container```

  | year | month | #Rows | #Files | Size   | Format | Incremental stats | Location                                                                                |
  |------|-------|-------|--------|--------|--------|-------------------|-----------------------------------------------------------------------------------------|
  | 2019 | 7     | 1     | 1      | 1.28KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/container/year=2019/month=7 |

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_container';
  ```

  | id_execution | table_name      | dateload | avro_name                                                                                          | start_execution     | end_execution       | status |
  |--------------|-----------------|----------|----------------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
  | 1            | tx_sw_container | 20200123 | /data/RCI/raw/smallworld/container/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Container.avro | 2020-01-23 17:42:42 | 2020-01-23 17:43:27 | 1      |

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_sw_container'
  and dateload = 20191225
  order by filedate asc;
  ```

  | uuid                                 | rowprocessed | datasetname     | filedate | filename                                                  | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|-----------------|----------|-----------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
  | 8af91107-89f2-4069-8839-37fbdae1a7b5 | 205          | tx_sw_container | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Container.csv | smallworld | 20200122 | 205        | 205          | 0            | 0            |

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 119   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 119
  ```

## <a name="PointOfAttachment"></a>Point Of Attachment

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Point Of Attachment](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
    [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_point_of_attachment```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                               |
     |----|----------------------|--------------|------------------------------------------|
     | 1  | id                   | string       | Type inferred from '4894712882786460000' |
     | 2  | label                | string       | Type inferred from 'CR'                  |
     | 3  | constructionstatus   | string       | Type inferred from 'In Service'          |

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 4  | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 5  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Point ' |
     | 6  | hash_id              | string       | Type inferred from 'null'                                               |
     | 7  | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 8  | registry_state       | string       | Type inferred from 'null'                                               |
     | 9  | datasetname          | string       | Type inferred from 'tx_sw_point_of_attachment'                          |
     | 10 | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 11 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_point_of_attachment**.

 Sentencia: ```show partitions rci_network_db.tx_sw_point_of_attachment```

  | year | month | #Rows | #Files | Size    | Format | Incremental stats | Location                                                                                          |
  |------|-------|-------|--------|---------|--------|-------------------|---------------------------------------------------------------------------------------------------|
  | 2019 | 7     | 340   | 1      | 81.31KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/point_of_attachment/year=2019/month=7 |

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_point_of_attachment';
   ```

  | id_execution | table_name                | dateload | avro_name                                                                                                              | start_execution     | end_execution       | status |
  |--------------|---------------------------|----------|------------------------------------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
  | 1            | tx_sw_point_of_attachment | 20200124 | /data/RCI/raw/smallworld/point_of_attachment/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Point_Of_Attachment.avro | 2020-01-24 10:45:43 | 2020-01-24 10:46:31 | 1      |

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_sw_point_of_attachment'
   and dateload = 20200122
   order by filedate asc;
   ```

  | uuid                                 | rowprocessed | datasetname               | filedate | filename                                                            | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|---------------------------|----------|---------------------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
  | 99bc0502-3292-4e45-adea-2eaeaba33a8b | 1071         | tx_sw_point_of_attachment | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Point Of Attachment.csv | smallworld | 20200124 | 1071       | 1071         | 0            | 0            |

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 120   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 120
  ```

## <a name="SheathLOC"></a>Sheath (LOC)

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [SheathLOC](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_sheath```

     | Id | Nombre de la Columna   | Tipo de Dato | Comentario                               |
     |----|------------------------|--------------|------------------------------------------|
     | 1  | id                     | string       | Type inferred from '4894712882786520000' |
     | 2  | name                   | string       | Type inferred from 'FOHMEX0243'          |
     | 3  | specification          | string       | Type inferred from 'AT&T LXE 96'         |
     | 4  | constructionstatus     | string       | Type inferred from 'In Service'          |
     | 5  | calculatedlength       | string       | Type inferred from '632.030 m'           |
     | 6  | calculatedsheathlength | string       | Type inferred from '692.030 m'           |
     | 7  | installedcost          | string       | Type inferred from 'null'                |
     | 8  | estadofisico           | string       | Type inferred from 'BUENO'               |
     | 9  | identificacion         | string       | Type inferred from 'DESCONOCIDO'         |

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 10 | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 11 | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Sheath' |
     | 12 | hash_id              | string       | Type inferred from 'null'                                               |
     | 13 | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 14 | registry_state       | string       | Type inferred from 'null'                                               |
     | 15 | datasetname          | string       | Type inferred from 'tx_sw_sheath'                                       |
     | 16 | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 17 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_sheath**.

 Sentencia: ```show partitions rci_network_db.tx_sw_sheath```

  | year | month | #Rows | #Files | Size     | Format | Incremental stats | Location                                                                             |
  |------|-------|-------|--------|----------|--------|-------------------|--------------------------------------------------------------------------------------|
  | 2019 | 7     | 649   | 1      | 178.30KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/sheath/year=2019/month=7 |

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_sheath';
   ```

  | id_execution | table_name   | dateload | avro_name                                                                                       | start_execution     | end_execution       | status |
  |--------------|--------------|----------|-------------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
  | 1            | tx_sw_sheath | 20200124 | /data/RCI/raw/smallworld/sheath/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_SheathLOC.avro | 2020-01-24 11:04:13 | 2020-01-24 11:05:04 | 1      |

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_sw_sheath'
   and dateload = 20200124
   order by filedate asc;
   ```

  | uuid                                 | rowprocessed | datasetname  | filedate | filename                                                  | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|--------------|----------|-----------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
  | 423f50b3-cfa7-49ac-bef7-e8fb211b22a8 | 19706        | tx_sw_sheath | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_SheathLOC.csv | smallworld | 20200124 | 19706      | 19706        | 0            | 0            |

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 121   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 121
  ```


## <a name="Floor"></a>Floor

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Floor](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_floor```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario             |
     |----|----------------------|--------------|------------------------|
     | 1  | name                 | string       | Type inferred from '1' |

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 2  | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 3  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Floor.' |
     | 4  | hash_id              | string       | Type inferred from 'null'                                               |
     | 5  | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 6  | registry_state       | string       | Type inferred from 'null'                                               |
     | 7  | datasetname          | string       | Type inferred from 'tx_sw_floor'                                        |
     | 8  | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 9  | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_floor**.

 Sentencia: ```show partitions rci_network_db.tx_sw_floor```

  | year | month | #Rows | #Files | Size   | Format | Incremental stats | Location                                                                            |
  |------|-------|-------|--------|--------|--------|-------------------|-------------------------------------------------------------------------------------|
  | 2019 | 7     | 4     | 1      | 1.73KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/floor/year=2019/month=7 |

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_floor';
   ```

  | id_execution | table_name  | dateload | avro_name                                                                                  | start_execution     | end_execution       | status |
  |--------------|-------------|----------|--------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
  | 1            | tx_sw_floor | 20200124 | /data/RCI/raw/smallworld/floor/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Floor.avro | 2020-01-24 11:06:35 | 2020-01-24 11:07:19 | 1      |

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_sw_floor'
   and dateload = 20200124
   order by filedate asc;
   ```

  | uuid                                 | rowprocessed | datasetname | filedate | filename                                              | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|-------------|----------|-------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
  | c72b48d7-62d8-4454-ace8-60649f3630a8 | 77           | tx_sw_floor | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Floor.csv | smallworld | 20200124 | 77         | 77           | 0            | 0            |

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 122   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 122
  ```

## <a name="FibreFigureEight"></a>Fibre Figure Eight

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Fibre Figure Eight](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_fibre_figure_eight```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                               |
     |----|----------------------|--------------|------------------------------------------|
     | 1  | id                   | string       | Type inferred from '4894712882786520000' |
     | 2  | constructionstatus   | string       | Type inferred from 'In Service'          |
     | 3  | type                 | string       | Type inferred from 'Circle'              |
     | 4  | length               | string       | Type inferred from '20.000 m'            |
     | 5  | estadofisico         | string       | Type inferred from 'BUENO'               |
     | 6  | distanciaaposte      | string       | Type inferred from '3.000 m'             |

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 7  | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 8  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Fibre ' |
     | 9  | hash_id              | string       | Type inferred from 'null'                                               |
     | 10 | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 11 | registry_state       | string       | Type inferred from 'null'                                               |
     | 12 | datasetname          | string       | Type inferred from 'tx_sw_fibre_figure_eight'                           |
     | 13 | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 14 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_fibre_figure_eight**.

 Sentencia: ```show partitions rci_network_db.tx_sw_fibre_figure_eight```

  | year | month | #Rows | #Files | Size     | Format | Incremental stats | Location                                                                                         |
  |------|-------|-------|--------|----------|--------|-------------------|--------------------------------------------------------------------------------------------------|
  | 2019 | 7     | 600   | 1      | 161.72KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/fibre_figure_eight/year=2019/month=7 |

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_fibre_figure_eight';
   ```

  | id_execution | table_name               | dateload | avro_name                                                                                                            | start_execution     | end_execution       | status |
  |--------------|--------------------------|----------|----------------------------------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
  | 1            | tx_sw_fibre_figure_eight | 20200124 | /data/RCI/raw/smallworld/fibre_figure_eight/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Fibre_Figure_Eight.avro | 2020-01-24 11:12:30 | 2020-01-24 11:13:21 | 1      |

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_sw_fibre_figure_eight'
   and dateload = 20200124
   order by filedate asc;
   ```

  | uuid                                 | rowprocessed | datasetname              | filedate | filename                                                           | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|--------------------------|----------|--------------------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
  | 7b18ad18-c262-447f-95f8-6f7df07e7010 | 31454        | tx_sw_fibre_figure_eight | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Fibre Figure Eight.csv | smallworld | 20200124 | 31454      | 31454        | 0            | 0            |

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 123   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 123
  ```

## <a name="AerialRoute"></a>Aerial Route

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Aerial Route](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_aerial_route```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                               |
     |----|----------------------|--------------|------------------------------------------|
     | 1  | id                   | string       | Type inferred from '4894712882786460000' |
     | 2  | constructionstatus   | string       | Type inferred from 'In Service'          |
     | 3  | calculatedlength     | string       | Type inferred from '82.1 m'              |
     | 4  | measuredlength       | string       | Type inferred from '80.0 m'              |
     | 5  | guytype              | string       | Type inferred from 'Overhead'            |
     | 6  | estadofisico         | string       | Type inferred from 'BUENO'               |

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 7  | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 8  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Aerial' |
     | 9  | hash_id              | string       | Type inferred from 'null'                                               |
     | 10 | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 11 | registry_state       | string       | Type inferred from 'null'                                               |
     | 12 | datasetname          | string       | Type inferred from 'tx_sw_aerial_route'                                 |
     | 13 | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 14 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_aerial_route**.

 Sentencia: ```show partitions rci_network_db.tx_sw_aerial_route```

  | year | month | #Rows | #Files | Size     | Format | Incremental stats | Location                                                                                   |
  |------|-------|-------|--------|----------|--------|-------------------|--------------------------------------------------------------------------------------------|
  | 2019 | 7     | 690   | 1      | 173.27KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/aerial_route/year=2019/month=7 |

- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_aerial_route';
    ```

  | id_execution | table_name         | dateload | avro_name                                                                                                | start_execution  | end_execution    | status |
  |--------------|--------------------|----------|----------------------------------------------------------------------------------------------------------|------------------|------------------|--------|
  | 1            | tx_sw_aerial_route | 20200124 | /data/RCI/raw/smallworld/aerial_route/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Aerial_Route.avro | 24/01/2020 11:14 | 24/01/2020 11:15 | 1      |

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_sw_aerial_route'
    and dateload = 20200124
    order by filedate asc;
    ```

  | uuid                                 | rowprocessed | datasetname        | filedate | filename                                                     | sourceid   | dateload | read_count | insert_count | update_count | delete_count |   |
  |--------------------------------------|--------------|--------------------|----------|--------------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|---|
  | 70d38a9c-f1d4-4229-a582-3fd45aeb7bb3 | 121351       | tx_sw_aerial_route | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Aerial Route.csv | smallworld | 20200124 | 121351     | 121351       | 0            | 0            |   |

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 124   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 124
  ```

## <a name="Port"></a>Port

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Port](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_port```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                      |
     |----|----------------------|--------------|---------------------------------|
     | 1  | type                 | string       | Type inferred from 'Signal'     |
     | 2  | description          | string       | Type inferred from '1'          |
     | 3  | servicelevel         | string       | Type inferred from 'Fibre'      |
     | 4  | physicalstatus       | string       | Type inferred from 'In Service' |
     | 5  | connectortype        | string       | Type inferred from 'SC'         |
     | 6  | sourcecrvs           | string       | Type inferred from 'null'       |

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 7  | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 8  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Port.c' |
     | 9  | hash_id              | string       | Type inferred from 'null'                                               |
     | 10 | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 11 | registry_state       | string       | Type inferred from 'null'                                               |
     | 12 | datasetname          | string       | Type inferred from 'tx_sw_port'                                         |
     | 13 | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 14 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

     A continuación se presentan las particiones creadas de la tabla **tx_sw_port**.

     Sentencia: ```show partitions rci_network_db.tx_sw_port```

     | year | month | #Rows | #Files | Size   | Format | Incremental stats | Location                                                                           |
     |------|-------|-------|--------|--------|--------|-------------------|------------------------------------------------------------------------------------|
     | 2019 | 7     | 24    | 1      | 6.53KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/port/year=2019/month=7 |

- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_port';
    ```

    | id_execution | table_name | dateload | avro_name                                                                                | start_execution     | end_execution       | status |
    |--------------|------------|----------|------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
    | 1            | tx_sw_port | 20200124 | /data/RCI/raw/smallworld/port/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Port.avro | 2020-01-24 11:22:09 | 2020-01-24 11:22:53 | 1      |

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_sw_port'
    and dateload = 20200124
    order by filedate asc;
    ```

    | uuid                                 | rowprocessed | datasetname | filedate | filename                                             | sourceid   | dateload | read_count | insert_count | update_count | delete_count |   |
    |--------------------------------------|--------------|-------------|----------|------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|---|
    | e709cbda-d47f-4f9e-99ef-ce4954f9360f | 1632         | tx_sw_port  | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Port.csv | smallworld | 20200124 | 1632       | 1632         | 0            | 0            |   |

## Componentes del procesos de ingestión:

 __Framework de Ingestión Automatizado__

 - Especificar parámetros del proceso kite:

 | Parámetro | Valor | Descripción|
 | ---------- | ---------- | ---------- |
 | parametro_01   | 125   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 125
   ```


## <a name="UndergroundUtilityBox"></a>Underground Utility Box

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Underground Utility Box](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_underground_utility_box```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                               |
     |----|----------------------|--------------|------------------------------------------|
     | 1  | id                   | string       | Type inferred from '4894712882786810000' |
     | 2  | type                 | string       | Type inferred from 'Manhole'             |
     | 3  | label                | string       | Type inferred from '8'                   |
     | 4  | specification        | string       | Type inferred from '2m x 1.2m x 1.2m'    |
     | 5  | constructionstatus   | string       | Type inferred from 'In Service'          |
     | 6  | estadofisico         | string       | Type inferred from 'BUENO'               |
     | 7  | tipodesuelo          | string       | Type inferred from 'ARROYO'              |
     | 8  | medioderutahuella    | string       | Type inferred from 'MINICEPA'            |
     | 9  | estadoderuta         | string       | Type inferred from 'BUENO'               |
     | 10 | identificacion       | string       | Type inferred from 'SIN LOGO'            |
     | 11 | width                | string       | Type inferred from '1820.0 mm'           |
     | 12 | installeddepth       | string       | Type inferred from '1500.0 mm'           |
     | 13 | installedcost        | string       | Type inferred from 'null'                |    

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 14 | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 15 | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Underg' |
     | 16 | hash_id              | string       | Type inferred from 'null'                                               |
     | 17 | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 18 | registry_state       | string       | Type inferred from 'null'                                               |
     | 19 | datasetname          | string       | Type inferred from 'tx_sw_underground_utility_box'                      |
     | 20 | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 21 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_underground_utility_box**.

 Sentencia: ```show partitions rci_network_db.tx_sw_underground_utility_box```

  | year | month | #Rows | #Files | Size    | Format | Incremental stats | Location                                                                                              |
  |------|-------|-------|--------|---------|--------|-------------------|-------------------------------------------------------------------------------------------------------|
  | 2019 | 7     | 220   | 1      | 70.61KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/underground_utility_box/year=2019/month=7 |

- **Ejecuciones**

     En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

     ```
     select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_underground_utility_box';
     ```

     | id_execution | table_name                    | dateload | avro_name                                                                                                                      | start_execution  | end_execution    | status |
     |--------------|-------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------|------------------|------------------|--------|
     | 1            | tx_sw_underground_utility_box | 20200124 | /data/RCI/raw/smallworld/underground_utility_box/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Underground_Utility_Box.avro | 24/01/2020 11:26 | 24/01/2020 11:27 | 1      |

- **Cifras de Control**

     En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

     ```
     select * from rci_network_db.tx_cifras_control
     where datasetname = 'tx_sw_underground_utility_box'
     and dateload = 20191225
     order by filedate asc;
     ```

     | uuid                                 | rowprocessed | datasetname                   | filedate | filename                                                                | sourceid   | dateload | read_count | insert_count | update_count | delete_count |   |
     |--------------------------------------|--------------|-------------------------------|----------|-------------------------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|---|
     | e1010fae-9909-4ce6-8137-b41d02ca0d2a | 1194         | tx_sw_underground_utility_box | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Underground Utility Box.csv | smallworld | 20200124 | 1194       | 1194         | 0            | 0            |   |


## Componentes del procesos de ingestión:

 __Framework de Ingestión Automatizado__

 - Especificar parámetros del proceso kite:

 | Parámetro | Valor | Descripción|
 | ---------- | ---------- | ---------- |
 | parametro_01   | 126   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 126
   ```


## <a name="Anchor"></a>Anchor

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Anchor](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_anchor```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                               |
     |----|----------------------|--------------|------------------------------------------|
     | 1  | id                   | string       | Type inferred from '4894712882786460000' |
     | 2  | type                 | string       | Type inferred from 'Plastic'             |    

     Las siguientes columnas son creadas para la identidad de la fuente:     

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 3  | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 4  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Anchor' |
     | 5  | hash_id              | string       | Type inferred from 'null'                                               |
     | 6  | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 7  | registry_state       | string       | Type inferred from 'null'                                               |
     | 8  | datasetname          | string       | Type inferred from 'tx_sw_anchor'                                       |
     | 9  | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 10 | transaction_status   | string       | Type inferred from 'null'                                               |     

- **Particiones**

   A continuación se presentan las particiones creadas de la tabla **tx_sw_anchor**.

   Sentencia: ```show partitions rci_network_db.tx_sw_anchor```

    | year | month | #Rows | #Files | Size    | Format | Incremental stats | Location                                                                             |
    |------|-------|-------|--------|---------|--------|-------------------|--------------------------------------------------------------------------------------|
    | 2019 | 7     | 432   | 1      | 88.35KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/anchor/year=2019/month=7 |

- **Ejecuciones**

     En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

     ```
     select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_anchor';
     ```

     | id_execution | table_name   | dateload | avro_name                                                                                    | start_execution     | end_execution       | status |
     |--------------|--------------|----------|----------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
     | 1            | tx_sw_anchor | 20200124 | /data/RCI/raw/smallworld/anchor/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Anchor.avro | 2020-01-24 11:29:17 | 2020-01-24 11:30:08 | 1      |

- **Cifras de Control**

     En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

     ```
     select * from rci_network_db.tx_cifras_control
     where datasetname = 'tx_sw_anchor'
     and dateload = 20191225
     order by filedate asc;
     ```

    | uuid                                 | rowprocessed | datasetname  | filedate | filename                                               | sourceid   | dateload | read_count | insert_count | update_count | delete_count |   |
    |--------------------------------------|--------------|--------------|----------|--------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|---|
    | b0e3ccda-c602-4519-b08e-1e1ad12ee341 | 17206        | tx_sw_anchor | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Anchor.csv | smallworld | 20200124 | 17206      | 17206        | 0            | 0            |   |

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 127   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 127
   ```

## <a name="Room"></a>Room

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Room](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_room```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                      |
     |----|----------------------|--------------|---------------------------------|
     | 1  | identifier           | string       | Type inferred from '1'          |
     | 2  | type                 | string       | Type inferred from 'Commercial' |
     | 3  | servicetype          | string       | Type inferred from 'Unknown'    |

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 4  | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 5  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Room.c' |
     | 6  | hash_id              | string       | Type inferred from 'null'                                               |
     | 7  | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 8  | registry_state       | string       | Type inferred from 'null'                                               |
     | 9  | datasetname          | string       | Type inferred from 'tx_sw_room'                                         |
     | 10 | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 11 | transaction_status   | string       | Type inferred from 'null'                                               |

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_room**.

 Sentencia: ```show partitions rci_network_db.tx_sw_room```

  | year | month | #Rows | #Files | Size   | Format | Incremental stats | Location                                                                           |
  |------|-------|-------|--------|--------|--------|-------------------|------------------------------------------------------------------------------------|
  | 2019 | 7     | 6     | 1      | 2.45KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/room/year=2019/month=7 |

- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_room';
    ```

  | id_execution | table_name | dateload | avro_name                                                                                | start_execution     | end_execution       | status |
  |--------------|------------|----------|------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
  | 1            | tx_sw_room | 20200124 | /data/RCI/raw/smallworld/room/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Room.avro | 2020-01-24 11:31:41 | 2020-01-24 11:32:26 | 1      |

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_sw_room'
    and dateload = 20191227
    order by filedate asc;
    ```

  | uuid                                 | rowprocessed | datasetname | filedate | filename                                             | sourceid   | dateload | read_count | insert_count | update_count | delete_count |   |
  |--------------------------------------|--------------|-------------|----------|------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|---|
  | 6e4efa15-d93e-4976-869a-cf35663ce4cb | 88           | tx_sw_room  | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Room.csv | smallworld | 20200124 | 88         | 88           | 0            | 0            |   |

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 128   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 128
   ```

## <a name="Shelf"></a>Shelf

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Shelf](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_shelf```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 1  | description          | string       | Type inferred from 'DIR CUERNAVACA I'                                   |
     | 2  | constructionstatus   | string       | Type inferred from 'In Service'                                         |
     | 3  | nename               | string       | Type inferred from 'null'                                               |
     | 4  | enidname             | string       | Type inferred from 'null'                                               |
     | 5  | accountcode          | string       | Type inferred from 'null'                                               |
     | 6  | installedcost        | string       | Type inferred from 'null'                                               |
     | 7  | dateinstalled        | string       | Type inferred from 'null'                                               |
     | 8  | installername        | string       | Type inferred from 'null'                                               |
     | 9  | firmwareversion      | string       | Type inferred from 'null'                                               |
     | 10 | softwareversion      | string       | Type inferred from 'null'                                               |
     | 11 | barcodenumber        | string       | Type inferred from 'null'                                               |
     | 12 | serialnumber         | string       | Type inferred from 'null'                                               |
     | 13 | acceptancedate       | string       | Type inferred from 'null'                                               |
     | 14 | acceptancename       | string       | Type inferred from 'null'                                               |
     | 15 | multiports           | string       | Type inferred from 'null'                                               |
     | 16 | shortname            | string       | Type inferred from 'DIR CUERNAVACA I'                                   |
     | 17 | mediumname           | string       | Type inferred from 'Shelf(DIR CUERNAVACA I)'                            |
     | 18 | longname             | string       | Type inferred from 'DIR CUERNAVACA I,In Service'                        |
     | 19 | shortdescription     | string       | Type inferred from 'DIR CUERNAVACA I'                                   |
     | 20 | mediumdescription    | string       | Type inferred from 'Shelf : DIR CUERNAVACA I, construction status - In' |
     | 21 | longdescription      | string       | Type inferred from 'Room : 1, HCUE0010 DOMINGO DIEZ 1, DIR CUERNAVACA ' |
     | 22 | specialisation       | string       | Type inferred from 'null'                                               |

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 23 | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 24 | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Shelf.' |
     | 25 | hash_id              | string       | Type inferred from 'null'                                               |
     | 26 | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 27 | registry_state       | string       | Type inferred from 'null'                                               |
     | 28 | datasetname          | string       | Type inferred from 'tx_sw_shelf'                                        |
     | 29 | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 30 | transaction_status   | string       | Type inferred from 'null'                                               |     

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_shelf**.

 Sentencia: ```show partitions rci_network_db.tx_sw_shelf```

  | year | month | #Rows | #Files | Size    | Format | Incremental stats | Location                                                                            |
  |------|-------|-------|--------|---------|--------|-------------------|-------------------------------------------------------------------------------------|
  | 2019 | 7     | 100   | 1      | 43.23KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/shelf/year=2019/month=7 |

- **Ejecuciones**

     En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

     ```
     select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_shelf';
     ```

  | id_execution | table_name  | dateload | avro_name                                                                                  | start_execution  | end_execution    | status |
  |--------------|-------------|----------|--------------------------------------------------------------------------------------------|------------------|------------------|--------|
  | 1            | tx_sw_shelf | 20200124 | /data/RCI/raw/smallworld/shelf/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Shelf.avro | 24/01/2020 11:49 | 24/01/2020 11:50 | 1      |

- **Cifras de Control**

     En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

     ```
     select * from rci_network_db.tx_cifras_control
     where datasetname = 'tx_sw_shelf'
     and dateload = 20200124
     order by filedate asc;
     ```

  | uuid                                 | rowprocessed | datasetname | filedate | filename                                              | sourceid   | dateload | read_count | insert_count | update_count | delete_count |   |
  |--------------------------------------|--------------|-------------|----------|-------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|---|
  | 3f6a7717-d95d-431c-ae36-f6466f79a522 | 136          | tx_sw_shelf | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Shelf.csv | smallworld | 20200124 | 136        | 136          | 0            | 0            |   |

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 129   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 129
   ```


## <a name="Building"></a>Building

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Building](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_building```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                    |
     |----|----------------------|--------------|-----------------------------------------------|
     | 1  | id                   | string       | Type inferred from '4894712882787270000'      |
     | 2  | name                 | string       | Type inferred from 'SITIO EN CLL. 4 PONIENTE' |
     | 3  | type                 | string       | Type inferred from 'MDU'                      |
     | 4  | constructionstatus   | string       | Type inferred from 'In Service'               |

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 5  | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 6  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Buildi' |
     | 7  | hash_id              | string       | Type inferred from 'null'                                               |
     | 8  | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 9  | registry_state       | string       | Type inferred from 'null'                                               |
     | 10 | datasetname          | string       | Type inferred from 'tx_sw_building'                                     |
     | 11 | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 12 | transaction_status   | string       | Type inferred from 'null'                                               |          

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_building**.

 Sentencia: ```show partitions rci_network_db.tx_sw_building```

  | year | month | #Rows | #Files | Size    | Format | Incremental stats | Location                                                                               |
  |------|-------|-------|--------|---------|--------|-------------------|----------------------------------------------------------------------------------------|
  | 2019 | 7     | 387   | 1      | 92.85KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/building/year=2019/month=7 |

- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_building';
    ```

  | id_execution | table_name     | dateload | avro_name                                                                                        | start_execution  | end_execution    | status |
  |--------------|----------------|----------|--------------------------------------------------------------------------------------------------|------------------|------------------|--------|
  | 1            | tx_sw_building | 20200124 | /data/RCI/raw/smallworld/building/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Building.avro | 24/01/2020 11:51 | 24/01/2020 11:52 | 1      |

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_sw_building'
    and dateload = 20200124
    order by filedate asc;
    ```

  | uuid                                 | rowprocessed | datasetname    | filedate | filename                                                 | sourceid   | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|----------------|----------|----------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|
  | b95d822a-7304-4e70-94b7-c54a1b806263 | 16052        | tx_sw_building | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Building.csv | smallworld | 20200124 | 16052      | 16052        | 0            | 0            |

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 130   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 130
   ```

## <a name="StructuralWiringConnectionPo"></a>Structural Wiring Connection Po

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)

## Descripción de la fuentes de datos
- **Descripción**
  [Structural Wiring Connection Po](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Smallworld/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_sw_structural_wiring_connection_po```

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                  |
     |----|----------------------|--------------|-------------------------------------------------------------|
     | 1  | description          | string       | Type inferred from 'Bay(HMEX0243), Number = 1 [Conn.Point]' |
     | 2  | type                 | string       | Type inferred from 'null'                                   |
     | 3  | coaxialcablepins     | string       | Type inferred from 'null'                                   |
     | 4  | sheathpins           | string       | Type inferred from 'null'                                   |
     | 5  | sheathlocpins        | string       | Type inferred from 'null'                                   |
     | 6  | coppercablepins      | string       | Type inferred from 'null'                                   |
     | 7  | powercablepins       | string       | Type inferred from 'null'                                   |

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
     |----|----------------------|--------------|-------------------------------------------------------------------------|
     | 8  | filedate             | bigint       | Type inferred from '20190701'                                           |
     | 9  | filename             | string       | Type inferred from '201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Struct' |
     | 10 | hash_id              | string       | Type inferred from 'null'                                               |
     | 11 | sourceid             | string       | Type inferred from 'smallworld'                                         |
     | 12 | registry_state       | string       | Type inferred from 'null'                                               |
     | 13 | datasetname          | string       | Type inferred from 'tx_sw_structural_wiring_connection_po'              |
     | 14 | timestamp            | bigint       | Type inferred from '20200124'                                           |
     | 15 | transaction_status   | string       | Type inferred from 'null'                                               |       

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_sw_structural_wiring_connection_po**.

 Sentencia: ```show partitions rci_network_db.tx_sw_structural_wiring_connection_po```

  | year | month | #Rows | #Files | Size   | Format | Incremental stats | Location                                                                                                      |
  |------|-------|-------|--------|--------|--------|-------------------|---------------------------------------------------------------------------------------------------------------|
  | 2019 | 7     | 2     | 1      | 2.22KB | AVRO   | false             | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/smallworld/structural_wiring_connection_po/year=2019/month=7 |

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_sw_structural_wiring_connection_po';
   ```

  | id_execution | table_name                            | dateload | avro_name                                                                                                                                      | start_execution  | end_execution    | status |
  |--------------|---------------------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------|------------------|------------------|--------|
  | 1            | tx_sw_structural_wiring_connection_po | 20200124 | /data/RCI/raw/smallworld/structural_wiring_connection_po/data/201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Structural_Wiring_Connection_Po.avro | 24/01/2020 11:56 | 24/01/2020 11:56 | 1      |

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_sw_structural_wiring_connection_po'
   and dateload = 20200124
   order by filedate asc;
   ```

  | uuid                                 | rowprocessed | datasetname                           | filedate | filename                                                                        | sourceid   | dateload | read_count | insert_count | update_count | delete_count |   |
  |--------------------------------------|--------------|---------------------------------------|----------|---------------------------------------------------------------------------------|------------|----------|------------|--------------|--------------|--------------|---|
  | 2ee96d5f-eb55-4b0c-a012-0a8b050b466b | 2            | tx_sw_structural_wiring_connection_po | 20190701 | 201907_ELEMENTOS_CARGADOS_EN_PNI_Julio_2019_Structural Wiring Connection Po.csv | smallworld | 20200124 | 2          | 2            | 0            | 0            |   |

## Componentes del procesos de ingestión:

 __Framework de Ingestión Automatizado__

 - Especificar parámetros del proceso kite:

 | Parámetro | Valor | Descripción|
 | ---------- | ---------- | ---------- |
 | parametro_01   | 131   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 131
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
