# Base única de fatos — FieldOps (fonte de verdade para TODOS os artefatos)

> Quem escrever qualquer artefato do FieldOps deve usar **exatamente** estes códigos, nomes, datas e IDs.
> Se precisar de algo que não está aqui, derive da documentação em `fieldops-src/docs/notion/*.md` e registre como *premissa*.

## 1. Identificação

- **Projeto:** FieldOps — Plataforma de Inspeção em Campo (MVP)
- **Instituição:** Centro Universitário SENAI São Paulo — UniSENAI-SP, Campus Sorocaba (Santa Rosália). Curso: Análise e Desenvolvimento de Sistemas. Disciplina: Gestão de Projetos. Orientador da disciplina: Prof. Me. Deivison S. Takatu. Ano: 2026.
- **Gerente do projeto:** Felipe Marques (TAP/Declaração de Escopo mais recentes, 30/09 e 04/10/2026).
- **Patrocinador / comitê executivo:** coordenação do curso + corpo docente das disciplinas envolvidas (Expo/React Native, Java/Spring Boot, desenvolvimento web). **Prof. Glauco Todesco** = autor da especificação (Notion), orientador e *product owner* acadêmico.
- **Fontes oficiais:** `fieldops-src/docs/notion/` (24 arquivos), TAP e Declaração de Escopo (`~/Downloads/TAP - FieldOps.docx`, `~/Downloads/Declaração do Escopo - FieldOps.docx`), `FieldOps_Sprint1_Planejamento.pdf`, repositórios GitHub da org `FieldOps-Project` (`docs`, `backend`, `frontend`, `app`).
- **Material do professor (formatos exigidos):** `material/` (slides em `material/Aulas`, templates em `material/Template`, enunciados em `material/Atividade`).

## 2. Stack REAL (usar isto; os documentos antigos dizem "Angular", o código é Next.js)

| Componente | Tecnologia |
|---|---|
| Mobile | Expo / React Native + TypeScript, Expo Router, SQLite local (offline), outbox; validação obrigatória em Android; build via EAS |
| Web administrativo | **Next.js 16 (App Router) + TypeScript** (o Notion aceita "Angular/React"; TAP/Escopo de 30/09 e 04/10 citam Angular — registrar como *decisão/divergência documentada*: o frontend foi implementado em Next.js/React) |
| API | Java + Spring Boot, PostgreSQL, Flyway, JWT, OpenAPI/Swagger, Docker Compose |
| Evidências | armazenamento compatível com S3 |
| Colaboração | GitHub (org FieldOps-Project, 4 repos), Conventional Commits, PR com revisão, branches `<tipo>/<epico>-<slug>`, CI por repo |

## 3. Equipe (5 integrantes) e papéis (inferidos dos repositórios; tratar como premissa confirmável)

| Sigla | Pessoa | Papel no projeto | Evidência |
|---|---|---|---|
| FM | Felipe Marques | **Gerente do Projeto** + desenvolvedor mobile (Expo) | gerente no TAP; issues do app atribuídas a `felipersas`; commits em `docs` |
| JV | João Victor Souza | Desenvolvedor backend (líder técnico da API) + convenções/docs | 25 commits em `backend`, issues #1 e #2 backend e docs |
| GR | Gabriel Ribeiro | Desenvolvedor backend (cadastros, modelos, qualidade de API) | issues backend (`gabrrkl7`) |
| PD | Pedro Dias | Desenvolvedor backend + documentação (TAP) | issues backend (`PedroDias010`), commits `docs: TAP` |
| AF | André Fernandes | Desenvolvedor web (Next.js) | 26 issues do frontend |

Observação de risco de pessoas: backend concentra 4 pessoas só em issues, mas o mobile depende quase só de FM (gerente + dev) → **sobrecarga do gerente** (acumula gestão e desenvolvimento mobile) e **dependência de pessoa-chave**. Usar como evidência nos riscos/RACI.

Capacidade: 5 pessoas × 16 semanas × 12 h/semana de dedicação ao projeto (aulas de projeto + extraclasse) = **960 h**.

## 4. Calendário-base (16 semanas efetivas, 8 sprints de 2 semanas, marcos M1–M8)

