![EncabezadoAxity][imgEncabezado]


# Documentación Data Ingestion para la fuente ATT **Segregación Almacén**

## Descripcion del `FTP`

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

## Descripción de la fuente de datos
- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda).

- **Diccionario de datos:**

A continuación se detalla el estado de la tabla de Hive `rci_network_db.tx_almacen_inventory`, en la cual se depositan los datos:

  | Id  | Nombre de la Columna                    | Tipo de Dato | Comentario                                                              |
  |-----|-----------------------------------------|--------------|-------------------------------------------------------------------------|
  | 1   | id                                      | string       | Type inferred from '22'                                                 |
  | 2   | qr                                      | string       | Type inferred from '2PX1S19-001051'                                     |
  | 3   | org                                     | string       | Type inferred from '2PX'                                                |
  | 4   | sub_inv                                 | string       | Type inferred from 'NUEVOS'                                             |
  | 5   | almacen                                 | string       | Type inferred from 'DHL Tepotzotlan'                                    |
  | 6   | articulo                                | string       | Type inferred from 'W.9044002'                                          |
  | 7   | descripcion                             | string       | Type inferred from 'MICROWAVE ANTENNA  1.2M  WITH SUPPORT HARDWARE  DU' |
  | 8   | udm                                     | string       | Type inferred from 'PZA'                                                |
  | 9   | lpn_nuevo                               | string       | Type inferred from 'ANC2018073000010'                                   |
  | 10  | ubicacion_nueva                         | string       | Type inferred from 'FR002A'                                             |
  | 11  | estado_fisico_usadonuevo                | string       | Type inferred from 'NUEVO'                                              |
  | 12  | cantidad                                | string       | Type inferred from '1.0'                                                |
  | 13  | tipo_de_control                         | string       | Type inferred from 'S/L'                                                |
  | 14  | pasillo                                 | string       | Type inferred from 'R'                                                  |
  | 15  | nivel                                   | string       | Type inferred from 'A'                                                  |
  | 16  | parnon                                  | string       | Type inferred from 'PAR'                                                |
  | 17  | tipo_de_articulo                        | string       | Type inferred from 'W'                                                  |
  | 18  | fecha                                   | string       | Type inferred from '20/03/2019'                                         |
  | 19  | serie                                   | string       | Type inferred from '21524311663AG7004232'                               |
  | 20  | etiqueta                                | string       | Type inferred from '00895089'                                           |
  | 21  | bolsa                                   | string       | Type inferred from 'null'                                               |
  | 22  | estatus_proyecto                        | string       | Type inferred from 'Con Proyecto'                                       |
  | 23  | con_po__sin_po                          | string       | Type inferred from 'Con PO'                                             |
  | 24  | po                                      | string       | Type inferred from '1620161442'                                         |
  | 25  | proveedor                               | string       | Type inferred from 'En Mapeo de Proveedor'                              |
  | 26  | proyecto                                | string       | Type inferred from 'MW For Sites Overlay 2016'                          |
  | 27  | proyectos_implementacion_20192020       | string       | Type inferred from 'null'                                               |
  | 28  | area_usuaria                            | string       | Type inferred from 'En Mapeo de Area Usuaria'                           |
  | 29  | usuario                                 | string       | Type inferred from 'REYBEL RODRIGUEZ'                                   |
  | 30  | avp3                                    | string       | Type inferred from 'NICOLE RODRIGUEZ'                                   |
  | 31  | proyecto_anteriormente_asignado         | string       | Type inferred from 'null'                                               |
  | 32  | comentarios_de_reasignacion_de_proyecto | string       | Type inferred from 'null'                                               |
  | 33  | id_pmo                                  | string       | Type inferred from 'Sin ID PMO asociado'                                |
  | 34  | estado_del_proyecto_pmo                 | string       | Type inferred from 'No Aplica'                                          |
  | 35  | control_de_cambios                      | string       | Type inferred from 'No Actualizado Perla O. / MW'                       |
  | 36  | fecha_cambio                            | string       | Type inferred from '16/05/2019'                                         |
  | 37  | control_de_prestamos                    | string       | Type inferred from 'null'                                               |
  | 38  | prestamo_autorizado_por                 | string       | Type inferred from 'null'                                               |
  | 39  | dias_sin_movimiento                     | string       | Type inferred from '>60'                                                |
  | 40  | meses                                   | string       | Type inferred from '3-Meses'                                            |
  | 41  | mes                                     | string       | Type inferred from '3.0'                                                |
  | 42  | lm                                      | string       | Type inferred from 'NO LENTO MOVIMIENTO'                                |
  | 43  | segregacion                             | string       | Type inferred from 'null'                                               |
  | 44  | marca                                   | string       | Type inferred from 'null'                                               |
  | 45  | num_parte                               | string       | Type inferred from 'null'                                               |
  | 46  | modeloversion                           | string       | Type inferred from 'null'                                               |
  | 47  | version_e                               | string       | Type inferred from 'null'                                               |
  | 48  | version_d                               | string       | Type inferred from 'null'                                               |
  | 49  | fanc                                    | string       | Type inferred from 'null'                                               |
  | 50  | fand                                    | string       | Type inferred from 'null'                                               |
  | 51  | fane                                    | string       | Type inferred from 'null'                                               |
  | 52  | fan_f                                   | string       | Type inferred from 'null'                                               |
  | 53  | mbts                                    | string       | Type inferred from 'null'                                               |
  | 54  | ubbpe4                                  | string       | Type inferred from 'null'                                               |
  | 55  | ubbpd6                                  | string       | Type inferred from 'null'                                               |
  | 56  | upeue                                   | string       | Type inferred from 'null'                                               |
  | 57  | upeuc                                   | string       | Type inferred from 'null'                                               |
  | 58  | upeud                                   | string       | Type inferred from 'null'                                               |
  | 59  | ueiu                                    | string       | Type inferred from 'null'                                               |
  | 60  | umptb1                                  | string       | Type inferred from 'null'                                               |
  | 61  | umptb2                                  | string       | Type inferred from 'null'                                               |
  | 62  | wbbp                                    | string       | Type inferred from 'null'                                               |
  | 63  | wbbpf4                                  | string       | Type inferred from 'null'                                               |
  | 64  | wmpt                                    | string       | Type inferred from 'null'                                               |
  | 65  | dbs_site_auxiliary_material_kit         | string       | Type inferred from 'null'                                               |
  | 66  | clave_de_sitio                          | string       | Type inferred from 'null'                                               |
  | 67  | nombre_de_sitio                         | string       | Type inferred from 'null'                                               |
  | 68  | fecha_de_asignacion                     | string       | Type inferred from 'null'                                               |
  | 69  | fecha_instalacion                       | string       | Type inferred from 'null'                                               |
  | 70  | nueva_recepcion_entradas                | string       | Type inferred from 'null'                                               |
  | 71  | agregados_wlog                          | string       | Type inferred from 'null'                                               |
  | 72  | num                                     | string       | Type inferred from '22'                                                 |
  | 73  | aplica_revision_en_cip_sino             | string       | Type inferred from 'SI'                                                 |
  | 74  | pend_inf                                | string       | Type inferred from 'OK'                                                 |
  | 75  | encontrado_cip_sino                     | string       | Type inferred from 'SI'                                                 |
  | 76  | capexopexcomp                           | string       | Type inferred from 'CAPEX'                                              |
  | 77  | activo                                  | string       | Type inferred from '2840187'                                            |
  | 78  | nombre_proyecto                         | string       | Type inferred from 'MW For Sites Overlay 2016'                          |
  | 79  | orden_de_compra                         | string       | Type inferred from '1620161442'                                         |
  | 80  | avp_cip                                 | string       | Type inferred from 'HECTOR VAZQUEZ'                                     |
  | 81  | tipo_de_ubicacion_resum                 | string       | Type inferred from 'Warehouse'                                          |
  | 82  | mxn                                     | string       | Type inferred from 'null'                                               |
  | 83  | usd                                     | string       | Type inferred from '670.61649071338559'                                 |
  | 84  | encontrado_por                          | string       | Type inferred from 'COD-SER-ETI'                                        |
  | 85  | obsoleto                                | string       | Type inferred from 'null'                                               |
  | 86  | cip_lm_encontrado_por                   | string       | Type inferred from 'ACTIVO-COD'                                         |
  | 87  | cip_lm_sep2019                          | string       | Type inferred from 'CIP LM'                                             |
  | 88  | usd_sep19                               | string       | Type inferred from '667.7504461461715'                                  |
  | 89  | nombre_proyecto_1                       | string       | Type inferred from 'MW For Sites Overlay 2016'                          |
  | 90  | mxn_1                                   | string       | Type inferred from '12983.94'                                           |
  | 91  | usd_1                                   | string       | Type inferred from '681.15688084945657'                                 |
  | 92  | tipo_de_ubicacion_resum_1               | string       | Type inferred from 'Warehouse'                                          |
  | 93  | orden_de_compra_1                       | string       | Type inferred from '1620161442.0'                                       |
  | 94  | proveedor_1                             | string       | Type inferred from 'HUAWEI TECHNOLOGIES DE MEXICO SA DE CV'             |
  | 95  | numero_etiqueta                         | string       | Type inferred from '00895089'                                           |
  | 96  | numero_serie                            | string       | Type inferred from '21524311663AG7004232'                               |
  | 97  | area_ok                                 | string       | Type inferred from 'Tx Eng.'                                            |
  | 98  | categoria_budget1_jc                    | string       | Type inferred from 'Capacity Expansion MW'                              |
  | 99  | categoria_budget2_jc                    | string       | Type inferred from 'MW For Overlay'                                     |
  | 100 | idpm                                    | string       | Type inferred from '2018-PRG-SITIOS-013'                                |
  | 101 | pm                                      | string       | Type inferred from 'Carlos Torrealba'                                   |
  | 102 | project_pm                              | string       | Type inferred from '121 Mercados Huawei'                                |
  | 103 | solicitante                             | string       | Type inferred from 'MIGUEL VALTIERRA'                                   |
  | 104 | director                                | string       | Type inferred from 'NICOLE RODRIGUEZ'                                   |
  | 105 | responsable                             | string       | Type inferred from 'REYBEL RODRIGUEZ'                                   |
  | 106 | area_homologada                         | string       | Type inferred from 'N. ENGINEERING'                                     |
  | 107 | avp_2                                   | string       | Type inferred from 'HECTOR VAZQUEZ'                                     |
  | 108 | encontrado_en_almacen                   | string       | Type inferred from 'Encontrado en almacen'                              |
  | 109 | encontrado_en_salidas                   | string       | Type inferred from 'No encontrado en SalidasA'                          |
  | 110 | id_almacen                              | string       | Type inferred from '22'                                                 |
  | 111 | revision_finanza                        | string       | Type inferred from 'null'                                               |
  | 112 | idpmo                                   | string       | Type inferred from 'Sin IDPMO'                                          |
  | 113 | con_id__sin_id_pmo                      | string       | Type inferred from 'Sin IDPMO'                                          |
  | 114 | usd_octubre                             | string       | Type inferred from 'null'                                               |
  | 115 | comentario                              | string       | Type inferred from 'null'                                               |

  Las siguientes columnas son datos de control que se insertan al momento de la ingesta para identificar a la fuente, el archivo original no las incluye:

  | Id  | Nombre de la Columna | Tipo de Dato | Comentario                                                              |
  |-----|----------------------|--------------|-------------------------------------------------------------------------|
  | 116 | filedate             | bigint       | Type inferred from '20191219'                                           |
  | 117 | filename             | string       | Type inferred from '20191219_Inventario_Proyectos_Revision_19-DIC-19_D' |
  | 118 | hash_id              | string       | Type inferred from 'null'                                               |
  | 119 | sourceid             | string       | Type inferred from 'Almacen'                                            |
  | 120 | registry_state       | string       | Type inferred from 'null'                                               |
  | 121 | datasetname          | string       | Type inferred from 'tx_almacen_inventory'                               |
  | 122 | timestamp            | bigint       | Type inferred from '20200131'                                           |
  | 123 | transaction_status   | string       | Type inferred from 'null'                                               |

  Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda).

