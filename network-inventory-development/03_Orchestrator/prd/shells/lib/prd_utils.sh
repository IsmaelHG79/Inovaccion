#!/bin/bash
# set -euo pipefail
# set -x
#---------------------------------------------------------------#
#	Nombre:		prd_utils.sh									#
#	Versión:	1.0.1                                           #
#	Objetivo:	Contiene funciones de uso comun					#
#	Autor: 	    ejesus											#
#	Vía de ejecución: Línea de comandos		                    #
#	Fecha:		04 de Noviembre de 2019							#
#	Area:		Datalake AT&T									#
#   Versionamiento: 20200724 Se agregan las variables de la vista de control y financiera #
#---------------------------------------------------------------#

if [ $# -lt 1 ]
	then
		echo '--------------------------------------------------------------'
		echo "Error: parameters"
		echo "usage: sh $(basename $0) tipo_ejecucion"
		echo '--------------------------------------------------------------'
	exit 1
fi

#---------------------------------------------------------------#
#			Area para definir variables globales				#
#---------------------------------------------------------------#
export impala_conf="balancer.attdatalake.com.mx -k --ssl"

#---------------------------------------------------------------#
#			Funcion que lee un archivo properties				#
#---------------------------------------------------------------#
read_properties(){
	print_line
	print_log "Lectura del archivo: $1"
	
	if [ -f "$1" ]; then 
		print_log "$1 listo para leer." 
		
		while IFS='=' read -r key value 
		do 
			#echo "$key => $value"
			#print_log "$key => $value"
			properties["$key"]="$value"
		done < "$1"
	else 
		print_log "$1 no encontrado."
	fi
}

#---------------------------------------------------------------#
#			Funcion que setea las variables de entorno			#
#---------------------------------------------------------------#
set_environment_variables(){
	notification_mail=${properties[notification_mail]}
	notification_mail="$(echo -e "${notification_mail}" | tr -d '[:space:]')"
	print_log "	notification_mail				$notification_mail."
	
	support_mail=${properties[support_mail]}
	support_mail="$(echo -e "${support_mail}" | tr -d '[:space:]')"
	print_log "	support_mail					$support_mail."
	
	ws_wf_notificacion=${properties[ws_wf_notificacion]}
	ws_wf_notificacion="$(echo -e "${ws_wf_notificacion}" | tr -d '[:space:]')"
	print_log "	ws_wf_notificacion				$ws_wf_notificacion."
	
	ws_wf_error_notificaction=${properties[ws_wf_error_notificaction]}
	ws_wf_error_notificaction="$(echo -e "${ws_wf_error_notificaction}" | tr -d '[:space:]')"
	print_log "	ws_wf_error_notificaction                       $ws_wf_error_notificaction."
	
	wspace_oozie_mail=${properties[wspace_oozie_mail]}
	wspace_oozie_mail="$(echo -e "${wspace_oozie_mail}" | tr -d '[:space:]')"
	print_log "	wspace_oozie_mail				$wspace_oozie_mail."
	
	ws_wf_generic=${properties[ws_wf_generic]}
	ws_wf_generic="$(echo -e "${ws_wf_generic}" | tr -d '[:space:]')"
	print_log "	ws_wf_generic				    $ws_wf_generic."
	
	nifi_api=${properties[nifi_api]}
	nifi_api="$(echo -e "${nifi_api}" | tr -d '[:space:]')"
	print_log "	nifi_api					$nifi_api."
	
	number_nodes=${properties[number_nodes]}
	number_nodes="$(echo -e "${number_nodes}" | tr -d '[:space:]')"
	print_log "	number_nodes					$number_nodes."
	
	schema=${properties[schema_table_rci]}
	schema="$(echo -e "${schema}" | tr -d '[:space:]')"
	print_log "	schema						$schema."
	
	schema_config=${properties[schema_table_config]}
	schema_config="$(echo -e "${schema_config}" | tr -d '[:space:]')"
	print_log "	schema_config					$schema_config."
	
	table_execution=${properties[table_execution]}
	table_execution="$(echo -e "${table_execution}" | tr -d '[:space:]')"
	print_log "	table_execution					$table_execution."
	
	table_source=${properties[table_source]}
	table_source="$(echo -e "${table_source}" | tr -d '[:space:]')"
	print_log "	table_source					$table_source."

	table_names=${properties[table_names]}
	table_names="$(echo -e "${table_names}" | tr -d '[:space:]')"
	print_log "	table_names					$table_names."
	
	table_config=${properties[table_config]}
	table_config="$(echo -e "${table_config}" | tr -d '[:space:]')"
	print_log "	table_config					$table_config."
	
	table_statistics=${properties[table_statistics]}
	table_statistics="$(echo -e "${table_statistics}" | tr -d '[:space:]')"
	print_log "	table_statistics				$table_statistics."
	
	table_processors=${properties[table_processors]}
	table_processors="$(echo -e "${table_processors}" | tr -d '[:space:]')"
	print_log "	table_processors				$table_processors."
	
	table_orchestration=${properties[table_orchestration]}
	table_orchestration="$(echo -e "${table_orchestration}" | tr -d '[:space:]')"
	print_log "	table_orchestration				$table_orchestration."
	
	table_validation=${properties[table_validation]}
	table_validation="$(echo -e "${table_validation}" | tr -d '[:space:]')"
	print_log "	table_validation				$table_validation."
	
	table_processors_detail=${properties[table_processors_detail]}
	table_processors_detail="$(echo -e "${table_processors_detail}" | tr -d '[:space:]')"
	print_log "	table_processors_detail			        $table_processors_detail."
	
	table_events=${properties[table_events]}
	table_events="$(echo -e "${table_events}" | tr -d '[:space:]')"
	print_log "	table_events			                $table_events."
	
	table_events_catalog=${properties[table_events_catalog]}
	table_events_catalog="$(echo -e "${table_events_catalog}" | tr -d '[:space:]')"
	print_log "	table_events_catalog			        $table_events_catalog."
	
	table_execution_references=${properties[table_execution_references]}
	table_execution_references="$(echo -e "${table_execution_references}" | tr -d '[:space:]')"
	print_log "	table_execution_references			    $table_execution_references."
	
	table_source_processed=${properties[table_source_processed]}
	table_source_processed="$(echo -e "${table_source_processed}" | tr -d '[:space:]')"
	print_log "	table_source_processed			    $table_source_processed."
	
	table_control=${properties[table_control]}
	table_control="$(echo -e "${table_control}" | tr -d '[:space:]')"
	print_log "	table_control				        $table_control."
	
	table_finance=${properties[table_finance]}
	table_finance="$(echo -e "${table_finance}" | tr -d '[:space:]')"
	print_log "	table_finance				        $table_finance."
	
	path_backup_file=${properties[path_backup_file]}
	path_backup_file="$(echo -e "${path_backup_file}" | tr -d '[:space:]')"
	print_log "	path_backup_file				$path_backup_file."
	
	path_odk_info=${properties[path_odk_info]}
	path_odk_info="$(echo -e "${path_odk_info}" | tr -d '[:space:]')"
	print_log "	path_odk_info					$path_odk_info."
	
	status_active=${properties[status_active]}
	status_active="$(echo -e "${status_active}" | tr -d '[:space:]')"
	print_log "	status_active					$status_active."
	
	status_processing=${properties[status_processing]}
	status_processing="$(echo -e "${status_processing}" | tr -d '[:space:]')"
	print_log "	status_processing               $status_processing."
	
	status_finished_raw=${properties[status_finished_raw]}
	status_finished_raw="$(echo -e "${status_finished_raw}" | tr -d '[:space:]')"
	print_log "	status_finished_raw				$status_finished_raw."
	
	status_processing_odk=${properties[status_processing_odk]}
	status_processing_odk="$(echo -e "${status_processing_odk}" | tr -d '[:space:]')"
	print_log "	status_processing_odk           $status_processing_odk."
	
	status_error_odk=${properties[status_error_odk]}
	status_error_odk="$(echo -e "${status_error_odk}" | tr -d '[:space:]')"
	print_log "	status_error_odk                $status_error_odk."
	
	status_pending_clean=${properties[status_pending_clean]}
	status_pending_clean="$(echo -e "${status_pending_clean}" | tr -d '[:space:]')"
	print_log "	status_pending_clean           $status_pending_clean."
	
	status_processing_clean=${properties[status_processing_clean]}
	status_processing_clean="$(echo -e "${status_processing_clean}" | tr -d '[:space:]')"
	print_log "	status_processing_clean        $status_processing_clean."
	
	status_error_clean=${properties[status_error_clean]}
	status_error_clean="$(echo -e "${status_error_clean}" | tr -d '[:space:]')"
	print_log "	status_error_clean             $status_error_clean."
	
	status_pending_ae=${properties[status_pending_ae]}
	status_pending_ae="$(echo -e "${status_pending_ae}" | tr -d '[:space:]')"
	print_log "	status_pending_ae              $status_pending_ae."
	
	status_processing_ae=${properties[status_processing_ae]}
	status_processing_ae="$(echo -e "${status_processing_ae}" | tr -d '[:space:]')"
	print_log "	status_processing_ae           $status_processing_ae."
	
	status_error_ae=${properties[status_error_ae]}
	status_error_ae="$(echo -e "${status_error_ae}" | tr -d '[:space:]')"
	print_log "	status_error_ae                $status_error_ae."
	
	status_pending_control_view=${properties[status_pending_control_view]}
	status_pending_control_view="$(echo -e "${status_pending_control_view}" | tr -d '[:space:]')"
	print_log "	status_pending_control_view    $status_pending_control_view."
	
	status_processing_control_view=${properties[status_processing_control_view]}
	status_processing_control_view="$(echo -e "${status_processing_control_view}" | tr -d '[:space:]')"
	print_log "	status_processing_control_view $status_processing_control_view."
	
	status_error_control_view=${properties[status_error_control_view]}
	status_error_control_view="$(echo -e "${status_error_control_view}" | tr -d '[:space:]')"
	print_log "	status_error_control_view      $status_error_control_view."

	status_pending_finance=${properties[status_pending_finance]}
	status_pending_finance="$(echo -e "${status_pending_finance}" | tr -d '[:space:]')"
	print_log "	status_pending_finance         $status_pending_finance."
	
	status_processing_finance=${properties[status_processing_finance]}
	status_processing_finance="$(echo -e "${status_processing_finance}" | tr -d '[:space:]')"
	print_log "	status_processing_finance      $status_processing_finance."
	
	status_error_finance=${properties[status_error_finance]}
	status_error_finance="$(echo -e "${status_error_finance}" | tr -d '[:space:]')"
	print_log "	status_error_finance           $status_error_finance."
	
	status_executed=${properties[status_executed]}
	status_executed="$(echo -e "${status_executed}" | tr -d '[:space:]')"
	print_log "	status_executed					$status_executed."
	
	status_no_executed=${properties[status_no_executed]}
	status_no_executed="$(echo -e "${status_no_executed}" | tr -d '[:space:]')"
	print_log "	status_no_executed                              $status_no_executed."
	
	status_power_on=${properties[status_power_on]}
	status_power_on="$(echo -e "${status_power_on}" | tr -d '[:space:]')"
	print_log "	status_power_on					$status_power_on."
	
	status_power_off=${properties[status_power_off]}
	status_power_off="$(echo -e "${status_power_off}" | tr -d '[:space:]')"
	print_log "	status_power_off                                $status_power_off."
	
	send_notification_mail=${properties[send_notification_mail]}
	send_notification_mail="$(echo -e "${send_notification_mail}" | tr -d '[:space:]')"
	print_log "	send_notification_mail                          $send_notification_mail."
	
	status_validation_ok=${properties[status_validation_ok]}
	status_validation_ok="$(echo -e "${status_validation_ok}" | tr -d '[:space:]')"
	print_log "	status_validation_ok                            $status_validation_ok."
	
	status_validation_ko=${properties[status_validation_ko]}
	status_validation_ko="$(echo -e "${status_validation_ko}" | tr -d '[:space:]')"
	print_log "	status_validation_ko                            $status_validation_ko."
	
	status_validation_no_files=${properties[status_validation_no_files]}
	status_validation_no_files="$(echo -e "${status_validation_no_files}" | tr -d '[:space:]')"
	print_log "	status_validation_no_files                      $status_validation_no_files."
	
	status_validation_processing=${properties[status_validation_processing]}
	status_validation_processing="$(echo -e "${status_validation_processing}" | tr -d '[:space:]')"
	print_log "	status_validation_processing                    $status_validation_processing."
	
	status_validation_no_validated=${properties[status_validation_no_validated]}
	status_validation_no_validated="$(echo -e "${status_validation_no_validated}" | tr -d '[:space:]')"
	print_log "	status_validation_no_validated                  $status_validation_no_validated."
	
	status_server_ok=${properties[status_server_ok]}
	status_server_ok="$(echo -e "${status_server_ok}" | tr -d '[:space:]')"
	print_log "	status_server_ok                                $status_server_ok."
	
	status_server_fail=${properties[status_server_fail]}
	status_server_fail="$(echo -e "${status_server_fail}" | tr -d '[:space:]')"
	print_log "	status_server_fail                              $status_server_fail."
	
	status_paths_ok=${properties[status_paths_ok]}
	status_paths_ok="$(echo -e "${status_paths_ok}" | tr -d '[:space:]')"
	print_log "	status_paths_ok                                 $status_paths_ok."
	
	status_paths_ko=${properties[status_paths_ko]}
	status_paths_ko="$(echo -e "${status_paths_ko}" | tr -d '[:space:]')"
	print_log "	status_paths_ko                                 $status_paths_ko."
	
	user=${properties[user]}
	user="$(echo -e "${user}" | tr -d '[:space:]')"
	print_log "	user                                            $user."
}

#---------------------------------------------------------------#
#     Funcion que obtiene la fecha de ejecución del proceso		#
#---------------------------------------------------------------#
getDate() {		
	date_load=$(date +%Y%m%d)
	print_log "Fecha entera obtenida: $date_load"
}

#---------------------------------------------------------------#
#	Funcion generica para ejecutar un query con impala-shell	#
# en caso de error, reintentará la ejecución max_intentos veces.#
#---------------------------------------------------------------#
execute_querys(){
	print_log ""
	print_log ""
	print_log "*****************************************************"
	print_log "Query_$3: $1."
	print_log "*****************************************************"
	print_log ""
	print_log ""
	intentos=$4

	case $2 in
	"query_cifras")
		print_log "Ejecutar consulta desde archivo."
		impala-shell -i $impala_conf --database="$5" -f "$path_sql$environment"_consulta_cifras2_"$id".sql > "$path_temp"resultado_cifras_"$id".txt
		;;
	'query_file')
		print_log "Ejecutar consulta con salida a archivo."
		impala-shell -i $impala_conf --database="$5" -q "$1" -B > "$path_temp$6"
		;;
	*)
		print_log "Ejecución normal del query"
		#Con esta línea escribimos el resultado de la consulta al archivo 1>, y en caso de error direccinamos el resultado al archivo 2>>
		$(impala-shell -i $impala_conf --database="$5" -q "$1" -B 1>"$path_temp"query_"$3"_"$a_id_table".txt 2>>$name_file)
		;;
	esac
	
	res=$?
	print_log "cod_respuesta_Query_$3:$res"

	if [ $res -eq 0 ]; then
		params=$(cat "$path_temp"query_"$3"_"$a_id_table".txt)
		print_log "Resultado Query_$3:"
		print_log "$params"
		print_log "*****************************************************"
		print_log ""
		print_log ""
		#Almacenamos el valor obtenido del query en un arreglo
		response_f["$2"]=$params
		export intentos=0
	else
		if [ $intentos -eq $max_intentos ]; then
			export intentos=0
			print_log "Se agotaron los $max_intentos intentos para Query_$3, terminará con error."
			print_log "Revisar el log asociado para más detalle del error: $name_file"
			print_log "#----------------------------------------------------------------------------------#"
			print_log "#                          Punto de control 12: exit $res                          #"
			print_log "#----------------------------------------------------------------------------------#"
			exit $res;
		fi
		let intentos=$(expr $intentos + 1 )	
		print_log "Hubo un error en Query_$3, se reinterará la ejecucion. próximo Reintento:#$intentos."
		print_log "Revisar el log asociado para más detalle del error: $name_file"
		print_log "*****************************************************"
		print_log ""
		print_log ""
		execute_querys "$1" "$2" "$3" "$intentos" "$5" "$6"
	fi
}

