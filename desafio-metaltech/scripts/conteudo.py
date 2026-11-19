#!/usr/bin/env python3
"""Textos e tabelas compartilhados entre analise-portfolio.md e relatorio-final-metaltech.docx.
Os numeros vem de modelo_portfolio.py; aqui ficam so os textos e as tabelas descritivas."""
import modelo_portfolio as M

GRUPO = ["Felipe Marques", "Gabriel Ribeiro", "Pedro Dias", "André Fernandes", "João Victor Souza"]


# ------------------------------------------------------------------ formatacao
def br(x, casas=0):
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def mil(x):
    """R$ 900 mil / R$ 1,2 mi"""
    if x >= 1000:
        v = x / 1000
        if abs(v - round(v)) < 1e-9:
            return "R$ " + br(v, 0) + " mi"
        if abs(v * 10 - round(v * 10)) < 1e-9:
            return "R$ " + br(v, 1) + " mi"
        return "R$ " + br(v, 2) + " mi"
    return "R$ " + br(x, 0 if abs(x - round(x)) < 1e-9 else 1) + " mil"


def pct(x, casas=0):
    return br(x, casas) + "%"


def n2(x):
    return br(x, 2)


# ------------------------------------------------------------------ justificativa das notas
JUST = {
    "P1": dict(AE="única fonte quantificada de produtividade: +12 p.p. dos 15 da meta (80%)",
               BC="R$ 75 mil por p.p. (faixa de 60 a 100 mil)", RI="risco Alto no enunciado",
               PR="6 meses (faixa de 6 a 9)", SI="P6 prepara a operação; é a precedência recomendada para o P8",
               VR="ocupa os 2 engenheiros de automação a 100% por 6 meses"),
    "P2": dict(AE="-20% de paradas equivale a 100% da meta", BC="R$ 22,5 mil por p.p. (faixa de 15 a 30 mil)",
               RI="risco Médio", PR="4 meses", SI="sem dependência explícita; complementa o P7, que fica para depois",
               VR="MAN a 100% e TI1 a 70% por 4 meses; engenheiros de automação só em consulta"),
    "P3": dict(AE="integração dos processos é benefício indireto, sem meta numérica",
               BC="R$ 1,2 mi sem benefício quantificado (acima de R$ 600 mil)", RI="risco Alto", PR="10 meses",
               SI="depende do P7 na etapa de integração, e o P7 só entra no G2",
               VR="ocuparia TI por 10 meses e exigiria integrador externo"),
    "P4": dict(AE="-25% de desperdício alimenta a meta de custos (efeito indireto, quantificado em desperdício)",
               BC="R$ 10 mil por p.p. (até 15 mil)", RI="risco Baixo", PR="3 meses",
               SI="complementar ao P5, ambos priorizados", VR="QUAL a 100% por 3 meses (sequenciável) e TI2 a 20%"),
    "P5": dict(AE="-30% de retrabalho equivale a 100% da meta", BC="R$ 11,7 mil por p.p. (até 15 mil)",
               RI="risco Médio", PR="4 meses", SI="complementar ao P4, que antecede e alimenta os requisitos",
               VR="QUAL a 100% e TI2 a 50% por 4 meses, depois do P4"),
    "P6": dict(AE="aumento de produtividade sem número no enunciado; contribui para os 15%",
               BC="sem benefício quantificado, investimento até R$ 150 mil; protege os R$ 900 mil do P1",
               RI="risco Baixo", PR="2 meses", SI="habilita a adoção do P1",
               VR="MAN a 20%; o conteúdo técnico vem do fornecedor do P1"),
    "P7": dict(AE="habilitador (dados em tempo real) sem meta numérica",
               BC="R$ 600 mil sem benefício quantificado (faixa de 150 a 600 mil)", RI="risco Médio", PR="5 meses",
               SI="relaciona-se ao P3 e ao Programa B, mas depende do G2",
               VR="exigiria engenheiros e TI quando ainda estão no P1"),
    "P8": dict(AE="+20% de capacidade não é nenhum dos 4 objetivos", BC="R$ 75 mil por p.p. de capacidade (fora das metas)",
               RI="risco Alto", PR="12 meses: benefício só depois do horizonte",
               SI="a empresa recomenda executar o P1 antes", VR="ocuparia engenheiros e TI o ano inteiro"),
}

