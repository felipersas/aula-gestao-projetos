#!/usr/bin/env python3
"""Gera analise-portfolio.md a partir do modelo (numeros) e de conteudo.py (textos)."""
from pathlib import Path

import modelo_portfolio as M
import conteudo as C
from conteudo import br, mil, pct, n2

RAIZ = Path(__file__).resolve().parent.parent
OUT = RAIZ / "analise-portfolio.md"
L = []


def w(s=""):
    L.append(s)


def tabela(cab, linhas, alin=None):
    alin = alin or ["l"] * len(cab)
    sep = {"l": ":---", "r": "---:", "c": ":---:"}
    w("| " + " | ".join(cab) + " |")
    w("|" + "|".join(sep[a] for a in alin) + "|")
    for l in linhas:
        w("| " + " | ".join(str(x) for x in l) + " |")
    w()


def NOMES_SENS(n):
    m = {"AE": "Alinhamento", "BC": "Benefício/custo", "RI": "Risco", "PR": "Prazo", "SI": "Sinergia", "VR": "Recursos"}
    return m.get(n[:2], n) + n[2:] if n[:2] in m else n


def sev_fmt(x):
    return br(x, 3) if round(x * 1000) % 10 else br(x, 2)


EMO = {"Prioridade": "🟢 Prioridade", "Posterior": "🟡 Posterior", "Adiado": "🔴 Adiado"}
P = M.PROJ
mesnome = ["m%d" % k for k in range(1, 13)]

# ================================================================= cabecalho
w("# Análise de Portfólio e Programas — MetalTech S.A.")
w()
tabela(["Campo", "Conteúdo"], [
    ["Atividade", "Desafio de Gestão de Portfólio e Programas (Gestão de Projetos, Prof. Me. Deivison Takatu, UniSENAI-SP Campus Sorocaba, ADS)"],
    ["Papel do grupo", "PMO (Project Management Office) da MetalTech S.A."],
    ["Grupo", ", ".join(C.GRUPO)],
    ["Data / versão", "18/11/2026 · v1.0"],
    ["Pergunta central", "Como a empresa deve organizar seu portfólio de projetos para alcançar seus objetivos estratégicos utilizando os recursos disponíveis?"],
    ["Entregas relacionadas", "`slide-executivo.pptx` (+ `.png`, `.pdf`) · `roteiro-apresentacao-3min.md` · `relatorio-final-metaltech.docx` · `scripts/` (todas as contas)"],
])
w("**Como ler os números.** Todo valor sai de `scripts/modelo_portfolio.py`. Neste documento, **DADO** é o que consta do enunciado do desafio; "
  "**(H)** marca hipótese ou premissa do grupo, a validar com a MetalTech. Valores em R$ mil, salvo indicação. T1 = meses 1 a 3, T2 = 4 a 6, T3 = 7 a 9, T4 = 10 a 12.")
w()
w("## Resposta em uma frase")
w()
w(f"Priorizar **P1, P2, P4, P5 e P6** ({mil(M.INV_PRIOR)}, {pct(100 * M.INV_PRIOR / M.ORCAMENTO_TETO)} do teto), organizados nos programas **A (Excelência Operacional)** e **B (Qualidade 4.0, fase 1)**, "
  f"manter **{mil(M.RESERVA)} ({pct(100 * M.RESERVA / M.ORCAMENTO_TETO)}) de reserva gerencial**, deixar o **P7 como posterior** (gate G2 no fim do m6) e **adiar P3 e P8**. "
  "É a única combinação dentro do teto que cobre as quatro metas com algum benefício quantificado e ainda deixa reserva para o projeto de risco alto.")
w()

# ================================================================= 1
w("## 1. Objetivos estratégicos e restrições (DADO)")
w()
tabela(["Objetivo", "Meta", "Leitura do PMO"], [
    ["Aumentar a produtividade", "+15%", "Só o P1 declara ganho numérico (+12%)"],
    ["Reduzir paradas de produção", "-20%", "Só o P2 declara ganho numérico (-20%)"],
    ["Reduzir custos operacionais", "-10%", "Nenhum projeto declara ganho em custo; o P4 reduz desperdício em 25%"],
    ["Melhorar a qualidade", "-30% de retrabalho", "Só o P5 declara ganho numérico (-30%)"],
], ["l", "c", "l"])
w(f"**Restrições (DADO):** orçamento máximo de {mil(M.ORCAMENTO_TETO)}; 2 engenheiros de automação, 2 analistas de TI, 1 especialista em qualidade, 1 gerente de projetos e 1 especialista em manutenção; "
  f"carteira total de {mil(M.TOTAL_CARTEIRA)} em 8 projetos, ou seja, {n2(M.TOTAL_CARTEIRA / M.ORCAMENTO_TETO)} vezes o orçamento.")
w()

# ================================================================= 2
w("## 2. Etapa 1 — Análise dos oito projetos")
w()
w("### 2.1 Dados do enunciado e indicadores derivados")
w()
linhas = []
for p in P:
    d = P[p]
    q = M.BEN_QUANT.get(p)
    cpp = M.custo_por_pp(p)
    linhas.append([f"**{p}**", d["nome"], mil(d["inv"]), pct(100 * d["inv"] / M.ORCAMENTO_TETO, 1), f"{d['prazo']} m", d["risco"], d["ben"],
                   (f"{br(cpp, 1)} mil/p.p." if cpp else "n/d"),
                   (f"{q[0]} de {M.METAS[q[1]]} p.p. ({pct(100 * q[0] / M.METAS[q[1]])})" if q and q[1] in M.METAS else ("desperdício, não custo: efeito sobre a meta de custos não convertido" if p == "P4" else "fora das 4 metas" if q else "sem número"))])
tabela(["ID", "Projeto", "Investimento", "% do teto", "Prazo", "Risco", "Principal benefício (DADO)", "Custo por p.p. (derivado)", "Cobertura da meta (derivado)"], linhas,
       ["l", "l", "r", "r", "r", "l", "l", "r", "l"])
