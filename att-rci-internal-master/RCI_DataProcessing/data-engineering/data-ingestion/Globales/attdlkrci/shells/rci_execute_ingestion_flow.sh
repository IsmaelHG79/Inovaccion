#set -xv
#!/bin/bash
#------------------------------------------------------------------------------------------------------------#
#	Nombre:		rci_execute_ingestion_flow.sh                                          			 		 	 #
#	Objetivo: 	Shell encargado de ejecutar un flujo de ingestion, encendiendo y apagando un procesador de nifi bajo demanda #
#	Autor:		ejesus				                                                                         #
#	Vía de ejecución: Línea de comandos		                                                            	 #
#	Fecha:		28 de Enero de 2019  	                                                           		 	 #
#	Area:		Datalake AT&T											                                     #
#	Salida:		Ingestión de una fuente																	     #
#------------------------------------------------------------------------------------------------------------#

if [ $# -lt 2 ]
	then
		echo '--------------------------------------------------------------'
		echo "Error: parametro"
		echo "usage: sh $(basename $0) num_flujo_procesar frecuencia_ejecucion"
		echo "num_flujo_procesar		Es el id de la fuente definida en la tabla de configuración (rci_metadata_db.tx_config)"
		echo "frecuencia_ejecucion		Indica la frecuencia con la que se ingestara la fuente, d=diaria, s=semanal, m=mensual"
		echo '--------------------------------------------------------------'
	exit 1
fi

export type_execution=$1
export a_type_execution=$1
export type_particion=$2
echo "type_particion:$type_particion."

export impala_conf="balancer.attdatalake.com.mx -d default -k --ssl --ca_cert=/opt/cloudera/security/ca-certs/CertToolkitCA.pem"
export nifi_api="http://10.150.25.145:18080/nifi-api"

export HOME_SC=/home/raw_rci/attdlkrci/
export path_properties=$HOME_SC"config/"
export enviroment="pro"
export group_exec="raw_rci"
export file_properties=$path_properties$enviroment"_rci_ingesta_generacion_avro.properties"
declare -A properties

#Agregamos las lineas para poder utilizar el log
export path_log4jadc=$HOME_SC"shells"
. $path_log4jadc/log4j_attdlkrci.sh 1 'rci_execute_ingestion_flow' "$enviroment" "$HOME_SC" "$group_exec"
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
declare -A response_f

export tiempos_espera=(5 3 2 1)
export indice=0
export lon=$(expr "${#tiempos_espera[@]}" - 1 )

export time_read=10

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
	
	tabla_config=${properties[tabla_config]}
	tabla_config="$(echo -e "${tabla_config}" | tr -d '[:space:]')"
	print_log "$tabla_config."
	
	tabla_cifras=${properties[tabla_cifras]}
	tabla_cifras="$(echo -e "${tabla_cifras}" | tr -d '[:space:]')"
	
	path_cifras=${properties[path_cifras]}
	path_cifras="$(echo -e "${path_cifras}" | tr -d '[:space:]')"
	
	tabla_processors=${properties[tabla_processors]}
	tabla_processors="$(echo -e "${tabla_processors}" | tr -d '[:space:]')"
	print_log "$tabla_processors."
	print_log "*****************************************************"
	
	#query_get_processor="select processor_name,'|',id_processor,'|',status,'|',power_on_date,'|',usuario,'|',hostname from $schema_config.$tabla_processors where id_source=$a_type_execution"
	query_get_processor="select p.processor_name,'|',p.id_processor,'|',p.status,'|',p.power_on_date,'|',p.usuario,'|',p.hostname,'|',c.path_avro_all from $schema_config.$tabla_processors p inner join $schema_config.$tabla_config c on p.id_source = c.id_source where p.id_source=$a_type_execution"
	execute_querys "$query_get_processor" "processor" 21 "$intentos" ""
	params=${response_f[processor]}
	
	export processor_name=$(echo ${params} | cut -d"|" -f1)
	export id_processor=$(echo ${params} | cut -d"|" -f2)
	export status=$(echo ${params} | cut -d"|" -f3)
	export power_on_date=$(echo ${params} | cut -d"|" -f4)
	export usuario=$(echo ${params} | cut -d"|" -f5)
	export hostname=$(echo ${params} | cut -d"|" -f6)
	export path_hdfs=$(echo ${params} | cut -d"|" -f7)
	
	export processor_namef="$(echo -e "${processor_name}" | tr -d '[:space:]')"
	export id_processor="$(echo -e "${id_processor}" | tr -d '[:space:]')"
	export status="$(echo -e "${status}" | tr -d '[:space:]')"
	export power_on_date="$(echo -e "${power_on_date}" | tr -d '[:space:]')"
	export usuario="$(echo -e "${usuario}" | tr -d '[:space:]')"
	export hostname="$(echo -e "${hostname}" | tr -d '[:space:]')"
	export path_hdfs="$(echo -e "${path_hdfs}" | tr -d '[:space:]')"
	
	print_log "Se encendera procesador:$processor_name"
	print_log "Nombre procesador limpio:$processor_namef"
	print_log "Id procesador es:$id_processor"
	print_log "Estatus es:$status"
	print_log "Fecha encendido:$power_on_date"
	print_log "Usuario:$usuario"
	print_log "Hostname:$hostname"
	print_log "Ruta leer archivos:$path_hdfs"
}

