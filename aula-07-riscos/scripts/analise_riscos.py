#!/usr/bin/env python3
"""Gera a analise de riscos do FieldOps: ../analise-riscos-fieldops.md, ../matriz-calor.png e ../dados/riscos.csv.

Todas as contas (niveis de impacto, severidade, ranking, EMV, reserva, Monte Carlo) saem de riscos_calculo.py a partir
de riscos_dados.py. Para alterar uma probabilidade ou um impacto, edite riscos_dados.py e rode de novo.
Uso: python3 analise_riscos.py   (requer numpy e matplotlib)
"""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from riscos_calculo import (AM, OP, CUSTO_BASE, RESERVA_10, RESERVA_5, DIAS_UTEIS, ESCALA_P, NIVEIS, LIM_ALTA, LIM_MEDIA,
                            LIM_OBS_MAX, TAXA_DEV, TAXA_GP, LINHA_BASE, ORCAMENTO_TOTAL, nivel_posicao, classe, monte_carlo)

BASE = Path(__file__).resolve().parent.parent
(BASE / "dados").mkdir(exist_ok=True)


def fmt(x, nd=0):
    s = f"{x:,.{nd}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def rs(x, nd=0):
    return "R$ " + fmt(x, nd)


def pct(x, nd=0):
    return fmt(100 * x, nd) + "%"


def nv(x):
    return fmt(x, 2)  # nivel de impacto: 0,05 / 0,10 ...


def tabela(cab, linhas, alinh=None):
    alinh = alinh or ["---"] * len(cab)
    s = "| " + " | ".join(cab) + " |\n| " + " | ".join(alinh) + " |\n"
    for l in linhas:
        s += "| " + " | ".join(str(c) for c in l) + " |\n"
    return s


POR_RANK = sorted(AM, key=lambda d: d["rank"])
POR_ID = {d["id"]: d for d in AM + OP}
ativos = [d for d in AM if not d["mat"]]
mats = [d for d in AM if d["mat"]]

# ------------------------------------------------------------------ csv
campos = ["id", "nome", "tipo", "rbs", "eap", "causa", "risco", "conseq", "p", "c", "t", "esc", "qual", "media", "max", "sev", "sev_max",
          "classe", "rank", "gatilho", "incl", "status", "mat", "custo_rs", "emv_rs", "dias", "emv_dias", "estrat", "prev", "cont", "resp",
          "prazo", "resp_rs", "p_res", "sev_res", "classe_res", "sec"]
with open(BASE / "dados" / "riscos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
    w.writeheader()
    for d in POR_RANK + OP:
        w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items() if k in campos})

# ------------------------------------------------------------------ matriz de calor (PNG)
POSICAO = {}
for d in AM:
    POSICAO.setdefault((d["p"], nivel_posicao(d["media"])), []).append(d["id"])
POSICAO_OP = {}
for d in OP:
    POSICAO_OP.setdefault((d["p"], nivel_posicao(d["media"])), []).append(d["id"])
PS = [0.9, 0.7, 0.5, 0.3, 0.1]


def heatmap():
    """Mapa de calor com posicoes exatas: linhas = probabilidade; eixo x = impacto medio; fundo = limiares de severidade."""
    fig, ax = plt.subplots(figsize=(13, 8.4))
    cores = {"Alta": "#e7a09a", "Média": "#f4d58d", "Baixa": "#b9dcc0"}
    XMIN, XMAX = 0.04, 0.44
    for i, p in enumerate(PS):
        t_media, t_alta = LIM_MEDIA / p, LIM_ALTA / p
        faixas = [(XMIN, min(t_media, XMAX), "Baixa"), (t_media, min(t_alta, XMAX), "Média"), (t_alta, XMAX, "Alta")]
        for x0, x1, c in faixas:
            if x1 > x0 and x0 < XMAX:
                ax.add_patch(Rectangle((max(x0, XMIN), i), x1 - max(x0, XMIN), 1, fc=cores[c], ec="none"))
        ax.axhline(i, color="white", lw=3)
    ax.axhline(5, color="white", lw=3)
    for n in NIVEIS:
        if n <= XMAX:
            ax.axvline(n, color="#777", lw=1, ls=":")
    pontos = {}
    for d in AM:
        pontos.setdefault(d["p"], []).append(d)
    for i, p in enumerate(PS):
        for k, d in enumerate(sorted(pontos.get(p, []), key=lambda x: (x["media"], x["id"]))):
            lane = [0.2, 0.5, 0.8][k % 3]
            ax.plot([d["media"]], [i + lane], "o", color="#222", ms=7)
            ax.text(d["media"] + 0.004, i + lane, d["id"], va="center", ha="left", fontsize=11.5, fontweight="bold", color="#1a1a1a")
    ops = {}
    for d in OP:
        ops.setdefault(d["p"], []).append(d)
    for i, p in enumerate(PS):
        for k, d in enumerate(sorted(ops.get(p, []), key=lambda x: x["media"])):
            y = i + 0.93 - 0.09 * k
            ax.plot([d["media"]], [y], "D", color="#1f4e79", ms=6)
            ax.text(d["media"] + 0.004, y, d["id"], va="center", ha="left", fontsize=10, fontweight="bold", color="#1f4e79")
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(0, 5)
    ax.set_xticks([n for n in NIVEIS if n <= XMAX] + [0.30])
    ax.set_xticklabels([nv(n) for n in NIVEIS if n <= XMAX] + ["0,30"], fontsize=10.5)
    ax.set_yticks([i + 0.5 for i in range(5)])
    ax.set_yticklabels([f"{fmt(p, 1)}\n" + t for p, t in zip(PS, ["Muito alta", "Alta", "Média", "Baixa", "Muito baixa"])], fontsize=10.5)
    ax.set_xlabel("Impacto médio (média de custo, tempo, escopo e qualidade); linhas pontilhadas = níveis da escala de impacto")
    ax.set_ylabel("Probabilidade")
    ax.set_title("Matriz de calor probabilidade × impacto do FieldOps (18/11/2026)", loc="left", fontsize=13)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    leg = [Rectangle((0, 0), 1, 1, fc=cores["Alta"]), Rectangle((0, 0), 1, 1, fc=cores["Média"]), Rectangle((0, 0), 1, 1, fc=cores["Baixa"])]
    ax.legend(leg, [f"Alta (severidade ≥ {nv(LIM_ALTA)})", f"Média ({nv(LIM_MEDIA)} a < {nv(LIM_ALTA)})", f"Baixa (< {nv(LIM_MEDIA)})"],
              loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False, fontsize=10)
    fig.text(0.12, 0.015, "● R01 a R22 = ameaças (severidade = probabilidade × impacto médio).   ◆ O01 a O04 = oportunidades (valor positivo, mesma escala).",
             fontsize=9.5, color="#333")
    fig.savefig(BASE / "matriz-calor.png", dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)


