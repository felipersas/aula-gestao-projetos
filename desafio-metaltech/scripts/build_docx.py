#!/usr/bin/env python3
"""Monta relatorio-final-metaltech.docx sobre o Template - Relatorio Final.docx do professor.

Mantem: capa, folha de rosto, estilos, margens, estrutura 1-13 + referencias + apendice/anexo.
Substitui todo o texto de exemplo. Numeros vem de modelo_portfolio.py; textos tabulares, de conteudo.py.
"""
import copy
import re
import shutil
import sys
import zipfile
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

import conteudo as C
import docx_lib as D
import modelo_portfolio as M
from conteudo import br, mil, n2, pct

RAIZ = Path(__file__).resolve().parent.parent
IMG = RAIZ / "img"
TEMPLATE = Path("/Users/felipersas/Documents/Facul/gestao-proj/material/Template/Template - Relatório Final.docx")
SAIDA = RAIZ / "relatorio-final-metaltech.docx"
P = M.PROJ
J = WD_ALIGN_PARAGRAPH.JUSTIFY
CEN = WD_ALIGN_PARAGRAPH.CENTER
LEFT = WD_ALIGN_PARAGRAPH.LEFT

TITULO = "GESTÃO DE PORTFÓLIO E PROGRAMAS: PROPOSTA DO PMO PARA A METALTECH S.A. NOS PRÓXIMOS 12 MESES"

doc = Document(str(TEMPLATE))
body = doc.element.body
filhos = list(body)
assert len(filhos) == 349, len(filhos)


# ------------------------------------------------------------------ capa e folha de rosto
def set_text(par_el, texto):
    """troca o texto do primeiro run com texto, preserva formatacao."""
    runs = par_el.findall(qn("w:r"))
    primeiro = True
    for r in runs:
        ts = r.findall(qn("w:t"))
        for t in ts:
            if primeiro:
                t.text = texto
                primeiro = False
            else:
                t.text = ""


def clone_after(el, texto):
    novo = copy.deepcopy(el)
    set_text(novo, texto)
    el.addnext(novo)
    return novo


def tira_vazios(inicio, n):
    """remove n paragrafos vazios a partir do indice 'inicio' (indices do template)."""
    for k in range(inicio, inicio + n):
        el = filhos[k]
        assert not "".join(t.text or "" for t in el.iter(qn("w:t"))).strip(), k
        body.remove(el)


def capa():
    for idx_nome, idx_tit, vazios_nome, vazios_tit in ((9, 17, (10, 4), (18, 3)), (29, 37, (30, 4), (38, 3))):
        nomes = C.GRUPO
        set_text(filhos[idx_nome], nomes[0])
        anterior = filhos[idx_nome]
        for n in nomes[1:]:
            anterior = clone_after(anterior, n)
        set_text(filhos[idx_tit], TITULO)
        tira_vazios(*vazios_nome)
        tira_vazios(*vazios_tit)


def sem_cor_marca(el):
    for c in el.iter(qn("w:color")):
        c.getparent().remove(c)


sem_cor_marca(filhos[27])
sem_cor_marca(filhos[57])
assert len(M.SUBS_4METAS) == 1
capa()

# ------------------------------------------------------------------ remove o miolo do template (indices 59 a 347); mantem sectPr
for el in filhos[59:348]:
    body.remove(el)
# limpa relacoes (imagem da Amazonia e hyperlinks do sumario) apos montar o documento

# ------------------------------------------------------------------ estado
CAP = {"Figura": [], "Tabela": [], "Quadro": []}
TOC = []  # (nivel, texto)
CONT = {"Figura": 0, "Tabela": 0, "Quadro": 0}


def par(texto="", size=12, align=J, first=1.27, line=1.5, before=0, after=6, bold=False, italic=False, keep_next=False, left=None, hanging=None):
    p = doc.add_paragraph()
    D.pfmt(p, align=align, line=line, before=before, after=after, first=first if hanging is None else None, left=left, hanging=hanging, keep_next=keep_next)
    if texto:
        D.add_runs(p, texto, size=size, bold=bold, italic=italic)
    return p


def corpo(texto):
    return par(texto)


def alineas(itens, ultimo_ponto=True):
    for i, t in enumerate(itens):
        letra = "abcdefghijklmnopqrstuvwxyz"[i]
        fim = "." if i == len(itens) - 1 else ";"
        t = t.rstrip(".;")
        par(f"{letra}) {t}{fim}", first=None, left=1.9, hanging=0.63, after=3)


def h1(texto, quebra=True):
    p = doc.add_paragraph(style="Heading 1")
    D.pfmt(p, line=1.5, before=0, after=12, page_break_before=quebra, keep_next=True)
    r = p.add_run(texto)
    D.set_font(r, 12, True)
    TOC.append((1, texto))
    return p


def h2(texto):
    p = doc.add_paragraph(style="Heading 2")
    D.pfmt(p, line=1.5, before=12, after=6, keep_next=True)
    r = p.add_run(texto)
    D.set_font(r, 12, True)
    TOC.append((2, texto))
    return p


def h3(texto):
    p = doc.add_paragraph(style="Heading 3")
    D.pfmt(p, line=1.5, before=6, after=3, keep_next=True)
    r = p.add_run(texto)
    D.set_font(r, 12, True, True)
    return p


REFMAP = {}


def legenda(tipo, titulo, key=None):
    CONT[tipo] += 1
    n = CONT[tipo]
    CAP[tipo].append((n, titulo))
    if key:
        assert key not in REFMAP, key
        REFMAP[key] = (tipo, n)
    p = doc.add_paragraph()
    D.pfmt(p, align=CEN, line=1.0, before=10, after=4, keep_next=True)
    D.add_runs(p, f"{tipo} ", size=11, bold=True)
    D.fld_runs(p, f"SEQ {tipo} \\* ARABIC", str(n), size=11, bold=True)
    D.add_runs(p, f" – {titulo}", size=11, bold=True)
    return p


def fonte(texto="Elaborado pelos autores (2026)."):
    p = doc.add_paragraph()
    D.pfmt(p, align=CEN, line=1.0, before=3, after=12)
    D.add_runs(p, "Fonte: " + texto, size=10)
    return p


def figura(arquivo, titulo, largura_cm=16.0, fonte_txt="Elaborado pelos autores (2026), com base nos dados do enunciado e nos cálculos do Apêndice B.", key=None):
    legenda("Figura", titulo, key)
    p = doc.add_paragraph()
    D.pfmt(p, align=CEN, line=1.0, before=0, after=0, keep_next=True)
    p.add_run().add_picture(str(IMG / arquivo), width=Cm(largura_cm))
    fonte(fonte_txt)


def tabela(titulo, cab, linhas, widths, kind="Tabela", fonte_txt="Elaborado pelos autores (2026).", key=None, **kw):
    legenda(kind, titulo, key)
    t = D.make_table(doc, cab, linhas, widths, kind=kind, **kw)
    fonte(fonte_txt)
    return t


def w_(cm_list):
    """converte larguras em cm para twips ajustando a soma ao TEXT_W."""
    tot = sum(cm_list)
    tw = [round(c / tot * D.TEXT_W) for c in cm_list]
    tw[-1] += D.TEXT_W - sum(tw)
    return tw


def sev_fmt(x):
    return br(x, 3) if round(x * 1000) % 10 else br(x, 2)


FONTE_ENUN = "dados do enunciado do desafio (material da disciplina)."
FONTE_PROPRIA = "Elaborado pelos autores (2026)."


# =====================================================================================
#  PRE-TEXTUAIS
# =====================================================================================
def titulo_pre(texto, quebra=True):
    p = doc.add_paragraph()
    D.pfmt(p, align=CEN, line=2.0, before=0, after=0, page_break_before=quebra)
    D.add_runs(p, texto, size=14, bold=True)
    return p


RESUMO = (
    "Este trabalho apresenta a proposta do PMO da MetalTech S.A., fabricante fictícia de componentes metálicos para os setores automotivo e de máquinas industriais, "
    "para organizar o portfólio de projetos dos próximos 12 meses. A empresa avalia oito projetos que somam R$ 5,4 milhões, mas dispõe de R$ 2,5 milhões e de uma equipe limitada, "
    "e precisa atingir quatro metas: aumentar a produtividade em 15%, reduzir as paradas em 20%, reduzir os custos operacionais em 10% e reduzir o retrabalho em 30%. "
    "Os projetos foram avaliados por uma matriz de priorização ponderada em seis critérios, por cenários alternativos e por verificações de recursos e riscos, com todas as contas feitas em scripts. "
    f"A proposta prioriza P1, P2, P4, P5 e P6, que somam {mil(M.INV_PRIOR)} e formam os programas Excelência Operacional e Qualidade 4.0, mantém {mil(M.RESERVA)} de reserva gerencial, "
    "deixa o P7 para depois de um gate no sexto mês e adia o P3 e o P8. Os conflitos de recursos são resolvidos por sequenciamento e alteração de escopo, os 14 riscos identificados têm resposta e dono, "
    "e o relatório declara onde as metas não têm folga: paradas e retrabalho dependem de 100% do benefício prometido e a produtividade depende de efeitos ainda não quantificados. "
    "Conclui-se que a combinação proposta é a única, dentro do teto, que atribui a cada meta um projeto com benefício quantificado, desde que a linha de base dos indicadores seja fechada no primeiro mês."
)
ABSTRACT = (
    "This paper presents the PMO proposal for MetalTech S.A., a fictional manufacturer of metal components for the automotive and industrial machinery sectors, "
    "to organize its project portfolio for the next 12 months. The company is evaluating eight projects totaling BRL 5.4 million, but has a budget of BRL 2.5 million and a limited team, "
    "and must reach four targets: a 15% increase in productivity, a 20% reduction in downtime, a 10% reduction in operating costs and a 30% reduction in rework. "
    "The projects were assessed with a six-criteria weighted prioritization matrix, alternative scenarios, and resource and risk checks, with all calculations done in scripts. "
    f"The proposal prioritizes projects P1, P2, P4, P5 and P6, which total BRL {br(M.INV_PRIOR / 1000, 1)} million and form the Operational Excellence and Quality 4.0 programs, keeps BRL {br(M.RESERVA / 1000, 1)} million as a management reserve, "
    "defers P7 until a decision gate in month six, and postpones P3 and P8. Resource conflicts are solved by sequencing and scope changes, the 14 identified risks have responses and owners, "
    "and the report states where the targets have no slack: downtime and rework depend on 100% of the promised benefit, and productivity depends on effects that are not yet quantified. "
    "The proposed combination is the only one within the ceiling that gives each target a project with a quantified benefit, provided that the indicator baseline is closed in the first month."
)

titulo_pre("RESUMO", quebra=False)
par("", after=0)
par(RESUMO, first=1.25, line=1.0, after=12)
par("**Palavras-chave:** Gestão de portfólio; Gestão de programas; Priorização de projetos; PMO; Indústria metal-mecânica.", first=None, line=1.0)

titulo_pre("ABSTRACT")
par("", after=0)
par(ABSTRACT, first=1.25, line=1.0, after=12)
par("**Keywords:** Portfolio management; Program management; Project prioritization; PMO; Metalworking industry.", first=None, line=1.0)

# listas de ilustracoes, tabelas, quadros: preenchidas depois (marcadores); guarda posicao
LISTAS = {}
for chave, tit in (("Figura", "LISTA DE ILUSTRAÇÕES"), ("Tabela", "LISTA DE TABELAS"), ("Quadro", "LISTA DE QUADROS")):
    titulo_pre(tit)
    LISTAS[chave] = doc.add_paragraph()  # placeholder (substituido ao final)
    D.pfmt(LISTAS[chave], line=1.0, after=0)

