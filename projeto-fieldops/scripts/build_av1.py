#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta avaliacao-1-documento-parcial.docx (linha de base de planejamento) sobre o mesmo template."""
from pathlib import Path

import rel_lib as L
import cap_a1, cap_a2, cap_a3, cap_a4, cap_c2
from build_comum import SIGLAS

RAIZ = Path(__file__).resolve().parent.parent
TITULO = "FIELDOPS: PLATAFORMA DE INSPEÇÃO EM CAMPO (MVP). DOCUMENTO PARCIAL DA AVALIAÇÃO 1: DEFINIÇÃO E PLANEJAMENTO INICIAL"

RESUMO = (
    "Este documento apresenta a linha de base de planejamento do FieldOps, uma plataforma de inspeção em campo formada por aplicativo mobile Android com operação offline, interface administrativa web e API REST, "
    "desenvolvida por cinco alunos de Análise e Desenvolvimento de Sistemas em 16 semanas (10/08 a 27/11/2026). Ele reúne a caracterização do projeto e os quatro blocos de requisitos da Avaliação 1: o termo de abertura e a integração; "
    "as partes interessadas e o plano de comunicação, com 13 partes e 19 comunicações; o escopo, com a estrutura analítica de 7 entregas e 36 pacotes de trabalho e os critérios de aceitação; "
    "e o cronograma de 63 atividades e 8 marcos, os recursos e a matriz de responsabilidades. As decisões estão justificadas, e as premissas estão rotuladas: os papéis da equipe foram inferidos dos repositórios e dependem de confirmação. "
    "O documento termina com a lista de entregáveis e o índice de onde cada artefato está no repositório da disciplina."
)
ABSTRACT = (
    "This document presents the planning baseline of FieldOps, a field inspection platform made up of an Android mobile app with offline operation, a web administration interface and a REST API, "
    "built by five Systems Analysis and Development students in 16 weeks (Aug 10 to Nov 27, 2026). It brings together the project description and the four requirement blocks of Assessment 1: the project charter and integration; "
    "stakeholders and the communication plan, with 13 stakeholders and 19 communications; scope, with a work breakdown structure of 7 deliverables and 36 work packages and the acceptance criteria; "
    "and the schedule of 63 activities and 8 milestones, resources and the responsibility matrix. Decisions are justified and assumptions are labeled: team roles were inferred from the repositories and need confirmation. "
    "The document ends with the list of deliverables and an index of where each artifact is in the course repository."
)


def entregaveis(r):
    n = r.N
    c = n['entregaveis']
    r.h1(f"{c} ENTREGÁVEIS DA AVALIAÇÃO 1 E ARTEFATOS NO REPOSITÓRIO")
    r.h2(f"{c}.1 Lista de entregáveis e índice dos artefatos")
    r.par("O enunciado da Avaliação 1 pede seis entregáveis. O quadro mostra onde cada um está neste documento, em que arquivo do repositório está a versão completa (caminhos relativos à pasta entrega/ do repositório da disciplina) e qual é a situação. Os artefatos foram elaborados pelo gerente a partir de uma base única de fatos; a revisão pelo grupo e a aprovação pelo orientador e pela coordenação ainda estão pendentes, e isso está declarado em cada artefato.")
    ent = [
        ["Documento parcial com a caracterização do projeto e os requisitos", "este documento", "projeto-fieldops/avaliacao-1-documento-parcial.docx", "elaborado"],
        ["Termo de abertura", f"capítulo {n['tap']}", "aula-02-integracao/tap-fieldops.md e .docx", "versão 2.0; aprovação da coordenação pendente"],
        ["Registro ou matriz de partes interessadas (+ imagem)", f"capítulo {n['partes']}", "aula-08-aquisicoes-partes-interessadas/matriz-poder-interesse-fieldops.md e .png", "elaborado; notas a validar com o orientador"],
        ["Plano de comunicação", f"capítulo {n['partes']}", "aula-06-rh-comunicacoes/plano-comunicacao-fieldops.md", "elaborado; canais a confirmar com o grupo"],
        ["Declaração de escopo e EAP (+ imagem)", f"capítulo {n['escopo']}", "aula-03-escopo/eap-fieldops.md e .png", "elaborado; revisão da equipe pendente"],
        ["Cronograma inicial (+ Gantt)", f"capítulo {n['crono']}; Apêndice A", "aula-04-tempo/cronograma-fieldops.md e gantt-fieldops.png", "elaborado; datas e durações são estimativas"],
        ["Matriz de responsabilidades (organograma e RACI)", f"capítulo {n['crono']}; Apêndice B", "aula-06-rh-comunicacoes/organograma-raci-fieldops.md e organograma-fieldops.png", "elaborado; R e A por pacote a confirmar com o grupo"],
        ["Base de fatos (códigos, datas, equipe)", "—", "_base/00-base-fieldops.md", "fonte única dos artefatos"],
    ]
    r.tabela("Entregáveis da Avaliação 1, localização neste documento, arquivo no repositório e situação", ["Entregável", "Neste documento", "Arquivo no repositório", "Situação"], ent, [4.3, 2.6, 5.9, 3.2], kind="Quadro", size=8, key="entreg")
    r.h2(f"{c}.2 Critérios de avaliação e onde são atendidos")
    cr = [
        ["Termo de abertura, objetivos, premissas e restrições", "0,75", f"{n['tap']}.1 a {n['tap']}.7"],
        ["Identificação das partes interessadas e plano de comunicação", "0,75", f"{n['partes']}.1 a {n['partes']}.4"],
        ["Definição do escopo, entregas e critérios de aceitação", "1,25", f"{n['escopo']}.1, {n['escopo']}.2, {n['escopo']}.5"],
        ["Qualidade e coerência da EAP", "1,00", f"{n['escopo']}.3, {n['escopo']}.4; {n['tap']}.8"],
        ["Cronograma, recursos, dependências e responsabilidades", "1,00", f"{n['crono']}.1 a {n['crono']}.6; Apêndices A e B"],
        ["Organização, clareza e consistência da entrega parcial", "0,25", f"{n['caract']} (convenções); {c}"],
        ["Total", "5,00", ""],
    ]
    r.tabela("Critérios de avaliação da Avaliação 1 e seções que os atendem", ["Critério", "Pontos", "Seções"], cr, [9, 1.8, 5.2], kind="Tabela", size=9, align=["l", "c", "l"], bold_rows=(6,), key="crit",
             fonte_txt="Enunciado do projeto (material da disciplina), Avaliação 1.")
    r.h2(f"{c}.3 Pontos a confirmar")
    r.par("Antes de a versão final ir ao orientador, o grupo precisa confirmar: (1) os papéis dos integrantes e o responsável e o aprovador de cada pacote; (2) a decisão sobre o painel web em Next.js, com o ADR e a ratificação do orientador; (3) as notas de poder e interesse e os níveis de engajamento; (4) os canais, os horários e as pastas do plano de comunicação; (5) os percentuais e as durações do cronograma, que são estimativas; e (6) as alçadas de aprovação de mudança de escopo.")


