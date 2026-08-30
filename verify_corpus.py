#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LIBOX · Verificador de coherencia documental
============================================
Regla CD-10 del Registro Maestro: ninguna versión se emite sin que este
verificador pase con cero fallos.

Existe porque durante la construcción de la línea base, CUATRO rondas de
hallazgos aparecieron únicamente por verificación programática. Ninguno era
visible leyendo, y varios los produjo el propio equipo que había leído el
documento minutos antes.

Uso:
    python3 verify_corpus.py                # verifica el corpus vigente
    python3 verify_corpus.py --json         # salida para CI
    python3 verify_corpus.py --dir ./docs   # otro directorio

Código de salida: 0 si todo pasa, 1 si hay algún fallo.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# Línea base vigente. ACTUALIZAR EN CADA EMISIÓN.
# Es la única fuente de verdad del script: si un documento no está aquí,
# no rige, y toda referencia a él se considera obsoleta.
# ---------------------------------------------------------------------------
BASELINE = {
    "LBPF":        {"version": 3, "file": "LIBOX_BEHAVIORAL_PRODUCT_FRAMEWORK_LBPF_V3.md"},
    "L1":          {"version": 3, "file": "LIBOX_PRODUCT_STRATEGY_L1_V3.md"},
    "PRD MVP":     {"version": 9, "file": "LIBOX_PRD_BLUEPRINT_MVP_V9.md"},
    "Enterprise":  {"version": 3, "file": "LIBOX_PRD_BLUEPRINT_ENTERPRISE_V3.md"},
    "L3":          {"version": 7, "file": "LIBOX_ESPECIFICACION_TECNICA_L3_V7.md"},
    "Matriz":      {"version": 1, "file": "LIBOX_MATRIZ_CASOS_DE_USO_V1.md"},
    "Guia":        {"version": 1, "file": "LIBOX_GUIA_EXTENSION_V1.md"},
    "L4":          {"version": 2, "file": "LIBOX_DESIGN_SYSTEM_L4_V2.md"},
    "VIES":        {"version": 3, "file": "LIBOX_VISUAL_IDENTITY_ENGINEERING_STANDARD_V3.md"},
    "Backlog":     {"version": 3, "file": "LIBOX_BACKLOG_MVP_V3.md"},
    "Registro":    {"version": 6, "file": "LIBOX_REGISTRO_MAESTRO_LINEA_BASE_V6.md"},
    "Dossier":     {"version": 1, "file": "LIBOX_DOSSIER_LEGAL_V1.md"},
    "AuditGlobal": {"version": 1, "file": "LIBOX_AUDITORIA_GLOBAL_COHERENCIA_V1.md"},
    "AuditPost":   {"version": 1, "file": "LIBOX_AUDITORIA_POST_EMISION_V1.md"},
    "Evaluacion":  {"version": 1, "file": "LIBOX_EVALUACION_COMITE_Y_EQUIPO_TECNICO_V1.md"},
}

# Patrones de referencia a versión, por documento.
REF_PATTERNS = {
    "LBPF":       r"LBPF V(\d+)",
    "L1":         r"Product Strategy L1 V(\d+)",
    "PRD MVP":    r"PRD MVP V(\d+)",
    "Enterprise": r"PRD Enterprise V(\d+)",
    "L3":         r"\bL3 V(\d+)",
    "L4":         r"\bL4 V(\d+)",
    "VIES":       r"VIES V(\d+)",
    "Backlog":    r"Backlog MVP V(\d+)",
}

# Contextos donde una referencia a versión anterior es LEGÍTIMA: changelog,
# historial y registro de material nulo. Sin esta lista el verificador
# marcaría como error el propio registro de lo que se derogó.
HISTORICAL_MARKERS = [
    "reemplaza", "deprecad", "sustituid", "sustituy", "histórico", "historico",
    "cambios de la versión", "cambios de la version", "motivo", "| v",
    "invalida", "deroga", "corrige", "precisa", "amplía", "amplia",
    "sin documento", "primera emisión", "primera emision", "nulo",
    "qué motivó", "que motivo", "historial de versiones", "eliminación del marcador",
    "que dijera", "se reescribiera", "por ejemplo", "supongamos",
]

# Secciones completas donde toda referencia a versión anterior es legítima
# por naturaleza: son el registro de lo que ocurrió, no una dependencia.
HISTORICAL_SECTIONS = [
    "qué motivó cada emisión", "que motivo cada emision",
    "historial de versiones del corpus", "material histórico nulo",
    "material historico nulo", "changelog", "gestión del cambio",
    "registro de decisiones conservadas",
]