ABREV = [
    ("Dir.", "Diretoria"), ("Contr.", "Controladoria"), ("m1 a m12", "mês 1 a mês 12 do horizonte de 12 meses"), ("mi", "milhões"),
    ("p.p.", "ponto percentual"), ("T1 a T4", "trimestres 1 a 4 (T1 = meses 1 a 3; T4 = meses 10 a 12)"), ("VME", "valor monetário esperado"),
    ("EA1, EA2", "engenheiros de automação"), ("TI1, TI2", "analistas de TI"), ("QUAL", "especialista em qualidade"), ("MAN", "especialista em manutenção"),
    ("GP", "gerente de projetos"),
]
SIGLAS = [
    ("ABNT", "Associação Brasileira de Normas Técnicas"), ("CEP", "Controle estatístico de processo"), ("CLP", "Controlador lógico programável"),
    ("EAP", "Estrutura analítica do projeto"), ("ERP", "Enterprise resource planning (sistema integrado de gestão)"), ("FAT", "Factory acceptance test (teste de aceitação em fábrica)"),
    ("G1, G2", "Gates (pontos de decisão) 1 e 2"), ("IoT", "Internet das coisas"), ("MTBF", "Mean time between failures (tempo médio entre falhas)"),
    ("NR-12", "Norma Regulamentadora 12, segurança em máquinas e equipamentos"), ("PMBOK", "Project Management Body of Knowledge"), ("PMI", "Project Management Institute"),
    ("PMO", "Project Management Office (escritório de projetos)"), ("RACI", "Responsible, Accountable, Consulted, Informed"), ("SAT", "Site acceptance test (teste de aceitação no local)"),
    ("SPI", "Schedule performance index (índice de desempenho de prazo)"), ("TI", "Tecnologia da informação"), ("UniSENAI-SP", "Centro Universitário SENAI São Paulo"),
]


def lista_sigla(tit, itens):
    titulo_pre(tit)
    for a, b in itens:
        p = doc.add_paragraph()
        D.pfmt(p, align=LEFT, line=1.15, before=0, after=4, left=3.2, hanging=3.2)
        D.add_runs(p, f"**{a}**\t{b}", size=12)
        pPr = p._p.get_or_add_pPr()
        tabs = OxmlElement("w:tabs")
        tb = OxmlElement("w:tab")
        tb.set(qn("w:val"), "left")
        tb.set(qn("w:pos"), str(round(3.2 * 567)))
        tabs.append(tb)
        pPr.append(tabs)


lista_sigla("LISTA DE ABREVIATURAS", ABREV)
lista_sigla("LISTA DE SIGLAS", SIGLAS)

titulo_pre("SUMÁRIO")
SUMARIO = doc.add_paragraph()
D.pfmt(SUMARIO, line=1.0, after=0)

# fim da secao pre-textual: nova secao (numeracao de pagina visivel a partir da Introducao)
doc.add_section(WD_SECTION.NEW_PAGE)

# =====================================================================================
#  1 INTRODUCAO
# =====================================================================================
h1("1 INTRODUÇÃO", quebra=False)
h2("1.1. Contextualização do Problema")
corpo("A MetalTech S.A. é uma indústria fictícia fabricante de componentes metálicos para os setores automotivo e de máquinas industriais. A empresa está em processo de modernização "
      "e tem oito projetos estratégicos em avaliação, que cobrem automação, manutenção, qualidade, treinamento, sistemas de informação e ampliação de capacidade. "
      f"O problema é que a carteira inteira custaria {mil(M.TOTAL_CARTEIRA)}, {n2(M.TOTAL_CARTEIRA / M.ORCAMENTO_TETO)} vezes o orçamento de {mil(M.ORCAMENTO_TETO)} aprovado pela diretoria para os próximos 12 meses, "
      "e a empresa também não tem pessoas especializadas para tocar tudo ao mesmo tempo. A diretoria pediu ao PMO uma proposta de gestão do portfólio.")
corpo("A diretoria definiu quatro objetivos estratégicos para o ano, resumidos na @T:obj@. As decisões do PMO precisam ser julgadas contra essas metas, e não apenas contra o custo de cada projeto.")
tabela("Objetivos estratégicos e metas da MetalTech S.A. para os próximos 12 meses", ["Objetivo estratégico", "Meta"],
       [["Aumentar a produtividade", "+15%"], ["Reduzir paradas de produção", "-20%"], ["Reduzir custos operacionais", "-10%"], ["Melhorar a qualidade", "-30% de retrabalho"]],
       w_([9, 5]), kind="Tabela", fonte_txt=FONTE_ENUN, size=10, align=["l", "c"], key="obj")
corpo("As restrições são de três tipos. Financeira: R$ 2,5 milhões como teto para a soma dos investimentos dos projetos selecionados. De pessoas: dois engenheiros de automação, dois analistas de TI, "
      "um especialista em qualidade, um gerente de projetos e um especialista em manutenção, que não podem assumir dedicações incompatíveis ao mesmo tempo. "
      "De relações entre projetos: o P1 se relaciona ao P6, o P3 ao P7, o P4 ao P5, e a empresa recomenda executar o P1 antes ou junto do P8. "
      "Os dados completos dos oito projetos estão no Anexo A. Como o enunciado diz, não há uma única resposta correta: o que se espera é uma decisão coerente, viável e justificada.")

h2("1.2. Justificativa e Objetivos")
corpo("Quando a demanda por projetos supera o orçamento e as pessoas, escolher por pressão da área mais ativa ou pelo projeto mais atraente isoladamente leva a uma carteira dispersa, "
      "com recursos pulverizados e metas descobertas. A gestão de portfólio existe para evitar isso: segundo o Project Management Institute, o portfólio reúne projetos e programas "
      "gerenciados em conjunto para atingir objetivos estratégicos, e sua gestão seleciona, prioriza e equilibra os componentes de acordo com a estratégia e a capacidade da organização (PMI, 2017a). "
      "A gestão de programas, por sua vez, coordena projetos relacionados para obter benefícios que não seriam obtidos se fossem geridos separadamente (PMI, 2017b).")
corpo("No caso da MetalTech, a decisão tem consequências concretas. Há projetos que dependem de outros, há um único gerente de projetos e há quatro metas, das quais pelo menos duas só têm um projeto com benefício declarado. "
      "Sem uma análise integrada, o risco é gastar o orçamento em projetos de benefício indireto e deixar uma meta sem responsável.")
corpo("O **objetivo geral** deste trabalho é propor à diretoria da MetalTech um portfólio de projetos para os próximos 12 meses que alcance os objetivos estratégicos com os recursos disponíveis. "
      "Os **objetivos específicos** são:")
alineas(["analisar os oito projetos quanto a investimento, prazo, risco, benefício, alinhamento estratégico, dependências e necessidade de recursos",
         "classificar os projetos em prioridade, posterior e adiado, e comparar cenários alternativos",
         "estruturar programas com os projetos selecionados e definir o objetivo e o benefício esperado de cada um",
         "distribuir o orçamento por projeto, programa e trimestre, respeitando o teto de R$ 2,5 milhões",
         "organizar os recursos humanos, identificar conflitos e decidir como resolvê-los",
         "elaborar o roadmap de 12 meses com marcos e gates, e analisar os riscos da estratégia",
         "demonstrar a rastreabilidade entre as metas e os benefícios esperados, deixando claro onde não há folga"])

h2("1.3. Metodologia Utilizada")
corpo("O trabalho foi feito em seis etapas. Primeiro, os dados do enunciado foram organizados e deles se derivaram indicadores: percentual do teto, custo por ponto percentual de meta e cobertura de cada meta. "
      "Segundo, os projetos foram pontuados em uma matriz de priorização ponderada, com seis critérios, pesos definidos pelo grupo e notas de 1 a 5 com rubrica explícita. "
      "Terceiro, a matriz foi submetida a um teste de sensibilidade e confrontada com cenários alternativos e com a enumeração de todos os subconjuntos de projetos que cabem no teto. "
      "Quarto, os projetos priorizados foram agrupados em programas e tiveram escopo, cronograma, orçamento, qualidade, recursos, comunicações, riscos, aquisições e partes interessadas detalhados nos capítulos 2 a 11. "
      "Quinto, a carga de cada profissional foi calculada mês a mês para detectar conflitos. Sexto, as metas foram rastreadas até os benefícios, com análise de sensibilidade à realização parcial do benefício.")
corpo("As ferramentas foram a matriz de priorização, a estrutura analítica do projeto, o roadmap, a matriz de responsabilidades (RACI), o plano de comunicações, a matriz de probabilidade e impacto, "
      "a matriz de poder e interesse e a tabela de aquisições, conforme as áreas de conhecimento do Guia PMBOK (PMI, 2013) e o conteúdo da disciplina (CARVALHO, 2018; SOUZA, 2020). "
      "A síntese de uma página que abre a apresentação à diretoria segue a ideia de visão visual de projeto defendida por Finocchio Júnior (2013), e os ritos curtos e frequentes de acompanhamento "
      "são comuns nas abordagens que combinam práticas ágeis ao PMBOK (CRUZ, 2013). Todas as contas foram feitas em scripts Python, entregues junto com o relatório, e os resultados são reproduzíveis.")
corpo("**Convenção de rastreabilidade.** Neste relatório, \"dado do enunciado\" é a informação fornecida no desafio; \"hipótese\" (H) é uma premissa do grupo que precisa ser validada com a MetalTech, "
      "como os pesos da matriz, a curva de desembolso e a composição do orçamento. As hipóteses estão listadas no Apêndice B. Valores em reais usam R$ mil ou R$ mi (milhões), e os meses do horizonte são identificados como m1 a m12.")

# =====================================================================================
#  2 INTEGRACAO
# =====================================================================================
h1("2 GERENCIAMENTO DA INTEGRAÇÃO")
corpo("Este capítulo mostra como o portfólio foi estruturado a partir dos objetivos estratégicos, quais decisões foram tomadas e como portfólio, programas e projetos se integram "
      "em dependências, prioridades, recursos, custos, prazos e benefícios.")
h2("2.1 Estrutura e Direcionamento do Portfólio")
corpo("A estrutura segue a lógica do enunciado: o portfólio da MetalTech reúne programas, e os programas reúnem projetos, cada um ligado a pelo menos uma meta estratégica. "
      "A @F:estrutura@ mostra a estrutura proposta, e o @Q:rastreab@ liga cada meta ao programa e ao projeto que a atende.")
figura("fig01_estrutura_portfolio.png", "Estrutura proposta para o portfólio da MetalTech S.A.", 16.0, key="estrutura")
tabela_q1 = [
    ["Aumentar a produtividade (+15%)", "A, Excelência Operacional", "P1 (+12%); P6 e efeitos de P2 e P4 sem valor declarado"],
    ["Reduzir paradas (-20%)", "A, Excelência Operacional", "P2 (-20% de paradas)"],
    ["Reduzir custos operacionais (-10%)", "B, Qualidade 4.0", "P4 (-25% de desperdício); efeitos indiretos de P5, P2 e P1"],
    ["Reduzir retrabalho (-30%)", "B, Qualidade 4.0", "P5 (-30% de retrabalho); P4 complementar"],
]
tabela("Rastreabilidade entre metas, programas e projetos priorizados", ["Meta estratégica", "Programa", "Projetos e benefício declarado"], tabela_q1,
       w_([5, 4, 7]), kind="Quadro", fonte_txt="Elaborado pelos autores (2026), com base em " + FONTE_ENUN, size=9.5, key="rastreab")
h3("Critérios de priorização")
corpo("Cada projeto foi pontuado em seis critérios, com pesos definidos pelo grupo (H): alinhamento estratégico (35%), relação benefício/custo (20%), risco (15%), prazo e rapidez de retorno (10%), "
      "sinergia e dependências (10%) e viabilidade de recursos (10%). O peso maior do alinhamento reflete o pedido da diretoria de que as decisões considerem os quatro objetivos. "
      "As notas vão de 1 a 5, sendo 5 a melhor, e seguem a rubrica do @Q:rubrica@. As notas de risco, prazo e benefício/custo aplicam regra objetiva sobre os dados do enunciado; "
      "as de alinhamento, sinergia e recursos são julgamento do grupo, justificado no Apêndice C.")
tabela("Rubrica das notas da matriz de priorização", ["Critério (peso)", "Rubrica (nota 5 a 1)"], [[a, b] for a, b in C.RUBRICA], w_([4, 12]), kind="Quadro", size=8.5, key="rubrica")
cab = ["Projeto", "Alinh.", "B/C", "Risco", "Prazo", "Sinerg.", "Recur.", "Pont.", "Pos.", "Decisão"]
linhas = [[f"{p} {P[p]['nome']}"] + [str(M.NOTAS[p][k]) for k, _, _ in M.CRIT] + [n2(M.SCORE[p]), f"{M.RANK.index(p) + 1}º", M.DECISAO[p]] for p in M.RANK]
tabela("Notas, pontuação ponderada e decisão dos oito projetos", cab, linhas, w_([3.9, 1.25, 1.1, 1.35, 1.35, 1.55, 1.4, 1.3, 1.1, 2.0]), kind="Tabela", size=8.5,
       align=["l"] + ["c"] * 9, bold_rows=(), fonte_txt="Elaborado pelos autores (2026), com cálculo em scripts/modelo_portfolio.py. Alinh.: alinhamento estratégico (35%); B/C: benefício/custo (20%); Risco (15%); Prazo (10%); Sinerg.: sinergia (10%); Recur.: viabilidade de recursos (10%); Pont.: pontuação; Pos.: posição.", key="notas")
