# -*- coding: utf-8 -*-

# Version: 1.1.0

import sys
import os
import re
import uuid
import hashlib
import pyspark.sql.functions as f
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import HiveContext
from pyspark.sql.functions import arrays_zip,explode,explode_outer, col, split, regexp_extract, array_contains, regexp_replace,concat_ws, create_map, create_map, lit
from pyspark.sql import Window
from pyspark.sql.functions import size
from pyspark.sql.functions import concat_ws
from pyspark.sql.functions import split, trim
from pyspark.sql import functions as F
from pyspark.sql.functions import first, monotonically_increasing_id
from pyspark.sql.functions import udf
from pyspark.sql.types import LongType
from pyspark.sql.types import StringType ,BooleanType
from pyspark.sql.functions import map_keys,map_values
from pyspark.sql.functions import when, sum, avg, col,lower
from pyspark.sql import types as T
from functools import partial
from pyspark.sql.functions import substring, length, col, expr
from datetime import datetime #from funciones import suma
from functions_odk import * #from search_functions import *

# Global variables
global spark
global dirt

dirt=['iligible','no','no visi','no tiene activo fijo','sin numero activo fijo','n/n','no contiene activo fijo','no visible', 'sin etiqueta', 'ni visible', 'n/v','nv','ilegible','n/a', 's/a', 'na','no legible', 'no cuenta con activo fijo',
	'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene','no visble','nos visible','no visible',
	'no viaible', '.fhy', 'bxfj', 'cambiar la foto', 'hdjdjjdjfjfj', 'hdjrnnfjfjf', 'hffhthjih', 'hhyhigch',
	'hswkwjj', 'no aplica', 'no pude borrar elemnto', 'ns no visible', 'sin serie', 'sitio ibs no aplica', 'tutj',
	'uflp serie no visible', 'xxxxxxx', 'hsid# djdncg', 'sin informacion disponible', 'no tiene numero de serie',
	'hdkoe kg udkke' 'no se ve', 'ninguna', 'no tiene etiqueta y no se alcnaza a ver.', 'fue un error',
	'no legible', 'sin etiqueta', 'no disponible', 'no tiene', 'sin datos', 'num de serie no legible', 'etiqueta no legible', 'no cuenta con numero de serie',
	'no aplica por error se selecciona una tarjeta mas', 'enviado ya en reporte anterior', 'hlk', 'ninguno', 'la antena no tiene etiqueta por lo tanto tampoco numero de serie', 'no leguible',
	'sin targeta (por equivocacion se agrego este eslot 18 )', 'no cuenta con numeros de serie', 'enviados en reporte anterior .', 'sin etiqueta de numero de serie',
	'sin numero', 'sin informacion disponible', 'sin acceso a la antena', 'no tiene serie', 'sin acceso', 'no se pudo sacar ya que esta clausurado el sitio',
	'no se hizo por que no tenemos tarjeta se las llevo el ing de huawei gabriel lopez', 'sin informacion disponible', 'no aplica ta este segmento',
	'sin numero de serie visible', 'enviada en reporte  anterior', 'no hay antena', 'no se pudo sacar ya que esta clausurado y nos sacaron de sitio',
	'sin serie falta etiqueta', 'sin numero de serie no cuenta con la etiqueta', 'no tiene etiqueta', 'no existe', 'no serie visible', 'no hay bbu esta en resguardo por el ing gabriel lopez',
	'no legible', 'na', 'na hay  tarjeta', 'sin acceso al numero de serie', 'no visibles', 'uelp serie no visible', 'sin informacion disponible', 'sin tarjeta', 'fue un error de dedo no ay mas slot',
	'codigo no visible', 'num de serie no visible', 'sin informacion', 'no se aprecia el codigo', 'sin numero de serie', 'no trae la etiketa de numero de serie',
	'no aplica.', 'no se pudo sacar el numero  de serie ya q nos sacaron del sitio ya q esta clausurado', 'no tiene serie visible', 'no tiene serial ala vista',
	'no se tiene acceso a la antena', 'etiqueta no visible', 'no se puede tomar la foto porque tenemos la fan', "n/a  no se instalan antenas", 'no aplica sitio ibs',
	'sin numero', 'kcuvicuv', 'error no hay mas', 'no se puede apreciar el codigo', 'no aplica es ibs.', 'no  cuenta con etiquetas de n/s', 'esta ultima no vale','NaN','nan',
	'no hay tarjeta', 'esta no vale', 'falta', 'sin nÃºmero','s/n','0','n','k', 'sin número', 'sin número de serie', 'sin num de serie', 'sin etiqueta de activo fijo', 'sin activo', 'no contiene activó fijó','no tiene activó','N/V','visible']

