#!/usr/bin/env python3
"""Analise de qualidade do FieldOps com as 7 ferramentas basicas.

Le os CSVs de ../dados (gerados por coleta_github.py), calcula todos os numeros e
gera os PNGs em ../ e o arquivo ../dados/resultados.json (numeros + tabelas em Markdown).
Depois rode montar_relatorio.py para produzir o .md final.

Uso: python3 analise_qualidade.py
Requer: numpy, matplotlib.
"""
import csv
import json
import re
import collections
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, Circle
from matplotlib.lines import Line2D

from estatistica import descritivas, pearson, spearman, regressao, fmt, p_valor_r

BASE = Path(__file__).resolve().parent.parent
DADOS = BASE / "dados"
OUT = BASE
BRT = timezone(timedelta(hours=-3))
INICIO = datetime(2026, 8, 10, tzinfo=BRT)
SNAPSHOT = datetime(2026, 11, 18, 23, 59, tzinfo=BRT)

AZUL, VERM, VERDE, AMAR, CINZA, ROXO = "#1f4e79", "#c0392b", "#2e8b57", "#e0a030", "#8a949e", "#6c4f9e"
plt.rcParams.update({"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 10, "xtick.labelsize": 9,
                     "ytick.labelsize": 9, "legend.fontsize": 9, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False})

SPRINTS = {1: ("10/08", "21/08"), 2: ("24/08", "04/09"), 3: ("07/09", "18/09"), 4: ("21/09", "02/10"),
           5: ("05/10", "16/10"), 6: ("19/10", "30/10"), 7: ("02/11", "13/11"), 8: ("16/11", "27/11")}
FIM_SPRINT = {s: datetime(2026, int(f[3:]), int(f[:2]), 23, 59, 59, tzinfo=BRT) for s, (_, f) in SPRINTS.items()}


def dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def le(nome):
    with open(DADOS / nome, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def tabela_md(cab, linhas, alinh=None):
    alinh = alinh or ["---"] * len(cab)
    s = "| " + " | ".join(cab) + " |\n| " + " | ".join(alinh) + " |\n"
    for l in linhas:
        s += "| " + " | ".join(str(c) for c in l) + " |\n"
    return s


R = {"md": {}}  # resultados
PRS, ISS, COM, RUNS = le("prs.csv"), le("issues.csv"), le("commits.csv"), le("ci_runs.csv")
META = json.loads((DADOS / "coleta_meta.json").read_text(encoding="utf-8"))
R["coleta_utc"] = META["coletado_em_utc"]

# ---------------------------------------------------------------- amostra de PRs
triviais = [p for p in PRS if p["state"] == "MERGED" and int(p["body_len"]) == 0]
fechados = [p for p in PRS if p["state"] == "CLOSED"]
abertos = [p for p in PRS if p["state"] == "OPEN"]
AMOSTRA = [p for p in PRS if p["state"] == "MERGED" and int(p["body_len"]) > 0]
AMOSTRA.sort(key=lambda p: (dt(p["created"]), p["repo"]))
R["prs"] = dict(total=len(PRS), mergeados=sum(p["state"] == "MERGED" for p in PRS), triviais=len(triviais),
                fechados_sem_merge=len(fechados), abertos=len(abertos), amostra=len(AMOSTRA),
                por_repo={r: sum(p["repo"] == r for p in AMOSTRA) for r in ["backend", "frontend", "app", "docs"]})
R["issues"] = dict(total=len(ISS), fechadas=sum(i["state"] == "CLOSED" for i in ISS),
                   abertas=sum(i["state"] == "OPEN" for i in ISS),
                   rotulos_defeito=sum(1 for i in ISS if i["tipo"] in ("bug", "defeito", "fix")))
R["issues"]["abertas_sem_responsavel"] = sum(1 for i in ISS if i["state"] == "OPEN" and i["n_assignees"] == "0")
R["issues"]["backend_abertas_sem_resp"] = sum(1 for i in ISS if i["state"] == "OPEN" and i["n_assignees"] == "0" and i["repo"] == "backend")

# primeira execucao de CI por repositorio
PRIM_CI = {}
for r in ["backend", "frontend", "app"]:
    ds = [dt(x["created"]) for x in RUNS if x["repo"] == r and x["workflow"] == "CI"]
    PRIM_CI[r] = min(ds) if ds else None
R["ci_primeiro_run"] = {r: (v.astimezone(BRT).strftime("%d/%m/%Y") if v else None) for r, v in PRIM_CI.items()}

# ---------------------------------------------------------------- (iii) folha de verificacao
DOD_ROTULOS = [
    ("D1", "dod1_branch_pr", "Código em branch própria, via PR"),
    ("D2", "dod2_lint_tipos", "Lint e verificação de tipos passando"),
    ("D3", "dod3_sem_segredos", "Sem segredos versionados"),
    ("D4", "dod4_sem_logs", "Sem logs sensíveis"),
    ("D5", "dod5_erros", "Comportamento de erro tratado"),
    ("D6", "dod6_docs", "Documentação/README atualizados"),
    ("D7", "dod7_evidencia", "Evidência de funcionamento anexada"),
    ("D8", "dod8_revisao", "Revisado por outra pessoa"),
]
RE_BRANCH = re.compile(r"^(feat|fix|chore|docs|refactor|test|ci|build|perf)/EP-\d\d-[a-z0-9-]+$")
RE_TITULO = re.compile(r"^(feat|fix|chore|docs|refactor|test|ci|build|perf|style)(\([^)]+\))?!?: .+")


def verifica(p):
    """Retorna dict V1..V8 com 1 (conforme), 0 (nao conforme) ou -1 (nao se aplica)."""
    v = {}
    v["V1"] = int(bool(RE_BRANCH.match(p["head"])))
    v["V2"] = int(bool(RE_TITULO.match(p["title"])))
    v["V3"] = int(p["base"] == "develop")
    v["V4"] = int(bool(p["issue_refs"]))
    ci_ini = PRIM_CI.get(p["repo"])
    if ci_ini is None or dt(p["created"]) < ci_ini - timedelta(minutes=10):
        v["V5"] = -1
    else:
        v["V5"] = int(p["ci"] == "SUCCESS")
    v["V6"] = int(int(p["n_reviews_outra_pessoa"]) >= 1)
    tipo = p["tipo_titulo"]
    v["V7"] = int(int(p["n_arquivos_teste"]) > 0) if tipo in ("feat", "fix", "refactor") else -1
    v["V8"] = int(int(p["n_arquivos_doc"]) > 0) if tipo == "feat" else -1
    return v


V_ROTULOS = [
    ("V1", "Branch no padrão <tipo>/EP-xx-slug"),
    ("V2", "Título em Conventional Commits"),
    ("V3", "PR aberto contra `develop`"),
    ("V4", "Issue/card vinculado (Closes #N)"),
    ("V5", "CI verde (onde havia CI)"),
    ("V6", "Revisão registrada por outra pessoa"),
    ("V7", "Testes no diff (feat/fix/refactor)"),
    ("V8", "README/OpenAPI/ADR no diff (feat)"),
]
MATRIZ = []  # linhas: lista de 55 valores
for cod, chave, _ in DOD_ROTULOS:
    MATRIZ.append([{"x": 1, "o": 0, "-": -1}[p[chave]] for p in AMOSTRA])
VV = [verifica(p) for p in AMOSTRA]
for cod, _ in V_ROTULOS:
    MATRIZ.append([v[cod] for v in VV])
ROTULOS_LINHAS = [f"{c}  {t}" for c, _, t in DOD_ROTULOS] + [f"{c}  {t}" for c, t in V_ROTULOS]
CONT = []
for i, linha in enumerate(MATRIZ):
    ok, nok, na = linha.count(1), linha.count(0), linha.count(-1)
    CONT.append(dict(item=ROTULOS_LINHAS[i], conformes=ok, nao_conformes=nok, nao_aplicavel=na,
                     aplicaveis=ok + nok, pct=(100 * ok / (ok + nok)) if ok + nok else None))
R["folha"] = dict(n=len(AMOSTRA), itens=CONT)
linhas = []
for c in CONT:
    marca = "(autodeclarado no PR)" if c["item"].startswith("D") else "(verificado nos metadados)"
    linhas.append([c["item"].replace("  ", " – ", 1), "autodeclarado" if c["item"].startswith("D") else "verificado",
                   c["aplicaveis"], c["conformes"], c["nao_conformes"], c["nao_aplicavel"], fmt(c["pct"], 0) + "%"])
R["md"]["folha"] = tabela_md(["Item", "Origem da marca", "Aplicáveis", "✔ Conforme", "✘ Não conforme", "N/A ou sem checklist", "% conforme"],
                             linhas, ["---", "---", "---:", "---:", "---:", "---:", "---:"])

# verificacoes cruzadas: declarado x verificado
idx = {p["repo"] + "#" + p["number"]: k for k, p in enumerate(AMOSTRA)}
d2x = [k for k, p in enumerate(AMOSTRA) if p["dod2_lint_tipos"] == "x"]
d6x = [k for k, p in enumerate(AMOSTRA) if p["dod6_docs"] == "x"]
d8x = [k for k, p in enumerate(AMOSTRA) if p["dod8_revisao"] == "x"]
R["cruzamento"] = dict(
    d2_declarado=len(d2x),
    d2_ci_sucesso=sum(AMOSTRA[k]["ci"] == "SUCCESS" for k in d2x),
    d2_ci_falha=sum(AMOSTRA[k]["ci"] == "FAILURE" for k in d2x),
    d2_sem_ci=sum(AMOSTRA[k]["ci"] == "NENHUM" for k in d2x),
    d6_declarado=len(d6x), d6_com_doc=sum(int(AMOSTRA[k]["n_arquivos_doc"]) > 0 for k in d6x),
    d8_declarado=len(d8x), d8_com_review=sum(int(AMOSTRA[k]["n_reviews_outra_pessoa"]) > 0 for k in d8x),
    revisados_total=sum(int(p["n_reviews_outra_pessoa"]) > 0 for p in AMOSTRA),
    aprovados_total=sum(int(p["aprovado_por_outra_pessoa"]) for p in AMOSTRA),
    pediram_mudancas=sum(int(p["pediu_mudancas"]) for p in AMOSTRA),
    com_checklist=sum(p["dod1_branch_pr"] != "-" for p in AMOSTRA),
    sem_checklist=sum(p["dod1_branch_pr"] == "-" for p in AMOSTRA),
    merge_ci_vermelho=[f'{p["repo"]}#{p["number"]}' for p in AMOSTRA if p["ci"] == "FAILURE"],
    base_fora_develop=[f'{p["repo"]}#{p["number"]}' for p in AMOSTRA if p["base"] != "develop"],
)
# escore de conformidade com DoD por PR (itens D marcados / itens D presentes)
ESCORE = []
for p in AMOSTRA:
    marcas = [p[c] for _, c, _ in DOD_ROTULOS]
    tot = marcas.count("x") + marcas.count("o")
    ESCORE.append(marcas.count("x") / tot if tot else np.nan)

# folha de verificacao de issues fechadas
fech = [i for i in ISS if i["state"] == "CLOSED"]
prs_merge = [p for p in PRS if p["state"] == "MERGED"]
ref_por_issue = collections.defaultdict(list)
for p in prs_merge:
    for n in filter(None, p["issue_refs"].split(";")):
        ref_por_issue[(p["repo"], int(n))].append(p["number"])
ic = collections.OrderedDict()
ic["Tem responsável designado"] = sum(i["n_assignees"] != "0" for i in fech)
ic["Vinculada a milestone (sprint)"] = sum(i["sprint"] != "" for i in fech)
ic["Citada por PR mergeado (Closes/ref)"] = sum((i["repo"], int(i["number"])) in ref_por_issue for i in fech)
ic["Fechada até o fim da sprint prevista"] = sum(
    1 for i in fech if i["sprint"] != "" and dt(i["closed"]) <= FIM_SPRINT[int(i["sprint"])])
ic["Critérios de aceitação marcados (≥1 caixa)"] = sum(int(i["ac_marcados"]) > 0 for i in fech)
ic["Checklist de DoD marcado (≥1 caixa)"] = sum(int(i["dod_marcados"]) > 0 for i in fech)
den_prazo = sum(1 for i in fech if i["sprint"] != "")
R["issues_folha"] = dict(fechadas=len(fech), itens=dict(ic), den_prazo=den_prazo,
                         ac_marcados=sum(int(i["ac_marcados"]) for i in fech), ac_total=sum(int(i["ac_total"]) for i in fech),
                         dod_marcados=sum(int(i["dod_marcados"]) for i in fech), dod_total=sum(int(i["dod_total"]) for i in fech))
ln = []
for k, v in ic.items():
    den = den_prazo if "prazo" in k else len(fech)
    ln.append([k, den, v, den - v, fmt(100 * v / den, 0) + "%"])
R["md"]["folha_issues"] = tabela_md(["Verificação (issue fechada)", "Aplicáveis", "✔", "✘", "% conforme"], ln,
                                    ["---", "---:", "---:", "---:", "---:"])

# ---------------------------------------------------------------- (iv) Pareto
FIX = [c for c in COM if c["tipo"] == "fix" and c["merge"] == "0"]
CATS = [
    ("Sessão, autenticação e segurança", r"sign-out|session|control characters|token|non-raster|revalidate", 10),
    ("Persistência, offline e sincronização", r"fix\(database|outbox|fix\(sync|relative paths|failed uploads", 10),
    ("Contrato, erros e migrações da API", r"openapi|renumber|migration|409|fix\(api\): describe", 5),
    ("Build, tipos, dependências e testes", r"typescript|route types|springdoc|fix\(test", 3),
    ("Regras de negócio e fluxo de inspeção", r"fix\((inspections|checklist|scanner|equipment|home)\)", 5),
    ("Acessibilidade e estados de interface", r"focus|language|unavailable|count fails", 3),
    ("Layout e acabamento visual", r".*", 1),
]


def classifica(msg):
    for nome, rx, w in CATS:
        if re.search(rx, msg, re.I):
            return nome
    return CATS[-1][0]


for c in FIX:
    c["categoria"] = classifica(c["msg"])
with open(DADOS / "fixes_classificados.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["repo", "data", "autor", "mensagem", "categoria"])
    for c in sorted(FIX, key=lambda c: (c["repo"], c["date"])):
        w.writerow([c["repo"], c["date"][:10], c["autor"], c["msg"], c["categoria"]])
PESO = {n: w for n, _, w in CATS}


def pareto(contagens):
    itens = sorted(contagens.items(), key=lambda kv: -kv[1])
    tot = sum(v for _, v in itens)
    acum, out = 0, []
    for k, v in itens:
        acum += v
        out.append(dict(categoria=k, n=v, pct=100 * v / tot, acum=100 * acum / tot))
    corte = next(i for i, o in enumerate(out) if o["acum"] >= 80)
    return out, corte, tot


cont_def = collections.Counter(c["categoria"] for c in FIX)
PA, corteA, totA = pareto(cont_def)
pond = collections.Counter()
for c in FIX:
    pond[c["categoria"]] += PESO[c["categoria"]]
PAp, cortePAp, totPAp = pareto(pond)
R["pareto_defeitos"] = dict(total=totA, itens=PA, corte=corteA + 1, ponderado=PAp, corte_pond=cortePAp + 1, total_pond=totPAp,
                            por_repo=dict(collections.Counter(c["repo"] for c in FIX)),
                            por_autor=dict(collections.Counter(c["autor"] for c in FIX)))
R["md"]["pareto_defeitos"] = tabela_md(
    ["Categoria de defeito (commits `fix`)", "Peso (sev.)", "Qtd.", "%", "% acum.", "Peso×Qtd.", "% acum. ponderado"],
    [[a["categoria"], PESO[a["categoria"]], a["n"], fmt(a["pct"], 1) + "%", fmt(a["acum"], 1) + "%",
      pond[a["categoria"]], next(fmt(b["acum"], 1) + "%" for b in PAp if b["categoria"] == a["categoria"])] for a in PA],
    ["---", "---:", "---:", "---:", "---:", "---:", "---:"])

# Pareto B: nao conformidades de processo (marcas ✘ da folha de verificacao)
NC = collections.OrderedDict()
for i, c in enumerate(CONT):
    cod = c["item"][:2]
    if cod in ("D1", "D2", "D3", "D4", "D5", "D6", "D8"):
        continue  # autodeclarados: D8 duplica V6; D1-D6 sao confrontados com V1/V5/V8 (secao de cruzamento)
    NC[c["item"][4:]] = c["nao_conformes"]
PB, corteB, totB = pareto(NC)
R["pareto_nc"] = dict(total=totB, itens=PB, corte=corteB + 1)
R["md"]["pareto_nc"] = tabela_md(["Não conformidade de processo (folha de verificação)", "Qtd. de marcas ✘", "%", "% acum."],
                                 [[a["categoria"], a["n"], fmt(a["pct"], 1) + "%", fmt(a["acum"], 1) + "%"] for a in PB],
                                 ["---", "---:", "---:", "---:"])

# falhas de CI por passo
falhas = [x for x in RUNS if x["conclusion"] == "failure"]
R["ci"] = dict(runs=len(RUNS), por_repo={r: dict(collections.Counter(x["conclusion"] for x in RUNS if x["repo"] == r and x["workflow"] == "CI"))
                                          for r in ["backend", "frontend", "app"]},
               falhas=len(falhas), falhas_passo=dict(collections.Counter(x["passo_falho"] for x in falhas)))
tot_ci = sum(1 for x in RUNS if x["workflow"] == "CI" and x["conclusion"] in ("success", "failure"))
R["ci"]["taxa_sucesso"] = 100 * sum(1 for x in RUNS if x["workflow"] == "CI" and x["conclusion"] == "success") / tot_ci
R["ci"]["total_ci_validos"] = tot_ci

# ---------------------------------------------------------------- (v) histograma
tam = np.array([int(p["additions_sem_lock"]) + int(p["deletions_sem_lock"]) for p in AMOSTRA], float)
t_abre = np.array([(dt(p["merged"]) - dt(p["created"])).total_seconds() / 3600 for p in AMOSTRA])
t_lead = np.array([(dt(p["merged"]) - dt(p["first_commit"])).total_seconds() / 3600 for p in AMOSTRA])
nfiles = np.array([int(p["changed_files"]) for p in AMOSTRA], float)
R["hist"] = dict(tamanho=descritivas(tam), tempo_pr=descritivas(t_abre), lead=descritivas(t_lead),
                 pct_tam_gt_1000=float(100 * (tam > 1000).mean()), pct_tam_gt_400=float(100 * (tam > 400).mean()),
                 pct_merge_lt_1h=float(100 * (t_abre < 1).mean()), pct_merge_lt_24h=float(100 * (t_abre < 24).mean()),
                 pct_merge_gt_72h=float(100 * (t_abre > 72).mean()), n_merge_gt_72h=int((t_abre > 72).sum()),
                 n_tam_gt_1000=int((tam > 1000).sum()), n_tam_gt_400=int((tam > 400).sum()),
                 n_merge_lt_1h=int((t_abre < 1).sum()))
sep_rep = {}
for r in ["backend", "frontend", "app"]:
    m = np.array([p["repo"] == r for p in AMOSTRA])
    sep_rep[r] = dict(n=int(m.sum()), tam_mediana=float(np.median(tam[m])), tempo_mediano=float(np.median(t_abre[m])))
R["hist"]["por_repo"] = sep_rep

# ---------------------------------------------------------------- (vi) graficos de controle
sp = {}
for s in range(1, 9):
    its = [i for i in ISS if i["sprint"] == str(s)]
    sp[s] = dict(n=len(its), k=sum(i["state"] == "CLOSED" for i in its))
    prazo = sum(1 for i in its if i["state"] == "CLOSED" and dt(i["closed"]) <= FIM_SPRINT[s])
    sp[s]["no_prazo"] = prazo
for s, d in sp.items():
    d["p"] = d["k"] / d["n"]
base_s = [s for s in range(1, 8)]
pbar = sum(sp[s]["k"] for s in base_s) / sum(sp[s]["n"] for s in base_s)
for s, d in sp.items():
    sig = np.sqrt(pbar * (1 - pbar) / d["n"])
    d["sigma"] = float(sig)
    d["ucl"] = float(min(1, pbar + 3 * sig))
    d["lcl"] = float(max(0, pbar - 3 * sig))
    d["u2"] = float(min(1, pbar + 2 * sig))
    d["l2"] = float(max(0, pbar - 2 * sig))
    d["sinal"] = "acima do LSC" if d["p"] > d["ucl"] else ("abaixo do LIC" if d["p"] < d["lcl"] else "")
# regra 2 de 3 acima de 2 sigma / abaixo
for s in range(1, 7):
    tri = [sp[x] for x in (s, s + 1, s + 2)]
    if sum(t["p"] < t["l2"] for t in tri) >= 2 and not sp[s + 2]["sinal"]:
        sp[s + 2]["sinal"] = "2 de 3 abaixo de 2σ"
sp[8]["sinal"] = "S8 em curso: não avaliada"
R["p_chart"] = dict(pbar=pbar, sprints=sp, total_k=sum(d["k"] for d in sp.values()), total_n=sum(d["n"] for d in sp.values()))
R["md"]["p_chart"] = tabela_md(
    ["Sprint", "Período", "Concluídas (k)", "Total (n)", "p = k/n", "LIC", "LSC", "Fechadas no prazo", "Sinal"],
    [[f"S{s}", f"{SPRINTS[s][0]}–{SPRINTS[s][1]}", d["k"], d["n"], fmt(100 * d["p"], 1) + "%", fmt(100 * d["lcl"], 1) + "%",
      fmt(100 * d["ucl"], 1) + "%", f"{d['no_prazo']}/{d['n']}" if s < 8 else "em curso", d["sinal"] or "—"] for s, d in sp.items()],
    ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"])

# commits por semana (sem merges; 4 repositorios; semanas 1..15)
sem = collections.Counter()
sem_rep = collections.defaultdict(collections.Counter)
for c in COM:
    if c["merge"] == "1":
        continue
    d = dt(c["date"]).astimezone(BRT)
    w = (d - INICIO).days // 7 + 1
    sem[w] += 1
    sem_rep[c["repo"]][w] += 1
semanas = list(range(1, 16))
X = np.array([sem.get(w, 0) for w in semanas], float)
base_w = X[:14]  # semana 15 incompleta (ate 18/11)
mr = np.abs(np.diff(base_w))
cl, mrbar = base_w.mean(), mr.mean()
ucl_i, lcl_i = cl + 2.66 * mrbar, cl - 2.66 * mrbar
ucl_mr = 3.267 * mrbar
sinais_i = [int(w) for w, x in zip(semanas[:14], base_w) if x > ucl_i or x < max(lcl_i, 0) and lcl_i > 0]
# regra: 8 pontos consecutivos do mesmo lado
acima = base_w > cl
run, melhor = 1, 1
for i in range(1, len(acima)):
    run = run + 1 if acima[i] == acima[i - 1] else 1
    melhor = max(melhor, run)
R["imr"] = dict(semanas=semanas, valores=X.tolist(), cl=float(cl), mrbar=float(mrbar), ucl=float(ucl_i), lcl=float(lcl_i),
                ucl_mr=float(ucl_mr), mr=mr.tolist(), sinais=sinais_i, sem15=float(X[14]), maior_sequencia_mesmo_lado=int(melhor),
                zero=[w for w, x in zip(semanas, X) if x == 0], total=float(X.sum()),
                pico=dict(semana=int(semanas[int(np.argmax(X))]), valor=float(X.max())),
                pct_pico_top3=float(100 * np.sort(X)[-3:].sum() / X.sum()),
                n_semanas_zero_ou_abaixo=int((base_w <= 2).sum()))
sinais_mr = [int(w) for w, m in zip(semanas[1:14], mr) if m > ucl_mr]
R["imr"]["sinais_mr"] = sinais_mr
# concentracao de commits por pessoa/repositorio (fator onibus)
conc = {}
for r in ["backend", "frontend", "app", "docs"]:
    cs = [c for c in COM if c["repo"] == r and c["merge"] == "0"]
    cnt = collections.Counter(c["autor"] for c in cs)
    top, n = cnt.most_common(1)[0]
    conc[r] = dict(total=len(cs), top=top, n_top=n, pct=100 * n / len(cs), dist=dict(cnt))
R["concentracao"] = conc

# ---------------------------------------------------------------- (vii) dispersao
rg1 = regressao(np.log10(tam), np.log10(t_abre + 0.01))
sp1 = spearman(tam, t_abre)
rg1["spearman"] = sp1
rg1["pearson_bruto"] = pearson(tam, t_abre)
ok = ~np.isnan(np.array(ESCORE))
rg2 = regressao(tam[ok], np.array(ESCORE)[ok] * 100)
rg2["spearman"] = spearman(tam[ok], np.array(ESCORE)[ok])
planej = np.array([sp[s]["n"] for s in range(1, 8)], float)
concl = np.array([sp[s]["k"] for s in range(1, 8)], float)
rg3 = regressao(planej, concl)
rg3["spearman"] = spearman(planej, concl)
rg4 = regressao(tam, nfiles)
rg4["spearman"] = spearman(tam, nfiles)
R["dispersao"] = dict(tam_x_tempo=rg1, tam_x_dod=rg2, plan_x_concl=rg3, tam_x_arquivos=rg4)

# ================================================================= FIGURAS


def salva(fig, nome):
    fig.savefig(OUT / nome, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---- 1. Ishikawa
def ishikawa():
    fig, ax = plt.subplots(figsize=(19, 10.5))
    ax.set_xlim(0, 19)
    ax.set_ylim(-5.6, 5.6)
    ax.axis("off")
    ax.plot([0.3, 14.6], [0, 0], color=AZUL, lw=3.5)
    ax.add_patch(FancyBboxPatch((14.7, -1.35), 4.1, 2.7, boxstyle="round,pad=0.08", fc=AZUL, ec=AZUL))
    ax.text(16.75, 0, "EFEITO\nFalhas de sincronização\noffline e defeitos que\nescapam para a integração",
            ha="center", va="center", color="white", fontsize=11.5, fontweight="bold", linespacing=1.4)
    cats = collections.OrderedDict([
        ("PESSOAS", [("Mobile quase só com um integrante: {mob}% dos commits do app".format(mob=fmt(conc['app']['pct'], 0)), "R"),
                     ("{n} issues do backend (sync, evidências, revisão) sem responsável".format(n=R['issues']['backend_abertas_sem_resp']), "R"),
                     ("PRs sem revisor: \"sem revisor disponível\" no checklist", "R"),
                     ("Equipe nova em outbox/idempotência (curva de aprendizado)", "P")]),
        ("PROCESSO", [("{m} de {a} PRs sem revisão registrada de outra pessoa".format(m=R['folha']['n'] - R['cruzamento']['revisados_total'], a=R['folha']['n']), "R"),
                      ("PRs empilhados e conflitos (migração V5 duplicada, shell fora da develop)", "R"),
                      ("Integração só no fim: mocks + sync do backend não iniciado", "R"),
                      ("Testes de integração planejados só para S7/S8", "R")]),
        ("FERRAMENTAS", [("CI do backend só desde {d} (PR #60)".format(d=R['ci_primeiro_run']['backend']), "R"),
                         ("CI do app vermelho: {n} de {t} falhas por expo-doctor".format(n=max(R['ci']['falhas_passo'].values()), t=R['ci']['falhas']), "R"),
                         ("Sem ambiente de integração compartilhado (backend#33 aberta)", "R"),
                         ("Sem teste de contrato OpenAPI × clientes", "P")]),
        ("REQUISITOS", [("Contrato de sync em aberto (docs#2; push/pull separados ou único)", "R"),
                        ("Idempotência/conflito: RN-067 a RN-078 (12 regras)", "R"),
                        ("by-qr sem escopo por perfil (RN-063) achado só no app", "R"),
                        ("Stack divergente (Angular × Next.js) sem ADR fechado", "R")]),
        ("AMBIENTE", [("Rede instável em campo; validação só em emulador (premissa)", "P"),
                      ("Dependências em movimento: Expo SDK 57, Spring Boot 4, Next 16", "R"),
                      ("4 feriados no período (07/09, 12/10, 02/11, 20/11)", "R"),
                      ("Android heterogêneo (câmera, QR Code, GPS)", "P")]),
        ("MEDIÇÃO", [("{a} de {b} caixas de DoD marcadas nas issues fechadas".format(a=R['issues_folha']['dod_marcados'], b=R['issues_folha']['dod_total']), "R"),
                     ("Fechamento em lote (ex.: 5 issues do web no mesmo minuto)", "R"),
                     ("Nenhum rótulo de defeito nas {n} issues".format(n=R['issues']['total']), "R"),
                     ("Cobertura de testes e taxa de defeitos não medidas", "P")]),
    ])
    xa = [5.3, 9.6, 13.9]
    dx = 1.7
    import textwrap
    for k, (nome, causas) in enumerate(cats.items()):
        top = k < 3
        sgn = 1 if top else -1
        x0 = xa[k % 3]
        ax.plot([x0 - dx, x0], [sgn * 4.4, 0], color=AZUL, lw=2.4)
        ax.text(x0 - dx, sgn * 4.75, nome, ha="center", va="center", fontsize=11.5, fontweight="bold", color="white",
                bbox=dict(boxstyle="round,pad=0.35", fc=VERM, ec=VERM))
        for j, (txt, tag) in enumerate(causas):
            y = sgn * (3.55 - j * 0.98)
            xb = x0 - dx * abs(y) / 4.4
            ax.plot([xb - 0.25, xb], [y, y], color=CINZA, lw=1.4)
            lab = ("★ " if tag == "R" else "○ ") + txt
            ax.text(xb - 0.32, y, textwrap.fill(lab, 33), ha="right", va="center", fontsize=9.2,
                    color="#111" if tag == "R" else "#555", linespacing=1.15)
    ax.text(0.3, -5.45, "★ evidência real coletada no GitHub (issues, PRs, commits, CI)     ○ premissa do gerente (sem dado)",
            fontsize=9.5, color="#333", ha="left")
    salva(fig, "01-ishikawa.png")


ishikawa()

# ---- 2. Fluxogramas


def no(ax, x, y, w, h, txt, kind="proc", fc="#e8f0f8", fs=9.6):
    ec = AZUL
    if kind == "proc":
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=ec, lw=1.6))
    elif kind == "term":
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.45", fc=fc, ec=ec, lw=1.6))
    elif kind == "dec":
        ax.add_patch(Polygon([(x - w / 2, y), (x, y + h / 2), (x + w / 2, y), (x, y - h / 2)], closed=True, fc="#fdf1d8", ec="#b07a10", lw=1.6))
    ax.text(x, y, txt, ha="center", va="center", fontsize=fs, linespacing=1.2)


def seta(ax, p, q, txt=None, rad=0.0, dx=0.0, dy=0.0, color="#333"):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5,
                                                    connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))
    if txt:
        ax.text((p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, txt, fontsize=9.5, fontweight="bold", color=color,
                ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.6))


