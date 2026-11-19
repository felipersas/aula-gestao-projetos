# -*- coding: utf-8 -*-
"""Consideracoes finais, referencias e apendices."""
import dados as DD
import fatos as F
from fatos import br, rs, pct
from cap_a2 import faixa_marcos
from rel_lib import LEFT

REFS = [
    "CARVALHO, Fábio Câmara Araújo de. **Gestão de projetos**. 2. ed. São Paulo: Pearson, 2018. E-book.",
    "CRUZ, Fábio. **Scrum e PMBOK unidos no gerenciamento de projetos**. Rio de Janeiro: Brasport, 2013. E-book.",
    "FINOCCHIO JÚNIOR, José. **Project model canvas**: gerenciamento de projetos sem burocracia. Rio de Janeiro: Elsevier, 2013.",
    "FIELDOPS-PROJECT. **Repositórios docs, backend, frontend e app**. Organização FieldOps-Project no GitHub. Issues, pull requests, commits e execuções de CI. Acesso em: 18 nov. 2026.",
    "PROJECT MANAGEMENT INSTITUTE. **Um guia do conhecimento em gerenciamento de projetos (Guia PMBOK)**. 5. ed. Newtown Square: Project Management Institute, 2013.",
    "SCHWABER, Ken; SUTHERLAND, Jeff. **O Guia do Scrum**: o guia definitivo para o Scrum: as regras do jogo. [S. l.]: Scrum Guides, nov. 2020. Versão em português.",
    "SOUZA, Carla Patricia da Silva. **Gestão de projetos**. 1. ed. São Paulo: Contentus, 2020. E-book.",
    "SUTHERLAND, Jeffrey Victor. **Scrum**: a arte de fazer o dobro do trabalho na metade do tempo. 2. ed. rev. São Paulo: LeYa, 2016.",
    "TAKATU, Deivison S. **Gestão de Projetos**: material das aulas e atividades da disciplina. Sorocaba: Centro Universitário SENAI São Paulo (UniSENAI-SP), 2026. Material de ensino.",
    "TODESCO, Glauco. **Projeto FieldOps**: especificação do produto (visão, objetivos, regras de negócio, arquitetura, backlog, critérios de aceitação, Definição de Pronto e critérios de avaliação). Notion. Disponível em: https://glaucotodesco.notion.site/Projeto-FieldOps-3af5d52a81f580c0b92ec261c686abb4. Acesso em: 18 nov. 2026.",
]


def referencias(r, n):
    r.h1(f"{n['refs']} REFERÊNCIAS")
    for x in REFS:
        r.par(x, first=None, line=1.0, after=12, align=LEFT)


