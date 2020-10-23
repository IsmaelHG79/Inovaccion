#!/bin/bash
#set -xv
#------------------------------------------------------------------------------------------------------------#
#	Nombre:           dev_rci_asset_engine_send_mail.sh                                                      #
#	Versión:	      1.1.0                                          			 		                     #
#	Objetivo: 	      Shell encargado de generar la notificación y enviarla por correo electrónico           #
#	Autor:		      ejesus                                                                                 #
#	Vía de ejecución: Desde pyspark, debe estar alojado en el HDFS                                           #
#	Fecha:            22 de Junio de 2020                                                                    #
#	Area:             Datalake AT&T                                                                          #
#------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------#
#						Leer parámetros para la ejecucion	   					   #
#----------------------------------------------------------------------------------#
export param_type_not=$1
export param_sch=$2
export param_tbl=$3
export param_err=$4
export param_type_flow=$5

echo "Recibi tipo notificacion       $param_type_not"
echo "Recibi esquema                 $param_sch"
echo "Recibi nombre tabla            $param_tbl"
echo "Recibi error                   $param_err"
echo "Recibi tipo de flujo           $param_type_flow"

#----------------------------------------------------------------------------------#
#				Definimos variables necesarias para la ejecucion	   		       #
#----------------------------------------------------------------------------------#
export environment="dev"
export group_exec="inventario"

export path_home=/user/raw_rci/attdlkrci/
export path_config=$path_home$environment/"config/"
export path_auth="$path_home"auth/

declare -A properties

#---------------------------------------------------------------#
#			Funcion que lee un archivo properties				#
#---------------------------------------------------------------#
read_properties(){
	print_log "Lectura del archivo: $1"
	hdfs dfs -test -e $1
	res=$?
	if [ 0 -eq $res ]; then 
		print_log "$1 listo para leer."
		while IFS='=' read -r key value; do
		  properties["$key"]="$value"
		done < <(hadoop fs -cat hdfs://attdatalakehdfs/$1)
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
#  Funcion para poner parametros genericos para envio de correo	#
#---------------------------------------------------------------#
put_mail_parameters_ae(){
	echo "oozie.use.system.libpath=True" > notification_ea_"$param_tbl".properties
	echo "security_enabled=False" >> notification_ea_"$param_tbl".properties
	echo "dryrun=False" >> notification_ea_"$param_tbl".properties
	echo "nameNode=hdfs://nameservice1" >> notification_ea_"$param_tbl".properties
	echo "jobTracker=yarnRM" >> notification_ea_"$param_tbl".properties
	echo "notification_mail"=$notification_mail >> notification_ea_"$param_tbl".properties
	echo "support_mail"=$support_mail >> notification_ea_"$param_tbl".properties
	echo "subject"=$subject >> notification_ea_"$param_tbl".properties
	echo "message"=$message >> notification_ea_"$param_tbl".properties
	echo "path_log"=$param_err >> notification_ea_"$param_tbl".properties
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
	hadoop fs -get "$path_auth"raw_rci.keytab .
	kinit -k -t raw_rci.keytab raw_rci@ATTDATALAKE.COM.MX
	export job_generic_id=$(oozie job -oozie https://mxtold01dlu02.attdatalake.com.mx:11443/oozie -auth KERBEROS -run -D oozie.wf.application.path hdfs://attdatalakehdfs/user/hue/oozie/workspaces/hue-oozie-"$ws_wf_generic"/workflow.xml -config notification_ea_"$param_tbl".properties -run)
	echo $job_generic_id > generic_id_"$param_tbl".txt
	export id_oozie=$(cat generic_id_"$param_tbl".txt | awk -F' ' '{ print $2 }')
	echo "id generic:$id_oozie"
	echo ""
	echo ""
}

#---------------------------------------------------------------#
#     Funcion para generar la notificación del Asset Engine	    #
#---------------------------------------------------------------#
create_notification_ae(){
	echo "Tipo notificacion          $param_type_not"
	echo "Tipo de flujo              $param_type_flow"
	export body='<table border=0 width=700px; style="font-family:Arial; font-size:13px; text-align:left;"><tr style="background-color: {3}; color:#FFFFFF;"><th style="color:#000000;" colspan="2">{0}</th></tr><tr style="background-color: #87CEEB; color:#FFFFFF;"><th>Tabla:</th><th style="color:#000000;">{1}</th></tr><tr style="background-color: #87CEEB; color:#FFFFFF;"><th>Fecha:</th><th style="color:#000000;">{2}</th></tr></table>'
		
	case $param_type_flow in
	'clean')
		export type_flow="Process Clean"
		;;
	'asset')
		export type_flow="Asset Engine"
		;;
	'control')
		export type_flow="Semantic Engine"
		;;
	'finance')
		export type_flow="Semantic Finance"
		;;
	'raw')
		export type_flow="Raw"
		;;
	esac
	
	case $param_type_not in
	'start')
		export subject="Inicio procesamiento fuente [$param_tbl] en $type_flow [$date_load]"
		export title="El procesamiento de tabla {0} en el $type_flow."
		export opt="se inicio"
		export color="#87CEEB"
		title_complete=$(echo "${title//'{0}'/\"$opt\"}")
		;;
	'end')
		export subject="Fin procesamiento fuente [$param_tbl] en $type_flow [$date_load]"
		export title="El procesamiento de tabla {0} en el $type_flow."
		export opt="finaliz&oacute;"
		export color="#87CEEB"
		title_complete=$(echo "${title//'{0}'/\"$opt\"}")
		;;
	'error')
		export subject="Error procesamiento fuente [$param_tbl] en $type_flow [$date_load]"
		export title_complete="Ocurri&oacute; un error en el procesamiento de tabla dentro del $type_flow."
		export color="#F3A110"
		;;
	esac
	
	message=$(echo "${body//'{0}'/\"$title_complete\"}")
	message=$(echo "${message//'{1}'/\"$param_sch.$param_tbl\"}")
	message=$(echo "${message//'{2}'/$date_load}")
	message=$(echo "${message//'{3}'/$color}")
}

print_log(){
	echo $1
}

execute_send_notification(){
	getDate
	#leemos el archivo de propiedades
	read_properties "$path_config${environment}_rci_ingesta_generacion_avro.properties"
	size_properties=${#properties[@]}
	print_log "properties longitud: $size_properties"
	if [ 0 -eq $size_properties ]; then
		print_log "Revisar la lectura del archivo de propiedades."
		
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 4: exit 0                              #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 0;
	fi

	set_environment_variables
	create_notification_ae
	put_mail_parameters_ae
	send_notification_ae
	echo "Fin de envío de notificación"
}


#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#								Funcion principal del shell						   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#

execute_send_notification
