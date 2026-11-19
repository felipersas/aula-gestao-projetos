# -*- coding: utf-8 -*-
"""Capitulos: termo de abertura e integracao; partes interessadas e comunicacao."""
import dados as DD
import fatos as F
from fatos import br, rs, pct


def faixa_marcos(ms):
    nums = sorted({int(m[1]) for m in ms})
    if not nums:
        return "—"
    partes, ini, ant = [], nums[0], nums[0]
    for x in nums[1:] + [None]:
        if x is not None and x == ant + 1:
            ant = x
            continue
        partes.append(f"M{ini}" if ini == ant else (f"M{ini}, M{ant}" if ant == ini + 1 else f"M{ini} a M{ant}"))
        ini = ant = x
    return ", ".join(partes)


def tap(r):
    n = r.N
    t = n['tap']
    r.h1(f"{t} TERMO DE ABERTURA E INTEGRAÇÃO")
    r.par("O termo de abertura (TAP) formaliza o projeto, a autoridade do gerente e os limites dentro dos quais ele opera. A versão consolidada (2.0, de 18/11/2026) reconcilia o TAP de 30/09/2026, o PDF anterior do repositório docs e a Declaração de Escopo de 04/10/2026 com a documentação do produto e o estado dos repositórios. O que não está em documento do projeto aparece como premissa.")
    r.h2(f"{t}.1 Objetivos e resultados esperados")
    r.par("**Objetivo geral.** Desenvolver e entregar, até 27/11/2026, o MVP do FieldOps: uma plataforma integrada, formada por aplicativo mobile Android com operação offline, interface administrativa web e API REST central, que permita configurar, planejar, executar, sincronizar, revisar e auditar inspeções técnicas em campo de forma padronizada, segura e rastreável, substituindo formulários em papel, planilhas e registros informais por um fluxo digital único.")
    r.par("**Objetivos específicos**, com os requisitos que cada um atende:")
    r.alineas([
        "padronizar as inspeções com modelos de checklist versionados e reutilizáveis (RP05)",
        "permitir a execução offline, com sincronização idempotente e sem perda ou duplicidade de dados (RP02, RP03)",
        "dar ao supervisor visibilidade do andamento, das evidências e das não conformidades (RP04, RP08)",
        "centralizar cadastros e autorização por perfil em uma API validada no backend (RP06, RP07)",
        "estabelecer um fluxo formal de revisão, aprovação e reprovação, com histórico e auditoria (RP09, RP10)",
        "demonstrar o fluxo completo no marco M8 e cumprir os marcos quinzenais M1 a M8 (RJ02)",
    ])
    r.h2(f"{t}.2 Contexto e justificativa")
    r.par("Planilhas compartilhadas e formulários genéricos não resolvem o problema: não funcionam sem internet, não ligam a evidência ao equipamento, não têm fluxo formal de revisão e não guardam histórico auditável. Por isso a opção é uma plataforma própria. Os benefícios esperados são a padronização por modelos versionados, menos retrabalho e menos campos em branco, a associação direta entre resposta, evidência, data, usuário, equipamento e localização, a execução em locais sem conectividade, o menor intervalo entre o campo e o resultado, e a menor dependência de acesso ao banco ou ao Swagger nas tarefas administrativas. Há ainda um benefício acadêmico: integrar mobile, backend e web em um produto realista, com Git, pull request e revisão de código.")
    r.h2(f"{t}.3 Premissas e restrições")
    pr = [
        ["P01", "Android é a plataforma mobile prioritária, com validação obrigatória em Android"],
        ["P02", "O sistema será usado por uma organização operadora que presta inspeções a vários clientes"],
        ["P03", "Cada inspeção tem um técnico responsável e o supervisor revisa o resultado"],
        ["P04", "As inspeções partem de modelos previamente configurados; o equipamento é identificado por QR Code único"],
        ["P05", "O app preserva dados não sincronizados mesmo fechado; a API é o registro oficial depois da sincronização"],
        ["P06", "As 16 semanas efetivas (10/08 a 27/11) são o limite do MVP; as 4 semanas restantes do calendário não são reserva"],
        ["P07", "A equipe tem dispositivos Android próprios e ferramentas gratuitas ou já disponíveis"],
        ["P08", "Os papéis dos integrantes foram inferidos dos repositórios e precisam de confirmação do grupo (premissa deste TAP)"],
        ["P09", "A dedicação é de 12 h por semana por pessoa: 5 pessoas × 16 semanas × 12 h = 960 h (premissa deste TAP)"],
    ]
    rs_ = [
        ["R01", "Android como plataforma prioritária, com validação obrigatória"],
        ["R02", "Prazo fixo de 16 semanas efetivas para o MVP"],
        ["R03", "Stack definida: Expo/React Native + TypeScript (mobile), Java/Spring Boot + PostgreSQL (API) e Next.js/React + TypeScript (web, conforme a decisão registrada na seção %s.7)" % t],
        ["R04", "A interface administrativa faz parte do MVP e não pode ser substituída por Swagger ou acesso direto ao banco"],
        ["R05", "Um único técnico responsável por inspeção no MVP"],
        ["R06", "Os itens excluídos do escopo não serão desenvolvidos"],
        ["R07", "Sem investimento financeiro direto: só recursos gratuitos ou já disponíveis"],
    ]
    r.tabela("Premissas do projeto", ["ID", "Premissa"], pr, [1.3, 14.7], kind="Quadro", size=9, align=["c", "l"], key="premissas")
    r.tabela("Restrições do projeto", ["ID", "Restrição"], rs_, [1.3, 14.7], kind="Quadro", size=9, align=["c", "l"], key="restricoes")
    r.h2(f"{t}.4 Entregas principais e marcos")
    r.par("As entregas principais são os sete ramos de nível 1 da EAP (capítulo %d): Gerenciamento do Projeto, Fundação Técnica, API REST Central, Interface Administrativa Web, Aplicativo Mobile (Android), Qualidade e Testes, e Entrega e Release (M8). Os oito marcos, com datas, incrementos demonstráveis e peso na avaliação, estão no @Q:marcos@. Cada marco funciona como portão: as atividades de abertura da sprint seguinte só começam depois da demonstração aceita (escolha de gestão, e não restrição técnica)." % n['escopo'])
    r.h2(f"{t}.5 Estimativa de investimento e de prazo")
    r.par("O projeto **não tem investimento financeiro direto** (restrição R07). O recurso principal é o esforço da equipe, de 960 h. Como hipótese de valoração, e não desembolso, o esforço é valorado ao custo de oportunidade de um aluno de ADS: R$ 45,00 por hora de desenvolvedor e R$ 60,00 por hora de gestão do gerente. A revisão e a mentoria docentes são contrapartida institucional e não entram na valoração. O caixa estimado fica entre R$ 0 e cerca de R$ 1.500 no semestre, caso seja necessário domínio, hospedagem, banco gerenciado, armazenamento S3 ou um plano pago do EAS Build em semana de pico." + (
        f" O orçamento detalhado, com estimativa de três pontos, fecha em custo base de {rs(F.CUSTO_BASE)}, linha de base de {rs(F.BAC)} e orçamento total de {rs(F.CUSTO_TOTAL)} (capítulo {n['custos']})." if r.av2 else " O orçamento detalhado é o objeto da Avaliação 2."))
    r.par("O prazo é de 16 semanas efetivas, de 10/08/2026 a 27/11/2026, dentro de um calendário institucional de 20 semanas. Os feriados de 07/09, 12/10, 02/11 e 20/11 (e 15/11, que cai num domingo) entram como risco de calendário e na dimensão das durações, sem alterar as datas dos marcos.")
    r.h2(f"{t}.6 Fatores críticos de sucesso e principais riscos")
    r.par("**Fatores críticos de sucesso.** (1) Equipes integradas nas três frentes, com contrato de dados (identificadores, enums, regras) alinhado desde o início. (2) Toda mudança relevante, depois de aprovado o escopo, passa por avaliação formal. (3) Cumprimento dos marcos M1 a M8, com demonstração incremental. (4) Uso disciplinado de Git, pull request e revisão de código. (5) Priorização do núcleo do MVP: autenticação, planejamento, checklist, foto, operação offline, sincronização e revisão. (6) Adesão à ordem de corte quando houver atraso.")
    r.par("**Ordem de corte (RJ07).** Em caso de atraso, o escopo é reduzido na seguinte ordem: (1) remover o dashboard avançado; (2) limitar os tipos de resposta; (3) aceitar só foto da câmera; (4) construtor de modelos sem arrastar e soltar; (5) conflito de sincronização só detectado e bloqueado; (6) adiar notificações, PDF e assinatura. O núcleo intocável é autenticação, planejamento, checklist, foto, offline, sincronização e revisão.")
    r.par("**Principais riscos do TAP:** atraso no cronograma de 16 semanas; falhas na sincronização offline (perda ou duplicidade); integração deficiente entre mobile, web e API; complexidade dos recursos nativos em aparelhos Android diversos; distribuição desigual do trabalho e dependência de pessoa-chave (o gerente também desenvolve o mobile e o painel web tem um só responsável principal); falhas de segurança; e feriados e eventos que reduzem o tempo útil das sprints. " + (
        f"O capítulo {n['riscos']} os detalha em um registro de 22 riscos e 4 oportunidades; o primeiro deles, o atraso, já se materializou." if r.av2 else "Eles são ampliados no gerenciamento de riscos da Avaliação 2."))
    r.h2(f"{t}.7 Decisões e divergências registradas")
    r.par("As fontes existentes divergem entre si e com o código. O @Q:diverg@ registra as decisões desta versão. As de stack, patrocinador e itens fora do escopo são do gerente e precisam ser **ratificadas pelo orientador e pela coordenação**.")
    dv = [
        ["Stack do painel web", "TAP e Declaração: Angular (R03, RJ04). Notion: Angular ou React", "Next.js 16 (App Router), React 19, TypeScript. A issue #1 do frontend pede Next.js e o plano do frontend registra a divergência e manda criar um ADR", "Mantém Next.js: trocar na semana 15 custaria retrabalho sem ganho, o Notion admite React e o conteúdo de aprendizagem é o mesmo. R03 e RJ04 passam a ler Next.js/React. Nenhum pacote da EAP muda. O ADR (docs #3) continua aberto"],
        ["Gerente do projeto", "PDF antigo: Pedro Dias. TAP de 30/09 e Declaração de 04/10: Felipe Marques", "Felipe Marques", "Vale o documento mais recente. Pedro Dias segue como desenvolvedor backend e da documentação"],
        ["Patrocinador e comitê", "PDF: Prof. Glauco como patrocinador e comitê. TAP de 30/09: coordenação e corpo docente", "Coordenação como patrocinador institucional; Prof. Glauco como orientador e product owner acadêmico", "Une as leituras: a coordenação aprova escopo e marcos; o Prof. Glauco define regras de negócio e critérios"],
        ["Investimento", "PDF: não aplicável. TAP: sem investimento direto", "Sem investimento direto, esforço valorado como hipótese", "Mantém R07 e registra horas e uma estimativa pequena de caixa, ambas hipóteses"],
        ["Itens fora do escopo", "Notion: 14 itens. TAP e Declaração: 8", "8 exclusões formais mais não objetivos do Notion", "A lista formal continua sendo a da Declaração de Escopo"],
        ["Prazo", "Ambos: 16 semanas, 8 sprints, M1 a M8, sem datas", "10/08/2026 a 27/11/2026, com a data de cada marco", "Datas derivadas da criação dos repositórios (10/08) e do calendário de 16 semanas"],
    ]
    r.tabela("Divergências entre as fontes e decisão adotada", ["Tema", "O que dizem as fontes", "Realidade verificada", "Decisão"], dv, [2.4, 4.2, 4.6, 4.8], kind="Quadro", size=8, fonte_txt="tap-fieldops.md, seção Decisões e divergências registradas (versão 2.0, 18/11/2026).", key="diverg")
    r.h2(f"{t}.8 Visão geral do gerenciamento do projeto")
    r.par("O projeto é gerido por sprints de duas semanas, cada uma fechada por um marco aceito em demonstração. A coordenação do curso (PI-01) aprova o termo de abertura e o encerramento; o Prof. Glauco (PI-02) aprova o plano de gerenciamento e decide regras de negócio e mudanças de escopo; os professores das disciplinas (PI-03) validam os marcos. O gerente (FM) aloca issues, muda prioridades dentro da sprint, propõe mudanças e aplica a ordem de corte com ciência do PI-02, mas não altera regra de negócio." + (" O @Q:planos@ mostra como cada área do gerenciamento foi tratada e onde está o artefato." if r.av2 else ""))
    if not r.av2:
        r.par(f"As nove áreas do gerenciamento têm um artefato cada, todos construídos sobre os códigos da EAP: integração (este termo de abertura e o controle de mudanças); escopo (declaração de escopo, EAP e dicionário, capítulo {n['escopo']}); cronograma (63 atividades, 8 marcos e 967 h, capítulo {n['crono']}); recursos humanos (organograma e matriz RACI de 36 pacotes, capítulo {n['crono']}); comunicações (19 comunicações e 10 gatilhos de escalonamento, capítulo {n['partes']}); partes interessadas (13 partes, capítulo {n['partes']}). Custos, qualidade, riscos e aquisições são planejados na Avaliação 2.")
    else:
        pl = [
            ["Integração", "TAP; controle integrado de mudanças", "TAP v2.0; log de mudanças", str(n['tap']) + (", " + str(n['monit']) if r.av2 else "")],
            ["Escopo", "Declaração de escopo, EAP e dicionário", "EAP com 7 entregas e 36 pacotes; 18 requisitos (RP, RJ)", str(n['escopo'])],
            ["Cronograma", "Cronograma com dependências e caminho crítico", "63 atividades e 8 marcos (71 itens); 967 h", str(n['crono'])],
        ]
        if r.av2:
            pl += [
                ["Custos", "Orçamento por três pontos; EVM", f"Custo base {rs(F.CUSTO_BASE)}; BAC {rs(F.BAC)}; total {rs(F.CUSTO_TOTAL)}", str(n['custos'])],
                ["Qualidade", "Plano de qualidade; sete ferramentas básicas", "DoD, critérios de aceitação por marco, metas, 5 ações", str(n['qual'])],
            ]
        pl += [
            ["Recursos humanos", "Organograma, papéis e matriz RACI", "36 pacotes, 1 A por linha; 5 integrantes", str(n['crono'])],
            ["Comunicações", "Plano de comunicação", "19 comunicações (COM-01 a COM-19) e 10 gatilhos de escalonamento", str(n['partes'])],
        ]
        if r.av2:
            pl += [["Riscos", "Plano de riscos e registro", "22 ameaças (R01 a R22) e 4 oportunidades (O01 a O04)", str(n['riscos'])],
                   ["Aquisições", "Tabela de aquisições e make-or-buy", "14 itens (P01 a P14)", str(n['custos'])]]
        pl += [["Partes interessadas", "Registro e matriz poder/interesse", "13 partes (PI-01 a PI-13)", str(n['partes'])]]
        r.tabela("Áreas do gerenciamento, artefatos e linhas de base", ["Área", "Plano ou artefato", "Linha de base ou produto", "Cap."], pl, [2.8, 4.8, 6.9, 1.5], kind="Quadro", size=9, align=["l", "l", "l", "c"], key="planos")
    if r.av2:
        integracao(r, t)
        ajustes(r, t)
    else:
        nota_revisao(r, t)


