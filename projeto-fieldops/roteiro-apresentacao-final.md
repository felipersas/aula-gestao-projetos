# Roteiro da apresentação final: FieldOps

| Campo | Informação |
|---|---|
| **Projeto** | FieldOps: Plataforma de Inspeção em Campo (MVP) |
| **Disciplina** | Gestão de Projetos, Prof. Me. Deivison S. Takatu, UniSENAI-SP Sorocaba |
| **Grupo** | Felipe Marques (FM), João Victor Souza (JV), Gabriel Ribeiro (GR), Pedro Dias (PD), André Fernandes (AF) |
| **Material** | `apresentacao-final.pptx` (16 slides: 15 principais + 1 de backup; notas do orador em cada slide) e `apresentacao-final.pdf` |
| **Duração-alvo** | 15 minutos de fala + perguntas |
| **Data-base dos números** | 18/11/2026 |
| **Versão** | 1.0 |

> **Sobre a divisão de falas.** Quem fala em cada slide é uma **sugestão**, equilibrada por tempo e por afinidade com o conteúdo (por exemplo, JV fala do caminho crítico e do risco de sincronização, que são do backend). O grupo pode trocar sem alterar o texto: as falas estão escritas na primeira pessoa do plural.

## 1. Quadro de tempo (15 minutos)

Velocidade usada: 140 palavras por minuto. A contagem de palavras e a estimativa de tempo foram feitas por script sobre as falas abaixo (mesmo texto das notas do pptx). O slide 16 é só de apoio e não entra no tempo.

| Slide | Assunto | Quem fala (sugestão) | Tempo alvo | Palavras | Estimativa pela contagem | Acumulado |
|---:|---|---|---:|---:|---:|---:|
| 1 | Capa | PD | 0:35 | 86 | 0:37 | 0:35 |
| 2 | Problema e proposta | FM | 1:00 | 137 | 0:59 | 1:35 |
| 3 | Abordagem de gestão | PD | 1:00 | 137 | 0:59 | 2:35 |
| 4 | Benchmarking | PD | 1:10 | 164 | 1:10 | 3:45 |
| 5 | EAP e rastreabilidade | JV | 0:45 | 106 | 0:45 | 4:30 |
| 6 | Cronograma e caminho crítico | JV | 0:55 | 127 | 0:54 | 5:25 |
| 7 | Recursos e responsabilidades | AF | 0:50 | 113 | 0:48 | 6:15 |
| 8 | Custos e orçamento | GR | 1:00 | 139 | 1:00 | 7:15 |
| 9 | Qualidade | GR | 1:00 | 137 | 0:59 | 8:15 |
| 10 | Riscos | JV | 1:05 | 147 | 1:03 | 9:20 |
| 11 | Comunicação e partes interessadas | GR | 0:50 | 115 | 0:49 | 10:10 |
| 12 | Monitoramento e controle (situação real) | FM | 1:25 | 204 | 1:27 | 11:35 |
| 13 | Lições aprendidas | AF | 0:50 | 120 | 0:51 | 12:25 |
| 14 | Decisões-chave justificadas | AF, JV, PD, GR | 1:10 | 169 | 1:12 | 13:35 |
| 15 | Conclusão e próximos passos | AF, FM | 0:55 | 126 | 0:54 | 14:30 |
| **Total** | | | **14:30** | **2027** | **14:29** | |

O total fica dentro de 15 minutos com folga de cerca de 30 segundos para transições e respiração. Se estourar no ensaio, cortar nesta ordem: (1) a lista de fontes no slide 4, (2) as respostas do slide 8 sobre alçadas, (3) o detalhe de gatilhos no slide 12. Não cortar o slide 12 nem o slide 14, que sustentam o critério de justificativa das decisões.

## 2. Divisão sugerida entre os integrantes

