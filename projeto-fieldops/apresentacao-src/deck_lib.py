#!/usr/bin/env python3
"""
Biblioteca minima de layout para a apresentacao final do FieldOps.

Uma unica especificacao de slide (lista de primitivas em polegadas) gera:
  - .pptx nativo e editavel (python-pptx): formas, tabelas e textos reais;
  - .html de referencia com a mesma geometria -> Chrome headless -> .pdf / .png.
Tambem mede o texto com as metricas da fonte Arial e acusa estouro de caixa.
"""
import html
from pathlib import Path

from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt
from lxml import etree

FONT = "Arial"
W, H = 13.333, 7.5
LH = 1.2  # fator de entrelinha usado na medida e no HTML

# paleta (mesma familia do slide executivo do desafio MetalTech)
PETROL = "0F4C5C"
TEAL = "2A7F91"
TEAL_L = "6BA8B5"
TEAL_XL = "D6E7EC"
GRAFITE = "2B2F33"
CINZA = "5F6B73"
CINZA_L = "DDE3E6"
CLARO = "E8EEF1"
CLARO2 = "F3F6F7"
BRANCO = "FFFFFF"
VERDE = "237A4B"
VERDE_L = "D5EBDD"
AMARELO = "E0A800"
AMARELO_L = "FBEFC4"
VERMELHO = "C0392B"
VERMELHO_L = "F5D5D1"
LARANJA = "D9822B"

_FP = {
    False: "/System/Library/Fonts/Supplemental/Arial.ttf",
    True: "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
}
_cache = {}


def _font(bold):
    if bold not in _cache:
        _cache[bold] = ImageFont.truetype(_FP[bold], 200)
    return _cache[bold]


def text_w(txt, size, bold):
    """largura em pontos"""
    return _font(bold).getlength(txt) * size / 200.0 * 1.04  # folga de 4% p/ diferencas entre renderizadores


def norm_paras(paras, d):
    """normaliza para lista de dict(runs, bullet, after, align)"""
    out = []
    if paras is None:
        return out
    if isinstance(paras, str):
        paras = [paras]
    for p in paras:
        if isinstance(p, dict):
            q = dict(p)
            runs = q["runs"]
        else:
            q = {}
            runs = p
        if isinstance(runs, str):
            runs = [(runs, {})]
        q["runs"] = [(t, dict(st)) for t, st in runs]
        q.setdefault("bullet", False)
        q.setdefault("after", 0)
        q.setdefault("align", None)
        out.append(q)
    return out


def wrap_lines(runs, width_pt, d):
    """quebra uma lista de runs em linhas; devolve numero de linhas e maior tamanho"""
    # tokens (palavra, bold, size)
    toks = []
    for t, st in runs:
        b = st.get("bold", d["bold"])
        sz = st.get("size", d["size"])
        parts = t.split(" ")
        for i, w in enumerate(parts):
            toks.append((w, b, sz, i < len(parts) - 1))
    lines = 1
    cur = 0.0
    maxsz = d["size"]
    for w, b, sz, sp in toks:
        maxsz = max(maxsz, sz)
        ww = text_w(w, sz, b)
        spw = text_w(" ", sz, b)
        if "\n" in w:
            lines += w.count("\n")
            cur = 0
            continue
        if cur > 0 and cur + ww > width_pt + 0.01:
            lines += 1
            cur = 0.0
        cur += ww + (spw if sp else 0)
    return lines, maxsz


def measure(paras, width_in, d):
    """altura em polegadas do texto com a largura dada (ja descontadas as margens)"""
    total = 0.0
    maxline = 0
    for p in paras:
        w = width_in * 72
        if p["bullet"]:
            w -= d.get("indent", 0.22) * 72
        n, mx = wrap_lines(p["runs"], w, d)
        sz = max([st.get("size", d["size"]) for _, st in p["runs"]] or [d["size"]])
        total += n * sz * LH + p["after"]
        maxline = max(maxline, n)
    return total / 72.0