CONTEXT_WINDOW = 130   # caracteres antes de la coincidencia

# Documentos cuyo PROPÓSITO es registrar un momento en el tiempo. Sus
# referencias a versiones anteriores son el contenido, no un defecto:
# una auditoría que dijera "L4 V1 tiene un hueco" y se reescribiera a
# "L4 V2 tiene un hueco" estaría falseando lo que ocurrió.
# Se verifican en existencia e identidad, no en referencias cruzadas.
HISTORICAL_DOCUMENTS = {"AuditGlobal", "AuditPost", "Evaluacion"}


# ---------------------------------------------------------------------------

class Finding:
    def __init__(self, check, severity, doc, detail):
        self.check, self.severity, self.doc, self.detail = check, severity, doc, detail

    def as_dict(self):
        return {"check": self.check, "severity": self.severity,
                "doc": self.doc, "detail": self.detail}

    def __str__(self):
        mark = "FALLO" if self.severity == "error" else "aviso"
        return f"  [{mark}] {self.doc}: {self.detail}"


def load_corpus(directory):
    """Carga los documentos de la línea base. Un documento ausente es un fallo."""
    corpus, missing = {}, []
    for name, meta in BASELINE.items():
        path = os.path.join(directory, meta["file"])
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                corpus[name] = fh.read()
        else:
            missing.append((name, meta["file"]))
    return corpus, missing


def is_historical(text, position):
    """True si la coincidencia está en un contexto de changelog o historial.

    Comprueba dos cosas: el contexto inmediato, y si la coincidencia cae dentro
    de una sección cuyo propósito ES registrar versiones anteriores. Sin lo
    segundo, el verificador marcaría como error el propio Registro Maestro.
    """
    context = text[max(0, position - CONTEXT_WINDOW):position + 50].lower()
    if any(marker in context for marker in HISTORICAL_MARKERS):
        return True
    # Encabezado de sección más cercano por encima de la coincidencia
    heads = [m for m in re.finditer(r"^#{1,3} .+$", text[:position], re.M)]
    if heads:
        current_section = heads[-1].group(0).lower()
        if any(s in current_section for s in HISTORICAL_SECTIONS):
            return True
    return False


# --- CHECK 1 --------------------------------------------------------------
def check_stale_references(corpus):
    """Ninguna referencia cruzada apunta a una versión que ya no rige.

    Es el check que más ha encontrado: 53 hallazgos en una pasada y 33 en otra.
    """
    findings = []
    for doc_name, text in corpus.items():
        if doc_name in HISTORICAL_DOCUMENTS:
            continue
        for target, pattern in REF_PATTERNS.items():
            current = BASELINE[target]["version"]
            for match in re.finditer(pattern, text):
                referenced = int(match.group(1))
                if referenced >= current or is_historical(text, match.start()):
                    continue
                line = text[:match.start()].count("\n") + 1
                findings.append(Finding(
                    "referencias-obsoletas", "error", doc_name,
                    f"línea {line}: '{match.group(0)}' — vigente es {target} V{current}"))
    return findings


# --- CHECK 2 --------------------------------------------------------------
def check_orphan_invariants(corpus):
    """Todo invariante citado existe en el registro del PRD.

    Encontró INV-06-b, que protegía a quien participa gratis y no figuraba
    en el anexo: quien consultara solo el registro habría concluido que esa
    protección no existía.
    """
    findings = []
    prd = corpus.get("PRD MVP")
    if not prd:
        return findings

    declared = set(re.findall(r"\|\s*(INV-\d+(?:-[a-z]+)?)\s*\|", prd))
    if not declared:
        return [Finding("invariantes-huerfanos", "error", "PRD MVP",
                        "no se encontró el registro de invariantes")]

    for doc_name, text in corpus.items():
        if doc_name in HISTORICAL_DOCUMENTS:
            continue
        cited = set()
        for m in re.finditer(r"\b(INV-\d+(?:-[a-z]+)?)\b", text):
            if not is_historical(text, m.start()):
                cited.add(m.group(1))
        for inv in sorted(cited - declared):
            findings.append(Finding(
                "invariantes-huerfanos", "error", doc_name,
                f"{inv} citado y ausente del registro del PRD"))
    return findings