heatmap()

# ------------------------------------------------------------------ numeros agregados
emv_total = sum(d["emv_rs"] for d in AM)
emv_ativos = sum(d["emv_rs"] for d in ativos)
emv_mats = sum(d["emv_rs"] for d in mats)
resp_total = sum(d["resp_rs"] for d in AM)
resp_op = sum(d["resp_rs"] for d in OP)
emv_op = sum(d["emv_rs"] for d in OP)
mc = monte_carlo(ativos)
mc_todos = monte_carlo(AM)
acum, cobertos = 0.0, []
for d in POR_RANK:
    if acum + d["resp_rs"] <= RESERVA_10:
        acum += d["resp_rs"]
        cobertos.append(d["id"])
    else:
        break
acum_cob = acum
resp_altos = sum(d["resp_rs"] for d in POR_RANK if d["classe"] == "Alta")
n_alta = sum(d["classe"] == "Alta" for d in AM)
n_media = sum(d["classe"] == "Média" for d in AM)
n_baixa = sum(d["classe"] == "Baixa" for d in AM)
reunioes_h = 5 * (20 / 60) * 16
reunioes_rs = (20 / 60) * 16 * TAXA_GP + 4 * (20 / 60) * 16 * TAXA_DEV
prep_rs = 0.5 * 16 * TAXA_GP
estr = {}
for d in AM:
    estr[d["estrat"]] = estr.get(d["estrat"], 0) + 1
dias_max = max(d["dias"] for d in AM)
top5 = POR_RANK[:5]
acima_6 = [d for d in AM if d["dias"] > 6]
R = dict(custo_base=CUSTO_BASE, reserva10=RESERVA_10, reserva5=RESERVA_5, emv_total=emv_total, emv_ativos=emv_ativos, emv_mats=emv_mats,
         resp_total=resp_total, mc=mc, mc_todos=mc_todos, cobertos=cobertos, n_alta=n_alta, n_media=n_media, n_baixa=n_baixa,
         ameacas=len(AM), oportunidades=len(OP), top5=[d["id"] for d in top5])
(BASE / "dados" / "resultados-riscos.json").write_text(json.dumps(R, ensure_ascii=False, indent=1, default=float), encoding="utf-8")

# ------------------------------------------------------------------ texto
out = []
w = out.append

