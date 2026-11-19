# -*- coding: utf-8 -*-
"""Capitulos de custos, qualidade e riscos (Avaliacao 2)."""
import dados as DD
import fatos as F
from fatos import br, rs, pct


# =====================================================================================  CUSTOS
def custos(r):
    n = r.N
    c = n['custos']
    r.h1(f"{c} CUSTOS E ORÇAMENTO")
    r.par("O FieldOps não tem investimento financeiro direto (restrição R07). O orçamento existe para dimensionar o esforço, comparar o plano com a realidade e dar uma base ao controle, por isso quase todo o custo é de mão de obra valorada como custo de oportunidade, e não desembolso. **Todos os valores deste capítulo são hipóteses de valoração.** O enunciado pede explicitar as hipóteses quando faltam dados reais, e é o que as seções seguintes fazem.")
    r.h2(f"{c}.1 Itens de custo e premissas")
    r.par("O orçamento tem **52 itens**: 36 linhas de mão de obra, uma por pacote da EAP; 14 linhas de custo direto (as mesmas aquisições P01 a P14); e 2 reservas. As premissas que sustentam os valores são as do @Q:premorc@.")
    pm = [
        ["Capacidade", "5 pessoas × 16 semanas × 12 h = 960 h; o cronograma fecha em 967 h (+0,7%)"],
        ["Taxa de desenvolvedor", "R$ 45,00/h (JV, GR, PD, AF e FM quando atua como desenvolvedor, pacotes 5.x, 6.x e 7.x)"],
        ["Taxa de gerente de projeto", "R$ 60,00/h, só nas horas de gestão do FM (pacotes 1.x); contam dentro das 192 h dele"],
        ["Mentoria e revisão docente", "não entram no orçamento financeiro (contrapartida institucional); 74 h estimadas, à parte"],
        ["Câmbio", "US$ 1,00 = R$ 5,50 para serviços em dólar (hipótese)"],
        ["Custos de caixa", "plano gratuito no cenário mais provável sempre que existir; plano pago só na janela de pico; o cenário pessimista cobre upgrades"],
        ["Estimativa de três pontos", "cO (otimista), cM (mais provável) e cP (pessimista); esperado PERT = (cO + 4·cM + cP) ÷ 6; desvio σ = (cP − cO) ÷ 6"],
        ["Reservas", "contingência de 10% sobre o custo base (riscos identificados), dentro da linha de base; reserva gerencial de 5% (desconhecidos), fora da linha de base"],
    ]
    r.tabela("Premissas do orçamento", ["Premissa", "Valor"], pm, [4, 12], kind="Quadro", size=9, first_col_bold=True, fonte_txt="orcamento-fieldops.md, seção (a). Todas as taxas e preços são hipóteses de valoração; preços de serviços devem ser confirmados antes de contratar.", key="premorc")
    r.par("Para a mão de obra, o cenário mais provável (cM) é horas do cronograma × taxa. Os cenários otimista e pessimista aplicam às horas um fator que depende da **classe de risco do pacote**, uma premissa do gerente justificada pela incerteza técnica de cada tipo de trabalho (@Q:classes@). A classe D, de offline e sincronização, tem a cauda pessimista mais pesada por ser o item de maior incerteza técnica do projeto; o atraso real de S6 confirma a escolha.")
    cl = [
        ["A", "Documentação e gestão (escopo conhecido)", "0,90", "1,20", "1,0167", "1.1, 1.2, 1.3, 1.4, 2.1, 6.1, 7.3, 7.4"],
        ["B", "Padrão conhecido (CRUD, autenticação, base de projeto)", "0,85", "1,30", "1,025", "2.2, 2.3, 2.4, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 7.1"],
        ["C", "Integração, UI complexa e recursos nativos", "0,85", "1,45", "1,05", "3.3, 3.4, 3.5, 3.7, 4.3 a 4.6, 5.3, 5.4, 5.5, 6.2, 6.3, 6.4, 7.2"],
        ["D", "Offline e sincronização (maior incerteza)", "0,85", "1,60", "1,075", "3.6, 5.6, 5.7"],
    ]
    r.tabela("Fatores de três pontos por classe de risco da mão de obra", ["Classe", "Tipo de trabalho", "cO", "cP", "PERT ÷ cM", "Pacotes"], cl, [1.2, 5.4, 1.0, 1.0, 1.6, 5.8], kind="Quadro", size=8.5, align=["c", "l", "c", "c", "c", "l"],
             fonte_txt="orcamento-fieldops.md, seção (a). Os fatores multiplicam as horas do cronograma (premissa do gerente).", key="classes")
    r.h2(f"{c}.2 Estimativas e linha de base")
    r.par(f"Cada item tem cO, cM, cP, valor esperado e desvio (Apêndice B). A mão de obra soma {rs(44475.00)} no cenário mais provável e {rs(46323.25)} no valor esperado (cerca de 1.008 h esperadas, 5% acima das 960 h); os custos diretos somam {rs(1391.58)} de valor esperado. O valor esperado PERT e o método do valor agregado seguem o Guia PMBOK (PMI, 2013). O orçamento usa o valor esperado, e não o mais provável, porque as estimativas são assimétricas: cP está mais longe de cM do que cO, e a soma dos cM ({rs(45545.00)}) é menor que o esperado base. O @Q:lb@ mostra a construção da linha de base.")
    lb = [
        ["Custo base, mão de obra (valor esperado PERT)", rs(46323.25), "967 h pelo cronograma; 1.008 h esperadas"],
        ["Custo base, custos diretos (valor esperado PERT)", rs(1391.58), "14 linhas de aquisições"],
        ["**Custo base (A)**", "**" + rs(F.CUSTO_BASE) + "**", "soma dos valores esperados"],
        ["Reserva de contingência de 10% (B)", rs(F.CONTING), "riscos identificados; liberada pelo gerente, com registro"],
        ["**Linha de base de custos, BAC (A + B)**", "**" + rs(F.BAC) + "**", "referência para o EVM"],
        ["Reserva gerencial de 5% (C)", rs(F.GERENCIAL), "desconhecidos; liberada só pela coordenação (PI-01)"],
        ["**Orçamento total (A + B + C)**", "**" + rs(F.CUSTO_TOTAL) + "**", ""],
    ]
    r.tabela("Linha de base de custos e orçamento total", ["Componente", "Valor (R$)", "Observação"], lb, [6.6, 3.0, 6.4], kind="Tabela", size=9, align=["l", "r", "l"], fonte_txt="orcamento-fieldops.md, seção (d). Valores hipotéticos de valoração.", key="lb")
    r.par("O desvio-padrão do custo total, supondo itens independentes, é de R$ 812,45, e a contingência de R$ 4.771,48 equivale a 5,9 desvios. A premissa de independência é otimista, porque os itens de offline, sincronização e revisão atrasam juntos. O cenário pessimista conjunto, com todos os cP ao mesmo tempo, soma R$ 65.181,50, ou R$ 10.309,45 acima do orçamento total. O orçamento cobre desvios isolados, não um atraso generalizado, e nesse caso a resposta é de escopo e prazo (ordem de corte), e não de reserva financeira.")
    r.h2(f"{c}.3 Distribuição por entrega, por categoria e por sprint")
    cab, rows = DD.tabela_generica("orc", "### Por entrega da EAP")
    r.tabela("Custo por entrega da EAP (valor esperado, sem reservas)", ["Entrega", "Mão de obra", "Infraestrutura", "Ferramentas e serviços", "Total", "% do custo base", "Horas"], rows, [3.4, 2.4, 2.3, 2.3, 2.4, 1.6, 1.2], kind="Tabela", size=8.5,
             align=["l", "r", "r", "r", "r", "r", "r"], bold_rows=(7,), fonte_txt="orcamento-fieldops.md, seção (c).", key="porent")
    cab, rows = DD.tabela_generica("orc", "### Por categoria")
    r.par("O custo concentra-se na API (24,2% do custo base), no aplicativo mobile (18,5%) e em qualidade e testes (16,1%). Por categoria, a mão de obra responde por 84,4% do orçamento total, a contingência (as duas reservas) por 13,0%, a infraestrutura por 2,1% e as ferramentas e serviços por 0,4% (@Q:porcat@).")
    r.tabela("Custo por categoria (inclui as reservas)", ["Categoria", "Valor (R$)", "% do orçamento total"], rows, [6, 4, 4], kind="Tabela", size=9, align=["l", "r", "r"], bold_rows=(4,), fonte_txt="orcamento-fieldops.md, seção (c).", key="porcat")
    r.par("A distribuição por sprint (@F:curvas@) reparte a mão de obra pelos dias úteis de cada atividade e os custos diretos pela data de aquisição; a contingência acompanha o custo base de cada sprint, e a reserva gerencial fica fora da curva. S5 e S6 são as sprints mais caras (R$ 7.386,22 e R$ 7.588,21) porque concentram recursos nativos, offline e sincronização, as classes C e D, que também são as que mais estouram.")
    r.figura("curva_s_ret.png", "Curva S da linha de base por sprint e EVM da mão de obra em 18/11/2026", 15.5, altura_max_cm=7.5, key="curvas",
             fonte_txt="Elaborado pelos autores (2026), a partir de orcamento-fieldops.md (seções e e f). AC (custo real) é hipótese: não há apontamento de horas. Versão original: curva-s-orcamento-fieldops.png.")
    r.h2(f"{c}.4 Aquisições")
    r.par("As 14 aquisições (P01 a P14) são as linhas de custo direto do orçamento, ligadas ao pacote que as consome e a uma data de entrega. No cenário mais provável, somam R$ 1.070,00: **R$ 374,00 de caixa** e R$ 696,00 de custo não monetário (aparelhos Android próprios e rateio de internet e energia). O valor esperado é de R$ 1.391,58, dos quais R$ 669,08 de caixa esperado; o pior caso conjunto de caixa é de R$ 2.478,50, que só passa do teto de R$ 1.500 admitido para o projeto por causa de dois itens contingentes (um aparelho Android de entrada, P10, e a conta de desenvolvedor do Google Play, P11), que dependem de um gatilho. Sem eles, o pior caso de caixa é de R$ 1.441,00.")
    cab, rows = DD.tabela_generica("aq", "### Estimativa de três pontos e ligação com o orçamento")
    linhas = [[x[0], x[2], x[1], x[3], x[4], x[5], x[6], x[7]] for x in rows if x[0].startswith("P")]
    r.tabela("Aquisições: item, linha do orçamento, tipo e estimativa de três pontos (R$)", ["ID", "Item", "Linha", "Tipo", "cO", "cM", "cP", "Esperado"], linhas, [0.9, 4.6, 1.1, 1.5, 1.7, 1.7, 1.7, 1.8], kind="Tabela", size=7.5, align=["c", "l", "c", "l", "r", "r", "r", "r"],
             fonte_txt="aquisicoes-fieldops.md. Urgência, motivo, fornecedores, previsão de entrega e observações: Apêndice F.", key="aqtab")
    r.par("A estratégia de fazer ou comprar é simples: o que gera valor para a disciplina é feito (API, regras de negócio, sincronização, autorização, painel e app); o que é infraestrutura de demonstração é contratado pelo menor custo (hospedagem da API, PostgreSQL, armazenamento S3, painel web, build Android, domínio e monitoramento); frameworks e bibliotecas são reutilizados com licenças abertas; e os aparelhos Android são os da equipe, com compra só como contingência. Os fornecedores foram comparados por critérios ponderados (custo 25%, plano gratuito e limites 20%, aderência técnica 20%, confiabilidade 15%, facilidade 10% e portabilidade 10%), com notas do gerente (premissa subjetiva): Render para a hospedagem da API (3,95), Neon para o PostgreSQL (4,25), Cloudflare R2 para o armazenamento (4,45) e Expo EAS para o build (4,05), com build local como plano B. Quase todas as aquisições são termos de serviço com adesão online, sem negociação; o controle é a conferência da fatura contra o orçamento e o cancelamento das assinaturas no encerramento (atividade A62).")
    r.par("Há uma pendência de leitura: a linha de base de P01, P02, P03, P05 e P11 vence entre 13/11 e 16/11, antes de 18/11, e o cronograma mostra EAS e deploy sem avanço, então é preciso confirmar com o gerente quais foram de fato contratados.")
    r.h2(f"{c}.5 Acompanhamento dos custos e tratamento de desvios")
    r.par("O acompanhamento usa o método do valor agregado (EVM). As fórmulas e os limiares do semáforo estão no @Q:evmf@; os limiares de custo são mais estreitos que os de prazo porque, num projeto sem caixa relevante, a hora é o único recurso e não se recupera.")
    ev = [
        ["PV (valor planejado)", "custo da linha de base planejado até a data", "—", "—", "—"],
        ["EV (valor agregado)", "Σ (% concluído × custo da atividade na linha de base)", "—", "—", "—"],
        ["AC (custo real)", "horas apontadas × taxa da pessoa + caixa pago", "—", "—", "—"],
        ["SPI", "EV ÷ PV", "≥ 0,95", "0,70 a 0,94", "< 0,70"],
        ["CPI", "EV ÷ AC", "≥ 0,95", "0,85 a 0,94", "< 0,85"],
        ["EAC e ETC", "EAC = BAC ÷ CPI; ETC = EAC − AC", "—", "—", "—"],
        ["TCPI", "(BAC − EV) ÷ (BAC − AC)", "≤ 1,00", "1,01 a 1,10", "> 1,10"],
    ]
    r.tabela("Indicadores do EVM, fórmulas e limiares do semáforo", ["Indicador", "Fórmula", "Verde", "Amarelo", "Vermelho"], ev, [3, 7.2, 1.8, 2.2, 1.8], kind="Quadro", size=8.5, align=["l", "l", "c", "c", "c"],
             fonte_txt="orcamento-fieldops.md, seção (f).", key="evmf")
    r.par("A rotina de apontamento ainda **precisa ser implantada**: cada integrante registraria as horas por atividade (ID do cronograma) até sexta-feira, e o gerente consolidaria AC e EV antes de cada marco. Sem isso, o custo real de 18/11 é uma **hipótese**: assume-se que cada pessoa cumpriu 12 h por semana, ou 168 h em 70 dias úteis, ao custo médio por hora da pessoa. O EV usa o percentual estimado das atividades. O cálculo cobre só a mão de obra (R$ 46.323,25), porque o caixa pesa menos de 3% do custo base.")
    ev2 = DD.evm_tabela()
    ev2 = [[a[0], a[1], a[2]] for a in ev2]
    r.tabela("EVM da mão de obra em 18/11/2026", ["Indicador", "Valor", "Situação"], ev2, [4.5, 3.4, 8.1], kind="Tabela", size=8.5, align=["l", "r", "l"], fonte_txt="orcamento-fieldops.md, seção (f). AC é hipótese (168 h por pessoa em 70 dias úteis); EV usa o percentual estimado por atividade.", key="evm")
    r.par("A leitura é a seguinte. A equipe consumiu cerca de 840 h de capacidade (87%% das 967 h planejadas) e entregou 49%% do trabalho em valor. O SPI de 0,53 confirma o atraso do cronograma, e o CPI de 0,58, vermelho, significa cerca de 58 centavos de entrega por real de esforço, **se** a hipótese de uso de capacidade estiver certa. Como as horas são fixas e não se compram, o EAC de R$ 79.416,81 não é gasto novo: é o esforço total que o projeto exigiria se o ritmo atual continuasse, e serve para dimensionar a decisão de escopo e prazo da seção %d.7. Por isso o desvio de custo, aqui, é um desvio de capacidade, e o tratamento dele é de escopo, não de verba." % n['crono'])
    r.par("Os desvios de custo são tratados por alçadas, que valem também para o processo de mudanças do capítulo %d (@Q:alcadas@). A ordem de grandeza das faixas é: 5%% da linha de base equivalem a R$ 2.624,32 e 10%%, a R$ 5.248,63." % n['monit'])
    al = [[a[0], a[1], a[2], a[3]] for a in DD.alcadas()]
    r.tabela("Tratamento de desvios de custo e alçadas de aprovação", ["Situação", "Gatilho", "Tratamento", "Quem aprova"], al, [2.7, 3.6, 5.5, 4.2], kind="Quadro", size=8, fonte_txt="orcamento-fieldops.md, seção (f).", key="alcadas")
    r.par("Por fim, as horas não valoradas (contrapartida institucional) somam cerca de 74 h estimadas: Prof. Glauco 28 h, professores das disciplinas 24 h, Prof. Deivison 18 h e coordenação 4 h. Elas não entram no orçamento nem no total de horas da equipe, e a taxa de docente não foi arbitrada.")


