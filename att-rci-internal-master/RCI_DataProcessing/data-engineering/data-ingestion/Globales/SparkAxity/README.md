|                       |                                    |
|----------------------	|------------------------------------|
| ![EncabezadoAxity][img1] | ![EncabezadoATT][img2] |

# Documentación del codigo y funcionamiento de **SPARK**

## Introduccion  
En el mundo de big data para manejar y procesar grandes cantidades existen diversas herramientas o engines de procesamiento, de los cuales Apache Spark es el que se utilizamos, ya que es el que se encuentra configurado en el server por lo que  los job o applications que se realizaron para procesar los datos fuente se realizaron con el lenguaje de programacion scala, ya que nos facilita y nos nos provee un mejor performance y desempeño que con python.  

## Objetivos
Los objetivos del proceso de ingestion con **SPARK**, es poder realizar el manejo de los datos fuentes e ingestarlos a **HIVE** en su respectiva tabla, la forma de manejar esas ingestas es de dos maneras de acuerdo al analisis previo relizado, las formas son **DELTAS** e **INCREMENTAL**, en ambas manera se implementa el **SCHEMA EVOLUTION** de kite, para el manejo de las columnas.

## Desarrollo
Como ya se habia explicado, las formas del funcionamiento de las ingestas utilizando spark son dos: ***DELTAS*** E ***INCREMENTAL***, por lo que explicara mas a fondo la logica que se utilizo en ambos procesos.

#### Cargas Incrementales
Las cargas de manera **INCREMENTAL** funcionan de la siguiente manera; durante el analisis de las fuentes se dieron varios casos de los cuales uno en especifico es que los datos que provienen de las fuentes siempre cambian, ya sean las columnas, los tipos de datos o los registros, por lo que no se pudo encontrar un patron o una llave para poder manejar la trazabilidad de dichos registros.

En ese caso cuando los registros siempre cambian y no tienen trazabilidad se decidio utilizar la estrategia de cargas incrementales, que son fotos por cada fuenten que llega, es decir que la manera en que se cargan es de que se toma de la fuente por spark, generamos un dataframe de esa informacion y se le agregan las columnas operativas y auditoria, como por ejemplo el timestamp entre otras columnas; una vez con ese datafranme final, se ingesta directamente a hive sin realizar comparaciones con los datos que se tenga en HIVE.

#### Cargas Deltas
Las cargas de manera **DELTA** funcionan de la siguiente manera, en este caso la logica que implemento fue de que en algunas fuentes en sus datos si se pudo encontrar trazabilidad en sus registros, por lo que si se puede saber cuando un registro fue dado de alta, cuando fue modificado e incluso cuando fue dado de baja, por lo que cuando una fuente llega, se transforma a un dataframe, se le agregan las columnas operativas y de auditoria y una vez que tengamos el dataframe final de la fuente, se procede a realizar varias validaciones con los datos que tengamos en la tabla de hive, esto para poder clasificar los registros que provengan del archivo que actualmente se procesa junto con el historico de hive; los registros se clasifican en 3 tipos utilizando la teoria de conjuntos : insert , delete, update.


- **INSERT**
  Para saber si un registro es de tipo insert, lo que se hace es que primero se leen ambos entradas, el del archivo y la tabla de hive, una vez que se cargaron ambas tablas y cada una en su dataframe correspondiente; en el dataframe del archivo con los registros mas recientes se le agrega una columna el cual es el hash_id y se calcula utilizando las columnas que se le pasan en los parametros, despues se procede a comparar el dataframe con los datos del archivo con la columna de hash_id contra la tabla de hive, ambas se comparan por medio del hash_id y los registros que existan en el dataframe del archivo y no existan en la tabla de hive son los que se clasifican como insert y se registran en la tabla de hive.


  - **UPDATE**
  Los update funcionan de la misma manera, una vez que ya se tengan ambos dataframes, y el dataframe de los datos de archivo ya tengan la columna de hash_id, se procede a clasificar los datos del archivo contra los de la tabla de hive, el metodo que utiliza es de que los registros que existen en el dataframe del archivo y tambien existen en el dataframe de la tabla en hive por medio del hash_id, y a la vez los registros del dataframe del archivo tengan alguna columna diferente que no sea el hash_id,ni columnas operativas y auditoria con los del dataframe de hive, son lo que se clasifican como update.
  De una manera sencilla son todos los registros del archivo que existan en hive y tengan una columna diferente.

  - **DELETE**
  Los delete, la manera en que se clasifican es de acuerdo a ambos dataframes, el df del archivo y el df de la tabla de hive, de igual manera se comparan por el hash_id,  y la logica que se utiliza es de que los registros que existan en la tabla de hive y no existan en df del archivo, son los que se clasifican como delete.


  #### Nota


Hay que tomar en cuenta que por cada carga de los datos fuentes del archivo puede variar lo que se registra en hive, ya que hay que validar los delete, update e insert, pero como tal los insert y update son datos que se toman del archivo fuente, y los delete se toman de hive de acuerdo a logica implementada, tambien esta el caso de que en el archivo fuente contiene datos que ya existen en hive, pero no cambio nada y el hash_id sigue siendo el mismo, esos datos pasan como ignorados es decir no se registran en hive ya que no son insert, update o delete.


El ciclo de vidad de un registro es el siguiente: si no existe en la tabla hive se registra como insert, mientras el registro venga en el archivo, no tenga ningun cambio y este registrado en hive pasa como ignorado(no se vuelve a registrar en hive), cuando el registro este en el archivo pero en alguna de sus columnas cambio con respecto a lo registrado en hive entonces se registra en hive como update, y por ultimo si el registro deja de venir en el archivo pero ya estuvo registrado en hive entonces se registra en hive como delete.

## Cifras Control:

Dentro del proceso de spark tambien se cargan las cifras control y se registran en avro en un directorio del hdfs que se le pasan por parametros, estas cifras contro se generan de acuerdo a las cifras que genera en nifi solo se complementa con datos de conteos que genera spark, por ejemplo los datos de entrada, los insert, update y delete, etc.

## Argumentos para deploy de Spark Submit

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
| parametro15 | 4        

## Compilacion del proyecto maven y generar Jar
Para generar el jar con dependencias con el codigo fuente de spark se utilizo maven, maven es un herramienta para gestionar proyectos de java, scala con el cual es mas facil mantener un control de versiones y dependencias que se utilizan de acuerdo a la version que de SPARK y scala.

Una vez que tengamos el codigo fuente con spark en scala, y tengamos todas las dependencias necesarias agregadas en el archivo pom.xml, se procede a ejecutar el template de maven, como tal maven genera jars sin dependencias, por lo que se tuvo que agregar una configuracion en especial para que al momento de generar el jar, te lo genere con las dependencias establecidas, el comando es el siguiente:

```mvn clean package```



## Referencias al Framework de Ingestion

- [Framework de Ingestion](../Globales/)

## Codigo Fuente Local

- [Codigo Fuente ](src/)



[img1]: ../Globales/ArquitecturaFrameworkIngestion/images/axity.png "Logo Axity"
[img2]: ../Globales/ArquitecturaFrameworkIngestion/images/att.png "Logo AT&T"
