#!/usr/bin/env python3
"""Gera versões .docx e .pdf dos artefatos em Markdown.

Requisitos: pandoc, Google Chrome (headless) e python-docx. Os diagramas Mermaid
são renderizados em PNG pelo Chrome (mermaid carregado de CDN).

Uso: python3 _base/gerar_exportacoes.py [caminho-relativo.md ...]
Sem argumentos, processa todos os .md fora de _base/ (os TAP já têm .docx pelo Modelo 4.1).
"""
import glob, html, os, re, subprocess, sys, tempfile
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
TMP = tempfile.mkdtemp(prefix='exp_')

# Orientação: tabelas largas ficam em paisagem.
PORTRAIT = {'resumo-aula-01', 'eap-fieldops', 'roteiro-apresentacao-3min',
            'roteiro-apresentacao-final', 'matriz-poder-interesse-fieldops',
            'analise-portfolio', 'qualidade-7-ferramentas-fieldops'}

CSS = """
@page { size: %(size)s; margin: 14mm 12mm 16mm 12mm;
  @bottom-center { content: counter(page) " / " counter(pages); font: 8pt Helvetica, Arial, sans-serif; color:#666 } }
body { font-family: -apple-system, 'Helvetica Neue', Arial, 'Apple Color Emoji', sans-serif; font-size: 9.5pt; line-height: 1.42; color:#1f2933 }
h1 { font-size: 20pt; color:#12355b; border-bottom: 2px solid #12355b; padding-bottom: 4px; margin-top: 0 }
h2 { font-size: 14.5pt; color:#12355b; margin-top: 18px; border-bottom: 1px solid #c8d3e0; padding-bottom: 2px; break-after: avoid }
h3 { font-size: 11.5pt; color:#1d4f87; break-after: avoid } h4 { font-size: 10pt; color:#1d4f87; break-after: avoid }
table { border-collapse: collapse; width: 100%%; margin: 8px 0; font-size: 8pt; line-height: 1.3 }
th { background:#12355b; color:#fff; text-align:left } th, td { border: 1px solid #b8c4d2; padding: 3px 5px; vertical-align: top }
tr { break-inside: avoid } tbody tr:nth-child(even) td { background:#f3f6fa }
thead { display: table-header-group }
code { font-family: Menlo, monospace; font-size: 8pt; background:#eef1f5; padding: 0 2px }
pre { background:#f3f5f8; padding: 6px 8px; font-size: 7.5pt; white-space: pre-wrap; border-left: 3px solid #9fb3c8; break-inside: avoid }
pre code { background: none }
blockquote { margin: 8px 0; padding: 4px 12px; border-left: 4px solid #1d4f87; background:#f3f7fb; color:#2c3e50 }
img { max-width: 100%%; max-height: %(maxh)s; display:block; margin: 8px auto; object-fit: contain }
a { color:#1d4f87; text-decoration: none } hr { border: 0; border-top: 1px solid #c8d3e0 }
"""


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def render_mermaid(src, name):
    page = f'''<html><body style="margin:0;background:#fff"><pre class="mermaid" id="d">{html.escape(src)}</pre>
<script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";
mermaid.initialize({{startOnLoad:false,theme:"default",securityLevel:"loose",gantt:{{useWidth:1400}},flowchart:{{useMaxWidth:false,htmlLabels:true}}}});
await mermaid.run({{querySelector:"#d"}});</script></body></html>'''
    p = f'{TMP}/{name}.html'
    open(p, 'w').write(page)
    r = run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox', '--virtual-time-budget=20000', '--dump-dom', 'file://' + p])
    m = re.search(r'<svg.*?</svg>', r.stdout, re.S)
    if not m:
        raise RuntimeError(f'mermaid falhou: {name}')
    svg = m.group(0)
    w, h = [float(x) for x in re.search(r'viewBox="([\d\.\-\s]+)"', svg).group(1).split()[2:4]]
    svg = re.sub(r'style="max-width:[^"]*"', '', svg, count=1)
    svg = svg.replace('<svg ', f'<svg width="{w}" height="{h}" ', 1)
    p2 = f'{TMP}/{name}-svg.html'
    open(p2, 'w').write(f'<html><body style="margin:0;background:#fff">{svg}</body></html>')
    png = f'{TMP}/{name}.png'
    run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars', '--force-device-scale-factor=2',
         f'--window-size={int(w)+1},{int(h)+1}', f'--screenshot={png}', 'file://' + p2])
    return png


