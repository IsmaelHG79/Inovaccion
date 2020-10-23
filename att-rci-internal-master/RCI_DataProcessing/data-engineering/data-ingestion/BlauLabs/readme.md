![EncabezadoAxity][imgEncabezado]


# Documentación Data Ingestion para la fuente ATT **BLAULABS**

Para esta fuente se documentan diferentes flujos de una sola fuente, esto debido a que existen diferentes archivos generados los cuales son los siguientes:

* [Blaulabs EM (Element Microwave)](#blaulabs_em)
* [Blaulabs NE (Network Element)](#blaulabs_ne)

## <a name="blaulabs_em"></a> Blaulabs EM

## Descripción del `FTP`  
El servidor FTP donde se tomaran los archivos de BLAULABS es :```10.150.25.149```.

La ruta donde se encontraran los archivos:
* BLAULABS :```/FILES_SPLUNK/INVENTARIO/BLAULABS/BlaulabsExcel```

Las rutas donde se hara un backup de los archivos que se procesarán:
* BLAULABS : ```/FILES_SPLUNK/INVENTARIO/BLAULABS/BlaulabsExcel/ingested```

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481174)

## Descripción de la fuentes de datos
- **Descripción**
  [Blaulabas EM EDA](../../../../RCI_DataAnalysis/eda/Gestor_Blaulabs/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Gestor_Blaulabs/README.md)

     Sentencia: ```describe formatted tx_bl_inventarioem```

  | Nombre de Columna        	| Tipo de Dato 	| Comentario                                              	|
  |--------------------	|-----------	|------------------------------------------------------	|
  | region             	| string    	| Type inferred from 'Region 1'                        	|
  | mso                	| string    	| Type inferred from 'Otay'                            	|
  | sala               	| string    	| Type inferred from 'Sala Fuerza'                     	|
  | elemento           	| string    	| Type inferred from 'MSOTIJ01-PLC01'                  	|
  | descripcion        	| string    	| Type inferred from 'Otay-Sala Fuerza-MSOTIJ01-PLC01' 	|
  | capacidad          	| string    	| Type inferred from '20 TR'                           	|
  | tipo               	| string    	| Type inferred from 'EM'                              	|
  | plataforma         	| string    	| Type inferred from 'PLC'                             	|
  | marca              	| string    	| Type inferred from 'NE'                              	|
  | modelo             	| string    	| Type inferred from 'NE'                              	|
  | serie              	| string    	| Type inferred from 'NE'                              	|
  | activofijo         	| string    	| Type inferred from 'NE'                              	|

  Las siguientes columnas son creadas para la identidad de la fuente:

  | Nombre de Columna        	| Tipo de Dato 	| Comentario                                              	|
  |--------------------	|-----------	|------------------------------------------------------	|
  | filedate           	| bigint    	| Type inferred from '20190719'                        	|
  | filename           	| string    	| Type inferred from 'InventarioEM_19072019.xlsx'      	|
  | hash_id            	| string    	| Type inferred from 'null'                            	|
  | sourceid           	| string    	| Type inferred from 'InventarioEM'                    	|
  | registry_state     	| string    	| Type inferred from 'null'                            	|
  | datasetname        	| string    	| Type inferred from 'bl_inventario'                   	|
  | timestamp          	| bigint    	| Type inferred from '20191129'                        	|
  | transaction_status 	| string    	| Type inferred from 'null'                            	|    



- **Particiones**

    A continuación se presentan las particiones creadas de la tabla **tx_bl_inventarioem**.

    Sentencia: ```show partitions tx_bl_inventarioem```

    | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Location                                                                                 	|
    |------	|-------	|-----	|-------	|--------	|----------	|--------	|------------------------------------------------------------------------------------------	|
    | 2019 	| 7     	| 19  	| 1,345  	| 1      	| 499.74KB 	| AVRO   	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/Gestores/BL/EM/year=2019/month=7/day=19 	|
    | 2019 	| 7     	| 26  	| 129   	| 6      	| 59.74KB  	| AVRO   	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/Gestores/BL/EM/year=2019/month=7/day=26 	|
    | 2019 	| 9     	| 10  	| 301   	| 6      	| 126.05KB 	| AVRO   	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/Gestores/BL/EM/year=2019/month=9/day=10 	|
    | 2019 	| 9     	| 20  	| 409   	| 6      	| 169.08KB 	| AVRO   	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/Gestores/BL/EM/year=2019/month=9/day=20 	|
    | 2019 	| 11    	| 1   	| 646   	| 6      	| 255.86KB 	| AVRO   	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/Gestores/BL/EM/year=2019/month=11/day=1 	|

## Componentes del procesos de ingestión:

1 __Ingestión y Serialización via NiFi__

![Blaulabs EM NiFi Vista General][imgEM1]

Pipeline Principal __Flujo Principal__

![Blaulabs EM NiFi Vista Subproceso][imgEM2]

Pipeline Subproceso __Flujo de Subproceso__

![Blaulabs EM NiFi Vista Lectura de Archivos][imgEM3]

Pipeline Lectura de Archivos __Lectura de Archivos__

![Blaulabs EM NiFi Vista Procesamiento][imgEM4]

[imgEM1]: images/BlaulabsEM-nifi-00.png "Blaulabs EM NiFi vista general"
[imgEM2]: images/BlaulabsEM-nifi-01.png "Blaulabs EM NiFi vista subproceso"
[imgEM3]: images/BlaulabsEM-nifi-02.png "Blaulabs EM NiFi Lectura de Archivos"
[imgEM4]: images/BlaulabsEM-nifi-03.png "Blaulabs EM NiFi Lectura de Archivos"

Pipeline Lectura de Archivos __Procesamiento de Archivos__

2 __Reglas de Estandarización del Esquema `Kite`__

Las siguientes reglas se aplicarón para estandarizar el esquema:

- Remover Caracteres especiales en el header.
- Reemplazo de caracter "_" por " " en el nombre del archivo.

3 __Generación Evolución Esquema vía `Kite`__

- Especificar parámetros del proceso kite:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 18   | Valor de correspondiente al flujo Blaulabs EM   |


Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```

Ejemplo:

```
./rci_ingesta_generacion_avro.sh 18
```

4 __Estrategia de Incrementalidad vía `Spark`__

- Especificar parámetros del shell kite:

| Parámetro   	| Valor del Parámetro                                                                                   	| Descripción del Parámetro                            	|
|-------------	|-------------------------------------------------------------------------------------------------------	|------------------------------------------------------	|
| parametro1  	| yarn-cluster                                                                                          	| Modo de ejecución de aplicación spark.               	|
| parametro2  	| cluster                                                                                               	| Modo en que se despliega la aplicación.              	|
| parametro3  	| 'Delta SPARK BlaulabsEM '                                                                         	| Nombre de la aplicación spark.                       	|
| parametro4  	| root.rci                                                                                              	| Nombre del recurso queue.                            	|
| parametro5  	| com.axity.DataFlowIngestion                                                                           	| Nombre de la clase.                                  	|
| parametro6  	| /home/fh967x/SparkNew/spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-dependencies.jar              	| Ruta del archivo jar.                                	|
| parametro7  	| /data/RCI/raw/Gestores/BL/EM/data/                                                                               	| Directorio de área stage de datos.                   	|
| parametro8  	| tx_bl_inventarioem                                                                                        	| Nombre de la tabla destino.                          	|
| parametro9  	| hash_id                                                                                               	| Nombre del atributo hash_id.                         	|
| parametro10 	| hive                                                                                                  	| Formato de registro de almacenamiento.               	|
| parametro11 	| Marca,Modelo,Serie 	| Campos de cálculo para llave Hash.                   	|
| parametro12 	| /data/RCI/stg/hive/work/ctl/ctrl_tx_bl_inventarioem.avro                                                  	| Ruta del archivo avro de cifra de control.           	|
| parametro13 	| /data/RCI/stg/hive/work/ctl/ctrl_tx_bl_inventarioem/InventarioEM 01112019                                 	| Directorio de salida de cifra control.               	|
| parametro14 	| nofull                                                                                                  	| Indicador de tipo de incrementalidad: full ó nofull. 	|
| parametro15 	| 6                                                                                                     	| Número de compactación de coalesce.                  	|

Agregar la línea de ejecución spark

```
spark-submit --master {parametro1} --deploy-mode {parametro2} --name {parametro3} --queue={parametro4} -class {parametro5} {parametro6} {parametro7} {parametro8} {parametro9} {parametro10} {parametr11} {parametro12} {parametro13} {parametro14} {parametro15}

```

Ejemplo:

```
spark-submit --master yarn-cluster --deploy-mode cluster --name 'Delta SPARK BlaulabsEM' --queue=root.rci --class com.axity.DataFlowIngestion /home/fh967x/SparkNew/spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-dependencies.jar /data/RCI/raw/Gestores/BL/data/ ctrl_tx_bl_inventarioem hash_id hive Marca,Modelo,Serie /data/RCI/stg/hive/work/ctl/ctrl_tx_bl_inventarioem.avro /data/RCI/stg/hive/work/ctl/ctrl_tx_bl_inventarioem/InventarioEM 01112019 nofull 6
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

## <a name="blaulabs_ne"></a> Blaulabs NE

## Descripción del `FTP`  
El servidor FTP donde se tomaran los archivos de BLAULABS es :```10.150.25.149```.

La ruta donde se encontraran los archivos:
* BLAULABS :```/FILES_SPLUNK/INVENTARIO/BLAULABS/BlaulabsExcel```

Las rutas donde se hara un backup de los archivos que se procesarán:
* BLAULABS : ```/FILES_SPLUNK/INVENTARIO/BLAULABS/BlaulabsExcel/ingested```

Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481174)

