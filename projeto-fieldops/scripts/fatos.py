#!/usr/bin/env python3
"""Numeros e tabelas derivadas dos artefatos, com conferencias (assert) contra os valores-chave."""
import re
from collections import Counter, defaultdict

import dados as D

CRONO = D.cronograma()
ATIV = [a for a in CRONO if not a["marco"]]
MARCOS = [a for a in CRONO if a["marco"]]
REAL = D.realizado_atividades()
ORC = D.orcamento()
RACI = D.raci()
RISCOS = D.riscos_registro()
QUALI = {q["id"]: q for q in D.riscos_quali()}
RESP = D.riscos_resp()
OPORT = D.oportunidades()
AQ = D.aquisicoes()
COM = D.comunicacoes()
PARTES = D.partes()
NOMES = D.eap_nomes()
PESSOAS = ["FM", "JV", "GR", "PD", "AF"]
NOME_P = {"FM": "Felipe Marques", "JV": "João Victor Souza", "GR": "Gabriel Ribeiro", "PD": "Pedro Dias", "AF": "André Fernandes"}

# ------------------------------------------------------------------ totais e conferencias
HORAS = sum(a["esf"] for a in ATIV)
_cab, _rows = D.md_tabelas("orc", "### Por profissional")
HORAS_P = {r[0].split("—")[0].strip().replace("*", ""): int(r[1]) for r in _rows if r[0].replace("*", "")[:2] in PESSOAS}
HORAS_RESP = {p: sum(a["esf"] for a in ATIV if p == a["resp"]) for p in PESSOAS}  # horas das atividades em que a pessoa e a responsavel (sem apoio)
CUSTO_TOTAL = round(sum(o["pert"] for o in ORC), 2)
RESERVAS = {o["id"]: o["pert"] for o in ORC if o["id"] in ("O51", "O52")}
CUSTO_BASE = round(CUSTO_TOTAL - sum(RESERVAS.values()), 2)
CONTING, GERENCIAL = RESERVAS["O51"], RESERVAS["O52"]
BAC = round(CUSTO_BASE + CONTING, 2)

assert len(CRONO) == 71 and len(ATIV) == 63 and len(MARCOS) == 8
assert HORAS == 967, HORAS
assert HORAS_P == {"FM": 202, "JV": 190, "GR": 192, "PD": 191, "AF": 192}, HORAS_P
assert len(ORC) == 52 and abs(CUSTO_TOTAL - 54872.05) < 0.01, CUSTO_TOTAL
assert abs(CUSTO_BASE - 47714.83) < 0.01 and abs(BAC - 52486.31) < 0.01, (CUSTO_BASE, BAC)
assert abs(CONTING - round(CUSTO_BASE * 0.10, 2)) < 0.01 and abs(GERENCIAL - round(CUSTO_BASE * 0.05, 2)) < 0.01
assert len(RACI) == 36 and len(NOMES) == 36 and len(RISCOS) == 22 and len(OPORT) == 4 and len(AQ) == 14 and len(COM) == 19 and len(PARTES) == 13
assert set(a["wbs"] for a in ATIV) == set(NOMES), set(NOMES) ^ set(a["wbs"] for a in ATIV)

# ------------------------------------------------------------------ por pacote
PACOTES = sorted(NOMES, key=lambda c: tuple(int(x) for x in c.split(".")))
RACI_D = {r["cod"]: r for r in RACI}


def papel(cod, tipo):
    return [p for p, v in RACI_D[cod]["papeis"].items() if v == tipo or (tipo in ("R", "A") and v == "A/R")]


CUSTO_PKG = defaultdict(float)
for o in ORC:
    if o["id"] in ("O51", "O52"):
        continue
    CUSTO_PKG[o["wbs"]] += o["pert"]
assert abs(sum(CUSTO_PKG.values()) - CUSTO_BASE) < 0.01
ATIV_PKG = defaultdict(list)
for a in ATIV:
    ATIV_PKG[a["wbs"]].append(a["id"])
HORAS_PKG = {c: sum(a["esf"] for a in ATIV if a["wbs"] == c) for c in PACOTES}
CUSTO_ENT = {k: round(sum(v for c, v in CUSTO_PKG.items() if c.startswith(k + ".")), 2) for k in "1234567"}
HORAS_ENT = {k: sum(v for c, v in HORAS_PKG.items() if c.startswith(k + ".")) for k in "1234567"}
ESPERADO_ENT = {"1": 5093.50, "2": 3636.50, "3": 11525.42, "4": 6939.00, "5": 8831.25, "6": 7659.16, "7": 4030.00}
for k, v in ESPERADO_ENT.items():
    assert abs(CUSTO_ENT[k] - v) < 0.02, (k, CUSTO_ENT[k], v)