figura("fig02_matriz_priorizacao.png", "Matriz de priorização ponderada: notas por critério e pontuação final", 16.0, key="priorizacao")
corpo("A @T:notas@ e a @F:priorizacao@ apresentam o resultado da pontuação.")
corpo(f"O resultado coloca P4 ({n2(M.SCORE['P4'])}), P5 ({n2(M.SCORE['P5'])}), P2 ({n2(M.SCORE['P2'])}), P6 ({n2(M.SCORE['P6'])}) e P1 ({n2(M.SCORE['P1'])}) nas cinco primeiras posições, "
      f"seguidos por P7 ({n2(M.SCORE['P7'])}), P8 ({n2(M.SCORE['P8'])}) e P3 ({n2(M.SCORE['P3'])}). Os cinco primeiros são exatamente os projetos priorizados. "
      f"O P1 é o quinto e não o primeiro: entra na carteira pelo alinhamento (é a única fonte quantificada de produtividade) e pela sinergia com o P6, apesar de ser o pior em risco, custo por ponto percentual e uso de recursos; "
      f"a margem sobre o P7 é de {n2(M.SCORE['P1'] - M.SCORE['P7'])} ponto. Por isso a matriz não foi usada sozinha.")
corpo(f"O teste de sensibilidade variou cada peso em 10 pontos percentuais para mais e para menos (12 casos) e usou quatro perfis alternativos de pesos (iguais, foco em custo, foco em risco e foco estratégico). "
      f"Em nenhum dos 16 casos o conjunto das cinco primeiras posições mudou. Em 20.000 sorteios aleatórios de pesos em torno dos pesos-base, o conjunto prioritário se repetiu em {pct(100 * M.MC_TOP5, 1)} das vezes, "
      "e o P1 superou o P7 no mesmo percentual.")
h3("Cenários alternativos")
corpo("Como a matriz é subjetiva, o grupo também enumerou por script todos os 255 subconjuntos possíveis de projetos. "
      f"Destes, {sum(1 for r in range(1, 9) for ps in __import__('itertools').combinations(M.PROJ, r) if sum(P[p]['inv'] for p in ps) <= M.ORCAMENTO_TETO)} cabem no teto e {len(M.SUBS)} também respeitam as dependências recomendadas. "
      "Entre eles, o único que cobre as quatro metas com benefício quantificado diretamente no enunciado é o cenário A, escolhido. O @Q:cenarios@ compara A com os três cenários que o grupo considerou.")
descr = {"A": "Escolhido. Cobre as 4 metas e deixa 16% de reserva para o projeto de risco alto.",
         "B": "Consome 98% do teto, sem reserva, e dispensa o P4: sem a vitória rápida de refugo e com o P1 sem colchão. Rejeitado.",
         "C": "Barato e de risco baixo, quase empata na pontuação, mas sem o P1 nenhuma meta de produtividade tem projeto com ganho declarado. Rejeitado.",
         "D": "Só projetos de risco alto, deixa paradas, retrabalho e custos sem projeto e o benefício do P8 chega depois do horizonte. Rejeitado."}
linhas = []
for k in "ABCD":
    c = M.CENARIOS[k]
    linhas.append([k, " + ".join(c["projetos"]), mil(c["custo"]), pct(c["pct"]), mil(c["reserva"]), f"{c['n_metas']} de 4", descr[k]])
tabela("Comparação dos cenários A, B, C e D", ["Cen.", "Projetos", "Custo", "% do teto", "Reserva", "Metas (direto)", "Avaliação"], linhas,
       w_([1, 3.2, 1.6, 1.3, 1.6, 1.5, 5.8]), kind="Quadro", size=8.5, align=["c", "l", "r", "r", "r", "c", "l"],
       fonte_txt="Elaborado pelos autores (2026). Incluir o P8 ao cenário A custaria " + mil(M.ESTOURO_A_MAIS_P8) + ", " + mil(M.ESTOURO_A_MAIS_P8 - M.ORCAMENTO_TETO) + " acima do teto.", key="cenarios")
h3("Classificação do portfólio")
cls = [
    ["P1 Automação da Linha 1", mil(900), "Prioridade", "Única fonte quantificada de produtividade (+12%); precisa do P6 e antecede o P8."],
    ["P2 Manutenção Preditiva", mil(450), "Prioridade", "Entrega sozinho a meta de -20% de paradas."],
    ["P4 Redução de Refugo", mil(250), "Prioridade", "Vitória rápida (3 meses, risco baixo); alimenta custos e o P5."],
    ["P5 Controle de Qualidade", mil(350), "Prioridade", "Entrega sozinho a meta de -30% de retrabalho; complementar ao P4."],
    ["P6 Treinamento de Operadores", mil(150), "Prioridade", "Barato e de risco baixo; habilita a adoção do P1."],
    ["P7 Monitoramento IoT", mil(600), "Posterior", "Habilitador, mas não cabe com reserva; gate G2 no fim do m6."],
    ["P3 Novo ERP Industrial", mil(1200), "Adiado", "Alto risco, 10 meses, benefício indireto, depende do P7."],
    ["P8 Expansão da Capacidade", mil(1500), "Adiado", "60% do teto e 12 meses; risco alto; sem meta direta; medir o P1 primeiro."],
]
tabela("Classificação dos projetos e racional da decisão", ["Projeto", "Investimento", "Classificação", "Racional"], cls, w_([4.2, 2.1, 2.2, 7.5]), kind="Quadro", size=9,
       align=["l", "r", "c", "l"], key="classif")
corpo("Nenhum projeto foi descartado. O P3 e o P8 ficam adiados com condição de retorno definida no capítulo 12.")

h2("2.2 Integração entre Portfólio, Programas e Projetos")
corpo("As decisões não foram tomadas projeto a projeto. A seleção do P5 depende da posição do P4, que antecede o P5 por causa do especialista em qualidade e dos requisitos do Pareto de defeitos. "
      "O P6 só começa depois do teste de aceitação em fábrica (FAT) do P1. O P2 não usa engenheiro de automação, e por isso o P1 mantém os dois engenheiros. "
      "O P7 não foi eliminado porque habilita dados em tempo real, mas ficou condicionado a um gate. O @Q:deps@ reúne as quatro dependências do enunciado e o tratamento dado a cada uma.")
tabela("Dependências do enunciado e tratamento no plano", ["Dependência", "Natureza", "Tratamento no plano", "Efeito"], [[a, b, c, d] for a, b, c, d in C.DEPS],
       w_([2.1, 3.4, 6.9, 3.6]), kind="Quadro", size=8.5, fonte_txt="Elaborado pelos autores (2026), com base em " + FONTE_ENUN, key="deps")
corpo("A integração é sustentada por quatro mecanismos. O primeiro é a **linha de base de indicadores**, fechada até o fim do m1 com a Controladoria, que serve de referência para medir todos os benefícios. "
      "O segundo é o **comitê de portfólio**, mensal, que decide sobre desvios, uso da reserva e mudanças de escopo; nenhuma mudança que afete custo, prazo ou recursos de outro projeto é aprovada fora dele. "
      "O terceiro são os **gates**: o G1, no fim do m3, confere se o contrato e o pedido de equipamentos do P1 saíram e se o P4 está encerrado; o G2, no fim do m6, decide o P7. "
      "O quarto é o **gerenciamento de benefícios**, com balanços no m9 e no m12 que comparam o resultado com a linha de base e alimentam a decisão sobre P7, P3 e P8 para o ciclo seguinte.")
corpo("A reserva gerencial de " + mil(M.RESERVA) + " é um recurso do portfólio, e não de cada projeto. Ela só é liberada por gatilho de risco, aprovada no comitê, o que evita que seja consumida por pequenos desvios "
      "e preserva a capacidade de decisão no G2.")

# =====================================================================================
#  3 ESCOPO
# =====================================================================================
h1("3 GERENCIAMENTO DO ESCOPO")
corpo("O escopo do portfólio é composto pelos cinco projetos priorizados, organizados em dois programas. Os projetos adiados e o posterior (P3, P7 e P8) estão fora do escopo deste ciclo, "
      "com a exceção condicional do P7. Este capítulo descreve o que cada projeto entrega e como as entregas se decompõem.")
h2("3.1 Definição do Escopo e Entregas")
esc = [
    ["P1 Automação da Linha 1", C.ENTREGAS_PROJ["P1"], "Fornecedor entrega no prazo; instalação em paradas programadas; operadores treinados pelo P6.", "R$ 900 mil; 6 meses; EA1 e EA2 a 100%."],
    ["P2 Manutenção Preditiva", C.ENTREGAS_PROJ["P2"], "Ativos críticos definidos no m1; sensores e dados contratados dentro do projeto, sem engenheiro de automação.", "R$ 450 mil; 4 meses; MAN a 100% e TI1 a 70%."],
    ["P4 Redução de Refugo", C.ENTREGAS_PROJ["P4"], "Dados de refugo disponíveis ou coletáveis em 1 mês; ações dentro do orçamento.", "R$ 250 mil; 3 meses; QUAL a 100%."],
    ["P5 Controle de Qualidade", C.ENTREGAS_PROJ["P5"], "Requisitos derivados do P4; calibração rastreável.", "R$ 350 mil; 4 meses; QUAL a 100% e TI2 a 50%."],
    ["P6 Treinamento de Operadores", C.ENTREGAS_PROJ["P6"], "Início após o FAT do P1; conteúdo técnico fornecido pelo fornecedor do P1.", "R$ 150 mil; 2 meses; MAN a 20%."],
]
corpo("O @Q:escopo@ resume a entrega principal, as premissas e as restrições de cada projeto priorizado.")
tabela("Escopo resumido dos projetos priorizados", ["Projeto", "Entrega principal", "Premissas", "Restrições"], esc, w_([3, 5, 5, 3.4]), kind="Quadro", size=8.5, key="escopo")
corpo("**Premissas gerais (H):** a MetalTech consegue fechar a linha de base de indicadores no m1; o fornecedor do P1 cumpre o prazo de fabricação; as áreas usuárias do P3 e do P8 aceitam o adiamento "
      "com a condição de retorno apresentada; o ganho de +12% do P1 refere-se ao indicador de produtividade acompanhado pela diretoria. "
      "**Restrições gerais:** teto de R$ 2,5 milhões, equipe fixa de sete profissionais e horizonte de 12 meses. "
      "**Fora do escopo:** implantação do ERP, expansão física da capacidade e monitoramento IoT em toda a fábrica, que só entra se o G2 aprovar.")
h2("3.2 Estrutura Analítica do Projeto (EAP)")
corpo("A EAP do portfólio tem três níveis acima dos pacotes de trabalho: portfólio, programa e projeto. O @Q:eap@ apresenta a decomposição de cada projeto priorizado no segundo nível, "
      "sempre em entregas, e não em atividades. O pacote de gestão aparece em todos os projetos e é o ponto de contato com o PMO.")
eap_lin = []
for prog, pj in (("A", ["P1", "P2", "P6"]), ("B", ["P4", "P5"])):
    for p in pj:
        eap_lin.append([f"Programa {prog}", f"{p} {P[p]['nome']}", "\n".join(C.EAP[p])])
tabela("EAP resumida dos projetos priorizados (nível 2)", ["Programa", "Projeto", "Entregas principais"], eap_lin, w_([2.4, 4.4, 9.2]), kind="Quadro", size=8.5,
       fonte_txt="Elaborado pelos autores (2026). A decomposição em pacotes de trabalho será detalhada no plano de cada projeto.", key="eap")
corpo("A numeração dos pacotes usa o número do projeto como prefixo (1.x para o P1, 2.x para o P2, e assim por diante), o que permite a rastreabilidade nos relatórios mensais e nos contratos de aquisição.")

