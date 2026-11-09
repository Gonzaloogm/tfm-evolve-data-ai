# Radar de Oportunidades — Prueba preliminar de concurrencia

**Autor:** Gonzalo Gardón Martín · **Fecha:** 09/11/2026
**Estado:** prueba exploratoria para orientar la variable objetivo. **No sustituye** a la muestra mensual ni a la ficha de la fuente, que lleva Ricardo (issues #1-#4).

## Objetivo
Comprobar, antes de comprometer el modelo, cuántas licitaciones TI quedan **desiertas** o con **poca competencia**. Si las desiertas son muy pocas, un modelo binario "desierta sí/no" estaría muy desequilibrado.

## Fuente y método
- **Fuente:** feed Atom público de la Plataforma de Contratación del Sector Público (PLACSP), `licitacionesPerfilesContratanteCompleto3.atom`, y sus páginas siguientes (enlace `rel="next"`).
  - URL: `https://contrataciondelestado.es/sindicacion/sindicacion_643/licitacionesPerfilesContratanteCompleto3.atom`
- **Muestra:** 8 páginas consultadas el 09/11/2026, con 5.118 entradas que corresponden a actualizaciones publicadas entre el **05/11/2026 y el 08/11/2026**.
- **Unidad de análisis:** el **lote**. Cada licitación puede tener varios lotes, y cada lote tiene su propio resultado y su número de ofertas.
- **Pasos:**
  1. Extraer de cada entrada los campos CODICE: `ContractFolderStatusCode` (estado), `ItemClassificationCode` (CPV), `ProcedureCode` (procedimiento), `TaxExclusiveAmount` (importe) y, por cada `TenderResult`, `ResultCode` y `ReceivedTenderQuantity` (ofertas recibidas).
  2. Quedarse con la **versión más reciente** de cada licitación y lote, porque el feed publica varias actualizaciones del mismo expediente.
  3. Considerar **resueltos** los lotes con `ResultCode` 3 (desierto), 8 (adjudicado) o 9 (formalizado).
  4. **TI** = CPV que empieza por 72 (servicios TI) o 48 (paquetes de software).
  5. **Baja concurrencia** = lote desierto o adjudicado con una oferta o menos.
- Los datos se procesaron en memoria y no se guardaron. El análisis se repite descargando las mismas páginas del feed.

## Resultados

| Grupo | Lotes resueltos | Desiertos | ≤1 oferta (de los adjudicados) | Baja concurrencia (desierto o ≤1 oferta) | Mediana de ofertas |
|---|---|---|---|---|---|
| Todas las licitaciones | 2.632 | 8,0% | 41,2% | 45,9% | 2 |
| **TI (CPV 72 y 48)** | **170 (140 expedientes)** | **5,3%** | **48,4%** | **51,2%** | **2** |
| TI, procedimiento abierto (código 1) | 69 | 2,9% | 34,3% | 36,2% | 2 |
| TI, abierto simplificado (código 9) | 45 | 11,1% | 37,5% | 44,4% | 2 |
| TI, restringido (código 2) | 18 | 0% | 33,3% | 33,3% | 3 |
| TI, negociado (código 3) | 33 | 6,1% | 100% | 100% | 1 |
| TI, importe ≥ 100.000 € | 88 | 1,1% | 47,1% | 47,7% | 2 |

Todos los lotes adjudicados de la muestra traen `ReceivedTenderQuantity` y `ResultCode` informados.

## Conclusiones
1. **"Desierta sí/no" no sirve como variable objetivo.** En TI solo quedan desiertas el 5,3% (9 casos en tres días), así que el modelo estaría muy desequilibrado.
2. **Propuesta de objetivo: "baja concurrencia"** (desierta o ≤1 oferta). En los procedimientos abiertos ronda el 36-44%, una clase razonablemente equilibrada, y responde a la pregunta del comercial: "¿tendré competencia?". Alternativa: predecir el **número de ofertas** (mediana 2, con cola larga).
3. **Excluir los procedimientos negociados.** En ellos, una sola oferta es lo normal por la naturaleza del procedimiento (100% en la muestra). Incluirlos haría que el modelo aprendiera una regla obvia y pareciera mejor de lo que es. El producto debería centrarse en los procedimientos abiertos, abiertos simplificados y restringidos.
4. **Volumen suficiente.** El feed publica unos 45-50 lotes TI resueltos al día. El histórico desde 2016 daría decenas de miles de lotes, lo que además apoya una posible Vía A en Big Data (Actividad 8).

## Limitaciones
- **Muestra corta:** 3 días de actualizaciones y 140 expedientes TI. Da el orden de magnitud, no una cifra definitiva. Hay que repetirlo con la muestra mensual.
- **Significado de los códigos:** `ResultCode` 3 = desierto, 8 = adjudicado, 9 = formalizado; `ProcedureCode` 1 = abierto, 2 = restringido, 3 = negociado, 9 = abierto simplificado. Se han **deducido** de los datos y del estándar CODICE, y hay que **confirmarlos con las listas de códigos oficiales de PLACSP**.
- **Uso de información posterior:** aquí se ha usado la versión más reciente de cada licitación para conocer su resultado. Para entrenar un modelo, las variables de entrada deben salir de la **versión publicada mientras la licitación estaba abierta** (issue #3), como pide el profesorado.
- **Sesgo de la ventana:** los lotes resueltos en esos días no tienen por qué representar a todo el año (estacionalidad, cierres de ejercicio).

## Siguientes pasos propuestos
- **Ricardo (#1, #2):** repetir la medición con la muestra mensual, separando por procedimiento y confirmando los códigos.
- **Vanessa (#6):** valorar "baja concurrencia" o "número de ofertas" como objetivo, con los negociados excluidos.
