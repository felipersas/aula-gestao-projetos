# -*- coding: utf-8 -*-
"""Capitulos: identificacao, introducao, caracterizacao do projeto (compartilhados pelos dois documentos)."""
import dados as DD
import fatos as F
from fatos import br, rs, pct

FONTE_ART = "Elaborado pelos autores (2026), a partir dos artefatos do repositório da disciplina."


def tabela_ident(r):
    n = r.N
    linhas = [
        ["Projeto", "FieldOps: Plataforma de Inspeção em Campo (MVP)"],
        ["Instituição", "Centro Universitário SENAI São Paulo (UniSENAI-SP), Campus Sorocaba (Santa Rosália)"],
        ["Curso e disciplina", "Análise e Desenvolvimento de Sistemas; Gestão de Projetos"],
        ["Orientador da disciplina", "Prof. Me. Deivison S. Takatu"],
        ["Gerente do projeto", "Felipe Marques (FM), também desenvolvedor mobile"],
        ["Equipe (papéis propostos a confirmar)", "João Victor Souza (JV), backend e líder técnico da API; Gabriel Ribeiro (GR), backend, cadastros e testes; Pedro Dias (PD), backend, offline no app e documentação; André Fernandes (AF), web (Next.js)"],
        ["Patrocinador e product owner acadêmico", "Coordenação do curso (patrocinador institucional); Prof. Glauco Todesco (autor da especificação, orientador e product owner acadêmico)"],
        ["Período do projeto", "10/08/2026 a 27/11/2026: 16 semanas efetivas, 8 sprints de duas semanas, marcos M1 a M8"],
        ["Data-base e versão", ("18/11/2026 (semana 15, sprint S8). Versão 1.0 do relatório final" if r.av2 else "Linha de base de planejamento, revisada em 18/11/2026. Versão 1.0 do documento parcial")],
        ["Repositórios do projeto", "Organização FieldOps-Project no GitHub: docs, backend, frontend e app (consulta em 18/11/2026)"],
        ["Artefatos de gerenciamento", "Pasta entrega/ do repositório da disciplina, por aula (aula-02 a aula-08); nomes de arquivo no " + ("Apêndice K" if r.av2 else f"capítulo {n['entregaveis']}")],
    ]
    r.tabela("Identificação do trabalho e do projeto", ["Campo", "Informação"], linhas, [4, 12], kind="Quadro", size=9.5, first_col_bold=True, key="ident")


def identificacao(r):
    n = r.N
    r.h1(f"{n['ident']} CAPA E IDENTIFICAÇÃO", quebra=False)
    r.par("A capa e a folha de rosto abrem este documento. O quadro a seguir completa a identificação do trabalho e do projeto.", first=1.27)
    tabela_ident(r)
    r.h2(f"{n['ident']}.1 Como ler este documento")
    r.par("Três convenções valem para todo o texto, porque o projeto mistura dados medidos e dados assumidos.")
    r.alineas([
        "**Dado real** é o que vem de documento do projeto (TAP, Declaração de Escopo, especificação no Notion do Prof. Glauco) ou do GitHub em 18/11/2026: issues por sprint, pull requests, commits e execuções de CI",
        "**Estimativa** é valor calculado ou julgado pelo gerente, como durações, horas, custos em reais, probabilidades e impactos de risco; está rotulada como estimativa ou premissa onde aparece",
        "**Proposta a confirmar** é o que depende de aceite do grupo ou dos professores: papéis dos integrantes (inferidos dos repositórios), responsável (R) e aprovador (A) por pacote, metas de qualidade e alçadas de decisão",
    ])
    if r.av2:
        r.par("O status do projeto é o do levantamento de 18/11/2026: 57 de 103 issues concluídas nos milestones por sprint (55%). Uma coleta automática posterior, feita pela análise de qualidade, encontrou 59 de 103, porque duas issues do frontend foram fechadas às 14h30 UTC desse mesmo dia, depois do primeiro levantamento. Os documentos de gestão usam 57 e a análise de qualidade usa 59; a diferença é só essa, e este relatório indica qual número vale em cada ponto.")
    else:
        r.par("Este documento é a linha de base de planejamento da Avaliação 1: não traz o capítulo de status real, que está no relatório final da Avaliação 2. As diferenças entre esta versão e os documentos iniciais (TAP de 30/09 e Declaração de Escopo de 04/10) estão na nota de revisão do capítulo %d." % n['tap'])