def consideracoes(r):
    n = r.N
    c = n['final']
    r.h1(f"{c} CONSIDERAÇÕES FINAIS")
    r.par("Este relatório consolidou o planejamento integrado do FieldOps em 18/11/2026, na semana 15 de 16. Ele mostra um planejamento coerente entre as áreas e um projeto que não o está cumprindo: o mesmo conjunto de números (967 h, 36 pacotes, R$ 52.486,31 de linha de base, 22 riscos) sustenta a linha de base e sustenta o diagnóstico do atraso. As seções abaixo ligam os resultados aos objetivos do TAP, dizem o que o planejamento revelou, assumem as limitações e indicam os próximos passos.")
    r.h2(f"{c}.1 Resultados frente aos objetivos do TAP")
    r.par("O @Q:objet@ confronta cada objetivo específico do TAP com o que o planejamento e o monitoramento mostram. O percentual realizado é a estimativa por pacote, ponderada por horas, do cronograma (premissa P7), e não uma medição.")
    rp = lambda *cods: ", ".join(f"{c} ({F.real_pkg(c)}%)" for c in cods)
    ob = [
        ["OE1. Modelos de checklist versionados (RP05)", rp("3.3", "4.3"), "parcial: API de modelos concluída (A17), publicação com snapshot (A22) e construtor (A18) incompletos"],
        ["OE2. Execução offline com sincronização idempotente (RP02, RP03)", rp("5.6", "3.6", "5.7"), "não atingido: M6 não atingido; é o item de maior risco (R06)"],
        ["OE3. Visibilidade para o supervisor (RP04, RP08)", rp("4.4", "4.5"), "parcial: acompanhamento e galeria de evidências concluídos; agendamento incompleto"],
        ["OE4. Cadastros e autorização por perfil na API (RP06, RP07)", rp("3.1", "3.2", "4.1", "4.2"), "atendido: M2 atingido por inteiro (17 de 17 issues)"],
        ["OE5. Fluxo formal de revisão, aprovação e auditoria (RP09, RP10)", rp("3.7", "4.6", "5.7"), "não atingido: M7 não atingido (2 de 14)"],
        ["OE6. Demonstrar o fluxo completo no M8 e cumprir M1 a M8 (RJ02)", "M2 atingido; M1, M3 e M4 com pendências; M5 a M7 não atingidos", "em risco alto: depende da decisão do re-baseline (SM-03)"],
    ]
    r.tabela("Objetivos específicos do TAP, avanço estimado dos pacotes e situação em 18/11/2026", ["Objetivo específico", "Pacotes (avanço estimado)", "Situação"], ob, [5.4, 4.6, 6.0], kind="Quadro", size=8.5,
             fonte_txt="tap-fieldops.md (objetivos); cronograma-fieldops.md (acompanhamento por atividade, percentual estimado).", key="objet")
    r.par("O balanço é desigual. A parte do produto que depende de padrão conhecido (autenticação, cadastros, painel e execução online) está entregue ou perto disso; a parte que define o produto, que é a operação offline com sincronização idempotente e o fluxo de revisão, não está. É o desfecho previsto pelo próprio planejamento: o orçamento classificou offline e sincronização como o maior fator de incerteza, e o registro de riscos deu a R06 a maior severidade. O que o planejamento não evitou foi a convergência dos riscos de prazo, pessoas e processo no mesmo ponto.")
    r.h2(f"{c}.2 O que o planejamento mostrou")
    r.par("**Primeiro, a integração entre as áreas explica o atraso.** O caminho crítico é uma corrente sem folga de 20 atividades quase toda do backend; o backend é o repositório mais atrasado, com 21 issues sem dono; a sincronização é classe D no orçamento, R06 nos riscos e M6, o marco de maior peso, na avaliação. As cinco áreas apontam para o mesmo lugar, e foi essa convergência que permitiu dizer que o atraso é causa especial (S6 e S7 abaixo do limite de controle) e não acaso.")
    r.par("**Segundo, o orçamento é um orçamento de capacidade.** O projeto não tem verba a gastar: o custo de R$ 54.872,05 é esforço valorado, e a reserva financeira não compra horas. Por isso o EAC de R$ 79.416,81 não é um pedido de dinheiro, e sim a medida de quanto trabalho falta, e por isso a resposta a desvio é escopo e prazo.")
    r.par("**Terceiro, a ordem de corte é um instrumento pequeno diante do déficit.** Os seis cortes liberam cerca de 22 h contra 498 h por fazer; só um re-baseline de prazo e de escopo do marco final fecha a conta, e essa decisão é do comitê, e não do gerente. O planejamento já continha a ordem de corte, mas não continha o plano para o caso em que ela não bastasse: esse foi o principal acréscimo do capítulo de monitoramento.")
    r.par("**Quarto, medir é parte do controle.** Sem apontamento de horas, sem rótulo de defeito e com issues fechadas em lote, 12 dos 17 indicadores estão em vermelho, mas 2 não podem ser lidos. O planejamento obriga a medir o que se promete controlar.")
    r.h2(f"{c}.3 Limitações do trabalho")
    r.alineas([
        "**dados estimados:** durações, horas por atividade, taxas horárias, preços de serviços, probabilidades e impactos de risco são estimativas ou hipóteses de valoração; o TAP declara que o projeto não tem investimento financeiro direto",
        "**status por atividade calibrado:** o GitHub informa issues por sprint, e o percentual de cada atividade foi calibrado para reproduzir essa razão (diferença máxima de 0,6 ponto percentual); SPI e CPI por valor agregado herdam essa estimativa, e o custo real é presumido (12 h por semana por pessoa), porque não há apontamento de horas",
        "**papéis inferidos:** os papéis dos integrantes foram inferidos de commits e issues, e o R e o A por pacote são proposta do gerente; nenhum deles foi confirmado pelo grupo ou pelos professores",
        "**avaliações do gerente:** as notas de poder e interesse, os níveis de engajamento, as metas de qualidade, os pesos de severidade do Pareto e as alçadas de decisão do capítulo %d não foram validados com as partes interessadas" % n['monit'],
        "**revisão fora do GitHub:** a medida de revisão registrada só enxerga a plataforma; revisões por chat ou presenciais não aparecem, e o número de 11% não é um juízo sobre as pessoas",
        "**fotografias diferentes do mesmo dia:** os documentos de gestão usam 57 de 103 issues, e a análise de qualidade, coletada depois, 59 de 103; a diferença é de duas issues do frontend",
        "**personas e comunicação:** os usuários finais são personas fictícias, e os canais de comunicação (WhatsApp, e-mail, videochamada) e as pastas do repositório docs são premissa",
        "**escopo do relatório:** o trabalho descreve planejamento e monitoramento; não avalia a qualidade do código do produto além dos metadados do GitHub",
    ])
    r.h2(f"{c}.4 Próximos passos")
    r.par("Em ordem de prazo: (1) até 19/11, decidir com o comitê o re-baseline do M8 e a aplicação dos cortes 1 a 6, atribuir as 21 issues do backend, proteger a `develop` e fechar o contrato de sincronização e o ADR da stack; (2) até 24/11, fechar o ciclo offline → online e ensaiar o AC-SYNC; (3) em 24/11 e 26/11, ensaiar duas vezes o AC-RELEASE; (4) a partir de 23/11, implantar o apontamento de horas e confirmar com o grupo o percentual por atividade, para substituir as hipóteses do EVM; (5) até 27/11, ou na nova data do M8, executar o checklist de encerramento e consolidar as lições aprendidas; (6) depois do projeto, usar este planejamento como base de comparação com o realizado, calculando o EVM final com horas reais, e preservar os repositórios e os artefatos. Os pontos que dependem de confirmação do grupo e do orientador, como os papéis, as alçadas e o re-baseline, devem ser tratados antes da apresentação final.")


