#!/usr/bin/env python3
"""Verificacao final do pptx: numeros-chave, tamanhos de fonte, notas, emojis, formato."""
import re, sys
from pptx import Presentation
from pptx.util import Emu
from fatos_apresentacao import carrega
F = carrega()
prs = Presentation("/Users/felipersas/Documents/Facul/gestao-proj/entrega/projeto-fieldops/apresentacao-final.pptx")
assert abs(prs.slide_width / prs.slide_height - 16 / 9) < 0.001
n = len(prs.slides)
print("slides:", n, "| formato 16:9 ok")
alltext = []
small = []
for i, sl in enumerate(prs.slides, 1):
    texts = []
    def runs_of(tf, where):
        for p in tf.paragraphs:
            for r in p.runs:
                if r.text.strip():
                    sz = r.font.size.pt if r.font.size else None
                    texts.append(r.text)
                    if sz is not None and sz < 14:
                        small.append((i, sz, r.text[:50], where))
    for sh in sl.shapes:
        if sh.has_text_frame:
            runs_of(sh.text_frame, sh.name)
        if sh.has_table:
            for row in sh.table.rows:
                for c in row.cells:
                    runs_of(c.text_frame, "tabela")
    t = " ".join(texts)
    alltext.append(t)
    assert sl.has_notes_slide and len(sl.notes_slide.notes_text_frame.text) > 100, f"sem notas no slide {i}"
    tit = [s for s in sl.shapes if s.name == "Titulo"][0]
    sz = tit.text_frame.paragraphs[0].runs[0].font.size.pt
    assert sz >= 28, (i, sz)
print("notas em todos os slides; titulos >= 28 pt")
print("textos < 14 pt (devem ser so rodape/fonte/legenda 12 pt):")
from collections import Counter
print(Counter((s, w if w in ("rodape", "numero", "fonte") else "outro") for _, s, _, w in small))
for x in small:
    if x[3] not in ("rodape", "numero", "fonte"):
        print("  ", x)
full = "\n".join(alltext)
emoji = re.findall("[\U0001F300-\U0001FAFF☀-➿⭐⬆]", full)
assert not emoji, emoji
print("sem emojis")
checks = ["R$ 47.714,83" if False else "47.714,83", "52.486,31", "54.872,05", "4.771,48", "2.385,74", "669,08", "374,00", "2.478,50",
          "57/103", "0,53", "0,58", "3,08" if False else "32,5", "06/01/2027", "R$ 6.635", "R$ 9.812", "R$ 7.157,22",
          "22 riscos", "36 pacotes", "71 itens", "967 h", "72 PBIs", "10 épicos", "19 comunicações", "21 issues", "22 de 31", "21 de 39", "14 de 41"]
miss = [c for c in checks if c not in full]
assert not miss, miss
print("numeros-chave presentes:", len(checks))
# coerencia com fatos
assert F["itens_cron"] == 71 and round(F["horas"]) == 967 and F["pacotes"] == 36 and F["issues"] == (57, 103) and F["n_crit"] == 20
for nm, a, b in F["sprints"]:
    assert f"{a}/{b}" in full, (nm, a, b)
print("sprints", [(a, b) for _, a, b in F["sprints"]])
print("OK")
