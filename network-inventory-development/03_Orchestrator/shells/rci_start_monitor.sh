#set -xv
#!/bin/bash
#-------------------------------------------------------------------------------------------------------------#
#	Nombre:		rci_start_monitor.sh                                          			 		              #
#	Versión:	1.1.0                                          			 		                              #
#	Objetivo: 	Shell que verifica si el monitor del asset engine esta iniciado, en caso de que no, lo inicia #
#	Autor:		ejesus                                                                                        #
#	Vía de ejecución: Línea de comandos		                                                            	  #
#	Fecha:		08 de Julio de 2020  	                                                           		 	  #
#	Area:		Datalake AT&T											                                      #
#   Versionamiemto: 20200724 Se agrega refresh de tablas de control y financiera para actualizar en Tableau   #
#   Versionamiemto: 20200807 Se agrega validación adicional para no enviar a ejecutar fuentes complementarias #
#-------------------------------------------------------------------------------------------------------------#

if [ $# -lt 2 ]
	then
		echo '--------------------------------------------------------------'
		echo "Error: parametros"
		echo "usage: sh $(basename $0) environment [command]"
		echo "environment    Ambiente de ejecucion del monitor"
		echo "type_monitor   Numero del 1 al 4, para elegir que tipo de proceso ejecutar."
		echo "               1) Procees Clean"
		echo "               2) Asset Engine"
		echo "               4) Semantic Finance"
		echo "command        Opcional: Comando para detener el monitor del Asset Engine, debe ser la palabra kill"
		echo '--------------------------------------------------------------'
	exit 1;
fi

#----------------------------------------------------------------------------------#
#						Leer parámetros para la ejecucion	   					   #
#----------------------------------------------------------------------------------#
export environment=$(echo $1 | awk '{print tolower($0)}')
export type_monitor=$2
export command=$3
echo "environment:$environment"
echo "type_monitor:$type_monitor"
echo "command:$command"
echo ""
echo ""

bn=$(basename $0)
bn=rci_start_monitor.sh
bn_p=$(echo $bn | awk '{print index($0, ".")}')
let di=$(expr $bn_p - 11)
let bn_p=$(expr $bn_p - 1)
name_file_log=$(echo $bn | awk -v i=$bn_p '{print substr($0,0,i)}')
echo "name_file_log:$name_file_log"

name_flow=$(echo $bn | awk -v d=$di '{print substr($0,11,d)}')
echo "name_flow:$name_flow"

#----------------------------------------------------------------------------------#
#				Definimos variables necesarias para la ejecucion	   		       #
#----------------------------------------------------------------------------------#
export dev_destination=""
export prd_destination=""
export prd_prefix=""
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
export path_pyspark_hdfs="hdfs://attdatalakehdfs/user/raw_rci/Pyspark/"
export path_temp_flags=$path_root"tmp/"
export flow_pending=0
export query_exists=""

case $type_monitor in
1)
	type_monitor_label="Process_Clean"
	;;
2)
	type_monitor_label="Asset_Engine"
	;;
3)
	type_monitor_label="Semantic_Engine"
	;;
4)
	type_monitor_label="Semantic_Finance"
	;;
esac

#----------------------------------------------------------------------------------#
#				Agregamos las lineas para poder usar las librerias	   		       #
#----------------------------------------------------------------------------------#
#Agregamos las lineas para poder utilizar el log
. $path_lib/"$environment"_log4j_attdlkrci.sh 6 "$name_flow"_"$type_monitor_label" "$environment" "$path_home" "$group_exec" "$type_monitor_label"
create_dir_logs

print_log "El log para darle seguimiento a la ejecución es:"
print_log "$log_file_base"
print_log ""
print_log ""
print_log "environment:$environment"
print_log "type_monitor:$type_monitor"
print_log "command:$command"
print_log ""
print_log ""

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
export time_wait_process_clean=1 #3 #Tiempo de espera en minutos del process clean
export time_wait_asset_engine=1 #5 #Tiempo de espera en minutos del asset engine
export time_wait_semantic_engine=1 #5 #Tiempo de espera en minutos del semantic engine
export time_wait_semantic_finance=1 #5 #Tiempo de espera en minutos del semantic engine

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#								Area de funciones comunes						   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#

