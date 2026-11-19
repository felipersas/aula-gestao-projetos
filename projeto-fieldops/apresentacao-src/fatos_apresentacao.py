#!/usr/bin/env python3
"""
Le os artefatos ja entregues (md) e extrai os numeros que a apresentacao usa.
Qualquer divergencia derruba a construcao (assert): a apresentacao so diz o que os artefatos dizem.
"""
import re
from datetime import date, timedelta
from pathlib import Path

E = Path("/Users/felipersas/Documents/Facul/gestao-proj/entrega")
F = Path("/Users/felipersas/Documents/Facul/gestao-proj/fieldops-src/docs/notion")


def rd(p):
    return Path(p).read_text(encoding="utf-8")


def tabela(txt, inicio_regex):
    """linhas (listas de celulas) da primeira tabela markdown depois do trecho que casa inicio_regex"""
    m = re.search(inicio_regex, txt)
    assert m, inicio_regex
    linhas = txt[m.start():].splitlines()
    out, ini = [], False
    for ln in linhas:
        if ln.startswith("|"):
            ini = True
            cel = [c.strip() for c in ln.strip().strip("|").split("|")]
            out.append(cel)
        elif ini:
            break
    return out


def num(s):
    s = re.sub(r"[^\d,.\-]", "", s)
    return float(s.replace(".", "").replace(",", "."))


