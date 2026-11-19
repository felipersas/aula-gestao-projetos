#!/usr/bin/env python3
"""Gera roteiro-apresentacao-3min.md e confere a contagem de palavras (alvo: 380 a 420)."""
import re
from pathlib import Path

import modelo_portfolio as M
from conteudo import br

RAIZ = Path(__file__).resolve().parent.parent
N_CONF = len(M.CONF_ING)
PCT_T2 = round(100 * sum(M.TRI[:2]) / M.INV_PRIOR)

BLOCOS = [
    ("0:00 a 0:20", "Abertura e pergunta",
     "o título do slide e a faixa de números (R$ 2,1 mi + R$ 0,4 mi).",
     "Boa tarde, diretoria. A pergunta é: como organizar oito projetos, que somam R$ 5,4 milhões, para alcançar quatro metas com R$ 2,5 milhões e uma equipe enxuta? "
     "A resposta está no título do slide: cinco projetos priorizados, R$ 2,1 milhões, e R$ 0,4 milhão de reserva."),
    ("0:20 a 0:55", "1. Projetos priorizados",
     "a tabela do portfólio (coluna Decisão): verdes, depois o amarelo do P7 e os vermelhos. Faixa de metas, embaixo.",
     "Priorizamos P1, P2, P4, P5 e P6. Cada meta ganha um responsável: o P1, automação da Linha 1, produtividade; o P2, manutenção preditiva, paradas; "
     "o P5, controle de qualidade, retrabalho; o P4, redução de refugo, custos. O P6 treina os operadores e protege o investimento do P1. "
     "O P7, IoT, é posterior: só entra se o gate G2, no fim do sexto mês, aprovar. ERP e expansão ficam adiados: juntos custariam R$ 2,7 milhões e nenhum ataca diretamente as quatro metas."),
    ("0:55 a 1:25", "2. Programas",
     "os cartões A, B e C, abaixo da tabela.",
     "Agrupamos em dois programas. O Programa A, Excelência Operacional, reúne P1, P2 e P6, por R$ 1,5 milhão, para produtividade e paradas. "
     "O Programa B, Qualidade 4.0, reúne P4 e P5, por R$ 0,6 milhão, para retrabalho e custos. O Programa C, Transformação Digital, não é ativado agora: ERP e IoT ficam como candidatos a 2027."),
    ("1:25 a 2:00", "3. Recursos e orçamento",
     "a barra de investimento (coluna do meio) e mapa de calor de recursos (coluna da direita); roadmap de passagem.",
     f"No orçamento, R$ 2,1 milhões nos cinco projetos, 84% do teto, mais R$ 400 mil de reserva, que protege o P1, o projeto de risco alto. Cerca de {PCT_T2}% do valor sai nos seis primeiros meses. "
     f"Nos recursos, se tudo começasse junto, o cálculo mostra {N_CONF} sobrecargas. Resolvemos em sequência: qualidade atende o P4 e depois o P5; o P2 não usa engenheiro de automação, que ficam inteiros no P1; "
     "e o treinamento só começa depois do teste de fábrica. Resultado: ninguém passa de 100%."),
    ("2:00 a 2:40", "4. Justificativa principal e riscos",
     "a faixa de metas (marcadores amarelos = sem folga) e quadro de riscos.",
     "A justificativa é cobertura de metas dentro do teto: é a única combinação que dá a cada meta um projeto com benefício medido, sem passar de R$ 2,5 milhões. "
     "Com honestidade: P2 e P5 entregam exatamente a meta, sem folga, e o P1 cobre 12 dos 15 pontos de produtividade. Por isso medimos desde o primeiro mês, com meta interna 10% acima. "
     "Os maiores riscos são benefício parcial, atraso do P1 e um único gerente de projetos; cada um tem resposta no slide."),
    ("2:40 a 3:00", "5. Recomendação e pedido",
     "a faixa verde e preta no rodapé (recomendação e pedido).",
     "Recomendamos aprovar os Programas A e B. O pedido de hoje: aprovar R$ 2,1 milhões, mais a reserva sob gestão do PMO, e nomear a Controladoria para fechar a linha de base até o primeiro mês. "
     "O P7 voltamos a discutir no gate G2, com dados na mão. Obrigado."),
]