trap ctrl_c INT

function ctrl_c() {
	echo "** Trapped CTRL-C"
}

#---------------------------------------------------------------#
#			Funcion para inicializar las propiedades    		#
#---------------------------------------------------------------#
start_monitor(){
	getDate
	#leemos el archivo de propiedades
	read_properties "$file_properties"

	size_properties=${#properties[@]}
	print_log "properties longitud: $size_properties"
	if [ 0 -eq $size_properties ]; then
		print_log "Revisar la lectura del archivo de propiedades."
		
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 4: exit 1                              #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 1;
	fi

	print_log "*****************************************************"
	#7.2.1 Asignación de variables globales 
	set_environment_variables
	print_log "*****************************************************"
	
	check_type_monitor
}

#---------------------------------------------------------------#
#			Funcion que valida el tipo de monitor elegido 		#
#---------------------------------------------------------------#
check_type_monitor(){
	case $type_monitor in
	1)
		export type_monitor_label="Process_Clean"
		get_query_execute $type_monitor $status_pending_clean
		check_pending $type_monitor $status_pending_clean
		;;
	2)
		#Validar si hay alguna ejecución de la vista de control que haya fallado, para procesarla antes de continuar con las ejecuciones del Asset engine
		export type_monitor_label="Semantic_Engine"
		export a_id_table=3000
		get_query_execute 3 $status_error_control_view
		check_pending 3 $status_error_control_view
		export flow_pending=0
		
		export type_monitor_label="Asset_Engine"
		get_query_execute $type_monitor $status_pending_ae
		check_pending $type_monitor $status_pending_ae
		;;
	3)
		export type_monitor_label="Semantic_Engine"
		get_query_execute $type_monitor $status_pending_control_view
		check_pending $type_monitor $status_pending_control_view
		;;
	4)
		export type_monitor_label="Semantic_Finance"
		get_query_execute $type_monitor $status_pending_finance
		check_pending $type_monitor $status_pending_finance
		;;
	esac
}