w(f"""# Análise de Riscos do Projeto FieldOps

| Campo | Informação |
|---|---|
| Projeto | FieldOps — Plataforma de Inspeção em Campo (MVP) |
| Instituição / curso | UniSENAI-SP Campus Sorocaba — Análise e Desenvolvimento de Sistemas |
| Disciplina / orientador | Gestão de Projetos — Prof. Me. Deivison S. Takatu |
| Atividade | Aula 07 — Riscos |
| Gerente do projeto | Felipe Marques (FM) |
| Data-base | 18/11/2026 (semana 15, sprint S8; marco M8 em 27/11/2026) |
| Versão | 1.0 |
| Escopo | {len(AM)} ameaças (R01 a R22) e {len(OP)} oportunidades (O01 a O04) |

> **Como ler.** O documento segue o formato dos slides da Aula 07: escala de impacto, tabela probabilidade × impacto com severidade e prioridade, e tabela de respostas. Cada risco é descrito como **causa → risco → consequência**. Dados do GitHub citados (issues, PRs, commits, CI) são de 18/11/2026. Probabilidades, impactos, horas e custos de resposta são **estimativas do gerente (premissas)** e estão rotuladas como tais; as contas saem do script em `scripts/` (editando `riscos_dados.py` o ranking e as tabelas se refazem).

## 1. Resumo executivo

O projeto está na semana 15 com 57 de 103 issues concluídas (55%) e as sprints S6 e S7 com 2 de 13 e 2 de 14 issues concluídas. Dos {len(AM)} riscos do registro, **{len(mats)} já se materializaram** e {n_alta} têm severidade alta. Os cinco maiores são: """ + "; ".join(f"**{d['id']}** {d['nome'][0].lower() + d['nome'][1:]} (severidade {nv(d['sev'])})" for d in top5) + f""". Os três primeiros se reforçam: a sincronização offline (RP03) ainda não existe nem no backend nem no app, 21 issues do backend estão sem responsável e restam apenas **6 dias úteis** até o M8. Nenhuma das respostas depende de dinheiro: a contingência real é a **ordem de corte do RJ07** e a redistribuição de pessoas. As respostas custam {rs(resp_total)} em horas adicionais, comparadas às reservas oficiais do orçamento (`aula-05-custos-qualidade/orcamento-fieldops.md`, linhas O51 e O52): as dos {n_alta} riscos de classe Alta ({rs(resp_altos)}) e as dos {len(cobertos)} primeiros do ranking cabem na contingência de 10% ({rs(RESERVA_10)}); o conjunto inteiro {'cabe' if resp_total <= RESERVA_10 + RESERVA_5 else 'ultrapassa'} a soma das duas reservas ({rs(RESERVA_10 + RESERVA_5)}), deixando {rs(abs(RESERVA_10 + RESERVA_5 - resp_total))} de {'folga' if resp_total <= RESERVA_10 + RESERVA_5 else 'déficit'}. O EMV dos riscos que ainda podem ocorrer ({rs(emv_ativos)}) {'supera' if emv_ativos > RESERVA_10 else 'cabe em'} a contingência de 10%.

## 2. Plano de gerenciamento de riscos (processo 11.1)

### 2.1 Metodologia

Segue os seis processos da Aula 07 (PMBOK 11.1 a 11.6):

| Processo | Como é feito no FieldOps | Saída |
|---|---|---|
| 11.1 Planejar | este plano: escalas, limiares, papéis, reservas e frequência | plano de gerenciamento |
| 11.2 Identificar | fontes: TAP e Declaração de Escopo, documentação (regras de negócio, arquitetura, critérios de aceitação), código e CI no GitHub, retrospectivas; escrita como **causa → risco → consequência** | registro de riscos |
| 11.3 Análise qualitativa | probabilidade × impacto (custo, tempo, escopo, qualidade); severidade = probabilidade × impacto médio; ranking | matriz de calor e prioridade |
| 11.4 Análise quantitativa | valor monetário esperado (EMV) e simulação de Monte Carlo do custo; dias de atraso por risco | reserva sugerida |
| 11.5 Planejar respostas | evitar, transferir, mitigar ou aceitar (ameaças); explorar, compartilhar, melhorar ou aceitar (oportunidades) | plano de respostas |
| 11.6 Controlar | revisão a cada sprint e semanal, gatilhos, lista de observação e escalonamento | registro atualizado e relatório de status |

### 2.2 Papéis e responsabilidades

| Papel | Quem | Responsabilidade |
|---|---|---|
| Gestor do processo de riscos (R e A) | FM | mantém o registro, conduz a reunião de risco, escalona e atualiza a reserva |
| Dono do risco | JV, GR, PD, AF ou FM (campo "Responsável") | monitora o gatilho e executa a resposta no prazo |
| Equipe | JV, GR, PD, AF, FM | informa novos riscos e sinais; marca gatilho observado |
| Orientador e product owner acadêmico | PI-02 (Prof. Glauco Todesco) | decide sobre cortes de escopo e aceita mudanças de requisito |
| Comitê executivo | PI-01 (coordenação) e PI-03 (professores das disciplinas) | recebem escalonamento de riscos que ameaçam marco ou nota; validam o plano de corte |
| Avaliador da disciplina | PI-04 (Prof. Deivison Takatu) | avalia este plano |

### 2.3 Orçamento e prazos para riscos

Valores monetários são **hipóteses de valoração** (o TAP declara "sem investimento financeiro direto"). Os totais e as reservas são os do orçamento oficial (`aula-05-custos-qualidade/orcamento-fieldops.md`); o custo das respostas aos riscos usa as taxas do projeto (desenvolvedor R$ 45/h, gerente R$ 60/h só nas horas de gestão).

| Item | Valor | Como foi calculado |
|---|---:|---|
| **Custo base (referência única deste documento)** | {rs(CUSTO_BASE, 2)} | valor esperado PERT do `orcamento-fieldops.md` (967 h de mão de obra mais custos diretos), **sem reservas**. Escolhi o custo base, e não a linha de base, porque é a base sobre a qual o próprio orçamento calcula as reservas (10% e 5%); assim as faixas da escala de custo e todas as porcentagens deste documento usam o mesmo denominador |
| Reserva de contingência (10%) | {rs(RESERVA_10, 2)} | 10% do custo base, para riscos identificados; linha O51 do orçamento; já faz parte da linha de base e é liberada pelo gerente com registro |
| Linha de base de custos (BAC) | {rs(LINHA_BASE, 2)} | custo base + contingência (orçamento) |
| Reserva gerencial (5%) | {rs(RESERVA_5, 2)} | 5% do custo base, para riscos desconhecidos; linha O52; liberada só pelo patrocinador (PI-01) |
| Orçamento total | {rs(ORCAMENTO_TOTAL, 2)} | BAC + reserva gerencial; reservas somadas = {rs(RESERVA_10 + RESERVA_5, 2)} |
| Reserva de prazo | 0 dia | o prazo é fixo em 16 semanas; **a reserva de escopo é a ordem de corte (RJ07)** |
| Custo do processo de risco | {rs(reunioes_rs + prep_rs)} | reunião de 20 min por semana com as 5 pessoas ({fmt(reunioes_h, 1)} h) mais 30 min semanais de preparação do FM; **já está dentro das horas de gestão do pacote 1.2**, não sai da reserva |

**Prazos.** Revisão formal ao fim de cada sprint (S1 a S7) e reunião semanal de 20 minutos. Na S8 (reta final) a frequência sobe: 19/11, 23/11, 25/11 e 27/11 (20/11 é feriado).

### 2.4 Estrutura analítica dos riscos (RBS)

""")
rbs_nomes = {"1.1": "Offline e sincronização", "1.2": "Integração e contrato de API", "1.3": "Plataforma Android e recursos nativos", "1.4": "Segurança",
             "1.5": "Ambiente, dependências e entrega", "2.1": "Prazo e capacidade", "2.2": "Pessoas", "2.3": "Comunicação e medição",
             "3.1": "Escopo e requisitos", "3.2": "Qualidade de processo", "4.1": "Provedores de serviço", "4.2": "Instituição e docentes"}
rbs_pai = {"1": "Técnico", "2": "Gerenciamento", "3": "Requisitos e qualidade", "4": "Externo"}
linhas = []
for cod, nome in rbs_nomes.items():
    ids = [d["id"] for d in AM if d["rbs"] == cod] + [d["id"] for d in OP if d["rbs"] == cod]
    linhas.append([f"{cod[0]}. {rbs_pai[cod[0]]}", f"{cod} {nome}", ", ".join(ids)])
