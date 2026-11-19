#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta avaliacao-2-relatorio-final.docx sobre o Template - Relatorio Final.docx do professor."""
import sys
from pathlib import Path

import rel_lib as L
import fatos as F
from fatos import rs
import cap_a1, cap_a2, cap_a3, cap_a4, cap_b, cap_c1, cap_c2
from build_comum import SIGLAS

RAIZ = Path(__file__).resolve().parent.parent
TITULO = "PLANEJAMENTO INTEGRADO DO PROJETO FIELDOPS: PLATAFORMA DE INSPEÇÃO EM CAMPO (MVP). RELATÓRIO FINAL"

RESUMO = (
    "Este relatório consolida o planejamento integrado do FieldOps, uma plataforma de inspeção em campo formada por aplicativo mobile Android com operação offline, interface administrativa web e API REST, "
    "desenvolvida por cinco alunos de Análise e Desenvolvimento de Sistemas em 16 semanas (10/08 a 27/11/2026). O trabalho reúne o termo de abertura, as partes interessadas e a comunicação, o escopo e a EAP de 36 pacotes, "
    f"o cronograma de 71 itens e 967 horas, o orçamento por estimativa de três pontos (custo base de {rs(F.CUSTO_BASE)}, linha de base de {rs(F.BAC)} e total de {rs(F.CUSTO_TOTAL)}, valores hipotéticos), "
    "a qualidade com as sete ferramentas aplicadas a dados do GitHub e 22 riscos com 4 oportunidades. Uma matriz de rastreabilidade mostra como as áreas se relacionam, e um capítulo novo define indicadores, "
    "tratamento de desvios, processo de mudanças, aceite e encerramento. Em 18/11/2026, 57 de 103 issues estavam concluídas, e as sprints de offline e de revisão (S6 e S7) tinham 2 de 13 e 2 de 14: "
    "o atraso é tratado como desvio monitorado, com ordem de corte e proposta de re-baseline. Conclui-se que o atraso se concentra no item de maior incerteza, na concentração do trabalho em poucas pessoas e na falta de revisão registrada, "
    "e que, num projeto de capacidade fixa, os desvios se resolvem por escopo e prazo, e não por verba."
)
ABSTRACT = (
    "This report consolidates the integrated plan of FieldOps, a field inspection platform made up of an Android mobile app with offline operation, a web administration interface and a REST API, "
    "built by five Systems Analysis and Development students in 16 weeks (Aug 10 to Nov 27, 2026). It covers the project charter, stakeholders and communication, scope and a 36-package WBS, a 71-item schedule with 967 hours, "
    f"a three-point budget (base cost of BRL {F.br(F.CUSTO_BASE)}, baseline of BRL {F.br(F.BAC)} and total of BRL {F.br(F.CUSTO_TOTAL)}, hypothetical values), quality analysis with the seven basic tools applied to GitHub data, and 22 risks with 4 opportunities. "
    "A traceability matrix shows how the areas relate, and a new chapter defines indicators, deviation handling, change control, acceptance and closure. On Nov 18, 2026, 57 of 103 issues were done, and the offline and review sprints (S6 and S7) had 2 of 13 and 2 of 14: "
    "the delay is handled as a monitored deviation, with a cut order and a rebaseline proposal. The report concludes that the delay concentrates on the most uncertain item, on work concentrated in few people and on missing recorded reviews, "
    "and that in a fixed-capacity project deviations are solved through scope and schedule, not budget."
)


def main():
    r = L.Rel(TITULO, RAIZ / "avaliacao-2-relatorio-final.docx", "Planejamento integrado do projeto FieldOps: relatório final", "Gestão de Projetos - Projeto, Avaliação 2")
    r.av2 = True
    r.N = dict(ident=1, intro=2, caract=3, tap=4, partes=5, escopo=6, crono=7, custos=8, qual=9, riscos=10, monit=11, final=12, refs=13, apend=14)
    r.dic = "Apêndice D"
    r.AP = dict(dic="D", raci="C")
    r.resumo(RESUMO, "Gestão de projetos; Planejamento integrado; Estrutura analítica do projeto; Gerenciamento de riscos; Monitoramento e controle.", ABSTRACT, "Project management; Integrated planning; Work breakdown structure; Risk management; Monitoring and control.")
    r.placeholders_listas()
    r.lista_sigla("LISTA DE ABREVIATURAS E SIGLAS", SIGLAS)
    r.sumario_placeholder()
    cap_a1.identificacao(r)
    cap_a1.introducao(r)
    cap_a1.caracterizacao(r)
    cap_a2.tap(r)
    cap_a3.partes(r)
    cap_a3.escopo(r)
    cap_a4.crono(r)
    cap_b.custos(r)
    cap_b.qualidade(r)
    cap_b.riscos(r)
    cap_c1.monitoramento(r)
    cap_c2.consideracoes(r)
    cap_c2.referencias(r, r.N)
    cap_c2.apendices(r)
    cont = r.finalizar("gestão de projetos; planejamento integrado; EAP; riscos; monitoramento e controle")
    print("av2 salvo:", r.saida, cont)


if __name__ == "__main__":
    main()
