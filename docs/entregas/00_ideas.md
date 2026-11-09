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

### Idea 1: RevPAR Pulse — Explorador de Precios Anunciados y Disponibilidad para Alojamientos Urbanos

#### Título y descripción
**RevPAR Pulse** es un explorador descriptivo para gestores de alojamientos turísticos de corta estancia en Madrid. Muestra la **disponibilidad** de los anuncios comparables de su barrio para las próximas fechas, según el último corte publicado, señala las fechas con menos disponibilidad de la habitual y sitúa el **precio anunciado** de su alojamiento frente al de esos comparables. **No predice reservas ni recomienda una tarifa óptima**: los datos no contienen reservas y solo traen un precio por anuncio, no un precio por noche.

#### Problema y usuario
- **Usuario objetivo:** Pequeños propietarios y gestores profesionales (*property managers*) de entre 3 y 30 apartamentos turísticos en Madrid.
- **Necesidad y solución actual:** Para revisar sus tarifas necesitan saber qué fechas se están cerrando antes en su zona y si su precio está por encima o por debajo del de anuncios parecidos. Hoy lo hacen revisando a mano los anuncios vecinos en las plataformas o con tarifas estáticas por temporada en Excel. *Hipótesis: la contrastaremos con 3-5 entrevistas a gestores.*

#### Uso y valor
Cuando el gestor revisa sus tarifas, abre la vista de su barrio y elige su tipo de alojamiento (por ejemplo, piso entero de 2-4 plazas). Ve dos cosas:
1. **Calendario de disponibilidad de los comparables** (último corte publicado): para cada fecha, el porcentaje de anuncios comparables que aparecen como no disponibles, frente a lo habitual para esa antelación en el mismo corte. Las fechas claramente por encima se marcan como **fechas con poca disponibilidad**. Es una foto del momento del corte, no una previsión.
2. **Posición de su precio:** el precio anunciado de los comparables (mediana y rango) y dónde queda el suyo. Es un precio por anuncio, no por fecha.

Ejemplo: *"Según el corte del 17/09, para el sábado 14 solo aparece disponible el 22% de los pisos comparables de tu barrio, frente al 48% habitual para esa antelación. Es festivo local. Tu precio anunciado (95 €) está entre el 30% más barato de los comparables (mediana: 120 €)."*

Con eso el gestor revisa su precio. El producto informa y la decisión es suya; no recomienda una tarifa. Un asistente LLM responde preguntas sobre las fechas y los barrios, citando los datos que usa.

