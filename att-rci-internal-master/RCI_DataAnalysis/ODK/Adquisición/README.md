<a name="main"></a>  ![Encabezado](./images/encabezado.png)


# Proceso de adquisición de ODK's

Este documento detalla la forma en la que se los datos ingestados en el Data Lake son tratados para convertirlos en un formato tabular. Los ODKs tienen  un formato de tipo documento en el que la mayor parte de los datos más se encuentran alojados en una columna de tipo clave-valor, además es necesario extraer ciertos datos de otras columnas que agrupan a los registros de la columna clave-valor. Los ODKs almacen información sobre gran parte de los elementos de red que hay instalados, incluyendo datos que permiten identificar equipos únicos mediante número de serie y de activo.

Se ha desarrollado un script de Spark que realiza la conversión de los datos a una estructura más manejable que permite contar el número de elementos por formulario, sin embargo, es necesario tratar de forma posterior los datos antes de que estos lleguen al modelo final. 

El documento contien los siguientes apartados:
- Descripción de los ODKs
- Tipos de ODKs
- Código de adquisición
- Reglas por ODK

## Descripción de los ODKs
---

Los ODKs se generan cuando el personal de operaciones llena un formulario en el que reporta las actividades que ha realizado en campo, estas pueden ser de varios tipos como instalación, mantenimiento, decomiso o algún proyecto especial. Cada una de estas actividades tiene designado un ODK, el cuál tiene su propia estructura y campos, el detalle de cada tipo de ODK se explicara en el siguiente apartado.

Los datos de los ODKs se guardan en un documento con una estructura por grupos, cada uno de los elementos que aparecen en el formulario pueden identificarse por las agrupaciones que encontramos en la columna `form_element`, para cada elemento encontramos uno o mas registros de la columna `ma`, los cuales contienen atributos sobre el elemento:

![Vista de los formualrios en Panda][img1]

*Vista de un formulario en Panda*

El equipo de infraestructura de AT&T trata estos datos y posteriormente los deposita en una tabla que se ingesta en el DataLake con el nombre `rci_network_db.tx_odk`:

![Vista de la tabla tx_odk][img2]

*Vista de la tabla tx_odk*

Para explotar estos datos la tabla será pivoteada para convertir los elementos de cada elemento que aparecen en la columna `ma` en una columna, de esta manera será mas simple realizar consultas de tipo SQL a los datos, además de facilitar su integración al modelo. Cada tipo de ODK tiene sus propias particularidades en la forma en la que agrupa los elementos en los grupos de la columna `form_element`, así como el campo en el que aparece el tippo de elemento al que se refiere el grupo, por esta razón se han desarrollado una serie de reglas que permiten pivotear cada ODK.

El detalle de la ingesta de los ODKs al DataLake se puede consultar [aquí](../RCI_DataProcessing/data-engineering/data-ingestion/ODK).

## Tipos de ODKs
---

Existen en la tabla `rci_network_db.tx_odk` mas de 60 tipos distintos de formularios, los cuales se identifican por una clave única en la columa `cve_type`, a continaución se describen cada uno de estos:

