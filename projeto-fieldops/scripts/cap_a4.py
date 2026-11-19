# -*- coding: utf-8 -*-
"""Capitulo: cronograma, recursos e responsabilidades."""
import re
from collections import Counter

import dados as DD
import fatos as F
from fatos import br, rs, pct

SPRINT_INFO = [  # sprint, periodo, du, marco, epicos
    ("S1", "10/08–21/08", 10, "M1 Fundação (21/08)", "EP-01"), ("S2", "24/08–04/09", 10, "M2 Autenticação (04/09)", "EP-02, EP-03"),
    ("S3", "07/09–18/09", 9, "M3 Planejamento (18/09)", "EP-04, EP-05"), ("S4", "21/09–02/10", 10, "M4 Execução online (02/10)", "EP-05 (PBI-030), EP-06"),
    ("S5", "05/10–16/10", 9, "M5 Recursos nativos (16/10)", "EP-07"), ("S6", "19/10–30/10", 10, "M6 Offline (30/10)", "EP-08"),
    ("S7", "02/11–13/11", 9, "M7 Revisão (13/11)", "EP-09, EP-10"), ("S8", "16/11–27/11", 9, "M8 Release (27/11)", "EP-10"),
]


def tipos_dep():
    c = Counter()
    for a in F.CRONO:
        for tok in re.findall(r"\((TI|II|TT|IT)\)", a["pred"]):
            c[tok] += 1
    return c