- **Particiones**

    Las particiones de la tabla **rci_network_db.tx_almacen_inventory** se generan de forma mensual usando el campo de auditoría **filedate**. A continuación se presentan las particiones creadas en la tabla:

    Sentencia `show partitions rci_network_db.tx_almacen_inventory`:

  | year | month | #Rows   | #Files | Size   | Format | Incremental | stats Location                                                                   |
  |------|-------|---------|--------|--------|--------|-------------|----------------------------------------------------------------------------------|
  | 2019 | 8     | 2105111 | 9      | 1.31GB | AVRO   | false       | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/sa/inventory/year=2019/month=8  |
  | 2019 | 9     | 5465298 | 14     | 3.06GB | AVRO   | false       | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/sa/inventory/year=2019/month=9  |
  | 2019 | 10    | 7052291 | 18     | 3.97GB | AVRO   | false       | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/sa/inventory/year=2019/month=10 |
  | 2019 | 11    | 2000849 | 9      | 1.16GB | AVRO   | false       | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/sa/inventory/year=2019/month=11 |
  | 2019 | 12    | 1847312 | 5      | 1.36GB | AVRO   | false       | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/sa/inventory/year=2019/month=12 |


- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:
  ```
  select * from rci_metadata_db.tx_rci_executions
  where table_name = 'tx_almacen_inventory'
  order by filedate;
  ```
  | id_execution | table_name           | dateload | avro_name                                                                                   | start_execution     | end_execution       | status |
  |--------------|----------------------|----------|---------------------------------------------------------------------------------------------|---------------------|---------------------|--------|
  | 1            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190903_Inventario_Proyectos_Revision_03-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 17:23:34 | 2020-01-30 17:27:32 | 1      |
  | 2            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190904_Inventario_Proyectos_Revision_04-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 17:27:54 | 2020-01-30 17:32:03 | 1      |
  | 3            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190905_Inventario_Proyectos_Revision_05-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 17:32:26 | 2020-01-30 17:36:24 | 1      |
  | 4            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190906_Inventario_Proyectos_Revision_06-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 17:36:47 | 2020-01-30 17:40:43 | 1      |
  | 5            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190909_Inventario_Proyectos_Revision_09-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 17:41:06 | 2020-01-30 17:44:56 | 1      |
  | 6            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190910_Inventario_Proyectos_Revision_10-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 17:45:20 | 2020-01-30 17:49:23 | 1      |
  | 7            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190911_Inventario_Proyectos_Revision_11-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 17:49:46 | 2020-01-30 17:53:44 | 1      |
  | 8            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190912_Inventario_Proyectos_Revision_12-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 17:54:07 | 2020-01-30 17:58:10 | 1      |
  | 9            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190913_Inventario_Proyectos_Revision_13-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 17:58:34 | 2020-01-30 18:02:26 | 1      |
  | 10           | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190917_Inventario_Proyectos_Revision_17-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 18:02:49 | 2020-01-30 18:07:05 | 1      |
  | 11           | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190918_Inventario_Proyectos_Revision_18-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 18:07:28 | 2020-01-30 18:11:32 | 1      |
  | 12           | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190919_Inventario_Proyectos_Revision_19-SEP-19_V1_LM_Detalle.avro   | 2020-01-30 18:11:55 | 2020-01-30 18:15:50 | 1      |
  | 13           | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190924_Inventario_Proyectos_Revision_24-SEP-19_V1_LM_2_Detalle.avro | 2020-01-30 18:16:12 | 2020-01-30 18:20:25 | 1      |
  | 14           | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190926_Inventario_Proyectos_Revision_26-SEP-19_V1_LM_2_Detalle.avro | 2020-01-30 18:20:51 | 2020-01-30 18:25:10 | 1      |
  | 15           | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20190930_Inventario_Proyectos_Revision_30-SEP-19_V1_LM_2_Detalle.avro | 2020-01-30 18:25:35 | 2020-01-30 18:29:47 | 1      |
  | 16            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20191202_Inventario_Proyectos_Revision_02-DIC-19_Detalle.avro         | 2020-01-30 22:44:22 | 2020-01-30 22:49:20 | 1      |
  | 17            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20191203_Inventario_Proyectos_Revision_03-DIC-19_Detalle.avro         | 2020-01-30 22:49:44 | 2020-01-30 22:54:49 | 1      |
  | 18            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20191205_Inventario_Proyectos_Revision_05-DIC-19_Detalle.avro         | 2020-01-30 22:55:12 | 2020-01-30 22:59:58 | 1      |
  | 19            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20191209_Inventario_Proyectos_Revision_09-DIC-19_Detalle.avro         | 2020-01-30 23:00:21 | 2020-01-30 23:04:49 | 1      |
  | 20            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20191210_Inventario_Proyectos_Revision_10-DIC-19_Detalle.avro         | 2020-01-30 23:05:12 | 2020-01-30 23:09:56 | 1      |
  | 21            | tx_almacen_inventory | 20200130 | /data/RCI/raw/sa/data/20191219_Inventario_Proyectos_Revision_19-DIC-19_Detalle.avro         | 2020-01-30 23:10:19 | 2020-01-30 23:14:40 | 1      |