| Integrante | Slides | Tempo de fala (estimado) | Por quê (sugestão) |
|---|---|---:|---|
| FM Felipe Marques | 2, 12, 15 | 2:36 | gerente; conta o problema, apresenta a situação real, a decisão e fecha |
| JV João Victor Souza | 5, 6, 10, 14 | 3:02 | líder técnico do backend; EAP, caminho crítico, risco de sincronização e ordem de corte |
| GR Gabriel Ribeiro | 8, 9, 11, 14 | 3:04 | custos, qualidade e partes interessadas; contingência |
| PD Pedro Dias | 1, 3, 4, 14 | 3:00 | abre a apresentação; processo de gestão no GitHub, benchmarking e outbox (offline) |
| AF André Fernandes | 7, 13, 14, 15 | 2:47 | recursos (pessoa-chave do web), lições, Next.js e conclusão |

Tempo de fala por pessoa entre 2:36 e 3:04: diferença máxima de 0:28. Na rodada de perguntas, quem é dono do tema responde primeiro (coluna *apoio* da seção 4 indica o slide e o artefato).

## 3. Roteiro slide a slide

### Slide 1: Capa
**Fala sugerida:** PD  ·  **Tempo alvo:** 0:35  ·  **Palavras:** 86

> Boa tarde, professor. Somos o grupo do FieldOps: Felipe, João Victor, Gabriel, Pedro e André. Em quinze minutos vamos mostrar o planejamento integrado do projeto, as decisões que tomamos e por quê, e a situação real de hoje, 18 de novembro. Os quatro números da base são: 8 sprints e marcos, 36 pacotes na EAP, 71 itens no cronograma com 967 horas, e 22 riscos mais 4 oportunidades. Todos vêm dos artefatos entregues. A apresentação segue a ordem do relatório final: problema, planejamento, monitoramento e lições.

**Apontar:** Os quatro cartões numéricos; dizer que a apresentação segue o relatório e os artefatos.

**Transição:** Começo pelo problema que o produto resolve.

### Slide 2: Problema e proposta
**Fala sugerida:** FM  ·  **Tempo alvo:** 1:00  ·  **Palavras:** 137

> O problema é conhecido de quem inspeciona equipamento: formulário em papel, planilha, foto solta e mensagem em vários canais. O resultado é dado perdido, retrabalho e nenhuma rastreabilidade. O FieldOps liga quatro passos num fluxo só: o supervisor planeja pelo painel web, o técnico executa no app Android mesmo sem internet, a API sincroniza sem duplicar e o supervisor revisa, aprova ou devolve para correção. O objetivo é entregar esse MVP em 16 semanas, até 27 de novembro, sem investimento financeiro direto. À direita está o limite do escopo: o que entra e, com a mesma clareza, o que fica de fora, como portal do cliente, multiempresa, pagamento, inteligência artificial e IoT. Na especificação, as dores são a foto sem identificação do item, a redigitação dos dados e o campo em branco que só aparece na revisão.

**Apontar:** Os quatro passos do fluxo; depois a coluna do que está fora do escopo.

**Transição:** Para entregar isso, o processo de gestão que adotamos foi este.

### Slide 3: Abordagem de gestão
**Fala sugerida:** PD  ·  **Tempo alvo:** 1:00  ·  **Palavras:** 137

> Adotamos sprints de duas semanas e oito marcos, um por sprint, de 21 de agosto a 27 de novembro. Cada cor mostra a situação do marco hoje: um fechou limpo, três fecharam com pendências, três não foram atingidos e o M8 ainda é futuro. O backlog tem 10 épicos e 72 itens P0; os 10 itens P1 ficam fora da linha de base. O GitHub é a fonte da verdade: quatro repositórios, uma milestone por sprint, pull request com revisão e CI. E como o prazo e as 960 horas são fixos, o que flexibiliza é o escopo: a ordem de corte, do dashboard avançado até notificações e PDF, está definida desde o início, com um núcleo intocável. Dois marcos pesam mais na avaliação: o M6, de offline e sincronização, vale 20%, e o M8 vale 15%.

**Apontar:** A faixa de marcos com as cores; depois a ordem de corte, que reaparece no slide 12.

**Transição:** Antes de aprofundar, vale comparar com o que já existe no mercado.