w("*Derivados:* custo por ponto percentual = investimento ÷ benefício declarado; só existe para os projetos com benefício numérico. "
  "O P4 reduz desperdício, não custo; o P8 aumenta capacidade, que não é um dos quatro objetivos; P3, P6 e P7 não têm benefício quantificado no enunciado. "
  "O ROI financeiro **não pode ser calculado** com os dados do enunciado (não há valor monetário de benefício); por isso o grupo usa custo por p.p. e cobertura de meta.")
w()
w("### 2.2 Relações, recursos e leitura de cada projeto")
w()
tabela(["Projeto", "Dependências (DADO)", "Recursos exigidos (H)", "Leitura do PMO"], [
    ["P1", "Relaciona-se ao P6; recomendado antes do P8", "EA1 e EA2 a 100% por 6 meses; TI1 a 30% no m3-m6", "Meta de produtividade e adoção dependem do P6; é o maior risco do ciclo"],
    ["P2", "Complementar ao P7 (dados)", "MAN a 100% e TI1 a 70% por 4 meses; EA só consultivo", "Entrega sozinho a meta de paradas, sem folga"],
    ["P3", "Depende do P7 na etapa de integração", "TI por 10 meses; integrador externo", "Alto risco e benefício indireto; só faz sentido depois do P7"],
    ["P4", "Complementar ao P5", "QUAL a 100% no m1-m3; TI2 a 20%", "Vitória rápida de baixo risco; alimenta o P5"],
    ["P5", "Complementar ao P4", "QUAL a 100% no m4-m7; TI2 a 50%", "Entrega sozinho a meta de retrabalho, sem folga"],
    ["P6", "Prepara os operadores para o P1", "MAN a 20% no m5-m6; conteúdo do fornecedor do P1", "Barato e de baixo risco; protege o investimento do P1"],
    ["P7", "Facilita a integração do P3", "EA e TI, ocupados pelo P1 até o m6", "Habilitador útil, mas não cabe com reserva no ciclo; decide-se no G2"],
    ["P8", "Executar o P1 antes ou junto", "EA e TI o ano todo", "Consumiria 60% do teto e 12 meses, com risco alto e sem meta direta"],
], ["l", "l", "l", "l"])

# ================================================================= 3
w("## 3. Matriz de priorização ponderada")
w()
w("Pesos (definidos pelo grupo, **H**), notas de 1 a 5 (5 = melhor) e rubrica. As notas de **risco, prazo e benefício/custo** seguem regra objetiva sobre dados do enunciado e o script confere se a tabela bate com a regra (`assert` em `modelo_portfolio.py`). "
  "As demais (alinhamento, sinergia, recursos) são julgamento do grupo, justificado na tabela 3.3.")
w()
w("### 3.1 Critérios, pesos e rubrica")
w()
tabela(["Critério (peso)", "Rubrica das notas"], [[a, b] for a, b in C.RUBRICA])
w("### 3.2 Notas e pontuação")
w()
cab = ["Projeto"] + [f"{n.split(' (')[0]} ({pct(100 * wgt)})" for k, n, wgt in M.CRIT] + ["**Pontuação**", "Posição", "Decisão"]
linhas = []
for p in M.RANK:
    linhas.append([f"**{p}** {P[p]['nome']}"] + [M.NOTAS[p][k] for k, _, _ in M.CRIT] + [f"**{n2(M.SCORE[p])}**", f"{M.RANK.index(p) + 1}º", EMO[M.DECISAO[p]]])
tabela(cab, linhas, ["l"] + ["c"] * 6 + ["r", "c", "l"])
w("Pontuação = soma de nota × peso (calculada em `modelo_portfolio.py`).")
w()
w("![Matriz de priorização ponderada](img/fig02_matriz_priorizacao.png)")
w()
w("### 3.3 Justificativa de cada nota")
w()
cab = ["Projeto"] + [n.split(" (")[0] for _, n, _ in M.CRIT]
linhas = []
for p in M.RANK:
    linhas.append([f"**{p}**"] + [f"**{M.NOTAS[p][k]}**: {C.JUST[p][k]}" for k, _, _ in M.CRIT])
tabela(cab, linhas)
w("### 3.4 O que o cálculo diz (e o que não diz)")
w()
w(f"- A ordem do cálculo é **P4 ({n2(M.SCORE['P4'])}), P5 ({n2(M.SCORE['P5'])}), P2 ({n2(M.SCORE['P2'])}), P6 ({n2(M.SCORE['P6'])}), P1 ({n2(M.SCORE['P1'])}), P7 ({n2(M.SCORE['P7'])}), P8 ({n2(M.SCORE['P8'])}), P3 ({n2(M.SCORE['P3'])})**. Os cinco primeiros são exatamente os projetos priorizados, e a decisão de corte (P7 abaixo da linha) coincide com a classificação.")
w(f"- **O P1 é o 5º, e não o 1º.** Ele fica na carteira por causa do alinhamento (única fonte quantificada de produtividade) e da sinergia com o P6, apesar de ser o pior em risco, custo por p.p. e uso de recursos. A margem sobre o P7 é de {n2(M.SCORE['P1'] - M.SCORE['P7'])} ponto. "
  "O PMO não esconde isso: o P1 entra por **cobertura de meta**, e a matriz sozinha não o protegeria de uma mudança grande de pesos.")
w(f"- **Sensibilidade (script):** variando cada peso em ±10 p.p. (12 testes) e usando quatro perfis alternativos (pesos iguais, foco em custo, foco em risco, foco estratégico), o conjunto dos cinco primeiros **não muda em nenhum dos 16 casos**. "
  f"Em 20.000 sorteios de pesos em torno dos pesos-base (distribuição de Dirichlet, semente 42), o conjunto prioritário se repete em {pct(100 * M.MC_TOP5, 1)} dos casos; é o mesmo percentual em que o P1 supera o P7.")
w("")
tabela(["Teste de sensibilidade", "Ordem resultante", "Top 5 igual?"],
       [[NOMES_SENS(n), ", ".join(r), "sim" if set(r[:5]) == M.TOP5 else "**não**"] for n, r in M.SENS])
