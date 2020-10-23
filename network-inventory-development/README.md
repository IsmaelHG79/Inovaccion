# network-inventory

## Objetivo

El objetivo del sistema de reconciliación de inventario es integración automática  de las distintas fuentes de información en una plataforma Big data que permita obtener mediante herramientas algoritmos de inferencia, correlación y limpieza de datos una base de datos central de activos de la red que pueda ser consumida por los usuarios de negocio y que contenga  la siguiente información:

* Activos lógicos y físicos de la red
* Ciclo de vida (planeación, procurement, logística, deployment, operación, decommisionamiento)
* Ultima ubicación registrada del activo.
* Propiedades del activo (modelo, marca, costo, etc.)
* Otras propiedades (configuración, proyecto, etc.)
* Clasificaciones de negocio (RAN, CORE, TX, etc.)
* Desviaciones y anomalías de los activos y de las fuentes.
* Información histórica (Snapshots)


## Diseño
Diseño modular que permite procesar la fuente desde la ingesta hasta la capa semantica y las vistas de negocio:



~~~mermaid
graph LR;

   f01[1. Source 1] --> d01[X];
   f02[1. Source 2] --> d02[X];
   f03[1. Source N] --> d03[X];
   d01[2. Data Extractor 1] --> ie1[X];
   d02[2. Data Extractor 2] --> ie1[X];
   d03[2. Data Extractor N] --> ie1[X];
   ie1[3. Ingestion Engine] --> r01[X];
   r01[5. RAW Data] --> ae1[X];
   ae1[6. Asset Engine] --> am1[X];
   am1[7. Asset Model] --> se1[X];
   se1[8. Semantic Engine] --> sm1[9. Semantic Model];
   sm1[9. Semantic Model] --> av1[10. Asset View 1];
   sm1[9. Semantic Model] --> av2[10. Asset View 2];
   sm1[9. Semantic Model] --> av3[10. Asset View N];

~~~    