## Descripción de la fuentes de datos
- **Descripción**
  [Blaulabas NE EDA](../../../../RCI_DataAnalysis/eda/Gestor_Blaulabs/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/Gestor_Blaulabs/README.md)

     Sentencia: ```describe formatted tx_bl_inventarione```

  | Nombre de Columna 	| Tipo de Dato 	| Comentario                                          	|
  |----------	|-----------	|--------------------------------------------------	|
  | region   	| string    	| Type inferred from 'Region 1'                    	|
  | mso      	| string    	| Type inferred from 'Otay'                        	|
  | sala     	| string    	| Type inferred from 'Sala pop evolution telcos 3' 	|
  | pasillo  	| string    	| Type inferred from 'Fila 1'                      	|
  | rack     	| string    	| Type inferred from 'Rack 001'                    	|
  | elemento 	| string    	| Type inferred from 'C406-0978'                   	|
  | tipo     	| string    	| Type inferred from 'NE'                          	|
  | marca    	| string    	| Type inferred from 'ACCEDIAN'                    	|
  | modelo   	| string    	| Type inferred from 'LT'                          	|
  | serie    	| string    	| Type inferred from 'C406-0978'                   	|

  Las siguientes columnas son creadas para la identidad de la fuente:

  | Nombre de Columna 	| Tipo de Dato 	| Comentario                                          	|
  |--------------------	|-----------	|-------------------------------------------------	|
  | filedate           	| bigint    	| Type inferred from '20190807'                   	|
  | filename           	| string    	| Type inferred from 'InventarioNE_07082019.XLSX' 	|
  | hash_id            	| string    	| Type inferred from 'null'                       	|
  | sourceid           	| string    	| Type inferred from 'InventarioEM'               	|
  | registry_state     	| string    	| Type inferred from 'null'                       	|
  | datasetname        	| string    	| Type inferred from 'bl_inventario'              	|
  | timestamp          	| bigint    	| Type inferred from '20191129'                   	|
  | transaction_status 	| string    	| Type inferred from 'null'                       	|

