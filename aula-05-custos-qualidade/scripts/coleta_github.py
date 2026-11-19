#!/usr/bin/env python3
"""Coleta dados reais do GitHub (org FieldOps-Project) e grava CSVs em ../dados/.

Requisitos: `gh` autenticado com acesso de leitura aos repositorios backend,
frontend, app e docs. Python 3.9+ (somente biblioteca padrao).

Uso:  python3 coleta_github.py [issues|prs|commits|runs]
Saida: dados/issues.csv, prs.csv, commits.csv, ci_runs.csv, coleta_meta.json

Os logins do GitHub sao convertidos nas siglas do projeto (FM, JV, GR, PD, AF)
e os agentes automaticos ficam como BOT. Nenhum token e gravado.
"""
import csv
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ORG = "FieldOps-Project"
REPOS = ["backend", "frontend", "app", "docs"]
DADOS = Path(__file__).resolve().parent.parent / "dados"
DADOS.mkdir(exist_ok=True)

# Mapeamento login -> sigla (premissa: ver base do projeto, secao 3).
SIGLAS = {
    "felipersas": "FM",
    "joaovictor015qzn": "JV",
    "joao victor de souza  santos": "JV",  # mesma pessoa, identidade de commit diferente (premissa)
    "gabrrkl7": "GR",
    "pedrodias010": "PD",
    "andrefernandes9010": "AF",
}
LOCKFILES = ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb", "bun.lock")


def sigla(login):
    if not login:
        return "?"
    k = login.strip().lower()
    if k in SIGLAS:
        return SIGLAS[k]
    if "copilot" in k or k.startswith("app/") or "bot" in k or "codex" in k:
        return "BOT"
    return "OUTRO"


def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if r.returncode != 0:
        print("gh falhou:", args, r.stderr[:200], file=sys.stderr)
        return None
    return r.stdout


def gh_json(*args):
    out = gh(*args)
    return json.loads(out) if out else None


def api_paginate(path):
    out = gh("api", path, "--paginate")
    if not out:
        return []
    return json.loads(out.replace("][", ","))


def tipo_titulo(t):
    m = re.match(r"^(\w+)(\([^)]*\))?!?:", t)
    return m.group(1).lower() if m else "outro"


def label_val(labels, prefix):
    for n in labels:
        if n.startswith(prefix):
            return n.split(":", 1)[1] if ":" in n else n
    return ""


def coleta_issues():
    rows = []
    for r in REPOS:
        data = gh_json("issue", "list", "-R", f"{ORG}/{r}", "--state", "all", "--limit", "300",
                       "--json", "number,title,state,createdAt,closedAt,labels,milestone,assignees,body")
        for i in data:
            labels = [l["name"] for l in i["labels"]]
            ms = i["milestone"]["title"] if i["milestone"] else ""
            m = re.match(r"Sprint (\d)", ms)
            body = i["body"] or ""
            # Separa a lista de criterios de aceitacao da lista de DoD (secoes do card).
            partes = re.split(r"\n## ", body)
            ac = [p for p in partes if p.lower().startswith("criterios de aceitacao")]
            dod = [p for p in partes if p.lower().startswith("definition of done")]
            def conta(txt, marcado):
                pat = r"- \[x\]" if marcado else r"- \[ \]"
                return sum(len(re.findall(pat, t, re.I)) for t in txt)
            rows.append(dict(
                repo=r, number=i["number"], title=i["title"], state=i["state"],
                milestone=ms, sprint=int(m.group(1)) if m else "",
                created=i["createdAt"], closed=i["closedAt"] or "",
                assignees=";".join(sorted({sigla(a["login"]) for a in i["assignees"]})),
                n_assignees=len(i["assignees"]),
                prio=next((n for n in labels if n in ("P0", "P1", "P2")), ""),
                epico=next((n for n in labels if re.fullmatch(r"EP-\d\d", n)), ""),
                tipo=label_val(labels, "tipo:"), area=label_val(labels, "area:"),
                ac_marcados=conta(ac, True), ac_total=conta(ac, True) + conta(ac, False),
                dod_marcados=conta(dod, True), dod_total=conta(dod, True) + conta(dod, False),
            ))
    return rows


