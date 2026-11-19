#!/usr/bin/env python3
"""Leitura dos artefatos .md do FieldOps (somente leitura) para alimentar tabelas, apendices e conferencias."""
import re
from pathlib import Path

ENT = Path("/Users/felipersas/Documents/Facul/gestao-proj/entrega")
F = {
    "tap": ENT / "aula-02-integracao/tap-fieldops.md",
    "eap": ENT / "aula-03-escopo/eap-fieldops.md",
    "crono": ENT / "aula-04-tempo/cronograma-fieldops.md",
    "orc": ENT / "aula-05-custos-qualidade/orcamento-fieldops.md",
    "qual": ENT / "aula-05-custos-qualidade/qualidade-7-ferramentas-fieldops.md",
    "raci": ENT / "aula-06-rh-comunicacoes/organograma-raci-fieldops.md",
    "com": ENT / "aula-06-rh-comunicacoes/plano-comunicacao-fieldops.md",
    "risco": ENT / "aula-07-riscos/analise-riscos-fieldops.md",
    "aq": ENT / "aula-08-aquisicoes-partes-interessadas/aquisicoes-fieldops.md",
    "pi": ENT / "aula-08-aquisicoes-partes-interessadas/matriz-poder-interesse-fieldops.md",
}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⬀-⯿️‍]")


def limpa(s):
    s = EMOJI.sub("", s)
    s = s.replace("**", "").replace("*", "") if False else s
    return re.sub(r"\s+", " ", s).strip()


def md_tabelas(chave, ancora, n=0):
    """retorna a n-esima tabela apos a linha que contem 'ancora'. Linhas como listas de celulas (texto cru)."""
    linhas = F[chave].read_text(encoding="utf8").splitlines()
    i0 = next(i for i, l in enumerate(linhas) if ancora in l)
    achadas = []
    i = i0
    while i < len(linhas):
        if linhas[i].startswith("|") and i + 1 < len(linhas) and re.match(r"^\|[\s:|-]+\|$", linhas[i + 1]):
            j = i
            blk = []
            while j < len(linhas) and linhas[j].startswith("|"):
                blk.append(linhas[j])
                j += 1
            achadas.append(blk)
            i = j
        else:
            i += 1
        if len(achadas) > n:
            break
    blk = achadas[n]
    rows = []
    for l in blk:
        cel = [c.strip() for c in l.strip().strip("|").split("|")]
        rows.append(cel)
    cab, corpo = rows[0], rows[2:]
    return cab, corpo


def sem_md(s):
    s = s.replace("**", "")
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = s.replace("<br>", "\n")
    return limpa_linhas(s)


def limpa_linhas(s):
    return "\n".join(limpa(p) for p in s.split("\n")).strip()


def num(s):
    """'R$ 1.234,56' -> float"""
    s = s.replace("R$", "").replace("**", "").replace(" ", "").replace(" ", "")
    s = s.replace(".", "").replace(",", ".")
    return float(s)


def brl(x, casas=2):
    return ("R$ " + f"{x:,.{casas}f}").replace(",", "X").replace(".", ",").replace("X", ".")


def brn(x, casas=2):
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------------------------------------------------------- cronograma
def cronograma():
    cab, rows = md_tabelas("crono", "## 📋 Lista de Atividades")
    out = []
    for r in rows:
        r = [sem_md(c) for c in r]
        id_, wbs, nome, ini, fim, dur, resp, pred, esf, sprint, status = r
        nome = nome.replace("🔺", "").strip()
        marco = id_.startswith("M")
        out.append(dict(id=id_, wbs=wbs, nome=re.sub(r"^Marco ", "Marco ", nome), ini=ini, fim=fim, dur=dur, resp=resp, pred=pred,
                        esf=0 if esf in ("—", "") else int(esf), sprint=sprint, status=status, marco=marco,
                        critica=("🔺" in r[2] or "🔺" in rows[len(out)][2])))
    return out


# ---------------------------------------------------------------- orcamento
def orcamento():
    cab, rows = md_tabelas("orc", "### Estimativa de três pontos por item")
    out = []
    for r in rows:
        r = [sem_md(c) for c in r]
        if not r[0].startswith("O"):
            continue
        id_, wbs, item, cat, qtd, un, resp, co, cm, cp, pert, sig = r
        out.append(dict(id=id_, wbs=wbs, item=item, cat=cat, qtd=qtd, un=un, resp=resp, co=num(co) if co != "—" else None,
                        cm=num(cm), cp=num(cp) if cp != "—" else None, pert=num(pert), sig=num(sig) if sig != "—" else None))
    return out


def orcamento_total_linha():
    cab, rows = md_tabelas("orc", "### Estimativa de três pontos por item")
    return rows[-1]


# ---------------------------------------------------------------- RACI
def raci():
    cab, rows = md_tabelas("raci", "### 3.3 Matriz")
    out = []
    for r in rows:
        r = [sem_md(c) for c in r]
        if re.match(r"^\d\.\d$", r[0]):
            out.append(dict(cod=r[0], nome=r[1], papeis=dict(zip(["FM", "JV", "GR", "PD", "AF", "PI-01", "PI-02", "PI-03"], r[2:10])), crit=r[10]))
    return out