class Slide:
    def __init__(self, title, notes="", backup=False, source=None, n=0, tot=0):
        self.title = title
        self.notes = notes
        self.backup = backup
        self.source = source
        self.n = n
        self.els = []
        self.issues = []

    # ---------------------------------------------------------------- primitivas
    def box(self, x, y, w, h, paras=None, fill=None, line=None, lw=1.0, dash=False, shape="rect",
            size=14, bold=False, color=GRAFITE, align="l", valign="m", mx=0.08, my=0.04, name=None, indent=0.22):
        d = dict(k="box", x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw, dash=dash, shape=shape,
                 size=size, bold=bold, color=color, align=align, valign=valign, mx=mx, my=my,
                 name=name or "forma", indent=indent)
        d["paras"] = norm_paras(paras, d) if paras is not None else None
        if d["paras"]:
            need = measure(d["paras"], w - 2 * mx, d) + 2 * my
            if need > h + 0.015:
                txt = " ".join(t for p in d["paras"] for t, _ in p["runs"])[:50]
                self.issues.append(f"texto estoura caixa ({need:.2f} > {h:.2f} in): '{txt}'")
        self.els.append(d)
        return d

    def text(self, x, y, w, h, paras, **kw):
        kw.setdefault("mx", 0.0)
        kw.setdefault("my", 0.0)
        kw.setdefault("valign", "t")
        return self.box(x, y, w, h, paras, **kw)

    def line(self, x1, y1, x2, y2, color=CINZA, lw=1.5, dash=False):
        self.els.append(dict(k="line", x1=x1, y1=y1, x2=x2, y2=y2, color=color, lw=lw, dash=dash))

    def poly(self, pts, color=PETROL, lw=2.5, dash=False):
        self.els.append(dict(k="poly", pts=pts, color=color, lw=lw, dash=dash))

    def table(self, x, y, colw, rowh, cells, border=BRANCO, bw=1.0, size=14, color=GRAFITE, mx=0.07, my=0.03):
        """cells[r][c] = dict(t=str|paras, fill, color, bold, size, align, valign)"""
        d = dict(k="table", x=x, y=y, colw=colw, rowh=rowh, border=border, bw=bw, rows=[])
        for r, row in enumerate(cells):
            rr = []
            for c, cell in enumerate(row):
                cd = dict(cell)
                cd.setdefault("fill", None)
                cd.setdefault("color", color)
                cd.setdefault("bold", False)
                cd.setdefault("size", size)
                cd.setdefault("align", "l")
                cd.setdefault("valign", "m")
                dd = dict(size=cd["size"], bold=cd["bold"], indent=0.2)
                cd["paras"] = norm_paras(cd.get("t", ""), dd)
                need = measure(cd["paras"], colw[c] - 2 * mx, dd) + 2 * my
                if need > rowh[r] + 0.015:
                    txt = " ".join(t for p in cd["paras"] for t, _ in p["runs"])[:40]
                    self.issues.append(f"celula estoura ({need:.2f} > {rowh[r]:.2f}) L{r}C{c}: '{txt}'")
                rr.append(cd)
            d["rows"].append(rr)
        d["mx"], d["my"], d["size"], d["color"] = mx, my, size, color
        self.els.append(d)


# ------------------------------------------------------------------ cabecalho e rodape padrao
def chrome(s, total):
    """barra de titulo, rodape e numero"""
    tw = 12.33 - (1.5 if s.backup else 0)
    s.els.insert(0, dict(k="box", x=0, y=0, w=W, h=1.2, fill=PETROL, line=None, lw=0, dash=False, shape="rect",
                         size=14, bold=False, color=BRANCO, align="l", valign="m", mx=0, my=0, name="faixa-titulo",
                         paras=None, indent=0))
    s.box(0.5, 0.08, tw, 1.04, [[(s.title, {})]], size=28, bold=True, color=BRANCO, valign="m", mx=0, my=0,
          name="Titulo")
    if s.backup:
        s.box(11.55, 0.4, 1.3, 0.4, ["BACKUP"], fill=AMARELO, color=GRAFITE, size=14, bold=True, align="c",
              shape="round", name="selo-backup")
    foot = "FieldOps  ·  Gestão de Projetos  ·  UniSENAI-SP Sorocaba  ·  Prof. Deivison Takatu"
    s.text(0.5, 7.14, 9.0, 0.26, [foot], size=12, color=CINZA, valign="m", name="rodape")
    s.text(11.8, 7.14, 1.03, 0.26, [f"{s.n} / {total}"], size=12, color=CINZA, align="r", valign="m", name="numero")
    if s.source:
        s.text(0.5, 6.82, 12.33, 0.3, [s.source], size=12, color=CINZA, valign="m", name="fonte")