# Special functions por odk's

# Special function to make a record for each serial or asset number that are concatenated into a single record in the odk99
# This rule is also defined by AT&T
def cleanSerieActivo(data):
	dataNew = data.where((F.col("serie").like("%|%")) | (F.col("activo")).like("%|%"))
	dataOld = data.where(~(F.col("serie").like("%|%")) | ~(F.col("activo")).like("%|%"))
	dataOld_2 = dataOld.select("cve_type","id_form","groups","element","created_on","updated_on","serie","activo","modelo","marca","ctl_file_date","ctl_file_name","orig_site_code","id_site",*cols)
	data1 = dataNew.withColumn("serie", processActivo("serie")).withColumn("activo", processActivo("activo"))\
	.withColumn("marca",processBrandModel(size(col("serie")),"marca")).withColumn("modelo",processBrandModel(size(col("serie")),"modelo")).cache()
	data2=data1.select("cve_type","id_form","groups","element","created_on","updated_on","serie","activo","modelo","marca","ctl_file_date","ctl_file_name","orig_site_code","id_site",\
	explode_outer(arrays_zip("serie","activo","marca","modelo")),*cols).cache()
	data3 = data2.select("cve_type","id_form","groups","element","created_on","updated_on","col.serie","col.activo","col.modelo","col.marca","ctl_file_date","ctl_file_name","orig_site_code","id_site",*cols)
	dataWell = dataOld_2.union(data3)
	return dataWell

# Special function for odk's that do not need special processing after the acquisition process
def post_normalTransformation(df_odk):
	return df_odk

# Special function to have make, model, series and assets in a single register that belongs to an element, applies only for odk38
def post_specialTransformation(df_odk):
	lista=[i.groups for i in df_odk.select('groups').distinct().collect()]
	newlist3 = get_groups(lista)
	dataframeDad = df_odk.filter(df_odk.groups.isin(newlist3)).select("cve_type","id_form","groups","marca","modelo")
	dfAll3=df_odk.withColumn("dad", extract('groups'))
	new_column_name_list= list(map(lambda x: x+"_2", dataframeDad.columns))
	dataframeDad_3 = dataframeDad.toDF(*new_column_name_list)
	dfAll3 = dfAll3.alias('dfAll3')
	dataframeDad_3 = dataframeDad_3.alias('dataframeDad_3')
	combination=dfAll3.join(dataframeDad_3,(dfAll3.id_form == dataframeDad_3.id_form_2)&(dfAll3.dad == dataframeDad_3.groups_2), "left").select('dfAll3.*','dataframeDad_3.marca_2', 'dataframeDad_3.modelo_2')
	columnas=['marca','modelo']
	for i in columnas:
		combination=combination.withColumn(i,discriminate(i,i+"_2")).drop(i+"_2").drop("dad").drop("id_form_2").drop("groups_2")
	return combination

# Special function for ODK'S that does not need pre-processing to start the acquisition process
def normal_transformation(df_odk):
	df_odk_0 = df_odk.withColumn("m_key",split(df_odk["map"],":").getItem(0)).withColumn("m_value",split(df_odk["map"],":").getItem(1)) \
	.withColumn("validate_key_dad",udf_valkeydad(split(df_odk["map"],":").getItem(1)))
	return df_odk_0

# Special function for pre-processing to start the acquisition process, only application for odk38
def especial_transformation(df_odk):
	df_odk_0 = df_odk.withColumn("groups",udf_transformgroup("groups")).withColumn("m_key",split(df_odk["map"],":").getItem(0)) \
	.withColumn("m_value",split(df_odk["map"],":").getItem(1)).withColumn("validate_key_dad",udf_valkeydad(split(df_odk["map"],":").getItem(1)))
	return df_odk_0

# Special function to look for elements from ODK APTMW
def search_odk12_ATPMW(subgrupo):
	for i in search_dic:
		if i['atributo'].find(subgrupo)!=-1:
			word=i['elemento']
			break
		else:
			word='Not Found'
	return word

