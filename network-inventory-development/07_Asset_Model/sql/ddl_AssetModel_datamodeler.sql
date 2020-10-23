-- DDL Script to Build Asset Data Model for Repository Central Inventory (RCI)
-- Axity
-- May, 2020

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla que permite llevar el control de los execution id procesados asi como su 
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_metadata.cg_rci_business_identifiers
CREATE TABLE rci_db_inventory.cr_rci_ae_processed_sources
(
    id      					string	    comment 'identificador único asociado al elemento único',
    last_ctl_eid                string      comment 'ultimo execution id ejecutado por el asset engine',
    ctl_tid                     int         comment 'id de la tabla procesada',
    table_name                  string      comment 'nombre de la tabla procesada',
    ctl_created_by				string		comment 'Usuario que inserta el registro',
    ctl_created_on				string  	comment 'Fecha de alta del registro'
)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para registrar los business identifiers de los diferentes assets en el modelo de datos
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_metadata.cg_rci_business_identifiers
CREATE TABLE rci_db_metadata.cg_rci_business_identifiers
(
    id      					string	    comment 'identificador único asociado al elemento único',
    bid_name   					string		comment 'nombre del identificador único',
    evaluation_order            int         comment 'orden de evaluación para descalificar un elmento de red, cuando sus propiedades se repitan'
    ctl_created_by				string		comment 'Usuario que inserta el registro',
    ctl_created_on				BIGINT  	comment 'Fecha de alta del registro',
    primary key(id)
)
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para mapear los business identifiers encontrados en las fuentes de inventario añadidas, para homologar en el asset engine los asset identifiers
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_metadata.lnk_rci_business_identifiers
CREATE TABLE rci_db_metadata.lnk_rci_business_identifiers
(
    id      					string		comment 'identificador único asociado al link',
    ctl_tid  					int 		comment 'id de la fuente asociado al registro',
    bid_id                      string      comment 'id del business identifier',
    bid_source_col_name         string      comment 'nombre de la columna',
    ctl_created_by				string		comment 'Usuario que inserta el registro',
    ctl_created_on				BIGINT	    comment 'Fecha de alta del registro',
    primary key(id)
)
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para registrar los asset properties para el modelo de datos
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_metadata.cg_rci_asset_properties
CREATE TABLE rci_db_metadata.cg_rci_asset_properties
(
    id      					    string      comment 'identificador único para la propiedad',
    prop_name   				    string		comment 'nombre de la propiedad encontrada',
    ctl_created_by					string		comment 'Usuario que inserta el registro',
    ctl_created_on					BIGINT  	comment 'Fecha de alta del registro',
    primary key(id)
)
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para registrar las ligas que unen a los asset properties con las tablas de asset
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_metadata.lnk_rci_asset_properties
CREATE TABLE rci_db_metadata.lnk_rci_asset_properties
(
    id      					int		    comment 'identificador único asociado al link',
    ctl_tid  					int 		comment 'id de la tabla fuente asociado al registro',
    prop_id                     int         comment 'id asociado al catálogo de propiedades (core del mapeo)',
    prop_source_col_name        string      comment 'nombre de la columna como aparece en la fuente (core del mapeo)',
    ctl_created_by				string		comment 'Usuario que inserta el registro',
    ctl_created_on				BIGINT	    comment 'Fecha de alta del registro',
    primary key(id)
)
stored as kudu
tblproperties ('column_stats_accurate'='true', 'orc.compress'='snappy');

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para registrar los elementos únicos del inventario
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_inventory.cg_rci_asset_master
CREATE TABLE rci_db_inventory.cg_rci_asset_master
(
	id      					string	    comment 'identificador único de registro',
	acn			        		string		comment 'identificador incremental único de negocio',
	ctl_rid        				string     	comment 'identificador único del origen del registro en todo el datalake',
	ctl_created_by				string		comment 'Usuario que inserta el registro',
	ctl_created_on				BIGINT	    comment 'Fecha de alta del registro',
	primary key(id)
)
PARTITIONED BY (
  created_on BIGINT
)
STORED AS PARQUET;

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla de trabajo donde se realiza la limpieza y estandarización y agregación de los elementos
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_inventory.cr_rci_asset_trace
CREATE TABLE rci_db_inventory.cr_rci_asset_trace
(
    id      					string	    comment 'identificador único de la tabla',
    acn                         string      comment 'idennficador único de negocio del elemento',
    concat                      string      comment 'concatenado de las propiedades extraídas del elemento',
    count                       int         comment 'conteo de las propiedades identificadas',
    col_name                    string      comment 'columna por la que fue asignado el elemento de red',
    value                       string      comment 'valor de la columna en la fuente',
    type                        string      comment 'tipo de propiedad, bid (business identifier), prop (property), ctl (campo de control)',
    ctl_tid                     int         comment 'fuente procesada',
    found                       string      comment 'bid por el que el elemento fue encontrado',
    traceable                   int         comment 'identificador que indica si el elemento es trazable o no',
    ctl_created_by				string		comment 'Usuario que inserta el registro',
    ctl_created_on				string  	comment 'Fecha de alta del registro',
    primary key(id)
)
PARTITIONED BY (
  created_on BIGINT
)
STORED AS PARQUET;

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla que almacena las propiedades de los diferentes assets encontrados por el asset engine y las veces que los ha encontrado
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_inventory.cr_rci_asset_properties
CREATE TABLE rci_db_inventory.cr_rci_asset_properties
(
    id      					string	    comment 'identificador único asociado al link',
    acn                         string      comment 'identificador único del elemento',
    property                    string      comment 'nombre de la propiedad encontrada',
    value                       string      comment 'valor encontrado para la propiedad',
    count                       int         comment 'número de veces en las que se ha encontrado la propiedad',
    ctl_created_by				string		comment 'Usuario que inserta el registro',
    ctl_created_on				string  	comment 'Fecha de alta del registro',
    primary key(id)
)
STORED AS PARQUET;

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla que almacena los business identifiers de los diferentes assets encontrados por el asset engine y las veces que los ha encontrado
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_inventory.cr_rci_asset_identifiers
CREATE TABLE rci_db_inventory.cr_rci_asset_identifiers
(
    id      					string	    comment 'identificador único asociado al link',
    acn                         string      comment 'identificador único del elemento',
    bid                         string      comment 'nombre de la propiedad encontrada',
    value                       string      comment 'valor encontrado para la propiedad',
    count                       int         comment 'número de veces en las que se ha encontrado la propiedad',
    ctl_created_by				string		comment 'Usuario que inserta el registro',
    ctl_created_on				string	    comment 'Fecha de alta del registro',
    primary key(id)
)
STORED AS PARQUET;

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla que almacena los etapas del ciclo de vida en las que ha sido encontrado el elemento, así como su ubicación
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_inventory.cr_rci_asset_events
create table rci_db_inventory.cr_rci_asset_events
(
    id      					string	    comment 'identificador único asociado al link',
    acn                         string      comment 'identificador único del elemento',
    type                        string      comment 'etapa del ciclo de vida en donde fue encontrado el elemento',
    location                    string      comment 'ubicación encontrada para el ACN si es que se encuentra en la fuente, en caso de no encontrarse, será nula',
    ctl_rid                     string      comment 'RID asociado al registro en donde se encontró el elemento',
    ctl_created_by				string		comment 'Usuario que inserta el registro',
    ctl_created_on              string      comment 'fecha en la que es encontrado el elemento',
    primary key(id)
)
PARTITIONED BY(
    ctl_created_on BIGINT
)
STORED AS PARQUET;

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla que registra los Row ID procesados durante la ejecución del asset engine.
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_inventory.cr_rci_processed_records
create table rci_db_inventory.cr_rci_processed_records
(
    id      					string	    comment 'identificador único asociado al link',
    ctl_rid                     string      comment 'RID asociado al registro en donde se encontró el elemento',
    ctl_rfp                     string      comment 'Fingerprint asociado al registro procesado',
    ctl_created_on              string      comment 'fecha de proceso del registro'
    ctl_created_by				string		comment 'Usuario que inserta el registro',
    primary key(id)
)
PARTITIONED BY(
    ctl_created_on BIGINT
)
STORED AS PARQUET;

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tabla para registrar los elementos únicos del inventario
-- Ejecutar en impala
--DROP TABLE IF EXISTS rci_db_inventory.cr_rci_anomalies
CREATE TABLE rci_db_inventory.cr_rci_anomalies
(
	id      					string	    comment 'identificador único de registro',
    acn                         string      comment 'elemento asociado a la anomalía',
	ctl_rid        				string     	comment 'identificador único del origen del registro en todo el datalake',
	bids_affected               int       	comment 'numero de business identifiers afectados durante el proceso del asset engine',
    rprops_affected             int         comment 'numero de propiedades rechazadas durante el proceso del asset engine',
    ctl_created_by				string		comment 'Usuario que inserta el registro',
	ctl_created_on				string	    comment 'Fecha de alta del registro',
	primary key(id)
)
STORED AS PARQUET;