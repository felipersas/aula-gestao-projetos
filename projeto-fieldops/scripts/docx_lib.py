#!/usr/bin/env python3
"""Utilitarios para montar o relatorio sobre o template do professor (python-docx + XML)."""
import copy
import re

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

FONT = "Arial"
TEXT_W = 9071  # largura util em twips (A4, margens 3 / 2 cm)


# ------------------------------------------------------------------ baixo nivel
def set_font(run, size=12, bold=None, italic=None, color=None):
    rpr = run._r.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for a in ("ascii", "hAnsi", "cs", "eastAsia"):
        rf.set(qn("w:" + a), FONT)
    run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def pfmt(p, align=None, line=None, before=None, after=None, first=None, left=None, hanging=None, keep_next=False, page_break_before=False,
         keep_lines=False):
    pf = p.paragraph_format
    if align is not None:
        pf.alignment = align
    if line is not None:
        pf.line_spacing = line
    if before is not None:
        pf.space_before = Pt(before)
    if after is not None:
        pf.space_after = Pt(after)
    if first is not None:
        pf.first_line_indent = Cm(first)
    if left is not None:
        pf.left_indent = Cm(left)
    if hanging is not None:
        pf.first_line_indent = Cm(-hanging)
    if keep_next:
        pf.keep_with_next = True
    if keep_lines:
        pf.keep_together = True
    if page_break_before:
        pf.page_break_before = True


def add_runs(p, text, size=12, bold=False, italic=False, color=None):
    """suporta **negrito** e __italico__ no texto."""
    partes = re.split(r"(\*\*.+?\*\*|__.+?__)", text)
    for part in partes:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            r = p.add_run(part[2:-2])
            set_font(r, size, True, italic, color)
        elif part.startswith("__") and part.endswith("__"):
            r = p.add_run(part[2:-2])
            set_font(r, size, bold, True, color)
        else:
            r = p.add_run(part)
            set_font(r, size, bold, italic, color)


def fld_runs(p, instr, cached, size=12, bold=False):
    """insere um campo simples (begin/instr/separate/texto/end) em runs."""
    def mk(kind):
        r = p.add_run()
        set_font(r, size, bold)
        fc = OxmlElement("w:fldChar")
        fc.set(qn("w:fldCharType"), kind)
        r._r.append(fc)
        return r
    mk("begin")
    r = p.add_run()
    set_font(r, size, bold)
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = " %s " % instr
    r._r.append(it)
    mk("separate")
    r = p.add_run(cached)
    set_font(r, size, bold)
    mk("end")


# ------------------------------------------------------------------ tabelas
def _cell_borders(tc, **kw):
    tcPr = tc.get_or_add_tcPr()
    b = tcPr.find(qn("w:tcBorders"))
    if b is None:
        b = OxmlElement("w:tcBorders")
        tcPr.append(b)
    for edge, val in kw.items():
        el = OxmlElement("w:" + edge)
        if val is None:
            el.set(qn("w:val"), "nil")
        else:
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(val))
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), "000000")
        b.append(el)


def _shade(tc, fill):
    tcPr = tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), fill)
    tcPr.append(sh)


def make_table(doc, cab, linhas, widths, kind="Quadro", size=9, align=None, bold_rows=(), fills=None, cell_fills=None, header_fill="E7ECEF",
               first_col_bold=False, total=None):
    """widths em twips (soma = TEXT_W). kind: 'Quadro' (bordas totais) ou 'Tabela' (so linhas horizontais)."""
    total = total or TEXT_W
    assert abs(sum(widths) - total) <= 5, sum(widths)
    n = len(cab)
    t = doc.add_table(rows=1 + len(linhas), cols=n)
    tbl = t._tbl
    tblPr = tbl.tblPr
    for el in list(tblPr):
        if el.tag in (qn("w:tblStyle"), qn("w:tblW"), qn("w:tblLayout")):
            tblPr.remove(el)
    tw = OxmlElement("w:tblW")
    tw.set(qn("w:w"), str(total))
    tw.set(qn("w:type"), "dxa")
    tblPr.append(tw)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)
    mar = OxmlElement("w:tblCellMar")
    for side, v in (("top", 30), ("left", 70), ("bottom", 30), ("right", 70)):
        e = OxmlElement("w:" + side)
        e.set(qn("w:w"), str(v))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tblPr.append(mar)
    grid = tbl.tblGrid
    for gc, wv in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(wv))
    align = align or ["l"] * n
    jc = {"l": WD_ALIGN_PARAGRAPH.LEFT, "c": WD_ALIGN_PARAGRAPH.CENTER, "r": WD_ALIGN_PARAGRAPH.RIGHT}
    todas = [cab] + linhas
    for i, row in enumerate(todas):
        tr = t.rows[i]._tr
        trPr = tr.get_or_add_trPr()
        cs = OxmlElement("w:cantSplit")
        trPr.append(cs)
        if i == 0:
            th = OxmlElement("w:tblHeader")
            trPr.append(th)
        for j, val in enumerate(row):
            cell = t.rows[i].cells[j]
            cell.width = Emu_from_twips(widths[j])
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            if tcPr.find(qn("w:tcW")) is None:
                w_ = OxmlElement("w:tcW")
                w_.set(qn("w:w"), str(widths[j]))
                w_.set(qn("w:type"), "dxa")
                tcPr.insert(0, w_)
            else:
                tcPr.find(qn("w:tcW")).set(qn("w:w"), str(widths[j]))
                tcPr.find(qn("w:tcW")).set(qn("w:type"), "dxa")
            if kind == "Quadro":
                _cell_borders(tc, top=4, left=4, bottom=4, right=4)
            else:
                if i == 0:
                    _cell_borders(tc, top=8, bottom=4, left=None, right=None)
                elif i == len(todas) - 1:
                    _cell_borders(tc, bottom=8, top=None, left=None, right=None)
                else:
                    _cell_borders(tc, top=None, bottom=None, left=None, right=None)
            if i == 0 and header_fill:
                _shade(tc, header_fill)
            elif fills and fills.get(i):
                _shade(tc, fills[i])
            if cell_fills and (i, j) in cell_fills:
                _shade(tc, cell_fills[(i, j)])
            vA = OxmlElement("w:vAlign")
            vA.set(qn("w:val"), "center" if (i == 0 or kind == "Tabela") else "top")
            tcPr.append(vA)
            p = cell.paragraphs[0]
            pfmt(p, align=(WD_ALIGN_PARAGRAPH.CENTER if i == 0 else jc[align[j]]), line=1.0, before=0, after=0)
            texto = str(val)
            partes = texto.split("\n")
            for k, parte in enumerate(partes):
                if k:
                    p = cell.add_paragraph()
                    pfmt(p, align=(WD_ALIGN_PARAGRAPH.CENTER if i == 0 else jc[align[j]]), line=1.0, before=2, after=0)
                bold = (i == 0) or (i - 1 in bold_rows) or (first_col_bold and j == 0)
                add_runs(p, parte, size=size, bold=bold)
    return t


def Emu_from_twips(tw):
    from docx.shared import Twips
    return Twips(tw)


# ------------------------------------------------------------------ remocao de relacoes sem uso
def limpa_rels(doc):
    xml = doc.element.xml
    for rid, rel in list(doc.part.rels.items()):
        if rel.reltype.endswith("/hyperlink") or rel.reltype.endswith("/image"):
            if ('"%s"' % rid) not in xml:
                del doc.part.rels[rid]