#---------------------------------------------------------------#
#			Funcion que define la consulta a ejecutar 			#
#			dependiendo del tipo de monitor elegido 			#
#---------------------------------------------------------------#
get_query_execute(){
	print_log "parametros en get_query_execute"
	print_log "1=$1"
	print_log "2=$2"

	if [ "dev" == "$environment" ]; then
		sufix=$dev_destination
	else
		sufix=$prd_destination
	fi

	#Query para validar si hay registros pendientes de procesar por el Process Clean, se toman todos los registros que no existan en la tabla cr_rci_ae_processed_sources + sufix y que esten en la tabla cr_rci_executions_id_references con estatus PENDING_CLEANING
	export query_count_pending_pc_ae="select count(*) as total from (select sp.ctl_tid, sp.last_ctl_eid from $schema.$table_source_processed$sufix sp where sp.stage = 'asset engine process' and sp.state = 'END' group by sp.ctl_tid, sp.last_ctl_eid) sp right join (select  rf.ctl_tid,rf.ctl_eid,rf.ctl_eid_origin from $schema_config.$table_execution_references rf where rf.status='{0}' group by rf.ctl_tid,rf.ctl_eid,rf.ctl_eid_origin ) missing on sp.ctl_tid = missing.ctl_tid and sp.last_ctl_eid = missing.ctl_eid left join $schema_config.$table_names t on missing.ctl_tid=t.ctl_tid left join $schema_config.$table_config tc on t.ctl_tid = tc.ctl_tid left join $schema_config.$table_source s on t.ctl_sid = s.ctl_sid where lower(tc.environment_config)='{1}' and t.type_source <> 'COMPLEMENTARY' and sp.last_ctl_eid is null"
	
	#Query para obtener el número de registros pendientes de procesar por el Process Clean, se cuentan todos los registros que esten en la tabla cr_rci_executions_id_references con estatus PENDING_CLEANING, este query se ejecuta solo cuando la tabla cr_rci_ae_processed_sources + sufix no existe
	export query_count_pending_pc_ae_not_exists="select count(*) as total from $schema_config.$table_execution_references missing left join $schema_config.$table_names t on missing.ctl_tid=t.ctl_tid left join $schema_config.$table_config tc on t.ctl_tid = tc.ctl_tid left join $schema_config.$table_source s on t.ctl_sid = s.ctl_sid where missing.status='{0}' and lower(tc.environment_config)='{1}' and t.type_source <> 'COMPLEMENTARY' "
	
	#Query para obtener el número de registros pendientes de procesar por el Semantic Engine
	export query_count_pending_se="select count(*) as total from $schema_config.$table_execution_references where status = '{0}'"
	
	#Query para obtener el número de registros pendientes de procesar por el Semantic Finance
	export query_count_pending_sf="with cip as (select count(*) as total, ctl_tid from $schema_config.$table_execution_references where status = '{0}' and ctl_tid = 1 group by ctl_tid),fixed as (select count(*) as total, ctl_tid from $schema_config.$table_execution_references where status = '{0}' and ctl_tid = 7 group by ctl_tid) select count(*) as total from cip, fixed"

	#Query para obtener los registros pendientes de procesar por el Process Clean, se toman todos los registros que no existan en la tabla cr_rci_ae_processed_sources + sufix y que esten en la tabla cr_rci_executions_id_references con estatus PENDING_CLEANING
	export query_get_pending_pc_ae="select concat(lower(tc.environment_config),'_') as environment_config,tc.schema_database,t.table_name,missing.ctl_eid,missing.ctl_eid_origin,s.ctl_sid,missing.ctl_tid from (select sp.ctl_tid, sp.last_ctl_eid from $schema.$table_source_processed$sufix sp where sp.stage = 'asset engine process' and sp.state = 'END' group by sp.ctl_tid, sp.last_ctl_eid) sp right join (select  rf.ctl_tid,rf.ctl_eid,rf.ctl_eid_origin from $schema_config.$table_execution_references rf where rf.status='{0}' group by rf.ctl_tid,rf.ctl_eid,rf.ctl_eid_origin ) missing on sp.ctl_tid = missing.ctl_tid and sp.last_ctl_eid = missing.ctl_eid left join $schema_config.$table_names t on missing.ctl_tid=t.ctl_tid left join $schema_config.$table_config tc on t.ctl_tid = tc.ctl_tid left join $schema_config.$table_source s on t.ctl_sid = s.ctl_sid where lower(tc.environment_config)='{1}' and t.type_source <> 'COMPLEMENTARY' and sp.last_ctl_eid is null order by missing.ctl_eid_origin desc"
	
	#Query que obtiene los registros pendientes de procesar por el Process Clean, solo de la tabla cr_rci_executions_id_references, este query se ejecutará solo en caso de que la tabla cr_rci_ae_processed_sources + sufix no exista (que solo debe ser en la primera ejecución dado que el Asset engine no ha creado esta tabla) por eso solo se hace el limit 1
	export query_get_pending_pc_ae_not_exists="select concat(lower(tc.environment_config),'_') as environment_config,tc.schema_database,t.table_name,missing.ctl_eid,missing.ctl_eid_origin,s.ctl_sid,missing.ctl_tid from $schema_config.$table_execution_references missing left join $schema_config.$table_names t on missing.ctl_tid=t.ctl_tid left join $schema_config.$table_config tc on t.ctl_tid = tc.ctl_tid left join $schema_config.$table_source s on t.ctl_sid = s.ctl_sid where missing.status='{0}' and lower(tc.environment_config)='{1}' and t.type_source <> 'COMPLEMENTARY' order by missing.ctl_eid_origin desc limit 1"
	
	#Query para obtener los registros pendientes de procesar por el Semantic Engine
	export query_get_pending_se="select '{1}' as environment_config,'$schema' as schema_database,'table_name' as table_name,ctl_eid,ctl_eid_origin,0 as ctl_sid,ctl_tid from $schema_config.$table_execution_references where status = '{0}'"
	
	#Query para obtener los registros pendientes de procesar por el Semantic Finance
	export query_get_pending_sf="select '{1}' as environment_config,'$schema' as schema_database,'table_name' as table_name,ctl_eid,ctl_eid_origin,0 as ctl_sid,ctl_tid from $schema_config.$table_execution_references where status = '{0}' and ctl_tid in (1,7)"

	case $1 in
	1 | 2 )
		#Actualizamos metadata para verificar si la tabla ya está creada
		query_invalidate_sp="invalidate metadata $schema.$table_source_processed$sufix "
		execute_querys_without_exit "$query_invalidate_sp" "inv_sp" 92 "$intentos" "$schema" ""
	
		#Validamos si existe la tabla cr_rci_ae_processed_sources + sufix
		query_validate_exists_table="show tables in $schema like '$table_source_processed$sufix'"
		execute_querys "$query_validate_exists_table" "query_exists" 91 "$intentos" ""
		query_exists=${response_f[query_exists]}
		
		if [ "" == "$query_exists" ]; then
			print_log "La tabla $schema.$table_source_processed$sufix no existe, no se validará si el ctl_eid ya se ha procesado."
			query_count_execute_monitor=$(echo "${query_count_pending_pc_ae_not_exists//'{0}'/$2}")
			query_count_execute_monitor=$(echo "${query_count_execute_monitor//'{1}'/$environment}")
			query_get_execute_monitor=$(echo "${query_get_pending_pc_ae_not_exists//'{0}'/$2}")
			query_get_execute_monitor=$(echo "${query_get_execute_monitor//'{1}'/$environment}")
		else
			export table_exists_res=$(echo ${query_exists} | cut -d" " -f1)
			export table_exists_res="$(echo -e "${table_exists_res}" | tr -d '[:space:]')"
			print_log " table_exists_res               $table_exists_res"

			query_count_execute_monitor=$(echo "${query_count_pending_pc_ae//'{0}'/$2}")
			query_count_execute_monitor=$(echo "${query_count_execute_monitor//'{1}'/$environment}")
			query_get_execute_monitor=$(echo "${query_get_pending_pc_ae//'{0}'/$2}")
			query_get_execute_monitor=$(echo "${query_get_execute_monitor//'{1}'/$environment}")
		fi
		;;
	3)
		query_count_execute_monitor=$(echo "${query_count_pending_se//'{0}'/$2}")
		query_get_execute_monitor=$(echo "${query_get_pending_se//'{0}'/$2}")
		query_get_execute_monitor=$(echo "${query_get_execute_monitor//'{1}'/$environment}")
		;;
	4)
		query_count_execute_monitor=$(echo "${query_count_pending_sf//'{0}'/$2}")
		query_get_execute_monitor=$(echo "${query_get_pending_sf//'{0}'/$2}")
		query_get_execute_monitor=$(echo "${query_get_execute_monitor//'{1}'/$environment}")
		;;
	esac
}

