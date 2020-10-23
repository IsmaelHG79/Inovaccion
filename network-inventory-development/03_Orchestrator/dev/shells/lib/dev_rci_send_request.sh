#set -xv
#!/bin/bash
#------------------------------------------------------------------------------------------------------------#
#	Nombre:		    dev_rci_send_request.sh                                            			             #
#	Versión:	    1.1.0                                          			 		                         #
#	Objetivo: 	    Shell encargado de realizar el spark submit de los diferentes monitores                  #
#	Autor:		    ejesus				                                                                     #
#	Vía de ejecución: Línea de comandos		                                                            	 #
#	Fecha:		    9 de Julio de 2020  	                                                           		 #
#	Area:		    Datalake AT&T											                                 #
#------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------#
#						Leer parámetros para la ejecucion	   					   #
#----------------------------------------------------------------------------------#

export param_type_request=$1

echo "Recibi param_type_request              $param_type_request"

#----------------------------------------------------------------------------------#
#				Definimos variables necesarias para la ejecucion	   		       #
#----------------------------------------------------------------------------------#

export environment="dev"
export group_exec="inventario"

export path_root=/home/raw_rci/attdlkrci/
export path_home=$path_root$environment/
export path_shells=$path_home"shells/"
export path_lib=$path_shells"lib/"
export path_config=$path_home"config/"
export path_temp=$path_home"tmp/"
export path_sql=$path_home"sql/"
export path_logs=$path_home"logs/"
export path_status=$path_home"status/"
export path_pyspark=$path_home"pyspark/"
export path_pyspark_hdfs="hdfs://attdatalakehdfs/user/raw_rci/attdlkrci/${environment}/pyspark/"
export path_jar_hdfs="hdfs://attdatalakehdfs/user/raw_rci/Pyspark/jars/"

#----------------------------------------------------------------------------------#
#				Agregamos las lineas para poder usar las librerias	   		       #
#----------------------------------------------------------------------------------#

#Agregamos las lineas para poder utilizar el log
. $path_lib/"$environment"_log4j_attdlkrci.sh 6 "${type_monitor_label}_${req_tid}" "$environment" "$path_home" "$group_exec" "${type_monitor_label}_${req_tid}"
create_dir_logs_sync
echo "Nombre del archivo de log: $name_file_sync"

#Referenciamos el nombre del archivo properties y declaramos el arreglo donde estarán los valores de las variables
export file_properties=$path_config$environment"_rci_ingesta_generacion_avro.properties"
declare -A properties

#Agregamos las lineas para poder utilizar la librería utils
. $path_lib/"$environment"_utils.sh

#----------------------------------------------------------------------------------#
#	Variables de ambiente para obtener parametros necesarios para la ejecucion	   #
#----------------------------------------------------------------------------------#
# Variables para poder reintentar ejecutar una consulta en caso de desconexión
export intentos=1
export max_intentos=3
declare -A response_f
export impala_conf="balancer.attdatalake.com.mx -k --ssl"

print_log_sync "El log para darle seguimiento a la ejecución es:"
print_log_sync "$name_file_sync"
print_log_sync ""
print_log_sync ""
print_log_sync "environment                $environment"
print_log_sync "type_monitor_label         $type_monitor_label"
print_log_sync "param_type_request         $param_type_request"
print_log_sync ""
print_log_sync ""

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#						Funciones por fases de ejecucion						             #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#



#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#								Funcion principal del shell						             #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#