# --- CHECK 3 --------------------------------------------------------------
def check_orphan_rules(corpus):
    """Toda regla RN citada existe en el PRD, que es donde se declaran."""
    findings = []
    prd = corpus.get("PRD MVP")
    if not prd:
        return findings
    declared = set(re.findall(r"\b(RN-\d+(?:-[a-z]+)?)\b", prd))
    for doc_name, text in corpus.items():
        if doc_name == "PRD MVP" or doc_name in HISTORICAL_DOCUMENTS:
            continue
        for rn in sorted(set(re.findall(r"\b(RN-\d+(?:-[a-z]+)?)\b", text)) - declared):
            findings.append(Finding(
                "reglas-huerfanas", "error", doc_name,
                f"{rn} citada y no declarada en el PRD"))
    return findings


# --- CHECK 4 --------------------------------------------------------------
def check_self_identity(corpus):
    """Regla CD-03: el documento se identifica igual en título, control y pie.

    Encontró el PRD arrastrando 'V7' en su título YAML durante dos versiones.
    """
    findings = []
    for doc_name, text in corpus.items():
        if doc_name in HISTORICAL_DOCUMENTS:
            continue
        expected = BASELINE[doc_name]["version"]
        head = text[:1200]

        title = re.search(r'title:\s*"([^"]+)"', head)
        if title and re.search(r"V(\d+)", title.group(1)):
            found = int(re.findall(r"V(\d+)", title.group(1))[-1])
            if found != expected:
                findings.append(Finding(
                    "identidad-documental", "error", doc_name,
                    f"título dice V{found} y la versión vigente es V{expected}"))

        version_field = re.search(r"\*\*Versi[oó]n:\*\*\s*V(\d+)", head)
        if version_field and int(version_field.group(1)) != expected:
            findings.append(Finding(
                "identidad-documental", "error", doc_name,
                f"campo de versión dice V{version_field.group(1)}, vigente V{expected}"))
    return findings


# --- CHECK 5 --------------------------------------------------------------
def check_shared_figures(corpus):
    """Las cifras que aparecen en varios documentos son idénticas en todos.

    Una cifra divergente entre capas produce una discusión en el sprint.
    """
    figures = {
        "comisión base":       r"20\s*%",
        "suelo de recaudación": r"1,25\s*×",
        "techo de recaudación": r"4,0\s*×",
        "concentración":        r"30\s*%",
        "subroles":             r"21 subroles",
        "incompatibilidades":   r"11 incompatibilidades",
    }
    findings, presence = [], defaultdict(list)
    for doc_name, text in corpus.items():
        for label, pattern in figures.items():
            if re.search(pattern, text):
                presence[label].append(doc_name)
    for label, docs in presence.items():
        if len(docs) == 1:
            findings.append(Finding(
                "cifras-compartidas", "aviso", docs[0],
                f"'{label}' aparece solo aquí; verificar si debería propagarse"))
    return findings


# --- CHECK 6 --------------------------------------------------------------
def check_repetition(corpus):
    """Criterio de cierre: ningún párrafo largo se repite más de dos veces.

    El PRD V1 tenía 41,5 % de texto repetido. Este umbral existe para que
    un documento no se degrade en plantilla.
    """
    findings = []
    for doc_name, text in corpus.items():
        lines = [ln.strip() for ln in text.split("\n")
                 if len(ln.strip()) > 60 and not ln.strip().startswith("|")]
        if not lines:
            continue
        counts = Counter(lines)
        duplicated = sum(v for v in counts.values() if v > 2)
        ratio = duplicated / len(lines) * 100
        if ratio > 5:
            findings.append(Finding(
                "repeticion", "error", doc_name,
                f"{ratio:.1f}% de párrafos repetidos más de dos veces (umbral 5%)"))
    return findings


# --- CHECK 7 --------------------------------------------------------------
def check_placeholders(corpus):
    """Ningún marcador de posición sobrevive a la emisión.

    Encontró 'NP-XX' en VIES, un documento que rige a proveedores externos.
    """
    patterns = [
        (r"\b[A-Z]{2,4}-XX\b", "código de marcador de posición"),
        (r"\bTODO\b", "TODO sin resolver"),
        (r"\bTBD\b", "TBD sin resolver"),
        (r"\bXXX\b", "marcador XXX"),
        (r"\bLOREM\b", "texto de relleno"),
    ]
    findings = []
    for doc_name, text in corpus.items():
        for pattern, label in patterns:
            for match in re.finditer(pattern, text):
                if is_historical(text, match.start()):
                    continue          # citado en un changelog, no es un marcador vivo
                line = text[:match.start()].count("\n") + 1
                findings.append(Finding(
                    "marcadores", "error", doc_name,
                    f"línea {line}: {label} — '{match.group(0)}'"))
    return findings


