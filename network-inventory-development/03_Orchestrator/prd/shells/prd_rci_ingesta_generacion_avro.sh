#set -xv
#!/bin/bash
#------------------------------------------------------------------------------------------------------------#
#	Nombre:		prd_rci_ingesta_generacion_avro.sh                                             			 	 #
#	Versión:	1.0.0                                          			 		                             #
#	Objetivo: 	Ejecuta comandos de kite para poder generar los schemas avro.							     #
#	Autor:		ejesus				                                                                         #
#	Vía de ejecución: Línea de comandos		                                                            	 #
#	Fecha:		04 de Noviembre de 2019  	                                                           		 #
#	Area:		Datalake AT&T											                                     #
#------------------------------------------------------------------------------------------------------------#

if [ $# -lt 1 ]
	then
		echo '--------------------------------------------------------------'
		echo "Error: parametro"
		echo "usage: sh $(basename $0) num_archivo_procesar"
		echo '--------------------------------------------------------------'
	exit 1
fi

export a_id_table=$1
export flow_continue=$2

#Agregamos las lineas para poder utilizar la librería utils
. $path_lib/"$environment"_utils.sh

print_log ""
print_log ""
print_log "#----------------------------------------------------------------------------------#"
print_log "#                         7.4.2 Componente de Transformación                       #"
print_log "#----------------------------------------------------------------------------------#"
print_log ""
print_log ""
print_log "Parámetro 1 recibido $a_id_table"
print_log "Parámetro 2 recibido $flow_continue"
print_log "Ejecutando shell $environment _rci_ingesta_generacion_avro.sh"
print_log ""
print_log ""

#----------------------------------------------------------------------------------#
#	Variables de ambiente para obtener parametros necesarios para la ejecucion	   #
#----------------------------------------------------------------------------------#
export ext_processed="_processed"
export processed_hist="historico/"
executer=0

# Variables para poder reintentar ejecutar una consulta en caso de desconexión
export intentos=1
export max_intentos=3
declare -A response

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#								Area de funciones comunes						   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#			Area de funciones para generar registros en ingestion_files			   #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
# Funcion para obtener la configuración de la tabla a procesar
get_file_process(){
	print_log "$schema."
	print_log "$schema_config."
	print_log "$table_execution."
	print_log "$table_source."
	print_log "$table_names."
	print_log "$table_config."
	print_log "$table_statistics."
	print_log "$path_backup_file."
	print_log "$path_odk_info."
	print_log "*****************************************************"
	
	query_get_param="select c.path_hdfs, c.path_backup, c.ban_process_all, c.path_avsc_all, c.path_avro_all, c.ctl_tid, c.json_partition, t.table_name, c.schema_database from $schema_config.$table_config c inner join $schema_config.$table_names t on c.ctl_tid = t.ctl_tid where c.ctl_tid=$a_id_table and t.table_status='$status_active' and lower(c.environment_config) = '$environment' "
	execute_querys "$query_get_param" "params" 10 "$intentos" "$schema_config"
	params=${response_f[params]}
	
	export location=$(echo ${params} | cut -d" " -f1)
	export path_back=$(echo ${params} | cut -d" " -f2)
	export process_all=$(echo ${params} | cut -d" " -f3)
	export path_avsc=$(echo ${params} | cut -d" " -f4)
	export path_avro=$(echo ${params} | cut -d" " -f5)
	export id=$(echo ${params} | cut -d" " -f6)
	export json=$(echo ${params} | cut -d" " -f7)
	export table_name=$(echo ${params} | cut -d" " -f8)
	export schema_load=$(echo ${params} | cut -d" " -f9)
	
	export location="$(echo -e "${location}" | tr -d '[:space:]')"
	export path_back="$(echo -e "${path_back}" | tr -d '[:space:]')"
	export process_all="$(echo -e "${process_all}" | tr -d '[:space:]')"
	export path_avsc="$(echo -e "${path_avsc}" | tr -d '[:space:]')"
	export path_avro="$(echo -e "${path_avro}" | tr -d '[:space:]')"
	export id="$(echo -e "${id}" | tr -d '[:space:]')"
	export json="$(echo -e "${json}" | tr -d '[:space:]')"	
	export table_name="$(echo -e "${table_name}" | tr -d '[:space:]')"
	export schema_load="$(echo -e "${schema_load}" | tr -d '[:space:]')"
		
	if [ "prd" != "$environment" -a "PRD" != "$environment" ]; then
		export table_name="$environment"_$table_name
	fi
	
	print_log "Location es          $location"
	print_log "Path respaldo        $path_back"
	print_log "Procesar todo        $process_all."
	print_log "Path esquemas        $path_avsc"
	print_log "Path avros           $path_avro"
	print_log "ctl_sid              $id"
	print_log "Json                 $json"
	print_log "Se creara tabla      $table_name"
	print_log "Se creara en esquema $schema_load"
}

#Funcion que obtiene el id del grupo de registros y la ejecución actual
read_avros_process(){
	#Validamos si debemos insertar registro de evento o sólo actualizar
	if [ "phase_all" == "$flow_continue" -o "5" == "$flow_continue" ]; then
		#Insertamos el registro relacionado al evento
		#Procesamiento de archivos estandarizados
		insert_events 7 "$status_processing" 48
		#Generar cifras de control
		insert_events 8 "$status_processing" 49
	else
		#Actualizamos el estatus del evento
		update_events "$status_processing" 7 50
		update_events "$status_processing" 8 51	
	fi

	#Creamos ruta temporal que usaremos para almacenar archivos de control
	if [ ! -d $path_temp ]; then
		mkdir $path_temp
	fi
	
	get_id_group
	if [ "NULL" == "$id_group" ]; then
		export id_group=1
	else
		#Validamos si hay ejecuciones pendientes
		get_id_executer
		if [ "$executer" == "NULL" ]; then
			print_log "id_group en NULL:$id_group"
			let new_id_group=$(expr $id_group + 1 )
			export id_group=$new_id_group
			print_log "id_group despues NULL:$id_group"
		fi
	fi
	
	get_id_executer
	
	if [ "$executer" == "NULL" ]; then
		executer=1
		generate_executions
	fi
	
	print_log "----------------------------------------------------------------------executer:$executer"
}

#Funcion para obtener el id_group actual desde la base de datos
get_id_group(){
	print_log "Obteniendo id_group de la tabla "
	get_group="select max(id_group) as id_group from $schema_config.$table_execution where ctl_tid=$a_id_table and dateload=$date_load"
	execute_querys "$get_group" "id_group" 24 "$intentos" ""
	export id_group=${response_f[id_group]}
	print_log "id_group es:$id_group"
}

#Función que obtiene el id de la primer ejecución a procesar.
get_id_executer(){
	print_log "Obteniendo primer ejecucion a procesar..."
	get_id_executer="select min(id_ingestion_file) as id_ingestion_file from $schema_config.$table_execution where ctl_tid=$a_id_table and dateload=$date_load and status_ingestion != '$status_executed' and id_group=$id_group "
	execute_querys "$get_id_executer" "executer" 1 "$intentos" ""
	export executer=${response_f[executer]}
	print_log "executer:$executer."
}

#Funcion que inserta registros en la tabla cr_rci_ingestion_files los nombres de los archivos avro a procesar.
generate_executions(){
	#Evaluamos si debemos leer varios esquemas o solo 1
	if [ $process_all -eq 1 ]; then
		hdfs dfs -ls -C $path_avro > "$path_temp"list_avro_"$id".txt
		
		export num_files_avro=$(wc -l "$path_temp"list_avro_"$id".txt | awk -F' ' '{ print $1}')
		print_log "Total avros a procesar:$num_files_avro."
		
		if [ 1 -eq $run_without_cluster ]; then
			num_files_avro=1
		fi
			
		cont_inverse=$num_files_avro
		if [ $num_files_avro -ne 0 ]; then
			#Comenzamos el ciclo de procesamiento de N archivo avros
			for i in $( eval echo {1..$num_files_avro} )
			do	
				#Obtenemos el avro a procesar
				current_file=$(tail -n $i "$path_temp"list_avro_"$id".txt)
				current_file=$(echo ${current_file} | cut -d" " -f1) # Obtiene el nombre del archivo
				current_file="$(echo -e "${current_file}" | tr -d '[:space:]')"

				print_log "********* Crear ejecucion:$cont_inverse con  archivo:$current_file. *********"
								
				#Insertar en la tabla de ejecuciones las N ejecuciones identificadas
				query_insert_execution="insert into table $schema_config.$table_execution (id_group,id_ingestion_file,ctl_tid,ctl_eid,dateload,avro_name,start_execution,end_execution,status_ingestion,command,id_application,attempts,created_by,created_on,updated_by,updated_on) VALUES ($id_group, $cont_inverse, $a_id_table ,'$ctl_eid', $date_load, '$current_file', NULL AS start_execution, NULL AS end_execution, '$status_pending', '' as command, '' as id_application,0,'$user',now(),null,null)"
				execute_querys "$query_insert_execution" "insert_execution" 13 "$intentos"
				insert_execution=${response_f[insert_execution]}	
				print_log "valor retornado Query_13:$insert_execution."
				cont_inverse=$(expr $cont_inverse - 1)
			done
		else
			print_log "No hay avros para procesar."
			update_events "$status_no_executed" 7 52
			update_events "$status_no_executed" 8 53
			print_log "#----------------------------------------------------------------------------------#"
			print_log "#                  Punto de control 8: exit 1, ctl_tid=$a_id_table                 #"
			print_log "#----------------------------------------------------------------------------------#"
			exit 1;
		fi
	else
		print_log "Procesar archivos de ODK's"		
		hdfs dfs -ls -R $path_avro | awk '{print $2$8}' | grep "-" > "$path_temp"list_odks_"$id".txt		
		export num_folders_avro=$(wc -l "$path_temp"list_odks_"$id".txt | awk -F' ' '{ print $1}')
		print_log "Total folders a procesar:$num_folders_avro."
			
		cont_inverse=$num_folders_avro
		if [ $num_folders_avro -ne 0 ]; then
			#Ccomenzamos el ciclo de procesamiento de N archivo avros
			for i in $( eval echo {1..$num_folders_avro} )
			do	
				#Obtenemos el avro a procesar
				current_file=$(tail -n $i "$path_temp"list_odks_"$id".txt)
				current_file=$(echo ${current_file} | cut -d"-" -f2)
				current_file=$current_file/
				current_file="$(echo -e "${current_file}" | tr -d '[:space:]')"

				print_log "********* Crear ejecucion:$cont_inverse con  archivo:$current_file. *********"
								
				#Insertar en la tabla de ejecuciones las N ejecuciones identificadas
				query_insert_execution="insert into table $schema_config.$table_execution (id_group,id_ingestion_file,ctl_tid,ctl_eid,dateload,avro_name,start_execution,end_execution,status_ingestion,command,id_application,attempts,created_by,created_on,updated_by,updated_on) VALUES ($id_group, $cont_inverse, $a_id_table ,'$ctl_eid', $date_load, '$current_file', NULL AS start_execution, NULL AS end_execution, '$status_pending', '' as command, '' as id_application,0,'$user',now(),null,null)"
				execute_querys "$query_insert_execution" "insert_execution" 22 "$intentos"
				insert_execution=${response_f[insert_execution]}
				cont_inverse=$(expr $cont_inverse - 1)
			done
		else
			print_log "No hay folders a procesar ODK."
			update_events "$status_no_executed" 7 52
			update_events "$status_no_executed" 8 53
			print_log "#----------------------------------------------------------------------------------#"
			print_log "#                          Punto de control 9: exit 1                              #"
			print_log "#----------------------------------------------------------------------------------#"
			exit 1;
		fi
	fi
}

# Funcion que verifica si procesaremos 1 esquema o mas, y lee el esquema(s) a procesar
read_schema_to_process(){
	#Creamos ruta temporal que usaremos para almacenar archivos de control
	if [ ! -d $path_temp ]; then
		mkdir $path_temp
	fi
	
	#Evaluamos si debemos leer varios esquemas o solo 1
	if [ $process_all -eq 1 ]; then
		#Validar si fallo el avro anterior, si fallo, no debemos procesar otro esquema, solo procesamos el avro
		#Si no fallo, procesar el siguiente avro
		
		query_get_attempts="select attempts from $schema_config.$table_execution where ctl_tid=$a_id_table and dateload=$date_load and id_ingestion_file = $executer and id_group = $id_group "
		execute_querys "$query_get_attempts" "get_attempts" 17 "$intentos"
		get_attempts=${response_f[get_attempts]}
		
		print_log "Total de intentos son:$get_attempts"
		
		if [ $get_attempts -eq 0 ]; then
			print_log "Se validará esquema"
			
			#Tomar el siguiente esquema a procesar
			ls -r "$path_avsc"*.avsc | awk -F' ' '{ print $1}' > "$path_temp"list_files_avsc_"$id".txt
			
			#Obtenemos el numero de lineas que contiene el archivo, para saber cuantos esquemas son los que generaron
			wc -l "$path_temp"list_files_avsc_"$id".txt | sed 's/${path_file}//' > "$path_temp"total_archivos_"$id".txt
			num_files=$(tail -n 1 "$path_temp"total_archivos_"$id".txt)
			export num_files=$(echo ${num_files} | cut -d" " -f1)
			print_log "Total esquemas a procesar:$num_files."
			
			hdfs dfs -ls -C $path_avro > "$path_temp"list_avro_"$id".txt
			export num_files_avro=$(wc -l "$path_temp"list_avro_"$id".txt | awk -F' ' '{ print $1}')
			print_log "Total avros a procesar:$num_files_avro."
			
			print_log "Total archivos a procesar:$num_files_avro."
			
			if [ 1 -eq $run_without_cluster ]; then
				num_files_avro=1
			fi
			
			if [ $num_files_avro -ne 0 ]; then
				#Comenzamos el ciclo de procesamiento de N esquenas
				for i in $( eval echo {1..$num_files_avro} )
				do	
					#Obtenemos el esquema a procesar
					current_file=$(tail -n $i "$path_temp"list_files_avsc_"$id".txt)
					current_file=$(echo ${current_file} | cut -d" " -f1) # Obtiene el nombre del archivo
					current_file="$(echo -e "${current_file}" | tr -d '[:space:]')"
					print_log ""
					print_log ""
					print_log ""
					print_log "*****************************************************"
					print_log "*****************************************************"
					print_log "Archivo $i a procesar:$current_file."
					print_log "*****************************************************"
					print_log "*****************************************************"		
					
					#Obtenemos el nombre del esquema a procesar
					num=$(grep -o "/" <<<"$current_file" | wc -l)
					let numf=$(expr $num + 1)
					current_name=$(echo ${current_file} | cut -d"/" -f$numf)
					current_name="$(echo -e "${current_name}" | tr -d '[:space:]')"
					
					#Generamos el esquema generico soporta por kite
					generate_avsc_generic "$current_file" "$current_name"
					compare_schema "$current_file"
					
					print_log "Se Realizara operacion esquema?:$update_schema"
					
					if [ $update_schema -eq 1 ]; then
						generate_schema "$current_file"
					fi
					get_num_files_processed
					
					print_log "Mover esquema update_schema?:$update_schema."
					print_log "Mover esquema move_schemas?:$move_schemas."
					if [ $update_schema -eq 1 ] && [ $move_schemas -eq 0 ]; then
						move_schema_loaded "$current_file" "$current_name"
					else
						move_schema_no_loaded "$current_file" "$current_name"
					fi
					#Siempre procesamos el AVRO, porque aunque no haya cambio de esquema, los datos se deben insertar
					print_log "Invocar process_avro 1"
					process_avro
					
					print_log ""
					print_log ""
					print_log ""
					print_log ""
					print_log ""
				done
			else
				print_log "No hay esquemas AVSC para procesar."
			fi
		else
			#Si la ejecucion anterior tiene mas de 0 intentos, se procesa solamente el avro
			print_log "No se valida esquema, sólo se procesarán avros"
			
			print_log "Invocar process_avro 2"
			process_avro
			#Actualizamos el contador de la ejecucion
			print_log "Invocar read_avros_process 2"
			#Y enseguida llamamos al proceso que itera para procesar los demas esquemas
			
			print_log "3-Finalizo ejecucion:$executer"			
			print_log "3-Continua ejecucion:$executer"
			print_log "3-Total executions:$executions"
			if [ $executer -lt $executions ]; then
				print_log "Invocar read_avros_process 2"
				read_avros_process
				#Y enseguida llamamos al proceso que itera para procesar los demas esquemas
				read_schema_to_process
			fi			
		fi
	else
		print_log "Procesar solo 1 esquema..."
		#################################################
		#Validar si fallo el avro anterior, si fallo, no debemos procesar otro esquema, solo procesamos el avro
		#Si no fallo, procesar el siguiente avro
		
		query_get_attempts="select attempts from $schema_config.$table_execution where ctl_tid=$a_id_table and dateload=$date_load and id_ingestion_file = $executer and id_group = $id_group "
		execute_querys "$query_get_attempts" "get_attempts" 17 "$intentos"
		get_attempts=${response_f[get_attempts]}
		
		if [ $get_attempts -eq 0 ]; then
			#Para los ODKS, solo se registra una vez el esquema y pueden llegar N cargas
			#No cumple con la logica de todas las demas fuentes, donde llegan
			#N esquemas y N avros
			#Tomar el siguiente esquema a procesar
			ls -r "$path_avsc"*.avsc | awk -F' ' '{ print $1}' > "$path_temp"list_files_avsc_"$id".txt
			export num_files=$(wc -l "$path_temp"list_files_avsc_"$id".txt | awk -F' ' '{ print $1}')
			print_log "Total esquemas-odk a procesar:$num_files."
			
			hdfs dfs -ls -C $path_avro > "$path_temp"list_avro_"$id".txt
			export num_avros=$(wc -l "$path_temp"list_avro_"$id".txt | awk -F' ' '{ print $1}')
			print_log "Total avros-odk a procesar:$num_avros."
			
			if [ $num_files -ne 0 ]; then
			
				if [ $num_files -lt $num_avros ]; then
					num_files=$num_avros
					print_log "Total esquemas queda:$num_files."
				fi
			
				#Ccomenzamos el ciclo de procesamiento de N esquenas
				for i in $( eval echo {1..$num_files} )
				do	
					if [ 1 -eq $i ]; then
						#Obtenemos el esquema a procesar
						#current_file=$(tail -n $i "$path_temp"list_avro_"$id".txt)
						current_file=$(tail -n $i "$path_temp"list_files_avsc_"$id".txt)
						current_file=$(echo ${current_file} | cut -d" " -f1)
						current_file="$(echo -e "${current_file}" | tr -d '[:space:]')"
						print_log ""
						print_log ""
						print_log ""
						print_log "*****************************************************"
						print_log "*****************************************************"
						print_log "Esquema $i a procesar:$current_file."
						print_log "*****************************************************"
						print_log "*****************************************************"		
						
						#Obtenemos el nombre del esquema a procesar
						num=$(grep -o "/" <<<"$current_file" | wc -l)
						let numf=$(expr $num + 1)
						current_name=$(echo ${current_file} | cut -d"/" -f$numf)
						current_name="$(echo -e "${current_name}" | tr -d '[:space:]')"
						
						#Generamos el esquema generico soporta por kite
						generate_avsc_generic "$current_file" "$current_name"
						compare_schema "$current_file"
						
						print_log "Se Realizara operacion esquema?:$update_schema"
						
						if [ $update_schema -eq 1 ]; then
							generate_schema "$current_file"
						fi
						get_num_files_processed
						
						print_log "Mover esquema update_schema?:$update_schema."
						print_log "Mover esquema move_schemas?:$move_schemas."
						if [ $update_schema -eq 1 ] && [ $move_schemas -eq 0 ]; then
							move_schema_loaded "$current_file" "$current_name"
						else
							move_schema_no_loaded "$current_file" "$current_name"
						fi
					fi
					#Siempre procesamos el AVRO, porque aunque no haya cambio de esquema, los datos se deben insertar
					print_log "Invocar process_avro 3"
					process_avro
					
					echo
					echo
					echo
					echo
					echo
				done
			else
				print_log "No hay esquemas AVSC para procesar."
				#procesar solo AVROS
				print_log "Invocar process_avro 4"
				process_avro
				#Actualizamos el contador de la ejecucion

				print_log "2-Finalizo ejecucion:$executer"			
				print_log "2-Continua ejecucion:$executer"
				print_log "2-Total executions:$executions"
				if [ $executer -lt $executions ]; then
					print_log "Invocar read_avros_process 4"
					read_avros_process
					#Y enseguida llamamos al proceso que itera para procesar los demas esquemas
					read_schema_to_process
				fi
			fi
		else
			#Si la ejecucion anterior tiene mas de 0 intentos, se procesa solamente el avro
			print_log "Invocar process_avro 5"
			process_avro
			#Actualizamos el contador de la ejecucion
			print_log "Invocar read_avros_process 5"
			read_avros_process
			#Y enseguida llamamos al proceso que itera para procesar los demas esquemas
			read_schema_to_process
		fi
		#################################################
	fi
}

#Funcion para generar el esquema generico soportado por kite
generate_avsc_generic(){ #"$current_file" "$current_name"
	file_read="$(echo -e "${1}" | tr -d '[:space:]')"
	
	name_v1=$(echo ${2} | cut -d"." -f1)
	name_v1=$name_v1"_v1.avsc"
	
	cat "$file_read" | sed -r 's/"},/","default" : null},/g' | sed -r 's/"}]}/","default" : null}]}/g' > "$path_avsc$name_v1"
	
	if [ $a_id_table -ge 57 -a $a_id_table -le 87 ]; then
		cat "$file_read" | sed -r 's/"]},/"],"default" : null},/g' | sed -r 's/"]}]}/"],"default" : null}]}/g' > "$path_avsc$name_v1"
	fi
	
	rm -f "$file_read"
	mv "$path_avsc$name_v1" "$file_read"
}

#Funcion para comparar el esquema actual vs el ultimo esquema procesado con anterioridad
compare_schema(){
	current_avsc=$1
	if [ ! -d $path_back ]; then
		mkdir $path_back
	fi
	
	#Si no hay ningun esquema procesado en la historia, siempre será create
	#Si la tabla no existe, el comando será create
	if [ "$(kite-dataset info dataset:hive:"$schema/$table_name" | grep 'not found')" != "" ]; then
		export command_is="create"
		print_log ""
		print_log "No hay esquemas procesados:**********$command_is**********"
		export update_schema=1
	else
		#Si la tabla ya existe el comando será update
		get_num_files_processed
		count_processed=$num_processed
		print_log "count_processed:$count_processed"
	
		arch_hist=$path_back$count_processed".avsc"
		print_log ""
		print_log "Archivo historico:$arch_hist."

		print_log "Comparar"
		print_log "$arch_hist"
		print_log "$current_avsc"
		export dif_files=$(diff -q $arch_hist $current_avsc)
		print_log "Diferencia:$dif_files."

		if [ "$dif_files" == '' ]; then
				print_log ""
				print_log "No se detectaron cambios en los esquemas, no se hará ninguna operacion"
				export update_schema=0
			else
				export command_is="update"
				print_log ""
				print_log "Si hubo cambios:**********$command_is**********"
				export update_schema=1
		fi
	fi
}

#Funcion que genera el la tabla en base al esquema proporcionado
generate_schema(){	
	if [ "$environment" == "dev" ] ; then
		export debug="-v"
	else
		export debug="-v"
	fi
	
	print_log ""
	print_log "$command_is         $schema_load/$table_name"
	print_log "location            $location"
	print_log "schema              $1"
	print_log "partition_by        $path_config$json"
	
	if [ 0 -eq $run_without_cluster ]; then
		if [ "$command_is" == "create" ] ; then
			res_kite=$(kite-dataset $debug $command_is dataset:hive:"$schema_load/$table_name" --location $location --schema $1 --partition-by "$path_config$json" 1>"$path_temp"kite_"$command_is"_"$a_id_table".txt 2>>$name_file)
		else
			res_kite=$(kite-dataset $debug $command_is dataset:hive:"$schema_load/$table_name" --schema $1 1>"$path_temp"kite_"$command_is"_"$a_id_table".txt 2>>$name_file)
		fi
		res=$?
		res_kite=$(cat "$path_temp"kite_"$command_is"_"$a_id_table".txt)
	else
		res=0
		res_kite=0
	fi
	
	print_log ""
	print_log ""
	print_log "res_kite:$res_kite"
	print_log "$res_kite"
	print_log ""
	print_log ""
	
	export move_schemas=$res
	
	print_log "*****************************************************"
	print_log "2)Resultado de kite-dataset $debug $command_is $schema_load/$table_name"
	print_log $res
	print_log "*****************************************************"

	if [ $res -eq 1 ]; then
		print_log "Error al $command_is $schema_load/$table_name"
		update_events "$status_no_executed" 7 52
		update_events "$status_no_executed" 8 53
		
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 10: exit $res                          #"
		print_log "#----------------------------------------------------------------------------------#"
		exit $res
	else
		kite-dataset schema dataset:hive:"$schema_load/$table_name"
		res=$?
		print_log "*****************************************************"
		print_log "3)Resultado de kite-dataset schema $schema_load/$table_name"
		print_log $res
		print_log "*****************************************************"
	fi
}

#Funcion para obtener el numero de archivos en la carpeta de procesados
get_num_files_processed(){
	ls -tla "$path_back"*.avsc | awk -F' ' '{ print $9}' > "$path_temp"total_processed_"$id".txt
	wc -l "$path_temp"total_processed_"$id".txt > "$path_temp"count_processed_"$id".txt
	
	num_processed=$(tail -n 1 "$path_temp"count_processed_"$id".txt)
	export num_processed=$(echo ${num_processed} | cut -d" " -f1)
	print_log "Count carpeta procesados:$num_processed."
}

#Funcion para mover los archivos procesados e historicos
move_schema_loaded(){
	print_log "num_processed en move_schema:$num_processed"	
	let num_name=$(expr $num_processed + 1)
	name_moved="$num_name.avsc"
	export name_processed=$path_back$name_moved
	print_log "Mover:$1."
	print_log "A:$name_processed."
	mv "$1" "$name_processed"
}

#Funcion para mover los archivos NO procesados
move_schema_no_loaded(){
	path_not=$path_back"not_processed/"
	if [ ! -d $path_not ]; then
		mkdir $path_not
	fi
	print_log "Mover no procesado:$1."
	print_log "A no procesado:$path_not."
	mv "$1" "$path_not"
}

#Función que leera los avros a procesar en la carga
process_avro(){
	get_num_executions
	if [ $executions -ne 0 ]; then
		get_executer "$executer"
		
		executing=$result
		print_log "executing:$executing"
		id_e=$(echo ${executing} | cut -d" " -f1)
		table=$(echo ${executing} | cut -d" " -f2)
		datel=$(echo ${executing} | cut -d" " -f3)
		avro=$(echo ${executing} | cut -d" " -f4)
		
		print_log "id_e       $id_e"
		print_log "table      $table"
		print_log "datel      $datel"
		
		#TO-DO ambientar comando de spark
		getCommandSpark "$a_id_table" 0  #Con 0 recupera los parametros, con 1 recupera solo el comando de spark
		getCommandSpark "$a_id_table" 1  #Con 0 recupera los parametros, con 1 recupera solo el comando de spark
		
		get_num=$(grep -o "/" <<<"$avro" | wc -l)

		if [ "odk" != "$type_source" ]; then
			let num_name=$(expr $get_num + 1)
		else
			let num_name=$(expr $get_num + 0)
		fi
		file_name=$(echo $avro | awk -v c=$num_name -F'/' '{ print $c}')
		file_name="$(echo -e "${file_name}" | tr -d '[:space:]')"
		print_log "file_name:$file_name"
		
		command_exe=$(echo "${command//'{0}'/\"$schema_load.$table_name\"}")
		command_exe=$(echo "${command_exe//'{1}'/$avro}")
		command_exe=$(echo "${command_exe//'{2}'/$c_keys}")
		
		#if [ $a_id_table -eq 45 ] || [ $a_id_table -eq 1000 ]; then
		if [ "odk" == "$type_source" ]; then
			command_exe=$(echo "${command_exe//'{3}'/$c_avro_cifras}")
			#echo "$ctl_sid" > "$path_temp"flags_"$a_id_table".txt
		else
			command_exe=$(echo "${command_exe//'{3}'/$c_avro_cifras$file_name}")
		fi

		t_cifras="$schema.$table_statistics"
		command_exe=$(echo "${command_exe//'{4}'/$t_cifras}")
		command_exe=$(echo "${command_exe//'{5}'/$c_type_load}")
		command_exe=$(echo "${command_exe//'{6}'/$c_num_partitions}")
		command_exe=$(echo "${command_exe//'{7}'/\"Delta_SPARK-$schema_load.$table_name\"}")
		
		ctl_fields="$ctl_sid,$a_id_table,$ctl_eid"
		command_exe=$(echo "${command_exe//'{8}'/$ctl_fields}")
		
		print_log "flow_continue:$flow_continue"
		#Verificamos si el flujo es ejecución completa enviamos parámetro 1 para que Spark ejecute las 2 fases: datos y cifras
		if [ "phase_all" == "$flow_continue" -o "7" == "$flow_continue" ]; then
			command_exe=$(echo "${command_exe//'{9}'/1}")
		else 
			if [ "8" == "$flow_continue" ]; then
				#Si no, sólo ejecutar cifras
				command_exe=$(echo "${command_exe//'{9}'/0}")
			fi
		fi
		
		#actualizar el campo de date_load inicio de ejecución
		hr_inicio=$(date '+%F %T')
		query_update_time_executer="update $schema_config.$table_execution set start_execution='$hr_inicio', status_ingestion='$status_processing', command='$command_exe', updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and id_ingestion_file = $executer and id_group = $id_group "
		execute_querys "$query_update_time_executer" "start_execution" 5 "$intentos"
		start_execution=${response_f[start_execution]}
			
		print_log "*****************************************************"
		print_log "*****************************************************"
		print_log "Avro $executer a procesar:$avro. *********"
		print_log "Comando sera:"
		print_log "$command_exe"
		print_log "*****************************************************"
		print_log "*****************************************************"
		
		print_log ""
		print_log ""
		print_log "Ejecutando componente de Spark, esperar unos minutos..."
		print_log "En caso de error consultar el archivo: $name_file"
		print_log ""
		print_log ""
		
		if [ 1 -eq $run_without_cluster ]; then
			res=0
		else
			res_spark=$(eval "$command_exe" 1>>$name_file 2>>$name_file)
			res=$?
		fi
		
		print_log ""
		print_log ""
		print_log "-----------------------------------------------------"
		print_log "------  Resultado Avro $executer:$res.  -------------"
		print_log "-----------------------------------------------------"
		
		if [ $res -eq 0 ]; then
			#termino correctamente la operacion
			print_log "Resultado:$res"
						
			#Eliminar el avro de datos procesado
			print_log "Borraremos:$avro"
			get_del=$(grep -o ".avro" <<<"$avro" | wc -l)
			print_log "get_del:$get_del"
			
			if [ 0 -eq $run_without_cluster ]; then			
				if [ $get_del -eq 0 ]; then
					print_log "Borrar carpeta $avro"
					#TO-DO descomentar esta linea
					hdfs dfs -rm -r $avro
				else
					print_log "Borrar archivo $avro"
					#TO-DO descomentar esta linea
					hdfs dfs -rm $avro
					print_log "Borrar archivo $c_avro_cifras$file_name"
					hdfs dfs -rm $c_avro_cifras$file_name
				fi
			fi
			
			hr_fin=$(date '+%F %T')
			query_update_time_end_executer="update $schema_config.$table_execution set end_execution='$hr_fin', status_ingestion='$status_executed', updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and id_ingestion_file = $executer and id_group = $id_group "
			execute_querys "$query_update_time_end_executer" "update_end" 6 "$intentos"
			update_end=${response_f[update_end]}
			
			#Actualizar executer
			print_log "Finalizo ejecucion:$executer"			
			let executer=$(expr $executer + 1 )
			print_log "Continua ejecucion:$executer"
			print_log "Total executions:$executions"
			if [ $executer -gt $executions ]; then
				#Actualizamos el estatus del evento
				update_events "$status_executed" 7 50
				update_events "$status_executed" 8 51
				notification_end
			fi
		else
			query_update_attempts="update $schema_config.$table_execution set attempts=cast( (attempts + 1) as int), status_ingestion='$status_no_executed', updated_by='$user', updated_on=now() where ctl_tid=$a_id_table and dateload=$date_load and id_ingestion_file = $executer and id_group = $id_group "
			execute_querys "$query_update_attempts" "attempts" 16 "$intentos"
			attempts=${response_f[attempts]}
			
			update_events "$status_no_executed" 7 50
			update_events "$status_no_executed" 8 51
			
			print_log "Hubo un error en el procesamiento. Salida $res"
			print_log "#----------------------------------------------------------------------------------#"
			print_log "#                         Punto de control 11: exit $res                           #"
			print_log "#----------------------------------------------------------------------------------#"
			exit $res;
		fi
	fi
}

# Función para obtener el número de ejecucioes que se deben procesar
get_num_executions(){
	print_log "Obteniendo # de ejecuciones..."
	query_count_executions="select count(*) as total from $schema_config.$table_execution where ctl_tid=$a_id_table and dateload=$date_load and id_group = $id_group "
	execute_querys "$query_count_executions" "executions" 3 "$intentos" ""
	executions=${response_f[executions]}
	print_log "# Ejecuciones:$executions."
	print_log "*****************************************************"
	print_log ""
	print_log ""
}

#Funcion para obtener el número de ejecucion que se debe procesar
get_executer(){
	print_log "Obteniendo ejecucion #$1..."
	query_get_executer="select id_ingestion_file, ctl_tid, dateload, avro_name, status_ingestion from $schema_config.$table_execution where ctl_tid=$a_id_table and dateload=$date_load and id_ingestion_file = $1 and id_group = $id_group "
	execute_querys "$query_get_executer" "result" 4 "$intentos"
	result=${response_f[result]}
}

#Funcion para obtener de la base de datos los parametros para ejecutar el componente de Spark
getCommandSpark(){
	type_query=$2
	
	if [ $type_query -eq 0 ]; then
		get_command="select t.table_name,c.path_avro_all,c.key_columns,c.path_avro_cifras,c.type_load,c.number_partitions from $schema_config.$table_config c inner join $schema_config.$table_names t on c.ctl_tid = t.ctl_tid where c.ctl_tid=$1 and t.table_status='$status_active' and lower(c.environment_config) = '$environment' "
		execute_querys "$get_command" "command" 11 "$intentos"
		command=${response_f[command]}
			
		c_table=$(echo ${command} | cut -d" " -f1)
		c_avro_data=$(echo ${command} | cut -d" " -f2)
		c_keys=$(echo ${command} | cut -d" " -f3)
		c_avro_cifras=$(echo ${command} | cut -d" " -f4)
		c_type_load=$(echo ${command} | cut -d" " -f5)
		c_num_partitions=$(echo ${command} | cut -d" " -f6)
		
		export c_table="$(echo -e "${c_table}" | tr -d '[:space:]')"
		export c_avro_data="$(echo -e "${c_avro_data}" | tr -d '[:space:]')"
		export c_keys="$(echo -e "${c_keys}" | tr -d '[:space:]')"
		export c_avro_cifras="$(echo -e "${c_avro_cifras}" | tr -d '[:space:]')"
		export c_type_load="$(echo -e "${c_type_load}" | tr -d '[:space:]')"
		export c_num_partitions="$(echo -e "${c_num_partitions}" | tr -d '[:space:]')"
	else
		get_command="select c.command_spark from $schema_config.$table_config c inner join $schema_config.$table_names t on c.ctl_tid = t.ctl_tid where c.ctl_tid=$1 and t.table_status='$status_active' and lower(c.environment_config) = '$environment' "
		execute_querys "$get_command" "command" 11 "$intentos"
		command=${response_f[command]}
	fi
}

notification_end(){
	echo $(date)
	
	if [ "phase_all" == "$flow_continue" -o "10" != "$flow_continue" ]; then
		print_log "Notificar la finalización de la carga mediante correo electrónico"
		envia_cifras
		compute_stats
	else
		compute_stats
	fi
	
	print_log "Fin de compute stats en notification_end"
	print_log "type_source          $type_source"
	print_log "is_referenced        $is_referenced"
	print_log "was_referenced     $was_referenced"
	
	if [ "odk" == "$type_source" ]; then
		invoke_odk_shell
		print_log "Fin llamado función: invoke_odk_shell"
	fi
	
	if [ 1 -eq $is_referenced -o 1 -eq $was_referenced ]; then
		generate_eid_references $a_id_table
	else
		insert_eid_references $a_id_table $ctl_eid $ctl_eid
	fi
}

#Funciona para actualizar las estadisticas de la tabla
compute_stats(){
	print_log ""
	print_log ""
	print_log "Actualizar las estadísticas de la tabla"
	
	upsert_events 10 "$status_processing" 54
	
	query_invalidate "$schema_load" "$table_name"
	query_update_compute="compute stats $schema_load.$table_name"
	execute_querys_without_exit "$query_update_compute" "update_stats" 19 "$intentos" "$schema_load" ""
	update_stats=${response_f[update_stats]}
	print_log "resultado stats:$update_stats"
	
	if [ "" == "$update_stats" ]; then
		upsert_events 10 "$status_no_executed" 55
	else
		upsert_events 10 "$status_executed" 55
		write_status_done $a_id_table
	fi
}

#Funcion para enviar las cifras de control de la carga
envia_cifras(){
	if [ -f "$path_temp"cifras_"$id".txt ]; then
		print_log "Archivo temporal "$path_temp"cifras_"$id".txt existente, se borrará"
		rm "$path_temp"cifras_"$id".txt
	fi
	
	upsert_events 9 "$status_processing" 52
	
	query_invalidate "$schema" "$table_statistics"
	print_log "Obtener conteo de cifras de control..."
	query_cifras="select count(*) from $schema.$table_statistics c inner join ( select ctl_tid, max(dateload) as dateload from $schema.$table_statistics where ctl_tid=$a_id_table group by ctl_tid ) cm on c.ctl_tid = cm.ctl_tid and c.dateload = cm.dateload "
	execute_querys_without_exit "$query_cifras" "cifras" 14 "$intentos" "$schema" ""
	export cifras=${response_f[cifras]}	
	print_log "valor retornado Query_14:$cifras."
	
	if [ "" != "$cifras" ]; then
		if [ $cifras -ne 0 ]; then
			print_log "Enviar correo con los conteos"
			
			obtiene_cifras
			export cifras_mail=$(cat "$path_temp"tabla_cifras_"$id".txt)
			put_parameters_oozie_mail
			invoca_oozie_cifras
			upsert_events 9 "$status_executed" 53
		else
			#Validar que se hará en el caso de que no se encuentre las cifras de control
			#En error regresa vacio:valor retornado Query_14:.
			print_log "No se encontraron cifras de control..."
			upsert_events 9 "$status_no_executed" 53
		fi
	else
		print_log "No se encontraron cifras de control..."
		upsert_events 9 "$status_no_executed" 53
	fi
}

#Funciona para armar la tabla con los conteos de las cifras de control cargadas
obtiene_cifras(){
	cat $path_sql$environment"_consulta_cifras.sql" | sed 's/$a_id_table/'${a_id_table}'/g' | sed 's/$schema/'${schema}'/g' | sed 's/$table_statistics/'${table_statistics}'/g'| sed 's/$table_names/'${table_names}'/g'| sed 's/$table_source/'${table_source}'/g' | sed 's/$config/'${schema_config}'/g'> "$path_sql$environment"_consulta_cifras2_"$id".sql
	execute_querys_without_exit "" "query_cifras" 15 "$intentos" "$schema" ""

	echo  "<table border=1 width=600px style='font-family:Arial; font-size:14px'><caption>Reporte de cifras de control</caption><tr style='background-color: #87CEEB; color:#FFFFFF;'><th>" "Tabla" "</th><th>" "Desc_tabla " "</th><th>" "Fecha_archivo" "</th><th>" "Nombre_archivo" "</th><th>" "Total_archivo" "</th><th>" "Total_insertados" "</th><th>" "Fecha_carga_dlk" "</th></tr>"  > "$path_temp"tabla_cifras_"$id".txt
	result_tail=$(tail -n +4 "$path_temp"resultado_cifras_"$id".txt | grep -v "+")
	print_log "result_tail:$result_tail."
	if [ "$result_tail" != "" ]; then
		tail -n +4 "$path_temp"resultado_cifras_"$id".txt | grep -v "+" | sed 's/|//g' |  sed 's/      / /g' >> "$path_temp"tabla_cifras_"$id".txt
		print_log "Tail con +"
	else
		tail -n +4 "$path_temp"resultado_cifras_"$id".txt | grep -v "-" | sed 's/|//g' |  sed 's/      / /g' >> "$path_temp"tabla_cifras_"$id".txt
		print_log "Tail con -"
	fi
	echo -e "</table>" >> "$path_temp"tabla_cifras_"$id".txt
}

#Funcion para ejecutar un invalidate metadata
query_invalidate(){
	print_log "Actualizamos la tabla:$1.$2 ..."
	invalidate_query="refresh $1.$2"
	execute_querys_without_exit "$invalidate_query" "invalidate_query" 18 "$intentos" "$1" ""
	export invalidate_query=${response_f[invalidate_query]}
}

#Funcion para respaldar los archivo de ODK
backup_odk(){
	if [ "odk" == "$type_source" ]; then
		#Si ya existe la ruta no crearla
		#creamos la carpeta backup del dia
		print_log "Crear ruta:$path_backup_file$date_load"
		hdfs dfs -mkdir "$path_backup_file$date_load"
		
		#respaldamos la informacion que llega en el hdfs
		print_log "Copiar de:$path_odk_info"
		print_log "A:$path_backup_file$date_load/"
		hdfs dfs -cp "$path_odk_info"* "$path_backup_file$date_load"/
	fi
}

#Funcion para respaldar los archivo de ODK
copy_data_odk(){
	if [ "odk" == "$type_source" ]; then
		#limpiamos nuestra ruta de trabajo
		print_log "Borramos info pasada de:$path_avro"
		hdfs dfs -rm "$path_avro"
		
		#creamos la carpeta del dia para ejecucion
		print_log "Crear2 ruta:$path_avro$date_load"
		hdfs dfs -mkdir "$path_avro$date_load"
		
		#copiamos la informacion a la ruta de trabajo
		print_log "Copiar2 de:$path_odk_info"
		print_log "A:$path_avro$date_load/"
		hdfs dfs -cp "$path_odk_info"* "$path_avro$date_load"/
	fi
}

clean_odk(){
	# Se limpia solo si y es el proceo de odk deltas
	#ya que es el segundo en correr, primero corre odk full
	if [ "odk" == "$type_source" ]; then
		#limpiamos la información que ya ha sido procesada
		print_log "Borramos info que ya se proceso:$path_odk_info"
		hdfs dfs -rm "$path_odk_info"*
	fi
}

#----------------------------------------------------------------------------------#
#								Funcion principal del shell						   #
#----------------------------------------------------------------------------------#
process_transformation(){
	print_log "flow_continue:$flow_continue"
	if [ "phase_all" == "$flow_continue" -o "5" == "$flow_continue" -o "7" == "$flow_continue" -o "8" == "$flow_continue" ]; then
		get_file_process
		print_log "*****************************************************"
		backup_odk
		copy_data_odk
		print_log "*****************************************************"
		print_log "Invocar read_avros_process 6"
		read_avros_process
		print_log "*****************************************************"
		read_schema_to_process
		print_log "*****************************************************"
		clean_odk
		print_log "*****************************************************"
	else 
		if [ "9" == "$flow_continue" -o "10" == "$flow_continue" ]; then
			get_file_process
			notification_end
		else
			if [ "11" == "$flow_continue" -a "odk" == "$type_source" ]; then
				invoke_odk_shell
			fi
		fi
	fi
}

process_transformation