# ---------------------------------------------------------------- riscos
def riscos_registro():
    cab, rows = md_tabelas("risco", "## 3. Registro de riscos")
    out = []
    for r in rows:
        id_ = r[0]
        txt = r[1]
        m = re.match(r"\*\*Causa:\*\*(.*?)<br>\*\*Risco:\*\*(.*?)<br>\*\*Consequência:\*\*(.*)", txt, re.S)
        causa, risco, cons = [x.strip() for x in m.groups()]
        out.append(dict(id=id_, causa=causa, risco=risco, cons=cons, tipo=r[2].split("<br>")[0], rbs=r[2].split("<br>")[-1], eap=r[3], gatilho=r[4], incl=r[5], status=r[6]))
    return out


def riscos_quali():
    cab, rows = md_tabelas("risco", "## 4. Análise qualitativa")
    out = []
    for r in rows:
        r = [sem_md(c) for c in r]
        out.append(dict(id=r[0], nome=r[1], tipo=r[2], p=float(r[3].replace(",", ".")), custo=r[4], prazo=r[5], esc=r[6], qual=r[7],
                        media=float(r[8].replace(",", ".")), maxi=r[9], sev=float(r[10].replace(",", ".")), sevmax=r[11], prio=int(r[12]), classe=r[13], obs=r[14]))
    return out


def riscos_resp():
    cab, rows = md_tabelas("risco", "### 5.1 Respostas às ameaças")
    out = {}
    for r in rows:
        r = [sem_md(c) for c in r]
        out[r[0]] = dict(abord=r[4], resp=r[5], dono=r[6], incl=r[3])
    cab, rows = md_tabelas("risco", "### 5.2 Detalhamento")
    for r in rows:
        r = [sem_md(c) for c in r]
        out[r[0]].update(contingencia=r[1], prazo=r[2], custo=r[3], residual=r[4], secund=r[5])
    return out


def oportunidades():
    cab, rows = md_tabelas("risco", "### 5.3 Oportunidades")
    out = []
    for r in rows:
        r = [sem_md(c) for c in r]
        if r[0].startswith("O0") and len(r) >= 11:
            out.append(r)
    return out


# ---------------------------------------------------------------- aquisicoes / comunicacoes
def aquisicoes():
    cab, rows = md_tabelas("aq", "## 📋 Tabela de aquisições")
    out = []
    for r in rows:
        r = [sem_md(c) for c in r]
        if r[0].startswith("P"):
            out.append(r)
    return out


def comunicacoes():
    cab, rows = md_tabelas("com", "## 2. Plano de comunicação")
    cab2, rows2 = md_tabelas("com", "## 3. Momento de realização")
    mom = {r[0]: (sem_md(r[1]), sem_md(r[2]), sem_md(r[3])) for r in rows2}
    out = []
    for r in rows:
        r = [sem_md(c) for c in r]
        out.append(dict(id=r[0], desc=r[1], freq=r[2], canal=r[3], publico=r[4], dono=r[5], mom=mom[r[0]]))
    return out


def gatilhos():
    cab, rows = md_tabelas("com", "## 7. Gatilhos de escalonamento")
    return [[sem_md(c) for c in r] for r in rows]


def partes():
    cab, rows = md_tabelas("pi", "## 3. Classificação das 13 partes interessadas")
    cab2, rows2 = md_tabelas("pi", "### 4.1 Nível de engajamento")
    eng = {r[0]: [sem_md(c) for c in r] for r in rows2}
    out = []
    for r in rows:
        r = [sem_md(c) for c in r]
        e = eng[r[0]]
        out.append(dict(id=r[0], nome=r[1], poder=int(r[2]), just_p=r[3], inter=int(r[4]), just_i=r[5], quad=r[6],
                        atual=e[2], desej=e[3], lacuna=int(e[4]), interesses=e[5], expect=e[6]))
    return out


def sprints_status():
    cab, rows = md_tabelas("crono", "### Planejado × Realizado por sprint")
    return [[sem_md(c) for c in r] for r in rows]


if __name__ == "__main__":
    c = cronograma(); print("cronograma", len(c), sum(x["esf"] for x in c), len([x for x in c if x["marco"]]))
    o = orcamento(); print("orcamento", len(o), round(sum(x["pert"] for x in o), 2))
    r = raci(); print("raci", len(r))
    rr = riscos_registro(); print("riscos", len(rr)); print(rr[0])
    q = riscos_quali(); print("quali", len(q))
    rs = riscos_resp(); print("resp", len(rs), rs["R06"])
    print("oport", len(oportunidades()))
    print("aq", len(aquisicoes()))
    cm = comunicacoes(); print("com", len(cm))
    print("gat", len(gatilhos()))
    p = partes(); print("partes", len(p), p[0])
    print(sprints_status()[0])
    print(c[0]); print(c[8])


def realizado_atividades():
    cab, rows = md_tabelas("crono", "### Comparação por atividade")
    out = {}
    for r in rows:
        r = [sem_md(c) for c in r]
        if r[0].startswith("A"):
            out[r[0]] = int(r[4].replace("%", ""))
    return out