def palavras(t):
    return len([x for x in re.split(r"\s+", t.strip()) if re.search(r"\w", x)])


total = sum(palavras(b[3]) for b in BLOCOS)
assert 380 <= total <= 420, total

QA = [
    ("Por que não o P8, a expansão da capacidade?",
     "Consumiria 60% do teto e os 12 meses inteiros, tem risco alto e +20% de capacidade não é nenhuma das quatro metas. A empresa também recomenda executar o P1 antes. "
     "Com o balanço de produtividade do P1 (meses 9 e 12), o P8 volta com números reais."),
    ("Por que não o P3, o ERP?",
     "Custa R$ 1,2 milhão, leva 10 meses, tem risco alto e benefício indireto, e depende do P7 para a etapa de integração. Sem meta numérica, perderia para qualquer projeto priorizado."),
    ("Por que não o P7 já?",
     "O P7 custa R$ 600 mil, mais que a reserva, e exigiria engenheiros e TI que estão no P1 até o mês 6. Ele não é descartado: o gate G2 decide no fim do mês 6, com dados e saldo na mão."),
    ("E se o P1 estourar?",
     "A reserva tem R$ 180 mil dedicados ao P1 (20%). O pedido de equipamentos é conferido no gate G1 (mês 3), o teste de fábrica libera o P6, e o contrato paga por marcos, com multa por atraso. "
     "Se passar da contingência, o comitê decide entre usar o saldo da reserva ou reduzir escopo."),
    ("Onde estão as folgas das metas?",
     "Não há. P2 (-20% de paradas) e P5 (-30% de retrabalho) entregam exatamente a meta: com 90% do benefício, a redução cai para 18% e 27%. O P1 cobre 12 dos 15 pontos de produtividade. "
     "Protegemos com linha de base no mês 1, meta interna 10% acima, aceite condicionado a indicador e balanços nos meses 9 e 12."),
    ("O gerente de projetos não é um gargalo?",
     f"É o ponto único de falha, e dizemos isso no slide. Sem apoio, a demanda chegaria a {round(max(M.GP_SEM_COORD))}% no mês 1. Com coordenadores locais cai para {M.PICO['GP']}%. "
     "Se passar de 90% por dois meses seguidos, contratamos um analista de planejamento externo, R$ 55 mil da reserva."),
    ("Por que reserva de 16%?",
     f"Os R$ 400 mil cobrem {br(M.RESERVA / M.EMV_TOTAL, 1)} vez o custo esperado dos riscos de custo (R$ {br(M.EMV_TOTAL)} mil, hipótese do grupo): contingências de 20% para P1 e P2, 10% para os demais e o analista externo. "
     "Não cobre o pior caso de P1 e P2 juntos (R$ 540 mil), por isso é liberada só por gatilho."),
    ("O que acontece no gate G2?",
     "No fim do mês 6 o comitê confere quatro coisas: P2 e P4 no prazo, P1 com teste de fábrica aprovado, recurso (saldo da reserva, economias auditadas ou complemento) e engenheiros livres. "
     "Resultados: iniciar o P7, iniciar uma fase 1 menor, ou adiar para 2027. Mesmo sem usar a reserva faltam R$ 200 mil para o P7 inteiro."),
    ("Como vocês vão medir o benefício?",
     "Linha de base de cinco indicadores (peças boas por hora-homem, horas de parada, retrabalho, refugo e custo por peça), aprovada pela Controladoria no mês 1. "
     "Relatório mensal de uma página, balanço parcial no mês 9 e final no mês 12, com gatilho se o indicador ficar abaixo de 90% da trajetória."),
    ("Dá para fazer só com os projetos baratos, sem o P1?",
     "É o cenário C, R$ 1,8 milhão. Quase empata na pontuação, mas sem o P1 nenhum projeto quantifica ganho de produtividade, e a meta de +15% fica descoberta. Preferimos assumir o risco do P1 com reserva."),
    ("Por que treinar operadores se o P6 não tem número de benefício?",
     "Porque ele protege R$ 900 mil: sem operador preparado, o P1 não entrega os +12%. Custa R$ 150 mil, 2 meses, risco baixo, e o conteúdo vem do fornecedor do P1."),
]

