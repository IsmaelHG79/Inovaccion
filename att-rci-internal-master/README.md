# AT&T - RCI - Axity Internal Repository

## AT&T RCI Technical Components

* Data Engineering link:
  * [Data Management](RCI_DataProcessing/data-management)
  * [Data Engineering](RCI_DataProcessing/data-engineering)
  * [Diccionario de Datos](RCI_DataAnalysis/DataUnderstanding)

##  AT&T BitBucket Guidelines

- *RCI_DataAnalysis* Contiene el código desarrollado para el análisis y explotación de datos.
- *RC_DataProcessing* Contiene el código desarrollado para la ingesta de los datos así como el procesamiento de estos.

## Estrategia CI/CD

Este repositorio contiene instrucciones para el ciclo de vida de desarrollo del proyecto *RCI* como parte de estrategia de CI/CD de Axity IM.

para utilizar este repositorio se debe utilizar **Fork** para trabajar desde su cuenta de BitBucket.

NOTA: NO agregue archivos a su repositorio a través de la interfaz del navegador BitBucket. Para más información sobre esto, lea `README_BitBucket.adoc`

Durante el desarrollo del proyecto, siga los siguientes **lineamientos**:

- Se usará BitBucket para recibir sus avances del trabajo asignado acorde a `backlog oficial` haciendo **PR** desde su fork/copia local. Tendremos cada repositorio de BitBucket como una copia de seguridad adicional de lo que está en nuestros equipos. Los únicos cambios se deben realizar directamente en su copia de BitBucket atraves de `Issues` y `Milestones`, que se describen a continuación:

- Agregue los siguientes usuarios como colaboradores a su repositorio de BitBucket. Dado que tenemos un equipo de desarrollo el trabajo será validado por los siguientes miembros del equipo, `jerryespn`, `eluddejesus`, `cariikat`, `radianv`.

- Agregar a estos miembros del equipo como Colaboradores les permitirá crear `pull requests` en su trabajo. Esta es una forma de validar sus `pull request` sin cambiarlos directamente. El `pull request` es un registro de esa interacciones.

- Utilizamos la función `Issue` de BitBucket para establecer un flujo de trabajo en torno a los envíos de sus activiades.

- Para cada actividad del trabajo asignado en base al `Backlog`, como Ingestion, Almacenamiento o Exploración, utilizará un `Issue` para realizar un seguimiento de su progreso. También usará las `Labels` de BitBucket para marcar el estado actual de cada actividad asignada (por ejemplo, enviado, bloqueado, revisión). Los lideres de cada track usarán estas etiquetas para revisar su trabajo una vez que lo haya marcado para `revisión` (como completo o 'incompleto').

Puede incluir mensajes de error o comentarios del `Issue`, o tomar una captura de pantalla para mostrar la condición actual de su avance. Es muy posible que estos pasos iniciales lo ayuden a resolver el problema usted mismo. De lo contrario, le mostrarán a un responsable de track lo que ha intentado hasta ahora.

- Finalmente, utilizaremos BitBucket Milestones para separar su trabajo a corde a la estrategia tecnologica `DataProcessing` de su trabajo de `DataAnalysis.

Antes de iniciar con su trabajo, será necesario realizar los siguientes ajustes a su repositorio de BitBucket:

* Agregar colaboradores desde las siguientes opciones: `Settings -> Collaborators`.
* Habilitar `Issues` debajo de `Settings -> Options`. Click en `Features` y habilitar `Issues`.
* Click en el tab de `Issues` y en el botón de `Milestones`
  * Generar dos milestones: `Ingestion, `Storing` and `Exploration`
  * Ajustar las fechas de entrega de acuerdo con el `Backlog Planning`

* Click en el botón `Labels` y ajustar las etiquetas como se describe a continuación:
  * Cambiar `bug` a `stuck`
  * Cambiar `duplicate` a `started`
  * Cambiar `enhancement` a `didNotSubmit`
  * Cambiar `help wanted` a `complete`
  * Cambiar `invalid` a `review`
  * Agregar la etiqueta `WorkInProgress` configurarla en morado
  * Cambiar `wontfix` a `incomplete`; configurar la etiqueta en el siguiente color: `#fbca04`
  * Dejar el "Issue" `question` tal cual está


Uno de los líderes abrirá un issue en su repositorio una vez confirmada la invitación a colaborar. Asimismo llevará a cabo la revisión del repositorio para todas las configuraciones descritas anteriormente. Los "issues" únicamente serán cerrados por el líder asignado como colaborador y no será necesaria ninguna revisión posterior.

## AT&T Documentación Complementaria y Presentaciones por SPRINT

- *1_Preparacion_Inicial:* Contiene información que proporciona el área de negocio para poder iniciar con el proceso de análisis y diseño, planes de trabajo, etc.

- *2_Analisis_Diseño:* Contiene los documentos generados por el equipo de desarrollo, aquí se presenta la propuesta y diseño de la solución al requerimiento solicitado por el área de negocio.
    
  - [Análisis: Cómo se encuentra el cliente actualmente y cuál es la necesidad de negocio](http://10.103.133.122/app/owncloud/f/14480813)
  - [Diseño: Propuesta Axity para dar solución a la necesidad de negocio](http://10.103.133.122/app/owncloud/f/14480777)

- *3_Ejecucion:* Contiene la documentación y códigos que dan solución al requerimiento solicitado. En esta carpeta se deberán ir generando sub carpetas con el número de sprints que se van liberando.
  - [Sprint 1: Presentación](http://10.103.133.122/app/owncloud/f/14480814)
  - [Sprint 2: Presentación](http://10.103.133.122/app/owncloud/f/14481175)
  - [Sprint 3: Presentación](http://10.103.133.122/app/owncloud/f/14481193)
  - [Sprint 4: Presentación](http://10.103.133.122/app/owncloud/f/14492657)
  - [Sprint 5: Presentación](http://10.103.133.122/app/owncloud/f/14492859)
  - [Sprint 6: Presentación](http://10.103.133.122/app/owncloud/f/14492860)
  - [Sprint 7: Presentación](http://10.103.133.122/app/owncloud/f/14494637)