w(tabela(["Categoria (nível 1)", "Subcategoria (nível 2)", "Riscos"], linhas))
w("""
O campo **Tipo** do registro usa uma lista curta (técnico, prazo, pessoas, requisitos/escopo, integração, segurança, externo e qualidade), mais fácil de filtrar; a RBS acima dá a hierarquia.

### 2.5 Escala de probabilidade

Definida para este projeto; riscos já ocorridos recebem 0,9.

""")
desc_p = {0.1: "improvável; nenhum sinal observado", 0.3: "possível; sem sinal atual, mas a causa existe", 0.5: "um sinal isolado já apareceu", 0.7: "sinais repetidos ou tendência clara", 0.9: "já ocorreu ou ocorrerá quase com certeza"}
w(tabela(["Probabilidade", "Nível", "Critério"], [[fmt(p, 1), n, desc_p[p]] for p, n, _ in ESCALA_P], ["---:", "---", "---"]))
w(f"""
### 2.6 Escala de impacto (custo, tempo, escopo e qualidade)

Mesmos níveis da Aula 07 (0,05; 0,10; 0,20; 0,40; 0,80), com as condições definidas para o FieldOps. **Custo** e **tempo** são calculados pelo script a partir das horas e dos dias estimados de cada risco; **escopo** e **qualidade** são atribuídos pelo gerente com a tabela. Para oportunidades, a mesma escala vale como benefício.

| Objetivo | Muito baixo / 0,05 | Baixo / 0,10 | Moderado / 0,20 | Alto / 0,40 | Muito alto / 0,80 |
|---|---|---|---|---|---|
| **Custo** (referência: custo base de {rs(CUSTO_BASE, 2)}) | aumento insignificante (< 2%, < {rs(0.02 * CUSTO_BASE)}) | 2% a < 10% (até {rs(0.10 * CUSTO_BASE)}) | 10% a < 20% (até {rs(0.20 * CUSTO_BASE)}) | 20% a < 40% (até {rs(0.40 * CUSTO_BASE)}) | ≥ 40% (acima de {rs(0.40 * CUSTO_BASE)}) |
| **Tempo** ({DIAS_UTEIS} dias úteis) | menos de 1 dia útil | 1 a 3 dias (< 5%) | 4 a 7 dias (5% a < 10%) | 8 a 15 dias (10% a < 20%) | 16 dias ou mais (≥ 20%, perda de um marco e meio) |
| **Escopo** | diminui pouco notavelmente (um item P1) | áreas secundárias afetadas (itens P1 e P2; itens 1 e 2 da ordem de corte) | áreas principais afetadas (itens 3 e 4 da ordem de corte: só foto de câmera, construtor sem arrastar e soltar) | redução inaceitável para o patrocinador (núcleo afetado: sincronização só detecta e bloqueia, sem correção) | produto final inútil (sem o fluxo AC-RELEASE: login, checklist, offline, sincronização ou revisão) |
| **Qualidade** (DoD §18.7) | degradação pouco notável (defeito baixo) | poucas telas afetadas (defeito médio com alternativa) | redução exige aprovação do PO (defeito alto corrigível antes da release) | redução inaceitável (defeito alto sem alternativa; falha de segurança com contenção) | produto inútil (defeito crítico: perda de dados, duplicidade grave ou fluxo principal bloqueado) |

### 2.7 Cálculo e limiares de severidade

- **Impacto médio** = média dos quatro impactos (custo, tempo, escopo, qualidade), como no slide. É o critério do **ranking**.
- **Impacto máximo** = maior dos quatro. A média dilui riscos com um impacto muito alto e os demais baixos (por exemplo, perda de dados: qualidade 0,80 e custo 0,10). Por isso o máximo é usado como **regra de lista de observação**: severidade máxima ≥ {nv(LIM_OBS_MAX)}.
- **Severidade** = probabilidade × impacto médio. **Severidade máxima** = probabilidade × impacto máximo.
- **Prioridade** = posição no ranking por severidade (desempate: severidade máxima, depois probabilidade).

| Classe | Severidade (P × impacto médio) | Conduta |
|---|---|---|
| Alta | ≥ {nv(LIM_ALTA)} | resposta ativa, dono nomeado, revisão a cada 48 h na S8 e escalonamento ao PI-02 se um marco for afetado |
| Média | {nv(LIM_MEDIA)} a < {nv(LIM_ALTA)} | resposta planejada e revisão semanal |
| Baixa | < {nv(LIM_MEDIA)} | monitorar; aceitar ou responder se o gatilho disparar |

**Frequência de revisão:** a cada sprint (S1 a S7), semanal em reunião de 20 minutos e a cada 48 h na S8 para os riscos de classe Alta e da lista de observação.

## 3. Registro de riscos (processo 11.2)

Convenções: **Inclusão** é a data em que o risco entrou no registro (TAP em 30/09/2026, Declaração de Escopo em 04/10/2026, ou 18/11/2026 para os identificados na análise do GitHub). Nos riscos que já ocorreram, a materialização foi **identificada em 18/11/2026**. **Gatilho** é o indicador que dispara a resposta (risk trigger). **EAP** usa os códigos da EAP do projeto.

""")
linhas = []
for d in sorted(AM, key=lambda x: x["id"]):
    st = d["status"]
    if d["mat"] and d["incl"] != "18/11/2026":
        st += "; materialização identificada em 18/11/2026"
    linhas.append([d["id"], f"**Causa:** {d['causa']}.<br>**Risco:** {d['risco']}.<br>**Consequência:** {d['conseq']}.", f"{d['tipo']}<br>RBS {d['rbs']}",
                   d["eap"], d["gatilho"], d["incl"], st])
w(tabela(["ID", "Causa → Risco → Consequência", "Tipo", "Pacote da EAP", "Gatilho (indicador)", "Inclusão", "Status em 18/11/2026"], linhas))