### Slide 4: Benchmarking
**Fala sugerida:** PD  ·  **Tempo alvo:** 1:10  ·  **Palavras:** 164

> Para o benchmarking olhamos quatro soluções: SafetyCulture, que hoje aparece como Mitti, Fulcrum, GoAudits e KoboToolbox. Verde é o que confirmamos na documentação oficial; azul é alegação do próprio fornecedor; cinza é o que não conseguimos confirmar. Todas resolvem o offline e o registro com foto e localização. O SafetyCulture tem ativos com QR e aprovação, e plano gratuito para até 10 usuários. O Kobo é gratuito, de código aberto, com status de validação e histórico de versões do formulário. O FieldOps se diferencia por reunir checklist versionado com snapshot, QR por equipamento, revisão formal e código próprio, que permite seguir as regras da especificação. A ressalva honesta: é um MVP acadêmico. Offline e revisão ainda estão em construção, e não competimos em maturidade nem em suporte. O SafetyCulture tem aprovação, mas o editor de modelos não funciona offline; Fulcrum e GoAudits dizem oferecer offline, foto e GPS, sem versionamento ou revisão confirmados; o Kobo é a opção mais próxima em custo e liberdade.

**Apontar:** A coluna do FieldOps e as cores; ler o rodapé de fontes e o 'n/c'.

**Transição:** Passando ao planejamento: o que exatamente vamos entregar.

### Slide 5: EAP e rastreabilidade
**Fala sugerida:** JV  ·  **Tempo alvo:** 0:45  ·  **Palavras:** 106

> A EAP é orientada a entregas: 7 entregas de primeiro nível e 36 pacotes de trabalho, e é nesses pacotes que penduramos cronograma, orçamento, RACI e aquisições. Aqui está a rastreabilidade: nas colunas, os 10 requisitos de produto e os 8 de projeto da Declaração de Escopo; nas linhas, as entregas. Verificamos por script que nenhum requisito ficou sem entrega e que os 72 itens P0 do backlog estão todos em algum pacote. A API cobre sete requisitos de produto, e a entrega final toca quase todos, porque a demonstração integra tudo. A linha do gerenciamento só cobre requisitos de projeto, como o controle de escopo.

**Apontar:** A linha 3, API, que cobre sete requisitos de produto; o rodapé da regra dos 100%.

**Transição:** Agora, o tempo.

### Slide 6: Cronograma e caminho crítico
**Fala sugerida:** JV  ·  **Tempo alvo:** 0:55  ·  **Palavras:** 127

> O cronograma tem 71 itens, 63 atividades e 8 marcos, 967 horas no total. Cada linha é uma entrega da EAP; o tom escuro é o realizado estimado e a linha vermelha, hoje. O caminho crítico, a fileira vermelha, é a corrente sem folga: 20 atividades e os 8 marcos, e quase todas são do backend, do contrato OpenAPI à sincronização. É por isso que o atraso do backend desloca o M8: restam cerca de 32 dias úteis de trabalho crítico para seis dias úteis de calendário. Sem cortar escopo, o M8 iria para janeiro. Um exemplo da cadeia: sem o contrato OpenAPI ninguém integra, sem autenticação não há cadastros, sem modelo publicado não se agenda e sem sincronização não existe revisão. Por isso a ordem importa.

**Apontar:** A fileira do caminho crítico e a linha de hoje; a faixa de baixo.

**Transição:** Quem executa tudo isso? Vamos aos recursos.

### Slide 7: Recursos e responsabilidades
**Fala sugerida:** AF  ·  **Tempo alvo:** 0:50  ·  **Palavras:** 113

> A equipe tem cinco pessoas e 960 horas de capacidade, cerca de 192 por pessoa. O organograma mostra o comitê e o orientador acima do gerente e as frentes de backend, web, mobile e qualidade. A matriz RACI cobre os 36 pacotes com um único aprovador por linha. O desequilíbrio é visível: o gerente, o Felipe, tem 11 responsabilidades e 21 aprovações e aparece em todos os 36 pacotes. Eu sou o único responsável pelo painel web, uma dependência de pessoa-chave. As respostas estão no plano de riscos: delegar aprovações, revisão cruzada e pareamento. Quem mais pode apoiar o web é o João Victor, que já é consultado no construtor de modelos.

