# Gestão de Projetos — Atividades da disciplina

**Curso:** Análise e Desenvolvimento de Sistemas — UniSENAI-SP, Campus Sorocaba (Santa Rosália)
**Disciplina:** Gestão de Projetos — Prof. Me. Deivison S. Takatu
**Projeto de referência:** FieldOps — Plataforma de Inspeção em Campo
**Grupo:** Felipe Marques (gerente do projeto), Gabriel Ribeiro, Pedro Dias, André Fernandes e João Victor Souza

Este repositório reúne as atividades das aulas, o Desafio de Gestão de Portfólio (MetalTech S.A.) e o Projeto de duas avaliações. Todos os artefatos do FieldOps partem de uma mesma base de dados (EAP, equipe, calendário, partes interessadas), por isso os códigos, valores e datas se repetem de um documento para outro.

## Atividades por aula

| Aula | Atividade | Arquivo |
|---|---|---|
| 01 | Resumo da Aula 01 | [resumo-aula-01.md](aula-01-introducao/resumo-aula-01.md) |
| 02 | Termo de Abertura do PII (sistema EASY) | [tap-pii-easy.md](aula-02-integracao/tap-pii-easy.md) · [.docx](aula-02-integracao/tap-pii-easy.docx) |
| 02 | Termo de Abertura do FieldOps | [tap-fieldops.md](aula-02-integracao/tap-fieldops.md) · [.docx](aula-02-integracao/tap-fieldops.docx) |
| 03 | EAP do FieldOps (7 entregas, 36 pacotes, requisitos) | [eap-fieldops.md](aula-03-escopo/eap-fieldops.md) |
| 04 | Cronograma (71 itens, caminho crítico, status em 18/11/2026) | [cronograma-fieldops.md](aula-04-tempo/cronograma-fieldops.md) |
| 05 | Orçamento (52 itens, estimativa de três pontos) | [orcamento-fieldops.md](aula-05-custos-qualidade/orcamento-fieldops.md) |
| 05 | Qualidade com as 7 ferramentas básicas (dados reais do GitHub) | [qualidade-7-ferramentas-fieldops.md](aula-05-custos-qualidade/qualidade-7-ferramentas-fieldops.md) |
| 06 | Organograma e Matriz RACI | [organograma-raci-fieldops.md](aula-06-rh-comunicacoes/organograma-raci-fieldops.md) |
| 06 | Plano de Comunicação | [plano-comunicacao-fieldops.md](aula-06-rh-comunicacoes/plano-comunicacao-fieldops.md) |
| 07 | Análise de Riscos | [analise-riscos-fieldops.md](aula-07-riscos/analise-riscos-fieldops.md) |
| 08 | Gerenciamento das Aquisições | [aquisicoes-fieldops.md](aula-08-aquisicoes-partes-interessadas/aquisicoes-fieldops.md) |
| 08 | Matriz de Poder/Interesse | [matriz-poder-interesse-fieldops.md](aula-08-aquisicoes-partes-interessadas/matriz-poder-interesse-fieldops.md) |

## Desafio de Gestão de Portfólio e Programas (MetalTech S.A.)

| Entrega | Arquivo |
|---|---|
| Slide executivo (1 slide) | [slide-executivo.pptx](desafio-metaltech/slide-executivo.pptx) · [PDF](desafio-metaltech/slide-executivo.pdf) · [PNG](desafio-metaltech/slide-executivo.png) |
| Roteiro da apresentação de 3 minutos | [roteiro-apresentacao-3min.md](desafio-metaltech/roteiro-apresentacao-3min.md) |
| Análise do portfólio (matriz de priorização, cenários, recursos, roadmap, riscos) | [analise-portfolio.md](desafio-metaltech/analise-portfolio.md) |
| Relatório final (modelo do professor) | [relatorio-final-metaltech.docx](desafio-metaltech/relatorio-final-metaltech.docx) |

## Projeto — Avaliações 1 e 2 (FieldOps)

| Avaliação | Entrega | Arquivo |
|---|---|---|
| 1 | Documento parcial: termo de abertura, partes interessadas e comunicação, escopo e EAP, cronograma e recursos | [avaliacao-1-documento-parcial.docx](projeto-fieldops/avaliacao-1-documento-parcial.docx) |
| 2 | Relatório final consolidado (estrutura de 14 itens) | [avaliacao-2-relatorio-final.docx](projeto-fieldops/avaliacao-2-relatorio-final.docx) |
| 2 | Apresentação final e roteiro | [apresentacao-final.pptx](projeto-fieldops/apresentacao-final.pptx) · [roteiro](projeto-fieldops/roteiro-apresentacao-final.md) |

## Formatos disponíveis

Todo artefato está em mais de um formato, com o mesmo nome de arquivo na mesma pasta:

- `.md` (Markdown): formato pedido na Aula 01 e usado nos modelos do professor (EAP e Cronograma). Renderiza no GitHub, com os diagramas Mermaid.
- `.docx` (Word) e `.pdf`: versões geradas a partir do `.md` para entrega em documento. Os diagramas Mermaid viram imagens e as tabelas largas ficam em página paisagem.
- Os termos de abertura, o relatório do desafio e as avaliações 1 e 2 já eram `.docx` (modelos 4.1 e Relatório Final); ganharam o `.pdf` correspondente.
- Para regerar as versões a partir dos `.md`: `python3 _base/gerar_exportacoes.py` (precisa de pandoc, Google Chrome e python-docx).

## Como ler os artefatos

- Os `.md` usam tabelas e diagramas Mermaid que o GitHub renderiza. Os gráficos estão em PNG na mesma pasta de cada atividade.
- Os scripts que geram contas e gráficos estão nas pastas `scripts/` de cada atividade, com os dados em `dados/` quando há coleta do GitHub.
- Valores monetários são **hipóteses de valoração** do esforço da equipe: o FieldOps é um projeto acadêmico sem investimento financeiro direto (ver o TAP).
- Os papéis de cada integrante nos artefatos (RACI, cronograma) foram propostos a partir dos repositórios e devem ser confirmados pelo grupo.
- O status de 18/11/2026 vem dos milestones e issues dos repositórios da organização FieldOps-Project.

## Estrutura

```
aula-01-introducao/            aula-05-custos-qualidade/
aula-02-integracao/            aula-06-rh-comunicacoes/
aula-03-escopo/                aula-07-riscos/
aula-04-tempo/                 aula-08-aquisicoes-partes-interessadas/
desafio-metaltech/             projeto-fieldops/
_base/   (base de fatos e plano de entrega usados para manter a consistência)
```
