# Actividad 1 · Python: fuentes de datos, EDA y limpieza

**Proyecto:** Radar de Oportunidades · **Equipo:** Gonzalo Gardón Martín, Vanessa Carnero Olivares, Ricardo Jiménez Fosado · **Fecha:** 15/11/2026

**Evidencias:** notebook [`notebooks/01_python.ipynb`](../../notebooks/01_python.ipynb) · parser [`src/radar/placsp.py`](../../src/radar/placsp.py) · códigos [`src/radar/codigos.py`](../../src/radar/codigos.py) · datos y diccionario de silver [`data/README.md`](../../data/README.md) · muestras [`data/muestras/`](../../data/muestras/) · decisiones [`docs/decisiones.md`](../decisiones.md) · análisis exploratorio previo de los ficheros mensuales [`radar-oportunidades/`](../../radar-oportunidades/README.md)

## 1. Idea candidata

**Radar de Oportunidades** es la idea definitiva del proyecto (ver [`docs/decisiones.md`](../decisiones.md)). CartRescue Marketplace dependía de que Brainy Commerce cediera datos y un revisor, y no hubo respuesta. Radar es la única propuesta con datos públicos reales que no depende de una colaboración externa.

**Problema que abordan los datos en esta actividad:** saber si los datos abiertos de contratación pública permiten identificar qué licitaciones TI reciben **poca competencia** (desiertas o con una sola oferta). Es la base de la pregunta del producto: *"¿a qué licitaciones abiertas merece la pena presentarse porque tendré poca competencia?"*.

## 2. Datos necesarios y para qué

| Información | Variables | Uso en el producto | Estado |
|---|---|---|---|
| Licitaciones TI y sus características | CPV, procedimiento, tipo de contrato, importe, órgano, lugar, duración, plazo, número de lotes | Variables explicativas del modelo y filtros del panel | **Obtenida** |
| Resultado de cada lote | Código de resultado (desierto, adjudicado, formalizado) y número de ofertas recibidas | Variable objetivo: baja concurrencia | **Obtenida** |
| Versión de cada licitación mientras estaba abierta | Estado de cada versión y fecha de publicación | Entrenar sin información posterior (solo lo que se sabía con la licitación abierta) | **Obtenida en parte**: dos meses no cubren la vida completa de todas las licitaciones |
| Histórico más largo | Ficheros mensuales anteriores (desde 2016) | Más casos para entrenar y validar en el tiempo | **Pendiente**: se ampliará en la Actividad 2 o en la 8 |
| Validación con un usuario real | Entrevista con un comercial o preventa de una consultora TI | Comprobar que la salida le ayuda a decidir | **Pendiente** (guía preparada en [S2](../../radar-oportunidades/docs/S2.md), sección H) |

## 3. Ficha de la fuente: PLACSP, sindicación 643