**Apontar:** As barras de R, A e C por pessoa; os dois alertas à direita.

**Transição:** Com horas e pessoas definidas, chegamos ao custo.

### Slide 8: Custos e orçamento
**Fala sugerida:** GR  ·  **Tempo alvo:** 1:00  ·  **Palavras:** 139

> O orçamento tem 52 linhas, estimadas por três pontos, com média PERT. O custo base é R$ 47.714,83; somamos 10% de contingência e chegamos à linha de base de R$ 52.486,31; com a reserva gerencial de 5%, o orçamento total é R$ 54.872,05. É quase tudo mão de obra valorada, a R$ 45 e R$ 60 por hora: custo de oportunidade, não desembolso. O caixa de verdade é pequeno: R$ 669 esperados, R$ 374 no cenário mais provável e R$ 2.478,50 no pior caso. A curva S mostra o gasto planejado por sprint, e acompanhamos por EVM a cada marco. Desvio de até 10% do item é do gerente; acima de 5% do BAC, o orientador aprova; gasto novo de caixa acima de R$ 150 exige exceção formal. Tudo isso está na seção de controle de custos do orçamento.

**Apontar:** A escada: base, contingência, BAC, reserva, total; depois os três valores de caixa.

**Transição:** E a qualidade desse trabalho?

### Slide 9: Qualidade
**Fala sugerida:** GR  ·  **Tempo alvo:** 1:00  ·  **Palavras:** 137

> Para a qualidade usamos a Definição de Pronto por história e por camada e critérios de aceitação por marco, no formato dado, quando e então. Aplicamos as sete ferramentas a dados reais do GitHub e o achado principal é de processo, não de código: só 11% dos pull requests mergeados têm revisão registrada de outra pessoa e 0 de 518 critérios de aceitação foram marcados ao fechar as issues. O CI, quando existe, funciona: 97% dos merges com CI estavam verdes. Garantia audita o processo e controle mede o produto. A ação número um é proteger a branch develop: uma aprovação e CI verde para merge. Uma ressalva: a medida enxerga só a revisão registrada na plataforma. Revisão feita por chat ou pessoalmente não aparece, então o número é um alerta, não um julgamento sobre as pessoas.

**Apontar:** A primeira barra, em vermelho; a faixa de ação embaixo.

**Transição:** Esses achados alimentam o plano de riscos.

### Slide 10: Riscos
**Fala sugerida:** JV  ·  **Tempo alvo:** 1:05  ·  **Palavras:** 147

> Identificamos 22 riscos e 4 oportunidades, cada risco escrito como causa, risco e consequência. Pela matriz de probabilidade e impacto, 5 são de severidade alta, 13 média e 4 baixa; nove já se materializaram. À direita, os cinco maiores: falha de sincronização offline, backend sem responsável, backlog acima da capacidade, integração tardia e sobrecarga do gerente, cada um com resposta e dono. Os três primeiros se reforçam. Na parte quantitativa, o valor monetário esperado dos riscos que ainda podem ocorrer é R$ 6.635, acima da contingência de R$ 4.771,48; a simulação de Monte Carlo dá R$ 9.812 no P80. Como as horas não se compram, o excedente vira corte de escopo, não dinheiro. Cada risco tem gatilho e dono, e uma reunião de 20 minutos, semanal e a cada 48 horas nesta sprint, revisa a lista de observação. Há também quatro oportunidades, como usar mocks do contrato.

**Apontar:** Os chips vermelhos na matriz e as quatro caixas de EMV embaixo.

**Transição:** Riscos de pessoas pedem comunicação e engajamento.

### Slide 11: Comunicação e partes interessadas
**Fala sugerida:** GR  ·  **Tempo alvo:** 0:50  ·  **Palavras:** 115

