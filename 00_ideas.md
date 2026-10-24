# Actividad 0: Equipos, ideas de producto y repositorio

## 1. Composición del equipo y justificación
- **Gonzalo Gardón Martín** @Gonzaloogm
- **Vanessa Carnero Olivares** @vanessacarn
- **Ricardo Jiménez Fosado** @jimenezfosadoricardo-sudo
- **Enlace al repositorio común:** `https://github.com/Gonzaloogm/tfm-evolve-data-ai`

**Justificación del equipo de tres.** Cada persona cubre un frente distinto del proyecto: Gonzalo, la parte de ingeniería (datos en SQL, backend, despliegue y MLOps); Vanessa, la estadística y el modelado; y Ricardo, la visión de negocio, los costes y la gestión ágil. Con tres personas podemos repartir las actividades sin que nadie quede como cuello de botella y revisar el trabajo entre nosotros.

**Convención de esta ficha.** "Confirmado" significa que el equipo ha descargado una muestra y comprobado el acceso y la licencia, con fecha. "Hipótesis" significa fuente candidata cuyo acceso o licencia todavía no se han comprobado.

---

## 2. Propuestas de Producto

### Idea 1: RevPAR Pulse — Asistente de Pricing Dinámico y Demanda Local para Alojamientos Urbanos

#### Título y descripción
**RevPAR Pulse** es una herramienta de inteligencia de precios y demanda para gestores de alojamientos turísticos de corta estancia en Madrid. Combina el histórico de disponibilidad y precios del mercado local con la presión de la agenda cultural y de eventos de la ciudad para recomendar tarifas diarias y explicar de forma transparente qué factores impulsan cada ajuste.

#### Problema y usuario
- **Usuario objetivo:** Pequeños propietarios y gestores profesionales (*property managers*) de entre 3 y 30 apartamentos turísticos o pequeños hostales en Madrid.
- **Necesidad y solución actual:** Fijar la tarifa por noche con semanas de antelación es crítico: si el precio es demasiado bajo durante un evento local, pierden margen; si es demasiado alto en días valle, la noche queda vacía. Actualmente lo resuelven con tarifas estáticas por temporada en Excel, copiando a ojo los precios de los pisos vecinos o con herramientas genéricas que desconocen la agenda municipal de eventos de cada distrito. *Hipótesis: la contrastaremos con 3-5 entrevistas a gestores.*

#### Uso y valor
Cuando el gestor planifica sus tarifas para las próximas semanas, consulta en la interfaz su alojamiento y el calendario. El producto le muestra para cada fecha la probabilidad estimada de ocupación, la presión de eventos cercanos en su zona, una tarifa recomendada y un desglose explicativo (ej. *"Se recomienda subir la tarifa el sábado por alta densidad de eventos culturales a menos de 1,5 km y alta ocupación estimada en tu barrio"*), acompañado de un resumen generado por IA sobre qué eventos concretos atraen público a su distrito.

#### Datos
- **Fuente 1 (Precios y disponibilidad):** *Inside Airbnb — Madrid* (`listings.csv` y `calendar.csv`: precios, disponibilidad diaria, coordenadas y atributos del inmueble).
  - *Estado y licencia:* **Hipótesis** (descarga pública en `insideairbnb.com`; muestra aún no descargada a fecha [dd/mm/aaaa]). Licencia: [copiar el texto literal de la página de datos de Inside Airbnb, con enlace]. Datos de anfitriones e inmuebles sin información personal sensible [por confirmar en la muestra].
  - *Limitación importante:* `calendar.csv` indica si una noche está **disponible o no**, no si fue **reservada**. Una noche no disponible puede ser una reserva o un bloqueo del anfitrión. Usaremos la no disponibilidad como *aproximación* (proxy) de ocupación y lo declararemos así en todos los resultados.
- **Fuente 2 (Eventos de la ciudad):** *Portal de Datos Abiertos del Ayuntamiento de Madrid — Agenda de Actividades y Eventos* (`300107-0-agenda-actividades-eventos`, CSV/JSON con fechas, horarios, coordenadas, distrito y recinto).
  - *Estado y licencia:* **Hipótesis** (muestra aún no descargada a fecha [dd/mm/aaaa]). Condiciones de reutilización: [copiar el texto literal del portal, con enlace].
- **Hipótesis pendientes de validar:**
  - Si la agenda del Ayuntamiento conserva eventos pasados o solo publica los futuros. Si no conserva histórico, no podremos cruzarla con ocupación pasada.
  - Cuántos cortes (*snapshots*) históricos de Inside Airbnb hay para Madrid y qué periodo cubren.
  - Si el precio de `calendar.csv` varía lo suficiente en el tiempo para estudiar su efecto.