#---------------------------------------------------------------#
#			Funcion para validar los totales de registros 		#
#---------------------------------------------------------------#
check_pending(){
	#Validamos si hay señal para detener el monitor
	check_for_stop

	execute_querys "$query_count_execute_monitor" "get_c_p" 90 "$intentos" "$schema_config" ""
	export res_count_pending=${response_f[get_c_p]}
	
	case $1 in
	1 | 2 )
		if [ 0 -eq $res_count_pending ]; then
			export execute_request=0
		else
			export execute_request=1
		fi
		;;
	3 )
		if [ 0 -eq $res_count_pending ]; then
			export execute_request=0
		else
			export execute_request=1
			export flow_pending=1
		fi
		;;
	4 )
		if [ 1 -eq $res_count_pending ]; then
			export execute_request=1
		else
			export execute_request=0
		fi
		;;
	esac
	
	if [ 0 -eq $execute_request ]; then
		if [ 3 -ne $1 ]; then
			wait_for_job $1
			
			if [ "" = "$query_exists" ]; then
				get_query_execute $1 $2
			fi
			
			check_pending $1 $2
		fi
	else
		execute_querys "$query_get_execute_monitor" "query_file" 91 "$intentos" "$schema_config" "${type_monitor_label}_pending_${date_load}.txt"
		
		export val_count=$(cat "${path_temp}${type_monitor_label}_pending_${date_load}.txt" | wc -l)
		print_log "val_count                  $val_count"
		print_log "res_count_pending          $res_count_pending"
		print_log ""
		print_log ""
		
		if [ 0 -eq $val_count ]; then
			print_log "No se encontraron registros para procesar."
			print_log "Existian registros pendientes de procesar, no se pudieron recuperar, verificar estatus en BD"
			print_log "#----------------------------------------------------------------------------------#"
			print_log "#              Punto de control 1: Volver a buscar registros pendientes.           #"
			print_log "#----------------------------------------------------------------------------------#"
			wait_for_job $1
			check_pending $1 $2
		else
			send_request $1
			
			if [ 0 -eq $flow_pending ]; then			
				if [ "" = "$query_exists" ]; then
					get_query_execute $1 $2
				fi
			
				check_pending $1 $2
			fi
		fi
	fi
}