DICAS = [
    "Cronometre três vezes com o slide aberto; o alvo é terminar entre 2:50 e 3:00. O texto tem " + str(total) + " palavras, o que dá cerca de 135 palavras por minuto.",
    "Decore a frase de abertura e a de fechamento; o miolo pode ser dito com suas palavras desde que os números fiquem iguais aos do slide.",
    "Números para memorizar: 8 projetos, R$ 5,4 mi; 5 priorizados, R$ 2,1 mi (84%); reserva R$ 0,4 mi (16%); programas A R$ 1,5 mi e B R$ 0,6 mi; G2 no fim do mês 6; " + f"{N_CONF} sobrecargas evitadas.",
    "Aponte, não leia: a cada bloco, olhe para a diretoria e use a mão ou o apontador na região do slide indicada na tabela.",
    "Se o tempo estourar, corte nesta ordem: a lista de recursos resolvidos (bloco 3), a frase dos riscos (bloco 4) e a menção ao Programa C (bloco 2). Nunca corte o pedido final.",
    "Peça a um colega para fazer as perguntas da seção abaixo e treine respostas de até 30 segundos.",
    "Não prometa o que o plano não promete: diga 'meta sem folga' e 'hipótese do grupo' sempre que for o caso. A honestidade dos limites é parte do argumento.",
]

L = []


def w(t=""):
    L.append(t)


w("# Roteiro de apresentação (3 minutos) — MetalTech S.A.")
w()
w("| Campo | Conteúdo |")
w("|:---|:---|")
w("| Apresentador | um integrante do grupo (Felipe Marques, Gabriel Ribeiro, Pedro Dias, André Fernandes ou João Victor Souza) |")
w("| Material | `slide-executivo.pptx` (1 slide) |")
w("| Tempo máximo | 3 minutos |")
w(f"| Palavras faladas | {total} (alvo de 380 a 420; contagem por `scripts/gerar_roteiro.py`) |")
w("| Perguntas do enunciado | 1) projetos priorizados; 2) programas; 3) recursos e orçamento; 4) principal justificativa; 5) recomendação final |")
w()
w("## 1. Roteiro cronometrado")
w()
JAN = [20, 35, 30, 35, 40, 20]
w("| Tempo | Bloco | Apontar no slide | Palavras | Duração estimada a 135 palavras/min |")
w("|:---|:---|:---|---:|---:|")
for (t, n, ap, fala), j in zip(BLOCOS, JAN):
    w(f"| {t} | {n} | {ap} | {palavras(fala)} | {round(palavras(fala) * 60 / 135)} s (janela de {j} s) |")
w(f"| **Total** | | | **{total}** | **{round(total * 60 / 135)} s** (limite de 180 s) |")
w()
for t, n, ap, fala in BLOCOS:
    w(f"### {t} — {n}")
    w()
    w(f"*Apontar: {ap}*")
    w()
    w(f"> {fala}")
    w()
w("## 2. Texto corrido (para ensaio)")
w()
w(" ".join(b[3] for b in BLOCOS))
w()
w("## 3. Perguntas prováveis da diretoria")
w()
w("Respostas curtas (cerca de 20 a 30 segundos). Os números são os mesmos de `analise-portfolio.md`.")
w()
for i, (q, a) in enumerate(QA, 1):
    w(f"**{i}. {q}**")
    w()
    w(a)
    w()
w("## 4. Dicas de ensaio")
w()
for d in DICAS:
    w(f"- {d}")
w()
Path(RAIZ / "roteiro-apresentacao-3min.md").write_text("\n".join(L), encoding="utf-8")
print("palavras por bloco:", [palavras(b[3]) for b in BLOCOS], "total", total, "| perguntas:", len(QA))
