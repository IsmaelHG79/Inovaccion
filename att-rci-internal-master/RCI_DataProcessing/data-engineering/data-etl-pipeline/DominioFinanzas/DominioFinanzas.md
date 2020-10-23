# Dominio Finanzas

El dominio Finanzas se define como todos los datos que se refieren a la administración del dinero de la compañía, estos incluyen actividades como gastos, inversiones, préstamos, presupuestos y desempeño de proyectos. El dominio se construye a partir de campos que existen en seis tablas distintas en el DataLake y su proceso de creación es el siguiente:

![Flujo de creación dle dominio Finanzas][img1]
*Diagrama 1. Proceso de construcción del dominio Finanzas*

## Descripción del proceso

A continuación se describe cada uno de los pasos mostrados en el diagrama 1.

1. Obtener la siguiente estructura de datos de la fuente “CIP Finanzas” desde la tabla tx_finance_cip:

**CAMPO**|**TIPO DE DATO**
:-----:|:-----:
column\_000|string
conspolsaldocuentas|string
cuenta|string
legalentity|string
libro|string
mxn|string
nofactura|string
notaalcomprador|string
notransaccion|string
noubicado|string
ordendecompra|string
polizacap|string
sub\_cta|string
tc|string
tc18|string
tc20|string
tipocuenta|string
ubicado|string
unidades|string
units\_assigned|string
usd|string

2. Obtener la estructura de datos de la fuente “Almacén Segregación” desde la tabla tx_almacen_inventory:

**CAMPO**|**TIPO DE DATO**
:-----:|:-----:
serie|string
etiqueta|string
mxn/mxn\_1|string
orden\_de\_compra|string
orden\_de\_compra\_1| 
usd/usd\_1|string
cantidad|string
bolsa|string
prestamo\_autorizado\_por|string
udm|string
usd\_octubre|string
usd\_sep19|string
revision\_finanza|string
control\_de\_prestamos|string

3.	Obtener la estructura de datos de la fuente “Activo Fijo” desde la tabla tx_fixed_asset:

**CAMPO**|**TIPO DE DATO**
:-----:|:-----:
serie|string
etiqueta|string
unidades|string
units\_assigned|string

4. Obtener la estructura de datos de la fuente “Salida Almacén” desde la tabla tx_wlog:

**CAMPO**|**TIPO DE DATO**
:-----:|:-----:
serie|string
activo|string
orden\_compra|string
cantidad|string
units|string

5. Realizar un UNION ALL de las estructuras de datos obtenidas del PASO1, PASO2, PASO3 y PASO4. De esta manera se completaran los campos faltantes para obtener la siguiente estructura de datos:

**UNION ALL**|**PASO1**|**PASO2**|**PASO3**|**PASO4**
:-----:|:-----:|:-----:|:-----:|:-----:
bolsa| |bolsa| | 
cantidad| |cantidad| |cantidad
column\_000|column\_000| | | 
conspolsaldocuentas|conspolsaldocuentas| | | 
control\_de\_prestamos| |control\_de\_prestamos| | 
cuenta|cuenta| | | 
legalentity|legalentity| | | 
libro|libro| | | 
mxn|mxn|mxn/mxn\_1| | 
nofactura|nofactura| | | 
notaalcomprador|notaalcomprador| | | 
notransaccion|notransaccion| | | 
noubicado|noubicado| | | 
ordendecompra|ordendecompra|orden\_de\_compra/| |orden\_compra
 | |orden\_de\_compra\_1| | 
polizacap|polizacap| | | 
prestamo\_autorizado\_por| |prestamo\_autorizado\_por| | 
revision\_finanza| |revision\_finanza| | 
sub\_cta|sub\_cta| | | 
tc|tc| | | 
tc18|tc18| | | 
tc20|tc20| | | 
tipocuenta|tipocuenta| | | 
ubicado|ubicado| | | 
udm| |udm| | 
unidades|unidades| |unidades|units
units\_assigned|units\_assigned| |units\_assigned| 
usd|usd|usd/usd\_1| | 
usd\_octubre| |usd\_octubre| | 
usd\_sep19| |usd\_sep19| | 

6. A continuación es necesario aplicar las siguientes reglas de limpieza al resultado del PASO5. Para todas las columnas aplican las siguientes reglas:

- Pasar todas las descripciones y nombres a mayúsculas para evitar repetidos en mayúsculas y minúsculas.
- 	Eliminar espacios en blanco en todos los campos para descartar repetidos.
- Cuando en el campo solamente se encuentren los valores '-', 'N/A', '  ' o NA'' reemplazarlos por null.
- Eliminar acentos.
- Si los encabezados requieren una separación, usar un guión bajo '_' simulando el espacio.

Posteriormente se aplican reglas específicas de limpieza para algunos de los campos, el detalle completo de las reglas puede consultarse en el documento Reglas de Limpieza. Las reglas de limpieza se han tomado directamente del análisis exploratorio de datos de las fuentes (EDA) que conforman el dominio.