#---------------------------------------------------------------#
# Funcion para validar si hay una señal para detener el monitor #
#---------------------------------------------------------------#
check_for_stop(){
	#Obtenemos el estatus actual del monitor
	get_status_flag
	
	#Validamos si hay señal de kill, para detener el monitor
	if [ "kill" = "$state" ]; then
		#Ponemos el estatus del monitor en stop
		put_flag_stop
		
		print_log ""
		print_log ""
		print_log "*******************************************************************"
		print_log "Se recibío solicitud ${state} para detener el monitor ${type_monitor_label}"
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 7: exit 0                              #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 0;
	fi
}

#---------------------------------------------------------------#
#   Funcion pone en standby el monitor que se esta ejecutando   #
#---------------------------------------------------------------#
wait_for_job(){
	print_log "No se encontraron registros para procesar por el monitor ${type_monitor_label}."

	case $type_monitor in
	1)
		print_log "Esperar ${time_wait_process_clean} minutos para volver a buscar registros para procesar"
		sleep ${time_wait_process_clean}m
		;;
	2)
		print_log "Esperar ${time_wait_asset_engine} minutos para volver a buscar registros para procesar"
		sleep ${time_wait_asset_engine}m
		;;
	3)
		print_log "Esperar ${time_wait_semantic_engine} minutos para volver a buscar registros para procesar"
		sleep ${time_wait_semantic_engine}m
		;;
	4)
		print_log "Esperar ${time_wait_semantic_finance} minutos para volver a buscar registros para procesar"
		sleep ${time_wait_semantic_finance}m
		;;
	esac
}