SHORT = {
    "1.1": "Termo de Abertura e Escopo", "1.2": "Plano de Gerenciamento", "1.3": "Relatórios e demos M1–M8", "1.4": "Encerramento",
    "2.1": "Repositórios e convenções", "2.2": "Contrato OpenAPI", "2.3": "Integração contínua (CI)", "2.4": "Ambiente padronizado",
    "3.1": "Identidade e acesso", "3.2": "Cadastros operacionais", "3.3": "Modelos versionados", "3.4": "Planejamento e atribuição",
    "3.5": "Execução e evidências", "3.6": "Sincronização idempotente", "3.7": "Revisão e auditoria",
    "4.1": "Shell e autenticação", "4.2": "Usuários e cadastros", "4.3": "Construtor de modelos", "4.4": "Agendamento e acompanhamento",
    "4.5": "Evidências e não conformidades", "4.6": "Revisão e histórico",
    "5.1": "Base do app", "5.2": "Login e sessão", "5.3": "Lista e detalhes", "5.4": "Checklist dinâmico", "5.5": "Recursos nativos",
    "5.6": "Offline e outbox", "5.7": "Sincronização e correção",
    "6.1": "Plano de testes", "6.2": "Testes automatizados", "6.3": "Integração e Android", "6.4": "Acessibilidade e correções",
    "7.1": "Dados de demonstração", "7.2": "Build e publicação", "7.3": "Documentação final", "7.4": "Demo ponta a ponta",
}
ENTREGAS = {"1": "Gerenciamento do Projeto", "2": "Fundação Técnica", "3": "API REST Central (Backend)", "4": "Interface Administrativa Web",
            "5": "Aplicativo Mobile (Android)", "6": "Qualidade e Testes", "7": "Entrega e Release (M8)"}


def eap_nomes():
    """nomes oficiais dos 36 pacotes (do dicionario da EAP)."""
    cab, rows = md_tabelas("eap", "## Dicionário da EAP")
    out = {}
    for r in rows:
        r = [sem_md(c) for c in r]
        if re.match(r"^\d\.[1-9]$", r[0]):
            out[r[0]] = dict(nome=r[1], desc=r[2], req=r[3], pbi=r[4], criterio=r[5])
    return out


def eap_entregas():
    cab, rows = md_tabelas("eap", "## Dicionário da EAP")
    out = {}
    for r in rows:
        r = [sem_md(c) for c in r]
        if re.match(r"^\d\.0$", r[0]):
            out[r[0][0]] = dict(nome=r[1], desc=r[2], req=r[3], pbi=r[4], criterio=r[5])
    return out


def curva_s():
    cab, rows = md_tabelas("orc", "## 📈 (e) Distribuição por sprint")
    return [[sem_md(c) for c in r] for r in rows]


def engaj_acoes():
    cab, rows = md_tabelas("pi", "### 4.3 Riscos de relacionamento")
    out = {}
    for r in rows:
        r = [sem_md(c) for c in r]
        out[r[0].split(" ")[0]] = dict(risco=r[1], acoes=r[2], resp=r[3])
    return out


def marcos_md():
    cab, rows = md_tabelas("crono", "## 🚩 Marcos do Projeto")
    return [[sem_md(c) for c in r] for r in rows]


def caminho_critico():
    cab, rows = md_tabelas("crono", "## 🔺 Caminho crítico")
    return [[sem_md(c) for c in r] for r in rows]


def evm_tabela():
    cab, rows = md_tabelas("orc", "### Situação em 18/11/2026")
    return [[sem_md(c) for c in r] for r in rows]


def alcadas():
    cab, rows = md_tabelas("orc", "### Como os desvios são tratados")
    return [[sem_md(c) for c in r] for r in rows]


def cortes():
    cab, rows = md_tabelas("crono", "### Ordem de corte aplicada")
    cab2, rows2 = md_tabelas("crono", "### Ordem de corte aplicada", 1)
    return [[sem_md(c) for c in r] for r in rows], [[sem_md(c) for c in r] for r in rows2]


def atrasos_acoes():
    cab, rows = md_tabelas("crono", "### Atrasos identificados e ações")
    return [[sem_md(c) for c in r] for r in rows]


def eap_req_matriz():
    cab, rows = md_tabelas("eap", "## Matriz de rastreabilidade: requisito para pacote")
    return [[sem_md(c) for c in r] for r in rows]


def carga_sprint():
    cab, rows = md_tabelas("crono", "### Carga por sprint")
    return [[sem_md(c) for c in r] for r in rows]


def capacidade():
    cab, rows = md_tabelas("crono", "### Capacidade restante")
    return [[sem_md(c) for c in r] for r in rows]


def verificacoes_crono():
    cab, rows = md_tabelas("crono", "## 🔍 Verificações automáticas")
    return [[sem_md(c) for c in r] for r in rows]


def tabela_generica(chave, ancora, n=0):
    cab, rows = md_tabelas(chave, ancora, n)
    return [sem_md(c) for c in cab], [[sem_md(c) for c in r] for r in rows]
