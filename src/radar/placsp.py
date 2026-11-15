"""Lectura de los ficheros mensuales de licitaciones de PLACSP (sindicación 643).

Cada ZIP mensual contiene varios documentos Atom. Cada entrada Atom es una VERSIÓN de
un expediente: el mismo expediente aparece varias veces a medida que cambia de estado
(en plazo, pendiente de adjudicación, adjudicada...). Por eso se conservan todas las
versiones y no solo la última: para entrenar un modelo hay que poder usar lo que se
sabía mientras la licitación estaba abierta, sin información posterior.

Este módulo solo EXTRAE: devuelve los valores tal y como vienen en el XML (texto), sin
convertir tipos ni corregir nada. La limpieza se hace después, en el notebook
`notebooks/01_python.ipynb`, donde cada transformación está justificada.

Privacidad: no se extraen los adjudicatarios (`WinningParty`), que pueden ser personas
físicas. Los órganos de contratación son organismos públicos.

Rutas XML según la especificación de sindicación de PLACSP (v1.3).
"""

from __future__ import annotations

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

from radar.codigos import DIVISIONES_TI

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "cbc": "urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2",
    "cbc-place-ext": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2",
    "cac-place-ext": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2",
    "at": "http://purl.org/atompub/tombstones/1.0",
}


def _texto(nodo: ET.Element | None, ruta: str) -> str | None:
    """Texto del primer nodo que cumple la ruta, o None si no existe o está vacío."""
    if nodo is None:
        return None
    encontrado = nodo.find(ruta, NS)
    if encontrado is None or encontrado.text is None:
        return None
    valor = encontrado.text.strip()
    return valor or None


def _atributo(nodo: ET.Element | None, ruta: str, atributo: str) -> str | None:
    if nodo is None:
        return None
    encontrado = nodo.find(ruta, NS)
    return encontrado.attrib.get(atributo) if encontrado is not None else None


def _cpvs(cfs: ET.Element) -> list[str]:
    """CPV del proyecto y de sus lotes, sin repetir y en orden de aparición."""
    codigos = []
    for ruta in ("cac:ProcurementProject", "cac:ProcurementProjectLot"):
        for bloque in cfs.findall(ruta, NS):
            for nodo in bloque.iter(f"{{{NS['cbc']}}}ItemClassificationCode"):
                if nodo.text and nodo.text.strip():
                    codigos.append(nodo.text.strip())
    return list(dict.fromkeys(codigos))


def _organo_id(party: ET.Element | None) -> str | None:
    """Identificador DIR3 del órgano si existe; si no, el primer identificador."""
    if party is None:
        return None
    ids = party.findall("cac:PartyIdentification/cbc:ID", NS)
    for nodo in ids:
        if nodo.attrib.get("schemeName") == "DIR3" and nodo.text:
            return nodo.text.strip()
    return ids[0].text.strip() if ids and ids[0].text else None


def leer_entrada(entrada: ET.Element) -> tuple[dict, list[dict]]:
    """Convierte una entrada Atom en una fila de versión y sus filas de resultado por lote."""
    cfs = entrada.find("cac-place-ext:ContractFolderStatus", NS)
    proyecto = cfs.find("cac:ProcurementProject", NS) if cfs is not None else None
    proceso = cfs.find("cac:TenderingProcess", NS) if cfs is not None else None
    parte = cfs.find("cac-place-ext:LocatedContractingParty", NS) if cfs is not None else None
    party = parte.find("cac:Party", NS) if parte is not None else None
    enlace = entrada.find("atom:link", NS)
    cpvs = _cpvs(cfs) if cfs is not None else []

    version = {
        "atom_id": _texto(entrada, "atom:id"),
        "updated": _texto(entrada, "atom:updated"),
        "titulo": _texto(entrada, "atom:title"),
        "enlace": enlace.attrib.get("href") if enlace is not None else None,
        "expediente": _texto(cfs, "cbc:ContractFolderID"),
        "estado": _texto(cfs, "cbc-place-ext:ContractFolderStatusCode"),
        "organo_nombre": _texto(party, "cac:PartyName/cbc:Name"),
        "organo_id": _organo_id(party),
        "tipo_organo": _texto(parte, "cbc:ContractingPartyTypeCode"),
        "tipo_contrato": _texto(proyecto, "cbc:TypeCode"),
        "subtipo_contrato": _texto(proyecto, "cbc:SubTypeCode"),
        "importe_sin_iva": _texto(proyecto, "cac:BudgetAmount/cbc:TaxExclusiveAmount"),
        "importe_con_iva": _texto(proyecto, "cac:BudgetAmount/cbc:TotalAmount"),
        "valor_estimado": _texto(proyecto, "cac:BudgetAmount/cbc:EstimatedOverallContractAmount"),
        "moneda": _atributo(proyecto, "cac:BudgetAmount/cbc:TaxExclusiveAmount", "currencyID"),
        "nuts": _texto(proyecto, "cac:RealizedLocation/cbc:CountrySubentityCode"),
        "lugar": _texto(proyecto, "cac:RealizedLocation/cbc:CountrySubentity"),
        "duracion": _texto(proyecto, "cac:PlannedPeriod/cbc:DurationMeasure"),
        "duracion_unidad": _atributo(proyecto, "cac:PlannedPeriod/cbc:DurationMeasure", "unitCode"),
        "cpv_principal": cpvs[0] if cpvs else None,
        "cpvs": "|".join(cpvs) if cpvs else None,
        "procedimiento": _texto(proceso, "cbc:ProcedureCode"),
        "urgencia": _texto(proceso, "cbc:UrgencyCode"),
        "sistema_contratacion": _texto(proceso, "cbc:ContractingSystemCode"),
        "fin_presentacion_fecha": _texto(proceso, "cac:TenderSubmissionDeadlinePeriod/cbc:EndDate"),
        "fin_presentacion_hora": _texto(proceso, "cac:TenderSubmissionDeadlinePeriod/cbc:EndTime"),
        "n_lotes": str(len(cfs.findall("cac:ProcurementProjectLot", NS))) if cfs is not None else None,
    }

    resultados = []
    if cfs is not None:
        for orden, resultado in enumerate(cfs.findall("cac:TenderResult", NS), start=1):
            proyecto_adj = resultado.find("cac:AwardedTenderedProject", NS)
            resultados.append({
                "atom_id": version["atom_id"],
                "updated": version["updated"],
                "orden_resultado": str(orden),
                "lote": _texto(proyecto_adj, "cbc:ProcurementProjectLotID"),
                "resultado": _texto(resultado, "cbc:ResultCode"),
                "ofertas": _texto(resultado, "cbc:ReceivedTenderQuantity"),
                "fecha_adjudicacion": _texto(resultado, "cbc:AwardDate"),
                "importe_adjudicacion_sin_iva": _texto(
                    proyecto_adj, "cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount"
                ),
            })
    return version, resultados


