#set -xv
#!/bin/bash
#------------------------------------------------------------------------------------------------------------#
#	Nombre:		rci_run_flow_prime_manager.sh                                          			 	 		 #
#	Versión:	1.0.0                                          			 		                             #
#	Objetivo: 	Shell encargado de ejecutar el flujo de ingestion de la fuente Prime Manager				 #
#	Autor:		ejesus				                                                                         #
#	Vía de ejecución: crontab		                                                            	         #
#	Fecha:		2 de Marzo de 2020  	                                                           		 	 #
#	Area:		Datalake AT&T											                                     #
#------------------------------------------------------------------------------------------------------------#

if [ $# -lt 1 ]
	then
		echo '--------------------------------------------------------------'
		echo "Error: parametros"
		echo "usage: sh $(basename $0) environment [reset]"
		echo "environment          Ambiente en el que se desea ejecutar la fuente dev=Desarrollo, prd=Producción"
		echo "reset                Bandera opcional que indica si se debe reiniciar toda la ejecución del flujo, el valor debe ser r"
		echo '--------------------------------------------------------------'
	exit 1;
fi

#----------------------------------------------------------------------------------#
#						Leer parámetros para la ejecucion	   					   #
#----------------------------------------------------------------------------------#

export environment=$(echo $1 | awk '{print tolower($0)}')
export reset=$2

export path_rci=/home/raw_rci/attdlkrci/
export group_exec="inventario"
export time_wait=1
#Agregamos las lineas para poder utilizar el log
export path_log4jadc=$path_rci"shells"
. $path_log4jadc/log4j_attdlkrci.sh 2 'rci_run_flow_prime_manager' "$environment" "$path_rci" "$group_exec" "$table_execute"
create_dir_logs

print_log "environment            $environment"
print_log "reset                  $reset"

export path_home=$path_rci$environment/
export path_lib="$path_home"shells/lib/
export path_status=$path_home"status"/

#Establecer los ids de las tablas a ejecutar
export ids_flows="91"
export pending_flows=""

#Agregamos las lineas para poder utilizar la librería utils
. $path_lib/"$environment"_utils.sh

#----------------------------------------------------------------------------------#
#								Area de funciones								   #
#----------------------------------------------------------------------------------#
# Funcion que obtiene la fecha de ejecución del proceso
getDate() {		
	FECHA=$(date +%Y%m%d)
	print_log "Ejecutando shell $(basename $0) con fecha:$FECHA"
}

#----------------------------------------------------------------------------------#
#								Funcion principal del shell						   #
#----------------------------------------------------------------------------------#
home(){
	getDate
	print_log "*****************************************************"
	clean_flag_execution
	check_flag_execution
	
	print_log "$pending_flows"
	print_log ""
	
	if [ 0 -lt $p_flows ]; then
		for idx in $( eval echo {1..$p_flows} )
		do
			idp_execute=$(echo $pending_flows | awk -v c=$idx -F',' '{ print $c}')
			print_log "4. id $idx es $idp_execute"
			print_log "Ejecutar flujo $idp_execute"
			. $path_rci$enviroment/"shells"/"$enviroment"_rci_execute_ingestion_flow.sh "$idp_execute" &
			print_log "En ${time_wait} minutos se lanzará el próximo flujo..."
			print_log ""
			print_log ""
			sleep ${time_wait}m
		done
	fi
	
	print_log "Finalizo correctamente el shell $(basename $0)"
}
  
home
