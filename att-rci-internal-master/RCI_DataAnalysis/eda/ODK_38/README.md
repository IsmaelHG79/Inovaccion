
# EDA (ODK 38)

## Descripción

La fuente que se presenta contiene la información referente a los datos de salida de almacén, proveedor y códigos de sitio destino de los elementos de red gestionados en inventario.

## 1. Recolectar los datos
Se hace la extracción del dataset mediante herramienta Spark. Debido a ventajas de manipulación, se transforma a un dataframe y se prosigue con la utilización de herramienta Python.

## 2. Descripción de los datos
Se busca observar el tamaño del dataset, nos interesa saber número de columnas, número de registros, número de registros únicos por columna, los tipos de datos y en los casos en que los campos sean discretos o continuos, nos interesa también conocer estadísticas básicas como moda, cuartiles, media.

## 3. Exploración de datos
Se hace una exploración a base de visualización en gráficos y dataframes. Se busca encontrar datos atípicos, reglas de limpieza, distribución de los datos y la posibilidad de obtener catálogos por campo.

## 4. Calidad de los datos.
Se verifica la calidad de los datos, si existen missing data, errores de datos e inconsistencias. Por motivos de visualización se hacen gráficos y dataframes de resultados expresados en porcentajes.

## 5. Preparación de datos.
En este etapa se presentan las reglas de calidad y limpieza que se proponen para los campos que lo requieran, una vez que se realizaron la exploración y  calidad de los datos.

## 6. Catálogos.

Este apartado corresponde a los catálogos óptimos que se podrían obtener después de una limpieza a las variables propuestas.

## 7. Métricas KPI's.

Se realiza el cálculo de indicadores concernientes a la fuente. Estos se presentan en una tabla para visualización y manipulación.

### FicherosCódigo fuente
* **src/**: contiene información de las fuentes originales.
* **image/**: contiene las imágenes utilizadas en el md.
* [EDA_ODK 38](ODK_38.md)
* [Adquisición de datos ODK 38](Adquisicion_Datos_ODK_38.md)