# ------------------------------------------------------------------ PPTX
def rgb(hexa):
    return RGBColor.from_string(hexa)


def _apply_paras(tf, d, paras):
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        al = p["align"] or d["align"]
        para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[al]
        para.line_spacing = 1.0
        para.space_before = Pt(0)
        para.space_after = Pt(p["after"])
        if p["bullet"]:
            pPr = para._p.get_or_add_pPr()
            ind = int(Inches(d.get("indent", 0.22)))
            pPr.set("marL", str(ind))
            pPr.set("indent", str(-ind))
            for ch in list(pPr):
                if ch.tag in (qn("a:buNone"), qn("a:buChar")):
                    pPr.remove(ch)
            bu = etree.SubElement(pPr, qn("a:buChar"))
            bu.set("char", "•")
        for t, st in p["runs"]:
            r = para.add_run()
            r.text = t
            r.font.name = FONT
            r.font.size = Pt(st.get("size", d["size"]))
            r.font.bold = st.get("bold", d["bold"])
            r.font.color.rgb = rgb(st.get("color", d["color"]))


def _cell_border(cell, color, wpt):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        for ch in tcPr.findall(qn(tag)):
            tcPr.remove(ch)
    # a ordem exigida pelo esquema: lnL, lnR, lnT, lnB antes do fill
    fills = [ch for ch in tcPr if ch.tag in (qn("a:solidFill"), qn("a:noFill"))]
    for ch in fills:
        tcPr.remove(ch)
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        ln = etree.SubElement(tcPr, qn(tag))
        ln.set("w", str(int(Pt(wpt))))
        ln.set("cap", "flat")
        ln.set("cmpd", "sng")
        sf = etree.SubElement(ln, qn("a:solidFill"))
        c = etree.SubElement(sf, qn("a:srgbClr"))
        c.set("val", color)
        etree.SubElement(ln, qn("a:prstDash")).set("val", "solid")
    for ch in fills:
        tcPr.append(ch)


def emit_slide_pptx(prs, s):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    for e in s.els:
        k = e["k"]
        if k == "line":
            c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(e["x1"]), Inches(e["y1"]), Inches(e["x2"]), Inches(e["y2"]))
            c.line.color.rgb = rgb(e["color"])
            c.line.width = Pt(e["lw"])
            if e["dash"]:
                c.line.dash_style = MSO_LINE.DASH
        elif k == "poly":
            pts = [(int(Inches(a)), int(Inches(b))) for a, b in e["pts"]]
            fb = sl.shapes.build_freeform(pts[0][0], pts[0][1], scale=1.0)
            fb.add_line_segments(pts[1:], close=False)
            sh = fb.convert_to_shape()
            sh.fill.background()
            sh.line.color.rgb = rgb(e["color"])
            sh.line.width = Pt(e["lw"])
            sh.shadow.inherit = False
            if e["dash"]:
                sh.line.dash_style = MSO_LINE.DASH
            sh.name = "curva"
        elif k == "box":
            shp = {"rect": MSO_SHAPE.RECTANGLE, "round": MSO_SHAPE.ROUNDED_RECTANGLE, "oval": MSO_SHAPE.OVAL,
                   "diamond": MSO_SHAPE.DIAMOND, "rarrow": MSO_SHAPE.RIGHT_ARROW}[e["shape"]]
            sh = sl.shapes.add_shape(shp, Inches(e["x"]), Inches(e["y"]), Inches(e["w"]), Inches(e["h"]))
            sh.name = e["name"]
            sh.shadow.inherit = False
            if e["shape"] == "round":
                sh.adjustments[0] = min(0.5, 0.09 / min(e["w"], e["h"]))
            if e["fill"]:
                sh.fill.solid()
                sh.fill.fore_color.rgb = rgb(e["fill"])
            else:
                sh.fill.background()
            if e["line"]:
                sh.line.color.rgb = rgb(e["line"])
                sh.line.width = Pt(e["lw"])
                if e["dash"]:
                    sh.line.dash_style = MSO_LINE.DASH
            else:
                sh.line.fill.background()
            if e["paras"] is not None:
                tf = sh.text_frame
                tf.word_wrap = True
                tf.auto_size = None
                tf.margin_left = tf.margin_right = Inches(e["mx"])
                tf.margin_top = tf.margin_bottom = Inches(e["my"])
                tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[e["valign"]]
                _apply_paras(tf, e, e["paras"])
        elif k == "table":
            nr, nc = len(e["rows"]), len(e["colw"])
            gf = sl.shapes.add_table(nr, nc, Inches(e["x"]), Inches(e["y"]), Inches(sum(e["colw"])), Inches(sum(e["rowh"])))
            gf.name = "tabela"
            tbl = gf.table
            tblPr = tbl._tbl.tblPr
            for a in ("firstRow", "bandRow", "firstCol", "lastRow", "lastCol", "bandCol"):
                tblPr.set(a, "0")
            for ch in list(tblPr):
                tblPr.remove(ch)  # remove o estilo padrao
            for c, wv in enumerate(e["colw"]):
                tbl.columns[c].width = Inches(wv)
            for r, hv in enumerate(e["rowh"]):
                tbl.rows[r].height = Inches(hv)
            for r, row in enumerate(e["rows"]):
                for c, cd in enumerate(row):
                    cell = tbl.cell(r, c)
                    cell.margin_left = cell.margin_right = Inches(e["mx"])
                    cell.margin_top = cell.margin_bottom = Inches(e["my"])
                    cell.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[cd["valign"]]
                    tf = cell.text_frame
                    tf.word_wrap = True
                    dd = dict(size=cd["size"], bold=cd["bold"], color=cd["color"], align=cd["align"], indent=0.2)
                    _apply_paras(tf, dd, cd["paras"])
                    if cd["fill"]:
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = rgb(cd["fill"])
                    else:
                        cell.fill.background()
                    _cell_border(cell, e["border"], e["bw"])
    if s.notes:
        sl.notes_slide.notes_text_frame.text = s.notes
    return sl


