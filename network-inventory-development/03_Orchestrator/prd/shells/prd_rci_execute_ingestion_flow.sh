#set -xv
#!/bin/bash
#------------------------------------------------------------------------------------------------------------#
#	Nombre:		prd_rci_execute_ingestion_flow.sh                                          			 		 #
#	Versión:	1.0.1                                          			 		                             #
#	Objetivo: 	Shell encargado de revisar que fuentes deben ser ingestadas y lanzar el proceso de ingesta	 #
#	Autor:		ejesus                                                                                       #
#	Vía de ejecución: Línea de comandos		                                                            	 #
#	Fecha:		28 de Enero de 2019  	                                                           		 	 #
#	Area:		Datalake AT&T											                                     #
#   Versionamiento:  20200724 Ajuste en la validación para obtener el numero de archivos de UMNSNEC          #
#------------------------------------------------------------------------------------------------------------#

if [ $# -lt 1 ]
	then
		echo '--------------------------------------------------------------'
		echo "Error: parametros"
		echo "usage: sh $(basename $0) ctl_tid [reset]"
		echo "ctl_tid		Es el id númerico de la tabla definida en la tabla de configuración (rci_db_metadata.cfg_rci_table)."
		echo "reset			Opcional: Valor para indicar que el flujo se debe reiniciar y ejecutar desde el inicio."
		echo '--------------------------------------------------------------'
	exit 1;
fi

#----------------------------------------------------------------------------------#
#				    Validar parámetros para la ejecucion	   					   #
#----------------------------------------------------------------------------------#
if [ "$(echo $1 | grep '^[0-9]\+$')" = "" ]; then
	echo "El parámetro 1 debe ser numérico..."
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

export environment="prd"
export group_exec="inventario"
export current_flow="phase_all"

export path_home=/home/raw_rci/attdlkrci/$environment/
export path_shells=$path_home"shells/"
export path_lib=$path_shells"lib/"
export path_config=$path_home"config/"
export path_temp=$path_home"tmp/"
export path_sql=$path_home"sql/"
export path_logs=$path_home"logs/"
export path_status=$path_home"status/"
cd $path_home

#----------------------------------------------------------------------------------#
#				Agregamos las lineas para poder usar las librerias	   		       #
#----------------------------------------------------------------------------------#

#Agregamos las lineas para poder utilizar la librería de logs
. $path_lib/"$environment"_log4j_attdlkrci.sh 1 "$environment"_rci_execute_ingestion_flow "$environment" "$path_home" "$group_exec" "$a_id_table"
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
export execute_all_phases_ref=1
export current_id_event=0
export phase_initialization=0
export init_validation_source=0
export telnet_valid=0
export init_validation_server=0
export init_validation_paths=1
export generate_eid=1
export send_alert_not_execute=0
export send_alert_execute=0
export next=0
export is_referenced=0
export was_referenced=0

export phase_pre_processing=0
export phase_processing=0
export phase_post_processing=0

# Variables para poder reintentar ejecutar una consulta en caso de desconexión
export intentos=1
export max_intentos=3
declare -A response_f
export time_wait_invoke=1 #Variable para indicar el tiempo de espera entre invocación de flujos

#Variables para controlar los intentos de lectura
export indice=1
export local_attempts=1
declare -A times_values
export avro_attempts=1

#TO-DO Variable para simular el proceso y hacer pruebas cuando falla el cluster
#TO-DO ejesus poner variable en 1 para ejecutar sin cluster
export run_without_cluster=0

#Definimos arreglos para guardar las N rutas en las que debemos validar la generación de archivos
declare -A paths_avro
declare -A paths_cifras
declare -A paths_not_processed
declare -A table_ids
declare -A ids_referenced
declare -A events_pending

print_log "Parámetro 1 recibid0 a_id_table:$a_id_table"
print_log "Parámetro 2 recibid0 reset:$reset"
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#								Area de funciones comunes						   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#			  Area de funciones de la fase de inicialización					   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
# Funcion para obtener la configuracion de ejecucion de las fuentes
get_config_validation_source(){
	query_get_config="select o.src_server,'|',o.path_in,'|',o.recursive_read,'|',o.name_expression_file,'|',o.attempts_read,'|',o.time_wait,'|',o.responsible_of_source,'|',o.email_responsible,'|',o.use_nifi,'|',o.referenced_tables,'|',o.periodicity,'|',s.source_name,'|',s.tech_source,'|',t.table_name,'|',s.ctl_sid,'|',c.schema_database from $schema_config.$table_orchestration o inner join $schema_config.$table_config c on o.ctl_tid = c.ctl_tid and o.environment_config = c.environment_config inner join $schema_config.$table_names t on c.ctl_tid = t.ctl_tid inner join $schema_config.$table_source s on t.ctl_sid = s.ctl_sid where o.ctl_tid=$a_id_table and t.table_status='$status_active' and lower(o.environment_config) = '$environment' "
	execute_querys "$query_get_config" "vc" 1 "$intentos" "$schema_config" ""
	values_config=${response_f[vc]}
	
	if [ "" == "$values_config" ]; then
		print_log "No se encontró configuración asociada al ctl_tid=$a_id_table y ambiente=$environment en la tabla $schema_config.$table_orchestration, validar con Query_1."
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 1: exit 1                              #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 1;
	fi
	
	export server=$(echo ${values_config} | cut -d"|" -f1)
	export path_in=$(echo ${values_config} | cut -d"|" -f2)
	export recursive_read=$(echo ${values_config} | cut -d"|" -f3)
	export name_expression_file=$(echo ${values_config} | cut -d"|" -f4)
	export attempts_read=$(echo ${values_config} | cut -d"|" -f5)
	export time_wait=$(echo ${values_config} | cut -d"|" -f6)
	export responsible_of_source=$(echo ${values_config} | cut -d"|" -f7)
	export email_responsible=$(echo ${values_config} | cut -d"|" -f8)
	export use_nifi=$(echo ${values_config} | cut -d"|" -f9)
	export referenced_tables=$(echo ${values_config} | cut -d"|" -f10)
	export periodicity_bd=$(echo ${values_config} | cut -d"|" -f11)
	export name_source=$(echo ${values_config} | cut -d"|" -f12)
	export type_source=$(echo ${values_config} | cut -d"|" -f13)
	export table_name=$(echo ${values_config} | cut -d"|" -f14)
	export ctl_sid=$(echo ${values_config} | cut -d"|" -f15)
	export schema_load=$(echo ${values_config} | cut -d"|" -f16)

	export server="$(echo -e "${server}" | tr -d '[:space:]')"
	if [[ "$name_source" != *"NETCM"* ]]; then
		export path_in="$(echo -e "${path_in}" | tr -d '[:space:]')"
	fi
	export recursive_read="$(echo -e "${recursive_read}" | tr -d '[:space:]')"
	export name_expression_file="$(echo -e "${name_expression_file}" | sed 's/^[[:space:]]*//')"
	export name_expression_file="$(echo -e "${name_expression_file}" | sed 's/[[:space:]]*$//')"
	export attempts_read="$(echo -e "${attempts_read}" | tr -d '[:space:]')"
	export time_wait="$(echo -e "${time_wait}" | tr -d '[:space:]')"
	export email_responsible="$(echo -e "${email_responsible}" | tr -d '[:space:]')"
	export use_nifi="$(echo -e "${use_nifi}" | tr -d '[:space:]')"
	export referenced_tables="$(echo -e "${referenced_tables}" | tr -d '[:space:]')"
	export periodicity_bd="$(echo -e "${periodicity_bd}" | tr -d '[:space:]')"
	export name_source="$(echo -e "${name_source}" | tr -d '[:space:]')"
	export type_source="$(echo -e "${type_source}" | tr -d '[:space:]')"
	export table_name="$(echo -e "${table_name}" | tr -d '[:space:]')"
	
	if [ "prd" != "$environment" -a "PRD" != "$environment" ]; then
		export table_name="$environment"_$table_name
	fi
	
	export ctl_sid="$(echo -e "${ctl_sid}" | tr -d '[:space:]')"
	export schema_load="$(echo -e "${schema_load}" | tr -d '[:space:]')"
	
	print_log "	server                      $server"
	print_log "	path_in                     $path_in"
	print_log "	recursive_read              $recursive_read"
	print_log "	name_expression_file        $name_expression_file"
	print_log "	attempts_read               $attempts_read"
	print_log "	time_wait                   $time_wait"
	print_log "	email_responsible           $email_responsible"
	print_log "	responsible_of_source       $responsible_of_source"
	print_log "	use_nifi                    $use_nifi"
	print_log "	referenced_tables           $referenced_tables"
	print_log "	periodicity_bd              $periodicity_bd"		
	print_log "	name_source                 $name_source"
	print_log "	type_source                 $type_source"		
	print_log "	table_name                  $table_name"
	print_log "	ctl_sid                     $ctl_sid"
	print_log "	schema_load                 $schema_load"
}

#Funcion para validar exista informacion en la ruta configurada
validate_source(){
	print_log "generate_eid es:$generate_eid"
	
	if [ 1 -eq $generate_eid ]; then
		#IDG:
		validation_start=$(date '+%F %T')
		#generamos el valor de la variable ctl_eid
		generate_field_ctl_eid "$ctl_sid" "$a_id_table"
		insert_events 1 "$status_processing" 33
		
		if [ 1 -eq $is_referenced ]; then
			insert_events_all 1 "$status_processing" 33
		fi
	fi
	
	local_attempts=$1
	print_log ""
	print_log ""
	print_log "Intento $local_attempts de $attempts_read para leer los archivos de la ruta a procesar."
			
	case $type_source in
	#7.2.2.1 Existencia de archivos a procesar
	'file' | 'set')
			f_read="$path_temp"files_read_in_path_"$a_id_table".txt
			f_read_ant="$path_temp"files_read_in_path_"$a_id_table"_ant.txt
			if [ 0 -eq $recursive_read ]; then
				$(ssh $user@$server find $path_in$name_expression_file -maxdepth 1 -type f 1>"$f_read" 2>>$name_file)
				command_ls="ssh $user@$server find $path_in$name_expression_file -maxdepth 1 -type f | wc -l"
				command_prev="ssh $user@$server find $path_in$name_expression_file -maxdepth 1 -type f | wc -l;"
			else
				#Obtenemos la lista de archivos existentes para tener snapshoot de lo leido
				$(ssh $user@$server find $path_in -iname "$name_expression_file" -type f 1>"$f_read_ant" 2>>$name_file)
				#limpiamos la lista, quitando los archivos de ingested
				cat $f_read_ant | grep -v "ingested" > "$f_read"
				command_ls="cat $f_read | wc -l"
				command_prev="ssh $user@$server find $path_in -iname $name_expression_file -type f > $f_read_ant;cat $f_read_ant | grep -v \"ingested\" > $f_read;cat $f_read | wc -l;"
			fi
			
			print_log "Comando sera $command_ls"
			command_i="shopt -s nocaseglob"
			eval $command_i
			if [ "set" == "$type_source" ]; then
				export count_file=$(eval "$command_ls" 2>>$name_file)
				print_log "count_file en set $count_file"
				if [ 0 -lt $count_file ]; then
					export count_file=1
				else
					export count_file=0
				fi
				print_log "count_file quedo en set $count_file"
			else	
				export count_file=$(eval "$command_ls" 2>>$name_file)
			fi
			print_log ""
			print_log ""
			print_log "Archivos en ruta:$count_file"
			export reason_no=" debido a que no existen archivos en la ruta FTP. "
		;;
	#7.2.2.2 Conexión a repositorio de almacenamiento relacional
	'db')
			#export path_in="10.32.218.155 1521"
			check_connection "$path_in"
			if [ 1 -eq $telnet_valid ];then
				export count_file=1
			else
				export count_file=0
			fi
			
			print_log "Archivos en ruta:$count_file"
			export reason_no=" debido a que no fue posible recuperar información de la Base de datos."
			#command_prev="select * from "
			command_prev="telnet $path_in"
		;;
	#7.2.2.1 Existencia de archivos a procesar
	'odk')
			command_ls="hdfs dfs -ls -C $path_in | wc -l"
			command_prev="hdfs dfs -ls -C $path_in | wc -l;"
			print_log "Comando sera $command_ls"
			export count_file=$(eval $command_ls)
			print_log "Archivos en ruta:$count_file"
			export reason_no=" debido a que no existen archivos en la ruta HDFS. "
		;;
	esac
	
	if [ 1 -eq $run_without_cluster ]; then
		export count_file=1
	fi
	
	export count_file_bck=$count_file
	
	#insertar en la bitácora los valores generales
	if [ 1 -eq $generate_eid ]; then
		query_insert_validation="insert into $schema_config.$table_validation (ctl_tid,dateload,ctl_eid,environment_config,start_validation,end_validation,command_shell,result_count,num_attempts,status_validation,status_server,status_paths,id_nifi_exe,created_by,created_on,updated_by,updated_on) values ($a_id_table,$date_load,'$ctl_eid',upper('$environment'),'$validation_start',null,'$command_prev',$count_file,$local_attempts,'$status_validation_processing',null,null,null,'$user',now(),null,null) "
		insert_update_validation "$query_insert_validation" 25
	
		if [ 1 -eq $is_referenced ]; then
			insert_validation_all
		fi
		export generate_eid=0
	fi
	
	if [ 1 -lt $local_attempts ]; then
		query_update_count="update $schema_config.$table_validation set num_attempts=$local_attempts, result_count=$count_file, updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and ctl_eid='$ctl_eid' "
		insert_update_validation "$query_update_count" 34
	fi
	
	if [ $count_file -gt 0 ]; then
		#Termina la validación exitosa, registrar en la bitácora
		export init_validation_source=1
		
		update_events "$status_executed" 1 34
	else
		if [ $local_attempts -eq $attempts_read ]; then
			export local_attempts=0
			print_log ""
			print_log ""
			print_log "Se agotaron los $attempts_read intentos de lectura de la informacion, fuente ctl_sid:$ctl_sid."
			print_log "Hora:($(date))"
			export init_validation_source=0
			export send_alert_not_execute=1
			next=1

			update_validation 1 26
			update_events "$status_no_executed" 1 35
		fi
		
		if [ 0 -eq $next ]; then
			minutes_wait=$time_wait
			print_log "Esperaremos $minutes_wait minutos a que se deposite la informacion  - ($(date)) ..."
			print_log ""
			print_log ""
			sleep ${minutes_wait}m
			
			let local_attempts=$(expr $local_attempts + 1 )	
		
			next=0
			validate_source "$local_attempts"
		fi
	fi
}