#---------------------------------------------------------------#
#    Funcion para enviar a ejecución los diferentes procesos    #
#---------------------------------------------------------------#
send_request(){
	case $1 in
		1 | 2)
			for i in $( eval echo {1..$val_count} )
			do
				#Validamos si hay señal para detener el monitor
				check_for_stop
				
				current_pending=$(tail -n $i "${path_temp}${type_monitor_label}_pending_${date_load}.txt")
				req_env=$(echo ${current_pending} | cut -d" " -f1)
				req_sch=$(echo ${current_pending} | cut -d" " -f2)
				req_tbl=$(echo ${current_pending} | cut -d" " -f3)
				req_eid=$(echo ${current_pending} | cut -d" " -f4)
				req_ori=$(echo ${current_pending} | cut -d" " -f5)
				req_sid=$(echo ${current_pending} | cut -d" " -f6)
				req_tid=$(echo ${current_pending} | cut -d" " -f7)
				
				req_env="$(echo -e "${req_env}" | tr -d '[:space:]')"
				req_sch="$(echo -e "${req_sch}" | tr -d '[:space:]')"
				req_tbl="$(echo -e "${req_tbl}" | tr -d '[:space:]')"
				req_eid="$(echo -e "${req_eid}" | tr -d '[:space:]')"
				req_ori="$(echo -e "${req_ori}" | tr -d '[:space:]')"
				req_sid="$(echo -e "${req_sid}" | tr -d '[:space:]')"
				req_tid="$(echo -e "${req_tid}" | tr -d '[:space:]')"
				
				if [ "dev" == "$environment" ]; then
					req_des=$dev_destination
					req_tbl=$req_env$req_tbl
				else
					req_env=$prd_prefix
					req_des=$prd_destination
				fi
				
				check_counts $req_tid $req_eid $req_ori
				
				if [ 0 -eq $put_finish ]; then
					print_log "#----------------------------------------------------------------------------------#"
					print_log "#                    Se genera Request ${i} con los siguientes datos                 #"
					print_log "#----------------------------------------------------------------------------------#"
					print_log "ambiente              $req_env"
					print_log "destino               $req_des"
					print_log "esquema               $req_sch"
					print_log "nombre tabla          $req_tbl"
					print_log "ctl_eid               $req_eid"
					print_log "usuario               $user"
					print_log "table_id              $req_tid"
					
					id_sources_origin="7 18 19 20 21"
					exists_origin=0
					for req_val in $id_sources_origin
					do
						if [ $req_sid -eq $req_val ]; then
							print_log "Fuente con ctl_eid_origin $req_sid"
							let exists_origin=$(expr $exists_origin + 1 )
						fi
					done
					print_log ""
					print_log "Numero de fuentes con ctl_eid_origin $exists_origin"
					
					if [ 0 -lt $exists_origin ]; then
						req_eid_send=$req_ori
					else
						req_eid_send=$req_eid
					fi

					invoke_monitor $1
					
					#Validamos si hubo una petición del Asset Engine, entonces se debe hacer una al Semantic Engine
					if [ 2 -eq $1 ]; then
						print_log ""
						print_log ""
						print_log "Respuesta de request a ${type_monitor_label} $req_tid - $req_tbl es ${res_gen}"
						if [ 0 -eq $res_gen ]; then
							export type_monitor_label="Semantic_Engine"
							invoke_monitor 3
							export type_monitor_label="Asset_Engine"
						fi
					fi
				fi
			done
			;;
		3 )
			for i in $( eval echo {1..$val_count} )
			do
				#Validamos si hay señal para detener el monitor
				check_for_stop
				
				current_pending=$(tail -n $i "${path_temp}${type_monitor_label}_pending_${date_load}.txt")
				req_env=$(echo ${current_pending} | cut -d" " -f1)
				req_sch=$(echo ${current_pending} | cut -d" " -f2)
				req_tbl=$(echo ${current_pending} | cut -d" " -f3)
				req_eid=$(echo ${current_pending} | cut -d" " -f4)
				req_ori=$(echo ${current_pending} | cut -d" " -f5)
				req_sid=$(echo ${current_pending} | cut -d" " -f6)
				req_tid=$(echo ${current_pending} | cut -d" " -f7)
				
				req_env="$(echo -e "${req_env}" | tr -d '[:space:]')"
				req_sch="$(echo -e "${req_sch}" | tr -d '[:space:]')"
				req_tbl="$(echo -e "${req_tbl}" | tr -d '[:space:]')"
				req_eid="$(echo -e "${req_eid}" | tr -d '[:space:]')"
				req_ori="$(echo -e "${req_ori}" | tr -d '[:space:]')"
				req_sid="$(echo -e "${req_sid}" | tr -d '[:space:]')"
				req_tid="$(echo -e "${req_tid}" | tr -d '[:space:]')"
				
				if [ "dev" == "$environment" ]; then
					req_des=$dev_destination
					req_tbl=$req_env$req_tbl
					tbl_control=$req_env$table_control$req_des
				else
					req_env=$prd_prefix
					req_des=$prd_destination
					tbl_control=$table_control$req_des
				fi
				
				query_upd_status_pending="update $schema_config.$table_execution_references set status='$status_pending_control_view', updated_by='$user', updated_on=now() where (ctl_eid='$req_eid' or ctl_eid_origin='$req_ori') and ctl_tid=$req_tid"
				execute_querys "$query_upd_status_pending" "upd_pending" 2 "$intentos" "$req_sch" ""
				
				print_log "#----------------------------------------------------------------------------------#"
				print_log "#                    Se genera Request ${i} con los siguientes datos                 #"
				print_log "#----------------------------------------------------------------------------------#"
				print_log "ambiente              $req_env"
				print_log "destino               $req_des"
				print_log "esquema               $req_sch"
				print_log "nombre tabla          $req_tbl"
				print_log "ctl_eid               $req_eid"
				print_log "usuario               $user"
				print_log "table_id              $req_tid"

				invoke_monitor $1
				
				if [ 0 -eq $res_gen ]; then
					refresh_table "$schema" "$tbl_control"
				fi
			done
			;;
		4)
			export ctl_eid_update=""
			export ctl_eid_ori_update=""
			export ctl_tid_update=""
			export wildcard="'"
			
			for i in $( eval echo {1..$val_count} )
			do
				#Validamos si hay señal para detener el monitor
				check_for_stop
				
				current_pending=$(tail -n $i "${path_temp}${type_monitor_label}_pending_${date_load}.txt")
				req_env=$(echo ${current_pending} | cut -d" " -f1)
				req_sch=$(echo ${current_pending} | cut -d" " -f2)
				req_tbl=$(echo ${current_pending} | cut -d" " -f3)
				req_eid=$(echo ${current_pending} | cut -d" " -f4)
				req_ori=$(echo ${current_pending} | cut -d" " -f5)
				req_sid=$(echo ${current_pending} | cut -d" " -f6)
				req_tid=$(echo ${current_pending} | cut -d" " -f7)
				
				req_env="$(echo -e "${req_env}" | tr -d '[:space:]')"
				req_sch="$(echo -e "${req_sch}" | tr -d '[:space:]')"
				req_tbl="$(echo -e "${req_tbl}" | tr -d '[:space:]')"
				req_eid="$(echo -e "${req_eid}" | tr -d '[:space:]')"
				req_ori="$(echo -e "${req_ori}" | tr -d '[:space:]')"
				req_sid="$(echo -e "${req_sid}" | tr -d '[:space:]')"
				req_tid="$(echo -e "${req_tid}" | tr -d '[:space:]')"
				
				req_eid=$wildcard$req_eid$wildcard
				req_ori=$wildcard$req_ori$wildcard
				
				export ctl_eid_update=$ctl_eid_update$req_eid","
				export ctl_eid_ori_update=$ctl_eid_ori_update$req_ori","
				export ctl_tid_update=$ctl_tid_update$req_tid","
			done
			
			if [ "dev" == "$environment" ]; then
				req_des=$dev_destination
				tbl_control=$req_env$table_control$req_des
			else
				req_des=$prd_destination
				tbl_control=$table_control$req_des
			fi
					
			ctl_eid_update=$(echo $ctl_eid_update | awk '{print substr($0,0,length($0)-1)}')
			ctl_eid_ori_update=$(echo $ctl_eid_update | awk '{print substr($0,0,length($0)-1)}')
			ctl_tid_update=$(echo $ctl_tid_update | awk '{print substr($0,0,length($0)-1)}')

			req_eid=$ctl_eid_update
			req_ori=$ctl_eid_ori_update
			req_tid=$ctl_tid_update
			
			print_log ""
			print_log ""
			print_log "ctl_eid para actualizar               ${req_eid}"
			print_log "ctl_eid_origin para actualizar        ${req_ori}"
			print_log "ctl_tid para actualizar               ${req_tid}"
			
			invoke_monitor $1
			
			if [ 0 -eq $res_gen ]; then
				refresh_table "$schema" "$tbl_control"
			fi
			;;
	esac
			
	print_log "Fin de la invocacion de $val_count registros pendientes"	
}