w("- **Limite do método:** notas e pesos são subjetivos. Por isso a decisão não se apoia só na matriz: ela é conferida contra restrições duras (teto, dependências, cobertura das metas) na seção seguinte.")
w()

# ================================================================= 4
w("## 4. Cenários considerados")
w()
import itertools
N_ORC = sum(1 for r in range(1, 9) for ps in itertools.combinations(M.PROJ, r) if sum(P[p]["inv"] for p in ps) <= M.ORCAMENTO_TETO)
assert abs(M.MC_TOP5 - M.MC_P1_P7) < 1e-12
w(f"Todos os 255 subconjuntos possíveis de projetos foram enumerados por script: {N_ORC} cabem no teto de R$ 2,5 mi e {len(M.SUBS)} também respeitam as dependências recomendadas (P8 só com P1, P3 só com P7, P1 só com P6; ver `enumera_subconjuntos`). "
  "Considerando a cobertura **direta** das metas (benefício quantificado no enunciado: P1 produtividade, P2 paradas, P4 desperdício → custos, P5 retrabalho), "
  f"**só o conjunto {{P1, P2, P4, P5, P6}} cobre as quatro metas dentro do teto** ({mil(M.MELHOR_COM_RESERVA['custo'])}; o P6 entra porque o P1 depende dele para a adoção). Os quatro cenários do grupo:")
w()
descr = {
    "A": ("**Escolhido.** P1+P2+P4+P5+P6, P7 condicionado ao G2.", "Cobre as 4 metas, deixa 16% de reserva para o projeto de risco alto."),
    "B": ("P1+P2+P5+P6+P7.", "Consome 98% do teto, sem reserva (R$ 50 mil), e deixa o P4 de fora: sem a vitória rápida de refugo e com o P1 (risco alto) sem colchão. Rejeitado."),
    "C": ("P2+P4+P5+P6+P7.", "Barato e de risco baixo, quase empata na pontuação (19,65 contra 20,15), mas sem o P1 **nenhum projeto quantifica ganho de produtividade**: a meta de +15% fica descoberta. Rejeitado."),
    "D": ("P1+P8 (P8 exige o P1 antes).", "Consome 96% do teto só com projetos de risco alto, deixa paradas, retrabalho e custos sem projeto e o benefício do P8 (12 meses) só chega depois do horizonte. Incluir o P8 ao cenário A custaria "
          f"{mil(M.ESTOURO_A_MAIS_P8)}, {mil(M.ESTOURO_A_MAIS_P8 - M.ORCAMENTO_TETO)} acima do teto. Rejeitado."),
}
linhas = []
for k in "ABCD":
    c = M.CENARIOS[k]
    linhas.append([f"**{k}**", descr[k][0], ", ".join(c["projetos"]), mil(c["custo"]), pct(c["pct"], 0), mil(c["reserva"]), n2(c["score"]),
                   f"{c['n_metas']} de 4", c["n_alto_risco"], descr[k][1]])
tabela(["Cen.", "Composição", "Projetos", "Custo", "% do teto", "Reserva", "Soma das notas", "Metas cobertas (direto)", "Proj. risco alto", "Avaliação"], linhas,
       ["c", "l", "l", "r", "r", "r", "r", "c", "c", "l"])
w(f"Soma das notas = soma das pontuações da matriz dos projetos do cenário (indicativa; cenários com mais projetos somam mais). Teste de subconjuntos: dos {len(M.SUBS)} subconjuntos viáveis em orçamento e dependências, "
  f"{len(M.SUBS_4METAS)} cobre as 4 metas diretamente, e é este.")
w()

# ================================================================= 5
w("## 5. Classificação do portfólio")
w()
tabela(["Projeto", "Investimento", "Classificação", "Racional"], [
    ["P1 Automação da Linha 1", mil(900), EMO["Prioridade"], "Única fonte quantificada de produtividade (+12%); precisa do P6 e antecede o P8"],
    ["P2 Manutenção Preditiva", mil(450), EMO["Prioridade"], "Entrega sozinho a meta de -20% de paradas"],
    ["P4 Redução de Refugo", mil(250), EMO["Prioridade"], "Vitória rápida (3 meses, risco baixo), -25% de desperdício, alimenta custos e o P5"],
    ["P5 Controle de Qualidade", mil(350), EMO["Prioridade"], "Entrega sozinho a meta de -30% de retrabalho; complementar ao P4"],
    ["P6 Treinamento de Operadores", mil(150), EMO["Prioridade"], "Barato e de risco baixo; habilita a adoção do P1 e contribui para os +15%"],
    ["P7 Monitoramento IoT", mil(600), EMO["Posterior"], "Habilitador, mas não cabe com reserva; **gate G2 no fim do m6**: inicia no m7 só se P2 e P4 estiverem no prazo e houver recurso"],
    ["P3 Novo ERP Industrial", mil(1200), EMO["Adiado"], "Alto risco, 10 meses, benefício indireto e dependência do P7"],
    ["P8 Expansão da Capacidade", mil(1500), EMO["Adiado"], "60% do teto e 12 meses, risco alto, sem meta direta; antes é preciso medir o P1"],
], ["l", "r", "l", "l"])
w("Nenhum projeto foi **descartado**: P3 e P8 ficam adiados com condição de retorno definida (seção 10).")
w()