#Funcion para obtener el status del cluster de Nifi
get_status_cluster(){
	#Insertamos el registro del evento a procesar
	insert_events 2 "$status_processing" 36
	if [ 1 -eq $is_referenced ]; then
		insert_events_all 2 "$status_processing" 36
	fi
	
	print_log ""
	print_log ""
	print_log "Inicia la validacion de $number_nodes nodos activos."
	export status_cluster="curl -i -X GET -H 'Content-Type: application/json' $nifi_api/controller/cluster;"
	print_log "$status_cluster"

	date_init_processor=$(date '+%Y-%m-%d_%H:%M:%S')
	eval $status_cluster > "$path_temp"status_cluster_"$date_init_processor".txt
	
	count_nodes=$(grep -o -i \"status\" "$path_temp"status_cluster_"$date_init_processor".txt | wc -l)
	let count_nodes=$(expr $count_nodes + 0 )	
	
	print_log "Nodos activos obtenidos:$count_nodes"
	#TO-DO eliminar esta línea se agrego para poder realizar la prueba completa sin ambiente
	if [ 1 -eq $run_without_cluster ]; then
		count_nodes=$number_nodes
	fi

	if [ $number_nodes -eq $count_nodes ]; then
		print_log "¡¡¡Servidor activo!!!"
		update_validation 2 28
		
		#Actualizamos el estatus del evento
		update_events "$status_executed" 2 37
		export init_validation_server=1
	else
		print_log "Solo hay $count_nodes de $number_nodes disponibles."
		update_validation 3 29
		
		#Actualizamos el estatus del evento
		update_events "$status_no_executed" 2 38
		export init_validation_server=0
	fi
}

#Funcion para validar que existan las rutas que se van a utilizar en la carga
validation_paths(){
	#Insertamos el registro del evento a procesar
	insert_events 3 "$status_processing" 39
	if [ 1 -eq $is_referenced ]; then
		insert_events_all 3 "$status_processing" 39
	fi
	
	query_get_paths="select c.path_backup,'|',c.path_avsc_all,'|',c.path_avro_all,'|',c.path_avro_cifras,'|',c.path_avro_not_processed,'|',o.path_in from $schema_config.$table_config c inner join $schema_config.$table_orchestration o on c.ctl_tid = o.ctl_tid and c.environment_config = o.environment_config inner join $schema_config.$table_names t on c.ctl_tid = t.ctl_tid where t.table_status = '$status_active' and c.ctl_tid = $a_id_table and lower(c.environment_config) = '$environment' "
	execute_querys "$query_get_paths" "paths" 2 "$intentos" "$schema_config" ""
	values_paths=${response_f[paths]}
	
	export v_path_backup=$(echo ${values_paths} | cut -d"|" -f1)
	export v_path_avsc_all=$(echo ${values_paths} | cut -d"|" -f2)
	export v_path_avro_all=$(echo ${values_paths} | cut -d"|" -f3)
	export v_path_avro_cifras=$(echo ${values_paths} | cut -d"|" -f4)
	export v_path_avro_not_processed=$(echo ${values_paths} | cut -d"|" -f5)
	export v_path_in=$(echo ${values_paths} | cut -d"|" -f6)

	export v_path_backup="$(echo -e "${v_path_backup}" | tr -d '[:space:]')"
	export v_path_avsc_all="$(echo -e "${v_path_avsc_all}" | tr -d '[:space:]')"
	export v_path_avro_all="$(echo -e "${v_path_avro_all}" | tr -d '[:space:]')"
	export v_path_avro_cifras="$(echo -e "${v_path_avro_cifras}" | tr -d '[:space:]')"
	export v_path_avro_not_processed="$(echo -e "${v_path_avro_not_processed}" | tr -d '[:space:]')"
	
	if [[ "$name_source" != *"NETCM"* ]]; then
		export v_path_in="$(echo -e "${v_path_in}" | tr -d '[:space:]')"
	fi

	export paths_msg_not_exists="Las siguientes rutas no existen: "
	export paths_not_exists=""
	export paths_name_not_exists=""
	
	print_log ""
	print_log ""
	print_log "Validar rutas de la tabla principal."
	
	#Validar rutas del file system
	check_path_file_system $v_path_backup "path_backup" 0
	check_path_file_system $v_path_avsc_all "path_avsc_all" 1
	
	#Validamos que existan las rutas en HDFS
	required=0
	if [ 11 -eq $ctl_sid ]; then
		required=1
	fi
	
	#7.3.2 Limpieza de rutas de entrada, si existe la ruta, se borra lo que exista la ruta
	check_path_hdfs "$v_path_avro_all" 1 "path_avro_all"
	check_path_hdfs "$v_path_avro_cifras" 1 "path_avro_cifras"
	check_path_hdfs "$v_path_avro_not_processed" $required "path_avro_not_processed"
	
	print_log ""
	print_log ""
	print_log "$paths_msg_not_exists"
	print_log "$paths_name_not_exists"
	print_log "$paths_not_exists"
	
	get_paths_referenced
	
	if [ 1 -eq $init_validation_paths ]; then		
		update_validation 4 47
		
		#Actualizamos el estatus del evento
		update_events "$status_executed" 3 40
	else
		update_validation 5 47
		
		#Actualizamos el estatus del evento
		update_events "$status_no_executed" 3 40		
	fi
}

#Función para obtener los paths de las tablas referenciadas y poder realizar la validación
get_paths_referenced(){
	#Validaremos si la tabla tiene flujos dependientes que ejecutar y por lo tanto, debemos contar los archivos generados en las rutas de los N flujos
	if [ "NA" != "$referenced_tables" ]; then
		print_log ""
		print_log ""
		print_log "Obtenemos la configuración de las tablas asociadas."
		query_get_paths="select c.path_avro_all,c.path_avro_not_processed,c.path_avro_cifras,c.ctl_tid from $schema_config.$table_config c inner join $schema_config.$table_names t on c.ctl_tid = t.ctl_tid where t.table_status = '$status_active' and lower(c.environment_config) = '$environment' and c.ctl_tid in ($referenced_tables)"
		execute_querys "$query_get_paths" "query_file" 5 "$intentos" "$schema_config" "result_paths_$a_id_table".txt
		
		count_ref=$(grep -o "," <<<"$referenced_tables" | wc -l)
		let count_ref=$(expr $count_ref + 1)
					
		#Incrementamos en 1 el contador de estructuras, ya que la tabla maestra tambien se debe validar
		let total_struct=$(expr $count_ref + 1)
		print_log "Total de configuraciones encontradas (total_struct):$total_struct"
		
		get_paths_sources
	fi
}

#Funciona que obtiene los N paths de las fuentes y los almacena en arreglos para poder realizar la validación del número de archivos creados
get_paths_sources(){
	#Validamos que existan las rutas en HDFS
	required=0
	if [ 11 -eq $ctl_sid ]; then
		required=1
	fi
	
	print_log ""
	print_log ""
	print_log "Validamos las rutas de los tablas asociadas."
	print_log ""
	print_log ""

	for i in $( eval echo {1..$count_ref} )
	do
		current_line=$(tail -n $i "$path_temp"result_paths_"$a_id_table".txt)
		p_a=$(echo ${current_line} | cut -d" " -f1) # Obtiene la ruta de los avros
		p_n=$(echo ${current_line} | cut -d" " -f2) # Obtiene la ruta de los no procesados
		p_c=$(echo ${current_line} | cut -d" " -f3) # Obtiene la ruta de las cifras
		p_i=$(echo ${current_line} | cut -d" " -f4) # Obtiene el id de la tabla
		
		p_a="$(echo -e "${p_a}" | tr -d '[:space:]')"
		p_n="$(echo -e "${p_n}" | tr -d '[:space:]')"
		p_c="$(echo -e "${p_c}" | tr -d '[:space:]')"
		p_i="$(echo -e "${p_i}" | tr -d '[:space:]')"
		
		#7.3.2 Limpieza de rutas de entrada, si existe la ruta, se borra lo que exista la ruta
		check_path_hdfs "$p_a" 1 "path_avro_all"
		check_path_hdfs "$p_n" $required "path_avro_not_processed"
		check_path_hdfs "$p_c" 1 "path_avro_cifras"
		
		paths_avro[$i]="$p_a"
		paths_not_processed[$i]="$p_n"
		paths_cifras[$i]="$p_c"
		table_ids[$i]="$p_i"
	done

	print_log "Agregar ruta:$v_path_avro_all"
	print_log "Agregar ruta:$v_path_avro_not_processed"
	print_log "Agregar ruta:$v_path_avro_cifras"
	
	i=$total_struct
	paths_avro[$i]="$v_path_avro_all"
	paths_not_processed[$i]="$v_path_avro_not_processed"
	paths_cifras[$i]="$v_path_avro_cifras"
	
	print_log ""
	print_log ""
	print_log "$paths_msg_not_exists"
	print_log "$paths_name_not_exists"
	print_log "$paths_not_exists"
	
	print_log ""
	print_log ""
	print_log "paths_avro lon:${#paths_avro[@]}"
	print_log "paths_not_processed lon:${#paths_not_processed[@]}"
	print_log "paths_cifras lon:${#paths_cifras[@]}"
	print_log "table_ids lon:${#table_ids[@]}"
}

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#			  Area de funciones de la fase de preparación                          #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#Funciones en las librerias de uso común

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#			  Area de funciones de la fase de procesamiento                        #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#Funcion para obtener la configuración del procesador a ejecutar
get_config_processor(){
	query_get_processor="select p.processor_name,'|',p.id_processor,'|',p.processor_status,'|',p.level,'|',p.sub_processor_name,'|',p.id_sub_processor,'|',o.attempts_read_avro,'|',o.times_wait_avro,'|',c.path_avro_all,'|',c.path_avro_not_processed,'|',c.path_avro_cifras from $schema_config.$table_processors p inner join ${schema_config}.${table_orchestration} o on p.ctl_tid = o.ctl_tid and p.environment_config = o.environment_config inner join $schema_config.$table_names t on p.ctl_tid = t.ctl_tid inner join $schema_config.$table_config c on p.ctl_tid = c.ctl_tid and p.environment_config = c.environment_config where p.ctl_tid=$a_id_table and t.table_status = '$status_active' and lower(p.environment_config) = '$environment' "
	execute_querys "$query_get_processor" "processor" 21 "$intentos" ""
	params=${response_f[processor]}
	
	export processor_name=$(echo ${params} | cut -d"|" -f1)
	export id_processor=$(echo ${params} | cut -d"|" -f2)
	export status=$(echo ${params} | cut -d"|" -f3)
	export level=$(echo ${params} | cut -d"|" -f4)
	export sub_processor_name=$(echo ${params} | cut -d"|" -f5)
	export id_sub_processor=$(echo ${params} | cut -d"|" -f6)
	export attempts_read_avro=$(echo ${params} | cut -d"|" -f7)
	export time_wait_avro=$(echo ${params} | cut -d"|" -f8)
	export path_avro_all=$(echo ${params} | cut -d"|" -f9)
	export path_avro_not_processed=$(echo ${params} | cut -d"|" -f10)
	export path_avro_cifras=$(echo ${params} | cut -d"|" -f11)
	
	export processor_namef="$(echo -e "${processor_name}" | tr -d '[:space:]')"
	export id_processor="$(echo -e "${id_processor}" | tr -d '[:space:]')"
	export status="$(echo -e "${status}" | tr -d '[:space:]')"
	export level="$(echo -e "${level}" | tr -d '[:space:]')"
	export sub_processor_namef="$(echo -e "${sub_processor_name}" | tr -d '[:space:]')"
	export id_sub_processor="$(echo -e "${id_sub_processor}" | tr -d '[:space:]')"
	export path_avro_all="$(echo -e "${path_avro_all}" | tr -d '[:space:]')"
	export path_avro_not_processed="$(echo -e "${path_avro_not_processed}" | tr -d '[:space:]')"
	export path_avro_cifras="$(echo -e "${path_avro_cifras}" | tr -d '[:space:]')"
	
	print_log "processor_name               $processor_name"
	print_log "processor_namef              $processor_namef"
	print_log "Id procesador es             $id_processor"
	print_log "Estatus es                   $status"
	print_log "level                        $level"
	print_log "sub_processor_name           $sub_processor_name"
	print_log "id_sub_processor             $id_sub_processor"
	print_log "path_avro_all                $path_avro_all"
	print_log "path_avro_not_processed      $path_avro_not_processed"
	print_log "path_avro_cifras             $path_avro_cifras"
	print_log ""
	print_log ""
}

#Funcion lee el parámetro de tiempo en formato 1,1,1,1 y lo transforma en arreglo 1 1 1 1
parser_times(){
	num_sep=$(grep -o "," <<<"$time_wait_avro" | wc -l)
	let num_sep=$(expr $num_sep + 1)

	for i in $( eval echo {1..$num_sep} )
	do
		current_time=$(echo $time_wait_avro | awk -v c=$i -F',' '{ print $c}')
		times_values[$i]="$current_time"
	done
	export lon=$(expr "${#times_values[@]}" - 1 )
	print_log "lon de times_values:$lon"
	echo "${times_values[@]}"
}

#Función para iniciar el procesador de Nifi asociado a la tabla
start_processor(){
	#Validamos el nivel del procesador para saber cual debemos encender
	if [ $level -eq 1 ]; then
		export current_id_processor=$id_processor
		export current_processor_name=$processor_name
		export current_processor_namef=$processor_namef
	else
		export current_id_processor=$id_sub_processor
		export current_processor_name=$sub_processor_name
		export current_processor_namef=$sub_processor_namef
	fi

	f_read_control="$path_temp"files_read_in_path_"$a_id_table"_control.txt
	f_read_control_r="$path_temp"files_read_in_path_"$a_id_table"_control_r.txt
	if [ 0 -eq $recursive_read ]; then
		print_log "Ejecutar conteo para validar si hay mas archivos de lo obtenidos inicialmente"
		print_log "ssh $user@$server find $path_in$name_expression_file -maxdepth 1 -type f 1>$f_read_control"
		$(ssh $user@$server find $path_in$name_expression_file -maxdepth 1 -type f 1>"$f_read_control" 2>>$name_file)
	else
		print_log "Ejecutar conteo para validar si hay mas archivos de lo obtenidis inicialmente"
		print_log "ssh $user@$server find $path_in -iname \"$name_expression_file\" -type f 1>$f_read_control"
		#Obtenemos la lista de archivos existentes para tener snapshoot de lo leido
		$(ssh $user@$server find $path_in -iname "$name_expression_file" -type f 1>"$f_read_control" 2>>$name_file)
		#limpiamos la lista, quitando los archivos de ingested
		cat $f_read_control | grep -v "ingested" > "$f_read_control_r"
		command_ls="cat $f_read_control_r | wc -l"
		export count_file_control=$(eval "$command_ls" 2>>$name_file)
		print_log "Conteo antes de iniciar el procesador $count_file_control"
	fi
	
	power_on_date=$(date '+%F %T')
	print_log "$power_on_date"
	print_log "Iniciar procesador:$current_processor_name"
	export command_start="curl -i -X PUT -H 'Content-Type: application/json' -d '{\"id\":\"$current_id_processor\",\"state\":\"RUNNING\"}' $nifi_api/flow/process-groups/$current_id_processor;"
	print_log "$command_start"

	eval $command_start > "$path_temp"start_"$current_processor_namef".txt
	res=$?
	
	print_log ""
	print_log ""
	print_log "Respuesta inicio procesador $current_processor_name es:$res"
	
	#Leer si la respuesta de la peticion fue correcta
	read_response=$(cat "$path_temp"start_"$current_processor_namef".txt | grep "HTTP")
	print_log "read_response:$read_response"
	res_code_start=$(echo ${read_response} | cut -d" " -f2)
	res_code_start="$(echo -e "${res_code_start}" | tr -d '[:space:]')"
	
	res_desc_start=$(echo ${read_response} | cut -d" " -f3)
	res_desc_start="$(echo -e "${res_desc_start}" | tr -d '[:space:]')"
	
	res_detail_start=$(tail -n 1 "$path_temp"start_"$current_processor_namef".txt)
	res_detail_start="$(echo -e "${res_detail_start}" | tr -d '[:space:]')"

	print_log "res_code_start:$res_code_start"
	print_log "res_desc_start:$res_desc_start"
	print_log "res_detail_start:$res_detail_start"
	
	host_name=$(eval hostname)
	print_log "Petición realizada desde $host_name"
	
	query_insert_detail="insert into $schema_config.$table_processors_detail (id_nifi_exe,ctl_eid,power_on_date,power_on_response,power_off_date,power_off_response,id_processor,status_process,user_name,hostname,created_by,created_on,updated_by,updated_on) values ('$id_nifi_exe','$ctl_eid','$power_on_date','$res_desc_start',null,null,'$current_id_processor','$status_processing','$user','$host_name','$user',now(),null,null)"
	execute_querys "$query_insert_detail" "idet" 30 "$intentos" "$schema_config" ""
	
	#TO-DO comentar esta línea, se puso para poder hacer la prueba completa del flujo
	if [ 1 -eq $run_without_cluster ]; then
		res_code_start="200"
	fi
	#Fin TO-DO
	if [ "$res_code_start" == "200" ]; then
		print_log "Procesador $current_processor_name iniciado"
		print_log ""
		print_log ""
		monitor_status "$avro_attempts"
	else
		print_log "Error al iniciar el procesador $current_processor_name"
		print_log ""
		print_log ""
		
		query_error_processor="update $schema_config.$table_processors_detail set power_on_response='$read_response', status_process='$status_power_off' where ctl_eid='$ctl_eid' "
		execute_querys "$query_error_processor" "ep" 30 "$intentos" "$schema_config" ""
		
		#Actualizamos el estatus del evento
		update_events "$status_no_executed" 5 44
		
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 2: exit 1                              #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 1;
	fi
}

#Funcion para monitorear las ejecucines
monitor_status(){
	print_log "----------------------------------------------------------------------"
	print_log "----------------------------------------------------------------------"
	print_log "---- Revisar estatus ejecucion $current_processor_name --------------"
	print_log "----------------------------------------------------------------------"
	print_log "----------------------------------------------------------------------"
	
	avro_attempts=$1
	print_log "Intentos iniciales avro_attempts:$avro_attempts"
	
	if [ $count_file -ne 0 ]; then
	
		#Validaremos si la tabla tiene flujos dependientes que ejecutar y por lo tanto, debemos contar los archivos generados en las rutas de los N flujos
		if [ "NA" != "$referenced_tables" ]; then
			#Calculamos el número de archivos totales generales
			calculate_number_files
		else
			#En caso de que la tabla no tenga flujos dependientes se valida solo el numero de archivos generados por un flujos
		
			#Leer la ruta del HDFS y contar los archivos depositados
			export num_files_read=$(hdfs dfs -ls -C $path_avro_all | wc -l)
			print_log "Numero de archivos esperados:$count_file"
			print_log "Numero de archivos leidos de la ruta $path_avro_all:$num_files_read"
			
			export num_files_not_processed=$(hdfs dfs -ls -C $path_avro_not_processed | wc -l)
			print_log "Numero de archivos no procesados:$num_files_not_processed"
			
			let total_files_read=$(expr $num_files_read + $num_files_not_processed )
			print_log "Total archivos leidos ambas rutas:$total_files_read"
			
			export num_files_cifras=$(hdfs dfs -ls -C $path_avro_cifras*avro | wc -l)
			print_log "Numero de archivos cifras $path_avro_cifras:$num_files_cifras"
		fi
		
		print_log ""
		print_log ""
		
		#TO-DO Comentar estas líneas, se puso para poder ejecutar el flujo completo
		if [ 1 -eq $run_without_cluster ]; then
			total_files_read=$count_file
			num_files_cifras=$num_files_read		
		fi

		if [ $count_file -eq $total_files_read ] && [ $num_files_read -eq $num_files_cifras ]; then
			echo $(date)
			print_log "Apagar el procesador $current_processor_name"
			end_processor
			
			#Actualizamos el estatus del evento
			update_events "$status_executed" 5 44
			print_log ""
			print_log ""
			print_log "Inicia ejecución de Spark, revisar el log correspondiente..."
			#Invocar el shell de ejecución masiva
			
			if [ 1 -eq $is_referenced ]; then
				if [ $count_ref -gt 0 ]; then
					invoke_process_transformation "$a_id_table" "$current_flow" 1
					print_log "Despues de invocación a 3.process_transformation $a_id_table $current_flow 1"
					print_log ""
					print_log ""
					print_log "Esperamos ${time_wait_invoke}m para lanzar los flujos dependientes..."
					sleep ${time_wait_invoke}m
					
					print_log "Haremos $count_ref invocaciones"
					for i in $( eval echo {1..$count_ref} )
					do
						current_idsource=${table_ids[$i]}
						current_idsource="$(echo -e "${current_idsource}" | tr -d '[:space:]')"
						print_log "Inovocación $i, con id=$current_idsource"
						
						invoke_process_transformation "$current_idsource" "$current_flow" 1
						print_log "Despues de invocación a 2.process_transformation $a_id_table $current_flow 1"
						print_log ""
						print_log ""
						print_log "Esperamos ${time_wait_invoke}m para lanzar el siguiente flujo dependiente..."
						sleep ${time_wait_invoke}m
					done
				fi
			else
				invoke_process_transformation "$a_id_table" "$current_flow" 0
				print_log "Despues de invocación a 1.process_transformation $a_id_table $current_flow 0"
			fi
		else
			#Esperar a que acabe la ejecucion de Nifi
			minutos=${times_values[$indice]}
			print_log "Intento $avro_attempts de $attempts_read_avro para obtener los $count_file avros generados"
			print_log "Ejecucion en curso del procesador $current_processor_name, esperar $minutos minuto(s) - ($(date))."
			print_log ""
			print_log ""
			sleep ${minutos}m
			
			if [ $avro_attempts -eq $attempts_read_avro ]; then
				export avro_attempts=0
				print_log "Se agotaron los $attempts_read_avro intentos para leer los $count_file avros generados por el procesador $current_processor_name de la fuente ctl_sid:$ctl_sid."
				print_log "Hora:($(date))"
				print_log ""
				print_log ""
				end_processor
				
				#Actualizamos el estatus del evento
				update_events "$status_no_executed" 5 44		
				
				#Insertamos el registro del evento a procesar
				insert_events 6 "$status_processing" 45
				
				if [ 1 -eq $is_referenced ]; then
					insert_events_all 6 "$status_processing" 45
				fi
	
				export color="#F3A110"
				if [ "true" == "$send_notification_mail" ]; then
					put_mail_parameters_error
					send_notification_error
				fi
				#Actualizamos el estatus del evento
				update_events "$status_executed" 6 46
				print_log ""
				print_log ""
				
				print_log "#----------------------------------------------------------------------------------#"
				print_log "#                          Punto de control 3: exit 0                              #"
				print_log "#----------------------------------------------------------------------------------#"
				exit 0;
			fi
			
			if [ $indice -eq $lon ]; then
				export indice=1
			fi
			let indice=$(expr $indice + 1 )
			let avro_attempts=$(expr $avro_attempts + 1 )
			monitor_status "$avro_attempts"
		fi
	fi
}

#Función para apagar el procesador Nifi asociado a la tabla
end_processor(){
	intentos=$1
	
	print_log "Detener procesador $current_processor_name"
	export command_stop="curl -i -X PUT -H 'Content-Type: application/json' -d '{\"id\":\"$current_id_processor\",\"state\":\"STOPPED\"}' $nifi_api/flow/process-groups/$current_id_processor;"
	print_log "$command_stop"
	hr_fin=$(date '+%F %T')
	print_log "$hr_fin"
	eval $command_stop > "$path_temp"stop_"$current_processor_namef".txt
	res=$?
	
	print_log ""
	print_log ""
	print_log "Respuesta detener procesador $current_processor_name es:$res"
	
	#Leeremos si la respuesta de la peticion fue correcta
	salida=$(cat "$path_temp"stop_"$current_processor_namef".txt | grep "HTTP")
	print_log "salida:$salida"
	response_code=$(echo ${salida} | cut -d" " -f2)
	response_code="$(echo -e "${response_code}" | tr -d '[:space:]')"
	
	response_desc=$(echo ${salida} | cut -d" " -f3)
	response_desc="$(echo -e "${response_desc}" | tr -d '[:space:]')"
	
	response_detail=$(tail -n 1 "$path_temp"stop_"$current_processor_namef".txt)
	response_detail="$(echo -e "${response_detail}" | tr -d '[:space:]')"

	print_log "response_code:$response_code"
	print_log "response_desc:$response_desc"
	print_log "response_detail:$response_detail"
	
	#TO-DO Comentar está línea, se puso para poder probar el flujo completo
	if [ 1 -eq $run_without_cluster ]; then	
		response_code="200"
	fi
	
	if [ "$response_code" == "200" ]; then
		print_log "Respuesta correcta en end_processor"
		print_log ""
		print_log ""
		
		power_off_date=$(date '+%F %T')
		query_update_detail="update $schema_config.$table_processors_detail set power_off_date='$power_off_date', power_off_response='$response_desc', status_process='$status_executed', updated_by='$user', updated_on=now() where id_nifi_exe='$id_nifi_exe' and ctl_eid='$ctl_eid' "
		execute_querys "$query_update_detail" "udet" 31 "$intentos" "$schema_config" ""

		export intentos=0
	else
		if [ $intentos -eq $max_intentos ]; then
			export intentos=0
			print_log "Se agotaron los $max_intentos intentos para Detener procesador $current_processor_name."
			
			query_update_detail="update $schema_config.$table_processors_detail set power_off_response='$response_detail', status_process='$status_power_on', updated_by='$user', updated_on=now() where id_nifi_exe='$id_nifi_exe' and ctl_eid='$ctl_eid' "
			execute_querys "$query_update_detail" "udet" 32 "$intentos" "$schema_config" ""
			
			#Actualizamos el estatus del evento
			update_events "$status_no_executed" 5 44
		fi
		let intentos=$(expr $intentos + 1 )	
		print_log "Hubo un error al Detener procesador $current_processor_name, se reinterará la ejecucion. Reintento:#$intentos."
		print_log "*****************************************************"
		echo
		echo
		if [ $intentos -ne $max_intentos ]; then
			end_processor "$intentos"
		fi
	fi
}

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#			  Area de funciones ????					   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#

calculate_number_files(){
	print_log "Numero de archivos esperados:$count_file"
	total_avro=0
	total_processed=0
	total_cifras=0
	sum_total=0
	
	print_log "Recorrer de 1 a $total_struct"
	for idx in $( eval echo {1..$total_struct} )
	do
		print_log "******************************************************"
		print_log "------------------------------------------------------"
		print_log "****************  Rutas a leer $idx  ********************"
		print_log "Ruta avros: ${paths_avro[$idx]}"
		print_log "Ruta cifra: ${paths_cifras[$idx]}"
		print_log "Ruta notpr: ${paths_not_processed[$idx]}"
		print_log "------------------------------------------------------"
		print_log "******************************************************"
		
		#Leer la ruta del HDFS y contar los archivos depositados
		if [ "${paths_avro[$idx]}" == "NULL" ]; then
			t_avro=0
		else
			t_avro=$(hdfs dfs -ls -C ${paths_avro[$idx]} | wc -l)
		fi
		print_log "Numero de archivos leidos de la ruta ${paths_avro[$idx]}:$t_avro"
		let total_avro=$(expr $t_avro + $total_avro)

		if [ "${paths_cifras[$idx]}" == "NULL" ]; then
			t_cifras=0
		else
			t_cifras=$(hdfs dfs -ls -C ${paths_cifras[$idx]}*avro | wc -l)
		fi
		print_log "Numero de archivos cifras ${paths_cifras[$idx]}:$t_cifras"
		let total_cifras=$(expr $t_cifras + $total_cifras)
		
		if [ "${paths_not_processed[$idx]}" == "NULL" ]; then
			t_processed=0
		else
			t_processed=$(hdfs dfs -ls -C ${paths_not_processed[$idx]} | wc -l)
		fi
		print_log "Numero de archivos no procesados:$t_processed"
		let total_processed=$(expr $t_processed + $total_processed)

		let t_files=$(expr $t_avro + $t_processed )
		print_log "Total archivos leidos ambas rutas:$t_files"
		
		let sum_total=$(expr $sum_total + $t_files )
		
		print_log ""
		print_log ""
	done

	print_log "Total avros:$total_avro"
	print_log "Total cifras:$total_cifras"
	print_log "Total no procesados:$total_processed"
	print_log "Suma ambas rutas:$t_files"
	print_log ""
	print_log ""
	
	export num_files_read=$total_avro
	export num_files_not_processed=$total_processed
	export num_files_cifras=$total_cifras
	export total_files_read=$sum_total
	
	print_log "num_files_read:$num_files_read"
	print_log "num_files_not_processed:$num_files_not_processed"
	print_log "num_files_cifras:$num_files_cifras"
	print_log "total_files_read:$total_files_read"
	print_log ""
	print_log ""
	
	count_file=$count_file_bck
	let count_file=$(expr $count_file \* $total_struct )
	print_log "count_file actualizado:$count_file"
}

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#						Funciones por fases de ejecucion						   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#Función para ejecutar las validaciones de fase de inicialización
process_initialization(){
	print_trace "process_initialization"
	print_log "#----------------------------------------------------------------------------------#"
	print_log "#                          7.2 Fase de inicialización                              #"
	print_log "#----------------------------------------------------------------------------------#"
	
	#7.2 Fase de inicialización 
	#leemos el archivo de propiedades
	read_properties "$file_properties"
	
	size_properties=${#properties[@]}
	print_log "properties longitud: $size_properties"
	if [ 0 -eq $size_properties ]; then
		print_log "Revisar la lectura del archivo de propiedades."
		
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 4: exit 0                              #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 0;
	fi
	
	print_log "*****************************************************"
	getDate
	print_log "*****************************************************"
	#7.2.1 Asignación de variables globales 
	set_environment_variables
	print_log "*****************************************************"
	
	get_param_referenced
	validate_execution_in_progress
	
	if [ 0 -eq $execution_in_process ]; then
		validate_incomplete_execution
		print_log "execute_all_phases        $execute_all_phases"
		print_log "incomplete_master         $incomplete_master"
		print_log "is_referenced             $is_referenced"
		print_log "execute_all_phases_ref    $execute_all_phases_ref"
		print_log "incomplete_referenced     $incomplete_referenced"
		print_log "current_id_event          $current_id_event"
		print_log "min_event                 $min_event"
		print_log ""
		print_log ""
		
		#Si el flujo solo es master
		if [ 0 -eq $is_referenced ]; then
			print_log "Caso 1."
			if [ 1 -eq $execute_all_phases ]; then
				#Ejecutar todas las fases del proceso
				print_log "Ejecutar todas las fases del proceso."
				process_execute_initialization
			else
				#Ejecutar desde la fase donde se quedó el proceso anterior
				get_config_validation_source
				print_log "Ejecutar a partir de la fase donde se quedo el proceso anterior."
				print_log "Ejecutar desde current_id_event:$current_id_event"
				print_log "Ejecutar con ctl_eid:$ctl_eid"
				function_mapping
				print_log "Se finalizará el flujo de carga"
				print_log "#----------------------------------------------------------------------------------#"
				print_log "#                          Punto de control 5: exit 0                              #"
				print_log "#----------------------------------------------------------------------------------#"
				exit 0;
			fi
		else
			#El flujo master tiene flujos hijos
			print_log "Caso 2."
			#No hay pendientes master y No hay pendientes hijos
			if [ 1 -eq $execute_all_phases -a 1 -eq $execute_all_phases_ref ]; then
				print_log "No hay pendientes master y No hay pendientes hijos"
				#Ejecutar todas las fases del proceso
				print_log "Ejecutar todas las fases del proceso."
				process_execute_initialization
			else
				#Si hay pendientes master y Si hay pendientes hijos
				if [ 0 -eq $execute_all_phases -a 0 -eq $execute_all_phases_ref ]; then
					print_log "Si hay pendientes master y Si hay pendientes hijos"
					#Si el evento pendiente master es igual al evento pendiente hijo
					if [ $current_id_event -eq $min_event -a 6 -gt $current_id_event ]; then
						print_log "Si el evento pendiente master es igual al evento pendiente hijo"
						print_log "Ejecutar a partir de la fase donde se quedo el proceso anterior."
						print_log "Ejecutar desde current_id_event:$current_id_event"
						print_log "Ejecutar con ctl_eid:$ctl_eid"
						function_mapping
						print_log "Se finalizará el flujo de carga"
						print_log "#----------------------------------------------------------------------------------#"
						print_log "#                          Punto de control 5: exit 0                              #"
						print_log "#----------------------------------------------------------------------------------#"
						exit 0;
					else
						#El evento pendiente master No es igual al evento pendiente hijo, lanzar por separado los flujos
						#Ponemos la bandera is_referenced a 0 para que el flujo master y los flujos hijos se procesen individualmente
						print_log "El evento pendiente master No es igual al evento pendiente hijo, lanzar por separado los flujos"
						export was_referenced=1
						export is_referenced=0
						function_mapping
						#Lanzar flujos hijos
						get_pending_flow
					fi
				else
					print_log "Solo hay eventos pendientes hijos"
					export is_referenced=0
					#Lanzar flujos hijos independientes
					get_pending_flow
				fi
			fi
		fi		
	else
		print_log "*****************************************************"
		print_log "Existe una ejecución en curso para el id de tabla: $a_id_table."
		summary
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 6: exit 0                              #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 0;
	fi
}


#Función para ejecutar la fase de inicialización
process_execute_initialization(){
	print_trace "process_execute_initialization"
	print_log "*****************************************************"
	get_config_validation_source
	print_log "*****************************************************"
	
	#7.2.2 Validaciones de control
	validate_source "$local_attempts"
	print_log "*****************************************************"
	
	#La validación 7.2.2.1 Existencia de archivos a procesar, fue exitosa
	if [ 1 -eq $init_validation_source ]; then
		#7.2.2.3 Validación de clúster
		if [ 1 -eq $use_nifi ]; then
			get_status_cluster
		else
			update_validation 6 27
			
			#Como el flujo no usa Nifi, se pone en 1 la validación del cluster para poder continuar con el proceso
			export init_validation_server=1
		fi
	fi
	
	if [ 1 -eq $init_validation_server ]; then
		#7.2.2.4 Validación de rutas:
		validation_paths
	fi

	#Actualizar la tabla de validación con la hora de fin
	validation_end=$(date '+%F %T')
	
	#Verificamos que las validaciones hayan sido correctas
	#7.2.2 Validaciones de control
	if [ 1 -eq $init_validation_source -a 1 -eq $init_validation_server -a 1 -eq $init_validation_paths ]; then
		generate_field_nifi_exe		
		update_validation 7 28
		
		export phase_initialization=1
		export send_alert_execute=1
		export send_alert_not_execute=0
	else
		update_validation 8 29
		
		export phase_initialization=0
		export send_alert_execute=0
		export send_alert_not_execute=1
	fi
}

#Función para ejecutar la fase de pre procesamiento
process_pre_processing(){
	print_log "#----------------------------------------------------------------------------------#"
	print_log "#                               7.3 Fase de preparación                            #"
	print_log "#----------------------------------------------------------------------------------#"
	
	#Insertamos el registro del evento a procesar
	insert_events 4 "$status_processing" 41
	
	if [ 1 -eq $is_referenced ]; then
		insert_events_all 4 "$status_processing" 41
	fi
	
	#7.3.1 Generación de notificación:
	#7.3.1.1 Notificación
	if [ 1 -eq $send_alert_execute ] ; then
		#Enviar correo de que si se ejecuta el proceso
		export si_no="si"
		export reason="."
		export color="#87CEEB"
		get_desc_periodicity
		if [ "true" == "$send_notification_mail" ]; then
			put_mail_parameters
			#7.3.3 Envío de notificación o alerta
			send_notification
		fi
		export phase_pre_processing=1
		
		#Actualizamos el estatus del evento
		update_events "$status_executed" 4 42
	fi
	
	#7.3.1 Generación de notificación:
	#7.3.1.2 Alerta
	if [ 1 -eq $send_alert_not_execute ] ; then
		#Enviar correo al responsable para que disponibilize la informacion y proceso no corre
		export si_no="no"
		export reason=$reason_no
		export color="#F3A110"
		get_desc_periodicity
		if [ "true" == "$send_notification_mail" ]; then
			put_mail_parameters
			#7.3.3 Envío de notificación o alerta
			send_notification
		fi
		
		#Actualizamos el estatus del evento
		update_events "$status_executed" 4 42
		
		print_log "Finaliza flujo en 7.3 Fase de preparación"
		summary
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 7: exit 0                              #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 0;
	fi	
}

#Función para ejecutar la fase de procesamiento
process_processing(){
	#7.4 Fase de procesamiento
	print_log "#----------------------------------------------------------------------------------#"
	print_log "#                               7.4 Fase de procesamiento                          #"
	print_log "#----------------------------------------------------------------------------------#"
	
	#Validamos si la fuente usa Nifi para saber si insertamos o no este evento	
	if [ 1 -eq $use_nifi ]; then
		#Insertamos el registro del evento a procesar
		insert_events 5 "$status_processing" 43
		if [ 1 -eq $is_referenced ]; then
			insert_events_all 5 "$status_processing" 43
		fi
	
		export local_attempts=0
		get_config_processor
		parser_times
		start_processor
	else
		#Invocar el shell de ejecución masiva
		invoke_process_transformation "$a_id_table" "$current_flow" 0
	fi
}

#Función para validar si la fase de procesamiento se ejecuta o no
validate_processing(){
	print_log "phase_pre_processing: $phase_pre_processing"
	if [ 1 -eq $phase_pre_processing ]; then
		#7.4 Fase de procesamiento
		process_processing
		print_log "processing"
	fi
}

#Función para ejecutar la fase post procesamiento
process_post_processing(){
	echo "process_post_processing"
}

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#								Funcion principal del shell						   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#

#7.1 Orquestador 
process_ingestion(){
	print_trace "process_ingestion"
	#Iniciamos el proceso ejecutando la fase de inicialización, para ambientar el proceso y leer las variables a utilizar
	process_initialization

	print_log "current_flow:$current_flow"
	if [ "phase_all" == "$current_flow" -o "7" == "$current_flow" -o "8" == "$current_flow"  -o "9" == "$current_flow"  -o "10" == "$current_flow" ]; then
		#7.3 Fase de preparación 
		process_pre_processing

		#7.4 Fase de procesamiento
		validate_processing
	fi
	
	print_log "#----------------------------------------------------------------------------------#"
	print_log "#                                Final de ejecución                                #"
	print_log "#                        Aquí debe finalizar siempre el flujo                      #"
	print_log "#----------------------------------------------------------------------------------#"
}

process_ingestion