- **Cifras de control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_almacen_inventory'
  and dateload = 20191224
  order by filedate asc;
  ```

  | uuid                                 | rowprocessed | datasetname          | filedate | filename                                                               | sourceid | dateload | read_count | insert_count | update_count | delete_count |
  |--------------------------------------|--------------|----------------------|----------|------------------------------------------------------------------------|----------|----------|------------|--------------|--------------|--------------|
  | 42507e79-d4c5-4c23-9f02-5bca227bbcbb | 129632       | tx_almacen_inventory | 20190812 | 20190812_Inventario_Proyectos_Revision_12-AGO-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 129632     | 129632       | 0            | 0            |
  | dff32a36-7e3b-4327-948e-dcfcc4696ed2 | 130038       | tx_almacen_inventory | 20190813 | 20190813_Inventario_Proyectos_Revision_13-AGO-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 130038     | 130038       | 0            | 0            |
  | edeb6cf8-6c30-4c26-bafc-1262294ea569 | 128724       | tx_almacen_inventory | 20190815 | 20190815_Inventario_Proyectos_Revision_15-AGO-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 128724     | 128724       | 0            | 0            |
  | a14db112-99db-4dc5-b9cb-0fe83147fe01 | 128723       | tx_almacen_inventory | 20190816 | 20190816_Inventario_Proyectos_Revision_16-AGO-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 128723     | 128723       | 0            | 0            |
  | ba8222a0-b440-4e29-b76e-2d407ecdb4e6 | 129204       | tx_almacen_inventory | 20190819 | 20190819_Inventario_Proyectos_Revision_19-AGO-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 129204     | 129204       | 0            | 0            |
  | 5234b56a-3e47-4f51-a42e-732b0966b009 | 129094       | tx_almacen_inventory | 20190820 | 20190820_Inventario_Proyectos_Revision_20-AGO-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 129094     | 129094       | 0            | 0            |
  | cb73e6e5-f620-4837-b874-13c6550955e4 | 129239       | tx_almacen_inventory | 20190821 | 20190821_Inventario_Proyectos_Revision_21-AGO-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 129239     | 129239       | 0            | 0            |
  | 29eccee0-03b0-4420-9b14-a3ce0752f7a3 | 128823       | tx_almacen_inventory | 20190822 | 20190822_Inventario_Proyectos_Revision_22-AGO-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 128823     | 128823       | 0            | 0            |
  | c312b61e-26e8-4636-b5d2-f917cb36fca1 | 348537       | tx_almacen_inventory | 20190826 | 20190826_Inventario_Proyectos_Revision_26-AGO-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 348537     | 348537       | 0            | 0            |
  | 6f39e1e8-2eb1-4307-8bfd-22d735694536 | 361016       | tx_almacen_inventory | 20190828 | 20190828_Inventario_Proyectos_Revision_28-AGO-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 361016     | 361016       | 0            | 0            |
  | a05e8b89-40c6-46e5-ba33-cadc085142f1 | 362081       | tx_almacen_inventory | 20190829 | 20190829_Inventario_Proyectos_Revision_29-AGO-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 362081     | 362081       | 0            | 0            |
  | 6fb8142e-c2e7-4565-9d4c-7e651eb717b4 | 362951       | tx_almacen_inventory | 20190903 | 20190903_Inventario_Proyectos_Revision_03-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 362951     | 362951       | 0            | 0            |
  | 787d6208-ddf2-4d6d-9f26-c2a852f94b7b | 362685       | tx_almacen_inventory | 20190904 | 20190904_Inventario_Proyectos_Revision_04-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 362685     | 362685       | 0            | 0            |
  | 8c263de0-a5d2-4169-849a-11101bbbe5e2 | 363130       | tx_almacen_inventory | 20190905 | 20190905_Inventario_Proyectos_Revision_05-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 363130     | 363130       | 0            | 0            |
  | 37ab6a05-2c96-47ac-ab7e-d92b6eacfb0b | 349788       | tx_almacen_inventory | 20190906 | 20190906_Inventario_Proyectos_Revision_06-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 349788     | 349788       | 0            | 0            |
  | f1413e16-7dbb-4313-b3ac-19eb0f0a3743 | 349258       | tx_almacen_inventory | 20190909 | 20190909_Inventario_Proyectos_Revision_09-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 349258     | 349258       | 0            | 0            |
  | a2b82937-dfa8-40e0-beb9-680f74561c19 | 348817       | tx_almacen_inventory | 20190910 | 20190910_Inventario_Proyectos_Revision_10-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 348817     | 348817       | 0            | 0            |
  | 0481704f-6b58-4bbd-8d12-ee9b1c314087 | 363647       | tx_almacen_inventory | 20190911 | 20190911_Inventario_Proyectos_Revision_11-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 363647     | 363647       | 0            | 0            |
  | 30e6f994-24e7-41ca-966b-c31cf639ffb1 | 366981       | tx_almacen_inventory | 20190912 | 20190912_Inventario_Proyectos_Revision_12-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 366981     | 366981       | 0            | 0            |
  | 94834049-a851-48b0-824d-4fb9bc0fd555 | 366756       | tx_almacen_inventory | 20190913 | 20190913_Inventario_Proyectos_Revision_13-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 366756     | 366756       | 0            | 0            |
  | ff847c23-7033-4910-bb91-71779c7ca50e | 382716       | tx_almacen_inventory | 20190917 | 20190917_Inventario_Proyectos_Revision_17-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 382716     | 382716       | 0            | 0            |
  | e8d0d07a-c57d-4675-a886-377b71955b12 | 370154       | tx_almacen_inventory | 20190918 | 20190918_Inventario_Proyectos_Revision_18-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 370154     | 370154       | 0            | 0            |
  | 5031acaf-38bf-4ea7-8927-9f3f9780d863 | 356196       | tx_almacen_inventory | 20190919 | 20190919_Inventario_Proyectos_Revision_19-SEP-19_V1_LM_Detalle.csv     | Almacen  | 20200130 | 356196     | 356196       | 0            | 0            |
  | 46a9e572-bdb2-4d68-b56f-f85f631507e4 | 372563       | tx_almacen_inventory | 20190924 | 20190924_Inventario_Proyectos_Revision_24-SEP-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 372563     | 372563       | 0            | 0            |
  | 3f0231f5-c2da-481d-ac64-5f42f7f093af | 378343       | tx_almacen_inventory | 20190926 | 20190926_Inventario_Proyectos_Revision_26-SEP-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 378343     | 378343       | 0            | 0            |
  | 4173e8b2-8a44-47db-8de7-da7c3565875e | 371316       | tx_almacen_inventory | 20190930 | 20190930_Inventario_Proyectos_Revision_30-SEP-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 371316     | 371316       | 0            | 0            |
  | 3fb2f0e8-b72a-4901-b797-41d55bd7eb7e | 370459       | tx_almacen_inventory | 20191001 | 20191001_Inventario_Proyectos_Revision_01-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 370459     | 370459       | 0            | 0            |
  | 55d6c81f-904e-4d15-ac3b-fb63174aff46 | 371962       | tx_almacen_inventory | 20191002 | 20191002_Inventario_Proyectos_Revision_02-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 371962     | 371962       | 0            | 0            |
  | b446771f-9842-43ac-99bf-fa17cf65ebf3 | 370738       | tx_almacen_inventory | 20191003 | 20191003_Inventario_Proyectos_Revision_03-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 370738     | 370738       | 0            | 0            |
  | 703051dd-cb34-43ff-85bd-bbd21442a316 | 372289       | tx_almacen_inventory | 20191004 | 20191004_Inventario_Proyectos_Revision_04-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 372289     | 372289       | 0            | 0            |
  | d73a0649-31b3-4814-9be1-c5d15cdb6098 | 373436       | tx_almacen_inventory | 20191007 | 20191007_Inventario_Proyectos_Revision_07-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 373436     | 373436       | 0            | 0            |
  | ba553ea0-6235-40bb-bbdb-20568110ea91 | 373183       | tx_almacen_inventory | 20191008 | 20191008_Inventario_Proyectos_Revision_08-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 373183     | 373183       | 0            | 0            |
  | d990aa2b-2478-411a-88d4-57c1f3811eeb | 373147       | tx_almacen_inventory | 20191009 | 20191009_Inventario_Proyectos_Revision_09-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 373147     | 373147       | 0            | 0            |
  | ad643cc4-824f-4f3d-8c72-c8ed49e740c6 | 372007       | tx_almacen_inventory | 20191010 | 20191010_Inventario_Proyectos_Revision_10-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 372007     | 372007       | 0            | 0            |
  | b0f4eb3e-b118-41a0-ae75-adfa5321c12c | 360890       | tx_almacen_inventory | 20191014 | 20191014_Inventario_Proyectos_Revision_14-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 360890     | 360890       | 0            | 0            |
  | 40123d67-57f2-4f08-a9e5-1184a855b268 | 341532       | tx_almacen_inventory | 20191015 | 20191015_Inventario_Proyectos_Revision_15-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 341532     | 341532       | 0            | 0            |
  | 22fe9104-b96c-4277-a20a-b94892f62ec1 | 346702       | tx_almacen_inventory | 20191016 | 20191016_Inventario_Proyectos_Revision_16-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 346702     | 346702       | 0            | 0            |
  | c55f4f56-db21-4988-8b2b-fb94e33350c3 | 342577       | tx_almacen_inventory | 20191017 | 20191017_Inventario_Proyectos_Revision_17-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 342577     | 342577       | 0            | 0            |
  | b9b450a2-7676-4569-b03c-a7dc77198ec0 | 337404       | tx_almacen_inventory | 20191018 | 20191018_Inventario_Proyectos_Revision_18-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 337404     | 337404       | 0            | 0            |
  | 480bf5e2-2ff6-4a54-b044-c9efdb2ee8e6 | 333988       | tx_almacen_inventory | 20191021 | 20191021_Inventario_Proyectos_Revision_21-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 333988     | 333988       | 0            | 0            |
  | 65e421af-a3d1-41a8-a957-3eb2b7471071 | 335323       | tx_almacen_inventory | 20191022 | 20191022_Inventario_Proyectos_Revision_22-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 335323     | 335323       | 0            | 0            |
  | 52e05be9-f58e-42ba-b367-900b81c1fbac | 334532       | tx_almacen_inventory | 20191023 | 20191023_Inventario_Proyectos_Revision_23-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 334532     | 334532       | 0            | 0            |
  | 4a3ec37b-4c93-4c5a-a058-e106c2eb4d1c | 336752       | tx_almacen_inventory | 20191024 | 20191024_Inventario_Proyectos_Revision_24-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 336752     | 336752       | 0            | 0            |
  | 4edea776-43ce-4847-a2ff-76c81f4a7943 | 334609       | tx_almacen_inventory | 20191028 | 20191028_Inventario_Proyectos_Revision_28-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 334609     | 334609       | 0            | 0            |
  | 670a88ab-620c-4f03-8e40-a7ed2b0251fa | 335568       | tx_almacen_inventory | 20191029 | 20191029_Inventario_Proyectos_Revision_29-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 335568     | 335568       | 0            | 0            |
  | 4f330e01-8a09-414f-a959-54865f8f2355 | 335193       | tx_almacen_inventory | 20191030 | 20191030_Inventario_Proyectos_Revision_30-OCT-19_V1_LM_(2)_Detalle.csv | Almacen  | 20200130 | 335193     | 335193       | 0            | 0            |
  | 45fd0141-03d6-44fb-8315-019219bfac73 | 334752       | tx_almacen_inventory | 20191101 | 20191101_Inventario_Proyectos_Revision_01-NOV-19_V1_LM_2_Detalle.csv   | Almacen  | 20200131 | 334752     | 334752       | 0            | 0            |
  | 652bd53f-2d38-4754-b00c-6fd8a955fde0 | 333822       | tx_almacen_inventory | 20191104 | 20191104_Inventario_Proyectos_Revision_04-NOV-19_V1_LM_2_Detalle.csv   | Almacen  | 20200131 | 333822     | 333822       | 0            | 0            |
  | cdfe0086-6aff-42f6-bdeb-462ce6ba6586 | 333995       | tx_almacen_inventory | 20191105 | 20191105_Inventario_Proyectos_Revision_05-NOV-19_V1_LM_2_Detalle.csv   | Almacen  | 20200131 | 333995     | 333995       | 0            | 0            |
  | 19b3222b-13af-4c14-bfee-ceae159ac6db | 333614       | tx_almacen_inventory | 20191106 | 20191106_Inventario_Proyectos_Revision_06-NOV-19_V1_LM_2_Detalle.csv   | Almacen  | 20200131 | 333614     | 333614       | 0            | 0            |
  | f5aad72a-8c97-4651-98a7-b102b12ade43 | 332407       | tx_almacen_inventory | 20191114 | 20191114_Inventario_Proyectos_Revision_14-NOV-19_Detalle.csv           | Almacen  | 20200131 | 332407     | 332407       | 0            | 0            |
  | b44ab574-2eef-4661-98e2-f56b7c7da173 | 332259       | tx_almacen_inventory | 20191119 | 20191119_Inventario_Proyectos_Revision_19-NOV-19_Detalle.csv           | Almacen  | 20200131 | 332259     | 332259       | 0            | 0            |
  | b724e4a0-811e-4933-9e9d-2db768fc1d3b | 354714       | tx_almacen_inventory | 20191202 | 20191202_Inventario_Proyectos_Revision_02-DIC-19_Detalle.csv           | Almacen  | 20200131 | 354714     | 354714       | 0            | 0            |
  | 6c3d74e9-ff47-4112-ba2c-148cc941a4d6 | 354224       | tx_almacen_inventory | 20191203 | 20191203_Inventario_Proyectos_Revision_03-DIC-19_Detalle.csv           | Almacen  | 20200131 | 354224     | 354224       | 0            | 0            |
  | 48ca4128-e491-4174-846e-308e2be265ee | 353640       | tx_almacen_inventory | 20191205 | 20191205_Inventario_Proyectos_Revision_05-DIC-19_Detalle.csv           | Almacen  | 20200131 | 353640     | 353640       | 0            | 0            |
  | a8513e1b-6608-4bbc-ad6f-94e48e987e5c | 311743       | tx_almacen_inventory | 20191209 | 20191209_Inventario_Proyectos_Revision_09-DIC-19_Detalle.csv           | Almacen  | 20200131 | 311743     | 311743       | 0            | 0            |
  | 8db08978-5de5-4ee9-80f1-3860881dd237 | 306167       | tx_almacen_inventory | 20191210 | 20191210_Inventario_Proyectos_Revision_10-DIC-19_Detalle.csv           | Almacen  | 20200131 | 306167     | 306167       | 0            | 0            |
  | 553b47de-edb1-4899-b638-7f1d06b36c8c | 281737       | tx_almacen_inventory | 20191219 | 20191219_Inventario_Proyectos_Revision_19-DIC-19_Detalle.csv           | Almacen  | 20200131 | 281737     | 281737       | 0            | 0            |


## Componentes del procesos de ingestion:

__1. Ingestion y Serialización via NiFi__

  Los datos son ingestados al Data Lake usando el flujo de NiFi llamado **ALMACEN (Inventario, CIP, Proyectos)**:

  ![Activo Fijo NiFi General View][img3]
  Pipeline General __Segregación Almacén__

  Debido a que la fuente es un archivo de hoja de cálculo `.xlsx` se realiza un tratamiento de los datos para convertir los registros a un formato estándar separado por pipes y con todos los valores citados con doble comillas; este proceso se realiza con un procesador `ConvertExceltoCSVProcessor`:

  ![Activo Fijo NiFi Detail View][img4]
  Pipeline Detalle __Segregación Almacén__

  El procesador `ConvertExceltoCSVProcessor` hace referencia a una pestaña del archivo llamada `Detalle`, si esta llegase a cambiar de nombre será necesario hacer el cambio en la configuración del procesador.

__2. Aplicación de Reglas de Estandarización del Esquema `Kite`__

  Las siguientes reglas se aplicarón para estandarizar el esquema de los datos que se genera al convertir los datos al formato Avro:

  - Eliminado de caracteres especiales en el encabezado del archivo inestado.

<<<<<<< HEAD
| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_00   | 3   | Valor que identifica a la fuente en  la documentación de Kite: [AX_IM_FrameworkIngestion_CommandExecutionV2.xlsx](http://10.103.133.122/app/owncloud/f/14480776).  |
=======
  ```
  ${'$1':replace("-",""):replace("[",""):replace("]",""):replace(" ","_"):replace("ñ","n"):replace("#","Num"):replace("Í","I"):replace("(",""):replace(")","")}$2
  ```
>>>>>>> f17ccfc48c11b46af8c37c2b5c513a6316537378

  - Remplazo de espacios por guiones bajos ( _ ) en el encabezado del archivo ingestado.

  ```
  ${'$1':replace(" ","_")}$2
  ```

__3. Framework de Ingestión Automatizado__

<<<<<<< HEAD
Debido a la naturaleza de los datos la fuente no requiere hacer cálculo de incrementales, por lo tanto, cada ingestión se inserta de forma completa. Este proceso se realiza mediante un script de [Spark](../Globales/SparkAxity), el cual se invoca mediante una linea de ejecución que necesita 15 parámetros:
=======
  - La generación del esquema con Kite se invoca a través del siguiente comando:
>>>>>>> f17ccfc48c11b46af8c37c2b5c513a6316537378

  ```
  ./rci_ingesta_generacion_avro.sh {parametro0}
  ```

  El comando necesita un parámetro para funcionar, el cual se especifica en la siguiente tabla:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_00   | 3   | Valor que identifica a la fuente en  la documentación de [Kite](https://intellego365.sharepoint.com/sites/ATT-InventoryManagement/_layouts/15/Doc.aspx?sourcedoc={09dc3f26-ba48-4bc5-96a0-6c64157a5d82}&action=embedview&wdAllowInteractivity=False&wdHideGridlines=True&wdHideHeaders=True&wdDownloadButton=True&wdInConfigurator=True).  |

  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 3
  ```

## Referencias al Framework de Ingestion

- [Framework de Ingestion](../Globales/)

## Codigo Fuente Local

- [Codigo NiFi - NFR](NFR/)

## Codigo Fuente Globales

- [Codigo NiFi](../Globales/NIFICustomProcessorXLSX)
- [Codigo Spark](../Globales/SparkAxity)
- [Codigo Kite](../Globales/attdlkrci)



[img1]: images/inventario-nifi-03.png "Logo Axity"
[img2]: ../Globales/ArquitecturaFrameworkIngestion/images/att.png "Logo AT&T"
[img3]: images/inventario-nifi-01.png "Segregación Almacén NiFi Detail View"
[img4]: images/inventario-nifi-02.png "Segregación Almacén NiFi Detail View"
[imgEncabezado]:../Globales/ArquitecturaFrameworkIngestion/images/encabezado.png ""