send_request_monitor(){
	print_log_sync "#----------------------------------------------------------------------------------#"
	print_log_sync "#                    Se recibe Request con los sigueintes datos                    #"
	print_log_sync "#----------------------------------------------------------------------------------#"
	print_log_sync ""
	print_log_sync ""
	print_log_sync "Tipo request          $param_type_request"
	print_log_sync "ambiente              $req_env"
	print_log_sync "destino               $req_des"
	print_log_sync "esquema               $req_sch"
	print_log_sync "nombre tabla          $req_tbl"
	print_log_sync "ctl_eid               $req_eid"
	print_log_sync "usuario               $user"
	print_log_sync "table_id              $req_tid"

	case $param_type_request in
	1)
		#Query que actualiza el estatus a Processing_X
		query_upd_status="update $schema_config.$table_execution_references set status='$status_processing_clean', updated_by='$user', updated_on=now() where (ctl_eid='$req_eid' or ctl_eid_origin='$req_eid') and ctl_tid=$req_tid"
		
		#Comando para realizar el submit de Spark
		command_to_exec="spark-submit --master yarn --deploy-mode cluster --driver-memory 16g --executor-memory 16g --executor-cores 6 --conf spark.executor.memoryOverhead=4096 --name ${req_env}procces_clean_${req_tbl} --queue=root.rci --jars ${path_jar_hdfs}kudu-spark-tools-1.4.0.jar ${path_pyspark_hdfs}asset_clean.py \"${req_env}\" \"${req_des}\" ${req_sch} ${req_tbl} ${req_eid_send} ${user}"
		
		#Status y mensaje para actualizar el registro en casi de finalizar correctamente y con error
		status_upd=$status_pending_ae
		status_not=$status_error_clean
		msg_end="Termino correctamente el proceso de limpieza $req_tid - $req_tbl"
		msg_ko="Ocurrio un error en el proceso de limpieza $req_tid - $req_tbl"
		param_label=5
		
		query_upd_finish_ok="update $schema_config.$table_execution_references set status='$status_upd', updated_by='$user', updated_on=now() where (ctl_eid='$req_eid' or ctl_eid_origin='$req_eid') and ctl_tid=$req_tid"
		
		query_upd_finish_ko="update $schema_config.$table_execution_references set status='$status_not', updated_by='$user', updated_on=now() where (ctl_eid='$req_eid' or ctl_eid_origin='$req_eid') and ctl_tid=$req_tid"
		;;
	2)
		#Query que actualiza el estatus a Processing_X
		query_upd_status="update $schema_config.$table_execution_references set status='$status_processing_ae', updated_by='$user', updated_on=now() where (ctl_eid='$req_eid' or ctl_eid_origin='$req_eid') and ctl_tid=$req_tid"
		
		#Comando para realizar el submit de Spark
		command_to_exec="spark-submit --master yarn --deploy-mode cluster --num-executors 40 --driver-cores 3 --driver-memory 16g --executor-memory 24g --executor-cores 8 --conf spark.executor.memoryOverhead=4096 --name ${req_env}asset_engine_${req_tbl} --queue=root.rci --jars ${path_jar_hdfs}kudu-spark-tools-1.4.0.jar ${path_pyspark_hdfs}asset_engine.py \"${req_env}\" \"${req_des}\" ${req_sch} ${req_tbl} ${req_eid_send} ${user}"
		
		#Status y mensaje para actualizar el registro en casi de finalizar correctamente y con error
		status_upd=$status_pending_control_view
		status_not=$status_error_ae
		msg_end="Termino correctamente la operacion del asset engine $req_tid - $req_tbl"
		msg_ko="Ocurrio un error al invocar el asset engine $req_tid - $req_tbl"
		param_label=4
		
		query_upd_finish_ok="update $schema_config.$table_execution_references set status='$status_upd', updated_by='$user', updated_on=now() where (ctl_eid='$req_eid' or ctl_eid_origin='$req_eid') and ctl_tid=$req_tid"
		
		query_upd_finish_ko="update $schema_config.$table_execution_references set status='$status_not', updated_by='$user', updated_on=now() where (ctl_eid='$req_eid' or ctl_eid_origin='$req_eid') and ctl_tid=$req_tid"
		;;
	3)		
		#Comando para realizar el submit de Spark
		command_to_exec="spark-submit --master yarn --deploy-mode cluster --driver-memory 8g --executor-memory 8g --executor-cores 5 --conf spark.executor.memoryOverhead=1024 --name ${environment}_control_view_${req_tbl} --queue=root.rci --jars ${path_jar_hdfs}kudu-spark-tools-1.4.0.jar --py-files ${path_pyspark_hdfs}libs.zip ${path_pyspark_hdfs}control_view.py ${environment} \"${req_des}\" "
		
		#Status y mensaje para actualizar el registro en caso de finalizar correctamente y con error
		if [ 1 -eq $req_tid -o 7 -eq $req_tid ]; then
			status_upd=$status_pending_finance
		else
			status_upd=$status_executed
		fi
		status_not=$status_error_control_view
		msg_end="Termino correctamente el proceso de la vista de control $req_tid - $req_tbl"
		msg_ko="Ocurrio un error en el proceso de la vista de control $req_tid - $req_tbl"
		
		query_upd_finish_ok="update $schema_config.$table_execution_references set status='$status_upd', updated_by='$user', updated_on=now() where (ctl_eid='$req_eid' or ctl_eid_origin='$req_eid') and ctl_tid=$req_tid"
		
		query_upd_finish_ko="update $schema_config.$table_execution_references set status='$status_not', updated_by='$user', updated_on=now() where (ctl_eid='$req_eid' or ctl_eid_origin='$req_eid') and ctl_tid=$req_tid"
		;;
	4)
		#Comando para realizar el submit de Spark
		command_to_exec="spark-submit --master yarn --deploy-mode cluster --driver-memory 8g --executor-memory 8g --executor-cores 5 --conf spark.executor.memoryOverhead=1024 --name ${environment}_snapshot_finance --queue=root.rci --jars ${path_jar_hdfs}kudu-spark-tools-1.4.0.jar --py-files ${path_pyspark_hdfs}libs.zip ${path_pyspark_hdfs}snapshot_finance.py ${environment} \"${req_des}\" "
		
		#Status y mensaje para actualizar el registro en casi de finalizar correctamente y con error
		status_upd=$status_executed
		status_not=$status_error_finance
		msg_end="Termino correctamente el proceso de la vista de control $req_tid - $req_tbl"
		msg_ko="Ocurrio un error en el proceso de la vista financiera $req_tid - $req_tbl"
		
		query_upd_finish_ok="update $schema_config.$table_execution_references set status='$status_upd', updated_by='$user', updated_on=now() where (ctl_eid in ($req_eid) or ctl_eid_origin in ($req_eid)) and ctl_tid in ($req_tid) "
		
		query_upd_finish_ko="update $schema_config.$table_execution_references set status='$status_not', updated_by='$user', updated_on=now() where (ctl_eid in ($req_eid) or ctl_eid_origin in ($req_eid)) and ctl_tid in ($req_tid) "
		;;
	esac
	
	case $param_type_request in
	1 | 2 )
		#Actualizamos el estatus del registro: Proccesing_X
		execute_querys "$query_upd_status" "upd_pro" 2 "$intentos" "$req_sch" ""
		;;
	esac
	
	print_log_sync "Invocar ==> $type_monitor_label <== "
	print_log_sync ""
	print_log_sync ""
	print_log_sync "Comando sera:"
	print_log_sync "$command_to_exec"
	print_log_sync ""
	print_log_sync ""

	res_pyspark=$(eval "$command_to_exec" 1>>$name_file_sync 2>>$name_file_sync)
	res_gen=$?

	print_log_sync "res_pyspark:$res_pyspark"
	print_log_sync "res_gen:$res_gen"
	print_log_sync ""
	print_log_sync ""
	
	if [ $res_gen -eq 0 ]; then
		print_log_sync "$msg_end"
		execute_querys "$query_upd_finish_ok" "upd_ref" 2 "$intentos" "$req_sch" ""
		res_upd_ref=${response_f[upd_ref]}
		print_log_sync "res_upd_ref:$res_upd_ref"
		print_log_sync ""
		print_log_sync ""
		print_log_sync "#----------------------------------------------------------------------------------#"
		print_log_sync "# Punto de control 2: Fin correcto de Request ${type_monitor_label} $req_tid - $req_tbl #"
		print_log_sync "#----------------------------------------------------------------------------------#"
	else
		print_log_sync "$msg_ko"
		execute_querys "$query_upd_finish_ko" "upd_ref" 2 "$intentos" "$req_sch" ""
		print_log_sync "Ocurrio un error en Request ${type_monitor_label} $req_tid - $req_tbl"
		print_log_sync "#----------------------------------------------------------------------------------#"
		print_log_sync "#   Punto de control 3: Termina la ejecución de flujo, se pasa control a monitor   #"
		print_log_sync "#----------------------------------------------------------------------------------#"
		#En caso de error en el Semantic Engine, termina el proceso y apagar todos los demas monitores
		case $param_type_request in
		3 )
			print_log_sync "Enviar señal para apagar monitor 1"
			. $path_root"shells"/"rci_start_monitor.sh" $environment 1 "kill" &
			print_log_sync "Enviar señal para apagar monitor 2"
			export type_monitor_label="Asset_Engine"
			put_flag_stop
			print_log_sync "Enviar señal para apagar monitor 4"
			. $path_root"shells"/"rci_start_monitor.sh" $environment 4 "kill" &
			print_log_sync "Terminar el proceso completamente..."
			exit 1;
			;;
		esac
	fi
}

send_request_monitor
