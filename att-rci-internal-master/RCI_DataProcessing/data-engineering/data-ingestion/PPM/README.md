![EncabezadoAxity][imgEncabezado]


# Documentación Data Ingestion para la fuente ATT **PPM**

Para esta fuente se documentan diferentes flujos de una sola fuente, esto debido a que existen diferentes tablas para su consumo.

## Descripción del `Orígen de Datos`  
Los datos de conexión son los siguientes:
```
BD:       Oracle
IP:       10.32.218.155
USR:      attnetworkinventory
Puerto:   1521
SID:      PPM
```

## Componentes del procesos de ingestión (Flujo General):

__Ingestión y Serialización via NiFi__

__Flujo Principal__

![TX_FM_APPROVED_BUDGETS][imgPPM1]

__Flujo de Subproceso__

![TX_FM_APPROVED_BUDGETS NiFi Vista General][imgPPM2]

![TX_FM_APPROVED_BUDGETS NiFi Vista Subproceso][imgPPM3]

__Ejecución de Consulta a BD__

![TX_FM_APPROVED_BUDGETS NiFi Vista Ejecución de Consulta a BD][imgPPM4]

__Limpieza y extracción de esquema Avro__

![TX_FM_APPROVED_BUDGETS NiFi Vista General][imgPPM9]

![TX_FM_APPROVED_BUDGETS NiFi Vista Procesamiento][imgPPM5]

__Envío de Esquema vía SFTP y HDFS__

![TX_FM_APPROVED_BUDGETS NiFi Vista Procesamiento][imgPPM6]

![TX_FM_APPROVED_BUDGETS NiFi Vista Procesamiento][imgPPM7]

__Inferencia de Esquema Avro__

![TX_FM_APPROVED_BUDGETS NiFi Vista Procesamiento][imgPPM8]

![TX_FM_APPROVED_BUDGETS NiFi Vista Procesamiento][imgPPM5]

__Envío de Archivo vía SFTP y HDFS__

![TX_FM_APPROVED_BUDGETS NiFi Vista Procesamiento][imgPPM6]

![TX_FM_APPROVED_BUDGETS NiFi Vista Procesamiento][imgPPM11]

__Cifra Control__

![TX_FM_APPROVED_BUDGETS NiFi Vista Procesamiento][imgPPM12]

![TX_FM_APPROVED_BUDGETS NiFi Vista Procesamiento][imgPPM13]

[imgPPM1]: images/PPM-nifi-00.png ""
[imgPPM2]: images/PPM-nifi-000.png ""
[imgPPM3]: images/PPM-nifi-01.png ""
[imgPPM4]: images/PPM-nifi-02.png ""
[imgPPM5]: images/PPM-nifi-03.png ""
[imgPPM6]: images/PPM-nifi-04.png ""
[imgPPM7]: images/PPM-nifi-05.png ""
[imgPPM8]: images/PPM-nifi-06.png ""
[imgPPM9]: images/PPM-nifi-07.png ""
[imgPPM10]: images/PPM-nifi-08.png ""
[imgPPM11]: images/PPM-nifi-10.png ""
[imgPPM12]: images/PPM-nifi-11.png ""
[imgPPM13]: images/PPM-nifi-12.png ""



## Listado de Tablas  