def es_ti(cpvs: str | None) -> bool:
    """True si alguno de los CPV (separados por '|') pertenece a las divisiones TI."""
    return bool(cpvs) and any(c[:2] in DIVISIONES_TI for c in cpvs.split("|"))


def leer_zip(ruta_zip: str | Path, solo_ti: bool = True) -> dict:
    """Extrae versiones, resultados por lote y borrados de un ZIP mensual.

    Con `solo_ti=True` se guardan solo las versiones con algún CPV 72 o 48 (y sus
    resultados). Los borrados (tombstones) se guardan siempre, porque pueden referirse
    a expedientes TI cuya versión ya no lleva CPV.

    Devuelve un diccionario con tres DataFrames de texto (`versiones`, `resultados`,
    `borrados`) y un diccionario `meta` con los recuentos de la lectura.
    """
    ruta_zip = Path(ruta_zip)
    versiones, resultados, borrados = [], [], []
    entradas = entradas_ti = documentos = 0
    with zipfile.ZipFile(ruta_zip) as paquete:
        miembros = sorted(n for n in paquete.namelist() if n.lower().endswith(".atom"))
        for nombre in miembros:
            with paquete.open(nombre) as archivo:
                raiz = ET.parse(archivo).getroot()
            documentos += 1
            for borrado in raiz.findall("at:deleted-entry", NS):
                borrados.append({
                    "atom_id": borrado.attrib.get("ref"),
                    "cuando": borrado.attrib.get("when"),
                    "documento": nombre,
                })
            for entrada in raiz.findall("atom:entry", NS):
                entradas += 1
                version, filas = leer_entrada(entrada)
                if solo_ti and not es_ti(version["cpvs"]):
                    continue
                entradas_ti += 1
                version["documento"] = nombre
                versiones.append(version)
                for fila in filas:
                    fila["documento"] = nombre
                resultados.extend(filas)

    meta = {
        "archivo": ruta_zip.name,
        "documentos_atom": documentos,
        "entradas_atom": entradas,
        "entradas_guardadas": entradas_ti,
        "borrados": len(borrados),
        "solo_ti": solo_ti,
    }
    return {
        "versiones": pd.DataFrame(versiones, dtype="string"),
        "resultados": pd.DataFrame(resultados, dtype="string"),
        "borrados": pd.DataFrame(borrados, dtype="string"),
        "meta": meta,
    }


def leer_varios(rutas: list[str | Path], solo_ti: bool = True) -> dict:
    """Lee varios ZIP mensuales y concatena sus tablas, añadiendo el archivo de origen."""
    partes = {"versiones": [], "resultados": [], "borrados": []}
    metas = []
    for ruta in rutas:
        datos = leer_zip(ruta, solo_ti=solo_ti)
        for clave in partes:
            tabla = datos[clave].copy()
            tabla["archivo"] = Path(ruta).name
            partes[clave].append(tabla)
        metas.append(datos["meta"])
    return {clave: pd.concat(tablas, ignore_index=True) for clave, tablas in partes.items()} | {"meta": metas}