def crono(r):
    n = r.N
    c = n['crono']
    r.h1(f"{c} CRONOGRAMA, RECURSOS E RESPONSABILIDADES")
    r.h2(f"{c}.1 Decomposição, durações e dependências")
    td = tipos_dep()
    tot = sum(td.values())
    r.par(f"As sete entregas da EAP foram decompostas em **63 atividades**, todas ligadas a um dos 36 pacotes, mais **8 marcos** de duração zero (M1 a M8): 71 itens, acima do mínimo de 50 pedido na disciplina. Cada atividade tem início, término, duração, responsável, predecessoras com tipo, esforço em horas e sprint. As durações são **estimativas** em dias úteis, contados de segunda a sexta, com os feriados em dia útil descontados (07/09, 12/10, 02/11 e 20/11; 15/11 cai num domingo e não afeta o prazo). O esforço é trabalho, não prazo: cada pessoa dedica 12 horas por semana (2,4 h por dia útil), em paralelo a outras atividades. O total é de **967 h**, 0,7% acima da capacidade de referência de 960 h; por pessoa, FM {F.HORAS_P['FM']} h, JV {F.HORAS_P['JV']} h, GR {F.HORAS_P['GR']} h, PD {F.HORAS_P['PD']} h e AF {F.HORAS_P['AF']} h, todos dentro de ±15% de 192 h.")
    r.par(f"As dependências são de quatro tipos, conforme a convenção do cronograma: término a início (TI), início a início (II), término a término (TT) e início a término (IT, não usado). Há {tot} relações no total, das quais {td['TI']} TI, {td['II']} II e {td['TT']} TT, e um script confere que nenhuma atividade começa antes do que as predecessoras permitem. A ordem técnica que o roteiro de integração exige é: contrato OpenAPI antes de integrar (RJ01); login antes de cadastros; modelo publicado antes de agendar; checklist online antes de offline; push de sincronização antes do pull; fluxo de correção antes do teste de reprovação a aprovação; build EAS antes do teste final em Android. Os marcos funcionam como portões (premissa de gestão): as atividades de abertura da sprint seguinte dependem do marco anterior.")
    r.h2(f"{c}.2 Sequência, marcos e sprints")
    cs = DD.curva_s()
    linhas = []
    for (sp, per, du, marco, ep), row in zip(SPRINT_INFO, cs):
        nat = sum(1 for a in F.ATIV if a["sprint"].split("–")[-1] == sp)
        linhas.append([sp, per, str(du), marco, ep, str(nat), row[2]])
    linhas.append(["Total", "10/08–27/11", "76", "8 marcos", "10 épicos", "63", "967"])
    r.tabela("Sprints, marcos, épicos, atividades concluídas na sprint e horas planejadas", ["Sprint", "Período", "Dias úteis", "Marco", "Épicos", "Ativ. que terminam", "Horas"], linhas, [1.2, 2.3, 1.2, 4.0, 3.0, 1.9, 1.4], kind="Tabela", size=8.5,
             align=["c", "c", "c", "l", "l", "c", "r"], bold_rows=(8,), fonte_txt="cronograma-fieldops.md; horas por sprint do orçamento (cenário mais provável, arredondadas). Os marcos e seus critérios estão no @Q:marcos@.", key="sprints")
    r.h2(f"{c}.3 Cronograma e caminho crítico")
    r.par("A @F:gantt@ mostra o cronograma por pacote da EAP, com a janela planejada de cada pacote (da primeira à última atividade)" + (" e a parcela estimada como realizada em 18/11/2026. O cronograma completo, com as 71 linhas, está no Apêndice A." if r.av2 else ". O cronograma completo, com as 71 linhas, está no Apêndice A."))
    if r.av2:
        r.figura("gantt_pacotes.png", "Cronograma por pacote da EAP: janela planejada e parcela realizada em 18/11/2026", 14.5, altura_max_cm=18.5, key="gantt",
                 fonte_txt="Elaborado pelos autores (2026), a partir de cronograma-fieldops.md. Realizado: percentual por atividade estimado pelo gerente (premissa P7), ponderado por horas. Diagrama original por atividade: gantt-fieldops.png.")
    else:
        r.figura("gantt_baseline.png", "Cronograma por pacote da EAP: janela planejada de cada pacote e marcos M1 a M8", 14.5, altura_max_cm=18.5, key="gantt",
                 fonte_txt="Elaborado pelos autores (2026), a partir de cronograma-fieldops.md (linha de base).")
    crit = [a for a in F.ATIV if a["critica"]]
    assert len(crit) == 20, len(crit)
    por_sp = {}
    for a in crit:
        por_sp.setdefault(a["sprint"].split("–")[-1], []).append(a)
    linhas = [[sp, ", ".join(f"{a['id']} ({a['resp']})" for a in sorted(v, key=lambda x: x['id']))] for sp, v in sorted(por_sp.items())]
    r.par("O caminho crítico foi encontrado em duas passagens: primeiro cada atividade foi posicionada na data mais cedo que as predecessoras e a abertura da sprint permitem; depois, uma passagem para trás a partir do marco M8, em 27/11, calculou em dias úteis o término mais tardio de cada atividade, respeitando o tipo de cada dependência. A folga total é o término mais tardio menos o término planejado, e o caminho crítico é o conjunto com folga zero. Não houve nivelamento de recursos. O resultado é uma corrente sem folga de 10/08 a 27/11, com **20 atividades e 8 marcos**, na qual **quase todas as atividades são do backend** (API e contrato); as exceções são os testes de integração, a build EAS e a demonstração final. " + ("O @Q:critico@ lista as atividades críticas por sprint." if r.av2 else "As atividades críticas estão marcadas com CC no Apêndice A e são, quase todas, do backend: A01 e A07 (JV) em S1; A09 (JV) e A14 (GR) em S2; A17 e A22 (GR) e A24 (PD) em S3; A27 (JV) em S4; A31 e A39 (JV) em S5; A40 e A46 (JV) e A49 (PD) em S6; A51, A53 e A55 (PD) e A54 (GR) em S7; A57 (FM), A61 (PD) e A63 (FM) em S8."))
    if r.av2:
        r.tabela("Atividades do caminho crítico por sprint (responsável entre parênteses)", ["Sprint", "Atividades críticas"], linhas, [1.5, 14.5], kind="Quadro", size=8.5, align=["c", "l"],
             fonte_txt="cronograma-fieldops.md, seção Caminho crítico. Atividades com folga de 1 dia útil (27, como A04, A05 e A29) e de 2 dias úteis (A03 e A18) são quase críticas.", key="critico")
    r.par("Essa leitura casa com o que o GitHub mostra: o backend é o repositório mais atrasado (14 de 41 issues fechadas), e a sincronização é o ponto em que a corrente quebrou. Como toda a corrente é do backend, qualquer atraso ali se propaga direto até M8. Há ainda 27 atividades com folga de apenas um dia útil, o que significa que um dia de atraso já consome a única folga antes do marco. Como o plano não reserva folga entre M7 e M8 além de 1 dia útil, e S8 tem 9 dias úteis por causa do feriado de 20/11, recomenda-se que re-baselines futuros reservem ao menos uma semana de colchão antes da demonstração final.")
    r.h2(f"{c}.4 Recursos humanos")
    r.par("Os recursos humanos são os cinco integrantes, sem contratação e com compromissos concorrentes de outras disciplinas. O quadro mostra o papel, as horas e a participação de cada um. Os papéis são **proposta a confirmar**, e as horas por pessoa incluem o apoio que cada um dá a atividades de que não é o responsável (por isso a soma de horas como responsável é menor que a de horas lançadas).")
    media = sum(F.HORAS_P.values()) / 5
    linhas = []
    papel = {"FM": "Gerente + dev. mobile", "JV": "Dev. backend, líder técnico", "GR": "Dev. backend, cadastros e testes", "PD": "Dev. backend + offline no app + docs", "AF": "Dev. web (Next.js)"}
    for p in F.PESSOAS:
        nat = sum(1 for a in F.ATIV if a["resp"] == p)
        rr = F.CONTA[p][0]
        linhas.append([f"{p} {F.NOME_P[p]}", papel[p], str(nat), str(rr), str(F.HORAS_P[p]), f"{(F.HORAS_P[p] / media - 1) * 100:+.1f}%".replace(".", ",")])
    linhas.append(["Total", "", "63", "36", "967", "média 193,4 h"])
    r.tabela("Equipe: papel, atividades e pacotes como responsável, horas e desvio da média", ["Integrante", "Papel proposto", "Ativ. (R)", "Pacotes (R)", "Horas", "Desvio"], linhas, [3.8, 4.8, 1.3, 1.5, 1.2, 2.2], kind="Tabela", size=8.5,
             align=["l", "l", "c", "c", "r", "r"], bold_rows=(5,), fonte_txt="cronograma-fieldops.md (seção Responsáveis) e organograma-raci-fieldops.md. Papéis: proposta a confirmar com o grupo.", key="equipe2")
    r.par("A carga por sprint mostra onde a distribuição uniforme esconde picos. A capacidade é de 24 h por pessoa por sprint (2 semanas × 12 h); " + ("o @Q:carga@ destaca em amarelo as combinações pessoa × sprint até 30 h (125%) e em vermelho as acima disso." if r.av2 else "a distribuição uniforme do esforço pelos dias úteis de cada atividade mostra picos acima de 30 h por sprint nas sprints S3 a S8, o que é um ponto de atenção para a execução.") + " Das 40 combinações, 9 estão em vermelho e 9 em amarelo. O gerente (FM) tem vermelho em S4, S5, S6 e S8, porque soma gestão, cinco pacotes de mobile e a build e demonstração final: é a evidência de sobrecarga e de ponto único de falha tratada nos riscos (R04). Os picos de S3 (GR e AF) e de S7 (AF e PD) vêm de atividades que precisam terminar antes do marco.")
    if r.av2:
        cab = ["Pessoa", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "Total", "Pico semanal"]
        linhas, fills = [], {}
        for i, row in enumerate(DD.carga_sprint(), 1):
            linhas.append(row[:11])
            for j in range(1, 9):
                v = float(row[j].replace(",", "."))
                if v > 30:
                    fills[(i, j)] = "F4C7C3"
                elif v > 24:
                    fills[(i, j)] = "FBE9B7"
        r.tabela("Carga por pessoa e sprint (horas; capacidade de 24 h por sprint)", cab, linhas, [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.4, 3.0], kind="Tabela", size=8.5, align=["l"] + ["c"] * 8 + ["c", "c"], cell_fills=fills,
                 fonte_txt="cronograma-fieldops.md, esforço distribuído uniformemente pelos dias úteis de cada atividade. Amarelo: acima de 24 h; vermelho: acima de 30 h.", key="carga")
    r.h2(f"{c}.5 Recursos materiais e tecnológicos")
    r.par("Os recursos materiais e tecnológicos são, em sua maioria, gratuitos ou já disponíveis (restrição R07), e os que têm custo estão na tabela de aquisições, com a numeração P01 a P14 (capítulo %s)." % (n['custos'] if r.av2 else "de custos da Avaliação 2"))
    mat = [
        ["Estações de trabalho, internet e energia", "equipamentos próprios dos integrantes; laboratório do campus (PI-13) quando necessário", "P14 (rateio, não-caixa)"],
        ["Dispositivos Android para teste (RJ05)", "3 aparelhos da equipe; aparelho de entrada e teste em nuvem como contingência", "P09, P10, P12"],
        ["Ambiente de desenvolvimento", "VS Code, Android Studio, Docker Desktop, IntelliJ, Postman, Figma Education (licenças gratuitas ou educacionais)", "P13"],
        ["Colaboração e CI", "organização GitHub FieldOps-Project (4 repositórios, Actions e Projects)", "P06"],
        ["Infraestrutura de demonstração", "hospedagem da API em contêiner, PostgreSQL gerenciado, armazenamento S3, hospedagem do painel Next.js, domínio", "P01, P02, P03, P04, P07"],
        ["Build e distribuição do app", "Expo EAS (plano pago em semana de pico; build local como plano B); conta Google Play apenas se exigida", "P05, P11"],
        ["Monitoramento", "monitoramento de erros e logs de web, app e API", "P08"],
    ]
    r.tabela("Recursos materiais e tecnológicos e itens de aquisição relacionados", ["Recurso", "Descrição", "Aquisição"], mat, [4.3, 8.9, 2.8], kind="Quadro", size=8.5, fonte_txt="aquisicoes-fieldops.md e cronograma-fieldops.md.", key="recmat")
    r.h2(f"{c}.6 Responsabilidades: organograma e matriz RACI")
    r.par("O organograma mostra a estrutura hierárquica e as partes interessadas que avaliam ou influenciam sem comandar a equipe (@F:org@). O comitê executivo (PI-01 e PI-03) e o orientador (PI-02) estão acima do gerente; o gerente coordena as frentes de backend, web, mobile e qualidade e documentação. PD aparece em três frentes, e AF e GR em duas, porque a divisão por pacote atravessa as frentes.")
    r.figura("organograma_ret.png", "Organograma do projeto FieldOps", 14.0, altura_max_cm=10.5, fonte_txt="Elaborado pelos autores (2026), a partir de organograma-raci-fieldops.md (original: organograma-fieldops.png). Linhas pontilhadas: partes interessadas sem comando sobre a equipe.", key="org")
    r.par("A matriz RACI cobre os 36 pacotes, com **exatamente um aprovador (A) e pelo menos um responsável (R) por linha**, conferido por script. Quem é A não aprova o próprio pull request de código: o aceite do pacote é diferente da revisão do PR, que o CONTRIBUTING.md exige de outro membro. O consultado (C) responde em até dois dias úteis; se não responder, o R segue e registra a decisão. R e A de cada pacote são **proposta do gerente a confirmar com o grupo**. A matriz completa está no Apêndice " + r.AP['raci'] + (r"; o @Q:raciq@ resume a contagem por pessoa." if r.av2 else "."))
    if r.av2:
        linhas = []
        nomes = {"FM": "FM Felipe Marques", "JV": "JV João Victor", "GR": "GR Gabriel Ribeiro", "PD": "PD Pedro Dias", "AF": "AF André Fernandes", "PI-01": "PI-01 Coordenação", "PI-02": "PI-02 Prof. Glauco", "PI-03": "PI-03 Comitê"}
        for p, (rr, aa, cc, ii) in F.CONTA.items():
            linhas.append([nomes[p], str(rr), str(aa), str(cc), str(ii), f"{3 * rr + 2 * aa + cc + 0.25 * ii:.1f}".replace(".", ",")])
        r.tabela("Contagem de R, A, C e I por pessoa e parte interessada", ["Pessoa ou parte", "R", "A", "C", "I", "Carga ponderada"], linhas, [5.0, 1.4, 1.4, 1.4, 1.4, 2.6], kind="Tabela", size=8.5, align=["l", "c", "c", "c", "c", "c"],
                 fonte_txt="organograma-raci-fieldops.md, seção 4.2. Carga ponderada = 3R + 2A + 1C + 0,25I, heurística do gerente (pesos são premissa, não padrão do PMBOK). A/R conta um R e um A.", key="raciq")
    r.par("Os números mostram dois desequilíbrios. FM acumula 11 R, 21 A e 7 C, aparece nos 36 pacotes (100% da EAP) e tem carga ponderada de 82,0, contra 31,5 de GR; os três pacotes com A/R (5.1, 5.3 e 5.5) são o único caso em que ninguém revisa o aceite. AF é o único R do painel web (7 pacotes) e é consultado em 20 pacotes: sem ele, o painel não evolui. A recomendação do RACI é delegar aceites (o cenário B, não adotado: A de 2.3, 6.1 e 6.2 para JV e de 6.3, 6.4 e 7.3 para GR; R de 1.1 para PD e de 7.2 para JV), o que reduziria a carga de FM de 82,0 para 67,5, sem eliminar a concentração. A suplência proposta é FM (gestão) por JV, FM (app) por PD, AF por JV com revisão de GR, JV por GR e PD por GR (premissa a confirmar).")
    if r.av2:
        situacao(r, c)


