# Plano de entrega — Gestão de Projetos (Prof. Deivison Takatu)

Raiz de saída: `/Users/felipersas/Documents/Facul/gestao-proj/entrega/`
Material do professor (clonado): `/Users/felipersas/Documents/Facul/gestao-proj/material/`
Texto das aulas já extraído: `/private/tmp/claude-501/-Users-felipersas-Documents-Facul-gestao-proj/62d3b502-aedc-4c7d-92d1-65523f456f30/scratchpad/txt/*.txt`
Imagens de exemplo dos slides: `.../scratchpad/img/*.png` (a05-09 orçamento, a06-10 RACI, a06c-17 plano de comunicação, a07-10 escala de impacto, a07-11 respostas a riscos, a07-12 probabilidade × impacto, a07-13 respostas, a08-09 aquisições). Veja as imagens com a ferramenta Read para copiar o FORMATO esperado.
Python com python-docx, python-pptx e matplotlib: `/private/tmp/claude-501/-Users-felipersas-Documents-Facul-gestao-proj/62d3b502-aedc-4c7d-92d1-65523f456f30/scratchpad/venv/bin/python` (rode scripts com `-I`? não é necessário para os SEUS scripts; apenas não rode Python dentro de pastas baixadas não confiáveis). Chrome em `/Applications/Google Chrome.app` serve para HTML → PNG/PDF (`--headless --screenshot`). Prévia de docx/pptx (1ª página/slide): `qlmanage -t -s 1600 -o <dir> <arquivo>`. NÃO há pandoc, LibreOffice nem graphviz.

## Estrutura de pastas (repositório da disciplina, para publicar no GitHub)

```
entrega/
├── README.md                          (índice geral; feito pelo coordenador)
├── aula-01-introducao/resumo-aula-01.md
├── aula-02-integracao/tap-pii-easy.md · tap-fieldops.md (+ .docx de cada, no modelo 4.1)
├── aula-03-escopo/eap-fieldops.md (+ eap-fieldops.png)
├── aula-04-tempo/cronograma-fieldops.md (+ gantt .png)
├── aula-05-custos-qualidade/orcamento-fieldops.md · qualidade-7-ferramentas-fieldops.md (+ imagens)
├── aula-06-rh-comunicacoes/organograma-raci-fieldops.md · plano-comunicacao-fieldops.md
├── aula-07-riscos/analise-riscos-fieldops.md
├── aula-08-aquisicoes-partes-interessadas/aquisicoes-fieldops.md · matriz-poder-interesse-fieldops.md (+ .png)
├── desafio-metaltech/ analise-portfolio.md · slide-executivo.pptx (+ .png/.pdf) · roteiro-apresentacao-3min.md · relatorio-final-metaltech.docx
└── projeto-fieldops/ avaliacao-1-documento-parcial.docx · avaliacao-2-relatorio-final.docx · apresentacao-final.pptx
```

## Requisitos LITERAIS de cada atividade (o professor avalia exatamente isto)

