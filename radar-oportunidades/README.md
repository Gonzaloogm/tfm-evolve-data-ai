# Radar de oportunidades PLACSP

Análisis exploratorio de licitaciones publicadas en la Plataforma de Contratación del Sector Público (PLACSP), a partir de sus ficheros mensuales de la sindicación 643. Estudia resultados de contratación, número de ofertas, CPV de servicios TI y software, posibles relicitaciones y expedientes sin adjudicación registrada.

Este repositorio contiene un *spike* analítico reproducible; no es todavía una aplicación de producción. Los métodos, resultados y limitaciones están documentados en [S2: septiembre de 2026](docs/S2.md) y [S3: octubre de 2026](docs/S3.md).

## Estructura

- `src/radar_oportunidades/analizar_643.py`: parser y análisis de los ZIP mensuales.
- `data/`: ubicación local para los ZIP de entrada y los resultados. Todo su contenido está excluido de Git.
- `docs/`: metodología, resultados, limitaciones y decisiones pendientes.
- `tests/`: reservado para pruebas; actualmente no contiene una suite.

## Requisitos

Python 3.12 o superior. El script usa únicamente la biblioteca estándar de Python y no requiere instalar paquetes adicionales ni crear un entorno virtual.

## Obtener el ZIP mensual

Si el ZIP no está en una carpeta o unidad compartida, puedes descargarlo desde la página oficial de [licitaciones publicadas en PLACSP](https://www.hacienda.gob.es/es-es/gobiernoabierto/datos%20abiertos/paginas/licitaciones_plataforma_contratacion.aspx) opción: "Licitaciones publicadas en los perfiles del contratante ubicados en la Plataforma de Contratación del Sector Público, excluyendo los contratos menores".

Guarda el ZIP localmente. Por ejemplo, para octubre de 2026, puedes colocarlo en:

`data/licitacionesPerfilesContratanteCompleto3_202610.zip`

No es necesario subir el ZIP a Git.

## Ejecución

Desde la raíz de este repositorio, ejecuta el script indicando la ruta del ZIP y la carpeta donde guardar los resultados:

```powershell
python ".\src\radar_oportunidades\analizar_643.py" `
  ".\data\licitacionesPerfilesContratanteCompleto3_AAAAMM.zip" `
  ".\data\salida_AAAAMM"
```

Sustituye `AAAAMM` por el año y mes del archivo. Por ejemplo, para octubre de 2026:

```powershell
python ".\src\radar_oportunidades\analizar_643.py" `
  ".\data\licitacionesPerfilesContratanteCompleto3_202610.zip" `
  ".\data\salida_202610"
```

El programa crea la carpeta de salida si no existe. Genera un resumen JSON y cuatro CSV: versiones, resultados, candidatos a relicitación y primeras versiones sin adjudicación. Los ZIP y los resultados son archivos locales que se pueden regenerar; no es necesario incluirlos en Git.

Para consultar los argumentos disponibles:

```powershell
python ".\src\radar_oportunidades\analizar_643.py" --help
```

## Interpretación y limitaciones

El mes analizado se determina por el campo `atom:updated`, que no necesariamente coincide con la fecha de publicación inicial del expediente. Los registros `TenderResult` pueden representar lotes y no expedientes únicos.

Las coincidencias de posibles relicitaciones son candidatos para revisión manual: no confirman que dos expedientes estén relacionados. La primera versión disponible en el ZIP tampoco tiene por qué ser la versión original del expediente.

Los informes detallan denominadores, criterios, cobertura y limitaciones. Los ZIP se validaron y pudieron parsearse, pero no se dispone de un inventario independiente que permita demostrar la exhaustividad de sus registros.

## Fuente de datos y reutilización

Los datos proceden de los ficheros mensuales oficiales de [licitaciones publicadas en PLACSP](https://www.hacienda.gob.es/es-es/gobiernoabierto/datos%20abiertos/paginas/licitaciones_plataforma_contratacion.aspx). Al compartir resultados, cita la fuente y la fecha de descarga o corte, conserva los metadatos aplicables y revisa las condiciones de reutilización resumidas en [S2](docs/S2.md).