def conector(ax, x, y, letra):
    ax.add_patch(Circle((x, y), 0.32, fc="white", ec=VERM, lw=1.6))
    ax.text(x, y, letra, ha="center", va="center", fontsize=10, fontweight="bold", color=VERM)


def fluxogramas():
    fig, ax = plt.subplots(figsize=(21, 15))
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 15)
    ax.axis("off")
    ax.text(0.2, 14.55, "A. Fluxo de qualidade de uma entrega: issue → PR → revisão → CI → merge → demo → aceite", fontsize=13, fontweight="bold", color=AZUL)
    y1 = 12.4
    xs = [1.7, 4.9, 8.2, 11.6, 15.2, 19.0]
    no(ax, xs[0], y1, 2.6, 1.3, "Issue da sprint\ncom critérios de\naceitação (AC) e DoD", "term", "#dff0e4")
    no(ax, xs[1], y1, 2.8, 1.3, "Branch a partir da\n`develop`:\n<tipo>/EP-xx-slug")
    no(ax, xs[2], y1, 3.0, 1.3, "Implementar + testar\nlocalmente (lint,\ntipos, testes)")
    no(ax, xs[3], y1, 3.2, 1.5, "Abrir PR para `develop`\ncom template: Closes #N,\nevidência, checklist DoD")
    no(ax, xs[4], y1, 3.2, 1.9, "CI verde?\n(build, lint, tipos,\ntestes, CodeQL)", "dec")
    conector(ax, xs[5], y1, "A")
    for a, b in zip(range(3), range(1, 4)):
        seta(ax, (xs[a] + [1.3, 1.4, 1.5][a], y1), (xs[b] - [1.4, 1.5, 1.6][a], y1))
    seta(ax, (xs[3] + 1.6, y1), (xs[4] - 1.6, y1))
    seta(ax, (xs[4] + 1.6, y1), (xs[5] - 0.32, y1), "Não", dy=0.3, color=VERM)
    # retorno A -> implementar
    conector(ax, xs[2], 14.1, "A")
    seta(ax, (xs[2], 14.1 - 0.32), (xs[2], y1 + 0.65), "corrige e\nreenvia push", dx=1.15, color=VERM)
    # linha 2
    y2 = 9.0
    seta(ax, (xs[4], y1 - 0.95), (xs[4], y2 + 0.65), "Sim", dx=0.45, color=VERDE)
    no(ax, 15.2, y2, 2.8, 1.3, "Revisão por outra\npessoa da equipe\n(política CONTRIBUTING)", fs=9.2)
    no(ax, 11.9, y2, 2.3, 1.8, "Aprovado?", "dec")
    no(ax, 8.5, y2, 2.7, 1.3, "Merge em `develop`\n(base correta, sem\nPR empilhado)", fs=9.2)
    no(ax, 5.3, y2, 2.8, 1.3, "Demo da sprint com\ndados de teste\n(DoD da sprint)", fs=9.2)
    no(ax, 2.0, y2, 2.6, 1.8, "Atende AC e\nDoD da sprint?", "dec", fs=9.2)
    seta(ax, (13.8, y2), (13.05, y2))
    seta(ax, (10.75, y2), (9.85, y2), "Sim", dy=0.3, color=VERDE)
    seta(ax, (7.15, y2), (6.7, y2))
    seta(ax, (3.9, y2), (3.3, y2))
    no(ax, 11.9, 6.7, 3.0, 1.2, "Ajustes pedidos\n(CHANGES_REQUESTED)")
    seta(ax, (11.9, y2 - 0.9), (11.9, 6.7 + 0.6), "Não", dx=0.45, color=VERM)
    conector(ax, 14.2, 6.7, "A")
    seta(ax, (13.4, 6.7), (14.2 - 0.32, 6.7))
    no(ax, 2.0, 6.4, 2.8, 1.3, "Registrar não\nconformidade\n(fluxo B)", "proc", "#fbe3e0")
    seta(ax, (2.0, y2 - 0.9), (2.0, 6.4 + 0.65), "Não", dx=0.5, color=VERM)
    no(ax, 6.0, 6.4, 3.9, 1.3, "Aceite do incremento (PI-02/PI-03);\natualizar issue, milestone e backlog", "term", "#dff0e4", fs=9.2)
    seta(ax, (2.65, y2 - 0.45), (5.0, 6.4 + 0.65), "Sim", dx=-0.3, dy=0.35, color=VERDE)
    ax.text(20.8, 6.7, "A = volta à etapa\n\"Implementar + testar\"", ha="right", va="center", fontsize=9.5, color=VERM)
    # painel B
    ax.plot([0.2, 20.8], [5.35, 5.35], color=CINZA, lw=1, ls="--")
    ax.text(0.2, 4.95, "B. Tratamento de não conformidade (defeito, desvio de DoD ou falha de CI)", fontsize=13, fontweight="bold", color=AZUL)
    yb = 3.35
    xb = [1.9, 5.6, 9.5, 13.6, 17.9]
    no(ax, xb[0], yb, 3.0, 1.3, "Detecção: revisão, CI,\ndemo, teste ou uso", "term", "#fbe3e0")
    no(ax, xb[1], yb, 3.4, 1.3, "Abrir issue de defeito\ncom evidência e severidade\n(DoD 18.7)")
    no(ax, xb[2], yb, 3.3, 1.9, "Severidade\ncrítica ou alta?", "dec")
    no(ax, xb[3], yb + 0.85, 3.6, 1.15, "Bloqueia a entrega: correção\nimediata e plano de contenção", "proc", "#fbe3e0")
    no(ax, xb[3], yb - 0.95, 3.6, 1.15, "Médio: aceitar com registro e plano;\nBaixo: manter no backlog")
    seta(ax, (xb[0] + 1.5, yb), (xb[1] - 1.7, yb))
    seta(ax, (xb[1] + 1.7, yb), (xb[2] - 1.65, yb))
    seta(ax, (xb[2] + 0.4, yb + 0.7), (xb[3] - 1.8, yb + 0.85), "Sim", dy=0.3, dx=-0.2, color=VERM)
    seta(ax, (xb[2] + 0.4, yb - 0.7), (xb[3] - 1.8, yb - 0.95), "Não", dy=-0.3, dx=-0.2, color=VERDE)
    no(ax, xb[4], yb, 3.0, 2.6, "Corrigir em branch\nfix/EP-xx via PR;\nteste de regressão\n+ revisão; reabrir\no fluxo A", "proc")
    seta(ax, (xb[3] + 1.8, yb + 0.85), (xb[4] - 1.5, yb + 0.5))
    seta(ax, (xb[3] + 1.8, yb - 0.95), (xb[4] - 1.5, yb - 0.5))
    no(ax, 15.2, 0.9, 4.2, 1.1, "Análise de causa (5 porquês / Ishikawa)\ne ação preventiva", "proc", "#e8f0f8", fs=9.2)
    no(ax, 8.6, 0.9, 5.4, 1.1, "Atualizar DoD/plano; registrar lição aprendida;\nacompanhar na revisão da sprint", "term", "#dff0e4", fs=9.2)
    seta(ax, (xb[4] - 0.3, yb - 1.3), (15.2 + 0.8, 0.9 + 0.55), rad=0.0)
    seta(ax, (15.2 - 2.1, 0.9), (8.6 + 2.7, 0.9))
    salva(fig, "02-fluxograma.png")


