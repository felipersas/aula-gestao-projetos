# Termo de Abertura de Projeto — EASY (Projeto Integrador, ciclo 2026/2)

| Campo | Informação |
|---|---|
| **Projeto** | EASY — Sistema de Gestão de Propostas Comerciais para Laboratórios de Calibração e Ensaios (PII) |
| **Gerente do projeto** | Felipe Marques (premissa, a confirmar com o grupo) |
| **Data** | 18/11/2026 |
| **Versão** | 1.0 |
| **Instituição / disciplina** | SENAI — curso de Análise e Desenvolvimento de Sistemas; Projeto Integrador (o artigo do PI usa o nome Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior). Documento entregue na disciplina Gestão de Projetos (Prof. Me. Deivison S. Takatu) |
| **Modelo** | Modelo 4.1 do professor; as linhas do modelo foram mantidas na ordem. Foram acrescentadas as linhas **Principais entregas**, **Requisitos iniciais**, **Decisões e divergências registradas** e **Responsáveis**, que o enunciado da Aula 02 exige e o modelo não traz |
| **Fontes** | Repositórios da organização Projeto-Integrador-TADS3 (backend, frontend, app, documentacao), lidos em 18/11/2026; `documentacao/` local (Planejamento, sprints, arquitetura, banco, AWS, PRDs e o artigo do PI de 13/06/2026) |

> O EASY é um projeto que já existe e está em andamento. Este termo descreve o produto **como ele está hoje** e formaliza o ciclo do semestre atual (2026/2). Não há patrocinador nem cliente real documentado: o patrocínio é tratado como **acadêmico (premissa)**. Datas e marcos vêm dos PRs e issues; o que é projeção está marcado. Valores monetários são **hipóteses**.

---

## Título do projeto

EASY — Sistema de Gestão de Propostas Comerciais para laboratórios de calibração e ensaios (Projeto Integrador, ciclo 2026/2).


## Objetivo geral e objetivos específicos

**Objetivo geral:** entregar, até 27/11/2026, a versão do EASY deste semestre: uma plataforma multiplataforma (API, painel web e aplicativo mobile) em que um laboratório de calibração e ensaios monta, revisa, acompanha e aprova propostas comerciais a partir de um catálogo técnico único, no lugar de planilhas dispersas.

**Objetivos específicos:**

1. manter um catálogo técnico único e versionado (fabricantes, equipamentos com várias tecnologias e fotos, serviços internos e subcontratados, análises críticas com horas de engenheiro e de técnico);
2. montar propostas por itens (equipamento, tecnologia, quantidades, serviços), com valor calculado e guardadas como cópia congelada, com revisões (Rev.00, Rev.01…) e linha do tempo;
3. controlar o acesso por perfil (Admin, Comercial, Engenheiro) na API, com valores monetários ocultos para o Engenheiro;
4. dar painéis por perfil, listagem gerencial com filtros e exportação CSV, e atualização em tempo real (SignalR);
5. permitir que o cliente consulte e responda a proposta por link assinado, sem login;
6. absorver os campos que faltavam em relação à planilha legada do cliente (laboratório, organismo certificador OCD/OCP, entregáveis, desconto, forma de pagamento, tempo de resposta): fase 1 entregue em 14/11, fase 2 em aberto;
7. fechar o ciclo com escopo congelado, testes ponta a ponta verdes e documentação alinhada à stack real.


## Justificativa do projeto (benefícios)

Empresas de engenharia que fazem calibração e ensaios montam propostas com dados espalhados em planilhas, mensagens e documentos soltos. Isso causa erro de preço e de escopo, retrabalho e demora para responder ao cliente, e deixa o conhecimento técnico preso a quem mantém a planilha. O artigo do PI (13/06/2026) descreve exatamente esse problema.

O EASY centraliza o cadastro técnico e o processo comercial em uma base única: o comercial monta a proposta como um "carrinho" com dados já preenchidos pela engenharia, e a engenharia trabalha no catálogo e na execução sem ver valores.

**Benefícios esperados:** menos retrabalho e erro de digitação; proposta rastreável (revisões, linha do tempo, histórico de alterações); preço histórico preservado mesmo se o catálogo mudar; medição do tempo de resposta (da solicitação à primeira emissão); funil comercial visível em painel; aceite do cliente por link.