#### Primera versión o MVP
- **Qué incluirá funcionando:** Pipeline reproducible de limpieza y cruce geográfico-temporal en base de datos SQL (capa `gold` por zona y fecha), análisis estadístico del impacto de eventos en la no disponibilidad, un modelo predictivo comparado contra un baseline estático con validación temporal (con restricción de monotonicidad respecto al precio si los datos lo permiten), una interfaz web con el calendario de recomendaciones y desglose de variables, y un asistente LLM que resume los eventos cercanos.
- **Qué queda fuera por ahora:** Integración con las APIs privadas de Airbnb/Booking y la ingesta de clics en tiempo real a gran escala (se evaluará solo como escenario de escalabilidad en la Actividad 8).

#### Viabilidad y dudas
- **Principal dificultad:** En los datos históricos, cuando la demanda es alta los precios suben y aun así se llenan (sesgo de confusión). Debemos comprobar en las Actividades 3 y 4 si las variables de contexto (ocupación del barrio, distancia a eventos y antelación) permiten acercarnos a la sensibilidad al precio. Si no, el producto se limitará a previsión de ocupación y explicación de factores.
- **Calidad de la variable objetivo:** disponibilidad no equivale a reserva (ver Datos). Es la duda más importante de esta idea.

---

### Idea 2: CartRescue AI — Predicción de Abandono de Carrito y Priorización de Sesiones en E-Commerce

#### Título y descripción
**CartRescue AI** es un sistema de analítica y decisión para responsables de comercio electrónico que estima la probabilidad de que una sesión con carrito termine en compra o en abandono, explica los factores que influyen y prioriza qué segmentos y categorías merecen una intervención.

#### Problema y usuario
- **Usuario objetivo:** Responsables de conversión, *growth managers* y directores de tiendas online medianas con catálogos amplios.
- **Necesidad y solución actual:** Gran parte de los carritos online se abandonan antes del pago [citar la fuente de la cifra, o eliminarla si no se encuentra]. Hoy las tiendas lo abordan con reglas estáticas (pop-ups de descuento para todos al salir, correos masivos horas después), que no distinguen entre quien iba a comprar de todos modos y quien duda. *Hipótesis: la contrastaremos con 3-5 entrevistas a responsables de tiendas online.*

#### Uso y valor
El gestor audita sus segmentos de abandono y consulta, por sesión y por categoría, la probabilidad estimada de compra y los factores que más pesan (categoría, rango de precio, número de productos vistos, comportamiento en el carrito). Con ello decide qué segmentos intervenir primero. Opcionalmente, un simulador con supuestos explícitos permite estimar el coste de distintas políticas de incentivo; el dato no contiene cupones ni descuentos, por lo que no estimamos un descuento exacto.

#### Datos
- **Fuente principal:** *REES46 Multi-Category eCommerce Behavior Dataset* (Kaggle), con eventos `view`, `cart`, `remove_from_cart` y `purchase` e `event_time`, `product_id`, `category_id`, `brand`, `price`, `user_id` y `user_session`. El volumen total es de cientos de millones de eventos repartidos en ficheros mensuales de varios GB.
  - *Estado y licencia:* **Hipótesis** (muestra aún no descargada a fecha [dd/mm/aaaa]). Licencia: [copiar el texto literal de la ficha de Kaggle, con enlace]. No damos por sentada ninguna licencia hasta leerla. Trabajaremos con una muestra temporal acotada y reproducible, y comprobaremos si la licencia permite redistribuir muestras en el repositorio; si no, solo se subirá el código que las descarga.
  - *Privacidad:* los identificadores de usuario y de sesión vienen seudonimizados. No se intentará reidentificar a nadie.
- **Hipótesis pendientes de validar:**
  - Que el evento `remove_from_cart` exista realmente en el fichero descargado (la documentación y los ficheros pueden no coincidir).
  - Duplicados de eventos y proporción de nulos en `brand` y `category_code`.
  - Variabilidad del precio por `product_id`: si es muy baja, no se podrá estudiar la sensibilidad al precio y el producto se centrará en abandono y explicación.

#### Primera versión o MVP
- **Qué incluirá funcionando:** Construcción de sesiones y tabla `gold` de embudos en SQL, contrastes estadísticos sobre patrones de abandono, experimento de ML con un baseline (tasa de conversión por categoría) y al menos dos modelos con validación temporal y métricas adecuadas a clases desbalanceadas, un dashboard interactivo con explicabilidad por segmento y un módulo LLM para consultar el comportamiento de las cohortes.
- **Qué queda fuera por ahora:** Despliegue de un widget en tiendas reales, estimación de cupones o descuentos exactos y procesamiento en tiempo real (el volumen se evaluará con cifras medidas en la Actividad 8).

#### Viabilidad y dudas
- **Principal dificultad:** Desbalanceo de clases (las compras son una fracción pequeña de los eventos), riesgo de fuga temporal si usamos información posterior al momento de la predicción y sesiones truncadas. Al ser una sola tienda en un periodo acotado, la generalización es limitada.
- **Volumen:** al ser grande, medir tamaño y tiempos de procesamiento nos permitirá decidir con cifras el enfoque de la Actividad 8.

