# Actividad 0: Equipos, ideas de producto y repositorio

## 1. Composición del equipo y justificación
- **Gonzalo Gardón Martín** @Gonzaloogm
- **Vanessa Carnero Olivares** @vanessacarn
- **Ricardo Jiménez Fosado** @jimenezfosadoricardo-sudo
- **Enlace al repositorio común:** `https://github.com/Gonzaloogm/tfm-evolve-data-ai`

**Organización del equipo.** Somos tres personas con perfiles complementarios:
- **Gonzalo:** ingeniería (SQL, backend, despliegue y MLOps).
- **Vanessa:** estadística y modelado.
- **Ricardo:** negocio, costes, gestión ágil y contraste con usuarios.

Cada actividad tendrá un responsable principal y un revisor, indicados en su ficha de entrega. Los cambios se integrarán mediante *pull requests* revisadas por otro integrante, de modo que el historial de Git muestre la aportación de cada uno.

**Convención de esta ficha.** "Confirmado" significa que el equipo ha descargado una muestra y comprobado el acceso y la licencia, con fecha. "Hipótesis" significa fuente candidata cuyo acceso o licencia todavía no se han comprobado.

---

## 2. Propuestas de Producto

### Idea 1: RevPAR Pulse — Monitor de Precios Anunciados y Disponibilidad para Alojamientos Urbanos

#### Título y descripción
**RevPAR Pulse** es una herramienta para gestores de alojamientos turísticos de corta estancia en Madrid. Les muestra cómo evolucionan los **precios anunciados** y la **disponibilidad** de los anuncios comparables de su barrio, les avisa de las fechas en que la disponibilidad cae antes de lo habitual y les dice dónde queda su precio frente a esos comparables. **No estima reservas ni ingresos**, porque los datos no contienen reservas.

#### Problema y usuario
- **Usuario objetivo:** Pequeños propietarios y gestores profesionales (*property managers*) de entre 3 y 30 apartamentos turísticos en Madrid.
- **Necesidad y solución actual:** Para fijar sus tarifas con semanas de antelación necesitan saber qué fechas se están cerrando antes en su zona y si su precio está por encima o por debajo del mercado. Hoy lo hacen revisando a mano los anuncios vecinos en las plataformas, fecha a fecha, o con tarifas estáticas por temporada en Excel. *Hipótesis: la contrastaremos con 3-5 entrevistas a gestores.*

#### Uso y valor
Cuando el gestor planifica las próximas semanas, abre el calendario de su barrio y elige su tipo de alojamiento (por ejemplo, piso entero de 2-4 plazas). Para cada fecha ve:
1. **Disponibilidad de los comparables:** porcentaje de anuncios comparables que ya no están disponibles, frente a lo habitual con la misma antelación.
2. **Alerta de fecha tensionada** cuando la disponibilidad cae claramente por debajo de lo habitual.
3. **Precio anunciado de los comparables** (mediana y rango) y **la posición de su precio** dentro de ese rango.
4. **Explicación**, por ejemplo: *"Sábado 14: solo queda disponible el 22% de los pisos comparables de tu barrio, frente al 48% habitual a 30 días vista. Es festivo local. Tu precio (95 €) está en el 30% más barato de los comparables (mediana: 120 €)."*

Con eso el gestor decide si sube el precio o lo mantiene. El producto informa y la decisión es suya. Un asistente LLM responde preguntas sobre las fechas y los barrios, citando los datos que usa.