| cve_type | external_id                          | name                                               | form_version | description                                                 |
|----------|--------------------------------------|----------------------------------------------------|--------------|-------------------------------------------------------------|
| ATPMW    | ATPMWInstallChange                   | 0012 ATP Instalación MW                            | 1            | 0012 ATP Instalacion MW                                     |
| MWITX    | ATPInstallationMW                    | 0012 ATP Instalación MW (Nuevo enlace Tx) Obsolete | 20190110     | 0012 ATP Instalación MW (Nuevo enlace, Tx)                  |
| MWIN2    | ATPInstallationMW                    | 0012 ATP Instalación MW (Nuevo Enlace)             | 20190329     | 0012 ATP Instalación MW (Nuevo Enlace)                      |
| AMWIN    | ATPInstallationMW                    | 0012 ATP Instalación MW (Nuevo Enlace) Obsolete    | 20180730     | 0012 ATP Instalación MW (Nuevo Enlace)                      |
| RFE80    | ATPInstallationMW                    | 0012 ATP Instalación MW (Nuevo enlace, MWS)        | 20190401     | 0012 ATP Instalación MW (Nuevo enlace, MWS)                 |
| WITX2    | ATPInstallationMW                    | 0012 ATP Instalación MW (Nuevo enlace, Tx)         | 20190329     | 0012 ATP Instalación MW (Nuevo enlace, Tx)                  |
| AOP2     | AtpOptimizacionMW                    | 0012 ATP Optimización MW                           | 20190603     | 0012 ATP Optimización MW                                    |
| MTX2     | AtpOptimizacionMW                    | 0012 ATP Optimización MW (Tx)                      | 20190603     | 0012 ATP Optimización MW (Tx)                               |
| MWOTX    | AtpOptimizacionMWObsolete            | 0012 ATP Optimización MW (Tx)-Obsolete             | 20190110     | 0012 ATP Optimización MW (Tx)-Obsolete                      |
| AMWOP    | AtpOptimizacionMWObsolete            | 0012 ATP Optimización MW-Obsolete                  | 20180730     | 0012 ATP Optimización MW-Obsolete                           |
| ATPRF    | ATPRFInstallChange                   | 0019 Cambio de Antenas RF                          | 20150527     | 0019 Cambio de Antenas RF                                   |
| PSSD     | ATTPreSSDReport                      | 0028 Reporte pre SSD                               | 20150508     | 0028 Reporte pre SSD                                        |
| PSSD3    | ATTPreSSDReportV3                    | 0028 Reporte pre SSD v3                            | 20151112     | 0028 Reporte pre SSD v3                                     |
| SCLE     | ATTSiteCleanUp                       | 0029 Clean Up Site Report                          | 20150917     | 0029 Site Clean Up                                          |
| AIATP    | ATTInstallationATP                   | 0032 ATP Instalacion y Comisionamiento             | 20160119     | 0032 ATP Instalacion y Comisionamiento                      |
| EIATP    | ATTATPEriccsonIC                     | 0034 ATT ATP Ericsson I&C                          | 20160718     | 0034 ATT ATP Ericsson I&C                                   |
| IPBV3    | ATTIPBackhaulIC                      | 0037 ATT IP Backhaul I&C                           | 20190711     | 0037 ATT IP Backhaul I&C                                    |
| AIIPB    | ATTIPBackhaulICObsolete              | 0037 ATT IP Backhaul I&C-Obsolete                  | 20160719     | 0037 ATT IP Backhaul I&C-Obsolete                           |
| IPBV2    | ATTIPBackhaulICObsolete2             | 0037 ATT IP Backhaul I&C-Obsolete2                 | 20190416     | 0037 ATT IP Backhaul I&C-Obsolete2                          |
| DECOR    | AttDecommissioning                   | 0038 ATT Decommissioning Report                    | 20170606     | 0038 ATT Decommissioning Report                             |
| DITPE    | AttEvictionInfraTpeTEST              | 0046 ATT Desalojo de infraestructura TPE           | 20161209     | 0046 ATT Desocupación de infraestructura                    |
| ATPSC    | AttSiteConsolidation                 | 0055 ATT ATP Site Consolidation                    | 20170721     | 0055 ATT ATP Site Consolidation                             |
| ATPCG    | AttCambioGabinetes                   | 0056 ATP Cambio de Gabinetes                       | 20170817     | 0056 ATP Cambio de Gabinetes                                |
| ARFCS    | AtpRfCambioSectores                  | 0058 ATP RF Cambio en sectores                     | 20180507     | 0058 ATP RF Cambio en sectores                              |
| ATPSA    | AtpSectorAdicionalCambioAltura       | 0058 ATP RF Cambio en sectores                     | 20170825     | 0058 ATP RF Cambio en sectores                              |
| CSRAN    | AtpRfCambioSectores                  | 0058 ATP RF Cambio en sectores RAN                 | 20180507     | 0058 ATP RF Cambio en sectores RAN                          |
| IESAU    | AtpInstallationEricssonSau           | 0060 ATP Installation Ericsson SAU                 | 20170915     | 0060 ATP Installation Ericsson SAU                          |
| AVGI     | AtpVerificacionGponIpbh              | 0061 ATP Verificación GPON-IPBH (DEPLOY)           | 20170922     | 0061 ATP Verificación GPON-IPBH (DEPLOY)                    |
| SEFOP    | AtpVerificacionGponIpbhFOPS          | 0061 ATP Verificación GPON-IPBH (FOPS)             | 20190903     | 0061 ATP Verificación GPON-IPBH (FOPS)                      |
| IECV2    | AtpInstalacionEquiposCarrier         | 0063 ATP Instalación Equipos Carrier               | 20190416     | 0063 ATP Instalación Equipos Carrier                        |
| AIEC     | AtpInstalacionEquiposCarrierObsolete | 0063 ATP Instalación Equipos Carrier-Obsolete      | 20180103     | 0063 ATP Instalación Equipos Carrier-Obsolete               |
| NRWRF    | ATTNonRegularWorksReport             | 0064 ATT Reporte Trabajos No Regulares (FOPS)      | 20171115     | 0064 ATT Reporte Trabajos No Regulares (FOPS)               |
| NRWRI    | ATTNonRegularWorksReport             | 0064 ATT Reporte Trabajos No Regulares (I&C)       | 20171115     | 0064 ATT Reporte Trabajos No Regulares (I&C)                |
| NRWRM    | ATTNonRegularWorksReport             | 0064 ATT Reporte Trabajos No Regulares (MSO)       | 20180327     | 0064 ATT Reporte Trabajos No Regulares (MSO)                |
| NRWRN    | ATTNonRegularWorksReport             | 0064 ATT Reporte Trabajos No Regulares (NE)        | 20180327     | 0064 ATT Reporte Trabajos No Regulares (Network Experience) |
| IEEV2    | AtpInstalacionEquiposEdge            | 0065 ATP Instalación Equipos EDGE                  | 20190416     | 0065 ATP Instalación Equipos EDGE                           |
| AIEE     | AtpInstalacionEquiposEdgeObsolete    | 0065 ATP Instalación Equipos EDGE-Obsolete         | 20171115     | 0065 ATP Instalación Equipos EDGE-Obsolete                  |
| WIFI     | AtpReporteWIFIMetro                  | 0066 Wi-Fi Installation                            | 20171129     | 0066 Wi-Fi Installation                                     |
| RRFM     | AtpReporteRFMetro                    | 0069 ATP Reporte RF Metro                          | 20180310     | 0069 ATP Reporte RF Metro                                   |
| ATPHD    | HardwareDatacomm                     | 0072 Hardware Datacomm                             | 20181207     | 0072 Hardware Datacomm                                      |
| HIXCR    | Hardware IXCR                        | 0072 Hardware IXC-R                                | 20181210     | 0072 Hardware IXC-R                                         |
| ATPPO    | PowerOnEquiposCentrales              | 0072 Power On Equipo Centrales                     | 20181113     | 0072 Power On Equipo Centrales                              |
| HIC2     | HardwareIngenieriaCore               | 0072 Proyectos Ingeniería Core                     | 20190424     | 0072 Proyectos Ingeniería Core                              |
| HIC      | HardwareIngenieriaCoreObsolete       | 0072 Proyectos Ingeniería Core-Obsolete            | 20181212     | 0072 Proyectos Ingeniería Core-Obsolete                     |
| ATPGA    | ReporteInstalacionEquiposCentrales   | 0072 Reporte de Instalación de Equipo Centrales    | 20180613     | 0072 Reporte de Instalación de Equipo Centrales             |
| IGR      | atpInstalacionGabineteRack           | 0075 Instalación de Gabinete-Rack                  | 20180928     | 0075 Instalación de Gabinete-Rack                           |
| ALMCN    | atpAlmacen                           | 0076 Salida Almacén                                | 20180801     | 0076 Almacén                                                |
| AIGD     | AtpInstallGenDeployment              | 0083 ATP Instalación Generadores Deployment        | 20181121     | 0083 ATP Instalación Generadores Deployment                 |
| ASMGD    | AtpSymGenDeployment                  | 0084 ATP S&M Generadores Deployment                | 20181121     | 0084 ATP S&M Generadores Deployment                         |
| ARGD     | AtpRetiroGenDeployment               | 0085 ATP Retiro Generadores Deployment             | 20181121     | 0085 ATP Retiro Generadores Deployment                      |
| SND      | Sondas                               | 0095 Sondas                                        | 20181127     | 0095 Sondas                                                 |
| IDBDA    | atpInstalacionDesinstalacionBDA      | 0097 InstalaciónDesinstalación de BDA              | 20181122     | 0097 InstalaciónDesinstalación de BDA                       |
| IDBDP    | atpInstalacionDesinstalacionBDAP     | 0097 InstalaciónDesinstalación de BDA(Panda)       | 20190816     | 0097 InstalaciónDesinstalación de BDA(Panda)                |
| IEPAS    | Instalacion10GPONV2                  | 0098 Instalación Equipamento 10GPON (AS)           | 20190823     | 0098 Instalación equipamiento Pon (AS)                      |
| PONV3    | Instalacion10GPONV2                  | 0098 Instalación Equipamento 10GPON (DEPLOY)       | 20190416     | 0098 Instalación equipamiento Pon (DEPLOY)                  |
| IEPIN    | Instalacion10GPONV2                  | 0098 Instalación Equipamento 10GPON (ING)          | 20190917     | 0098 Instalación Equipamento 10GPON (ING)                   |
| IEPON    | ATP10GPONObsolete                    | 0098 Instalación equipamiento Pon-Obsolete         | 20181016     | 0098 Instalación equipamiento Pon-Obsolete                  |
| SINV     | ATTRANInventory                      | 0099 Inventario de Sitio (DG)                      | 20181008     | 0099 Inventario de Sitio (DG)                               |
| SINR     | ATTInventoryRAN                      | 0099 Inventario de Sitio RAN                       | 20181109     | 0099 Inventario de Sitio RAN                                |
| MFO      | atpMantenimientoDeFO                 | 0108 Monitoreo de FO                               | 20181217     | 0108 Monitoreo de FO                                        |
| ISGV2    | InstalacionSitioGenerico             | 0111 Instalación en Sitio (Genérico)               | 20190416     | 0111 Instalación en Sitio (Genérico)                        |
| ISG      | InstalacionSitioGenericoObsolete     | 0111 Instalación en Sitio (Genérico)-Obsolete      | 20181214     | 0111 Instalación en Sitio (Genérico)-Obsolete               |
| ISGV3    | InstalacionSitioGenericoTX           | 0111 Instalación en Sitio (Genérico)-TX            | 20190815     | 0111 Instalación en Sitio (Genérico)-TX                     |
| ATPLT    | AtpLTE580                            | 0114 ATP LTE 850                                   | 20190213     | 0114 ATP LTE 850                                            |
| ATTSC    | attSmallCells                        | 0115 ATT Small Cells                               | 20190208     | 0115 ATT Small Cells                                        |
| AFO      | AcometidasFOV4                       | 0136 Acometidas FO                                 | 20190510     | 0136 Acometidas FO                                          |
| RFPME    | RF - Proyecto Metro                  | 0154 RF - Proyecto Metro                           | 20190827     | 0154 RF - Proyecto Metro                                    |
| WIPME    | WIFI - Proyecto Metro                | 0155 WIFI - Proyecto Metro                         | 20190827     | 0155 WIFI - Proyecto Metro                                  |