> Mapeamos 13 partes interessadas. Sete têm poder alto: a coordenação, o professor Glauco, o comitê, o professor Deivison, o gerente e a equipe, mais a infraestrutura do campus. Os usuários finais têm interesse alto e poder baixo, e são personas fictícias da especificação. O plano tem 19 comunicações: planning, daily, review, demo de cada marco, relatório quinzenal, alinhamento semanal com o orientador e escalonamento em 24 horas. A maior lacuna é de engajamento dos usuários finais, que ainda nem viram o produto; o remédio realista é o teste com usuário-proxy nos marcos M3, M5 e M7. Quem mais precisa ser informado do atraso é a coordenação, e o aviso sai em até 24 horas.

**Apontar:** Os chips vermelhos no quadrante superior direito; a lacuna dos usuários.

**Transição:** Com tudo planejado, o que mostra o monitoramento hoje?

### Slide 12: Monitoramento e controle (situação real)
**Fala sugerida:** FM  ·  **Tempo alvo:** 1:25  ·  **Palavras:** 204

> Esta é a situação real em 18 de novembro, semana 15. Das 103 issues, 57 estão concluídas, 55%. O gráfico mostra o problema: S6, offline e sincronização, tem 2 de 13; S7, revisão, tem 2 de 14. Os marcos M6 e M7 não foram entregues e o M8 está em risco. O EVM da mão de obra dá SPI 0,53 e CPI 0,58, com uma ressalva: o custo real é hipótese, 12 horas por pessoa por semana, porque não há apontamento de horas. À direita, o que já funciona: o web tem 22 de 31 issues, com cadastros, QR, construtor de modelos e fila de revisão; o app tem 21 de 39, com checklist dinâmico, foto, QR, localização, SQLite e outbox; a API tem 14 de 41, e é lá que falta sincronização, evidências e revisão, com 21 issues sem responsável. A decisão: refazer a linha de base do backlog restante, aplicar já os itens 1 e 2 da ordem de corte, dar dono às 21 issues e proteger o núcleo. Mudanças entram por issue, com impacto avaliado e decisão do orientador. O TCPI de 3,08 diz que teríamos de render três vezes mais para fechar no orçamento: isso confirma o corte de escopo.

**Apontar:** As barras de S6 e S7; o cartão da API; o banner de decisão.

**Transição:** O que aprendemos com isso.

### Slide 13: Lições aprendidas
**Fala sugerida:** AF  ·  **Tempo alvo:** 0:50  ·  **Palavras:** 120

> Registramos cinco lições, cada uma com evidência e recomendação. Primeira: integração tardia; o login do app só foi integrado à API em 18 de setembro e a sincronização ainda não. Segunda: o backend ficou sem dono, 21 issues sem responsável e 88% dos commits de uma pessoa. Terceira: a Definição de Pronto é autodeclarada, nada a verifica. Quarta: prioridade desalinhada, o dashboard P1 foi concluído em 9 de novembro enquanto a sincronização não começou. Quinta: o PERT já dava cauda pesada para offline e sincronização, e se confirmou; riscos técnicos do caminho crítico merecem um protótipo antecipado e folga. Cada lição virou ação com dono e prazo no plano de qualidade, e a retrospectiva de cada sprint alimenta o registro.

**Apontar:** A coluna de evidências, com os números; depois a de recomendação.

**Transição:** Dessas lições vêm as decisões que defendemos.

### Slide 14: Decisões-chave justificadas
**Fala sugerida:** AF + JV + PD + GR  ·  **Tempo alvo:** 1:10  ·  **Palavras:** 169

> **AF:** Quatro decisões, cada uma com justificativa e com o custo que assumimos. Next.js em vez de Angular: a especificação aceita Angular ou React e o Next.js mantém a sessão no servidor, com o token fora do navegador; o custo é divergir do TAP, e o registro dessa decisão ainda está aberto na documentação.

> **JV:** Ordem de corte: o prazo e as 960 horas são fixos, então o que cede é o escopo, e já definimos o núcleo intocável: login, planejamento, checklist, foto, offline, sincronização e revisão. O custo é abrir mão de dashboard, tipos de resposta e PDF.