# ====================================================================================  APENDICES
def apendices(r):
    n = r.N
    r.h1(f"{n['apend']} APÊNDICES E ANEXOS")
    r.par("Os apêndices trazem os artefatos completos, em tabelas longas, que o corpo do relatório resume. Todos são tabelas geradas dos arquivos do repositório da disciplina, e conferidas por script contra os totais-chave (71 itens e 967 h do cronograma; 52 itens e R$ 54.872,05 do orçamento; 36 pacotes do RACI; 22 riscos e 4 oportunidades; 14 aquisições; 19 comunicações).")
    idx = [
        ["A", "Cronograma completo (71 itens)", "cronograma-fieldops.md"], ["B", "Orçamento por três pontos (52 itens)", "orcamento-fieldops.md"],
        ["C", "Matriz RACI (36 pacotes)", "organograma-raci-fieldops.md"], ["D", "Dicionário da EAP (7 entregas e 36 pacotes)", "eap-fieldops.md"],
        ["E", "Registro de riscos (22 ameaças e 4 oportunidades) e respostas", "analise-riscos-fieldops.md"], ["F", "Tabela de aquisições (14 itens)", "aquisicoes-fieldops.md"],
        ["G", "Plano de comunicação: momento e formato; gatilhos de escalonamento", "plano-comunicacao-fieldops.md"], ["H", "Matriz de rastreabilidade por pacote", "gerada dos artefatos anteriores"],
        ["I", "Premissas consolidadas", "todos os artefatos"], ["J", "Figuras complementares da análise de qualidade", "qualidade-7-ferramentas-fieldops.md"],
        ["K", "Índice dos artefatos no repositório", "—"],
    ]
    r.tabela("Apêndices e artefato de origem", ["Apêndice", "Conteúdo", "Origem"], idx, [2, 9, 5], kind="Quadro", size=9, align=["c", "l", "l"], key="idxapend")
    # ------------- A: cronograma
    r.secao_paisagem()
    r.h2("Apêndice A – Cronograma completo (71 itens)", quebra=False)
    cronograma_tabela(r, com_status=True)
    r.h2("Apêndice B – Orçamento por três pontos (52 itens)", quebra=True)
    orcamento_tabela(r)
    r.h2("Apêndice C – Matriz RACI (36 pacotes)", quebra=True)
    raci_tabela(r)
    r.h2("Apêndice D – Dicionário da EAP", quebra=True)
    dicionario(r)
    r.h2("Apêndice E – Registro de riscos e respostas", quebra=True)
    riscos_tabelas(r)
    r.h2("Apêndice F – Tabela de aquisições (14 itens)", quebra=True)
    aquisicoes_tabela(r)
    r.h2("Apêndice G – Plano de comunicação: momento, formato e gatilhos de escalonamento", quebra=True)
    comunicacao_tabelas(r)
    r.h2("Apêndice H – Matriz de rastreabilidade por pacote", quebra=True)
    rastreab_pacote(r)
    r.secao_retrato()
    r.h2("Apêndice I – Premissas consolidadas", quebra=False)
    premissas(r)
    r.secao_paisagem()
    r.h2("Apêndice J – Figuras complementares da análise de qualidade", quebra=False)
    r.figura("fluxograma_qualidade.png", "Fluxograma de qualidade: entrega (A) e tratamento de não conformidade (B)", 17.0, altura_max_cm=11.6, key="fluxq",
             fonte_txt="qualidade-7-ferramentas-fieldops.md (figura 2). Portões da entrega: CI verde, revisão por outra pessoa e demonstração contra os critérios de aceitação.")
    r.figura("folha_verificacao.png", "Folha de verificação do DoD em 55 pull requests", 24.0, altura_max_cm=11.0, key="folha",
             fonte_txt="qualidade-7-ferramentas-fieldops.md (figura 3). Verde: conforme; vermelho: não conforme; cinza: não se aplica ou PR sem checklist.")
    r.figura("histograma.png", "Histogramas do tamanho do pull request e do tempo até o merge", 21.0, altura_max_cm=7.2, key="histo",
             fonte_txt="qualidade-7-ferramentas-fieldops.md (figura 5). Tamanho sem arquivos de lockfile; tempo em escala logarítmica.")
    r.figura("dispersao.png", "Diagramas de dispersão: tamanho do PR, tempo até o merge, DoD marcado e issues planejadas × concluídas", 22.0, altura_max_cm=6.6, key="disp",
             fonte_txt="qualidade-7-ferramentas-fieldops.md (figura 7). r de Pearson: (a) 0,06, (b) -0,07, (c) 0,67 (n = 7, não significativo).")
    r.secao_retrato()
    r.h2("Apêndice K – Índice dos artefatos no repositório", quebra=False)
    indice_artefatos(r)