def situacao(r, c):
    n = r.N
    r.h2(f"{c}.7 Situação em 18/11/2026 e re-baseline")
    r.par("A linha de base acima é a do planejamento. Em 18/11/2026, na semana 15, o realizado fica bem abaixo dela. A medida oficial de avanço são as **issues concluídas por sprint** nos milestones do GitHub (4 repositórios somados): 57 de 103 (55,3%). O percentual de cada atividade é uma **estimativa do gerente, calibrada para reproduzir a razão de issues de cada sprint** (diferença máxima de 0,6 ponto percentual), porque o GitHub não informa avanço por atividade; precisa ser confirmada com o grupo antes de virar medição oficial. O @Q:plan_real@ compara o planejado com o realizado por sprint, e a @F:burnup@ mostra o mesmo dado em forma de burnup.")
    linhas = []
    for row in DD.sprints_status():
        sp, per, marco, conc, real, plan, spi, _, esf = row
        sit = "—" if sp == "Total" else ("verde" if float(spi.replace(",", ".")) >= 0.95 else "amarelo" if float(spi.replace(",", ".")) >= 0.70 else "vermelho")
        if sp == "Total":
            sit = "vermelho"
        linhas.append([sp, per, marco, conc, real, plan, spi, sit, esf])
    fills = {}
    cor = {"verde": "CFE8D5", "amarelo": "FBE9B7", "vermelho": "F4C7C3"}
    for i, l in enumerate(linhas, 1):
        fills[(i, 7)] = cor[l[7]]
    r.tabela("Planejado × realizado por sprint em 18/11/2026", ["Sprint", "Período", "Marco", "Issues concluídas", "Realizado (issues)", "Planejado em 18/11", "SPI", "Sinal", "Realizado por esforço (est.)"], linhas,
             [1.1, 2.1, 1.2, 2.0, 1.9, 1.9, 1.0, 1.5, 2.3], kind="Tabela", size=8, align=["c", "c", "c", "c", "r", "r", "c", "c", "r"], bold_rows=(8,), cell_fills=fills,
             fonte_txt="cronograma-fieldops.md, seção Acompanhamento (GitHub, 18/11/2026). SPI = realizado ÷ planejado; sinal: verde a partir de 0,95, amarelo de 0,70 a 0,94, vermelho abaixo de 0,70. Planejado em S8: fração dos dias úteis decorridos.", key="plan_real")
    r.figura("burnup_sprints.png", "Burnup de issues e conclusão por sprint em 18/11/2026", 15.0, altura_max_cm=7.5, key="burnup",
             fonte_txt="Elaborado pelos autores (2026), a partir dos milestones do GitHub (4 repositórios) em 18/11/2026: 57 de 103 issues concluídas. As issues são alocadas à sprint do milestone, não à data de fechamento.")
    r.par("O dado crítico é que S6 (offline e sincronização) tem 2 de 13 issues e S7 (revisão) 2 de 14, com o calendário já na semana 15. S5 (4 de 8) também carrega pendências, e S3 e S4 foram aceitas com pendências. Das 63 atividades, 22 estão concluídas, 5 em atenção, 33 atrasadas e 3 ainda não iniciadas. Os marcos M5, M6 e M7 não foram atingidos; M1, M3 e M4 foram atingidos com pendências; só M2 foi atingido por inteiro; M8 é futuro e está em risco alto. O backend concentra o atraso, e 21 issues abertas dele não têm responsável.")
    cap = DD.capacidade()
    r.par("O que falta é muito maior do que a capacidade restante. Do esforço planejado de 967 h, cerca de 469 h (48,5%) estão realizadas por estimativa, o que deixa **498 h** por fazer. Restam 6 dias úteis até 27/11 (19, 23, 24, 25, 26 e 27/11), ou 72 h de capacidade da equipe (5 pessoas × 2,4 h × 6 dias): o trabalho restante é **6,9 vezes** a capacidade. O ritmo necessário em issues é igualmente fora de escala: 46 issues abertas em 6 dias úteis exigem cerca de 7,7 issues por dia útil, contra uma média de 1,1 nas sprints S1 a S5 (cálculo feito para este relatório). Com a capacidade atual e sem cortes, o fim do projeto iria para cerca de 19/01/2027; se apenas o que falta da corrente crítica (32,5 dias úteis) fosse executado em sequência e sem compressão, o M8 ocorreria por volta de 06/01/2027. As duas datas são projeções de ordem de grandeza, e não previsões; elas diferem porque partem de bases diferentes (esforço restante total e corrente crítica).")
    atrasos = DD.atrasos_acoes()
    linhas = [[a[0], a[1], a[3], a[4], a[5]] for a in atrasos]
    r.tabela("Atrasos identificados, ação corretiva, responsável e prazo (RJ07)", ["Atividades (sprint)", "Problema", "Ação planejada", "Resp.", "Prazo"], linhas, [2.6, 4.2, 6.1, 1.2, 1.9], kind="Quadro", size=7.5,
             fonte_txt="cronograma-fieldops.md, seção Atrasos e ações. Ações e prazos propostos pelo gerente, ainda por confirmar com o grupo e com o orientador.", key="atrasos")
    cortes, cenarios = DD.cortes()
    linhas = [[a[0], a[1], a[2], a[3]] for a in cortes]
    r.par("A ordem de corte do RJ07 foi aplicada às atividades afetadas. As economias são **estimativas do gerente** sobre o esforço restante e somam cerca de 22 h, contra 498 h por fazer; o núcleo (autenticação, planejamento, checklist, foto, offline, sincronização e revisão) não pode ser cortado. Os seis cortes, portanto, não resolvem: a decisão que falta é de prazo e de escopo do marco final.")
    r.tabela("Ordem de corte aplicada (RJ07) e economia estimada", ["Ordem", "Corte", "Atividades afetadas", "Economia (h)"], linhas, [1.3, 5.7, 6.5, 2.5], kind="Tabela", size=8.5, align=["c", "l", "l", "r"], bold_rows=(6,),
             fonte_txt="cronograma-fieldops.md, seção Atrasos e ações. Economia estimada pelo gerente (premissa).", key="cortes")
    linhas = [[a[0], a[1], a[2], a[3]] for a in cenarios]
    r.tabela("Cenários de decisão para o marco final", ["Cenário", "O que muda", "Efeito", "Condição"], linhas, [3.6, 3.8, 4.8, 3.8], kind="Quadro", size=8.5, fonte_txt="cronograma-fieldops.md, seção Atrasos e ações.", key="cenarios")
    r.par("A recomendação do gerente, **a validar com o grupo e o orientador**, é o cenário C: aplicar já os cortes 1 a 6, tratar a sincronização como prioridade número um, e fazer um **re-baseline** em que o M8 demonstra criar, atribuir, executar, sincronizar e revisar com o que estiver pronto, e o restante vira um marco M8b. O cálculo que sustenta o cenário é que 476 horas, a 60 horas por semana de equipe, levam cerca de 8 semanas. A decisão exige aprovação formal do comitê (PI-01, PI-02 e PI-03): o roadmap diz que as semanas 17 a 20 do calendário institucional não são dependência de entrega, e usá-las é decisão deles, e não do gerente. Até lá, o relatório de status passa a semanal. A matéria é tratada como mudança de classe 3 no processo do capítulo %d." % n['monit'])
