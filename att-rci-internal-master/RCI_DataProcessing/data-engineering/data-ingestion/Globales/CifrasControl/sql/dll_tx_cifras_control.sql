CREATE EXTERNAL TABLE default.tx_cifras_control
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'
LOCATION '/data/RCI/stg/hive/staging/cifras_control/data'
TBLPROPERTIES ('avro.schema.url'='/data/RCI/stg/hive/staging/cifras_control/schemas/tx_cifras_control.avsc')
;