def prepare_md(path):
    text = open(path, encoding='utf-8').read()
    # A EAP já tem o diagrama em PNG; a versão Mermaid (muito alta) fica só no .md.
    text = re.sub(r'### Mesma estrutura em Mermaid\n+```mermaid\n.*?```\n', '', text, flags=re.S)
    base = os.path.splitext(os.path.basename(path))[0]
    n = [0]

    def sub(m):
        png = render_mermaid(m.group(1), f'{base}-mm{n[0]}')
        n[0] += 1
        return f'![Diagrama]({png})'
    return re.sub(r'```mermaid\n(.*?)```', sub, text, flags=re.S)


def make_reference(landscape):
    ref = f'{TMP}/ref-{"l" if landscape else "p"}.docx'
    with open(ref, 'wb') as f:
        f.write(subprocess.run(['pandoc', '--print-default-data-file', 'reference.docx'], capture_output=True).stdout)
    d = Document(ref)
    st = d.styles
    for name in ('Normal', 'Body Text', 'First Paragraph', 'Compact'):
        if name in [s.name for s in st]:
            s = st[name]; s.font.name = 'Calibri'; s.font.size = Pt(10)
    for name, size in (('Heading 1', 20), ('Heading 2', 15), ('Heading 3', 12), ('Heading 4', 10.5)):
        s = st[name]; s.font.name = 'Calibri'; s.font.size = Pt(size); s.font.bold = True
        s.font.color.rgb = RGBColor(0x12, 0x35, 0x5B) if name != 'Heading 4' else RGBColor(0x1D, 0x4F, 0x87)
    sec = d.sections[0]
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
    else:
        sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(1.6)
    sec.top_margin = sec.bottom_margin = Cm(1.6)
    d.save(ref)
    return ref


def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), color)
    tcPr.append(shd)


def post_docx(path, landscape):
    d = Document(path)
    sec = d.sections[0]
    max_w = sec.page_width - sec.left_margin - sec.right_margin
    max_h = sec.page_height - sec.top_margin - sec.bottom_margin - Cm(1.5)
    for sh in d.inline_shapes:
        w, h = sh.width, sh.height
        k = min(1.0, max_w / w, max_h / h) if w and h else 1.0
        # imagens menores que a área útil também são ampliadas até ~80% da largura
        if w < max_w * 0.5 and h < max_h * 0.5:
            k = min(max_w * 0.8 / w, max_h * 0.6 / h, 2.5)
        sh.width, sh.height = int(w * k), int(h * k)
    for t in d.tables:
        tblPr = t._tbl.tblPr
        borders = OxmlElement('w:tblBorders')
        for b in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            e = OxmlElement(f'w:{b}'); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4'); e.set(qn('w:space'), '0'); e.set(qn('w:color'), 'B8C4D2')
            borders.append(e)
        tblPr.append(borders)
        # largura total da página, colunas ajustadas ao conteúdo
        for old in tblPr.findall(qn('w:tblW')):
            tblPr.remove(old)
        total = int(max_w / 635)  # EMU -> dxa (twips)
        w = OxmlElement('w:tblW'); w.set(qn('w:w'), str(total)); w.set(qn('w:type'), 'dxa'); tblPr.append(w)
        for old_l in tblPr.findall(qn('w:tblLayout')):
            tblPr.remove(old_l)
        lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblPr.append(lay)
        ncol = len(t.columns)
        weights = []
        for ci in range(ncol):
            lens = [len(r.cells[ci].text) for r in t.rows if ci < len(r.cells)]
            mx = min(max(lens), 70); av = min(sum(lens) / len(lens), 70)
            words = [len(w) for r in t.rows if ci < len(r.cells) for w in r.cells[ci].text.split()] or [1]
            weights.append(max(6.0, 0.5 * mx + 0.5 * av, 1.15 * max(words)))
        sw = sum(weights)
        widths = [max(500, int(total * x / sw)) for x in weights]
        grid = t._tbl.tblGrid
        for gc, wd in zip(grid.findall(qn('w:gridCol')), widths):
            gc.set(qn('w:w'), str(wd))
        for row in t.rows:
            for ci, c in enumerate(row.cells):
                if ci < len(widths):
                    tcPr = c._tc.get_or_add_tcPr()
                    for o in tcPr.findall(qn('w:tcW')):
                        tcPr.remove(o)
                    tw = OxmlElement('w:tcW'); tw.set(qn('w:w'), str(widths[ci])); tw.set(qn('w:type'), 'dxa'); tcPr.insert(0, tw)
        for ri, row in enumerate(t.rows):
            if ri == 0:
                trPr = row._tr.get_or_add_trPr(); h = OxmlElement('w:tblHeader'); trPr.append(h)
            cant = OxmlElement('w:cantSplit'); row._tr.get_or_add_trPr().append(cant)
            for c in row.cells:
                if ri == 0:
                    shade(c, '12355B')
                for p in c.paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(8)
                        if ri == 0:
                            r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)
    def fix_br(paragraphs):
        for p in paragraphs:
            for r in list(p.runs):
                if '§BR§' in r.text:
                    parts = [x.strip() for x in r.text.split('§BR§')]
                    r.text = parts[0]
                    cur = r
                    for part in parts[1:]:
                        cur.add_break()
                        cur.add_text(part)
    fix_br(d.paragraphs)
    for t in d.tables:
        for row in t.rows:
            for c in row.cells:
                fix_br(c.paragraphs)
    d.core_properties.author = 'Grupo FieldOps'
    d.save(path)


