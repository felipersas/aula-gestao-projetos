#!/usr/bin/env python3
"""Gera roteiro-apresentacao-final.md a partir de roteiro_dados.py (mesmas falas das notas do pptx)."""
import re
from pathlib import Path

from roteiro_dados import ROT, NOMES, PERGUNTAS

RAIZ = Path(__file__).resolve().parent.parent
WPS = 140 / 60.0  # palavras por segundo (140 palavras por minuto, fala clara com apoio de slide)

TITULOS = {
    1: "Capa", 2: "Problema e proposta", 3: "Abordagem de gestão", 4: "Benchmarking", 5: "EAP e rastreabilidade",
    6: "Cronograma e caminho crítico", 7: "Recursos e responsabilidades", 8: "Custos e orçamento", 9: "Qualidade",
    10: "Riscos", 11: "Comunicação e partes interessadas", 12: "Monitoramento e controle (situação real)",
    13: "Lições aprendidas", 14: "Decisões-chave justificadas", 15: "Conclusão e próximos passos", 16: "Backup: perguntas difíceis",
}


def palavras(t):
    return len(re.findall(r"\w+(?:[,.]\w+)*", t, flags=re.UNICODE))


def mmss(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


def main():
    linhas = []
    tot_pal = 0
    tot_seg = 0
    por_pessoa = {k: 0.0 for k in NOMES}
    slides_pessoa = {k: [] for k in NOMES}
    quadro = []
    for n in range(1, 16):
        r = ROT[n]
        pal = sum(palavras(t) for _, t in r["fala"])
        est = pal / WPS
        tot_pal += pal
        tot_seg += r["seg"]
        quem = list(dict.fromkeys(q for q, _ in r["fala"]))
        for q, t in r["fala"]:
            por_pessoa[q] += palavras(t) / WPS
            if n not in slides_pessoa[q]:
                slides_pessoa[q].append(n)
        quadro.append((n, TITULOS[n], r["seg"], est, pal, quem))
    est_total = tot_pal / WPS

    L = []
    ap = L.append
    ap("# Roteiro da apresentação final: FieldOps\n")
    ap("| Campo | Informação |\n|---|---|")
    ap("| **Projeto** | FieldOps: Plataforma de Inspeção em Campo (MVP) |")
    ap("| **Disciplina** | Gestão de Projetos, Prof. Me. Deivison S. Takatu, UniSENAI-SP Sorocaba |")
    ap("| **Grupo** | Felipe Marques (FM), João Victor Souza (JV), Gabriel Ribeiro (GR), Pedro Dias (PD), André Fernandes (AF) |")
    ap("| **Material** | `apresentacao-final.pptx` (16 slides: 15 principais + 1 de backup; notas do orador em cada slide) e `apresentacao-final.pdf` |")
    ap("| **Duração-alvo** | 15 minutos de fala + perguntas |")
    ap("| **Data-base dos números** | 18/11/2026 |")
    ap("| **Versão** | 1.0 |\n")
    ap("> **Sobre a divisão de falas.** Quem fala em cada slide é uma **sugestão**, equilibrada por tempo e por afinidade com o conteúdo (por exemplo, JV fala do caminho crítico e do risco de sincronização, que são do backend). O grupo pode trocar sem alterar o texto: as falas estão escritas na primeira pessoa do plural.\n")
    ap("## 1. Quadro de tempo (15 minutos)\n")
    ap(f"Velocidade usada: {int(WPS * 60)} palavras por minuto. A contagem de palavras e a estimativa de tempo foram feitas por script sobre as falas abaixo (mesmo texto das notas do pptx). O slide 16 é só de apoio e não entra no tempo.\n")
    ap("| Slide | Assunto | Quem fala (sugestão) | Tempo alvo | Palavras | Estimativa pela contagem | Acumulado |")
    ap("|---:|---|---|---:|---:|---:|---:|")
    acum = 0
    for n, t, seg, est, pal, quem in quadro:
        acum += seg
        ap(f"| {n} | {t} | {', '.join(quem)} | {mmss(seg)} | {pal} | {mmss(est)} | {mmss(acum)} |")
    ap(f"| **Total** | | | **{mmss(tot_seg)}** | **{tot_pal}** | **{mmss(est_total)}** | |\n")
    ap("O total fica dentro de 15 minutos com folga de cerca de 30 segundos para transições e respiração. Se estourar no ensaio, cortar nesta ordem: (1) a lista de fontes no slide 4, (2) as respostas do slide 8 sobre alçadas, (3) o detalhe de gatilhos no slide 12. Não cortar o slide 12 nem o slide 14, que sustentam o critério de justificativa das decisões.\n")
    ap("## 2. Divisão sugerida entre os integrantes\n")
    ap("| Integrante | Slides | Tempo de fala (estimado) | Por quê (sugestão) |")
    ap("|---|---|---:|---|")
    why = {
        "FM": "gerente; conta o problema, apresenta a situação real, a decisão e fecha",
        "JV": "líder técnico do backend; EAP, caminho crítico, risco de sincronização e ordem de corte",
        "GR": "custos, qualidade e partes interessadas; contingência",
        "PD": "abre a apresentação; processo de gestão no GitHub, benchmarking e outbox (offline)",
        "AF": "recursos (pessoa-chave do web), lições, Next.js e conclusão",
    }
    for k in ["FM", "JV", "GR", "PD", "AF"]:
        sl = ", ".join(str(x) for x in sorted(slides_pessoa[k]))
        ap(f"| {k} {NOMES[k]} | {sl} | {mmss(por_pessoa[k])} | {why[k]} |")
    ap("")
    ap(f"Tempo de fala por pessoa entre {mmss(min(por_pessoa.values()))} e {mmss(max(por_pessoa.values()))}: diferença máxima de {mmss(max(por_pessoa.values()) - min(por_pessoa.values()))}. Na rodada de perguntas, quem é dono do tema responde primeiro (coluna *apoio* da seção 4 indica o slide e o artefato).\n")
    ap("## 3. Roteiro slide a slide\n")
    for n in range(1, 17):
        r = ROT[n]
        ap(f"### Slide {n}: {TITULOS[n]}" + ("  (backup)" if n == 16 else ""))
        quem = " + ".join(dict.fromkeys(q for q, _ in r["fala"]))
        if n < 16:
            ap(f"**Fala sugerida:** {quem}  ·  **Tempo alvo:** {mmss(r['seg'])}  ·  **Palavras:** {sum(palavras(t) for _, t in r['fala'])}\n")
        for q, t in r["fala"]:
            pre = f"**{q}:** " if len(r["fala"]) > 1 else ""
            ap(f"> {pre}{t}\n")
        ap(f"**Apontar:** {r['apontar']}\n")
        ap(f"**Transição:** {r['transicao']}\n")
    ap("## 4. Perguntas prováveis do professor\n")
    ap("Respostas curtas (30 a 60 segundos cada). A coluna *apoio* diz onde está a evidência; as oito primeiras mais difíceis também estão no slide 16.\n")
    for i, (q, a, ap_) in enumerate(PERGUNTAS, 1):
        ap(f"**{i}. {q}**\n")
        ap(f"{a}\n")
        ap(f"*Apoio:* {ap_}\n")
    ap("## 5. Orientações de condução\n")
    for t in [
        "Começar pelo número, não pela ferramenta: cada slide tem uma frase-título que é a mensagem; a fala só a explica.",
        "O atraso é dito uma vez, com dado, no slide 3 (cores dos marcos), de novo no 6 (caminho crítico) e resolvido no 12. Não minimizar nem pedir desculpas: mostrar medição e decisão.",
        "Ao falar de custo, repetir sempre que são horas valoradas (hipótese), não desembolso.",
        "Ao falar de percentual realizado e de CPI, repetir a ressalva: o custo real é hipótese porque não há apontamento de horas.",
        "No benchmarking, dizer o que é confirmado em documentação oficial e o que é alegação do fornecedor, e fechar com a ressalva de MVP acadêmico.",
        "Cada integrante deve saber responder também sobre os slides dos colegas; o RACI não dispensa o domínio individual que a disciplina avalia.",
        "Ensaiar duas vezes com cronômetro; o tempo estimado pela contagem de palavras é referência, não garantia.",
    ]:
        ap(f"- {t}")
    ap("")
    ap("## 6. Verificações feitas\n")
    ap("- Todos os números do roteiro e dos slides foram conferidos por script contra os artefatos (`aula-*/*.md`): 36 pacotes, 71 itens de cronograma (63 atividades e 8 marcos), 967 h, 20 atividades críticas, 22 riscos e 4 oportunidades, top 5 (R06, R03, R02, R14, R04), R$ 47.714,83 / R$ 52.486,31 / R$ 54.872,05, 57/103 issues, SPI 0,53 e CPI 0,58.")
    ap(f"- Contagem de palavras das falas dos slides 1 a 15: {tot_pal}; estimativa {mmss(est_total)} a {int(WPS * 60)} palavras por minuto.")
    ap("- Divergência conhecida e explicada: a coleta do GitHub feita depois do levantamento-base mostra 59/103 issues (duas issues do frontend fechadas às 14h30 UTC de 18/11); a apresentação usa 57/103, como cronograma, riscos e relatório.")
    (RAIZ / "roteiro-apresentacao-final.md").write_text("\n".join(L), encoding="utf-8")
    print(f"palavras={tot_pal} estimativa={mmss(est_total)} alvo={mmss(tot_seg)} perguntas={len(PERGUNTAS)}")
    for k, v in por_pessoa.items():
        print(k, mmss(v), slides_pessoa[k])
    for n, t, seg, est, pal, quem in quadro:
        print(n, seg, round(est), pal, quem)


if __name__ == "__main__":
    main()