def refs_issue(pr, repo):
    """Numeros de issue DO MESMO REPOSITORIO citados no PR (Closes #N, issue #N, card #N, (#N) no titulo)."""
    txt = (pr.get("body") or "")
    refs = set()
    for m in re.finditer(r"(?i)\b(?:closes|fixes|resolves|issue|issues|card|refs?)\s*:?\s*(?:([\w.-]+/[\w.-]+))?#(\d+)", txt):
        qual = m.group(1)
        if qual is None or qual.lower() == f"{ORG}/{repo}".lower():
            refs.add(int(m.group(2)))
    for m in re.finditer(r"\(#(\d+)\)", pr["title"]):
        refs.add(int(m.group(1)))
    return sorted(refs)


DOD_ITENS = [  # (chave, trecho que identifica a linha no checklist do template de PR)
    ("dod1_branch_pr", "código no repositório"),
    ("dod2_lint_tipos", "lint e verifica"),
    ("dod3_sem_segredos", "sem segredos"),
    ("dod4_sem_logs", "sem logs"),
    ("dod5_erros", "comportamento de erro"),
    ("dod6_docs", "documenta"),
    ("dod7_evidencia", "evidência de funcionamento"),
    ("dod8_revisao", "conteúdo revisado"),
]


def dod_marcas(body):
    """Estado de cada item do checklist de DoD do template: x (marcado), o (aberto), - (ausente)."""
    res = {k: "-" for k, _ in DOD_ITENS}
    for linha in (body or "").splitlines():
        m = re.match(r"\s*- \[( |x|X)\]\s*(.*)", linha)
        if not m:
            continue
        txt = m.group(2).lower().replace("evidencia", "evidência")
        for k, trecho in DOD_ITENS:
            if txt.startswith(trecho):
                res[k] = "x" if m.group(1).lower() == "x" else "o"
    return res


def coleta_prs():
    rows = []
    for r in REPOS:
        data = gh_json("pr", "list", "-R", f"{ORG}/{r}", "--state", "all", "--limit", "300",
                       "--json", "number,title,state,createdAt,mergedAt,closedAt,additions,deletions,"
                                 "changedFiles,author,headRefName,baseRefName,body,reviewDecision")
        for p in data:
            d = gh_json("pr", "view", str(p["number"]), "-R", f"{ORG}/{r}",
                        "--json", "reviews,comments,statusCheckRollup,commits,files") or {}
            rc = api_paginate(f"repos/{ORG}/{r}/pulls/{p['number']}/comments")
            autor = sigla(p["author"]["login"])
            files = d.get("files", [])
            add_x = sum(f["additions"] for f in files if not f["path"].endswith(LOCKFILES))
            del_x = sum(f["deletions"] for f in files if not f["path"].endswith(LOCKFILES))
            testes = [f for f in files if re.search(r"(\.test\.|\.spec\.|__tests__|/test/|/tests/|Test\.java)", f["path"])]
            docs = [f for f in files if re.search(r"(README|\.md$|openapi|/adr/|/docs/)", f["path"], re.I)]
            revs = d.get("reviews", [])
            nao_autor = [x for x in revs if sigla(x["author"]["login"]) != autor]
            checks = d.get("statusCheckRollup", [])
            concl = {c.get("conclusion") or c.get("state") for c in checks}
            if not checks:
                ci = "NENHUM"
            elif concl <= {"SUCCESS", "NEUTRAL", "SKIPPED"}:
                ci = "SUCCESS"
            else:
                ci = "FAILURE" if "FAILURE" in concl else "OUTRO"
            commits = d.get("commits", [])
            datas = sorted(c["authoredDate"] for c in commits) or [p["createdAt"]]
            body = p["body"] or ""
            rows.append(dict(
                repo=r, number=p["number"], title=p["title"], state=p["state"], autor=autor,
                head=p["headRefName"], base=p["baseRefName"], tipo_titulo=tipo_titulo(p["title"]),
                created=p["createdAt"], merged=p["mergedAt"] or "", closed=p["closedAt"] or "",
                first_commit=datas[0], last_commit=datas[-1], n_commits=len(commits),
                additions=p["additions"], deletions=p["deletions"],
                additions_sem_lock=add_x, deletions_sem_lock=del_x,
                changed_files=p["changedFiles"], n_arquivos_teste=len(testes), n_arquivos_doc=len(docs),
                n_reviews=len(revs), n_reviews_outra_pessoa=len(nao_autor),
                aprovado_por_outra_pessoa=int(any(x["state"] == "APPROVED" for x in nao_autor)),
                pediu_mudancas=int(any(x["state"] == "CHANGES_REQUESTED" for x in revs)),
                n_comentarios=len(d.get("comments", [])), n_comentarios_codigo=len(rc),
                ci=ci, body_len=len(body), body_secoes=len(re.findall(r"(?m)^#{2,3} ", body)),
                body_tem_checklist=int("- [" in body), issue_refs=";".join(map(str, refs_issue(p, r))),
                **dod_marcas(body),
            ))
    return rows


