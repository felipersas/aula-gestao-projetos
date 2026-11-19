# -*- coding: utf-8 -*-
"""Capitulos: partes interessadas e comunicacao; escopo e EAP."""
import dados as DD
import fatos as F
from fatos import br, rs, pct


def partes(r):
    n = r.N
    c = n['partes']
    r.h1(f"{c} PARTES INTERESSADAS E COMUNICAÇÃO")
    r.par("O registro tem 13 partes interessadas (PI-01 a PI-13). Elas se dividem entre quem aprova e avalia (PI-01 a PI-04), quem gerencia e executa (PI-05 e PI-06), quem usa ou usará o produto (PI-07 a PI-10), o cliente representado (PI-11) e quem fornece condições externas (PI-12 e PI-13). Os usuários finais são personas da especificação (Carlos, Marina, Ana e Roberto) e **não são pessoas reais**: o Prof. Glauco, como product owner, fala por elas, e o engajamento delas é feito por testes com usuários-proxy.")
    r.h2(f"{c}.1 Registro, interesses e influência")
    linhas = [[p["id"], p["nome"], p["interesses"], str(p["poder"]), str(p["inter"]), p["quad"]] for p in F.PARTES]
    r.tabela("Registro de partes interessadas: interesses, poder, interesse e quadrante", ["ID", "Parte interessada", "Interesses", "Poder", "Interesse", "Quadrante"], linhas, [1.1, 3.3, 6.0, 1.0, 1.2, 2.4], kind="Quadro", size=8,
             align=["c", "l", "l", "c", "c", "l"], fonte_txt="matriz-poder-interesse-fieldops.md (versão 1.0, 18/11/2026). Notas de 1 a 10: avaliação do gerente, não validada com as partes interessadas (premissa).", key="registro")
    r.h2(f"{c}.2 Matriz de poder e interesse")
    r.par("Cada parte recebeu duas notas inteiras de 1 a 10. Poder é a capacidade de aprovar, bloquear, avaliar ou mudar escopo, prazo, nota ou condições de execução; interesse é o quanto o projeto afeta a parte e o quanto ela o acompanha. O corte entre alto e baixo é 5,5 nos dois eixos, e como as notas são inteiras nenhuma parte cai sobre a linha. Resultaram 5 partes em gerenciar com atenção (PI-02, PI-03, PI-04, PI-05 e PI-06), 2 em manter satisfeito (PI-01 e PI-13), 4 em manter informado (PI-07, PI-08, PI-09 e PI-11) e 2 em monitorar (PI-10 e PI-12). A @F:pi@ mostra a distribuição.")
    r.figura("poder_interesse_ret.png", "Matriz de poder e interesse das 13 partes interessadas do FieldOps", 14.0, altura_max_cm=11.5,
             fonte_txt="Elaborado pelos autores (2026), a partir das notas do @Q:registro@ (versão original: matriz-poder-interesse-fieldops.png).", key="pi")
    r.par("Duas notas merecem atenção, porque uma unidade a mais ou a menos muda o quadrante: o interesse da coordenação (PI-01, nota 5) e o do Prof. Deivison (PI-04, nota 6). Se a coordenação acompanhar o projeto mais de perto do que o gerente supõe, ela passa a gerenciar com atenção.")
    r.h2(f"{c}.3 Estratégias de engajamento")
    r.par("O nível de engajamento atual e o desejado seguem as cinco categorias da disciplina: desinformado, resistente, neutro, apoia e lidera. A lacuna é a distância entre os dois níveis. Os níveis atuais são avaliação do gerente em 18/11/2026 (premissa). Nenhuma parte foi classificada como resistente: não há registro de oposição ao projeto. As maiores lacunas são as dos usuários finais (PI-07 e PI-08, com três níveis), que são personas e hoje não veem o produto funcionando; a forma realista de fechá-las são os testes com usuário-proxy nos marcos M3, M5 e M7 (COM-15), e não uma comunicação formal.")
    ac = DD.engaj_acoes()
    estr = {"Gerenciar com atenção": "engajar de perto: comunicar com frequência, envolver nas decisões, tratar problemas no ato", "Manter satisfeito": "informar nos marcos e nunca surpreender; sem sobrecarregar com detalhe técnico",
            "Manter informado": "comunicar com regularidade e coletar feedback de uso (teste com usuário-proxy)", "Monitorar": "esforço mínimo; acompanhar mudanças e reavaliar a cada sprint"}
    linhas = []
    for p in F.PARTES:
        a = ac[p["id"]]
        if r.av2:
            linhas.append([f"{p['id']} {p['nome']}", f"{p['atual']} → {p['desej']} ({p['lacuna']})", a["acoes"], a["resp"]])
        else:
            linhas.append([f"{p['id']} {p['nome']}", f"{p['atual']} → {p['desej']} ({p['lacuna']})", estr[p["quad"]], a["resp"]])
    r.tabela("Engajamento: nível atual e desejado (lacuna), " + ("ações do plano de comunicação, " if r.av2 else "estratégia por quadrante, ") + "responsável e frequência", ["Parte interessada", "Atual → desejado (lacuna)", "Ações de engajamento (comunicações do plano)" if r.av2 else "Estratégia de engajamento", "Responsável e frequência"], linhas, [3.1, 2.4, 7.6, 2.9], kind="Quadro", size=7.5,
             fonte_txt="matriz-poder-interesse-fieldops.md, seções 4.1 e 4.3. Códigos COM-xx do plano de comunicação.", key="engaj")
    if r.av2:
        r.par("Pela heurística lacuna × poder, a ordem de prioridade é PI-08 (12), PI-01 (9), PI-07 (9), PI-03 (8), PI-06 (7) e PI-09 (6). A coordenação aparece por ter o maior poder entre os que precisam subir um nível, e o desvio de prazo atual é o assunto sobre o qual ela deve ser informada antes de saber por outro caminho. A equipe tem lacuna de um nível, mas é a mais crítica para a recuperação do prazo, por isso as ações com ela são diárias. O engajamento é reavaliado a cada sprint, na retrospectiva, junto com os indicadores de comunicação.")
    r.h2(f"{c}.4 Plano de comunicação")
    r.par("O plano tem 19 comunicações (COM-01 a COM-19). O que está documentado no projeto é o fluxo de GitHub (branches, Conventional Commits, pull request com revisão, CI), a rotina semanal de aulas (duas de conteúdo e três de projeto, com a última aula da semana reservada a integração, testes, revisão e demonstração parcial) e os marcos. Os demais canais, como WhatsApp para dailies, e-mail institucional e videochamada, são **premissa** do gerente e precisam de confirmação do grupo. Os idiomas são o português nas comunicações e atas e o inglês nos commits.")
    linhas = [[x["id"], x["desc"], x["freq"], x["canal"], x["publico"], x["dono"]] for x in F.COM]
    r.tabela("Plano de comunicação: descrição, frequência, canal, público e proprietário", ["ID", "Comunicação", "Frequência", "Canal", "Público", "Proprietário"], linhas, [1.6, 3.8, 2.3, 3.5, 2.6, 2.2], kind="Quadro", size=7.5, align=["c", "l", "l", "l", "l", "l"],
             fonte_txt="plano-comunicacao-fieldops.md, seção 2." + (" Momento de realização e formato de cada comunicação: Apêndice G." if r.av2 else " Momento e formato de cada comunicação constam do arquivo de origem (seção 3)."), key="com")
    r.par("O gerente (FM) é proprietário de 13 das 19 comunicações, o que é natural para o canal formal com professores e coordenação, mas pesa sobre um gerente que também desenvolve o app. Por isso a compilação do relatório de status (COM-06), as lições aprendidas (COM-19) e o monitoramento de provedores (COM-17) ficam com PD, o contrato OpenAPI (COM-09) com JV e os testes com usuário-proxy (COM-15) com GR; a relatoria das atas gira entre os cinco integrantes.")
    r.par("O plano fixa tempos de resposta (premissa de equipe): bloqueio urgente em 4 h corridas, primeira revisão de pull request em 24 h úteis, pergunta técnica em 1 dia útil, consulta (o C do RACI) em 2 dias úteis, e pedido ao orientador ou à coordenação em até 5 dias úteis. Decisão sobre escopo, contrato de API ou papel só vale se estiver registrada em issue, pull request ou ata: combinado apenas por WhatsApp não conta. " + (
        f"Dez gatilhos de escalonamento (G1 a G10, Apêndice G) acionam a comunicação COM-11; eles são usados no capítulo {n['monit']} como limites de monitoramento." if r.av2 else "Dez gatilhos de escalonamento (G1 a G10) acionam a comunicação COM-11 quando um limite é ultrapassado."))