#---------------------------------------------------------------#
#    Funcion para invocar el shell que realiza el spark submit  #
#---------------------------------------------------------------#
invoke_monitor(){
	name_shell_sr="${environment}_rci_send_request.sh";
	print_log "Invocando proceso: $path_lib$name_shell_sr"
	print_log "parámetro: $1"
	
	. $path_lib$name_shell_sr $1
	res_sr=$?
	print_log "Respuesta de shell $path_lib$name_shell_sr: $res_sr"
}

#---------------------------------------------------------------#
#    Funcion para poner el flag del monitor en status running   #
#---------------------------------------------------------------#
put_flag_execution(){
	print_log "Generar flag por inicio de ejecución del monitor ${environment}_${type_monitor_label}"
	touch ${path_temp_flags}${environment}_${type_monitor_label}_flag
	echo "running" > ${path_temp_flags}${environment}_${type_monitor_label}_flag
}

#---------------------------------------------------------------#
#    Funcion para poner el flag del monitor en status stop      #
#---------------------------------------------------------------#
put_flag_stop(){
	print_log "Generar flag por detencion de ejecución del monitor ${environment}_${type_monitor_label}"
	touch ${path_temp_flags}${environment}_${type_monitor_label}_flag
	echo "stop" > ${path_temp_flags}${environment}_${type_monitor_label}_flag
}