Início: **segunda 10/08/2026** (criação dos repositórios). Fim do planejamento-base: **sexta 27/11/2026**. As 4 semanas restantes do calendário institucional NÃO são reserva de desenvolvimento.

| Sprint | Semanas | Período | Marco (fim da sprint) | Épicos | Incremento demonstrável |
|---|---|---|---|---|---|
| S1 | 1–2 | 10/08 – 21/08 | **M1 Fundação** (21/08) | EP-01 | 3 aplicações executáveis + contrato OpenAPI inicial |
| S2 | 3–4 | 24/08 – 04/09 | **M2 Autenticação** (04/09) | EP-02, EP-03 | login integrado, usuários e cadastros |
| S3 | 5–6 | 07/09 – 18/09 | **M3 Planejamento** (18/09) | EP-04, EP-05 | supervisor cria modelo, agenda e atribui |
| S4 | 7–8 | 21/09 – 02/10 | **M4 Execução online** (02/10) | EP-05(PBI-030), EP-06 | técnico executa inspeção online |
| S5 | 9–10 | 05/10 – 16/10 | **M5 Recursos nativos** (16/10) | EP-07 | câmera, QR Code, GPS, não conformidade |
| S6 | 11–12 | 19/10 – 30/10 | **M6 Offline** (30/10) | EP-08 | inspeção offline sincronizada |
| S7 | 13–14 | 02/11 – 13/11 | **M7 Revisão** (13/11) | EP-09, EP-10 | aprovação/reprovação/correção + testes |
| S8 | 15–16 | 16/11 – 27/11 | **M8 Release** (27/11) | EP-10 | build Android, deploy, demo ponta a ponta |

Feriados no período: 07/09 (Independência), 12/10 (N. Sra. Aparecida), 02/11 (Finados), 15/11 (Proclamação, domingo), 20/11 (Consciência Negra) — citar como **risco de calendário** e usar para dimensionar durações (descontar nas estimativas, sem alterar as datas dos marcos).

## 5. Backlog (fonte: `15-backlog-do-produto.md`)

72 PBIs P0 (PBI-001…PBI-072) em 10 épicos (EP-01 Fundação técnica; EP-02 Identidade e acesso; EP-03 Cadastros operacionais; EP-04 Modelos de inspeção; EP-05 Planejamento; EP-06 Execução de campo; EP-07 Recursos nativos e evidências; EP-08 Offline e sincronização; EP-09 Revisão e decisão; EP-10 Qualidade e entrega) + 10 PBIs P1 (PBI-073…PBI-082). Regras de negócio RN-001…; requisitos de produto **RP01–RP10** e de projeto **RJ01–RJ08** estão na Declaração de Escopo (ver §8).

## 6. EAP CONGELADA (códigos e nomes obrigatórios; níveis 1–2)

Orientada a ENTREGAS (substantivo/particípio), não a verbos. Nível 0 = "FieldOps — Plataforma de Inspeção em Campo (MVP)".

