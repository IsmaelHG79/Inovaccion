impala-shell -i balancer.attdatalake.com.mx -d default -k --ssl --ca_cert=/opt/cloudera/security/ca-certs/CertToolkitCA.pem


export impala_conf="balancer.attdatalake.com.mx -d default -k --ssl --ca_cert=/opt/cloudera/security/ca-certs/CertToolkitCA.pem"
export schema=rci_network_db
export query="select count(*) from rci_network_db.tx_cifras_control"
impala-shell -i $impala_conf --database="$schema" -q "$query"

export impala_conf="balancer.attdatalake.com.mx -d default -k --ssl --ca_cert=/opt/cloudera/security/ca-certs/CertToolkitCA.pem"
export schema=rci_network_db
export query="CREATE TABLE dm_propiedades(idk string NOT NULL, articulo string, concepto string, descripcion string, director string, estado_fisico_usadonuevo string, etiqueta string, filedate integer, marca string, modeloversion string, nuevooenproceso string, productiondate string, productnumber string, proveedor string, responsable string, retiro string, serie string, solicitante string, sourceid string, swproductnumber string, tipo string, type string, typeofswunit string, typeofunit string, version string, val_retiro string, fecha_ins string, ida string, fecha_upd string, PRIMARY KEY(idk)) STORED AS KUDU;"
export queryf="CREATE TABLE dm_finanzas(idk string NOT NULL, categoria string, cip_areaok string, cip_categoria_budget1_jc string, cip_categoria_budget2_jc string, cip_categoriamastercipbudget string, cip_categoriamastplann string, cip_column_year string, cip_days string, cip_dias string, cip_mes string, cip_noubicado string, cip_polizacap string, cip_ref string, cip_sub_cta string, cip_tc20 string, cip_tipocuenta string, cip_ubicado string, cip_unidades string, consecpapeldetrabajo string, conspolsaldocuentas string, cuenta string, filedate integer, filename string, id string, legalentity string, libro string, mxn string, nofactura string, notransaccion string, nuevooenproceso string, oc string, ordendecompra string, parametrosdays string, subarea string, tarea string, tc string, tc18 string, unidades string, units_assigned string, usd string, valid string, vnl_asignado_mxn string, vnl_del_activo_mxn string, serie string, etiqueta string, articulo string, activo string, llave string, fecha_ins string, ida string, fecha_upd string, PRIMARY KEY(idk)) STORED AS KUDU;"
export queryne="CREATE TABLE cg_nemaster(acn string NOT NULL, activo int, etiqueta string, serie string, articulo string, retiro string, descripcion string, trazable int, ultima_actualizacion int, PRIMARY KEY(acn)) STORED AS KUDU;"
impala-shell -i $impala_conf --database="$schema" -q "$query"
impala-shell -i $impala_conf --database="$schema" -q "$queryf"
impala-shell -i $impala_conf --database="$schema" -q "$queryne"