def introducao(r):
    n = r.N
    r.h1(f"{n['intro']} INTRODUÇÃO")
    r.h2(f"{n['intro']}.1 Contexto e problema")
    r.par("Inspeções técnicas de equipamentos e instalações acontecem fora do escritório, muitas vezes em locais com conexão irregular. Em muitas operações, o processo ainda depende de formulários impressos, planilhas, fotos sem identificação e mensagens em canais diferentes. A cadeia entre planejar, executar e analisar fica fragmentada, o que gera retrabalho, campos em branco, pouca rastreabilidade e dificuldade de auditoria (especificação do FieldOps, documentos 01 e 03).")
    r.par("O FieldOps é a resposta proposta na especificação do Prof. Glauco Todesco: uma plataforma com aplicativo mobile Android com operação offline, interface administrativa web e API REST central, para planejar, executar, sincronizar, revisar e auditar inspeções. O produto serve também como projeto integrador de três disciplinas (Expo/React Native, Java/Spring Boot e desenvolvimento web) e é o objeto de planejamento da disciplina de Gestão de Projetos.")
    r.h2(f"{n['intro']}.2 Objetivos deste trabalho")
    if r.av2:
        r.par("O objetivo geral é consolidar o planejamento integrado do FieldOps em um relatório técnico-acadêmico, mostrando como escopo, cronograma, recursos, custos, qualidade, riscos, comunicação e partes interessadas se relacionam e como o projeto será monitorado, controlado e encerrado. Os objetivos específicos são:")
        r.alineas([
            "revisar e consolidar a base de planejamento da Avaliação 1 (termo de abertura, partes interessadas, escopo e EAP, cronograma e responsabilidades), registrando os ajustes feitos desde então",
            "complementar o planejamento com custos e orçamento, qualidade e critérios de aceitação, e gerenciamento dos riscos",
            "definir indicadores, frequência de monitoramento, tratamento de desvios, processo de mudanças, aceite das entregas e encerramento",
            "demonstrar a consistência entre as áreas por uma matriz de rastreabilidade e por números conferidos por script",
            "apresentar a situação real do projeto em 18/11/2026, com o atraso das sprints S6 e S7 tratado como desvio monitorado e com ação corretiva",
        ])
    else:
        r.par("O objetivo deste documento é registrar a linha de base de planejamento do FieldOps exigida na Avaliação 1: caracterização do projeto, termo de abertura e integração, partes interessadas e comunicação, escopo e EAP, e cronograma, recursos e responsabilidades. O documento mostra as decisões e as premissas por trás de cada artefato, para que os artefatos possam ser lidos juntos.")
    r.h2(f"{n['intro']}.3 Metodologia")
    r.par("O planejamento seguiu as áreas de conhecimento do Guia PMBOK (PMI, 2013) e o conteúdo da disciplina (CARVALHO, 2018; SOUZA, 2020), combinados com o ciclo de sprints e marcos que a própria especificação impõe ao projeto (SCHWABER; SUTHERLAND, 2020). Cada artefato foi feito em um arquivo do repositório da disciplina, a partir de uma base única de fatos (códigos da EAP, identificadores, datas, equipe e status), para que os números batam entre as áreas.")
    r.par("Os dados reais vieram do GitHub (issues, pull requests, commits e execuções de CI dos quatro repositórios, em 18/11/2026) e da documentação do produto. Onde não havia dado, o trabalho usou premissa declarada, como as taxas horárias, as durações e os percentuais por atividade. As contas dos artefatos (cronograma, orçamento, riscos, carga da equipe, análise da qualidade) foram feitas e conferidas por script; as tabelas e os valores deste " + ("relatório" if r.av2 else "documento") + " são lidos desses artefatos e comparados com os totais-chave antes da geração do arquivo.")
    r.h2(f"{n['intro']}.4 Organização " + ("do relatório" if r.av2 else "do documento"))
    if r.av2:
        r.par("O relatório segue a estrutura recomendada no enunciado do projeto. O @Q:mapa@ relaciona cada capítulo ao requisito que ele atende e ao artefato de origem.")
        linhas = [
            [str(n['ident']), "Capa e identificação", "Identificação", "capa e folha de rosto"],
            [str(n['intro']), "Introdução", "Contexto, objetivos, metodologia", "—"],
            [str(n['caract']), "Caracterização do projeto", "Contexto e justificativa", "documentos 01 a 20 do Notion; TAP"],
            [str(n['tap']), "Termo de abertura e integração", "Av.1, requisito 1", "tap-fieldops.md"],
            [str(n['partes']), "Partes interessadas e comunicação", "Av.1, requisito 2", "matriz-poder-interesse-fieldops.md; plano-comunicacao-fieldops.md"],
            [str(n['escopo']), "Gerenciamento do escopo e EAP", "Av.1, requisito 3", "eap-fieldops.md"],
            [str(n['crono']), "Cronograma, recursos e responsabilidades", "Av.1, requisito 4", "cronograma-fieldops.md; organograma-raci-fieldops.md"],
            [str(n['custos']), "Custos e orçamento", "Av.2, requisito 1", "orcamento-fieldops.md; aquisicoes-fieldops.md"],
            [str(n['qual']), "Qualidade e critérios de aceitação", "Av.2, requisito 2", "qualidade-7-ferramentas-fieldops.md"],
            [str(n['riscos']), "Gerenciamento dos riscos", "Av.2, requisito 3", "analise-riscos-fieldops.md"],
            [str(n['monit']), "Monitoramento, controle e encerramento", "Av.2, requisito 4", "conteúdo novo, escrito para este relatório"],
            [str(n['final']), "Considerações finais", "Av.2, requisito 5", "—"],
            [str(n['refs']), "Referências", "—", "—"],
            [str(n['apend']), "Apêndices e anexos", "Artefatos completos", "todos os artefatos"],
        ]
        r.tabela("Capítulos do relatório, requisitos atendidos e artefatos de origem", ["Cap.", "Capítulo", "Requisito do enunciado", "Artefato de origem"], linhas, [1, 5, 4, 6], kind="Quadro", size=9, align=["c", "l", "l", "l"], key="mapa")
        r.par("Os artefatos completos, de tabelas longas, estão nos apêndices ou são citados pelo nome do arquivo no repositório; o corpo do relatório traz as tabelas essenciais, as figuras e a argumentação. O capítulo %d é conteúdo novo e não existe em nenhum artefato anterior." % n['monit'])
    else:
        pass


