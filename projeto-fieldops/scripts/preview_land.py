#!/usr/bin/env python3
"""Gera uma copia do docx com TODAS as secoes em paisagem (o Pages so aceita um tamanho de pagina por documento),
para inspecionar visualmente as tabelas largas dos apendices. Apenas para conferencia; nao e entregue."""
import re, shutil, sys, zipfile
src, dst = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename == "word/document.xml":
            s = data.decode("utf8")
            s = re.sub(r'<w:pgSz [^>]*/>', '<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>', s)
            data = s.encode("utf8")
        zout.writestr(it, data)
