# EDA (Exploratory Data Analysis) - CIP Finanzas

## Descripción

Analizaremos los datos de las fuente CIP Finanzas con un tratamiento estadístico descriptivo para comenzar con el tracking del ciclo de vida de los elementos de red.

En esta fuente se decribe los elementos que están generando un costo y una ganancia para el negocio. Dentro de la fuente se describen las diferentes
características a tomar en cuenta de estos elementos, así como su costo en pesos y en dólares.

## 1. Recolectar los datos
Se hace la extracción del dataset mediante herramienta Spark. Debido a ventajas de manipulación, se transforma a un dataframe y se prosigue con la utilización de herramienta Python.

## 2. Descripción de los datos
Se busca observar el tamaño del dataset, nos interesa saber número de columnas, número de registros, número de registros únicos por columna, los tipos de datos y en los casos en que los campos sean discretos o continuos, nos interesa también conocer estadísticas básicas como moda, cuartiles, media.

## 3. Exploración de datos
Se hace una exploración a base de visualización en gráficos y dataframes. Se busca encontrar datos atípicos, reglas de limpieza, distribución de los datos y la posibilidad de obtener catálogos por campo.

## 4. Calidad de los datos.
Se verifica la calidad de los datos, si existen missing data, errores de datos e inconsistencias. Por motivos de visualización se hacen gráficos y dataframes de resultados expresados en porcentajes.

## 5. Preparación de datos
En este etapa se presentan las reglas de calidad y limpieza a hacer en las columnas que lo requieran, una vez que se realizo la exploración y la calidad de los datos.

## 6. Catálogos.
Este apartado corresponde a los catálogos óptimos que se podrían obtener después de una limpieza a las variables propuestas.

## 7. Métricas KPI's.
Se realiza el cálculo de indicadores concernientes a la fuente. Estos se presentan en una tabla para visualización y manipulación.


### Ficheros

Código fuente
* **src/**: contiene información de las fuentes originales.
* **image/**: contiene las imágenes utilizadas en el md.
* [EDA CIP FINANZAS](EDA_CIP_Finanzas.md)
