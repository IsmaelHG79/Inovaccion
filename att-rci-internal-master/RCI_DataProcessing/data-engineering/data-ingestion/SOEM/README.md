<a name="main"></a>  ![Encabezado](./images/encabezado.png)

----

# Documentación Data Ingestion para la fuente ATT **SOEM**

Para esta fuente se documentan diferentes flujos de una sola fuente, esto debido a que existen diferentes archivos generados los cuales son los siguientes:

1. [soem13_NE_Inventory](#ne)
2. [soem13_HW_Module_Inventory](#hw)
3. [soem13_SW_Module_Inventory](#sw)

En total son 3 diferentes tipos de archivos que se tienen que procesar y sera explicados con mas detalle en los siguientes apartados.

* __Vista Principal de Nifi para SOEM__

    ![Soem NiFi Main View][img1]
    *Pipeline General de __SOEM__*

* __Vista Principal Flujo de Nifi para SOEM__

    ![Soem NiFi All Inventory View][img2]                        
    *Vista Flujo Principal Nifi __SOEM__*

* __Vista Flujo de Nifi para SOEM (NE, HW, SW)__

    ![Soem NiFi All Inventory View][img3]                        
    *Vista Flujo de Detalle Principal Nifi __SOEM__*

## Descripcion del *`FTP`*

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

<<<<<<< HEAD
Las rutas donde se hara un backup de los archivos que se procesaran para cada tema de la fuente SOEM para despues procesarlos son las siguientes:

``` /FILES/SOEM/101.33.0.15/home/ftpuser/tn_inventory/ingested/ ```

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481174)
=======
- El directorio de HDFS en donde se colocan los datos ingestados.
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

##### [Ir a Inicio](#main)

## <a name="ne"></a> Soem NE Inventory

### Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA SOEM](/RCI_DataAnalysis/eda/Gestor_SOEM/README.md#descripcion)**

- **[dicciorario de datos]** La siguiente tabla muestra el resultado de ejecutar el siguiente comando: 
    
    ```
    describe formatted rci_network_db.tx_soem_ne;
    ``` 

| col_name | data_type | comment |
|--------------------|-----------|-------------------------------------------------------------------------|
| nodename | string | Type inferred from 'kite' |
| id | string | Type inferred from 'kite' |
| type | string | Type inferred from 'kite' |
| address | string | Type inferred from 'kite' |
| nename | string | Type inferred from 'kite' |
| location | string | Type inferred from 'kite' |
| information | string | Type inferred from 'kite' |
| site_id | string | Type inferred from 'kite' |
| nealias | string | Type inferred from 'kite' |
| nenotes | string | Type inferred from 'kite' |
| updatedate | string | Type inferred from 'kite' |
| neaddedtime | string | Type inferred from 'kite' |
| nelastmanagedtime | string | Type inferred from 'kite' |
| nelaststartedtime | string | Type inferred from 'kite' |
| nelastmodifiedtime | string | Type inferred from 'kite' |

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

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA SOEM](/RCI_DataAnalysis/eda/Gestor_SOEM/README.md)
    
- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:
    
    ```
    show partitions rci_network_db.tx_soem_ne;
    ```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|-------|--------|----------|--------|---------------------------------------------------------------------------------------------|
| 2019 | 9 | 5 | 178 | 1 | 101.50KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=9/day=5 |
| 2019 | 9 | 12 | 190 | 1 | 106.37KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=9/day=12 |
| 2019 | 9 | 19 | 190 | 1 | 106.37KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=9/day=19 |
| 2019 | 9 | 26 | 190 | 1 | 106.37KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=9/day=26 |
| 2019 | 10 | 3 | 190 | 1 | 106.37KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=10/day=3 |
| 2019 | 10 | 10 | 190 | 1 | 106.37KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=10/day=10 |
| 2019 | 10 | 17 | 190 | 1 | 106.37KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=10/day=17 |
| 2019 | 10 | 24 | 190 | 1 | 106.41KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=10/day=24 |
| 2019 | 10 | 31 | 192 | 1 | 107.21KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=10/day=31 |
| 2019 | 11 | 7 | 192 | 1 | 107.21KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=11/day=7 |
| 2019 | 11 | 14 | 192 | 1 | 107.21KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=11/day=14 |
| 2019 | 11 | 21 | 192 | 1 | 107.21KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=11/day=21 |
| 2019 | 11 | 28 | 198 | 1 | 109.60KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=11/day=28 |
| 2019 | 12 | 5 | 205 | 1 | 112.38KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=12/day=5 |
| 2019 | 12 | 12 | 234 | 1 | 124.47KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/ne/year=2019/month=12/day=12 |
| Total |  |  | 2913 | 15 | 1.58MB |  |  |

### Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Soem NE NiFi General View][img4]             
    *Pipeline General View __SOEM NE__*

    ![Soem NE NiFi Flow General View][img0]      
    *Pipeline General Flow View __SOEM NE__*

    ![Soem NE NiFi Detail View][img5]      
    *Pipeline Detail View __SOEM NE__*

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
| parametro_01   | 10   | Valor de correspondiente al flujo de SOEM NE  |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización : 
    
     ```
     sh rci_ingesta_generacion_avro.sh 10
     ```

##### [Ir a Inicio](#main)

## <a name="hw"></a> Soem HW Module Inventory

### Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA SOEM](/RCI_DataAnalysis/eda/Gestor_SOEM/README.md#descripcion)**

- **[dicciorario de datos]** La siguiente tabla muestra el resultado de ejecutar el siguiente comando: 
    
    ```
    describe formatted rci_network_db.tx_soem_hw;
    ``` 

| col_name | data_type | comment |
|---------------------|-----------|-------------------------------------------------------------------------|
| nodename | string | Type inferred from 'kite' |
| id | string | Type inferred from 'kite' |
| ammposition | string | Type inferred from 'kite' |
| assetid | string | Type inferred from 'kite' |
| typeofunit | string | Type inferred from 'kite' |
| productnumber | string | Type inferred from 'kite' |
| version | string | Type inferred from 'kite' |
| serialnumber | string | Type inferred from 'kite' |
| productiondate | string | Type inferred from 'kite' |
| elapsedruntime | string | Type inferred from 'kite' |
| ne_id | string | Type inferred from 'kite' |
| nealias | string | Type inferred from 'kite' |
| notes | string | Type inferred from 'kite' |
| updatedate | string | Type inferred from 'kite' |
| moduleproductnumber | string | Type inferred from 'kite' |
| moduleserialnumber | string | Type inferred from 'kite' |

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

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA SOEM](/RCI_DataAnalysis/eda/Gestor_SOEM/README.md)
    
- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:
    
    ```
    show partitions rci_network_db.tx_soem_hw;
    ```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|-------|--------|----------|--------|---------------------------------------------------------------------------------------------|
| 2019 | 9 | 5 | 2156 | 1 | 859.64KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=9/day=5 |
| 2019 | 9 | 12 | 2225 | 1 | 884.33KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=9/day=12 |
| 2019 | 9 | 19 | 2225 | 1 | 884.33KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=9/day=19 |
| 2019 | 9 | 26 | 2225 | 1 | 884.33KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=9/day=26 |
| 2019 | 10 | 3 | 2225 | 1 | 884.21KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=10/day=3 |
| 2019 | 10 | 10 | 2225 | 1 | 884.24KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=10/day=10 |
| 2019 | 10 | 17 | 2225 | 1 | 884.25KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=10/day=17 |
| 2019 | 10 | 24 | 2225 | 1 | 884.26KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=10/day=24 |
| 2019 | 10 | 31 | 2237 | 1 | 888.47KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=10/day=31 |
| 2019 | 11 | 7 | 2237 | 1 | 888.47KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=11/day=7 |
| 2019 | 11 | 14 | 2237 | 1 | 888.47KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=11/day=14 |
| 2019 | 11 | 21 | 2237 | 1 | 888.47KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=11/day=21 |
| 2019 | 11 | 28 | 2279 | 1 | 903.24KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=11/day=28 |
| 2019 | 12 | 5 | 2328 | 1 | 920.42KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=12/day=5 |
| 2019 | 12 | 12 | 2527 | 1 | 991.36KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/hw/year=2019/month=12/day=12 |
| Total |  |  | 33813 | 15 | 13.10MB |  |  |

### Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Soem HW NiFi General View][img6]             
    *Pipeline General View __SOEM HW__*

    ![Soem HW NiFi Flow General View][img0]      
    *Pipeline General Flow View __SOEM HW__*

    ![Soem HW NiFi Detail View][img7]      
    *Pipeline Detail View __SOEM HW__*

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
| parametro_01   | 9   | Valor de correspondiente al flujo de SOEM HW  |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización : 
    
     ```
     sh rci_ingesta_generacion_avro.sh 9
     ```