| Código | Entrega / pacote de trabalho | Épico/PBI de referência |
|---|---|---|
| **1** | **Gerenciamento do Projeto** | — |
| 1.1 | Termo de Abertura e Declaração de Escopo aprovados | — |
| 1.2 | Plano de Gerenciamento do Projeto (escopo, cronograma, custos, qualidade, recursos, comunicações, riscos, aquisições, partes interessadas) | — |
| 1.3 | Relatórios de status e demonstrações dos marcos M1–M8 | — |
| 1.4 | Encerramento do projeto (aceite, lições aprendidas, relatório final) | — |
| **2** | **Fundação Técnica** | EP-01 |
| 2.1 | Repositórios e convenções Git/PR definidos | PBI-001 |
| 2.2 | Contrato OpenAPI e padrões compartilhados (enums, IDs, erros) | PBI-006 |
| 2.3 | Pipelines de integração contínua (backend, web, app) | PBI-005 |
| 2.4 | Ambiente de desenvolvimento padronizado (Docker Compose, PostgreSQL, migrações) | PBI-004 |
| **3** | **API REST Central (Backend)** | EP-02…EP-09 (lado API) |
| 3.1 | Identidade e acesso (JWT, perfis, autorização) | PBI-007, 010, 011, 012 |
| 3.2 | Cadastros operacionais (usuários, clientes, locais, equipamentos, QR) | PBI-013…017 |
| 3.3 | Modelos de inspeção versionados com snapshot | PBI-018…024 |
| 3.4 | Planejamento e atribuição de inspeções | PBI-025…030 |
| 3.5 | Execução, respostas e evidências (upload de arquivos, localização, não conformidades) | PBI-031…047 (API) |
| 3.6 | Sincronização idempotente (push/pull, cursor, conflitos) | PBI-051…053, 055 |
| 3.7 | Revisão, aprovação e trilha de auditoria | PBI-056…063 (API) |
| **4** | **Interface Administrativa Web** | EP-02…EP-09 (lado web) |
| 4.1 | Shell administrativo, autenticação e navegação | PBI-003, 009 |
| 4.2 | Gestão de usuários e cadastros | PBI-011, 013…017 |
| 4.3 | Construtor e publicação de modelos de inspeção | PBI-018…023 |
| 4.4 | Agendamento, atribuição e acompanhamento de inspeções | PBI-025…030 |
| 4.5 | Visualização de evidências e não conformidades | PBI-047 |
| 4.6 | Revisão: aprovação, reprovação e histórico | PBI-056…061 |
| **5** | **Aplicativo Mobile (Android)** | EP-02…EP-09 (lado app) |
| 5.1 | Base do app, navegação e design system | PBI-002 |
| 5.2 | Login e sessão segura | PBI-008, 010 |
| 5.3 | Lista, filtros e detalhes das inspeções | PBI-031…033 |
| 5.4 | Checklist dinâmico, respostas e progresso | PBI-034…040 |
| 5.5 | Recursos nativos (câmera, QR Code, localização) e evidências | PBI-041…046 |
| 5.6 | Persistência offline (SQLite) e fila outbox | PBI-048…050 |
| 5.7 | Sincronização, tela de pendências e fluxo de correção | PBI-051, 054, 055, 062 |
| **6** | **Qualidade e Testes** | PBI-064, 065 |
| 6.1 | Plano de testes e critérios de aceitação | — |
| 6.2 | Testes automatizados dos fluxos críticos | PBI-065 |
| 6.3 | Testes de integração mobile–API–web e validação em dispositivos Android | RJ05 |
| 6.4 | Acessibilidade, desempenho e correção de falhas | PBI-064 |
| **7** | **Entrega e Release (M8)** | EP-10 |
| 7.1 | Dados de demonstração reproduzíveis | PBI-066 |
| 7.2 | Build Android (EAS), painel web e API publicados/executáveis | PBI-068, 069, 070 |
| 7.3 | Documentação final (README, OpenAPI, diagramas) | PBI-067, 071 |
| 7.4 | Demonstração ponta a ponta e apresentação final | PBI-072 |

## 7. Partes interessadas (IDs fixos)

| ID | Parte interessada | Categoria | Papel / interesse resumido |
|---|---|---|---|
| PI-01 | Coordenação do curso (UniSENAI-SP Sorocaba) | Patrocinador / comitê executivo | aprova escopo, valida marcos, quer produto integrado e avaliação justa |
| PI-02 | Prof. Glauco Todesco | Orientador / product owner acadêmico | autor da especificação; define regras de negócio e critérios; avalia entregas |
| PI-03 | Professores das disciplinas Expo, Spring Boot e Web (comitê executivo) | Avaliadores | avaliam por marco; exigem qualidade técnica e participação equilibrada |
| PI-04 | Prof. Deivison S. Takatu (Gestão de Projetos) | Avaliador da disciplina | avalia o planejamento e a documentação de GP |
| PI-05 | Felipe Marques | Gerente do projeto | responde por prazo, escopo, integração; também dev mobile |
| PI-06 | Equipe de desenvolvimento (JV, GR, PD, AF) | Equipe | executa; quer escopo claro e carga equilibrada |
| PI-07 | Técnicos de campo (persona Carlos) | Usuário final (app) | executar checklist offline, sem perder dados |
| PI-08 | Supervisores (persona Marina) | Usuário final (web) | planejar, acompanhar, revisar e aprovar |
| PI-09 | Administradores (persona Ana) | Usuário final (web) | manter cadastros, usuários e permissões |
| PI-10 | Responsáveis do cliente (persona Roberto) | Usuário futuro (somente leitura, fora do MVP) | receber resultados e evidências |
| PI-11 | Organização operadora (empresa que presta inspeções) | Cliente representado | quer padronização, rastreabilidade e menos retrabalho |
| PI-12 | Provedores de serviço (Expo/EAS, GitHub, hospedagem, armazenamento S3) | Fornecedores | disponibilidade e limites de planos gratuitos |
| PI-13 | UniSENAI-SP — infraestrutura (laboratórios, rede, calendário institucional) | Instituição | calendário, feriados, eventos que afetam o prazo |