* [FM_APPROVED_BUDGETS](#FM_APPROVED_BUDGETS)
* [KCRT_FG_PFM_PROJECT](#KCRT_FG_PFM_PROJECT)
* [KCRT_FG_PROJ_ISSUE](#KCRT_FG_PROJ_ISSUE)
* [KCRT_FG_PROJ_RISK](#KCRT_FG_PROJ_RISK)
* [KCRT_FG_PROJ_SCOPE_CHANGE](#KCRT_FG_PROJ_SCOPE_CHANGE)
* [KCRT_REQ_HEADER_DETAILS](#KCRT_REQ_HEADER_DETAILS)
* [KCRT_REQUEST_DETAILS](#KCRT_REQUEST_DETAILS)
* [KCRT_REQUESTS](#KCRT_REQUESTS)
* [KCRT_REQUESTS_V](#KCRT_REQUESTS_V)
* [KCRT_STATUSES](#KCRT_STATUSES)
* [KDRV_PROJECT_BUDGET_COSTS_V](#KDRV_PROJECT_BUDGET_COSTS_V)
* [KNTA_NOTES_V](#KNTA_NOTES_V)
* [KNTA_REGIONS](#KNTA_REGIONS)
* [KNTA_USERS](#KNTA_USERS)
* [KWFL_STEP_TRANSACTIONS](#KWFL_STEP_TRANSACTIONS)
* [KWFL_WORKFLOW_INSTANCES](#KWFL_WORKFLOW_INSTANCES)
* [KWFL_WORKFLOW_STEPS_NLS](#KWFL_WORKFLOW_STEPS_NLS)
* [KWFL_WORKFLOWS_V](#KWFL_WORKFLOWS_V)
* [PFM_LIFECYCLE_PARENT_ENTITY](#PFM_LIFECYCLE_PARENT_ENTITY)
* [PFM_REQUEST_DETAILS_V](#PFM_REQUEST_DETAILS_V)
* [PGM_PROGRAM_CONTENT](#PGM_PROGRAM_CONTENT)
* [PGM_PROGRAMS](#PGM_PROGRAMS)
* [PM_EXCEPTION_RULE_RESULTS](#PM_EXCEPTION_RULE_RESULTS)
* [PM_PROJECT_ROLLUP](#PM_PROJECT_ROLLUP)
* [PM_PROJECT_TYPES](#PM_PROJECT_TYPES)
* [PM_PROJECTS](#PM_PROJECTS)
* [PM_WORK_PLANS](#PM_WORK_PLANS)
* [WP_TASK_ACTUALS](#WP_TASK_ACTUALS)
* [WP_TASK_INFO](#WP_TASK_INFO)
* [WP_TASK_SCHEDULE](#WP_TASK_SCHEDULE)
* [WP_TASKS](#WP_TASKS)




## <a name="FM_APPROVED_BUDGETS"></a>FM_APPROVED_BUDGETS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [FM_APPROVED_BUDGETS](../../../../RCI_DataAnalysis/eda/PPM/FM_APPROVED_BUDGETS/README.md)

- **Diccionario de Datos**
  [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/FM_APPROVED_BUDGETS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_fm_apporved_budgets```

    | Id 	| Nombre de Columna    	| Tipo de Dato|
    |----	|----------------------	|-----------	|
    | 1  	| approved_budget_id   	| string    	|
    | 2  	| created_by           	| string    	|
    | 3  	| creation_date        	| string    	|
    | 4  	| last_updated_by      	| string    	|
    | 5  	| last_update_date     	| string    	|
    | 6  	| version              	| string    	|
    | 7  	| name                 	| string    	|
    | 8  	| labor_type_code      	| string    	|
    | 9  	| category_code        	| string    	|
    | 10 	| expense_type_code    	| string    	|
    | 11 	| amount_lcl           	| string    	|
    | 12 	| amount_bse           	| string    	|
    | 13 	| approval_date        	| string    	|
    | 14 	| approved_by          	| string    	|
    | 15 	| notes                	| string    	|
    | 16 	| financial_summary_id 	| string    	|
    | 17 	| fiscal_period_id     	| string    	|
    | 18 	| synch_source_flag    	| string    	|
    | 19 	| source_fs_id         	| string    	|

  Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestión.

    | Id 	| Nombre de Columna     | Tipo de Dato|
    |----	|----------------------	|-----------	|
    | 20 	| filedate             	| bigint    	|
    | 21 	| filename             	| string    	|
    | 22 	| hash_id              	| string    	|
    | 23 	| sourceid             	| string    	|
    | 24 	| registry_state       	| string    	|
    | 25 	| datasetname          	| string    	|
    | 26 	| timestamp            	| bigint    	|
    | 27 	| transaction_status   	| string    	|    



- **Particiones**

    A continuación se presentan las particiones creadas de la tabla **tx_fm_approved_budgets**.

    Sentencia: ```show partitions rci_network_db.tx_fm_approved_budgets```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                                           	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------	|----------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 606   	| 1      	| 242.86KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/fm_approved_budgets/year=2019/month=12/day=25 	|


- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_fm_approved_budgets';
    ```    

  | id_execution 	| table_name             	| dateload 	| avro_name                                                                       	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|------------------------	|----------	|---------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_fm_approved_budgets 	| 20191225 	| /data/RCI/raw/ppm/fm_approved_budgets/data/20191225_tx_fm_approved_budgets.avro 	| 2019-12-25 11:21:15 	| 2019-12-25 11:21:58 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_fm_approved_budgets'
    and dateload = 20191225
    order by filedate asc;
    ```    

  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 606          	| fm_approved_budgets         	| 20191225 	| 20191225_tx_fm_approved_budgets.avro         	| PPM      	| 20191225 	| 606        	| 606          	| 0            	| 0            	|

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

Especificar parámetros del proceso kite:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 58   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 58
```


## <a name="KCRT_FG_PFM_PROJECT"></a>KCRT_FG_PFM_PROJECT

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KCRT_FG_PFM_PROJECT](../../../../RCI_DataAnalysis/eda/PPM/KCRT_FG_PFM_PROJECT/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KCRT_FG_PFM_PROJECT/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kcrt_fg_pfm_project```

     | Id 	| Nombre de Columna            	| Tipo de Dato 	|
     |----	|------------------------------	|--------------	|
     | 1  	| request_id                   	| string       	|
     | 2  	| request_type_id              	| string       	|
     | 3  	| project_name                 	| string       	|
     | 4  	| project_health_code          	| string       	|
     | 5  	| project_health_meaning       	| string       	|
     | 6  	| prj_business_unit_code       	| string       	|
     | 7  	| prj_business_unit_meaning    	| string       	|
     | 8  	| prj_business_objective_id    	| string       	|
     | 9  	| prj_business_objective_name  	| string       	|
     | 10 	| prj_project_class_code       	| string       	|
     | 11 	| prj_project_class_meaning    	| string       	|
     | 12 	| prj_asset_class_code         	| string       	|
     | 13 	| prj_asset_class_meaning      	| string       	|
     | 14 	| prj_project_manager_user_id  	| string       	|
     | 15 	| prj_project_manager_username 	| string       	|
     | 16 	| prj_project_id               	| string       	|
     | 17 	| prj_project_name             	| string       	|
     | 18 	| prj_project_url              	| string       	|
     | 19 	| prj_staff_prof_id            	| string       	|
     | 20 	| prj_staff_prof_name          	| string       	|
     | 21 	| prj_return_on_investment     	| string       	|
     | 22 	| prj_net_present_value        	| string       	|
     | 23 	| prj_custom_field_value       	| string       	|
     | 24 	| prj_value_rating             	| string       	|
     | 25 	| prj_risk_rating              	| string       	|
     | 26 	| prj_total_score              	| string       	|
     | 27 	| prj_discount_rate            	| string       	|
     | 28 	| prj_plan_start_period_id     	| string       	|
     | 29 	| prj_plan_finish_period_id    	| string       	|
     | 30 	| prj_plan_start_period_name   	| string       	|
     | 31 	| prj_plan_finish_period_name  	| string       	|
     | 32 	| prj_dependencies_code        	| string       	|
     | 33 	| prj_dependencies_meaning     	| string       	|
     | 34 	| prj_phase_code               	| string       	|
     | 35 	| prj_phase_meaning            	| string       	|
     | 36 	| prj_benefit_manager_user_id  	| string       	|
     | 37 	| prj_benefit_manager_username 	| string       	|
     | 38 	| prj_financial_summary_id     	| string       	|
     | 39 	| prj_financial_summary_name   	| string       	|
     | 40 	| prj_portfolio_id             	| string       	|
     | 41 	| prj_portfolio_name           	| string       	|
     | 42 	| prj_program_id               	| string       	|
     | 43 	| prj_program_name             	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna            	| Tipo de Dato 	|
     |----	|------------------------------	|--------------	|
     | 44 	| filedate                     	| bigint       	|
     | 45 	| filename                     	| string       	|
     | 46 	| hash_id                      	| string       	|
     | 47 	| sourceid                     	| string       	|
     | 48 	| registry_state               	| string       	|
     | 49 	| datasetname                  	| string       	|
     | 50 	| timestamp                    	| bigint       	|
     | 51 	| transaction_status           	| string       	|


- **Particiones**

  A continuación se presentan las particiones creadas de la tabla **tx_kcrt_fg_pfm_project**.

  Sentencia: ```show partitions rci_network_db.tx_kcrt_fg_pfm_project```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                                           	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------	|----------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 342   	| 1      	| 198.08KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/kcrt_fg_pfm_project/year=2019/month=12/day=25 	|

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_kcrt_fg_pfm_project';
  ```

  | id_execution 	| table_name             	| dateload 	| avro_name                                                                       	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|------------------------	|----------	|---------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_kcrt_fg_pfm_project 	| 20191225 	| /data/RCI/raw/ppm/kcrt_fg_pfm_project/data/20191225_tx_kcrt_fg_pfm_project.avro 	| 2019-12-25 12:46:55 	| 2019-12-25 12:47:37 	| 1      	|         	|                	| 0        	|   	|    

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_kcrt_fg_pfm_project'
  and dateload = 20191225
  order by filedate asc;
  ```      
  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 342          	| kcrt_fg_pfm_project         	| 20191225 	| 20191225_tx_kcrt_fg_pfm_project.avro         	| PPM      	| 20191225 	| 342        	| 342          	| 0            	| 0            	|

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 59   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 59
```


## <a name="KCRT_FG_PROJ_ISSUE"></a>KCRT_FG_PROJ_ISSUE

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KCRT_FG_PROJ_ISSUE](../../../../RCI_DataAnalysis/eda/PPM/KCRT_FG_PROJ_ISSUE/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KCRT_FG_PROJ_ISSUE/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kcrt_fg_proj_issue```

     | Id 	| Nombre de Columna             	| Tipo de Dato 	|
     |----	|----------------------	|-----------	|
     | 1 	| request_type_id          	| string 	|
     | 2 	| escalation_level_code    	| string 	|
     | 3 	| escalation_level_meaning 	| string 	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna             	| Tipo de Dato 	|
     |----	|----------------------	|-----------	|
     | 4 	| filedate             	| bigint    	|
     | 5 	| filename             	| string    	|
     | 6 	| hash_id              	| string    	|
     | 7 	| sourceid             	| string    	|
     | 8 	| registry_state       	| string    	|
     | 9 	| datasetname          	| string    	|
     | 10 | timestamp            	| bigint    	|
     | 11 | transaction_status   	| string    	|    


- **Particiones**

  A continuación se presentan las particiones creadas de la tabla **tx_kcrt_fg_proj_issue**.

  Sentencia: ```show partitions rci_network_db.tx_kcrt_fg_proj_issue```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                                          	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------	|---------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 622   	| 1      	| 143.55KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/kcrt_fg_proj_issue/year=2019/month=12/day=25 	|  

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_kcrt_fg_proj_issue';
  ```

  | id_execution 	| table_name            	| dateload 	| avro_name                                                                     	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|-----------------------	|----------	|-------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_kcrt_fg_proj_issue 	| 20191225 	| /data/RCI/raw/ppm/kcrt_fg_proj_issue/data/20191225_tx_kcrt_fg_proj_issue.avro 	| 2019-12-25 12:57:01 	| 2019-12-25 12:57:49 	| 1      	|         	|                	| 0        	|   	|    

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_kcrt_fg_proj_issue'
  and dateload = 20191225
  order by filedate asc;
  ```

  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 622          	| kcrt_fg_proj_issue          	| 20191225 	| 20191225_tx_kcrt_fg_proj_issue.avro          	| PPM      	| 20191225 	| 622        	| 622          	| 0            	| 0            	|     

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

      | Parámetro | Valor | Descripción|
      | ---------- | ---------- | ---------- |
      | parametro_01   | 60   | Valor de correspondiente al flujo|

       Sentencia kite:

      ```
      ./rci_ingesta_generacion_avro.sh {parametro_01}
      ```
      Ejemplo:

      ```
      ./rci_ingesta_generacion_avro.sh 60
      ```

## <a name="KCRT_FG_PROJ_RISK"></a>KCRT_FG_PROJ_RISK

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
  Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
  - **Descripción**
    [KCRT_FG_PROJ_RISK](../../../../RCI_DataAnalysis/eda/PPM/KCRT_FG_PROJ_RISK/README.md)

  - **Diccionario de Datos**
       [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KCRT_FG_PROJ_RISK/README.md)

       Sentencia: ```describe formatted rci_network_db.tx_kcrt_fg_proj_risk```

       | Id 	| Nombre de Columna             	| Tipo de Dato 	|
       |----	|-------------------------------	|--------------	|
       | 1  	| request_id                    	| string       	|
       | 2  	| request_type_id               	| string       	|
       | 3  	| probability_code              	| string       	|
       | 4  	| probability_meaning           	| string       	|
       | 5  	| risk_impact_level_code        	| string       	|
       | 6  	| risk_impact_level_meaning     	| string       	|
       | 7  	| risk_escalation_level_code    	| string       	|
       | 8  	| risk_escalation_level_meaning 	| string       	|

       Las siguientes columnas son creadas para la identidad de la fuente:

       | Id 	| Nombre de Columna  	| Tipo de Dato 	|
       |----	|--------------------	|--------------	|
       | 9  	| filedate           	| bigint       	|
       | 10 	| filename           	| string       	|
       | 11 	| hash_id            	| string       	|
       | 12 	| sourceid           	| string       	|
       | 13 	| registry_state     	| string       	|
       | 14 	| datasetname        	| string       	|
       | 15 	| timestamp          	| bigint       	|
       | 16 	| transaction_status 	| string       	|

  - **Particiones**

    A continuación se presentan las particiones creadas de la tabla **tx_kcrt_fg_proj_risk**.

    Sentencia: ```show partitions rci_network_db.tx_kcrt_fg_proj_risk```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                                         	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------	|--------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 1233  	| 1      	| 328.39KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/kcrt_fg_proj_risk/year=2019/month=12/day=25 	|

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_kcrt_fg_proj_risk';
  ```

  | id_execution 	| table_name           	| dateload 	| avro_name                                                                   	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|----------------------	|----------	|-----------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_kcrt_fg_proj_risk 	| 20191225 	| /data/RCI/raw/ppm/kcrt_fg_proj_risk/data/20191225_tx_kcrt_fg_proj_risk.avro 	| 2019-12-25 13:03:32 	| 2019-12-25 13:04:12 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_kcrt_fg_proj_risk'
  and dateload = 20191225
  order by filedate asc;
  ```
  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 1233         	| kcrt_fg_proj_risk           	| 20191225 	| 20191225_tx_kcrt_fg_proj_risk.avro           	| PPM      	| 20191225 	| 1233       	| 1233         	| 0            	| 0            	|

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

       | Parámetro | Valor | Descripción|
       | ---------- | ---------- | ---------- |
       | parametro_01   | 61   | Valor de correspondiente al flujo|

      Sentencia kite:

       ```
       ./rci_ingesta_generacion_avro.sh {parametro_01}
       ```
       Ejemplo:

       ```
       ./rci_ingesta_generacion_avro.sh 61
       ```

## <a name="KCRT_FG_PROJ_SCOPE_CHANGE"></a>KCRT_FG_PROJ_SCOPE_CHANGE

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KCRT_FG_PROJ_SCOPE_CHANGE](../../../../RCI_DataAnalysis/eda/PPM/KCRT_FG_PROJ_SCOPE_CHANGE/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KCRT_FG_PROJ_SCOPE_CHANGE/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kcrt_fg_proj_scope_change```

     | Id 	| Nombre de Columna              	| Tipo de Dato 	|
     |----	|--------------------------------	|--------------	|
     | 1  	| request_id                     	| string       	|
     | 2  	| request_type_id                	| string       	|
     | 3  	| impact_severity_code           	| string       	|
     | 4  	| impact_severity_meaning        	| string       	|
     | 5  	| cr_level_code                  	| string       	|
     | 6  	| cr_level_meaning               	| string       	|
     | 7  	| scope_escalation_level_code    	| string       	|
     | 8  	| scope_escalation_level_meaning 	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 9  	| filedate           	| bigint       	|
     | 10 	| filename           	| string       	|
     | 11 	| hash_id            	| string       	|
     | 12 	| sourceid           	| string       	|
     | 13 	| registry_state     	| string       	|
     | 14 	| datasetname        	| string       	|
     | 15 	| timestamp          	| bigint       	|
     | 16 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_kcrt_fg_proj_scope_change**.

 Sentencia: ```show partitions rci_network_db.tx_kcrt_fg_proj_scope_change```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size    	| Format 	| Incremental stats 	| Location                                                                                                 	|
  |------	|-------	|-----	|-------	|--------	|---------	|--------	|-------------------	|----------------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 269   	| 1      	| 70.94KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/kcrt_fg_proj_scope_change/year=2019/month=12/day=25 	|

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_kcrt_fg_proj_scope_change';
   ```

  | id_execution 	| table_name                   	| dateload 	| avro_name                                                                                   	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|------------------------------	|----------	|---------------------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_kcrt_fg_proj_scope_change 	| 20191225 	| /data/RCI/raw/ppm/kcrt_fg_proj_scope_change/data/20191225_tx_kcrt_fg_proj_scope_change.avro 	| 2019-12-25 13:10:22 	| 2019-12-25 13:11:05 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_kcrt_fg_proj_scope_change'
   and dateload = 20191225
   order by filedate asc;
   ```

  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 269          	| kcrt_fg_proj_scope_change   	| 20191225 	| 20191225_tx_kcrt_fg_proj_scope_change.avro   	| PPM      	| 20191225 	| 269        	| 269          	| 0            	| 0            	|

## Componentes del procesos de ingestión:

  __Framework de Ingestión Automatizado__

  - Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 62   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 62
```


## <a name="KCRT_REQ_HEADER_DETAILS"></a>KCRT_REQ_HEADER_DETAILS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KCRT_REQ_HEADER_DETAILS](../../../../RCI_DataAnalysis/eda/PPM/KCRT_REQ_HEADER_DETAILS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KCRT_REQ_HEADER_DETAILS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kcrt_req_header_details```

## <a name="KCRT_REQUEST_DETAILS"></a>KCRT_REQUEST_DETAILS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KCRT_REQUEST_DETAILS](../../../../RCI_DataAnalysis/eda/PPM/KCRT_REQUEST_DETAILS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KCRT_REQUEST_DETAILS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kcrt_request_details```

## <a name="KCRT_REQUESTS"></a>KCRT_REQUESTS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KCRT_REQUESTS](../../../../RCI_DataAnalysis/eda/PPM/KCRT_REQUESTS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KCRT_REQUESTS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kcrt_requests```

     | Id 	| Nombre de Columna        	| Tipo de Dato 	|
     |----	|--------------------------	|--------------	|
     | 1  	| request_id               	| string       	|
     | 2  	| creation_date            	| string       	|
     | 3  	| created_by               	| string       	|
     | 4  	| last_update_date         	| string       	|
     | 5  	| last_updated_by          	| string       	|
     | 6  	| entity_last_update_date  	| string       	|
     | 7  	| request_number           	| string       	|
     | 8  	| request_type_id          	| string       	|
     | 9  	| request_subtype_id       	| string       	|
     | 10 	| description              	| string       	|
     | 11 	| release_date             	| string       	|
     | 12 	| status_id                	| string       	|
     | 13 	| workflow_id              	| string       	|
     | 14 	| department_code          	| string       	|
     | 15 	| priority_code            	| string       	|
     | 16 	| application              	| string       	|
     | 17 	| assigned_to_user_id      	| string       	|
     | 18 	| assigned_to_group_id     	| string       	|
     | 19 	| project_code             	| string       	|
     | 20 	| contact_id               	| string       	|
     | 21 	| company                  	| string       	|
     | 22 	| updated_flag             	| string       	|
     | 23 	| status_code              	| string       	|
     | 24 	| source_type_code         	| string       	|
     | 25 	| source                   	| string       	|
     | 26 	| user_data_set_context_id 	| string       	|
     | 27 	| user_data1               	| string       	|
     | 28 	| visible_user_data1       	| string       	|
     | 29 	| user_data2               	| string       	|
     | 30 	| visible_user_data2       	| string       	|
     | 31 	| user_data3               	| string       	|
     | 32 	| visible_user_data3       	| string       	|
     | 33 	| user_data4               	| string       	|
     | 34 	| visible_user_data4       	| string       	|
     | 35 	| user_data5               	| string       	|
     | 36 	| visible_user_data5       	| string       	|
     | 37 	| user_data6               	| string       	|
     | 38 	| visible_user_data6       	| string       	|
     | 39 	| user_data7               	| string       	|
     | 40 	| visible_user_data7       	| string       	|
     | 41 	| user_data8               	| string       	|
     | 42 	| visible_user_data8       	| string       	|
     | 43 	| user_data9               	| string       	|
     | 44 	| visible_user_data9       	| string       	|
     | 45 	| user_data10              	| string       	|
     | 46 	| visible_user_data10      	| string       	|
     | 47 	| user_data11              	| string       	|
     | 48 	| visible_user_data11      	| string       	|
     | 49 	| user_data12              	| string       	|
     | 50 	| visible_user_data12      	| string       	|
     | 51 	| user_data13              	| string       	|
     | 52 	| visible_user_data13      	| string       	|
     | 53 	| user_data14              	| string       	|
     | 54 	| visible_user_data14      	| string       	|
     | 55 	| user_data15              	| string       	|
     | 56 	| visible_user_data15      	| string       	|
     | 57 	| user_data16              	| string       	|
     | 58 	| visible_user_data16      	| string       	|
     | 59 	| user_data17              	| string       	|
     | 60 	| visible_user_data17      	| string       	|
     | 61 	| user_data18              	| string       	|
     | 62 	| visible_user_data18      	| string       	|
     | 63 	| user_data19              	| string       	|
     | 64 	| visible_user_data19      	| string       	|
     | 65 	| user_data20              	| string       	|
     | 66 	| visible_user_data20      	| string       	|
     | 67 	| percent_complete         	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 68 	| filedate           	| bigint       	|
     | 69 	| filename           	| string       	|
     | 70 	| hash_id            	| string       	|
     | 71 	| sourceid           	| string       	|
     | 72 	| registry_state     	| string       	|
     | 73 	| datasetname        	| string       	|
     | 74 	| timestamp          	| bigint       	|
     | 75 	| transaction_status 	| string       	|


   - **Particiones**

     A continuación se presentan las particiones creadas de la tabla **tx_kcrt_requests**.

     Sentencia: ```show partitions rci_network_db.tx_kcrt_requests```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size   	| Bytes Cached 	| Cache Replication 	| Format 	| Incremental stats 	| Location                                                                                     	|
  |------	|-------	|-----	|-------	|--------	|--------	|--------------	|-------------------	|--------	|-------------------	|----------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 26  	| 2403  	| 1      	| 1.23MB 	| NOT CACHED   	| NOT CACHED        	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/kcrt_requests/year=2019/month=12/day=26 	|

   - **Ejecuciones**

      En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

      ```
      select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_kcrt_requests';
      ```

  | id_execution 	| table_name       	| dateload 	| avro_name                                                           	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|------------------	|----------	|---------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_kcrt_requests 	| 20191226 	| /data/RCI/raw/ppm/kcrt_requests/data/20191226_tx_kcrt_requests.avro 	| 2019-12-26 12:07:52 	| 2019-12-26 12:08:33 	| 1      	|         	|                	| 0        	|   	|

   - **Cifras de Control**

      En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

      ```
      select * from rci_network_db.tx_cifras_control
      where datasetname = 'tx_kcrt_requests'
      and dateload = 20191226
      order by filedate asc;
      ```
| uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
|------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
|      	| 2403         	| kcrt_requests               	| 20191226 	| 20191226_tx_kcrt_requests.avro               	| PPM      	| 20191225 	| 2403       	| 2403         	| 0            	| 0            	|

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 65   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 65
```


## <a name="KCRT_REQUESTS_V"></a>KCRT_REQUESTS_V

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KCRT_REQUESTS_V](../../../../RCI_DataAnalysis/eda/PPM/KCRT_REQUESTS_V/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KCRT_REQUESTS_V/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kcrt_requests_v```

## <a name="KCRT_STATUSES"></a>KCRT_STATUSES

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KCRT_STATUSES](../../../../RCI_DataAnalysis/eda/PPM/KCRT_STATUSES/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KCRT_STATUSES/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kcrt_statuses```

     | Id 	| Nombre de Columna       	| Tipo de Dato 	|
     |----	|-------------------------	|--------------	|
     | 1  	| definition_language     	| string       	|
     | 2  	| status_id               	| string       	|
     | 3  	| creation_date           	| string       	|
     | 4  	| created_by              	| string       	|
     | 5  	| last_update_date        	| string       	|
     | 6  	| last_updated_by         	| string       	|
     | 7  	| entity_last_update_date 	| string       	|
     | 8  	| status_name             	| string       	|
     | 9  	| enabled_flag            	| string       	|
     | 10 	| auto_link_flag          	| string       	|
     | 11 	| source_type_code        	| string       	|
     | 12 	| source                  	| string       	|
     | 13 	| system_status_flag      	| string       	|
     | 14 	| reference_code          	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 15 	| filedate           	| bigint       	|
     | 16 	| filename           	| string       	|
     | 17 	| hash_id            	| string       	|
     | 18 	| sourceid           	| string       	|
     | 19 	| registry_state     	| string       	|
     | 20 	| datasetname        	| string       	|
     | 21 	| timestamp          	| bigint       	|
     | 22 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_kcrt_statuses**.

 Sentencia: ```show partitions rci_network_db.tx_kcrt_statuses```

 | year 	| month 	| day 	| #Rows 	| #Files 	| Size    	| Format 	| Incremental stats 	| Location                                                                                     	|
|------	|-------	|-----	|-------	|--------	|---------	|--------	|-------------------	|----------------------------------------------------------------------------------------------	|
| 2019 	| 12    	| 25  	| 281   	| 1      	| 98.79KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/kcrt_statuses/year=2019/month=12/day=25 	|

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_kcrt_statuses';
  ```

  | id_execution 	| table_name       	| dateload 	| avro_name                                                           	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|------------------	|----------	|---------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_kcrt_statuses 	| 20191225 	| /data/RCI/raw/ppm/kcrt_statuses/data/20191225_tx_kcrt_statuses.avro 	| 2019-12-25 12:10:03 	| 2019-12-25 12:10:45 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_kcrt_statuses'
  and dateload = 20191225
  order by filedate asc;
  ```
  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 281          	| kcrt_statuses               	| 20191225 	| 20191225_tx_kcrt_statuses.avro               	| PPM      	| 20191225 	| 281        	| 281          	| 0            	| 0            	|

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 67   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 67
```


## <a name="KDRV_PROJECT_BUDGET_COSTS_V"></a>KDRV_PROJECT_BUDGET_COSTS_V

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KDRV_PROJECT_BUDGET_COSTS_V](../../../../RCI_DataAnalysis/eda/PPM/KDRV_PROJECT_BUDGET_COSTS_V/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KDRV_PROJECT_BUDGET_COSTS_V/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kdrv_project_budget_costs_v```

     | Id 	| Nombre de Columna           	| Tipo de Dato 	|
     |----	|-----------------------------	|--------------	|
     | 1  	| project_id                  	| string       	|
     | 2  	| project_name                	| string       	|
     | 3  	| prj_capex_opex_enabled_flag 	| string       	|
     | 4  	| project_currency_id         	| string       	|
     | 5  	| budget_id                   	| string       	|
     | 6  	| budget_name                 	| string       	|
     | 7  	| budget_currency_id          	| string       	|
     | 8  	| bud_capex_opex_enabled_flag 	| string       	|
     | 9  	| currency_id                 	| string       	|
     | 10 	| capex_opex_enabled_flag     	| string       	|
     | 11 	| active_linked_budget_flag   	| string       	|
     | 12 	| plan_capex_total_lcl        	| string       	|
     | 13 	| plan_opex_total_lcl         	| string       	|
     | 14 	| plan_total_lcl              	| string       	|
     | 15 	| actual_capex_total_lcl      	| string       	|
     | 16 	| actual_opex_total_lcl       	| string       	|
     | 17 	| actual_total_lcl            	| string       	|
     | 18 	| plan_labor_total_lcl        	| string       	|
     | 19 	| plan_nonlabor_total_lcl     	| string       	|
     | 20 	| actual_labor_total_lcl      	| string       	|
     | 21 	| actual_nonlabor_total_lcl   	| string       	|
     | 22 	| plan_capex_labor_lcl        	| string       	|
     | 23 	| plan_opex_labor_lcl         	| string       	|
     | 24 	| plan_capex_nonlabor_lcl     	| string       	|
     | 25 	| plan_opex_nonlabor_lcl      	| string       	|
     | 26 	| actual_capex_labor_lcl      	| string       	|
     | 27 	| actual_opex_labor_lcl       	| string       	|
     | 28 	| actual_capex_nonlabor_lcl   	| string       	|
     | 29 	| actual_opex_nonlabor_lcl    	| string       	|
     | 30 	| plan_capex_total_bse        	| string       	|
     | 31 	| plan_opex_total_bse         	| string       	|
     | 32 	| plan_total_bse              	| string       	|
     | 33 	| actual_capex_total_bse      	| string       	|
     | 34 	| actual_opex_total_bse       	| string       	|
     | 35 	| actual_total_bse            	| string       	|
     | 36 	| plan_labor_total_bse        	| string       	|
     | 37 	| plan_nonlabor_total_bse     	| string       	|
     | 38 	| actual_labor_total_bse      	| string       	|
     | 39 	| actual_nonlabor_total_bse   	| string       	|
     | 40 	| plan_capex_labor_bse        	| string       	|
     | 41 	| plan_opex_labor_bse         	| string       	|
     | 42 	| plan_capex_nonlabor_bse     	| string       	|
     | 43 	| plan_opex_nonlabor_bse      	| string       	|
     | 44 	| actual_capex_labor_bse      	| string       	|
     | 45 	| actual_opex_labor_bse       	| string       	|
     | 46 	| actual_capex_nonlabor_bse   	| string       	|
     | 47 	| actual_opex_nonlabor_bse    	| string       	|
     | 48 	| task_id                     	| string       	|
     | 49 	| work_plan_id                	| string       	|
     | 50 	| outline_level               	| string       	|
     | 51 	| ev_planned_value_bse        	| string       	|
     | 52 	| ev_planned_value_lcl        	| string       	|
     | 53 	| spi                         	| string       	|
     | 54 	| cpi                         	| string       	|
     | 55 	| ev_earned_value_bse         	| string       	|
     | 56 	| ev_earned_value_lcl         	| string       	|
     | 57 	| ev_actual_cost_bse          	| string       	|
     | 58 	| ev_actual_cost_lcl          	| string       	|
     | 59 	| ev_sched_variance_bse       	| string       	|
     | 60 	| ev_sched_variance_lcl       	| string       	|
     | 61 	| ev_cost_variance_bse        	| string       	|
     | 62 	| ev_cost_variance_lcl        	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 63 	| filedate           	| bigint       	|
     | 64 	| filename           	| string       	|
     | 65 	| hash_id            	| string       	|
     | 66 	| sourceid           	| string       	|
     | 67 	| registry_state     	| string       	|
     | 68 	| datasetname        	| string       	|
     | 69 	| timestamp          	| bigint       	|
     | 70 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_kdrv_project_budget_costs_v**.

 Sentencia: ```show partitions rci_network_db.tx_kdrv_project_budget_costs_v```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size   	| Format 	| Incremental stats 	| Location                                                                                                   	|
  |------	|-------	|-----	|-------	|--------	|--------	|--------	|-------------------	|------------------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 2484  	| 1      	| 1.12MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/kdrv_project_budget_costs_v/year=2019/month=12/day=25 	|

- **Ejecuciones**

 En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

 ```
 select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_kdrv_project_budget_costs_v';
 ```

  | id_execution 	| table_name                     	| dateload 	| avro_name                                                                                       	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|--------------------------------	|----------	|-------------------------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_kdrv_project_budget_costs_v 	| 20191225 	| /data/RCI/raw/ppm/kdrv_project_budget_costs_v/data/20191225_tx_kdrv_project_budget_costs_v.avro 	| 2019-12-25 12:32:37 	| 2019-12-25 12:33:22 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

 En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

 ```
 select * from rci_network_db.tx_cifras_control
 where datasetname = 'tx_kdrv_project_budget_costs_v'
 and dateload = 20191225
 order by filedate asc;
 ```

  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 2484         	| kdrv_project_budget_costs_v 	| 20191225 	| 20191225_tx_kdrv_project_budget_costs_v.avro 	| PPM      	| 20191225 	| 2484       	| 2484         	| 0            	| 0            	|

## Componentes del procesos de ingestión:

 __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 68   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 68
```

## <a name="KNTA_NOTES_V"></a>KNTA_NOTES_V

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KNTA_NOTES_V](../../../../RCI_DataAnalysis/eda/PPM/KNTA_NOTES_V/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KNTA_NOTES_V/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_knta_notes_v```

     | Id 	| Nombre de Columna          	| Tipo de Dato 	|
     |----	|----------------------------	|--------------	|
     | 1  	| note_id                    	| string       	|
     | 2  	| creation_date              	| string       	|
     | 3  	| created_by                 	| string       	|
     | 4  	| last_update_date           	| string       	|
     | 5  	| last_updated_by            	| string       	|
     | 6  	| parent_entity_id           	| string       	|
     | 7  	| parent_entity_primary_key  	| string       	|
     | 8  	| author_id                  	| string       	|
     | 9  	| author_username            	| string       	|
     | 10 	| author_full_name           	| string       	|
     | 11 	| authored_date              	| string       	|
     | 12 	| note_context_value         	| string       	|
     | 13 	| note_context_visible_value 	| string       	|
     | 14 	| note_type_code             	| string       	|
     | 15 	| note                       	| string       	|
     | 16 	| old_column_value           	| string       	|
     | 17 	| old_visible_column_value   	| string       	|
     | 18 	| new_column_value           	| string       	|
     | 19 	| new_visible_column_value   	| string       	|
     | 20 	| column_prompt              	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 21 	| filedate           	| bigint       	|
     | 22 	| filename           	| string       	|
     | 23 	| hash_id            	| string       	|
     | 24 	| sourceid           	| string       	|
     | 25 	| registry_state     	| string       	|
     | 26 	| datasetname        	| string       	|
     | 27 	| timestamp          	| bigint       	|
     | 28 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_knta_notes_v**.

 Sentencia: ```show partitions rci_network_db.tx_knta_notes_v```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size   	|  Format 	| Incremental stats 	| Location                                                                                    	|
  |------	|-------	|-----	|-------	|--------	|--------		|--------	|-------------------	|---------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 9646  	| 1      	| 6.66MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/knta_notes_v/year=2019/month=12/day=25 	|

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_knta_notes_v';
  ```

  | id_execution 	| table_name      	| dateload 	| avro_name                                                         	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|-----------------	|----------	|-------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_knta_notes_v 	| 20191225 	| /data/RCI/raw/ppm/knta_notes_v/data/20191225_tx_knta_notes_v.avro 	| 2019-12-25 11:47:33 	| 2019-12-25 11:48:16 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_knta_notes_v'
  and dateload = 20191225
  order by filedate asc;
  ```

  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 9646         	| knta_notes_v                	| 20191225 	| 20191225_tx_knta_notes_v.avro                	| PPM      	| 20191225 	| 9646       	| 9646         	| 0            	| 0            	|

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 69   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 69
  ```

## <a name="KNTA_REGIONS"></a>KNTA_REGIONS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KNTA_REGIONS](../../../../RCI_DataAnalysis/eda/PPM/KNTA_REGIONS/README.md)

- **Diccionario de Datos**
    [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KNTA_REGIONS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_knta_regions```

     | Id 	| Nombre de Columna       	| Tipo de Dato 	|
     |----	|-------------------------	|--------------	|
     | 1  	| definition_language     	| string       	|
     | 2  	| region_id               	| string       	|
     | 3  	| creation_date           	| string       	|
     | 4  	| created_by              	| string       	|
     | 5  	| last_update_date        	| string       	|
     | 6  	| last_updated_by         	| string       	|
     | 7  	| region_name             	| string       	|
     | 8  	| description             	| string       	|
     | 9  	| calendar_id             	| string       	|
     | 10 	| currency_id             	| string       	|
     | 11 	| enabled_flag            	| string       	|
     | 12 	| entity_last_update_date 	| string       	|
     | 13 	| version                 	| string       	|
     | 14 	| reference_code          	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 15 	| filedate           	| bigint       	|
     | 16 	| filename           	| string       	|
     | 17 	| hash_id            	| string       	|
     | 18 	| sourceid           	| string       	|
     | 19 	| registry_state     	| string       	|
     | 20 	| datasetname        	| string       	|
     | 21 	| timestamp          	| bigint       	|
     | 22 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_knta_regions**.

 Sentencia: ```show partitions rci_network_db.tx_knta_regions```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size   	| Format 	| Incremental stats 	| Location                                                                                    	|
  |------	|-------	|-----	|-------	|--------	|--------	|--------	|-------------------	|---------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 1     	| 1      	| 1.85KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/knta_regions/year=2019/month=12/day=25 	|

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_knta_regions';
   ```

  | id_execution 	| table_name      	| dateload 	| avro_name                                                         	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|-----------------	|----------	|-------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_knta_regions 	| 20191225 	| /data/RCI/raw/ppm/knta_regions/data/20191225_tx_knta_regions.avro 	| 2019-12-25 10:00:26 	| 2019-12-25 10:01:09 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_knta_regions'
   and dateload = 20191225
   order by filedate asc;
   ```

  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 1            	| knta_regions                	| 20191225 	| 20191225_tx_knta_regions.avro                	| PPM      	| 20191225 	| 1          	| 1            	| 0            	| 0            	|

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 70   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 70
  ```

## <a name="KNTA_USERS"></a>KNTA_USERS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KNTA_USERS](../../../../RCI_DataAnalysis/eda/PPM/KNTA_USERS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KNTA_USERS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_knta_users```

     | Id 	| Nombre de Columna        	| Tipo de Dato 	|
     |----	|--------------------------	|--------------	|
     | 1  	| user_id                  	| string       	|
     | 2  	| creation_date            	| string       	|
     | 3  	| created_by               	| string       	|
     | 4  	| last_update_date         	| string       	|
     | 5  	| last_updated_by          	| string       	|
     | 6  	| entity_last_update_date  	| string       	|
     | 7  	| username                 	| string       	|
     | 8  	| password                 	| string       	|
     | 9  	| password_expiration_days 	| string       	|
     | 10 	| password_expiration_date 	| string       	|
     | 11 	| email_address            	| string       	|
     | 12 	| first_name               	| string       	|
     | 13 	| last_name                	| string       	|
     | 14 	| start_date               	| string       	|
     | 15 	| end_date                 	| string       	|
     | 16 	| default_accelerator_id   	| string       	|
     | 17 	| user_data_set_context_id 	| string       	|
     | 18 	| user_data1               	| string       	|
     | 19 	| visible_user_data1       	| string       	|
     | 20 	| user_data2               	| string       	|
     | 21 	| visible_user_data2       	| string       	|
     | 22 	| user_data3               	| string       	|
     | 23 	| visible_user_data3       	| string       	|
     | 24 	| user_data4               	| string       	|
     | 25 	| visible_user_data4       	| string       	|
     | 26 	| user_data5               	| string       	|
     | 27 	| visible_user_data5       	| string       	|
     | 28 	| user_data6               	| string       	|
     | 29 	| visible_user_data6       	| string       	|
     | 30 	| user_data7               	| string       	|
     | 31 	| visible_user_data7       	| string       	|
     | 32 	| user_data8               	| string       	|
     | 33 	| visible_user_data8       	| string       	|
     | 34 	| user_data9               	| string       	|
     | 35 	| visible_user_data9       	| string       	|
     | 36 	| user_data10              	| string       	|
     | 37 	| visible_user_data10      	| string       	|
     | 38 	| user_data11              	| string       	|
     | 39 	| visible_user_data11      	| string       	|
     | 40 	| user_data12              	| string       	|
     | 41 	| visible_user_data12      	| string       	|
     | 42 	| user_data13              	| string       	|
     | 43 	| visible_user_data13      	| string       	|
     | 44 	| user_data14              	| string       	|
     | 45 	| visible_user_data14      	| string       	|
     | 46 	| user_data15              	| string       	|
     | 47 	| visible_user_data15      	| string       	|
     | 48 	| user_data16              	| string       	|
     | 49 	| visible_user_data16      	| string       	|
     | 50 	| user_data17              	| string       	|
     | 51 	| visible_user_data17      	| string       	|
     | 52 	| user_data18              	| string       	|
     | 53 	| visible_user_data18      	| string       	|
     | 54 	| user_data19              	| string       	|
     | 55 	| visible_user_data19      	| string       	|
     | 56 	| user_data20              	| string       	|
     | 57 	| visible_user_data20      	| string       	|
     | 58 	| authentication_mode      	| string       	|
     | 59 	| source_type_code         	| string       	|
     | 60 	| source                   	| string       	|
     | 61 	| company                  	| string       	|
     | 62 	| logon_identifier         	| string       	|
     | 63 	| domain                   	| string       	|
     | 64 	| phone_number             	| string       	|
     | 65 	| department_code          	| string       	|
     | 66 	| location_code            	| string       	|
     | 67 	| manager_user_id          	| string       	|
     | 68 	| resource_category_code   	| string       	|
     | 69 	| resource_title_code      	| string       	|
     | 70 	| full_name                	| string       	|
     | 71 	| calendar_id              	| string       	|
     | 72 	| region_id                	| string       	|
     | 73 	| region_override_flag     	| string       	|
     | 74 	| resource_flag            	| string       	|
     | 75 	| labor_category           	| string       	|
     | 76 	| distinguished_name       	| string       	|
     | 77 	| ldap_username            	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 78 	| filedate           	| bigint       	|
     | 79 	| filename           	| string       	|
     | 80 	| hash_id            	| string       	|
     | 81 	| sourceid           	| string       	|
     | 82 	| registry_state     	| string       	|
     | 83 	| datasetname        	| string       	|
     | 84 	| timestamp          	| bigint       	|
     | 85 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_knta_users**.

 Sentencia: ```show partitions rci_network_db.tx_knta_users```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                                  	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------	|-------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 249   	| 1      	| 184.91KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/knta_users/year=2019/month=12/day=25 	|

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_knta_users';
   ```

  | id_execution 	| table_name    	| dateload 	| avro_name                                                     	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|---------------	|----------	|---------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_knta_users 	| 20191225 	| /data/RCI/raw/ppm/knta_users/data/20191225_tx_knta_users.avro 	| 2019-12-25 10:08:29 	| 2019-12-25 10:09:13 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_knta_users'
   and dateload = 20191225
   order by filedate asc;
   ```

  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 249          	| knta_users                  	| 20191225 	| 20191225_tx_knta_users.avro                  	| PPM      	| 20191225 	| 249        	| 249          	| 0            	| 0            	|

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 71   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 71
  ```


## <a name="KWFL_STEP_TRANSACTIONS"></a>KWFL_STEP_TRANSACTIONS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KWFL_STEP_TRANSACTIONS](../../../../RCI_DataAnalysis/eda/PPM/KWFL_STEP_TRANSACTIONS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KWFL_STEP_TRANSACTIONS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kwfl_step_transactions```

     | Id 	| Nombre de Columna             	| Tipo de Dato 	|
     |----	|-------------------------------	|--------------	|
     | 1  	| step_transaction_id           	| string       	|
     | 2  	| created_by                    	| string       	|
     | 3  	| creation_date                 	| string       	|
     | 4  	| last_updated_by               	| string       	|
     | 5  	| last_update_date              	| string       	|
     | 6  	| workflow_instance_step_id     	| string       	|
     | 7  	| workflow_instance_id          	| string       	|
     | 8  	| instance_source_set_id        	| string       	|
     | 9  	| instance_source_type_code     	| string       	|
     | 10 	| instance_source_id            	| string       	|
     | 11 	| top_instance_source_type_code 	| string       	|
     | 12 	| top_instance_source_set_id    	| string       	|
     | 13 	| top_instance_source_id        	| string       	|
     | 14 	| workflow_id                   	| string       	|
     | 15 	| workflow_step_id              	| string       	|
     | 16 	| group_id                      	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 90 	| filedate           	| bigint       	|
     | 91 	| filename           	| string       	|
     | 92 	| hash_id            	| string       	|
     | 93 	| sourceid           	| string       	|
     | 94 	| registry_state     	| string       	|
     | 95 	| datasetname        	| string       	|
     | 96 	| timestamp          	| bigint       	|
     | 97 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_kwfl_step_transactions**.

 Sentencia: ```show partitions rci_network_db.tx_kwfl_step_transactions```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size   	| Format 	| Incremental stats 	| Location                                                                                              	|
  |------	|-------	|-----	|-------	|--------	|--------	|--------	|-------------------	|-------------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 15942 	| 1      	| 8.29MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/kwfl_step_transactions/year=2019/month=12/day=25 	|

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_kwfl_step_transactions';
   ```

  | id_execution 	| table_name                	| dateload 	| avro_name                                                                             	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|---------------------------	|----------	|---------------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_kwfl_step_transactions 	| 20191225 	| /data/RCI/raw/ppm/kwfl_step_transactions/data/20191225_tx_kwfl_step_transactions.avro 	| 2019-12-25 10:16:29 	| 2019-12-25 10:17:16 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_kwfl_step_transactions'
   and dateload = 20191225
   order by filedate asc;
   ```

  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 15942        	| kwfl_step_transactions      	| 20191225 	| 20191225_tx_kwfl_step_transactions.avro      	| PPM      	| 20191225 	| 15942      	| 15942        	| 0            	| 0            	|

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 72   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 72
  ```

## <a name="KWFL_WORKFLOW_INSTANCES"></a>KWFL_WORKFLOW_INSTANCES

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KWFL_WORKFLOW_INSTANCES](../../../../RCI_DataAnalysis/eda/PPM/KWFL_WORKFLOW_INSTANCES/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KWFL_WORKFLOW_INSTANCES/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kwfl_workflow_instances```

     | Id 	| Nombre de Columna             	| Tipo de Dato 	|
     |----	|-------------------------------	|--------------	|
     | 1  	| workflow_instance_id          	| string       	|
     | 2  	| created_by                    	| string       	|
     | 3  	| creation_date                 	| string       	|
     | 4  	| last_updated_by               	| string       	|
     | 5  	| last_update_date              	| string       	|
     | 6  	| workflow_id                   	| string       	|
     | 7  	| instance_source_set_id        	| string       	|
     | 8  	| instance_source_type_code     	| string       	|
     | 9  	| instance_source_id            	| string       	|
     | 10 	| top_instance_source_type_code 	| string       	|
     | 11 	| top_instance_source_set_id    	| string       	|
     | 12 	| top_instance_source_id        	| string       	|
     | 13 	| instance_name                 	| string       	|
     | 14 	| status                        	| string       	|
     | 15 	| completion_date               	| string       	|
     | 16 	| current_flag                  	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 17 	| filedate           	| bigint       	|
     | 18 	| filename           	| string       	|
     | 19 	| hash_id            	| string       	|
     | 20 	| sourceid           	| string       	|
     | 21 	| registry_state     	| string       	|
     | 22 	| datasetname        	| string       	|
     | 23 	| timestamp          	| bigint       	|
     | 24 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_kwfl_workflow_instances**.

 Sentencia: ```show partitions rci_network_db.tx_kwfl_workflow_instances```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size   	| Format 	| Incremental stats 	| Location                                                                                               	|
  |------	|-------	|-----	|-------	|--------	|--------	|--------	|-------------------	|--------------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 3252  	| 1      	| 1.12MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/kwfl_workflow_instances/year=2019/month=12/day=25 	|

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_kwfl_workflow_instances';
   ```

  | id_execution 	| table_name                 	| dateload 	| avro_name                                                                               	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|----------------------------	|----------	|-----------------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_kwfl_workflow_instances 	| 20191225 	| /data/RCI/raw/ppm/kwfl_workflow_instances/data/20191225_tx_kwfl_workflow_instances.avro 	| 2019-12-25 10:25:01 	| 2019-12-25 10:25:43 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_kwfl_workflow_instances'
   and dateload = 20191225
   order by filedate asc;
   ```
  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 3252         	| kwfl_workflow_instances     	| 20191225 	| 20191225_tx_kwfl_workflow_instances.avro     	| PPM      	| 20191225 	| 3252       	| 3252         	| 0            	| 0            	|

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 73   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 73
  ```

## <a name="KWFL_WORKFLOW_STEPS_NLS"></a>KWFL_WORKFLOW_STEPS_NLS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KWFL_WORKFLOW_STEPS_NLS](../../../../RCI_DataAnalysis/eda/PPM/KWFL_WORKFLOW_STEPS_NLS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KWFL_WORKFLOW_STEPS_NLS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kwfl_workflow_steps_nls```

     | Id 	| Nombre de Columna            	| Tipo de Dato 	|
     |----	|------------------------------	|--------------	|
     | 1  	| workflow_step_id             	| string       	|
     | 2  	| created_by                   	| string       	|
     | 3  	| creation_date                	| string       	|
     | 4  	| last_updated_by              	| string       	|
     | 5  	| last_update_date             	| string       	|
     | 6  	| workflow_id                  	| string       	|
     | 7  	| step_type_code               	| string       	|
     | 8  	| step_source_id               	| string       	|
     | 9  	| result_workflow_parameter_id 	| string       	|
     | 10 	| product_scope_code           	| string       	|
     | 11 	| parent_assigned_to_user_id   	| string       	|
     | 12 	| parent_assigned_to_group_id  	| string       	|
     | 13 	| parent_status                	| string       	|
     | 14 	| source_environment_id        	| string       	|
     | 15 	| source_env_group_id          	| string       	|
     | 16 	| dest_environment_id          	| string       	|
     | 17 	| dest_env_group_id            	| string       	|
     | 18 	| om_archive_flag              	| string       	|
     | 19 	| average_lead_time            	| string       	|
     | 20 	| step_name                    	| string       	|
     | 21 	| jump_receive_label_code      	| string       	|
     | 22 	| description                  	| string       	|
     | 23 	| information_url              	| string       	|
     | 24 	| request_type_list            	| string       	|
     | 25 	| action_button_label          	| string       	|
     | 26 	| sort_order                   	| string       	|
     | 27 	| enabled_flag                 	| string       	|
     | 28 	| display_type_code            	| string       	|
     | 29 	| draw_center_pos              	| string       	|
     | 30 	| source_type_code             	| string       	|
     | 31 	| source                       	| string       	|
     | 32 	| user_data_set_context_id     	| string       	|
     | 33 	| user_data1                   	| string       	|
     | 34 	| visible_user_data1           	| string       	|
     | 35 	| user_data2                   	| string       	|
     | 36 	| visible_user_data2           	| string       	|
     | 37 	| user_data3                   	| string       	|
     | 38 	| visible_user_data3           	| string       	|
     | 39 	| user_data4                   	| string       	|
     | 40 	| visible_user_data4           	| string       	|
     | 41 	| user_data5                   	| string       	|
     | 42 	| visible_user_data5           	| string       	|
     | 43 	| user_data6                   	| string       	|
     | 44 	| visible_user_data6           	| string       	|
     | 45 	| user_data7                   	| string       	|
     | 46 	| visible_user_data7           	| string       	|
     | 47 	| user_data8                   	| string       	|
     | 48 	| visible_user_data8           	| string       	|
     | 49 	| user_data9                   	| string       	|
     | 50 	| visible_user_data9           	| string       	|
     | 51 	| user_data10                  	| string       	|
     | 52 	| visible_user_data10          	| string       	|
     | 53 	| user_data11                  	| string       	|
     | 54 	| visible_user_data11          	| string       	|
     | 55 	| user_data12                  	| string       	|
     | 56 	| visible_user_data12          	| string       	|
     | 57 	| user_data13                  	| string       	|
     | 58 	| visible_user_data13          	| string       	|
     | 59 	| user_data14                  	| string       	|
     | 60 	| visible_user_data14          	| string       	|
     | 61 	| user_data15                  	| string       	|
     | 62 	| visible_user_data15          	| string       	|
     | 63 	| user_data16                  	| string       	|
     | 64 	| visible_user_data16          	| string       	|
     | 65 	| user_data17                  	| string       	|
     | 66 	| visible_user_data17          	| string       	|
     | 67 	| user_data18                  	| string       	|
     | 68 	| visible_user_data18          	| string       	|
     | 69 	| user_data19                  	| string       	|
     | 70 	| visible_user_data19          	| string       	|
     | 71 	| user_data20                  	| string       	|
     | 72 	| visible_user_data20          	| string       	|
     | 73 	| percent_complete             	| string       	|
     | 74 	| release_is_required_flag     	| string       	|
     | 75 	| step_timeout_type            	| string       	|
     | 76 	| step_timeout_value           	| string       	|
     | 77 	| step_timeout_unit_code       	| string       	|
     | 78 	| use_source_timeout_flag      	| string       	|
     | 79 	| allowed_child_pkg_wf_list    	| string       	|
     | 80 	| default_child_pkg_wf_id      	| string       	|
     | 81 	| default_child_req_rt_id      	| string       	|
     | 82 	| ref_relationship_id          	| string       	|
     | 83 	| step_auth_type_code          	| string       	|
     | 84 	| normal_background_color      	| string       	|
     | 85 	| assigned_to_user_token       	| string       	|
     | 86 	| assigned_to_group_token      	| string       	|
     | 87 	| definition_language          	| string       	|
     | 88 	| reference_code               	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 89 	| filedate           	| bigint       	|
     | 90 	| filename           	| string       	|
     | 91 	| hash_id            	| string       	|
     | 92 	| sourceid           	| string       	|
     | 93 	| registry_state     	| string       	|
     | 94  	| datasetname        	| string       	|
     | 95 	| timestamp          	| bigint       	|
     | 96 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_kwfl_workflow_steps_nls**.

 Sentencia: ```show partitions rci_network_db.tx_kwfl_workflow_steps_nls```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                                               	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------	|--------------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 753   	| 1      	| 448.00KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/kwfl_workflow_steps_nls/year=2019/month=12/day=25 	|

- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_kwfl_workflow_steps_nls';
    ```

  | id_execution 	| table_name                 	| dateload 	| avro_name                                                                               	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|----------------------------	|----------	|-----------------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_kwfl_workflow_steps_nls 	| 20191225 	| /data/RCI/raw/ppm/kwfl_workflow_steps_nls/data/20191225_tx_kwfl_workflow_steps_nls.avro 	| 2019-12-25 10:42:14 	| 2019-12-25 10:42:54 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_kwfl_workflow_steps_nls'
    and dateload = 20191225
    order by filedate asc;
    ```

  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 753          	| kwfl_workflow_steps_nls     	| 20191225 	| 20191225_tx_kwfl_workflow_steps_nls.avro     	| PPM      	| 20191225 	| 753        	| 753          	| 0            	| 0            	|

## Componentes del procesos de ingestión:

__Framework de Ingestión Automatizado__

- Especificar parámetros del proceso kite:

  | Parámetro | Valor | Descripción|
  | ---------- | ---------- | ---------- |
  | parametro_01   | 74   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 74
  ```

## <a name="KWFL_WORKFLOWS_V"></a>KWFL_WORKFLOWS_V

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [KWFL_WORKFLOWS_V](../../../../RCI_DataAnalysis/eda/PPM/KWFL_WORKFLOWS_V/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/KWFL_WORKFLOWS_V/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_kwfl_workflows_v```

     | Id 	| Nombre de Columna            	| Tipo de Dato 	|
     |----	|------------------------------	|--------------	|
     | 1  	| workflow_id                  	| string       	|
     | 2  	| created_by                   	| string       	|
     | 3  	| creation_date                	| string       	|
     | 4  	| last_updated_by              	| string       	|
     | 5  	| last_update_date             	| string       	|
     | 6  	| entity_last_update_date      	| string       	|
     | 7  	| workflow_name                	| string       	|
     | 8  	| description                  	| string       	|
     | 9  	| product_scope_code           	| string       	|
     | 10 	| first_workflow_step_id       	| string       	|
     | 11 	| reopen_step_id               	| string       	|
     | 12 	| restrict_objects_flag        	| string       	|
     | 13 	| force_app_code_flag          	| string       	|
     | 14 	| workflow_object_info         	| string       	|
     | 15 	| restrict_workflows_flag      	| string       	|
     | 16 	| workflow_settings_info       	| string       	|
     | 17 	| restrict_child_req_rts_flag  	| string       	|
     | 18 	| restricted_child_req_rt_list 	| string       	|
     | 19 	| default_child_pkg_wf_id      	| string       	|
     | 20 	| default_child_pkg_wf_name    	| string       	|
     | 21 	| default_child_req_rt_id      	| string       	|
     | 22 	| default_child_req_rt_name    	| string       	|
     | 23 	| enabled_flag                 	| string       	|
     | 24 	| sub_workflow_flag            	| string       	|
     | 25 	| result_validation_id         	| string       	|
     | 26 	| icon_name                    	| string       	|
     | 27 	| use_in_release_dist_flag     	| string       	|
     | 28 	| restriction_code             	| string       	|
     | 29 	| assigned_to_filter_code      	| string       	|
     | 30 	| assigned_grp_filter_code     	| string       	|
     | 31 	| audit_flag                   	| string       	|
     | 32 	| user_data_set_context_id     	| string       	|
     | 33 	| user_data1                   	| string       	|
     | 34 	| visible_user_data1           	| string       	|
     | 35 	| user_data2                   	| string       	|
     | 36 	| visible_user_data2           	| string       	|
     | 37 	| user_data3                   	| string       	|
     | 38 	| visible_user_data3           	| string       	|
     | 39 	| user_data4                   	| string       	|
     | 40 	| visible_user_data4           	| string       	|
     | 41 	| user_data5                   	| string       	|
     | 42 	| visible_user_data5           	| string       	|
     | 43 	| user_data6                   	| string       	|
     | 44 	| visible_user_data6           	| string       	|
     | 45 	| user_data7                   	| string       	|
     | 46 	| visible_user_data7           	| string       	|
     | 47 	| user_data8                   	| string       	|
     | 48 	| visible_user_data8           	| string       	|
     | 49 	| user_data9                   	| string       	|
     | 50 	| visible_user_data9           	| string       	|
     | 51 	| user_data10                  	| string       	|
     | 52 	| visible_user_data10          	| string       	|
     | 53 	| user_data11                  	| string       	|
     | 54 	| visible_user_data11          	| string       	|
     | 55 	| user_data12                  	| string       	|
     | 56 	| visible_user_data12          	| string       	|
     | 57 	| user_data13                  	| string       	|
     | 58 	| visible_user_data13          	| string       	|
     | 59 	| user_data14                  	| string       	|
     | 60 	| visible_user_data14          	| string       	|
     | 61 	| user_data15                  	| string       	|
     | 62 	| visible_user_data15          	| string       	|
     | 63 	| user_data16                  	| string       	|
     | 64 	| visible_user_data16          	| string       	|
     | 65 	| user_data17                  	| string       	|
     | 66 	| visible_user_data17          	| string       	|
     | 67 	| user_data18                  	| string       	|
     | 68 	| visible_user_data18          	| string       	|
     | 69 	| user_data19                  	| string       	|
     | 70 	| visible_user_data19          	| string       	|
     | 71 	| user_data20                  	| string       	|
     | 72 	| visible_user_data20          	| string       	|
     | 73 	| product_scope_meaning        	| string       	|
     | 74 	| result_validation_name       	| string       	|
     | 75 	| reference_code               	| string       	|
     | 76 	| definition_language          	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 77 	| filedate           	| bigint       	|
     | 78 	| filename           	| string       	|
     | 79 	| hash_id            	| string       	|
     | 80 	| sourceid           	| string       	|
     | 81 	| registry_state     	| string       	|
     | 82 	| datasetname        	| string       	|
     | 83 	| timestamp          	| bigint       	|
     | 84 	| transaction_status 	| string       	|

- **Particiones**

     A continuación se presentan las particiones creadas de la tabla **tx_kwfl_workflows_v**.

     Sentencia: ```show partitions rci_network_db.tx_kwfl_workflows_v```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size    	| Format 	| Incremental stats 	| Location                                                                                        	|
  |------	|-------	|-----	|-------	|--------	|---------	|--------	|-------------------	|-------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 56    	| 1      	| 35.12KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/kwfl_workflows_v/year=2019/month=12/day=25 	|

- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_kwfl_workflows_v';
    ```

  | id_execution 	| table_name          	| dateload 	| avro_name                                                                 	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|---------------------	|----------	|---------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_kwfl_workflows_v 	| 20191225 	| /data/RCI/raw/ppm/kwfl_workflows_v/data/20191225_tx_kwfl_workflows_v.avro 	| 2019-12-25 10:50:34 	| 2019-12-25 10:51:20 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_kwfl_workflows_v'
    and dateload = 20191225
    order by filedate asc;
    ```

  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 56           	| kwfl_workflows_v            	| 20191225 	| 20191225_tx_kwfl_workflows_v.avro            	| PPM      	| 20191225 	| 56         	| 56           	| 0            	| 0            	|

## Componentes del procesos de ingestión:

 __Framework de Ingestión Automatizado__

 - Especificar parámetros del proceso kite:

 | Parámetro | Valor | Descripción|
 | ---------- | ---------- | ---------- |
 | parametro_01   | 75   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 75
   ```


## <a name="PFM_LIFECYCLE_PARENT_ENTITY"></a>PFM_LIFECYCLE_PARENT_ENTITY

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [PFM_LIFECYCLE_PARENT_ENTITY](../../../../RCI_DataAnalysis/eda/PPM/PFM_LIFECYCLE_PARENT_ENTITY/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/PFM_LIFECYCLE_PARENT_ENTITY/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_pfm_lifecycle_parent_entity```

     | Id 	| Nombre de Columna 	| Tipo de Dato 	|
     |----	|-------------------	|--------------	|
     | 1  	| lifecycle_id      	| string       	|
     | 2  	| version           	| string       	|
     | 3  	| creation_date     	| string       	|
     | 4  	| created_by        	| string       	|
     | 5  	| last_update_date  	| string       	|
     | 6  	| last_updated_by   	| string       	|
     | 7  	| proposal_req_id   	| string       	|
     | 8  	| project_req_id    	| string       	|
     | 9  	| asset_req_id      	| string       	|
     | 10 	| active_entity     	| string       	|     

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 11 	| filedate           	| bigint       	|
     | 12 	| filename           	| string       	|
     | 13 	| hash_id            	| string       	|
     | 14 	| sourceid           	| string       	|
     | 15 	| registry_state     	| string       	|
     | 16 	| datasetname        	| string       	|
     | 17 	| timestamp          	| bigint       	|
     | 18 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_pfm_lifecycle_parent_entity**.

 Sentencia: ```show partitions rci_network_db.tx_pfm_lifecycle_parent_entity```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                                                   	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------	|------------------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 841   	| 1      	| 257.33KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/pfm_lifecycle_parent_entity/year=2019/month=12/day=25 	|

- **Ejecuciones**

     En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

     ```
     select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_pfm_lifecycle_parent_entity';
     ```

  | id_execution 	| table_name                     	| dateload 	| avro_name                                                                                       	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|--------------------------------	|----------	|-------------------------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_pfm_lifecycle_parent_entity 	| 20191225 	| /data/RCI/raw/ppm/pfm_lifecycle_parent_entity/data/20191225_tx_pfm_lifecycle_parent_entity.avro 	| 2019-12-25 11:01:05 	| 2019-12-25 11:01:48 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

     En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

     ```
     select * from rci_network_db.tx_cifras_control
     where datasetname = 'tx_pfm_lifecycle_parent_entity'
     and dateload = 20191225
     order by filedate asc;
     ```

  | uuid 	| rowprocessed 	| datasetname                 	| filedate 	| filename                                     	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-----------------------------	|----------	|----------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 841          	| pfm_lifecycle_parent_entity 	| 20191225 	| 20191225_tx_pfm_lifecycle_parent_entity.avro 	| PPM      	| 20191225 	| 841        	| 841          	| 0            	| 0            	|


## Componentes del procesos de ingestión:

 __Framework de Ingestión Automatizado__

 - Especificar parámetros del proceso kite:

 | Parámetro | Valor | Descripción|
 | ---------- | ---------- | ---------- |
 | parametro_01   | 76   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 76
   ```


## <a name="PFM_REQUEST_DETAILS_V"></a>PFM_REQUEST_DETAILS_V

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [PFM_REQUEST_DETAILS_V](../../../../RCI_DataAnalysis/eda/PPM/PFM_REQUEST_DETAILS_V/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/PFM_REQUEST_DETAILS_V/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_pfm_request_details_v```

     | Id  	| Nombre de Columna              	| Tipo de Dato 	|
     |-----	|--------------------------------	|--------------	|
     | 1   	| request_id                     	| string       	|
     | 2   	| request_type_id                	| string       	|
     | 3   	| proposal_name                  	| string       	|
     | 4   	| prop_business_unit_code        	| string       	|
     | 5   	| prop_business_unit_meaning     	| string       	|
     | 6   	| prop_business_objective_id     	| string       	|
     | 7   	| prop_business_objective_name   	| string       	|
     | 8   	| prop_project_class_code        	| string       	|
     | 9   	| prop_project_class_meaning     	| string       	|
     | 10  	| prop_asset_class_code          	| string       	|
     | 11  	| prop_asset_class_meaning       	| string       	|
     | 12  	| prop_project_manager_user_id   	| string       	|
     | 13  	| prop_project_manager_username  	| string       	|
     | 14  	| prop_staff_prof_id             	| string       	|
     | 15  	| prop_staff_prof_name           	| string       	|
     | 16  	| prop_return_on_investment      	| string       	|
     | 17  	| prop_net_present_value         	| string       	|
     | 18  	| prop_custom_field_value        	| string       	|
     | 19  	| prop_value_rating              	| string       	|
     | 20  	| prop_risk_rating               	| string       	|
     | 21  	| prop_total_score               	| string       	|
     | 22  	| prop_discount_rate             	| string       	|
     | 23  	| prop_plan_start_period_id      	| string       	|
     | 24  	| prop_plan_finish_period_id     	| string       	|
     | 25  	| prop_plan_start_period_name    	| string       	|
     | 26  	| prop_plan_finish_period_name   	| string       	|
     | 27  	| prop_project_id                	| string       	|
     | 28  	| prop_project_name              	| string       	|
     | 29  	| prop_dependencies_code         	| string       	|
     | 30  	| prop_dependencies_meaning      	| string       	|
     | 31  	| prop_project_type_id           	| string       	|
     | 32  	| prop_project_type_name         	| string       	|
     | 33  	| prop_region_id                 	| string       	|
     | 34  	| prop_region_name               	| string       	|
     | 35  	| prop_benefit_manager_user_id   	| string       	|
     | 36  	| prop_benefit_manager_username  	| string       	|
     | 37  	| prop_financial_summary_name    	| string       	|
     | 38  	| prop_financial_summary_id      	| string       	|
     | 39  	| prop_approved_snapshot_id      	| string       	|
     | 40  	| prop_approved_snapshot_name    	| string       	|
     | 41  	| project_name                   	| string       	|
     | 42  	| project_health_code            	| string       	|
     | 43  	| project_health_meaning         	| string       	|
     | 44  	| prj_business_unit_code         	| string       	|
     | 45  	| prj_business_unit_meaning      	| string       	|
     | 46  	| prj_business_objective_id      	| string       	|
     | 47  	| prj_business_objective_name    	| string       	|
     | 48  	| prj_project_class_code         	| string       	|
     | 49  	| prj_project_class_meaning      	| string       	|
     | 50  	| prj_asset_class_code           	| string       	|
     | 51  	| prj_asset_class_meaning        	| string       	|
     | 52  	| prj_project_manager_user_id    	| string       	|
     | 53  	| prj_project_manager_username   	| string       	|
     | 54  	| prj_project_id                 	| string       	|
     | 55  	| prj_project_name               	| string       	|
     | 56  	| prj_project_url                	| string       	|
     | 57  	| prj_staff_prof_id              	| string       	|
     | 58  	| prj_staff_prof_name            	| string       	|
     | 59  	| prj_return_on_investment       	| string       	|
     | 60  	| prj_net_present_value          	| string       	|
     | 61  	| prj_custom_field_value         	| string       	|
     | 62  	| prj_value_rating               	| string       	|
     | 63  	| prj_risk_rating                	| string       	|
     | 64  	| prj_total_score                	| string       	|
     | 65  	| prj_discount_rate              	| string       	|
     | 66  	| prj_plan_start_period_id       	| string       	|
     | 67  	| prj_plan_finish_period_id      	| string       	|
     | 68  	| prj_plan_start_period_name     	| string       	|
     | 69  	| prj_plan_finish_period_name    	| string       	|
     | 70  	| prj_dependencies_code          	| string       	|
     | 71  	| prj_dependencies_meaning       	| string       	|
     | 72  	| prj_phase_code                 	| string       	|
     | 73  	| prj_phase_meaning              	| string       	|
     | 74  	| prj_benefit_manager_user_id    	| string       	|
     | 75  	| prj_benefit_manager_username   	| string       	|
     | 76  	| prj_financial_summary_name     	| string       	|
     | 77  	| prj_financial_summary_id       	| string       	|
     | 78  	| asset_name                     	| string       	|
     | 79  	| asset_health_code              	| string       	|
     | 80  	| asset_health_meaning           	| string       	|
     | 81  	| asset_business_unit_code       	| string       	|
     | 82  	| asset_business_unit_meaning    	| string       	|
     | 83  	| asset_business_objective_id    	| string       	|
     | 84  	| asset_business_objective_name  	| string       	|
     | 85  	| asset_project_class_code       	| string       	|
     | 86  	| asset_project_class_meaning    	| string       	|
     | 87  	| asset_asset_class_code         	| string       	|
     | 88  	| asset_asset_class_meaning      	| string       	|
     | 89  	| asset_project_id               	| string       	|
     | 90  	| asset_project_name             	| string       	|
     | 91  	| asset_project_url              	| string       	|
     | 92  	| asset_staff_prof_id            	| string       	|
     | 93  	| asset_staff_prof_name          	| string       	|
     | 94  	| asset_return_on_investment     	| string       	|
     | 95  	| asset_net_present_value        	| string       	|
     | 96  	| asset_custom_field_value       	| string       	|
     | 97  	| asset_value_rating             	| string       	|
     | 98  	| asset_risk_rating              	| string       	|
     | 99  	| asset_total_score              	| string       	|
     | 100 	| asset_discount_rate            	| string       	|
     | 101 	| asset_dependencies_code        	| string       	|
     | 102 	| asset_dependencies_meaning     	| string       	|
     | 103 	| asset_project_manager_user_id  	| string       	|
     | 104 	| asset_project_manager_username 	| string       	|
     | 105 	| asset_region_id                	| string       	|
     | 106 	| asset_region_name              	| string       	|
     | 107 	| asset_benefit_manager_user_id  	| string       	|
     | 108 	| asset_benefit_manager_username 	| string       	|
     | 109 	| asset_financial_summary_name   	| string       	|
     | 110 	| asset_financial_summary_id     	| string       	|     

     Las siguientes columnas son creadas para la identidad de la fuente:     

     | Id  	| Nombre de Columna  	| Tipo de Dato 	|
     |-----	|--------------------	|--------------	|
     | 111 	| filedate           	| bigint       	|
     | 112 	| filename           	| string       	|
     | 113 	| hash_id            	| string       	|
     | 114 	| sourceid           	| string       	|
     | 115 	| registry_state     	| string       	|
     | 116 	| datasetname        	| string       	|
     | 117 	| timestamp          	| bigint       	|
     | 118 	| transaction_status 	| string       	|     

- **Particiones**

   A continuación se presentan las particiones creadas de la tabla **tx_pfm_request_details_v**.

   Sentencia: ```show partitions rci_network_db.tx_pfm_request_details_v```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size   	| Format 	| Incremental stats 	| Location                                                                                             	|
  |------	|-------	|-----	|-------	|--------	|--------	|--------	|-------------------	|------------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 2403  	| 1      	| 1.11MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/pfm_request_details_v/year=2019/month=12/day=25 	|

- **Ejecuciones**

     En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

     ```
     select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_pfm_request_details_v';
     ```

  | id_execution 	| table_name               	| dateload 	| avro_name                                                                           	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|--------------------------	|----------	|-------------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_pfm_request_details_v 	| 20191225 	| /data/RCI/raw/ppm/pfm_request_details_v/data/20191225_tx_pfm_request_details_v.avro 	| 2019-12-25 11:10:51 	| 2019-12-25 11:11:36 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

     En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

     ```
     select * from rci_network_db.tx_cifras_control
     where datasetname = 'tx_pfm_request_details_v'
     and dateload = 20191225
     order by filedate asc;
     ```

  | uuid 	| rowprocessed 	| datasetname               	| filedate 	| filename                                   	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|---------------------------	|----------	|--------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 2403         	| pfm_request_details_v     	| 20191225 	| 20191225_tx_pfm_request_details_v.avro     	| PPM      	| 20191225 	| 2403       	| 2403         	| 0            	| 0            	|

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 77   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 77
   ```

## <a name="PGM_PROGRAM_CONTENT"></a>PGM_PROGRAM_CONTENT

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [PGM_PROGRAM_CONTENT](../../../../RCI_DataAnalysis/eda/PPM/PGM_PROGRAM_CONTENT/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/PGM_PROGRAM_CONTENT/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_pgm_program_content```

     | Id 	| Nombre de Columna 	| Tipo de Dato 	|
     |----	|-------------------	|--------------	|
     | 1  	| program_id        	| string       	|
     | 2  	| content_id        	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 3  	| filedate           	| bigint       	|
     | 4  	| filename           	| string       	|
     | 5  	| hash_id            	| string       	|
     | 6  	| sourceid           	| string       	|
     | 7  	| registry_state     	| string       	|
     | 8  	| datasetname        	| string       	|
     | 9  	| timestamp          	| bigint       	|
     | 10 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_pgm_program_content**.

 Sentencia: ```show partitions rci_network_db.tx_pgm_program_content```

  | Year| Month|Day|#Rows|#Files|Size|Format|Location|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|----------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 319   	| 71.51KB      	| 1.12MB 	| AVRO   	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/pgm_program_content/year=2019/month=12/day=25 	|

- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_pgm_program_content';
    ```

  | id_execution 	| table_name             	| dateload 	| avro_name                                                                       	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|------------------------	|----------	|---------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_pgm_program_content 	| 20191227 	| /data/RCI/raw/ppm/pgm_program_content/data/20191225_tx_pgm_program_content.avro 	| 2019-12-27 01:37:10 	| 2019-12-27 01:37:50 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_pgm_program_content'
    and dateload = 20191227
    order by filedate asc;
    ```

  | uuid 	| rowprocessed 	| datasetname               	| filedate 	| filename                                   	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|---------------------------	|----------	|--------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 319          	| pgm_program_content       	| 20191227 	| 20191227_tx_pgm_program_content.avro       	| PPM      	| 20191225 	| 319        	| 319          	| 0            	| 0            	|

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 78   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 78
   ```

## <a name="PGM_PROGRAMS"></a>PGM_PROGRAMS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [PGM_PROGRAMS](../../../../RCI_DataAnalysis/eda/PPM/PGM_PROGRAMS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/PGM_PROGRAMS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_pgm_programs```

     | Id 	| Nombre de Columna            	| Tipo de Dato 	|
     |----	|------------------------------	|--------------	|
     | 1  	| program_id                   	| string       	|
     | 2  	| entity_type_code             	| string       	|
     | 3  	| version                      	| string       	|
     | 4  	| parent_projects_container_id 	| string       	|
     | 5  	| container_name               	| string       	|
     | 6  	| depth                        	| string       	|
     | 7  	| created_by                   	| string       	|
     | 8  	| creation_date                	| string       	|
     | 9  	| last_updated_by              	| string       	|
     | 10 	| last_update_date             	| string       	|
     | 11 	| description                  	| string       	|
     | 12 	| user_data1                   	| string       	|
     | 13 	| visible_user_data1           	| string       	|
     | 14 	| user_data2                   	| string       	|
     | 15 	| visible_user_data2           	| string       	|
     | 16 	| user_data3                   	| string       	|
     | 17 	| visible_user_data3           	| string       	|
     | 18 	| user_data4                   	| string       	|
     | 19 	| visible_user_data4           	| string       	|
     | 20 	| user_data5                   	| string       	|
     | 21 	| visible_user_data5           	| string       	|
     | 22 	| user_data6                   	| string       	|
     | 23 	| visible_user_data6           	| string       	|
     | 24 	| user_data7                   	| string       	|
     | 25 	| visible_user_data7           	| string       	|
     | 26 	| user_data8                   	| string       	|
     | 27 	| visible_user_data8           	| string       	|
     | 28 	| user_data9                   	| string       	|
     | 29 	| visible_user_data9           	| string       	|
     | 30 	| user_data10                  	| string       	|
     | 31 	| visible_user_data10          	| string       	|
     | 32 	| user_data11                  	| string       	|
     | 33 	| visible_user_data11          	| string       	|
     | 34 	| user_data12                  	| string       	|
     | 35 	| visible_user_data12          	| string       	|
     | 36 	| user_data13                  	| string       	|
     | 37 	| visible_user_data13          	| string       	|
     | 38 	| user_data14                  	| string       	|
     | 39 	| visible_user_data14          	| string       	|
     | 40 	| user_data15                  	| string       	|
     | 41 	| visible_user_data15          	| string       	|
     | 42 	| user_data16                  	| string       	|
     | 43 	| visible_user_data16          	| string       	|
     | 44 	| user_data17                  	| string       	|
     | 45 	| visible_user_data17          	| string       	|
     | 46 	| user_data18                  	| string       	|
     | 47 	| visible_user_data18          	| string       	|
     | 48 	| user_data19                  	| string       	|
     | 49 	| visible_user_data19          	| string       	|
     | 50 	| user_data20                  	| string       	|
     | 51 	| visible_user_data20          	| string       	|
     | 52 	| status_notes                 	| string       	|
     | 53 	| benefit                      	| string       	|
     | 54 	| state                        	| string       	|
     | 55 	| priority                     	| string       	|
     | 56 	| prog_settings_key            	| string       	|
     | 57 	| issues_health                	| string       	|
     | 58 	| risk_health                  	| string       	|
     | 59 	| scope_change_health          	| string       	|
     | 60 	| program_access_id            	| string       	|
     | 61 	| program_cost_access_id       	| string       	|
     | 62 	| child_seq                    	| string       	|
     | 63 	| financial_summary_id         	| string       	|
     | 64 	| score                        	| string       	|
     | 65 	| overall_health               	| string       	|
     | 66 	| discount_rate                	| string       	|
     | 67 	| npv                          	| string       	|
     | 68 	| tnr                          	| string       	|
     | 69 	| rollupable                   	| string       	|
     | 70 	| program_type_id              	| string       	|
     | 71 	| pgm_request_id               	| string       	|
     | 72 	| display_status               	| string       	|
     | 73 	| override_date                	| string       	|
     | 74 	| override_description         	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 75 	| filedate           	| bigint       	|
     | 76 	| filename           	| string       	|
     | 77 	| hash_id            	| string       	|
     | 78 	| sourceid           	| string       	|
     | 79 	| registry_state     	| string       	|
     | 80 	| datasetname        	| string       	|
     | 81 	| timestamp          	| bigint       	|
     | 82 	| transaction_status 	| string       	|     

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_pgm_programs**.

 Sentencia: ```show partitions rci_network_db.tx_pgm_programs```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size    	| Format 	| Incremental stats 	| Location                                                                                    	|
  |------	|-------	|-----	|-------	|--------	|---------	|--------	|-------------------	|---------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 19    	| 1      	| 15.53KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/pgm_programs/year=2019/month=12/day=25 	|

- **Ejecuciones**

     En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

     ```
     select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_pgm_programs';
     ```

  | id_execution 	| table_name      	| dateload 	| avro_name                                                         	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|-----------------	|----------	|-------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_pgm_programs 	| 20191225 	| /data/RCI/raw/ppm/pgm_programs/data/20191225_tx_pgm_programs.avro 	| 2019-12-25 09:45:55 	| 2019-12-25 09:46:38 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

     En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

     ```
     select * from rci_network_db.tx_cifras_control
     where datasetname = 'tx_pgm_programs'
     and dateload = 20191225
     order by filedate asc;
     ```

  | uuid 	| rowprocessed 	| datasetname               	| filedate 	| filename                                   	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|---------------------------	|----------	|--------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 19           	| pgm_programs              	| 20191225 	| 20191225_tx_pgm_programs.avro              	| PPM      	| 20191225 	| 19         	| 19           	| 0            	| 0            	|

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 79   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 79
   ```


## <a name="PM_EXCEPTION_RULE_RESULTS"></a>PM_EXCEPTION_RULE_RESULTS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [PM_EXCEPTION_RULE_RESULTS](../../../../RCI_DataAnalysis/eda/PPM/PM_EXCEPTION_RULE_RESULTS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/PM_EXCEPTION_RULE_RESULTS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_pm_exception_rule_results```

     | Id 	| Nombre de Columna        	| Tipo de Dato 	|
     |----	|--------------------------	|--------------	|
     | 1  	| exception_rule_result_id 	| string       	|
     | 2  	| hib_class                	| string       	|
     | 3  	| version                  	| string       	|
     | 4  	| new_task_id              	| string       	|
     | 5  	| exception_name           	| string       	|
     | 6  	| exception_sub_type       	| string       	|
     | 7  	| exception_type           	| string       	|
     | 8  	| affects_schedule_health  	| string       	|
     | 9  	| description_type         	| string       	|
     | 10 	| details                  	| string       	|
     | 11 	| created_by               	| string       	|
     | 12 	| creation_date            	| string       	|
     | 13 	| last_updated_by          	| string       	|
     | 14 	| last_update_date         	| string       	|
     | 15 	| target_task_id           	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 16 	| filedate           	| bigint       	|
     | 17 	| filename           	| string       	|
     | 18 	| hash_id            	| string       	|
     | 19 	| sourceid           	| string       	|
     | 20 	| registry_state     	| string       	|
     | 21 	| datasetname        	| string       	|
     | 22 	| timestamp          	| bigint       	|
     | 23 	| transaction_status 	| string       	|          

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_pm_exception_rule_results**.

 Sentencia: ```show partitions rci_network_db.tx_pm_exception_rule_results```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size   	| Format 	| Incremental stats 	| Location                                                                                                 	|
  |------	|-------	|-----	|-------	|--------	|--------	|--------	|-------------------	|----------------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 8391  	| 1      	| 2.89MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/pm_exception_rule_results/year=2019/month=12/day=25 	|

- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_pm_exception_rule_results';
    ```

  | id_execution 	| table_name                   	| dateload 	| avro_name                                                                                   	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|------------------------------	|----------	|---------------------------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_pm_exception_rule_results 	| 20191225 	| /data/RCI/raw/ppm/pm_exception_rule_results/data/20191225_tx_pm_exception_rule_results.avro 	| 2019-12-25 01:00:32 	| 2019-12-25 01:01:14 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_pm_exception_rule_results'
    and dateload = 20191225
    order by filedate asc;
    ```

  | uuid 	| rowprocessed 	| datasetname               	| filedate 	| filename                                   	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|---------------------------	|----------	|--------------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 8391         	| pm_exception_rule_results 	| 20191225 	| 20191225_tx_pm_exception_rule_results.avro 	| PPM      	| 20191225 	| 8391       	| 8391         	| 0            	| 0            	|

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 80   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 80
   ```

## <a name="PM_PROJECT_ROLLUP"></a>PM_PROJECT_ROLLUP

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [PM_PROJECT_ROLLUP](../../../../RCI_DataAnalysis/eda/PPM/PM_PROJECT_ROLLUP/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/PM_PROJECT_ROLLUP/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_pm_project_rollup```

     | Id 	| Nombre de Columna         	| Tipo de Dato 	|
     |----	|---------------------------	|--------------	|
     | 1  	| rollup_id                 	| string       	|
     | 2  	| version                   	| string       	|
     | 3  	| schedule_health_indicator 	| string       	|
     | 4  	| override_date             	| string       	|
     | 5  	| override_description      	| string       	|
     | 6  	| overall_health_indicator  	| string       	|
     | 7  	| cost_health_indicator     	| string       	|
     | 8  	| budget_overrun            	| string       	|
     | 9  	| issue_health_indicator    	| string       	|
     | 10 	| created_by                	| string       	|
     | 11 	| creation_date             	| string       	|
     | 12 	| last_updated_by           	| string       	|
     | 13 	| last_update_date          	| string       	|  

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 14 	| filedate           	| bigint       	|
     | 15 	| filename           	| string       	|
     | 16 	| hash_id            	| string       	|
     | 17 	| sourceid           	| string       	|
     | 18 	| registry_state     	| string       	|
     | 19 	| datasetname        	| string       	|
     | 20 	| timestamp          	| bigint       	|
     | 21 	| transaction_status 	| string       	|        

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_pm_project_rollup**.

 Sentencia: ```show partitions rci_network_db.tx_pm_project_rollup```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                                         	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------	|--------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 519   	| 1      	| 154.68KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/pm_project_rollup/year=2019/month=12/day=25 	|

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_pm_project_rollup';
   ```

  | id_execution 	| table_name           	| dateload 	| avro_name                                                                   	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|----------------------	|----------	|-----------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_pm_project_rollup 	| 20191225 	| /data/RCI/raw/ppm/pm_project_rollup/data/20191225_tx_pm_project_rollup.avro 	| 2019-12-25 00:39:06 	| 2019-12-25 00:39:48 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_pm_project_rollup'
   and dateload = 20191225
   order by filedate asc;
   ```

  | uuid 	| rowprocessed 	| datasetname       	| filedate 	| filename                           	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-------------------	|----------	|------------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 519          	| pm_project_rollup 	| 20191225 	| 20191225_tx_pm_project_rollup.avro 	| PPM      	| 20191225 	| 519        	| 519          	| 0            	| 0            	|

## Componentes del procesos de ingestión:

 __Framework de Ingestión Automatizado__

 - Especificar parámetros del proceso kite:

 | Parámetro | Valor | Descripción|
 | ---------- | ---------- | ---------- |
 | parametro_01   | 81   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 81
   ```


## <a name="PM_PROJECT_TYPES"></a>PM_PROJECT_TYPES

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [PM_PROJECT_TYPES](../../../../RCI_DataAnalysis/eda/PPM/PM_PROJECT_TYPES/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/PM_PROJECT_TYPES/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_pm_project_types```

     | Id 	| Nombre de Columna              	| Tipo de Dato 	|
     |----	|--------------------------------	|--------------	|
     | 1  	| project_type_id                	| string       	|
     | 2  	| version                        	| string       	|
     | 3  	| source_id                      	| string       	|
     | 4  	| project_type_name              	| string       	|
     | 5  	| description                    	| string       	|
     | 6  	| enabled_flag                   	| string       	|
     | 7  	| workplan_template_id           	| string       	|
     | 8  	| resource_pool_id               	| string       	|
     | 9  	| project_request_type_id        	| string       	|
     | 10 	| project_request_type_name      	| string       	|
     | 11 	| issue_request_type_id          	| string       	|
     | 12 	| issue_request_type_name        	| string       	|
     | 13 	| project_type_edit_access_id    	| string       	|
     | 14 	| project_type_usage_id          	| string       	|
     | 15 	| project_id                     	| string       	|
     | 16 	| indicator_overridable_flag     	| string       	|
     | 17 	| pt_settings_key                	| string       	|
     | 18 	| context_path                   	| string       	|
     | 19 	| source                         	| string       	|
     | 20 	| source_type_code               	| string       	|
     | 21 	| created_by                     	| string       	|
     | 22 	| creation_date                  	| string       	|
     | 23 	| last_updated_by                	| string       	|
     | 24 	| last_update_date               	| string       	|
     | 25 	| project_container_id           	| string       	|
     | 26 	| allowed_project_types_seq      	| string       	|
     | 27 	| risk_request_type_id           	| string       	|
     | 28 	| risk_request_type_name         	| string       	|
     | 29 	| scope_change_request_type_id   	| string       	|
     | 30 	| scope_change_request_type_name 	| string       	|
     | 31 	| work_load_category_code        	| string       	|
     | 32 	| en_change_to_demand_approval   	| string       	|  

     Las siguientes columnas son creadas para la identidad de la fuente:      

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 33 	| filedate           	| bigint       	|
     | 34 	| filename           	| string       	|
     | 35 	| hash_id            	| string       	|
     | 36 	| sourceid           	| string       	|
     | 37 	| registry_state     	| string       	|
     | 38 	| datasetname        	| string       	|
     | 39 	| timestamp          	| bigint       	|
     | 40 	| transaction_status 	| string       	|

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_pm_project_types**.

 Sentencia: ```show partitions rci_network_db.tx_pm_project_types```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                                        	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------	|-------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 25  	| 345   	| 1      	| 173.43KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/pm_project_types/year=2019/month=12/day=25 	|

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_pm_project_types';
  ```

  | id_execution 	| table_name          	| dateload 	| avro_name                                                                 	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|---------------------	|----------	|---------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_pm_project_types 	| 20191225 	| /data/RCI/raw/ppm/pm_project_types/data/20191225_tx_pm_project_types.avro 	| 2019-12-25 00:17:35 	| 2019-12-25 00:18:18 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_pm_project_types'
  and dateload = 20191225
  order by filedate asc;
  ```

  | uuid 	| rowprocessed 	| datasetname      	| filedate 	| filename                          	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|------------------	|----------	|-----------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 345          	| pm_project_types 	| 20191225 	| 20191225_tx_pm_project_types.avro 	| PPM      	| 20191225 	| 345        	| 345          	| 0            	| 0            	|

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 82   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 82
```


## <a name="PM_PROJECTS"></a>PM_PROJECTS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [PM_PROJECTS](../../../../RCI_DataAnalysis/eda/PPM/PM_PROJECTS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/PM_PROJECTS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_pm_projects```

     | Id 	| Nombre de Columna      	| Tipo de Dato 	|
     |----	|------------------------	|--------------	|
     | 1  	| project_id             	| string       	|
     | 2  	| version                	| string       	|
     | 3  	| rollup_id              	| string       	|
     | 4  	| project_name           	| string       	|
     | 5  	| description            	| string       	|
     | 6  	| associated_msp_project 	| string       	|
     | 7  	| project_manager        	| string       	|
     | 8  	| start_date_period      	| string       	|
     | 9  	| finish_date_period     	| string       	|
     | 10 	| region_id              	| string       	|
     | 11 	| project_type_id        	| string       	|
     | 12 	| pfm_request_id         	| string       	|
     | 13 	| display_status         	| string       	|
     | 14 	| status                 	| string       	|
     | 15 	| project_access_id      	| string       	|
     | 16 	| project_cost_access_id 	| string       	|
     | 17 	| created_by             	| string       	|
     | 18 	| creation_date          	| string       	|
     | 19 	| last_updated_by        	| string       	|
     | 20 	| last_update_date       	| string       	|
     | 21 	| mpp_file_name          	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:     

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 22 	| filedate           	| bigint       	|
     | 23 	| filename           	| string       	|
     | 24 	| hash_id            	| string       	|
     | 25 	| sourceid           	| string       	|
     | 26 	| registry_state     	| string       	|
     | 27 	| datasetname        	| string       	|
     | 28 	| timestamp          	| bigint       	|
     | 29 	| transaction_status 	| string       	|     

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_pm_projects**.

 Sentencia: ```show partitions rci_network_db.tx_pm_projects```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                                   	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------	|--------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 24  	| 342   	| 1      	| 161.45KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/pm_projects/year=2019/month=12/day=24 	|

- **Ejecuciones**

 En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

 ```
 select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_pm_projects';
 ```

  | id_execution 	| table_name     	| dateload 	| avro_name                                                       	| start_execution     	| end_execution 	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|----------------	|----------	|-----------------------------------------------------------------	|---------------------	|---------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_pm_projects 	| 20191224 	| /data/RCI/raw/ppm/pm_projects/data/20191224_tx_pm_projects.avro 	| 2019-12-24 01:25:54 	| NULL          	| 0      	|         	|                	| 0        	|   	|

- **Cifras de Control**

 En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

 ```
 select * from rci_network_db.tx_cifras_control
 where datasetname = 'tx_pm_projects'
 and dateload = 20191224
 order by filedate asc;
 ```

  | uuid 	| rowprocessed 	| datasetname      	| filedate 	| filename                          	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|------------------	|----------	|-----------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 342          	| pm_projects      	| 20191224 	| 20191224_tx_pm_projects.avro      	| PPM      	| 20191225 	| 342        	| 342          	| 0            	| 0            	|

## Componentes del procesos de ingestión:

 __Framework de Ingestión Automatizado__

 - Especificar parámetros del proceso kite:

 | Parámetro | Valor | Descripción|
 | ---------- | ---------- | ---------- |
 | parametro_01   | 57   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 57
   ```

## <a name="PM_WORK_PLANS"></a>PM_WORK_PLANS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [PM_WORK_PLANS](../../../../RCI_DataAnalysis/eda/PPM/PM_WORK_PLANS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/PM_WORK_PLANS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_pm_work_plans```

     | Id 	| Nombre de Columna     	| Tipo de Dato 	|
     |----	|-----------------------	|--------------	|
     | 1  	| work_plan_id          	| string       	|
     | 2  	| entity_type           	| string       	|
     | 3  	| version               	| string       	|
     | 4  	| master_work_plan_id   	| string       	|
     | 5  	| work_plan_template_id 	| string       	|
     | 6  	| work_plan_name        	| string       	|
     | 7  	| owner_user_id         	| string       	|
     | 8  	| description           	| string       	|
     | 9  	| is_active_flag        	| string       	|
     | 10 	| obsolete_flag         	| string       	|
     | 11 	| project_id            	| string       	|
     | 12 	| work_plan_seq         	| string       	|
     | 13 	| is_copy_flag          	| string       	|
     | 14 	| root_task_id          	| string       	|
     | 15 	| lock_reason           	| string       	|
     | 16 	| lock_timeout          	| string       	|
     | 17 	| unlock_time           	| string       	|
     | 18 	| source                	| string       	|
     | 19 	| source_type_code      	| string       	|
     | 20 	| created_by            	| string       	|
     | 21 	| creation_date         	| string       	|
     | 22 	| last_updated_by       	| string       	|
     | 23 	| last_update_date      	| string       	|
     | 24 	| baseline_type         	| string       	|
     | 25 	| cost_contour_id       	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 26 	| filedate           	| bigint       	|
     | 27 	| filename           	| string       	|
     | 28 	| hash_id            	| string       	|
     | 29 	| sourceid           	| string       	|
     | 30 	| registry_state     	| string       	|
     | 31 	| datasetname        	| string       	|
     | 32 	| timestamp          	| bigint       	|
     | 33 	| transaction_status 	| string       	|          

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_pm_work_plans**.

 Sentencia: ```show partitions rci_network_db.tx_pm_work_plans```

  | year 	| month 	| day 	| #Rows 	| #Files 	| Size     	| Format 	| Incremental stats 	| Location                                                                                     	|
  |------	|-------	|-----	|-------	|--------	|----------	|--------	|-------------------	|----------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 24  	| 791   	| 1      	| 313.41KB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/pm_work_plans/year=2019/month=12/day=24 	|

- **Ejecuciones**

  En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

  ```
  select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_pm_work_plans';
  ```

  | id_execution 	| table_name       	| dateload 	| avro_name                                                           	| start_execution     	| end_execution 	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|------------------	|----------	|---------------------------------------------------------------------	|---------------------	|---------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_pm_work_plans 	| 20191224 	| /data/RCI/raw/ppm/pm_work_plans/data/20191224_tx_pm_work_plans.avro 	| 2019-12-24 12:02:45 	| NULL          	| 0      	|         	|                	| 0        	|   	|

- **Cifras de Control**

  En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

  ```
  select * from rci_network_db.tx_cifras_control
  where datasetname = 'tx_pm_work_plans'
  and dateload = 20191224
  order by filedate asc;
  ```

  | uuid 	| rowprocessed 	| datasetname      	| filedate 	| filename                          	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|------------------	|----------	|-----------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 791          	| pm_work_plans    	| 20191224 	| 20191224_tx_pm_work_plans.avro    	| PPM      	| 20191225 	| 791        	| 791          	| 0            	| 0            	|

## Componentes del procesos de ingestión:

 __Framework de Ingestión Automatizado__

 - Especificar parámetros del proceso kite:

 | Parámetro | Valor | Descripción|
 | ---------- | ---------- | ---------- |
 | parametro_01   | 83   | Valor de correspondiente al flujo|

    Sentencia kite:

   ```
   ./rci_ingesta_generacion_avro.sh {parametro_01}
   ```
   Ejemplo:

   ```
   ./rci_ingesta_generacion_avro.sh 83
   ```


## <a name="WP_TASK_ACTUALS"></a>WP_TASK_ACTUALS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [WP_TASK_ACTUALS](../../../../RCI_DataAnalysis/eda/PPM/WP_TASK_ACTUALS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/WP_TASK_ACTUALS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_wp_task_actuals```

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 1  	| actuals_id         	| string       	|
     | 2  	| version            	| string       	|
     | 3  	| act_duration       	| string       	|
     | 4  	| act_effort         	| string       	|
     | 5  	| act_finish_date    	| string       	|
     | 6  	| act_start_date     	| string       	|
     | 7  	| est_finish_date    	| string       	|
     | 8  	| est_rem_effort     	| string       	|
     | 9  	| perc_complete      	| string       	|
     | 10 	| created_by         	| string       	|
     | 11 	| creation_date      	| string       	|
     | 12 	| last_updated_by    	| string       	|
     | 13 	| last_update_date   	| string       	|
     | 14 	| tot_sched_duration 	| string       	|
     | 15 	| owner_task_id      	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 16 	| filedate           	| bigint       	|
     | 17 	| filename           	| string       	|
     | 18 	| hash_id            	| string       	|
     | 19 	| sourceid           	| string       	|
     | 20 	| registry_state     	| string       	|
     | 21 	| datasetname        	| string       	|
     | 22 	| timestamp          	| bigint       	|
     | 23 	| transaction_status 	| string       	|          

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_wp_task_actuals**.

 Sentencia: ```show partitions rci_network_db.tx_wp_task_actuals```

  | year 	| month 	| day 	| #Rows  	| #Files 	| Size    	| Format 	| Incremental stats 	| Location                                                                                       	|
  |------	|-------	|-----	|--------	|--------	|---------	|--------	|-------------------	|------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 24  	| 278872 	| 1      	| 90.97MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/wp_task_actuals/year=2019/month=12/day=24 	|

- **Ejecuciones**

   En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

   ```
   select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_wp_task_actuals';
   ```

  | id_execution 	| table_name         	| dateload 	| avro_name                                                               	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|--------------------	|----------	|-------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_wp_task_actuals 	| 20191226 	| /data/RCI/raw/ppm/wp_task_actuals/data/20191224_tx_wp_task_actuals.avro 	| 2019-12-26 11:43:56 	| 2019-12-26 11:45:13 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

   En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

   ```
   select * from rci_network_db.tx_cifras_control
   where datasetname = 'tx_wp_task_actuals'
   and dateload = 20191224
   order by filedate asc;
   ```

  | uuid 	| rowprocessed 	| datasetname      	| filedate 	| filename                          	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|------------------	|----------	|-----------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 278872       	| wp_task_actuals  	| 20191224 	| 20191224_tx_wp_task_actuals.avro  	| PPM      	| 20191225 	| 278872     	| 278872       	| 0            	| 0            	|

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 84   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 84
```


## <a name="WP_TASK_INFO"></a>WP_TASK_INFO

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [WP_TASK_INFO](../../../../RCI_DataAnalysis/eda/PPM/WP_TASK_INFO/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/WP_TASK_INFO/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_wp_task_info```

     | Id 	| Nombre de Columna       	| Tipo de Dato 	|
     |----	|-------------------------	|--------------	|
     | 1  	| task_info_id            	| string       	|
     | 2  	| version                 	| string       	|
     | 3  	| activity_id             	| string       	|
     | 4  	| critical_path_task      	| string       	|
     | 5  	| auto_effort_mode        	| string       	|
     | 6  	| milestone_manual_conv   	| string       	|
     | 7  	| name                    	| string       	|
     | 8  	| task_desc               	| string       	|
     | 9  	| override_activity       	| string       	|
     | 10 	| priority                	| string       	|
     | 11 	| task_type_code          	| string       	|
     | 12 	| role_id                 	| string       	|
     | 13 	| role_explicit           	| string       	|
     | 14 	| schedule_code           	| string       	|
     | 15 	| schedule_health         	| string       	|
     | 16 	| slack                   	| string       	|
     | 17 	| status                  	| string       	|
     | 18 	| eligible_task_count     	| string       	|
     | 19 	| exception_task_count    	| string       	|
     | 20 	| total_exception_count   	| string       	|
     | 21 	| unassigned_work_unit_id 	| string       	|
     | 22 	| required                	| string       	|
     | 23 	| created_by              	| string       	|
     | 24 	| creation_date           	| string       	|
     | 25 	| last_updated_by         	| string       	|
     | 26 	| last_update_date        	| string       	|
     | 27 	| owner_task_id           	| string       	|
     | 28 	| service_id              	| string       	|
     | 29 	| service_name            	| string       	|
     | 30 	| override_service        	| string       	|     

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 31 	| filedate           	| bigint       	|
     | 32 	| filename           	| string       	|
     | 33 	| hash_id            	| string       	|
     | 34 	| sourceid           	| string       	|
     | 35 	| registry_state     	| string       	|
     | 36 	| datasetname        	| string       	|
     | 37 	| timestamp          	| bigint       	|
     | 38 	| transaction_status 	| string       	|     


 - **Particiones**

   A continuación se presentan las particiones creadas de la tabla **tx_wp_task_info**.

   Sentencia: ```show partitions rci_network_db.tx_wp_task_info```

  | year 	| month 	| day 	| #Rows  	| #Files 	| Size    	| Format 	| Incremental stats 	| Location                                                                                    	|
  |------	|-------	|-----	|--------	|--------	|---------	|--------	|-------------------	|---------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 24  	| 156839 	| 1      	| 54.71MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/wp_task_info/year=2019/month=12/day=24 	|

 - **Ejecuciones**

      En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

      ```
      select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_wp_task_info';
      ```

  | id_execution 	| table_name      	| dateload 	| avro_name                                                         	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|-----------------	|----------	|-------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_wp_task_info 	| 20191224 	| /data/RCI/raw/ppm/wp_task_info/data/20191225_tx_wp_task_info.avro 	| 2019-12-24 21:25:39 	| 2019-12-24 21:26:46 	| 1      	|         	|                	| 0        	|   	|

 - **Cifras de Control**

      En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

      ```
      select * from rci_network_db.tx_cifras_control
      where datasetname = 'tx_wp_task_info'
      and dateload = 20191224
      order by filedate asc;
      ```

  | uuid 	| rowprocessed 	| datasetname      	| filedate 	| filename                          	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|------------------	|----------	|-----------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 156839       	| wp_task_info     	| 20191224 	| 20191224_tx_wp_task_info.avro     	| PPM      	| 20191225 	| 156839     	| 156839       	| 0            	| 0            	|

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 85   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 85
```


## <a name="WP_TASK_SCHEDULE"></a>WP_TASK_SCHEDULE

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [WP_TASK_SCHEDULE](../../../../RCI_DataAnalysis/eda/PPM/WP_TASK_SCHEDULE/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/WP_TASK_SCHEDULE/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_wp_task_schedule```

     | Id 	| Nombre de Columna 	| Tipo de Dato 	|
     |----	|-------------------	|--------------	|
     | 1  	| task_schedule_id  	| string       	|
     | 2  	| version           	| string       	|
     | 3  	| sched_duration    	| string       	|
     | 4  	| sched_effort      	| string       	|
     | 5  	| sched_finish_date 	| string       	|
     | 6  	| sched_start_date  	| string       	|
     | 7  	| early_finish      	| string       	|
     | 8  	| early_start       	| string       	|
     | 9  	| late_finish       	| string       	|
     | 10 	| late_start        	| string       	|
     | 11 	| created_by        	| string       	|
     | 12 	| creation_date     	| string       	|
     | 13 	| last_updated_by   	| string       	|
     | 14 	| last_update_date  	| string       	|
     | 15 	| owner_task_id     	| string       	|    

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 16 	| filedate           	| bigint       	|
     | 17 	| filename           	| string       	|
     | 18 	| hash_id            	| string       	|
     | 19 	| sourceid           	| string       	|
     | 20 	| registry_state     	| string       	|
     | 21 	| datasetname        	| string       	|
     | 22 	| timestamp          	| bigint       	|
     | 23 	| transaction_status 	| string       	|      

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_wp_task_schedule**.

 Sentencia: ```show partitions rci_network_db.tx_wp_task_schedule```

  | year 	| month 	| day 	| #Rows  	| #Files 	| Size    	| Format 	| Incremental stats 	| Location                                                                                        	|
  |------	|-------	|-----	|--------	|--------	|---------	|--------	|-------------------	|-------------------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 24  	| 278872 	| 1      	| 89.90MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/wp_task_schedule/year=2019/month=12/day=24 	|

- **Ejecuciones**

    En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

    ```
    select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_wp_task_schedule';
    ```

  | id_execution 	| table_name          	| dateload 	| avro_name                                                                 	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|---------------------	|----------	|---------------------------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_wp_task_schedule 	| 20191224 	| /data/RCI/raw/ppm/wp_task_schedule/data/20191225_tx_wp_task_schedule.avro 	| 2019-12-24 22:43:08 	| 2019-12-24 22:44:30 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

    En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

    ```
    select * from rci_network_db.tx_cifras_control
    where datasetname = 'tx_wp_task_schedule'
    and dateload = 20191224
    order by filedate asc;
    ```

  | uuid 	| rowprocessed 	| datasetname      	| filedate 	| filename                          	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|------------------	|----------	|-----------------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 278872       	| wp_task_schedule 	| 20191224 	| 20191224_tx_wp_task_schedule.avro 	| PPM      	| 20191225 	| 278872     	| 278872       	| 0            	| 0            	|

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 86   | Valor de correspondiente al flujo|

Sentencia kite:

```
./rci_ingesta_generacion_avro.sh {parametro_01}
```
Ejemplo:

```
./rci_ingesta_generacion_avro.sh 86
```


## <a name="WP_TASKS"></a>WP_TASKS

<<<<<<< HEAD
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14481193)
=======
Para mas detalle revisar la siguiente documentacion: [Data Lake Guide](http://10.103.133.122/app/owncloud/f/14480776)
>>>>>>> 8cf4d4f4476c1993f4306b6e3d71c6ddbf259596

## Descripción de la fuentes de datos
- **Descripción**
  [WP_TASKS](../../../../RCI_DataAnalysis/eda/PPM/WP_TASKS/README.md)

- **Diccionario de Datos**
     [Diccionario de Datos](../../../../RCI_DataAnalysis/eda/PPM/WP_TASKS/README.md)

     Sentencia: ```describe formatted rci_network_db.tx_wp_tasks```

     | Id 	| Nombre de Columna      	| Tipo de Dato 	|
     |----	|------------------------	|--------------	|
     | 1  	| task_id                	| string       	|
     | 2  	| version                	| string       	|
     | 3  	| task_actuals_id        	| string       	|
     | 4  	| calendar_constraint_id 	| string       	|
     | 5  	| task_cost_id           	| string       	|
     | 6  	| milestone_id           	| string       	|
     | 7  	| task_notification_id   	| string       	|
     | 8  	| outline_level          	| string       	|
     | 9  	| parent_task_id         	| string       	|
     | 10 	| path_id_list           	| string       	|
     | 11 	| task_schedule_id       	| string       	|
     | 12 	| sequence_number        	| string       	|
     | 13 	| task_info_id           	| string       	|
     | 14 	| task_userdata_id       	| string       	|
     | 15 	| child_task_seq         	| string       	|
     | 16 	| work_plan_id           	| string       	|
     | 17 	| msp_uid                	| string       	|
     | 18 	| business_uid           	| string       	|
     | 19 	| created_by             	| string       	|
     | 20 	| creation_date          	| string       	|
     | 21 	| last_updated_by        	| string       	|
     | 22 	| last_update_date       	| string       	|
     | 23 	| mapping_type           	| string       	|
     | 24 	| external_uid           	| string       	|

     Las siguientes columnas son creadas para la identidad de la fuente:

     | Id 	| Nombre de Columna  	| Tipo de Dato 	|
     |----	|--------------------	|--------------	|
     | 25 	| filedate           	| bigint       	|
     | 26 	| filename           	| string       	|
     | 27 	| hash_id            	| string       	|
     | 28 	| sourceid           	| string       	|
     | 29 	| registry_state     	| string       	|
     | 30 	| datasetname        	| string       	|
     | 31 	| timestamp          	| bigint       	|
     | 32 	| transaction_status 	| string       	|     

- **Particiones**

 A continuación se presentan las particiones creadas de la tabla **tx_wp_tasks**.

 Sentencia: ```show partitions rci_network_db.tx_wp_tasks```

  | year 	| month 	| day 	| #Rows  	| #Files 	| Size    	| Format 	| Incremental stats 	| Location                                                                                	|
  |------	|-------	|-----	|--------	|--------	|---------	|--------	|-------------------	|-----------------------------------------------------------------------------------------	|
  | 2019 	| 12    	| 24  	| 138848 	| 1      	| 47.54MB 	| AVRO   	| false             	| hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ppm/wp_tasks/year=2019/month=12/day=24 	|

- **Ejecuciones**

     En la siguiente tabla se enlistan las ejecuciones que contiene la tabla ejecutando el siguiente comando:

     ```
     select * from rci_metadata_db.tx_rci_executions where table_name = 'tx_wp_tasks';
     ```

  | id_execution 	| table_name  	| dateload 	| avro_name                                                 	| start_execution     	| end_execution       	| status 	| command 	| id_application 	| attempts 	|   	|
  |--------------	|-------------	|----------	|-----------------------------------------------------------	|---------------------	|---------------------	|--------	|---------	|----------------	|----------	|---	|
  | 1            	| tx_wp_tasks 	| 20191224 	| /data/RCI/raw/ppm/wp_tasks/data/20191225_tx_wp_tasks.avro 	| 2019-12-24 23:10:32 	| 2019-12-24 23:11:35 	| 1      	|         	|                	| 0        	|   	|

- **Cifras de Control**

     En la siguiente tabla se enlistan las cifras de control que contiene la tabla ejecutando el siguiente comando:    

     ```
     select * from rci_network_db.tx_cifras_control
     where datasetname = 'tx_wp_tasks'
     and dateload = 20191224
     order by filedate asc;
     ```

  | uuid 	| rowprocessed 	| datasetname 	| filedate 	| filename                  	| sourceid 	| dateload 	| read_count 	| insert_count 	| update_count 	| delete_count 	|
  |------	|--------------	|-------------	|----------	|---------------------------	|----------	|----------	|------------	|--------------	|--------------	|--------------	|
  |      	| 138848       	| wp_tasks    	| 20191224 	| 20191224_tx_wp_tasks.avro 	| PPM      	| 20191225 	| 138848     	| 138848       	| 0            	| 0            	|

## Componentes del procesos de ingestión:

   __Framework de Ingestión Automatizado__

   - Especificar parámetros del proceso kite:

   | Parámetro | Valor | Descripción|
   | ---------- | ---------- | ---------- |
   | parametro_01   | 87   | Valor de correspondiente al flujo|

   Sentencia kite:

  ```
  ./rci_ingesta_generacion_avro.sh {parametro_01}
  ```
  Ejemplo:

  ```
  ./rci_ingesta_generacion_avro.sh 87
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
