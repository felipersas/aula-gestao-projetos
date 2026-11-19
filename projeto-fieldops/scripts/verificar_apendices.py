#!/usr/bin/env python3
"""Confere o numero de linhas das tabelas dos apendices contra os artefatos."""
from pathlib import Path
from docx import Document

RAIZ = Path(__file__).resolve().parent.parent
doc = Document(str(RAIZ / "avaliacao-2-relatorio-final.docx"))
doc1 = Document(str(RAIZ / "avaliacao-1-documento-parcial.docx"))


def acha(d, titulo_inicio):
    # legenda e o paragrafo imediatamente anterior a tabela (elemento irmao)
    body = d.element.body
    kids = list(body)
    from docx.oxml.ns import qn
    for i, el in enumerate(kids):
        if el.tag == qn("w:p"):
            t = "".join(x.text or "" for x in el.iter(qn("w:t")))
            if (t.startswith(titulo_inicio) or (titulo_inicio.startswith('*') and titulo_inicio[1:] in t[:60])) and i + 1 < len(kids) and kids[i + 1].tag == qn("w:tbl"):
                tbl = kids[i + 1]
                return len(tbl.findall(qn("w:tr"))) - 1
    return None


casos = [
    ("Tabela 14 – Cronograma completo", 71), ("Tabela 15 – Orçamento por estimativa", 52 + 1), ("Tabela 16 – Matriz RACI", 36), ("Quadro 49 – Dicionário da EAP", 43),
    ("Quadro 50 – Registro de riscos", 22), ("Quadro 51 – Respostas aos riscos", 22), ("Quadro 52 – Oportunidades", 4), ("Quadro 53 – Tabela de aquisições", 14 + 1),
    ("Quadro 54 – Plano de comunicação: momento", 19), ("Quadro 55 – Gatilhos", 10), ("Tabela 17 – Rastreabilidade por pacote", 36 + 1),
]
erros = 0
for ini, n in casos:
    got = acha(doc, ini)
    ok = got == n
    erros += 0 if ok else 1
    print(f"{ini}: {got} linhas (esperado {n}) {'OK' if ok else 'ERRO'}")
for ini, n in (("*Cronograma completo", 71), ("*Matriz RACI", 36)):
    got = acha(doc1, ini)
    print(f"[Av.1] {ini}: {got} (esperado {n}) {'OK' if got == n else 'ERRO'}")
    erros += 0 if got == n else 1
raise SystemExit(1 if erros else 0)