RUBRICA = [
    ("Alinhamento estratégico (35%)",
     "5 = fonte principal quantificada de uma das 4 metas (80% ou mais); 4 = benefício quantificado com efeito indireto sobre uma meta; "
     "3 = ligado a uma meta, sem quantificação; 2 = benefício indireto ou fora das 4 metas; 1 = sem relação"),
    ("Benefício/custo (20%)",
     "Com benefício quantificado: custo por p.p. de até R$ 15 mil = 5; até 30 = 4; até 60 = 3; até 100 = 2; acima = 1. "
     "Sem benefício quantificado: investimento até R$ 150 mil = 3; até R$ 600 mil = 2; acima = 1"),
    ("Risco (15%)", "Baixo = 5; Médio = 3; Alto = 1 (classificação do enunciado)"),
    ("Prazo / retorno (10%)", "até 3 meses = 5; 4 meses = 4; 5 meses = 3; 6 a 9 meses = 2; 10 meses ou mais = 1"),
    ("Sinergia / dependências (10%)",
     "5 = relação direta com projeto também priorizado; 3 = independente ou relação condicionada; 2 = depende de projeto não priorizado ou de precedência não cumprida"),
    ("Viabilidade de recursos (10%)",
     "5 = uso marginal de especialistas; 4 = um especialista, sequenciável; 3 = 1 a 2 profissionais a 100% por até 4 meses; "
     "2 = profissionais críticos por 5 meses ou mais; 1 = vários especialistas por 10 meses ou mais"),
]

# ------------------------------------------------------------------ programas
PROG_TXT = {
    "A": dict(
        objetivo="Aumentar a produtividade e reduzir as paradas da fábrica, automatizando a Linha 1, antecipando falhas de equipamentos e preparando os operadores.",
        beneficio="+12% de produtividade (P1) e -20% de paradas (P2); o P6 protege a adoção e responde pelos 3 p.p. restantes da meta de 15%, sem quantificação própria.",
        metas="Produtividade +15%; Paradas -20%"),
    "B": dict(
        objetivo="Reduzir desperdícios e retrabalho, atacando a causa do refugo (P4) e modernizando o controle de qualidade (P5). É a fase 1 da Qualidade 4.0; o P7 seria a fase 2.",
        beneficio="-25% de desperdício (P4) e -30% de retrabalho (P5); os dois alimentam a meta de -10% de custos.",
        metas="Retrabalho -30%; Custos -10%"),
}
PROG_C = ("Programa C, Transformação Digital (P3 + P7), não ativado neste ciclo: o P3 está adiado e o P7 depende do gate G2. "
          "Fica como candidato a 2027, com o P7 antes do P3 para que a integração de dados industriais já exista quando o ERP começar.")

# ------------------------------------------------------------------ dependencias
DEPS = [
    ("P1 - P6", "O treinamento prepara os operadores para o equipamento novo",
     "Executar P6 no m5-m6, com gatilho no FAT do P1 (fim do m4). O conteúdo técnico vem do fornecedor do P1, sem tirar engenheiro do projeto.",
     "Atraso do FAT desloca o P6 (R08)"),
    ("P3 - P7", "A integração de dados industriais facilita uma etapa do ERP",
     "P3 adiado e P7 posterior (gate G2). Se o P3 voltar em 2027, o P7 vai antes.", "Programa C inativo; sem custo no ciclo"),
    ("P4 - P5", "Benefícios complementares em desperdício e retrabalho",
     "P4 no m1-m3 e P5 no m4-m7. O Pareto de defeitos do P4 vira requisito do P5; QUAL atende um projeto por vez.",
     "Sequência evita o conflito de QUAL"),
    ("P8 - P1", "A empresa recomenda P1 antes ou junto da expansão",
     "P8 adiado. A decisão de retomá-lo usa o balanço de produtividade do P1 (m9 e m12).", "P8 depende de dados reais do P1"),
]