#---------------------------------------------------------------#
#	Funcion generica para ejecutar un query con impala-shell	#
# en caso de error, reintentará la ejecución max_intentos veces.#
#   si no se puede ejecutar la consulta, el flujo continuará    #
#---------------------------------------------------------------#
execute_querys_without_exit(){
	print_log ""
	print_log ""
	print_log "*****************************************************"
	print_log "Query_$3: $1."
	print_log "*****************************************************"
	print_log ""
	print_log ""
	intentos=$4

	case $2 in
	"query_cifras")
		print_log "Ejecutar consulta desde archivo."
		impala-shell -i $impala_conf --database="$5" -f "$path_sql$environment"_consulta_cifras2_"$id".sql > "$path_temp"resultado_cifras_"$id".txt
		;;
	'query_file')
		print_log "Ejecutar consulta con salida a archivo."
		impala-shell -i $impala_conf --database="$5" -q "$1" -B > "$path_temp$6"
		;;
	*)
		print_log "Ejecución normal del query"
		#Con esta línea escribimos el resultado de la consulta al archivo 1>, y en caso de error direccinamos el resultado al archivo 2>>
		$(impala-shell -i $impala_conf --database="$5" -q "$1" -B 1>"$path_temp"query_"$3"_"$a_id_table".txt 2>>$name_file)
		;;
	esac
	
	res=$?
	print_log "cod_respuesta_Query_$3:$res"

	if [ $res -eq 0 ]; then
		params=$(cat "$path_temp"query_"$3"_"$a_id_table".txt)
		print_log "Resultado Query_$3:"
		print_log "$params"
		print_log "*****************************************************"
		print_log ""
		print_log ""
		#Almacenamos el valor obtenido del query en un arreglo
		response_f["$2"]=$params
		export intentos=0
	else
		if [ $intentos -eq $max_intentos ]; then
			export intentos=0
			print_log "Se agotaron los $max_intentos intentos para Query_$3, terminará con error."
			print_log "Revisar el log asociado para más detalle del error: $name_file"
		fi
		let intentos=$(expr $intentos + 1 )	
		print_log "Hubo un error en Query_$3, se reinterará la ejecucion. próximo Reintento:#$intentos."
		print_log "Revisar el log asociado para más detalle del error: $name_file"
		print_log "*****************************************************"
		print_log ""
		print_log ""
		
		print_log "intentos $intentos vs $max_intentos max_intentos"
		if [ $intentos -lt $max_intentos ]; then
			print_log "Invocar funcion"
			execute_querys_without_exit "$1" "$2" "$3" "$intentos" "$5" "$6"
		fi
	fi
}