---

### Idea 3: Radar de Oportunidades — Detección y Priorización de Licitaciones TI Desiertas o de Baja Concurrencia en Contratación Pública

#### Título y descripción
**Radar de Oportunidades** (nombre provisional) es un pipeline de datos y una herramienta de priorización para equipos comerciales B2B del sector tecnológico. Procesa los datos abiertos de la **Plataforma de Contratación del Sector Público (PLACSP)** sobre licitaciones TI (**CPV** división 72, servicios informáticos) para detectar las que quedan **desiertas o reciben muy pocas ofertas**, y las ordena con una puntuación explicable que indica por qué merece la pena acercarse a cada una.

#### Problema y usuario
- **Usuario objetivo:** Responsables comerciales y de desarrollo de negocio de consultoras tecnológicas e integradores de sistemas (pymes y medianas) que venden a administraciones públicas.
- **Necesidad y solución actual:** Para encontrar oportunidades revisan a mano las sedes electrónicas y los perfiles del contratante, sin una vista agregada de qué licitaciones TI han quedado desiertas o con una única oferta. Por ello no saben a qué órganos de contratación acercarse. Creemos que parte de esas licitaciones quedan desiertas por presupuestos o requisitos poco ajustados al mercado, pero eso no se puede verificar solo con los metadatos. *Hipótesis: la contrastaremos con entrevistas a 3-5 responsables comerciales.*

#### Uso y valor
Cada semana, el responsable comercial abre el ranking de licitaciones TI recientes. Filtra por organismo, comunidad e importe, ve las que quedaron desiertas o con una sola oferta y, para cada una, el motivo de su puntuación (ej. *"Puntuación alta: 180.000 €, desierta, y este organismo ha tenido baja concurrencia en 3 de sus últimas 5 licitaciones TI"*). Con ello decide a qué órganos de contratación acercarse y con qué prioridad.

#### Datos
- **Fuente principal:** *PLACSP — datos abiertos de licitaciones*, distribuidos mediante sindicación **Atom**, con los datos de cada licitación en formato **XML CODICE**. Variables previstas: importe de licitación (presupuesto base), número de ofertas, código CPV, órgano de contratación, tipo de procedimiento y estado de adjudicación.
  - *Estado y licencia:* **Hipótesis.** Aún no hemos descargado una muestra ni verificado las condiciones de reutilización. Muestra a fecha [dd/mm/aaaa]; licencia: [copiar el texto literal, con enlace]. Pendiente: confirmar campos disponibles y cobertura histórica.
- **Privacidad:** los adjudicatarios son sobre todo personas jurídicas. Si aparecen autónomos, se excluirán o seudonimizarán.
- **Fuera del MVP:** *Tenders Electronic Daily (TED)* para licitaciones europeas, y análisis de los pliegos técnicos en PDF con OCR y NLP. Se valorarán como ampliación o como función del módulo LLM en la Actividad 6.

#### Primera versión o MVP
- **Qué incluirá funcionando:** Ingesta reproducible de un periodo acotado del feed de PLACSP y parseo de las variables; capa `gold` en SQL con una fila por licitación TI; análisis estadístico de qué características (importe, organismo, tipo de procedimiento) se asocian a baja concurrencia; experimento de ML con un baseline (tasa histórica de baja concurrencia por organismo y CPV) y al menos dos modelos interpretables que estiman la probabilidad de que una licitación quede desierta o con una sola oferta (variable objetivo a confirmar según los campos disponibles); ranking en panel con filtros y desglose de la puntuación; y un asistente LLM que resume las licitaciones filtradas y explica la puntuación citando los registros usados.
- **Qué queda fuera por ahora:** TED, OCR y NLP sobre pliegos PDF, exportación de leads, alertas automáticas e integración con CRM.

#### Viabilidad y dudas
- **Principal dificultad:** Tres incertidumbres que comprobar en la Actividad 1:
  - **Prevalencia:** no sabemos cuántas licitaciones TI quedan desiertas. Si son pocas, habrá fuerte desbalance de clases.
  - **Consistencia:** campos como el número de ofertas o el estado pueden venir incompletos o codificados de forma distinta según el organismo.
  - **Relicitaciones:** no sabemos si el feed permite enlazar una licitación desierta con su posterior relicitación. Si no, el producto se limita a detectar desiertas y baja concurrencia.
- **Alcance de las conclusiones:** Los datos mostrarán asociaciones (por ejemplo, entre importe y concurrencia), no causas. No podremos afirmar que un presupuesto sea la causa de que una licitación quede desierta. Esa relación, y el valor de una alerta temprana, se contrastarán con entrevistas. Los procedimientos posteriores (relicitación o negociado sin publicidad) se documentarán con su fuente normativa antes de basar el producto en ellos.
- **Qué comprobaremos:** Descargar un periodo, medir la proporción de desiertas y el porcentaje de registros con campos completos, y copiar la licencia con su enlace.
