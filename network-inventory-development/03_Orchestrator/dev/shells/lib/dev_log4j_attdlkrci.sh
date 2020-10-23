#!/bin/bash
# set -euo pipefail
# set -x
#---------------------------------------------------------------#
#	Nombre:		dev_log4j_attdlkrci.sh							#
#	Versión:	1.0.0                                           #
#	Objetivo:	Imprime logs de ejecución de shell				#
#	Autor: 	    ejesus											#
#	Vía de ejecución: Línea de comandos		                    #
#	Fecha:		04 de Noviembre de 2019							#
#	Area:		Datalake AT&T									#
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
type_execution=$1
file_excution=$2
environment=$3
home=$4
group_exec=$5
id_source=$6
number_param=$#

label_execution='Ejecucion_'
label_execution_hadoop='Datalake_'
label_execution_flow='Flow_'
label_execucion_liberacion='Liberacion_'
label_execucion_asset='AssetEngine_'
label_execucion_clean='ProcessClean_'
label_execution_monitor="Monitor_"
datetime=''
date=''
group=$group_exec

export path_files_logs=$home"logs/"
export path_files_lib=$home"shells/lib/"

#---------------------------------------------------------------#
#					Area para definir funciones					#
#---------------------------------------------------------------#

get_date_time_start(){
	date_start=$(date '+%Y%m%d')
	time_start=$(date '+%H%M%S')
	export datetime=${date_start}_${time_start}
}

get_date_time_logs(){
	export date=$(date '+%Y-%m-%d %H:%M:%S')
}

create_dir_logs(){
	get_label
	get_date_time_start
	name_file=${environment}_${label_execution}${label}${datetime}
	name_dir=${path_files_logs}${name_file}
	unset datetime
	
	#create dir for logs files
	[ ! -d "$name_dir" ] && mkdir -p $name_dir && chgrp -R ${group} ${name_dir} && chmod -R 770 $name_dir
	
	find $name_dir -type f -mtime +20 -print | xargs rm -f 2>/dev/null
	
	create_file_log $name_dir
	
	return $?
}

create_file_log(){
	path_general=$1
	get_date_time_start
	get_date_time_logs
	export name_file=${path_general}/${file_excution}_${datetime}.log
	current_path=$(echo $PWD)
	msg="Inicio ejecucion     : $date"
	msg2="Script               : $current_path/$file_excution.sh"
	print_banner
	echo -e "$msg\n$msg2" 2>&1 | tee -a $name_file
	print_line	
	print_log "El log generado es: $name_file"
	unset datetime date
}

print_log(){
	get_date_time_logs
	echo -e "$date .... $1" 2>&1 | tee -a $name_file
	unset date
}

print_log_length(){
	max=50
	msg=$1
	lon=${#msg}
	add=$(expr $max - $lon)
	add=${add#-}
	
	for i in $( ls ); do
		echo item: $i
	done
	
	get_date_time_logs
	echo -e "$date .... $1" 2>&1 | tee -a $name_file
	unset date
}

print_line(){
	echo -e "#---------------------------------------------------------------#" | tee -a $name_file
}

print_fill_line(){
	head="#---------------------------------------------------------------#"
	footer="#---------------------------------------------------------------#"
	fill="#"
	echo -e "$head\n$fill\n$1$fill\n$footer" | tee -a
	msg=printf "$fill%+10s$fill\n" "Tu mensaje"
	echo -e "$head\n $fill\n$footer" | tee -a
}

print_banner(){
	cat $path_files_lib/logo_att.ascii 2>&1 | tee -a $name_file
	cat $path_files_lib/logo_environment.ascii 2>&1 | tee -a $name_file
}

print_trace(){
	get_date_time_logs
	echo -e "$date .... $1" 2>&1 | tee -a "$name_file"_trace
	unset date
}

get_label(){
	case $type_execution in
	1)
		export label="$label_execution_hadoop$id_source"_
		;;
	2)
		export label="$label_execution_flow$id_source"_
		;;
	3)
		export label=$label_execucion_liberacion
		;;
	4)
		export label="$label_execucion_asset$id_source"_
		;;
	5)
		export label="$label_execucion_clean$id_source"_
		;;
	6)
		export label="$label_execution_monitor$id_source"_
		;;
	esac
}

create_dir_logs_sync(){
	get_label
	get_date_time_start
	name_file_sync=${environment}_${label_execution}${label}${datetime}
	name_dir_sync=${path_files_logs}${name_file_sync}
	unset datetime
	
	#create dir for logs files
	[ ! -d "$name_dir_sync" ] && mkdir -p $name_dir_sync && chgrp -R ${group} ${name_dir_sync} && chmod -R 770 $name_dir_sync
	
	find $name_dir_sync -type f -mtime +20 -print | xargs rm -f 2>/dev/null
	
	create_file_log_sync $name_dir_sync
	
	return $?
}

create_file_log_sync(){
	path_general=$1
	get_date_time_start
	get_date_time_logs
	export name_file_sync=${path_general}/${file_excution}_${datetime}.log
	current_path=$(echo $PWD)
	msg="Inicio ejecucion     : $date"
	msg2="Script               : $current_path/$file_excution.sh"
	print_banner
	echo -e "$msg\n$msg2" 2>&1 | tee -a $name_file_sync
	print_line	
	print_log "El log generado es: $name_file_sync"
	unset datetime date
}

print_log_sync(){
	get_date_time_logs
	echo -e "$date .... $1" 2>&1 | tee -a $name_file_sync
	unset date
}

print_line_sync(){
	echo -e "#---------------------------------------------------------------#" | tee -a $name_file_sync
}

print_banner_sync(){
	cat $path_files_lib/logo_att.ascii 2>&1 | tee -a $name_file_sync
	cat $path_files_lib/logo_environment.ascii 2>&1 | tee -a $name_file_sync
}