> **PD:** Outbox com idempotência: o SQLite é persistência operacional e reenviar a mesma operação não pode duplicar nem perder dados. É a parte mais complexa e a mais atrasada, mas é o coração do produto.

> **GR:** Contingência de 10% mais 5%: a primeira cobre riscos identificados, a segunda os desconhecidos e só a coordenação libera. O custo assumido é que o valor esperado dos riscos supera a contingência; o excedente vira corte de escopo.

**Apontar:** Para cada cartão: decisão, por quê, custo assumido.

**Transição:** Fechando.

### Slide 15: Conclusão e próximos passos
**Fala sugerida:** AF + FM  ·  **Tempo alvo:** 0:55  ·  **Palavras:** 126

> **AF:** Concluindo: o planejamento está integrado, porque os mesmos 36 pacotes sustentam cronograma, orçamento, RACI e riscos, e todos os números batem entre os artefatos. O atraso foi medido e não escondido, e tem resposta definida. Os próximos passos até 27 de novembro estão datados: proteger a develop e dar dono às 21 issues até 19; fechar o contrato de sincronização até 21; ensaiar sincronização e demonstração em 24; demonstrar de ponta a ponta em 26; e encerrar no M8 com aceite, lições aprendidas e relatório final. As datas vêm do plano de respostas a riscos e podem ser acompanhadas na reunião de risco.

> **FM:** Se o M8 não fechar tudo, entregamos o núcleo e registramos o restante como trabalho futuro. Obrigado, ficamos à disposição para as perguntas.

**Apontar:** A cadeia de artefatos; a linha do tempo; a faixa de encerramento.

**Transição:** Perguntas. Os slides de backup têm respostas prontas.

### Slide 16: Backup: perguntas difíceis  (backup)
> Slide de apoio para a rodada de perguntas. Respostas completas no roteiro.

**Apontar:** Usar apenas se a pergunta coincidir com uma das oito.

**Transição:** —

## 4. Perguntas prováveis do professor

Respostas curtas (30 a 60 segundos cada). A coluna *apoio* diz onde está a evidência; as oito primeiras mais difíceis também estão no slide 16.

**1. Por que o projeto está atrasado e o que muda?**

O atraso é real: 57 de 103 issues, S6 com 2/13 e S7 com 2/14, M6 e M7 sem entrega. Causas medidas: 21 issues do backend sem dono, integração tardia e capacidade fixa de 960 h para um backlog grande. O que muda já: dono para cada issue, nova linha de base do backlog restante, itens 1 e 2 da ordem de corte (dashboard e tipos de resposta) e núcleo protegido. Sem corte, o M8 iria para cerca de 06/01/2027.

*Apoio:* Slide 12; cronograma (Acompanhamento); riscos R02, R03, R14

**2. Por que Next.js em vez de Angular?**

