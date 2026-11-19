# Análise da Qualidade do FieldOps com as Sete Ferramentas Básicas

| Campo | Informação |
|---|---|
| Projeto | FieldOps — Plataforma de Inspeção em Campo (MVP) |
| Instituição / curso | UniSENAI-SP Campus Sorocaba — Análise e Desenvolvimento de Sistemas |
| Disciplina / orientador | Gestão de Projetos — Prof. Me. Deivison S. Takatu |
| Atividade | Aula 05 — Custos e Qualidade (atividade de Qualidade) |
| Gerente do projeto | Felipe Marques (FM) |
| Data-base da análise | 18/11/2026 (semana 15, sprint S8) |
| Versão | 1.0 |
| Coleta dos dados | `{{coleta_utc}}` (UTC), org `FieldOps-Project`: repositórios `backend`, `frontend`, `app` e `docs` |

> **Como ler este documento.** Os números vêm de dados reais do GitHub (issues, pull requests, commits e execuções de CI), coletados e calculados por script. Onde o dado não existe, a ferramenta usa uma **premissa**, e ela aparece rotulada (○ ou "premissa"). Os scripts e os CSVs ficam em `scripts/` e `dados/`, na mesma pasta deste arquivo, e qualquer pessoa consegue refazer as contas.

## 1. Resumo

O FieldOps tem {{issues.total}} issues, {{prs.total}} pull requests e {{imr.total|0}} commits (sem merges) em 15 semanas. A qualidade do **processo** é o ponto fraco, mais do que a do código: dos {{prs.amostra}} PRs mergeados analisados, **{{d.sem_rev}} ({{d.pct_sem_rev|0}}%) não têm revisão registrada de outra pessoa no GitHub** (a medida enxerga apenas a revisão registrada na plataforma: revisões por chat ou presenciais não aparecem, e o número não é um juízo sobre as pessoas), embora o `CONTRIBUTING.md` peça uma; só {{d.pct_evid|0}}% anexaram a evidência de funcionamento que o DoD pede; e as issues fechadas quase nunca têm os critérios de aceitação marcados ({{issues_folha.ac_marcados}} de {{issues_folha.ac_total}}). O CI, quando existe, funciona (taxa de sucesso de {{d.ci_taxa|0}}%), e a maioria dos defeitos que apareceram foi pequena e corrigida logo. O risco está no que ainda não foi construído: a sincronização offline (RP03; o marco M6 é o de maior peso, 20%) ainda não tem endpoint no backend nem motor no app, e as {{issues.backend_abertas_sem_resp}} issues do backend dessa trilha estão **sem responsável**. As sete ferramentas apontam, por caminhos diferentes, para o mesmo ponto: o DoD hoje é autodeclarado, e não verificado. A seção 6 reúne cinco ações para a sprint S8.

## 2. Plano de qualidade resumido (processo 8.1)

Esta seção define *o que é qualidade* no FieldOps, como ela será medida e quem faz o quê. Segue os três processos da Aula 05: **8.1** planejar, **8.2** garantir (auditar processos) e **8.3** controlar (medir resultados e recomendar mudanças).

### 2.1 Padrões e requisitos de qualidade aplicáveis

