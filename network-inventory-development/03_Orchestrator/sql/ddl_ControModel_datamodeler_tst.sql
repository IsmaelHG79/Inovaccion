-- DDL Script to Build Control Model for Repository Central Inventory for test purposes (RCI)
-- Axity
-- April, 2020
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para registrar el catálogo de fuentes a ingestar.
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_metadata.cfg_rci_source_tst;
create table rci_db_metadata.cfg_rci_source_tst
(
	ctl_sid						int		    comment 'Es el identificador único asociada a la fuente.',
	source_name					string		comment 'Es el nombre con el que se identifica la fuente ingestada.',
	is_automatic				int     	comment '1=Indica que el archivo llega de forma automatica, 0=El archivo es depositado manualmente en el FTP',
	hour_in						string  	comment 'Hora de llegada del archivo en formato 24 horas',
	tech_source					string  	comment 'Indica si la fuente es archivo=file, base de datos=db u odk=odk',
    created_by					string		comment 'Usuario que inserta el registro',
	created_on					timestamp	comment 'Fecha de alta del registro',
	updated_by					string		comment 'Usuario que actuliza el registro',
	updated_on					timestamp	comment 'Fecha de modificación del registro',
	primary key(ctl_sid)
)
comment 'Tabla para registrar el catálogo de fuentes a ingestar.'
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla que registra las tablas existentes en el proyecto.
-- Ejecuta en impala
--drop table if exists rci_db_metadata.cfg_rci_table_tst;
create table rci_db_metadata.cfg_rci_table_tst
(
	ctl_tid						int			comment 'Identificador único de la tabla.',
	ctl_sid						int			comment 'Identificador único de la fuente asociada.',
	table_name					string		comment 'Nombre de la tabla asociada a la ejecución',
	programed					int			comment 'Campo para indicar si la fuente esta programada para ejecución automática',
	table_status			    string		comment 'Estatus de la tabla - a (Activo) i (Inactivo) -',
    type_source                 string      comment 'Campo para indicar el tipo de información que tiene la tabla: - i (Inventario), ni (noInventario) ',
    lifecycle                   string      comment 'Campo para identificar al ciclo de vida de la tabla: - p (planning), a (acquisition), w (warehouse), wo (warehouse out), i (installation), o (operation), d (decommissioning)',
	created_by					string		comment 'Usuario que inserta el registro',
	created_on					timestamp	comment 'Fecha de alta del registro',
	updated_by					string		comment 'Usuario que actuliza el registro',
	updated_on					timestamp	comment 'Fecha de modificación del registro',
	primary key(ctl_tid,ctl_sid)	
)
comment 'Tabla que registra las tablas existentes en el proyecto.'
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla que almacena las configuraciones de las tablas necesarias para ser ejecutadas por el Modelo de Control
-- Ejecutar en impala
--drop table if exists rci_db_metadata.cfg_rci_table_config_tst;
create table rci_db_metadata.cfg_rci_table_config_tst
(
	ctl_tid					int		    comment 'Identificador único de la tabla asociada a la configuración.',
	environment_config		string		comment 'Id del ambiente asociado a la configuración, DEV=Desarrollo, QA=Pruebas, PRO=Producción.',
	path_hdfs				string		comment 'Ruta del HDFS donde se depositaran los datos insertados en la tabla.',
	path_backup				string		comment 'Ruta del file system donde se depositaran los esquemas procesados.',
	ban_process_all			int		    comment 'Bandera para indicar si el procesamiento es masivo o archivo por archivo, 0=Archivo, 1=Mascivo.',
	path_avsc_all			string		comment 'Ruta donde se encuentran todos los esquemas a procesar, se lee cuando la ban_process_all es igual a 1.',
	path_avro_all			string		comment 'Ruta donde se encuentran todos los avros a procesar, se lee cuando la ban_process_all es igual a 1.',
	schema_database			string		comment 'Esquema de la base de datos en donde se creara la tabla.',
	json_partition			string		comment 'Ruta en donde estará el json que definira la particion de la tabla.',
	command_kite			string		comment 'Comando que ejecutara el shell de kite para crear la tabla.',
	key_columns				string		comment 'Columnas para definir la llave (hash_id) que generara el componente de spark.',
	path_avro_cifras		string		comment 'Ruta de donde leeremos el archivo avro generado por Nifi que contiene las cifras de control.',
	type_load				string		comment 'Indica el tipo de carga que se realizara, full=carga todo, nofull=carga incremental. nofull, puede ser cualquier otra palabra.',
	number_partitions		int		    comment 'Valor que indica el numero de particiones que se creara para la comprension.',
	command_spark			string		comment 'Comando para invocar el componente de Spark.',
	path_avro_not_processed	string		comment 'Ruta para indicar donde se depositarán los archivos que no se procesaran debido a que no contienen información procesable.',
	created_by				string		comment 'Usuario que inserta el registro',
	created_on				timestamp	comment 'Fecha de alta del registro',
	updated_by				string		comment 'Usuario que actuliza el registro',
	updated_on				timestamp	comment 'Fecha de modificación del registro',
	primary key(ctl_tid,environment_config)
)
comment 'Tabla que almacena las configuraciones de las tablas necesarias para ser ejecutadas por el Modelo de Control.'
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');
		
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para registrar los procesadores de Nifi y sus propiedades.
-- Ejecuta en impala
--drop table if exists rci_db_metadata.cfg_rci_nifi_tst;
create table rci_db_metadata.cfg_rci_nifi_tst
(
	ctl_tid					int		    comment 'Identificador único de la tabla asociada a la configuración.',
	environment_config		string		comment 'Id del ambiente asociado a la configuración, DEV=Desarrollo, QA=Pruebas, PRO=Producción.',
	processor_name		    string		comment 'Nombre del procesador',
	id_processor		    string		comment 'Identificador del procesador',
	level                   int     	comment 'Indica el nivel hacia abajo con el que cuenta el procesador principal',
	sub_processor_name      string  	comment 'Es el nombre del sub procesador de nivel 2 ',
	id_sub_processor        string  	comment 'Identificador del sub procesador',
	processor_status  		string		comment 'Estatus del procesador, S (Apagado), R (Prendido)',
	created_by				string		comment 'Usuario que inserta el registro',
	created_on				timestamp	comment 'Fecha de alta del registro',
	updated_by				string		comment 'Usuario que actuliza el registro',
	updated_on				timestamp	comment 'Fecha de modificación del registro',
	primary key(ctl_tid,environment_config)
)
comment 'Tabla para registrar los procesadores de NiFi y sus propiedades.'
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para registrar la configuracion de la fuente para ejecutarse automaticamente.
-- Ejecuta en impala
--drop table if exists rci_db_metadata.cfg_rci_config_orchestration_tst;
create table rci_db_metadata.cfg_rci_automation_config_tst
(
	ctl_tid			       		int		    comment 'Identificador único de la tabla asociada a la configuración.',
	environment_config			string		comment 'Id del ambiente asociado a la configuración, DEV=Desarrollo, QA=Pruebas, PRO=Producción.',
    ctl_sid               		int  	    comment 'Id de la fuente por procesar',
    periodicity             	string  	comment 'Indica la periodicidad con la que llega la fuente, d=diaria, s=semanal, m=mensual',
    src_server                  string  	comment 'Servidor de donde se debe tomar el archivo',
    path_in                 	string  	comment 'Ruta del FTP donde se deposita el archivo con la información a ingestar',
    recursive_read          	int     	comment '1=Indica que la ruta tiene subcarpetas, 0=Solo hay archivos',
    name_expression_file    	string  	comment 'Expresion que debe cumplir el nombre del archivo a ser leido, "all" lee todo',
    attempts_read_avro          int         comment 'Numero de intento para esperar la generacion de los archivo AVRO',
    times_wait_avro             string      comment 'Tiempo de espera en minutos para esperar a que se generen los archivos AVRO en la ruta del FTP, en formato (5,3,2,1)',
    --is_automatic            	int     	comment '1=Indica que el archivo llega de forma automatica, 0=El archivo es depositado manualmente en el FTP',
    attempts_read           	int     	comment 'Numero de intentos de lectura para obtener el archivo de la ruta FTP, HDFS o BD',
    time_wait               	int     	comment 'Tiempo de espera en minutos entre intento de lectura del archivo de la ruta FTP, HDFS o BD',
    responsible_of_source   	string  	comment 'Nombre de quien deposita el archivo en el FTP de forma manual',
    email_responsible       	string  	comment 'Correo de quien deposita la fuente manualmente en el FTP',
    use_nifi                	int     	comment '1=Indica que la fuente usa un flujo de Nifi,0=No usa flujo Nifi',
    crontab_config          	string  	comment 'Hora en la que debe ejecutar el proceso',
	programed			        int		    comment 'Campo para indicar si la fuente esta programada para ejecución automática',
	referenced_tables			string		comment 'Campo usado para indicar que una tabla debe ejecutarse como flujo principal, y que tiene flujos dependientes de ella. Formato 145,146,147. Si no hay flujos dependientes poner NA',
	created_by			        string		comment 'Usuario que inserta el registro',
	created_on			        timestamp	comment 'Fecha de alta del registro',
	updated_by			        string		comment 'Usuario que actuliza el registro',
	updated_on			        timestamp	comment 'Fecha de modificación del registro',
    primary key(ctl_tid,environment_config)
)
comment 'Tabla para registrar la configuracion de la fuente para ejecutarse automaticamente.'
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla que registra si se ejecutará una ingesta o no.
-- Ejecuta en impala
--drop table if exists rci_db_metadata.cr_rci_validation_tst;
create table rci_db_metadata.cr_rci_validation_tst
(
	ctl_tid						int			comment 'Identificador único de la tabla asociada a la configuración.',
	dateload					int			comment 'Fecha de registro de la alerta',
	ctl_eid                     string      comment 'Es el ID con el que reconoceremos la carga dentro del proceso',
	environment_config			string		comment 'Id del ambiente asociado a la configuración, DEV=Desarrollo, QA=Pruebas, PRO=Producción.',
	start_validation			timestamp	comment 'Hora inicio de la validación de archivos en el FTP',
	end_validation				timestamp	comment 'Hora fin de la validación de archivos en el FTP',
	command_shell				string		comment 'Comando que se utilizó para buscar los archivos',
	result_count				int			comment 'Número de archivos encontrados',
	num_attempts				int			comment 'Número de intentos de lectura sobre la ruta del FTP para obtener los archivos',
	status_validation		    string		comment 'Status de la validación de archivos.',
	status_server			    string		comment 'Status de la validación del server.',
	status_paths				string		comment 'Status de la validación de los paths.',
	id_nifi_exe 				string		comment 'Identificador unico de la ejecución NiFi asociada',
	created_by					string		comment 'Usuario que inserta el registro',
	created_on					timestamp	comment 'Fecha de alta del registro',
	updated_by					string		comment 'Usuario que actuliza el registro',
	updated_on					timestamp	comment 'Fecha de modificación del registro',
	--primary key (id_table,dateload,ctl_eid,start_validation)
	primary key (ctl_tid,dateload,ctl_eid,environment_config)
)
comment 'Tabla que registra si se ejecutará una ingesta o no.'
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para registrar el detalle de las ejecuciones de procesadores Nifi que se llevaran a cabo
-- Ejecuta en impala
--drop table if exists rci_db_metadata.cr_rci_nifi_status_detail_tst;
create table rci_db_metadata.cr_rci_nifi_process_detail_tst
(
	id_nifi_exe 				string			comment 'Identificador unico de la ejecución Nifi',
	ctl_eid                     string         	comment 'Es el ID con el que reconoceremos la carga dentro del proceso',
	power_on_date				timestamp		comment 'Hora de encendido del procesador',
	power_on_response			string			comment 'Respuesta del cluster de Nifi al encender el procesador',
	power_off_date				timestamp		comment 'Hora de apagado del procesador',
	power_off_response			string			comment 'Respuesta del cluster de Nifi al apagar el procesador',
	id_processor				string			comment 'Identificador del procesador asociado a la ejecución',
	status_process				string	    	comment 'Estatus de la ejecución del procesador Nifi',
	user_name					string			comment 'Usuario con el que se realizó la invocación al CLI de Nifi',
	hostname            		string   		comment 'Servidor desde donde fue ejecutado el componente',
	created_by					string			comment 'Usuario que inserta el registro',
	created_on					timestamp		comment 'Fecha de alta del registro',
	updated_by					string			comment 'Usuario que actuliza el registro',
	updated_on					timestamp		comment 'Fecha de modificación del registro',
	primary key(id_nifi_exe,ctl_eid,power_on_date)
)
comment 'Tabla para registrar el detalle de las ejecuciones de procesadores Nifi que se llevaran a cabo.'
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para almacenar los eventos del proceso de ingesta.
-- Ejecuta en impala
--drop table if exists rci_db_metadata.cr_rci_events_tst;
create table rci_db_metadata.cr_rci_events_tst
(
	id_event					int			    comment 'Identificador del evento',
	ctl_tid						int 			comment 'Identificador de la fuente asociada a la fase',
	ctl_eid                     string         	comment 'Es el ID con el que reconoceremos la carga dentro del proceso',
	start_event					timestamp		comment 'Hora inicio de la ejecución de la fase',
	end_event					timestamp		comment 'Hora fin de la ejecución de la fase',
	dateload					int			    comment 'Fecha de registro',
	status_event				string			comment 'Estatus del evento',
	created_by					string			comment 'Usuario que inserta el registro',
	created_on					timestamp		comment 'Fecha de alta del registro',
	updated_by					string			comment 'Usuario que actuliza el registro',
	updated_on					timestamp		comment 'Fecha de modificación del registro',
	primary key(id_event,ctl_tid,ctl_eid,start_event)
)
comment 'Tabla para almacenar los eventos del proceso de ingesta.'
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla que registra los archivos que se estarán ingestando.
-- Ejecuta en impala
--drop table if exists rci_db_metadata.cr_rci_ingestion_files_tst;
create table rci_db_metadata.cr_rci_ingestion_files_tst
(
	id_group					bigint		comment 'Número para identificar el grupo de ejecuciones realizadas, servirá para agrupar las ejecuciones por día',
	id_ingestion_file			bigint		comment 'Consecutivo del archivo avro a ingestar',
	ctl_tid						int 		comment 'ID la tabla asociada a la ejecución',
	ctl_eid                     string      comment 'Es el ID con el que reconoceremos la carga dentro del proceso',
	dateload					int			comment 'Fecha de la ejecución',
	avro_name					string		comment 'Nombre del avro procesado',
	start_execution				timestamp	comment 'Hora de inicio de la ejecución',
	end_execution				timestamp	comment 'Hora de fin de la ejecución',
	status_ingestion			string		comment 'Estatus de la ejecucion',
	command						string		comment 'Comando de Spark con el que fue creada la ejecución',
	id_application				string		comment 'Id generado por yarn para la ejecución de Spark',
	attempts					int			comment 'Número de intentos para realizar la ejecución',
	created_by					string		comment 'Usuario que inserta el registro',
	created_on					timestamp	comment 'Fecha de alta del registro',
	updated_by					string		comment 'Usuario que actuliza el registro',
	updated_on					timestamp	comment 'Fecha de modificación del registro',
	primary key(id_group,id_ingestion_file,ctl_tid,ctl_eid)
)
comment 'Tabla que registra los archivos que se estarán ingestando.'
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para registrar las cifras de control de las cargas realizadas.
-- Ejecuta en impala
--drop table if exists rci_db_inventory.cr_rci_statistics_tst;
create table rci_db_inventory.cr_rci_statistics_tst
(
	ctl_tid				        int		    comment 'Es el nombre de la tabla que se proceso.',
    ctl_sid                     int         comment 'Es el Id con el que se identifica la fuente que se proceso',
    ctl_eid                     string      comment 'Es el ID con el que reconoceremos la carga dentro del proceso',
	dateload	        		bigint		comment 'Es la fecha en que se realizó la carga de la fuente.',
	ctl_file_date	        	bigint		comment 'Es la fecha recuperada del nombre del archivo procesado.',
	ctl_file_name	        	string		comment 'Es el nombre del archivo que se proceso en la ejecución.',
	rowprocessed				bigint		comment 'Indica el número de registros procesados en cada ejecución.',
	read_count	        		bigint		comment 'Es el número de registros leidos de la fuente procesada.',
	insert_count	    		bigint		comment 'Es el número de registros insertados en la tabla.'
)
comment 'Tabla para registrar las cifras de control de las cargas realizadas.'
stored as parquet
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Catálogo de los eventos definidos en el proceso de ingesta.
-- Ejecuta en impala
--drop table if exists rci_db_metadata.cg_rci_events_catalog;
create table rci_db_metadata.cg_rci_events_catalog_tst
(
	id_event					int			    comment 'Identificador del evento registrado',
	event						string		    comment 'Mensaje completo',
	event_desc					string		    comment 'Mensaje completo con parámetros',
	event_order					int			    comment 'Indica el orden en que se lleva acabo la fase',
	created_by					string			comment 'Usuario que inserta el registro',
	created_on					timestamp		comment 'Fecha de alta del registro',
	updated_by					string			comment 'Usuario que actuliza el registro',
	updated_on					timestamp		comment 'Fecha de modificación del registro',
	primary key(id_event)
)
comment 'Catálogo de los eventos definidos en el proceso de ingesta.'
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');