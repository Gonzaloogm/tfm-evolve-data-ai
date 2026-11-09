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
| Qué es una fila / nulos / precio | **Comprobado el 09/11/2026** (ver sección siguiente). Una fila es un anuncio y una noche. Sin nulos. **Sin columna de precio en `calendar`**: el precio es por anuncio, en `listings`. |
| Contradicciones con la ficha | Con cuatro cortes trimestrales, el histórico libre es corto: un año, con una foto cada tres meses. Para más profundidad hay que pedir los datos archivados. |

**Estado:** acceso, licencia y contenido comprobados (09/11/2026).

---

## Inside Airbnb — inspección de la muestra (09/11/2026)

**Ficheros descargados el 09/11/2026** (en `data/raw/`, que no se versiona): `calendar` de los cortes del 20/06/2026 y del 17/09/2026, y `listings` del corte del 17/09/2026.

| Punto | `calendar` 17/09/2026 | `calendar` 20/06/2026 |
|---|---|---|
| Qué es una fila | Un anuncio y una noche | Igual |
| Filas × columnas | 8.438.629 × 5 | 8.334.782 × 5 |
| Columnas | `listing_id`, `date`, `available`, `minimum_nights`, `maximum_nights` | Igual |
| Anuncios / noches | 23.109 / 19/09/2026 → 21/09/2027 | 22.835 / 20/06/2026 → 01/07/2027 |
| Nulos y duplicados (anuncio + noche) | 0 / 0 | 0 / 0 |
| Noches no disponibles | 47,9% | 47,3% |
| Anuncios no disponibles todo el año | 13,8% | 12,3% |

**No disponibilidad según la antelación (corte del 17/09/2026):** 83,2% a ≤7 días, 75,4% a 8-30 días, 47,8% a 31-90 días, 39,0% a 91-180 días y 47,7% a más de 180 días. La subida en el tramo más lejano apunta a anfitriones que cierran el calendario a largo plazo, no a reservas.

**Comparación entre cortes:** hay 5.793.043 noches (de 20.936 anuncios) presentes en los dos cortes. De las noches no disponibles en junio, el **22,6% pasa a estar disponible** en septiembre. Una reserva no suele deshacerse en esa proporción, así que "no disponible" mezcla reservas y bloqueos.

**`listings` 17/09/2026:** 23.109 anuncios × 90 columnas.
- `price`: vacío en el 18,7%; mediana de 151 € (p10: 54 €, p90: 346 €).
- `price_quote_*`: una sola cotización por anuncio, para una estancia de fechas y duración variables (1, 2, 3, 30 noches…).
- Por tanto, **el precio es por anuncio, no por noche**.
- Tipo de alojamiento: el 70% son viviendas enteras. Hay 128 barrios en 21 distritos. `license` está vacío en el 47,2%.
- Incluye `host_name` y `host_id`, que se excluirán en silver.

**Respuestas al feedback del profesor:**
- **¿El precio es por noche o por anuncio?** Por anuncio. `calendar` ya no trae precio.
- **¿Bastan cuatro cortes para prever a 30 días?** No. Con un corte cada tres meses no se puede seguir una misma noche desde 30 días antes hasta la estancia. Haría falta una frecuencia al menos mensual.

**Contradicciones con la ficha:**
1. La ficha contaba con `price` en `calendar`, y ya no existe.
2. El modelo de disponibilidad a 30 días no es viable con los datos libres.
3. La proporción de noches que se liberan entre cortes refuerza que la disponibilidad no es un buen sustituto de las reservas.