# ================================================================= 6
w("## 6. Etapa 2 — Estrutura de programas")
w()
w("```text")
w("PORTFÓLIO DA METALTECH  (teto R$ 2,5 mi · 12 meses)")
w("│")
w(f"├── Programa A — Excelência Operacional ({mil(M.PROG_CUSTO['A'])})")
w("│   ├── P1 Automação da Linha 1            R$ 900 mil")
w("│   ├── P2 Manutenção Preditiva            R$ 450 mil")
w("│   └── P6 Treinamento de Operadores       R$ 150 mil")
w("│")
w(f"├── Programa B — Qualidade 4.0, fase 1 ({mil(M.PROG_CUSTO['B'])})")
w("│   ├── P4 Redução de Refugo               R$ 250 mil")
w("│   └── P5 Controle de Qualidade           R$ 350 mil")
w("│")
w("├── Programa C — Transformação Digital (NÃO ATIVADO; candidato a 2027)")
w("│   ├── P7 Monitoramento IoT               R$ 600 mil  (posterior: gate G2)")
w("│   └── P3 Novo ERP Industrial             R$ 1,2 mi   (adiado)")
w("│")
w("├── Projetos independentes: nenhum")
w("└── Fora do ciclo: P8 Expansão da Capacidade R$ 1,5 mi (adiado)   |   Reserva gerencial R$ 400 mil")
w("```")
w()
w("![Estrutura do portfólio](img/fig01_estrutura_portfolio.png)")
w()
linhas = []
for k, v in M.PROGRAMAS.items():
    linhas.append([f"**{k}. {v['nome']}**", ", ".join(v["projetos"]), mil(M.PROG_CUSTO[k]), C.PROG_TXT[k]["objetivo"], C.PROG_TXT[k]["beneficio"], C.PROG_TXT[k]["metas"]])
tabela(["Programa", "Projetos", "Investimento", "Objetivo", "Benefício esperado", "Metas atendidas"], linhas, ["l", "l", "r", "l", "l", "l"])
w(f"**Por que a estrutura difere (em parte) da sugestão do enunciado.** O Programa B sugerido continha o P7; o PMO mantém P4 e P5 no programa e trata o P7 como **fase 2** futura, porque ele depende do gate G2. "
  f"{C.PROG_C} Não há projetos independentes: os cinco priorizados têm relação direta com outro projeto do mesmo programa (P1-P6; P4-P5) ou com a meta do programa (P2).")
w()

# ================================================================= 7
w("## 7. Etapa 3 — Orçamento")
w()
w("### 7.1 Decisão por projeto")
w()
linhas = []
for p in ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]:
    dec = {"Prioridade": "Priorizar", "Posterior": "Posterior (condicionado ao G2)", "Adiado": "Adiar"}[M.DECISAO[p]]
    linhas.append([p, P[p]["nome"], mil(P[p]["inv"]), dec, pct(100 * P[p]["inv"] / M.ORCAMENTO_TETO, 1) if M.DECISAO[p] == "Prioridade" else "—"])
linhas.append(["", "**Total priorizado**", f"**{mil(M.INV_PRIOR)}**", f"{pct(100 * M.INV_PRIOR / M.ORCAMENTO_TETO)} do teto", f"**{pct(100 * M.INV_PRIOR / M.ORCAMENTO_TETO, 1)}**"])
linhas.append(["", "**Reserva gerencial**", f"**{mil(M.RESERVA)}**", f"{pct(100 * M.RESERVA / M.ORCAMENTO_TETO)} do teto", f"**{pct(100 * M.RESERVA / M.ORCAMENTO_TETO, 1)}**"])
linhas.append(["", "**Total comprometido**", f"**{mil(M.INV_PRIOR + M.RESERVA)}**", f"= teto de {mil(M.ORCAMENTO_TETO)}", "**100,0%**"])
tabela(["ID", "Projeto", "Investimento (DADO)", "Decisão", "% do teto"], linhas, ["l", "l", "r", "l", "r"])
w(f"**Verificação por script:** {' + '.join(str(P[p]['inv']) for p in M.PRIORIZADOS)} = {M.INV_PRIOR} mil ≤ {M.ORCAMENTO_TETO} mil (regra do enunciado); {M.INV_PRIOR} + {M.RESERVA} = {M.INV_PRIOR + M.RESERVA} mil. "
  f"Os três projetos fora do ciclo somam {mil(sum(P[p]['inv'] for p in ['P3', 'P7', 'P8']))}; com eles a carteira inteira custaria {mil(M.TOTAL_CARTEIRA)}.")
w()
w("### 7.2 Por programa")
w()
tabela(["Item", "Investimento", "% do teto", "% dos priorizados"], [
    ["Programa A — Excelência Operacional (P1+P2+P6)", mil(M.PROG_CUSTO["A"]), pct(100 * M.PROG_CUSTO["A"] / M.ORCAMENTO_TETO), pct(100 * M.PROG_CUSTO["A"] / M.INV_PRIOR, 1)],
    ["Programa B — Qualidade 4.0, fase 1 (P4+P5)", mil(M.PROG_CUSTO["B"]), pct(100 * M.PROG_CUSTO["B"] / M.ORCAMENTO_TETO), pct(100 * M.PROG_CUSTO["B"] / M.INV_PRIOR, 1)],
    ["Reserva gerencial", mil(M.RESERVA), pct(100 * M.RESERVA / M.ORCAMENTO_TETO), "—"],
    ["**Total**", f"**{mil(M.ORCAMENTO_TETO)}**", "**100%**", "—"],
], ["l", "r", "r", "r"])
w("### 7.3 Distribuição por trimestre (curva de desembolso)")
w()
w("**Premissa (H):** o investimento de cada projeto é desembolsado **linearmente, mês a mês, ao longo da duração do projeto** (por exemplo, P1: R$ 900 mil ÷ 6 = R$ 150 mil por mês). "
  "A reserva não entra na curva: só é liberada por decisão do comitê, mediante gatilho de risco.")
w()
linhas = []
for p in M.PRIORIZADOS:
    linhas.append([p, f"m{M.JANELA[p][0]}-m{M.JANELA[p][1]}"] + [br(x, 1) if x else "—" for x in M.TRI_PROJ[p]] + [br(P[p]["inv"])])
linhas.append(["**Total**", ""] + [f"**{br(x, 1) if x else '0'}**" for x in M.TRI] + [f"**{br(M.INV_PRIOR)}**"])
linhas.append(["Acumulado", ""] + [br(sum(M.TRI[:k + 1]), 1) for k in range(4)] + [""])
linhas.append(["% acumulado do teto", ""] + [pct(100 * sum(M.TRI[:k + 1]) / M.ORCAMENTO_TETO, 1) for k in range(4)] + [""])
tabela(["Projeto", "Janela", "T1", "T2", "T3", "T4", "Total (R$ mil)"], linhas, ["l", "l", "r", "r", "r", "r", "r"])
linhas = []
for g, v in M.PROGRAMAS.items():
    linhas.append([f"Programa {g}"] + [br(x, 1) if x else "—" for x in M.TRI_PROG[g]] + [br(M.PROG_CUSTO[g])])
