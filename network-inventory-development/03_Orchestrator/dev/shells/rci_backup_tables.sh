#set -xv
#!/bin/bash
#------------------------------------------------------------------------------------------------------------#
#	Nombre:		rci_backup_tables.sh                                          			 		             #
#	Objetivo: 	Shell encargado de ejecutar el backup de las tablas lisadas	                                 #
#	Autor:		ejesus				                                                                         #
#	Vía de ejecución: Línea de comandos		                                                            	 #
#	Fecha:		28 de Enero de 2019  	                                                           		 	 #
#	Area:		Datalake AT&T											                                     #
#------------------------------------------------------------------------------------------------------------#

if [ $# -lt 1 ]
	then
		echo '--------------------------------------------------------------'
		echo "Error: parametros"
		echo "usage: sh $(basename $0) ctl_tid [reset]"
		echo "ctl_tid		Es el id de la tabla definida en la tabla de configuración (rci_db_metadata.cfg_rci_table)."
		echo "reset			Opcional: Valor para indicar que el flujo se debe reiniciar y ejecutar desde el inicio."
		echo '--------------------------------------------------------------'
	exit 1;
fi

#----------------------------------------------------------------------------------#
#						Leer parámetros para la ejecucion	   					   #
#----------------------------------------------------------------------------------#
export a_id_table=$1
export reset=$2

#----------------------------------------------------------------------------------#
#				Definimos variables necesarias para la ejecucion	   		       #
#----------------------------------------------------------------------------------#

export environment="dev"
export group_exec="inventario"
export current_flow="phase_all"

export path_home=/home/raw_rci/attdlkrci/$environment/
export path_shells=$path_home"shells/"
export path_lib=$path_shells"lib/"
export path_config=$path_home"config/"
export path_temp=$path_home"tmp/"
export path_sql=$path_home"sql/"
export path_logs=$path_home"logs/"

#----------------------------------------------------------------------------------#
#				Agregamos las lineas para poder usar las librerias	   		       #
#----------------------------------------------------------------------------------#

#Agregamos las lineas para poder utilizar la librería de logs
. $path_lib/"$environment"_log4j_attdlkrci.sh 1 "$environment"_rci_envia_mail "$environment" "$path_home" "$group_exec" "$a_id_table"
create_dir_logs
echo "Nombre del archivo de log: $name_file"

#Referenciamos el nombre del archivo properties y declaramos el arreglo donde estarán los valores de las variables
export file_properties=$path_config$environment"_rci_ingesta_generacion_avro.properties"
declare -A properties

#Agregamos las lineas para poder utilizar la librería utils
. $path_lib/"$environment"_utils.sh
	
#----------------------------------------------------------------------------------#
#	Variables de ambiente para obtener parametros necesarios para la ejecucion	   #
#----------------------------------------------------------------------------------#

#variables para controlar el flujo de la ejecución
export execution_in_process=0
export execute_all_phases=1
export current_id_event=0
export current_ctl_eid=""
export phase_initialization=0
export init_validation_source=0
export telnet_valid=0
export init_validation_server=0
export init_validation_paths=1
export generate_eid=1
export send_alert_not_execute=0
export send_alert_execute=0
export next=0

export phase_pre_processing=0
export phase_processing=0
export phase_post_processing=0
export execute_phase="all"

# Variables para poder reintentar ejecutar una consulta en caso de desconexión
export intentos=1
export max_intentos=3
declare -A response_f

#Variables para controlar los intentos de lectura
export indice=1
export local_attempts=1
declare -A times_values
export avro_attempts=1

#Definimos arreglos para guardar las N rutas en las que debemos validar la generación de archivos
declare -A paths_avro
declare -A paths_cifras
declare -A paths_not_processed

print_log "Parámetro 1 recibid0 a_id_table:$a_id_table"
print_log "Parámetro 2 recibid0 a_id_table:$reset"

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#						Funciones por fases de ejecucion						   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#								Funcion principal del shell						   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#

#Funcion para ejecutar un invalidate metadata
query_invalidate(){
	print_log "Actualizamos la tabla:$1.$2 ..."
	invalidate_query="invalidate metadata $1.$2"
	execute_querys_without_exit "$invalidate_query" "invalidate_query" 18 "$intentos"
	export invalidate_query=${response_f[invalidate_query]}
}

export
impala_conf="balancer.attdatalake.com.mx -k --ssl"


echo 'Report Snapshot' > /home/raw_rci/attdlkrci/report_snapshot.txt
echo 'rci_db_inventory Snapshot' >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cg_rci_asset_master stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cg_rci_asset_master	; invalidate metadata rci_db_snapshot.cg_rci_asset_master; select count(*) as total, 'rci_db_inventory.cg_rci_asset_master' as source from rci_db_inventory.cg_rci_asset_master union all select count(*) as total, 'rci_db_snapshot.cg_rci_asset_master' as source from rci_db_snapshot.cg_rci_asset_master" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cg_rci_model_properties stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cg_rci_model_properties	; invalidate metadata rci_db_snapshot.cg_rci_model_properties; select count(*) as total, 'rci_db_inventory.cg_rci_model_properties' as source from rci_db_inventory.cg_rci_model_properties union all select count(*) as total, 'rci_db_snapshot.cg_rci_model_properties' as source from rci_db_snapshot.cg_rci_model_properties" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cg_rci_total_rows stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cg_rci_total_rows	; invalidate metadata rci_db_snapshot.cg_rci_total_rows; select count(*) as total, 'rci_db_inventory.cg_rci_total_rows' as source from rci_db_inventory.cg_rci_total_rows union all select count(*) as total, 'rci_db_snapshot.cg_rci_total_rows' as source from rci_db_snapshot.cg_rci_total_rows" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cg_rci_total_stats stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cg_rci_total_stats	; invalidate metadata rci_db_snapshot.cg_rci_total_stats; select count(*) as total, 'rci_db_inventory.cg_rci_total_stats' as source from rci_db_inventory.cg_rci_total_stats union all select count(*) as total, 'rci_db_snapshot.cg_rci_total_stats' as source from rci_db_snapshot.cg_rci_total_stats" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_asset_trace stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_asset_trace	; invalidate metadata rci_db_snapshot.cr_asset_trace; select count(*) as total, 'rci_db_inventory.cr_asset_trace' as source from rci_db_inventory.cr_asset_trace union all select count(*) as total, 'rci_db_snapshot.cr_asset_trace' as source from rci_db_snapshot.cr_asset_trace" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_acn_mapping stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_acn_mapping	; invalidate metadata rci_db_snapshot.cr_rci_acn_mapping; select count(*) as total, 'rci_db_inventory.cr_rci_acn_mapping' as source from rci_db_inventory.cr_rci_acn_mapping union all select count(*) as total, 'rci_db_snapshot.cr_rci_acn_mapping' as source from rci_db_snapshot.cr_rci_acn_mapping" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_ae_processed_sources stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_ae_processed_sources	; invalidate metadata rci_db_snapshot.cr_rci_ae_processed_sources; select count(*) as total, 'rci_db_inventory.cr_rci_ae_processed_sources' as source from rci_db_inventory.cr_rci_ae_processed_sources union all select count(*) as total, 'rci_db_snapshot.cr_rci_ae_processed_sources' as source from rci_db_snapshot.cr_rci_ae_processed_sources" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_anomalies stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_anomalies	; invalidate metadata rci_db_snapshot.cr_rci_anomalies; select count(*) as total, 'rci_db_inventory.cr_rci_anomalies' as source from rci_db_inventory.cr_rci_anomalies union all select count(*) as total, 'rci_db_snapshot.cr_rci_anomalies' as source from rci_db_snapshot.cr_rci_anomalies" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_asset_events stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_asset_events	; invalidate metadata rci_db_snapshot.cr_rci_asset_events; select count(*) as total, 'rci_db_inventory.cr_rci_asset_events' as source from rci_db_inventory.cr_rci_asset_events union all select count(*) as total, 'rci_db_snapshot.cr_rci_asset_events' as source from rci_db_snapshot.cr_rci_asset_events" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_asset_group stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_asset_group	; invalidate metadata rci_db_snapshot.cr_rci_asset_group; select count(*) as total, 'rci_db_inventory.cr_rci_asset_group' as source from rci_db_inventory.cr_rci_asset_group union all select count(*) as total, 'rci_db_snapshot.cr_rci_asset_group' as source from rci_db_snapshot.cr_rci_asset_group" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_asset_identifiers_count_bysrc stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_asset_identifiers_count_bysrc	; invalidate metadata rci_db_snapshot.cr_rci_asset_identifiers_count_bysrc; select count(*) as total, 'rci_db_inventory.cr_rci_asset_identifiers_count_bysrc' as source from rci_db_inventory.cr_rci_asset_identifiers_count_bysrc union all select count(*) as total, 'rci_db_snapshot.cr_rci_asset_identifiers_count_bysrc' as source from rci_db_snapshot.cr_rci_asset_identifiers_count_bysrc" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_asset_identifiers_count_gral stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_asset_identifiers_count_gral	; invalidate metadata rci_db_snapshot.cr_rci_asset_identifiers_count_gral; select count(*) as total, 'rci_db_inventory.cr_rci_asset_identifiers_count_gral' as source from rci_db_inventory.cr_rci_asset_identifiers_count_gral union all select count(*) as total, 'rci_db_snapshot.cr_rci_asset_identifiers_count_gral' as source from rci_db_snapshot.cr_rci_asset_identifiers_count_gral" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_asset_properties_count_bysrc stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_asset_properties_count_bysrc	; invalidate metadata rci_db_snapshot.cr_rci_asset_properties_count_bysrc; select count(*) as total, 'rci_db_inventory.cr_rci_asset_properties_count_bysrc' as source from rci_db_inventory.cr_rci_asset_properties_count_bysrc union all select count(*) as total, 'rci_db_snapshot.cr_rci_asset_properties_count_bysrc' as source from rci_db_snapshot.cr_rci_asset_properties_count_bysrc" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_asset_properties_count_gral stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_asset_properties_count_gral	; invalidate metadata rci_db_snapshot.cr_rci_asset_properties_count_gral; select count(*) as total, 'rci_db_inventory.cr_rci_asset_properties_count_gral' as source from rci_db_inventory.cr_rci_asset_properties_count_gral union all select count(*) as total, 'rci_db_snapshot.cr_rci_asset_properties_count_gral' as source from rci_db_snapshot.cr_rci_asset_properties_count_gral" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_control_processed_sources stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_control_processed_sources	; invalidate metadata rci_db_snapshot.cr_rci_control_processed_sources; select count(*) as total, 'rci_db_inventory.cr_rci_control_processed_sources' as source from rci_db_inventory.cr_rci_control_processed_sources union all select count(*) as total, 'rci_db_snapshot.cr_rci_control_processed_sources' as source from rci_db_snapshot.cr_rci_control_processed_sources" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_finance_processed_sources stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_finance_processed_sources	; invalidate metadata rci_db_snapshot.cr_rci_finance_processed_sources; select count(*) as total, 'rci_db_inventory.cr_rci_finance_processed_sources' as source from rci_db_inventory.cr_rci_finance_processed_sources union all select count(*) as total, 'rci_db_snapshot.cr_rci_finance_processed_sources' as source from rci_db_snapshot.cr_rci_finance_processed_sources" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_processed_records stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_processed_records	; invalidate metadata rci_db_snapshot.cr_rci_processed_records; select count(*) as total, 'rci_db_inventory.cr_rci_processed_records' as source from rci_db_inventory.cr_rci_processed_records union all select count(*) as total, 'rci_db_snapshot.cr_rci_processed_records' as source from rci_db_snapshot.cr_rci_processed_records" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_sem_control_table stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_sem_control_table	; invalidate metadata rci_db_snapshot.cr_rci_sem_control_table; select count(*) as total, 'rci_db_inventory.cr_rci_sem_control_table' as source from rci_db_inventory.cr_rci_sem_control_table union all select count(*) as total, 'rci_db_snapshot.cr_rci_sem_control_table' as source from rci_db_snapshot.cr_rci_sem_control_table" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_sem_finance_table stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_sem_finance_table	; invalidate metadata rci_db_snapshot.cr_rci_sem_finance_table; select count(*) as total, 'rci_db_inventory.cr_rci_sem_finance_table' as source from rci_db_inventory.cr_rci_sem_finance_table union all select count(*) as total, 'rci_db_snapshot.cr_rci_sem_finance_table' as source from rci_db_snapshot.cr_rci_sem_finance_table" >> /home/raw_rci/attdlkrci/report_snapshot.txt
impala-shell -i $impala_conf --database='rci_db_inventory' -q "create table if not exists rci_db_snapshot.cr_rci_statistics stored as parquet TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_inventory.cr_rci_statistics	; invalidate metadata rci_db_snapshot.cr_rci_statistics; select count(*) as total, 'rci_db_inventory.cr_rci_statistics' as source from rci_db_inventory.cr_rci_statistics union all select count(*) as total, 'rci_db_snapshot.cr_rci_statistics' as source from rci_db_snapshot.cr_rci_statistics" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#echo 'rci_db_metadata Snapshot' >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cg_anomalies PRIMARY KEY (id) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cg_anomalies	; invalidate metadata rci_db_snapshot.cg_anomalies; select count(*) as total, 'rci_db_metadata.cg_anomalies' as source from rci_db_metadata.cg_anomalies union all select count(*) as total, 'rci_db_snapshot.cg_anomalies' as source from rci_db_snapshot.cg_anomalies" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cg_clean_patterns PRIMARY KEY (id) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cg_clean_patterns	; invalidate metadata rci_db_snapshot.cg_clean_patterns; select count(*) as total, 'rci_db_metadata.cg_clean_patterns' as source from rci_db_metadata.cg_clean_patterns union all select count(*) as total, 'rci_db_snapshot.cg_clean_patterns' as source from rci_db_snapshot.cg_clean_patterns" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cg_rci_asset_properties PRIMARY KEY (id) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cg_rci_asset_properties	; invalidate metadata rci_db_snapshot.cg_rci_asset_properties; select count(*) as total, 'rci_db_metadata.cg_rci_asset_properties' as source from rci_db_metadata.cg_rci_asset_properties union all select count(*) as total, 'rci_db_snapshot.cg_rci_asset_properties' as source from rci_db_snapshot.cg_rci_asset_properties" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cg_rci_business_identifiers PRIMARY KEY (id) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cg_rci_business_identifiers	; invalidate metadata rci_db_snapshot.cg_rci_business_identifiers; select count(*) as total, 'rci_db_metadata.cg_rci_business_identifiers' as source from rci_db_metadata.cg_rci_business_identifiers union all select count(*) as total, 'rci_db_snapshot.cg_rci_business_identifiers' as source from rci_db_snapshot.cg_rci_business_identifiers" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cg_rci_categories PRIMARY KEY (id) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cg_rci_categories	; invalidate metadata rci_db_snapshot.cg_rci_categories; select count(*) as total, 'rci_db_metadata.cg_rci_categories' as source from rci_db_metadata.cg_rci_categories union all select count(*) as total, 'rci_db_snapshot.cg_rci_categories' as source from rci_db_snapshot.cg_rci_categories" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cg_rci_location PRIMARY KEY (id) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cg_rci_location	; invalidate metadata rci_db_snapshot.cg_rci_location; select count(*) as total, 'rci_db_metadata.cg_rci_location' as source from rci_db_metadata.cg_rci_location union all select count(*) as total, 'rci_db_snapshot.cg_rci_location' as source from rci_db_snapshot.cg_rci_location" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cg_rci_model PRIMARY KEY (id, id_model) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cg_rci_model	; invalidate metadata rci_db_snapshot.cg_rci_model; select count(*) as total, 'rci_db_metadata.cg_rci_model' as source from rci_db_metadata.cg_rci_model union all select count(*) as total, 'rci_db_snapshot.cg_rci_model' as source from rci_db_snapshot.cg_rci_model" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cg_rci_vendor PRIMARY KEY (id) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cg_rci_vendor	; invalidate metadata rci_db_snapshot.cg_rci_vendor; select count(*) as total, 'rci_db_metadata.cg_rci_vendor' as source from rci_db_metadata.cg_rci_vendor union all select count(*) as total, 'rci_db_snapshot.cg_rci_vendor' as source from rci_db_snapshot.cg_rci_vendor" >> /home/raw_rci/attdlkrci/report_snapshot.txt
impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cr_rci_events PRIMARY KEY (id_event, ctl_tid, ctl_eid, start_event) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cr_rci_events	; invalidate metadata rci_db_snapshot.cr_rci_events; select count(*) as total, 'rci_db_metadata.cr_rci_events' as source from rci_db_metadata.cr_rci_events union all select count(*) as total, 'rci_db_snapshot.cr_rci_events' as source from rci_db_snapshot.cr_rci_events" >> /home/raw_rci/attdlkrci/report_snapshot.txt
impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cr_rci_executions_id_references PRIMARY KEY (ctl_tid, ctl_eid) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cr_rci_executions_id_references	; invalidate metadata rci_db_snapshot.cr_rci_executions_id_references; select count(*) as total, 'rci_db_metadata.cr_rci_executions_id_references' as source from rci_db_metadata.cr_rci_executions_id_references union all select count(*) as total, 'rci_db_snapshot.cr_rci_executions_id_references' as source from rci_db_snapshot.cr_rci_executions_id_references" >> /home/raw_rci/attdlkrci/report_snapshot.txt
impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cr_rci_ingestion_file PRIMARY KEY (id_group, id_ingestion_file, ctl_tid, ctl_eid) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cr_rci_ingestion_file	; invalidate metadata rci_db_snapshot.cr_rci_ingestion_file; select count(*) as total, 'rci_db_metadata.cr_rci_ingestion_file' as source from rci_db_metadata.cr_rci_ingestion_file union all select count(*) as total, 'rci_db_snapshot.cr_rci_ingestion_file' as source from rci_db_snapshot.cr_rci_ingestion_file" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cr_rci_nifi_process_detail PRIMARY KEY (id_nifi_exe, ctl_eid, power_on_date) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cr_rci_nifi_process_detail	; invalidate metadata rci_db_snapshot.cr_rci_nifi_process_detail; select count(*) as total, 'rci_db_metadata.cr_rci_nifi_process_detail' as source from rci_db_metadata.cr_rci_nifi_process_detail union all select count(*) as total, 'rci_db_snapshot.cr_rci_nifi_process_detail' as source from rci_db_snapshot.cr_rci_nifi_process_detail" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cr_rci_sources_processed PRIMARY KEY (id) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cr_rci_sources_processed	; invalidate metadata rci_db_snapshot.cr_rci_sources_processed; select count(*) as total, 'rci_db_metadata.cr_rci_sources_processed' as source from rci_db_metadata.cr_rci_sources_processed union all select count(*) as total, 'rci_db_snapshot.cr_rci_sources_processed' as source from rci_db_snapshot.cr_rci_sources_processed" >> /home/raw_rci/attdlkrci/report_snapshot.txt
impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.cr_rci_validation PRIMARY KEY (ctl_tid, dateload, ctl_eid, environment_config) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.cr_rci_validation	; invalidate metadata rci_db_snapshot.cr_rci_validation; select count(*) as total, 'rci_db_metadata.cr_rci_validation' as source from rci_db_metadata.cr_rci_validation union all select count(*) as total, 'rci_db_snapshot.cr_rci_validation' as source from rci_db_snapshot.cr_rci_validation" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.lnk_rci_asset_properties PRIMARY KEY (id, ctl_tid, prop_id) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.lnk_rci_asset_properties	; invalidate metadata rci_db_snapshot.lnk_rci_asset_properties; select count(*) as total, 'rci_db_metadata.lnk_rci_asset_properties' as source from rci_db_metadata.lnk_rci_asset_properties union all select count(*) as total, 'rci_db_snapshot.lnk_rci_asset_properties' as source from rci_db_snapshot.lnk_rci_asset_properties" >> /home/raw_rci/attdlkrci/report_snapshot.txt
#impala-shell -i $impala_conf --database='rci_db_metadata' -q "create table if not exists rci_db_snapshot.lnk_rci_business_identifiers PRIMARY KEY (id, ctl_tid, bid_id) stored as kudu TBLPROPERTIES ('kite.compression.type'='snappy') AS select * from rci_db_metadata.lnk_rci_business_identifiers	; invalidate metadata rci_db_snapshot.lnk_rci_business_identifiers; select count(*) as total, 'rci_db_metadata.lnk_rci_business_identifiers' as source from rci_db_metadata.lnk_rci_business_identifiers union all select count(*) as total, 'rci_db_snapshot.lnk_rci_business_identifiers' as source from rci_db_snapshot.lnk_rci_business_identifiers" >> /home/raw_rci/attdlkrci/report_snapshot.txt