#---------------------------------------------------------------#
#		Funcion para agregar los parametros necesarios para		#
#			     enviar el correo de no ejecucion			    #
#---------------------------------------------------------------#
put_mail_parameters(){
	echo "oozie.use.system.libpath=True" > "$path_config"alertas_"$a_id_table".properties
	echo "security_enabled=False" >> "$path_config"alertas_"$a_id_table".properties
	echo "dryrun=False" >> "$path_config"alertas_"$a_id_table".properties
	echo "nameNode=hdfs://nameservice1" >> "$path_config"alertas_"$a_id_table".properties
	echo "jobTracker=yarnRM" >> "$path_config"alertas_"$a_id_table".properties
	echo "date_load"=$date_load >> "$path_config"alertas_"$a_id_table".properties
	echo "table_name"=$table_name >> "$path_config"alertas_"$a_id_table".properties
	echo "notification_mail"=$notification_mail >> "$path_config"alertas_"$a_id_table".properties
	echo "esquema_tablas_rci"=$schema >> "$path_config"alertas_"$a_id_table".properties
	echo "responsible_of_source"=$responsible_of_source >> "$path_config"alertas_"$a_id_table".properties
	echo "email_responsible"=$email_responsible >> "$path_config"alertas_"$a_id_table".properties
	echo "reason"=$reason >> "$path_config"alertas_"$a_id_table".properties
	echo "name_source"=$name_source >> "$path_config"alertas_"$a_id_table".properties
	echo "server"=$server >> "$path_config"alertas_"$a_id_table".properties
	echo "path_in"=$path_in >> "$path_config"alertas_"$a_id_table".properties
	echo "periodicity_desc"=$periodicity_desc >> "$path_config"alertas_"$a_id_table".properties
	echo "si_no"=$si_no >> "$path_config"alertas_"$a_id_table".properties
	echo "color"=$color >> "$path_config"alertas_"$a_id_table".properties
	echo "count_file"=$count_file >> "$path_config"alertas_"$a_id_table".properties
	echo "schema_load"=$schema_load  >> "$path_config"alertas_"$a_id_table".properties
}

#---------------------------------------------------------------#
#		Funcion para enviar la notificacion de ingesta			#
#---------------------------------------------------------------#
send_notification(){
	print_log ""
	print_log ""
	print_log "Envío de notificación de ejecución"
	export OOZIE_CLIENT_OPTS='-Djavax.net.ssl.trustStore=/opt/cloudera/security/jks/truststore.jks'
	echo $OOZIE_CLIENT_OPTS
	export job_id_oozie=$(oozie job -oozie https://mxtold01dlu02.attdatalake.com.mx:11443/oozie -auth KERBEROS -run -D oozie.wf.application.path hdfs://attdatalakehdfs/user/hue/oozie/workspaces/hue-oozie-"$ws_wf_notificacion"/workflow.xml -config "$path_config"alertas_"$a_id_table".properties -run)
	echo $job_id_oozie > "$path_temp"oozie_alertas_"$a_id_table".txt
	export id_generado=$(cat "$path_temp"oozie_alertas_"$a_id_table".txt | awk -F' ' '{ print $2 }')
	print_log "id notificación:$id_generado"
	print_log ""
	print_log ""
}

#---------------------------------------------------------------#
#		Funcion para agregar los parametros de error			#
#---------------------------------------------------------------#
put_mail_parameters_error(){
	echo "oozie.use.system.libpath=True" > "$path_config"error_"$a_id_table".properties
	echo "security_enabled=False" >> "$path_config"error_"$a_id_table".properties
	echo "dryrun=False" >> "$path_config"error_"$a_id_table".properties
	echo "nameNode=hdfs://nameservice1" >> "$path_config"error_"$a_id_table".properties
	echo "jobTracker=yarnRM" >> "$path_config"error_"$a_id_table".properties
	echo "date_load"=$date_load >> "$path_config"error_"$a_id_table".properties
	echo "table_name"=$table_name >> "$path_config"error_"$a_id_table".properties
	echo "notification_mail"=$notification_mail >> "$path_config"error_"$a_id_table".properties
	echo "mail_soporte"=$support_mail >> "$path_config"error_"$a_id_table".properties
	echo "esquema_tablas_rci"=$schema >> "$path_config"error_"$a_id_table".properties
	echo "count_file"=$count_file >> "$path_config"error_"$a_id_table".properties
	echo "current_processor_name"=$current_processor_name >> "$path_config"error_"$a_id_table".properties
	echo "name_source"=$name_source >> "$path_config"error_"$a_id_table".properties
	echo "server"=$server >> "$path_config"error_"$a_id_table".properties
	echo "path_in"=$path_in >> "$path_config"error_"$a_id_table".properties
	echo "path_avro_all"=$path_avro_all >> "$path_config"error_"$a_id_table".properties
	echo "num_files_read"=$total_files_read >> "$path_config"error_"$a_id_table".properties
	echo "attempts_read_avro"=$attempts_read_avro >> "$path_config"error_"$a_id_table".properties
	echo "color"=$color >> "$path_config"error_"$a_id_table".properties
	echo "schema_load"=$schema_load  >> "$path_config"error_"$a_id_table".properties
}

#---------------------------------------------------------------#
#		Funcion para enviar alerta de error por correo			#
#---------------------------------------------------------------#
send_notification_error(){
	print_log ""
	print_log ""
	print_log "Envío de alerta por no ejecución"
	export OOZIE_CLIENT_OPTS='-Djavax.net.ssl.trustStore=/opt/cloudera/security/jks/truststore.jks'
	echo $OOZIE_CLIENT_OPTS
	export job_id_oozie=$(oozie job -oozie https://mxtold01dlu02.attdatalake.com.mx:11443/oozie -auth KERBEROS -run -D oozie.wf.application.path hdfs://attdatalakehdfs/user/hue/oozie/workspaces/hue-oozie-"$ws_wf_error_notificaction"/workflow.xml -config "$path_config"error_"$a_id_table".properties -run)
	echo $job_id_oozie > "$path_temp"oozie_alertas_"$a_id_table".txt
	export id_generado=$(cat "$path_temp"oozie_alertas_"$a_id_table".txt | awk -F' ' '{ print $2 }')
	print_log "id alerta:$id_generado"
	print_log ""
	print_log ""
}

#---------------------------------------------------------------#
#	Funcion para obtener la descripcion de la periodicidad		#
#---------------------------------------------------------------#
get_desc_periodicity(){
	case $periodicity_bd in
	'd')
		export periodicity_desc="Diaria"
		;;
	's')
		export periodicity_desc="Semanal"
		;;
	'q')
		export periodicity_desc="Quincenal"
		;;
	'm')
		export periodicity_desc="Mensual"
		;;
	'o')
		export periodicity_desc="OneShot"
		;;
	esac
}