tabela(["Programa", "T1", "T2", "T3", "T4", "Total (R$ mil)"], linhas, ["l", "r", "r", "r", "r", "r"])
w("Desembolso mensal (R$ mil): " + "; ".join(f"m{k + 1} = {br(x, 1)}" for k, x in enumerate(M.MES_TOTAL) if x) + ". "
  f"O pico mensal é de R$ {br(max(M.MES_TOTAL), 1)} mil (m4). Em T2 o acumulado chega a {pct(100 * sum(M.TRI[:2]) / M.INV_PRIOR, 1)} do valor priorizado; T3 recebe só o final do P5 e T4 não tem desembolso de projeto, o que deixa o orçamento de T3-T4 livre para o G2.")
w()
w("![Curva de desembolso](img/fig04_curva_desembolso.png)")
w()
w(f"**Sensibilidade (H):** se 50% do P1 (R$ 450 mil, pedido de equipamentos) fosse pago nos meses 1 e 2, a distribuição seria T1 = R$ {br(M.TRI_ALT[0], 1)} mil, T2 = R$ {br(M.TRI_ALT[1], 1)} mil, T3 = R$ {br(M.TRI_ALT[2], 1)} mil. "
  "O total e o teto não mudam; o que muda é o fluxo de caixa de T1, que a Controladoria deve confirmar antes do pedido.")
w()
w("### 7.4 Composição da reserva gerencial (H)")
w()
tabela(["Uso previsto da reserva", "Valor (R$ mil)"], [[a, br(b)] for a, b in M.RESERVA_COMP] + [["**Total**", f"**{br(M.RESERVA)}**"]], ["l", "r"])
w("**Teste de adequação da reserva (valor monetário esperado, H):**")
w()
tabela(["Componente", "VME (R$ mil)"], [[a, br(b, 1)] for a, b in M.EMV] + [["**Total esperado**", f"**{br(M.EMV_TOTAL, 1)}**"]], ["l", "r"])
w(f"A reserva de R$ {br(M.RESERVA)} mil cobre {n2(M.RESERVA / M.EMV_TOTAL)} vez o valor esperado de {br(M.EMV_TOTAL)} mil, mas **não cobre** o pior caso de estouro do P1 (40% = R$ {br(0.4 * 900)} mil) somado ao do P2 (40% = R$ {br(0.4 * 450)} mil), que soma R$ {br(0.4 * 1350)} mil. "
  "Por isso a reserva é mantida sob gestão do PMO e liberada só por gatilho.")
w()
w("### 7.5 Composição por categoria de aquisição (H, a validar nas cotações)")
w()
linhas = []
for c, nome in M.CATS.items():
    linhas.append([nome] + [br(M.COMP[p].get(c, 0)) if M.COMP[p].get(c, 0) else "—" for p in M.PRIORIZADOS] + [br(M.CAT_TOTAL[c])])
linhas.append(["**Total**"] + [f"**{br(P[p]['inv'])}**" for p in M.PRIORIZADOS] + [f"**{br(M.INV_PRIOR)}**"])
tabela(["Categoria"] + M.PRIORIZADOS + ["Total (R$ mil)"], linhas, ["l"] + ["r"] * 6)

# ================================================================= 8
w("## 8. Etapa 4 — Recursos")
w()
w("### 8.1 Alocação adotada (carga % por profissional, por mês)")
w()
w("**Premissas (H):** 100% = dedicação integral de um profissional no mês; operação assistida e medição de benefícios após o m7; GP calculado por modelo de demanda (início de projeto 35%, execução 25%, encerramento 30% do tempo do GP, mais 10% de governança do portfólio e 15% de operação assistida a partir do m7), com os coordenadores locais assumindo 30% do esforço de gestão de cada projeto.")
w()
linhas = []
for r_, atv, i, f, pc in M.ALOC:
    linhas.append([r_, atv, f"m{i}-m{f}", f"{pc}%"])
linhas.append(["GP", "Gestão de programas (modelo de demanda)", "m1-m12", f"{min(M.MAT['GP'])}% a {M.PICO['GP']}%"])
tabela(["Recurso", "Atividade", "Meses", "Carga"], linhas, ["l", "l", "c", "r"])
w("**Matriz de carga (%) — plano adotado:**")
w()
tabela(["Recurso"] + mesnome + ["Pico"], [[f"**{r}**"] + [f"{v}" if v else "·" for v in M.MAT[r]] + [f"**{M.PICO[r]}%**"] for r in M.RECS], ["l"] + ["r"] * 13)
w("Verificação por script: **nenhuma célula acima de 100%**. Picos: EA1, EA2 e MAN em 100% no m1-m4 (EA1 e EA2 até o m6), TI1 em 100% no m3-m4, QUAL em 100% do m1 ao m7, GP em "
  f"{M.PICO['GP']}% no m1 (o recurso mais crítico é o GP, não por carga nominal, mas por ser único).")
w()
w("![Matriz de recursos: sem as decisões e plano adotado](img/fig05_matriz_recursos.png)")
w()
w("### 8.2 Conflitos encontrados e como foram resolvidos")
w()
w("O script primeiro monta um **cenário ingênuo** (os cinco projetos partem no m1, cada um com sua duração; o P2 usa 50% de um engenheiro de automação para a instrumentação; P6 no m1-m2) e acusa "
  f"**{len(M.CONF_ING)} células acima de 100%**. As decisões do grupo eliminam todas:")