def nota_revisao(r, t):
    r.h2(f"{t}.9 Nota de revisão")
    r.par("Este documento reorganiza a linha de base de planejamento. Em relação aos documentos iniciais, ele já incorpora três correções que o relatório final também traz: o painel web consta como Next.js/React (e não Angular), com a divergência registrada na seção %d.7; o gerente consta como Felipe Marques; e a EAP tem 36 pacotes de trabalho, número conferido por script. O status real das sprints e os capítulos de custos, qualidade, riscos e monitoramento pertencem à Avaliação 2." % t)


def integracao(r, t):
    n = r.N
    r.h2(f"{t}.9 Integração entre as áreas e rastreabilidade")
    r.par("Integrar, aqui, significa que uma mudança em uma área pode ser seguida até as demais. Quatro mecanismos sustentam isso. Primeiro, a **EAP congelada** (códigos de 1.1 a 7.4) é a chave de tudo: cada atividade do cronograma, cada linha do orçamento, cada linha do RACI, cada risco e cada aquisição aponta para um pacote. Segundo, um **dicionário único de dados** alimenta cronograma, orçamento e aquisições, de modo que as horas por pessoa e os valores em reais são os mesmos nos três (967 h; R$ 47.714,83 de custo base). Terceiro, os **semáforos** têm limiares comuns: SPI de 0,95 e 0,70, 70% de conclusão por sprint, severidade de risco de 0,15 e 0,05. Quarto, a **ordem de corte (RJ07)** é o ponto em que escopo, prazo, custo e risco se encontram: é a reserva de escopo, porque o prazo é fixo e a capacidade, também.")
    r.par("O @Q:rastreab@ liga cada entrega de nível 1 às demais áreas. A leitura por pacote, com as 36 linhas, está no Apêndice H.")
    ac = {"1": "documentos aprovados; 8 relatórios e demos", "2": "DoD geral; RJ01", "3": "AC-AUTH, AC-SYNC, AC-REVIEW, AC-SECURITY", "4": "AC-TEMPLATE, AC-SCHEDULING, AC-REVIEW",
          "5": "AC-CHECKLIST, AC-EVIDENCE, AC-QR, AC-LOCATION, AC-SYNC", "6": "DoD, severidade (sem crítico ou alto aberto)", "7": "AC-RELEASE (19 etapas); DoD do MVP"}
    linhas = []
    for k in "1234567":
        pks = [c for c in F.PACOTES if c.startswith(k + ".")]
        ms = set()
        for c in pks:
            ms.update(F.marcos_pkg(c))
        ats = sum(len(F.ATIV_PKG[c]) for c in pks)
        esf = F.HORAS_ENT[k]
        real = round(sum(a["esf"] * F.REAL[a["id"]] for a in F.ATIV if a["wbs"].startswith(k + ".")) / esf)
        linhas.append([f"{k}. {DD.ENTREGAS[k]}", str(len(pks)), str(ats), str(esf), br(F.CUSTO_ENT[k]), ", ".join(F.RISCOS_ENT[k]), ac[k], faixa_marcos(ms), f"{real}%"])
    tot_at = sum(len(F.ATIV_PKG[c]) for c in F.PACOTES)
    linhas.append(["Total", "36", str(tot_at), "967", br(F.CUSTO_BASE), "22 riscos", "", "M1 a M8", ""])
    r.tabela("Matriz de rastreabilidade por entrega: escopo, cronograma, custo, riscos e qualidade", ["Entrega da EAP", "Pac.", "Ativ.", "Horas", "Custo base (R$)", "Riscos do registro", "Critérios de qualidade", "Marcos", "Real. (est.)"],
             linhas, [3.0, 0.9, 0.9, 1.0, 1.8, 3.0, 3.2, 1.6, 1.1], kind="Tabela", size=7.5, align=["l", "c", "c", "r", "r", "l", "l", "l", "r"], bold_rows=(7,),
             fonte_txt="Elaborado pelos autores (2026): atividades e horas de cronograma-fieldops.md; custo base (valor esperado PERT, sem reservas) de orcamento-fieldops.md; riscos pela coluna EAP de analise-riscos-fieldops.md (um risco pode aparecer em mais de uma entrega); critérios de qualidade-7-ferramentas-fieldops.md e do dicionário da EAP; marcos pela sprint de término das atividades; realizado = percentual estimado, ponderado por horas.",
             key="rastreab")
    # exemplo de leitura integrada: sincronizacao
    pk = ["3.6", "5.6", "5.7"]
    horas = sum(F.HORAS_PKG[c] for c in pk)
    ids = [i for c in pk for i in F.ATIV_PKG[c]]
    nat, lista = len(ids), ", ".join(ids)
    custo = sum(F.CUSTO_PKG[c] for c in pk)
    r.par(f"**Exemplo de leitura integrada: a sincronização offline.** Em escopo, são os pacotes 3.6, 5.6 e 5.7 (RP02 e RP03). No cronograma, são {nat} atividades ({lista}) com {horas} h; A40, A46 e A53 estão no caminho crítico. No custo, são {rs(custo)} de valor esperado, no maior fator de incerteza do orçamento (classe D, cenário pessimista 60% acima das horas). Nos riscos, é o R06, o de maior severidade (0,262), com resposta a cargo de JV e ação contingencial na ordem de corte (item 5). Na qualidade, é o AC-SYNC (envio, reenvio sem duplicidade e falha parcial) e o marco M6, que pesa 20% na avaliação. E, no status de 18/11, é a sprint S6 com 2 de 13 issues concluídas. As cinco áreas contam a mesma história, e é por isso que a decisão de corte e de re-baseline (seção {n['crono']}.7) se concentra aqui.")