##### [Ir a Inicio](#main)

## <a name="sw"></a> Soem SW Module Inventory

### Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA SOEM](/RCI_DataAnalysis/eda/Gestor_SOEM/README.md#descripcion)**

- **[dicciorario de datos]** La siguiente tabla muestra el resultado de ejecutar el siguiente comando: 
    
    ```
    describe formatted rci_network_db.tx_soem_sw;
    ``` 

| col_name | data_type | comment |
|--------------------|-----------|---------------------------------------------------------------------|
| nodename | string | Type inferred from 'kite' |
| id | string | Type inferred from 'kite' |
| minimumswversion | string | Type inferred from 'kite' |
| typeofswunit | string | Type inferred from 'kite' |
| swproductnumber | string | Type inferred from 'kite' |
| activesw | string | Type inferred from 'kite' |
| passivesw | string | Type inferred from 'kite' |
| hw_module_id | string | Type inferred from 'kite' |
| nealias | string | Type inferred from 'kite' |
| updatedate | string | Type inferred from 'kite' |

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

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA SOEM](/RCI_DataAnalysis/eda/Gestor_SOEM/README.md)
    
- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:
    
    ```
    show partitions rci_network_db.tx_soem_sw;
    ```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|-------|--------|----------|--------|---------------------------------------------------------------------------------------------|
| 2019 | 9 | 5 | 1277 | 1 | 446.59KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=9/day=5 |
| 2019 | 9 | 12 | 1312 | 1 | 459.55KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=9/day=12 |
| 2019 | 9 | 19 | 1312 | 1 | 459.55KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=9/day=19 |
| 2019 | 9 | 26 | 1313 | 1 | 459.89KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=9/day=26 |
| 2019 | 10 | 3 | 1313 | 1 | 459.89KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=10/day=3 |
| 2019 | 10 | 10 | 1312 | 1 | 459.55KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=10/day=10 |
| 2019 | 10 | 17 | 1312 | 1 | 459.56KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=10/day=17 |
| 2019 | 10 | 24 | 1312 | 1 | 459.57KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=10/day=24 |
| 2019 | 10 | 31 | 1318 | 1 | 461.75KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=10/day=31 |
| 2019 | 11 | 7 | 1318 | 1 | 461.76KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=11/day=7 |
| 2019 | 11 | 14 | 1318 | 1 | 461.76KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=11/day=14 |
| 2019 | 11 | 21 | 1318 | 1 | 461.76KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=11/day=21 |
| 2019 | 11 | 28 | 1336 | 1 | 468.34KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=11/day=28 |
| 2019 | 12 | 5 | 1357 | 1 | 476.02KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=12/day=5 |
| 2019 | 12 | 12 | 1444 | 1 | 508.33KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/gestores/soem/sw/year=2019/month=12/day=12 |
| Total |  |  | 19872 | 15 | 6.80MB |  |  |

### Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![Soem HW NiFi General View][img8]             
    *Pipeline General View __SOEM SW__*

    ![Soem HW NiFi Flow General View][img0]      
    *Pipeline General Flow View __SOEM SW__*

    ![Soem HW NiFi Detail View][img9]      
    *Pipeline Detail View __SOEM SW__*

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
| parametro_01   | 8   | Valor de correspondiente al flujo de SOEM SW  |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización : 
    
     ```
     sh rci_ingesta_generacion_avro.sh 8
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
[img0]: images/soem-nifi-00.png "Soem NiFi General Flow View"
[img1]: images/soem-nifi-01.png "Soem NiFi Principal View"
[img2]: images/soem-nifi-02.png "Soem NiFi Main Flow View"
[img3]: images/soem-nifi-03.png "Soem NiFi Flows View"
[img4]: images/soem-ne-nifi-01.png "Soem NiFi NE Main View"
[img5]: images/soem-ne-nifi-02.png "Soem NiFi NE Detail View"
[img6]: images/soem-hw-nifi-01.png "Soem NiFi HW Main View"
[img7]: images/soem-hw-nifi-02.png "Soem NiFi HW Detail View"
[img8]: images/soem-sw-nifi-01.png "Soem NiFi SW Main View"
[img9]: images/soem-sw-nifi-02.png "Soem NiFi SW Detail View"