w()
tabela(["Conflito no cenário ingênuo", "Carga sem decisão", "Decisão do grupo", "Efeito"], [
    ["EA1 e EA2 no P1 e o P2 pedindo engenheiro de automação", "150% (EA1, m1-m4)",
     "**Modificar o escopo:** P2 não usa EA; sensores e instrumentação são contratados dentro dos R$ 450 mil; EA só consultivo (até 4 h/sem)", "EA1 em 100% no P1; EA2 em 90% + 10% consultivo"],
    ["QUAL no P4 e no P5 ao mesmo tempo", "200% (m1-m3)", "**Alterar o cronograma:** P4 no m1-m3 e P5 no m4-m7, em sequência", "QUAL em 100% sem sobreposição"],
    ["MAN no P2 e no P6", "120% (m1-m2)", "**Alterar o cronograma:** P6 só depois do FAT do P1 (m5-m6), quando o P2 já terminou; MAN a 20%", "MAN em 100% até o m4 e 20% depois"],
    ["GP em cinco projetos simultâneos", "185% (m1)", "**Executar em sequência** (P5 e P6 mais tarde) e **coordenadores locais** por projeto; analista de planejamento externo pago pela reserva se o GP passar de 90% por 2 meses",
     f"GP no máximo em {M.PICO['GP']}% (sem coordenadores seria {round(max(M.GP_SEM_COORD))}% no m1)"],
    ["TI1 no P2 e no P1", "100% (m3-m4)", "**Aceito no limite:** P2 a 70% + P1 a 30%; TI2 como backup; sem demanda extra no m3-m4", "TI1 em 100%, sem folga (risco R09)"],
], ["l", "r", "l", "l"])
w("Conflito residual descoberto na checagem do próprio plano adotado: somando literalmente P1 a 100% e o consultivo do P2 (10%), **o EA2 chegaria a 110% no m1-m4**. O PMO resolve alocando o EA2 a **90% no P1 + 10% de consultoria ao P2**, "
  "o que tira 0,4 engenheiro-mês (3,3% dos 12 engenheiros-mês do P1) do projeto de risco alto. É um custo pequeno, mas real, e fica registrado como premissa a confirmar com a empresa.")
w()
w("### 8.3 O gerente de projetos como ponto único de falha")
w()
w("O enunciado dá **um** gerente de projetos para três projetos simultâneos nos m1-m4. Pelo modelo de demanda, sem apoio ele teria "
  f"{', '.join(f'm{k + 1} = {round(x)}%' for k, x in enumerate(M.GP_SEM_COORD[:6]))}, ou seja, **acima de 100% no m1** e perto do limite do m4 ao m6. "
  f"Com coordenadores locais (EA1 no P1, MAN no P2, QUAL no P4/P5) o pico cai para {M.PICO['GP']}%. Não há folga para absorver atraso: por isso o gatilho de contratar o analista de planejamento externo (R$ 55 mil da reserva) está definido e vira risco R02.")
w()
w("### 8.4 Se o G2 liberar o P7 (m7-m11)")
w()
w("Alocação adicional (H): EA1 a 40%, TI1 a 50% e TI2 a 30%, todos já livres do P1. Resultado por script: nenhuma célula acima de 100%.")
w()
tabela(["Recurso"] + mesnome[6:], [[f"**{r}**"] + [str(v) for v in M.MAT_P7[r][6:]] for r in M.RECS], ["l"] + ["r"] * 6)

# ================================================================= 9
w("## 9. Etapa 5 — Roadmap de 12 meses")
w()
w("### 9.1 Visão por trimestre e mês")
w()
cel = lambda p: "".join("██ " if M.JANELA[p][0] <= m <= M.JANELA[p][1] else "·  " for m in range(1, 13))


def bloco(p):
    i, f = M.JANELA[p]
    return ["██" if i <= m <= f else "" for m in range(1, 13)]


tabela(["Iniciativa"] + [f"T{t // 3 + 1}·m{t + 1}" if t % 3 == 0 else f"m{t + 1}" for t in range(12)],
       [[f"**{p}** {P[p]['nome']}"] + bloco(p) for p in ["P1", "P2", "P4", "P5", "P6"]] +
       [[f"**P7** {P['P7']['nome']} (condicional ao G2)"] + ["▒▒" if M.JANELA["P7"][0] <= m <= M.JANELA["P7"][1] else "" for m in range(1, 13)]] +
       [["Operação assistida e medição de benefícios"] + ["▓▓" if m >= 7 else "" for m in range(1, 13)]] +
       [["P3 e P8"] + ["fora do ciclo (adiados)"] + [""] * 11],
       ["l"] + ["c"] * 12)
w("██ = execução · ▒▒ = P7 só se o G2 aprovar · ▓▓ = hypercare e medição. As janelas respeitam o prazo do enunciado (P1 6 m, P2 4 m, P4 3 m, P5 4 m, P6 2 m, P7 5 m; conferido por script).")
w()
w("![Roadmap de 12 meses](img/fig03_roadmap_12_meses.png)")
w()
w("### 9.2 Marcos e gates")
w()
tabela(["Marco", "Fim do mês", "Descrição", "Critério de passagem"], [
    ["M1", "m1", "Linha de base de indicadores aprovada", "Produtividade, paradas, retrabalho, refugo e custo por peça medidos e aprovados pela Controladoria"],
    ["G1", "m3 (proposto pelo grupo)", "Gate 1: pedido de equipamentos do P1 emitido e P4 encerrado", "Contrato do P1 assinado e pedido emitido até o m2; P4 com plano de ações aceito"],
    ["FAT", "m4", "FAT do P1 aprovado (teste de aceitação em fábrica)", "Teste de integração e de segurança aprovados; libera o P6 e a instalação (m5)"],
    ["G2", "m6", "Gate 2: decide o P7", "Ver 9.3"],
    ["GL", "m6", "Go-live do P1 e aceite do P6", "SAT na Linha 1 e avaliação de competência dos operadores de 80% ou mais"],
    ["M9", "m9", "Balanço parcial de benefícios", "Comparação com a linha de base e com a trajetória até a meta"],
    ["M12", "m12", "Balanço final e proposta do ciclo 2027", "Decisão sobre P7, P3 e P8 com dados reais"],
], ["l", "l", "l", "l"])
w("### 9.3 Critérios do gate G2 (fim do m6)")
w()
tabela(["Dimensão", "Critério para liberar o P7"], [[a, b] for a, b in C.G2_CRITERIOS])
tabela(["Resultado do G2", "Ação"], [[a, b] for a, b in C.G2_RESULT])
w(f"**Um ponto de honestidade sobre o G2.** O P7 custa {mil(P['P7']['inv'])} e a reserva é de {mil(M.RESERVA)}. Mesmo sem usar nenhuma contingência, faltam R$ {br(P['P7']['inv'] - M.RESERVA)} mil; "
  "o P7 integral só cabe com **economias capturadas e auditadas** ou **complemento de orçamento aprovado pela diretoria**, e o total aprovado deixaria de respeitar o teto de R$ 2,5 mi. "
  "Por isso o G2 prevê o *Go faseado*. Saldo e falta por situação:")