# ------------------------------------------------------------------ G2
G2_CRITERIOS = [
    ("Prazo", "P4 encerrado no m3 e P2 no m4, ambos dentro do prazo (SPI de 0,95 ou mais)"),
    ("P1", "FAT aprovado no m4 e comissionamento no prazo para o go-live do m6"),
    ("Recursos financeiros", "saldo da reserva, economias capturadas e auditadas pela Controladoria e eventual complemento aprovado cobrem o P7 integral (R$ 600 mil) ou uma fase 1"),
    ("Recursos humanos", "EA e TI livres a partir do m7 (P1 concluído), sem conflito com a sustentação do P2 e do P5"),
    ("Dados", "linha de base aprovada e indicadores medidos desde o m1"),
]
G2_RESULT = [
    ("Go", "iniciar o P7 no m7 (m7-m11), integral"),
    ("Go faseado", "iniciar fase 1 do P7 com valor até o saldo disponível; o restante entra no ciclo seguinte"),
    ("Adiar", "sem recurso ou prazo comprometido: P7 volta ao Programa C em 2027"),
]


def saldo_g2():
    """cenarios de saldo da reserva no G2 e complemento necessario para o P7 integral"""
    p7 = M.PROJ["P7"]["inv"]
    cen = [
        ("Nenhuma contingência usada", M.RESERVA),
        ("Uso esperado (VME de R$ %s mil)" % br(M.EMV_TOTAL), M.RESERVA - M.EMV_TOTAL),
        ("Contingência do P1 inteira usada", M.RESERVA - 180),
        ("Reserva toda usada", 0),
    ]
    return [(n, s, p7 - s) for n, s in cen]


# ------------------------------------------------------------------ metas
METAS_TAB = [
    ("Produtividade", "+15%", "P1 (+12%); P6 e efeitos de P2 e P4 sem número",
     "12 de 15 p.p. (80%)", "negativa: faltam 3 p.p.",
     "Mesmo com o P1 a 100%, a meta só fecha se P6, P2 e P4 somarem 3 p.p. O enunciado não quantifica esses efeitos."),
    ("Paradas", "-20%", "P2 (-20%)", "20 de 20 p.p. (100%)", "zero",
     "Fecha apenas se o P2 entregar 100% do benefício. Com 90%, a redução é de 18%."),
    ("Custos", "-10%", "P4 (-25% de desperdício); efeitos indiretos de P5, P2 e P1",
     "não quantificada em custo", "não demonstrável",
     "Depende de quanto o refugo, o retrabalho e as paradas pesam no custo (hipótese na seção de sensibilidade) e da linha de base."),
    ("Retrabalho", "-30%", "P5 (-30%); P4 complementar", "30 de 30 p.p. (100%)", "zero",
     "Fecha apenas se o P5 entregar 100% do benefício. Com 90%, a redução é de 27%."),
]

PROTECOES = [
    "Linha de base de produtividade, paradas, retrabalho, refugo e custo por peça fechada e aprovada pela Controladoria até o fim do m1 (marco M1).",
    "Meta interna 10% acima do alvo nos indicadores sem folga: paradas -22%, retrabalho -33% e produtividade +16,5%.",
    "Aceite de fornecedor condicionado a indicador: o pagamento final do P1, do P2 e do P5 depende da medição em operação, não só da entrega do equipamento.",
    "Medição mensal no relatório executivo; balanço parcial no m9 e final no m12, com o resultado confrontado à trajetória linear até a meta.",
    "Gatilho de correção: indicador abaixo de 90% da trajetória aciona plano de ação no comitê e uso dirigido da reserva.",
    "No G2, os dados medidos no m1-m6 entram como evidência para liberar ou não o P7, que amplia a base de dados do P2.",
]