#### Datos
- **Fuente 1 (Precios anunciados y disponibilidad):** *Inside Airbnb — Madrid*. `listings.csv` aporta el precio anunciado, las coordenadas, el barrio y los atributos del inmueble; `calendar.csv` aporta la disponibilidad de los 365 días siguientes a cada corte.
  - *Enlaces:* [descarga](https://insideairbnb.com/get-the-data/) · [políticas de uso](https://insideairbnb.com/data-policies/)
  - *Estado y licencia:* **Acceso y licencia confirmados (27/10/2026).** La [página de descarga](https://insideairbnb.com/get-the-data/) indica literalmente *"This data is licensed under a Creative Commons Attribution 4.0 International License."* Para Madrid ofrece cuatro cortes trimestrales de descarga libre (14/12/2025, 24/03/2026, 20/06/2026 y 17/09/2026), es decir, *"generally quarterly data for the last 12 months"*. Los cortes anteriores hay que pedirlos con un *Archived Data Request*. Sus [políticas de uso](https://insideairbnb.com/data-policies/) piden citar la fuente y no republicar los datos, así que no se subirán al repositorio: solo el código y las instrucciones de descarga.
  - *Contenido:* **confirmado (09/11/2026)** con los calendarios de los cortes del 20/06/2026 y del 17/09/2026 y los anuncios del 17/09/2026 (notas en `docs/notas_fuentes/idea1_gonzalo.md`). Cada fila de `calendar` es un anuncio y una noche: 8,4 millones de filas, unos 23.000 anuncios y 365 noches por corte, sin nulos ni duplicados. **`calendar` ya no incluye columna de precio**; solo `listing_id`, `date`, `available`, `minimum_nights` y `maximum_nights`. El 47,9% de las noches aparece como no disponible.
  - *Privacidad:* `listings.csv` incluye el nombre de pila y el identificador del anfitrión (`host_name`, `host_id`; comprobado el 09/11/2026). No se necesitan y se excluirán en silver.
  - *Limitación asumida:* `calendar.csv` indica si una noche está **disponible o no**, no si fue **reservada**, porque puede ser un bloqueo del anfitrión. Por eso el producto habla siempre de **disponibilidad**, nunca de ocupación ni de reservas.
  - *Cómo usaremos los cortes:* cada corte mira 365 días hacia delante, así que la misma noche aparece en varios cortes con distinta antelación. **Hallazgo (09/11/2026):** entre los cortes de junio y septiembre, el 22,6% de las noches que estaban no disponibles pasan a estar disponibles, y entre el 12% y el 14% de los anuncios están bloqueados todo el año. Esto confirma que "no disponible" mezcla reservas y bloqueos del anfitrión.
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
  1. Pipeline reproducible y capa `gold` en SQL con dos tablas: una fila por barrio, tipo de alojamiento, noche y corte (disponibilidad, antelación y festivo) y una fila por anuncio y corte (precio anunciado y atributos).
  2. Análisis estadístico de si la disponibilidad difiere en festivos y fines de semana, y de cómo varía el precio anunciado entre barrios y tipos de alojamiento.
  3. Experimento de ML de **precio de referencia**: estima el precio anunciado típico de un anuncio según sus características (barrio, tipo, capacidad…), comparado con un baseline (mediana del barrio y tipo). Sirve para situar el precio del gestor frente a anuncios parecidos; **no es una tarifa óptima ni predice reservas**.
  4. Interfaz web con el calendario de disponibilidad de los comparables, las fechas con poca disponibilidad y la posición del precio del gestor.
  5. Asistente LLM que explica las fechas y los barrios citando los datos usados.
- **Qué queda fuera:** previsión de disponibilidad o de reservas (los cortes trimestrales no la sostienen), precios por noche (solo hay precio por anuncio), estimación de ingresos o tarifa óptima, grandes eventos, integración con las APIs de Airbnb/Booking y procesamiento en tiempo real.

#### Viabilidad y dudas
- **Principal dificultad (comprobada el 09/11/2026):** con cortes cada tres meses, una misma noche solo se observa una vez por trimestre. No se puede seguir cómo cambia su disponibilidad entre 30 días antes y el día de la estancia, así que **los cuatro cortes no sostienen una previsión a 30 días**. Haría falta una frecuencia mensual o mayor, que no está disponible de forma libre. Por eso el MVP es descriptivo y no incluye ningún modelo de previsión de disponibilidad.
- **Precio (comprobado el 09/11/2026):** **es por anuncio, no por noche.** `listings.csv` trae un único `price` por anuncio (vacío en el 18,7%; mediana de 151 €) y una cotización (`price_quote_*`) para una sola estancia de fechas y duración variables según el anuncio. No permite construir una serie de precio por noche, así que el precio solo sirve para comparar anuncios entre sí en cada corte.
- **Validación con usuarios:** concertar al menos una prueba con un gestor real de la tarea "revisar mi precio frente a anuncios parecidos y ver qué fechas se están cerrando en mi barrio" (pendiente a 09/11/2026).

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

### Idea 4: CartRescue Marketplace — Previsión de ventas y alertas por producto para marcas en marketplaces (nombre provisional)

> **Idea condicionada a una colaboración.** Es la adaptación de CartRescue al caso de una agencia que gestiona marcas en Amazon y otros marketplaces. Solo será candidata si **Brainy Commerce** acepta compartir datos y validar el producto con nosotros (propuesta enviada; pendiente de respuesta a 06/11/2026).

#### Título y descripción
**CartRescue Marketplace** ayuda a los gestores de cuentas de marcas en marketplaces a detectar a tiempo **qué productos van a vender por debajo de lo esperado o pueden quedarse sin stock**, y a decidir dónde revisar el precio, la publicidad o la reposición. Compara las ventas de cada producto con su previsión, avisa cuando se desvía y explica qué factores empujan cada previsión.

#### Problema y usuario
- **Usuario objetivo:** gestores de cuentas (*account managers*) de una agencia que lleva marcas en Amazon y otros marketplaces, y las propias marcas.
- **Necesidad y solución actual:** cada gestor lleva muchos productos de varias marcas a la vez. Las caídas de ventas o las roturas de stock se detectan revisando informes a mano, a menudo cuando ya han costado ventas. *Hipótesis: la contrastaremos con el equipo de Brainy Commerce y con 3-5 entrevistas a gestores de cuentas.*

#### Uso y valor
Cada semana, el gestor abre el panel de sus cuentas y ve, para cada producto:
1. **Ventas observadas:** unidades, ventas y conversión hasta la fecha.
2. **Previsión** de las próximas semanas, con un rango.
3. **Alertas** cuando un producto se desvía de su previsión o el stock no cubre la demanda prevista. Por ejemplo: *"Producto X: −28% de unidades frente a la previsión en las dos últimas semanas, coincidiendo con una subida de precio del 12%. Con el stock actual hay cobertura para 9 días."*
4. **Explicación** de los factores: estacionalidad, precio, inversión publicitaria y campañas como Prime Day o Black Friday.

Con eso decide dónde actuar primero y tiene un argumento claro para hablar con la marca. La herramienta **distingue siempre lo observado de lo previsto**.

**Momento de la predicción:** cada semana, con los datos disponibles hasta ese día y sin información posterior.

#### Datos

| Fuente | Qué aporta | Estado (06/11/2026) | Licencia | Limitaciones conocidas |
|---|---|---|---|---|
| Datos de cuentas cedidos por Brainy Commerce | Por producto y día: sesiones, unidades, ventas, conversión, precio, inventario, categoría e inversión publicitaria | Hipótesis: pendiente de la colaboración | Acuerdo con el colaborador, con confidencialidad si hace falta | Sin colaboración, la idea se descarta. Marcas y productos anonimizados. Los datos no se subirán al repositorio |
| Calendario de campañas comerciales (Prime Day, Black Friday, rebajas) y festivos | Picos de demanda conocidos | Hipótesis: fuente por localizar | Pendiente | Calendario pequeño construido por el equipo, con la fuente de cada fecha |

*Privacidad:* datos agregados por producto y día, sin datos de clientes finales.

#### Primera versión o MVP
- **Qué incluirá funcionando:**
  1. Capa `gold` con una fila por producto y día.
  2. Análisis estadístico de la estacionalidad y del efecto de las campañas comerciales en las ventas.
  3. Modelo de previsión de ventas por producto, comparado con un baseline (ventas de las mismas semanas del año anterior o media móvil), usando validación temporal.
  4. Panel de productos con previsión, alertas de desviación y cobertura de stock.
  5. Asistente LLM que explica las alertas citando los datos.
- **Opción alternativa, a elegir con el colaborador:** priorizar la inversión publicitaria, detectando qué campañas y palabras clave gastan sin retorno. Solo entra si el colaborador lo prefiere a la previsión de ventas.
- **Fuera:** integración en tiempo real con las APIs de los marketplaces, cambio automático de precios o pujas e infraestructura distribuida.
- **Criterio de éxito:** el modelo mejora al baseline en las semanas reservadas para la prueba, y un gestor de cuentas usa las alertas para decidir en una prueba breve.

#### Viabilidad y dudas
- **Depende por completo de la colaboración.** Hay que confirmar antes de la Actividad 2 qué datos se pueden obtener, con qué periodo y nivel de detalle, y quién validará el producto.
- **Histórico y número de productos:** con menos de un año de datos no se puede separar bien la estacionalidad anual. Pediremos de 12 a 24 meses.
- **Sesgo de confusión en precio y publicidad:** el precio y la inversión suelen cambiar precisamente cuando las ventas van bien o mal. Los mostraremos como factores asociados, no como causas.
- **Confidencialidad:** si el acuerdo impide publicar los datos, acordaremos con el profesorado una vía de revisión y usaremos muestras anonimizadas o simuladas, declaradas como tales.

---

### Idea 5: Cuándo Enchufo — Planificador semanal de consumos aplazables para hogares con tarifa PVPC (nombre provisional)

> **Idea con limitaciones ya medidas.** Los datos son públicos y accesibles, pero una simulación con precios reales (corregida el 09/11/2026, ver *Viabilidad y dudas*) indica que **el valor añadido de la previsión a varios días es pequeño**. La mantenemos como propuesta para recibir feedback, declarando esa limitación.

#### Título y descripción
**Cuándo Enchufo** ayuda a los hogares con tarifa PVPC **a decidir cuándo hacer, en los próximos 7 días, los consumos que se pueden aplazar** (sobre todo cargar el coche eléctrico, y también el termo, el lavavajillas o la lavadora) para pagar menos, respetando sus plazos y horarios. Para el día siguiente usa los precios ya publicados; para los días posteriores, una previsión con su margen de error. Muestra el ahorro estimado en euros y explica por qué recomienda cada ventana.

#### Problema y usuario
- **Usuario objetivo:** hogares con tarifa PVPC con algún consumo aplazable. El perfil principal es el de **quien carga un coche eléctrico en casa**, porque es el consumo doméstico en el que el ahorro es más  apreciable (ver *Viabilidad y dudas*).
- **Necesidad y solución actual:** muchas de las apps y webs existentes permiten consultar los precios de hoy y del día siguiente, pero no necesariamente ayudan a decidir si conviene esperar unos días para realizar un consumo ni cuánto podría ahorrarse. Algunos usuarios pueden seguir estrategias fijas, como cargar siempre por la noche. *Hipótesis: la contrastaremos con 5-8 hogares con PVPC, de los que al menos 2 tengan coche eléctrico.*

#### Uso y valor
El usuario da de alta cada aparato una vez: consumo, duración, plazo y horas no permitidas. Recibe un **plan semanal**:
1. **Ventana recomendada** para cada consumo. Las recomendaciones para el día siguiente se basan en precios PVPC ya publicados, por lo que se consideran conocidas. Para los días posteriores se utilizan precios estimados por el modelo, acompañados de un intervalo de incertidumbre.
2. **Ahorro estimado en €** frente a su forma habitual de hacerlo.
3. **Explicación**, por ejemplo: *"El jueves se espera más eólica y es festivo nacional; cargar el coche de 13:00 a 17:00 ahorra unos 1,20 € frente a hacerlo esta noche."*

Cada noche, cuando REE publica los precios del día siguiente (sobre las 20:15-21:00), el plan se recalcula. Un asistente LLM responde preguntas sobre el plan usando el planificador y los datos, sin inventar cifras.

**Momento de la predicción:** cada día, tras la publicación de los precios del día siguiente, con la información disponible hasta ese momento.

#### Datos

| Fuente | Qué aporta | Estado (06/11/2026) | Licencia | Limitaciones conocidas |
|---|---|---|---|---|
| [REData (Red Eléctrica)](https://www.ree.es/es/apidatos): precios de mercado en tiempo real | Precio PVPC hora a hora (variable objetivo) | **Confirmado (06/11/2026):** descargado 01/11/2025-31/10/2026, **8.760 horas sin huecos**. Acceso sin token | La página de la API solo indica que admite consultas GET. Pendiente de revisar el aviso legal de REE | El PVPC es **horario** (24 valores al día). El mercado spot ya es cuartohorario, pero no afecta a la tarifa de los hogares |
| [ESIOS (Red Eléctrica)](https://www.esios.ree.es/) | Datos del mercado eléctrico, incluyendo precios spot y PVPC. | **Confirmado (07/11/2026):** token de acceso obtenido y primeras descargas de datos realizadas. | Pendiente | Las previsiones de REE solo llegan al día siguiente |
| Previsiones meteorológicas de viento e irradiación en varios puntos de la Península (p. ej. Open-Meteo, AEMET) | Variables para 2-7 días vista | Hipótesis: pendiente a 06/11/2026 | Pendiente | **Riesgo de fuga de información:** el archivo de previsiones históricas de Open-Meteo guarda solo las primeras horas de cada ejecución, no lo que se preveía a varios días. Pendiente comprobar si existe un histórico de previsiones con antelación real |
| Festivos nacionales | Calendario | Hipótesis: fuente por localizar | Pendiente | — |

*Nota:* el precio PVPC es común para los consumidores peninsulares acogidos a esta tarifa, por lo que el producto puede plantearse inicialmente para todo el territorio peninsular. Las variables meteorológicas y de calendario se estudiarán a escala adecuada para comprobar si aportan capacidad predictiva.

*Privacidad:* solo datos públicos agregados. Los datos de los hogares de la prueba (aparatos y horarios) se tratarán anonimizados.

#### Primera versión o MVP
- **Qué incluirá funcionando:**
  1. Pipeline diario de REData/ESIOS y capa `gold` con una fila por hora.
  2. Análisis estadístico: ¿cambia el precio en festivos y fines de semana? ¿Cuánto varía de un día a otro la ventana más barata?
  3. Previsión horaria del PVPC de 2 a 7 días vista, con rangos (cuantiles), comparada con tres baselines: regla fija, repetir el último día conocido y media del mismo día de la semana. Se usará validación temporal.
  4. Planificador sencillo: no es ML, elige para cada consumo la ventana de menor coste esperado dentro de sus condiciones.
  5. Interfaz con el plan semanal, diferenciando lo seguro de lo previsto, y con el ahorro.
  6. Asistente LLM que consulta el plan y lo explica.
- **Qué queda fuera por ahora:** control de enchufes o cargadores, autoconsumo solar, tarifas del mercado libre, y los sistemas no peninsulares.
- **Criterio de éxito:** en una simulación con el último año que use solo la información disponible en cada momento, **planificar con la previsión ahorra más que la mejor regla sin previsión**, con la misma energía y los mismos plazos. Además, los hogares de la prueba entienden la diferencia entre lo seguro y lo previsto.

#### Viabilidad y dudas
- **Limitación principal, medida con el PVPC real del último año** (01/11/2025-31/10/2026; simulación corregida el 09/11/2026). **Todas las estrategias sirven la misma energía y respetan el mismo plazo:** cada consumo debe hacerse dentro de su bloque de días, y el último día del bloque se hace sí o sí. **Todas las estrategias, salvo el techo, disponen en cada fecha de la misma información:** la decisión de cada día se toma con los precios de ese día, ya publicados por REE la tarde anterior, y con todos los precios pasados. Ninguna usa precios todavía no publicados. Coste anual según la estrategia:

| Consumo (misma energía y plazo en todas las columnas) | Hora fija | Mejor ventana del primer día | **Regla sin previsión** (umbral con precios pasados) | **Previsión ingenua** (media de 7 días) | Techo teórico (precios futuros perfectos) |
|---|---|---|---|---|---|
| Coche, 15 kWh, plazo 2 días, a cualquier hora | 235,67 € | 193,09 € | 177,00 € | 177,41 € | 164,34 € |
| Coche, 15 kWh, plazo 2 días, solo de noche (0-8 h) | 366,92 € | 363,77 € | 357,11 € | 358,37 € | 344,02 € |
| Coche, 22,5 kWh, plazo 3 días, a cualquier hora | 239,33 € | 195,50 € | 165,80 € | 166,37 € | 144,13 € |
| Coche, 22,5 kWh, plazo 3 días, solo de noche (0-8 h) | 370,02 € | 366,54 € | 347,98 € | 345,99 € | 333,54 € |
| Lavadora, 1 kWh, plazo 7 días (8-22 h) | 2,41 € | 2,25 € | 2,21 € | 2,23 € | 1,95 € |

*Hora fija:* 13-17 h para el coche a cualquier hora, 2-6 h de noche y 14-16 h la lavadora. *Regla sin previsión:* hacer el consumo el día que su mejor ventana esté por debajo del percentil 30 de los 28 días anteriores. *Previsión ingenua:* esperar si se prevé un día más barato en lo que queda de plazo. La **columna del techo no es un ahorro alcanzable**: supone conocer los precios futuros, así que solo marca el máximo teórico.

- **Qué significa:**
  - En el escenario analizado, el ahorro potencial de la lavadora es muy reducido (céntimos al año) debido a su bajo consumo energético y frecuencia de uso. Por ello, no parece el caso de uso prioritario.
  - En el coche eléctrico, la mayor parte del ahorro se consigue con dos estrategias que no necesitan modelos predictivos: cargar en las horas centrales del día en lugar de por la noche (unos 130 € al año) y elegir el día de carga con una regla sencilla basada en precios pasados (unos 60 € adicionales).
  - Una previsión ingenua no mejora a esa regla sin previsión (diferencias de entre −2 y +1 € al año).
  - El ahorro adicional máximo que podría aportar un modelo se sitúa aproximadamente entre 12 y 22 € al año por coche, que es la diferencia entre la regla sin previsión y el techo teórico. Un modelo real previsiblemente obtendría solo una parte.
  - Un primer análisis (06/11/2026) estimaba entre 30 y 55 €, pero no aplicaba los mismos plazos a todas las estrategias ni incluía una regla sin previsión. Esta versión lo sustituye.
  - La ventana más barata cambia respecto al día anterior el 63% de los días, y se desplaza 3 horas o más el 32%. La señal existe, pero su valor económico es limitado.
  - Para elegir esta idea habría que comprobar con hogares reales que valoran ese ahorro y la comodidad del plan; añadir predicción no basta por sí solo.
- **Otras limitaciones:**
  - Desde 2026, el 55% de la energía del PVPC se indexa a futuros y solo el 45% al mercado diario, y los peajes por periodos son fijos. Eso reduce la diferencia entre horas.
  - Hay muchas apps que ya muestran el precio de hoy y mañana. Lo único diferencial sería el plan a varios días con el ahorro calculado.
  - Las cuentas simplifican: la carga nocturna no cruza la medianoche y el consumo es fijo. No cambian el orden de magnitud.
- **Qué haríamos si se elige:** presentar el resultado tal cual, midiendo cuánto aporta prever a varios días y en qué casos no merece la pena. Sería una conclusión válida, aunque hace el producto menos contundente que otras ideas.