def cronograma_tabela(r, com_status=True, baseline=False):
    cab = ["ID", "EAP", "Atividade", "Início", "Término", "Dur.", "Resp.", "Predecessoras (tipo)", "Esf. (h)", "Sprint", "CC"] + (["Status em 18/11"] if com_status else [])
    linhas, bold = [], []
    for i, a in enumerate(F.CRONO):
        nome = a["nome"]
        row = [a["id"], a["wbs"], nome, a["ini"], a["fim"], a["dur"].replace(" du", ""), a["resp"], a["pred"], "" if a["marco"] else str(a["esf"]), a["sprint"], "sim" if a["critica"] else ""]
        if com_status:
            row.append(a["status"])
        linhas.append(row)
        if a["marco"]:
            bold.append(i)
    rel = [0.9, 0.9, 6.3, 1.3, 1.4, 0.8, 0.9, 4.4, 0.9, 1.1, 0.8] + ([2.8] if com_status else [])
    fills = {i + 1: "E7ECEF" for i in bold}
    r.tabela("Cronograma completo: 63 atividades e 8 marcos (datas de 2026; duração em dias úteis; CC = caminho crítico)", cab, linhas, rel, kind="Tabela", size=7, align=["c", "c", "l", "c", "c", "c", "c", "l", "r", "c", "c"] + (["l"] if com_status else []),
             bold_rows=tuple(bold), fills=fills, fonte_txt="cronograma-fieldops.md (versão 1.0, 18/11/2026). Total de esforço: 967 h. Os percentuais de status por atividade são estimativas do gerente (premissa P7).", key="apa")


