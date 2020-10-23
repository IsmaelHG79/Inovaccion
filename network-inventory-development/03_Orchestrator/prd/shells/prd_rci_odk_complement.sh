#set -xv
#!/bin/bash
#------------------------------------------------------------------------------------------------------------#
#	Nombre:		prd_rci_odk_complement.sh                                          			 		 	     #
#	Versión:	1.0.0                                          			 		                             #
#	Objetivo: 	Shell encargado de ejecutar los flujos complementarios de ODK's         					 #
#	Autor:		ejesus				                                                                         #
#	Vía de ejecución: Línea de comandos		                                                            	 #
#	Fecha:		26 de Mayo de 2020  	                                                           		 	 #
#	Area:		Datalake AT&T											                                     #
#------------------------------------------------------------------------------------------------------------#

#Establecer los ids de las tablas a ejecutar
export ids_flows="270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302"
export pending_flows=""

if [ $# -lt 1 ]
	then
		echo '--------------------------------------------------------------'
		echo "Error: parametros"
		echo "usage: sh $(basename $0)  [flow_continue] [reset]"
		echo "flow_continue             Parámetro para poder ejecutar el componente independientemente palabra distinta de phase_all"
		echo "reset                     Opcional: Valor para indicar que el flujo se debe reiniciar y ejecutar desde el inicio."
		echo '--------------------------------------------------------------'
	exit 1;
fi

#----------------------------------------------------------------------------------#
#						Leer parámetros para la ejecucion	   					   #
#----------------------------------------------------------------------------------#

export flow_continue=$1
export reset=$2

#----------------------------------------------------------------------------------#
#				Definimos variables necesarias para la ejecucion	   		       #
#----------------------------------------------------------------------------------#

export environment="prd"
export group_exec="inventario"
export time_wait=1

export path_home=/home/raw_rci/attdlkrci/$environment/
export path_shells=$path_home"shells/"
export path_lib=$path_shells"lib/"
export path_config=$path_home"config/"
export path_temp=$path_home"tmp/"
export path_sql=$path_home"sql/"
export path_logs=$path_home"logs/"
export path_status=$path_home"status/"
export path_pyspark=$path_home"pyspark/"

bn=$(basename $0)
bn_p=$(echo $bn | awk '{print index($0, ".")}')
let di=$(expr $bn_p - 9)
let bn_p=$(expr $bn_p - 1)
name_file_log=$(echo $bn | awk -v i=$bn_p '{print substr($0,0,i)}')
echo "name_file_log:$name_file_log"

name_flow=$(echo $bn | awk -v d=$di '{print substr($0,9,d)}')
echo "name_flow:$name_flow"

#----------------------------------------------------------------------------------#
#				Agregamos las lineas para poder usar las librerias	   		       #
#----------------------------------------------------------------------------------#

if [ "phase_all" != "$flow_continue" ]; then
	#Agregamos las lineas para poder utilizar la librería de logs
	. $path_lib/"$environment"_log4j_attdlkrci.sh 1 "$environment"_$name_file_log "$environment" "$path_home" "$group_exec" "$name_flow"
	create_dir_logs
	echo "Nombre del archivo de log: $name_file"
	
	#Referenciamos el nombre del archivo properties y declaramos el arreglo donde estarán los valores de las variables
	export file_properties=$path_config$environment"_rci_ingesta_generacion_avro.properties"
	declare -A properties
	
	# Variables para poder reintentar ejecutar una consulta en caso de desconexión
	export intentos=1
	export max_intentos=3
	declare -A response_f
	
	export a_id_table=45
fi

#Agregamos las lineas para poder utilizar la librería utils
. $path_lib/"$environment"_utils.sh

#----------------------------------------------------------------------------------#
#								Area de funciones								   #
#----------------------------------------------------------------------------------#

get_id_odk(){
    #Obtenemos el id del odk a ejecutar en base al ctl_tid
    print_log "Recuperar id_odk para tabla $1"
    case $1 in
    270)
        export odk_id=12
        ;;
    271)
        export odk_id=29
        ;;
    272)
        export odk_id=32
        ;;
    273)
        export odk_id=34
        ;;
    274)
        export odk_id=38
        ;;
    275)
        export odk_id=46
        ;;
    276)
        export odk_id=55
        ;;
    277)
        export odk_id=56
        ;;
    278)
        export odk_id=58
        ;;
    279)
        export odk_id=60
        ;;
    280)
        export odk_id=61
        ;;
    281)
        export odk_id=63
        ;;
    282)
        export odk_id=64
        ;;
    283)
        export odk_id=65
        ;;
    284)
        export odk_id=66
        ;;
    285)
        export odk_id=69
        ;;
    286)
        export odk_id=75
        ;;
    287)
        export odk_id=76
        ;;
    288)
        export odk_id=83
        ;;
    289)
        export odk_id=84
        ;;
    290)
        export odk_id=85
        ;;
    291)
        export odk_id=95
        ;;
    292)
        export odk_id=98
        ;;
    293)
        export odk_id=99
        ;;
    294)
        export odk_id=108
        ;;
    295)
        export odk_id=111
        ;;
    296)
        export odk_id=114
        ;;
    297)
        export odk_id=115
        ;;
    298)
        export odk_id=136
        ;;
    299)
        export odk_id=28
        ;;
    300)
        export odk_id=37
        ;;
    301)
        export odk_id=72
        ;;
    302)
        export odk_id=97
        ;;
    esac
    print_log "odk_id recuperado:$odk_id"
}