def export(md_rel):
    path = os.path.join(ROOT, md_rel)
    base = os.path.splitext(path)[0]
    name = os.path.basename(base)
    landscape = name not in PORTRAIT
    src = prepare_md(path)
    tmp_md = f'{TMP}/{name}.md'
    open(tmp_md, 'w', encoding='utf-8').write(src)
    res = os.path.dirname(path)
    title = next((l[2:].strip() for l in src.splitlines() if l.startswith('# ')), name)
    # DOCX (<br> vira token; post_docx troca por quebra de linha real)
    docx_md = f'{TMP}/{name}-docx.md'
    open(docx_md, 'w', encoding='utf-8').write(re.sub(r'<br\s*/?>', ' §BR§ ', src))
    r = run(['pandoc', '-f', 'gfm', '-t', 'docx', f'--reference-doc={make_reference(landscape)}', f'--resource-path={res}',
             '--metadata', f'pagetitle={title}', '--metadata', 'lang=pt-BR', '-o', base + '.docx', docx_md])
    if r.returncode: raise RuntimeError(r.stderr)
    post_docx(base + '.docx', landscape)
    # PDF (HTML -> Chrome)
    size = 'A4 landscape' if landscape else 'A4'
    css = CSS % {'size': size, 'maxh': '165mm' if landscape else '235mm'}
    cssf = f'{TMP}/{name}.css'
    open(cssf, 'w').write(css)
    htmlf = f'{TMP}/{name}.html'
    r = run(['pandoc', '-f', 'gfm', '-t', 'html5', '-s', '--embed-resources', f'--resource-path={res}', '--metadata', f'pagetitle={title}',
             '--metadata', 'lang=pt-BR', '-c', cssf, '-o', htmlf, tmp_md])
    if r.returncode: raise RuntimeError(r.stderr)
    r = run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox', '--no-pdf-header-footer', '--virtual-time-budget=15000',
             f'--print-to-pdf={base}.pdf', 'file://' + htmlf])
    if not os.path.exists(base + '.pdf'):
        raise RuntimeError('pdf falhou: ' + r.stderr[-300:])
    print('ok', md_rel)


if __name__ == '__main__':
    files = sys.argv[1:] or sorted(os.path.relpath(f, ROOT) for f in glob.glob(ROOT + '/*/*.md') if '/_base/' not in f and not os.path.basename(f).startswith('tap-'))
    for f in files:
        try:
            export(f)
        except Exception as e:
            print('ERRO', f, e)