### Origen y acceso
- **Proveedor:** Ministerio de Hacienda, Dirección General del Patrimonio del Estado, a través de la Plataforma de Contratación del Sector Público (PLACSP).
- **Conjunto:** *licitaciones publicadas en los perfiles del contratante ubicados en PLACSP, excluyendo los contratos menores* (sindicación 643). Página oficial: [licitaciones publicadas en PLACSP](https://www.hacienda.gob.es/es-es/gobiernoabierto/datos%20abiertos/paginas/licitaciones_plataforma_contratacion.aspx).
- **Método:** descarga manual de un ZIP mensual por HTTPS, sin registro ni credenciales. Pasos y URL en [`data/README.md`](../../data/README.md).
- **Formato:** ZIP con varios documentos **Atom (XML)**. Cada entrada sigue el estándar **CODICE** ([especificación de sindicación v1.3](https://www.hacienda.gob.es/Documentacion/Publico/D.G.%20PATRIMONIO/Plataforma_Contratacion/especificacion-sindicacion-1-3.pdf)).
- **Ficheros usados:** `licitacionesPerfilesContratanteCompleto3_202609.zip` (302.945.644 bytes) y `..._202610.zip` (193.793.721 bytes), con su SHA-256 en `data/README.md`. Descargados el 11/11/2026 y el 15/11/2026.

### Condiciones de uso
- La página del conjunto lo ofrece como datos reutilizables en **modalidad básica, sin condiciones específicas**.
- Se aplican las [condiciones generales de reutilización de Hacienda](https://www.hacienda.gob.es/es-ES/GobiernoAbierto/Datos%20Abiertos/paginas/Datosabiertos.aspx): citar la fuente y la fecha de actualización, no alterar ni desnaturalizar la información, no sugerir respaldo institucional y conservar los metadatos de actualización. También el [aviso legal de Hacienda](https://www.hacienda.gob.es/es-ES/Paginas/AvisoLegal.aspx).
- **Uso previsto, transformación y publicación de muestras:** permitidos con esas condiciones. Por tamaño, en el repositorio solo se publica una muestra de 200 expedientes ya transformados, citando la fuente. Los ZIP originales no se suben.

### Protección y privacidad
- Los órganos de contratación son organismos públicos, y el título, el importe y el resultado de una licitación son información pública.
- Los **adjudicatarios** pueden ser personas físicas (autónomos). **No se extraen**: el parser no lee `WinningParty` y la silver no tiene ningún dato de adjudicatarios.
- Los datos completos solo están en los equipos del equipo; en el repositorio no hay credenciales, porque la fuente no las requiere.

### Frecuencia y cobertura
- **Generación:** continua. Cada cambio de estado de una licitación (publicación, adjudicación, formalización, anulación) crea una nueva versión.
- **Publicación:** el feed Atom se actualiza a diario; los ficheros mensuales se publican al cerrar cada mes. El retraso entre un cambio y su aparición en el fichero mensual es, como máximo, de un mes.
- **Periodo disponible:** licitaciones desde 2016. En esta actividad se usan los ficheros de septiembre y octubre de 2026. El de septiembre incluye versiones anteriores de los expedientes (desde 2021); el de octubre, solo las del mes.
- **Cobertura:** licitaciones de los perfiles del contratante alojados en PLACSP. **Quedan fuera** los contratos menores y las licitaciones de las plataformas autonómicas que no se agregan en esta sindicación, que se publican en otros conjuntos.
- **¿Sirve para el producto?** Sí. El producto trabaja con un ritmo semanal y el feed se actualiza a diario.

### Granularidad y variables
- **Unidad original:** una entrada Atom es una **versión de un expediente**, identificada por `atom_id` + `updated`. El mismo expediente aparece una vez por cada cambio de estado.
- Dentro de cada versión, los **resultados son por lote** (`TenderResult`): un expediente con 3 lotes tiene 3 resultados, cada uno con su código y su número de ofertas.
- **Identificadores:** `atom_id` (URL estable del expediente en el feed), `expediente` (número del órgano, que puede repetirse entre órganos) y `lote`.
- **Unidades:** importes en euros sin IVA (`importe_sin_iva`), con IVA y valor estimado; duración con su unidad (meses, años o días); fechas en ISO 8601 con zona horaria.
- El diccionario completo de la capa silver está en [`data/README.md`](../../data/README.md).

## 4. EDA y diagnóstico de calidad

Volumen leído (CPV 72 o 48): **11.768 versiones** de **4.692 expedientes** y **8.938 resultados de lote**, más 359 avisos de borrado. Todos los gráficos y tablas están en la sección 2 del notebook.

| Aspecto | Hallazgo | Consecuencia |
|---|---|---|
| Duplicados | 0 filas idénticas, pero 2.346 versiones repiten la clave `atom_id` + `updated` (el mismo cambio aparece en varios documentos Atom). En 369 el contenido difiere, casi siempre el `estado` (348) | Deduplicar quedándose con el documento más reciente |
| Cobertura temporal | Versiones desde 2021-09 (el ZIP de septiembre arrastra histórico) hasta 2026-10. La mayoría son de septiembre (6.507) y octubre (4.649) de 2026 | Se conservan todas las versiones con su fecha |
| Estados | En la última versión: 51,3 % resuelta, 17,3 % pendiente de adjudicación, 15,9 % adjudicada, 14,5 % en plazo | Muchos expedientes no tienen su versión en plazo en la muestra |
| Procedimiento | Abierto 44,0 %, abierto simplificado 27,3 %, negociado sin publicidad 12,0 %, restringido 12,0 % | Los negociados se tratan aparte |
| Tipo de contrato | Servicios 59,3 %, suministros 40,2 % | — |
| Importes | Mediana ≈ 96.000 €, p99 ≈ 22,3 M€, máximo 461 M€ (acuerdo marco real). 103 importes ≤ 0 en bruto | Escala logarítmica; los ≤ 0 pasan a nulo y los atípicos solo se marcan |
| Resultados | Formalizado 56,1 %, adjudicado 39,9 %, desierto 3,0 %. 85 lotes desiertos con ofertas > 0 (ofertas rechazadas) y ningún adjudicado con 0 ofertas | "Desierta sí/no" está muy desequilibrada |
| Nulos | Lote vacío en el 52,6 % de los resultados (contratos sin lotes); importe nulo en el 0,9 % de las versiones; ofertas nulas en el 0,9 % de los resultados | Esperado; no se imputa |

**Concurrencia por procedimiento** (lotes TI con resultado, versión limpia):

| Procedimiento | Lotes | % desiertos | % baja concurrencia | Mediana de ofertas |
|---|---:|---:|---:|---:|
| Abierto | 2.151 | 2,7 | 29,3 | 3 |
| Abierto simplificado | 854 | 6,1 | 43,2 | 2 |
| Negociado sin publicidad | 562 | 3,2 | 95,7 | 1 |
| Restringido | 521 | 6,0 | 43,2 | 2 |
| **Total TI** | **4.275** | | **43,6** | |
| **Total sin negociados** | **3.682** | | **35,4** | |

*Baja concurrencia* = lote desierto o adjudicado con 0-1 ofertas.

## 5. Decisiones de limpieza

Cada paso queda anotado en un registro dentro del notebook (sección 6) con las filas afectadas y el motivo.

| Paso | Qué se hace | Filas afectadas | Por qué |
|---|---|---:|---|
| L1 Duplicados | Por cada `atom_id` + `updated` se conserva la copia del documento Atom más reciente, y sus resultados | 2.346 versiones, 2.005 resultados | El mismo cambio aparece en varios documentos; el más reciente refleja el estado corregido |
| L2 Tipos | Importes y duración a decimal, ofertas y lotes a entero, fechas a fecha UTC | 0 valores no convertibles | Poder calcular y filtrar |
| L3 Valores inválidos | Importe ≤ 0 → nulo y marca `importe_invalido`; importe > p99,9 (95,1 M€) → solo marca `importe_atipico`; ofertas < 0 → nulo | 89 importes anulados, 7 marcados | Un presupuesto ≤ 0 no es válido; los importes altos son contratos reales |
| L4 Etiquetas y CPV | Etiquetas `*_desc` de los códigos, CPV de 8 dígitos, división, marcas `cpv_72`, `cpv_48` y `procedimiento_negociado` | — | Lectura humana y filtros del producto |
| L5 Versiones | Orden de versión, primera y última versión, `es_primera_en_plazo` y `tiene_borrado` | 1.092 expedientes con versión en plazo; 27 con borrado | Entrenar solo con lo que se sabía con la licitación abierta |
| L6 Columnas | Se eliminan columnas técnicas (`documento`) y se une la fecha y hora de fin de plazo | — | Silver más simple |

**Lo que no se hace, a propósito:** no se imputan nulos, no se eliminan importes altos y no se guardan adjudicatarios (privacidad). Las etiquetas de códigos están pendientes de verificar (#2); los análisis usan siempre el código.

## 6. Resultados: antes y después

| Tabla | Filas antes | Filas después | Columnas antes | Columnas después | Expedientes |
|---|---:|---:|---:|---:|---:|
| Versiones | 11.768 | 9.422 | 29 | 42 | 4.692 |
| Resultados | 8.938 | 6.933 | 10 | 11 | 3.156 |

Las 9 validaciones de la silver se cumplen: clave única en ambas tablas, ningún resultado sin versión, todas las versiones son TI, `updated` sin nulos, importes positivos o nulos, ofertas no negativas, una sola última versión por expediente y ninguna columna de adjudicatario.

Salidas: `data/silver/placsp_ti_versiones.parquet`, `data/silver/placsp_ti_resultados.parquet`, `data/silver/placsp_ti_resumen.json` y la muestra en `data/muestras/` (200 expedientes).

## 7. Conclusiones de viabilidad

1. **La fuente sirve para el producto.** Es pública, reutilizable, se actualiza a diario y contiene las características de cada licitación y, por lote, el resultado y el número de ofertas.
2. **La variable objetivo es viable.** La baja concurrencia afecta al 43,6 % de los lotes TI (35,4 % sin negociados), frente al 3 % de desiertos. Varía mucho según el procedimiento (29,3 % en abierto, 95,7 % en negociado sin publicidad), así que hay patrones que modelar. Los negociados se tratarán aparte.
3. **La calidad es buena y la limpieza, acotada.** El problema principal eran las versiones repetidas entre documentos; los nulos son pocos o tienen explicación.
4. **Limitación principal: falta histórico.** Solo 1.092 de 4.692 expedientes tienen su versión en plazo dentro de los dos meses. Para entrenar sin fuga de información hay que ampliar a 12 meses o más y unir la versión en plazo con el resultado final.
5. **Siguientes pasos:** verificar las etiquetas de códigos (#2), ampliar el histórico (Actividad 2) y validar con un comercial o preventa TI que la salida le ayuda a decidir.

## 8. Cómo reproducir

1. Crear el entorno: `python -m venv .venv`, activarlo e instalar `pip install -r requirements.txt`.
2. Descargar los dos ZIP en `data/raw/placsp/` según [`data/README.md`](../../data/README.md).
3. Ejecutar `notebooks/01_python.ipynb` de principio a fin (o `jupyter nbconvert --to notebook --execute --inplace notebooks/01_python.ipynb`).
4. La capa silver queda en `data/silver/` y la muestra en `data/muestras/`.