fluxogramas()


# ---- 3. Folha de verificacao (matriz de marcas)
def folha_fig():
    from matplotlib.colors import ListedColormap
    M = np.array(MATRIZ)
    cm = ListedColormap(["#e4e7ea", "#d9534f", "#4cae6a"])
    fig, ax = plt.subplots(figsize=(21, 8.6))
    ax.imshow(M + 1, cmap=cm, aspect="auto", vmin=0, vmax=2, interpolation="nearest")
    ax.set_yticks(range(len(ROTULOS_LINHAS)))
    ax.set_yticklabels(ROTULOS_LINHAS, fontsize=10)
    rep = {"backend": "B", "frontend": "W", "app": "M"}
    ax.set_xticks(range(len(AMOSTRA)))
    ax.set_xticklabels([f"{rep[p['repo']]}{p['number']}" for p in AMOSTRA], rotation=90, fontsize=9)
    ax.set_xticks(np.arange(-.5, len(AMOSTRA), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(ROTULOS_LINHAS), 1), minor=True)
    ax.grid(which="minor", color="white", lw=1.2)
    ax.tick_params(which="minor", length=0)
    ax.axhline(7.5, color="black", lw=2.2)
    ax.spines[:].set_visible(False)
    for i, c in enumerate(CONT):
        ax.text(len(AMOSTRA) - 0.3, i, f"  ✔ {c['conformes']}   ✘ {c['nao_conformes']}   N/A {c['nao_aplicavel']}", va="center", fontsize=10)
    ax.set_title("Folha de verificação do DoD em {n} PRs mergeados (B = backend, W = web/frontend, M = mobile/app; ordem cronológica de abertura)".format(n=len(AMOSTRA)),
                 fontsize=12, loc="left")
    leg = [Rectangle((0, 0), 1, 1, fc="#4cae6a"), Rectangle((0, 0), 1, 1, fc="#d9534f"), Rectangle((0, 0), 1, 1, fc="#e4e7ea")]
    ax.legend(leg, ["conforme (marcado ou verificado)", "não conforme (aberto ou ausente)", "não se aplica / PR sem checklist"],
              loc="upper center", bbox_to_anchor=(0.45, -0.17), ncol=3, frameon=False, fontsize=10)
    ax.text(-0.01, 1.01, "", transform=ax.transAxes)
    salva(fig, "03-folha-verificacao.png")