#---------------------------------------------------------------#
#Funcion para poner en el flag del monitor la señal para detenerlo#
#---------------------------------------------------------------#
put_flag_kill(){
	print_log "Generar flag por señal para detener la ejecución del monitor ${environment}_${type_monitor_label}"
	touch ${path_temp_flags}${environment}_${type_monitor_label}_flag
	echo "kill" > ${path_temp_flags}${environment}_${type_monitor_label}_flag
}

#---------------------------------------------------------------#
#      Funcion para obtener el status del flag del monitor      #
#---------------------------------------------------------------#
get_status_flag(){
	print_log "Obtener flag para revisar status de la ejecución del monitor ${environment}_${type_monitor_label}"
	export state=$(cat ${path_temp_flags}${environment}_${type_monitor_label}_flag)
	print_log "state        ${state}"
}

refresh_table(){
	print_log "refresh de la tabla:$1.$2"
	refresh_query="refresh $1.$2"
	execute_querys_without_exit "$refresh_query" "refresh_tbl" 96 "$intentos" "$1" ""
}
	
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#								Funcion principal del shell						   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#

check_monitor(){
	print_log "#----------------------------------------------------------------------------------#"
	print_log "#                    Validación del monitor ${type_monitor_label}                  #"
	print_log "#                                      Inicio                                      #"
	print_log "#----------------------------------------------------------------------------------#"

	#Verificamos si se envío señal de kill al monitor
	if [ "kill" = "$command" ]; then
		put_flag_kill
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 5: exit 0                              #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 0;
	fi
	
	#Obtenemos el estatus actual del monitor
	get_status_flag
	#Validamos si hay una instancia del monitor ejecutando
	if [ "running" = "$state" ]; then
		print_log ""
		print_log ""
		print_log "*******************************************************************"
		print_log "Existe una instancia del monitor ${type_monitor_label} en ejecución"
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 6: exit 0                              #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 0;
	else
		#Si no hay alguna instancia ejecutando, poner el flag en run e iniciamos el monitor
		put_flag_execution
		start_monitor
	fi
}

check_monitor