#---------------------------------------------------------------#
#		Funcion para imprimir los valores de las variables		#
#---------------------------------------------------------------#
summary(){
	print_log "#####################################################"
	print_log "#       Resumen de las variables y sus valores      #"
	print_log "#####################################################"
	print_log "execution_in_process     $execution_in_process"
	print_log "execute_all_phases       $execute_all_phases"
	print_log "execute_all_phases_ref   $execute_all_phases_ref"
	print_log "current_id_event         $current_id_event"
	print_log "ctl_eid                  $ctl_eid"
	print_log "phase_initialization     $phase_initialization"
	print_log "generate_eid             $generate_eid"
	print_log "init_validation_source   $init_validation_source"
	print_log "telnet_valid             $telnet_valid"
	print_log "init_validation_server   $init_validation_server"
	print_log "init_validation_paths    $init_validation_paths"
	print_log "send_alert_not_execute   $send_alert_not_execute"
	print_log "send_alert_execute       $send_alert_execute"
	print_log "next                     $next"
	print_log "is_referenced            $is_referenced"
	print_log "phase_pre_processing     $phase_pre_processing"
	print_log "phase_processing         $phase_processing"
	print_log "phase_post_processing    $phase_post_processing"
	print_log "use_nifi                 $use_nifi"
	print_log "#####################################################"
	print_log "#                     FIN                           #"
	print_log "#####################################################"
}

#---------------------------------------------------------------#
#		Funcion para generar el valor del campo ctl_eid			#
#---------------------------------------------------------------#
generate_field_ctl_eid(){
	#para hacer unico este id, se genera con los siguientes valores
	#4 dígitos para el año                2020
	#2 dígitos para el mes                  04
	#2 dígitos para el día                  21
	get_date=$(date '+%Y%m%d')
	
	#2 dígitos para la hora                 17
	#2 dígitos para el minutos              01
	#2 dígitos para el segundo              34
	get_time=$(date '+%H%M%S')
	
	#3 dígitos para el id de la fuente     001
	let aut_id_source=$(expr $1 - 0 )
	export aut_id_source=$(printf %03d $aut_id_source)
	
	#5 dígitos para el id de la tabla    00007
	let aut_id_table=$(expr $2 - 0 )
	export aut_id_table=$(printf %05d $aut_id_table)
	
	export ctl_eid=${get_date}${get_time}${aut_id_source}${aut_id_table}
	print_log "El id execution será:$ctl_eid"
}

#---------------------------------------------------------------#
#   Funcion que genera variables para enviar correo de cifras	#
#---------------------------------------------------------------#
put_parameters_oozie_mail(){
	echo "oozie.use.system.libpath=True" > "$path_config"cifras_"$a_id_table".properties
	echo "security_enabled=False" >> "$path_config"cifras_"$a_id_table".properties
	echo "dryrun=False" >> "$path_config"cifras_"$a_id_table".properties
	echo "nameNode=hdfs://nameservice1" >> "$path_config"cifras_"$a_id_table".properties
	echo "jobTracker=yarnRM" >> "$path_config"cifras_"$a_id_table".properties
	echo "cifras_mail="$cifras_mail >> "$path_config"cifras_"$a_id_table".properties	
	echo "date_load"=$date_load  >> "$path_config"cifras_"$a_id_table".properties
	echo "table_name"=$table_name  >> "$path_config"cifras_"$a_id_table".properties
	echo "notification_mail"=$notification_mail  >> "$path_config"cifras_"$a_id_table".properties
	echo "schema_table_rci"=$schema  >> "$path_config"cifras_"$a_id_table".properties
	echo "schema_table_config"=$schema_config  >> "$path_config"cifras_"$a_id_table".properties
	echo "table_statistics"=$table_statistics  >> "$path_config"cifras_"$a_id_table".properties
	echo "schema_load"=$schema_load  >> "$path_config"cifras_"$a_id_table".properties
}

#---------------------------------------------------------------#
#		Funcion para enviar cifras de control por correo		#
#---------------------------------------------------------------#
invoca_oozie_cifras(){
	print_log ""
	print_log ""
	print_log "Invocando Oozie para envio de cifras de control"
	export OOZIE_CLIENT_OPTS='-Djavax.net.ssl.trustStore=/opt/cloudera/security/jks/truststore.jks'
	echo $OOZIE_CLIENT_OPTS
	
	export OBTENJOB=$(oozie job -oozie https://mxtold01dlu02.attdatalake.com.mx:11443/oozie -auth KERBEROS -run -D oozie.wf.application.path hdfs://attdatalakehdfs/user/hue/oozie/workspaces/hue-oozie-"$wspace_oozie_mail"/workflow.xml -config "$path_config"cifras_"$a_id_table".properties -run)
	echo $OBTENJOB > "$path_temp"oozie_job_rci_"$id".txt
	export OOZIEJOB=$(cat "$path_temp"oozie_job_rci_"$id".txt | awk -F' ' '{ print $2 }')
	print_log "El id del workflow es: $OOZIEJOB"
	print_log ""
	print_log ""
}

#---------------------------------------------------------------#
#		    Funcion actualizar la tabla de validación		    #
#---------------------------------------------------------------#
update_validation(){
	# $1 tipo de validación
	# $2 número de consulta
	
	case $1 in
		1 )
			query_update_validacion="update $schema_config.$table_validation set num_attempts=$local_attempts, status_validation='$status_validation_no_files', status_server='$status_validation_no_validated', id_nifi_exe='NA', updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and ctl_eid='$ctl_eid' "
			;;
		2 )
			query_update_validacion="update $schema_config.$table_validation set status_server='$status_server_ok', updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and ctl_eid='$ctl_eid' "
			;;
		3 )
			query_update_validacion="update $schema_config.$table_validation set status_validation='$status_validation_ko', status_server='$status_server_fail', updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and ctl_eid='$ctl_eid' "
			;;
		4 )
			query_update_validacion="update $schema_config.$table_validation set status_validation='$status_validation_ok', status_paths='$status_paths_ok', updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and ctl_eid='$ctl_eid' "
			;;
		5 )
			query_update_validacion="update $schema_config.$table_validation set status_validation='$status_validation_ko', status_paths='$status_paths_ko', updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and ctl_eid='$ctl_eid' "
			;;
		6 )
			query_update_validacion="update $schema_config.$table_validation set num_attempts=$local_attempts, status_validation='$status_validation_ok', status_server='$status_validation_no_validated', id_nifi_exe='NA', updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and ctl_eid='$ctl_eid' "
			;;
		7 )
			query_update_validacion="update $schema_config.$table_validation set end_validation='$validation_end', status_validation='$status_validation_ok', id_nifi_exe='$id_nifi_exe', updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and ctl_eid='$ctl_eid' "
			;;
		8 )
			query_update_validacion="update $schema_config.$table_validation set end_validation='$validation_end', updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and ctl_eid='$ctl_eid' "
			;;
	esac
	insert_update_validation "$query_update_validacion" $2
	
	if [ 1 -eq $is_referenced ]; then
		case $1 in
			1 )
				query_update_validacion="update $schema_config.$table_validation set num_attempts=$local_attempts, status_validation='$status_validation_no_files', status_server='$status_validation_no_validated', id_nifi_exe='NA', updated_by='$user', updated_on=now() where ctl_tid in ($param_referenced) and dateload=$date_load and ctl_eid='$ctl_eid' "
				;;
			2 )
				query_update_validacion="update $schema_config.$table_validation set status_server='$status_server_ok', updated_by='$user', updated_on=now() where ctl_tid in ($param_referenced) and dateload=$date_load and ctl_eid='$ctl_eid' "
				;;
			3 )
				query_update_validacion="update $schema_config.$table_validation set status_validation='$status_validation_ko', status_server='$status_server_fail', updated_by='$user', updated_on=now() where ctl_tid in ($param_referenced) and dateload=$date_load and ctl_eid='$ctl_eid' "
				;;
			4 )
				query_update_validacion="update $schema_config.$table_validation set status_validation='$status_validation_ok', status_paths='$status_paths_ok', updated_by='$user', updated_on=now() where ctl_tid in ($param_referenced) and dateload=$date_load and ctl_eid='$ctl_eid' "
				;;
			5 )
				query_update_validacion="update $schema_config.$table_validation set status_validation='$status_validation_ko', status_paths='$status_paths_ko', updated_by='$user', updated_on=now() where ctl_tid in ($param_referenced) and dateload=$date_load and ctl_eid='$ctl_eid' "
				;;
			6 )
				query_update_validacion="update $schema_config.$table_validation set num_attempts=$local_attempts, status_validation='$status_validation_ok', status_server='$status_validation_no_validated', id_nifi_exe='NA', updated_by='$user', updated_on=now() where ctl_tid in ($param_referenced) and dateload=$date_load and ctl_eid='$ctl_eid' "
				;;
			7 )
				query_update_validacion="update $schema_config.$table_validation set end_validation='$validation_end', status_validation='$status_validation_ok', id_nifi_exe='$id_nifi_exe', updated_by='$user', updated_on=now() where ctl_tid in ($param_referenced) and dateload=$date_load and ctl_eid='$ctl_eid' "
				;;
			8 )
				query_update_validacion="update $schema_config.$table_validation set end_validation='$validation_end', updated_by='$user', updated_on=now() where ctl_tid in ($param_referenced) and dateload=$date_load and ctl_eid='$ctl_eid' "
				;;
		esac
	fi
	
	insert_update_validation "$query_update_validacion" $2
}