# =====================================================================================
#  4 TEMPO
# =====================================================================================
h1("4 GERENCIAMENTO DO TEMPO")
corpo("Este capítulo explica a sequência de execução dos projetos, as decisões de cronograma que resolvem conflitos de recursos e o roadmap de 12 meses, com marcos e gates.")
h2("4.1 Planejamento e Sequenciamento das Atividades")
corpo("A sequência decorre de três tipos de restrição. A primeira são as dependências do enunciado: o P6 prepara os operadores para o P1, e o P4 e o P5 são complementares. "
      "A segunda é a disponibilidade dos profissionais: o especialista em qualidade atende um projeto por vez, e os dois engenheiros de automação ficam inteiros no P1 até o m6. "
      "A terceira é a necessidade de ganhos rápidos: os projetos de ciclo curto e baixo risco (P4, com 3 meses, e P2, com 4) começam no m1, para que haja resultado medido antes do gate G2.")
corpo("O resultado é a seguinte ordem. No m1, partem P1, P2 e P4. O P4 termina no m3 e libera o especialista em qualidade para o P5, que começa no m4. "
      "O P2 termina no m4. O teste de aceitação em fábrica (FAT) do P1 acontece no fim do m4 e libera o P6, que ocorre no m5 e no m6, junto da instalação e do comissionamento. "
      "O P1 termina no m6, e o P5 no m7. A partir do m7, a MetalTech entra em operação assistida (hypercare) e em medição de benefícios. O P7, se aprovado no G2, ocupa os m7 a m11. "
      "As durações de todos os projetos coincidem com os prazos do enunciado, o que foi conferido por script.")
h2("4.2 Cronograma e Roadmap do Portfólio")
corpo("A @F:roadmap@ apresenta o roadmap em trimestres e meses, e o Apêndice A detalha as principais atividades por mês. Os marcos e gates estão no @Q:marcos@.")
figura("fig03_roadmap_12_meses.png", "Roadmap de 12 meses do portfólio, com marcos e gates", 16.0, key="roadmap")
tabela("Marcos e gates do roadmap", ["Marco", "Fim do mês", "Descrição", "Critério de passagem"], [
    ["M1", "m1", "Linha de base de indicadores aprovada", "Cinco indicadores medidos e aprovados pela Controladoria"],
    ["G1", "m3", "Gate 1 (proposto pelo grupo)", "Contrato do P1 assinado, pedido de equipamentos emitido até o m2 e P4 encerrado"],
    ["FAT", "m4", "Teste de aceitação em fábrica do P1", "Testes de integração e de segurança aprovados; libera o P6 e a instalação"],
    ["G2", "m6", "Gate 2: decide o P7", "P2 e P4 no prazo, FAT aprovado, recurso disponível e engenheiros livres"],
    ["GL", "m6", "Go-live do P1 e aceite do P6", "Teste de aceitação no local (SAT) e avaliação de competência de 80% ou mais"],
    ["M9", "m9", "Balanço parcial de benefícios", "Comparação com a linha de base e com a trajetória até a meta"],
    ["M12", "m12", "Balanço final e proposta do ciclo seguinte", "Decisão sobre P7, P3 e P8 com dados reais"],
], w_([1.6, 1.8, 5.2, 7.4]), kind="Quadro", size=9, align=["c", "c", "l", "l"], key="marcos")
corpo("O gate G2 merece detalhe. O P7 só começa se P2 e P4 estiverem no prazo e se houver recurso para ele. Os critérios completos estão no @Q:g2@, e o tratamento financeiro, no capítulo 5.")
tabela("Critérios do gate G2 e possíveis resultados", ["Dimensão / resultado", "Critério ou ação"], [[a, b] for a, b in C.G2_CRITERIOS] + [[f"Resultado: {a}", b] for a, b in C.G2_RESULT],
       w_([4, 12]), kind="Quadro", size=9, first_col_bold=True, key="g2")

# =====================================================================================
#  5 CUSTOS
# =====================================================================================
h1("5 GERENCIAMENTO DOS CUSTOS")
corpo(f"A soma dos projetos priorizados é de {mil(M.INV_PRIOR)}, o que equivale a {pct(100 * M.INV_PRIOR / M.ORCAMENTO_TETO)} do teto de {mil(M.ORCAMENTO_TETO)}. "
      f"Os {mil(M.RESERVA)} restantes ({pct(100 * M.RESERVA / M.ORCAMENTO_TETO)}) formam a reserva gerencial. Este capítulo mostra como os valores foram considerados na decisão, "
      "como se distribuem por projeto, programa e trimestre, e como a reserva está composta.")
h2("5.1 Estimativa e Distribuição dos Custos")
corpo("Os investimentos de cada projeto são dados do enunciado e foram tomados como estimativa de custo total. Para comparar projetos de benefícios diferentes, o grupo calculou o custo por ponto percentual do benefício declarado, "
      "que só existe para quem tem benefício numérico. Esse custo mostra, por exemplo, que o P4 (R$ 10 mil por ponto) e o P5 (R$ 11,7 mil) são mais baratos por unidade de meta que o P1 (R$ 75 mil), "
      "o que é coerente com o fato de o P1 ser o projeto de maior risco. O ROI financeiro não pode ser calculado, porque o enunciado não informa o valor monetário dos benefícios.")
linhas = []
for p in ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]:
    cpp = M.custo_por_pp(p)
    dec = {"Prioridade": "Priorizar", "Posterior": "Posterior (G2)", "Adiado": "Adiar"}[M.DECISAO[p]]
    linhas.append([p, P[p]["nome"], br(P[p]["inv"]), pct(100 * P[p]["inv"] / M.ORCAMENTO_TETO, 1), (br(cpp, 1) if cpp else "n/d"), dec])
linhas.append(["", "Total priorizado", br(M.INV_PRIOR), pct(100 * M.INV_PRIOR / M.ORCAMENTO_TETO, 1), "", ""])
linhas.append(["", "Reserva gerencial", br(M.RESERVA), pct(100 * M.RESERVA / M.ORCAMENTO_TETO, 1), "", ""])
linhas.append(["", "Total comprometido (teto)", br(M.ORCAMENTO_TETO), "100,0%", "", ""])
tabela("Investimento por projeto, custo por ponto percentual de benefício e decisão (R$ mil)", ["ID", "Projeto", "Investimento", "% do teto", "Custo por p.p.", "Decisão"], linhas,
       w_([1, 5, 2.4, 2, 2.4, 3.2]), kind="Tabela", size=9, align=["l", "l", "r", "r", "r", "l"], bold_rows=(8, 9, 10),
       fonte_txt="Elaborado pelos autores (2026), com " + FONTE_ENUN + " n/d: sem benefício numérico no enunciado.", key="investimento")
corpo(f"Por programa, o Programa A (P1, P2 e P6) soma {mil(M.PROG_CUSTO['A'])}, que é {pct(100 * M.PROG_CUSTO['A'] / M.ORCAMENTO_TETO)} do teto e {pct(100 * M.PROG_CUSTO['A'] / M.INV_PRIOR, 1)} do valor priorizado. "
      f"O Programa B (P4 e P5) soma {mil(M.PROG_CUSTO['B'])}, ou {pct(100 * M.PROG_CUSTO['B'] / M.ORCAMENTO_TETO)} do teto e {pct(100 * M.PROG_CUSTO['B'] / M.INV_PRIOR, 1)} do valor priorizado. "
      "Os três projetos fora do ciclo (P3, P7 e P8) somam R$ 3,3 milhões.")
corpo("A @T:investimento@ reúne o investimento de cada projeto, o percentual do teto e a decisão.")
corpo("Como o orçamento detalhado por item depende de cotações, o grupo assumiu uma composição por categoria de aquisição (H), mostrada na @T:categorias@, que também orienta o capítulo 10.")
linhas = []
for c, nome in M.CATS.items():
    linhas.append([nome] + [br(M.COMP[p].get(c, 0)) if M.COMP[p].get(c, 0) else "—" for p in M.PRIORIZADOS] + [br(M.CAT_TOTAL[c])])
linhas.append(["Total"] + [br(P[p]["inv"]) for p in M.PRIORIZADOS] + [br(M.INV_PRIOR)])
tabela("Composição estimada do orçamento por categoria de aquisição (R$ mil, hipótese)", ["Categoria"] + M.PRIORIZADOS + ["Total"], linhas, w_([5.6, 1.6, 1.6, 1.6, 1.6, 1.6, 2.2]),
       kind="Tabela", size=9, align=["l"] + ["r"] * 6, bold_rows=(6,), fonte_txt="Elaborado pelos autores (2026). Composição hipotética, a validar nas cotações.", key="categorias")
h2("5.2 Orçamento Consolidado do Portfólio")
corpo("**Premissa de desembolso (H):** o investimento de cada projeto é pago de forma linear, mês a mês, ao longo da duração do projeto. O P1, por exemplo, desembolsa R$ 150 mil por mês durante seis meses. "
      "A reserva não entra na curva, porque só é liberada por decisão do comitê. A @T:trimestre@ mostra o resultado por trimestre e a @F:desembolso@ apresenta a curva mensal e a acumulada.")
linhas = []
for p in M.PRIORIZADOS:
    linhas.append([p, f"m{M.JANELA[p][0]}-m{M.JANELA[p][1]}"] + [br(x, 1) if x else "—" for x in M.TRI_PROJ[p]] + [br(P[p]["inv"])])
linhas.append(["Total", ""] + [br(x, 1) if x else "0" for x in M.TRI] + [br(M.INV_PRIOR)])
linhas.append(["Acumulado", ""] + [br(sum(M.TRI[:k + 1]), 1) for k in range(4)] + [""])
linhas.append(["% do teto", ""] + [pct(100 * sum(M.TRI[:k + 1]) / M.ORCAMENTO_TETO, 1) for k in range(4)] + [""])
tabela("Distribuição trimestral do desembolso dos projetos priorizados (R$ mil)", ["Projeto", "Janela", "T1", "T2", "T3", "T4", "Total"], linhas, w_([2.6, 2, 2, 2, 2, 2, 2.4]),
       kind="Tabela", size=9, align=["l", "c", "r", "r", "r", "r", "r"], bold_rows=(5,), fonte_txt="Elaborado pelos autores (2026), com premissa de desembolso linear (H).", key="trimestre")
figura("fig04_curva_desembolso.png", "Curva de desembolso mensal e acumulada dos projetos priorizados", 16.0, key="desembolso")
corpo(f"Por programa, o Programa A desembolsa R$ {br(M.TRI_PROG['A'][0], 1)} mil em T1 e R$ {br(M.TRI_PROG['A'][1], 1)} mil em T2. O Programa B desembolsa R$ {br(M.TRI_PROG['B'][0], 1)} mil em T1, "
      f"R$ {br(M.TRI_PROG['B'][1], 1)} mil em T2 e R$ {br(M.TRI_PROG['B'][2], 1)} mil em T3. O pico mensal é de R$ {br(max(M.MES_TOTAL), 1)} mil no m4. "
      f"Em T2 já foram desembolsados {pct(100 * sum(M.TRI[:2]) / M.INV_PRIOR, 1)} do valor priorizado, e T4 não tem desembolso de projeto. "
      f"Se 50% do P1 (pedido de equipamentos) fossem pagos nos m1 e m2, T1 subiria para R$ {br(M.TRI_ALT[0], 1)} mil e T2 cairia para R$ {br(M.TRI_ALT[1], 1)} mil; a Controladoria deve confirmar o fluxo de caixa antes do pedido.")
corpo("A composição da reserva é uma hipótese do grupo (@T:reserva@). A parte maior é a contingência do P1, por ser o projeto de risco alto.")
tabela("Composição da reserva gerencial (R$ mil, hipótese)", ["Uso previsto da reserva", "Valor"], [[a, br(b)] for a, b in M.RESERVA_COMP] + [["Total", br(M.RESERVA)]], w_([12, 4]),
       kind="Tabela", size=9, align=["l", "r"], bold_rows=(4,), key="reserva")
corpo(f"Para testar se a reserva é adequada, o grupo calculou o valor monetário esperado (VME) dos riscos de custo: R$ {br(M.EMV_TOTAL)} mil, com P1 respondendo por R$ {br(M.EMV[0][1])} mil. "
      f"A reserva de R$ {br(M.RESERVA)} mil cobre {n2(M.RESERVA / M.EMV_TOTAL)} vez esse valor, mas não cobre o pior caso de estouro simultâneo de P1 (40%, R$ 360 mil) e P2 (40%, R$ 180 mil), que somaria R$ 540 mil. "
      "Por isso a reserva é liberada apenas por gatilho.")
