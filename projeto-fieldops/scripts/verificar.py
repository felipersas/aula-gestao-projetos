#!/usr/bin/env python3
"""Conferencia final dos dois .docx: restos do template, ordem dos capitulos, numeracao de legendas, numeros-chave."""
import re, sys
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn

RAIZ = Path(__file__).resolve().parent.parent
PROIB = ["<NOME>", "<TÍTULO>", "sustentabilidade", "Sustentabilidade", "Amazônia", "Amazonia", "MetalTech", "Green Computing", "@Q:", "@T:", "@F:", "%d", "%s", "**", "__", "None"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿️]")


def texto_total(doc):
    partes = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                partes.append(c.text)
    return "\n".join(partes)


def confere(arq, capitulos, chaves, ausentes_ok=()):
    doc = Document(str(arq))
    txt = texto_total(doc)
    print("==", arq.name)
    erros = 0
    for p in PROIB:
        if p in txt and p not in ausentes_ok:
            idx = txt.index(p)
            print("  PROIBIDO:", repr(p), "...", repr(txt[max(0, idx - 50): idx + 60]))
            erros += 1
    if EMOJI.search(txt):
        print("  EMOJI encontrado:", EMOJI.findall(txt)[:5]); erros += 1
    h1 = [p.text for p in doc.paragraphs if p.style.name == "Heading 1"]
    print("  H1:", h1)
    num = [re.match(r"^(\d+) ", h) for h in h1]
    seq = [int(m.group(1)) for m in num if m]
    if seq != capitulos:
        print("  ORDEM dos capitulos diferente:", seq, "esperado", capitulos); erros += 1
    # legendas sequenciais
    for tipo in ("Figura", "Tabela", "Quadro"):
        nums = [int(m.group(1)) for p in doc.paragraphs for m in [re.match(rf"^{tipo} (\d+) – ", p.text)] if m]
        # a lista de ilustracoes tambem casa; separa: legendas reais ficam apos o sumario
        n = len(nums) // 2
        real = nums[n:] if len(nums) >= 2 * 1 else nums
        lista = nums[:n]
        ok = real == list(range(1, len(real) + 1)) and lista == real
        print(f"  {tipo}: {len(real)} legendas, sequencia {'OK' if ok else 'COM PROBLEMA'}")
        if not ok:
            erros += 1
    for k in chaves:
        if k not in txt:
            print("  FALTA numero-chave:", k); erros += 1
    print("  secoes:", len(doc.sections), "| erros:", erros)
    return erros


def conta_tabelas(arq, esperado):
    doc = Document(str(arq))
    achados = {}
    for t in doc.tables:
        cab = [c.text for c in t.rows[0].cells]
        for nome, (c0, c1, n) in esperado.items():
            if cab[0] == c0 and len(cab) > 1 and cab[1] == c1:
                achados[nome] = len(t.rows) - 1
    erros = 0
    for nome, (c0, c1, n) in esperado.items():
        got = achados.get(nome)
        ok = got == n
        print(f"  tabela {nome}: {got} linhas (esperado {n}) {'OK' if ok else 'ERRO'}")
        erros += 0 if ok else 1
    return erros


if __name__ == "__main__":
    av2_chaves = ["47.714,83", "52.486,31", "54.872,05", "967 h", "71 itens", "36 pacotes", "22 ameaças", "4 oportunidades", "57 de 103", "59 de 103", "R06", "SM-01", "M8b", "Next.js"]
    av1_chaves = ["967 h", "36 pacotes", "63 atividades", "Next.js", "13 partes", "19 comunicações", "10 gatilhos"]
    e = confere(RAIZ / "avaliacao-2-relatorio-final.docx", list(range(1, 15)), av2_chaves)
    e += confere(RAIZ / "avaliacao-1-documento-parcial.docx", list(range(1, 9)), av1_chaves)
    sys.exit(1 if e else 0)