| Padrão / requisito | Fonte | O que exige | Onde é verificado |
|---|---|---|---|
| Definição de Pronto (DoD) de história | `18-definicao-de-pronto` §18.1 | critérios de aceitação claros; código em branch própria via PR; lint e tipos; sem segredos nem logs sensíveis; testes dos critérios; estados de tela; contrato de API; evidência de funcionamento | checklist do template de PR; folha de verificação (ferramenta iii) |
| DoD específico por camada | §18.2 mobile, §18.3 web, §18.4 API | teste em Android; persistência após reinício; permissões negadas; paginação; erros 401/403/404/409/422; DTO ≠ entidade; autorização no backend; sincronização testada para repetição | revisão do PR + testes automatizados |
| DoD da sprint e do MVP | §18.5 e §18.6 | incremento integrado e demonstrável; PRs revisados; riscos registrados; MVP com fluxo ponta a ponta, build Android, migrações, sem defeito crítico sem contenção | demonstração e revisão da sprint |
| Severidade de defeitos | §18.7 | crítico (bloqueia), alto (corrigir antes da release), médio (aceitar com plano), baixo (backlog) | fluxo de não conformidade (ferramenta ii) |
| Critérios de aceitação por entrega | `17-criterios-de-aceitacao` | cenários dado/quando/então, por marco (tabela 2.2) | demonstração do marco |
| Regras de negócio críticas | `09-regras-de-negocio` | RN-003 (autorização na API), RN-007 (sem credenciais em logs), RN-041/066 (dados locais sobrevivem ao reinício), **RN-067/068 (idempotência, sem duplicidade)**, RN-070 (falha parcial não apaga fila), RN-075/076 (conflito detectado, aprovado prevalece), RN-082/084 (aprovada protegida; revisor não altera resposta) | testes de regra + AC-SYNC, AC-REVIEW |
| Requisitos de projeto | Declaração de Escopo | RJ01 OpenAPI desde M1; RJ03 Git/PR/**revisão de código**; RJ05 validação em Android; RJ06 sem segredos e autorização no backend | folha de verificação, CI, revisão de segurança (backend #35) |
| Requisitos não funcionais | `11-arquitetura` §11.14 | RNF-001 (dados pendentes após reinício), RNF-002 (erros padronizados), RNF-005 (sync idempotente), RNF-009 (tipos e lint), RNF-010 (sem dados sensíveis no repo) | CI e testes |

### 2.2 Critérios de aceitação por marco (resumo)

| Marco | Critério principal (rubrica 19.6) | Critérios de aceitação (doc. 17) | Pacotes da EAP |
|---|---|---|---|
| M1 Fundação (21/08) | três aplicações executáveis e contrato OpenAPI inicial | 17.1 gerais; RJ01 | 2.1–2.4 |
| M2 Autenticação (04/09) | sessão integrada e autorização | AC-AUTH, AC-USERS, AC-MASTER, AC-SECURITY | 3.1, 3.2, 4.1, 4.2, 5.2 |
| M3 Planejamento (18/09) | modelo e inspeção criados pela web | AC-TEMPLATE, AC-SCHEDULING | 3.3, 3.4, 4.3, 4.4 |
| M4 Execução online (02/10) | checklist dinâmico e respostas | AC-MOBILE-LIST, AC-START, AC-CHECKLIST, AC-ADMIN-MONITOR | 3.5, 5.3, 5.4 |
| M5 Recursos nativos (16/10) | foto, QR Code e localização | AC-EVIDENCE, AC-QR, AC-LOCATION, AC-NONCONFORMITY | 3.5, 4.5, 5.5 |
| M6 Offline (30/10) | persistência e sincronização confiável | AC-COMPLETE, **AC-SYNC** (envio, reenvio sem duplicidade, falha parcial, conflito) | 3.6, 5.6, 5.7 |
| M7 Revisão (13/11) | aprovação, reprovação e correção | AC-REVIEW; RN-079 a RN-085 | 3.7, 4.6, 6.2, 6.3 |
| M8 Release (27/11) | integração final, build, documentação e defesa | **AC-RELEASE** (19 passos sem editar o banco); DoD do MVP (§18.6) | 7.1–7.4 |

### 2.3 Métricas, linha de base e metas

A coluna "linha de base" foi **calculada por script** com os dados de 18/11/2026. As metas são **propostas** do gerente (premissa a confirmar com o grupo); a coluna "ferramenta" diz onde a métrica é acompanhada.

| Métrica | Linha de base (18/11) | Meta proposta | Ferramenta |
|---|---|---|---|
| PRs com revisão registrada de outra pessoa | {{d.pct_rev|0}}% ({{cruzamento.revisados_total}} de {{prs.amostra}}) | 100% nos PRs do núcleo (sync, auth, revisão) e ≥ 80% nos demais | folha (iii) |
| PRs com evidência de funcionamento anexada | {{d.pct_evid|0}}% | ≥ 90% | folha (iii) |
| PRs com issue vinculada (`Closes #N`) | {{d.pct_issue|0}}% | 100% | folha (iii) |
| CI verde no momento do merge | {{d.pct_ci|0}}% (onde havia CI) | 100% | folha (iii) |
| Taxa de sucesso das execuções de CI | {{d.ci_taxa|0}}% | ≥ 90% | Pareto (iv) |
| Tamanho mediano do PR | {{hist.tamanho.mediana|0}} linhas | ≤ 400 linhas (referência de revisão) | histograma (v) |
| Taxa de conclusão por sprint | {{d.pbar|0}}% (média S1–S7) | ≥ 80%, sem pontos abaixo do LIC | gráfico p (vi) |
| Issues fechadas dentro da sprint prevista | {{d.pct_prazo|0}}% ({{d.prazo_n}} de {{issues_folha.den_prazo}}) | ≥ 70% | gráfico p (vi) |
| Commits por semana | média {{imr.cl|0}}; {{d.pct_8_semanas|0}}% dos commits só na semana 11 | sem semana acima do LSC; sem semana zerada | I-MR (vi) |
| Critérios de aceitação marcados ao fechar issue | {{issues_folha.ac_marcados}} de {{issues_folha.ac_total}} | 100% | folha (iii) |
| Defeitos críticos abertos no M8 | não medido (sem rótulo de defeito) | 0 (DoD do MVP) | Pareto (iv) |

### 2.4 Atividades de garantia (8.2) e de controle (8.3), com responsáveis

Responsáveis seguem a proposta da base do projeto (FM, JV, GR, PD, AF); são **premissas a confirmar**.

| Processo | Atividade | Frequência | Responsável | Evidência |
|---|---|---|---|---|
| 8.2 Garantia | Auditar PRs contra o DoD (folha de verificação) | a cada sprint | FM | folha e resultados desta análise, atualizados |
| 8.2 Garantia | Revisão de código cruzada (backend ↔ app ↔ web) | todo PR | autor ≠ revisor; PD revisa JV/GR, JV revisa AF, GR revisa FM | review `APPROVED` no GitHub |
| 8.2 Garantia | Revisão do contrato OpenAPI antes de integrar | por épico | JV (A: FM) | `docs`, OpenAPI regenerado |
| 8.2 Garantia | Retrospectiva com ação de melhoria (DoD da sprint) | fim de sprint | FM | issue de melhoria |
| 8.3 Controle | CI obrigatório e verde para merge (build, lint, tipos, testes, CodeQL) | todo PR | PD (CI backend), AF (web), FM (app) | status checks |
| 8.3 Controle | Testes automatizados dos fluxos críticos (sync, auth, revisão) | por épico | GR (6.2), PD (6.3) | relatório de testes |
| 8.3 Controle | Gráficos de controle (p e I-MR) e Pareto atualizados | semanal | FM | figuras 4, 6a e 6b |
| 8.3 Controle | Revisão de segurança (AC-SECURITY) antes da release | M8 | JV | issue backend #35 |

### 2.5 Tratamento de não conformidades

Não conformidade (NC) é qualquer desvio do DoD, defeito, falha de CI ou critério de aceitação não atendido. O fluxo está desenhado na figura 2 (painel B). Regras:

| Severidade (DoD §18.7) | Prazo de tratamento | Quem decide | Registro |
|---|---|---|---|
| Crítica (perda de dados, falha de segurança, duplicidade grave, fluxo principal impossível) | imediato; bloqueia a entrega | FM + dono do pacote | issue de defeito + plano de contenção + análise de causa |
| Alta (P0 indisponível sem alternativa) | antes da release | dono do pacote | issue de defeito |
| Média (há alternativa, sem perda de dados) | aceitar com plano | FM | issue + nota na revisão da sprint |
| Baixa (visual, melhoria) | backlog | dono do pacote | issue |

Todo defeito vira issue com **rótulo de defeito e severidade**. Hoje isso não acontece: nenhuma das {{issues.total}} issues tem rótulo de defeito (achado da ferramenta iii).

## 3. Dados e método

| Fonte | Como foi coletada | O que alimenta |
|---|---|---|
| Issues (117) | `gh issue list --json` nos 4 repositórios; milestones = sprints; caixas de critérios de aceitação e DoD contadas no texto do card | folha de issues, gráfico p, dispersão (c) |
| Pull requests ({{prs.total}}) | `gh pr list/view --json` (tamanho, datas, revisões, checks, arquivos) e API de comentários | folha, histograma, dispersão (a, b) |
| Commits ({{imr.total|0}} sem merges) | API `commits` em todas as branches; mensagens no padrão Conventional Commits | Pareto (a), gráfico I-MR |
| Execuções de CI ({{ci.runs}}) | `gh run list` e passo que falhou (`gh run view`) | Pareto, Ishikawa |
| Documentação | `fieldops-src/docs/notion` (17, 18, 09, 11, 12), TAP e Declaração de Escopo | plano de qualidade, Ishikawa |

**Amostra de PRs.** Dos {{prs.total}} PRs, {{prs.mergeados}} foram mergeados. Retirei {{prs.triviais}} PRs que só carregam os templates de PR/issue (corpo vazio; o template ainda não existia), {{prs.fechados_sem_merge}} fechados sem merge (retrabalho, tratado no Pareto) e {{prs.abertos}} abertos. Sobram **{{prs.amostra}} PRs mergeados** (backend {{prs.por_repo.backend}}, frontend {{prs.por_repo.frontend}}, app {{prs.por_repo.app}}).

**Tamanho do PR** = adições + remoções, sem `package-lock.json`, `pnpm-lock.yaml` e similares (que inflavam dois PRs do app em milhares de linhas).

**Limitações que o leitor deve ter em mente.**
- Revisão feita fora do GitHub (conversa, reunião presencial) não aparece nos dados. Os números dizem "sem revisão **registrada**".
- Vários PRs são abertos pouco antes do merge (o `createdAt` é do PR, não do início do trabalho). Por isso o "tempo de ciclo do PR" mede o tempo de fila de revisão e integração, não o tempo de desenvolvimento. O tempo do primeiro commit ao merge também está no CSV.
- Algumas issues foram fechadas em lote (por exemplo, as 7 issues de web do S2 em um único minuto, em 19/10). A data de fechamento dessas issues é de organização do quadro, e não da entrega.
- Os logins do GitHub foram trocados por siglas na base de dados, e duas identidades de commit da mesma pessoa foram unificadas (premissa). Os gráficos e tabelas não identificam quem concentra commits.
- Instantâneo do GitHub coletado em 18/11/2026 às 14h56 UTC (11h56 em Brasília; ver `dados/coleta_meta.json`). A base do projeto (§9) registra 57/103 issues concluídas, levantadas antes da coleta; esta análise mostra {{p_chart.total_k}}/{{p_chart.total_n}} porque as issues `frontend#19` e `frontend#21` foram fechadas às 14h30 UTC de 18/11, depois desse levantamento. Os dois documentos de gestão (riscos e demais) usam 57/103; aqui vale a coleta. A diferença é só essa, de duas issues.

## 4. As sete ferramentas

### 4.1 Diagrama de causa e efeito (Ishikawa)

**Objetivo no projeto.** Organizar as causas do problema que mais ameaça o MVP: *falhas de sincronização offline e defeitos que escapam para a integração*. O problema é relevante porque o núcleo do produto (RP02/RP03, offline e sincronização) vale 15 pontos da rubrica do produto e 20% do peso do marco M6, e porque o TAP o lista entre os principais riscos.

**Dados usados.** As causas vêm de (★) evidência coletada no GitHub e (○) premissas do gerente quando não há dado. As evidências são calculadas pelo script: concentração de commits por pessoa, PRs sem revisão, falhas de CI por passo, data de início do CI do backend, caixas de DoD marcadas.

![Diagrama de Ishikawa: falhas de sincronização offline e defeitos que escapam para a integração](01-ishikawa.png)

*Figura 1. Diagrama de Ishikawa (6M adaptado a software: pessoas, processo, ferramentas, requisitos, ambiente e medição).*

**Análise.**
- **Pessoas.** Em cada repositório, um único integrante concentra a maior parte dos commits: {{concentracao.app.pct|0}}% no app, {{concentracao.backend.pct|0}}% no backend e {{concentracao.frontend.pct|0}}% no frontend. A trilha de sincronização do backend (issues #24 a #27) não tem responsável.
- **Processo.** {{d.sem_rev}} de {{prs.amostra}} PRs sem revisão registrada; PRs empilhados (merge em branch que não é a `develop`) deixaram código fora da `develop`, como no `frontend#36` ("restaurar o shell que ficou fora da develop"); a migração Flyway V5 saiu duplicada (`backend#57`).
- **Ferramentas.** O CI do backend só entrou em {{ci_primeiro_run.backend}} (PR #60), então os PRs anteriores foram mergeados sem verificação automática. No app, {{ci.falhas_passo.Validar configuração do Expo}} das {{ci.falhas}} falhas de CI vieram do mesmo passo (`expo-doctor`, por patches novos do Expo SDK 57).
- **Requisitos.** O contrato de sincronização ainda não está fechado (`docs#2` aberta); RN-067 a RN-078 são 12 regras de idempotência e conflito. O app descobriu, em `app#60`, que `by-qr` devolve qualquer equipamento a qualquer usuário autenticado (RN-063).
- **Medição.** {{issues_folha.dod_marcados}} de {{issues_folha.dod_total}} caixas de DoD e {{issues_folha.ac_marcados}} de {{issues_folha.ac_total}} caixas de critérios de aceitação estão marcadas nas issues fechadas. Sem rótulo de defeito, não existe taxa de defeitos.

**Cinco porquês (causa-raiz provável).** (1) Por que o defeito de integração aparece tarde? Porque mobile, web e API só se encontram no fim; o login real do app foi integrado em 18/09 e a sincronização ainda não. (2) Por que só no fim? Porque cada frente trabalha com mocks e o backend atrasou: 21 issues sem dono. (3) Por que o backend atrasou? Porque a capacidade ficou concentrada em poucas pessoas e a ordem das issues não priorizou o núcleo (o dashboard P1 do web, `frontend#28`, foi entregue em 09/11 enquanto a sincronização não começou). (4) Por que ninguém percebeu a tempo? Porque o quadro de issues não reflete o estado real (fechamento em lote, caixas sem marcar). (5) Por que o quadro e o DoD não alertaram? Porque o DoD é **autodeclarado**: o PR diz "revisado" ou "CI passando" e nada verifica.

**Conclusão e ação.** A causa-raiz é de processo (DoD sem verificação) somada a uma concentração de pessoas, e não uma falha técnica isolada. **Ação:** transformar o DoD em verificação automática e obrigatória (ação 1 da seção 6) e fechar o contrato de sincronização antes de escrever o motor (ação 3).

### 4.2 Fluxograma

**Objetivo no projeto.** Tornar explícito o caminho de uma entrega até o aceite e o caminho de uma não conformidade, para que cada etapa tenha dono e critério. Dá o desenho do que a folha de verificação mede.

**Dados usados.** Não há dados numéricos; o desenho vem do `CONTRIBUTING.md` (fluxo de PR e revisão), do DoD (§18.1 e §18.5), da severidade de defeitos (§18.7) e do template de PR, que existe nos três repositórios.

![Fluxograma de qualidade: entrega (A) e tratamento de não conformidade (B)](02-fluxograma.png)

*Figura 2. Painel A: issue, branch, implementação, PR, CI, revisão, merge, demo e aceite. Painel B: tratamento de não conformidade.*

**Análise.** O fluxo A tem três portões de qualidade: **CI verde**, **revisão por outra pessoa** e **demo contra os critérios de aceitação e o DoD**. Confrontado com os dados: o portão de CI funcionou (apenas 1 PR, `app#46`, foi mergeado com CI vermelho, entre {{folha.itens[12].aplicaveis}} PRs com CI aplicável); o portão da revisão quase não deixa registro (só {{d.pct_rev|0}}% dos PRs têm revisão registrada); o portão da demo não deixa rastro (as issues fechadas não registram os critérios marcados). No fluxo B, o passo "abrir issue de defeito com severidade" não é praticado, e por isso não existe taxa de defeitos.

**Conclusão e ação.** O fluxo está correto no papel e quebrado em dois portões. **Ação:** ativar a proteção da branch `develop` no GitHub (exigir 1 aprovação e CI verde) e adotar o rótulo `defeito` mais severidade para alimentar o fluxo B (ações 1 e 5 da seção 6).

### 4.3 Folha de verificação

**Objetivo no projeto.** Registrar, com marcas contáveis, se cada PR cumpre o DoD que o próprio grupo definiu, e comparar o que o autor **declara** com o que os metadados do GitHub **comprovam**.

**Dados usados.** {{prs.amostra}} PRs mergeados (amostra descrita na seção 3). Dois tipos de marca: **D1 a D8**, as caixas do "Checklist de DoD" do template de PR (autodeclaradas pelo autor; {{cruzamento.com_checklist}} PRs têm o checklist e {{cruzamento.sem_checklist}} não); e **V1 a V8**, verificações feitas por script nos metadados (nome da branch, título, base, issue citada, status de CI, revisão por outra pessoa, arquivos de teste e de documentação no diff). Itens que o GitHub não permite auditar (ausência de segredos, acessibilidade, teste manual) ficam fora e dependem da revisão humana. Os dados brutos estão em `dados/prs.csv`.

![Folha de verificação do DoD em 55 PRs](03-folha-verificacao.png)

*Figura 3. Matriz de marcas: verde = conforme, vermelho = não conforme, cinza = não se aplica ou PR sem checklist. Colunas em ordem cronológica de abertura.*

{{md.folha}}

**Issues fechadas.** A mesma lógica aplicada às {{issues_folha.fechadas}} issues fechadas:

{{md.folha_issues}}

**Análise.**
- **Revisão.** O autor marcou "revisado por outra pessoa" em apenas 4 PRs, e só 2 delas têm revisão registrada. Nos demais, o checklist traz notas como "Sem revisor disponível". Pelos metadados, {{cruzamento.revisados_total}} PRs foram revisados ({{cruzamento.aprovados_total}} aprovados e {{cruzamento.pediram_mudancas}} com mudanças pedidas, `app#40`).
- **Evidência.** Dos {{folha.itens[6].aplicaveis}} PRs com checklist, {{folha.itens[6].conformes}} marcaram a evidência de funcionamento e {{folha.itens[6].nao_conformes}} deixaram a caixa aberta, em geral com a nota "falta anexar os prints" ou "print a anexar" (web) e "pendente: simulador" (app). É o segundo maior problema de processo do projeto.
- **Declarado × verificado.** Dos {{cruzamento.d2_declarado}} PRs que marcaram "lint e tipos passando", {{cruzamento.d2_ci_sucesso}} ({{d.pct_ci_cruz|0}}%) têm CI verde, {{cruzamento.d2_ci_falha}} tem CI vermelho (`app#46`) e {{cruzamento.d2_sem_ci}} foram mergeados antes de existir CI. Dos {{cruzamento.d6_declarado}} que marcaram "documentação atualizada", {{cruzamento.d6_com_doc}} têm arquivo de documentação no diff.
- **Padronização.** Branch fora do padrão (6 PRs, entre eles os do backend com nome `issue-N-...` e os criados por agentes), PRs empilhados ({{cruzamento.base_fora_develop|0}}: mergeados em base diferente da `develop`) e 14 PRs sem issue citada. Os três PRs com o checklist inteiro em branco são de backend.
- **Issues.** Nenhuma issue fechada tem critério de aceitação marcado e só {{issues_folha.dod_marcados}} de {{issues_folha.dod_total}} caixas de DoD estão marcadas. Apenas {{d.prazo_n}} de {{issues_folha.den_prazo}} issues com sprint foram fechadas até o fim da sprint prevista.

**Conclusão e ação.** O grupo preenche o checklist (94% nos itens D1–D5), mas as duas barreiras que mais protegem a integração (**revisão por outra pessoa** e **evidência anexada**) são as menos cumpridas. **Ação:** tornar V4, V5 e V6 requisitos de merge (proteção de branch) e marcar os critérios de aceitação na issue no momento do fechamento (ações 1 e 4).

### 4.4 Diagrama de Pareto

**Objetivo no projeto.** Separar os poucos tipos de defeito e de não conformidade que respondem pela maior parte do retrabalho, para decidir onde agir primeiro.

**Dados usados.** (1) **{{pareto_defeitos.total}} commits `fix`** (sem merges) dos quatro repositórios, classificados por script em 7 categorias de causa com regras de palavra-chave (a lista commit a commit está em `dados/fixes_classificados.csv`, para auditoria). Como o projeto não usa rótulo de defeito, o commit `fix` é o melhor indicador de defeito corrigido; **limitação:** ele só conta o que foi corrigido, não o que escapou. Para mostrar que a frequência não é tudo, o painel (b) da figura 4a pondera cada categoria por um peso de severidade presumido (**premissa**: baixo = 1, médio = 3, alto = 5, crítico potencial = 10, com base no §18.7). (2) As marcas ✘ da folha de verificação, como não conformidades de processo (itens D1–D6 e D8 ficam de fora para não duplicar V1, V5, V6 e V8).

![Pareto de defeitos corrigidos, por frequência e ponderado por severidade](04a-pareto-defeitos.png)

*Figura 4a. Pareto dos defeitos (commits `fix`).*

{{md.pareto_defeitos}}

![Pareto das não conformidades de processo](04b-pareto-nao-conformidades.png)

*Figura 4b. Pareto das não conformidades do DoD nos PRs.*

{{md.pareto_nc}}

**Análise.**
- **Defeitos por frequência.** {{d.pareto_a_top}} de {{pareto_defeitos.total}} commits (cerca de {{d.pareto_a_top_pct|0}}%) estão nas {{pareto_defeitos.corte}} primeiras categorias; a maior, de longe, é **layout e acabamento visual** (40%), concentrada no frontend e em duas rajadas de ajustes (09/11 e 18/11). É retrabalho barato e de baixa severidade.
- **Defeitos ponderados.** Com o peso de severidade, a ordem muda: **sessão/segurança** e **regras de negócio** passam à frente, e persistência/sincronização sobe para o terceiro lugar. Ou seja, o que dói pouco aparece muito e o que dói muito aparece pouco. Apesar de raros, os defeitos de sessão, segurança, offline e sincronização (7 commits) merecem prioridade nos testes.
- **Processo.** Quatro itens respondem por cerca de {{d.pareto_b_top_pct|0}}% das marcas ✘: revisão registrada ({{pareto_nc.itens[0].n}}), evidência ({{pareto_nc.itens[1].n}}), issue vinculada ({{pareto_nc.itens[2].n}}) e testes no diff ({{pareto_nc.itens[3].n}}). Os três primeiros somam {{d.pareto_b_top3}} marcas ({{d.pareto_b_top3_pct|0}}%).
- **Outros sinais de retrabalho** (fora do Pareto): {{prs.fechados_sem_merge}} PRs fechados sem merge (por exemplo, `frontend#37`, refeito em seis PRs menores; `backend#47` e `#49`, substituídos) e {{ci.falhas}} execuções de CI que falharam, **{{ci.falhas_passo.Validar configuração do Expo}} delas por um único passo** (`expo-doctor`). Esse passo, sozinho, deixou a `develop` do app vermelha de 18/09 (PR #46, mergeado com CI vermelho) até 14/10 (PR #49), segundo o comentário do próprio PR #48.

**Conclusão e ação.** A regra dos 80/20 aparece no processo (quatro itens do DoD) mais do que nos defeitos de código. **Ação:** atacar a revisão e a evidência primeiro; no código, concentrar os testes de regressão nas categorias sessão, regras de negócio e sincronização, e resolver o `expo-doctor` na raiz (fixar as versões do SDK 57 no `package.json` e atualizá-las em um PR dedicado).

### 4.5 Histograma

**Objetivo no projeto.** Ver como se distribuem duas variáveis contínuas que condicionam a qualidade da revisão: o **tamanho** do PR e o **tempo de ciclo** do PR (aberto até o merge).

**Dados usados.** Os {{hist.tamanho.n}} PRs da amostra. Tamanho em linhas alteradas (sem lockfiles); tempo em horas entre a abertura e o merge. `dados/prs.csv`.

![Histogramas do tamanho do PR e do tempo até o merge](05-histograma.png)

*Figura 5. (a) Tamanho dos PRs; (b) tempo de ciclo dos PRs, em escala logarítmica.*

| Estatística | Tamanho (linhas) | Tempo de ciclo do PR (h) | Primeiro commit até o merge (h) |
|---|---:|---:|---:|
| n | {{hist.tamanho.n}} | {{hist.tempo_pr.n}} | {{hist.lead.n}} |
| Média | {{hist.tamanho.media|0}} | {{hist.tempo_pr.media|1}} | {{hist.lead.media|1}} |
| Mediana | {{hist.tamanho.mediana|0}} | {{hist.tempo_pr.mediana|2}} ({{d.mediana_pr_min|0}} min) | {{hist.lead.mediana|2}} ({{d.mediana_lead_min|0}} min) |
| Desvio-padrão | {{hist.tamanho.dp|0}} | {{hist.tempo_pr.dp|1}} | {{hist.lead.dp|1}} |
| Q1 – Q3 | {{hist.tamanho.q1|0}} – {{hist.tamanho.q3|0}} | {{hist.tempo_pr.q1|2}} – {{hist.tempo_pr.q3|1}} | {{hist.lead.q1|2}} – {{hist.lead.q3|1}} |
| Percentil 90 | {{hist.tamanho.p90|0}} | {{hist.tempo_pr.p90|0}} | {{hist.lead.p90|0}} |
| Máximo | {{hist.tamanho.maximo|0}} | {{hist.tempo_pr.maximo|0}} | {{hist.lead.maximo|0}} |
| Assimetria | {{hist.tamanho.assimetria|1}} | {{hist.tempo_pr.assimetria|1}} | {{hist.lead.assimetria|1}} |

**Análise.**
- **Tamanho.** A distribuição é assimétrica à direita (assimetria {{hist.tamanho.assimetria|1}}), com média ({{hist.tamanho.media|0}}) acima da mediana ({{hist.tamanho.mediana|0}}). **{{hist.n_tam_gt_400}} dos {{hist.tamanho.n}} PRs ({{hist.pct_tam_gt_400|0}}%) passam de 400 linhas** (a referência usual para uma revisão eficaz) e {{hist.n_tam_gt_1000}} ({{hist.pct_tam_gt_1000|0}}%) passam de 1.000. Os maiores trazem funcionalidades inteiras (o do backend com 5.344 linhas inclui a edição de rascunho de modelos).
- **Tempo de ciclo.** A distribuição é **bimodal**: {{hist.n_merge_lt_1h}} PRs ({{hist.pct_merge_lt_1h|0}}%) foram mergeados em menos de 1 hora (mediana de {{d.mediana_pr_min|0}} minutos, compatível com merge rápido, logo após o CI, sem etapa de revisão registrada), enquanto {{hist.n_merge_gt_72h}} PRs ({{hist.pct_merge_gt_72h|0}}%) ficaram abertos por mais de 72 horas, entre 3 e 21 dias (conflitos, dependência de outro PR, ADR pendente). O desvio-padrão ({{hist.tempo_pr.dp|0}} h) é maior que a média ({{hist.tempo_pr.media|0}} h), sinal de que a média não descreve o processo.
- **Combinação.** PRs medianos de {{hist.tamanho.mediana|0}} linhas mergeados em minutos dificilmente tiveram uma etapa de revisão registrada. É coerente com a folha de verificação (só {{d.pct_rev|0}}% com revisão registrada).

**Conclusão e ação.** O tamanho dos PRs está acima do que se revisa bem e o tempo de revisão é, na prática, zero para a maioria. **Ação:** adotar meta de PR ≤ 400 linhas (quebrar por camada ou por critério de aceitação, como o `frontend#37` acabou sendo refeito) e mínimo de revisão registrada para os PRs do núcleo.

### 4.6 Gráfico de controle

**Objetivo no projeto.** Separar variação normal de variação por causa especial no desempenho do projeto, para saber quando reagir. Foram usados dois gráficos: **gráfico p** (proporção de issues concluídas por sprint, com tamanho de amostra variável) e **gráfico I-MR** (commits por semana, medida individual).

**Dados usados.** (1) `dados/issues.csv`: issues por milestone/sprint (S1 a S8) e estado em 18/11. (2) `dados/commits.csv`: commits não-merge por semana (semana 1 = 10/08). Limites de 3σ calculados por script. Gráfico p: p̄ = {{d.pbar|1}}% ({{d.k17}} concluídas de {{d.n17}}, em S1–S7; S8 está em curso e fica fora do cálculo), σᵢ = √(p̄(1−p̄)/nᵢ), LSC/LIC = p̄ ± 3σᵢ. Regras de sinal: ponto fora dos limites; 2 de 3 pontos além de 2σ. I-MR: X̄ ± 2,66·MR̄; sinais: ponto fora do limite e 8 pontos seguidos do mesmo lado da média; a semana 15 (parcial) não entra no cálculo.

![Gráfico p da taxa de conclusão por sprint](06a-grafico-p-sprints.png)

*Figura 6a. Gráfico p: issues concluídas por sprint (concluídas/total em cada ponto).*

{{md.p_chart}}

![Gráfico I-MR de commits por semana](06b-grafico-imr-commits.png)

*Figura 6b. Gráfico de valores individuais e de amplitude móvel dos commits semanais.*

| Parâmetro do I-MR | Valor |
|---|---:|
| Média X̄ (semanas 1–14) | {{imr.cl|1}} commits/semana |
| Amplitude móvel média MR̄ | {{imr.mrbar|1}} |
| LSC = X̄ + 2,66·MR̄ | {{imr.ucl|1}} |
| LIC | {{imr.lcl|1}} (negativo, não se aplica) |
| LSC da amplitude (3,267·MR̄) | {{imr.ucl_mr|1}} |
| Semanas com zero commit | semanas 5 e 9 |
| Maior sequência do mesmo lado da média | {{imr.maior_sequencia_mesmo_lado}} semanas (semanas 2 a 10, abaixo da média) |

**Análise.**
- **Gráfico p.** O processo tinha comportamento estável até S5 (62,5% a 88,2%), com um ponto de exceção favorável: **S2 acima do LSC** (17/17 = 100%). Esse resultado não é desempenho extraordinário: as 7 issues de web e outras do backend dessa sprint foram **fechadas em lote**, semanas depois do fim da sprint (web em 19/10; backend em 26/09), o que mostra o problema de medição já apontado. **S6 ({{d.s6_p|1}}%) e S7 ({{d.s7_p|1}}%) estão abaixo do LIC** ({{d.s6_lcl|1}}% e {{d.s7_lcl|1}}%): causa especial, e não variação do acaso. A causa é identificável: as 4 issues de push/pull/conflito/arquivos do backend (S6) não têm responsável e o motor de sincronização do app (7 das 9 issues de S6) não foi iniciado. S8 (0/10) ainda não é avaliável, pois a sprint não terminou. **Pontualidade:** só {{d.prazo_n}} das {{issues_folha.den_prazo}} issues com sprint foram fechadas até o fim da sprint prevista ({{d.pct_prazo|0}}%); o atraso começou já em S2 (2 de 17 no prazo), bem antes do sinal estatístico, e é o que o gráfico p de "concluídas até hoje" esconde.
- **Gráfico I-MR.** {{imr.total|0}} commits em 15 semanas, mas **{{imr.pct_pico_top3|0}}% deles caem em apenas 3 semanas** (semanas 1, 11 e 14). A **semana 11** (19 a 25/10, antes do marco M6) tem {{imr.pico.valor|0}} commits, acima do LSC ({{imr.ucl|0}}); as amplitudes das semanas 11 e 12 estão acima do LSC da amplitude. Há 9 semanas seguidas abaixo da média e duas semanas sem commit. O padrão é de **entrega em rajadas** antes dos prazos, seguido de silêncio, e não de fluxo contínuo. A semana 14 (163 commits) não ultrapassa o LSC, mas reforça o padrão.

**Conclusão e ação.** Os dois gráficos mostram um processo **fora de controle** em S6–S7 (atraso por causa especial) e **instável** no ritmo (rajadas). Ação: tratar S6–S7 como causa especial (atribuir dono, aplicar a ordem de corte do RJ07) e passar a acompanhar o gráfico p no fim de cada sprint (com o número de issues fechadas **até a data de fim da sprint**), e não só em 18/11; além disso, impor integração diária (merge de PRs pequenos) para reduzir a rajada (ações 3 e 4).

### 4.7 Diagrama de dispersão

**Objetivo no projeto.** Testar relações que o time costuma assumir: "PR grande demora mais para ser revisado", "PR grande cumpre menos o DoD" e "quanto mais planejamos, mais entregamos".

**Dados usados.** (a) tamanho do PR × tempo até o merge ({{dispersao.tam_x_tempo.n}} PRs; escala log nos dois eixos porque as variáveis são muito assimétricas); (b) tamanho do PR × percentual de itens de DoD marcados no PR ({{dispersao.tam_x_dod.n}} PRs com checklist; pequeno deslocamento vertical aleatório de ±1,2 pontos só para separar pontos sobrepostos); (c) issues planejadas × concluídas nas sprints S1–S7 ({{dispersao.plan_x_concl.n}} sprints). Retas de mínimos quadrados, coeficiente de correlação de Pearson r, R² e p-valor do teste de r = 0; o ρ de Spearman é dado como verificação por ser robusto a valores extremos.

![Diagramas de dispersão](07-dispersao.png)

*Figura 7. (a) Tamanho × tempo até o merge; (b) tamanho × conformidade declarada; (c) planejadas × concluídas.*

| Par de variáveis | n | r (Pearson) | R² | ρ (Spearman) | p-valor | Leitura |
|---|---:|---:|---:|---:|---:|---|
| (a) tamanho × tempo até o merge (log-log) | {{dispersao.tam_x_tempo.n}} | {{dispersao.tam_x_tempo.r|2}} | {{dispersao.tam_x_tempo.r2|2}} | {{dispersao.tam_x_tempo.spearman|2}} | {{dispersao.tam_x_tempo.p|2}} | sem relação |
| (b) tamanho × % de DoD marcado | {{dispersao.tam_x_dod.n}} | {{dispersao.tam_x_dod.r|2}} | {{dispersao.tam_x_dod.r2|2}} | {{dispersao.tam_x_dod.spearman|2}} | {{dispersao.tam_x_dod.p|2}} | sem relação |
| (c) issues planejadas × concluídas | {{dispersao.plan_x_concl.n}} | {{dispersao.plan_x_concl.r|2}} | {{dispersao.plan_x_concl.r2|2}} | {{dispersao.plan_x_concl.spearman|2}} | {{dispersao.plan_x_concl.p|2}} | moderada, não significativa (n = 7) |

**Análise.**
- **(a)** O coeficiente é praticamente zero ({{dispersao.tam_x_tempo.r|2}}; R² ≈ 0): **o tempo de revisão não cresce com o tamanho**. Um PR de 5.000 linhas é mergeado em minutos, como um de 50. Num processo de revisão que funciona, espera-se correlação positiva; a ausência dela indica que a revisão registrada não acompanha o tamanho do PR. A relação sem log também é fraca ({{dispersao.tam_x_tempo.pearson_bruto|2}}).
- **(b)** O tamanho não explica o cumprimento do DoD (r = {{dispersao.tam_x_dod.r|2}}). O DoD é cumprido (ou ignorado) de forma uniforme, independentemente do tamanho: depende do hábito do autor, e não do esforço do PR.
- **(c)** Há correlação positiva moderada (r = {{dispersao.plan_x_concl.r|2}}, R² = {{dispersao.plan_x_concl.r2|2}}), mas com 7 pontos o p-valor ({{dispersao.plan_x_concl.p|2}}) não permite afirmar associação. **Correlação não é causalidade:** as sprints com mais issues (S1 e S2) são as primeiras, de setup, e também as mais "fechadas em lote". O tempo é um fator escondido que afeta as duas variáveis. A reta não serve para prever a próxima sprint.

**Conclusão e ação.** As duas hipóteses de tamanho do PR não se confirmam e levam à mesma lição: o processo de revisão e o preenchimento do DoD não reagem ao risco do PR. **Ação:** definir regra de revisão por **risco** (núcleo de sincronização, autenticação e revisão = revisão obrigatória por outra pessoa, qualquer que seja o tamanho) e repetir o gráfico (a) depois dela; esperamos ver correlação positiva e significativa.

## 5. Quadro-resumo das ferramentas

| Ferramenta | Pergunta respondida | Achado principal | Ação |
|---|---|---|---|
| (i) Ishikawa | Por que a sincronização e a integração são frágeis? | causa-raiz de processo (DoD autodeclarado) e de pessoas (um dono por repositório) | tornar o DoD verificável; fechar o contrato de sincronização |
| (ii) Fluxograma | Qual é o caminho de qualidade? | portões de revisão e de demonstração não deixam rastro | proteção da `develop`; rótulo de defeito |
| (iii) Folha de verificação | O DoD é cumprido? | {{d.pct_rev|0}}% com revisão; {{d.pct_evid|0}}% com evidência | requisitos de merge |
| (iv) Pareto | Onde está o retrabalho? | processo (4 itens = {{d.pareto_b_top_pct|0}}%); defeito visual domina a frequência, e sessão e sincronização dominam a severidade | testes nas categorias críticas |
| (v) Histograma | Como são os PRs? | mediana de {{hist.tamanho.mediana|0}} linhas e de {{d.mediana_pr_min|0}} min até o merge; bimodal | PR ≤ 400 linhas |
| (vi) Gráfico de controle | O processo é estável? | S6 e S7 fora de controle; commits em rajadas | dono para o backend; integração diária |
| (vii) Dispersão | O tamanho explica a revisão? | r ≈ 0: a revisão não acompanha o risco | revisão por risco |

## 6. Síntese integrada e ações priorizadas

**O que as sete ferramentas dizem em conjunto.** O FieldOps produz código com padrão razoável (branches e títulos no padrão em {{d.pct_branch|0}}% e {{d.pct_titulo|0}}% dos PRs, CI verde em {{d.pct_ci|0}}% dos merges verificáveis, testes no diff em {{d.pct_testes|0}}% e documentação no diff em {{d.pct_docs|0}}% dos PRs aplicáveis), mas **não verifica o que declara**. A falta de revisão (folha, Pareto, histograma e dispersão) e a medição frágil (Ishikawa, gráficos de controle) fazem com que os problemas sejam descobertos tarde, na integração. O atraso nas sprints S6 e S7 é causa especial (gráfico p) e se soma à concentração de pessoas e ao ritmo em rajadas (I-MR). Como o núcleo ainda por construir é justamente o de maior risco (sincronização, RP03), o custo da qualidade sobe a cada dia sem integração.

**Cinco ações priorizadas para a sprint S8 (até 27/11/2026).** Prioridade = impacto sobre o núcleo do MVP ÷ esforço. Responsáveis e prazos são propostas (premissa a confirmar).

| # | Ação | Ferramenta de origem | Responsável | Prazo | Indicador de sucesso |
|---|---|---|---|---|---|
| 1 | **Proteger a `develop`**: exigir 1 aprovação de outra pessoa e CI verde para merge, em `backend`, `frontend` e `app`; PRs do núcleo (sync, auth, revisão) com revisor definido na abertura | Ishikawa, fluxograma, folha, dispersão | JV (admin) com FM | 19/11 | PRs com revisão registrada: de {{d.pct_rev|0}}% para ≥ 80% |
| 2 | **Teste de integração da sincronização** antes do merge: três cenários do AC-SYNC (envio, reenvio da mesma operação sem duplicidade, falha parcial) contra o backend real, com evidência no PR | Ishikawa, Pareto | GR e PD (backend), FM (app) | 25/11 | 3 de 3 cenários verdes; 0 duplicidade na demo |
| 3 | **Fechar o contrato de sincronização** (`docs#2` e OpenAPI) e **atribuir dono às {{issues.backend_abertas_sem_resp}} issues do backend** sem responsável; aplicar a ordem de corte do RJ07 ao que não couber (dashboard avançado, P1) | Ishikawa, gráfico p | JV e FM | 19/11 | 0 issues P0 sem responsável; contrato publicado |
| 4 | **PRs pequenos e integração diária**: meta ≤ 400 linhas e merge ao menos em dias alternados; marcar critérios de aceitação e DoD na issue **no fechamento**; acompanhar o gráfico p e o I-MR no fim da sprint | histograma, I-MR, folha de issues | FM (acompanha), todos | 23/11 em diante | mediana ≤ 400 linhas; 0 semana sem commit |
| 5 | **Medir defeitos**: rótulo `defeito` com severidade (§18.7) em toda issue de defeito; resolver o `expo-doctor` na raiz fixando as versões do SDK; registrar as limitações conhecidas (`docs#6`) | Pareto, Ishikawa, fluxo B | AF (web) e FM (app); PD (CI) | 23/11 | taxa de sucesso do CI ≥ 90% (hoje {{d.ci_taxa|0}}%); 100% dos defeitos com severidade |

## 7. Premissas e como reproduzir

**Premissas deste documento**
1. Siglas e papéis das pessoas conforme a base do projeto (FM gerente e mobile; JV, GR e PD backend; AF web); duas identidades de commit da mesma pessoa foram unificadas.
2. As metas de qualidade (seção 2.3) e os pesos de severidade do Pareto (1, 3, 5, 10) são propostas do gerente, e não decisões do grupo.
3. O commit `fix` representa defeito corrigido; a classificação em categorias é por palavra-chave (auditável em `dados/fixes_classificados.csv`).
4. Marcas D1–D8 são o que o autor declarou no PR; V1–V8 são verificações automáticas nos metadados do GitHub, sem avaliar o conteúdo do código.
5. Revisão presencial ou por chat não está nos dados. A recomendação de registrar a revisão no GitHub vem daí.
6. Itens do DoD que não são auditáveis por metadados (segredos, acessibilidade, teste manual) estão fora da folha.

**Reprodutibilidade.** Na pasta `scripts/`: `python3 coleta_github.py` (requer `gh` autenticado) gera os CSVs em `dados/`; `python3 analise_qualidade.py` calcula tudo e gera as figuras e `dados/resultados.json`; `python3 montar_relatorio.py` regenera este documento a partir do modelo `relatorio_template.md`. Dependências: Python 3, numpy e matplotlib.

| Arquivo | Conteúdo |
|---|---|
| `dados/issues.csv`, `prs.csv`, `commits.csv`, `ci_runs.csv` | dados brutos tratados (siglas no lugar de logins) |
| `dados/fixes_classificados.csv` | commits `fix` com a categoria atribuída |
| `dados/resultados.json` | todos os números usados no texto |
| `scripts/` | coleta, estatística, análise e montagem do relatório |

## Referências

1. TAKATU, Deivison S. **Gestão de Projetos: Custos e Qualidade (Aula 05)**. UniSENAI-SP, 2026. Processos 8.1 a 8.3 e sete ferramentas básicas da qualidade.
2. FIELDOPS. **Documentação do projeto** (`docs/notion`: 09 Regras de negócio, 11 Arquitetura, 17 Critérios de aceitação, 18 Definição de Pronto, 19 Critérios de avaliação) e `CONTRIBUTING.md`.
3. FIELDOPS. **Termo de Abertura do Projeto** e **Declaração do Escopo** (04/10/2026).
4. GITHUB. Repositórios `FieldOps-Project/backend`, `frontend`, `app` e `docs` (consulta de 18/11/2026).
5. CARVALHO, Fábio Câmara Araújo de. **Gestão de projetos**. 2. ed. São Paulo: Pearson, 2018.