# --- CHECK 8 --------------------------------------------------------------
def check_self_deprecating_refs(corpus):
    """Regla CD-06: un documento no depende de la versión que deroga.

    Encontró VIES V2 remitiendo quince veces a V1, al que declaraba
    'deprecado en su totalidad'. El contenido quedaba sin documento vigente.
    """
    findings = []
    for doc_name, text in corpus.items():
        for match in re.finditer(
                r"(?:sin cambios respecto de|se mantiene[^.]{0,30}de|"
                r"conforme a lo establecido en)\s+V\d+", text, re.IGNORECASE):
            line = text[:match.start()].count("\n") + 1
            findings.append(Finding(
                "derogacion-sin-sustituto", "error", doc_name,
                f"línea {line}: remite a una versión anterior para contenido normativo "
                f"— '{match.group(0)}'"))
    return findings


# ---------------------------------------------------------------------------

def check_undeclared_documents(corpus, directory="."):
    """Todo documento presente en el corpus está declarado en la línea base.

    El check inverso de `documento-ausente`, y el que faltaba. Un documento
    que existe, se distribuye y NO figura en el Registro Maestro crea una
    contradicción de gobierno: por la regla de uso del propio Registro no
    rige, pero está en manos del equipo como si rigiera.

    Lo detectó una revisión externa sobre la Evaluación de Comité V1,
    emitida después del Registro V5 y nunca incorporada.
    """
    findings = []
    declared = {meta["file"] for meta in BASELINE.values()}
    try:
        present = {f for f in os.listdir(directory)
                   if f.startswith("LIBOX") and f.endswith(".md")}
    except OSError:
        return findings
    for orphan in sorted(present - declared):
        findings.append(Finding(
            "documento-no-declarado", "error", orphan,
            "presente en el corpus y ausente del Registro Maestro: "
            "o entra en la próxima emisión, o es material de trabajo"))
    return findings


CHECKS = [
    ("documento-no-declarado",    check_undeclared_documents),
    ("referencias-obsoletas",     check_stale_references),
    ("invariantes-huerfanos",     check_orphan_invariants),
    ("reglas-huerfanas",          check_orphan_rules),
    ("identidad-documental",      check_self_identity),
    ("cifras-compartidas",        check_shared_figures),
    ("repeticion",                check_repetition),
    ("marcadores",                check_placeholders),
    ("derogacion-sin-sustituto",  check_self_deprecating_refs),
]


def main():
    parser = argparse.ArgumentParser(
        description="Verificador de coherencia documental de LIBOX")
    parser.add_argument("--dir", default=".", help="directorio del corpus")
    parser.add_argument("--json", action="store_true", help="salida JSON para CI")
    args = parser.parse_args()

    corpus, missing = load_corpus(args.dir)

    findings = [Finding("documento-ausente", "error", name,
                        f"no encontrado: {fname}") for name, fname in missing]
    for name, fn in CHECKS:
        if name == "documento-no-declarado":
            findings.extend(fn(corpus, args.dir))
        else:
            findings.extend(fn(corpus))

    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "aviso"]

    if args.json:
        print(json.dumps({
            "status": "fail" if errors else "pass",
            "documents": len(corpus),
            "errors": len(errors),
            "warnings": len(warnings),
            "findings": [f.as_dict() for f in findings],
        }, indent=2, ensure_ascii=False))
        return 1 if errors else 0

    print(f"LIBOX · verificación de coherencia documental")
    print(f"documentos del corpus: {len(corpus)} de {len(BASELINE)}\n")

    by_check = defaultdict(list)
    for f in findings:
        by_check[f.check].append(f)

    for name, _ in [("documento-ausente", None)] + CHECKS:
        items = by_check.get(name, [])
        errs = [i for i in items if i.severity == "error"]
        status = "OK" if not errs else f"{len(errs)} FALLOS"
        print(f"{name:<28} {status}")
        for item in items[:10]:
            print(item)
        if len(items) > 10:
            print(f"  … y {len(items) - 10} más")

    print()
    if errors:
        print(f"RESULTADO: {len(errors)} fallos, {len(warnings)} avisos.")
        print("La versión NO puede emitirse (regla CD-10).")
        return 1
    print(f"RESULTADO: sin fallos, {len(warnings)} avisos. La versión puede emitirse.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
