-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla que registra las ejecuciones que se generan para la ingesta de una fuente.
-- Ejecuta en impala
drop table if exists rci_metadata_db.tx_rci_executions;
create table rci_metadata_db.tx_rci_executions
(
	id_execution		int				comment 'Identificador de la ejecución',
	table_name			string			comment 'Nombre de la tabla asociada a la ejecución',
	dateload			int				comment 'Fecha de la ejecución',
	avro_name			string			comment 'Nombre del avro procesado',
	start_execution		timestamp		comment 'Hora de inicio de la ejecución',
	end_execution		timestamp		comment 'Hora de fin de la ejecución',
	status				int				comment 'Estatus de la ejecucion, 0=Pendiente, 1=Ejecutada',
	command				string			comment 'Comando de Spark con el que fue creada la ejecución',
	id_application		string			comment 'Id generado por yarn para la ejecución de Spark',
	attempts			int				comment 'Número de intentos para realizar la ejecución',
	primary key(id_execution,table_name,dateload)
)
comment 'Tabla que registra las ejecuciones que se generan para la ingesta de una fuente.'
stored as kudu
tblproperties ('numfiles'='0', 'column_stats_accurate'='false', 'transient_lastddltime'='1549330565', 'numrows'='-1', 'totalsize'='0', 'rawdatasize'='-1', 'orc.compress'='snappy')
;

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para almacenar las propiedades necesarias para ejecutar el framework de ingestion.
-- Ejecuta en impala
drop table if exists rci_metadata_db.tx_rci_config;
create table rci_metadata_db.tx_rci_config
(
	id_source			int				comment 'Identificador numerico de la fuente.',
	table_name			string			comment 'Nombre de la tabla asociada a la ejecución',
	status				int				comment 'Bandera para controlar el cambio de versiones, 1=Activo, 0=Inactivo.',
	date_insert			int				comment 'Fecha en la que se registro el cambio.',
	path_avsc			string			comment 'Ruta donde se encontrara el esquema a procesar en modo cliente.',
	path_hdfs			string			comment 'Ruta del HDFS donde se depositaran los datos insertados en la tabla.',
	path_backup			string			comment 'Ruta del file system donde se depositaran los esquemas procesados.',
	ban_process_all		int				comment 'Bandera para indicar si el procesamiento es masivo o archivo por archivo, 0=Archivo, 1=Mascivo.',
	path_avsc_all		string			comment 'Ruta donde se encuentran todos los esquemas a procesar, se lee cuando la ban_process_all es igual a 1.',
	path_avro_all		string			comment 'Ruta donde se encuentran todos los avros a procesar, se lee cuando la ban_process_all es igual a 1.',
	schema_database		string			comment 'Esquema de la base de datos en donde se creara la tabla.',
	json_partition		string			comment 'Ruta en donde estará el json que definira la particion de la tabla.',
	command_kite		string			comment 'Comando que ejecutara el shell de kite para crear la tabla.',
	path_data_spark		string			comment 'Ruta de donde el componente de spark leera los archivos avros (datos) a ingestar.',
	key_columns			string			comment 'Columnas para definir la llave (hash_id) que generara el componente de spark.',
	path_avro_cifras	string			comment 'Ruta de donde leeremos el archivo avro generado por Nifi que contiene las cifras de control.',
	path_write_cifras	string			comment 'Ruta en donde se escribiran las cifras de conttrol homologadas.',
	type_load			string			comment 'Indica el tipo de carga que se realizara, full=carga todo, nofull=carga incremental. nofull, puede ser cualquier otra palabra.',
	number_partitions	int				comment 'Valor que indica el numero de particiones que se creara para la comprension.',
	command_spark		string			comment 'Comando para invocar el componente de Spark.',
	primary key(id_source,table_name,status,date_insert)
)
comment 'Tabla para almacenar las propiedades necesarias para ejecutar el framework de ingestion.'
stored as kudu
tblproperties ('numfiles'='0', 'column_stats_accurate'='false', 'transient_lastddltime'='1549330565', 'numrows'='-1', 'totalsize'='0', 'rawdatasize'='-1', 'orc.compress'='snappy')
;

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para registrar los procesadores de Nifi y poder controlar sus propiedades.
-- Ejecuta en impala
drop table if exists rci_metadata_db.tx_rci_processor_nifi;
create table rci_metadata_db.tx_rci_processors_nifi
(
	id_source   		int				comment 'Identificador de la fuente asociada a este procesador',
	processor_name		string			comment 'Nombre del procesador',
	dateload			int				comment 'Fecha inserción registro',
	id_processor		string			comment 'Identificador del procesador',
	status				int				comment 'Estatus del procesador, 0=Apagado, 1=Prendido',
	power_on_date		timestamp		comment 'Hora de encendido',
	power_off_date		timestamp		comment 'Hora de apagado',
	usuario				string			comment 'Comando de Spark con el que fue creada la ejecución',
	hostname            string          comment 'Servidor desde donde fue ejecutado el componente',
	primary key(id_source,processor_name,dateload)
)
comment 'Tabla para registrar los procesadores de Nifi y poder controlar sus propiedades.'
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy')
;