- **Particiones**

    A continuación se presentan las particiones creadas de la tabla **tx_bl_inventarione**.

    Sentencia: ```show partitions tx_bl_inventarione```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Location                                                                                 	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|------------------------------------------------------------------------------------------	|
  | 2019 	| 8     	| 7  	| 6678     	| 1      	| 499.74KB 	| AVRO   	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/Gestores/BL/NE/year=2019/month=8/day=7 	|

  ## Componentes del procesos de ingestión:

  1 __Ingestión y Serialización via NiFi__

  ![Blaulabs NE NiFi Vista General][imgNE1]

  Pipeline Principal __Flujo Principal__

  ![Blaulabs NE NiFi Vista Subproceso][imgNE2]

  Pipeline Subproceso __Flujo de Subproceso__

  ![Blaulabs NE NiFi Vista Lectura de Archivos][imgNE3]

  Pipeline Lectura de Archivos __Lectura de Archivos__

  ![Blaulabs NE NiFi Vista Procesamiento][imgNE4]

  Pipeline Lectura de Archivos __Procesamiento de Archivos__

  [imgNE1]: images/BlaulabsNE-nifi-00.png "Blaulabs NE NiFi vista general"
  [imgNE2]: images/BlaulabsNE-nifi-01.png "Blaulabs NE NiFi vista subproceso"
  [imgNE3]: images/BlaulabsNE-nifi-02.png "Blaulabs NE NiFi Lectura de Archivos"
  [imgNE4]: images/BlaulabsNE-nifi-03.png "Blaulabs NE NiFi Lectura de Archivos"

  2 __Reglas de Estandarización del Esquema `Kite`__

  Las siguientes reglas se aplicarón para estandarizar el esquema:

  - Remover Caracteres especiales en el header.
  - Reemplazo de caracter "_" por " " en el nombre del archivo.

