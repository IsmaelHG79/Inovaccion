<a name="main"></a>  ![Encabezado](./images/encabezado.png)

----

# Documentación Data Ingestion para la fuente ATT **CIENA**

## Descripcion del *`FTP`*

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

<<<<<<< HEAD
La ruta donde se hara un backup de los archivos que se procesaran de la fuente CIENA para despues procesarlos es la siguiente:

``` /FILES/CIENA/ingested/ ```

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481174)
=======
- El directorio de HDFS en donde se colocan los datos ingestados.
>>>>>>> f17ccfc48c11b46af8c37c2b5c513a6316537378

## Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA Ciena](/RCI_DataAnalysis/eda/Gestor_Ciena/README.md#descripcion)**

- **[dicciorario de datos]** La siguiente tabla muestra el resultado de ejecutar el siguiente comando: 
    
    ```
    describe formatted rci_network_db.tx_ciena;
    ```
    
| col_name | data_type | comment |
|--------------------|-----------|------------------------------------------|
| system_name | string | Type inferred from 'kite' |
| ne_type | string | Type inferred from 'kite' |
| component | string | Type inferred from 'kite' |
| component_subtype | string | Type inferred from 'kite' |
| clei_code | string | Type inferred from 'kite' |
| serial_number | string | Type inferred from 'kite' |
| part_number | string | Type inferred from 'kite' |
| manufacture_date | string | Type inferred from 'kite' |
| hardware_version | string | Type inferred from 'kite' |
| firmware_version | string | Type inferred from 'kite' |
| software_version | string | Type inferred from 'kite' |
| operational_status | string | Type inferred from 'kite' |
| model_id | string | Type inferred from 'kite' |
| accuracy_date | string | Type inferred from 'kite' |
| wavelength | string | Type inferred from 'kite' |
| frequency | string | Type inferred from 'kite' |
| channel_number | string | Type inferred from 'kite' |

Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestion.

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

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA CIENA](/RCI_DataAnalysis/eda/Gestor_Ciena/README.md)

- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:
    
    ```
    show partitions rci_network_db.tx_ciena;
    ```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|-------|--------|--------|--------|---------------------------------------------------------------------------------------|
| 2019 | 7 | 15 | 3785 | 1 | 1.24MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/gc/year=2019/month=7/day=15 |
| Total |  |  | 3785 | 1 | 1.24MB |  |  |


## Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Ciena NiFi General View][img1]
    *Pipeline General __Ciena__*

    ![Ciena NiFi Main View][img2]                             
    *Pipeline Main __Ciena__*

    ![Ciena NiFi Flow View][img3]      
    *Pipeline Flow __Ciena__*

    ![Cisco EPN NiFi Detail View][img4]      
    *Pipeline Detalle __Ciena__*

2. **Reglas de estandarizacion del esquema**

    * Sobre el esquema se eliminaron caracteres para que se generara correctamente el esquema del archivo avro con la siguiente expresion regular:
    
     ```
     Valor de Busqueda: (?s)(^[^\n]*)(.*$)
     Expresion regular a ejecutar: ${'$1':replace(" ","_"):replace("[",""):replace("]",""):replace("-","")}$2
     ```
   
3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 11   | Valor de correspondiente al flujo de CIENA  |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización: 
    
     ```
     sh rci_ingesta_generacion_avro.sh 11
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

 [img1]: images/ciena-nifi-01.png "Ciena NiFi General View"
 [img2]: images/ciena-nifi-02.png "Ciena NiFi Main View"
 [img3]: images/ciena-nifi-03.png "Ciena NiFi Flow View"
 [img4]: images/ciena-nifi-04.png "Ciena NiFi Detail View"
 