corpo(f"O P7 merece nota à parte. Ele custa {mil(P['P7']['inv'])} e a reserva é de {mil(M.RESERVA)}. Mesmo sem uso nenhum da reserva faltam R$ {br(P['P7']['inv'] - M.RESERVA)} mil. "
      "O P7 integral só cabe se, no G2, houver economias capturadas e auditadas, ou complemento aprovado pela diretoria, e o total aprovado deixaria então de respeitar o teto de R$ 2,5 milhões. "
      "A alternativa prevista é iniciar uma fase 1 do P7 com valor até o saldo da reserva e deixar o restante para o ciclo seguinte.")

# =====================================================================================
#  6 QUALIDADE
# =====================================================================================
h1("6 GERENCIAMENTO DA QUALIDADE")
corpo("A qualidade do portfólio é medida por dois conjuntos de critérios: a qualidade das entregas de cada projeto (aceite) e a qualidade do resultado para a empresa, que são as quatro metas. "
      "Um projeto pode ser entregue no prazo e dentro do custo e, ainda assim, não produzir o benefício esperado; por isso os indicadores das metas são acompanhados desde o primeiro mês.")
h2("6.1 Critérios e Indicadores de Qualidade")
corpo("O @Q:indicadores@ relaciona cada meta estratégica a um indicador, que será medido na linha de base do m1. Nos indicadores sem folga, o grupo propõe uma meta interna 10% acima do alvo, "
      "para que uma realização parcial do benefício ainda deixe a meta da diretoria ao alcance. Os indicadores são hipóteses do grupo e dependem de dados que a MetalTech já deve ter em apontamento de produção, manutenção e inspeção.")
tabela("Indicadores de qualidade ligados às quatro metas estratégicas", ["Meta", "Indicador (H)", "Linha de base", "Alvo", "Fonte e frequência", "Responsável"], [list(i) for i in C.IND],
       w_([2.2, 4.1, 2.2, 2.8, 2.6, 2.6]), kind="Quadro", size=8.5, fonte_txt="Elaborado pelos autores (2026).", key="indicadores")
corpo("Cada projeto também tem critérios de aceite, que definem quando a entrega pode ser considerada concluída e liberar o pagamento ao fornecedor (@Q:aceite@).")
tabela("Critérios de aceite das entregas dos projetos priorizados", ["Projeto", "Critério de aceite", "Responsável"], [list(c) for c in C.CRITERIOS_ACEITE], w_([1.8, 11.2, 3]), kind="Quadro", size=8.5, key="aceite")
h2("6.2 Controle e Garantia da Qualidade")
corpo("A **garantia da qualidade** está nos processos: o comitê de portfólio revisa mensalmente o semáforo de cada projeto; o relatório executivo de uma página mostra os cinco indicadores e o orçamento; "
      "os gates G1 e G2 têm critérios escritos; e as aquisições seguem o processo do capítulo 10, com requisitos técnicos no contrato. Nos projetos de equipamentos (P1 e P5), o FAT e o SAT funcionam como pontos de verificação formais.")
corpo("O **controle da qualidade** está nas medições. Os indicadores de retrabalho e refugo são acompanhados semanalmente com ferramentas simples: lista de verificação para registrar defeitos, "
      "diagrama de Pareto para priorizar causas e carta de controle (CEP) depois da implantação do P5. A produtividade e as paradas são acompanhadas mensalmente. "
      "O balanço no m9 compara cada indicador com a trajetória linear até a meta. Se um indicador ficar abaixo de 90% da trajetória, o comitê abre plano de ação e pode liberar parte da reserva. "
      "Os problemas identificados entram no registro de riscos e de lições aprendidas, para serem tratados no ciclo seguinte.")

# =====================================================================================
#  7 RECURSOS HUMANOS
# =====================================================================================
h1("7 GERENCIAMENTO DOS RECURSOS HUMANOS")
corpo("A MetalTech disponibiliza sete profissionais para o período: dois engenheiros de automação (EA1 e EA2), dois analistas de TI (TI1 e TI2), um especialista em qualidade (QUAL), "
      "um especialista em manutenção (MAN) e um gerente de projetos (GP). Este capítulo mostra o que cada um faz, em quais projetos e como os conflitos de alocação foram resolvidos.")
h2("7.1 Recursos e Responsabilidades")
corpo("O @Q:recursos@ relaciona os recursos aos projetos, e o @Q:raci@ apresenta a matriz de responsabilidades (RACI) das principais entregas de gestão. "
      "O gerente de projetos atua como gerente de programas e é o único com visão dos cinco projetos; cada projeto tem um coordenador local, que é o profissional técnico mais envolvido.")
rec = [
    ["EA1", "P1 (100%, m1-m6); coordenador local do P1", "Especificação, acompanhamento do fabricante, FAT, instalação e comissionamento"],
    ["EA2", "P1 (90% + 10% consultivo ao P2, m1-m4; 100% no m5-m6)", "Integração com a base instalada; consultoria de até 4 h por semana ao P2"],
    ["TI1", "P2 (70%, m1-m4) e P1 (30%, m3-m6)", "Aquisição de dados do P2 e integração de sistemas do P1"],
    ["TI2", "P4 (20%, m1-m3) e P5 (50%, m4-m7)", "Registro de refugo e integração dos equipamentos de inspeção"],
    ["QUAL", "P4 (100%, m1-m3) e P5 (100%, m4-m7); coordenador local do P4 e do P5", "Análise de causas, requisitos de inspeção, calibração e CEP"],
    ["MAN", "P2 (100%, m1-m4) e P6 (20%, m5-m6); coordenador local do P2", "Ativos críticos, plano de manutenção preditiva e apoio ao treinamento"],
    ["GP", "Todos (gestão do portfólio)", "Gerente de programas: ritos, riscos, gates, relatório e interface com a diretoria"],
]
tabela("Recursos humanos, alocação nos projetos e responsabilidades", ["Recurso", "Alocação", "Responsabilidade"], rec, w_([1.8, 7, 7.2]), kind="Quadro", size=9, first_col_bold=True, key="recursos")
raci_cab = ["Atividade", "Dir.", "GP", "EA", "TI", "QUAL", "MAN", "Prod. e RH", "Contr.", "Forn."]
raci = [
    ["Aprovar orçamento, reserva e gates", "A", "R", "I", "I", "I", "I", "C", "C", "–"],
    ["Fechar a linha de base de indicadores", "I", "R", "I", "C", "R", "R", "C", "A", "–"],
    ["Executar o P1", "I", "A", "R", "C", "I", "I", "C", "I", "R"],
    ["Executar o P2", "I", "A", "C", "R", "I", "R", "C", "I", "R"],
    ["Executar o P4", "I", "A", "I", "C", "R", "C", "C", "I", "R"],
    ["Executar o P5", "I", "A", "I", "R", "R", "I", "C", "I", "R"],
    ["Executar o P6", "I", "A", "C", "I", "I", "R", "R", "I", "R"],
    ["Relatório mensal e gestão de riscos", "I", "A/R", "C", "C", "C", "C", "I", "C", "–"],
    ["Medir benefícios (m7 a m12)", "I", "A", "C", "C", "R", "R", "C", "R", "–"],
    ["Recomendar a decisão do G2", "A", "R", "C", "C", "C", "C", "I", "C", "–"],
]
for linha in raci:
    assert sum(1 for c in linha[1:] if c.startswith("A")) == 1, linha[0]
    assert any("R" in c for c in linha[1:]), linha[0]
tabela("Matriz de responsabilidades (RACI) das principais entregas", raci_cab, raci, w_([5.4, 1, 1.1, 1, 1, 1.3, 1.3, 1.7, 1.3, 1.2]), kind="Quadro", size=8.5,
       align=["l"] + ["c"] * 9, fonte_txt="Elaborado pelos autores (2026). R: responsável; A: aprova (um por linha); C: consultado; I: informado. Forn.: fornecedores.", key="raci")
h2("7.2 Alocação e Gestão dos Recursos")
corpo("A carga de cada profissional foi calculada mês a mês para os 12 meses. A @F:figrecursos@ compara dois cenários: no painel A, o que aconteceria se os cinco projetos partissem juntos no m1, cada um com sua duração, "
      f"e se o P2 usasse metade de um engenheiro de automação para a instrumentação; no painel B, o plano adotado. O primeiro cenário produz {len(M.CONF_ING)} células acima de 100%. O plano adotado não produz nenhuma.")
figura("fig05_matriz_recursos.png", "Carga mensal dos recursos: cenário sem as decisões (A) e plano adotado (B)", 15.5, key="figrecursos")
corpo("Os conflitos encontrados e as decisões tomadas são os do @Q:conflitos@. Cada decisão corresponde a uma das opções que o enunciado propõe: alterar o cronograma, executar em sequência, modificar o escopo, "
      "contratar recursos externos ou priorizar um projeto.")
tabela("Conflitos de recursos e decisões tomadas", ["Conflito sem a decisão", "Carga", "Decisão (tipo)", "Resultado"], [
    ["EA1 e EA2 no P1 e o P2 pedindo engenheiro de automação", "150% (EA1, m1-m4)", "Modificar o escopo: o P2 não usa EA; sensores e instrumentação são contratados dentro dos R$ 450 mil; EA só consultivo", "EA1 em 100% e EA2 em 90% + 10% consultivo"],
    ["QUAL no P4 e no P5 ao mesmo tempo", "200% (m1-m3)", "Alterar o cronograma: P4 no m1-m3 e P5 no m4-m7, em sequência", "QUAL em 100%, sem sobreposição"],
    ["MAN no P2 e no P6", "120% (m1-m2)", "Alterar o cronograma: P6 só depois do FAT do P1 (m5-m6), quando o P2 já terminou", "MAN em 100% até o m4 e 20% depois"],
    ["GP em cinco projetos simultâneos", "185% (m1)", "Executar em sequência e criar coordenadores locais; analista de planejamento externo pago pela reserva se o GP passar de 90% por 2 meses", f"GP no máximo em {M.PICO['GP']}%"],
    ["TI1 no P2 e no P1", "100% (m3-m4)", "Aceitar no limite: P2 a 70% e P1 a 30%; TI2 como apoio; sem demandas extras no m3-m4", "TI1 em 100%, sem folga (risco R09)"],
], w_([4.6, 2.2, 6, 3.2]), kind="Quadro", size=8.5, key="conflitos")
corpo("A checagem do próprio plano adotado revelou um conflito residual: somar o P1 a 100% com a consultoria de 10% ao P2 levaria o EA2 a 110% no m1-m4. "
      "A solução foi alocar o EA2 a 90% no P1 e 10% de consultoria ao P2, o que retira 0,4 engenheiro-mês dos 12 do P1. É um custo pequeno, mas real, e fica registrado como premissa a confirmar com a empresa. "
      "O conteúdo técnico do P6 é fornecido pelo fornecedor do P1, para não retirar engenheiro do projeto de risco alto.")
mm = [[r] + [str(v) if v else "·" for v in M.MAT[r]] + [f"{M.PICO[r]}%"] for r in M.RECS]
tabela("Matriz de carga dos recursos por mês no plano adotado (% de dedicação)", ["Rec."] + [f"m{k}" for k in range(1, 13)] + ["Pico"], mm, w_([1.4] + [1.0] * 12 + [1.4]), kind="Tabela", size=8, align=["l"] + ["c"] * 13,
       fonte_txt="Elaborado pelos autores (2026), com cálculo em scripts/modelo_portfolio.py. Carga de GP calculada por modelo de demanda (H).", key="cargas")
corpo("A @T:cargas@ traz os percentuais mês a mês do plano adotado.")
corpo(f"O gerente de projetos é o ponto único de falha do plano. Pelo modelo de demanda do grupo (H), em que cada projeto consome 35% do tempo do GP no mês de início, 25% na execução e 30% no encerramento, mais 10% de governança, "
      f"a carga sem apoio seria de {round(M.GP_SEM_COORD[0])}% no m1, {round(M.GP_SEM_COORD[3])}% no m4 e {round(M.GP_SEM_COORD[4])}% nos m5 e m6. Com coordenadores locais assumindo 30% do esforço de cada projeto, o pico cai para {M.PICO['GP']}% no m1. "
      "Não há folga para absorver atraso, e por isso o gatilho de contratar um analista de planejamento externo está definido.")
corpo("Se o G2 liberar o P7 (m7 a m11), ele ocupa EA1 a 40%, TI1 a 50% e TI2 a 30%, todos já livres do P1. A checagem por script mostra que nenhum profissional passa de 100% nessa configuração. "
      "Para o desenvolvimento da equipe, o P6 prepara os operadores, e a rotação entre pares (EA1 e EA2, TI1 e TI2) reduz a dependência de uma pessoa só.")