#---------------------------------------------------------------#
#		Funcion para insertar en la tabla de validation			#
#---------------------------------------------------------------#
insert_update_validation(){
	print_log "Generar registro en la tabla $table_validation"
	execute_querys "$1" "iv" $2 "$intentos" "$schema_config" ""
	result_iv=${response_f[iv]}
	print_log "valor retornado Query_$2:$result_iv."
	print_log ""
	print_log ""
}

#---------------------------------------------------------------#
#		     Funcion generar el campo id_nifi_exe			    #
#---------------------------------------------------------------#
generate_field_nifi_exe(){
	#para hacer unico este id, se genera con los siguientes valores
	#4 dígitos para el año                2020
	#2 dígitos para el mes                  04
	#2 dígitos para el día                  21
	get_date=$(date '+%Y%m%d')
	
	#2 dígitos para la hora                 17
	#2 dígitos para el minutos              01
	#2 dígitos para el segundo              34
	get_time=$(date '+%H%M%S')
	
	export id_nifi_exe=${get_date}${get_time}
	print_log "El id de nifi es:$id_nifi_exe"
}

#---------------------------------------------------------------#
#	Funcion para verificar si hay una ejecución en curso	    #
#---------------------------------------------------------------#
validate_execution_in_progress(){
	print_trace "validate_execution_in_progress"
	
	print_log "#----------------------------------------------------------------------------------#"
	print_log "#                Validar ejecución en progreso para tablas $param                  #"
	print_log "#----------------------------------------------------------------------------------#"

	if [ 1 -eq $is_referenced ]; then
		param="$a_id_table,$param_referenced"
	else
		param=$a_id_table
	fi
	print_log "param es:$param"
	
	#Realizar un conteo para saber si hay alguna ejecución en progreso
	#query_get_in_process="select count(*) as total from $schema_config.$table_events where ctl_tid=$a_id_table and status_event='$status_processing'"
	query_get_in_process="select count(*) as total from $schema_config.$table_events where ctl_tid in ($param) and status_event='$status_processing'"
	execute_querys "$query_get_in_process" "in_progress" 34 "$intentos" "$schema_config" ""
	export in_progress=${response_f[in_progress]}
	
	if [ 0 -lt $in_progress ]; then
		export execution_in_process=1
	fi
}

#---------------------------------------------------------------#
#	Funcion para verificar si hay una ejecución en curso	    #
#---------------------------------------------------------------#
get_param_referenced(){
	#Obtenemos el parámetro de tablas referenciadas para poder realizar validaciones de flujos dependientes
	query_param_referenced="select o.referenced_tables from $schema_config.$table_orchestration o where o.ctl_tid=$a_id_table and lower(o.environment_config)='$environment' "
	execute_querys "$query_param_referenced" "param_referenced" 55 "$intentos" "$schema_config" ""
	export param_referenced=${response_f[param_referenced]}
	
	if [ "NA" != "$param_referenced" -a "\"\"" != "$param_referenced" -a "" != "$param_referenced" ]; then
		export is_referenced=1
		parser_param_referenced
	else
		export is_referenced=0
	fi
}

#---------------------------------------------------------------#
# Funcion para pasar el parámetro param_referenced a un arreglo #
#---------------------------------------------------------------#
parser_param_referenced(){
	if [ 1 -eq $is_referenced ]; then
		count_referenced=$(grep -o "," <<<"$param_referenced" | wc -l)
		let count_referenced=$(expr $count_referenced + 1)

		for i in $( eval echo {1..$count_referenced} )
		do
			p_r=$(echo ${param_referenced} | cut -d"," -f$i) # Obtenemos el id
			p_r="$(echo -e "${p_r}" | tr -d '[:space:]')"
			ids_referenced[$i]="$p_r"
		done
		
		print_log "ids_referenced lon:${#ids_referenced[@]}"
	fi
}

#---------------------------------------------------------------#
#	Funcion para verificar si hay una ejecución incompleta	    #
#---------------------------------------------------------------#
validate_incomplete_execution(){
	print_trace "validate_incomplete_execution" #pending
	#Realizar un conteo para saber si hay alguna fase en estado de PROCESSING
	#Identificamos primero para el flujo único
	print_log "#----------------------------------------------------------------------------------#"
	print_log "#                  Validar ejecución incompleta para tabla $a_id_table             #"
	print_log "#----------------------------------------------------------------------------------#"

	query_get_incomplete="select count(*) as total from $schema_config.$table_events where ctl_tid=$a_id_table and status_event != '$status_executed'"
	execute_querys "$query_get_incomplete" "incomplete" 35 "$intentos" "$schema_config" ""
	export incomplete_master=${response_f[incomplete]}
	
	if [ 0 -lt $incomplete_master ]; then
		execute_all_phases=0
		
		query_get_event="select min(e.id_event) as id_event, e.ctl_eid, t.ctl_sid from $schema_config.$table_events e inner join $schema_config.$table_names t on e.ctl_tid=t.ctl_tid where e.ctl_tid=$a_id_table and e.status_event != '$status_executed' group by e.ctl_eid, t.ctl_sid"
		execute_querys "$query_get_event" "min_event" 35 "$intentos" "$schema_config" ""
		values_event=${response_f[min_event]}
	
		export current_id_event=$(echo ${values_event} | cut -d" " -f1)
		export ctl_eid=$(echo ${values_event} | cut -d" " -f2)
		export ctl_sid=$(echo ${values_event} | cut -d" " -f3)
	else
		execute_all_phases=1
	fi
	
	#Identificamos flujos pendientes para las tablas referenciadas
	if [ 1 -eq $is_referenced ]; then
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#            Validar ejecución incompleta para tablas $param_referenced            #"
		print_log "#----------------------------------------------------------------------------------#"
	
		#El flujo tiene sub flujos
		query_get_incomplete="select count(*) as total from $schema_config.$table_events where ctl_tid in ($param_referenced) and status_event != '$status_executed'"
		
		execute_querys "$query_get_incomplete" "incomplete_referenced" 35 "$intentos" "$schema_config" ""
		export incomplete_referenced=${response_f[incomplete_referenced]}
		
		if [ 0 -lt $incomplete_referenced ]; then
			execute_all_phases_ref=0				
			#Recorrer el resultado para obtener todas las tablas que tiene ejecuciones pendientes
			query_get_event="select min(e.id_event) as id_event, e.ctl_eid, t.ctl_sid, t.ctl_tid from $schema_config.$table_events e inner join $schema_config.$table_names t on e.ctl_tid=t.ctl_tid where e.ctl_tid in ($param_referenced) and e.status_event != '$status_executed' group by e.ctl_eid, t.ctl_sid, t.ctl_tid"
			execute_querys "$query_get_event" "query_file" 50 "$intentos" "$schema_config" "result_events_$a_id_table".txt
			
			#Obtenemos el min evento para saber si se debe reinicar el flujo desde el principio o a partir de algun punto
			query_min_event="select min(e.id_event) as id_event from $schema_config.$table_events e inner join $schema_config.$table_names t on e.ctl_tid=t.ctl_tid where e.ctl_tid in ($param_referenced) and e.status_event != '$status_executed' "
			execute_querys "$query_min_event" "min_event" 51 "$intentos" "$schema_config" ""
			export min_event=${response_f[min_event]}
		else
			execute_all_phases_ref=1
			#print_log "Np hay flujos pendientes... terminar flujo"
			#print_log "#----------------------------------------------------------------------------------#"
			#print_log "#                          Punto de control 13: exit 0                             #"
			#print_log "#----------------------------------------------------------------------------------#"
			#exit 0;
		fi
	fi
}