## Código de adquisición:
---

El código de adquisición para todos los ODKs es el mismo, está dividido en un script para cada tipo de formulario y puede consultarse aquí. El código realiza los siguientes pasos:

- Inicia la sesión de Spark e importa las librerías necesarias.
- Importa los datos desde la tabla `tx_odk` para el tipo de formulario del script.
- Realiza una limpieza de los datos, quitando caracteres inválidos, en este apartado la actividad más importante que se realiza es la de remplazar el caractér `:` cuando no es necesario, esto debe hacerse por que los datos de la columna `ma` se separarán por este caracter así que no debe eliminarse por completo, se usan expresiones regulares para hacer el trabajo.
- Se separa la columna `ma` usando el caractér `:`.
- Se crea y aplica una función que identifica cada elemento y el campo por el que debe de tomar su tipo.
- Se hace una segunda limpieza para estandarizar codificación uft-8, eliminar acentos y homologar el nombre de los campos `número de serie` y `activo`.
- Se pivotean los datos.
- Se persisten los datos en una tabla en el DataLake.

Se ha decidido persistir cada tipo de formulario distinto en tablas individuales debido a que cada atributo distinto de la columna `ma` genera una nueva columna, tener varios formularios en la misma tabla implicaria cientos de columnas distintas en su mayor parte vacías.