**Benefício acadêmico:** aplicar, em um produto real e contínuo, backend .NET, web React e mobile Expo, com Git, PR, testes ponta a ponta e Docker.


## Premissas

1. o ciclo de 2026/2 vai de 10/08/2026 (primeira alteração do semestre nos repositórios) a 27/11/2026, o mesmo calendário de 16 semanas do semestre (**premissa**);
2. a equipe é a do artigo do PI, confirmada pelos contribuidores dos repositórios (4 pessoas);
3. existe uma planilha legada de um cliente (laboratório) que serve de referência de requisitos; os PRs a citam, mas **a identidade do cliente não está documentada** nos repositórios (**premissa**: é tratado como parte interessada, não como patrocinador);
4. o patrocínio é acadêmico: o professor orientador do PI e a coordenação do curso (**premissa**). A conta `senaideivison`, provavelmente o Prof. Deivison Takatu, é colaboradora dos quatro repositórios (**confirmar**);
5. a hospedagem usa créditos acadêmicos da AWS (Learner Lab), sem custo para o grupo (**premissa**, inferida dos commits);
6. não há dados reais de clientes em produção: demonstrações usam dados de exemplo (seed com 14 propostas, mais 250 de carga opcionais);
7. o Engenheiro nunca vê valores monetários, regra aplicada na API;
8. a documentação de planejamento do primeiro ciclo (Node.js, PostgreSQL, Next.js) está superada pelo código (ver decisões).


## Breve descrição do projeto

O EASY é um sistema de gestão comercial e técnica de propostas para laboratórios de calibração e ensaios. Três perfis usam o sistema: **Admin** (acesso completo, usuários, auditoria), **Comercial** (clientes, contatos, propostas, aprovação, link para o cliente) e **Engenheiro** (catálogo técnico e etapa de execução, sem valores).

**Stack real:** API em .NET 8 / ASP.NET Core com Entity Framework Core 8 e MySQL 8, JWT com refresh token, BCrypt, SignalR e Amazon S3 para fotos; painel web em React 18 + TypeScript + Vite, React Router, TanStack Query, Tailwind e shadcn/ui; app mobile em Expo (SDK 55, React Native 0.83, Expo Router) com TanStack Query e Zustand; Docker Compose; testes ponta a ponta em 5 baterias.

**Como funciona hoje:** o Admin cadastra usuários; o Engenheiro mantém equipamentos, tecnologias, serviços e análises críticas com fotos; o Comercial abre uma proposta, escolhe cliente e itens e a emite; cada edição gera uma nova revisão e a anterior fica congelada; só uma pessoa edita por vez (trava de 2 minutos); o cliente responde pelo link assinado (30 dias); painéis e listagens se atualizam em tempo real.


## Principais entregas

1. **API EASY (.NET 8)** — autenticação por e-mail ou CPF, perfis e ocultação de valores, catálogo, propostas congeladas e revisões, trava de edição, link público, histórico de alterações, versionamento de cadastros, painéis por perfil, exportação CSV, notificação em tempo real;
2. **Painel web (React/Vite)** — cadastros, montagem de proposta em 4 seções (cliente e solicitação, itens, entrega, condições comerciais), listagem gerencial, painéis comercial e de engenharia, página pública da proposta, tela de organismos e laboratórios, histórico de auditoria (69 testes unitários);
3. **App mobile (Expo)** — catálogo para o engenheiro (equipamentos com tecnologias e fotos, serviços, análises críticas com horas), painel que atualiza a cada 30 s, histórico de versões;
4. **Campos da planilha legada, fase 1** — laboratório, organismo certificador, data da solicitação, idiomas, entregáveis, desconto, forma de pagamento e tempo de resposta (14/11/2026);
5. **Testes e dados de demonstração** — baterias legado, painéis, segurança, trava de edição e planilha; seed de exemplo e carga opcional de 250 propostas;
6. **Infraestrutura** — Docker Compose (MySQL, API, front em Nginx), bucket S3 e scripts de provisionamento;
7. **Documentação** — README de cada repositório, Swagger da API, este TAP e os planos da disciplina.

