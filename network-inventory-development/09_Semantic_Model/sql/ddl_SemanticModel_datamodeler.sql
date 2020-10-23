-- DDL Script to Build Semantic Data Model for Repository Central Inventory (RCI)
-- Axity
-- June, 2020

CREATE TABLE rci_db_inventory.dev_cr_rci_finance_snapshot (
  id STRING,
  mxn FLOAT,
  usd FLOAT,
  unidades FLOAT,
  vnl_activo_mxn FLOAT,
  vnl_asignado_mxn FLOAT,
  created_on STRING,
  date_id STRING
)
WITH SERDEPROPERTIES ('path'='hdfs://attdatalakehdfs/user/hive/warehouse/rci_db_inventory.db/dev_cr_rci_finance_snapshot', 'serialization.format'='1')
STORED AS PARQUET

CREATE TABLE rci_db_inventory.dev_cr_rci_control_view (
  ctl_tid INT,
  type_source STRING,
  lifecycle STRING,
  source_name STRING,
  table_name STRING,
  rows BIGINT,
  assets BIGINT,
  props BIGINT,
  match BIGINT,
  w_brand BIGINT,
  w_model BIGINT,
  w_location BIGINT,
  anomalies BIGINT,
  no_bids BIGINT,
  no_props BIGINT,
  updates BIGINT,
  n_brand BIGINT,
  n_model BIGINT,
  n_location BIGINT,
  date_id STRING,
  avg_bids DOUBLE,
  avg_props DOUBLE,
  created_on TIMESTAMP
)
WITH SERDEPROPERTIES ('path'='hdfs://attdatalakehdfs/user/hive/warehouse/rci_db_inventory.db/dev_cr_rci_control_view', 'serialization.format'='1')
STORED AS PARQUET