3 __Generación Evolución Esquema vía `Kite`__

  - Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 17   | Valor de correspondiente al flujo Blaulabs NE   |


  Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```

  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 17
  ```

  4 __Estrategia de Incrementalidad vía `Spark`__

  - Especificar parámetros del shell kite:

  | Parámetro   	| Valor del Parámetro                                                                                   	| Descripción del Parámetro                            	|
  |-------------	|-------------------------------------------------------------------------------------------------------	|------------------------------------------------------	|
  | parametro1  	| yarn-cluster                                                                                          	| Modo de ejecución de aplicación spark.               	|
  | parametro2  	| cluster                                                                                               	| Modo en que se despliega la aplicación.              	|
  | parametro3  	| 'Delta SPARK BlaulabsNE '                                                                         	| Nombre de la aplicación spark.                       	|
  | parametro4  	| root.rci                                                                                              	| Nombre del recurso queue.                            	|
  | parametro5  	| com.axity.DataFlowIngestion                                                                           	| Nombre de la clase.                                  	|
  | parametro6  	| /home/fh967x/SparkNew/spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-dependencies.jar              	| Ruta del archivo jar.                                	|
  | parametro7  	| /data/RCI/raw/Gestores/BL/NE/data/                                                                               	| Directorio de área stage de datos.                   	|
  | parametro8  	| tx_bl_inventarione                                                                                        	| Nombre de la tabla destino.                          	|
  | parametro9  	| hash_id                                                                                               	| Nombre del atributo hash_id.                         	|
  | parametro10 	| hive                                                                                                  	| Formato de registro de almacenamiento.               	|
  | parametro11 	| Marca,Modelo,Serie 	| Campos de cálculo para llave Hash.                   	|
  | parametro12 	| /data/RCI/stg/hive/work/ctl/ctrl_tx_bl_inventarione.avro                                                  	| Ruta del archivo avro de cifra de control.           	|
  | parametro13 	| /data/RCI/stg/hive/work/ctl/ctrl_tx_bl_inventarione/InventarioNE 01112019                                 	| Directorio de salida de cifra control.               	|
  | parametro14 	| nofull                                                                                                  	| Indicador de tipo de incrementalidad: full ó nofull. 	|
  | parametro15 	| 6                                                                                                     	| Número de compactación de coalesce.                  	|

  Agregar la línea de ejecución spark

  ```
  spark-submit --master {parametro1} --deploy-mode {parametro2} --name {parametro3} --queue={parametro4} -class {parametro5} {parametro6} {parametro7} {parametro8} {parametro9} {parametro10} {parametr11} {parametro12} {parametro13} {parametro14} {parametro15}

  ```

  Ejemplo:

  ```
  spark-submit --master yarn-cluster --deploy-mode cluster --name 'Delta SPARK BlaulabsNE' --queue=root.rci --class com.axity.DataFlowIngestion /home/fh967x/SparkNew/spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-dependencies.jar /data/RCI/raw/Gestores/BL/NE/data/ ctrl_tx_bl_inventarione hash_id hive Marca,Modelo,Serie /data/RCI/stg/hive/work/ctl/ctrl_tx_bl_inventarione.avro /data/RCI/stg/hive/work/ctl/ctrl_tx_bl_inventarione/InventarioNE 01112019 nofull 6
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



[imgLogoAxity]:../Globales/ArquitecturaFrameworkIngestion/images/axity.png ""
[imgLogoAtt]:../Globales/ArquitecturaFrameworkIngestion/images/att.png ""
[imgEncabezado]:../Globales/ArquitecturaFrameworkIngestion/images/encabezado.png ""
