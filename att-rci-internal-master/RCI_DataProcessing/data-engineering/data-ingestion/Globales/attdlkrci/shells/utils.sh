#!/bin/bash
# set -euo pipefail
# set -x
#---------------------------------------------------------------#
#	Nombre:		utils.sh										#
#	Objetivo:	Contiene funciones de uso comun					#
#	Version:	1.0												#
#	Creador: 	ejesus											#
#	Fecha:		2019-11-04										#
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
file_properties=$1

#---------------------------------------------------------------#
#			Funcion que lee un archivo properties				#
#---------------------------------------------------------------#
read_properties()
{
	print_line
	echo "Lectura del archivo: $file_properties"
	print_log "Lectura del archivo: $file_properties"
	
	if [ -f "$file_properties" ]; then 
		echo "$file_properties listo para leer." 
		print_log "$file_properties listo para leer." 
		
		while IFS='=' read -r key value 
		do 
			#echo "$key => $value"
			#print_log "$key => $value"
			properties["$key"]="$value"
		done < "$file_properties"
	else 
		echo "$file_properties no encontrado."
		print_log "$file_properties no encontrado."
	fi
}

