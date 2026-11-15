"""Etiquetas legibles de los códigos CODICE que usa PLACSP.

Los cálculos del proyecto se hacen siempre sobre el código, no sobre la etiqueta.
Las etiquetas siguen las listas de códigos de CODICE/PLACSP según la documentación
consultada y están PENDIENTES DE VERIFICAR contra las listas oficiales publicadas en
contrataciondelestado.es (issue #2). Si un código no aparece aquí, se etiqueta como
"desconocido" y se conserva el código original.
"""

ESTADO = {
    "PRE": "Anuncio previo",
    "PUB": "En plazo",
    "EV": "Pendiente de adjudicación",
    "ADJ": "Adjudicada",
    "RES": "Resuelta",
    "ANUL": "Anulada",
}

PROCEDIMIENTO = {
    "1": "Abierto",
    "2": "Restringido",
    "3": "Negociado sin publicidad",
    "4": "Negociado con publicidad",
    "5": "Diálogo competitivo",
    "6": "Contrato menor",
    "7": "Derivado de acuerdo marco",
    "8": "Concurso de proyectos",
    "9": "Abierto simplificado",
    "10": "Asociación para la innovación",
    "11": "Derivado de asociación para la innovación",
    "12": "Basado en sistema dinámico de adquisición",
    "13": "Licitación con negociación",
    "100": "Normas internas",
    "999": "Otros",
}

# En los negociados es habitual recibir una sola oferta por la naturaleza del
# procedimiento; se tratan aparte al medir la concurrencia.
PROCEDIMIENTOS_NEGOCIADOS = {"3", "4"}

TIPO_CONTRATO = {
    "1": "Suministros",
    "2": "Servicios",
    "3": "Obras",
    "7": "Administrativo especial",
    "8": "Privado",
    "21": "Gestión de servicios públicos",
    "22": "Concesión de servicios",
    "31": "Concesión de obras",
    "32": "Concesión de obras públicas",
    "40": "Colaboración público-privada",
    "50": "Patrimonial",
    "999": "Otros",
}

RESULTADO = {
    "1": "Adjudicado provisionalmente",
    "2": "Adjudicado definitivamente",
    "3": "Desierto",
    "4": "Desistimiento",
    "5": "Renuncia",
    "6": "Desierto provisionalmente",
    "7": "Desierto definitivamente",
    "8": "Adjudicado",
    "9": "Formalizado",
}

# Resultados que cierran un lote y se usan para medir concurrencia.
RESULTADOS_DESIERTO = {"3"}
RESULTADOS_ADJUDICADO = {"8", "9"}

# Divisiones CPV de TI: 72 (servicios TI) y 48 (paquetes de software).
DIVISIONES_TI = ("72", "48")


def etiqueta(diccionario: dict[str, str], codigo: str | None) -> str | None:
    """Devuelve la etiqueta de un código, 'desconocido' si no está o None si falta."""
    if codigo is None or codigo == "":
        return None
    return diccionario.get(str(codigo), "desconocido")