## 8. Requisitos (Declaração de Escopo, 04/10/2026)

Produto: RP01 App mobile de execução · RP02 Operação offline (SQLite) · RP03 Sincronização idempotente (outbox) · RP04 Interface administrativa web (não substituível por Swagger/BD) · RP05 Modelos versionados · RP06 API REST central + OpenAPI · RP07 Autenticação/autorização por perfil (validada na API) · RP08 Evidências rastreáveis (S3) · RP09 Fluxo de revisão (aprova/reprova/corrige; aprovada fica protegida) · RP10 Auditoria.
Projeto: RJ01 Contrato OpenAPI desde M1 · RJ02 8 sprints + marcos M1–M8 · RJ03 Git/PR/revisão · RJ04 Stack definida · RJ05 Validação em Android · RJ06 Segurança (sem segredos no repo; autorização no backend) · RJ07 Controle de escopo/ordem de corte · RJ08 Avaliação por marcos.
Premissas P01–P07 e Restrições R01–R07 conforme a Declaração de Escopo. Exclusões: portal do cliente, multiempresa, pagamento, IA, IoT, assinatura com validade jurídica, mais de um técnico por inspeção, validação obrigatória fora do Android.
Ordem de corte em atraso: (1) remover dashboard avançado; (2) limitar tipos de resposta; (3) só foto da câmera; (4) construtor sem arrastar e soltar; (5) conflitos de sync = detectar e bloquear; (6) adiar notificações, PDF e assinatura. Núcleo intocável: autenticação, planejamento, checklist, foto, offline, sincronização, revisão.

## 9. Status REAL em 18/11/2026 (GitHub, milestones por sprint — 4 repos somados)

| Sprint | Issues concluídas / total |
|---|---|
| S1 | 15 / 17 |
| S2 | 17 / 17 |
| S3 | 7 / 10 |
| S4 | 10 / 14 |
| S5 | 4 / 8 |
| S6 | 2 / 13 |
| S7 | 2 / 14 |
| S8 | 0 / 10 |
| **Total** | **57 / 103 (≈ 55%)** |

Por repo (issues fechadas/total, todas as issues): backend 14/41, frontend 22/31, app 21/39, docs 1/6. PRs mergeados/fechados: backend 23/24, frontend 19/20, app 22/22, docs 1/1. 21 issues abertas do backend sem responsável. Hoje (18/11) estamos na semana 15 (S8) com S6 e S7 muito atrasadas → **desvio de prazo real**, usar no monitoramento/lições aprendidas como *snapshot de 18/11/2026* e aplicar a ordem de corte (RJ07). Não esconder o atraso; apresentá-lo como situação monitorada com ações corretivas.

## 9-A. Responsável principal (R) e aprovador (A) por pacote da EAP — PROPOSTA DE PLANEJAMENTO (usar em RACI, cronograma, orçamento)

Regra: cada pacote tem exatamente 1 R principal (quem responde pela entrega) e 1 A. C e I são definidos no RACI. Rotular como **proposta/premissa a confirmar com o grupo** (não afirmar como fato histórico).