**No.**|**CAMPO**|**REGLA DE LIMPIEZA**
:-----:|:-----:|:-----:
CIP-9|mxn|Eliminar caractér ')'
CIP-9 | mxn |Remplazar el caractér '(' por '-'
CIP-9 |mxn |Eliminar espacios en blanco intermedios
CIP-7|numeroetiqueta|Cambiar nombre a 'etiqueta'
CIP-8|numeroserie|Cambiar nombre a 'serie'
WLOG-1|activo|Cambiar nombre de campo a ‘articulo’
WLOG-2|sku\_oracle|Cambiar nombre de campo a ‘etiqueta’

7. Aplicar reglas de transformación de la tabla obtenida en el PASO6.

**No.**|**CAMPOS CALCULADOS**|**REGLA DE TRANSFORMACION**
:-----:|:-----:|:-----:
RT01|CALC\_ACN|Concatenar el campo “serie” + “etiqueta” + “articulo”  y aplicar la función md5 sobre la concatenación para generar un campo hash de 64 bits
RT02|CALC\_ACD|Concatenar todos los campos atributos  excepto “serie”, “etiqueta” y “articulo” y aplicar la función md5 sobre la concatenación para generar un campo hash de 64 bits
RT03|CALC\_productiondate|Convertir el valor del campo “productiondate” a tipo de dato TIMESTAMP con el siguiente formato “YYYY-MM-DD HH:MM:SS”
RT04|CALC\_FECHA|Establecer la fecha del sistema como valor de este campo con el siguiente formato “YYYY-MM-DD HH:MM:SS”

8.	Validar la existencia de la información obtenida del PASO7 contra el Dominio de Propiedades mediante los siguientes condiciones:

- 8.1    Validar lo siguiente:
	PASO7.ACN sea igual a FINANZAS.ACN 
	PASO7.ACD sea diferente a FINANZAS.ACD
- 8.2 PASO7.ACN sea diferente a FINANZAS.ACN

9.	Actualizar la información obtenida del PASO8.1 en el dominio de propiedades mediante las siguientes condiciones:

- PASO8.1 ACN sea igual a FINANZAS.ACN

**TARGET**|**TARGET**|**SOURCE**|**SOURCE**
:-----:|:-----:|:-----:|:-----:
CAMPO|TIPO DE DATO|CAMPO|TIPO DE DATO
ACN|string|CALC\_ACN| 
DESCRIPCION|string|descripcion|string
NUEVO\_O\_EN\_PROCESO|string|nuevooenproceso|string
RESPONSABLE|string|responsable|string
DIRECTOR|string|director|string
SOLICITANTE|string|solicitante|string
CONCEPTO|string|concepto|string
TIPO|string|tipo|string
PROVEEDOR|string|proveedor|string
FILEDATE| |filedate|long
SOURCE\_ID|string|sourceid|string
RETIRO|string|retiro|string
MARCA|string|marca|string
MODELO|string|modeloversion|string
ESTADO\_FISICO|string|estado\_fisico\_usadonuevo|string
ORDEN\_COMPRA|string|orden\_de\_compra|string
ORDEN\_COMPRA\_1|string|orden\_de\_compra\_1|string
VERSION|string|version|string
TIPO\_UNIDAD|string|typeofunit|string
TIPO|string|type|string
PRODUCT\_NUMBER|string|productnumber|string
PRODUCTION\_DATE|timestamp|productiondate|string
PRODUCT\_NUMBER\_SW|string |swproductnumber|string
TIPO\_UNIDAD\_SW|string|typeofswunit|string
FECHA\_UPD|timestamp|CALC\_FECHA|timestamp

10.	Insertar la información en la tabla del dominio de “Finanzas” con la información obtenida del PASO9:

**TARGET**|**TARGET**|**SOURCE**|**SOURCE**
:-----:|:-----:|:-----:|:-----:
DOMINIO FINANZAS|TIPO DE DATO|PASO9|TIPO DE DATO
MILES|string|column\_000|string
SALDO|string|conspolsaldocuentas|string
CUENTA|string|cuenta|string
ENTIDAD|string|legalentity|string
LIBRO|string|libro|string
MXN|string|mxn|string
FACTURA|string|nofactura|string
NOTA\_COMPRADOR|string|notaalcomprador|string
TRANSACCION|string|notransaccion|string
UBICADO|string|noubicado|string
ORDEN\_COMPRA|string|ordendecompra|string
POLIZA| |polizacap|long
SUBCUENTA|string|sub\_cta|string
TIPO\_CAMBIO|string|tc|string
TIPO\_CAMBIO18|string|tc18|string
TIPO\_CAMBIO120|string|tc20|string
TIPO\_CUENTA|string|tipocuenta|string
ORDEN\_COMPRA|string|orden\_compra|string
UBICADO|string|unidades|string
UNIDADES|string|units\_assigned|string
USD|string|usd|string
CANTIDAD|string|cantidad|string
BOLSA|string|bolsa|string
AUTORIZADO\_POR|string|prestamo\_autorizado\_por|string
UDM|string |udm|string
USD\_MES|string|usd\_octubre|string
USD\_SEP19|string|usd\_sep19|string
REVISION\_FINANZA|string|revision\_finanza|string
CONTROL\_DE\_PRESTAMOS|string|control\_de\_prestamos|string




[img1]: ./images/Diagrama.png "Activo Fijo NiFi Detail View"