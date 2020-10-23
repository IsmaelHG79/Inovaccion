select distinct 
'<tr><th>' , c.datasetname as Tabla , 
'</th><th>', c.sourceid as Desc_tabla , 
'</th><th>', c.filedate as Fecha_archivo , 
'</th><th>', c.filename as Nombre_archivo , 
'</th><th>', c.read_count as Total_archivo , 
'</th><th>', c.insert_count as Total_insertados , 
'</th><th>', c.update_count as Total_actualizados , 
'</th><th>', c.delete_count as Total_borrados , 
'</th><th>', c.dateload as Fecha_carga_dlk , 
'</th></tr>'
from $schema.$tabla_cifras c
inner join (
select datasetname, max(dateload) as dateload from $schema.$tabla_cifras where datasetname='$table_name' 
group by datasetname
) cm
on c.datasetname = cm.datasetname
and c.dateload = cm.dateload
order by c.filedate asc 