w(f"""
## 4. Análise qualitativa: probabilidade × impacto (processo 11.3)

Tabela no formato do slide "Exemplo de Probabilidade × Impacto". Impactos de custo e tempo derivam das horas e dias da seção 6; escopo e qualidade foram atribuídos com a escala 2.6. Ordenada por prioridade.

""")
linhas = []
for d in POR_RANK:
    linhas.append([d["id"], d["nome"], d["tipo"], fmt(d["p"], 1), nv(d["c"]), nv(d["t"]), nv(d["esc"]), nv(d["qual"]), fmt(d["media"], 3),
                   nv(d["max"]), fmt(d["sev"], 3), fmt(d["sev_max"], 3), d["rank"], ("**" + d["classe"] + "**") if d["classe"] == "Alta" else d["classe"],
                   "sim" if d["obs"] else "não"])
w(tabela(["ID", "Risco", "Tipo", "Prob.", "Custo", "Prazo", "Escopo", "Qualid.", "Média", "Máx.", "Severidade", "Sev. máx.", "Prioridade", "Classe", "Lista de observação"],
         linhas, ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---", "---"]))
w(f"""
Resultado: **{n_alta} riscos de classe Alta, {n_media} Média e {n_baixa} Baixa**. Entram na lista de observação {sum(d['obs'] for d in AM)} riscos: os de classe Alta mais os que têm severidade máxima ≥ {nv(LIM_OBS_MAX)} (""" + ", ".join(d["id"] for d in POR_RANK if d["obs"] and d["classe"] != "Alta") + f""").

### 4.1 Matriz probabilidade × impacto

![Matriz de calor probabilidade × impacto](matriz-calor.png)

*Figura 1. Mapa de calor. Cada ponto está na probabilidade do risco e no seu impacto médio exato; a cor de fundo mostra a classe de severidade (limiares em 2.7). A tabela abaixo é a versão tabular da escala, em que cada risco cai no nível de impacto mais próximo.*

""")
# matriz em tabela
cab = ["Prob. \\ Impacto médio"] + [f"{nv(n)}" for n in NIVEIS]
linhas = []
for p in PS:
    linha = [f"**{fmt(p, 1)}**"]
    for n in NIVEIS:
        ids = sorted(POSICAO.get((p, n), []))
        cel = ", ".join(ids) if ids else "—"
        linha.append(f"{cel}<br>*(célula {nv(p * n)})*")
    linhas.append(linha)
w(tabela(cab, linhas))
op_txt = "; ".join(f"{k[0]:.1f} × {nv(k[1])}: {', '.join(v)}" for k, v in sorted(POSICAO_OP.items(), reverse=True))
w(f"\nOportunidades (probabilidade × impacto médio): {op_txt}.\n")

w("""
## 5. Plano de respostas (processo 11.5)

Opções de tratamento da Aula 07: **evitar** (não iniciar ou descontinuar a atividade que origina o risco), **transferir** (passar parte do risco a terceiros), **mitigar** (reduzir probabilidade ou impacto) e **aceitar** (tolerar, com ou sem plano de contingência). O gerente escolheu **mitigar** na maioria dos casos porque os riscos vêm do próprio trabalho de desenvolvimento, e não há a quem transferi-los.

### 5.1 Respostas às ameaças (formato do slide "Exemplo de Respostas para Riscos")

""")
linhas = []
for d in POR_RANK:
    linhas.append([d["id"], d["nome"], d["tipo"], d["incl"], d["estrat"], d["prev"], d["resp"]])
w(tabela(["ID", "Risco", "Tipo", "Data de inclusão", "Abordagem", "Resposta / observação (ação preventiva)", "Responsável"], linhas))
w("""
### 5.2 Detalhamento: contingência, prazo, custo e risco residual

**Ação contingencial** é o que se faz se o gatilho disparar. **Custo da resposta** = horas adicionais × taxa + caixa (premissa; o trabalho já previsto na linha de base não entra). **Risco residual** = probabilidade esperada depois da resposta × impacto médio (o impacto não muda). **Risco secundário** é o risco criado pela própria resposta.

""")
linhas = []
for d in POR_RANK:
    linhas.append([d["id"], d["cont"], d["prazo"], rs(d["resp_rs"]), f"P {fmt(d['p_res'], 1)}: severidade {fmt(d['sev_res'], 3)} ({d['classe_res']})", d["sec"]])
w(tabela(["ID", "Ação contingencial", "Prazo", "Custo da resposta", "Risco residual", "Risco secundário"], linhas,
         ["---", "---", "---", "---:", "---", "---"]))
w(f"""
Total de respostas às ameaças: **{rs(resp_total)}** ({pct(resp_total / CUSTO_BASE, 1)} do custo base). Distribuição: {estr.get('Mitigar', 0)} mitigar, {estr.get('Evitar', 0)} evitar (R10), {estr.get('Transferir', 0)} transferir (R12) e {estr.get('Aceitar', 0)} aceitar (R11).

### 5.3 Oportunidades (riscos positivos)

Respostas para oportunidades: **explorar** (garantir que ocorra), **compartilhar** (dividir com quem tem mais capacidade de capturá-la), **melhorar** (aumentar probabilidade ou impacto) e **aceitar** (aproveitar se ocorrer, sem ação específica).

""")
linhas = []
for d in sorted(OP, key=lambda x: x["id"]):
    linhas.append([d["id"], f"**Causa:** {d['causa']}.<br>**Oportunidade:** {d['risco']}.<br>**Benefício:** {d['conseq']}.", d["tipo"], fmt(d["p"], 1),
                   nv(d["c"]), nv(d["t"]), nv(d["esc"]), nv(d["qual"]), fmt(d["sev"], 3), d["incl"], d["gatilho"]])
w(tabela(["ID", "Causa → Oportunidade → Benefício", "Tipo", "Prob.", "Custo", "Prazo", "Escopo", "Qualid.", "Valor (P × média)", "Inclusão", "Gatilho"], linhas,
         ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---", "---"]))
w("")
linhas = []
for d in sorted(OP, key=lambda x: x["id"]):
    linhas.append([d["id"], d["nome"], d["estrat"], d["prev"], d["cont"], d["resp"], d["prazo"], rs(d["resp_rs"]), d["sec"]])
w(tabela(["ID", "Oportunidade", "Abordagem", "Resposta (ação)", "Se não ocorrer / alternativa", "Responsável", "Prazo", "Custo", "Risco secundário"], linhas,
         ["---", "---", "---", "---", "---", "---", "---", "---:", "---"]))
w(f"""
Respostas às oportunidades: {rs(resp_op)}. Benefício esperado (EMV positivo, horas poupadas × taxa): {rs(emv_op)}. Não é abatido da reserva: é tratado como folga, e não como dinheiro, porque horas poupadas só rendem se forem realocadas ao núcleo.

## 6. Análise quantitativa simples (processo 11.4)

### 6.1 Valor monetário esperado (EMV) dos riscos de custo

EMV = probabilidade × custo se ocorrer, com custo = horas extras × taxa + caixa (premissa do gerente por risco). Tabela ordenada por EMV; riscos já materializados estão marcados.

""")
linhas = []
for d in sorted(AM, key=lambda x: -x["emv_rs"]):
    linhas.append([d["id"], d["nome"], fmt(d["p"], 1), f"{d['horas']} h" + (f" + {rs(d['caixa'])}" if d["caixa"] else ""), rs(d["custo_rs"]), rs(d["emv_rs"]),
                   "sim" if d["mat"] else "não"])
w(tabela(["ID", "Risco", "Prob.", "Esforço extra se ocorrer", "Custo se ocorrer", "EMV", "Já materializado"], linhas, ["---", "---", "---:", "---:", "---:", "---:", "---"]))
w(f"""
| Indicador | Valor | Leitura |
|---|---:|---|
| EMV de todas as ameaças | {rs(emv_total)} ({pct(emv_total / CUSTO_BASE, 1)} do custo base) | limite superior; soma riscos correlacionados |
| EMV dos riscos **ainda não materializados** (previsão para a reserva) | {rs(emv_ativos)} ({pct(emv_ativos / CUSTO_BASE, 1)}) | o que ainda pode custar |
| EMV dos riscos já materializados | {rs(emv_mats)} ({pct(emv_mats / CUSTO_BASE, 1)}) | já está acontecendo: entra no custo real (variação), e não na reserva |
| Reserva de contingência (10%) | {rs(RESERVA_10, 2)} | orçamento oficial, linha O51 |
| Reserva gerencial (5%) | {rs(RESERVA_5, 2)} | orçamento oficial, linha O52 (só o PI-01 libera) |

### 6.2 Reserva de contingência sugerida

- **Pelo EMV dos riscos que ainda podem ocorrer:** {rs(emv_ativos)} ({pct(emv_ativos / CUSTO_BASE, 1)} do custo base). Comparação com a contingência oficial de 10% ({rs(RESERVA_10, 2)}): {'déficit' if emv_ativos > RESERVA_10 else 'folga'} de {rs(abs(emv_ativos - RESERVA_10))}. Somando a reserva gerencial de 5% ({rs(RESERVA_10 + RESERVA_5, 2)} no total), a cobertura equivale a {pct((RESERVA_10 + RESERVA_5) / emv_ativos)} do EMV: {'as duas reservas cobrem os riscos conhecidos, mas a reserva gerencial, que é para os desconhecidos, seria consumida por eles e só o PI-01 pode liberá-la' if emv_ativos > RESERVA_10 else 'a contingência de 10% cobre os riscos conhecidos'}.
- **Por simulação de Monte Carlo** ({fmt(mc['n'])} rodadas, semente {mc['seed']}; cada risco ainda não materializado ocorre com sua probabilidade e custa de 0,5 a 2 vezes o valor estimado, com moda no valor estimado): custo extra médio {rs(mc['media'])}, P50 {rs(mc['p50'])}, **P80 {rs(mc['p80'])}** e P90 {rs(mc['p90'])}. A probabilidade de ultrapassar a contingência de 10% é de {pct(mc['prob_gt_reserva10'])} e a de ultrapassar 10% + 5% é de {pct(mc['prob_gt_reservas'])}. O P80 equivale a {pct(mc['p80'] / CUSTO_BASE, 1)} do custo base, contra {pct((RESERVA_10 + RESERVA_5) / CUSTO_BASE, 1)} das duas reservas somadas.
- **Respostas × reservas oficiais:** as respostas planejadas custam {rs(resp_total)} ({pct(resp_total / RESERVA_10)} da contingência de 10% e {pct(resp_total / (RESERVA_10 + RESERVA_5))} das duas reservas); as dos {n_alta} riscos de classe Alta custam {rs(resp_altos)} ({pct(resp_altos / RESERVA_10)} da contingência). Seguindo o ranking, as respostas dos riscos {", ".join(cobertos)} cabem integralmente nos {rs(RESERVA_10, 2)}; {'as demais, ' + rs(resp_total - acum_cob) + ', dependeriam da reserva gerencial (pedido formal ao PI-01)' if resp_total > RESERVA_10 else 'todas cabem'}.
- **Conclusão:** a contingência de 10% do orçamento cobre as respostas planejadas aos riscos mais graves, mas {'o EMV dos riscos que ainda podem ocorrer e o P80 da simulação excedem' if (emv_ativos > RESERVA_10 and mc['p80'] > RESERVA_10) else 'os valores simulados ficam dentro d'}{' a contingência' if (emv_ativos > RESERVA_10 and mc['p80'] > RESERVA_10) else 'a contingência'}. O orçamento oficial já diz que um atraso generalizado se trata por escopo e prazo, e não por reserva financeira; as horas são fixas (capacidade de 960 h) e não se compram. O que passar da contingência vira **corte de escopo pela ordem do RJ07**, ou pedido de reserva gerencial ao PI-01.

### 6.3 Impacto em dias nos riscos de prazo

Dias são dias úteis de atraso no caminho crítico, se o risco ocorrer. **Não são somáveis** (as causas se sobrepõem: R02, R03, R04 e R14 descrevem o mesmo déficit visto por ângulos diferentes). O que importa é a comparação com a folga: **o prazo é fixo e restam 6 dias úteis (19/11 a 27/11, sem o feriado de 20/11)**.

""")
linhas = []
for d in sorted(AM, key=lambda x: -x["emv_dias"])[:10]:
    linhas.append([d["id"], d["nome"], fmt(d["p"], 1), d["dias"], fmt(d["emv_dias"], 1), nv(d["t"]), "sim" if d["dias"] > 6 else "não"])
w(tabela(["ID", "Risco", "Prob.", "Atraso se ocorrer (dias úteis)", "Dias esperados (P × dias)", "Nível de impacto no prazo", "Maior que os 6 dias restantes"], linhas,
         ["---", "---", "---:", "---:", "---:", "---:", "---"]))
w(f"""
{len(acima_6)} dos {len(AM)} riscos, se ocorrerem, consomem mais dias do que restam ({", ".join(d["id"] for d in acima_6)}). Como a folga é zero, **qualquer atraso adicional se converte em corte de escopo**, e não em extensão do prazo.

## 7. Controle e monitoramento (processo 11.6)

### 7.1 Indicadores

| Indicador | Fonte | Limite de alerta | Risco monitorado |
|---|---|---|---|
| Issues P0 sem responsável | GitHub (issues) | > 0 por mais de 2 dias | R03 |
| Issues concluídas por sprint (gráfico p) | GitHub (milestones) | ponto abaixo do limite inferior | R02, R14 |
| PRs mergeados sem revisão de outra pessoa | GitHub (PRs) | qualquer PR do núcleo | R15, R19 |
| Execuções de CI com falha e `develop` vermelha | GitHub Actions | `develop` vermelha por mais de 1 dia | R13, R22 |
| Cenários do AC-SYNC passando (envio, reenvio sem duplicidade, falha parcial) | testes de integração | menos de 3 de 3 até 25/11 | R06, R20 |
| Execuções do fluxo ponta a ponta no ambiente de integração | roteiro AC-RELEASE | nenhuma na semana | R14, R17 |
| Dias sem commit por camada | GitHub (commits) | 3 dias úteis | R04, R05 |
| Issues P1 em andamento | GitHub | qualquer uma antes do ensaio do AC-RELEASE | R10 |
| Fila do build EAS | Expo | mais de 1 hora | R12 |

### 7.2 Lista de observação

Riscos de classe Alta ou com severidade máxima ≥ {nv(LIM_OBS_MAX)}, revisados a cada 48 h na S8:

""")
linhas = []
for d in POR_RANK:
    if d["obs"]:
        linhas.append([d["rank"], d["id"], d["nome"], d["classe"], fmt(d["sev"], 3), fmt(d["sev_max"], 3), d["gatilho"], d["resp"]])
w(tabela(["Prioridade", "ID", "Risco", "Classe", "Severidade", "Sev. máx.", "Gatilho", "Dono"], linhas, ["---:", "---", "---", "---", "---:", "---:", "---", "---"]))
w("""
### 7.3 Regras de escalonamento

| Situação | Quem é avisado | Prazo |
|---|---|---|
| Gatilho disparado em risco de classe Alta | FM e o dono do risco | no mesmo dia |
| Risco que afeta um marco (impacto em prazo ou escopo ≥ 0,40) ou ação sem avanço por 2 dias | FM comunica ao PI-02 e ao PI-03 com a proposta de corte | em 24 h |
| Materialização de risco com impacto em qualidade 0,80 (perda de dados, duplicidade grave) ou em segurança | FM, PI-02 e PI-01 (coordenação) | em 24 h, com plano de contenção |
| Necessidade de usar a reserva de 10% ou a de 5% | FM registra no relatório de status e comunica ao PI-02 | antes de gastar |
| Mudança de escopo (aplicação de item da ordem de corte) | decisão do FM com aprovação do PI-02 | na reunião seguinte |

### 7.4 Reunião de risco

Reunião de 20 minutos, semanal (e a cada 48 h na S8), conduzida por FM. Pauta fixa:

1. Fatos novos desde a última reunião, com dados do GitHub (2 min).
2. Lista de observação: gatilho observado? resposta no prazo? (10 min).
3. Riscos novos ou que mudaram de probabilidade ou impacto (5 min).
4. Riscos a encerrar e decisão de escalonamento (3 min).

Saída: registro atualizado (`riscos.csv` e este documento) e uma linha no relatório de status do pacote 1.3.

### 7.5 Como um novo risco entra

1. Qualquer pessoa abre uma issue com o rótulo `risco`, escrevendo **causa → risco → consequência**, o pacote da EAP afetado e o gatilho.
2. O FM atribui probabilidade e impactos com as escalas 2.5 e 2.6 em até 2 dias úteis e define dono e resposta.
3. O risco entra no registro com a data de inclusão e é apresentado na reunião seguinte.
4. Um risco é encerrado quando o gatilho deixa de existir, a causa foi eliminada ou o marco passou. O encerramento fica registrado com a data.

## 8. Riscos já materializados em 18/11/2026

Dados do status real (levantamento do GitHub de 18/11/2026, base do projeto §9, milestones por sprint, 4 repositórios): **57 de 103 issues concluídas (55%)**; S1 15/17, S2 17/17, S3 7/10, S4 10/14, S5 4/8, **S6 2/13**, **S7 2/14**, S8 0/10. Por repositório: backend 14/41, frontend 22/31, app 21/39, docs 1/6. Estamos na semana 15 (S8) com os marcos M6 (30/10) e M7 (13/11) sem entrega completa: o **desvio de prazo é real** e é tratado aqui como situação monitorada, com ações corretivas e aplicação da ordem de corte (RJ07).

""")
ev = {
    "R01": ("3 dos 4 feriados já passaram (07/09, 12/10, 02/11)", "semanas curtas e marcos fechados sem o incremento completo"),
    "R02": ("S6 com 2 de 13 e S7 com 2 de 14 issues concluídas; gráfico p abaixo do limite inferior", "M6 (30/10) e M7 (13/11) não entregues"),
    "R03": ("21 issues abertas do backend sem responsável (push, pull, conflitos, arquivos, evidências, revisão, seed, container)", "app e web sem endpoint de sincronização e revisão para integrar"),
    "R04": ("app com 21 das 39 issues concluídas; 18 abertas; 98% dos commits do app vêm de um único integrante", "motor de sincronização, fila de upload e fluxo de correção do app parados"),
    "R10": ("dashboard P1 do web (`frontend #28`) mergeado em 09/11 com issues P0 de S6 abertas", "horas fora do núcleo"),
    "R13": ("8 das 10 falhas de CI no passo `expo-doctor`; `develop` do app vermelha de 18/09 a 14/10", "PRs mergeados com CI vermelho (app #46) e correção dedicada (app #49 e #57)"),
    "R15": ("49 de 55 PRs mergeados sem revisão registrada no GitHub (só a revisão registrada é visível)", "defeitos só vistos na integração (V5 duplicada, 409 no lugar de 500)"),
    "R16": ("0 de 518 critérios de aceitação marcados nas issues fechadas; 7 issues do web fechadas no mesmo minuto", "status do quadro não reflete o produto"),
    "R22": ("migração V5 duplicada (backend #57) e shell fora da `develop` (frontend #36)", "retrabalho de merge"),
}
linhas = []
for d in sorted(mats, key=lambda x: x["rank"]):
    e = ev[d["id"]]
    linhas.append([d["id"], d["nome"], e[0], e[1], f"{d['estrat']}: {d['prev']}", d["resp"]])
w(tabela(["ID", "Risco que ocorreu", "Evidência em 18/11/2026", "Efeito já visto", "Ação em curso (seção 5)", "Dono"], linhas))
w(f"""
**Concentração e carga.** Medida pelos commits, em cada repositório um único integrante concentra a maior parte: no backend 114 de 129 commits (88%), no frontend 276 de 368 (75%), no app 93 de 95 (98%). O mobile depende de um único integrante, que também acumula a gestão (papéis da base do projeto). A distribuição R do plano (FM com 1.x, 5.1 a 5.5, 7.2 e 7.4; AF único R do web; JV, GR e PD no backend e na documentação) amplifica o efeito.

**Riscos que viraram problema e o que já foi tratado.** R11 (construtor de modelos) materializou em S3, mas foi entregue em 11/11 e hoje só deixa risco de regressão. R08 (recursos nativos) está parcialmente mitigado: foto, QR Code e localização foram concluídos entre 04/11 e 11/11, e falta validar em aparelhos físicos.

**Ordem de corte (RJ07) a aplicar já.** Itens 1 e 2 liberam horas imediatamente: remover o dashboard avançado e as 12 issues P1; limitar tipos de resposta. Itens 3 a 5 só se o ensaio do AC-SYNC em 24/11 falhar. O núcleo intocável é autenticação, planejamento, checklist, foto, offline, sincronização e revisão.

## 9. Premissas e limitações

1. Probabilidades, níveis de escopo e qualidade, horas de impacto, custos de resposta e probabilidades residuais são **estimativas do gerente**, sem base estatística. Podem ser contestadas e, ao editar `scripts/riscos_dados.py`, o documento é regerado.
2. A referência monetária é o custo base PERT do orçamento oficial ({rs(CUSTO_BASE, 2)}), com contingência de {rs(RESERVA_10, 2)} e reserva gerencial de {rs(RESERVA_5, 2)} (`orcamento-fieldops.md`). Se o orçamento mudar, atualize as constantes no início de `riscos_calculo.py` e rode o script. O custo das respostas e dos impactos usa R$ 45/h e R$ 60/h; as horas de impacto são estimativas minhas.
3. Responsáveis e prazos das respostas são **propostas a confirmar** com o grupo.
4. Riscos já ocorridos usam probabilidade 0,9 para manter a escala; o impacto continua em curso.
5. Os dias de atraso não são somáveis (causas correlacionadas). O Monte Carlo trata só custo e sorteia os riscos de forma independente, o que subestima a variância de eventos correlacionados.
6. O status das issues é o do levantamento do GitHub de 18/11/2026 registrado na base do projeto (§9, milestones por sprint). A coleta automática feita depois, usada em `aula-05-custos-qualidade/qualidade-7-ferramentas-fieldops.md`, traz data e hora (UTC) e a explicação da pequena diferença na seção 3 daquele documento.

**Reprodutibilidade.** `python3 scripts/analise_riscos.py` regenera este arquivo, `matriz-calor.png`, `dados/riscos.csv` e `dados/resultados-riscos.json`. Dependências: Python 3, numpy e matplotlib.

## Referências

1. TAKATU, Deivison S. **Gestão de Projetos: Riscos (Aula 07)**. UniSENAI-SP, 2026. Processos 11.1 a 11.6; causa, risco e consequência; escala de impacto; respostas a riscos.
2. FIELDOPS. **Termo de Abertura do Projeto** (principais riscos) e **Declaração do Escopo** (04/10/2026): requisitos RP01 a RP10, RJ01 a RJ08, premissas, restrições e ordem de corte.
3. FIELDOPS. **Documentação** (`docs/notion`: 09 Regras de negócio, 11 Arquitetura, 12 API, 17 Critérios de aceitação, 18 Definição de Pronto, 19 Critérios de avaliação).
4. GITHUB. Repositórios `FieldOps-Project/backend`, `frontend`, `app` e `docs` (18/11/2026).
5. CARVALHO, Fábio Câmara Araújo de. **Gestão de projetos**. 2. ed. São Paulo: Pearson, 2018.
""")
(BASE / "analise-riscos-fieldops.md").write_text("".join(out), encoding="utf-8")
print("ok", len("".join(out)), "caracteres; riscos:", len(AM), "ameacas,", len(OP), "oportunidades")
print("top5:", [d["id"] for d in top5], "emv", round(emv_total), round(emv_ativos), "resp", resp_total, "cobertos", cobertos)