def orcamento_tabela(r):
    cab = ["ID", "EAP", "Item", "Categoria", "Qtd.", "Un.", "Resp.", "cO (R$)", "cM (R$)", "cP (R$)", "Esperado PERT (R$)", "σ (R$)"]
    linhas = []
    f = lambda v: "—" if v is None else br(v)
    for o in F.ORC:
        linhas.append([o["id"], o["wbs"], o["item"], o["cat"], o["qtd"], o["un"], o["resp"], f(o["co"]), f(o["cm"]), f(o["cp"]), br(o["pert"]), f(o["sig"])])
    linhas.append(["", "", "Soma das 52 linhas (50 de custo e 2 reservas)", "", "", "", "", "38.927,50", "45.545,00", "65.181,50", br(F.CUSTO_TOTAL), "812,45"])
    r.tabela("Orçamento por estimativa de três pontos: 52 itens (mão de obra, custos diretos e reservas)", cab, linhas, [0.9, 0.9, 6.4, 2.1, 0.8, 1.6, 0.9, 1.5, 1.5, 1.5, 1.9, 1.2], kind="Tabela", size=7,
             align=["c", "c", "l", "l", "r", "l", "c", "r", "r", "r", "r", "r"], bold_rows=(52,), fonte_txt="orcamento-fieldops.md, seção (b). Valores hipotéticos de valoração; esperado = (cO + 4cM + cP) ÷ 6; σ = (cP − cO) ÷ 6; o σ total é √Σσ².", key="apb")


def raci_tabela(r):
    cab = ["Cód.", "Pacote de trabalho", "FM", "JV", "GR", "PD", "AF", "PI-01", "PI-02", "PI-03", "Critério de C e I"]
    linhas = []
    for x in F.RACI:
        p = x["papeis"]
        linhas.append([x["cod"], x["nome"]] + [p[k] if p[k] != "·" else "" for k in ["FM", "JV", "GR", "PD", "AF", "PI-01", "PI-02", "PI-03"]] + [x["crit"]])
    r.tabela("Matriz RACI dos 36 pacotes da EAP (R: responsável; A: aprovador; C: consultado; I: informado)", cab, linhas, [0.9, 5.4, 0.7, 0.7, 0.7, 0.7, 0.7, 0.9, 0.9, 0.9, 7.2], kind="Tabela", size=7,
             align=["c", "l"] + ["c"] * 8 + ["l"], fonte_txt="organograma-raci-fieldops.md, seção 3.3. Um A e ao menos um R por linha, verificado por script; A/R indica a mesma pessoa. R e A são proposta a confirmar com o grupo.", key="apc")


def dicionario(r):
    ent = DD.eap_entregas()
    linhas = []
    for k in "1234567":
        e = ent[k]
        linhas.append([f"{k}.0", e["nome"], e["req"], e["pbi"], e["criterio"]])
        for cod in F.PACOTES:
            if cod.startswith(k + "."):
                d = F.NOMES[cod]
                linhas.append([cod, d["nome"], d["req"], d["pbi"], d["criterio"]])
    bold = tuple(i for i, l in enumerate(linhas) if l[0].endswith(".0"))
    fills = {i + 1: "E7ECEF" for i in bold}
    r.tabela("Dicionário da EAP: elemento, requisitos, itens do backlog e critério de aceitação", ["Cód.", "Elemento", "Requisitos", "PBI / épico", "Critério de aceitação (resumo)"], linhas, [0.9, 6.0, 2.4, 2.6, 12.0], kind="Quadro", size=7, align=["c", "l", "l", "l", "l"],
             bold_rows=bold, fills=fills, fonte_txt="eap-fieldops.md, dicionário da EAP. A descrição completa de cada elemento está no arquivo de origem.", key="apd")


