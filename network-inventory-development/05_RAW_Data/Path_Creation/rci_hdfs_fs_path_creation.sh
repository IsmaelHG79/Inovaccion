#!/bin/bash

# Shell script to create hdfs and file system directories for RCI Inventory at AT&T
# Var initialization

#RAW = 'AF'
#STG = 'af'
#CTLDIR = 'ctrl_tx_rci_fixed_asset'
#FSDIR = 'tx_rci_fixed_asset'

echo "Introduce las siglas para la capa de RAW TEMP"
read RAW
echo "Introduce las siglas para la capa RAW HIVE External"
read STG
echo "Introduce el nombre del directorio para cifras control"
read CTLDIR
echo "Introduce el nombre del directorio para las rutas de los esquemas"
read FSDIR

# RAW path hdfs

hdfs dfs -mkdir -p /data/RCI/inv_raw/$RAW/data
hdfs dfs -mkdir -p /data/RCI/inv_raw/$RAW/schema

# RSTG path for External Tables at HIVE this is RAW 

hdfs dfs -mkdir -p /data/RCI/inv_stg/hive/staging/$STG
hdfs dfs -mkdir -p /data/RCI/inv_stg/hive/work/ctl/$CTLDIR

# Files for processed sources and not processed

mkdir -p /files/working_dir/RCI_schemas/$FSDIR/all/
mkdir -p /files/working_dir/RCI_schemas/$FSDIR/processed

