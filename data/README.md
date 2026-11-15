# Datos del proyecto

Los datos originales y procesados **no se suben al repositorio** (ver `.gitignore`). Esta guía explica cómo obtenerlos y regenerarlos. Solo se versionan las muestras pequeñas de `data/muestras/`.

## Fuente

**Plataforma de Contratación del Sector Público (PLACSP)**, Ministerio de Hacienda. Ficheros mensuales de la sindicación 643: *licitaciones publicadas en los perfiles del contratante ubicados en PLACSP, excluyendo los contratos menores*.

- Página oficial: [licitaciones publicadas en PLACSP](https://www.hacienda.gob.es/es-es/gobiernoabierto/datos%20abiertos/paginas/licitaciones_plataforma_contratacion.aspx)
- Condiciones de reutilización: [condiciones generales de datos abiertos de Hacienda](https://www.hacienda.gob.es/es-ES/GobiernoAbierto/Datos%20Abiertos/paginas/Datosabiertos.aspx). Hay que citar la fuente y la fecha de actualización, no alterar ni desnaturalizar la información ni sugerir respaldo institucional. El detalle está en la ficha de [`docs/entregas/01_python.md`](../docs/entregas/01_python.md).

## Cómo obtener la muestra

1. Descarga los dos ZIP mensuales (≈300 MB y ≈190 MB). Es una descarga manual desde el navegador:
   - `https://contrataciondelestado.es/sindicacion/sindicacion_643/licitacionesPerfilesContratanteCompleto3_202609.zip`
   - `https://contrataciondelestado.es/sindicacion/sindicacion_643/licitacionesPerfilesContratanteCompleto3_202610.zip`
2. Guárdalos **sin descomprimir** en `data/raw/placsp/`.
3. Comprueba que son los mismos ficheros usados en el análisis (SHA-256):
   - `202609`: `1d3730f0c8c77642f142fbe268ca802cb6af89443e615d8ba2bc68c57dd6d500`
   - `202610`: `ff33e8c0bd02fbd900589131137d7a2728a8f433c7e851a26edc8deb7b7afc4f`

   En macOS o Linux: `shasum -a 256 data/raw/placsp/*.zip`. En Windows: `Get-FileHash data\raw\placsp\*.zip`.

   PLACSP puede regenerar los ficheros mensuales. Si el hash no coincide, el resultado puede variar ligeramente; anota la fecha de descarga.

## Cómo generar la capa silver

Desde la raíz del repositorio, con el entorno instalado (`pip install -r requirements.txt`):

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_python.ipynb
```

O abre `notebooks/01_python.ipynb` y ejecuta todas las celdas en orden. La primera lectura de los ZIP tarda varios minutos; después se reutiliza la copia extraída.

## Estructura local

| Carpeta | Contenido | ¿En git? |
|---|---|---|
| `data/raw/placsp/` | ZIP originales, sin modificar | No |
| `data/raw/placsp/extraido/` | Tablas extraídas de los ZIP, como texto y sin limpiar (parquet). Se regeneran desde los ZIP | No |
| `data/silver/` | Capa silver: datos limpios de licitaciones TI (parquet) y resumen JSON | No |
| `data/muestras/` | Muestra de 200 expedientes de la silver en CSV, para revisar sin ejecutar | **Sí** |

## Capa silver

Alcance: versiones de expedientes con algún CPV **72** (servicios TI) o **48** (paquetes de software) presentes en los ZIP de septiembre y octubre de 2026.

### `placsp_ti_versiones.parquet` — una fila por versión de expediente (`atom_id` + `updated`)

| Campo | Tipo | Descripción |
|---|---|---|
| `atom_id` | texto | Identificador del expediente en el feed (URL). Clave junto a `updated` |
| `updated` | fecha y hora (UTC) | Momento de publicación de esta versión |
| `expediente` | texto | Número de expediente del órgano (`ContractFolderID`) |
| `titulo`, `enlace` | texto | Título y enlace público de la licitación |
| `estado`, `estado_desc` | texto | Estado de la versión (PUB en plazo, EV, ADJ, RES, ANUL, PRE) |
| `organo_nombre`, `organo_id`, `tipo_organo` | texto | Órgano de contratación (organismo público) e identificador DIR3 |
| `tipo_contrato`, `tipo_contrato_desc`, `subtipo_contrato` | texto | Tipo de contrato (servicios, suministros...) |
| `importe_sin_iva`, `importe_con_iva`, `valor_estimado` | decimal (€) | Presupuesto base de licitación y valor estimado. Nulo si falta o es ≤ 0 |
| `importe_invalido`, `importe_atipico` | booleano | Importe ≤ 0 original / importe por encima del percentil 99,9 |
| `moneda` | texto | Moneda del importe |
| `nuts`, `lugar` | texto | Lugar de ejecución (código NUTS y nombre) |
| `duracion`, `duracion_unidad` | decimal / texto | Duración prevista y su unidad (MON, ANN, DAY) |
| `cpv_principal`, `cpv_division`, `cpvs` | texto | CPV principal (8 dígitos), su división y todos los CPV separados por `\|` |
| `cpv_72`, `cpv_48` | booleano | Tiene algún CPV de la división 72 / 48 |
| `procedimiento`, `procedimiento_desc`, `procedimiento_negociado` | texto / booleano | Procedimiento de adjudicación |
| `urgencia`, `sistema_contratacion` | texto | Tramitación y sistema de contratación |
| `fin_presentacion` | fecha y hora | Fin del plazo de presentación de ofertas |
| `n_lotes` | entero | Número de lotes |
| `n_version`, `versiones_en_muestra` | entero | Orden de la versión y número de versiones del expediente en la muestra |
| `es_primera_version`, `es_ultima_version` | booleano | Primera / última versión del expediente dentro de la muestra |
| `es_primera_en_plazo` | booleano | Primera versión en estado PUB: **lo que se sabía mientras la licitación estaba abierta** |
| `tiene_borrado` | booleano | El expediente tiene un aviso de borrado en el feed |
| `archivo` | texto | ZIP mensual de origen |

### `placsp_ti_resultados.parquet` — una fila por resultado de lote (`atom_id` + `updated` + `orden_resultado`)

| Campo | Tipo | Descripción |
|---|---|---|
| `atom_id`, `updated` | texto / fecha | Versión a la que pertenece (clave externa a versiones) |
| `orden_resultado`, `lote` | entero / texto | Orden del resultado en la versión e identificador del lote |
| `resultado`, `resultado_desc` | texto | Resultado (3 desierto, 8 adjudicado, 9 formalizado...) |
| `ofertas` | entero | Ofertas recibidas (`ReceivedTenderQuantity`) |
| `adjudicado_sin_ofertas` | booleano | Adjudicado con 0 ofertas: inconsistente, se marca |
| `fecha_adjudicacion` | fecha | Fecha de adjudicación |
| `importe_adjudicacion_sin_iva` | decimal (€) | Importe de adjudicación sin IVA |
| `archivo` | texto | ZIP mensual de origen |

**Privacidad:** no se guardan adjudicatarios, que pueden ser personas físicas. Los órganos de contratación son organismos públicos.

**Etiquetas de códigos:** las columnas `*_desc` vienen de `src/radar/codigos.py` y están pendientes de verificar con las listas oficiales de PLACSP. Los análisis usan siempre el código.