def riscos_tabelas(r):
    linhas = []
    for x in F.RISCOS:
        corpo = f"**Causa:** {x['causa']}\n**Risco:** {x['risco']}\n**Consequência:** {x['cons']}"
        linhas.append([x["id"], corpo, f"{x['tipo']} ({x['rbs']})", x["eap"], x["gatilho"], x["incl"], x["status"]])
    r.tabela("Registro de riscos: causa, risco e consequência, tipo, pacote da EAP, gatilho, inclusão e situação em 18/11/2026", ["ID", "Causa → risco → consequência", "Tipo (RBS)", "EAP", "Gatilho", "Inclusão", "Situação em 18/11/2026"], linhas,
             [0.9, 10.5, 1.8, 1.4, 3.6, 1.5, 4.4], kind="Quadro", size=6.5, align=["c", "l", "l", "l", "l", "c", "l"], fonte_txt="analise-riscos-fieldops.md, seção 3. Estimativas do gerente; estado de 18/11/2026.", key="ape1")
    linhas = []
    for rid in [x["id"] for x in F.RISCOS]:
        q = F.QUALI[rid]; rp = F.RESP[rid]
        linhas.append([rid, q["nome"], f"{q['p']:.1f}".replace(".", ","), f"{q['sev']:.3f}".replace(".", ","), q["classe"], rp["abord"], rp["resp"], rp["contingencia"], rp["prazo"], rp["custo"], rp["residual"], rp["secund"], rp["dono"]])
    r.tabela("Respostas aos riscos: abordagem, ação preventiva, ação contingencial, prazo, custo, risco residual, risco secundário e dono", ["ID", "Risco", "P", "Sev.", "Classe", "Abord.", "Ação preventiva", "Ação contingencial", "Prazo", "Custo", "Risco residual", "Risco secundário", "Dono"], linhas,
             [0.8, 2.4, 0.6, 0.9, 1.0, 1.1, 5.0, 4.0, 1.4, 1.2, 1.7, 2.8, 0.8], kind="Quadro", size=6, align=["c", "l", "c", "c", "c", "c", "l", "l", "c", "r", "l", "l", "c"],
             fonte_txt="analise-riscos-fieldops.md, seções 4, 5.1 e 5.2. Custo da resposta: horas adicionais × taxa (estimativa). Responsáveis e prazos: proposta a confirmar.", key="ape2")
    lin = []
    for x in F.OPORT:
        lin.append([x[0], x[1].replace("\n", " "), x[2], x[3], x[8], x[9], x[10]])
    r.tabela("Oportunidades: causa, oportunidade e benefício, probabilidade, valor esperado, inclusão e gatilho", ["ID", "Causa → oportunidade → benefício", "Tipo", "Prob.", "Valor", "Inclusão", "Gatilho"], lin, [0.9, 11.5, 1.6, 1.0, 1.2, 1.7, 5.0], kind="Quadro", size=6.5,
             align=["c", "l", "l", "c", "c", "c", "l"], fonte_txt="analise-riscos-fieldops.md, seção 5.3. Respostas: O01 explorar (PD, 21/11, R$ 270); O02 melhorar (GR, 21/11, R$ 180); O03 compartilhar (FM, 21/11, R$ 120); O04 aceitar (FM, 26/11, R$ 0).", key="ape3")


def aquisicoes_tabela(r):
    cab = ["ID", "EAP", "Item a ser adquirido", "Urgência", "Motivo da decisão de compra", "Fornecedores potenciais", "Qtde.", "Custo unit.", "Custo total (cM)", "Previsão de entrega", "Observações"]
    linhas = [[a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10]] for a in F.AQ]
    linhas.append(["", "", "Total mais provável (cM)", "", "", "", "", "", "R$ 1.070,00", "", "R$ 374,00 de caixa e R$ 696,00 não monetário"])
    r.tabela("Tabela de aquisições (formato da Aula 08)", cab, linhas, [0.8, 0.8, 3.3, 1.2, 4.0, 3.0, 1.2, 1.3, 1.5, 2.0, 4.4], kind="Quadro", size=6.3, align=["c", "c", "l", "c", "l", "l", "l", "r", "r", "l", "l"], bold_rows=(14,),
             fonte_txt="aquisicoes-fieldops.md. Valores hipotéticos; preços em US$ convertidos a US$ 1,00 = R$ 5,50; confirmar no site do fornecedor antes de contratar.", key="apf")


def comunicacao_tabelas(r):
    linhas = [[x["id"], x["mom"][0], x["mom"][1], x["mom"][2]] for x in F.COM]
    r.tabela("Plano de comunicação: momento de realização, formato do documento e saída", ["ID", "Momento de realização", "Formato do documento", "Saída e onde fica"], linhas, [1.3, 8.3, 7.8, 6.3], kind="Quadro", size=6.8, align=["c", "l", "l", "l"],
             fonte_txt="plano-comunicacao-fieldops.md, seção 3.", key="apg1")
    g = DD.gatilhos()
    r.tabela("Gatilhos de escalonamento (COM-11) e situação em 18/11/2026", ["#", "Gatilho", "Como medir", "Quem detecta", "Ação e prazo", "Destinatário", "Situação em 18/11/2026"], g, [0.7, 4.0, 3.3, 1.6, 5.0, 2.0, 6.5], kind="Quadro", size=6.8,
             align=["c", "l", "l", "l", "l", "l", "l"], fonte_txt="plano-comunicacao-fieldops.md, seção 7. Níveis: conversa na daily, decisão do FM com a equipe, orientador (PI-02), coordenação (PI-01).", key="apg2")