w()
tabela(["Situação da reserva no G2", "Saldo (R$ mil)", "Falta para o P7 integral (R$ mil)"], [[a, br(b, 0), br(c, 0)] for a, b, c in C.saldo_g2()], ["l", "r", "r"])

# ================================================================= 10
w("## 10. Dependências tratadas")
w()
tabela(["Dependência (DADO)", "Natureza", "Tratamento no plano", "Efeito"], [[f"**{a}**", b, c, d] for a, b, c, d in C.DEPS])
w("**Condições de retorno dos adiados:** *P3* volta somente depois do P7 e com o balanço do m12 mostrando benefício real nos Programas A e B; *P8* volta com o balanço de produtividade do P1 (m9 e m12) e uma nova avaliação de capacidade.")
w()

# ================================================================= 11
w("## 11. Riscos")
w()
w("**Escalas (as da disciplina).** Probabilidade: 0,1 muito baixa; 0,3 baixa; 0,5 média; 0,7 alta; 0,9 muito alta. Impacto: 0,05 muito baixo; 0,10 baixo; 0,20 moderado; 0,40 alto; 0,80 muito alto "
  "(nos objetivos custo, tempo, escopo e qualidade, conforme o quadro de definição de escala de impacto da Aula 7). **Severidade = probabilidade × impacto.** Zonas (convenção do grupo, H): alta a partir de 0,18; média de 0,06 a 0,17; baixa abaixo de 0,06.")
w()
linhas = []
for r in M.RISCOS_DADOS:
    linhas.append([r["rank"], r["id"], f"**{r['titulo']}**", f"**Causa:** {r['causa']}. **Risco:** {r['risco']}. **Consequência:** {r['consequencia']}.",
                   br(r["prob"], 1), br(r["imp"], 2), r["tipo"], f"**{sev_fmt(r['sev'])}**", r["zona"]])
tabela(["#", "ID", "Risco", "Descrição (causa → risco → consequência)", "Prob.", "Impacto", "Objetivo afetado", "Severidade", "Zona"], linhas,
       ["c", "l", "l", "l", "r", "r", "l", "r", "l"])
w("### 11.1 Respostas, donos e gatilhos")
w()
linhas = []
for r in M.RISCOS_DADOS:
    linhas.append([r["id"], r["estrategia"], r["resposta"], r["dono"], r["gatilho"], "18/11/2026"])
tabela(["ID", "Estratégia", "Resposta e ação", "Dono", "Gatilho", "Inclusão"], linhas)
w("### 11.2 Matriz probabilidade × impacto")
w()
w("![Matriz de riscos](img/fig06_matriz_riscos.png)")
w()
w(f"Três riscos de severidade alta: **R03** (benefício parcial, 0,28), **R01** (P1, 0,20) e **R02** (GP, 0,20). Os três se reforçam: se o GP está sobrecarregado, o P1 atrasa e os benefícios saem abaixo do previsto. "
  "A resposta comum é monitoramento mensal contra a linha de base e uso dirigido da reserva. O risco R13 tem a maior probabilidade (0,9) e a menor severidade: é sabido e aceito, porque o G2 já prevê o escopo faseado. "
  "Riscos positivos (oportunidades), como economia superior à prevista no P4, não foram quantificados; entram no G2 como fonte de recurso.")
w()

# ================================================================= 12
w("## 12. Metas × benefício esperado (rastreabilidade e folga)")
w()
w("![Cobertura das metas pelo benefício quantificado](img/fig07_metas_vs_beneficio.png)")
w()
tabela(["Meta (DADO)", "Alvo", "Iniciativas", "Cobertura quantificada", "Folga", "Leitura honesta"], [list(l) for l in C.METAS_TAB])
w("### 12.1 Onde não há folga")
w()
w(f"- **Paradas (P2) e retrabalho (P5):** a meta só é atingida **se o benefício se realizar 100%**. Com 90% do prometido, as reduções seriam de 18% e 27%. A meta de produtividade, por sua vez, nem a 100% do P1 fecha: faltam {M.PRODUT_FALTA} p.p.")
w()
tabela(["Realização do benefício", "Produtividade (P1)", "Faltam para +15%", "Paradas (P2)", "Retrabalho (P5)"],
       [[pct(100 * s["r"]), f"+{br(s['prod'], 1)}%", f"{br(s['prod_falta'], 1)} p.p.", f"-{br(s['par'], 0)}%", f"-{br(s['ret'], 0)}%"] for s in M.SENS_BEN], ["r", "r", "r", "r", "r"])
w("### 12.2 Meta de custos: sensibilidade ilustrativa (H)")
w()
w(f"O enunciado não diz quanto do custo operacional é refugo, retrabalho ou parada. **Hipótese do grupo, a validar com a linha de base do m1:** refugo = {br(M.CUSTO_H['refugo'], 0)}%, retrabalho = {br(M.CUSTO_H['retrabalho'], 0)}% e paradas = {br(M.CUSTO_H['paradas'], 0)}% do custo operacional. "
  f"Com as reduções do enunciado (25%, 30% e 20%), os três projetos contribuiriam {br(M.CUSTO_CONTR['refugo'], 1)} + {br(M.CUSTO_CONTR['retrabalho'], 1)} + {br(M.CUSTO_CONTR['paradas'], 1)} = **{br(M.CUSTO_SOMA, 1)} p.p.** dos 10 da meta. "
  f"Os {br(M.CUSTO_RESTO, 1)} p.p. restantes teriam que vir do ganho de produtividade diluído no custo unitário: com +12% de produtividade, o custo unitário da parte sensível à produtividade cai {br(M.GANHO_UNIT_12, 1)}%, "
  f"e essa parte precisaria ser de pelo menos **{br(M.CUSTO_FRACAO_NEC_12, 0)}% do custo operacional**. Essa é a razão pela qual o PMO trata a meta de custos como **a menos demonstrável das quatro**.")
