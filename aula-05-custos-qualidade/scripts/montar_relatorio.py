#!/usr/bin/env python3
"""Monta ../qualidade-7-ferramentas-fieldops.md a partir de relatorio_template.md e dados/resultados.json.

Os marcadores {{caminho.no.json|casas}} sao substituidos por numeros calculados em analise_qualidade.py
(formato pt-BR). Tabelas prontas ficam em md.* e entram com {{md.nome}}.
Uso: python3 montar_relatorio.py   (depois de analise_qualidade.py)
"""
import json
import re
from pathlib import Path

from estatistica import fmt

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parent
R = json.loads((BASE / "dados" / "resultados.json").read_text(encoding="utf-8"))

# ---- valores derivados
n = R["prs"]["amostra"]
rev = R["cruzamento"]["revisados_total"]
itens = {c["item"][:2]: c for c in R["folha"]["itens"]}
D = dict(
    sem_rev=n - rev,
    pct_rev=100 * rev / n,
    pct_sem_rev=100 * (n - rev) / n,
    pct_evid=itens["D7"]["pct"],
    pct_issue=itens["V4"]["pct"],
    pct_testes=itens["V7"]["pct"],
    pct_docs=itens["V8"]["pct"],
    pct_ci=itens["V5"]["pct"],
    pct_branch=itens["V1"]["pct"],
    pct_dod_marcado_issue=100 * R["issues_folha"]["dod_marcados"] / R["issues_folha"]["dod_total"],
    pct_prazo=100 * R["issues_folha"]["itens"]["Fechada até o fim da sprint prevista"] / R["issues_folha"]["den_prazo"],
    prazo_n=R["issues_folha"]["itens"]["Fechada até o fim da sprint prevista"],
    k17=sum(R['p_chart']['sprints'][str(s)]['k'] for s in range(1, 8)),
    n17=sum(R['p_chart']['sprints'][str(s)]['n'] for s in range(1, 8)),
    pct_titulo=itens['V2']['pct'],
    pct_ci_cruz=100 * R["cruzamento"]["d2_ci_sucesso"] / R["cruzamento"]["d2_declarado"],
    pareto_a_top=sum(i["n"] for i in R["pareto_defeitos"]["itens"][:R["pareto_defeitos"]["corte"]]),
    pareto_a_top_pct=R["pareto_defeitos"]["itens"][R["pareto_defeitos"]["corte"] - 1]["acum"],
    pareto_p_top_pct=R["pareto_defeitos"]["ponderado"][R["pareto_defeitos"]["corte_pond"] - 1]["acum"],
    pareto_b_top_pct=R["pareto_nc"]["itens"][R["pareto_nc"]["corte"] - 1]["acum"],
    pareto_b_top3=sum(i["n"] for i in R["pareto_nc"]["itens"][:3]),
    pareto_b_top3_pct=R["pareto_nc"]["itens"][2]["acum"],
    pct_8_semanas=100 * R["imr"]["valores"][10] / R["imr"]["total"],
    ci_taxa=R["ci"]["taxa_sucesso"],
    p1=12,
    media_lead_h=R["hist"]["lead"]["media"],
    mediana_lead_min=R["hist"]["lead"]["mediana"] * 60,
    mediana_pr_min=R["hist"]["tempo_pr"]["mediana"] * 60,
    n_pct_lt1h=R["hist"]["n_merge_lt_1h"],
    s2_p=100 * R["p_chart"]["sprints"]["2"]["p"],
    s6_p=100 * R["p_chart"]["sprints"]["6"]["p"],
    s7_p=100 * R["p_chart"]["sprints"]["7"]["p"],
    pbar=100 * R["p_chart"]["pbar"],
    s6_lcl=100 * R["p_chart"]["sprints"]["6"]["lcl"],
    s7_lcl=100 * R["p_chart"]["sprints"]["7"]["lcl"],
    abs_r_tam_tempo=abs(R["dispersao"]["tam_x_tempo"]["r"]),
)
R["d"] = D


def resolve(caminho):
    cur = R
    for parte in re.findall(r"[^.\[\]]+|\[\d+\]", caminho):
        cur = cur[int(parte[1:-1])] if parte.startswith("[") else cur[parte]
    return cur


def subst(m):
    caminho, casas = m.group(1).strip(), m.group(2)
    v = resolve(caminho)
    if isinstance(v, list):
        return (", ".join(v) if casas is None else str(len(v)))
    if isinstance(v, str):
        return v
    if casas is not None:
        return fmt(v, int(casas))
    if isinstance(v, int) or (isinstance(v, float) and float(v).is_integer() and abs(v) >= 100):
        return fmt(v, 0)
    return fmt(v, 1)


tpl = (AQUI / "relatorio_template.md").read_text(encoding="utf-8")
out = re.sub(r"\{\{\s*([^}|]+?)\s*(?:\|\s*(\d+))?\s*\}\}", subst, tpl)
(BASE / "qualidade-7-ferramentas-fieldops.md").write_text(out, encoding="utf-8")
print("gerado:", BASE / "qualidade-7-ferramentas-fieldops.md", len(out), "caracteres")