folha_fig()


# ---- 4. Pareto
def pareto_ax(ax, itens, corte, titulo, ylabel, wrap=15):
    import textwrap
    n = [i["n"] for i in itens]
    cum = [i["acum"] for i in itens]
    cores = [AZUL if k < corte else "#a9b8c9" for k in range(len(itens))]
    ax.bar(range(len(itens)), n, color=cores, width=0.7)
    for k, v in enumerate(n):
        ax.text(k, v + max(n) * 0.015, str(int(v) if float(v).is_integer() else v), ha="center", fontsize=10, fontweight="bold")
    ax.set_xticks(range(len(itens)))
    ax.set_xticklabels([textwrap.fill(i["categoria"], wrap, break_long_words=False) for i in itens], fontsize=9)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, max(n) * 1.18)
    ax2 = ax.twinx()
    ax2.plot(range(len(itens)), cum, color=VERM, marker="o", lw=2)
    for k, v in enumerate(cum):
        ax2.text(k, v + 4.0, f"{fmt(v, 0)}%", ha="center", fontsize=9, color=VERM, bbox=dict(fc="white", ec="none", pad=0.8, alpha=0.85))
    ax2.axhline(80, color=CINZA, ls="--", lw=1.2)
    ax2.text(len(itens) - 0.5, 82, "80%", color=CINZA, fontsize=9, ha="right")
    ax2.set_ylim(0, 112)
    ax2.set_ylabel("% acumulado")
    ax2.spines["right"].set_visible(True)
    ax.set_title(titulo, loc="left")


