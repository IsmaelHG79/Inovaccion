<<<<<<< HEAD
![EncabezadoAxity][img1]

# Documentación Data Ingestion para la fuente ATT **Activo Fijo**

## Descripcion del `FTP`

El diseño del Data Lake se detalla en el documento [AX_IM_RCI_DataLakeGuide_ATT_v1.3.xlsx](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

## Descripción de la fuente de datos

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_fixed_asset`, en la cual se depositan los datos:

| col_name           | data_type | comment                                                         |
|--------------------|-----------|-----------------------------------------------------------------|
| activo             | string    | Type inferred from '1004414'                                    |
| units_assigned     | string    | Type inferred from '1.00'                                       |
| location           | string    | Type inferred from 'ST2327'                                     |
| etiqueta           | string    | Type inferred from 'FS2017021201'                               |
| serie              | string    | Type inferred from '7'                                          |
| descripcion        | string    | Type inferred from '1446 Transporte Bodega a Sitio torres'      |
| unidades           | string    | Type inferred from '1.0'                                        |
| retiro             | string    | Type inferred from 'F'                                          |
| oc                 | string    | Type inferred from '1620161754'                                 |
| vnl_del_activo_mxn | string    | Type inferred from '0.0'                                        |
| vnl_asignado_mxn   | string    | Type inferred from '0.00'                                       |

Las siguientes columnas son datos de control que se insertan al momento de la ingesta para identificar a la fuente, el archivo original no las incluye:

| col_name           | data_type | comment                                                         |
|--------------------|-----------|-----------------------------------------------------------------|
| filedate           | bigint    | Type inferred from '20190901'                                   |
| filename           | string    | Type inferred from 'ACTIVOS_APERTURADOS_SEPTIEMBRE_2019_V2.txt' |
| hash_id            | string    | Type inferred from 'null'                                       |
| sourceid           | string    | Type inferred from 'Activo Fijo'                                |
| registry_state     | string    | Type inferred from 'null'                                       |
| datasetname        | string    | Type inferred from 'af_activos_aperturados'                     |
| timestamp          | bigint    | Type inferred from '20191115'                                   |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda).

- **Particiones**

    Las particiones de la tabla **tx_fixed_asset** se generan de forma mensual usando el campo de auditoría **filedate**. A continuación se presentan las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_fixed_asset`:

| year  | month | day | #Rows   | #Files | Size     | Format | Location                                                                     |
|-------|-------|-----|---------|--------|----------|--------|------------------------------------------------------------------------------|
| 2019  | 5     | 1   | 1281000 | 2      | 390.13MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/AF/year=2019/month=5/day=1  |
| 2019  | 7     | 1   | 1303370 | 200    | 400.99MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/AF/year=2019/month=7/day=1  |
| 2019  | 8     | 1   | 1368761 | 200    | 430.71MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/AF/year=2019/month=8/day=1  |
| 2019  | 9     | 1   | 1384231 | 200    | 477.61MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/AF/year=2019/month=9/day=1  |
| 2019  | 10    | 1   | 1398204 | 200    | 477.27MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/AF/year=2019/month=10/day=1 |
| Total |      |    | 6735566 | 802    | 2.13GB   |       |                                                                             |


## Componentes del procesos de ingestion:

__1. Ingestion y Serialización via NiFi__

Los datos son ingestados al Data Lake usando el flujo de NiFi llamado **G - Activo Fijo**:

![Activo Fijo NiFi General View][img3]
Pipeline General __Activo Fijo__

Debido a que la fuente es una archivo `.csv` el único tratamiento de los datos que se realiza es convertir los registros a un formato estándar separado por pipes y con todos los valores citados con doble comillas; este proceso se realiza con un procesador ConvertRecord:

![Activo Fijo NiFi Detail View][img4]
Pipeline Detalle __activo Fijo__

__2. Aplicación de Reglas de Estandarización del Esquema `Kite`__

Las siguientes reglas se aplicarón para estandarizar el esquema de los datos que se genera al convertir los datos al formato Avro:

- Eliminado de caracteres especiales en el encabezado del archivo inestado.

```
${'$1':replace("-",""):replace("[",""):replace("]",""):replace(" ","_"):replace("ñ","n"):replace("#","Num"):replace("Í","I"):replace("(",""):replace(")","")}$2
```

- Remplazo de espacios por guiones bajos ( _ ) en el encabezado del archivo ingestado.

```
${'$1':replace(" ","_")}$2
```

__3. Generación de la Evolución del Esquema via `Kite`__

- La generación del esquema con Kite se invoca a través del siguiente comando:

```
./rci_ingesta_generacion_avro.sh {parametro0} 
```

El comando necesita un parámetro para funcionar, el cual se especifica en la siguiente tabla:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_00   | 7   | Valor que identifica a la fuente en  la documentación de Kite: [AX_IM_FrameworkIngestion_CommandExecutionV2](http://10.103.133.122/app/owncloud/f/14480776).  |

Ejemplo:

```
./rci_ingesta_generacion_avro.sh 7
```

__3. Estrategia Incremental vía `Spark`__

Debido a la naturaleza de los datos la fuente no requiere hacer cálculo de incrementales, por lo tanto, cada ingestión se inserta de forma completa. Este proceso se realiza mediante un script de [Spark](../Globales/SparkAxity), el cual se invoca mediante una linea de ejecución que necesita 16 parámetros:

```
spark-submit --master {parametro1} --deploy-mode {parametro2} --name {parametro3} --queue={parametro4} -class {parametro5} {parametro6} {parametro7} {parametro8} {parametro9} {parametro10} {parametr11} {parametro12} {parametro13} {parametro14} {parametro15}
```

- Especificación de parámetros del proceso Spark:

| Parámetro   | Valor del Parámetro                                                                      | Descripción del Parámetro                              |
|-------------|------------------------------------------------------------------------------------------|--------------------------------------------------------|
| parametro1  | yarn-cluster                                                                             |  Modo de ejecución de aplicación spark.                |
| parametro2  | cluster                                                                                  |  Modo en que se despliega la aplicación.               |
| parametro3  | Delta SPARK Activo Fijo'                                                                 |  Nombre de la aplicación spark.                        |
| parametro4  | root.rci                                                                                 |  Nombre del recurso queue.                             |
| parametro5  | com.axity.DataFlowIngestion                                                              |  Nombre de la clase.                                   |
| parametro6  | /home/fh967x/SparkNew/spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-dependencies.jar |  Ruta del archivo jar.                                 |
| parametro7  |  /data/RCI/raw/AF/data/                                                                  |  Directorio de área stage de datos.                    |
| parametro8  |  tx_fixed_asset                                                                          |  Nombre de la tabla destino.                           |
| parametro9  | hash_id                                                                                  |  Nombre del atributo hash_id.                          |
| parametro10 | hive                                                                                     |  Formato de registro de almacenamiento.                |
| parametro11 |  ACTIVO,ETIQUETA,SERIE,LOCATION,filedate                                                 |  Campos de cálculo para llave Hash.                    |
| parametro12 |  /data/RCI/stg/hive/work/ctl/ctrl_tx_fixed_asset.avro                                    |  Ruta del archivo avro de cifra de control.            |
| parametro13 |  /data/RCI/stg/hive/work/ctl/ctrl_tx_fixed_asset/20191126                                |  Directorio de salida de cifra control.                |
| parametro14 |  full                                                                                    |  Indicador de tipo de incrementalidad: full ó nofull.  |
| parametro15 | 4                                                                                        |  Número de compactación de coalesce.                   |


Ejemplo:

```
spark-submit --master yarn-cluster --deploy-mode cluster --name 'Delta SPARK' --queue=root.rci --class com.axity.DataFlowIngestion /home/fh967x/SparkNew/spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-dependencies.jar /data/RCI/raw/AF/data/ tx_fixed_asset hash_id hive ACTIVO,ETIQUETA,SERIE,LOCATION,filedate /data/RCI/stg/hive/work/ctl/ctrl_tx_fixed_asset.avro /data/RCI/stg/hive/work/ctl/ctrl_tx_fixed_asset/20191126 full 4
```

## Referencias al Framework de Ingestión

- [Framework de Ingestion](../Globales/)

## Código Fuente Local

- [Codigo NiFi - NFR](NFR/)

## Código Fuente Globales

- [Codigo NiFi](../Globales/NIFICustomProcessorXLSX)
- [Codigo Spark](../Globales/SparkAxity)
- [Codigo Kite](../Globales/attdlkrci)



[img1]: images/activofijo-nifi-03.png "Logo Axity"
[img2]: ../Globales/ArquitecturaFrameworkIngestion/images/att.png "Logo AT&T"
[img3]: images/activofijo-nifi-01.png "Activo Fijo NiFi Detail View"
=======
<a name="main"></a>  ![Encabezado](./images/encabezado.png)

----


# Documentación Data Ingestion para la fuente ATT **Activo Fijo**

## Descripcion del `FTP`

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](https://intellego365.sharepoint.com/sites/ATT-InventoryManagement/_layouts/15/Doc.aspx?sourcedoc={9fe304e1-34ab-495a-b38b-e99a17627460}&action=embedview&wdAllowInteractivity=False&wdHideGridlines=True&wdHideHeaders=True&wdDownloadButton=True&wdInConfigurator=True), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

## Descripción de la fuente de datos

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `rci_network_db.tx_fixed_asset`, en la cual se depositan los datos:

| col_name           | data_type | comment                                                         |
|--------------------|-----------|-----------------------------------------------------------------|
| activo             | string    | Type inferred from 'kite'                                    |
| units_assigned     | string    | Type inferred from 'kite'                                       |
| location           | string    | Type inferred from 'kite'                                     |
| etiqueta           | string    | Type inferred from 'kite'                               |
| serie              | string    | Type inferred from 'kite'                                          |
| descripcion        | string    | Type inferred from 'kite'      |
| unidades           | string    | Type inferred from 'kite'                                        |
| retiro             | string    | Type inferred from 'kite'                                          |
| oc                 | string    | Type inferred from 'kite'                                 |
| vnl_del_activo_mxn | string    | Type inferred from 'kite'                                        |
| vnl_asignado_mxn   | string    | Type inferred from 'kite'                                       |

Las siguientes columnas son datos de control que se insertan al momento de la ingesta para identificar a la fuente, el archivo original no las incluye:

| col_name           | data_type | comment                                                         |
|--------------------|-----------|-----------------------------------------------------------------|
| filedate           | bigint    | Type inferred from 'kite'                                   |
| filename           | string    | Type inferred from 'kite' |
| hash_id            | string    | Type inferred from 'kite'                                       |
| sourceid           | string    | Type inferred from 'kite'                                |
| registry_state     | string    | Type inferred from 'kite'                                       |
| datasetname        | string    | Type inferred from 'kite'                     |
| timestamp          | bigint    | Type inferred from 'kite'                                   |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda).

- **Particiones**

    Las particiones de la tabla **tx_fixed_asset** se generan de forma mensual usando el campo de auditoría **filedate**. A continuación se presentan las particiones creadas en la tabla: 
    
    ```
    show partitions rci_network_db.tx_fixed_asset:
    ```

| year  | month | #Rows   | #Files | Size     | Format | Location                                                               |
|-------|-------|---------|--------|----------|--------|------------------------------------------------------------------------|
| 2019  | 5     | 1281000 | 1      | 299.70MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/af/year=2019/month=5  |
| 2019  | 7     | 1303370 | 1      | 307.44MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/af/year=2019/month=7  |
| 2019  | 8     | 1368761 | 1      | 332.46MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/af/year=2019/month=8  |
| 2019  | 9     | 1384231 | 1      | 378.20MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/af/year=2019/month=9  |
| 2019  | 10    | 1398204 | 1      | 378.19MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/af/year=2019/month=10 |
| 2019  | 11    | 1413996 | 1      | 383.81MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/af/year=2019/month=11 |
| 2019  | 12    | 1424886 | 1      | 388.01MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/af/year=2019/month=12 |
| Total |       | 9574448 | 7      | 2.41GB   |        |                                                                        |


## Componentes del procesos de ingestion:

__1. Ingestion y Serialización via NiFi__

Los datos son ingestados al Data Lake usando el flujo de NiFi llamado **G - Activo Fijo**:

![Activo Fijo NiFi General View][img3]
Pipeline General __Activo Fijo__

Debido a que la fuente es una archivo `.csv` el único tratamiento de los datos que se realiza es convertir los registros a un formato estándar separado por pipes y con todos los valores citados con doble comillas; este proceso se realiza con un procesador ConvertRecord:

![Activo Fijo NiFi Detail View][img4]
Pipeline Detalle __activo Fijo__

__2. Aplicación de Reglas de Estandarización del Esquema `Kite`__

Las siguientes reglas se aplicarón para estandarizar el esquema de los datos que se genera al convertir los datos al formato Avro:

- Eliminado de caracteres especiales en el encabezado del archivo inestado.

```
${'$1':replace("-",""):replace("[",""):replace("]",""):replace(" ","_"):replace("ñ","n"):replace("#","Num"):replace("Í","I"):replace("(",""):replace(")","")}$2
```

- Remplazo de espacios por guiones bajos ( _ ) en el encabezado del archivo ingestado.

```
${'$1':replace(" ","_")}$2
```

3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 7   | Valor de correspondiente al flujo de Activo Fijo |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización: 
    
     ```
     sh rci_ingesta_generacion_avro.sh 7
     ```

## Referencias al Framework de Ingestión

- [Framework de Ingestion](../Globales/)

## Código Fuente Local

- [Codigo NiFi - NFR](NFR/)

## Código Fuente Globales

- [Codigo NiFi](../Globales/NIFICustomProcessorXLSX)
- [Codigo Spark](../Globales/SparkAxity)
- [Codigo Kite](../Globales/attdlkrci)



[img1]: images/activofijo-nifi-03.png "Logo Axity"
[img2]: ../Globales/ArquitecturaFrameworkIngestion/images/att.png "Logo AT&T"
[img3]: images/activofijo-nifi-01.png "Activo Fijo NiFi Detail View"
>>>>>>> f17ccfc48c11b46af8c37c2b5c513a6316537378
[img4]: images/activofijo-nifi-02.png "Activo Fijo NiFi Detail View"