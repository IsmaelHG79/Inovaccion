![EncabezadoAxity][img1]

# Documentación Data Ingestion para la fuente ATT **CERAGON**

La ingesta de la fuente CERAGON requirió la construcción de varios flujos de NiFi debido a que en el repositorio de origen existen archivos con estructuras distintas y que deben de guardarse en tablas separadas:

![Flujo NiFi CERAGON][img2]

Vista general del flujo **G - CERAGON**

 Esta fuente se compone de cinco flujos de NiFi que ingestan nueve tipos distintos de archivos, que se separan de la siguiente manera:

 <a name="main"></a>

1. **PERFORMANCE**
    * [MSE Performance](#mse)
    * [AMC Performance](#amc)
    * [Eth Performance](#eth)
    * [Power Levels Performance](#power)
    * [G826 Performance](#g826)

El detalle del flujo se especifica en el apartado de [Performance](#performance).

![Grupo Performance][img3]

Vista general de **G - INVENTORYDUMP**

2. **TRANSMISSION INVENTORY**
    * [Transmission_Inventory](#transmission)

![Grupo Transmission Inventory][img4]

Vista general de **G - TRANSMISSION**

3. **HW INVENTORY**
    * [HW_Inventory](#hw)

![Grupo pfm_output][img5]

Vista general de **G - HW INVENTORY**

4. **ETHERNET PERFORMANCE**
    * [EthernetPerformancereport](#ethernet)

![Grupo Ethernet Performance][img6]

Vista general de **G - ETHERNET PERFORMANCE**

5. **RADIO PERFORMANCE**
    * [RadioPerformancereport](#radio)

![Grupo Radio Performance][img7]

Vista general de **G - RADIO PERFORMANCE**


El detalle de cada uno de los flujos será explicado con mas detalle en los siguientes apartados.

## Descripcion del `FTP`

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14481174), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

En el directorio del SFTP todos los archivos de CERAGON viven en un misma carpeta, por lo que el flujo esta configurado para buscar los archivos de forma recursiva usando la siguiente expresión regular en el procesador GetSFTP:

```
(?=<archivo>).*.zip$
```

En esta expresion se buscan las primeras palabras con las que inicia el nombre del archivo a cargar y que aparecen como `<archivo>`, además la expresión confirma que el archivo tenga una extension `.zip`. Hay dos archivos de origen que se depositan en el SFTP como archivos `.csv`, estos son EthernetPerformancereport y RadioPerformancereport por lo que se reemplaza el `.zip` por `.csv`. 

![Procesador GetSFTP][img8]

Vista del procesador **GetSFTP**

<a name="performance"></a>
## CERAGON Performance

La fuente se compone de cinco archivos con estructuras idénticas, por lo que se usa el mismo flujo para depositarlas en una sola tabla.   La fuente original tiene un campo llamado `PMP Type` que indica el origen de los datos, por lo tanto no es necesario aregar una columna artificial que los identifique.

- **Descripción:**
  La descripción de la fuente puede consultarse en el [EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Diccionario de datos:**
A continuación se detalla el estado de la tabla de Hive `tx_ceragon_performance`, en la cual se depositan los datos:

| col_name                     | data_type | comment                                             |
|------------------------------|-----------|-----------------------------------------------------|
| pmp_type                     | string    | Type inferred from 'Ethernet Utilization IP-10 24h' |
| granularity_seconds          | string    | Type inferred from '86400'                          |
| managed_element_user_label   | string    | Type inferred from 'Las Piedras Dir: Plateros'      |
| resource__display_path       | string    | Type inferred from 'ETH-HSB12.Radio'                |
| parameter__name_of_parameter | string    | Type inferred from 'Average'                        |
| value                        | string    | Type inferred from '0'                              |
| unit                         | string    | Type inferred from 'percent'                        |
| status                       | string    | Type inferred from 'Valid'                          |
| period_start_time_system     | string    | Type inferred from '2019-10-31 00:00:58.212'        |
| period_start_time_ne         | string    | Type inferred from '2019-10-29 18:00:00.000'        |
| period_end_time_system       | string    | Type inferred from '2019-10-31 00:00:58.212'        |
| period_end_time_ne           | string    | Type inferred from '2019-10-30 18:00:00.000'        |

Las siguientes columnas son datos de control que se insertan al momento de la ingesta para identificar a la fuente o que se usan durante la ejecución del proceso Spark, el archivo original no las incluye. Por ser las mismas columnas para todos los flujos de NiFi solo se listarán una vez aunque todas las tablas de CERAGON los llevan:

| col_name           | data_type | comment                                                  |
|--------------------|-----------|----------------------------------------------------------|
| filedate           | bigint    | Type inferred from '20191105'                            |
| filename           | string    | Type inferred from 'Eth_Performance_2019_11_05_2230.csv' |
| hash_id            | string    | Type inferred from 'null'                                |
| sourceid           | string    | Type inferred from 'CERAGON'                             |
| registry_state     | string    | Type inferred from 'null'                                |
| datasetname        | string    | Type inferred from 'ceragon_performance'                 |
| timestamp          | bigint    | Type inferred from '20191210'                            |
| transaction_status | string    | Type inferred from 'null'                                |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA](../RCI_DataAnalysis/eda/Gestor_U2000).

- **Particiones**

    Las particiones de la tabla **tx_ceragon_performance** se generan de forma diaria usando el campo de auditoría **filedate**, al momento de escribir este documento la tabla tiene un total de 328 particiones, que van del 01-ene-2019 al 24-nov-2019. A continuación se presentan algunas de las particiones creadas en la tabla: 
    
    Sentencia `show partitions tx_ceragon_performance`:

| year  | month | day | #Rows    | #Files | Size     | Format | Location                                                                                       |
|-------|-------|-----|----------|--------|----------|--------|------------------------------------------------------------------------------------------------|
| 2019  | 11    | 1   | 225781   | 4      | 93.77MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=1  |
| 2019  | 11    | 2   | 225581   | 4      | 93.69MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=2  |
| 2019  | 11    | 3   | 225357   | 4      | 93.59MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=3  |
| 2019  | 11    | 4   | 225756   | 4      | 93.76MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=4  |
| 2019  | 11    | 5   | 225562   | 4      | 93.68MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=5  |
| 2019  | 11    | 6   | 225318   | 4      | 93.57MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=6  |
| 2019  | 11    | 7   | 225672   | 4      | 93.72MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=7  |
| 2019  | 11    | 8   | 225470   | 4      | 93.64MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=8  |
| 2019  | 11    | 9   | 225194   | 4      | 93.52MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=9  |
| 2019  | 11    | 10  | 374509   | 5      | 156.59MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=10 |
| 2019  | 11    | 11  | 374163   | 5      | 156.45MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=11 |
| 2019  | 11    | 12  | 375099   | 6      | 156.89MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=12 |
| 2019  | 11    | 13  | 375909   | 5      | 157.22MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=13 |
| 2019  | 11    | 14  | 374359   | 5      | 156.59MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=14 |
| 2019  | 11    | 15  | 373789   | 5      | 156.35MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=15 |
| 2019  | 11    | 16  | 374515   | 5      | 156.65MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=16 |
| 2019  | 11    | 17  | 374197   | 5      | 156.51MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=17 |
| 2019  | 11    | 18  | 373777   | 6      | 156.34MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=18 |
| 2019  | 11    | 19  | 374732   | 5      | 156.73MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=19 |
| 2019  | 11    | 20  | 374758   | 5      | 156.74MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=20 |
| 2019  | 11    | 21  | 374433   | 5      | 156.60MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=21 |
| 2019  | 11    | 22  | 374777   | 6      | 156.76MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=22 |
| 2019  | 11    | 23  | 374299   | 5      | 156.54MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=23 |
| 2019  | 11    | 24  | 373645   | 5      | 156.27MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/performance/year=2019/month=11/day=24 |
| Total |      |    | 11443627 | 755    | 4.65GB   |       |                                                                                               |
<a name="amc"></a>
### AMC_Performance

Debido a que en la misma particion se cargan varios tipos de archivos no es posible distinguir las particiones de una sola fuente, por lo que se usa el siguiente query para identificar los registros insertados por partición para la fuente `AMC Performance`:

```
select year, month, day, count(*) as '#Rows'
from tx_ceragon_performance 
where pmp_type = 'ACM Profile 24h'
group by year, month, day
order by year asc, month asc, day asc;
```
El resultado es la siguiente tabla:

| year | month | day | #rows | Format |
|------|-------|-----|-------|--------|
| 2019 | 10    | 1   | 71438 | AVRO   |
| 2019 | 10    | 2   | 71584 | AVRO   |
| 2019 | 10    | 3   | 71494 | AVRO   |
| 2019 | 10    | 4   | 71468 | AVRO   |
| 2019 | 10    | 5   | 71534 | AVRO   |
| 2019 | 10    | 6   | 71438 | AVRO   |
| 2019 | 10    | 7   | 71334 | AVRO   |
| 2019 | 10    | 8   | 71418 | AVRO   |
| 2019 | 10    | 9   | 71336 | AVRO   |
| 2019 | 10    | 10  | 71234 | AVRO   |
| 2019 | 10    | 11  | 71304 | AVRO   |
| 2019 | 10    | 12  | 71220 | AVRO   |
| 2019 | 10    | 13  | 71132 | AVRO   |
| 2019 | 10    | 14  | 71244 | AVRO   |
| 2019 | 10    | 15  | 71264 | AVRO   |
| 2019 | 10    | 16  | 71162 | AVRO   |
| 2019 | 10    | 17  | 71240 | AVRO   |
| 2019 | 10    | 18  | 71160 | AVRO   |
| 2019 | 10    | 19  | 71050 | AVRO   |
| 2019 | 10    | 20  | 71148 | AVRO   |
| 2019 | 10    | 21  | 71054 | AVRO   |
| 2019 | 10    | 22  | 70956 | AVRO   |
| 2019 | 10    | 23  | 71038 | AVRO   |
| 2019 | 10    | 24  | 70988 | AVRO   |
| 2019 | 10    | 25  | 70900 | AVRO   |
| 2019 | 10    | 26  | 71022 | AVRO   |
| 2019 | 10    | 27  | 70938 | AVRO   |
| 2019 | 10    | 28  | 68814 | AVRO   |
| 2019 | 10    | 29  | 68818 | AVRO   |
| 2019 | 10    | 30  | 68260 | AVRO   |
| 2019 | 10    | 31  | 70770 | AVRO   |
| 2019 | 11    | 1   | 70880 | AVRO   |
| 2019 | 11    | 2   | 70830 | AVRO   |
| 2019 | 11    | 3   | 70752 | AVRO   |
| 2019 | 11    | 4   | 70866 | AVRO   |
| 2019 | 11    | 5   | 70816 | AVRO   |
| 2019 | 11    | 6   | 70728 | AVRO   |
| 2019 | 11    | 7   | 70828 | AVRO   |
| 2019 | 11    | 8   | 70766 | AVRO   |
| 2019 | 11    | 9   | 70678 | AVRO   |
| 2019 | 11    | 10  | 70774 | AVRO   |
| 2019 | 11    | 11  | 70710 | AVRO   |
| 2019 | 11    | 12  | 70862 | AVRO   |
| 2019 | 11    | 13  | 70994 | AVRO   |
| 2019 | 11    | 14  | 70684 | AVRO   |
| 2019 | 11    | 15  | 70582 | AVRO   |
| 2019 | 11    | 16  | 70704 | AVRO   |
| 2019 | 11    | 17  | 70646 | AVRO   |
| 2019 | 11    | 18  | 70582 | AVRO   |
| 2019 | 11    | 19  | 70796 | AVRO   |
| 2019 | 11    | 20  | 70754 | AVRO   |
| 2019 | 11    | 21  | 70704 | AVRO   |
| 2019 | 11    | 22  | 70756 | AVRO   |
| 2019 | 11    | 23  | 70658 | AVRO   |
| 2019 | 11    | 24  | 70542 | AVRO   |

<a name="eth"></a>
### Eth_Performance

Debido a que en la misma particion se cargan varios tipos de archivos no es posible distinguir las particiones de una sola fuente, por lo que se usa el siguiente query para identificar los registros insertados por partición para la fuente `Eth Performance`:

```
select year, month, day, count(*) as '#Rows'
from tx_ceragon_performance 
where pmp_type = 'Ethernet Utilization IP-10 24h'
group by year, month, day
order by year asc, month asc, day asc;
```
El resultado es la siguiente tabla:

| year | month | day | #rows | Format |
|------|-------|-----|-------|--------|
| 2019 | 10    | 1   | 894   | AVRO   |
| 2019 | 10    | 2   | 894   | AVRO   |
| 2019 | 10    | 3   | 890   | AVRO   |
| 2019 | 10    | 4   | 888   | AVRO   |
| 2019 | 10    | 5   | 888   | AVRO   |
| 2019 | 10    | 6   | 886   | AVRO   |
| 2019 | 10    | 7   | 888   | AVRO   |
| 2019 | 10    | 8   | 886   | AVRO   |
| 2019 | 10    | 9   | 882   | AVRO   |
| 2019 | 10    | 10  | 878   | AVRO   |
| 2019 | 10    | 11  | 876   | AVRO   |
| 2019 | 10    | 12  | 890   | AVRO   |
| 2019 | 10    | 13  | 894   | AVRO   |
| 2019 | 10    | 14  | 898   | AVRO   |
| 2019 | 10    | 15  | 904   | AVRO   |
| 2019 | 10    | 16  | 912   | AVRO   |
| 2019 | 10    | 17  | 914   | AVRO   |
| 2019 | 10    | 18  | 914   | AVRO   |
| 2019 | 10    | 19  | 914   | AVRO   |
| 2019 | 10    | 20  | 912   | AVRO   |
| 2019 | 10    | 21  | 912   | AVRO   |
| 2019 | 10    | 22  | 912   | AVRO   |
| 2019 | 10    | 23  | 912   | AVRO   |
| 2019 | 10    | 24  | 912   | AVRO   |
| 2019 | 10    | 25  | 914   | AVRO   |
| 2019 | 10    | 26  | 914   | AVRO   |
| 2019 | 10    | 27  | 914   | AVRO   |
| 2019 | 10    | 28  | 914   | AVRO   |
| 2019 | 10    | 29  | 913   | AVRO   |
| 2019 | 10    | 30  | 865   | AVRO   |
| 2019 | 10    | 31  | 865   | AVRO   |
| 2019 | 11    | 1   | 867   | AVRO   |
| 2019 | 11    | 2   | 867   | AVRO   |
| 2019 | 11    | 3   | 867   | AVRO   |
| 2019 | 11    | 4   | 868   | AVRO   |
| 2019 | 11    | 5   | 868   | AVRO   |
| 2019 | 11    | 6   | 868   | AVRO   |
| 2019 | 11    | 7   | 868   | AVRO   |
| 2019 | 11    | 8   | 868   | AVRO   |
| 2019 | 11    | 9   | 868   | AVRO   |
| 2019 | 11    | 10  | 868   | AVRO   |
| 2019 | 11    | 11  | 868   | AVRO   |
| 2019 | 11    | 12  | 868   | AVRO   |
| 2019 | 11    | 13  | 868   | AVRO   |
| 2019 | 11    | 14  | 844   | AVRO   |
| 2019 | 11    | 15  | 840   | AVRO   |
| 2019 | 11    | 16  | 836   | AVRO   |
| 2019 | 11    | 17  | 832   | AVRO   |
| 2019 | 11    | 18  | 828   | AVRO   |
| 2019 | 11    | 19  | 824   | AVRO   |
| 2019 | 11    | 20  | 828   | AVRO   |
| 2019 | 11    | 21  | 836   | AVRO   |
| 2019 | 11    | 22  | 840   | AVRO   |
| 2019 | 11    | 23  | 844   | AVRO   |
| 2019 | 11    | 24  | 848   | AVRO   |

<a name="mse"></a>
### MSE_Performance

Debido a que en la misma particion se cargan varios tipos de archivos no es posible distinguir las particiones de una sola fuente, por lo que se usa el siguiente query para identificar los registros insertados por partición para la fuente `MSE Performance`:

```
select year, month, day, count(*) as '#Rows'
from tx_ceragon_performance 
where pmp_type = 'MSE 24h'
group by year, month, day
order by year asc, month asc, day asc;
```
El resultado es la siguiente tabla:

| year | month | day | #rows | Format |
|------|-------|-----|-------|--------|
| 2019 | 10    | 1   | 726   | AVRO   |
| 2019 | 10    | 2   | 702   | AVRO   |
| 2019 | 10    | 3   | 744   | AVRO   |
| 2019 | 10    | 4   | 712   | AVRO   |
| 2019 | 10    | 5   | 668   | AVRO   |
| 2019 | 10    | 6   | 728   | AVRO   |
| 2019 | 10    | 7   | 704   | AVRO   |
| 2019 | 10    | 8   | 674   | AVRO   |
| 2019 | 10    | 9   | 730   | AVRO   |
| 2019 | 10    | 10  | 714   | AVRO   |
| 2019 | 10    | 11  | 684   | AVRO   |
| 2019 | 10    | 12  | 746   | AVRO   |
| 2019 | 10    | 13  | 706   | AVRO   |
| 2019 | 10    | 14  | 670   | AVRO   |
| 2019 | 10    | 15  | 752   | AVRO   |
| 2019 | 10    | 16  | 700   | AVRO   |
| 2019 | 10    | 17  | 664   | AVRO   |
| 2019 | 10    | 18  | 740   | AVRO   |
| 2019 | 10    | 19  | 692   | AVRO   |
| 2019 | 10    | 20  | 658   | AVRO   |
| 2019 | 10    | 21  | 730   | AVRO   |
| 2019 | 10    | 22  | 680   | AVRO   |
| 2019 | 10    | 23  | 648   | AVRO   |
| 2019 | 10    | 24  | 716   | AVRO   |
| 2019 | 10    | 25  | 676   | AVRO   |
| 2019 | 10    | 26  | 650   | AVRO   |
| 2019 | 10    | 27  | 2624  | AVRO   |
| 2019 | 10    | 28  | 12    | AVRO   |
| 2019 | 10    | 29  | 712   | AVRO   |
| 2019 | 10    | 30  | 686   | AVRO   |
| 2019 | 10    | 31  | 692   | AVRO   |
| 2019 | 11    | 1   | 760   | AVRO   |
| 2019 | 11    | 2   | 730   | AVRO   |
| 2019 | 11    | 3   | 712   | AVRO   |
| 2019 | 11    | 4   | 784   | AVRO   |
| 2019 | 11    | 5   | 748   | AVRO   |
| 2019 | 11    | 6   | 740   | AVRO   |
| 2019 | 11    | 7   | 810   | AVRO   |
| 2019 | 11    | 8   | 782   | AVRO   |
| 2019 | 11    | 9   | 754   | AVRO   |
| 2019 | 11    | 10  | 830   | AVRO   |
| 2019 | 11    | 11  | 800   | AVRO   |
| 2019 | 11    | 12  | 776   | AVRO   |
| 2019 | 11    | 13  | 890   | AVRO   |
| 2019 | 11    | 14  | 846   | AVRO   |
| 2019 | 11    | 15  | 834   | AVRO   |
| 2019 | 11    | 16  | 950   | AVRO   |
| 2019 | 11    | 17  | 930   | AVRO   |
| 2019 | 11    | 18  | 878   | AVRO   |
| 2019 | 11    | 19  | 962   | AVRO   |
| 2019 | 11    | 20  | 938   | AVRO   |
| 2019 | 11    | 21  | 908   | AVRO   |
| 2019 | 11    | 22  | 944   | AVRO   |
| 2019 | 11    | 23  | 924   | AVRO   |
| 2019 | 11    | 24  | 878   | AVRO   |

<a name="power"></a>
### Power_Levels_Performance

Debido a que en la misma particion se cargan varios tipos de archivos no es posible distinguir las particiones de una sola fuente, por lo que se usa el siguiente query para identificar los registros insertados por partición para la fuente `Power Levels Performance`:

```
select year, month, day, count(*) as '#Rows'
from tx_ceragon_performance 
where pmp_type = 'Power Levels IP-10 24h' 
      or pmp_type = 'Power Levels IP-20 24h'
group by year, month, day
order by year asc, month asc, day asc;
```

Hay que considerar que a diferencia de las demás fuentes que maneja este procesador, en vez de un solo valor existen dos en el campo `pmp_type`, estos son `Power Levels IP-10 24h` y `Power Levels IP-20 24h`. El resultado es la siguiente tabla:

| year | month | day | #rows  | Format |
|------|-------|-----|--------|--------|
| 2019 | 11    | 10  | 148951 | AVRO   |
| 2019 | 11    | 11  | 148835 | AVRO   |
| 2019 | 11    | 12  | 149087 | AVRO   |
| 2019 | 11    | 13  | 149387 | AVRO   |
| 2019 | 11    | 14  | 148791 | AVRO   |
| 2019 | 11    | 15  | 148519 | AVRO   |
| 2019 | 11    | 16  | 148759 | AVRO   |
| 2019 | 11    | 17  | 148651 | AVRO   |
| 2019 | 11    | 18  | 148471 | AVRO   |
| 2019 | 11    | 19  | 148691 | AVRO   |
| 2019 | 11    | 20  | 148879 | AVRO   |
| 2019 | 11    | 21  | 148731 | AVRO   |
| 2019 | 11    | 22  | 148863 | AVRO   |
| 2019 | 11    | 23  | 148691 | AVRO   |
| 2019 | 11    | 24  | 148415 | AVRO   |

<a name="g826"></a>
### G826_Performance

Debido a que en la misma particion se cargan varios tipos de archivos no es posible distinguir las particiones de una sola fuente, por lo que se usa el siguiente query para identificar los registros insertados por partición para la fuente `G826 Performance`:

```
select year, month, day, count(*) as '#Rows'
from tx_ceragon_performance 
where pmp_type = 'G.826 Radio Aggregate 24h'
group by year, month, day
order by year asc, month asc, day asc;
```

El resultado es la siguiente tabla:

| year | month | day | #rows  | Format |
|------|-------|-----|--------|--------|
| 2019 | 11    | 1   | 153274 | AVRO   |
| 2019 | 11    | 2   | 153154 | AVRO   |
| 2019 | 11    | 3   | 153026 | AVRO   |
| 2019 | 11    | 4   | 153238 | AVRO   |
| 2019 | 11    | 5   | 153130 | AVRO   |
| 2019 | 11    | 6   | 152982 | AVRO   |
| 2019 | 11    | 7   | 153166 | AVRO   |
| 2019 | 11    | 8   | 153054 | AVRO   |
| 2019 | 11    | 9   | 152894 | AVRO   |
| 2019 | 11    | 10  | 153086 | AVRO   |
| 2019 | 11    | 11  | 152950 | AVRO   |
| 2019 | 11    | 12  | 153506 | AVRO   |
| 2019 | 11    | 13  | 153770 | AVRO   |
| 2019 | 11    | 14  | 153194 | AVRO   |
| 2019 | 11    | 15  | 153014 | AVRO   |
| 2019 | 11    | 16  | 153266 | AVRO   |
| 2019 | 11    | 17  | 153138 | AVRO   |
| 2019 | 11    | 18  | 153018 | AVRO   |
| 2019 | 11    | 19  | 153459 | AVRO   |
| 2019 | 11    | 20  | 153359 | AVRO   |
| 2019 | 11    | 21  | 153254 | AVRO   |
| 2019 | 11    | 22  | 153374 | AVRO   |
| 2019 | 11    | 23  | 153182 | AVRO   |
| 2019 | 11    | 24  | 152962 | AVRO   |

<a name="ethernet"></a>
### EthernetPerformance

Las particiones cargadas en la tabla `tx_ceragon_ethernet` son las siguientes:

| year  | month | day | #Rows   | #Files | Size     | Format | Location                                                                                    |
|-------|-------|-----|---------|--------|----------|--------|---------------------------------------------------------------------------------------------|
| 2019  | 1     | 9   | 562409  | 1      | 182.24MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=1/day=9   |
| 2019  | 3     | 11  | 77110   | 1      | 24.95MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=3/day=11  |
| 2019  | 3     | 18  | 75936   | 1      | 24.58MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=3/day=18  |
| 2019  | 3     | 25  | 77153   | 1      | 24.89MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=3/day=25  |
| 2019  | 4     | 8   | 75028   | 1      | 24.21MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=4/day=8   |
| 2019  | 4     | 15  | 77052   | 1      | 24.86MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=4/day=15  |
| 2019  | 4     | 22  | 77996   | 1      | 25.18MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=4/day=22  |
| 2019  | 4     | 29  | 78196   | 1      | 25.22MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=4/day=29  |
| 2019  | 5     | 6   | 77034   | 1      | 24.93MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=5/day=6   |
| 2019  | 5     | 13  | 75225   | 1      | 24.26MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=5/day=13  |
| 2019  | 5     | 20  | 73319   | 1      | 23.69MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=5/day=20  |
| 2019  | 5     | 27  | 75576   | 1      | 24.44MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=5/day=27  |
| 2019  | 8     | 6   | 712170  | 1      | 227.68MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=8/day=6   |
| 2019  | 10    | 22  | 697931  | 1      | 223.11MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=10/day=22 |
| 2019  | 10    | 28  | 1334    | 1      | 437.28KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/ethernet/year=2019/month=10/day=28 |
| Total | .     | .   | 2813469 | 15     | 904.67MB | .      | .                                                                                           |


<a name="radio"></a>
### RadioPerformance

Las particiones cargadas en la tabla `tx_ceragon_radio` son las siguientes:

| year  | month | day | #Rows   | #Files | Size     | Format | Location                                                                                 |
|-------|-------|-----|---------|--------|----------|--------|------------------------------------------------------------------------------------------|
| 2019  | 3     | 4   | 123269  | 1      | 44.78MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=3/day=4   |
| 2019  | 3     | 11  | 122155  | 1      | 44.49MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=3/day=11  |
| 2019  | 3     | 18  | 118061  | 1      | 43.00MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=3/day=18  |
| 2019  | 3     | 25  | 122098  | 1      | 44.47MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=3/day=25  |
| 2019  | 4     | 1   | 123567  | 1      | 45.01MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=4/day=1   |
| 2019  | 4     | 8   | 119808  | 1      | 43.64MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=4/day=8   |
| 2019  | 5     | 27  | 119405  | 1      | 43.84MB  | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=5/day=27  |
| 2019  | 7     | 5   | 1119    | 1      | 420.78KB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=7/day=5   |
| 2019  | 8     | 6   | 1188900 | 1      | 431.85MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=8/day=6   |
| 2019  | 10    | 22  | 1177688 | 1      | 428.88MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=10/day=22 |
| 2019  | 10    | 28  | 1165812 | 1      | 424.53MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=10/day=28 |
| 2019  | 11    | 15  | 1172162 | 1      | 426.84MB | AVRO   | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/CERAGON/radio/year=2019/month=11/day=15 |
| Total | .     | .   | 5554044 | 12     | 1.97GB   | 0B     | .                                                                                        |

## Componentes del procesos de ingestion:

### 1. Ingestion y Serialización via NiFi

Los datos son ingestados al Data Lake usando los siguientes flujos de NiFi:

- Para los archivos que se encuentran dentro del grupo **G - PERFORMANCE**:

| Procesador GetSFTP              | Fuente ingestada     |
|-------------------------|----------------------|
| G – GET MSE PERFORMANCE        | MSE_Performance…        |
| G – GET AMC PERFORMANCE           | AMC_Performance…           |
| G – GET ETH PERFORMANCE     | Eth_Performance…      |
| G – GET POWER PERFORMANCE         | Power_Levels…         |
| G – GET G826 PERFORMANCE     | G826_Performance…     |

- Para las archivos restantes:

| Flujo NiFi     | Fuente ingestada |
|----------------|------------------|
| G - TRANSMISSION | Transmission_Inventory …  |
| G - HW INVENTORY | HW_inventory…  |
| G - ETHERNET PERFORMANCE | EthernetPerformance_…  |
| G - RADIO PERFORMANCE | RadioPerformance…  |

Todos los flujos tienen la misma estructura generaL:

![Activo Fijo NiFi General View][img10]

Pipeline General NiFi

Los flujos varian entre ellos en los siguientes aspectos:
- El filtro del archivo a ingestar en el procesador GetSFTP como se describe en el apartado [Descripcion del FTP]().
- El campo `datasetName` que tiene que referenciar a su fuente de acuerdo a la lista que aparece al [inicio](#main) de este documento.
- El nombre del esquema de avro que se escribe en el SFTP (parámetro `var_HPathLogSchema`).
- La ruta de HDFS en donde se depositan los datos al final del proceso (parámetro `var_HPathData`).

![Activo Fijo NiFi Detail View][img11]

Detalle del Pipeline.

El flujo `G -PERFORMANCE` sigue el estándar del framework de ingestión, con la excepción de que en vez de tener un solo procesador `GetSFTP` se manejan cinco, cada uno apuntando a un tipo de archivo distinto; una vez que los archivos llegan al flujo de NiFi se unen usando un funel, esto es posible porque los cinco archivos tienen la misma estructura:

![GetSFTP en G- PERFORMANCE][img9]

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

| Flujo NiFi               | Archivo a ingestar       | Valor | Ejemplo                             |
|--------------------------|--------------------------|-------|-------------------------------------|
| G – PERFORMANCE          | AMC_Performance          | 52    | ./rci_ingesta_generacion_avro.sh 52 |
| G – PERFORMANCE          | Eth_Performance          | 52    | ./rci_ingesta_generacion_avro.sh 52 |
| G – PERFORMANCE          | G826_Performance         | 52    | ./rci_ingesta_generacion_avro.sh 52 |
| G – PERFORMANCE          | MSE_Performance          | 52    | ./rci_ingesta_generacion_avro.sh 52 |
| G – PERFORMANCE          | Power Levels Performance | 52    | ./rci_ingesta_generacion_avro.sh 52 |
| G – ETHERNET PERFORMANCE | EthernetPerformance      | 53    | ./rci_ingesta_generacion_avro.sh 53 |
| G – RADIO PERFORMANCE    | RadioPerformance         | 54    | ./rci_ingesta_generacion_avro.sh 54 |
| G – TRANSMISSION         | Transmission_Inventory   | 55    | ./rci_ingesta_generacion_avro.sh 55 |
| G – HW INVENTORY         | HW_Inventory             | 56    | ./rci_ingesta_generacion_avro.sh 56 |

Ejemplo para el flujo NiFi `G – ETHERNET PERFORMANCE `:

```
./rci_ingesta_generacion_avro.sh 53
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

| Flujo NiFi               |  Archivo a ingestar      |  Valor de `parametro3`  |  Valor de `parametro7`                  |  Valor de `parametro8`  |  Valor de `parametro11`                                                                                          |  Valor de `parametro12`                                       |  Valor de `parametro13`                                           |
|--------------------------|--------------------------|-------------------------|-----------------------------------------|-------------------------|------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|-------------------------------------------------------------------|
| G – PERFORMANCE          | AMC_Performance          | Delta Spark Ceragon AMC | /data/RCI/raw/CERAGON/data/performance  | tx_ceragon_performance  | Managed_Element_user_label,Resource__display_path,Parameter__name_of_parameter,Period_Start_Time_System,filedate | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_performance.avro  | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_performance/20191210  |
| G – PERFORMANCE          | Eth_Performance          | Delta Spark Ceragon Eth | /data/RCI/raw/CERAGON/data/performance  | tx_ceragon_performance  | Managed_Element_user_label,Resource__display_path,Parameter__name_of_parameter,Period_Start_Time_System,filedate | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_performance.avro  | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_performance/20191210  |
| G – PERFORMANCE          | G826_Performance         | Delta Spark Ceragon G82 | /data/RCI/raw/CERAGON/data/performance  | tx_ceragon_performance  | Managed_Element_user_label,Resource__display_path,Parameter__name_of_parameter,Period_Start_Time_System,filedate | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_performance.avro  | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_performance/20191210  |
| G – PERFORMANCE          | MSE_Performance          | Delta Spark Ceragon MSE | /data/RCI/raw/CERAGON/data/performance  | tx_ceragon_performance  | Managed_Element_user_label,Resource__display_path,Parameter__name_of_parameter,Period_Start_Time_System,filedate | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_performance.avro  | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_performance/20191210  |
| G – PERFORMANCE          | Power Levels Performance | Delta Spark Ceragon Pow | /data/RCI/raw/CERAGON/data/performance  | tx_ceragon_performance  | Managed_Element_user_label,Resource__display_path,Parameter__name_of_parameter,Period_Start_Time_System,filedate | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_performance.avro  | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_performance/20191210  |
| G – ETHERNET PERFORMANCE | EthernetPerformance      | Delta Spark Ceragon Eth | /data/RCI/raw/CERAGON/data/ethernet     | tx_ceragon_ethernet     | Date,IP,filedate                                                                                                 | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_ethernet.avro     | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_ethernet/20191210     |
| G – RADIO PERFORMANCE    | RadioPerformance         | Delta Spark Ceragon Rad | /data/RCI/raw/CERAGON/data/radio        | tx_ceragon_radio        | Date,IP,filedate                                                                                                 | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_radio.avro        | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_radio/20191210        |
| G – TRANSMISSION         | Transmission_Inventory   | Delta Spark Ceragon Tra | /data/RCI/raw/CERAGON/data/transmission | tx_ceragon_transmission | Resource_Name,Rx_Frequency_MHz,filedate                                                                          | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_transmission.avro | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_transmission/20191210 |
| G – HW INVENTORY         | HW_Inventory             | Delta Spark Ceragon HW_ | /data/RCI/raw/CERAGON/data/hw           | tx_ceragon_hw           | Resource_Name,Article_Code,Serial_No,filedate                                                                    | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_hw.avro           | /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_hw/20191211           |

Los demás parametros se configuran igual para todos los flujos de NiFi de CERAGON.

Ejemplo para el flujo `G - RADIO PERFORMANCE`:

```
spark-submit --master yarn-cluster --deploy-mode cluster --name 'Delta SPARK' --queue=root.rci --class com.axity.DataFlowIngestion /home/fh967x/SparkNew/spark-scala-maven-project-0.0.1-SNAPSHOT-jar-with-dependencies.jar /data/RCI/raw/CERAGON/data/radio tx_ceragon_radio hash_id hive Date,IP,filedate /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_radio.avro /data/RCI/stg/hive/work/ctl/ctrl_tx_ceragon_radio/20191210 full 1

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

[img1]: images/CERAGON-nifi-01.png "Logo Axity"
[img2]: images/CERAGON-nifi-02.png "Grupo G - CERAGON"
[img3]: images/CERAGON-nifi-03.png "Grupo G - PERFORMANCE"
[img4]: images/CERAGON-nifi-04.png "Grupo G- TRANSMISSION"
[img5]: images/CERAGON-nifi-05.png "Grupo G - HW INVENTORY"
[img6]: images/CERAGON-nifi-06.png "Grupo G - ETHERNET PERFORMANCE"
[img7]: images/CERAGON-nifi-07.png "Grupo G - RADIO PERFORMANCE"
[img8]: images/CERAGON-nifi-08.png "Procesador GetSFTP"
[img9]: images/CERAGON-nifi-09.png "Detalle de GetSFTP para grupo G - PERFORMANCE"
[img10]: images/CERAGON-nifi-10.png "Vista general del flujo"
[img11]: images/CERAGON-nifi-11.png "Detalle del flujo de ingesta"