|                       |                                    |
|----------------------	|------------------------------------|
| ![EncabezadoAxity][img1] | ![EncabezadoATT][img2] |

# Documentación del codigo y funcionamiento de **PROCESADORES CUSTOM DE NIFI**

## Introduccion  
Apache NIFI es una herramienta grafica, la cual se utiliza para desarrollas diferentes tipos de pipelines, ya sea transforomacion de datos, limpieza, agregaciones,etc. En este caso lo utilizamos solo como medio de transporte en el cual se le realiza diferentes tipos de limpieza y homologacion de la fuente de datos, para generar un avro final.

## Objetivos
Los objetivos son: generar dos procesadores custom en nifi, uno para manejar ciertas fuentes con archivos en excel y otro para manejar la fuente de wlog; ya que por el analisis son fuentes que necesitan un trato en especial y muy adecuado, todo con la finalidad de que el pipeline nifi sea mas facil y transparente con los datos fuente.

## Desarrollo
Como ya se habia comentado el motivo de generar procesadores custom es con la finalidad de facilitar el desarrollo del pipeline y tratar de una manera facil las fuentes de datos, en especial los excel con varias sheet y las fuente de wlog que es un json.

El codigo fuente esta en java, por que nifi y todos sus componentes estan desarrollado sobre java 8, ademas de que el dato que se toma en el pipeline es un tipo de dato stream en binario por lo que es muy facil de castearlo y manejarlo a una clase definida, ya que es facil convertilo a un tipo string.


Son procesadores que se realizaron:
- **FlatXLSXToCSV.java**
- **HandleWLOGJSON.java**

### HandleWLOGJSON.java
Este procesador se encarga de tomar del pipeline el archivo que se cargo el cual son los archivos de wlog en especifico los tipo json, y el funcionamiento es de que se toma de los item de columns y data del json, se parsean a un string csv, en el cual los columns son los headers y data los registros, por lo que se genera esa salida de string csv y se pasa al siguiente flujo dentro del pipeleine.


### FlatXLSXToCSV.java
Este procesador se encarga tomar del pipeline el stream de los archivos xlsx que se cargaron, la logica que se utiliza que para esta fuente los archivos xlsx contienen varias sheet y en cada sheet hay veces que tienen las mismas columnas o son diferentes, por lo que es necesario realizar un flat de todo el archivo y generar un string csv con una estructura definida.

Como tal el proceso toma del stream  y genera un header en comun, los cuales son los headers de todas las sheet, este proceso con lleva varias validaciones: si la columna ya existe se renombra agregandole el indice de la posicion, de igual manera si algun header tiene caracteres especiales se procede a limpiar, tambien si lo headers tienen un nombre como &&& o #, de igual manera se renombra remplazandolo por col_+ el indice de la columna.

Una vez que se tienen un header en comun se procede a leer y acomodar los datos y que cada uno pertenezca a su respectiva columna, si en alguna columna no exite valor se le agrega un valor vacio, esto sucede por la homologacion de los headers, por ejemplo en un sheet tiene 3 columnas con valores y otra sheet con 2 headers, al momento de la homologacion se genera un header con 5 columnas y al momento de estructurar los registros cada registro debe pertenecer a su columna padre por lo que las 3 columnas iniciales se llenan con sus respectivos datos y las 2 que se agregaron se le agrega un valor vacio en esos campos, esa es la funcion principal del procesador.

Resumiendo el procesador, lo que hace es que genera un header homologado de acuerdo a los headers de las diferentes sheet, y los datos de que tengan en cada sheet y con su respectivo header padre, se restructura con el nuevo header homologado en donde cada registro debe de machar con su header padre y los headers que se complementaron y no tengan un valor de origen se le agrega un vacio, para el final generar un string csv de esa estructura y pasarlo al siguiente flujo.

## Compilacion del proyecto maven y generar Nar
Para generar el nar con dependencias con el codigo fuente de NIFI y se utilizo maven, maven es un herramienta para gestionar proyectos de java, scala con el cual es mas facil mantener un control de versiones y dependencias que se utilizan de acuerdo a la version  de java que utiliza NIFI.

Una vez que tengamos el codigo fuente de java, y tengamos todas las dependencias necesarias agregadas en el archivo pom.xml, se procede a ejecutar el template de maven para procesadores nifi, como tal maven genera un archivo nar, el comando es el siguiente:


```mvn clean install```

Se genera dentro de la siguiente direccion ```nifi-dev-nar/target/``` . dentro de ese folder se encuentra el fat nar llamado ```nifi-dev-nar-1.0-SNAPSHOT.nar```.

Ahora se copia ese  build nar,dentro del directorio de lib de nifi, y se procede a reiniciar el servicio de nifi:

    cp target/nifi-dev-nar-1.0-SNAPSHOT.nar $NIFI_HOME/lib



## Referencias al Framework de Ingestion


- [Framework de Ingestion](../Globales/)


## Codigo Fuente Local

- [Codigo Fuente ](nifi-dev-processors/src/)
- [Nar ](nifi-dev-nar)




[img1]: ../Globales/ArquitecturaFrameworkIngestion/images/axity.png "Logo Axity"
[img2]: ../Globales/ArquitecturaFrameworkIngestion/images/att.png "Logo AT&T"