def build_pptx(slides, path, title, author):
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    for s in slides:
        emit_slide_pptx(prs, s)
    prs.core_properties.title = title
    prs.core_properties.author = author
    prs.save(str(path))


# ------------------------------------------------------------------ HTML
PX = 144.0


def _paras_html(e, paras, sizefn=None):
    out = []
    for p in paras:
        al = p["align"] or e["align"]
        styl = f"margin:0 0 {p['after'] * PX / 72:.1f}px 0;text-align:{ {'l': 'left', 'c': 'center', 'r': 'right'}[al] }"
        if p["bullet"]:
            ind = e.get("indent", 0.22) * PX
            styl += f";padding-left:{ind:.1f}px;text-indent:-{ind:.1f}px"
        spans = []
        if p["bullet"]:
            spans.append(f"<span style='display:inline-block;width:{e.get('indent', 0.22) * PX:.1f}px;text-indent:0'>•</span>")
        for t, st in p["runs"]:
            b = st.get("bold", e["bold"])
            c = st.get("color", e["color"])
            sz = st.get("size", e["size"])
            spans.append(f"<span style='font-size:{sz * PX / 72:.2f}px;font-weight:{700 if b else 400};color:#{c}'>{html.escape(t)}</span>")
        out.append(f"<div class='p' style='{styl}'>{''.join(spans) or '&nbsp;'}</div>")
    return "".join(out)