def entregas_do_risco(eap):
    ks = set()
    for tok in re.split(r"[,\s]+", eap):
        if re.match(r"^\d(\.[\dx])?$", tok):
            ks.add(tok[0])
    return ks


RISCOS_ENT = defaultdict(list)
RISCOS_PKG = defaultdict(list)
for r in RISCOS:
    for k in entregas_do_risco(r["eap"]):
        RISCOS_ENT[k].append(r["id"])
    for tok in re.split(r"[,\s]+", r["eap"]):
        if re.match(r"^\d\.\d$", tok):
            RISCOS_PKG[tok].append(r["id"])
for k in "1234567":
    RISCOS_ENT[k].sort()

# marcos que cada pacote entrega (pelo sprint das atividades)
MARCO_DO_SPRINT = {"S1": "M1", "S2": "M2", "S3": "M3", "S4": "M4", "S5": "M5", "S6": "M6", "S7": "M7", "S8": "M8"}


def marcos_pkg(cod):
    ms = []
    for a in ATIV:
        if a["wbs"] == cod:
            ult = a["sprint"].split("–")[-1]
            m = MARCO_DO_SPRINT[ult]
            if m not in ms:
                ms.append(m)
    return sorted(ms)


def real_pkg(cod):
    ats = [a for a in ATIV if a["wbs"] == cod]
    return round(sum(a["esf"] * REAL[a["id"]] for a in ats) / sum(a["esf"] for a in ats))


# ------------------------------------------------------------------ RACI contagem
def contagem_raci():
    out = {}
    cols = PESSOAS + ["PI-01", "PI-02", "PI-03"]
    for c in cols:
        r = a = cc = i = 0
        for x in RACI:
            v = x["papeis"][c]
            if v == "R": r += 1
            elif v == "A": a += 1
            elif v == "A/R": r += 1; a += 1
            elif v == "C": cc += 1
            elif v == "I": i += 1
        out[c] = (r, a, cc, i)
    return out


CONTA = contagem_raci()
assert CONTA["FM"] == (11, 21, 7, 0) and CONTA["AF"] == (7, 0, 20, 9), CONTA

# ------------------------------------------------------------------ riscos
ALTAS = [q for q in QUALI.values() if q["classe"] == "Alta"]
assert len(ALTAS) == 5
CLASSES = Counter(q["classe"] for q in QUALI.values())
assert CLASSES == {"Alta": 5, "Média": 13, "Baixa": 4}, CLASSES
MATERIALIZADOS = [r["id"] for r in RISCOS if r["status"].startswith("Materializado")]
# o documento de riscos (secao 8) lista 9 riscos materializados; o registro marca R11 tambem como "Materializado"
MATERIALIZADOS_SEC8 = ["R01", "R02", "R03", "R04", "R10", "R13", "R15", "R16", "R22"]

# ------------------------------------------------------------------ status (base, secao 9)
SPRINTS = [("S1", 15, 17), ("S2", 17, 17), ("S3", 7, 10), ("S4", 10, 14), ("S5", 4, 8), ("S6", 2, 13), ("S7", 2, 14), ("S8", 0, 10)]
OK_TOT = sum(s[1] for s in SPRINTS)
N_TOT = sum(s[2] for s in SPRINTS)
assert (OK_TOT, N_TOT) == (57, 103)
ABERTAS = N_TOT - OK_TOT  # 46
DU_SPRINT = [10, 10, 9, 10, 9, 10, 9, 9]
RITMO_S1_S5 = sum(s[1] for s in SPRINTS[:5]) / sum(DU_SPRINT[:5])  # issues concluidas por dia util
DU_RESTANTES = 6          # 19, 23, 24, 25, 26 e 27/11 (cronograma, 'Atrasos e Acoes')
RITMO_NECESSARIO = ABERTAS / DU_RESTANTES


def br(x, casas=2):
    return D.brn(x, casas)


def rs(x, casas=2):
    return D.brl(x, casas)


def pct(x, casas=0):
    return f"{x:.{casas}f}".replace(".", ",") + "%"


if __name__ == "__main__":
    print("custo base", CUSTO_BASE, "BAC", BAC, "total", CUSTO_TOTAL)
    print("ritmo S1-S5", round(RITMO_S1_S5, 2), "necessario", round(RITMO_NECESSARIO, 2), "razao", round(RITMO_NECESSARIO / RITMO_S1_S5, 1))
    print("custo ent", CUSTO_ENT); print("horas ent", HORAS_ENT)
    print("riscos por entrega", dict(RISCOS_ENT))
    print("mat", MATERIALIZADOS)
    print({c: real_pkg(c) for c in PACOTES[:6]})
    print(marcos_pkg("3.6"), papel("5.1", "A"), papel("3.1", "R"))