def ajustes(r, t):
    n = r.N
    r.h2(f"{t}.10 Ajustes feitos desde a Avaliação 1")
    r.par("A Avaliação 2 pede que os ajustes necessários na Avaliação 1 sejam incorporados. O quadro lista apenas mudanças que existem nos artefatos, entre a visão anterior (TAP de 30/09/2026, Declaração de Escopo de 04/10/2026 e o PDF antigo do repositório docs) e a versão final de 18/11/2026. Nenhuma mudança mexeu na EAP, no escopo do MVP ou nos marcos.")
    aj = [
        ["Stack do painel web", "Angular + TypeScript (R03 e RJ04 do TAP e da Declaração)", "Next.js 16 (App Router), React 19 e TypeScript; R03 e RJ04 reescritos; divergência registrada como mudança retroativa (SM-01), com ADR e ratificação pendentes", f"{n['caract']}.4; {t}.7; {n['monit']}.5"],
        ["Gerente do projeto", "PDF antigo: Pedro Dias", "Felipe Marques, conforme TAP e Declaração mais recentes; Pedro Dias segue como dev backend e da documentação", f"{t}.7"],
        ["Patrocinador e comitê", "PDF: Prof. Glauco como patrocinador e comitê", "coordenação como patrocinador institucional; Prof. Glauco como orientador e product owner acadêmico; comitê com coordenação e professores", f"{t}.7; {n['crono']}.6"],
        ["Investimento", "PDF: não aplicável", "sem investimento direto, com 960 h valoradas como hipótese e orçamento por três pontos (custo base R$ 47.714,83; BAC R$ 52.486,31; total R$ 54.872,05)", f"{t}.5; {n['custos']}"],
        ["Pacotes da EAP", "fontes de partida com contagens divergentes; o RACI registra que são 36 pacotes, e não 31", "36 pacotes de nível 2 em 7 entregas (4+4+7+6+7+4+4), conferidos por script e usados como chave de cronograma, orçamento, RACI, riscos e aquisições", f"{n['escopo']}.3"],
        ["Itens fora do escopo", "Notion: 14 itens", "8 exclusões formais da Declaração; os demais do Notion ficam como não objetivos", f"{n['caract']}.2; {t}.7"],
        ["Datas e calendário", "16 semanas, 8 sprints e marcos sem datas", "10/08 a 27/11/2026; 4 feriados em dia útil (S3, S5, S7 e S8 com 9 dias úteis); marcos nas sextas; Declaração emitida num domingo (04/10), 1 dia útil depois do planejado", f"{n['crono']}.1; {n['crono']}.2"],
        ["Aprovação do TAP e da Declaração", "linha de base: versões iniciais em S1 (A02, 10 a 19/08)", "versões vigentes de 30/09 e 04/10 entram como revisão e aprovação em S4 (A30, concluída); TAP reconciliado na versão 2.0 de 18/11", f"{n['crono']}.1; {t}"],
        ["Responsabilidades", "papéis dos integrantes inferidos dos repositórios (P08)", "R e A por pacote propostos no RACI de 36 pacotes; sobrecarga de FM medida (11 R, 21 A, 36 de 36 pacotes) e cenário B de redistribuição registrado, não adotado", f"{n['crono']}.6"],
        ["Riscos", "7 riscos principais no TAP", "registro de 22 ameaças e 4 oportunidades, com escalas, respostas, EMV e Monte Carlo, atualizado com o GitHub em 18/11 (9 riscos materializados)", f"{t}.6; {n['riscos']}"],
        ["Status e plano de recuperação", "linha de base, sem medição", "situação monitorada em 18/11 (57 de 103 issues; SPI 0,60 por issues), ordem de corte aplicada e re-baseline proposto (cenário C), em decisão do comitê", f"{n['crono']}.7; {n['monit']}"],
    ]
    r.tabela("Ajustes entre a visão da Avaliação 1 e a versão final", ["Tema", "Visão anterior", "Versão final", "Onde"], aj, [2.6, 3.8, 7.4, 2.2], kind="Quadro", size=7.5,
             fonte_txt="Elaborado pelos autores (2026), a partir de tap-fieldops.md (histórico e decisões), organograma-raci-fieldops.md (nota sobre a contagem de pacotes) e cronograma-fieldops.md (observações).", key="ajustes")