def pareto_fig():
    fig, axs = plt.subplots(1, 2, figsize=(22, 7.6))
    pareto_ax(axs[0], PA, corteA + 1, f"(a) Defeitos corrigidos por categoria: frequência (n = {totA} commits fix)", "commits fix")
    pareto_ax(axs[1], PAp, cortePAp + 1, "(b) Os mesmos defeitos ponderados pela severidade presumida (pesos 1, 3, 5, 10)", "peso × quantidade")
    fig.tight_layout(w_pad=4)
    salva(fig, "04a-pareto-defeitos.png")
    fig, ax = plt.subplots(figsize=(15, 6.6))
    pareto_ax(ax, PB, corteB + 1, f"Não conformidades de processo nos {len(AMOSTRA)} PRs (marcas ✘ da folha de verificação, n = {totB})", "marcas ✘", wrap=17)
    fig.tight_layout()
    salva(fig, "04b-pareto-nao-conformidades.png")


pareto_fig()


# ---- 5. Histograma
def hist_fig():
    fig, axs = plt.subplots(1, 2, figsize=(18, 6.4))
    ax = axs[0]
    bins = np.arange(0, 5600, 500)
    ax.hist(tam, bins=bins, color=AZUL, edgecolor="white")
    h = R["hist"]["tamanho"]
    ax.axvline(h["media"], color=VERM, lw=2, ls="--", label=f"média = {fmt(h['media'], 0)}")
    ax.axvline(h["mediana"], color=VERDE, lw=2, label=f"mediana = {fmt(h['mediana'], 0)}")
    ax.axvline(400, color=AMAR, lw=2, ls=":", label="referência de revisão: 400 linhas")
    ax.set_xlabel("linhas alteradas por PR (adições + remoções, sem lockfiles)")
    ax.set_ylabel("nº de PRs")
    ax.set_title(f"(a) Tamanho dos PRs (n = {h['n']}; desvio-padrão = {fmt(h['dp'], 0)})", loc="left")
    ax.legend(frameon=False)
    ax = axs[1]
    h2 = R["hist"]["tempo_pr"]
    bins2 = np.logspace(np.log10(0.005), np.log10(600), 15)
    ax.hist(t_abre, bins=bins2, color=ROXO, edgecolor="white")
    ax.set_xscale("log")
    ax.axvline(h2["mediana"], color=VERDE, lw=2, label=f"mediana = {fmt(h2['mediana'] * 60, 0)} min")
    ax.axvline(h2["media"], color=VERM, lw=2, ls="--", label=f"média = {fmt(h2['media'], 1)} h")
    ax.axvline(24, color=AMAR, lw=2, ls=":", label="meta de revisão: 24 h")
    ax.set_xlabel("tempo do PR aberto até o merge (horas, escala log)")
    ax.set_ylabel("nº de PRs")
    ax.set_title(f"(b) Tempo de ciclo do PR (n = {h2['n']}; dp = {fmt(h2['dp'], 1)} h)", loc="left")
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout(w_pad=3)
    salva(fig, "05-histograma.png")