# =====================================================================================  QUALIDADE
def qualidade(r):
    n = r.N
    c = n['qual']
    r.h1(f"{c} QUALIDADE E CRITÉRIOS DE ACEITAÇÃO")
    r.par("O plano de qualidade segue os três processos da disciplina: planejar (definir o que é qualidade e como medi-la), garantir (auditar processos) e controlar (medir resultados e recomendar mudanças). Os números vêm de dados reais do GitHub, coletados e calculados por script em 18/11/2026 às 14h56 UTC (117 issues, 69 pull requests, 601 commits sem merges e 99 execuções de CI), e onde o dado não existe a ferramenta usa premissa rotulada.")
    r.h2(f"{c}.1 Padrões e requisitos de qualidade")
    cab, rows = DD.tabela_generica("qual", "### 2.1 Padrões e requisitos")
    r.tabela("Padrões e requisitos de qualidade aplicáveis ao FieldOps", ["Padrão ou requisito", "Fonte", "O que exige", "Onde é verificado"], rows, [3.2, 2.6, 6.2, 4.0], kind="Quadro", size=7.5,
             fonte_txt="qualidade-7-ferramentas-fieldops.md, seção 2.1. DoD: Definição de Pronto (documento 18 da especificação).", key="padroes")
    r.h2(f"{c}.2 Critérios de aceitação por marco e por entrega")
    r.par("Cada marco tem um critério principal, que vem da rubrica de avaliação por marcos (documento 19.6), e um conjunto de critérios de aceitação por funcionalidade (documento 17), escritos como cenários dado/quando/então. Os critérios das entregas de nível 1 estão no @Q:entregas@ e os dos 36 pacotes, no Apêndice D. O @Q:acmarco@ liga cada marco aos critérios e aos pacotes verificados.")
    cab, rows = DD.tabela_generica("qual", "### 2.2 Critérios de aceitação por marco")
    r.tabela("Critérios de aceitação por marco", ["Marco", "Critério principal (rubrica 19.6)", "Critérios de aceitação (documento 17)", "Pacotes da EAP"], rows, [2.8, 4.4, 5.6, 3.2], kind="Quadro", size=8,
             fonte_txt="qualidade-7-ferramentas-fieldops.md, seção 2.2. Pesos dos marcos no @Q:marcos@.", key="acmarco")
    r.par("Duas barreiras valem para todas as entregas. A primeira é a Definição de Pronto: código em branch própria com pull request e revisão, lint e tipos, sem segredos ou logs sensíveis, critérios de aceitação testados (o caso principal e ao menos uma exceção), estados de carregamento, vazio, erro e offline tratados, contrato de API atualizado, autorização validada no backend e evidência de funcionamento. A segunda é a **severidade de defeitos**: um defeito crítico (perda de dados, falha de segurança, duplicidade grave ou fluxo principal impossível) bloqueia a entrega; um defeito alto precisa ser corrigido antes da release.")
    r.h2(f"{c}.3 Verificação, validação e responsáveis")
    cab, rows = DD.tabela_generica("qual", "### 2.4 Atividades de garantia")
    r.par("A **verificação** confere se a entrega foi feita conforme o padrão (CI, revisão de pull request, folha de verificação do DoD, testes automatizados), e a **validação** confere se ela atende à necessidade (demonstração do marco contra os critérios de aceitação, teste com usuário-proxy e o ensaio do AC-RELEASE). Os responsáveis são **proposta a confirmar com o grupo**; a regra de autoria é que o revisor de um pull request nunca é o autor.")
    r.tabela("Atividades de garantia e de controle da qualidade, frequência e responsáveis", ["Processo", "Atividade", "Frequência", "Responsável", "Evidência"], rows, [2.1, 5.2, 2.0, 3.6, 3.1], kind="Quadro", size=8, fonte_txt="qualidade-7-ferramentas-fieldops.md, seção 2.4.", key="garantia")
    r.h2(f"{c}.4 Tratamento de não conformidades")
    r.par("Uma não conformidade é qualquer desvio do DoD, defeito, falha de CI ou critério de aceitação não atendido. Todo defeito vira uma issue com **rótulo de defeito e severidade**. Hoje isso não acontece: nenhuma das 117 issues tem rótulo de defeito, e por isso não existe taxa de defeitos, apenas o proxy dos commits fix.")
    cab, rows = DD.tabela_generica("qual", "### 2.5 Tratamento de não conformidades")
    r.tabela("Severidade, prazo de tratamento, decisão e registro", ["Severidade (DoD 18.7)", "Prazo", "Quem decide", "Registro"], rows, [5.4, 2.4, 3.2, 5.0], kind="Quadro", size=8.5, fonte_txt="qualidade-7-ferramentas-fieldops.md, seção 2.5.", key="sev")
    r.h2(f"{c}.5 Diagnóstico com as sete ferramentas básicas")
    r.par("As sete ferramentas foram aplicadas a dados reais. O @Q:sete@ resume a pergunta de cada uma, o achado e a ação; as figuras principais seguem no texto, e o fluxograma, a folha de verificação, o histograma e a dispersão estão no Apêndice J. O achado de conjunto é que o FieldOps produz código com padrão razoável (branches no padrão em 89% dos pull requests e títulos em Conventional Commits em 95%, CI verde em 97% dos merges verificáveis, testes no diff em 85% e documentação no diff em 82%), mas **não verifica o que declara**: o DoD é autodeclarado.")
    cab, rows = DD.tabela_generica("qual", "## 5. Quadro-resumo das ferramentas")
    r.tabela("As sete ferramentas: pergunta, achado principal e ação", ["Ferramenta", "Pergunta respondida", "Achado principal", "Ação"], rows, [2.4, 3.8, 5.6, 4.2], kind="Quadro", size=8, fonte_txt="qualidade-7-ferramentas-fieldops.md, seção 5.", key="sete")
    r.par("**Causas.** O diagrama de causa e efeito (@F:ishi@) organiza as causas das falhas de sincronização e dos defeitos que escapam para a integração. A causa-raiz provável, pelos cinco porquês, é de processo e de pessoas: um DoD sem verificação, somado à concentração de commits (98% no app, 88% no backend e 75% no frontend em uma só pessoa por repositório). O contrato de sincronização (docs #2) continua aberto, e o login real do app só foi integrado à API em 18/09.")
    r.secao_paisagem()
    r.figura("ishikawa.png", "Diagrama de causa e efeito: falhas de sincronização offline e defeitos que escapam para a integração", 22.0, altura_max_cm=12.6, key="ishi",
             fonte_txt="qualidade-7-ferramentas-fieldops.md (figura 1). Causas com evidência no GitHub (marcadas com estrela) ou premissa do gerente (marcadas com círculo vazio).")
    r.secao_retrato()
    r.par("**Defeitos e não conformidades.** O Pareto de defeitos usa 50 commits fix classificados por script em sete categorias (@F:pareto@). Por frequência, layout e acabamento visual lideram (40%), são de baixa severidade e concentram-se em duas rajadas de ajustes (09/11 e 18/11). Ponderados por severidade presumida (pesos 1, 3, 5 e 10, premissa do gerente), a ordem muda: regras de negócio e sessão e segurança passam à frente, e persistência, offline e sincronização sobe para o terceiro lugar. O que dói pouco aparece muito; o que dói muito aparece pouco, e por isso os testes de regressão devem se concentrar em sessão, regras de negócio e sincronização.")
    r.figura("pareto_defeitos_ret.png", "Pareto dos defeitos corrigidos: frequência e ponderação por severidade", 14.0, altura_max_cm=13.5, key="pareto",
             fonte_txt="Elaborado pelos autores (2026), a partir de qualidade-7-ferramentas-fieldops.md (figura 4a; dados em dados/fixes_classificados.csv). Pesos de severidade: premissa.")
    r.par("No processo, o Pareto das não conformidades (@F:paretonc@) mostra que **quatro itens do DoD respondem por cerca de 82% das marcas**: a revisão registrada por outra pessoa (49), a evidência de funcionamento (28), a issue vinculada (14) e os testes no diff (7). Dos 55 pull requests mergeados analisados, 49 (89%) **não têm revisão registrada de outra pessoa no GitHub**. A medida enxerga só a revisão registrada na plataforma, e revisão por chat ou presencial não aparece; o número não é um juízo sobre as pessoas. O autor marcou revisão em apenas 4 pull requests, e só 40% anexaram a evidência de funcionamento que o DoD pede. O tamanho mediano do pull request é de 936 linhas (75% passam de 400), e a mediana do tempo até o merge é de 9 minutos, o que é coerente com a ausência de uma etapa de revisão; a dispersão entre tamanho e tempo mostra correlação praticamente nula (r = 0,06).")
    r.figura("pareto_nc.png", "Pareto das não conformidades do DoD nos pull requests", 14.0, altura_max_cm=7.0, key="paretonc",
             fonte_txt="qualidade-7-ferramentas-fieldops.md (figura 4b). 55 pull requests mergeados analisados.")
    r.par("**Estabilidade do processo.** O gráfico p (@F:gp@) mostra comportamento estável até S5 (62,5% a 88,2%) e dois pontos abaixo do limite inferior de controle: **S6 (15,4%) e S7 (21,4%)**. Isso indica causa especial, e não variação do acaso, e a causa é identificável: as issues de push, pull, conflito e arquivos do backend não têm responsável, e o motor de sincronização do app não foi iniciado. O ponto de S2 acima do limite superior não é desempenho extraordinário: as issues dessa sprint foram fechadas em lote, semanas depois. Só 12 das 59 issues com sprint foram fechadas até o fim da sprint prevista (20%). Nota de coleta: a análise de qualidade usa a coleta de 18/11 às 14h56 UTC, com 59 de 103 issues concluídas (S5 5/8 e S7 3/14), enquanto os demais documentos usam o levantamento anterior (57 de 103; S5 4/8 e S7 2/14); a diferença é de duas issues do frontend fechadas às 14h30 UTC.")
    r.figura("grafico_p.png", "Gráfico p: proporção de issues concluídas por sprint, com limites de controle de 3 sigma", 13.5, altura_max_cm=7.8, key="gp",
             fonte_txt="qualidade-7-ferramentas-fieldops.md (figura 6a). Coleta de 18/11/2026 (59 de 103 issues). S8 está em curso e fica fora do cálculo.")
    r.par("O gráfico I-MR de commits por semana (@F:imr@) mostra que 73% dos 601 commits caem em apenas 3 semanas (1, 11 e 14), que a semana 11 (19 a 25/10, antes do marco M6) tem 214 commits, acima do limite superior de 203, e que houve duas semanas sem commit (5 e 9). O padrão é de entrega em rajadas antes dos prazos, seguida de silêncio, e não de fluxo contínuo.")
    r.figura("grafico_imr.png", "Gráfico I-MR de commits por semana", 13.5, altura_max_cm=8.5, key="imr", fonte_txt="qualidade-7-ferramentas-fieldops.md (figura 6b). Semana 1 = 10/08/2026; a semana 15 (parcial) não entra no cálculo.")
    r.h2(f"{c}.6 Métricas, metas e ações")
    r.par("As metas abaixo são **propostas do gerente** (premissa a confirmar com o grupo); a linha de base foi calculada por script com os dados de 18/11/2026. Os mesmos números alimentam os indicadores do capítulo %d." % n['monit'])
    cab, rows = DD.tabela_generica("qual", "### 2.3 Métricas")
    r.tabela("Métricas de qualidade: linha de base em 18/11/2026 e meta proposta", ["Métrica", "Linha de base", "Meta proposta", "Ferramenta"], rows, [5.6, 3.8, 4.2, 2.4], kind="Quadro", size=8, fonte_txt="qualidade-7-ferramentas-fieldops.md, seção 2.3.", key="metricas")
    r.par("As cinco ações priorizadas para a sprint S8, com responsáveis e prazos propostos, são:")
    cab, rows = DD.tabela_generica("qual", "## 6. Síntese integrada")
    rows = [[x[0], x[1], x[3], x[4], x[5]] for x in rows]
    r.tabela("Ações priorizadas para a sprint S8", ["#", "Ação", "Responsável", "Prazo", "Indicador de sucesso"], rows, [0.7, 8.0, 2.6, 1.6, 3.1], kind="Quadro", size=7.5, align=["c", "l", "l", "c", "l"],
             fonte_txt="qualidade-7-ferramentas-fieldops.md, seção 6. Responsáveis e prazos são propostas a confirmar.", key="acoesq")