**Em aberto até 27/11:** 28 itens "Todo" e 3 "In Progress" no Kanban (70 itens no total), entre eles Selo NATEL (rastreável × acreditado), relatório por cliente, ajustes do fluxo do engenheiro e a simplificação do app (issue #21); parte dos itens de requisitos comerciais já aparece no código, então o quadro precisa ser conciliado; fase 2 da planilha legada (validade da proposta, impostos, PDF).


## Requisitos iniciais

**Funcionais:** login por e-mail ou CPF com renovação de sessão; cadastro de usuários só pelo Admin; catálogo de fabricantes, equipamentos (várias tecnologias, fotos), serviços (internos e externos) e análises críticas; empresas com vários contatos; proposta por itens com subtotal (soma dos serviços × quantidade de equipamentos); código sequencial da proposta; revisões; linha do tempo; etapa de acompanhamento (em análise, aguardando cliente, em execução, concluída); status (emitida, aprovada, reprovada); link de aceite; painéis e filtros; exportação CSV.

**Não funcionais:** valores ocultos ao Engenheiro por lista de permissão na API (a API não inicia se um campo de valor ficar sem classificação); erros padronizados (400 regra de negócio, 409 conflito, 500 sem detalhe interno); datas em UTC; trava de edição; execução por Docker Compose; testes ponta a ponta.

**Limitações conhecidas (README do frontend):** proposta sem validade, condição de pagamento detalhada, impostos e geração de PDF; cadastros com vínculo não podem ser excluídos (só desativados); sem testes de componentes de interface.


## Patrocinador (sponsor)

Professor orientador do Projeto Integrador e coordenação do curso, como patrocínio acadêmico (**premissa**: não há patrocinador comercial nem cliente real documentado). A identidade do orientador deve ser confirmada pelo grupo.


## Estimativa de investimentos

**Sem investimento financeiro direto** (premissa): a hospedagem usa créditos acadêmicos da AWS.

**Hipótese de esforço:** 4 pessoas × 16 semanas × 10 h por semana = 640 h; valorado a R$ 45/h (custo de oportunidade de aluno de ADS, não desembolsado) dá R$ 28.800.

**Hipótese de caixa, se a hospedagem saísse dos créditos acadêmicos:** a arquitetura-alvo de `diagrama-cloud-aws.md` custa cerca de US$ 76,15 por mês (EC2 US$ 15 + RDS Multi-AZ US$ 26 + S3 US$ 0,15 + NAT US$ 32 + tráfego US$ 3), ou cerca de US$ 304,60 em 4 meses. O que está nos repositórios (MySQL em contêiner) deve custar menos; não há estimativa documentada.


## Estimativa de prazo

16 semanas, de **10/08/2026 a 27/11/2026** (premissa de calendário). Em 18/11 estamos na semana 15 e restam 7 dias úteis (20/11 é feriado). Marcos do ciclo, com o que já aconteceu e o que falta:

| Data | Tipo | Marco |
|---|---|---|
| 26/08/2026 | Observado | Perfil Engenheiro sem acesso a valores, análise crítica compartilhada, histórico de alterações (auditoria) e mensagens de erro em português (PRs do backend #27 a #30, do frontend #22 a #26 e do app #15 a #20) |
| 10/09/2026 | Observado | Requisitos comerciais levantados (18 issues abertas em 10/09: 9 no backend, 8 no frontend e 1 no app) e primeira implementação no backend (PR #31); filtros, ordenação e paginação de propostas (PR #41, 14/09) |
| 05/11/2026 | Observado | Início da entrega das propostas congeladas, revisões e painéis por perfil (PRs abertos em 05/11) |
| 14/11/2026 | Observado | Propostas congeladas, revisões, trava de edição, painéis, link de aceite e tempo real integrados na API e no painel web (backend #42 e #43, frontend #36 e #37); campos da planilha legada, fase 1 (backend #44, frontend #38) |
| 17/11/2026 | Observado | App Expo alinhado às novas regras: sem valores para o engenheiro, várias tecnologias por equipamento, horas na análise crítica, histórico de versões (app #22) |
| 27/11/2026 | Previsto (premissa) | Entrega e apresentação final do ciclo: escopo congelado, documentação alinhada à stack real e demonstração com dados de exemplo |

**Ritmo observado:** as entregas se concentram em três momentos (26/08, 10 a 14/09 e 05 a 17/11), com intervalos de semanas sem integração, o que dá pouca margem para a entrega final.

**Kanban em 18/11:** 36 de 70 itens em Done (cerca de 51%), 28 em Todo, 3 em In Progress e 3 sem status.


## Fatores Críticos de Sucesso (FCS)

1. congelar o escopo da entrega final e decidir agora o que fica para o próximo ciclo (fase 2 da planilha legada, Selo NATEL, relatórios adicionais);
2. manter issues, Kanban e código em sincronia, para que o andamento seja medido com dado confiável;
3. todo PR passar pela revisão de outra pessoa e pelas 5 baterias de testes ponta a ponta;
4. preservar a regra de que o Engenheiro nunca vê valores, em API, painel e app;
5. ter uma demonstração reproduzível com dados de exemplo;
6. atualizar a documentação (stack, banco, nuvem) para refletir o que o código faz;
7. feedback do professor orientador e do cliente da planilha legada antes do fechamento.


## Principais riscos

1. escopo maior que o tempo: 28 itens abertos e 7 dias úteis restantes, com risco de entregar tudo incompleto;
2. Kanban defasado em relação ao código, levando a decisões sobre prazo com dado errado;
3. concentração de conhecimento: cerca de 73% dos commits dos quatro repositórios (133 de 182, segundo o GitHub) vêm de uma única pessoa, e o app tem um só contribuidor;
4. dependência de créditos acadêmicos da AWS e de ambiente de deploy não documentado nos repositórios, com o app apontando para a API por HTTP (sem TLS) nos builds do EAS;
5. documentação antiga (Node.js, PostgreSQL, Next.js) contradiz o código e pode confundir a avaliação;
6. vazamento de valores para o Engenheiro por algum campo novo de DTO (mitigado por verificação na partida da API e por testes de segurança);
7. requisitos baseados em uma só planilha de um cliente sem validação direta, com risco de entregar o que não atende ao uso real;
8. interface sem testes de componentes e de navegação.


## Restrições

1. prazo final em 27/11/2026 (premissa de calendário);
2. stack em uso: .NET 8 e MySQL 8 (API), React 18 + Vite (web) e Expo SDK 55 (mobile); mudar de tecnologia neste ciclo está fora de questão;
3. sem orçamento financeiro: apenas créditos e ferramentas gratuitas;
4. equipe de 4 pessoas, em dedicação parcial (hipótese de 10 h por semana cada);
5. o Engenheiro não pode ver nem alterar valores monetários;
6. a proposta deve ser congelada e versionada (nova revisão a cada edição);
7. nenhum dado real de cliente em ambiente de demonstração;
8. fora do escopo desta entrega: validade da proposta, impostos e geração de PDF (limitações conhecidas), assinatura digital e notificações push.


## Interessados no projeto (stakeholders)

Professor orientador e coordenação do curso (patrocínio acadêmico); Prof. Deivison S. Takatu (Gestão de Projetos, colaborador dos repositórios, a confirmar); equipe de 4 integrantes; **Comercial** (monta e acompanha propostas); **Engenheiros** de calibração e ensaio (catálogo e execução); **Admin** (usuários e auditoria); **clientes dos laboratórios** (recebem o link da proposta e a aprovam ou reprovam); **laboratório da planilha legada** (referência de requisitos, identidade a confirmar); organismos certificadores OCD/OCP (entram como cadastro e referência da proposta); fornecedores de serviço (AWS, GitHub, Expo/EAS, Cloudflare).


## Comitê Executivo

Professor orientador do Projeto Integrador e coordenação do curso (premissa; nomes a confirmar), com o Prof. Deivison S. Takatu como avaliador da disciplina de Gestão de Projetos.


## Gerente do Projeto

Felipe Marques (premissa, a confirmar com o grupo).


## Responsáveis (equipe e papéis)

Papéis inferidos dos repositórios (as contas do GitHub foram associadas aos nomes do artigo; **premissa, a confirmar**):

| Integrante | Papel | Evidência |
|---|---|---|
| Felipe Marques | Gerente do projeto (premissa) e desenvolvedor: app mobile, API e infraestrutura | 49 dos 49 commits do app; 58 dos 84 commits do backend; issues do app e de documentação |
| Tobias Perassi Alquezar | Desenvolvedor web (React/Vite) | 22 dos 44 commits do frontend; issues do frontend; integração de autenticação |
| Pedro Henrique Dias de Paula Santos | Desenvolvedor backend e documentação | 15 commits no backend; responsável por issues do backend; autor do artigo do PI |
| Gabriel Ribeiro de Camargo Miranda | Desenvolvedor backend | 8 commits no backend; responsável por issues do backend |


## Decisões e divergências registradas

A documentação de planejamento do primeiro ciclo não bate com o que foi construído. Decisões desta versão: prevalece o código dos repositórios.

| Tema | O que dizem os documentos | Realidade verificada | Decisão |
|---|---|---|---|
| Web | `Planejamento.md`, `arquitetura.md` e artigo: Next.js | React 18 + TypeScript + Vite + React Router (README e issue #7 do frontend, 06/04) | Vale o código. A documentação antiga está superada neste ponto |
| API | Docs: Node.js (Express ou NestJS) ou .NET; issue de docs #3: Prisma | .NET 8 / ASP.NET Core com Entity Framework Core 8 (README e issue #3 do backend) | Vale o código |
| Banco e nuvem | Docs: PostgreSQL 15 no RDS Multi-AZ, VPC com NAT (~US$ 76,15/mês) | MySQL 8 (Pomelo) em contêiner no Docker Compose; arquivos no Amazon S3; commits de junho falam em AWS Learner Lab, Caddy e túnel Cloudflare | Vale o código. O diagrama AWS é a arquitetura-alvo, não o que está no repositório; confirmar o ambiente de deploy com o grupo |
| Escopo do mobile | PRD do engenheiro (27/04): cadastro e edição de equipamentos e serviços, fotos, editor rich text | Issue #21 do app (10/09): reduzir o app a dashboard e consulta; as telas de cadastro ainda existem no código | Decisão de produto de 10/09 prevalece; a remoção das telas segue como item aberto |
| Modelo de dados | 6 tabelas (usuários, clientes, equipamentos, serviços, propostas, itens) | Empresa e contatos, análises críticas com horas, tecnologias, versões de cadastros, propostas congeladas com revisões, laboratórios e organismos certificadores | O modelo cresceu com os requisitos comerciais; o diagrama de banco em docs precisa ser atualizado |
| Equipe | Artigo: 4 integrantes | 4 contribuidores nos repositórios, com os mesmos nomes | Confirmado |

---

## Mapa do enunciado da Aula 02

| Item exigido | Onde está neste TAP |
|---|---|
| Objetivo | Objetivo geral e objetivos específicos |
| Justificativa | Justificativa do projeto (benefícios) |
| Principais entregas | Principais entregas |
| Requisitos iniciais | Requisitos iniciais |
| Premissas | Premissas |
| Restrições | Restrições |
| Stakeholders | Interessados no projeto (stakeholders) |
| Responsáveis | Gerente do Projeto e Responsáveis (equipe e papéis) |
| Prazo estimado | Estimativa de prazo |

---

## O que precisa ser confirmado pelo grupo

- quem é o gerente do EASY (este TAP assume Felipe Marques);

- quem é o professor orientador do PI e o aprovador deste termo;

- qual é o laboratório da planilha legada e se ele pode ser citado;

- se o ciclo termina mesmo em 27/11/2026 e como será a entrega final;

- onde o EASY está hospedado hoje (AWS Learner Lab, instância, TLS);

- a dedicação semanal de cada integrante (aqui, 10 h).

---

## Assinaturas

| | Nome | Data | Assinatura |
|---|---|---|---|
| **Elaborado por** | Felipe Marques | 18/11/2026 | |
| **Aprovado por** | Professor orientador do PI (nome a confirmar) | ____/____/____ | |