#---------------------------------------------------------------#
#	Funcion para mapear las funciones a su id de fase   	    #
#---------------------------------------------------------------#
get_pending_flow(){
	t_pending=$(cat "$path_temp"result_events_"$a_id_table".txt | wc -l)
	print_log "Recoreremos $t_pending veces"

	for i in $( eval echo {1..$t_pending} )
	do
		current_event=$(tail -n $i "$path_temp"result_events_"$a_id_table".txt)
		p_event=$(echo ${current_event} | cut -d" " -f1) # Obtiene el id del evento
		p_eid=$(echo ${current_event} | cut -d" " -f2) # Obtiene el id de ejecución
		p_sid=$(echo ${current_event} | cut -d" " -f3) # Obtiene el id de la fuente
		p_tid=$(echo ${current_event} | cut -d" " -f4) # Obtiene el id de la tabla
		
		p_event="$(echo -e "${p_event}" | tr -d '[:space:]')"
		p_eid="$(echo -e "${p_eid}" | tr -d '[:space:]')"
		p_sid="$(echo -e "${p_sid}" | tr -d '[:space:]')"
		p_tid="$(echo -e "${p_tid}" | tr -d '[:space:]')"
		
		events_pending[$i]="$p_tid $p_event"
		
		export current_id_event=$p_event
		export ctl_eid=$p_eid
		export ctl_sid=$p_sid
		
		print_log "Invocar flujo pendiente rci_execute_ingestion_flow.sh $p_tid"
		
		. "$path_shells$environment"_rci_execute_ingestion_flow.sh "$p_tid" &
		print_log "Esperaremos ${time_wait_invoke}m para invocar el $i flujo pendiente ..."
		print_log ""
		print_log ""
		sleep ${time_wait_invoke}m
	done

	print_log ""
	print_log ""
	print_log "Finaliza ejecución de este componente, ya que se ejecutan en 2do plano los pendientes."
	print_log "#----------------------------------------------------------------------------------#"
	print_log "#                          Punto de control 14: exit 0                             #"
	print_log "#----------------------------------------------------------------------------------#"
	exit 0;
}

#---------------------------------------------------------------#
#	Funcion para mapear las funciones a su id de fase   	    #
#---------------------------------------------------------------#
function_mapping(){
	print_trace "function_mapping"
	print_log "Fase detectada: $current_id_event"
	print_log ""
	print_log ""
	
	export current_flow="$current_id_event"
	case $current_id_event in
	1 | 2 | 3 | 4 | 5 | 6)
		export current_flow="phase_all"
		print_log "Ejecutar process_execute_initialization"
		#export generate_eid=0;
		query_delete_validation="delete from $schema_config.$table_validation where ctl_eid='$ctl_eid' and environment_config=upper('$environment') "
		insert_update_validation "$query_delete_validation" 58
		
		query_delete_events="delete from $schema_config.$table_events where ctl_eid='$ctl_eid' "
		insert_update_validation "$query_delete_events" 59
		
		process_execute_initialization
		process_pre_processing
		validate_processing
		;;
	7 | 8 | 9 | 10 | 11)
		print_log "Ejecutar read_avros_process"
		invoke_process_transformation "$a_id_table" "$current_id_event" 0
		;;
	*)
		print_log "Sin fase detectada, revisar logs para más detalle."
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 15: exit 1                             #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 1;
		;;
	esac
}

#---------------------------------------------------------------#
#	Funcion insertar un evento en la tabla de eventos    	    #
#---------------------------------------------------------------#
insert_events(){
	# $1	id_event
	# $2	status
	# $3	num_query
	query_insert_events="insert into $schema_config.$table_events (id_event,ctl_tid,ctl_eid,start_event,end_event,dateload,status_event,created_by,created_on,updated_by,updated_on) values ($1,$a_id_table,'$ctl_eid',now(),null,$date_load,'$2','$user',now(),null,null)"
	execute_querys "$query_insert_events" "ie" $3 "$intentos" "$schema_config" ""
}

#---------------------------------------------------------------#
#Funcion insertar o actualizar un evento en la tabla de eventos #
#---------------------------------------------------------------#
upsert_events(){
	# $1	id_event
	# $2	status
	# $3	num_query
	#Validar si ya tenemos un registro con los valores enviados
	query_validate_reg="select count(*) from $schema_config.$table_events where id_event=$1 and ctl_tid=$a_id_table and ctl_eid='$ctl_eid' "
	execute_querys "$query_validate_reg" "vreg" $3 "$intentos" "$schema_config" ""
	res_validate=${response_f[vreg]}
	print_log "res_validate:$res_validate"
	
	#insert_events 9 "$status_processing" 52
	if [ 0 -eq $res_validate ]; then
		#Realizar el insert
		query_insert_events="insert into $schema_config.$table_events (id_event,ctl_tid,ctl_eid,start_event,end_event,dateload,status_event,created_by,created_on,updated_by,updated_on) values ($1,$a_id_table,'$ctl_eid',now(),null,$date_load,'$2','$user',now(),null,null)"	
	else
		#Realizar el update
		query_insert_events="update $schema_config.$table_events set end_event=now(), status_event='$2', updated_by='$user', updated_on=now() where id_event=$1 and ctl_tid=$a_id_table and ctl_eid='$ctl_eid' "
	fi
	
	execute_querys "$query_insert_events" "ie" $3 "$intentos" "$schema_config" ""
}

#---------------------------------------------------------------#
#	    Funcion insertar un evento para varias tablas    	    #
#---------------------------------------------------------------#
insert_events_all(){
	# $1 Id del evento a insertar
	# $2 Estatus del evento
	# Numero de consulta
	print_log "Insertaremos $count_referenced eventos: $1 $2 $3"
	for idx in $( eval echo {1..$count_referenced} )
	do
		print_log " id $idx es ${ids_referenced[$idx]}"
		print_log " id tabla es $a_id_table"
		print_log " id evento es $1"
		
		#if [ $a_id_table -eq ${ids_referenced[$idx]} ]; then
		if [ $1 -gt 0 -a $1 -lt 7 ]; then
			query_insert_events="insert into $schema_config.$table_events (id_event,ctl_tid,ctl_eid,start_event,end_event,dateload,status_event,created_by,created_on,updated_by,updated_on) values ($1,${ids_referenced[$idx]},'$ctl_eid',now(),null,$date_load,'$2','$user',now(),null,null)"
			execute_querys "$query_insert_events" "ie" $3 "$intentos" "$schema_config" ""
		else
			if [ $a_id_table -eq ${ids_referenced[$idx]} ]; then
				query_insert_events="insert into $schema_config.$table_events (id_event,ctl_tid,ctl_eid,start_event,end_event,dateload,status_event,created_by,created_on,updated_by,updated_on) values ($1,${ids_referenced[$idx]},'$ctl_eid',now(),null,$date_load,'$2','$user',now(),null,null)"
				execute_querys "$query_insert_events" "ie" $3 "$intentos" "$schema_config" ""
			fi
		fi
	done
}

#---------------------------------------------------------------#
#	   Funcion para insertar validaciones de varias tablas    	#
#---------------------------------------------------------------#
insert_validation_all(){
	# $1 Id del evento a insertar
	# $2 Estatus del evento
	# Numero de consulta
		
	print_log "Insertaremos $count_referenced eventos: $1 $2 $3"
	for idx in $( eval echo {1..$count_referenced} )
	do
		print_log " id $idx es ${ids_referenced[$idx]}"		
		query_insert_validation="insert into $schema_config.$table_validation (ctl_tid,dateload,ctl_eid,environment_config,start_validation,end_validation,command_shell,result_count,num_attempts,status_validation,status_server,status_paths,id_nifi_exe,created_by,created_on,updated_by,updated_on) values (${ids_referenced[$idx]},$date_load,'$ctl_eid',upper('$environment'),'$validation_start',null,'$command_prev',$count_file,$local_attempts,'$status_validation_processing',null,null,null,'$user',now(),null,null) "
		insert_update_validation "$query_insert_validation" 25
	done
}