#-- **********************************************--#
#--                                       Main                                    --#
#-- **********************************************--#
def main():
	print ("Start Process")
	listArgs = sys.argv
	print (listArgs)

	# Get parameters from orquestator
	numberODK = listArgs[1]
	types = listArgs[2]
	global cols
	cols = listArgs[3]
	parameters = listArgs[4]
	parameters_1 = parameters.split(',')
	sid = parameters_1[0]
	tid = parameters_1[1]
	eid = parameters_1[2]
	environment = listArgs[5]
	schema = listArgs[6]
	key_cols = listArgs[7]

	print ("#-- Parameters received for processing the ODK Acquisition --#")
	print ("ODK = " + numberODK)
	print ("ODK_VALUES = " + types)
	print ("ATTRIBUTES = " + cols)
	print ("ID_SOURCE = " + sid)
	print ("ID_TABLE = " + tid)
	print ("ID_EXECUTION = " + eid)
	print ("ENVIRONMENT = " + environment)
	print ("DB_SCHEMA = " + schema)
	print ("KEY_COLUMNS = " + key_cols)

	# Spark Configuration

	# Set configurations parameters
	conf = SparkConf().setAppName('{0}_odk_delta_{1}'.format(environment,numberODK))  \
		.setMaster('yarn') \
		.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
		.set("spark.sql.tungsten.enabled", "true") \
		.set("spark.io.compression.codec", "snappy") \
		.set("spark.sql.crossJoin.enabled", "true") \
		.set("spark.kryoserializer.buffer.mb","128") \
		.set("spark.sql.autoBroadcastJoinThreshold", -1) \
		.set("spark.sql.shuffle.partition","2001") \
		.set("spark.shuffle.compress","true") \
		.set("spark.shuffle.spill.compress","true" )
	spark = SparkSession.builder.config(conf=conf).getOrCreate()
	sc = spark.sparkContext
	sqlContext = HiveContext(sc)

	# Processing types
	b = types.split(',')
	string = """"""
	for i in b:
		string = string + "'" + i + "'" + ","
	string = string[:-1]
	types = string
	print ("New types")
	print (types)

	# Get columns and format them for processing
	cols = cols.split(',')
	print (cols)

	# Dictionaries for storage functions in memory

	# Load item dictionary when acquiring odk 12 is executed
	if str(numberODK) == "12":
		searching = spark.read.format("csv").option("header", "true").load("/user/raw_rci/attdlkrci/spark/ATPMW_patron_search.csv")
		search_collect = searching.collect()
		global search_dic
		search_dic = list(map(lambda x : {"atributo":x[0], "elemento":x[1]},search_collect))

	# Search functions dictionary
	functionsODK = {
	'99': search_odk99,'32': search_odk32,'37': search_odk37,'38': search_odk38,'12': search_odk12,'76': search_odk76, \
	'29': search_odk29,'28': search_odk28,'97': search_odk97,'98': search_odk98,'85': search_odk85,'95': search_odk95, \
	'34': search_odk34,'46': search_odk46,'55': search_odk55,'56': search_odk56,'58': search_odk58,'60': search_odk60, \
	'61': search_odk61,'63': search_odk63,'64': search_odk64,'65': search_odk65,'66': search_odk66,'69': search_odk69, \
	'72': search_odk72,'75': search_odk75,'83': search_odk83,'84': search_odk84,'108': search_odk108,'111': search_odk111, \
	'114': search_odk114,'115': search_odk115,'136': search_odk136 }

	# Clean key functions dictionary
	functionsODKClean = {
	'99': clean_str_odk99,'32': clean_str_odk32,'37': clean_str_odk37,'38': clean_str_odk38,'12': clean_str_odk12,'76': clean_str_odk76, \
	'28': clean_str_odk28,'29': clean_str_odk29,'34': clean_str_odk34,'46': clean_str_odk46,'55': clean_str_odk55,'56': clean_str_odk56, \
	'97': clean_str_odk97,'58': clean_str_odk58,'60': clean_str_odk60,'61': clean_str_odk61,'63': clean_str_odk63,'64': clean_str_odk64, \
	'65': clean_str_odk65,'66': clean_str_odk66,'69': clean_str_odk69,'72': clean_str_odk72,'75': clean_str_odk75,'83': clean_str_odk83, \
	'84': clean_str_odk84,'85': clean_str_odk85,'95': clean_str_odk95,'98': clean_str_odk98,'108': clean_str_odk108,'111': clean_str_odk111, \
	'114': clean_str_odk114,'115': clean_str_odk115,'136': clean_str_odk136 }

	# Pre-process for main algorithm
	transformationsBefore = {
	'99': normal_transformation,'32': normal_transformation,'37': normal_transformation,'38': especial_transformation,'12': normal_transformation, \
	'28': normal_transformation,'76': normal_transformation,'29': normal_transformation,'34': normal_transformation,'46': normal_transformation, \
	'97': normal_transformation,'55': normal_transformation,'56': normal_transformation,'58': normal_transformation,'60': normal_transformation, \
	'61': normal_transformation,'63': normal_transformation,'64': normal_transformation,'65': normal_transformation,'66': normal_transformation, \
	'69': normal_transformation,'72': normal_transformation,'75': normal_transformation,'83': normal_transformation,'84': normal_transformation, \
	'85': normal_transformation,'95': normal_transformation,'98': normal_transformation,'108': normal_transformation,'111': normal_transformation, \
	'114': normal_transformation,'115': normal_transformation,'136': normal_transformation }

	# Post-process for incremental algorithm
	transformationAfter = {
	'99': post_normalTransformation,'32': post_normalTransformation,'37': post_normalTransformation,'38': post_specialTransformation,'12': post_normalTransformation, \
	'28': post_normalTransformation,'76': post_normalTransformation,'29': post_normalTransformation,'34': post_normalTransformation,'46': post_normalTransformation, \
	'97': post_normalTransformation,'55': post_normalTransformation,'56': post_normalTransformation,'58': post_normalTransformation,'60': post_normalTransformation, \
	'61': post_normalTransformation,'63': post_normalTransformation,'64': post_normalTransformation,'65': post_normalTransformation,'66': post_normalTransformation, \
	'69': post_normalTransformation,'72': post_normalTransformation,'75': post_normalTransformation,'83': post_normalTransformation,'84': post_normalTransformation, \
	'85': post_normalTransformation,'95': post_normalTransformation,'98': post_normalTransformation,'108': post_normalTransformation,'111': post_normalTransformation, \
	'114': post_normalTransformation,'115': post_normalTransformation,'136': post_normalTransformation }

	# Clear repeated asset and series fields functions dictionary
	serieActivoClean = {
	'99': cleanSerieActivo,'32': post_normalTransformation,'37': post_normalTransformation,'38': post_normalTransformation,'12': cleanSerieActivo, \
	'28': post_normalTransformation,'76': post_normalTransformation,'29': post_normalTransformation,'34': post_normalTransformation,'46': post_normalTransformation, \
	'97': post_normalTransformation,'55': post_normalTransformation,'56': post_normalTransformation,'58': post_normalTransformation,'60': post_normalTransformation, \
	'61': post_normalTransformation,'63': post_normalTransformation,'64': post_normalTransformation,'65': post_normalTransformation,'66': post_normalTransformation, \
	'69': post_normalTransformation,'72': post_normalTransformation,'75': post_normalTransformation,'83': post_normalTransformation,'84': post_normalTransformation, \
	'85': post_normalTransformation,'95': post_normalTransformation,'98': post_normalTransformation,'108': post_normalTransformation,'111': post_normalTransformation, \
	'114': post_normalTransformation,'115': post_normalTransformation,'136': post_normalTransformation }

	# Define UDF'S
	global udf_valkeydad, udf_HashKey, udf_updated, udf_search_odkATPMW,udf_searchelement,udf_cleanstr,udf_transformgroup, extract, discriminate, modifyBrandModel
	udf_valkeydad = udf(validate_key_dad, BooleanType())                    # Key Dad function
	udf_HashKey = udf(hash_key,StringType())                                # Hash function
	udf_generate_acn = udf(generate_acn, StringType())                      # Uuid function
	udf_updated = udf(update_updated,StringType())                          # Clean update_on function
	udf_search_odkATPMW = udf(search_odk12_ATPMW, StringType())             # Search function odk 12 ATPMW
	udf_searchelement = udf(functionsODK[str(numberODK)], StringType())     # Search_element
	udf_cleanstr = udf(functionsODKClean[str(numberODK)], StringType())     # Clean key field
	udf_transformgroup = udf(transform_ODK38, StringType())                 # Pre-process groups field for odk 38
	extract = udf(extraer, StringType())                                    # Pre-process for odk38
	discriminate = udf(discriminateColumns, StringType())                   # Post-process for odk38
	modifyBrandModel = udf(modify_brand,StringType())                       # function for clean marca and modelo fields
	global processActivo
	processActivo = udf(process_activo,ArrayType(StringType()))             # function for repeated serie and activo fields apply only odk99
	global processBrandModel
	processBrandModel = udf(process_marca_modelo,ArrayType(StringType()))   #function for repeated marca annd modelo fields apply only odk99

	# Define tables to use

	# Define raw table
	if str(environment) == "dev":
		table_odk = str(schema)+"."+str(environment)+"_tx_rci_odk"
	else:
		table_odk = str(schema)+".tx_rci_odk"
	print(table_odk)

	# Define old odk table
	if str(environment) == "dev":
		table_old = str(schema) + "." +str(environment) + "_ds_rci_odk_" + str(numberODK)
	else:
		table_old = str(schema) + "." +"ds_rci_odk_" + str(numberODK)
	print(table_old)

	# Define statistics table
	if str(environment)=="dev":
		table_cifras = str(schema)+".cr_rci_statistics_tst"
	else:
		table_cifras = str(schema)+".cr_rci_statistics"
	print(table_cifras)

	# Extraction of information required for processing

	# Extract ODK by cve_type from raw layer
	df_odk = spark.sql("""
		SELECT a.*
		FROM """ + str(table_odk) + """ a
		inner join (select max(ctl_file_date) as maxdate from """ + str(table_odk) + """) b
		on a.ctl_file_date = b.maxdate
		WHERE a.cve_type in (""" + types + """)""").cache().withColumn("updated_on",udf_updated("updated_on")).cache()
	df_read = df_odk.count()
	print(df_read)

	# Extract location codes properties for ODK
	df_panda = spark.sql("""
		SELECT cast(id as string) as id ,cve_type, orig_site_code, cast(id_site as string) as id_site 
		FROM inventario.raw_panda_eform_site
		WHERE cve_type in (""" + types + """)""").cache()

	#Extract old table
	try:
		df_stg = spark.sql("""
			SELECT ctl_key as ctl_key_old, ctl_atb as ctl_atb_old, max(ctl_ts) as ctl_ts_old
			FROM """ + str(table_old) + """ group by ctl_key, ctl_atb""").cache()
		table_old_exist = True
	except:
		table_old_exist = False

	# Main Algorithm

	# Delimit map field values
	if str(numberODK) == "38":
		df_odk_0 = transformationsBefore[str(numberODK)](df_odk)
	else:
		df_odk_0 = df_odk.withColumn("m_key",split(df_odk["map"],":").getItem(0)) \
		.withColumn("m_value",split(df_odk["map"],":").getItem(1)) \
		.withColumn("validate_key_dad",udf_valkeydad(split(df_odk["map"],":").getItem(1)))

	# Only for ODK 12
	if str(numberODK) == "12":
		df_odk_atpmw_0 = df_odk_0.where(F.col("cve_type")=="ATPMW")
		df_odk_0 = df_odk_0.where(F.col("cve_type")!="ATPMW")

	# Groups the values ​​and generates lists of the values ​​contained in each grouping
	df_odk_1 = df_odk_0.groupBy("cve_type","id_form","groups","ctl_file_date","ctl_file_name","created_on","updated_on") \
	.agg(F.collect_list("sub_group").alias("sub_group"), \
	F.collect_list("m_key").alias("key"), \
	F.collect_list("m_value").alias("value"),F.collect_list("map").alias("map"), \
	F.collect_list("validate_key_dad").alias("validate_key"),\
	F.first(when(F.col("validate_key_dad")==True, \
	F.col("m_key").cast("string")).otherwise("root")).alias("key_dad")).cache()

	# The search for each element is performed and the lists are decomposed by records
	df_odk_2 = df_odk_1.withColumn("element", udf_searchelement('cve_type','groups','sub_group','map','key','value')) \
	.select("cve_type","id_form","groups","ctl_file_date","ctl_file_name","key_dad","element","created_on","updated_on", \
	explode_outer(arrays_zip("sub_group","key","value","validate_key"))) \
	.select("cve_type","id_form","groups","ctl_file_date","ctl_file_name","key_dad","element","created_on","updated_on", \
	"col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key").cache()

	# Processing only for odk 12
	if str(numberODK) == "12":
		df_odk_atpmw_1 = df_odk_atpmw_0.withColumn("element", udf_search_odkATPMW('sub_group'))
		df_odk_atpmw_2 = df_odk_atpmw_1.groupBy("cve_type","id_form","groups","element","ctl_file_date","ctl_file_name", \
		"created_on","updated_on").agg(F.collect_list("sub_group").alias("sub_group"),F.collect_list("m_key").alias("key"), \
		F.collect_list("m_value").alias("value"),F.collect_list("map").alias("map"), \
		F.collect_list("validate_key_dad").alias("validate_key"),F.first(when(F.col("validate_key_dad")==True, \
		F.col("m_key").cast("string")).otherwise("root")).alias("key_dad")).cache()
		df_odk_atpmw_3 = df_odk_atpmw_2.select("cve_type","id_form","groups","ctl_file_date","ctl_file_name", \
		"key_dad","element","created_on","updated_on",explode_outer(arrays_zip("sub_group","key","value","validate_key"))) \
		.select("cve_type","id_form","groups","ctl_file_date","ctl_file_name","key_dad","element","created_on","updated_on", \
		"col.sub_group",lower(col("col.key")).alias("key"),lower(col("col.value")).alias("value"),"col.validate_key").cache()
		df_odk_2 = df_odk_atpmw_3.union(df_odk_2).cache()

	# Pivot the values ​​columnarly
	df_odk_3 = df_odk_2.where(F.col("validate_key")==False).drop("validate_key").withColumn("key_clean",udf_cleanstr("key")) \
	.drop("key").groupBy("cve_type","id_form",'groups',"ctl_file_date","ctl_file_name","key_dad","element","created_on","updated_on") \
	.pivot("key_clean").agg(concat_ws("|",F.collect_list("value"))).cache()

	# Apply an upper case of the business key fields and remove junk columns
	cols_to = "keydad|Irving.garcia@wfinet.com.mx|Fernando.mendoza@wfinet.com.mx|cesar.uribe@wfinet.com.mx|claudia.resendiz@wfinet.com.mx|eduardo.torres.1@huawei.com|eduardo.torres1@huawei.com|eduardo.torres@Huawei.com|eduardo.torres@huawei.com|emmanuel.estrada.ortiz@huawei.com|fernando.martinez@wfinet.com.mx|fralvarezh@gmail.com|irving.garcia@wfinet.com.mx|jafet.vera@wfinet.com.mx|javiair.jjr@gmail.com|jmgalvanv@hotmail.com|jose.morales@wfinet.com.mx|josue.jimenez@wfinet.com.mx|luis.quintero@tinnova.mx|luis.rodriguez@wfinet.com.mx|mauroF.Diaz@huawei.com|maurof.diaz@huawei.com|miguel.acosta@huawei.com|pedro.montalvo@wfinet.com.mx|raul.perez810823@gmail.com|sergio.paz@huawei.com"
	columns_a_borrar = cols_to.split('|')
	if str(numberODK)=="76" or str(numberODK)=="29" or str(numberODK)=="61":
		key_columns = ["id_form","cve_type","groups","element"]
		df_odk_4 = df_odk_3.drop(*columns_a_borrar).select("cve_type","id_form","groups","ctl_file_date","ctl_file_name", \
		"element","created_on","updated_on",*cols).cache()
	elif str(numberODK)=="46" or str(numberODK)=="83" or str(numberODK)=="84" or str(numberODK)=="85":
		key_columns = ["id_form","cve_type","groups","serie","element"]
		df_odk_4 = df_odk_3.drop(*columns_a_borrar).withColumn("serie", f.upper(col("serie"))) \
		.select("cve_type","id_form","groups","ctl_file_date","ctl_file_name", \
		"element","created_on","updated_on","serie",*cols).cache()
	elif str(numberODK) == "136":
		key_columns = ["id_form","cve_type","groups","activo","element"]
		df_odk_4 = df_odk_3.drop(*columns_a_borrar).withColumn("activo", f.upper(col("activo"))) \
		.select("cve_type","id_form","groups","ctl_file_date","ctl_file_name", \
		"element","created_on","updated_on","activo",*cols).cache()
	elif str(numberODK) == "55" or str(numberODK) == "28":
		key_columns = ["id_form","cve_type","groups","serie","modelo","element"]
		df_odk_4 = df_odk_3.drop(*columns_a_borrar).withColumn("serie", f.upper(col("serie"))) \
		.select("cve_type","id_form","groups","ctl_file_date","ctl_file_name", \
		"element","created_on","updated_on","serie","modelo",*cols).cache()
	elif str(numberODK) == "60" or str(numberODK)=="63" or str(numberODK)=="75" or str(numberODK)=="37":
		key_columns = ["id_form","cve_type","groups","serie","activo","modelo","element"]
		df_odk_4 = df_odk_3.drop(*columns_a_borrar).withColumn("activo", f.upper(col("activo"))) \
		.withColumn("serie", f.upper(col("serie"))).select("cve_type","id_form","groups","ctl_file_date","ctl_file_name", \
		"element","created_on","updated_on","serie","activo","modelo",*cols).cache()
	elif str(numberODK) == "99" or str(numberODK)=="56" or str(numberODK)=="38":
	    key_columns = ["id_form","cve_type","groups","serie","activo","marca","modelo"]
	    df_odk_4 = df_odk_3.drop(*columns_a_borrar).withColumn("activo", f.upper(col("activo"))) \
	    .withColumn("serie", f.upper(col("serie"))).select("cve_type","id_form","groups","ctl_file_date","ctl_file_name", \
	    "element","created_on","updated_on","serie","activo","modelo","marca",*cols).cache()
	else:
		key_columns = ["id_form","cve_type","groups","serie","activo","marca","modelo","element"]
		df_odk_4 = df_odk_3.drop(*columns_a_borrar).withColumn("activo", f.upper(col("activo"))) \
		.withColumn("serie", f.upper(col("serie"))).select("cve_type","id_form","groups","ctl_file_date","ctl_file_name", \
		"element","created_on","updated_on","serie","activo","modelo","marca",*cols).cache()

	# Assign the site code to each id_form
	df_odk_4 = df_odk_4.alias('df_odk_4')
	df_panda = df_panda.alias('df_panda')
	df_odk_5 = df_odk_4.join(df_panda, (df_odk_4.id_form == df_panda.id) & (df_odk_4.cve_type == df_panda.cve_type), "left_outer") \
	.select('df_odk_4.*','df_panda.orig_site_code','df_panda.id_site').na.fill("").cache()

	# Post-processing onlu for fix odk38
	df_odk_6 = transformationAfter[str(numberODK)](df_odk_5).cache()

	# Post-processing only for fix odk99
	df_odk_7 = serieActivoClean[str(numberODK)](df_odk_6).cache()

	# Post-processing only for fix marca and modelo fields
	cols_for_evaluate=df_odk_7.columns
	if "modelo" in cols_for_evaluate and "marca" in cols_for_evaluate:
		print("marca y modelo")
		df_odk_8 = df_odk_7.withColumn("marca",modifyBrandModel("marca")).withColumn("modelo",modifyBrandModel("modelo")).cache()
	elif "modelo" in cols_for_evaluate:
		print("modelo")
		df_odk_8 = df_odk_7.withColumn("modelo",modifyBrandModel("modelo")).cache()
	elif "marca" in cols_for_evaluate:
		print("marca")
		df_odk_8 = df_odk_7.withColumn("marca",modifyBrandModel("marca")).cache()
	else:
		print("ninguno")
		df_odk_8 = df_odk_7

	# Control fields

	# Add control fields to the processed information
	df_odk_9 = df_odk_8.withColumn("ctl_tid", lit(str(tid)).cast("int")) \
		.withColumn("ctl_sid", lit(str(sid)).cast("int")) \
		.withColumn("ctl_eid", lit(str(eid))) \
		.withColumn("ctl_file_date_new", col("ctl_file_date").cast("int")) \
		.withColumn("ctl_file_name_new", col("ctl_file_name").cast("string")) \
		.drop("ctl_file_date","ctl_file_name","ctl_rid","ctl_rfp") \
		.withColumnRenamed("ctl_file_date_new","ctl_file_date") \
		.withColumnRenamed("ctl_file_name_new","ctl_file_name").na.fill("").cache()

	# Get columns to hash code
	dftable = map( lambda x: x.lower(),df_odk_9.columns)
	ctl_columns = ["ctl_file_name","ctl_file_date","ctl_eid","ctl_tid","ctl_sid","created_on","updated_on"]
	atb_columns = key_columns+ctl_columns
	columns_to_rfp = [x for x in dftable if x not in ctl_columns]
	columns_to_key = [x for x in dftable if x in key_columns]
	columns_to_atb = [x for x in dftable if x not in atb_columns]

	# Concat columns to hash codec
	if str(numberODK) == "99" or str(numberODK) == "56":
	    df_odk_10 = df_odk_9.withColumn("ctl_rfp_hash", f.concat(*columns_to_rfp)) \
	        .withColumn("ctl_rid", udf_generate_acn()) \
	        .withColumn("ctl_key_hash", f.concat(*columns_to_key)) \
	        .withColumn("ctl_atb_hash", f.concat("updated_on")).cache()
	else:
		df_odk_10 = df_odk_9.withColumn("ctl_rfp_hash", f.concat(*columns_to_rfp)) \
			.withColumn("ctl_rid", udf_generate_acn()) \
			.withColumn("ctl_key_hash", f.concat(*columns_to_key)) \
			.withColumn("ctl_atb_hash", f.concat(*columns_to_atb)).cache()

	# Generate hash code with concat columns
	df_odk_end = df_odk_10.withColumn("ctl_rfp", udf_HashKey(col("ctl_rfp_hash"))) \
		.withColumn("ctl_key", udf_HashKey(col("ctl_key_hash"))) \
		.withColumn("ctl_atb", udf_HashKey(col("ctl_atb_hash"))) \
		.withColumn("ctl_ts", lit(datetime.now()).cast("string")) \
		.drop("ctl_rfp_hash","ctl_key_hash","ctl_atb_hash").drop_duplicates(subset=['ctl_key']).cache()
	df_processed = df_odk_end.count()

	# Incremental Algorithm

	if table_old_exist:
		print("Incremental phase will be processed")

		# Validate if exists
		df_incremental = df_odk_end.join(df_stg, df_odk_end.ctl_key == df_stg.ctl_key_old, "left_outer").cache()
		#df_incremental.count()

		# Get only insert rows
		df_insert = df_incremental.where(F.col("ctl_key_old").isNull()).drop("ctl_key_old","ctl_atb_old","ctl_ts_old").cache()
		df_ins = df_insert.count()
		print(df_ins)

		# Get only update rows
		df_update = df_incremental.where(F.col("ctl_key_old").isNotNull() & (F.col("ctl_atb") != F.col("ctl_atb_old"))) \
		.drop("ctl_key_old","ctl_atb_old","ctl_ts_old").cache()
		df_upd = df_update.count()
		print(df_upd)

		# Union insert rows with update rows
		df_carga = df_insert.union(df_update)
		df_val = df_carga.count()

		# Insert rows in table from incremental process
		if df_val == 0:
			print("No records to process")
		else:
			print("Records to process")
			print(table_old)
			df_carga.write.format("parquet").mode("append").saveAsTable(str(table_old))
	else:
		print("Full phase will be processed")

		# Insert rows to new table from full process
		df_odk_end.write.format("parquet").mode("overwrite").saveAsTable(str(table_old))

	# Get statistics information

	if table_old_exist:
		print("Incremental phase will be processed to statistics")
		df_cifras = df_odk_end.withColumn("num",lit(1)) \
		.groupBy("ctl_tid","ctl_sid","ctl_eid","ctl_file_name","ctl_file_date").agg({"num":"sum"}) \
		.withColumn("ctl_tid",col("ctl_tid").cast("int")).withColumn("ctl_sid",col("ctl_sid").cast("int")) \
		.withColumn("ctl_file_date",col("ctl_file_date").cast("int")) \
		.withColumn("dateload", regexp_replace(lit(datetime.now()).cast("date"),"-","").cast("int")) \
		.withColumn("rowprocessed", lit(df_processed).cast("int")).withColumn("read_count", lit(df_read).cast("int")) \
		.withColumn("insert_count", lit(df_ins).cast("int")).withColumn("update_count",lit(df_upd).cast("int")) \
		.select("ctl_tid","ctl_sid","ctl_eid","dateload","ctl_file_date","ctl_file_name","rowprocessed","read_count","insert_count","update_count")
		df_cifras.write.format("hive").mode("append").saveAsTable(str(table_cifras))
	else:
		print("Full phase will be processed to statistics")
		df_cifras = df_odk_end.withColumn("num",lit(1)) \
		.groupBy("ctl_tid","ctl_sid","ctl_eid","ctl_file_name","ctl_file_date").agg({"num":"sum"}) \
		.withColumn("ctl_tid",col("ctl_tid").cast("int")).withColumn("ctl_sid",col("ctl_sid").cast("int")) \
		.withColumn("ctl_file_date",col("ctl_file_date").cast("int")) \
		.withColumn("dateload", regexp_replace(lit(datetime.now()).cast("date"),"-","").cast("int")) \
		.withColumn("rowprocessed", lit(df_processed).cast("int")).withColumn("read_count", lit(df_read).cast("int")) \
		.withColumn("insert_count", lit(df_processed).cast("int")).withColumn("update_count",lit(0).cast("int")) \
		.select("ctl_tid","ctl_sid","ctl_eid","dateload","ctl_file_date","ctl_file_name","rowprocessed","read_count","insert_count","update_count")
		df_cifras.write.format("hive").mode("append").saveAsTable(str(table_cifras))

	print ("Odk execution finished = " + str(numberODK))
	sc.stop()
	spark.stop()

if __name__ == "__main__":
	main()
