"""Spike para analizar el ZIP mensual 643 sin extraer sus XML al disco.

Uso desde la raíz del repositorio:
    python src/radar_oportunidades/analizar_643.py <zip_643_aaaamm.zip> <salida>

No guarda adjudicatarios ni identificadores de personas físicas.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import statistics
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "cbc": "urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2",
    "cbc-place-ext": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2",
    "cac-place-ext": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2",
    "at": "http://purl.org/atompub/tombstones/1.0",
}

RESULTADOS = {
    "3": "Desierto",
    "4": "Desistimiento",
    "5": "Renuncia",
    "8": "Adjudicación",
    "9": "Formalización",
}
CODIGOS_RESUELTOS = set(RESULTADOS)
CODIGOS_ADJUDICADOS = {"8", "9"}
# Divisiones CPV de TI que analiza Radar: 72 (servicios TI) y 48 (paquetes de software).
DIVISIONES_TI = ("72", "48")
# ProcedureCode de CODICE para procedimientos negociados (sin y con publicidad).
# En ellos una sola oferta es habitual por la naturaleza del procedimiento, así que
# se excluyen del cálculo de baja concurrencia "comparable". Pendiente de confirmar
# contra la lista de códigos oficial de PLACSP.
PROCEDIMIENTOS_NEGOCIADOS = {"3", "4"}


def texto(nodo: ET.Element | None, ruta: str) -> str:
    if nodo is None:
        return ""
    encontrado = nodo.find(ruta, NS)
    return (encontrado.text or "").strip() if encontrado is not None else ""


def valor_atomo(entrada: ET.Element, ruta: str) -> str:
    encontrado = entrada.find(ruta, NS)
    return (encontrado.text or "").strip() if encontrado is not None else ""


def fecha_utc(valor: str) -> datetime:
    return datetime.fromisoformat(valor.replace("Z", "+00:00")).astimezone(timezone.utc)


def normalizar(valor: str) -> str:
    return re.sub(r"\s+", " ", valor.casefold()).strip()


def leer_entrada(entrada: ET.Element, archivo: str) -> tuple[dict, list[dict]]:
    cfs = entrada.find("cac-place-ext:ContractFolderStatus", NS)
    proyecto = cfs.find("cac:ProcurementProject", NS) if cfs is not None else None
    organo = cfs.find("cac-place-ext:LocatedContractingParty/cac:Party", NS) if cfs is not None else None
    cpvs = list(dict.fromkeys(
        (n.text or "").strip()
        for n in proyecto.findall(".//cbc:ItemClassificationCode", NS)
        if (n.text or "").strip()
    )) if proyecto is not None else []
    enlace = entrada.find("atom:link", NS)
    referencias = []
    if cfs is not None:
        for ref in cfs.findall(".//cac:NoticeDocumentReference", NS):
            ref_id = texto(ref, "cbc:ID")
            if ref_id:
                referencias.append(ref_id)
        for ref in cfs.findall(".//cac:ProjectReference", NS):
            ref_id = texto(ref, "cbc:ID")
            if ref_id:
                referencias.append(ref_id)

    fila = {
        "atom_id": valor_atomo(entrada, "atom:id"),
        "updated": valor_atomo(entrada, "atom:updated"),
        "archivo_atom": archivo,
        "enlace": enlace.attrib.get("href", "") if enlace is not None else "",
        "expediente": texto(cfs, "cbc:ContractFolderID"),
        "titulo": valor_atomo(entrada, "atom:title"),
        "organo": texto(organo, "cac:PartyName/cbc:Name"),
        "estado": texto(cfs, "cbc-place-ext:ContractFolderStatusCode"),
        "cpv_principal": cpvs[0] if cpvs else "",
        "cpvs": ", ".join(cpvs),
        "procedimiento": texto(cfs, "cac:TenderingProcess/cbc:ProcedureCode"),
        "tipo_contrato": texto(proyecto, "cbc:TypeCode"),
        "importe_sin_iva": texto(proyecto, "cac:BudgetAmount/cbc:TaxExclusiveAmount"),
        "referencias": json.dumps(list(dict.fromkeys(referencias)), ensure_ascii=False),
    }
    resultados = []
    if cfs is not None:
        for indice, resultado in enumerate(cfs.findall("cac:TenderResult", NS), start=1):
            codigo = texto(resultado, "cbc:ResultCode")
            resultados.append({
                "atom_id": fila["atom_id"],
                "updated": fila["updated"],
                "expediente": fila["expediente"],
                "organo": fila["organo"],
                "titulo": fila["titulo"],
                "cpv_principal": fila["cpv_principal"],
                "cpvs": fila["cpvs"],
                "procedimiento": fila["procedimiento"],
                "importe_sin_iva": fila["importe_sin_iva"],
                "lote": texto(resultado, "cac:AwardedTenderedProject/cbc:ProcurementProjectLotID"),
                "result_index": indice,
                "result_code": codigo,
                "result_label": RESULTADOS.get(codigo, ""),
                "ofertas": texto(resultado, "cbc:ReceivedTenderQuantity"),
                "fecha_adjudicacion": texto(resultado, "cbc:AwardDate"),
            })
    return fila, resultados


def es_ti(resultado: dict) -> bool:
    """True si el expediente tiene algún CPV de las divisiones TI (72 o 48)."""
    return any(cpv[:2] in DIVISIONES_TI for cpv in resultado["cpvs"].split(", ") if cpv)


def resumen_concurrencia(resultados: list[dict]) -> dict:
    """Desiertos, una oferta y baja concurrencia sobre lotes resueltos (3, 8 y 9).

    Baja concurrencia = lote desierto (3) o adjudicado/formalizado (8, 9) con 0 o 1
    ofertas. Los lotes con desistimiento (4) o renuncia (5) no entran en el cálculo.
    """
    resueltos = [r for r in resultados if r["result_code"] in {"3", "8", "9"}]
    desiertos = [r for r in resueltos if r["result_code"] == "3"]
    adjudicados_con_ofertas = []
    for r in resueltos:
        if r["result_code"] in CODIGOS_ADJUDICADOS:
            try:
                adjudicados_con_ofertas.append(float(r["ofertas"]))
            except ValueError:
                pass
    pocas = [n for n in adjudicados_con_ofertas if n <= 1]
    pct = lambda a, b: round(100 * a / b, 2) if b else None
    return {
        "lotes_resueltos_3_8_9": len(resueltos),
        "desiertos": len(desiertos),
        "pct_desiertos": pct(len(desiertos), len(resueltos)),
        "adjudicados_con_ofertas_numericas": len(adjudicados_con_ofertas),
        "pct_adjudicados_con_0_o_1_ofertas": pct(len(pocas), len(adjudicados_con_ofertas)),
        "pct_baja_concurrencia": pct(len(desiertos) + len(pocas), len(desiertos) + len(adjudicados_con_ofertas)),
        "mediana_ofertas": statistics.median(adjudicados_con_ofertas) if adjudicados_con_ofertas else None,
    }


def metricas_concurrencia_ti(resultados_ultimos: list[dict]) -> dict:
    """Concurrencia en lotes TI, en total, sin negociados y por procedimiento."""
    ti = [r for r in resultados_ultimos if es_ti(r)]
    por_procedimiento: dict[str, list[dict]] = defaultdict(list)
    for r in ti:
        por_procedimiento[r["procedimiento"] or "sin_codigo"].append(r)
    return {
        "nota": "Lotes de la última versión del periodo con algún CPV 72 o 48. Códigos de procedimiento pendientes de confirmar con la lista oficial.",
        "total": resumen_concurrencia(ti),
        "sin_negociados": resumen_concurrencia([r for r in ti if r["procedimiento"] not in PROCEDIMIENTOS_NEGOCIADOS]),
        "por_procedimiento": {codigo: resumen_concurrencia(filas) for codigo, filas in sorted(por_procedimiento.items())},
    }


def escribir_csv(ruta: Path, filas: list[dict], columnas: list[str]) -> None:
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas, extrasaction="ignore")
        escritor.writeheader()
        escritor.writerows(filas)


def sha256(ruta: Path) -> str:
    digest = hashlib.sha256()
    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            digest.update(bloque)
    return digest.hexdigest()


def analizar(ruta_zip: Path, salida: Path) -> dict:
    salida.mkdir(parents=True, exist_ok=True)
    periodo_archivo = ruta_zip.stem[-6:]
    periodo = f"{periodo_archivo[:4]}-{periodo_archivo[4:]}"
    versiones_por_clave: dict[tuple[str, str], dict] = {}
    resultados_por_clave: dict[tuple[str, str], list[dict]] = {}
    paginas = 0
    entradas_totales = 0
    tombstones = 0
    bytes_xml = 0

    with zipfile.ZipFile(ruta_zip) as paquete:
        miembros = [n for n in paquete.namelist() if n.lower().endswith(".atom")]
        for nombre in miembros:
            with paquete.open(nombre) as archivo:
                raiz = ET.parse(archivo).getroot()
            paginas += 1
            tombstones += len(raiz.findall("at:deleted-entry", NS))
            entradas = raiz.findall("atom:entry", NS)
            entradas_totales += len(entradas)
            for entrada in entradas:
                fila, resultados = leer_entrada(entrada, nombre)
                if not fila["atom_id"] or not fila["updated"]:
                    continue
                clave = (fila["atom_id"], fila["updated"])
                versiones_por_clave[clave] = fila
                resultados_por_clave[clave] = resultados
        bytes_xml = sum(info.file_size for info in paquete.infolist() if info.filename.lower().endswith(".atom"))

    versiones = list(versiones_por_clave.values())
    por_id: dict[str, list[dict]] = defaultdict(list)
    for fila in versiones:
        por_id[fila["atom_id"]].append(fila)
    ultimas = [max(grupo, key=lambda fila: fecha_utc(fila["updated"])) for grupo in por_id.values()]
    iniciales = [min(grupo, key=lambda fila: fecha_utc(fila["updated"])) for grupo in por_id.values()]
    versiones_periodo = [fila for fila in versiones if fila["updated"].startswith(periodo)]
    por_id_periodo: dict[str, list[dict]] = defaultdict(list)
    for fila in versiones_periodo:
        por_id_periodo[fila["atom_id"]].append(fila)
    ultimas_periodo = [max(grupo, key=lambda fila: fecha_utc(fila["updated"])) for grupo in por_id_periodo.values()]

    filas_resultados = []
    resultados_ultimos = []
    for fila in versiones_periodo:
        clave = (fila["atom_id"], fila["updated"])
        filas_resultados.extend(resultados_por_clave[clave])
    for fila in ultimas_periodo:
        resultados_ultimos.extend(resultados_por_clave[(fila["atom_id"], fila["updated"])])

    resueltos = [r for r in resultados_ultimos if r["result_code"] in CODIGOS_RESUELTOS]
    desiertos = [r for r in resultados_ultimos if r["result_code"] == "3"]
    ofertas_presentes = [r for r in resultados_ultimos if r["ofertas"].strip()]
    ofertas_numericas = []
    for resultado in ofertas_presentes:
        try:
            ofertas_numericas.append((resultado, float(resultado["ofertas"])))
        except ValueError:
            pass
    una_oferta = [r for r, valor in ofertas_numericas if valor == 1]

    cpv_principal = Counter()
    cpv_cualquiera = Counter()
    for fila in ultimas_periodo:
        if fila["cpv_principal"]:
            cpv_principal[fila["cpv_principal"][:2]] += 1
        divisiones = {cpv[:2] for cpv in fila["cpvs"].split(", ") if cpv}
        for division in divisiones:
            cpv_cualquiera[division] += 1

    iniciales_sin_adjudicacion = []
    for ultima in ultimas_periodo:
        resultados_finales = resultados_por_clave[(ultima["atom_id"], ultima["updated"])]
        if not any(r["result_code"] in CODIGOS_ADJUDICADOS for r in resultados_finales):
            iniciales_sin_adjudicacion.append(min(
                por_id[ultima["atom_id"]], key=lambda fila: fecha_utc(fila["updated"])
            ))

    # Candidatos conservadores: mismo número de expediente y órgano en IDs distintos,
    # con el registro posterior actualizado después de una resolución desierta.
    resultados_ultima_version = []
    for fila in ultimas:
        resultados_ultima_version.extend(resultados_por_clave[(fila["atom_id"], fila["updated"])])
    desierto_ids = {r["atom_id"] for r in resultados_ultima_version if r["result_code"] == "3"}
    nuevas_periodo = [min(grupo, key=lambda fila: fecha_utc(fila["updated"])) for grupo in por_id_periodo.values()]
    desiertos_previos = [f for f in ultimas if f["atom_id"] in desierto_ids]
    por_titulo_organo: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for fila in nuevas_periodo:
        if fila["titulo"] and fila["organo"]:
            por_titulo_organo[(normalizar(fila["organo"]), normalizar(fila["titulo"]), fila["cpv_principal"])].append(fila)
    candidatos = []
    for anterior in desiertos_previos:
        clave_match = (normalizar(anterior["organo"]), normalizar(anterior["titulo"]), anterior["cpv_principal"])
        for posterior in por_titulo_organo.get(clave_match, []):
            if posterior["atom_id"] != anterior["atom_id"] and posterior["expediente"] != anterior["expediente"] and fecha_utc(posterior["updated"]) > fecha_utc(anterior["updated"]):
                candidatos.append({
                    "id_desierto": anterior["atom_id"], "id_candidato": posterior["atom_id"],
                    "expediente_desierto": anterior["expediente"], "expediente_candidato": posterior["expediente"],
                    "organo": anterior["organo"], "titulo_desierto": anterior["titulo"], "titulo_candidato": posterior["titulo"],
                    "cpv_principal": anterior["cpv_principal"], "updated_desierto": anterior["updated"],
                    "updated_candidato": posterior["updated"],
                    "referencias_explicitas": posterior["referencias"],
                    "regla": "mismo órgano, título normalizado y CPV principal; IDs y expediente distintos; validar manualmente",
                })

    concurrencia_ti = metricas_concurrencia_ti(resultados_ultimos)

    cols_version = ["atom_id", "updated", "archivo_atom", "enlace", "expediente", "titulo", "organo", "estado", "cpv_principal", "cpvs", "procedimiento", "tipo_contrato", "importe_sin_iva", "referencias"]
    cols_resultado = ["atom_id", "updated", "expediente", "organo", "titulo", "cpv_principal", "cpvs", "procedimiento", "importe_sin_iva", "lote", "result_index", "result_code", "result_label", "ofertas", "fecha_adjudicacion"]
    escribir_csv(salida / f"versiones_643_{periodo_archivo}.csv", versiones_periodo, cols_version)
    escribir_csv(salida / f"resultados_643_{periodo_archivo}.csv", filas_resultados, cols_resultado)
    escribir_csv(salida / f"versiones_iniciales_sin_adjudicacion_643_{periodo_archivo}.csv", iniciales_sin_adjudicacion, cols_version)
    escribir_csv(salida / f"candidatos_relicitacion_643_{periodo_archivo}.csv", candidatos,
                 ["id_desierto", "id_candidato", "expediente_desierto", "expediente_candidato", "organo", "titulo_desierto", "titulo_candidato", "cpv_principal", "updated_desierto", "updated_candidato", "referencias_explicitas", "regla"])

    fechas = [fecha_utc(f["updated"]) for f in versiones]
    metadatos = {
        "fuente": f"PLACSP sindicación 643, ZIP mensual {periodo_archivo}",
        "periodo_analizado_por_updated": periodo,
        "archivo": ruta_zip.name,
        "tamano_bytes": ruta_zip.stat().st_size,
        "sha256": sha256(ruta_zip),
        "paginas_atom": paginas,
        "entradas_atom": entradas_totales,
        "entradas_version_unicas_atom_id_updated": len(versiones),
        "versiones_updated_en_periodo": len(versiones_periodo),
        "expedientes_con_update_en_periodo": len(por_id_periodo),
        "expedientes_atom_id_distintos": len(por_id),
        "deleted_entry": tombstones,
        "bytes_atom_descomprimidos": bytes_xml,
        "updated_min": min(fechas).isoformat() if fechas else None,
        "updated_max": max(fechas).isoformat() if fechas else None,
        "result_code_en_ultima_version_de_expedientes_actualizados_en_periodo": dict(Counter(r["result_code"] for r in resultados_ultimos)),
        "resultados_lotes_ultima_version": len(resultados_ultimos),
        "resultados_resueltos_codigos_3_4_5_8_9": len(resueltos),
        "desiertos_codigo_3": len(desiertos),
        "porcentaje_desiertos_sobre_resultados_resueltos": round(100 * len(desiertos) / len(resueltos), 2) if resueltos else None,
        "resultados_con_ofertas_no_vacias": len(ofertas_presentes),
        "cobertura_ofertas_sobre_resultados_lotes": round(100 * len(ofertas_presentes) / len(resultados_ultimos), 2) if resultados_ultimos else None,
        "resultados_con_ofertas_numericas": len(ofertas_numericas),
        "resultados_con_una_oferta": len(una_oferta),
        "porcentaje_una_oferta_sobre_ofertas_numericas": round(100 * len(una_oferta) / len(ofertas_numericas), 2) if ofertas_numericas else None,
        "expedientes_ultima_version_sin_tender_result_en_periodo": sum(not resultados_por_clave[(f["atom_id"], f["updated"])] for f in ultimas_periodo),
        "cpv_division_72_principal": cpv_principal["72"],
        "cpv_division_48_principal": cpv_principal["48"],
        "cpv_division_72_cualquier_cpv": cpv_cualquiera["72"],
        "cpv_division_48_cualquier_cpv": cpv_cualquiera["48"],
        "versiones_iniciales_dentro_del_zip_sin_adjudicacion_final": len(iniciales_sin_adjudicacion),
        "candidatos_relicitacion_heuristica_titulo_organo_cpv": len(candidatos),
        "desiertos_historicos_ultima_version_feed": len(desiertos_previos),
        "concurrencia_ti_cpv_72_48": concurrencia_ti,
        "limitacion_temporal": "La versión inicial se refiere a la primera versión presente en este ZIP mensual; la historia anterior al mes puede no estar incluida.",
    }
    (salida / f"resumen_643_{periodo_archivo}.json").write_text(json.dumps(metadatos, ensure_ascii=False, indent=2), encoding="utf-8")
    return metadatos


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip", type=Path)
    parser.add_argument("salida", type=Path)
    args = parser.parse_args()
    resultado = analizar(args.zip, args.salida)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