#---------------------------------------------------------------#
#	Funcion actualizar la tabla de eventos y su estatus   	    #
#---------------------------------------------------------------#
update_events(){
	# $1	status
	# $2	id_event
	# $3	Num_query
	
	print_log ""
	print_log ""
	print_log "Update de eventos con param:$param_referenced."
	
	query_update_events="update $schema_config.$table_events set end_event=now(), status_event='$1', updated_by='$user', updated_on=now() where id_event=$2 and ctl_tid=$a_id_table and ctl_eid='$ctl_eid' "
	execute_querys "$query_update_events" "ue" $3 "$intentos" "$schema_config" ""
	
	if [ 1 -eq $is_referenced ]; then
		query_update_events="update $schema_config.$table_events set end_event=now(), status_event='$1', updated_by='$user', updated_on=now() where id_event=$2 and ctl_tid in ($param_referenced) and ctl_eid='$ctl_eid' "
		execute_querys "$query_update_events" "ue" $3 "$intentos" "$schema_config" ""
	fi
}

#---------------------------------------------------------------#
#	Funcion para validar que existe una ruta en el file system  #
#---------------------------------------------------------------#
check_path_file_system(){
	# $1	path a validar
	# $2	Nombre de la ruta a validar
	if [ ! -d "$1" ]; then
		export paths_not_exists=$paths_not_exists$1", "
		export paths_name_not_exists=$paths_name_not_exists$2", "
		export init_validation_paths=0
	else
		print_log "La ruta $1 SI existe"
		if [ 1 -eq $3 ]; then
			print_log "Borraremos el contenido, ejecutar comando:rm $1*.avsc"
			rm $1*.avsc
			print_log ""
			print_log ""
		fi
	fi
}

#---------------------------------------------------------------#
#	Funcion para validar que existe una ruta del HDFS   	    #
#---------------------------------------------------------------#
check_path_hdfs(){
	# $1	Ruta a validar
	# $2	Parámetro para especificar si la ruta debe ser obligatoria o no.
	# $3	Nombre de la ruta a validar
	#Validamos que existan las rutas en HDFS
	if $(hdfs dfs -test -d "$1"); then
		print_log "La ruta $1 SI existe, borraremos el contenido"
		#Borramos el contenido de la carpeta hdfs para no alterar el conteo de los archivos
		print_log "Ejecutar comando:hdfs dfs -rm $1*"
		hdfs dfs -rm "$1"*
		print_log ""
		print_log ""
	else
		if [ 1 -eq $2 ]; then
			export init_validation_paths=0
		else
			export init_validation_paths=1
		fi
		export paths_not_exists=$paths_not_exists$1", ";
		export paths_name_not_exists=$paths_name_not_exists$3", ";
	fi
}

#---------------------------------------------------------------#
#  Funcion para validar una conexión a un host mediante telnet  #
#---------------------------------------------------------------#
check_connection(){
	# $1 host puerto a validar
	print_log ""
	print_log ""
	print_log "Se validará la conexión a la base de datos $1 $2, esperar unos segundos, validando..."
	telnet $1 > "$path_temp$environment"_result_telnet_"$a_id_table".txt
	print_log "Terminó la validación"
	print_log ""
	print_log ""

	export res_tel=$(cat "$path_temp$environment"_result_telnet_"$a_id_table".txt | grep "Connected")

	if [ "" != "$res_tel" ]; then
		export telnet_valid=1
		print_log "Validación telnet exitosa"
	else
		export telnet_valid=0
		print_log "Validación telnet erronea"
	fi
}

#---------------------------------------------------------------#
#  Funcion para validar una conexión a un host mediante telnet  #
#---------------------------------------------------------------#
invoke_process_transformation(){
	name_shell="_rci_ingesta_generacion_avro.sh";
	print_log "Invocando proceso: $path_shells$environment$name_shell"
	print_log "parámetros: $1 $2"
	
	if [ 1 -eq $3 ];then
		. $path_shells$environment$name_shell "$1" "$2" &
		print_log "Esperar ${time_wait_invoke} minuto para proxima regresar control a Shell"
		sleep ${time_wait_invoke}m
	else
		. $path_shells$environment$name_shell "$1" "$2"
	fi
	
	res=$?
	print_log "Respuesta de shell $path_shells$environment$name_shell: $res"
}

#---------------------------------------------------------------#
#  Funcion que marca como finalizado el flujo en file system    #
#---------------------------------------------------------------#
write_status_done(){
	# $1	nombre del shell ejecutar
	touch $path_status/$1
	echo "done" > $path_status/$1
}

#---------------------------------------------------------------#
#Funcion que lee la bandera que indica si un flujo ya se ejecuto #
#---------------------------------------------------------------#
clean_flag_execution(){
	num_ids_flows=$(grep -o "," <<<"$ids_flows" | wc -l)
	let num_ids_flows=$(expr $num_ids_flows + 1)
	count_done=0
	
	if [ "" = "$reset" ]; then
		for idx in $( eval echo {1..$num_ids_flows} )
		do
			current_idp=$(echo $ids_flows | awk -v c=$idx -F',' '{ print $c}')
			print_log "1. Validar flujo $idx => $current_idp"
			if [ -f "$path_status$current_idp" ]; then
				print_log "Archivo tiene:$(find $path_status -type f -name $current_idp | xargs cat)."
				if [ "$(find $path_status -type f -name $current_idp | xargs cat)" = "done" ]; then
					print_log "2. Marcar para borrar bandera del flujo $current_idp"
					print_log ""
					let count_done=$(expr $count_done + 1)
				fi
			fi
		done
	fi
	
	print_log ""
	print_log ""
	print_log "num_ids_flows:$num_ids_flows"
	print_log "count_done:$count_done"
	if [ $num_ids_flows -eq $count_done -o "r" = "$reset" ]; then
		num_ids_flows=$(grep -o "," <<<"$ids_flows" | wc -l)
		let num_ids_flows=$(expr $num_ids_flows + 1)
		count_done=0
		
		for idx in $( eval echo {1..$num_ids_flows} )
		do
			current_idp=$(echo $ids_flows | awk -v c=$idx -F',' '{ print $c}')
			print_log "1. Validar flujo $idx => $current_idp"
			if [ -f "$path_status$current_idp" ]; then
				print_log "Eliminamos bandera del flujo $current_idp"
				rm -f "$path_status$current_idp"
			fi
		done	
	fi
}

#---------------------------------------------------------------#
#          Funcion que valida las banderas de ejecución         #
#---------------------------------------------------------------#
check_flag_execution(){
	num_ids_flows=$(grep -o "," <<<"$ids_flows" | wc -l)
	let num_ids_flows=$(expr $num_ids_flows + 1)
	
	for idx in $( eval echo {1..$num_ids_flows} )
	do
		current_idp=$(echo $ids_flows | awk -v c=$idx -F',' '{ print $c}')
		print_log "1. Flujo $idx es $current_idp"
		if [ -f "$path_status$current_idp" ]; then
			print_log "Archivo tiene:$(find $path_status -type f -name $current_idp | xargs cat)."
			if [ "$(find $path_status -type f -name $current_idp | xargs cat)" != "done" ]; then
				print_log "2. Agregar el flujo $current_idp a lista de pendientes de ejecutar"
				print_log ""
				export pending_flows=$pending_flows$current_idp","
			fi
		else
			print_log "3. Agregar el flujo $current_idp a lista de pendientes de ejecutar"
			print_log ""
			export pending_flows=$pending_flows$current_idp","
		fi
	done
	
	print_log ""
	print_log ""
	export p_flows=$(grep -o "," <<<"$pending_flows" | wc -l)
	print_log "Flujos pendientes $p_flows"
	print_log ""
}

#---------------------------------------------------------------#
#	   Funcion para invocar al shell que genera los Odks		#
#---------------------------------------------------------------#
invoke_odk_shell(){
	print_log "Invocando el shell que genera los Odks"
	
	ctl_eid_origin=$ctl_eid
	
	upsert_events 11 "$status_processing" 58
	
	name_shell="_rci_odk_complement.sh";
	print_log "Invocando proceso: $path_shells$environment$name_shell"
	print_log "parámetros: $flow_continue"
	
	#. $path_shells$environment$name_shell $flow_continue &
	. $path_shells$environment$name_shell $flow_continue

	res=$?
	print_log "Respuesta de shell $path_shells$environment$name_shell: $res"
}