# =====================================================================================
#  8 COMUNICACOES
# =====================================================================================
h1("8 GERENCIAMENTO DAS COMUNICAÇÕES")
corpo("A comunicação do portfólio precisa cumprir duas funções: dar à diretoria a informação necessária para decidir nos gates e no comitê, e preparar quem será afetado pelas mudanças, em especial os operadores da Linha 1. "
      "O plano segue a lógica de poucos ritos, curtos e frequentes, para não consumir o tempo de um GP que já está perto do limite.")
h2("8.1 Plano de Comunicação")
corpo("O @Q:comunic@ apresenta as principais comunicações, com frequência, canal, público e proprietário.")
tabela("Plano de comunicação do portfólio", ["Descrição", "Frequência", "Canal", "Público", "Proprietário"], [list(c) for c in C.COMUNICACOES], w_([5.2, 2.2, 3.2, 3.2, 2.2]), kind="Quadro", size=8.5,
       fonte_txt="Elaborado pelos autores (2026).", key="comunic")
h2("8.2 Comunicação com as Partes Interessadas")
corpo("A informação é adaptada a cada público. A **diretoria** recebe o relatório mensal de uma página, com semáforo por projeto, orçamento e reserva e os cinco indicadores, e participa do comitê nos gates. "
      "A **Controladoria** valida a linha de base e os balanços. Os **gerentes e a equipe dos projetos** têm o rito semanal e o registro de riscos. "
      "Os **operadores** recebem a comunicação sobre a mudança na Linha 1 em reunião de turno, com a explicação do porquê da automação e do cronograma de treinamento, e os operadores-chave participam do FAT. "
      "Os **fornecedores** recebem cobrança de status a cada 15 dias. As **áreas usuárias do ERP e da expansão** recebem a ata do portfólio, que registra os projetos adiados e as condições de retorno, para que o adiamento seja entendido como decisão, e não como esquecimento.")
corpo("O alerta de desvio é a única comunicação com prazo curto: qualquer gatilho de risco dispara aviso à diretoria em até 24 horas, com a ação proposta, e fica registrado no log de riscos. "
      "O PMO guarda as atas e os relatórios como lições aprendidas e base para o balanço final do m12.")

# =====================================================================================
#  9 RISCOS
# =====================================================================================
h1("9 GERENCIAMENTO DOS RISCOS")
corpo("Os riscos foram identificados a partir das decisões do grupo, das dependências e dos limites de recursos, e descritos na forma causa, risco e consequência. "
      "Cada risco recebeu probabilidade, impacto, severidade, estratégia de resposta e dono. Foram identificados 14 riscos.")
h2("9.1 Identificação e Análise dos Riscos")
corpo("A probabilidade usa a escala 0,1 (muito baixa), 0,3 (baixa), 0,5 (média), 0,7 (alta) e 0,9 (muito alta). O impacto usa os valores 0,05, 0,10, 0,20, 0,40 e 0,80, definidos por objetivo no @Q:escala@. "
      "A severidade é o produto de probabilidade e impacto. O grupo adotou, como convenção (H), severidade alta a partir de 0,18, média de 0,06 a 0,17 e baixa abaixo de 0,06.")
esc_imp = [
    ["Custo", "Aumento insignificante do custo", "Menos de 10% de aumento", "10 a 20% de aumento", "20 a 40% de aumento", "Mais de 40% de aumento"],
    ["Tempo", "Aumento insignificante do tempo", "Menos de 5% de aumento", "5 a 10% de aumento", "10 a 20% de aumento", "Mais de 20% de aumento"],
    ["Escopo", "Diminuição pouco notável", "Áreas secundárias afetadas", "Áreas principais afetadas", "Redução inaceitável para o patrocinador", "Produto final inútil"],
    ["Qualidade", "Degradação pouco notável", "Só aplicações muito exigentes afetadas", "Redução requer aprovação do patrocinador", "Redução inaceitável para o patrocinador", "Produto final inútil"],
]
tabela("Escala de impacto de um risco nos objetivos do projeto", ["Objetivo", "Muito baixo (0,05)", "Baixo (0,10)", "Moderado (0,20)", "Alto (0,40)", "Muito alto (0,80)"], esc_imp,
       w_([1.9, 2.8, 2.9, 3, 3, 2.4]), kind="Quadro", size=8, first_col_bold=True, fonte_txt="Adaptado de PMI (2013) e do material da Aula 7 da disciplina.", key="escala")
reg = []
for r in M.RISCOS_DADOS:
    reg.append([r["id"], f"**{r['titulo']}.** {r['causa']}; {r['risco']}; {r['consequencia']}.", br(r["prob"], 1), br(r["imp"], 2), sev_fmt(r["sev"]), r["zona"]])
fills = {}
cell_fills = {}
for i, r in enumerate(M.RISCOS_DADOS, 1):
    cell_fills[(i, 5)] = {"Alta": "F1B5AE", "Média": "FBE3A0", "Baixa": "CFE8D8"}[r["zona"]]
tabela("Registro e análise dos riscos, em ordem de severidade", ["ID", "Risco: causa, evento e consequência", "Prob.", "Impacto", "Severidade", "Zona"], reg,
       w_([1.1, 8.9, 1.1, 1.5, 1.9, 1.5]), kind="Quadro", size=8, align=["c", "l", "c", "c", "c", "c"], cell_fills=cell_fills,
       fonte_txt="Elaborado pelos autores (2026), com as escalas da disciplina. Severidade = probabilidade x impacto.", key="registro")
figura("fig06_matriz_riscos.png", "Matriz de probabilidade e impacto dos 14 riscos", 15.0, key="matrizriscos")
corpo("O @Q:registro@ traz o registro dos riscos em ordem de severidade, e a @F:matrizriscos@ os posiciona na matriz de probabilidade e impacto.")
corpo("Três riscos têm severidade alta: o benefício parcial (R03, 0,28), o atraso ou estouro do P1 (R01, 0,20) e o gerente de projetos como ponto único de falha (R02, 0,20). "
      "Eles se reforçam: com o GP sobrecarregado, o P1 atrasa, e com o P1 atrasado os benefícios saem abaixo do previsto. "
      "O R13 tem a maior probabilidade (0,9) e a menor severidade, porque o G2 já prevê o escopo faseado. As oportunidades, como economia superior à prevista no P4, não foram quantificadas e entram no G2 como fonte de recurso.")
h2("9.2 Respostas e Monitoramento dos Riscos")
corpo("O @Q:respostas@ reúne a estratégia de resposta, a ação, o dono e o gatilho de cada risco. Predomina a mitigação, porque a maioria dos riscos vem de condições do próprio plano que não podem ser evitadas sem abrir mão de uma meta. "
      "Dois riscos são evitados por decisão antecipada (R10 e R14) e um é aceito conscientemente (R13).")
resp = [[r["id"], r["estrategia"], r["resposta"], r["dono"], r["gatilho"]] for r in M.RISCOS_DADOS]
tabela("Respostas, donos e gatilhos dos riscos", ["ID", "Estratégia", "Resposta e ação", "Dono", "Gatilho"], resp, w_([1.1, 1.8, 7, 2.9, 3.2]), kind="Quadro", size=8, align=["c", "c", "l", "l", "l"],
       fonte_txt="Elaborado pelos autores (2026). SPI: índice de desempenho de prazo.", key="respostas")
corpo("O acompanhamento é feito no log de riscos, revisado a cada semana no rito do GP e a cada mês no comitê de portfólio, com a probabilidade e o impacto reavaliados. "
      "Quando um gatilho é atingido, o dono comunica à diretoria em até 24 horas e o comitê decide sobre o uso da reserva. A reserva tem VME de R$ 212 mil para os riscos de custo, o que a deixa folgada para o esperado e curta para o pior caso, "
      "como discutido no capítulo 5. Ao final do ciclo, o log vira lição aprendida para o ciclo 2027.")

# =====================================================================================
#  10 AQUISICOES
# =====================================================================================
h1("10 GERENCIAMENTO DAS AQUISIÇÕES")
corpo("Quase todo o investimento dos projetos priorizados passa por aquisições externas: equipamentos de automação e de inspeção, sensores, software, consultoria de integração, instalação e treinamento. "
      "A MetalTech faz internamente a coordenação, a especificação técnica e a validação, e compra o restante. Este capítulo lista as necessidades, a estratégia e os critérios de seleção.")
h2("10.1 Necessidades e Estratégia de Aquisições")
corpo("O @Q:aquisicoes@ apresenta as 17 aquisições previstas. Os valores são a composição hipotética do orçamento (H) e somam exatamente o investimento de cada projeto, o que foi conferido por script. "
      "O prazo limite do pedido considera o tempo de fabricação e entrega, que é o principal risco de cronograma do P1.")
aq = []
for a in C.AQUIS:
    aq.append([a[0], a[1], M.CATS[a[2]].split(" ")[0].replace("Equipamentos", "Equip.").replace("Consultoria", "Consult."), br(a[3]), a[4], a[5]])
tabela("Aquisições previstas, valor estimado (R$ mil, hipótese) e estratégia", ["Item", "Proj.", "Categoria", "R$ mil", "Estratégia de contratação", "Prazo do pedido"], aq,
       w_([4.6, 1, 1.8, 1.2, 5.4, 2]), kind="Quadro", size=7.5, align=["l", "c", "l", "r", "l", "l"], fonte_txt="Elaborado pelos autores (2026). Valores a validar nas cotações.", key="aquisicoes")
corpo(f"Por categoria, equipamentos de automação e inspeção somam R$ {br(M.CAT_TOTAL['A'])} mil, consultoria de integração e engenharia R$ {br(M.CAT_TOTAL['C'])} mil, sensores e instrumentação R$ {br(M.CAT_TOTAL['B'])} mil, "
      f"software e licenças R$ {br(M.CAT_TOTAL['E'])} mil, instalação e adequações R$ {br(M.CAT_TOTAL['F'])} mil e treinamento R$ {br(M.CAT_TOTAL['D'])} mil. Os equipamentos do P1 (R$ 500 mil) são o maior item individual, "
      f"com {pct(100 * 500 / M.INV_PRIOR, 1)} do valor priorizado.")
corpo("A estratégia de contratação varia com o risco do item. Nos equipamentos do P1, o contrato é de preço global com marcos de pagamento, prazo contratual e multa por atraso, com a última parcela condicionada ao SAT. "
      "Nas consultorias de modelagem, o contrato é por tempo e material com teto e entregas por marco. Nos softwares de nuvem, a decisão passa por prova de conceito de 30 dias e contrato anual. "
      "Nos sensores e nos instrumentos, a compra é por cotação, com atenção ao prazo de entrega. O treinamento dos operadores é previsto no contrato do P1, o que evita contratar um segundo fornecedor para o mesmo equipamento. "
      "Os itens a decidir primeiro são os equipamentos do P1 e os sensores do P2, que precisam ser pedidos até o m2 e o m1, respectivamente.")
h2("10.2 Seleção e Gestão de Fornecedores")
corpo("Para itens de valor igual ou superior a R$ 100 mil, o grupo propõe pelo menos três propostas, com avaliação por critérios ponderados. Para itens menores, bastam duas cotações. "
      "Os pesos do @Q:criterios@ são uma hipótese do grupo e dão peso alto ao prazo, porque o atraso do fornecedor do P1 desloca o P6 e o G2.")
tabela("Critérios de seleção de fornecedores e pesos", ["Critério", "Peso"], [[a, f"{b}%"] for a, b in C.CRIT_FORN] + [["Total", "100%"]], w_([12, 4]), kind="Quadro", size=9, align=["l", "c"], bold_rows=(5,), key="criterios")
corpo("A gestão dos fornecedores segue o contrato: acompanhamento quinzenal de status e de prazo de fabricação; verificação no FAT com a participação de operadores-chave; pagamento por marcos; "
      "e registro de desvios no log de riscos. O PMO qualifica um fornecedor alternativo para os equipamentos do P1, como proteção contra atraso. "
      "Entre os riscos de aquisição estão a dependência de fornecedor único, o prazo de importação e a variação de preços, tratados nos riscos R06 e R01.")

# =====================================================================================
#  11 PARTES INTERESSADAS
# =====================================================================================
h1("11 GERENCIAMENTO DAS PARTES INTERESSADAS")
corpo("Foram identificadas 12 partes interessadas, entre pessoas, áreas e fornecedores. Poder e interesse foram pontuados de 1 a 5 pelo grupo (H), por não haver dados sobre a estrutura real da MetalTech, "
      "e o corte entre alto e baixo é 4: pontuação igual ou superior a 4 é alta.")
