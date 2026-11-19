#!/bin/bash
# Uso: preview.sh <arquivo.docx> <pasta_saida>   (exporta PDF pelo Pages e gera PNGs das paginas)
DOCX="$1"; OUT="$2"; mkdir -p "$OUT"
cp "$DOCX" "$OUT/doc.docx"
osascript <<APPLESCRIPT
tell application "Pages Creator Studio"
  set d to open POSIX file "$OUT/doc.docx"
  export d to POSIX file "$OUT/doc.pdf" as PDF
  close d saving no
end tell
APPLESCRIPT
pdfinfo "$OUT/doc.pdf" | grep Pages
pdftoppm -r 60 -png "$OUT/doc.pdf" "$OUT/p"