def slide_html(s):
    out = [f"<section class='s' id='s{s.n}'>"]
    svg = []
    for e in s.els:
        k = e["k"]
        if k == "line":
            x1, y1, x2, y2 = e["x1"] * PX, e["y1"] * PX, e["x2"] * PX, e["y2"] * PX
            da = " stroke-dasharray='10,7'" if e["dash"] else ""
            svg.append(f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='#{e['color']}' stroke-width='{e['lw'] * PX / 72:.1f}'{da}/>")
        elif k == "poly":
            da = " stroke-dasharray='10,7'" if e["dash"] else ""
            pts = " ".join(f"{a * PX:.1f},{b * PX:.1f}" for a, b in e["pts"])
            svg.append(f"<polyline points='{pts}' fill='none' stroke='#{e['color']}' stroke-width='{e['lw'] * PX / 72:.1f}' stroke-linejoin='round'{da}/>")
    # ordem: caixas/tabelas primeiro (z), linhas e polilinhas sobre elas
    for e in s.els:
        k = e["k"]
        if k == "box":
            st = [f"left:{e['x'] * PX:.1f}px", f"top:{e['y'] * PX:.1f}px", f"width:{e['w'] * PX:.1f}px", f"height:{e['h'] * PX:.1f}px"]
            if e["fill"]:
                st.append(f"background:#{e['fill']}")
            if e["line"]:
                st.append(f"border:{max(1.0, e['lw'] * PX / 72):.1f}px {'dashed' if e['dash'] else 'solid'} #{e['line']}")
            if e["shape"] == "round":
                st.append("border-radius:%.1fpx" % (min(0.5 * min(e["w"], e["h"]), 0.09) * PX))
            if e["shape"] == "oval":
                st.append("border-radius:50%")
            if e["shape"] == "diamond":
                st.append("clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%)")
            if e["shape"] == "rarrow":
                st.append("clip-path:polygon(0 25%,55% 25%,55% 0,100% 50%,55% 100%,55% 75%,0 75%)")
            if e["paras"] is not None:
                st.append({"t": "justify-content:flex-start", "m": "justify-content:center", "b": "justify-content:flex-end"}[e["valign"]])
                st.append(f"padding:{e['my'] * PX:.1f}px {e['mx'] * PX:.1f}px")
            out.append(f"<div class='e' style='{';'.join(st)}'>")
            if e["paras"] is not None:
                out.append(_paras_html(e, e["paras"]))
            out.append("</div>")
        elif k == "table":
            y = e["y"]
            for r, row in enumerate(e["rows"]):
                x = e["x"]
                for c, cd in enumerate(row):
                    st = [f"left:{x * PX:.1f}px", f"top:{y * PX:.1f}px", f"width:{e['colw'][c] * PX:.1f}px", f"height:{e['rowh'][r] * PX:.1f}px"]
                    if cd["fill"]:
                        st.append(f"background:#{cd['fill']}")
                    st.append(f"border:{max(1.0, e['bw'] * PX / 72):.1f}px solid #{e['border']}")
                    st.append({"t": "justify-content:flex-start", "m": "justify-content:center", "b": "justify-content:flex-end"}[cd["valign"]])
                    st.append(f"padding:{e['my'] * PX:.1f}px {e['mx'] * PX:.1f}px")
                    dd = dict(size=cd["size"], bold=cd["bold"], color=cd["color"], align=cd["align"], indent=0.2)
                    out.append(f"<div class='e' style='{';'.join(st)}'>{_paras_html(dd, cd['paras'])}</div>")
                    x += e["colw"][c]
                y += e["rowh"][r]
    if svg:
        out.append(f"<svg class='v' width='{W * PX:.0f}' height='{H * PX:.0f}' xmlns='http://www.w3.org/2000/svg'>{''.join(svg)}</svg>")
    out.append("</section>")
    return "\n".join(out)


def build_html(slides, path, title):
    css = ("@page{size:%.3fin %.3fin;margin:0}"
           "html,body{margin:0;padding:0;background:#fff}"
           ".s{position:relative;width:%dpx;height:%dpx;overflow:hidden;font-family:Arial,Helvetica,sans-serif;"
           "-webkit-print-color-adjust:exact;print-color-adjust:exact;page-break-after:always;break-after:page}"
           ".s:last-child{page-break-after:auto;break-after:auto}"
           ".e{position:absolute;box-sizing:border-box;display:flex;flex-direction:column;margin:0}"
           ".p{line-height:%s;white-space:normal;overflow-wrap:normal}"
           ".v{position:absolute;left:0;top:0;pointer-events:none}"
           "body.one .s{display:none}body.one .s.on{display:block}") % (W, H, round(W * PX), round(H * PX), LH)
    body = "\n".join(slide_html(s) for s in slides)
    js = ("<script>var m=location.hash.match(/s(\\d+)/);if(m){document.body.className='one';"
          "var el=document.getElementById('s'+m[1]);if(el)el.className='s on';}</script>")
    Path(path).write_text(f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>{html.escape(title)}</title>"
                          f"<style>{css}</style></head><body>{body}{js}</body></html>", encoding="utf-8")