h2("11.1 Identificação e Análise das Partes Interessadas")
corpo("O @Q:partes@ lista as partes interessadas, e a @F:figpartes@ as posiciona por poder e interesse.")
pa = [[pid, nome, str(po), str(it), q, ex] for pid, nome, po, it, q, atual, des, ex, estr in C.PARTES]
tabela("Partes interessadas, poder, interesse e expectativas", ["ID", "Parte interessada", "Poder", "Interesse", "Quadrante", "Expectativa principal"], pa, w_([1, 4.3, 1.3, 1.8, 3.1, 4.5]),
       kind="Quadro", size=8.5, align=["c", "l", "c", "c", "l", "l"], fonte_txt="Elaborado pelos autores (2026). Pontuações hipotéticas.", key="partes")
figura("fig08_partes_interessadas.png", "Matriz de poder e interesse das partes interessadas", 15.0, key="figpartes", fonte_txt="Elaborado pelos autores (2026). Números dos pontos correspondem aos IDs S1 a S12 do @Q:partes@.")
h2("11.2 Estratégias de Engajamento e Gestão das Expectativas")
corpo("A maior distância entre o nível atual e o desejado está nos operadores, que o grupo supõe resistentes, porque o P1 muda a rotina da Linha 1. A estratégia é informar cedo, treinar por turno e envolver os operadores-chave no FAT. "
      "Para a diretoria, o desafio é manter o apoio apesar das metas sem folga: o relatório mensal mostra o semáforo e os limites. Para as áreas do ERP e da expansão, a estratégia é registrar o adiamento com condição de retorno.")
corpo("O @Q:engaj@ compara o nível de engajamento atual e o desejado e define a estratégia de cada parte.")
pe = [[pid, nome, atual, des, estr] for pid, nome, po, it, q, atual, des, ex, estr in C.PARTES]
tabela("Nível de engajamento atual e desejado e estratégia", ["ID", "Parte interessada", "Atual", "Desejado", "Estratégia de engajamento"], pe, w_([1, 4.2, 2, 2, 6.8]), kind="Quadro", size=8.5,
       align=["c", "l", "c", "c", "l"], fonte_txt="Elaborado pelos autores (2026). Níveis hipotéticos: desinformado, resistente, neutro, apoia, lidera.", key="engaj")

# =====================================================================================
#  12 RESULTADOS E DISCUSSAO
# =====================================================================================
h1("12 RESULTADOS E DISCUSSÃO")
corpo("Este capítulo consolida as decisões do portfólio e discute se a estratégia é viável, que benefícios entrega e onde estão seus limites.")
h2("12.1 Portfólio e Programas Propostos")
corpo(f"A proposta do PMO é executar os projetos P1, P2, P4, P5 e P6, que somam {mil(M.INV_PRIOR)}, no Programa A (Excelência Operacional, {mil(M.PROG_CUSTO['A'])}) e no Programa B (Qualidade 4.0, fase 1, {mil(M.PROG_CUSTO['B'])}). "
      f"A reserva gerencial é de {mil(M.RESERVA)}. O P7 é posterior e depende do G2, e o P3 e o P8 estão adiados. O Programa C (Transformação Digital) não é ativado neste ciclo. "
      "O @Q:programas@ resume cada programa com nome, projetos, objetivo e benefício esperado.")
linhas = [[f"{k}. {v['nome']}", ", ".join(v["projetos"]), mil(M.PROG_CUSTO[k]), C.PROG_TXT[k]["objetivo"], C.PROG_TXT[k]["beneficio"]] for k, v in M.PROGRAMAS.items()]
linhas.append(["C. Transformação Digital (não ativado)", "P3, P7", "—", "Aumentar a integração dos processos e das informações da empresa.", "Candidato a 2027, com o P7 antes do P3."])
tabela("Programas propostos: projetos, objetivo e benefício esperado", ["Programa", "Projetos", "Investimento", "Objetivo", "Benefício esperado"], linhas, w_([3.0, 1.5, 2.4, 4.55, 4.55]), kind="Quadro", size=8.5,
       align=["l", "l", "r", "l", "l"], key="programas")
corpo(f"Em recursos, o plano usa sete profissionais sem sobrecarga: o pico de dedicação é de 100% para EA1, EA2, TI1, QUAL e MAN, e de {M.PICO['GP']}% para o GP. "
      f"Em orçamento, {pct(100 * sum(M.TRI[:2]) / M.INV_PRIOR, 1)} do valor priorizado são desembolsados em seis meses, e a reserva só é liberada por gatilho. "
      "Em prazo, os projetos priorizados terminam até o m7 e deixam cinco meses para operação assistida e medição de benefícios.")
h2("12.2 Análise da Estratégia e Viabilidade")
corpo("A principal justificativa da estratégia é a **cobertura das metas dentro do teto**. Dos 255 subconjuntos possíveis de projetos, o conjunto escolhido é o único que cabe em R$ 2,5 milhões, respeita as dependências "
      "e dá a cada uma das quatro metas um projeto com benefício quantificado no enunciado. Os cinco projetos também são os cinco primeiros da matriz de priorização, o que mostra que o critério de cobertura e o de pontuação apontam para a mesma carteira.")
corpo("A estratégia tem limites, e o PMO os declara. O @Q:metas@ mostra, para cada meta, o que o benefício declarado cobre e qual é a folga.")
tabela("Metas estratégicas, benefício esperado e folga", ["Meta", "Alvo", "Iniciativas", "Cobertura quantificada", "Folga", "Leitura"], [list(l) for l in C.METAS_TAB], w_([2.3, 1.2, 3.3, 2.5, 2.0, 4.7]),
       kind="Quadro", size=8, align=["l", "c", "l", "l", "l", "l"], fonte_txt="Elaborado pelos autores (2026), com " + FONTE_ENUN, key="metas")
figura("fig07_metas_vs_beneficio.png", "Cobertura das metas pelo benefício quantificado, conforme a realização do benefício", 15.5, key="figmetas")
corpo(f"A @F:figmetas@ mostra o problema. Nos projetos P2 e P5, a meta só é atingida se o benefício se realizar 100%: com 90% do prometido, as reduções seriam de 18% (paradas) e 27% (retrabalho). "
      f"A meta de produtividade nem sequer fecha com o P1 a 100%, porque o ganho declarado é de 12 dos 15 pontos; os {M.PRODUT_FALTA} pontos restantes dependem do P6 e dos efeitos de P2 e P4, que o enunciado não quantifica. "
      "A proteção proposta tem cinco partes: linha de base fechada no m1; meta interna 10% acima do alvo (paradas -22%, retrabalho -33%, produtividade +16,5%); aceite de fornecedor condicionado a indicador; "
      "medição mensal com balanços no m9 e no m12; e gatilho de correção quando o indicador ficar abaixo de 90% da trajetória.")
corpo(f"A meta de custos é a menos demonstrável. O enunciado não informa quanto do custo operacional é refugo, retrabalho ou parada. Com a hipótese do grupo de que sejam {br(M.CUSTO_H['refugo'], 0)}%, {br(M.CUSTO_H['retrabalho'], 0)}% e {br(M.CUSTO_H['paradas'], 0)}% do custo, "
      f"e com as reduções declaradas, P4, P5 e P2 contribuiriam com {br(M.CUSTO_SOMA, 1)} dos 10 pontos percentuais. Os {br(M.CUSTO_RESTO, 1)} restantes teriam de vir da produtividade diluída no custo unitário, "
      f"o que exigiria que pelo menos {br(M.CUSTO_FRACAO_NEC_12, 0)}% do custo operacional fosse sensível à produtividade. Só a linha de base do m1 permitirá saber se isso é plausível.")
corpo("Quanto à viabilidade, a análise por dimensão é a seguinte. **Financeira:** o plano cabe no teto com 16% de folga, mas a reserva não cobre o pior caso simultâneo de P1 e P2 e não cobre o P7 integral. "
      "**Recursos:** nenhum profissional passa de 100%, mas cinco estão no limite em algum mês, e o GP é único. **Prazo:** os projetos respeitam os prazos do enunciado, mas o P6 depende do FAT do P1 e o G2 depende dos três. "
      "**Risco:** há três riscos de severidade alta, todos com resposta. **Benefício:** é o ponto mais frágil, por não haver folga em duas metas e por a terceira depender de dados que não existem hoje.")
corpo("O cenário C, mais barato (R$ 1,8 milhão), é a alternativa mais forte e fica próximo na pontuação. Ele é rejeitado porque deixa a meta de produtividade sem projeto com ganho declarado. "
      "Se a diretoria considerar que o risco do P1 é maior do que o benefício que ele traz, o C é a alternativa defensável, com a ressalva de que a meta de +15% passa a ser tratada como não coberta.")

# =====================================================================================
#  13 CONSIDERACOES FINAIS
# =====================================================================================
h1("13 CONSIDERAÇÕES FINAIS")
corpo(f"O trabalho respondeu à pergunta do desafio com uma proposta de portfólio: executar P1, P2, P4, P5 e P6 em dois programas, por {mil(M.INV_PRIOR)}, manter {mil(M.RESERVA)} de reserva, condicionar o P7 a um gate no m6 e adiar P3 e P8. "
      "Em relação aos objetivos específicos, os projetos foram analisados e classificados (capítulo 2), os programas estruturados com objetivo e benefício (capítulos 2 e 12), o orçamento distribuído por projeto, programa e trimestre (capítulo 5), "
      "os recursos alocados mês a mês com os conflitos resolvidos (capítulo 7), o roadmap e os gates definidos (capítulo 4), os riscos analisados (capítulo 9) e a rastreabilidade das metas demonstrada (capítulo 12).")
corpo("O principal resultado analítico é que a matriz de priorização, por si só, não decide: o P1 é o quinto na pontuação e foi mantido pela cobertura de meta. O enunciado deixa claro que não há resposta única, e o valor do exercício está em mostrar o raciocínio e os limites. "
      "O maior limite é a falta de folga nas metas: dois projetos entregam exatamente o alvo e um terceiro não fecha a meta de produtividade, por isso a linha de base do m1 e a medição contínua são a parte mais importante do plano.")
corpo("**Lições aprendidas.** Primeiro, os conflitos de recursos só aparecem quando a carga é calculada mês a mês; o plano parecia viável até que a soma literal levou o EA2 a 110%. Segundo, um único gerente de projetos para três projetos simultâneos é um risco de portfólio, e não um detalhe de alocação. "
      "Terceiro, adiar um projeto exige definir a condição de retorno, para que a decisão seja entendida pelas áreas afetadas. Quarto, separar o que é dado do que é hipótese deixa a análise verificável e mostra o que precisa ser confirmado.")
corpo("**Recomendações à MetalTech.** (a) Aprovar o portfólio e a reserva, com a Controladoria fechando a linha de base até o fim do m1. (b) Confirmar os gates G1 e G2 na agenda da diretoria. "
      "(c) Validar as hipóteses do Apêndice B, em especial a composição do orçamento e a carga do GP. (d) Preparar, para o G2, a decisão sobre o complemento de orçamento do P7 ou sua versão faseada. "
      "(e) Usar o balanço do m12 para decidir sobre o P8 e o Programa C em 2027, começando pelo P7.")

# =====================================================================================
#  REFERENCIAS
# =====================================================================================
h1("REFERÊNCIAS")
REFS = [
    "CARVALHO, Fábio Câmara Araújo de. **Gestão de projetos**. 2. ed. São Paulo: Pearson, 2018. E-book.",
    "CRUZ, Fábio. **Scrum e PMBOK unidos no gerenciamento de projetos**. Rio de Janeiro: Brasport, 2013. E-book.",
    "FINOCCHIO JÚNIOR, José. **Project Model Canvas**: gerenciamento de projetos sem burocracia. Rio de Janeiro: Elsevier, 2013.",
    "PROJECT MANAGEMENT INSTITUTE (PMI). **Um guia do conhecimento em gerenciamento de projetos (Guia PMBOK)**. 5. ed. Newtown Square: PMI, 2013.",
    "PROJECT MANAGEMENT INSTITUTE (PMI). **The standard for portfolio management**. 4. ed. Newtown Square: PMI, 2017a.",
    "PROJECT MANAGEMENT INSTITUTE (PMI). **The standard for program management**. 4. ed. Newtown Square: PMI, 2017b.",
    "SOUZA, Carla Patricia da Silva. **Gestão de projetos**. São Paulo: Contentus, 2020.",
]
for r in REFS:
    par(r, first=None, line=1.0, after=12, align=LEFT)