#Funcion generica para ejecutar un query, a atraves de impala-shell, en caso de error, reintentará la ejecución max_intentos veces.
execute_querys(){
	echo
	echo
	echo "5:$5."
	print_log "*****************************************************"
	print_log "Query_$3:$1."
	intentos=$4

	if [ $2 == "query_cifras" ]; then
		print_log "Ejecutar consulta desde archivo."
		impala-shell -i $impala_conf -f $ruta_sql"consulta_cifras2.sql" > $ruta_tmp"resultado_cifras.txt"
	else
		if [ "$5" != "" ]; then
			echo "Salida a archivo"
			impala-shell -i $impala_conf -q "$1" -B > $ruta_tmp"$5"
			#params="ok"
		else
			params=$(impala-shell -i $impala_conf -q "$1" -B)
		fi
	fi
	
	res=$?
	print_log "res_Query_$3:$res."

	if [ $res -eq 0 ]; then
		print_log "valor Query_$3:$params"
		print_log "*****************************************************"
		echo
		echo
		#Almacenamos el valor obtenido del query en un arreglo
		response_f["$2"]=$params
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
		execute_querys "$1" "$2" "$3" "$intentos"
	fi
}

start_processor(){
	#"curl -i -X PUT -H 'Content-Type: application/json' -d '{"id":"ef10285e-5432-33b7-b161-ce18ac804d0d","state":"RUNNING"}' http://10.150.25.145:18080/nifi-api/flow/process-groups/ef10285e-5432-33b7-b161-ce18ac804d0d;"
	print_log "Iniciar procesador:$processor_name"
	export command_start="curl -i -X PUT -H 'Content-Type: application/json' -d '{\"id\":\"$id_processor\",\"state\":\"RUNNING\"}' $nifi_api/flow/process-groups/$id_processor;"	
	print_log "$command_start"
	hr_inicio=$(date '+%F %T')
	print_log "$hr_inicio"

	eval $command_start > "$ruta_tmp"start_"$processor_namef".txt
	res=$?
	print_log "Respuesta inicio procesador $processor_name es:$res"
	
	if [ $res -eq 0 ]; then
		print_log "Procesador $processor_name iniciado"
		get_status
		monitor_status
	else
		print_log "Error al iniciar el procesador $processor_name"
	fi
}