def carrega():
    F_ = {}
    # ---------------- cronograma
    cr = rd(E / "aula-04-tempo/cronograma-fieldops.md")
    t = tabela(cr, r"## 📋 Lista de Atividades")
    ativ, marcos = [], []
    for r in t[2:]:
        idr = r[0].replace("*", "")
        if idr.startswith("M"):
            marcos.append(idr)
            continue
        ini = tuple(int(x) for x in r[3].split("/"))
        fim = tuple(int(x) for x in r[4].split("/"))
        ativ.append(dict(id=idr, wbs=r[1], nome=r[2].replace("🔺", "").strip(), ini=date(2026, ini[1], ini[0]),
                         fim=date(2026, fim[1], fim[0]), resp=r[6], esforco=float(r[8]),
                         critica="🔺" in r[2]))
    assert len(ativ) == 63 and len(marcos) == 8, (len(ativ), len(marcos))
    F_["itens_cron"] = len(ativ) + len(marcos)
    assert F_["itens_cron"] == 71
    F_["horas"] = sum(a["esforco"] for a in ativ)
    assert round(F_["horas"]) == 967, F_["horas"]
    # % realizado por atividade (tabela de comparacao)
    t2 = tabela(cr, r"### Comparação por atividade")
    real = {}
    for r in t2[2:]:
        idr = r[0].replace("*", "")
        if idr.startswith("A"):
            real[idr] = float(r[4].strip("%")) / 100
    assert len(real) == 63, len(real)
    for a in ativ:
        a["real"] = real[a["id"]]
    F_["ativ"] = ativ
    crit = [a for a in ativ if a["critica"]]
    assert len(crit) == 20, len(crit)
    F_["n_crit"] = 20
    assert "32,5 dias úteis" in cr and "06/01/2027" in cr
    # situacao dos marcos
    t3 = tabela(cr, r"\| Marco \| Data prevista")
    F_["marcos"] = []
    for r in t3[2:]:
        F_["marcos"].append(dict(id=re.search(r"M\d", r[0]).group(0), nome=r[0].split("—")[1].replace("*", "").strip(),
                                 data=r[1], sit=r[5]))
    assert len(F_["marcos"]) == 8
    # sprints
    t4 = tabela(cr, r"### Planejado × Realizado por sprint")
    F_["sprints"] = []
    for r in t4[2:10]:
        a, b = [int(x) for x in re.findall(r"\d+", r[3])][:2]
        F_["sprints"].append((r[0], a, b))
    tot = sum(x[1] for x in F_["sprints"]), sum(x[2] for x in F_["sprints"])
    assert tot == (57, 103), tot
    F_["issues"] = tot
    assert "0,53" in rd(E / "aula-05-custos-qualidade/orcamento-fieldops.md")
    # WBS: 36 pacotes
    pac = {a["wbs"] for a in ativ}
    assert len(pac) == 36, len(pac)
    F_["pacotes"] = 36

    # ---------------- orcamento
    og = rd(E / "aula-05-custos-qualidade/orcamento-fieldops.md")
    for s in ["R$ 47.714,83", "R$ 52.486,31", "R$ 54.872,05", "R$ 4.771,48", "R$ 2.385,74", "R$ 669,08", "R$ 374,00",
              "R$ 2.478,50", "R$ 65.181,50", "**52**"]:
        assert s in og, s
    F_["orc"] = dict(base=47714.83, cont=4771.48, bac=52486.31, ger=2385.74, total=54872.05)
    assert round(F_["orc"]["base"] + F_["orc"]["cont"], 2) == F_["orc"]["bac"]
    assert round(F_["orc"]["bac"] + F_["orc"]["ger"], 2) == F_["orc"]["total"]
    t5 = tabela(og, r"\| Sprint \| Marco \| Horas \(cM\)")
    F_["curvaS"] = [num(r[8]) for r in t5[2:10]]
    assert F_["curvaS"][-1] == 52486.31
    assert len(F_["curvaS"]) == 8
    ev = re.search(r"\| \*\*SPI\*\* \| \*\*([\d,]+)\*\*", og)
    cp = re.search(r"\| \*\*CPI\*\* \| \*\*([\d,]+)\*\*", og)
    assert ev.group(1) == "0,53" and cp.group(1) == "0,58"
    assert "TCPI = (BAC − EV) ÷ (BAC − AC) | 3,08" in og

    # ---------------- riscos
    rk = rd(E / "aula-07-riscos/analise-riscos-fieldops.md")
    t6 = tabela(rk, r"\| ID \| Risco \| Tipo \| Prob\.")
    riscos = []
    for r in t6[2:]:
        riscos.append(dict(id=r[0], nome=r[1], p=num(r[3]), sev=num(r[10]), classe=r[13].replace("*", ""), prio=int(r[12])))
    assert len(riscos) == 22
    top5 = [r["id"] for r in sorted(riscos, key=lambda r: r["prio"])[:5]]
    assert top5 == ["R06", "R03", "R02", "R14", "R04"], top5
    F_["riscos"] = riscos
    assert sum(1 for r in riscos if r["classe"] == "Alta") == 5
    assert sum(1 for r in riscos if r["classe"] == "Média") == 13
    assert sum(1 for r in riscos if r["classe"] == "Baixa") == 4
    assert len(re.findall(r"^\| O0[1-4] \|", rk, re.M)) >= 4
    assert "**9 já se materializaram**" in rk
    for s in ["R$ 13.655", "R$ 6.635", "**P80 R$ 9.812**", "R$ 7.157,22"]:
        assert s in rk, s
    # celulas da matriz (do md)
    t7 = tabela(rk, r"\| Prob\. \\ Impacto médio")
    cel = {}
    for r in t7[2:]:
        p = num(r[0].replace("*", ""))
        for j, c in enumerate(r[1:]):
            ids = re.findall(r"R\d\d", c)
            cel[(p, j)] = ids
    F_["matriz"] = cel
    n_cel = sum(len(v) for v in cel.values())
    assert n_cel == 22, n_cel

    # ---------------- RACI
    ra = rd(E / "aula-06-rh-comunicacoes/organograma-raci-fieldops.md")
    assert "36 pacotes de trabalho de nível 2" in ra or "36 pacotes" in ra
    t8 = tabela(ra, r"\| Pessoa \| R \| A \| C \| I \|")
    raci = {}
    for r in t8[2:]:
        raci[r[0].split()[0].replace("*", "")] = tuple(int(x) for x in r[1:5])
    F_["raci"] = {k: raci[k] for k in ["FM", "JV", "GR", "PD", "AF"]}
    assert F_["raci"]["FM"] == (11, 21, 7, 0)
    assert sum(v[0] for v in F_["raci"].values()) == 36

    # ---------------- comunicacao
    pc = rd(E / "aula-06-rh-comunicacoes/plano-comunicacao-fieldops.md")
    assert "**19 comunicações.**" in pc
    # ---------------- partes interessadas
    pi = rd(E / "aula-08-aquisicoes-partes-interessadas/matriz-poder-interesse-fieldops.md")
    t9 = tabela(pi, r"\| ID \| Parte interessada \| Poder \|")
    parts = []
    for r in t9[2:]:
        parts.append(dict(id=r[0], nome=r[1], poder=int(r[2]), interesse=int(r[4]), quad=r[6].replace("*", "")))
    assert len(parts) == 13
    F_["partes"] = parts
    assert "Gerenciar com atenção: 5, Manter satisfeito: 2, Manter informado: 4, Monitorar: 2" in pi
    # ---------------- EAP: requisitos por entrega
    ea = rd(E / "aula-03-escopo/eap-fieldops.md")
    reqs = {}
    nomes = {}
    for ln in ea.splitlines():
        m = re.match(r"^\| (?:\*\*)?([1-7])\.(\d)(?:\*\*)? \| (?:\*\*)?(.+?)(?:\*\*)? \|", ln)
        if m:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            g = int(m.group(1))
            if m.group(2) == "0":
                nomes[g] = m.group(3)
            reqs.setdefault(g, "")
            reqs[g] += ", " + cells[3]
    assert len(reqs) == 7 and len(nomes) == 7, (len(reqs), len(nomes))

    def expande(txt):
        out = set()
        for part in re.split(r",\s*", txt.strip()):
            m = re.match(r"(RP|RJ)(\d\d) a (RP|RJ)(\d\d)", part)
            if m:
                for k in range(int(m.group(2)), int(m.group(4)) + 1):
                    out.add(f"{m.group(1)}{k:02d}")
            elif re.match(r"(RP|RJ)\d\d", part):
                out.add(part)
        return out
    F_["eap_req"] = {k: (nomes[k], expande(reqs[k])) for k in reqs}
    todos = set().union(*[v[1] for v in F_["eap_req"].values()])
    esperado = {f"RP{i:02d}" for i in range(1, 11)} | {f"RJ{i:02d}" for i in range(1, 9)}
    assert todos == esperado, esperado - todos
    F_["pacotes_por_entrega"] = {1: 4, 2: 4, 3: 7, 4: 6, 5: 7, 6: 4, 7: 4}
    assert sum(F_["pacotes_por_entrega"].values()) == 36
    # ---------------- qualidade
    ql = rd(E / "aula-05-custos-qualidade/qualidade-7-ferramentas-fieldops.md")
    for s in ["11% (6 de 55)", "| PRs com evidência de funcionamento anexada | 40%", "| PRs com issue vinculada (`Closes #N`) | 75%",
              "97% (onde havia CI)", "0 de 518", "| Taxa de sucesso das execuções de CI | 89%", "49 (89%)"]:
        assert s in ql, s
    # ---------------- backlog / base
    bk = rd(F / "15-backlog-do-produto.md")
    assert len(set(re.findall(r"PBI-0(?:0\d|[1-6]\d|7[0-2])\b", bk))) >= 72
    assert "EP-10" in bk
    return F_


if __name__ == "__main__":
    f = carrega()
    print("ok", f["issues"], f["horas"], f["itens_cron"], f["pacotes"])