# =====================================================================================
#  APENDICES E ANEXO
# =====================================================================================
h1("APÊNDICE A - CRONOGRAMA DE ATIVIDADES")
corpo("O @Q:cronograma@ detalha as principais atividades por mês, por projeto. As janelas de cada atividade são hipóteses do grupo e ficam dentro da janela de execução de cada projeto (verificado por script).")
ATV = [
    ("P1", "1.1 Gestão do projeto", 1, 6), ("P1", "1.2 Especificação e projeto executivo", 1, 2), ("P1", "1.3 Contratação e fabricação", 2, 4), ("P1", "1.4 FAT", 4, 4),
    ("P1", "1.5 Instalação e integração", 5, 5), ("P1", "1.6 Comissionamento, SAT e go-live", 6, 6),
    ("P2", "2.2 Ativos críticos e linha de base", 1, 1), ("P2", "2.3 Sensores e aquisição de dados", 2, 3), ("P2", "2.4 Modelos e plataforma", 2, 4),
    ("P2", "2.5 Integração ao plano de manutenção", 4, 4), ("P2", "2.6 Treinamento e transição", 4, 4),
    ("P4", "4.2 Medição e linha de base de refugo", 1, 1), ("P4", "4.3 Análise de causas", 1, 2), ("P4", "4.4 Plano de ações", 2, 3), ("P4", "4.5 Controle e padronização", 3, 3),
    ("P5", "5.2 Requisitos de qualidade", 4, 4), ("P5", "5.3 Equipamentos e CEP", 4, 6), ("P5", "5.4 Integração e registro", 5, 6), ("P5", "5.5 Procedimentos e calibração", 6, 6),
    ("P5", "5.6 Piloto e validação", 7, 7),
    ("P6", "6.2 Necessidades por função", 5, 5), ("P6", "6.3 Conteúdo e material", 5, 5), ("P6", "6.4 Turmas por turno", 5, 6), ("P6", "6.5 Avaliação de competências", 6, 6),
    ("P7", "P7 (condicional ao G2)", 7, 11), ("BM", "Operação assistida e medição", 7, 12),
]
for pj, nome, i, f in ATV:
    if pj in M.JANELA:
        assert M.JANELA[pj][0] <= i <= f <= M.JANELA[pj][1], (nome, i, f)
CORES = {"P1": "0F4C5C", "P2": "2A7F91", "P4": "6BA8B5", "P5": "8C9A5B", "P6": "C98B3A", "P7": "E0A800", "BM": "9AA5AB"}
lin = []
cf = {}
for r_, (pj, nome, i, f) in enumerate(ATV, 1):
    row = [nome] + [""] * 12
    lin.append(row)
    for m in range(i, f + 1):
        cf[(r_, m)] = CORES[pj]
marcos_txt = {1: "M1", 3: "G1", 4: "FAT", 6: "G2 GL", 9: "M9", 12: "M12"}
lin.append(["Marcos"] + [marcos_txt.get(m, "") for m in range(1, 13)])
tabela("Cronograma de atividades por mês (cada célula colorida indica execução)", ["Atividade"] + [f"m{m}" for m in range(1, 13)], lin, w_([5.3] + [0.89] * 12 + [0.02]) if False else
       [2951] + [510] * 12, kind="Quadro", size=7, align=["l"] + ["c"] * 12, cell_fills=cf, fonte_txt="Elaborado pelos autores (2026). Janelas das atividades: hipótese. P7 só se o G2 aprovar.", key="cronograma")

h1("APÊNDICE B - PREMISSAS (H) E CÁLCULOS")
corpo("As premissas abaixo foram assumidas pelo grupo e precisam ser validadas com a MetalTech. Os cálculos estão nos scripts entregues com o relatório (scripts/modelo_portfolio.py), que também verificam automaticamente a soma do orçamento, "
      "as durações, a carga dos recursos e a coerência da matriz de priorização.")
alineas(["pesos da matriz de priorização, rubrica das notas e zonas de severidade dos riscos",
         "desembolso linear mês a mês durante a duração de cada projeto, composição da reserva e composição do orçamento por categoria de aquisição",
         "modelo de demanda do GP (35% no mês de início, 25% na execução, 30% no encerramento, 10% de governança, 15% de operação assistida e 70% do esforço com coordenadores locais)",
         "cargas de operação assistida, sustentação e medição de benefícios (m7 a m12) e cargas do P7, se aprovado",
         "alocação do EA2 em 90% no P1 e 10% de consultoria ao P2 no m1 a m4",
         "gate G1 no fim do m3, FAT no fim do m4 e janela do P7 em m7 a m11",
         "percentuais de refugo, retrabalho e paradas no custo operacional, usados apenas na sensibilidade da meta de custos",
         "o ganho de +12% do P1 refere-se ao indicador de produtividade acompanhado pela diretoria; se a Linha 1 for só parte da fábrica, o efeito sobre a meta é proporcionalmente menor",
         "pontuações de poder e interesse das partes interessadas e níveis de engajamento"])

h1("APÊNDICE C - JUSTIFICATIVA DAS NOTAS DA MATRIZ DE PRIORIZAÇÃO")
corpo("O @Q:justif@ justifica cada nota. A letra indica o critério: AE, alinhamento estratégico; BC, benefício/custo; RI, risco; PR, prazo; SI, sinergia; VR, viabilidade de recursos.")
jt = []
for p in M.RANK:
    jt.append([f"{p} {P[p]['nome']}", "\n".join(f"**{k} {M.NOTAS[p][k]}:** {C.JUST[p][k]}" for k, _, _ in M.CRIT)])
tabela("Justificativa das notas por projeto", ["Projeto", "Notas e justificativas"], jt, w_([3.4, 12.6]), kind="Quadro", size=8, key="justif")

h1("ANEXO A - DADOS DO ENUNCIADO DO DESAFIO")
corpo("O @Q:anexo@ reproduz os dados dos oito projetos fornecidos no enunciado do desafio. Os demais dados são: orçamento máximo de R$ 2,5 milhões; recursos disponíveis de dois engenheiros de automação, "
      "dois analistas de TI, um especialista em qualidade, um gerente de projetos e um especialista em manutenção; dependências P1 com P6, P3 com P7, P4 com P5 e P8 com P1.")
an = [[p, P[p]["nome"], "R$ " + br(P[p]["inv"]) + " mil", f"{P[p]['prazo']} meses", P[p]["risco"], P[p]["ben"]] for p in P]
tabela("Projetos disponíveis (dados do enunciado)", ["ID", "Projeto", "Investimento", "Prazo", "Risco", "Principal benefício"], an, w_([1, 4.8, 2.6, 2, 1.8, 4.4]), kind="Quadro", size=9,
       align=["c", "l", "r", "c", "c", "l"], fonte_txt="Material da disciplina de Gestão de Projetos (Desafio de Gestão de Portfólio e Programas), UniSENAI-SP, 2026.", key="anexo")

# =====================================================================================
#  LISTAS E SUMARIO (campos com resultado em cache, sem numeros de pagina)
# =====================================================================================
def preenche_lista(ph, chave):
    ph_el = ph._p
    itens = CAP[chave]
    ultimo = ph_el
    for k, (n, tit) in enumerate(itens):
        p = doc.add_paragraph()
        D.pfmt(p, align=LEFT, line=1.15, before=0, after=4)
        pPr = p._p.get_or_add_pPr()
        tabs = OxmlElement("w:tabs")
        tb = OxmlElement("w:tab")
        tb.set(qn("w:val"), "right")
        tb.set(qn("w:leader"), "dot")
        tb.set(qn("w:pos"), str(D.TEXT_W))
        tabs.append(tb)
        pPr.append(tabs)
        if k == 0:
            def mk(kind):
                r = p.add_run()
                fc = OxmlElement("w:fldChar")
                fc.set(qn("w:fldCharType"), kind)
                r._r.append(fc)
                return r
            mk("begin")
            r = p.add_run()
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = f' TOC \\h \\z \\c "{chave}" '
            r._r.append(it)
            mk("separate")
        D.add_runs(p, f"{chave} {n} – {tit}", size=11)
        if k == len(itens) - 1:
            r = p.add_run()
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), "end")
            r._r.append(fc)
        ph_el.addnext(p._p)
        ph_el = p._p
        # mantem ordem: p foi criado no fim do corpo; move para depois de 'ultimo'
    ph._p.getparent().remove(ph._p)


# adicionar na ordem correta: cada paragrafo e movido para depois do anterior
for chave in ("Figura", "Tabela", "Quadro"):
    preenche_lista(LISTAS[chave], chave)


def preenche_sumario():
    ph_el = SUMARIO._p
    entradas = TOC
    for k, (nivel, tit) in enumerate(entradas):
        p = doc.add_paragraph()
        D.pfmt(p, align=LEFT, line=1.15, before=(6 if nivel == 1 else 0), after=2, left=(0 if nivel == 1 else 0.8))
        if k == 0:
            def mk(kind):
                r = p.add_run()
                fc = OxmlElement("w:fldChar")
                fc.set(qn("w:fldCharType"), kind)
                r._r.append(fc)
                return r
            mk("begin")
            r = p.add_run()
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = ' TOC \\o "1-2" \\h \\z \\u '
            r._r.append(it)
            mk("separate")
        D.add_runs(p, tit, size=11 if nivel == 1 else 11, bold=(nivel == 1))
        if k == len(entradas) - 1:
            r = p.add_run()
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), "end")
            r._r.append(fc)
        ph_el.addnext(p._p)
        ph_el = p._p
    SUMARIO._p.getparent().remove(SUMARIO._p)


preenche_sumario()

# =====================================================================================
#  CABECALHO (numero de pagina na secao textual), propriedades, atualizacao de campos
# =====================================================================================
sec_pre, sec_txt = doc.sections[0], doc.sections[1]
sec_txt.header.is_linked_to_previous = False
hp = sec_txt.header.paragraphs[0]
D.pfmt(hp, align=WD_ALIGN_PARAGRAPH.RIGHT, line=1.0, after=0)
D.fld_runs(hp, "PAGE", "1", size=10)
sec_txt.header_distance = Cm(1.25)

doc.core_properties.title = "Gestão de Portfólio e Programas: proposta do PMO para a MetalTech S.A."
doc.core_properties.author = ", ".join(C.GRUPO)
doc.core_properties.subject = "Gestão de Projetos - Desafio de Gestão de Portfólio e Programas"
doc.core_properties.comments = ""
doc.core_properties.keywords = "gestão de portfólio; programas; PMO"

# pede ao Word para atualizar os campos (sumario e listas) ao abrir
settings = doc.settings.element
uf = OxmlElement("w:updateFields")
uf.set(qn("w:val"), "true")
settings.append(uf)

def resolve_refs():
    pad = re.compile(r"@([QTF]):(\w+)@")
    nome = {"Q": "Quadro", "T": "Tabela", "F": "Figura"}
    for t in doc.element.body.iter(qn("w:t")):
        if t.text and "@" in t.text:
            def sub(m):
                tipo, n = REFMAP[m.group(2)]
                assert tipo == nome[m.group(1)], (m.group(0), tipo)
                return f"{tipo} {n}"
            t.text = pad.sub(sub, t.text)


resolve_refs()
D.limpa_rels(doc)
doc.save(str(SAIDA))

# pos-processamento: remove a nota de rodape do template (imagem da Amazonia) e relacoes orfas
tmp = SAIDA.with_suffix(".tmp.docx")
with zipfile.ZipFile(SAIDA) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "word/footnotes.xml":
            s = data.decode("utf8")
            s = re.sub(r"<w:footnote [^>]*w:id=\"0\"[^>]*>.*?</w:footnote>", "", s, flags=re.S)
            data = s.encode("utf8")
        if item.filename == "word/_rels/footnotes.xml.rels":
            s = data.decode("utf8")
            s = re.sub(r"<Relationship [^>]*ipam[^>]*/>", "", s)
            data = s.encode("utf8")
        zout.writestr(item, data)
shutil.move(str(tmp), str(SAIDA))
print("salvo", SAIDA, "| figuras", CONT["Figura"], "tabelas", CONT["Tabela"], "quadros", CONT["Quadro"])