hist_fig()


# ---- 6. Graficos de controle
def p_fig():
    fig, ax = plt.subplots(figsize=(13, 6.6))
    ss = list(range(1, 9))
    p = [sp[s]["p"] * 100 for s in ss]
    ucl = [sp[s]["ucl"] * 100 for s in ss]
    lcl = [sp[s]["lcl"] * 100 for s in ss]
    ax.step(ss, ucl, where="mid", color=VERM, lw=1.8, ls="--", label="LSC (+3σ)")
    ax.step(ss, lcl, where="mid", color=VERM, lw=1.8, ls="--", label="LIC (−3σ)")
    ax.axhline(pbar * 100, color=VERDE, lw=2, label=f"linha central p̄ = {fmt(pbar * 100, 1)}%")
    ax.plot(ss[:7], p[:7], color=AZUL, lw=1.6, marker="o", ms=8)
    ax.plot(ss[6:], p[6:], color=AZUL, lw=1.2, ls=":")
    ax.plot([8], [p[7]], marker="o", ms=9, mfc="white", mec=AZUL, mew=2)
    for s in ss:
        d = sp[s]
        txt = f"{d['k']}/{d['n']}"
        ax.text(s, p[s - 1] + (-9 if d["sinal"] == "abaixo do LIC" else 4.5), txt, ha="center", fontsize=9.5)
        if d["sinal"] and s < 8:
            ax.plot([s], [p[s - 1]], marker="o", ms=13, mfc="none", mec=VERM, mew=2.4)
    ax.set_xticks(ss)
    ax.set_xticklabels([f"S{s}\n{SPRINTS[s][0]}–{SPRINTS[s][1]}" for s in ss])
    ax.set_ylim(-8, 112)
    ax.set_ylabel("% das issues da sprint concluídas em 18/11/2026")
    ax.set_title("Gráfico p: taxa de conclusão por sprint (limites calculados com S1–S7; S8 em curso)", loc="left")
    ax.legend(frameon=False, loc="lower left")
    fig.tight_layout()
    salva(fig, "06a-grafico-p-sprints.png")