def main():
    r = L.Rel(TITULO, RAIZ / "avaliacao-1-documento-parcial.docx", "FieldOps: documento parcial da Avaliação 1", "Gestão de Projetos - Projeto, Avaliação 1")
    r.av2 = False
    r.N = dict(caract=1, tap=2, partes=3, escopo=4, crono=5, entregaveis=6, refs=7, apend=8)
    r.dic = "o arquivo eap-fieldops.md (dicionário da EAP)"
    r.AP = dict(dic="C", raci="B")
    r.resumo(RESUMO, "Gestão de projetos; Termo de abertura; Estrutura analítica do projeto; Cronograma; Partes interessadas.", ABSTRACT, "Project management; Project charter; Work breakdown structure; Schedule; Stakeholders.")
    r.placeholders_listas()
    r.lista_sigla("LISTA DE ABREVIATURAS E SIGLAS", [x for x in SIGLAS if x[0] not in ("BAC", "CPI", "EAC", "EV", "EVM", "PERT", "PV", "RBS", "SPI", "CI")] )
    r.sumario_placeholder()
    cap_a1.caracterizacao(r)
    cap_a2.tap(r)
    cap_a3.partes(r)
    cap_a3.escopo(r)
    cap_a4.crono(r)
    entregaveis(r)
    r.h1("7 REFERÊNCIAS")
    for x in cap_c2.REFS:
        if any(k in x for k in ("CARVALHO", "SOUZA", "PROJECT MANAGEMENT", "SCHWABER", "TODESCO", "FIELDOPS-PROJECT", "TAKATU")):
            r.par(x, first=None, line=1.0, after=12, align=L.LEFT)
    r.h1("8 APÊNDICES", quebra=True)
    r.par("Os apêndices trazem os artefatos completos da linha de base: o cronograma de 71 itens e a matriz RACI de 36 pacotes. O dicionário da EAP, com os critérios de aceitação dos 36 pacotes, está no arquivo eap-fieldops.md.")
    r.secao_paisagem()
    r.h2("Apêndice A – Cronograma inicial (63 atividades e 8 marcos)", quebra=False)
    cap_c2.cronograma_tabela(r, com_status=False)
    r.h2("Apêndice B – Matriz de responsabilidades (RACI de 36 pacotes)", quebra=True)
    cap_c2.raci_tabela(r)
    cont = r.finalizar("gestão de projetos; termo de abertura; EAP; cronograma; partes interessadas")
    print("av1 salvo:", r.saida, cont)


if __name__ == "__main__":
    main()
