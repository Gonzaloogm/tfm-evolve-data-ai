# Notas de muestras — Idea 1 (RevPAR Pulse)

Responsable: Gonzalo Gardón Martín · Fecha de comprobación: 27/10/2026

Los datos no se suben al repositorio. Aquí solo van las notas y los enlaces de descarga.

---

## Fuente 1: Agenda de actividades y eventos (Ayuntamiento de Madrid)

| Punto | Resultado |
|---|---|
| Enlace | [Ficha del conjunto](https://datos.madrid.es/en/dataset/300107-0-agenda-actividades-eventos) · [CSV](https://datos.madrid.es/en/dataset/300107-0-agenda-actividades-eventos/resource/300107-2-agenda-actividades-eventos-csv/download/300107-2-agenda-actividades-eventos-csv.csv) · [estructura del fichero](https://datos.madrid.es/FWProjects/egob/Catalogo/XComun/Ficheros/Estructura_DS_eventos_actividades.pdf) |
| Fecha de descarga | 27/10/2026. El fichero está actualizado el 26/10/2026, con cobertura declarada "Until October 25, 2026". |
| Qué es una fila | Una actividad publicada en www.madrid.es (`ID-EVENTO`), con fecha de inicio y fin y la instalación donde se celebra. |
| Periodo y frecuencia | Actualización **diaria**. Solo incluye actividades que se van a celebrar o se están celebrando. La fecha de fin mínima es el 25/10/2026, así que **no hay histórico**. Las fechas de inicio llegan hasta el 06/07/2027 y se concentran en octubre (573) y noviembre (446) de 2026. Hay 526 actividades de larga duración, con fechas de fin que llegan hasta 2040. |
| Filas × columnas | 1.344 × 29 (todas las filas tienen 29 campos). Separador `;`, codificación UTF-8, unos 1,5 MB. |
| Nulos en campos clave | `ID-EVENTO`, `FECHA` y `FECHA-FIN`: 0%. `LATITUD`/`LONGITUD`, `DISTRITO-INSTALACION` y `TIPO`: 5,8%. `BARRIO-INSTALACION`: 6,9%. `HORA`: 20,4%. `DESCRIPCION`: 53,1%. `PRECIO`: 88,4%. `AUDIENCIA`: 65%. |
| Calidad | No hay `ID-EVENTO` duplicados. Todas las coordenadas válidas caen dentro de Madrid (latitud entre 40,3 y 40,6). Aparecen 23 valores de distrito. El 75% de las actividades son gratuitas (1.005 frente a 339). |
| Tipos más frecuentes | Cursos y talleres (254), programación destacada (157), conferencias (96), teatro (96), exposiciones (87), cine (84). |
| Licencia (literal) | Ficha: "Creative Commons Attribution 4.0 International (CC BY 4.0)". [Condiciones de uso](https://datos.madrid.es/pages/condiciones-de-uso): "Las condiciones generales permiten la reutilización de los documentos para fines comerciales y no comerciales." Permite el uso y la redistribución citando la fuente. |
| Contradicciones con la ficha | 1) **No conserva histórico**, por lo que no se puede cruzar con la ocupación pasada. 2) **No tiene ningún campo de aforo ni de asistencia**, así que no se puede ponderar cada evento por su tamaño. 3) **Cubre sobre todo actividad cultural municipal** y no los grandes eventos que mueven la demanda turística (estadios, IFEMA, congresos). |

**Conclusión:** la fuente es accesible y su licencia es clara, por lo que pasa a "Confirmado". Para la idea 1 no basta tal cual. Habría que guardar una descarga diaria desde ya para construir histórico y buscar una fuente complementaria de grandes eventos.

---

## Fuente 2: Inside Airbnb — Madrid

| Punto | Resultado |
|---|---|
| Enlace | [Página de descarga](https://insideairbnb.com/get-the-data/) · [políticas de uso](https://insideairbnb.com/data-policies/) |
| Ficheros del último corte | `https://data.insideairbnb.com/spain/comunidad-de-madrid/madrid/2026-09-17/data/listings.csv.gz` y `.../2026-09-17/data/calendar.csv.gz` |
| Cortes disponibles | Cuatro de descarga libre: 14/12/2025, 24/03/2026, 20/06/2026 y 17/09/2026. La página dice "generally quarterly data for the last 12 months. For additional data, make an archived data request." |
| Licencia (literal) | "This data is licensed under a Creative Commons Attribution 4.0 International License." Las políticas añaden que hay que atribuir y citar los datos, no republicarlos y descargarlos una sola vez. |
| Qué es una fila / nulos / precio | **Pendiente.** No se ha podido descargar automáticamente porque el servidor bloquea el acceso desde la herramienta. Hay que descargarlo a mano y comprobar: qué representa una fila de `calendar` (alojamiento × fecha), si `price` viene vacío, el reparto de `available` y si el precio varía entre cortes. |
| Contradicciones con la ficha | Con cuatro cortes trimestrales, el histórico libre es corto: un año, con una foto cada tres meses. Para más profundidad hay que pedir los datos archivados. |

**Estado:** el acceso y la licencia están comprobados, pero el contenido sigue en hipótesis hasta inspeccionar `calendar.csv.gz`.