# =====================================================================================  RISCOS
def riscos(r):
    n = r.N
    c = n['riscos']
    r.h1(f"{c} GERENCIAMENTO DOS RISCOS")
    r.par("O gerenciamento de riscos segue os seis processos da disciplina (planejar, identificar, analisar qualitativamente, analisar quantitativamente, planejar respostas e controlar). O registro tem **22 ameaças (R01 a R22) e 4 oportunidades (O01 a O04)**. Cada risco é escrito como causa, risco e consequência, com gatilho, pacote da EAP, dono e resposta. Probabilidades, impactos, horas e custos de resposta são **estimativas do gerente**, sem base estatística; os dados do GitHub citados são de 18/11/2026.")
    r.h2(f"{c}.1 Método, escalas e critérios")
    r.par("A probabilidade usa cinco níveis (0,1 muito baixa a 0,9 muito alta; riscos já ocorridos recebem 0,9). O impacto usa os níveis de 0,05 a 0,80 da disciplina, em quatro objetivos, com condições próprias do FieldOps: **custo** (referência: custo base de R$ 47.714,83, de menos de 2% a 40% ou mais), **tempo** (80 dias úteis, de menos de 1 dia a 16 dias ou mais), **escopo** (ligado à ordem de corte: os itens 1 e 2 afetam áreas secundárias, os itens 3 e 4 áreas principais e o núcleo é 0,40 ou 0,80) e **qualidade** (ligada à severidade do DoD: defeito baixo a crítico). Custo e tempo são calculados pelo script das horas e dos dias estimados de cada risco; escopo e qualidade são atribuídos pelo gerente.")
    r.par("A **severidade** é a probabilidade multiplicada pelo impacto médio dos quatro objetivos, e define a prioridade no ranking. Como a média dilui riscos com um impacto muito alto e os demais baixos (perda de dados: qualidade 0,80 e custo 0,10), a severidade máxima (probabilidade × maior impacto) é usada como regra da lista de observação (≥ 0,24). As classes são: **Alta** (≥ 0,15: resposta ativa, dono nomeado e revisão a cada 48 h na S8), **Média** (0,05 a menos de 0,15: revisão semanal) e **Baixa** (< 0,05: monitorar).")
    r.par("A estrutura analítica dos riscos (RBS) tem quatro categorias: técnico (offline e sincronização R06, R11 e R21; integração e contrato R07, R14, R22 e O01; Android R08; segurança R09; ambiente e dependências R13, R17 e O02), gerenciamento (prazo e capacidade R01 e R02; pessoas R03, R04 e R05; comunicação e medição R16), requisitos e qualidade (escopo R10, R18 e O04; qualidade de processo R15, R19 e R20) e externo (provedores R12; instituição e docentes O03). Não há reserva de prazo: o prazo é fixo em 16 semanas, e a reserva de escopo é a ordem de corte (RJ07). O custo do processo de risco (R$ 1.760, uma reunião semanal de 20 minutos) está dentro das horas do pacote 1.2.")
    r.h2(f"{c}.2 Análise qualitativa e priorização")
    r.par("Dos 22 riscos, **5 têm classe Alta, 13 Média e 4 Baixa**, e 7 entram na lista de observação. Os cinco maiores são R06 (falha de sincronização offline, 0,262), R03 (backend sem responsável, 0,248), R02 (backlog acima da capacidade, 0,225), R14 (integração tardia entre app, web e API, 0,193) e R04 (sobrecarga do gerente, 0,158). Os três primeiros se reforçam: a sincronização offline (RP03) ainda não existe nem no backend nem no app, 21 issues do backend estão sem responsável e restam apenas 6 dias úteis até o M8. A @F:calor@ mostra o mapa de calor e o @Q:rank@ traz o ranking completo.")
    r.figura("matriz_calor.png", "Matriz de calor de probabilidade × impacto médio dos 22 riscos", 13.5, altura_max_cm=11.0, key="calor",
             fonte_txt="analise-riscos-fieldops.md (figura 1). Cada ponto está na probabilidade do risco e no seu impacto médio exato; a cor de fundo é a classe de severidade.")
    linhas = []
    fills = {}
    cor = {"Alta": "F4C7C3", "Média": "FBE9B7", "Baixa": "CFE8D5"}
    for i, q in enumerate(sorted(F.QUALI.values(), key=lambda x: x["prio"]), 1):
        rid = q["id"]
        rp = F.RESP[rid]
        st = [x for x in F.RISCOS if x["id"] == rid][0]["status"].split(":")[0]
        st = "Materializado" if st.startswith("Materializado") and "parcial" not in st else ("Materializado parcialmente" if "parcial" in st else "Ativo")
        linhas.append([str(q["prio"]), rid, q["nome"], f"{q['p']:.1f}".replace(".", ","), f"{q['media']:.3f}".replace(".", ","), f"{q['sev']:.3f}".replace(".", ","), q["classe"], rp["abord"], rp["dono"], st])
        fills[(i, 6)] = cor[q["classe"]]
    r.tabela("Ranking dos riscos por severidade (probabilidade × impacto médio), classe, resposta, dono e situação", ["#", "ID", "Risco", "Prob.", "Impacto médio", "Severidade", "Classe", "Resposta", "Dono", "Situação em 18/11"], linhas,
             [0.7, 1.0, 4.6, 1.0, 1.4, 1.5, 1.3, 1.5, 1.0, 2.5], kind="Tabela", size=7.5, align=["c", "c", "l", "c", "c", "c", "c", "c", "c", "l"], cell_fills=fills,
             fonte_txt="analise-riscos-fieldops.md, seções 4 e 5.1 (estimativas do gerente). Registro completo (causa, risco e consequência, gatilho e inclusão): Apêndice E.", key="rank")
    r.h2(f"{c}.3 Respostas, responsáveis e ações")
    r.par("O gerente escolheu **mitigar** na maioria dos casos (19 dos 22), porque os riscos vêm do próprio trabalho de desenvolvimento e não há a quem transferi-los; evitar foi escolhido para R10 (escopo ampliado indevidamente), transferir para R12 (limites de provedores gratuitos, com o custo transferido ao provedor) e aceitar para R11 (complexidade do construtor de modelos, com monitoramento). Nenhuma resposta depende de dinheiro: a contingência real é a **ordem de corte do RJ07** e a redistribuição de pessoas. O @Q:resp@ mostra as respostas dos riscos de classe Alta, mais R20 e R10, com a ação preventiva, a ação contingencial, o prazo, o custo em horas valoradas e o risco residual; as respostas dos 22 riscos estão no Apêndice E.")
    linhas = []
    for rid in ["R06", "R03", "R02", "R14", "R04", "R20", "R10"]:
        rp = F.RESP[rid]
        linhas.append([f"{rid} ({rp['dono']})", rp["resp"], rp["contingencia"], rp["prazo"], rp["custo"], rp["residual"]])
    r.tabela("Respostas aos principais riscos: ação preventiva, contingência, prazo, custo e risco residual", ["Risco (dono)", "Ação preventiva", "Ação contingencial", "Prazo", "Custo", "Risco residual"], linhas, [1.8, 5.2, 4.2, 1.5, 1.2, 2.1], kind="Quadro", size=7.5,
             fonte_txt="analise-riscos-fieldops.md, seções 5.1 e 5.2. Custo da resposta = horas adicionais × taxa; estimativa do gerente. Responsáveis e prazos: proposta a confirmar.", key="resp")
    r.par("As respostas custam **R$ 6.815** em horas adicionais (14,3% do custo base); as dos cinco riscos de classe Alta custam R$ 2.460. As oportunidades (@Q:oport@) são respondidas por **explorar** (O01, mocks gerados do contrato OpenAPI), **melhorar** (O02, assistência de IA para código repetitivo, sempre com revisão humana), **compartilhar** (O03, revisão docente antecipada do contrato de sincronização) e **aceitar** (O04, pontos extras por diferenciais depois do MVP estável). Elas custam R$ 570 e têm benefício esperado de R$ 1.647 em horas poupadas, que é tratado como folga e não abate a reserva, porque horas poupadas só rendem se forem realocadas ao núcleo.")
    lin = []
    for x in F.OPORT:
        txt = x[1].replace("\n", " ")
        opo = txt.split("Oportunidade:")[1].split("Benefício:")[0].strip() if "Oportunidade:" in txt else txt
        lin.append([x[0], opo, x[3], x[8], x[9]])
    r.tabela("Oportunidades (riscos positivos): descrição, probabilidade, valor esperado e gatilho", ["ID", "Oportunidade", "Prob.", "Valor (P × média)", "Inclusão"], lin, [1.0, 9.2, 1.2, 2.4, 2.2], kind="Quadro", size=8, align=["c", "l", "c", "c", "c"],
             fonte_txt="analise-riscos-fieldops.md, seção 5.3. Respostas e custos das oportunidades: Apêndice E.", key="oport")
    r.h2(f"{c}.4 Análise quantitativa e reservas")
    r.par("O valor monetário esperado (EMV) é a probabilidade multiplicada pelo custo se o risco ocorrer (horas extras × taxa mais caixa). O EMV de todas as ameaças é de R$ 13.655 (28,6% do custo base), limite superior que soma riscos correlacionados. Separando por situação, o EMV dos riscos **já materializados** é de R$ 7.020 e entra no custo real (variação), e não na reserva; o dos riscos **que ainda podem ocorrer** é de R$ 6.635 (13,9% do custo base), e é o que se compara com a reserva. A simulação de Monte Carlo (20.000 rodadas, semente 42, cada risco ainda não materializado ocorrendo com sua probabilidade e custando de 0,5 a 2 vezes o valor estimado) dá custo extra médio de R$ 7.768, P80 de R$ 9.812 e P90 de R$ 10.782, com 89% de probabilidade de ultrapassar a contingência de 10% e 60% de ultrapassar as duas reservas somadas.")
    cmp_ = [
        ["Contingência de 10% (linha O51)", rs(F.CONTING), "dentro da linha de base; liberada pelo gerente"],
        ["Reserva gerencial de 5% (linha O52)", rs(F.GERENCIAL), "só o PI-01 libera"],
        ["Soma das duas reservas", rs(F.CONTING + F.GERENCIAL), "15,0% do custo base"],
        ["EMV dos riscos que ainda podem ocorrer", "R$ 6.635,00", "déficit de R$ 1.864 contra a contingência de 10%; as duas reservas cobrem 108%"],
        ["Monte Carlo: P80 do custo extra", "R$ 9.812,00", "20,6% do custo base, contra 15,0% das reservas"],
        ["Respostas planejadas (22 ameaças)", "R$ 6.815,00", "143% da contingência; as dos 12 primeiros do ranking cabem nela (R$ 2.145 dependeriam da reserva gerencial)"],
    ]
    r.tabela("Reservas e riscos: comparação das medidas quantitativas", ["Medida", "Valor", "Leitura"], cmp_, [5.5, 2.6, 7.9], kind="Quadro", size=8.5, align=["l", "r", "l"], fonte_txt="analise-riscos-fieldops.md, seção 6; orcamento-fieldops.md.", key="reservas")
    r.par("A conclusão é a mesma do orçamento: a contingência de 10% cobre as respostas aos riscos mais graves, mas o EMV e o P80 passam dela, e as horas são fixas (960 h) e não se compram. O que passar da contingência vira **corte de escopo pela ordem do RJ07**, ou pedido de reserva gerencial à coordenação. No prazo, os atrasos esperados não se somam (as causas de R02, R03, R04 e R14 se sobrepõem), mas **cinco riscos, se ocorrerem, consomem mais dias úteis do que restam (6)**: R02, R03, R04, R05 e R14. Com folga zero, qualquer atraso adicional se converte em corte de escopo, e não em extensão do prazo. A simulação trata só custo e sorteia os riscos de forma independente, o que subestima a variância de eventos correlacionados.")
    r.h2(f"{c}.5 Acompanhamento dos riscos")
    r.par("Os riscos são revisados a cada sprint (S1 a S7), em reunião semanal de 20 minutos conduzida pelo gerente e, na S8, a cada 48 horas para os de classe Alta e da lista de observação (19/11, 23/11, 25/11 e 27/11; 20/11 é feriado). A pauta é fixa: fatos novos com dados do GitHub (2 min), lista de observação (10 min), riscos novos ou alterados (5 min) e riscos a encerrar e escalonamento (3 min). A saída é o registro atualizado e uma linha no relatório de status. Os indicadores e os gatilhos usados no acompanhamento (issues sem responsável, ponto abaixo do limite no gráfico p, pull requests sem revisão, CI vermelho, cenários do AC-SYNC, fluxo ponta a ponta, dias sem commit por camada, issues P1 em andamento e fila do EAS) estão integrados ao quadro de indicadores do capítulo %d. Um risco novo entra por uma issue com o rótulo risco, escrita como causa, risco e consequência, e o gerente atribui probabilidade, impacto, dono e resposta em até 2 dias úteis." % n['monit'])
    r.par("A lista de observação tem sete riscos: os cinco de classe Alta e dois com severidade máxima de 0,24 ou mais (R20 e R21). O escalonamento é por regra: gatilho disparado em risco Alta, aviso a FM e ao dono no mesmo dia; risco que afeta um marco (impacto em prazo ou escopo de 0,40 ou mais) ou ação sem avanço por 2 dias, aviso ao PI-02 e ao PI-03 em 24 h com proposta de corte; materialização com impacto de qualidade 0,80 (perda de dados, duplicidade grave) ou em segurança, aviso ao PI-02 e ao PI-01 em 24 h com plano de contenção; uso de reserva, registro no relatório de status e aviso ao PI-02 antes de gastar.")
    r.h2(f"{c}.6 Riscos já materializados em 18/11/2026")
    r.par("O resumo do documento de riscos conta **9 riscos já materializados** (R01, R02, R03, R04, R10, R13, R15, R16 e R22); o registro marca também R11 como materializado em S3, mas entregue em 11/11 e hoje só com risco de regressão. O desvio de prazo é real e é tratado como situação monitorada, com as ações do @Q:mat@.")
    cab, rows = DD.tabela_generica("risco", "## 8. Riscos já materializados")
    rows = [[x[0], x[1], x[2], x[3], x[5]] for x in rows]
    r.tabela("Riscos materializados: evidência, efeito já visto e dono", ["ID", "Risco que ocorreu", "Evidência em 18/11/2026", "Efeito já visto", "Dono"], rows, [1.0, 3.0, 5.6, 4.4, 1.2], kind="Quadro", size=7.5, fonte_txt="analise-riscos-fieldops.md, seção 8. A ação em curso de cada risco está na coluna Ação do Apêndice E.", key="mat")
    r.par("A ordem de corte a aplicar já, segundo o documento de riscos, tem os itens 1 e 2 (remover o dashboard avançado e as issues P1; limitar os tipos de resposta) liberando horas de imediato, e os itens 3 a 5 só se o ensaio do AC-SYNC em 24/11 falhar. O cronograma, por sua vez, recomenda aplicar os seis cortes já (seção %d.7). As duas leituras convivem: os itens 1 e 2 são consenso, e a decisão sobre 3 a 5 depende do resultado do ensaio e da decisão do comitê sobre o re-baseline." % n['crono'])
