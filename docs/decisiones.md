# Registro de decisiones

Cambios relevantes del proyecto y su motivo, en orden cronológico.

| Fecha | Decisión | Motivo |
|---|---|---|
| 06/11/2026 | Se descarta Taquilla Pulse (antigua idea 4) | Fever no puede ceder sus datos de venta por confidencialidad |
| 09/11/2026 | Radar de Oportunidades pasa a ser la candidata principal provisional | Es la única propuesta con datos públicos reales que no depende de una colaboración externa (feedback del profesorado del 09/11/2026) |
| 09/11/2026 | RevPAR Pulse queda limitada a un explorador descriptivo | Inside Airbnb no trae precio por noche y los cortes trimestrales no sostienen una previsión a 30 días |
| 09/11/2026 | Cuándo Enchufo no se continúa | Margen de 12-22 €/año por coche frente a una regla sin previsión; habría que validar antes con hogares |
| 15/11/2026 | **Radar de Oportunidades es la idea definitiva** | Sin respuesta de Brainy Commerce a la propuesta de colaboración, CartRescue Marketplace no tiene datos ni revisor. Radar tiene datos públicos confirmados (PLACSP, septiembre y octubre de 2026) |
| 15/11/2026 | Alcance de la Actividad 1: licitaciones con CPV 72 o 48 de los ficheros mensuales de septiembre y octubre de 2026 | Es el segmento del producto (TI) y un volumen manejable para revisar el proceso |
| 15/11/2026 | La capa silver conserva todas las versiones de cada expediente y marca la primera versión en plazo | El modelo solo podrá usar lo que se sabía mientras la licitación estaba abierta (feedback del profesorado) |
| 15/11/2026 | Variable objetivo provisional: **baja concurrencia** (lote desierto o adjudicado con 0-1 ofertas), con los procedimientos negociados tratados aparte | Solo queda desierto un 3 % de los lotes TI (hasta un 6 % según el procedimiento), lo que desequilibraría un modelo binario "desierta sí/no". La decisión final corresponde a las Actividades 3 y 4 |
| 15/11/2026 | No se guardan adjudicatarios | Pueden ser personas físicas y no son necesarios para el producto |
| 17/11/2026 | Se fijan las versiones exactas de las dependencias en `requirements.txt` (pandas 3.1.1) | Con `pandas>=2.2` se instaló pandas 3, que escribe las fechas de las muestras en otro formato. Fijarlas garantiza que la silver y las muestras salgan idénticas en cualquier equipo |
| 17/11/2026 | La tasa de baja concurrencia (43,6 %) se presenta como descripción de los lotes resueltos en septiembre y octubre de 2026, no como tasa general | Censura temporal: solo 97 de los 1.092 expedientes con versión en plazo tienen ya resultado. Se revisará con el histórico de la Actividad 2 |
