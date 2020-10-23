set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstrict;
insert overwrite table $schema.$table_name
partition(year,month,day)
select * from $schema.$table_name
where   year=$anio
and     month=$mes
and     day=$dia
