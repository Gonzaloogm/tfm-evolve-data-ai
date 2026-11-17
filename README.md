# Proyecto Transversal · Máster Data Science e IA (Evolve Academy)

Repositorio común del equipo para el proyecto transversal del máster. Se irá completando actividad a actividad (0 a 8).

## Equipo

| Nombre y apellidos | Rol principal | Usuario de GitHub |
|---|---|---|
| Gonzalo Gardón Martín | Cloud, Backend y MLOps | [@Gonzaloogm](https://github.com/Gonzaloogm) |
| Vanessa Carnero Olivares | Estadística y ML | [@vanessacarn](https://github.com/vanessacarn) |
| Ricardo Jiménez Fosado | Negocio, FinOps y Agile | [@jimenezfosadoricardo-sudo](https://github.com/jimenezfosadoricardo-sudo) |

## Estado del proyecto

**Actividad 1 entregada; siguiente, Actividad 2 (SQL y capa gold). Idea definitiva: Radar de Oportunidades**, un radar de licitaciones públicas TI con baja concurrencia a partir de los datos abiertos de la Plataforma de Contratación del Sector Público (PLACSP). La decisión y su motivo están en [`docs/decisiones.md`](docs/decisiones.md). Las otras cuatro propuestas siguen documentadas en [`docs/entregas/00_ideas.md`](docs/entregas/00_ideas.md).

## Índice de entregas

| Actividad | Documento |
|---|---|
| 0. Equipo, ideas y repositorio | [docs/entregas/00_ideas.md](docs/entregas/00_ideas.md) |
| 1. Python: fuentes de datos, EDA y limpieza | [docs/entregas/01_python.md](docs/entregas/01_python.md) · notebook [notebooks/01_python.ipynb](notebooks/01_python.ipynb) |

Registro de decisiones del proyecto: [docs/decisiones.md](docs/decisiones.md).

### Exploración de datos (previa a la Actividad 1)

| Contenido | Enlace |
|---|---|
| Radar: análisis de los ficheros mensuales de PLACSP (septiembre y octubre de 2026) | [radar-oportunidades/](radar-oportunidades/README.md) |
| Radar: prueba preliminar de concurrencia en lotes TI | [docs/notas_fuentes/radar_prueba_concurrencia.md](docs/notas_fuentes/radar_prueba_concurrencia.md) |
| RevPAR Pulse: inspección de Inside Airbnb y agenda de Madrid | [docs/notas_fuentes/idea1_gonzalo.md](docs/notas_fuentes/idea1_gonzalo.md) |

## Instrucciones de ejecución

1. Crear el entorno (Python 3.12 o superior; probado con 3.13) e instalar las dependencias:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # en Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Descargar los ficheros mensuales de PLACSP en `data/raw/placsp/`, como se explica en [data/README.md](data/README.md).
3. Ejecutar [notebooks/01_python.ipynb](notebooks/01_python.ipynb) de principio a fin. Genera la capa silver en `data/silver/`.

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| `docs/entregas/` | Fichas de cada actividad |
| `docs/notas_fuentes/` | Notas de las comprobaciones de fuentes |
| `notebooks/` | Notebooks ejecutables (EDA y limpieza) |
| `src/radar/` | Código reutilizable: lectura de PLACSP y etiquetas de códigos |
| `data/` | Datos locales (no versionados) y muestras pequeñas en `data/muestras/` |
| `radar-oportunidades/` | Análisis exploratorio previo de los ficheros mensuales (11/11/2026) |

## Datos

Los datos crudos y procesados no se suben al repositorio (ver `.gitignore`). Fuente, condiciones de uso, forma de obtenerlos y diccionario de la capa silver: [data/README.md](data/README.md).