### Agregar un nuevo ODK

Si se desea agregar un nuevo ODK se puede copiar el código de uno existente y reemplazar tres partes:
1. El query que importa los datos de la tabla `tx_odk` para que apunte al nuevo ODK.

![Importar los datos a Spark][img3]

2. La función de búsqueda de elementos.

![Identificación de elementos y su tipo][img4]

3. El query que persiste el dataframe en el DataLake.

![Persistencia de datos en el DataLake][img5]


Debido a que todos los ODKs agrupan los elementos en niveles distintos en la columna `form_element` e identifican el tipo de elemento en campos con nombres distintos, se debe editar en cada script la función `search`. Normalmente la función identifica el nivel del elemento separando el campo `form_element`y posteriormente aplica una serie de reglas *IF* para encontrar el el elemento y su tipo. Todas las demás partes del código permanecen igual.

Todos los scripts se corren de forma automática usando un orquestador programado en Oozie, el detalle de su operación puede consultarse en este [documento](./Orquestador).

## Reglas de adquisición por ODK
---

Laas reglas identificadas para cada ODK se listan a continuación:

| ODK Nombre                                                         | Regla            | Descripción (campo atributo)                                                                                                                                                                                                                                                      |
|--------------------------------------------------------------------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0012 ATP Instalación MW                                            | Tipo de elemento | Campos que contengan: 'picOutAPM30' es el elemnto APM30; 'Antenna', 'ODU', 'Acoplador', 'PTR', 'Atizador', 'GroundBar' es Barra de Tierra en Torre, 'GroundBar2' es Segunda Barra de Tierra en Torre, 'GroundBarPC' es Barra de Tierra, 'Radio', 'LabelBB', 'IndRack' es un Rack. |
| 0012 ATP Instalación MW (Nuevo enlace Tx) Obsolete                 | Tipo de elemento | Extraer el tipo de elemento del campo 'strElement'                                                                                                                                                                                                                                |
| 0012 ATP Instalación MW (Nuevo Enlace)                             | Tipo de elemento | Extraer el tipo de elemento del campo 'strElement'                                                                                                                                                                                                                                |
| 0012 ATP Instalación MW (Nuevo Enlace) Obsolete                    | Tipo de elemento | Extraer el tipo de elemento del campo 'strElement'                                                                                                                                                                                                                                |
| 0012 ATP Instalación MW (Nuevo enlace, MWS)                        | Tipo de elemento | Extraer el tipo de elemento del campo 'strElement'                                                                                                                                                                                                                                |
| 0012 ATP Instalación MW (Nuevo enlace, Tx)                         | Tipo de elemento | Extraer el tipo de elemento del campo 'strElement'                                                                                                                                                                                                                                |
| 0012 ATP Optimización MW                                           | Tipo de elemento | Extraer el tipo de elemento del campo 'keyElement'                                                                                                                                                                                                                                |
| 0012 ATP Optimización MW (Tx)                                      | Tipo de elemento | Extraer el tipo de elemento del campo 'keyElement'                                                                                                                                                                                                                                |
| 0012 ATP Optimización MW (Tx)-Obsolete                             | Tipo de elemento | Extraer el tipo de elemento del campo 'keyElement'                                                                                                                                                                                                                                |
| 0012 ATP Optimización MW-Obsolete                                  | Tipo de elemento | Extraer el tipo de elemento del campo 'keyElement'                                                                                                                                                                                                                                |
| 0032 ATP Instalacion y Comisionamiento                             | Vistas           | Todos los elementos con 'pic' dentro del campo atributo son vistas.                                                                                                                                                                                                               |
| 0032 ATP Instalacion y Comisionamiento                             | Pantallas        | Todos los elementos dentro del grupo 'groupComm' son pantallas.                                                                                                                                                                                                                   |
| 0037 ATT IP Backhaul I&C                                           | Tipo de elemento | Extraer el nombre del elemento del campo 'keyEquipType' ubicado en el root                                                                                                                                                                                                        |
| 0037 ATT IP Backhaul I&C                                           | Agrupación       | Todos los elementos se encuentran dentro del 'groupInv' y se agruparán de acuerdo al elemento 'keyEquipType'                                                                                                                                                                      |
| 0037 ATT IP Backhaul I&C-Obsolete2                                 | Número elementos | El número de elementos aparece en el campo 'groupBancoBaterias'.                                                                                                                                                                                                                  |
| 0037 ATT IP Backhaul I&C-Obsolete2                                 | Vistas           | Todos los elementos dentro del grupo 'groupInd' son vistas.                                                                                                                                                                                                                       |
| 0037 ATT IP Backhaul I&C-Obsolete2                                 | Interconexiones  | Todos los elementos dentro del grupo 'groupIxn' son interconexiones.                                                                                                                                                                                                              |
| 0037 ATT IP Backhaul I&C-Obsolete2                                 | Vistas           | Todos los elementos dentro del grupo 'groupPow' son vistas.                                                                                                                                                                                                                       |
| 0046 ATT Desalojo de infraestructura TPE                           | Tipo elemento    | Extraer el nombre o tipo de elemento del campo 'keyEqpt'.                                                                                                                                                                                                                         |
| 0046 ATT Desalojo de infraestructura TPE                           | Agrupación       | Todos los elementos dentro del grupo 'groupWdEqpt' se agruparán de acuerdo al elemento que aparezca en el campo 'keyEqpt'.                                                                                                                                                        |
| 0046 ATT Desalojo de infraestructura TPE                           | Vistas           | Todos los elementos con 'pic' dentro del campo atributo son vistas.                                                                                                                                                                                                               |
| 0056 ATP Cambio de Gabinetes                                       | Tipo elemento    | Extraer el tipo de elemento del campo 'keyElementoInv' para el grupo 'groupInventario'.                                                                                                                                                                                           |
| 0056 ATP Cambio de Gabinetes                                       | Vistas           | Todos los elementos con 'pic' dentro del campo atributo son vistas.                                                                                                                                                                                                               |
| 0058 ATP RF Cambio en sectores                                     | Tipo elemento    | Extraer el nombre o tipo de elemento del campo 'keyElemInv'.                                                                                                                                                                                                                      |
| 0058 ATP RF Cambio en sectores                                     | Agrupación       | Todos los elementos dentro del grupo 'groupElemInv' se agruparán de acuerdo al elemento que aparezca en el campo 'keyElemInv'.                                                                                                                                                    |
| 0058 ATP RF Cambio en sectores                                     | Vistas           | Todos los elementos dentro del grupo 'groupSectoresPhoto' son vistas.                                                                                                                                                                                                             |
| 0060 ATP Installation Ericsson SAU                                 | Tipo elemento    | Extraer el nombre o tipo de elemento del campo 'strElementoInventarioOth'.                                                                                                                                                                                                        |
| 0063 ATP Instalación Equipos Carrier-Obsolete                      | Vistas           | Todos los elementos con 'pic' dentro del campo atributo son vistas.                                                                                                                                                                                                               |
| 0064 ATT Reporte Trabajos No Regulares (MSO) , (NE), (I&C), (FOPS) | Tipo de trabajo  | Se identifica el tipo de trabajo con el campo 'id:root:keyWorkType'                                                                                                                                                                                                               |
| 0064 ATT Reporte Trabajos No Regulares (MSO) , (NE), (I&C), (FOPS) | Tipo elemento    | "Extraer el nombre o tipo de elemento del campo: 'WorkingElems'."                                                                                                                                                                                                                 |
| 0064 ATT Reporte Trabajos No Regulares (MSO) , (NE), (I&C), (FOPS) | Descripción      | Campo: 'strEvidenceTx'                                                                                                                                                                                                                                                            |
| 0065 ATP Instalación Equipos EDGE-Obsolete                         | Tipo elemento    | Extraer el nombre o tipo de elemento del campo 'keyEquipment'.                                                                                                                                                                                                                    |
| 0065 ATP Instalación Equipos EDGE-Obsolete                         | Agrupación       | Todos los elementos dentro del grupo 'groupInventarioSitio' se agruparán de acuerdo al elemento que aparezca en el campo 'keyEquipment'.                                                                                                                                          |
| 0065 ATP Instalación Equipos EDGE-Obsolete                         | Vistas           | Todos lo elementos dentro ddel grupo 'groupReporteFotografico1Insta' y el grupo 'groupReporteFotograficoInst' son vistas.                                                                                                                                                         |
| 0069 ATP Reporte RF Metro                                          | Pantallas        | Todos los elementos dentro del grupo 'picTestUTPVw' son pantallas.                                                                                                                                                                                                                |
| 0069 ATP Reporte RF Metro                                          | Tipo elemento    | Extraer el tipo de elemento del campo 'keyEquipmentDAS ' para el grupo 'groupInventarioEquiposDAS'.                                                                                                                                                                               |
| 0069 ATP Reporte RF Metro                                          | Vistas           | Todos los elementos que no son pantallas y que tienen 'pic' dentro del campo atributo son vistas.                                                                                                                                                                                 |
| 0072 Power On Equipo Centrales                                     | Tipo elemento    | Extraer el nombre o tipo de elemento del campo 'keyEqType'.                                                                                                                                                                                                                       |
| 0072 Power On Equipo Centrales                                     | Agrupación       | Todos los elementos dentro del grupo 'groupInstall' se agruparán de acuerdo al elemento que aparezca en el campo 'keyEqType'.                                                                                                                                                     |
| 0072 Power On Equipo Centrales                                     | Agrupación       | Todos los elementos dentro del grupo 'groupEquiOld' se agruparán de acuerdo al elemento que aparezca en el campo 'strRetModel'.                                                                                                                                                   |
| 0072 Power On Equipo Centrales                                     | Vistas           | Todos los elementos con 'pic' dentro del campo atributo son vistas.                                                                                                                                                                                                               |
| 0084 ATP S&M Generadores Deployment                                | Tipo elemento    | Extraer el nombre o tipo de elemento del campo 'strElement'.                                                                                                                                                                                                                      |
| 0084 ATP S&M Generadores Deployment                                | Agrupación       | Todos los elementos dentro del grupo 'groupSiteInventory' se agruparán de acuerdo al elemento que aparezca en el campo 'strElement'.                                                                                                                                              |
| 0084 ATP S&M Generadores Deployment                                | Vistas           | Todos los elementos con 'pic' dentro del campo atributo son vistas.                                                                                                                                                                                                               |
| 0098 Instalación equipamiento Pon-Obsolete                         | Tipo elemento    | Extraer el nombre del elemento del campo 'strElemInvOth'                                                                                                                                                                                                                          |
| 0098 Instalación equipamiento Pon-Obsolete                         | Agrupación       | Todos los elementos dentro del grupo 'groupInventario' se agruparán de acuerdo al elemento que aparezca en el campo 'strElemInvOth'.                                                                                                                                              |
| 0098 Instalación equipamiento Pon-Obsolete                         | Vistas           | Todos los elementos con 'pic' dentro del campo atributo son vistas.                                                                                                                                                                                                               |
| 0098 Instalación equipamiento Pon-Obsolete                         | Pantallas        | Todos los elementos con 'img' dentro del campo atributo son pantallas.                                                                                                                                                                                                            |
| 0108 Monitoreo de FO                                               | Tipo elemento    | Que el campo contenga 'keyElemInv'                                                                                                                                                                                                                                                |
| 0111 Instalación en Sitio (Genérico)                               | Tipo elemento    | Extraer el nombre o tipo de elemento del campo 'keyEqType'.                                                                                                                                                                                                                       |
| 0111 Instalación en Sitio (Genérico)                               | Agrupación       | Todos los elementos dentro del grupo 'groupInstallInventory' se agruparán de acuerdo al elemento que aparezca en el campo 'keyEqType'.                                                                                                                                            |
| 0111 Instalación en Sitio (Genérico)                               | Vistas           | Todos los elementos con 'pic' dentro del campo atributo son vistas.                                                                                                                                                                                                               |
| 0115 ATT Small Cells                                               | Tipo elemento    | Para el grupo 'groupInventarioU' el tipo de elemento se toma del campo 'keyElemInvU'.                                                                                                                                                                                             |
| 0115 ATT Small Cells                                               | Tipo elemento    | Para el grupo 'groupInventoryIn' el tipo de elemento se toma del campo 'keyElemInvI'.                                                                                                                                                                                             |
| 0115 ATT Small Cells                                               | Agrupación       | Todos los elementos dentro del grupo 'groupInventarioU' se agruparán de acuerdo al elemento que aparezca en el campo 'keyElemInvU'.                                                                                                                                               |
| 0115 ATT Small Cells                                               | Agrupación       | Todos los elementos dentro del grupo 'groupInventoryIn' se agruparán de acuerdo al elemento que aparezca en el campo 'keyElemInvI'.                                                                                                                                               |
| 0037 ATT IP Backhaul I&C                                           | Interconexiones  | Todos los registros que se encuentran dentro del grupo 'groupIxn' son Interconexiones                                                                                                                                                                                             |
| 0095 Sondas                                                        | Tipo elemento    | Extraer el tipo de elemento del campo 'keyElemInv'                                                                                                                                                                                                                                |
| 0098 Instalación Equipamento 10GPON (DEPLOY)                       | Vistas           | Todos los elementos del grupo 'groupPicRepONT' son vistas                                                                                                                                                                                                                         |
| 0098 Instalación Equipamento 10GPON (DEPLOY)                       | Tipo elemento    | Extraer el tipo de elemento del campo 'keyElemInv'                                                                                                                                                                                                                                |
| 0098 Instalación Equipamento 10GPON (DEPLOY)                       | Pantallas        | Todos los elementos dentro del grupo 'groupScreensONT' son pantallas.                                                                                                                                                                                                             |
| 0108 Monitoreo de FO                                               | Tipo elemento    | Extraer el tipo de elemento del campo 'keyElemInv'                                                                                                                                                                                                                                |
| 0111 Instalación en Sitio (Genérico)-TX                            | Tipo elemento    | Extraer el tipo de elemento del campo 'keyEqType'                                                                                                                                                                                                                                 |
[img1]: images/Adquisicion-01.png "Formulario"
[img2]: images/Adquisicion-02.jpg "tx_odk"
[img3]: images/Adquisicion-03.jpg "Importar datos"
[img4]: images/Adquisicion-04.jpg "Identificación de Elementos"
[img5]: images/Adquisicion-05.jpg "Persistir datos en el DataLake"