def coleta_commits():
    rows, vistos = [], set()
    for r in REPOS:
        branches = api_paginate(f"repos/{ORG}/{r}/branches")
        for b in branches:
            for c in api_paginate(f"repos/{ORG}/{r}/commits?sha={b['name']}&per_page=100"):
                if (r, c["sha"]) in vistos:
                    continue
                vistos.add((r, c["sha"]))
                msg = c["commit"]["message"].split("\n")[0]
                login = (c.get("author") or {}).get("login") or c["commit"]["author"]["name"]
                rows.append(dict(
                    repo=r, sha=c["sha"][:7], date=c["commit"]["author"]["date"], autor=sigla(login),
                    tipo=tipo_titulo(msg) if re.match(r"^\w+(\([^)]*\))?!?:", msg) else
                    ("merge" if msg.lower().startswith("merge") else "outro"),
                    merge=int(len(c["parents"]) > 1), msg=msg))
    return rows


def coleta_runs():
    rows = []
    for r in REPOS:
        runs = gh_json("run", "list", "-R", f"{ORG}/{r}", "--limit", "300",
                       "--json", "databaseId,workflowName,conclusion,createdAt,headBranch,event") or []
        for x in runs:
            passo = ""
            if x["conclusion"] == "failure":
                j = gh_json("run", "view", str(x["databaseId"]), "-R", f"{ORG}/{r}", "--json", "jobs") or {}
                passo = ";".join(s["name"] for job in j.get("jobs", []) for s in job["steps"] if s["conclusion"] == "failure")
            rows.append(dict(repo=r, run_id=x["databaseId"], workflow=x["workflowName"], conclusion=x["conclusion"],
                             created=x["createdAt"], branch=x["headBranch"], event=x["event"], passo_falho=passo))
    return rows


def grava(nome, rows):
    if not rows:
        return
    with open(DADOS / nome, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(nome, len(rows), "linhas")


if __name__ == "__main__":
    # Uso: python3 coleta_github.py [issues] [prs] [commits] [runs]  (sem argumentos: tudo)
    alvo = set(sys.argv[1:]) or {"issues", "prs", "commits", "runs"}
    if "issues" in alvo:
        grava("issues.csv", coleta_issues())
    if "prs" in alvo:
        grava("prs.csv", coleta_prs())
    if "commits" in alvo:
        grava("commits.csv", coleta_commits())
    if "runs" in alvo:
        grava("ci_runs.csv", coleta_runs())
    (DADOS / "coleta_meta.json").write_text(json.dumps(
        {"coletado_em_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "org": ORG, "repos": REPOS},
        indent=2), encoding="utf-8")