#----------------------------------------------------------------------------------#
#			Funcion para obtener la configiración de las tablas a procesar		   #
#----------------------------------------------------------------------------------#
get_config_table(){
	query_config_table="select c.ctl_tid,'|',t.ctl_sid,'|',t.table_name,'|',c.schema_database,'|',c.key_columns,'|',c.command_spark from $schema_config.$table_config c inner join $schema_config.$table_names t on c.ctl_tid=t.ctl_tid where c.ctl_tid=$idp_execute and t.table_status='$status_active' and lower(c.environment_config) = '$environment' "
	execute_querys "$query_config_table" "ct" 60 "$intentos" "$schema_config" ""
	values_conf_tbl=${response_f[ct]}
	
	if [ "" == "$values_conf_tbl" ]; then
		print_log "No se encontró configuración asociada al ctl_tid=$idp_execute y ambiente=$environment en la tabla $schema_config.$table_config, validar con Query_60."
		print_log "#----------------------------------------------------------------------------------#"
		print_log "#                          Punto de control 1: exit 1                              #"
		print_log "#----------------------------------------------------------------------------------#"
		exit 1;
	fi
	
	export odk_tid=$(echo ${values_conf_tbl} | cut -d"|" -f1)
	export odk_sid=$(echo ${values_conf_tbl} | cut -d"|" -f2)
	export odk_tnm=$(echo ${values_conf_tbl} | cut -d"|" -f3)
	export odk_tsh=$(echo ${values_conf_tbl} | cut -d"|" -f4)
	export odk_tkc=$(echo ${values_conf_tbl} | cut -d"|" -f5)
	export odk_tcp=$(echo ${values_conf_tbl} | cut -d"|" -f6)
	
	export odk_tid="$(echo -e "${odk_tid}" | tr -d '[:space:]')"
	export odk_sid="$(echo -e "${odk_sid}" | tr -d '[:space:]')"
	export odk_tnm="$(echo -e "${odk_tnm}" | tr -d '[:space:]')"
	export odk_tsh="$(echo -e "${odk_tsh}" | tr -d '[:space:]')"
	export odk_tkc="$(echo -e "${odk_tkc}" | tr -d '[:space:]')"
	
	print_log "	table id                      $odk_tid"
	print_log "	source id                     $odk_sid"
	print_log "	table name                    $odk_tnm"
	print_log "	table schema                  $odk_tsh"
	print_log "	key columns                   $odk_tkc"
}