| Pacote | R | A | | Pacote | R | A |
|---|---|---|---|---|---|---|
| 1.1 | FM | PI-01 Coordenação | | 4.4 | AF | FM |
| 1.2 | FM | PI-02 Prof. Glauco | | 4.5 | AF | FM |
| 1.3 | FM | PI-03 Comitê (valida marcos) | | 4.6 | AF | FM |
| 1.4 | FM | PI-01 Coordenação | | 5.1 | FM | FM (auto-A: sinalizar como risco de concentração) |
| 2.1 | JV | FM | | 5.2 | FM | JV (contrato de auth) |
| 2.2 | JV | FM | | 5.3 | FM | FM |
| 2.3 | PD | FM | | 5.4 | FM | PI-02 (regras do checklist) |
| 2.4 | GR | JV | | 5.5 | FM | FM |
| 3.1 | JV | FM | | 5.6 | PD | FM |
| 3.2 | GR | JV | | 5.7 | PD | JV |
| 3.3 | GR | PI-02 (regras de modelo) | | 6.1 | GR | FM |
| 3.4 | PD | JV | | 6.2 | GR | FM |
| 3.5 | JV | FM | | 6.3 | PD | FM |
| 3.6 | JV | FM | | 6.4 | AF | FM |
| 3.7 | PD | PI-02 (regras de revisão) | | 7.1 | JV | FM |
| 4.1 | AF | FM | | 7.2 | FM | PI-03 |
| 4.2 | AF | FM | | 7.3 | PD | FM |
| 4.3 | AF | PI-02 | | 7.4 | FM | PI-03 |

Leitura de risco embutida nessa distribuição (citar nos riscos/RACI): FM acumula gestão (1.x) + 6 pacotes do mobile + build/demo (7.2, 7.4) → **sobrecarga/ponto único de falha**; AF é o único R do web (6 pacotes) → dependência de pessoa-chave; backend e documentação têm 3 pessoas (JV, GR, PD) → capacidade de apoiar mobile (PD) e web (JV, em 4.1/4.2 como C).

## 9-B. Horas e custos (premissas de valoração — ficam em `orcamento-fieldops.md` como fonte; os demais artefatos só referenciam)

- Capacidade total: **960 h** (≈ 192 h por pessoa) em 16 semanas. O orçamento e o cronograma devem fechar em torno desse total (±10%), por pessoa (≈ 192 h ± 15%). Horas de gerenciamento do FM contam dentro das 192 h dele.
- Taxas hipotéticas (custo de oportunidade de aluno de ADS em estágio/júnior): **desenvolvedor R$ 45/h**; **gerente de projeto R$ 60/h** (só nas horas de gestão do FM); revisão/mentoria docente NÃO entra no orçamento financeiro (contrapartida institucional, listada à parte como horas não valoradas).
- Custos diretos de caixa (hipóteses, preços de 2026 plausíveis): domínio, hospedagem/API container, PostgreSQL gerenciado, armazenamento S3, EAS Build (plano gratuito → pode exigir plano pago em semana de pico), dispositivos Android da equipe (depreciação/uso, custo zero de caixa), internet/energia. Total de caixa esperado: poucas centenas de reais (R$ 0 a ~R$ 1.500) — o TAP diz "sem investimento financeiro direto".
- Reserva de contingência: 10% sobre o custo valorizado (para riscos identificados) + reserva gerencial 5% (desconhecidos). Mostrar a linha de base de custos e o orçamento total.
- Estimativa de três pontos por item (otimista cO, mais provável cM, pessimista cP) com esperado PERT = (cO + 4cM + cP)/6 e desvio = (cP − cO)/6.

## 10. Convenções de escrita

- Português do Brasil, tom técnico-acadêmico claro e direto. Sem emojis em documentos formais (relatório/slide); nos `.md` de atividade, no máximo marcadores de status (🟢🟡🔴) quando o template do professor os usa.
- Premissas explícitas quando não houver dado real (o enunciado pede). Valores monetários são HIPÓTESES de valoração: o TAP declara "sem investimento financeiro direto".
- Datas no formato DD/MM/AAAA. Moeda: R$ com vírgula decimal.
- Cada documento começa com tabela de identificação (projeto, gerente, data, versão) conforme os templates em `material/Template/`.
- Nada de texto genérico de IA ("é importante ressaltar", "em suma", "fundamental", listas de três por reflexo). Escrever como um aluno competente de ADS escreveria, com números e referências ao projeto real.
- Todos os arquivos finais vão em `/Users/felipersas/Documents/Facul/gestao-proj/entrega/` na pasta da atividade indicada (ver `01-plano-de-entrega.md`).