# ------------------------------------------------------------------ indicadores (cap. 6)
IND = [
    ("Produtividade", "Peças boas por hora-homem na Linha 1", "Linha de base no m1", "+15% (interna: +16,5%)", "Apontamento de produção, mensal", "Gerente de produção"),
    ("Paradas", "Horas de parada não planejada por mês e MTBF dos ativos críticos", "Linha de base no m1", "-20% (interna: -22%)", "Registro de manutenção, mensal", "Especialista em manutenção"),
    ("Custos", "Custo operacional por peça boa (R$/peça)", "Linha de base no m1", "-10% (interna: -11%)", "Controladoria, mensal", "Controladoria"),
    ("Retrabalho", "Peças retrabalhadas / peças produzidas (%)", "Linha de base no m1", "-30% (interna: -33%)", "Inspeção, semanal", "Especialista em qualidade"),
    ("Refugo (apoio)", "Peso ou peças refugadas / produzidas (%)", "Linha de base no m1", "-25%", "Apontamento de refugo, semanal", "Especialista em qualidade"),
]
CRITERIOS_ACEITE = [
    ("P1", "FAT aprovado com teste de integração; comissionamento e SAT na Linha 1; documentação e ensaio de segurança (NR-12); operação assistida", "EA1 e fornecedor"),
    ("P2", "Sensores e coleta nos ativos críticos; modelos validados em piloto de 3 ativos; alertas gerando ordens de serviço", "MAN e TI1"),
    ("P4", "Linha de base de refugo; Pareto de causas; plano de ações executado e controle padronizado", "QUAL"),
    ("P5", "Requisitos derivados do Pareto do P4; equipamentos calibrados; registro e CEP em uso; piloto validado", "QUAL e TI2"),
    ("P6", "Turmas concluídas por turno; avaliação de competência de 80% ou mais antes do go-live", "RH e MAN"),
]

# ------------------------------------------------------------------ EAP resumida (nivel 2)
EAP = {
    "P1": ["1.1 Gestão do projeto", "1.2 Especificação e projeto executivo", "1.3 Contratação e fabricação dos equipamentos",
           "1.4 FAT (teste de aceitação em fábrica)", "1.5 Instalação e integração à Linha 1", "1.6 Comissionamento, SAT e go-live",
           "1.7 Documentação e operação assistida"],
    "P2": ["2.1 Gestão do projeto", "2.2 Levantamento de ativos críticos e linha de base de paradas", "2.3 Sensores e aquisição de dados",
           "2.4 Modelos e plataforma preditiva", "2.5 Integração ao plano de manutenção (alertas e ordens de serviço)", "2.6 Treinamento e transição"],
    "P4": ["4.1 Gestão do projeto", "4.2 Medição e linha de base de refugo", "4.3 Análise de causas (Pareto e Ishikawa)",
           "4.4 Plano de ações e ajustes de processo", "4.5 Controle e padronização"],
    "P5": ["5.1 Gestão do projeto", "5.2 Requisitos de qualidade a partir do P4", "5.3 Equipamentos de inspeção e CEP",
           "5.4 Integração e registro de dados", "5.5 Procedimentos e calibração", "5.6 Piloto e validação"],
    "P6": ["6.1 Gestão do projeto", "6.2 Levantamento de necessidades por função", "6.3 Conteúdo e material com o fornecedor do P1",
           "6.4 Turmas por turno", "6.5 Avaliação de competências"],
}
ENTREGAS_PROJ = {
    "P1": "Linha 1 automatizada, integrada e aceita em operação; equipe com manual e operação assistida",
    "P2": "Sensores e plataforma de manutenção preditiva nos ativos críticos, com alertas ligados às ordens de serviço",
    "P4": "Causas do refugo identificadas, plano de ações executado e controle padronizado",
    "P5": "Sistema de inspeção e controle estatístico de processo calibrado e em uso",
    "P6": "Operadores treinados e avaliados para o equipamento novo",
}