#### Datos
- **Fuente 1 (Precios anunciados y disponibilidad):** *Inside Airbnb — Madrid*. `listings.csv` aporta el precio anunciado, las coordenadas, el barrio y los atributos del inmueble; `calendar.csv` aporta la disponibilidad de los 365 días siguientes a cada corte.
  - *Enlaces:* [descarga](https://insideairbnb.com/get-the-data/) · [políticas de uso](https://insideairbnb.com/data-policies/)
  - *Estado y licencia:* **Acceso y licencia confirmados (27/10/2026).** La [página de descarga](https://insideairbnb.com/get-the-data/) indica literalmente *"This data is licensed under a Creative Commons Attribution 4.0 International License."* Para Madrid ofrece cuatro cortes trimestrales de descarga libre (14/12/2025, 24/03/2026, 20/06/2026 y 17/09/2026), es decir, *"generally quarterly data for the last 12 months"*. Los cortes anteriores hay que pedirlos con un *Archived Data Request*. Sus [políticas de uso](https://insideairbnb.com/data-policies/) piden citar la fuente y no republicar los datos, así que no se subirán al repositorio: solo el código y las instrucciones de descarga.
  - *Contenido:* **pendiente a 27/10/2026.** Falta descargar e inspeccionar `calendar.csv.gz` del corte del 17/09/2026 (responsable: Gonzalo): filas, columna `price` y reparto de `available`.
  - *Privacidad:* `listings.csv` incluye el nombre de pila y el identificador del anfitrión. No se necesitan y se excluirán en silver. Los campos exactos se confirmarán con la muestra (pendiente a 27/10/2026).
  - *Limitación asumida:* `calendar.csv` indica si una noche está **disponible o no**, no si fue **reservada**, porque puede ser un bloqueo del anfitrión. Por eso el producto habla siempre de **disponibilidad**, nunca de ocupación ni de reservas.
  - *Cómo usaremos los cortes:* cada corte mira 365 días hacia delante, así que la misma noche aparece en varios cortes con distinta antelación. Eso permite comparar la disponibilidad de una fecha con lo habitual a la misma antelación.
- **Fuente 2 (Agenda municipal):** *Portal de Datos Abiertos del Ayuntamiento de Madrid — Agenda de Actividades y Eventos* (`300107-0-agenda-actividades-eventos`).
  - *Enlaces:* [ficha del conjunto de datos](https://datos.madrid.es/en/dataset/300107-0-agenda-actividades-eventos) · [estructura del fichero](https://datos.madrid.es/FWProjects/egob/Catalogo/XComun/Ficheros/Estructura_DS_eventos_actividades.pdf) · [condiciones de uso](https://datos.madrid.es/pages/condiciones-de-uso)
  - *Estado y licencia:* **Confirmado (27/10/2026).** Hemos descargado el CSV publicado el 26/10/2026, con cobertura declarada hasta el 25/10/2026: **1.344 filas y 29 columnas**, una fila por actividad. La licencia es **CC BY 4.0** y las [condiciones de uso](https://datos.madrid.es/pages/condiciones-de-uso) *"permiten la reutilización de los documentos para fines comerciales y no comerciales"*. La actualización es diaria.
  - *Hallazgos:* **no conserva histórico**, porque solo recoge actividades actuales o futuras. **No tiene aforo** y recoge sobre todo actividad cultural municipal, no grandes eventos.
  - *Papel en el producto:* solo como **contexto del asistente LLM** para las fechas futuras. No entra en el análisis ni en el modelo.
- **Fuente 3 (Estacionalidad oficial):** *INE — Encuesta de Ocupación en Apartamentos Turísticos (EOAP), tabla 2083*, con datos mensuales de Madrid municipio.
  - *Enlaces:* [tabla 2083](https://www.ine.es/jaxiT3/Tabla.htm?t=2083) · [ficha en datos.gob.es](https://datos.gob.es/gl/catalogo/ea0010587-plazas-apartamentos-grados-de-ocupacion-y-personal-empleado-por-puntos-turisticos-mensual-municipios-encuesta-de-ocupacion-en-apartamentos-turisticos-identificador-api-20831.csv) · [aviso legal del INE](https://www.ine.es/aviso_legal)
  - *Estado:* **Acceso confirmado (27/10/2026)** mediante la API del INE: series mensuales de enero de 2005 a agosto de 2026. Condiciones de reutilización: pendiente a 27/10/2026 citar literalmente el aviso legal del INE.
  - *Papel en el producto:* contexto de temporada (mes alto o bajo) y contraste de tendencia: comprobar si la disponibilidad agregada de Inside Airbnb se mueve en sentido contrario a la ocupación oficial mes a mes. Es un contraste de coherencia, no una medida de reservas.
- **Fuente 4 (Festivos):** calendario laboral oficial de Madrid (festivos nacionales, autonómicos y locales). *Estado:* **pendiente a 27/10/2026** localizar la fuente oficial en datos abiertos y su licencia.

#### Primera versión o MVP
- **Qué incluirá funcionando:**
  1. Pipeline reproducible y capa `gold` en SQL con una fila por barrio, tipo de alojamiento, noche y corte: disponibilidad, antelación, precio anunciado (mediana y percentiles) y festivo.
  2. Análisis estadístico de si la disponibilidad y el precio anunciado difieren en festivos y fines de semana frente al resto de días.
  3. Modelo que predice la disponibilidad del barrio para una noche con 30 días de antelación, comparado con un baseline estacional (mismo día de la semana y mes) mediante validación temporal entre cortes.
  4. Interfaz web con el calendario, las alertas de fechas tensionadas y la posición del precio del gestor.
  5. Asistente LLM que explica las fechas y los barrios citando los datos usados.
- **Qué queda fuera por ahora:** estimación de reservas, ingresos o tarifa óptima (no hay datos de reservas), grandes eventos, integración con las APIs de Airbnb/Booking y procesamiento en tiempo real.

#### Viabilidad y dudas
- **Principal dificultad:** solo hay cuatro cortes trimestrales de libre descarga. Con ellos, cada noche se observa a pocas antelaciones distintas, lo que limita el modelo de la Actividad 4. Hay que comprobar con la muestra si basta para predecir mejor que el baseline. Si no, el producto se queda en análisis descriptivo y alertas por reglas.
- **Precio:** comprobar si `price` viene informado en `calendar.csv`. Si viene vacío, se usará el precio de `listings.csv` de cada corte, que es un precio por anuncio y no por noche.
- **Validación con usuarios:** concertar al menos una prueba de la tarea "decidir el precio de las próximas 4 semanas" con un gestor real (pendiente a 27/10/2026).

---

### Idea 2: CartRescue AI — Predicción de Abandono de Carrito y Priorización de Sesiones en E-Commerce

#### Título y descripción
**CartRescue AI** es un sistema de analítica y decisión para responsables de comercio electrónico que estima la probabilidad de que una sesión con carrito termine en compra o en abandono, explica los factores que influyen y prioriza qué segmentos y categorías merecen una intervención.

#### Problema y usuario
- **Usuario objetivo:** Responsables de conversión, *growth managers* y directores de tiendas online medianas con catálogos amplios.
- **Necesidad y solución actual:** Alrededor del 70% de los carritos online se abandonan antes del pago, según la media de estudios recopilada por [Baymard Institute](https://baymard.com/research/cart-abandonment-rate) (consultada el 27/10/2026). Hoy las tiendas lo abordan con reglas estáticas (pop-ups de descuento para todos al salir, correos masivos horas después), que no distinguen entre quien iba a comprar de todos modos y quien duda. *Hipótesis: la contrastaremos con 3-5 entrevistas a responsables de tiendas online.*

#### Uso y valor
**Momento de la predicción:** cada vez que una sesión añade un producto al carrito (evento `cart`), el sistema estima la probabilidad de que la sesión termine en compra usando **solo los eventos de esa sesión hasta ese instante**. La etiqueta es si la sesión acaba en `purchase`.

El gestor audita sus segmentos de abandono y consulta, por sesión y por categoría, la probabilidad estimada de compra y los factores que más pesan (categoría, rango de precio, número de productos vistos, comportamiento en el carrito). Con ello decide qué segmentos intervenir primero. Opcionalmente, un simulador con supuestos explícitos permite estimar el coste de distintas políticas de incentivo; el dato no contiene cupones ni descuentos, por lo que no estimamos un descuento exacto.

#### Datos
- **Fuente principal:** *REES46 Multi-Category eCommerce Behavior Dataset* (Kaggle), con eventos `view`, `cart`, `remove_from_cart` y `purchase` e `event_time`, `product_id`, `category_id`, `brand`, `price`, `user_id` y `user_session`. El volumen total es de cientos de millones de eventos repartidos en ficheros mensuales de varios GB (unos 9 GB solo noviembre de 2019).
  - *Enlace:* [ficha en Kaggle](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store)
  - *Estado y licencia:* **Hipótesis (pendiente a 27/10/2026).** Falta descargar un fichero mensual y leer la licencia de la ficha de Kaggle (responsable: Vanessa). No damos por sentada ninguna licencia hasta leerla. Trabajaremos con una muestra temporal acotada y reproducible, y comprobaremos si la licencia permite redistribuir muestras en el repositorio; si no, solo se subirá el código que las descarga.
  - *Privacidad:* los identificadores de usuario y de sesión vienen seudonimizados. No se intentará reidentificar a nadie.
- **Datos de una tienda real (feedback del profesorado):** el conjunto de Kaggle sirve para empezar, pero no demuestra que la solución funcione en una tienda concreta. **Pendiente a 27/10/2026:** buscar una tienda online colaboradora que comparta datos de eventos y un responsable con quien validar el producto. Si no la conseguimos antes de la Actividad 2, descartaremos esta idea como candidata final.
- **Hipótesis pendientes de validar:**
  - Que el evento `remove_from_cart` exista realmente en el fichero descargado (la documentación y los ficheros pueden no coincidir).
  - Duplicados de eventos y proporción de nulos en `brand` y `category_code`.
  - Variabilidad del precio por `product_id`: si es muy baja, no se podrá estudiar la sensibilidad al precio y el producto se centrará en abandono y explicación.

#### Primera versión o MVP
- **Qué incluirá funcionando:** Construcción de sesiones y tabla `gold` de embudos en SQL, contrastes estadísticos sobre patrones de abandono, experimento de ML con un baseline (tasa de conversión por categoría) y al menos dos modelos con validación temporal y métricas adecuadas a clases desbalanceadas, un dashboard interactivo con explicabilidad por segmento y un módulo LLM para consultar el comportamiento de las cohortes.
- **Qué queda fuera por ahora:** Despliegue de un widget en tiendas reales, estimación de cupones o descuentos exactos y procesamiento en tiempo real (el volumen se evaluará con cifras medidas en la Actividad 8).

#### Viabilidad y dudas
- **Principal dificultad:** Desbalanceo de clases (las compras son una fracción pequeña de los eventos), riesgo de fuga temporal si usamos información posterior al momento de la predicción y sesiones truncadas. Al ser una sola tienda en un periodo acotado, la generalización es limitada.
- **Cómo comprobaremos la utilidad:** con una partición temporal (entrenar con semanas anteriores y evaluar con las siguientes), mediremos qué parte de los abandonos se concentra en el 10-20% de sesiones mejor puntuadas, frente al baseline por categoría. Con la tienda colaboradora, el responsable revisará si esa priorización le sirve para decidir dónde intervenir.
- **Volumen:** al ser grande, medir tamaño y tiempos de procesamiento nos permitirá decidir con cifras el enfoque de la Actividad 8.

---

### Idea 3: Radar de Oportunidades — Detección y Priorización de Licitaciones TI Desiertas o de Baja Concurrencia en Contratación Pública

#### Título y descripción
**Radar de Oportunidades** (nombre provisional) es un pipeline de datos y una herramienta de priorización para equipos comerciales B2B del sector tecnológico. Procesa los datos abiertos de la **Plataforma de Contratación del Sector Público (PLACSP)** sobre licitaciones TI (**CPV** división 72, servicios informáticos; valoraremos incluir la división 48, paquetes de software) para detectar las que quedan **desiertas o reciben muy pocas ofertas**, y las ordena con una puntuación explicable que indica por qué merece la pena acercarse a cada una.

#### Problema y usuario
- **Usuario objetivo:** Responsables comerciales y de desarrollo de negocio de consultoras tecnológicas e integradores de sistemas (pymes y medianas) que venden a administraciones públicas.
- **Necesidad y solución actual:** Para encontrar oportunidades revisan a mano las sedes electrónicas y los perfiles del contratante, sin una vista agregada de qué licitaciones TI han quedado desiertas o con una única oferta. Por ello no saben a qué órganos de contratación acercarse. Creemos que parte de esas licitaciones quedan desiertas por presupuestos o requisitos poco ajustados al mercado, pero eso no se puede verificar solo con los metadatos. *Hipótesis: la contrastaremos con entrevistas a 3-5 responsables comerciales.*

#### Uso y valor
El producto separa dos vistas, porque responden a preguntas distintas:
1. **Licitaciones cerradas (resultado conocido).** Histórico de licitaciones TI ya resueltas: cuáles quedaron desiertas o con una sola oferta y qué organismos lo repiten. Es un dato observado, no una predicción, y sirve para decidir a qué órganos de contratación acercarse.
2. **Licitaciones abiertas (predicción).** Para las licitaciones TI en plazo, el modelo estima el **riesgo de baja concurrencia** a partir del histórico. Se muestra como estimación, con su explicación (ej. *"Riesgo alto: 180.000 €, procedimiento abierto, y este organismo tuvo una sola oferta en 3 de sus últimas 5 licitaciones TI"*), y se evalúa cuando la licitación se resuelve.

Cada semana, el responsable comercial revisa ambas vistas, filtra por organismo, comunidad e importe y decide a qué licitaciones presentarse y a qué organismos acercarse.

#### Datos
- **Fuente principal:** *PLACSP — datos abiertos de licitaciones*, distribuidos mediante sindicación **Atom**, con los datos de cada licitación en formato **XML CODICE**. Variables previstas: importe de licitación (presupuesto base), número de ofertas, código CPV, órgano de contratación, tipo de procedimiento y estado de adjudicación.
  - *Enlaces:* [datos abiertos de licitaciones (Ministerio de Hacienda)](https://www.hacienda.gob.es/es-ES/GobiernoAbierto/Datos%20Abiertos/Paginas/licitaciones_plataforma_contratacion.aspx) · [especificación de sindicación](https://www.hacienda.gob.es/Documentacion/Publico/D.G.%20PATRIMONIO/Plataforma_Contratacion/especificacion-sindicacion-1-3.pdf). Para leer los ficheros, la propia página ofrece la herramienta OpenPLACSP.
  - *Cobertura según la página (27/10/2026):* licitaciones agregadas desde el 1/1/2016, contratos menores desde el 1/1/2018 y consultas preliminares de mercado desde el 1/4/2022.
  - *Estado y licencia:* **Hipótesis (pendiente a 27/10/2026).** Falta descargar un mes del feed (responsable: Ricardo). La página dice que la información está "disponible para su reutilización", pero no nombra una licencia concreta. Revisaremos el [aviso legal](https://www.hacienda.gob.es/es-es/paginas/avisolegal.aspx) y copiaremos las condiciones literales antes de usar los datos. Pendiente también: confirmar los campos disponibles.
- **Privacidad:** los adjudicatarios son sobre todo personas jurídicas. Si aparecen autónomos, se excluirán o seudonimizarán.
- **Fuera del MVP:** *Tenders Electronic Daily (TED)* para licitaciones europeas, y análisis de los pliegos técnicos en PDF con OCR y NLP. Se valorarán como ampliación o como función del módulo LLM en la Actividad 6.

#### Primera versión o MVP
- **Qué incluirá funcionando:** Ingesta reproducible de un periodo acotado del feed de PLACSP y parseo de las variables; capa `gold` en SQL con una fila por licitación TI; análisis estadístico de qué características (importe, organismo, tipo de procedimiento) se asocian a baja concurrencia; experimento de ML entrenado **solo con licitaciones cerradas**, con un baseline (tasa histórica de baja concurrencia por organismo y CPV) y al menos dos modelos interpretables que estiman la probabilidad de que una licitación quede desierta o con una sola oferta (variable objetivo a confirmar según los campos disponibles), validado con una partición temporal; aplicación del modelo a las licitaciones abiertas; ranking en panel con filtros y desglose de la puntuación; y un asistente LLM que resume las licitaciones filtradas y explica la puntuación citando los registros usados.
- **Qué queda fuera por ahora:** TED, OCR y NLP sobre pliegos PDF, exportación de leads, alertas automáticas e integración con CRM.

#### Viabilidad y dudas
- **Principal dificultad:** Tres incertidumbres que comprobar en la Actividad 1:
  - **Prevalencia:** no sabemos cuántas licitaciones TI quedan desiertas. Si son pocas, habrá fuerte desbalance de clases.
  - **Consistencia:** campos como el número de ofertas o el estado pueden venir incompletos o codificados de forma distinta según el organismo.
  - **Relicitaciones:** no sabemos si el feed permite enlazar una licitación desierta con su posterior relicitación. Si no, el producto se limita a detectar desiertas y baja concurrencia.
- **Alcance de las conclusiones:** Los datos mostrarán asociaciones (por ejemplo, entre importe y concurrencia), no causas. No podremos afirmar que un presupuesto sea la causa de que una licitación quede desierta. Esa relación, y el valor de una alerta temprana, se contrastarán con entrevistas. Los procedimientos posteriores (relicitación o negociado sin publicidad) se documentarán con su fuente normativa antes de basar el producto en ellos.
- **Validación con usuarios:** probar con al menos un responsable comercial de una consultora TI la tarea "elegir a qué licitaciones abiertas presentarse esta semana" (pendiente de concertar a 27/10/2026; responsable: Ricardo).
- **Qué comprobaremos:** Descargar un periodo, medir la proporción de desiertas y el porcentaje de registros con campos completos, y copiar la licencia con su enlace.

---

### Idea 4: Asistente de ocupación y precios para espacios escénicos y festivales (nombre provisional)

#### Título y descripción
Herramienta que ayuda a gestores de espacios culturales y festivales a anticipar la ocupación de cada sesión y a decidir dónde concentrar promoción o ajustar tarifas. Se apoya en la asistencia histórica, la meteorología y la agenda de eventos simultáneos, y explica qué factores empujan cada previsión.

#### Problema y usuario
- **Usuario objetivo:** gestores de teatros y auditorios municipales, salas pequeñas y festivales.
- **Necesidad y solución actual:** programan y fijan tarifas con la experiencia de temporadas anteriores. Revisan la asistencia en hojas de cálculo y tienen poca información sobre qué sesiones suelen quedar vacías y por qué.
- *Hipótesis: la contrastaremos con 3-5 entrevistas a gestores.*

#### Uso y valor
Un gestor prepara la programación de la próxima temporada. Consulta la ocupación prevista por día de la semana, franja y tipo de espectáculo, identifica las sesiones con riesgo de baja ocupación y decide dónde reforzar la comunicación o probar una política de precios distinta.

#### Datos

| Fuente candidata | Qué aporta | Estado de acceso | Licencia | Limitaciones conocidas |
|---|---|---|---|---|
| [ICANE, "Recaudación de teatro"](https://datos.icane.es/sr_Latn/dataset/artes-escenicas/resource/08f46e22-02a4-4d5a-b423-d71130fdf489) (CSV y JSON-stat) | Recaudación de teatro | Hipótesis (pendiente a 27/10/2026) | La ficha del portal no indica licencia | Parece agregado. Granularidad por comprobar |
| [Ayuntamiento de Alcobendas, "Teatro Auditorio. Asistentes a espectáculos desde 2012. Histórico"](https://datos.gob.es/es/catalogo/l01280066-teatro-auditorio-asistentes-a-espectaculos-desde-2012-historico1) (datos.gob.es) | Asistentes por espectáculo | Hipótesis (pendiente a 27/10/2026) | Sin verificar a 27/10/2026 | La descripción menciona asistentes, no precio ni recaudación |
| [AEMET OpenData](https://opendata.aemet.es/) | Meteorología | Hipótesis (requiere clave gratuita; pendiente a 27/10/2026) | Sin verificar a 27/10/2026 | Cobertura por estación meteorológica |
| Agenda de eventos de ayuntamientos (por ejemplo, la [agenda del Ayuntamiento de Madrid](https://datos.madrid.es/en/dataset/300107-0-agenda-actividades-eventos)) | Eventos simultáneos en la ciudad | Hipótesis: fuente por localizar para cada ciudad | Madrid: CC BY 4.0. Resto sin verificar | Cobertura desigual. La de Madrid no conserva histórico (comprobado el 27/10/2026, ver idea 1) |

*Comprobación de muestras:* pendiente a 27/10/2026. Al descargar cada muestra se anotará su fecha y se cambiará su estado.

*Privacidad:* son datos agregados sin personas identificables.

#### Primera versión o MVP
- **Usuario y tarea:** un gestor que prepara la programación y decide dónde reforzar la promoción.
- **Mostraríamos:** previsión de ocupación por sesión frente a un baseline (media histórica por día y franja), identificación de sesiones de riesgo y explicación por factores.
- **El módulo de precio solo entra si los datos traen precio con variación suficiente.** Si no, el producto se limita a previsión de ocupación.
- **Dejamos fuera:** tiempo real, detección de bots e infraestructura distribuida.
- **Criterio de éxito:** el modelo mejora al baseline con validación temporal y el gestor entiende la explicación en una prueba breve.

#### Viabilidad y dudas
Lo que más nos preocupa es la granularidad. Si cada fila es un año o un mes, no podremos entrenar un modelo por sesión. Tampoco sabemos si alguna fuente trae precio, y sin variación de precio no se puede estimar su efecto. Además, la licencia de ICANE no consta. Comprobaremos qué representa una fila, el periodo cubierto, los nulos y la licencia en una hora de trabajo. Si la granularidad no basta, pasamos a otra de las ideas.