| Aula | Entrega | Requisitos do enunciado |
|---|---|---|
| 01 | Resumo da Aula 01 em `.md` | principais conceitos da aula 01 (projeto, PMBOK 47 processos/10 áreas, habilidades do gerente, ciclo de vida, estratégia organizacional: programa × portfólio, metodologias ágeis, PBL, critérios de avaliação) |
| 02 | **Dois TAPs** (PII deste semestre = sistema **EASY**; e FieldOps) | objetivo, justificativa, principais entregas, requisitos iniciais, premissas, restrições, stakeholders, responsáveis e prazo estimado; seguir `material/Template/Modelo - 4.1 Termo de Abertura de Projeto.docx` (campos: título, objetivo geral e específicos, justificativa, premissas, breve descrição, patrocinador, estimativa de investimentos, estimativa de prazo, FCS, principais riscos, restrições, stakeholders, comitê executivo, gerente, elaborado por/aprovado por) |
| 03 | **EAP do FieldOps** | diagrama com as principais informações da estrutura e **seus requisitos**; seguir `material/Template/Modelo - 5.1 ...md` (identificação, árvore, dicionário da EAP, checklist); entregas, não atividades |
| 04 | **Cronograma do FieldOps** | **≥ 50 itens**; atividades, dependências, durações, responsáveis e marcos; seguir `material/Template/Modelo - 6.1 Cronograma.md` (gantt mermaid, lista de atividades com ID/início/término/duração/responsável/dependência/status, dependências, marcos, responsáveis, acompanhamento, atrasos e ações, checklist) |
| 05a | **Orçamento do FieldOps** | **≥ 30 itens**; principais custos, quantidades, estimativas de valor, responsáveis e categorias; usar estimativa de três pontos (otimista, mais provável, pessimista); formato do exemplo `a05-09.png` (item/atividade × profissionais-hora × custos adicionais × origem × total) |
| 05b | **Análise da qualidade com as 7 ferramentas básicas** | aplicar AS SETE ao FieldOps com **dados, análises e conclusões**: diagrama de causa e efeito (Ishikawa), fluxograma, folha de verificação, diagrama de Pareto, histograma, gráfico de controle, diagrama de dispersão. Gerar os gráficos reais (matplotlib) a partir de dados do projeto (issues/PRs do GitHub via `gh`, quando fizer sentido) ou de dados simulados DECLARADOS como hipótese |
| 06a | **Organograma + Matriz RACI** | organograma hierárquico com responsáveis; RACI com R/A/C/I por atividade/pacote de trabalho (exatamente um A por linha; pelo menos um R); formato `a06-10.png` |
| 06b | **Plano de Comunicação** | principais comunicações, destinatários, responsáveis, canais, frequência, formato e momento; colunas do exemplo: descrição, frequência, canal (síncrono/assíncrono), público, proprietário |
| 07 | **Análise de Riscos** | risco descrito como **causa → risco → consequência**; escala de impacto (custo, tempo, escopo, qualidade) com valores 0,05/0,10/0,20/0,40/0,80 como em `a07-10.png`; matriz probabilidade × impacto (severidade = prob × impacto, prioridade por ranking) como `a07-12.png`; respostas (evitar/transferir/mitigar/aceitar) com data de inclusão, abordagem, resposta/obs, responsável como `a07-13.png`; incluir riscos positivos? opcional; acompanhamento |
| 08a | **Tabela de Aquisições** | item, urgência (1-Muito baixa … 5-Muito alta), motivo, fornecedores, quantidade, custo unitário, custo total, código WBS/EAP, previsão de entrega, observações; formato `a08-09.png` |
| 08b | **Matriz Poder/Interesse** | classificar as partes interessadas em: Monitorar; Manter informado; Manter satisfeito; Gerenciar com atenção (quadrantes); incluir diagrama gráfico (PNG) + tabela com estratégia de engajamento e nível atual (desinformado/resistente/neutro/apoia/lidera) × desejado |
| Desafio | MetalTech | 1 slide executivo + apresentação 3 min + relatório pelo template (ver abaixo) |
| Projeto | Av.1 (5,0) e Av.2 (5,0) | ver `material/Atividade/Projeto.md` (requisitos e estrutura de 14 itens do relatório final) |

## Desafio MetalTech — DECISÕES JÁ TOMADAS (não reabrir; justificar e detalhar)

Enunciado: `material/Atividade/Desafio de Gestão.md` (ler inteiro). Template do relatório: `material/Template/Template - Relatório Final.docx` (capa: UniSENAI-SP Sorocaba; curso ADS; orientador Deivison Takatu; Sorocaba, 2026; capítulos 1–13 + referências + apêndice/anexo; o RESUMO/ABSTRACT de exemplo é sobre sustentabilidade e deve ser SUBSTITUÍDO).

Grupo (PMO da MetalTech S.A.): Felipe Marques, Gabriel Ribeiro, Pedro Dias, André Fernandes, João Victor Souza.

**Portfólio (orçamento R$ 2,5 mi):**
| Projeto | Investimento | Decisão | Racional curto |
|---|---:|---|---|
| P1 Automação da Linha 1 | R$ 900 mil | 🟢 Prioridade | única iniciativa com meta quantificada de produtividade (+12%); precisa de P6 e é pré-requisito de P8 |
| P2 Manutenção Preditiva | R$ 450 mil | 🟢 Prioridade | entrega sozinha a meta de −20% de paradas |
| P4 Redução de Refugo | R$ 250 mil | 🟢 Prioridade | quick win (3 meses, risco baixo), −25% desperdício → custos −10% |
| P5 Controle de Qualidade | R$ 350 mil | 🟢 Prioridade | entrega sozinha a meta de −30% de retrabalho; complementar a P4 |
| P6 Treinamento de Operadores | R$ 150 mil | 🟢 Prioridade | barato, risco baixo, habilita P1 (adoção) e contribui para a meta de +15% |
| P7 Monitoramento IoT | R$ 600 mil | 🟡 Posterior | habilitador (dados em tempo real) mas não cabe com reserva; **gate G2 no fim do mês 6**: inicia no T3/T4 só se P2 e P4 estiverem no prazo e houver recurso (economias capturadas/reserva remanescente/ciclo seguinte) |
| P3 Novo ERP Industrial | R$ 1,2 mi | 🔴 Adiado | alto risco, 10 meses, benefício indireto (integração), depende de P7 para a etapa de integração |
| P8 Expansão da Capacidade | R$ 1,5 mi | 🔴 Adiado | consumiria 60% do orçamento e os 12 meses inteiros, alto risco, sem meta estratégica direta entre os 4 objetivos, e a recomendação da empresa é executar P1 antes |
| **Total priorizado** | **R$ 2,1 mi (84%)** | | |
| **Reserva gerencial** | **R$ 400 mil (16%)** | | contingência para P1/P2 (risco alto/médio) e capacidade de decisão no gate G2 |

