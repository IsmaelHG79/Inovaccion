#set -xv
#!/bin/bash
#------------------------------------------------------------------------------------------------------------#
#	Nombre:		rci_ingesta_generacion_avro.sh                                             			 		 #
#	Objetivo: 	Ejecuta comandos de kite para poder generar los schemas avro.							     #
#	Autor:		ejesus				                                                                         #
#	Vía de ejecución: ksh/Control M (Kernel ksh)                                                           	 #
#	Fecha:		04 de Noviembre de 2019  	                                                           		 #
#	Area:		Datalake AT&T											                                     #
#	Salida:		Dataset en el hdfs de Haddop															     #
#------------------------------------------------------------------------------------------------------------#

if [ $# -lt 1 ]
	then
		echo '--------------------------------------------------------------'
		echo "Error: parametro"
		echo "usage: sh $(basename $0) num_archivo_procesar"
		echo '--------------------------------------------------------------'
	exit 1
fi

export type_execution=$1
export a_type_execution=$1
export impala_conf="balancer.attdatalake.com.mx -d default -k --ssl --ca_cert=/opt/cloudera/security/ca-certs/CertToolkitCA.pem"

export HOME_SC=/home/raw_rci/attdlkrci/
export path_properties=$HOME_SC"config/"
export enviroment="pro"
export group_exec="raw_rci"
export file_properties=$path_properties$enviroment"_rci_ingesta_generacion_avro.properties"
declare -A properties

#Agregamos las lineas para poder utilizar el log
export path_log4jadc=$HOME_SC"shells"
. $path_log4jadc/log4j_attdlkrci.sh 1 'rci_ingesta_generacion_avro' "$enviroment" "$HOME_SC" "$group_exec"
create_dir_logs

#Agregamos las lineas para poder utilizar el archivo utils
. $path_log4jadc/utils.sh "$file_properties"

#----------------------------------------------------------------------------------#
#	Variables de ambiente para obtener parametros necesarios para la ejecucion	   #
#----------------------------------------------------------------------------------#
export ftmp="tmp/"
export ruta_tmp=$HOME_SC$ftmp
export fsql="sql/"
export ruta_sql=$HOME_SC$fsql
export ext_processed="_processed"
export processed_hist="historico/"
executer=0

# Variables para poder reintentar ejecutar una consulta en caso de desconexión
export intentos=1
export max_intentos=3
declare -A response

#----------------------------------------------------------------------------------#
#								Area de funciones								   #
#----------------------------------------------------------------------------------#
# Funcion que obtiene la fecha de ejecución del proceso
getDate() {		
	FECHA=$(date +%Y%m%d)
	print_log "Fecha entera obtenida: $FECHA"
}

# Funcion para determinar que layout se va a procesar
get_file_process(){
	schema=${properties[esquema_tablas_rci]}
	schema="$(echo -e "${schema}" | tr -d '[:space:]')"
	print_log "$schema."
	
	schema_config=${properties[esquema_tablas_config]}
	schema_config="$(echo -e "${schema_config}" | tr -d '[:space:]')"
	print_log "$schema_config."
	
	tbl_execute=${properties[tabla_ejecuciones]}
	tbl_execute="$(echo -e "${tbl_execute}" | tr -d '[:space:]')"
	print_log "$tbl_execute."
	
	tabla_config=${properties[tabla_config]}
	tabla_config="$(echo -e "${tabla_config}" | tr -d '[:space:]')"
	print_log "$tabla_config."
	
	tabla_cifras=${properties[tabla_cifras]}
	tabla_cifras="$(echo -e "${tabla_cifras}" | tr -d '[:space:]')"
	print_log "$tabla_cifras."
	
	path_cifras=${properties[path_cifras]}
	path_cifras="$(echo -e "${path_cifras}" | tr -d '[:space:]')"
	print_log "$path_cifras."
	print_log "*****************************************************"
	
	query_get_param="select path_avsc, table_name, path_hdfs, path_backup, ban_process_all, path_avsc_all, path_avro_all, id_source, json_partition from $schema_config.$tabla_config where id_source=$a_type_execution and status=1"
	execute_querys "$query_get_param" "params" 10 "$intentos"
	params=${response[params]}	
	#print_log "valor retornado Query_10:$params."
	
	export file_process=$(echo ${params} | cut -d" " -f1)
	export table_name=$(echo ${params} | cut -d" " -f2)
	export location=$(echo ${params} | cut -d" " -f3)
	export path_back=$(echo ${params} | cut -d" " -f4)
	export process_all=$(echo ${params} | cut -d" " -f5)
	export path_avsc=$(echo ${params} | cut -d" " -f6)
	export path_avro=$(echo ${params} | cut -d" " -f7)
	export id=$(echo ${params} | cut -d" " -f8)
	export json=$(echo ${params} | cut -d" " -f9)
	
	export file_process="$(echo -e "${file_process}" | tr -d '[:space:]')"
	export table_name="$(echo -e "${table_name}" | tr -d '[:space:]')"
	export location="$(echo -e "${location}" | tr -d '[:space:]')"
	export path_back="$(echo -e "${path_back}" | tr -d '[:space:]')"
	export process_all="$(echo -e "${process_all}" | tr -d '[:space:]')"
	export path_avsc="$(echo -e "${path_avsc}" | tr -d '[:space:]')"
	export path_avro="$(echo -e "${path_avro}" | tr -d '[:space:]')"
	export id="$(echo -e "${id}" | tr -d '[:space:]')"
	export json="$(echo -e "${json}" | tr -d '[:space:]')"
	

	print_log "Se creara tabla: $table_name"
	print_log "Location es: $location"
	print_log "Path respaldo: $path_back"
	print_log "Procesar todo?:$process_all."
	print_log "Path esquemas: $path_avsc"
	print_log "Path avros: $path_avro"
	print_log "Id_source: $id"
	print_log "Json: $json"
}

# Funcion que verifica si procesaremos 1 esquemas o mas, y lee el esquema(s) a procesar
read_schema_to_process(){
	#Creamos ruta temporal que usaremos para almacenar archivos de control
	mkdir $ruta_tmp
	
	#Evaluamos si debemos leer varios esquemas o solo 1
	if [ $process_all -eq 1 ]; then
	
		#Validar si fallo el avro anterior, si fallo, no debemos procesar otro esquema, solo procesamos el avro
		#Si no fallo, procesar el siguiente avro
		
		query_get_attempts="select attempts from $schema_config.$tbl_execute where table_name='$table_name' and dateload=$FECHA and id_execution = $executer "
		execute_querys "$query_get_attempts" "get_attempts" 17 "$intentos"
		get_attempts=${response[get_attempts]}
		#print_log "valor retornado Query_17:$get_attempts."
		
		if [ $get_attempts -eq 0 ]; then
			#Tomar el siguiente esquema a procesar
			ls -r "$path_avsc"*.avsc | awk -F' ' '{ print $1}' > "$ruta_tmp"list_files_avsc.txt
			
			#Obtenemos el numero de lineas que contiene el archivo, para saber cuantos esquemas son los que generaron
			wc -l "$ruta_tmp"list_files_avsc.txt | sed 's/${path_file}//' > "$ruta_tmp"total_archivos.txt
			num_files=$(tail -n 1 "$ruta_tmp"total_archivos.txt)
			export num_files=$(echo ${num_files} | cut -d" " -f1)
			print_log "Total archivos a procesar:$num_files."
				
			if [ $num_files -ne 0 ]; then
				#Ccomenzamos el ciclo de procesamiento de N esquenas
				for i in $( eval echo {1..$num_files} )
				do	
					#Obtenemos el esquema a procesar
					current_file=$(tail -n $i "$ruta_tmp"list_files_avsc.txt)
					current_file=$(echo ${current_file} | cut -d" " -f1) # Obtiene el nombre del archivo
					current_file="$(echo -e "${current_file}" | tr -d '[:space:]')"
					echo
					echo
					echo					
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

					process_avro
					
					echo
					echo
					echo
					echo
					echo
				done
			else
				print_log "No hay esquemas AVSC para procesar."
			fi
		else
			#Si la ejecucion anterior tiene mas de 0 intentos, se procesa solamente el avro
			process_avro
			#Actualizamos el contador de la ejecucion
			read_avros_process
			#Y enseguida llamamos al proceso que itera para procesar los demas esquemas
			read_schema_to_process
		fi
	else
		print_log "Procesar solo 1 esquema..."
	fi
}

#Funcion para generar el esquema generico soportado por kite
generate_avsc_generic(){ #"$current_file" "$current_name"
	file_read="$(echo -e "${1}" | tr -d '[:space:]')"
	
	name_v1=$(echo ${2} | cut -d"." -f1)
	name_v1=$name_v1"_v1.avsc"
	
	cat "$file_read" | sed -r 's/"},/","default" : null},/g' | sed -r 's/"}]}/","default" : null}]}/g' > "$path_avsc$name_v1"
	
	if [ $a_type_execution -ge 57 -a $a_type_execution -le 87 ]; then
		cat "$file_read" | sed -r 's/"]},/"],"default" : null},/g' | sed -r 's/"]}]}/"],"default" : null}]}/g' > "$path_avsc$name_v1"
	fi
	
	rm -f "$file_read"
	mv "$path_avsc$name_v1" "$file_read"
}

#Funcion para comparar el esquema actual vs el ultimo esquema procesado con anterioridad
compare_schema(){
	current_avsc=$1
	mkdir $path_back
	
	
	get_num_files_processed
	count_processed=$num_processed
	print_log "count_processed:$count_processed"

	#Si no hay ningun esquema procesado en la historia, siempre será create
	if [ $count_processed -eq 0 ]; then
		export command_is="create"
		print_log "No hay esquemas procesados:**********$command_is**********"
		export update_schema=1
	else
		arch_hist=$path_back$count_processed".avsc"
		print_log "Archivo historico:$arch_hist."

		if [ "$arch_hist" == '' ]; then
			export command_is="create"
			print_log "No hay historico:**********$command_is**********"
			export update_schema=1
		else
			print_log "Comparar"
			print_log "$arch_hist"
			print_log "$current_avsc"
			export dif_files=$(diff -q $arch_hist $current_avsc)
			print_log "Diferencia:$dif_files."

			if [ "$dif_files" == '' ]; then
					print_log "No se detectaron cambios en los esquemas, no se hará ninguna operacion"
					export update_schema=0
				else
					export command_is="update"
					print_log "Si hubo cambios:**********$command_is**********"
					export update_schema=1
			fi
		fi	
	fi
}

#Funcion que genera el la tabla en base al esquema proporcionado
generate_schema(){	
	if [ "$enviroment" == "des" ] ; then
		export debug="-v"
	else
		export debug="-v"
	fi
	
	print_log "$schema/$table_name"
				
	if [ "$command_is" == "create" ] ; then
		#kite-dataset $debug $command_is dataset:hive:"$schema/$table_name" --location $location --schema $1 --partition-by "${properties[json_partition_config]}"
		kite-dataset $debug $command_is dataset:hive:"$schema/$table_name" --location $location --schema $1 --partition-by "$json"
	else
		kite-dataset $debug $command_is dataset:hive:"$schema/$table_name" --schema $1
	fi
	
	res=$?
	export move_schemas=$res
	print_log "move_schemas fue:$move_schemas"
	
	print_log "*****************************************************"
	print_log "2)Resultado de kite-dataset $debug $command_is $table_name"
	print_log $res
	print_log "*****************************************************"

	if [ $res -eq 1 ]; then
		print_log "Error al $command_is $table_name"
		exit $res
	fi
	
	kite-dataset schema dataset:hive:"$schema/$table_name"
	res=$?
	print_log "*****************************************************"
	print_log "3)Resultado de kite-dataset schema $table_name"
	print_log $res
	print_log "*****************************************************"
}

#Funcion para obtener el numero de archivos en la carpeta de procesados
get_num_files_processed(){
	ls -tla "$path_back"*.avsc | awk -F' ' '{ print $9}' > "$ruta_tmp"total_processed.txt
	wc -l "$ruta_tmp"total_processed.txt > "$ruta_tmp"count_processed.txt
	
	num_processed=$(tail -n 1 "$ruta_tmp"count_processed.txt)
	export num_processed=$(echo ${num_processed} | cut -d" " -f1)
	print_log "Count carpeta procesados:$num_processed."
}

#Funcion para obtener el numero de archivos en la carpeta de procesados historicos
get_num_files_processed_hist(){
	ls -tla "$path_back$processed_hist"*.avsc | awk -F' ' '{ print $9}' > "$ruta_tmp"total_processed_hist.txt
	wc -l "$ruta_tmp"total_processed_hist.txt | sed 's/${path_back}//' > "$ruta_tmp"count_processed_hist.txt
	
	num_processed_hist=$(tail -n 1 "$ruta_tmp"count_processed_hist.txt)
	export num_processed_hist=$(echo ${num_processed_hist} | cut -d" " -f1)
	print_log "Count carpeta procesados historico:$num_processed_hist"
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
	mkdir $path_not
	print_log "Mover no procesado:$1."
	print_log "A no procesado:$path_not."
	mv "$1" "$path_not"
}

#Funcion para procesar N avros localizados en una carpeta
read_avros_process(){
	#Creamos ruta temporal que usaremos para almacenar archivos de conttrol
	mkdir $ruta_tmp
	
	get_id_executer
	
	if [ "$executer" == "NULL" ]; then
		reiniciar=1
		executer=1
	else
		reiniciar=0
	fi

	print_log "Reiniciar flujo? $reiniciar"
	if [ $reiniciar -eq 1 ]; then
		delete_executions
		generate_executions			
	fi
	print_log "----------------------------------------------------------------------executer:$executer"
}

#Función que obtiene el id de la primer ejecución a procesar.
get_id_executer(){
	print_log "Obteniendo primer ejecucion a procesar..."
	get_id_executer="SELECT min(id_execution) as id_execution FROM $schema_config.$tbl_execute where table_name='$table_name' and dateload=$FECHA and status != 1 "
	execute_querys "$get_id_executer" "executer" 1 "$intentos"
	executer=${response[executer]}	
	print_log "valor retornado Query_1:$executer."
	
	rm $ruta_tmp"id_ejecucion.txt"
	echo -e $executer | sed 's/id_execution//' | sed 's/-//g' | sed 's/ //g' > $ruta_tmp"id_ejecucion.txt"
	executer=$(cat $ruta_tmp"id_ejecucion.txt")
	print_log "executer:$executer."
}

# Funcion para eliminar los registros del día de la ejecución por tabla
delete_executions(){
	print_log "Eliminaremos los registros del dia"
	query_delete="delete from $schema_config.$tbl_execute where table_name='$table_name' and dateload=$FECHA"
	execute_querys "$query_delete" "query_deletes" 12 "$intentos"
	query_deletes=${response[query_deletes]}	
	print_log "valor retornado Query_12:$query_deletes."
}

#Funcion que inserta el número de ejecuciones para procesar el lote de archivos avro.
generate_executions(){
	id_executer=1
	
	#Evaluamos si debemos leer varios esquemas o solo 1
	if [ $process_all -eq 1 ]; then
		hdfs dfs -ls -C $path_avro > "$ruta_tmp"list_avro.txt
		
		export num_files_avro=$(wc -l "$ruta_tmp"list_avro.txt | awk -F' ' '{ print $1}')
		print_log "Total avros a procesar:$num_files_avro."
			
		cont_inverse=$num_files_avro
		if [ $num_files_avro -ne 0 ]; then
			#Ccomenzamos el ciclo de procesamiento de N archivo avros
			for i in $( eval echo {1..$num_files_avro} )
			do	
				#Obtenemos el avro a procesar
				current_file=$(tail -n $i "$ruta_tmp"list_avro.txt)
				current_file=$(echo ${current_file} | cut -d" " -f1) # Obtiene el nombre del archivo
				current_file="$(echo -e "${current_file}" | tr -d '[:space:]')"

				print_log "********* Crear ejecucion:$cont_inverse con  archivo:$current_file. *********"
								
				#Insertar en la tabla de ejecuciones las N ejecuciones identificadas
				query_insert_execution="INSERT INTO TABLE $schema_config.$tbl_execute ( id_execution, table_name, dateload, avro_name, start_execution, end_execution, status, command, id_application, attempts ) VALUES ($cont_inverse, '$table_name', $FECHA, '$current_file', NULL AS start_execution, NULL AS end_execution, 0, '' as command, '' as id_application,0)"
				execute_querys "$query_insert_execution" "insert_execution" 13 "$intentos"
				insert_execution=${response[insert_execution]}	
				print_log "valor retornado Query_13:$insert_execution."
				id_executer=$(expr $id_executer + 1)
				cont_inverse=$(expr $cont_inverse - 1)
			done
		else
			print_log "No hay avros a procesar."
			exit 1
		fi
	else
		print_log "Procesar solo 1 avro..."
		exit 1
	fi
}

process_avro(){
	get_num_executions
	if [ $executions -ne 0 ]; then
		get_executer "$executer"
		
		executing=$result
		print_log "executing:$executing"
		id=$(echo ${executing} | cut -d" " -f1)
		table=$(echo ${executing} | cut -d" " -f2)
		datel=$(echo ${executing} | cut -d" " -f3)
		avro=$(echo ${executing} | cut -d" " -f4)
		
		print_log "id:$id."
		print_log "table:$table."
		print_log "datel:$datel."
		
		#TO-DO ambientar comando de spark
		getCommandSpark "$a_type_execution" 0  #Con 0 recupera los parametros, con 1 recupera solo el comando de spark
		getCommandSpark "$a_type_execution" 1  #Con 0 recupera los parametros, con 1 recupera solo el comando de spark
		
		get_num=$(grep -o "/" <<<"$avro" | wc -l)
		let num_name=$(expr $get_num + 1)
		print_log "aunnn hay loggg 3"
		file_name=$(echo $avro | awk -v c=$num_name -F'/' '{ print $c}')
		print_log "aunnn hay loggg 4"
		file_name="$(echo -e "${file_name}" | tr -d '[:space:]')"
		print_log "aunnn hay loggg 5"
		print_log "file_name:$file_name"
		
		command_exe=$(echo "${command//'{0}'/\"$schema.$c_table\"}")
		command_exe=$(echo "${command_exe//'{1}'/$avro}")
		command_exe=$(echo "${command_exe//'{2}'/$c_keys}")
		
		#if [ $a_type_execution -ge 45 -a $a_type_execution -le 45 ]; then		
		if [ $a_type_execution -eq 45 ]; then
			command_exe=$(echo "${command_exe//'{3}'/$FECHA}")
		else
			command_exe=$(echo "${command_exe//'{3}'/$c_avro_cifras$file_name}")
		fi
		command_exe=$(echo "${command_exe//'{4}'/$c_write_cifras}")
		command_exe=$(echo "${command_exe//'{5}'/$c_type_load}")
		command_exe=$(echo "${command_exe//'{6}'/$c_num_partitions}")
		command_exe=$(echo "${command_exe//'{7}'/\"Delta_SPARK-$schema.$c_table\"}")
		
		#actualizar el campo de fecha inicio de ejecución
		hr_inicio=$(date '+%F %T')		
		query_update_time_executer="UPDATE $schema_config.$tbl_execute SET start_execution='$hr_inicio', command='$command_exe' where table_name='$table_name' and dateload=$FECHA and id_execution = $executer "
		execute_querys "$query_update_time_executer" "start_execution" 5 "$intentos"
		start_execution=${response[start_execution]}	
		#print_log "valor retornado Query_5:$start_execution."
			
		print_log "*****************************************************"
		print_log "*****************************************************"
		print_log "Avro $executer a procesar:$avro. *********"
		print_log "Comando sera:$command_exe"
		print_log "*****************************************************"
		print_log "*****************************************************"
		
		eval "$command_exe"
		res=$?
		
		print_log "-----------------------------------------------------"
		print_log "------  Resultado Avro $executer:$res.  -------------"
		print_log "-----------------------------------------------------"
		
		id=$(echo $(yarn application -list -appTypes SPARK | grep "$c_table") | cut -d" " -f1)
		print_log "applicationId:$id"
		
		if [ $res -eq 0 ]; then
			#termino correctamente la operacion
			print_log "Resultado:$res"
			
			#TO-DO
			#Mover el archivo avro de las cifras complementadas a la ruta de la tabla de cifras			
			print_log "Moveremos de:$c_write_cifras*.avro"
			print_log "Moveremos a:$path_cifras/$file_name."
			#print_log "Moveremos a:$path_cifras"
			hdfs dfs -rm "$path_cifras/$file_name"
			
			hdfs dfs -mv $c_write_cifras"*.avro" "$path_cifras/$file_name"
			#hdfs dfs -mv $c_write_cifras"*.avro" "$path_cifras"
			
			#Eliminar el avro de datos procesado
			print_log "Borraremos:$avro"
			hdfs dfs -rm $avro
			
			hr_fin=$(date '+%F %T')
			query_update_time_end_executer="UPDATE $schema_config.$tbl_execute SET end_execution='$hr_fin', status=1 where table_name='$table_name' and dateload=$FECHA and id_execution = $executer "
			execute_querys "$query_update_time_end_executer" "update_end" 6 "$intentos"
			update_end=${response[update_end]}
			#print_log "valor retornado Query_6:$update_end."
			
			#Actualizar executer
			print_log "Finalizo ejecucion:$executer"			
			let executer=$(expr $executer + 1 )
			print_log "Continua ejecucion:$executer"
			print_log "Total executions:$executions"
			if [ $executer -gt $executions ]; then
				echo $(date)
				print_log "Notificar la finalización de la carga"
				envia_cifras
				compute_stats
			fi
		else
			query_update_attempts="UPDATE $schema_config.$tbl_execute SET attempts=cast( (attempts + 1) as int) where table_name='$table_name' and dateload=$FECHA and id_execution = $executer "
			execute_querys "$query_update_attempts" "attempts" 16 "$intentos"
			attempts=${response[attempts]}
			#print_log "valor retornado Query_16:$attempts."

			print_log "Borrar: $path_log4jadc/$file_name"
			rm -f "$path_log4jadc/$file_name"
		
			print_log "Hubo un error en el procesamiento. Salida $res"
			exit $res;
		fi
		
		print_log "Borrar: $path_log4jadc/$file_name"
		rm -f "$path_log4jadc/$file_name"
	fi
}

# Función para obtener el número de ejecucioes que se deben procesar
get_num_executions(){
	print_log "Obteniendo # de ejecuciones..."
	query_count_executions="SELECT count(*) as total FROM $schema_config.$tbl_execute where table_name='$table_name' and dateload=$FECHA "
	
	execute_querys "$query_count_executions" "executions" 3 "$intentos"
	executions=${response[executions]}	
	#print_log "valor retornado Query_3:$executions."
	
	rm $ruta_tmp"count_executions.txt"
	echo -e $executions | sed 's/total//' | sed 's/-//g' | sed 's/ //g' > $ruta_tmp"count_executions.txt"
	executions=$(cat $ruta_tmp"count_executions.txt")
	print_log "# Ejecuciones:$executions."
	print_log "*****************************************************"
	echo
	echo
}

#Funcion para obtener el número de ejecucion que se debe procesar
get_executer(){
	print_log "Obteniendo ejecucion #$1..."
	query_get_executer="SELECT id_execution, table_name, dateload, avro_name, status FROM $schema_config.$tbl_execute where table_name='$table_name' and dateload=$FECHA and id_execution = $1 "
	
	execute_querys "$query_get_executer" "result" 4 "$intentos"
	result=${response[result]}	
	#print_log "valor retornado Query_4:$result."
	#echo -e $result > $ruta_tmp"executerall.txt"
}

#Funcion para obtener de la base de datos los parametros para ejecutar el componente de Spark
getCommandSpark(){
	type_query=$2
	
	if [ $type_query -eq 0 ]; then
		echo "Obteniendo parametros para spark, id_source:$1."
		get_command="select table_name,path_avro_all,key_columns,path_avro_cifras,path_write_cifras,type_load,number_partitions from $schema_config.$tabla_config where id_source=$1 and status=1"
		
		execute_querys "$get_command" "command" 11 "$intentos"
		command=${response[command]}	
		#print_log "valor retornado Query_11:$command."
			
		c_table=$(echo ${command} | cut -d" " -f1)
		c_avro_data=$(echo ${command} | cut -d" " -f2)
		c_keys=$(echo ${command} | cut -d" " -f3)
		c_avro_cifras=$(echo ${command} | cut -d" " -f4)
		c_write_cifras=$(echo ${command} | cut -d" " -f5)
		c_type_load=$(echo ${command} | cut -d" " -f6)
		c_num_partitions=$(echo ${command} | cut -d" " -f7)
		
		export c_table="$(echo -e "${c_table}" | tr -d '[:space:]')"
		export c_avro_data="$(echo -e "${c_avro_data}" | tr -d '[:space:]')"
		export c_keys="$(echo -e "${c_keys}" | tr -d '[:space:]')"
		export c_avro_cifras="$(echo -e "${c_avro_cifras}" | tr -d '[:space:]')"
		export c_write_cifras="$(echo -e "${c_write_cifras}" | tr -d '[:space:]')"
		export c_type_load="$(echo -e "${c_type_load}" | tr -d '[:space:]')"
		export c_num_partitions="$(echo -e "${c_num_partitions}" | tr -d '[:space:]')"
	else
		echo "Obteniendo comando para spark, id_source:$1."
		get_command="select command_spark from $schema_config.$tabla_config where id_source=$1 and status=1"
		
		execute_querys "$get_command" "command" 11 "$intentos"
		command=${response[command]}	
		#print_log "valor retornado Query_11:$command."
	fi
}

#Funcion generica para ejecutar un query, a atraves de impala-shell, en caso de error, reintentará la ejecución max_intentos veces.
execute_querys(){
	echo
	echo
	print_log "*****************************************************"
	print_log "Query_$3:$1."
	intentos=$4
	#print_log "Intentos llega:$intentos"

	if [ $2 == "query_cifras" ]; then
		print_log "Ejecutar consulta desde archivo."
		impala-shell -i $impala_conf -f $ruta_sql"consulta_cifras2.sql" > $ruta_tmp"resultado_cifras.txt"
	else
		params=$(impala-shell -i $impala_conf -q "$1" -B)
	fi
	
	res=$?
	print_log "res_Query_$3:$res."

	if [ $res -eq 0 ]; then
		print_log "valor Query_$3:$params"
		print_log "*****************************************************"
		echo
		echo
		#Almacenamos el valor obtenido del query en un arreglo
		response["$2"]=$params
		export intentos=0
	else
		if [ $intentos -eq $max_intentos ]; then
			export intentos=0
			print_log "Se agotaron los $max_intentos intentos para Query_$3, terminará con error."
			exit $res;
		fi
		let intentos=$(expr $intentos + 1 )	
		print_log "Hubo un error en Query_$3, se reinterará la ejecucion. Reintento:#$intentos."
		print_log "*****************************************************"
		echo
		echo
		execute_querys "$1" "$2" "$3" "$intentos" "$5"
	fi
}

#Funcion generica para ejecutar un query, a atraves de impala-shell, en caso de error, reintentará la ejecución max_intentos veces.
execute_querys_hive(){
	echo
	echo
	print_log "*****************************************************"
	print_log "Query_$3:$1."
	intentos=$4

	if [ $2 == "query_cifras" ]; then
		print_log "Ejecutar consulta desde archivo."
		#impala-shell -i $impala_conf -f $ruta_sql"consulta_cifras2.sql" > $ruta_tmp"resultado_cifras.txt"
		hive -f $ruta_sql"consulta_cifras2.sql" > $ruta_tmp"resultado_cifras.txt"
	else
		params=$(hive -e "$1" -S)
	fi
	
	res=$?
	print_log "res_Query_$3:$res."

	if [ $res -eq 0 ]; then
		print_log "valor Query_$3:$params"
		print_log "*****************************************************"
		echo
		echo
		#Almacenamos el valor obtenido del query en un arreglo
		response["$2"]=$params
		export intentos=0
	else
		if [ $intentos -eq $max_intentos ]; then
			export intentos=0
			print_log "Se agotaron los $max_intentos intentos para Query_$3, terminará con error."
			exit $res;
		fi
		let intentos=$(expr $intentos + 1 )	
		print_log "Hubo un error en Query_$3, se reinterará la ejecucion. Reintento:#$intentos."
		print_log "*****************************************************"
		echo
		echo
		execute_querys_hive "$1" "$2" "$3" "$intentos" "$5"
	fi
}

#Funcion para monitorear las ejecucines
monitor_status(){
	print_log "Revisar estatus ejecucion #$1"
	query_get_status="SELECT status FROM $schema_config.$tbl_execute where table_name='$table_name' and dateload=$FECHA and id_execution = $1 "
	
	execute_querys "$query_get_status" "status" 8 "$intentos"
	status=${response[status]}	
	print_log "valor retornado Query_8:$status."
	print_log "Status ejecucion #$1: $status"
	
	if [ $status -eq 1 ]; then
		#Enviar siguiente ejecución
		let executer=$(expr $executer + 1 )
		
		if [ $executer -gt $executions ]; then
			echo $(date)
			print_log "Notificar la finalización de la carga"
			envia_cifras
		else
			echo "----------------------------------------------------------------------executer:$executer"
			process_avro		
		fi
		
	else
		#Dormir para esperar que acabe la ejecucion N
		minutos_reproceso=${tiempos_espera_reproceso[indice_reproceso]}
		print_log "Ejecucion en curso, Ejecucion #$1, esperar $minutos_reproceso minuto(s) - ($(date))."
		echo
		echo
		let indice_reproceso=$(expr $indice_reproceso + 1 )	
		sleep ${minutos_reproceso}m
		if [ $indice_reproceso -eq $lon_reproceso ]; then
			export indice_reproceso=0
		fi
		monitor_status "$1"
	fi
	
}

#Funciona para actualizar las estadisticas de la tabla
compute_stats(){
	query_invalidate "$schema" "$table_name"

	query_update_compute="compute stats $schema.$table_name"
	execute_querys "$query_update_compute" "update_stats" 19 "$intentos"
	update_stats=${response_i[update_stats]}
}

#Funcion para enviar las cifras de control de la carga
envia_cifras(){
	rm $ruta_tmp"cifras.txt"

	query_invalidate "$schema" "$tabla_cifras"
	print_log "Obtener conteo de cifras de control..."
	query_cifras="select count(*) from $schema.$tabla_cifras c inner join ( select datasetname, max(dateload) as dateload from $schema.$tabla_cifras where datasetname='$table_name' group by datasetname ) cm on c.datasetname = cm.datasetname and c.dateload = cm.dateload "
	execute_querys "$query_cifras" "cifras" 14 "$intentos"
	#execute_querys_hive "$query_cifras" "cifras" 14 "$intentos"
	export cifras=${response[cifras]}	
	print_log "valor retornado Query_14:$cifras."
	echo -e $cifras > $ruta_tmp"cifras.txt"
	
	if [ $cifras -ne 0 ]; then
		print_log "Enviar correo con los conteos"
		obtiene_cifras
		export cifras_mail=$(cat $ruta_tmp"tabla_cifras.txt")
		put_parameters_oozie_mail
		invoca_oozie_cifras
	else
		#Validar que se hará en el caso de que no se encuentre las cifras de control
		echo "No se encontraron cifras de control..."
		#query_invalidate "$schema" "$tabla_cifras"
		#sleep 1m
		#envia_cifras
	fi
}

#Funciona para armar la tabla con los conteos de las cifras de control cargadas
obtiene_cifras(){
	cat $ruta_sql"consulta_cifras.sql" | sed 's/$table_name/'${table_name}'/g' | sed 's/$FECHA/'${FECHA}'/g' | sed 's/$schema/'${schema}'/g' | sed 's/$tabla_cifras/'${tabla_cifras}'/g' > $ruta_sql"consulta_cifras2.sql"
	execute_querys "" "query_cifras" 15 "$intentos"
	#execute_querys_hive "" "query_cifras" 15 "$intentos"

	echo  "<table border=1 width=600px style='font-family:Arial; font-size:14px'><caption>Reporte de cifras de control</caption><tr style='background-color: #87CEEB; color:#FFFFFF;'><th>" "Tabla" "</th><th>" "Desc_tabla " "</th><th>" "Fecha_archivo" "</th><th>" "Nombre_archivo" "</th><th>" "Total_archivo" "</th><th>" "Total_insertados" "</th><th>" "Total_actualizados" "</th><th>" "Total_borrados" "</th><th>" "Fecha_carga_dlk" "</th></tr>"  > $ruta_tmp"tabla_cifras.txt"
	result_tail=$(tail -n +4 $ruta_tmp"resultado_cifras.txt" | grep -v "+")
	if [ "$result_tai" != "" ]; then
		tail -n +4 $ruta_tmp"resultado_cifras.txt" | grep -v "+" | sed 's/|//g' |  sed 's/      / /g' >> $ruta_tmp"tabla_cifras.txt"
		echo "Tail con +"
	else
		tail -n +4 $ruta_tmp"resultado_cifras.txt" | grep -v "-" | sed 's/|//g' |  sed 's/      / /g' >> $ruta_tmp"tabla_cifras.txt"
		echo "Tail con -"
	fi
	echo -e "</table>" >> $ruta_tmp"tabla_cifras.txt"
}

#Funcion para ejecutar un invalidate metadata
query_invalidate(){
	print_log "Actualizamos la tabla:$1.$2 ..."
	#invalidate_query="invalidate metadata $schema.$tabla_cifras"
	invalidate_query="invalidate metadata $1.$2"
	execute_querys "$invalidate_query" "invalidate_query" 18 "$intentos"
	export invalidate_query=${response[invalidate_query]}
	#print_log "valor retornado Query_18:$invalidate_query."
}

#Funcion para agregar los parametros necesarios para enviar el correo de cifras
put_parameters_oozie_mail(){
	echo "oozie.use.system.libpath=True" > "$path_properties"cifras.properties
	echo "security_enabled=False" >> "$path_properties"cifras.properties
	echo "dryrun=False" >> "$path_properties"cifras.properties
	echo "nameNode=hdfs://nameservice1" >> "$path_properties"cifras.properties
	echo "jobTracker=yarnRM" >> "$path_properties"cifras.properties
	echo "CUERPO="$cifras_mail >> "$path_properties"cifras.properties	
	echo "FECHA"=$FECHA  >> "$path_properties"cifras.properties
	echo "table_name"=$table_name  >> "$path_properties"cifras.properties
	echo "PARA"=${properties[MAIL]}  >> "$path_properties"cifras.properties
	echo "esquema_tablas_rci"=$schema  >> "$path_properties"cifras.properties
	echo "esquema_tablas_config"=$schema_config  >> "$path_properties"cifras.properties
	echo "tabla_cifras"=$tabla_cifras  >> "$path_properties"cifras.properties
}

invoca_oozie_cifras(){
	print_log "Invocando Oozie para envio de cifras de control"
	
	wspace_oozie_mail=${properties[wspace_oozie_mail]}
	wspace_oozie_mail="$(echo -e "${wspace_oozie_mail}" | tr -d '[:space:]')"
	print_log "$wspace_oozie_mail."
	
	export OOZIE_CLIENT_OPTS='-Djavax.net.ssl.trustStore=/opt/cloudera/security/jks/truststore.jks'
	echo $OOZIE_CLIENT_OPTS
	
	export OBTENJOB=$(oozie job -oozie https://mxtold01dlu02.attdatalake.com.mx:11443/oozie -auth KERBEROS -run -D oozie.wf.application.path hdfs://attdatalakehdfs/user/hue/oozie/workspaces/hue-oozie-"$wspace_oozie_mail"/workflow.xml -config "$path_properties"cifras.properties -run)	

	print_log "El id del workflow es: $OBTENJOB"

	echo $OBTENJOB > $ruta_tmp"oozie_job_rci.txt"
	export OOZIEJOB=$(cat $ruta_tmp"oozie_job_rci.txt" | awk -F' ' '{ print $2 }')
	print_log "El id del workflow es: $OOZIEJOB"	
}

#----------------------------------------------------------------------------------#
#								Funcion principal del shell						   #
#----------------------------------------------------------------------------------#
home()
{	
	read_properties "$file_properties"	
	print_log "*****************************************************"
	getDate
	print_log "*****************************************************"
	get_file_process 
	print_log "*****************************************************"
	read_avros_process
	print_log "*****************************************************"
	read_schema_to_process
	print_log "*****************************************************"
}

home