def escopo(r):
    n = r.N
    c = n['escopo']
    r.h1(f"{c} GERENCIAMENTO DO ESCOPO E EAP")
    r.h2(f"{c}.1 Declaração de escopo")
    r.par("O escopo do projeto é o MVP do FieldOps, entregue até 27/11/2026: o aplicativo mobile Android com operação offline e sincronização idempotente, a interface administrativa web, a API REST central com contrato OpenAPI, a infraestrutura de dados, os testes e a documentação necessários para demonstrar de ponta a ponta o fluxo do AC-RELEASE (19 etapas, sem edição manual do banco). O escopo do produto está descrito nos requisitos RP01 a RP10 e o do projeto em RJ01 a RJ08 (@Q:req@).")
    r.par("Os limites são dois. De um lado, o **backlog**: 72 itens P0 (PBI-001 a PBI-072), em 10 épicos, formam a linha de base; 10 itens P1 (PBI-073 a PBI-082, como dashboard, notificações, assinatura e PDF) ficam fora da linha de base e só entram por controle de mudanças. De outro, as **exclusões** formais: portal do cliente, multiempresa, pagamento, inteligência artificial, integração com IoT, assinatura com validade jurídica, mais de um técnico por inspeção e validação obrigatória fora do Android.")
    r.h2(f"{c}.2 Entregas, requisitos e critérios de aceitação")
    ent = DD.eap_entregas()
    linhas = []
    for k in "1234567":
        e = ent[k]
        linhas.append([f"{k}. {e['nome']}", e["desc"], e["req"], e["criterio"]])
    r.tabela("Entregas principais (nível 1 da EAP): descrição, requisitos atendidos e critério de aceitação", ["Entrega", "Descrição", "Requisitos", "Critério de aceitação"], linhas, [2.6, 5.6, 2.2, 5.6], kind="Quadro", size=7.5,
             fonte_txt="eap-fieldops.md, dicionário da EAP (entregas de nível 1). Critérios por pacote: " + r.dic + ".", key="entregas")
    r.par("Os critérios de aceitação de cada um dos 36 pacotes estão no dicionário da EAP (" + r.dic + ") e se apoiam nos documentos 17 (critérios de aceitação por funcionalidade, AC-AUTH, AC-SYNC, AC-REVIEW, AC-RELEASE e outros) e 18 (Definição de Pronto) da especificação. Eles seguem a forma dado/quando/então e valem para o conjunto de requisitos RP e RJ " + (f"(capítulo {n['qual']} e seção {n['monit']}.6, onde são ligados aos marcos)." if r.av2 else "(a ligação com os marcos está no cronograma)."))
    # EAP em pagina paisagem
    r.secao_paisagem()
    r.h2(f"{c}.3 Estrutura analítica do projeto (EAP)", quebra=False)
    r.par("A EAP é orientada a entregas, com substantivos e particípios, e nunca a verbos de atividade. O agrupamento usa três critérios: gestão (ramo 1), componentes do produto (ramos 2 a 5: fundação, API, web e mobile) e verificação e entrega (ramos 6 e 7). Ela foi construída com a regra dos 100%: os 72 itens P0 do backlog aparecem em algum pacote, e nada fora do escopo tem pacote.", line=1.15, after=4)
    r.figura("eap_resumo.png", "EAP do FieldOps: 7 entregas e 36 pacotes de trabalho", 24.0, altura_max_cm=10.6,
             fonte_txt="eap-fieldops.md (versão 1.0, 18/11/2026). Nomes completos, requisitos e PBIs de cada pacote: " + r.dic + ".", key="eap")
    r.secao_retrato()
    r.par("O pacote de trabalho é o menor nível usado para planejar e controlar: é nele que se penduram as atividades do cronograma, as linhas do orçamento, o RACI, as aquisições e os riscos, sempre com o mesmo código. Por isso a EAP é a referência única dos demais artefatos.")
    r.h2(f"{c}.4 Rastreabilidade de requisitos")
    r.par("Todo requisito tem pelo menos um pacote que o implementa ou define (ramos 1 a 5) e, quando cabe, pacotes que o verificam ou entregam (ramos 6 e 7). A matriz é gerada do mesmo dado do dicionário e conferida por script: nenhum dos dez requisitos de produto nem dos oito de projeto ficou sem pacote.")
    linhas = [[x[0], x[1], x[3], x[4]] for x in DD.eap_req_matriz()]
    r.tabela("Requisitos e pacotes da EAP que os implementam e que os verificam", ["Req.", "Descrição", "Implementam ou definem (ramos 1 a 5)", "Verificam ou entregam (ramos 6 e 7)"], linhas, [1.2, 5.6, 4.9, 4.3], kind="Quadro", size=8.5, align=["c", "l", "l", "l"],
             fonte_txt="eap-fieldops.md, matriz de rastreabilidade requisito para pacote.", key="reqmat")
    if r.av2:
        r.par("A especificação classifica os requisitos em seis categorias, e o planejamento as cobre: necessidades de negócio (NN-01 a NN-07, como substituir o papel e permitir inspeção sem conectividade), requisitos das partes interessadas (RPI-01 a RPI-06, por persona), de solução (RP01 a RP10), de transição (RT-01 a RT-05: dados de demonstração, build instalável, instruções de execução), de projeto (RJ01 a RJ08) e de qualidade (RQ-01 a RQ-07). O portal do cliente (persona Roberto) é registrado como necessidade e fica fora do MVP. Os requisitos foram levantados por análise de documentos, personas e cenários, benchmarking informal (planilha e formulário genérico) e refinamento do backlog com critérios de aceitação. As reuniões com o orientador e o brainstorming do grupo são premissa plausível, sem ata nos repositórios; entrevistas e observação in loco não foram usadas, pois o MVP acadêmico não tem usuários reais.")
    r.h2(f"{c}.5 Exclusões e como mudanças de escopo são avaliadas")
    r.par("O que está fora do escopo não tem pacote e não pode entrar por omissão: a lista formal é a da Declaração de Escopo, e os itens do Notion mantidos como não objetivos funcionam como limite adicional. Uma mudança de escopo é qualquer pedido para incluir, remover ou alterar uma entrega, um requisito, um critério de aceitação ou um item P1. Ela é avaliada por quatro perguntas feitas ao pacote afetado: (1) altera o núcleo (autenticação, planejamento, checklist, foto, offline, sincronização, revisão)? (2) quantas horas custa e a que pacotes e marcos se refere? (3) cabe nas 12 horas semanais por pessoa, ou desloca outra entrega? (4) cria risco de qualidade ou de segurança? O pedido é feito por escrito, em uma issue, e a decisão cabe ao orientador (PI-02), com a coordenação e o comitê quando o prazo final ou o núcleo forem afetados. Quando o prazo aperta, o escopo é reduzido pela ordem de corte do RJ07, e não por omissão." + (f" O fluxo completo, o formulário e as alçadas estão na seção {n['monit']}.5." if r.av2 else ""))
    if r.av2:
        r.par("O escopo da linha de base não mudou desde a Declaração de 04/10, e a EAP continua com 36 pacotes. O que mudou foi a pressão sobre ele: com as sprints S6 e S7 atrasadas, a ordem de corte deixa de ser uma regra de contingência e passa a ser aplicada. O dashboard avançado (PBI-073) já está fora da linha de base; mesmo assim foi entregue no frontend em 09/11, antes da sincronização, o que o registro de riscos trata como ampliação indevida de escopo (R10, materializado).")