def rastreab_pacote(r):
    linhas = []
    for cod in F.PACOTES:
        d = F.NOMES[cod]
        linhas.append([cod, d["nome"], "/".join(F.papel(cod, "R")), "/".join(F.papel(cod, "A")), d["req"], ", ".join(F.ATIV_PKG[cod]), str(F.HORAS_PKG[cod]), br(F.CUSTO_PKG[cod]), ", ".join(F.RISCOS_PKG.get(cod, [])) or "—", faixa_marcos(F.marcos_pkg(cod)), f"{F.real_pkg(cod)}%"])
    linhas.append(["", "Total", "", "", "", "63 atividades", "967", br(F.CUSTO_BASE), "", "", ""])
    r.tabela("Rastreabilidade por pacote: responsável, aprovador, requisitos, atividades, horas, custo, riscos citados, marcos e avanço estimado", ["Pacote", "Nome", "R", "A", "Requisitos", "Atividades", "Horas", "Custo base (R$)", "Riscos (pacote citado)", "Marcos", "Real. (est.)"], linhas,
             [0.9, 6.4, 0.8, 1.1, 2.6, 3.4, 0.9, 1.8, 2.4, 1.7, 1.2], kind="Tabela", size=6.8, align=["c", "l", "c", "c", "l", "l", "r", "r", "l", "l", "r"], bold_rows=(36,),
             fonte_txt="Elaborado pelos autores (2026). Riscos: só os que citam o pacote pelo código completo (os que citam um ramo, como 3.x, aparecem na matriz por entrega). Custo: valor esperado PERT, sem reservas. Avanço: estimativa por atividade, ponderada por horas.", key="aph")


def premissas(r):
    pr = [
        ["Papéis dos integrantes", "inferidos dos repositórios (commits, issues, documentos)", "confirmação do grupo", "caract., crono., RACI"],
        ["R e A por pacote; C e I", "proposta do gerente", "confirmação do grupo e dos professores (PI-01 a PI-03 como A)", "RACI"],
        ["Dedicação de 12 h por semana", "960 h = 5 × 16 × 12", "apontamento de horas", "crono., custos"],
        ["Taxas de R$ 45/h e R$ 60/h; preços de serviços", "hipóteses de valoração (custo de oportunidade)", "confirmar preços no fornecedor", "custos"],
        ["Fatores de três pontos por classe", "julgamento do gerente por incerteza técnica", "comparar com horas reais no encerramento", "custos"],
        ["Percentual realizado por atividade (P7)", "estimativa calibrada pelas issues de cada sprint", "confirmação do grupo; apontamento", "crono., EVM"],
        ["Custo real (AC) de 18/11", "12 h por semana por pessoa × custo médio (hipótese)", "apontamento de horas", "custos, indicadores"],
        ["Economia dos cortes da ordem do RJ07", "estimativa do gerente (21,8 h)", "reestimar após decisão do comitê", "crono."],
        ["Notas de poder e interesse; níveis de engajamento", "avaliação do gerente", "validar com o orientador", "partes interessadas"],
        ["Canais (WhatsApp, e-mail, videochamada), horários, pastas do repositório docs", "premissas do plano de comunicação", "confirmação do grupo", "comunicação"],
        ["Probabilidades, impactos, horas e custos de resposta dos riscos", "estimativas do gerente", "revisão a cada sprint", "riscos"],
        ["Metas de qualidade e pesos de severidade do Pareto", "propostas do gerente", "confirmação do grupo", "qualidade"],
        ["Indicadores, limiares próprios e alçadas de mudança", "propostas deste relatório (limiares de SPI, CPI, sprint e severidade vêm dos artefatos)", "confirmação do orientador e da coordenação", "monitoramento"],
        ["Datas de encerramento após 27/11 (cancelamentos, acessos)", "premissa", "confirmação do gerente", "monitoramento"],
    ]
    r.tabela("Premissas consolidadas, origem, forma de validação e onde são usadas", ["Premissa", "Origem", "Como validar", "Usada em"], pr, [5.2, 5.0, 4.0, 2.2], kind="Quadro", size=8, fonte_txt="Elaborado pelos autores (2026), a partir das premissas rotuladas nos artefatos.", key="api")