def mapa_av1(r):
    n = r.N
    linhas = [
        [str(n['caract']), "Introdução e caracterização do projeto", "contexto, justificativa", "documentos do Notion; TAP"],
        [str(n['tap']), "Termo de abertura e integração", "requisito 1", "tap-fieldops.md"],
        [str(n['partes']), "Partes interessadas e comunicação", "requisito 2", "matriz-poder-interesse-fieldops.md; plano-comunicacao-fieldops.md"],
        [str(n['escopo']), "Gerenciamento do escopo", "requisito 3", "eap-fieldops.md"],
        [str(n['crono']), "Cronograma, recursos e responsabilidades", "requisito 4", "cronograma-fieldops.md; organograma-raci-fieldops.md"],
        [str(n['entregaveis']), "Entregáveis da Avaliação 1 e artefatos no repositório", "lista de entregáveis", "—"],
    ]
    r.tabela("Capítulos do documento parcial, requisitos atendidos e artefatos de origem", ["Cap.", "Capítulo", "Requisito do enunciado", "Artefato de origem"], linhas, [1, 5.5, 3.5, 6], kind="Quadro", size=9, align=["c", "l", "l", "l"], key="mapa")


def caracterizacao(r):
    n = r.N
    c = n['caract']
    r.h1(f"{c} CARACTERIZAÇÃO DO PROJETO" if r.av2 else f"{c} INTRODUÇÃO E CARACTERIZAÇÃO DO PROJETO", quebra=r.av2)
    if not r.av2:
        r.par("O objetivo deste documento é registrar a linha de base de planejamento do FieldOps exigida na Avaliação 1: caracterização do projeto, termo de abertura e integração, partes interessadas e comunicação, escopo e EAP, e cronograma, recursos e responsabilidades. O documento mostra as decisões e as premissas por trás de cada artefato, para que eles possam ser lidos juntos.")
        r.par("A equipe é formada por Felipe Marques (gerente do projeto), João Victor Souza, Gabriel Ribeiro, Pedro Dias e André Fernandes, e o orientador da disciplina é o Prof. Me. Deivison S. Takatu. A data-base da linha de base é 18/11/2026, e o período do projeto vai de 10/08/2026 a 27/11/2026.")
        r.par("Três convenções valem para todo o texto. **Dado real** é o que vem de documento do projeto (TAP, Declaração de Escopo, especificação no Notion do Prof. Glauco). **Estimativa** é valor calculado ou julgado pelo gerente, como durações, horas e percentuais, e está rotulada onde aparece. **Proposta a confirmar** é o que depende de aceite do grupo ou dos professores, como os papéis dos integrantes (inferidos dos repositórios) e o responsável (R) e o aprovador (A) por pacote. Este documento não traz o capítulo de status real, que está no relatório final da Avaliação 2; as diferenças em relação aos documentos iniciais (TAP de 30/09 e Declaração de 04/10) estão na nota de revisão do capítulo %d." % n['tap'])
        r.par("Inspeções técnicas de equipamentos e instalações acontecem fora do escritório, muitas vezes sem conexão estável, e ainda dependem de formulários impressos, planilhas, fotos sem identificação e mensagens em vários canais. A cadeia entre planejar, executar e analisar fica fragmentada, com retrabalho, campos em branco, pouca rastreabilidade e dificuldade de auditoria (especificação do FieldOps, documentos 01 e 03). O FieldOps, definido pelo Prof. Glauco Todesco, é a plataforma proposta para esse problema e é o objeto de planejamento da disciplina de Gestão de Projetos.")
    r.h2(f"{c}.1 O produto")
    r.par("O FieldOps tem quatro componentes que compartilham um contrato de API. O aplicativo mobile Android é usado pelo técnico para consultar as inspeções atribuídas, ler o QR Code do equipamento, responder checklists dinâmicos, registrar fotos, observações, localização e não conformidades, inclusive sem internet. A interface administrativa web é usada por administradores e supervisores para cadastrar, criar modelos de inspeção versionados, agendar, atribuir, acompanhar, revisar, aprovar ou reprovar. A API REST central concentra autenticação, autorização, regras de negócio, sincronização, upload de evidências e auditoria. A infraestrutura de dados reúne PostgreSQL, armazenamento compatível com S3 e SQLite local no aparelho. A @F:arq@ mostra a arquitetura.")
    r.figura("arquitetura.png", "Arquitetura do FieldOps: componentes e contrato compartilhado", 15.0, altura_max_cm=9.0, fonte_txt="Elaborado pelos autores (2026), com base na especificação do produto (documento 11, Arquitetura) e na stack real dos repositórios.", key="arq")
    r.par("A decisão de produto que mais pesa no planejamento é a de que o SQLite é persistência operacional, e não cache descartável (Anexo B da especificação). Isso torna a sincronização idempotente com fila de saída (outbox) a parte de maior incerteza técnica, e é por isso que o planejamento a trata como classe de risco própria nos custos (classe D) e nos riscos (R06).")
    r.h2(f"{c}.2 Escopo do MVP e exclusões")
    r.par("O MVP deve demonstrar o fluxo completo: o administrador cadastra os dados básicos, o supervisor cria um modelo de inspeção, agenda e atribui a inspeção a um técnico, o técnico executa o checklist com fotos, QR Code e localização, trabalha temporariamente sem internet, sincroniza os dados, e o supervisor revisa e aprova ou reprova. Esse fluxo é o critério de aceitação final (AC-RELEASE, 19 etapas, sem edição manual do banco).")
    r.par("Ficam fora do MVP: portal do cliente, multiempresa com isolamento completo, pagamento, inteligência artificial, integração com IoT, assinatura com validade jurídica, mais de um técnico por inspeção e validação obrigatória fora do Android. A especificação lista outros itens como não objetivos (roteirização, localização contínua, vídeo, relatórios regulatórios, integração com ERP), mantidos como limites do escopo.")
    r.h2(f"{c}.3 Requisitos de produto e de projeto")
    r.par("A Declaração de Escopo de 04/10/2026 define dez requisitos de produto (RP01 a RP10) e oito de projeto (RJ01 a RJ08). Eles são a referência de rastreabilidade de todo o planejamento: cada requisito tem pacotes da EAP que o implementam e pacotes que o verificam (seção %s)." % (f"{n['escopo']}.4"))
    rp = [
        ["RP01", "Aplicativo mobile de execução"], ["RP02", "Operação offline (SQLite)"], ["RP03", "Sincronização idempotente (outbox)"],
        ["RP04", "Interface administrativa web, não substituível por Swagger ou banco"], ["RP05", "Modelos de inspeção versionados"],
        ["RP06", "API REST central com OpenAPI"], ["RP07", "Autenticação e autorização por perfil, validadas na API"],
        ["RP08", "Evidências rastreáveis (armazenamento S3)"], ["RP09", "Fluxo de revisão: aprova, reprova, corrige; aprovada fica protegida"], ["RP10", "Auditoria"],
        ["RJ01", "Contrato OpenAPI desde M1"], ["RJ02", "8 sprints e marcos M1 a M8"], ["RJ03", "Git, pull request e revisão de código"], ["RJ04", "Stack definida"],
        ["RJ05", "Validação em Android"], ["RJ06", "Segurança: sem segredos no repositório, autorização no backend"], ["RJ07", "Controle de escopo e ordem de corte"], ["RJ08", "Avaliação por marcos"],
    ]
    meio = 9
    linhas = [[rp[i][0], rp[i][1], rp[i + meio][0], rp[i + meio][1]] for i in range(meio)]
    r.tabela("Requisitos de produto (RP) e de projeto (RJ) da Declaração de Escopo", ["ID", "Requisito de produto e de projeto", "ID", "Requisito de projeto"], linhas, [1.2, 6.8, 1.2, 6.8], kind="Quadro", size=9, align=["c", "l", "c", "l"],
             fonte_txt="Declaração de Escopo do FieldOps (04/10/2026), reproduzida na base de fatos do projeto.", key="req")
    r.h2(f"{c}.4 Stack e decisão sobre o painel web")
    r.par("O mobile usa Expo / React Native com TypeScript, Expo Router, SQLite local e build por EAS. A API usa Java e Spring Boot, PostgreSQL, Flyway, JWT e OpenAPI, com Docker Compose. A colaboração usa GitHub com Conventional Commits, pull request com revisão e CI por repositório. O painel web foi implementado em **Next.js 16 (App Router) com React 19 e TypeScript**, embora o TAP de 30/09/2026 e a Declaração de Escopo de 04/10/2026 citem Angular. A especificação (documentos 02 e 11) aceita Angular ou React. Essa divergência foi tratada como mudança retroativa e está registrada na seção %s." % f"{n['tap']}.7")
    r.h2(f"{c}.5 Equipe, capacidade e calendário")
    r.par("A equipe tem cinco integrantes. Os papéis do quadro abaixo foram **inferidos dos repositórios** (commits, issues e documentos) e são **proposta a confirmar com o grupo** (premissa P08 do TAP). A capacidade de referência é de 12 horas por semana por pessoa durante 16 semanas, ou 960 horas (premissa P09).")
    eq = [
        ["Felipe Marques (FM)", "Gerente do projeto e desenvolvedor mobile (Expo)", "TAP e Declaração de Escopo; issues do app; commits em docs"],
        ["João Victor Souza (JV)", "Desenvolvedor backend; líder técnico da API; convenções e contrato", "25 commits no backend; issues #1 e #2 do backend e docs"],
        ["Gabriel Ribeiro (GR)", "Desenvolvedor backend: cadastros, modelos e qualidade da API", "issues do backend"],
        ["Pedro Dias (PD)", "Desenvolvedor backend e documentação; offline e sincronização no app", "issues do backend; commits de TAP em docs"],
        ["André Fernandes (AF)", "Desenvolvedor web (Next.js)", "26 issues do frontend"],
    ]
    if r.av2:
        r.tabela("Equipe, papéis propostos e evidências nos repositórios", ["Integrante", "Papel proposto", "Evidência"], eq, [3.6, 7, 5.4], kind="Quadro", size=9, key="equipe")
    else:
        r.par("Os papéis propostos são: Felipe Marques (FM), gerente do projeto e desenvolvedor mobile; João Victor Souza (JV), backend e líder técnico da API; Gabriel Ribeiro (GR), backend, cadastros, modelos e testes; Pedro Dias (PD), backend, documentação e offline no app; e André Fernandes (AF), painel web em Next.js. As evidências são os commits e as issues dos repositórios, e a tabela de horas por pessoa está na seção %d.4." % r.N["crono"])
    r.par("O calendário vai de 10/08/2026, data de criação dos repositórios, a 27/11/2026, em oito sprints de duas semanas, cada uma terminando em um marco numa sexta-feira (@Q:marcos@). Quatro feriados em dia útil (07/09, 12/10, 02/11 e 20/11) reduzem as sprints S3, S5, S7 e S8 a nove dias úteis. As quatro semanas que restam no calendário institucional não são reserva de desenvolvimento (premissa P06).")
    cal = []
    pesos = {"M1": "5%", "M2": "10%", "M3": "10%", "M4": "15%", "M5": "15%", "M6": "20%", "M7": "10%", "M8": "15%"}
    for rw in DD.marcos_md():
        mid = rw[0].split("—")[0].strip().replace("Marco ", "")
        mid = mid[:2]
        cal.append([rw[0].replace("Marco ", ""), rw[1], rw[3], pesos[mid]])
    r.tabela("Marcos do projeto, data, incremento demonstrável e peso na avaliação", ["Marco", "Data", "Critério de aceitação (incremento demonstrável)", "Peso (doc. 19.6)"], cal, [3.6, 2.2, 8.2, 2], kind="Quadro", size=9, align=["l", "c", "l", "c"],
             fonte_txt="cronograma-fieldops.md (seção Marcos) e documento 19.6 da especificação (peso sugerido de cada marco na avaliação do projeto).", key="marcos")
    if r.av2:
        r.h2(f"{c}.6 Situação em 18/11/2026")
        r.par("Em 18/11/2026, o projeto está na semana 15 de 16, em S8. Dos 103 issues dos milestones por sprint, 57 estão concluídos (55%%): S1 15/17, S2 17/17, S3 7/10, S4 10/14, S5 4/8, S6 2/13, S7 2/14 e S8 0/10. Por repositório, as issues fechadas em relação ao total são backend 14/41, frontend 22/31, app 21/39 e docs 1/6; há 21 issues abertas do backend sem responsável. As sprints S6 (offline e sincronização) e S7 (revisão) estão muito atrasadas, e o desvio de prazo é real. Este relatório não o esconde: o capítulo %d o trata como situação monitorada, com ordem de corte e proposta de re-baseline, e o capítulo %d explica como ele foi detectado e como será tratado daqui em diante." % (n['crono'], n['monit']))