A especificação aceita 'Angular/React' (PBI-003). O frontend foi feito em Next.js 16 porque mantém a sessão em cookie httpOnly e o acesso à API pelo servidor, deixando o token fora do navegador (RJ06); a equipe também já usa React no app (premissa). O custo é divergir do TAP de 30/09 e da rubrica 'Arquitetura Angular'. Por isso o risco R18 está registrado e o ADR-0008 (docs#3) precisa ser publicado e aceito pelo Prof. Glauco antes do M8.

*Apoio:* Slide 14; riscos R18; TAP (decisões e divergências)

**3. Por que estimar custos se o projeto é acadêmico?**

Porque o enunciado pede custos, estimativas e premissas explícitas quando não há dado real. Valoramos as horas a R$ 45 (desenvolvedor) e R$ 60 (gestão): custo de oportunidade, não desembolso. O caixa real é de R$ 374 (mais provável) a R$ 2.478,50 (pior caso). A estimativa serve para decidir escopo e prazo e para praticar EVM e reservas, não para pagar alguém.

*Apoio:* Slide 8; orçamento (premissas P2 a P4)

**4. Como vocês sabem o percentual realizado?**

O dado medido é o de issues fechadas por milestone de sprint: 57 de 103, 55%. O percentual por atividade é estimativa do gerente, calibrada para reproduzir a razão de issues de cada sprint (premissa P7 do cronograma). Há limites: issues fechadas em lote, critérios sem marcar e nenhum apontamento de horas. Por isso o AC do EVM é hipótese e o CPI de 0,58 é indicativo, não medição oficial. A rotina proposta é apontar horas por ID de atividade toda sexta.

*Apoio:* Slide 12; cronograma P7; orçamento (EVM)

**5. Como tratam o risco de sincronização?**

É o R06, o maior risco (severidade 0,26). Resposta: fechar o contrato de push e pull (docs#2), chave de idempotência única no banco, e testar os três cenários do AC-SYNC (envio, reenvio sem duplicidade, falha parcial) contra o backend real até 25/11. Dono: JV. Gatilhos: reenvio gera duplicado ou o push do backend sem PR até 21/11. Se o ensaio de 24/11 falhar, aplicam-se os itens 3 a 5 da ordem de corte, como detectar e bloquear conflitos.

*Apoio:* Slides 10 e 14; riscos R06; AC-SYNC

**6. Qual a diferença entre garantia e controle da qualidade?**

Garantia (processo 8.2) audita o processo: revisão cruzada de PR, folha de verificação do DoD, retrospectiva, revisão do contrato. Controle (8.3) mede o resultado e recomenda mudanças: CI obrigatório, testes dos fluxos críticos, gráficos p e I-MR, Pareto. A garantia pergunta 'estamos seguindo o processo certo?'; o controle pergunta 'o produto está dentro do critério?'.

*Apoio:* Slide 9; qualidade §2.4

**7. O que é o caminho crítico no projeto?**

É a corrente de atividades sem folga entre 10/08 e 27/11: 20 atividades e os 8 marcos, do repositório e contrato OpenAPI, passando por autenticação, modelos, execução, evidências, sincronização e revisão, até o teste final e a demonstração. Quase todas são do backend. Qualquer atraso nelas desloca o M8. Restam 32,5 dias úteis de trabalho crítico contra 6 de calendário.

*Apoio:* Slide 6; cronograma (Caminho crítico)

**8. Como seria o encerramento do projeto?**

Pacote 1.4: demonstração ponta a ponta no M8 segundo o AC-RELEASE (19 passos, sem editar o banco), aceite do comitê (PI-03) e da coordenação (PI-01), lições aprendidas consolidadas em docs/lessons-learned.md, relatório final e arquivo do repositório. O que não couber é registrado como trabalho futuro (portal do cliente, itens P1).

*Apoio:* Slide 15; EAP 1.4; plano de comunicação COM-18 e COM-19

**9. Por que contingência de 10% mais 5%, se o EMV passa disso?**

Os 10% cobrem riscos identificados e são liberados pelo gerente; os 5% cobrem desconhecidos e só a coordenação libera. O EMV dos riscos ainda possíveis (R$ 6.635) e o P80 da simulação (R$ 9.812) superam os R$ 4.771,48. Como a capacidade é fixa em horas, reserva financeira não compra prazo: o excedente é tratado por corte de escopo (RJ07) ou pedido formal da reserva gerencial.

*Apoio:* Slides 10 e 14; riscos §6

**10. Por que a EAP é por entregas e não por fases?**

Porque o PMBOK pede decomposição por entregas e é nelas que se penduram cronograma, orçamento e RACI. Misturamos três critérios, como no exemplo da aula: gestão (1), componentes do produto (2 a 5) e verificação e entrega (6 e 7). Todo elemento é substantivo ou particípio e há 36 pacotes sem lacuna.

*Apoio:* Slide 5; EAP 'Como a EAP foi construída'

**11. Como tratam mudanças de escopo?**

Qualquer pessoa abre uma issue com rótulo mudanca-de-escopo descrevendo o que muda, o motivo e o impacto em prazo, escopo e qualidade. O gerente avalia, aplica a ordem de corte (RJ07) e o Prof. Glauco decide como product owner; a decisão fica registrada e a versão do plano é atualizada. Os 10 itens P1 só entram por esse caminho.

*Apoio:* Slide 12; plano de comunicação COM-10

**12. Por que não usar uma solução pronta, como SafetyCulture ou Kobo?**

O projeto existe para integrar as disciplinas de mobile, backend e web e é avaliado por marcos e por domínio individual, então construir é o objetivo. Reconhecemos que, para uma operação real, uma solução pronta pode ser mais madura. O benchmarking mostra onde o FieldOps se encaixa: checklist versionado com snapshot, QR por equipamento, revisão formal e código próprio, mas ainda como MVP.

*Apoio:* Slide 4; benchmarking (fontes oficiais)

**13. Como evitam que o gerente seja ponto único de falha?**

A RACI mostra o problema: Felipe tem 11 R e 21 A e aparece nos 36 pacotes. Respostas: delegar a revisão dos PRs do app a PD, seed e documentação a JV, passar o A de seis pacotes a JV e GR (cenário B do RACI), janela fixa de gestão e revisão cruzada dos pacotes em que ele é A/R (5.1, 5.3 e 5.5).

*Apoio:* Slide 7; RACI §4.4; riscos R04

**14. Como garantem a consistência entre os artefatos?**

Os números saem de uma base única (códigos da EAP, datas, horas por pessoa) e cada artefato foi conferido por script: 36 pacotes, 71 itens, 967 h, 52 linhas de orçamento, 22 riscos. A apresentação também lê os arquivos e interrompe a geração se um número divergir. Há uma diferença conhecida: a coleta do GitHub feita depois mostra 59/103; usamos 57/103 do levantamento-base e explicamos a diferença.

*Apoio:* Todos; qualidade §3

**15. Os 57/103 do status e os 59/103 da análise de qualidade divergem?**

Sim, por duas issues do frontend (#19 e #21) fechadas às 14h30 UTC de 18/11, depois do levantamento usado nos documentos de gestão. Usamos 57/103 de forma consistente em riscos, cronograma e apresentação e registramos a diferença no documento de qualidade.

*Apoio:* Qualidade §3; riscos §9

## 5. Orientações de condução

- Começar pelo número, não pela ferramenta: cada slide tem uma frase-título que é a mensagem; a fala só a explica.
- O atraso é dito uma vez, com dado, no slide 3 (cores dos marcos), de novo no 6 (caminho crítico) e resolvido no 12. Não minimizar nem pedir desculpas: mostrar medição e decisão.
- Ao falar de custo, repetir sempre que são horas valoradas (hipótese), não desembolso.
- Ao falar de percentual realizado e de CPI, repetir a ressalva: o custo real é hipótese porque não há apontamento de horas.
- No benchmarking, dizer o que é confirmado em documentação oficial e o que é alegação do fornecedor, e fechar com a ressalva de MVP acadêmico.
- Cada integrante deve saber responder também sobre os slides dos colegas; o RACI não dispensa o domínio individual que a disciplina avalia.
- Ensaiar duas vezes com cronômetro; o tempo estimado pela contagem de palavras é referência, não garantia.

## 6. Verificações feitas

- Todos os números do roteiro e dos slides foram conferidos por script contra os artefatos (`aula-*/*.md`): 36 pacotes, 71 itens de cronograma (63 atividades e 8 marcos), 967 h, 20 atividades críticas, 22 riscos e 4 oportunidades, top 5 (R06, R03, R02, R14, R04), R$ 47.714,83 / R$ 52.486,31 / R$ 54.872,05, 57/103 issues, SPI 0,53 e CPI 0,58.
- Contagem de palavras das falas dos slides 1 a 15: 2027; estimativa 14:29 a 140 palavras por minuto.
- Divergência conhecida e explicada: a coleta do GitHub feita depois do levantamento-base mostra 59/103 issues (duas issues do frontend fechadas às 14h30 UTC de 18/11); a apresentação usa 57/103, como cronograma, riscos e relatório.