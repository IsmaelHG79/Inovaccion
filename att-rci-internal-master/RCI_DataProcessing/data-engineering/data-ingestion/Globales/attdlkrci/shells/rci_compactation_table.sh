#set -xv
#!/bin/bash
#------------------------------------------------------------------------------------------------------------#
#	Nombre:		rci_compactation_table.sh                                             			 		 	 #
#	Objetivo: 	Realiza la compactación de las diferentes particiones de una tabla						     #
#	Autor:		ejesus				                                                                         #
#	Vía de ejecución: Línea de comandos		                                                            	 #
#	Fecha:		26 de Enero de 2019  	                                                           		 	 #
#	Area:		Datalake AT&T											                                     #
#	Salida:		Partición compactada																	     #
#------------------------------------------------------------------------------------------------------------#

if [ $# -lt 2 ]
	then
		echo '--------------------------------------------------------------'
		echo "Error: parametro"
		echo "usage: sh $(basename $0) num_archivo_procesar tipo_particion [particion_especifica AAAA,[M]M,[D]D]"
		echo "num_archivo_procesar		Es el id de la fuiente definida en la tabla de configuración (rci_metadata_db.tx_config)"
		echo "tipo_particion			Indica el tipo de particion con la que cuenta la tabla a compactar, m=AAAAMM, d=AAAAMMDD"
		echo "particion_especifica		Especifica una partición especifica compactar, AAAA,[M]M,[D]D, si el mes o dia solo tiene 1 digito, se manda 1 digito"
		echo "Ejemplo:"
		echo "1. Para compactar todas las particiones año,mes de la tabla rci_network_db.tx_test_load el comando sera: $ rci_compactation_table.sh 0 m"
		echo "2. Si la tabla rci_network_db.tx_test_load tiene particion por año,mes,dia el comando sera: $ rci_compactation_table.sh 0 d"
		echo "3. Si solo queremos compactar la particion mensual 2020,1 el comando sera: $ rci_compactation_table.sh 0 m 2020,1"
		echo "4. Si solo queremos compactar la particion diaria 2020,1,5 el comando sera: $ rci_compactation_table.sh 0 d 2020,1,5"
		echo '--------------------------------------------------------------'
	exit 1
fi

export type_execution=$1
export a_type_execution=$1
export type_particion=$2
echo "type_particion:$type_particion."
export particion=$3
echo "particion:$particion."

export impala_conf="balancer.attdatalake.com.mx -d default -k --ssl --ca_cert=/opt/cloudera/security/ca-certs/CertToolkitCA.pem"

export HOME_SC=/home/raw_rci/attdlkrci/
export path_properties=$HOME_SC"config/"
export enviroment="pro"
export group_exec="raw_rci"
export file_properties=$path_properties$enviroment"_rci_ingesta_generacion_avro.properties"
declare -A properties

#Agregamos las lineas para poder utilizar el log
export path_log4jadc=$HOME_SC"shells"
. $path_log4jadc/log4j_attdlkrci.sh 1 'rci_compactation_table' "$enviroment" "$HOME_SC" "$group_exec"
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
declare -A response_p

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
	#print_log "$tbl_execute."
	
	tabla_config=${properties[tabla_config]}
	tabla_config="$(echo -e "${tabla_config}" | tr -d '[:space:]')"
	print_log "$tabla_config."
	
	tabla_cifras=${properties[tabla_cifras]}
	tabla_cifras="$(echo -e "${tabla_cifras}" | tr -d '[:space:]')"
	#print_log "$tabla_cifras."
	
	path_cifras=${properties[path_cifras]}
	path_cifras="$(echo -e "${path_cifras}" | tr -d '[:space:]')"
	#print_log "$path_cifras."
	print_log "*****************************************************"
	
	query_get_param="select path_avsc, table_name, path_hdfs, path_backup, ban_process_all, path_avsc_all, path_avro_all, id_source, json_partition from $schema_config.$tabla_config where id_source=$a_type_execution and status=1"
	execute_querys "$query_get_param" "params" 10 "$intentos" ""
	params=${response_p[params]}
	
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
	
	print_log "Se compactara tabla: $table_name"
	print_log "Location es: $location"
	print_log "Id_source: $id"
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
		response_p["$2"]=$params
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

# Funcion para realizar la compactacion de las particiones de una tabla
generate_list_dates(){

	if [ "$particion" == "" ]; then
		query_partitions="show partitions $schema.$table_name"
		execute_querys "$query_partitions" "partitions" 20 "$intentos" "result_show_partitions.txt"
		
		wc -l $ruta_tmp"result_show_partitions.txt" > $ruta_tmp"total_par.txt"
		num_par=$(tail -n 1 $ruta_tmp"total_par.txt")
		export num_par=$(echo ${num_par} | cut -d" " -f1)
		let num=$(expr $num_par - 1)
		print_log "Total particiones:$num."
	fi
			
		if [ "$type_particion" == "m" ]; then
			#recuperar mes
			print_log "Particion por mes"
			generate_query_by_month
		else 
			if [ "$type_particion" == "d" ]; then
				#recuperar mes
				print_log "Particion por dia"
				generate_query_by_day
			fi
		fi
}

# Funcion para generar la consulta de compactacion por mes
generate_query_by_month(){
	if [ "$particion" == "" ]; then 
		if [ $num -ne 0 ]; then
			let num=$(expr $num + 1)
			#Comenzamos el ciclo de procesamiento de N particiones
			for i in $( eval echo {2..$num} )
			do
				v_anio=$(tail -n $i "$ruta_tmp"result_show_partitions.txt | awk -F' ' '{ print $1}')
				v_anio=$(echo ${v_anio} | cut -d" " -f1)
				print_log "Anio $i:$v_anio."
				
				v_mes=$(tail -n $i "$ruta_tmp"result_show_partitions.txt | awk -F' ' '{ print $2}')
				v_mes=$(echo ${v_mes} | cut -d" " -f1)
				print_log "Mes $i:$v_mes."
				
				execute_query_by_month
			done
			print_log "Fin recorrido particiones."
		fi
	else
		v_anio=$(echo ${particion} | cut -d"," -f1)
		print_log "Anio:$v_anio."
		v_mes=$(echo ${particion} | cut -d"," -f2)
		print_log "Mes:$v_mes."
		
		execute_query_by_month
	fi
}

execute_query_by_month(){
	cat $ruta_sql"consulta_compactacion_mes.sql" | sed 's/$schema/'${schema}'/g' | sed 's/$table_name/'${table_name}'/g' | sed 's/$anio/'${v_anio}'/g' | sed 's/$mes/'${v_mes}'/g' > $ruta_sql"consulta_compactacion_mes2.sql"
	print_log "*****************************************************"
	print_log "*****************************************************"
	cat $ruta_sql"consulta_compactacion_mes2.sql"
	execute_querys_hive "consulta_compactacion_mes2.sql" "query_file" 15 "$intentos"
	print_log "*****************************************************"
	print_log "*****************************************************"
}

# Funcion para generar la consulta de compactacion por dia
generate_query_by_day(){
	if [ "$particion" == "" ]; then 
		if [ $num -ne 0 ]; then
			let num=$(expr $num + 1)
			#Comenzamos el ciclo de procesamiento de N particiones
			for i in $( eval echo {2..$num} )
			do
				v_anio=$(tail -n $i "$ruta_tmp"result_show_partitions.txt | awk -F' ' '{ print $1}')
				v_anio=$(echo ${v_anio} | cut -d" " -f1)
				print_log "Anio $i:$v_anio."
				
				v_mes=$(tail -n $i "$ruta_tmp"result_show_partitions.txt | awk -F' ' '{ print $2}')
				v_mes=$(echo ${v_mes} | cut -d" " -f1)
				print_log "Mes $i:$v_mes."
				
				v_dia=$(tail -n $i "$ruta_tmp"result_show_partitions.txt | awk -F' ' '{ print $3}')
				v_dia=$(echo ${v_dia} | cut -d" " -f1)
				print_log "Dia $i:$v_dia."
				
				execute_query_by_day
			done
			print_log "Fin recorrido particiones."
		fi
	else
		v_anio=$(echo ${particion} | cut -d"," -f1)
		print_log "Anio:$v_anio."
		v_mes=$(echo ${particion} | cut -d"," -f2)
		print_log "Mes:$v_mes."
		v_dia=$(echo ${particion} | cut -d"," -f3)
		print_log "Dia $i:$v_dia."
		
		execute_query_by_day
	fi
}

execute_query_by_day(){
	cat $ruta_sql"consulta_compactacion_dia.sql" | sed 's/$schema/'${schema}'/g' | sed 's/$table_name/'${table_name}'/g' | sed 's/$anio/'${v_anio}'/g' | sed 's/$mes/'${v_mes}'/g' | sed 's/$dia/'${v_dia}'/g' > $ruta_sql"consulta_compactacion_dia2.sql"
	print_log "*****************************************************"
	print_log "*****************************************************"
	cat $ruta_sql"consulta_compactacion_dia2.sql"
	execute_querys_hive "consulta_compactacion_dia2.sql" "query_file" 16 "$intentos"
	print_log "*****************************************************"
	print_log "*****************************************************"
}

#Funcion generica para ejecutar un query, a atraves de impala-shell, en caso de error, reintentará la ejecución max_intentos veces.
execute_querys_hive(){
	echo
	echo
	print_log "*****************************************************"
	print_log "Query_$3:$1."
	intentos=$4

	if [ $2 == "query_file" ]; then
		print_log "Ejecutar consulta desde archivo."
		hive -f $ruta_sql"$1" > $ruta_tmp"resultado_$1.txt"
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
		response_p["$2"]=$params
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
	generate_list_dates
	print_log "*****************************************************"
	print_log "Finalizo la compactacion para $table_name"
}

home