#---------------------------------------------------------------#
#	     Funcion para generar un sólo ctl_eid por tabla 		#
#---------------------------------------------------------------#
generate_eid_references(){
	print_log ""
	print_log ""
	print_log "Generamos ctl_eid para cada tabla referenciada"
	#print_log "Tablas master                  $a_id_table"
	print_log "Tablas master                  $1"
	print_log "Tablas hijas                     $param_referenced"
	print_log "Tablas con mismo eid       $param"
	print_log "ctl_eid master                  $ctl_eid"

	ctl_eid_master=$ctl_eid
	#generate_field_ctl_eid "$ctl_sid" "$a_id_table"
	generate_field_ctl_eid "$ctl_sid" "$1"
	#insert_eid_references $a_id_table $ctl_eid $ctl_eid_master
	insert_eid_references $1 $ctl_eid $ctl_eid_master
}

insert_eid_references(){
	#Obtener el type_source para poner en FINISHED las tablas de tipo COMPLEMENTARY
	get_type_source="select type_source from $schema_config.$table_names where ctl_tid=$1 "
	execute_querys "$get_type_source" "type_source" 61 "$intentos" ""
	type_source=${response_f[type_source]}
	
	refresh_table "$schema" "$table_statistics"
	
	print_log ""
	print_log ""
	print_log "Insertamos el ctl_eid generado"
	
	if [ "COMPLEMENTARY" == "$type_source" ]; then
		query_insert_ref="insert into $schema_config.$table_execution_references (ctl_tid,ctl_eid,ctl_eid_origin,status,dateload,environment_config,created_by,created_on,updated_by,updated_on) values ($1,'$2','$3','$status_executed',$date_load,upper('$environment'),'$user',now(),null,null)"		
	else
		query_insert_ref="insert into $schema_config.$table_execution_references (ctl_tid,ctl_eid,ctl_eid_origin,status,dateload,environment_config,created_by,created_on,updated_by,updated_on) values ($1,'$2','$3','$status_pending_clean',$date_load,upper('$environment'),'$user',now(),null,null)"
	fi
	print_log "$query_insert_ref"
	execute_querys "$query_insert_ref" "iref" 61 "$intentos" "$schema_config" ""
}

#---------------------------------------------------------------#
#  Funcion para poner parametros genericos para envio de correo	#
#---------------------------------------------------------------#
put_mail_parameters_ae(){
	echo "oozie.use.system.libpath=True" > "$path_config"notification_ea_"$table_id".properties
	echo "security_enabled=False" >> "$path_config"notification_ea_"$table_id".properties
	echo "dryrun=False" >> "$path_config"notification_ea_"$table_id".properties
	echo "nameNode=hdfs://nameservice1" >> "$path_config"notification_ea_"$table_id".properties
	echo "jobTracker=yarnRM" >> "$path_config"notification_ea_"$table_id".properties
	echo "notification_mail"=$notification_mail >> "$path_config"notification_ea_"$table_id".properties
	echo "support_mail"=$support_mail >> "$path_config"notification_ea_"$table_id".properties
	echo "subject"=$subject >> "$path_config"notification_ea_"$table_id".properties
	echo "message"=$message >> "$path_config"notification_ea_"$table_id".properties
}

#---------------------------------------------------------------#
#		Funcion para enviar la notificacion de ingesta			#
#---------------------------------------------------------------#
send_notification_ae(){
	echo ""
	echo ""
	echo "Envío de notificación del Asset Engine"
	export OOZIE_CLIENT_OPTS='-Djavax.net.ssl.trustStore=/opt/cloudera/security/jks/truststore.jks'
	echo $OOZIE_CLIENT_OPTS
	export job_generic_id=$(oozie job -oozie https://mxtold01dlu02.attdatalake.com.mx:11443/oozie -auth KERBEROS -run -D oozie.wf.application.path hdfs://attdatalakehdfs/user/hue/oozie/workspaces/hue-oozie-"$ws_wf_generic"/workflow.xml -config "$path_config"notification_ea_"$table_id".properties -run)
	echo $job_generic_id > "$path_temp"generic_id_"$table_id".txt
	export id_oozie=$(cat "$path_temp"generic_id_"$table_id".txt | awk -F' ' '{ print $2 }')
	echo "id generic:$id_oozie"
	echo ""
	echo ""
}

#---------------------------------------------------------------#
#     Funcion para generar la notificación del Asset Engine	    #
#---------------------------------------------------------------#
create_notification_ae(){
	echo "Tipo notificacion:$param_type_not"
	export body='<table border=0 width=700px; style="font-family:Arial; font-size:13px; text-align:left;"><tr style="background-color: {3}; color:#FFFFFF;"><th style="color:#000000;" colspan="2">{0}</th></tr><tr style="background-color: #87CEEB; color:#FFFFFF;"><th>Tabla:</th><th style="color:#000000;">{1}</th></tr><tr style="background-color: #87CEEB; color:#FFFFFF;"><th>Fecha:</th><th style="color:#000000;">{2}</th></tr></table>'
		
	case $param_type_not in
	'start')
		export subject="Inicio procesamiento fuente [$param_tbl] en Asset Engine [$date_load]"
		export title="El procesamiento de tabla {0} en el Asset Engine."
		export opt="se inicio"
		export color="#87CEEB"
		title_complete=$(echo "${title//'{0}'/\"$opt\"}")
		;;
	'end')
		export subject="Fin procesamiento fuente [$param_tbl] en Asset Engine [$date_load]"
		export title="El procesamiento de tabla {0} en el Asset Engine."
		export opt="finaliz&oacute;"
		export color="#87CEEB"
		title_complete=$(echo "${title//'{0}'/\"$opt\"}")
		;;
	'error')
		export subject="Error procesamiento fuente [$param_tbl] en Asset Engine [$date_load]"
		export title_complete="Ocurri&oacute; un error en el procesamiento de tabla dentro del Asset Engine."
		export color="#F3A110"
		;;
	esac
	
	message=$(echo "${body//'{0}'/\"$title_complete\"}")
	message=$(echo "${message//'{1}'/\"$param_sch.$param_tbl\"}")
	message=$(echo "${message//'{2}'/$date_load}")
	message=$(echo "${message//'{3}'/$color}")
}

refresh_table(){
	print_log "refresh de la tabla:$1.$2"
	refresh_query="refresh $1.$2"
	execute_querys_without_exit "$refresh_query" "refresh_tbl" 96 "$intentos" "$1" ""
	
	invalidate_query="invalidate metadata $1.$2"
	execute_querys_without_exit "$invalidate_query" "refresh_tbl" 96 "$intentos" "$1" ""
}

check_counts(){
	get_total_processed="select insert_count,'|',update_count,'|',(insert_count + update_count) as total from $schema.$table_statistics where ctl_tid = $1 and (ctl_eid='$2' or ctl_eid='$3') "
	execute_querys "$get_total_processed" "get_tprocess" 90 "$intentos" ""
	get_tprocess=${response_f[get_tprocess]}
	
	if [ "" == "$get_tprocess" ]; then
		print_log "No se encontraron resultados, por lo cual el registro se marca con estatus $status_executed"
		export put_finish=1
		
		query_insert_ref="update $schema_config.$table_execution_references set status='$status_executed', updated_by='$user', updated_on=now() where (ctl_eid='$2' or ctl_eid_origin='$3') and ctl_tid=$1"
		print_log "$query_insert_ref"
		execute_querys "$query_insert_ref" "iref" 61 "$intentos" "$schema_config" ""
	else
		export total_process=$(echo ${get_tprocess} | cut -d"|" -f3)
		export total_process="$(echo -e "${total_process}" | tr -d '[:space:]')"
		print_log " total_process               $total_process"
		
		if [ 0 -eq $total_process ]; then
			export put_finish=1
			query_insert_ref="update $schema_config.$table_execution_references set status='$status_executed', updated_by='$user', updated_on=now() where (ctl_eid='$2' or ctl_eid_origin='$3') and ctl_tid=$1"
			print_log "$query_insert_ref"
			execute_querys "$query_insert_ref" "iref" 61 "$intentos" "$schema_config" ""
		else
			export put_finish=0
		fi
	fi
	
	print_log " put_finish               $put_finish."
}