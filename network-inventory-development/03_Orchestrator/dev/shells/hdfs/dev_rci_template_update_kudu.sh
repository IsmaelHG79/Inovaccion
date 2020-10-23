#set -xv
#!/bin/bash
#------------------------------------------------------------------------------------------------------------#
#	Nombre:		dev_rci_template_update_kudu.sh                                            			 		 #
#	Versión:	1.1.0                                          			 		                             #
#	Objetivo: 	Plantilla para actualizar una tabla de kudu desde pyspark o scala                            #
#	Autor:		ejesus                                                                                       #
#	Vía de ejecución: Línea de comandos		                                                            	 #
#	Fecha:		10 de Junio de 2020  	                                                           		 	 #
#	Area:		Datalake AT&T											                                     #
#------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------#
#						Leer parámetros para la ejecucion	   					   #
#----------------------------------------------------------------------------------#
echo "param1         $1"
echo "param2         $2"
echo "param3         $3"
echo "param4         $4"
echo "param5         $5"
echo "param6         $6"
echo "param7         $7"

#----------------------------------------------------------------------------------#
#				Definimos variables necesarias para la ejecucion	   		       #
#----------------------------------------------------------------------------------#

export environment="dev"
export group_exec="inventario"

mkdir -p /tmp/attdlkrci/shells 
chmod 777 /tmp/attdlkrci/shells
export PYTHON_EGG_CACHE=/tmp/attdlkrci/shells

#----------------------------------------------------------------------------------#
#	Variables de ambiente para obtener parametros necesarios para la ejecucion	   #
#----------------------------------------------------------------------------------#
# Variables para poder reintentar ejecutar una consulta en caso de desconexión
export intentos_t=1
export max_intentos_t=3
declare -A response_t
export impala_conf="balancer.attdatalake.com.mx -k --ssl"


#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#						Funciones por fases de ejecucion						             #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#


#---------------------------------------------------------------#
#	Funcion generica para ejecutar un query con impala-shell	#
# en caso de error, reintentará la ejecución max_intentos_t veces.#
#---------------------------------------------------------------#
execute_querys(){
	echo ""
	echo ""
	echo "*****************************************************"
	echo "Query_$3: $1."
	echo "*****************************************************"
	echo ""
	echo ""
	intentos_t=$4

	case $2 in
	*)
		echo "Ejecución normal del query"
		params=$(impala-shell -i $impala_conf --database="$5" -q "$1" -B)
		;;
	esac
	
	res=$?
	echo "cod_respuesta_Query_$3:$res"

	if [ $res -eq 0 ]; then
		echo "Resultado Query_$3:"
		echo "$params"
		echo "*****************************************************"
		echo ""
		echo ""
		#Almacenamos el valor obtenido del query en un arreglo
		response_t["$2"]=$params
		export intentos_t=0
	else
		if [ $intentos_t -eq $max_intentos_t ]; then
			export intentos_t=0
			echo "Se agotaron los $max_intentos_t intentos_t para Query_$3, terminará con error."
			echo "Revisar el log asociado para más detalle del error: $name_file"
			echo "#----------------------------------------------------------------------------------#"
			echo "#                          Punto de control 12: exit $res                          #"
			echo "#----------------------------------------------------------------------------------#"
			exit $res;
		fi
		let intentos_t=$(expr $intentos_t + 1 )	
		echo "Hubo un error en Query_$3, se reinterará la ejecucion. próximo Reintento:#$intentos_t."
		echo "Revisar el log asociado para más detalle del error: $name_file"
		echo "*****************************************************"
		echo ""
		echo ""
		execute_querys "$final_query" "$2" "$3" "$intentos_t" "$5" "$6"
	fi
}

functions_catalog(){
	case $7 in
	1 )
		echo "Ejecutar update de status_references"
		query_update_status_references $1 $2 $3 $4 $5 $6
		;;
	esac
}

query_update_status_references(){
	query="update $1.$2 set status='$3', updated_by='$4', updated_on=now() where ctl_tid=$5 and ctl_eid='$6' "
	execute_querys "$query" "update_t" 1000 "$intentos_t" "$1" ""
}

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
#						Cuerpo del shell, funcion principal   			             #
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#

#execute_querys "$param_query" "update_t" "template" "$intentos_t" "$param_schema" ""
functions_catalog $1 $2 $3 $4 $5 $6 $7

echo "Fin de ${environment}_rci_template_update_kudu"