def imr_fig():
    fig, axs = plt.subplots(2, 1, figsize=(13, 8), gridspec_kw=dict(height_ratios=[2, 1]), sharex=True)
    d = R["imr"]
    ax = axs[0]
    ax.plot(semanas[:14], X[:14], color=AZUL, marker="o", lw=1.6)
    ax.plot(semanas[13:], X[13:], color=AZUL, ls=":", lw=1.2)
    ax.plot([15], [X[14]], marker="o", mfc="white", mec=AZUL, mew=2, ms=9)
    ax.axhline(cl, color=VERDE, lw=2, label=f"média X̄ = {fmt(cl, 1)} commits/semana")
    ax.axhline(ucl_i, color=VERM, ls="--", lw=1.8, label=f"LSC = X̄ + 2,66·MR̄ = {fmt(ucl_i, 1)}")
    if lcl_i > 0:
        ax.axhline(lcl_i, color=VERM, ls="--", lw=1.8, label=f"LIC = {fmt(lcl_i, 1)}")
    else:
        ax.plot([], [], color=VERM, ls="--", label=f"LIC calculado = {fmt(lcl_i, 1)} (< 0: não se aplica)")
    for w, x in zip(semanas, X):
        ax.text(w, x + max(X) * 0.03, str(int(x)), ha="center", fontsize=9)
        if w <= 14 and x > ucl_i:
            ax.plot([w], [x], marker="o", ms=14, mfc="none", mec=VERM, mew=2.4)
    ax.set_ylabel("commits por semana\n(4 repositórios, sem merges)")
    ax.set_title("Gráfico I-MR: ritmo semanal de commits (limites com semanas 1–14; semana 15 parcial = ○)", loc="left")
    ax.legend(frameon=True, facecolor="white", edgecolor="none", loc="upper center", bbox_to_anchor=(0.33, 0.93))
    ax = axs[1]
    ax.plot(semanas[1:14], mr, color=ROXO, marker="o", lw=1.6)
    ax.axhline(mrbar, color=VERDE, lw=2, label=f"MR̄ = {fmt(mrbar, 1)}")
    ax.axhline(ucl_mr, color=VERM, ls="--", lw=1.8, label=f"LSC(MR) = 3,267·MR̄ = {fmt(ucl_mr, 1)}")
    for w, m in zip(semanas[1:14], mr):
        ax.text(w, m + max(mr) * 0.04, str(int(m)), ha="center", fontsize=9)
        if m > ucl_mr:
            ax.plot([w], [m], marker="o", ms=14, mfc="none", mec=VERM, mew=2.4)
    ax.set_ylabel("amplitude móvel |Xᵢ − Xᵢ₋₁|")
    ax.set_xlabel("semana do projeto (1 = 10/08; 15 = 16/11)")
    ax.set_xticks(semanas)
    ax.legend(frameon=True, facecolor="white", edgecolor="none", loc="upper center", bbox_to_anchor=(0.33, 0.95))
    fig.tight_layout()
    salva(fig, "06b-grafico-imr-commits.png")


p_fig()
imr_fig()


# ---- 7. Dispersao
def reta(ax, x, y, rg, logx=False, logy=False, cor=VERM):
    xs = np.linspace(x.min(), x.max(), 100)
    ys = rg["a"] + rg["b"] * xs
    ax.plot(xs if not logx else 10 ** xs, ys if not logy else 10 ** ys - 0.01, color=cor, lw=2)


def disp_fig():
    fig, axs = plt.subplots(1, 3, figsize=(21, 6.4))
    ax = axs[0]
    ax.scatter(tam, t_abre, s=52, color=AZUL, alpha=0.8, edgecolor="white")
    ax.set_xscale("log")
    ax.set_yscale("log")
    xs = np.linspace(np.log10(tam.min()), np.log10(tam.max()), 100)
    ax.plot(10 ** xs, 10 ** (rg1["a"] + rg1["b"] * xs) - 0.01, color=VERM, lw=2)
    ax.set_xlabel("tamanho do PR (linhas alteradas, escala log)")
    ax.set_ylabel("PR aberto até merge (h, escala log)")
    ax.set_title("(a) Tamanho do PR × tempo até o merge", loc="left")
    ax.text(0.03, 0.97, f"n = {rg1['n']}\nr (log-log) = {fmt(rg1['r'], 2)}\nR² = {fmt(rg1['r2'], 2)}\nρ Spearman = {fmt(rg1['spearman'], 2)}\np = {fmt(rg1['p'], 2)}",
            transform=ax.transAxes, va="top", fontsize=10, bbox=dict(fc="white", ec=CINZA))
    ax = axs[1]
    esc = np.array(ESCORE)[ok] * 100
    ax.scatter(tam[ok], esc + np.random.default_rng(1).uniform(-1.2, 1.2, ok.sum()), s=52, color=ROXO, alpha=0.8, edgecolor="white")
    xs = np.linspace(tam[ok].min(), tam[ok].max(), 100)
    ax.plot(xs, rg2["a"] + rg2["b"] * xs, color=VERM, lw=2)
    ax.set_xlabel("tamanho do PR (linhas alteradas)")
    ax.set_ylabel("% dos itens de DoD marcados no PR")
    ax.set_title("(b) Tamanho do PR × conformidade declarada com o DoD", loc="left")
    ax.text(0.97, 0.05, f"n = {rg2['n']}\nr = {fmt(rg2['r'], 2)}   R² = {fmt(rg2['r2'], 2)}\nρ Spearman = {fmt(rg2['spearman'], 2)}\np = {fmt(rg2['p'], 2)}",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=10, bbox=dict(fc="white", ec=CINZA))
    ax = axs[2]
    ax.scatter(planej, concl, s=90, color=AZUL, edgecolor="white", zorder=3)
    for s in range(1, 8):
        ax.annotate(f"S{s}", (planej[s - 1], concl[s - 1]), textcoords="offset points", xytext=(7, 5), fontsize=10)
    xs = np.linspace(planej.min(), planej.max(), 50)
    ax.plot(xs, rg3["a"] + rg3["b"] * xs, color=VERM, lw=2)
    ax.set_xlabel("issues planejadas na sprint")
    ax.set_ylabel("issues concluídas até 18/11")
    ax.set_title("(c) Issues planejadas × concluídas (S1–S7)", loc="left")
    ax.text(0.03, 0.97, f"n = {rg3['n']}\nr = {fmt(rg3['r'], 2)}   R² = {fmt(rg3['r2'], 2)}\nρ Spearman = {fmt(rg3['spearman'], 2)}\np = {fmt(rg3['p'], 2)}\ny = {fmt(rg3['a'], 2)} + {fmt(rg3['b'], 2)}·x",
            transform=ax.transAxes, va="top", fontsize=10, bbox=dict(fc="white", ec=CINZA))
    fig.tight_layout(w_pad=3)
    salva(fig, "07-dispersao.png")


disp_fig()

(DADOS / "resultados.json").write_text(json.dumps(R, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
print("ok: figuras e resultados.json gerados")
