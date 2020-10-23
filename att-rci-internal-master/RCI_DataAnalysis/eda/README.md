# EDA (Exploratory Data Analysis)

## Descripción

Analizaremos los datos de las fuentes de inventarios con un tratamiento estadístico descriptivo para hacer el tracking del ciclo de vida de los elementos de red.
Se creará un EDA por cada fuente debido a que cada una tiene un tratamiento diferente de datos. A continuación se enlistan las diferentes fuentes de datos con las que estaremos trabajando:

### Fuentes

* Almacen Inventario
* Almacen CIP
* Almacen Proyectos
* Salida de Almacen (wlog)
* CIP Finanzas
* Gestores
  * BLAULABS
  * NETCM
  * CIENA
  * U2000 FB TX
  * U2000 GPON
  * SOEM
* ODK's
  * 12
  * 32
  * 38
  * 76
  * 99

## 1. Recolectar los datos
Se identifica y se reúnen los recursos de datos disponibles (estructurados, no estructurados y semiestructurados) y relevantes para el dominio del problema.

## 2. Descripción de los datos
Los métodos analíticos a utilizar requieren de determinados contenidos de datos, formatos y representaciones, orientados por el conocimiento en el dominio.
Se generan los modelos de información por cada fuente para la exploración.

## 3. Exploración de datos
Con los modelos de datos definidos anteriormente, se utilizan estadísticas descriptivas y técnicas de visualización para comprender el contenido de los datos, evaluar su calidad y descubrir insights iniciales sobre ellos.

## 4. Calidad de los datos
Se verifica la calidad de los datos, si existen missing data, errores de datos, inconsistencias, etc.
Se utilizarán gráficos Bokeh para la exploración, siendo estos interactivos se pueden acomodar a como el usuario prefiera directamente en el gráfico. Estos sólo serán usados para exploración. Para reportes se hará uso de la herramienta de visualización Tableau.

## 5. Preparación de datos
En este etapa se realiza la limpieza de datos (tratar con valores no válidos o que faltan,eliminar duplicados y dar un formato adecuado), combinar datos de múltiples fuentes (archivos, tablas y plataformas) y transformar los datos en variables más útiles.

## 6. Modelado
La etapa de modelado utiliza la primera versión del conjunto de datos preparado y se enfoca en desarrollar modelos
predictivos o descriptivos según el enfoque analítico previamente definido. En los modelos predictivos, los científicos de datos utilizan un conjunto de capacitación (datos históricos en los que se conoce el resultado de interés) para construir el modelo.

## 7. Evaluación
Se evalúa el modelo para comprender su calidad y garantizar que aborda el problema empresarial de manera adecuada y completa. La evaluación del modelo implica el cálculo de varias medidas de diagnóstico y de otros resultados, como tablas y gráficos, lo que permite interpretar la calidad y la eficacia del modelo en la resolución del problema.

## 8. Implementación
Cuando el modelo satisfactorio ha sido desarrollado y aprobado por los promotores del negocio, se implementa en el entorno de producción o en un entorno de pruebas comparable.


### Ficheros

Código fuente
* **src/conexiones.txt**: contiene información de conexiones a las fuentes.
* **image/**: se encuentran los archivos de flujo de datos.
* **src/**: se encuentran archivos muestra de las fuentes de datos.
