# EDA (Exploratory Data Analysis) - CIP Finanzas

## Descripci�n

Analizaremos los datos de las fuente CIP Finanzas con un tratamiento estad�stico descriptivo para comenzar con el tracking del ciclo de vida de los elementos de red.

En esta fuente se decribe los elementos que est�n generando un costo y una ganancia para el negocio. Dentro de la fuente se describen las diferentes
caracter�sticas a tomar en cuenta de estos elementos, as� como su costo en pesos y en d�lares.

## 1. Recolectar los datos
Se hace la extracci�n del dataset mediante herramienta Spark. Debido a ventajas de manipulaci�n, se transforma a un dataframe y se prosigue con la utilizaci�n de herramienta Python.

## 2. Descripci�n de los datos
Se busca observar el tama�o del dataset, nos interesa saber n�mero de columnas, n�mero de registros, n�mero de registros �nicos por columna, los tipos de datos y en los casos en que los campos sean discretos o continuos, nos interesa tambi�n conocer estad�sticas b�sicas como moda, cuartiles, media.

## 3. Exploraci�n de datos
Se hace una exploraci�n a base de visualizaci�n en gr�ficos y dataframes. Se busca encontrar datos at�picos, reglas de limpieza, distribuci�n de los datos y la posibilidad de obtener cat�logos por campo.

## 4. Calidad de los datos.
Se verifica la calidad de los datos, si existen missing data, errores de datos e inconsistencias. Por motivos de visualizaci�n se hacen gr�ficos y dataframes de resultados expresados en porcentajes.

## 5. Preparaci�n de datos
En este etapa se presentan las reglas de calidad y limpieza a hacer en las columnas que lo requieran, una vez que se realizo la exploraci�n y la calidad de los datos.

## 6. Cat�logos.
Este apartado corresponde a los cat�logos �ptimos que se podr�an obtener despu�s de una limpieza a las variables propuestas.

## 7. M�tricas KPI's.
Se realiza el c�lculo de indicadores concernientes a la fuente. Estos se presentan en una tabla para visualizaci�n y manipulaci�n.


### Ficheros

C�digo fuente
* **src/**: contiene informaci�n de las fuentes originales.
* **image/**: contiene las im�genes utilizadas en el md.
* [EDA CIP FINANZAS](EDA_CIP_Finanzas.md)