get_status(){
	print_log "Esperando a que el procesador $processor_name lea los archivos..."
	sleep ${time_read}
	export command_status="curl -i -X GET -H 'Content-Type: application/json' $nifi_api/flow/process-groups/$id_processor/status;"
	print_log "$command_status"
	eval $command_status > "$ruta_tmp"status_"$processor_namef".txt
	res=$?
}

end_processor(){
	#export host="curl -i -X PUT -H 'Content-Type: application/json' -d '{"id":"ef10285e-5432-33b7-b161-ce18ac804d0d","state":"STOPPED"}' http://10.150.25.145:18080/nifi-api/flow/process-groups/ef10285e-5432-33b7-b161-ce18ac804d0d;"
	print_log "Detener procesador $processor_name"
	export command_stop="curl -i -X PUT -H 'Content-Type: application/json' -d '{\"id\":\"$id_processor\",\"state\":\"STOPPED\"}' $nifi_api/flow/process-groups/$id_processor;"	
	print_log "$command_stop"
	hr_fin=$(date '+%F %T')
	print_log "$hr_fin"
	eval $command_stop > "$ruta_tmp"stop_"$processor_namef".txt
	res=$?	
	print_log "Respuesta detener procesador $processor_name es:$res"
}

#Funcion para monitorear las ejecucines
monitor_status(){
	print_log "----------------------------------------------------------------------"
	print_log "----------------------------------------------------------------------"
	print_log "------------- Revisar estatus ejecucion $processor_name --------------"
	print_log "----------------------------------------------------------------------"
	print_log "----------------------------------------------------------------------"
	
	#Obtener el numero de archivos que va a escribir el procesador en la ruta HDFS
	#grep -Po '"flowFilesIn":.*?[^\\]",' $ruta_tmp"status_"$processor_name".txt" | head -1
	export files_input=$(grep -Po '"flowFilesIn":.*?[^\\]",' $ruta_tmp"status_"$processor_namef".txt" | head -1)
	print_log "files_input es:$files_input"
	export value_input=$(echo ${files_input} | cut -d"," -f1)
	print_log "value_input es:$value_input"
	export value_input=$(echo ${value_input} | cut -d":" -f2)
	print_log "value_input:$value_input"
	let num_files=$(expr $value_input + 0 )	
	print_log "Archivos a escribir son:$num_files"
	
	if [ $num_files -ne 0 ]; then
		#Leer la ruta del HDFS y contar los archivos depositados
		#export path_hdfs=/data/RCI/raw/cip/data/
		export num_files_read=$(hdfs dfs -ls -C $path_hdfs | wc -l)
		print_log "Numero de archivos leidos de la ruta $path_hdfs:$num_files_read"
		
		if [ $num_files -eq $num_files_read ] || [ $num_files -lt $num_files_read ]; then
			echo $(date)
			print_log "Apagar el procesador $processor_name"
			end_processor
			#Invocar el shell de ejecución masiva
			. $path_log4jadc/rci_ingesta_generacion_avro.sh "$a_type_execution"
			res=$?
			print_log "Respuesta de shell $path_log4jadc / rci_ingesta_generacion_avro.sh: $res"
			exit $res
		else
			#Esperar a que acabe la ejecucion de Nifi
			minutos=${tiempos_espera[indice]}
			print_log "Ejecucion en curso del procesador $processor_name, esperar $minutos minuto(s) - ($(date))."
			echo
			echo
			let indice=$(expr $indice + 1 )
			sleep ${minutos}m
			if [ $indice -eq $lon ]; then
				export indice=0
			fi
			monitor_status
		fi
	else
		get_status
		monitor_status
	fi
}

#----------------------------------------------------------------------------------#
#								Funcion principal del shell						   #
#----------------------------------------------------------------------------------#
home(){	
	read_properties "$file_properties"	
	print_log "*****************************************************"
	getDate
	print_log "*****************************************************"
	get_file_process
	print_log "*****************************************************"
	start_processor
	print_log "*****************************************************"
	print_log "Finalizo la ejecución del procesador:$processor_name"
}

home