# ------------------------------------------------------------------ comunicacoes
COMUNICACOES = [
    ("Reunião de status do portfólio (30 min)", "Semanal", "Síncrono (reunião)", "GP e coordenadores locais dos projetos", "GP"),
    ("Relatório executivo de uma página: semáforo por projeto, orçamento e reserva, 4 indicadores", "Mensal", "Assíncrono (PDF por e-mail)", "Diretoria", "PMO"),
    ("Comitê de portfólio: decisões, riscos e gates G1 (m3) e G2 (m6)", "Mensal e nos gates", "Síncrono (reunião)", "Diretoria, gerente de produção, Controladoria", "PMO"),
    ("Alerta de desvio ou gatilho de risco, com ação proposta", "Em até 24 h do evento", "Assíncrono (mensagem e registro no log de riscos)", "Diretoria e dono do risco", "GP"),
    ("Comunicado aos operadores: o que muda na Linha 1, quando e como será o treinamento", "Quinzenal a partir do m3", "Reunião de turno e quadro de avisos", "Operadores e supervisores da Linha 1", "Gerente de produção e RH"),
    ("Aviso de parada programada para instalação e comissionamento do P1", "15 dias antes de cada janela", "Reunião de turno e e-mail", "Produção, PCP e Comercial", "EA1"),
    ("Status de entrega e prazos de fabricação", "Quinzenal", "Síncrono (chamada) e e-mail", "Fornecedores de automação, sensores e inspeção", "EA1 e Compras"),
    ("Balanço de benefícios contra a linha de base (m9 e m12)", "Dois marcos", "Documento e apresentação", "Diretoria e Controladoria", "PMO e Controladoria"),
    ("Ata do portfólio com projetos adiados e condições de retorno", "Após cada comitê", "Assíncrono (documento)", "Áreas usuárias do ERP e da expansão", "PMO"),
]

# ------------------------------------------------------------------ partes interessadas (poder, interesse: 1-5, hipoteses)
PARTES = [
    ("S1", "Diretoria (patrocinador)", 5, 5, "Gerenciar com atenção", "Apoia", "Lidera",
     "Decisões nos gates, orçamento e reserva", "Comitê mensal e relatório executivo"),
    ("S2", "Gerente de produção e supervisores", 4, 5, "Gerenciar com atenção", "Neutro", "Apoia",
     "Janelas de instalação, operação da Linha 1, adoção", "Reunião semanal e envolvimento no FAT"),
    ("S3", "Controladoria e financeiro", 4, 3, "Manter satisfeito", "Neutro", "Apoia",
     "Linha de base, custo por peça, auditoria das economias", "Relatório mensal e validação da linha de base"),
    ("S4", "Clientes (automotivo e máquinas industriais)", 4, 2, "Manter satisfeito", "Neutro", "Neutro",
     "Prazo de entrega e qualidade durante as paradas", "Aviso prévio de janelas; indicadores de qualidade"),
    ("S5", "Operadores da Linha 1", 2, 5, "Manter informado", "Resistente", "Apoia",
     "Segurança no emprego, treinamento, mudança de rotina", "Reunião de turno, treinamento do P6 e operadores-chave no FAT"),
    ("S6", "Engenharia de automação (EA1, EA2)", 3, 5, "Manter informado", "Apoia", "Lidera",
     "Escopo técnico e dedicação integral", "Rito semanal e backup entre pares"),
    ("S7", "TI (TI1, TI2)", 3, 4, "Manter informado", "Neutro", "Apoia", "Integração de dados e sistemas", "Rito semanal"),
    ("S8", "Qualidade e Manutenção (QUAL, MAN)", 3, 5, "Manter informado", "Apoia", "Lidera",
     "Metas de retrabalho e paradas", "Rito semanal e coordenação local dos projetos"),
    ("S9", "Fornecedores de automação (P1)", 3, 4, "Manter informado", "Neutro", "Apoia", "Escopo, prazos e pagamentos por marco", "Reunião quinzenal"),
    ("S10", "Fornecedores de sensores, software e inspeção", 2, 3, "Monitorar", "Neutro", "Neutro", "Escopo e prazo de entrega", "Cotação e acompanhamento de pedido"),
    ("S11", "RH e treinamento", 2, 3, "Monitorar", "Neutro", "Apoia", "Turmas e liberação dos operadores", "Planejamento do P6 a partir do m3"),
    ("S12", "Áreas usuárias do ERP e da expansão (P3, P8)", 3, 4, "Manter informado", "Neutro", "Neutro",
     "Projetos adiados e condições de retorno", "Ata do portfólio e revisão no m12"),
]