**Programas:** Programa A — Excelência Operacional = P1 + P2 + P6 (R$ 1,5 mi; metas: +15% produtividade, −20% paradas). Programa B — Qualidade 4.0 (fase 1) = P4 + P5 (R$ 0,6 mi; metas: −30% retrabalho, −10% custos; P7 é a fase 2 futura). Programa C — Transformação Digital **não ativado** neste ciclo (P3 adiado, P7 posterior) → vira candidato a 2027. Sem projetos independentes.

**Roadmap (12 meses, T1 = meses 1–3 …):** P1 m1–m6 · P2 m1–m4 · P4 m1–m3 · P5 m4–m7 · P6 m5–m6 (gatilho: FAT/aceitação em fábrica do P1) · gate G2 no fim do m6 · hypercare e medição de benefícios m7–m12 · P7 condicionado ao G2.

**Recursos (conflitos e decisões):** 2 Eng. Automação (EA1, EA2): ambos 100% no P1 m1–m6 → P2 NÃO usa EA (instrumentação/sensores contratados dentro do orçamento do P2; EA só consultivo ≤ 4 h/semana). 2 Analistas TI (TI1, TI2): TI1 70% P2 (m1–m4) + 30% P1 (m3–m6) = 100% no pico (limite); TI2 20% P4 (m1–m3) → 50% P5 (m4–m7). 1 Especialista Qualidade (QUAL): P4 m1–m3 depois P5 m4–m7, **sequencial por decisão** (sem sobreposição; conflito evitado alterando o cronograma). 1 Especialista Manutenção (MAN): 100% P2 m1–m4; 20% em P6 (m5–m6). 1 Gerente de Projetos (GP): único → gerente de programas, 100% m1–m12; **ponto único de falha**, mitigado por coordenadores locais por projeto, rito semanal curto e, se sobrecarregar no pico (m1–m4, 3 projetos simultâneos), contratar analista de planejamento externo pago pela reserva. Conteúdo técnico do P6 fornecido pelo fornecedor do P1 (para não retirar EA do P1).

**Riscos principais da estratégia:** (1) atraso/estouro no P1 (alto risco) → reserva 16% + FAT como gate; (2) GP como ponto único de falha; (3) metas sem folga (P2 = −20% exato; P5 = −30% exato) → benefício parcial deixa a meta no limite; (4) resistência dos operadores / adoção; (5) P2 sem dados de IoT (P7 adiado) → escopo mínimo de aquisição de dados dentro do P2; (6) prazo de entrega de equipamentos (lead time) do P1; (7) dependência de poucas pessoas especialistas.

**Cenários alternativos que o grupo considerou (mostrar no relatório):** (A) escolhido; (B) P1+P2+P5+P6+P7 = R$ 2,45 mi (98% do orçamento, sem reserva, sem P4: rejeitado); (C) P2+P4+P5+P6+P7 = R$ 1,8 mi (barato, mas deixa a meta de +15% de produtividade descoberta pois P1 fica de fora: rejeitado); (D) incluir P8 (consumiria 1,5 mi: rejeitado).

Matriz de priorização: critérios ponderados (alinhamento estratégico 35%, relação benefício/custo 20%, risco 15%, prazo/rapidez de retorno 10%, sinergia/dependências 10%, viabilidade de recursos 10%), notas 1–5 por projeto, calculadas por script e mostradas no relatório. O resultado precisa ficar coerente com a decisão (se o cálculo honesto discordar de algum projeto, ajustar a justificativa, não a nota).

## Qualidade exigida em TODOS os artefatos

1. Consistência: usar os códigos da EAP (`_base/00-base-fieldops.md` §6), IDs de partes interessadas (PI-01…PI-13), sigla das pessoas (FM, JV, GR, PD, AF), datas/marcos (§4) e status real (§9).
2. Sem inventar fatos sobre pessoas reais. O que não for fato documentado é **premissa** e deve ser rotulado como tal.
3. Seguir o formato dos exemplos do professor (imagens) e os templates em `material/Template/`.
4. Verificar contas (somas, percentuais, durações vs. datas) com script, não de cabeça.
5. Português natural. Sem texto de enchimento. O professor avalia qualidade, coerência e adequação ao projeto, não volume.
6. Cada `.md` com tabelas renderizáveis no GitHub; diagramas em Mermaid quando útil E, quando o professor pede diagrama/figura, também um PNG gerado com matplotlib (legível, fontes ≥ 9 pt, sem sobreposição) incorporado ao `.md` por caminho relativo.