w()
w("### 12.3 Como medir e proteger")
w()
for t in C.PROTECOES:
    w(f"- {t}")
w()
tabela(["Meta", "Indicador (H)", "Linha de base", "Alvo (interno)", "Fonte e frequência", "Responsável"], [list(l) for l in C.IND])

# ================================================================= 13
w("## 13. Recomendação final do PMO")
w()
w(f"**Aprovar o portfólio do cenário A:** executar P1, P2, P4, P5 e P6 ({mil(M.INV_PRIOR)}, Programas A e B), manter {mil(M.RESERVA)} de reserva sob gestão do PMO, tratar o P7 como posterior com decisão no gate G2 (fim do m6) e adiar P3 e P8 com condição de retorno.")
w()
w("**Pedido à diretoria (o que precisamos decidir hoje):**")
w()
w(f"1. Aprovar {mil(M.INV_PRIOR)} para P1, P2, P4, P5 e P6 e a reserva de {mil(M.RESERVA)} sob gestão do PMO, liberável por gatilho.")
w("2. Nomear a Controladoria para fechar a linha de base de indicadores até o fim do m1.")
w("3. Confirmar os gates G1 (fim do m3) e G2 (fim do m6) no calendário da diretoria e os critérios do G2.")
w("4. Autorizar coordenadores locais por projeto e, se o gatilho ocorrer, o analista de planejamento externo (R$ 55 mil da reserva).")
w()
w("**Por que esta é a estratégia certa:** é a única combinação dentro do teto que ataca as quatro metas com algum benefício quantificado; usa os recursos escassos em sequência, sem estourar nenhum profissional; "
  "começa por ganhos rápidos (P4, P2) e deixa o projeto de maior risco (P1) com colchão de 16%; e transforma o que ainda não sabemos (P7, P3, P8) em decisão futura com critério, não em aposta.")
w()
w("**Limites que o PMO assume diante da diretoria:** (1) P2 e P5 entregam exatamente a meta, sem folga; (2) a meta de +15% de produtividade depende de efeitos que o enunciado não quantifica; (3) a meta de custos depende de uma linha de base ainda inexistente; (4) o P7 não cabe integral sem complemento; (5) o plano tem um único gerente de projetos.")
w()

# ================================================================= anexos
w("## Anexo A — Premissas do grupo (H) a confirmar")
w()
for t in [
    "Pesos da matriz de priorização, rubrica das notas e zonas de severidade dos riscos.",
    "Desembolso linear mês a mês ao longo da duração de cada projeto; composição da reserva; composição do orçamento por categoria de aquisição.",
    "Modelo de demanda do GP (35/25/30% por fase, 10% de governança, 15% de operação assistida, 70% com coordenadores locais).",
    "Cargas de operação assistida, sustentação e medição de benefícios (m7-m12) e cargas do P7 se aprovado.",
    "EA2 a 90% no P1 mais 10% de consultoria ao P2 no m1-m4 (para não passar de 100%).",
    "Gate G1 no fim do m3 e FAT no fim do m4; janela do P7 em m7-m11.",
    "Percentuais de refugo, retrabalho e paradas no custo operacional (apenas na sensibilidade da meta de custos).",
    "O ganho de +12% do P1 refere-se ao indicador de produtividade que a diretoria acompanha; se a Linha 1 for só parte da fábrica, o efeito na meta é menor (a linha de base do m1 define isso).",
]:
    w(f"- {t}")
w()
w("## Anexo B — Glossário")
w()
tabela(["Termo", "Significado"], [
    ["EA1, EA2, TI1, TI2, QUAL, MAN, GP", "Engenheiros de automação, analistas de TI, especialista em qualidade, especialista em manutenção e gerente de projetos"],
    ["FAT / SAT", "Teste de aceitação em fábrica (no fornecedor) / teste de aceitação no local de operação"],
    ["G1 / G2", "Gates (pontos de decisão do comitê) no fim do m3 e no fim do m6"],
    ["SPI", "Índice de desempenho de prazo (valor agregado ÷ valor planejado); abaixo de 1 indica atraso"],
    ["VME", "Valor monetário esperado: probabilidade × impacto em R$"],
    ["p.p.", "Ponto percentual"],
    ["CLP / CEP", "Controlador lógico programável / controle estatístico de processo"],
    ["NR-12", "Norma Regulamentadora de segurança em máquinas e equipamentos"],
    ["MTBF", "Tempo médio entre falhas"],
], ["l", "l"])
w("## Anexo C — Como reproduzir os números")
w()
w("```bash")
w("cd scripts")
w("python3 modelo_portfolio.py   # (saída salva em saida_verificacao.txt) imprime pontuações, cenários, orçamento, matriz de recursos, riscos e checagens (assert)")
w("python3 gerar_figuras.py      # figuras em ../img/")
w("python3 gerar_md.py           # regenera este documento")
w("```")
w()
w("Checagens automáticas (falham o script se violadas): durações = prazos do enunciado; notas de risco, prazo e benefício/custo conforme a regra; top 5 da matriz = priorizados; "
  "priorizados = 2.100 mil e reserva = 400 mil; categorias somam o investimento de cada projeto; reserva decomposta = 400 mil; nenhuma célula de carga acima de 100% no plano adotado e no plano com P7.")
w()

OUT.write_text("\n".join(L), encoding="utf-8")
print("gerado", OUT, len(L), "linhas")