# ------------------------------------------------------------------ aquisicoes (valores = composicao COMP, hipotese)
AQUIS = [
    ("Equipamentos de automação da Linha 1 (CLPs, atuadores, transporte)", "P1", "A", 500, "RFP com 3 ou mais propostas; contrato de preço global com marcos de pagamento e multa por atraso", "Pedido até o m2"),
    ("Consultoria de integração e engenharia (projeto executivo, legado)", "P1", "C", 180, "RFP; escopo e aceite no FAT", "Contrato até o m1"),
    ("Instalação, comissionamento e adequação de segurança (NR-12)", "P1", "F", 150, "Incluída na proposta do fornecedor ou cotação separada; em paradas programadas", "Plano até o m3"),
    ("Licenças de automação e supervisório", "P1", "E", 70, "Licença perpétua ou anual conforme o fornecedor", "Com o pedido de equipamentos"),
    ("Sensores de vibração, temperatura e corrente (ativos críticos)", "P2", "B", 170, "Três cotações; menor preço técnico", "Pedido até o m1"),
    ("Plataforma de manutenção preditiva (SaaS)", "P2", "E", 110, "Prova de conceito de 30 dias e contrato anual", "Decisão até o m2"),
    ("Consultoria de modelagem e integração de dados", "P2", "C", 100, "Tempo e material com teto e entregas por marco", "Contrato até o m1"),
    ("Gateways, rede industrial e instalação dos sensores", "P2", "F", 70, "Cotação com instalador", "Pedido até o m2"),
    ("Consultoria de análise de causas do refugo", "P4", "C", 100, "Escopo fechado de diagnóstico", "Contrato até o m1"),
    ("Instrumentos de medição e apontamento de refugo", "P4", "B", 80, "Cotação; compra por catálogo", "Pedido até o m1"),
    ("Treinamento da equipe em ferramentas de qualidade", "P4", "D", 40, "Turma fechada com instituição de ensino", "m2"),
    ("Ajustes de ferramental e processo", "P4", "F", 30, "Compra direta, executada pelo plano de ações", "m3"),
    ("Equipamentos de inspeção (medição dimensional e visão)", "P5", "A", 200, "Três cotações; calibração rastreável", "Pedido até o m4"),
    ("Software de CEP e registro de qualidade", "P5", "E", 70, "Avaliação técnica e contrato anual", "Decisão até o m4"),
    ("Integração e calibração dos equipamentos", "P5", "C", 40, "Serviço do próprio fornecedor ou terceiro acreditado", "m5-m6"),
    ("Treinamento em inspeção e CEP", "P5", "D", 40, "Turma fechada", "m6"),
    ("Treinamento dos operadores (conteúdo do fornecedor do P1, instrutores, avaliação)", "P6", "D", 150, "Previsto no contrato do P1; instrutores internos certificados", "m4-m5"),
]
for _p in M.COMP:
    assert sum(a[3] for a in AQUIS if a[1] == _p) == M.PROJ[_p]["inv"], _p
for _c in M.CATS:
    assert sum(a[3] for a in AQUIS if a[2] == _c) == M.CAT_TOTAL[_c], _c

CRIT_FORN = [("Capacidade técnica e referências na área", 30), ("Prazo de entrega e cumprimento do cronograma", 25),
             ("Preço total de propriedade", 25), ("Suporte local e garantia", 10), ("Aderência a segurança e normas", 10)]
assert sum(c[1] for c in CRIT_FORN) == 100

# ------------------------------------------------------------------ referencias (ABNT; sem DOI/URL inventados)
REFS = [
    "CARVALHO, Fábio Câmara Araújo de. **Gestão de projetos**. 2. ed. São Paulo: Pearson, 2018. E-book.",
    "CRUZ, Fábio. **Scrum e PMBOK unidos no gerenciamento de projetos**. Rio de Janeiro: Brasport, 2013. E-book.",
    "FINOCCHIO JÚNIOR, José. **Project Model Canvas**: gerenciamento de projetos sem burocracia. Rio de Janeiro: Elsevier, 2013.",
    "PROJECT MANAGEMENT INSTITUTE. **Um guia do conhecimento em gerenciamento de projetos (Guia PMBOK)**. 5. ed. Newtown Square: PMI, 2013.",
    "PROJECT MANAGEMENT INSTITUTE. **The standard for portfolio management**. 4. ed. Newtown Square: PMI, 2017.",
    "PROJECT MANAGEMENT INSTITUTE. **The standard for program management**. 4. ed. Newtown Square: PMI, 2017.",
    "SOUZA, Carla Patricia da Silva. **Gestão de projetos**. São Paulo: Contentus, 2020.",
]