#----------------------------------------------------------------------------------#
#								Funcion principal del shell						   #
#----------------------------------------------------------------------------------#
home(){
	if [ "phase_all" != "$flow_continue" ]; then
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
		
		#7.2.1 Asignación de variables globales 
		set_environment_variables
	fi

	getDate
	print_log "*****************************************************"
	clean_flag_execution
	check_flag_execution
	
	print_log "$pending_flows"
	print_log ""

	#Recuperamos los parámetros id_source y table_id
			
	if [ 0 -lt $p_flows ]; then
		for idx in $( eval echo {1..$p_flows} )
		do			
			idp_execute=$(echo $pending_flows | awk -v c=$idx -F',' '{ print $c}')
			print_log "4. id $idx es $idp_execute"
			print_log ""
			print_log ""
			
			get_config_table
			
			#Generamos el ctl_eid para cada tabla ce Odk
			generate_field_ctl_eid $odk_sid $idp_execute
			get_id_odk $idp_execute
			
			command_py=$(echo "${odk_tcp//'{1}'/\"Adquisicion_ODK_$odk_id\"}")
			command_py=$(echo "${command_py//'{2}'/$path_pyspark}")
			command_py=$(echo "${command_py//'{3}'/\"$odk_sid,$idp_execute,$ctl_eid\"}")
			command_py=$(echo "${command_py//'{4}'/$environment}")
			command_py=$(echo "${command_py//'{5}'/$odk_tsh}")
			command_py=$(echo "${command_py//'{6}'/$odk_tkc}")
			
			print_log "Ejecutar Adquisicion ODK$odk_id"
			
			print_log ""
			print_log "Comando es:"
			print_log "$command_py"
			
			res_pyspark=$(eval "$command_py" 1>>$name_file 2>>$name_file)
			res_py=$?
			
			print_log ""
			print_log ""
			print_log "-----------------------------------------------------"
			print_log "-------  Resultado py $idp_execute:$res_py.  --------"
			print_log "-----------------------------------------------------"
			
			if [ 0 -eq $res_py ]; then
				print_log "Generar bandera en done"
				write_status_done $idp_execute
				generate_eid_references $idp_execute
			fi
			
			print_log "En ${time_wait} minutos se lanzará el próximo flujo..."
			print_log ""
			print_log ""
			sleep ${time_wait}m
		done
	fi
	
	#Validamos que todos los flujos se ejecutaron
	num_ids_flows=$(grep -o "," <<<"$ids_flows" | wc -l)
	let num_ids_flows=$(expr $num_ids_flows + 1)
	count_done=0
	
	for j in $( eval echo {1..$num_ids_flows} )
	do
		flow=$(echo $ids_flows | awk -v c=$j -F',' '{ print $c}')
		print_log "Validar flujo $j => $flow"
		if [ -f "$path_status$flow" ]; then
			print_log "Archivo tiene:$(find $path_status -type f -name $flow | xargs cat)."
			if [ "$(find $path_status -type f -name $flow | xargs cat)" = "done" ]; then
				print_log "Marcar flujo como finalizado $flow"
				print_log ""
				let count_done=$(expr $count_done + 1)
			fi
		fi
	done
	
	print_log "Flujos $num_ids_flows vs $count_done Terminados"
	
	ctl_eid=$ctl_eid_origin
	if [ $num_ids_flows -eq $count_done ]; then
		#update_events "$status_executed" 11 59
		upsert_events 11 "$status_executed" 59
	else
		#update_events "$status_no_executed" 11 59
		upsert_events 11 "$status_no_executed" 59
	fi
	
	print_log "Finalizo correctamente el shell $(basename $0)"
	
	if [ "phase_all" != "$flow_continue" ]; then
		exit 0;
	fi

}
  
home