ARTEFATOS = [
    ["Termo de abertura (TAP) do FieldOps e do sistema EASY", "aula-02-integracao/tap-fieldops.md, tap-fieldops.docx (e tap-pii-easy)", "capítulo 4"],
    ["Declaração de escopo, EAP e dicionário (+ imagem)", "aula-03-escopo/eap-fieldops.md, eap-fieldops.png", "capítulo 6; Apêndice D"],
    ["Cronograma (+ Gantt)", "aula-04-tempo/cronograma-fieldops.md, gantt-fieldops.png", "capítulo 7; Apêndice A"],
    ["Orçamento por três pontos (+ curva S e custo por entrega)", "aula-05-custos-qualidade/orcamento-fieldops.md, curva-s-orcamento-fieldops.png, orcamento-por-entrega-fieldops.png", "capítulo 8; Apêndice B"],
    ["Análise da qualidade com as sete ferramentas (+ 9 imagens, dados e scripts)", "aula-05-custos-qualidade/qualidade-7-ferramentas-fieldops.md, 01-ishikawa.png a 07-dispersao.png, dados/, scripts/", "capítulo 9; Apêndice J"],
    ["Organograma e matriz RACI", "aula-06-rh-comunicacoes/organograma-raci-fieldops.md, organograma-fieldops.png", "capítulo 7; Apêndice C"],
    ["Plano de comunicação", "aula-06-rh-comunicacoes/plano-comunicacao-fieldops.md", "capítulo 5; Apêndice G"],
    ["Análise de riscos (+ matriz de calor, dados e scripts)", "aula-07-riscos/analise-riscos-fieldops.md, matriz-calor.png, dados/, scripts/", "capítulo 10; Apêndice E"],
    ["Aquisições", "aula-08-aquisicoes-partes-interessadas/aquisicoes-fieldops.md", "capítulo 8; Apêndice F"],
    ["Matriz de poder e interesse (+ imagem)", "aula-08-aquisicoes-partes-interessadas/matriz-poder-interesse-fieldops.md, matriz-poder-interesse-fieldops.png", "capítulo 5"],
    ["Base de fatos e plano de entrega", "_base/00-base-fieldops.md, _base/01-plano-de-entrega.md", "fonte única de códigos, datas e status"],
    ["Relatório final e documento parcial (este trabalho)", "projeto-fieldops/avaliacao-2-relatorio-final.docx, avaliacao-1-documento-parcial.docx, scripts/ e img/", "—"],
]


def indice_artefatos(r, av2=True):
    r.par("Os caminhos são relativos à pasta entrega/ do repositório da disciplina. Cada artefato foi escrito em um arquivo Markdown próprio, e o relatório os consolida e revisa; em caso de dúvida sobre um número, vale o arquivo de origem, com data-base de 18/11/2026.", first=None, line=1.15)
    rows = ARTEFATOS if av2 else ARTEFATOS_AV1
    r.tabela("Artefatos de planejamento e arquivos no repositório", ["Artefato", "Arquivo no repositório", "Neste " + ("relatório" if av2 else "documento")], rows, [4.5, 8.0, 3.5], kind="Quadro", size=8, key="apk")


ARTEFATOS_AV1 = [
    ["Termo de abertura (TAP)", "aula-02-integracao/tap-fieldops.md, tap-fieldops.docx", "capítulo 2"],
    ["Registro e matriz de partes interessadas (+ imagem)", "aula-08-aquisicoes-partes-interessadas/matriz-poder-interesse-fieldops.md, matriz-poder-interesse-fieldops.png", "capítulo 3"],
    ["Plano de comunicação", "aula-06-rh-comunicacoes/plano-comunicacao-fieldops.md", "capítulo 3"],
    ["Declaração de escopo e EAP (+ imagem)", "aula-03-escopo/eap-fieldops.md, eap-fieldops.png", "capítulo 4"],
    ["Cronograma inicial (+ Gantt)", "aula-04-tempo/cronograma-fieldops.md, gantt-fieldops.png", "capítulo 5; Apêndice A"],
    ["Matriz de responsabilidades (organograma e RACI)", "aula-06-rh-comunicacoes/organograma-raci-fieldops.md, organograma-fieldops.png", "capítulo 5; Apêndice B"],
    ["Base de fatos (códigos, datas, equipe)", "_base/00-base-fieldops.md", "fonte única dos artefatos"],
]
