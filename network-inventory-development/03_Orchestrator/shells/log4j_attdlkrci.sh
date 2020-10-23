#!/bin/bash
# set -euo pipefail
# set -x
#---------------------------------------------------------------#
#	Nombre:	    log4j_attdlkrci.sh				                #
#	Versión:	1.0.0                                           #
#	Objetivo:	Imprime logs de ejecución de shell			    #
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
#			    Area para definir variables globales				 #
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
datetime=''
date=''
group=$group_exec

export path_files_logs=$home"logs/"
export path_files_shells=$home"shells/"

#---------------------------------------------------------------#
#					    Area para definir funciones					 #
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
	case $type_execution in
	1)
		label="$label_execution_hadoop$id_source"_
		;;
	2)
		label="$label_execution_flow$id_source"_
		;;
	3)
		label=$label_execucion_liberacion
		;;
	esac
	
	get_date_time_start
	log_file_base=${environment}_${label_execution}${label}${datetime}
	name_dir=${path_files_logs}${log_file_base}
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
	export log_file_base=${path_general}/${file_excution}_${datetime}.log
	current_path=$(echo $PWD)
	msg="Inicio ejecucion     : $date"
	msg2="Script                 : $current_path/$file_excution.sh"
	print_banner
	echo -e "$msg\n$msg2" 2>&1 | tee -a $log_file_base
	print_line	
	print_log "El log generado es: $log_file_base"
	unset datetime date
}

print_log(){
	get_date_time_logs
	echo -e "$date .... $1" 2>&1 | tee -a $log_file_base
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
	echo -e "$date .... $1" 2>&1 | tee -a $log_file_base
	unset date
}

print_line(){
	echo -e "#---------------------------------------------------------------#" | tee -a $log_file_base
}

print_fill_line(){
	head="#---------------------------------------------------------------#"
	footer="#---------------------------------------------------------------#"
	fill="#"
	echo -e "$head\n$fill\n$1$fill\n$footer" | tee -a
	#echo -e "$head\n$fill Tu mensaje$fill\n$footer" | tee -a
	msg=printf "$fill%+10s$fill\n" "Tu mensaje"
	echo -e "$head\n $fill\n$footer" | tee -a
	#echo -e "$head echo $fill $1 $fill echo $footer" | tee -a $log_file_base
	
}

print_banner(){
	cat $home$environment/"shells/lib/logo_att.ascii" 2>&1 | tee -a $log_file_base
}