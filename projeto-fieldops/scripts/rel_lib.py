#!/usr/bin/env python3
"""Biblioteca de montagem dos dois documentos (sobre o Template - Relatorio Final.docx do professor)."""
import copy
import re
import shutil
import zipfile
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from PIL import Image

import docx_lib as D

RAIZ = Path(__file__).resolve().parent.parent
IMG = RAIZ / "img"
TEMPLATE = Path("/Users/felipersas/Documents/Facul/gestao-proj/material/Template/Template - Relatório Final.docx")
J = WD_ALIGN_PARAGRAPH.JUSTIFY
CEN = WD_ALIGN_PARAGRAPH.CENTER
LEFT = WD_ALIGN_PARAGRAPH.LEFT
GRUPO = ["Felipe Marques", "Gabriel Ribeiro", "Pedro Dias", "André Fernandes", "João Victor Souza"]
W_PORT = D.TEXT_W          # 9071 twips (16 cm)
W_LAND = 14003             # 24,7 cm


class Rel:
    def __init__(self, titulo_capa, saida, titulo_prop, assunto):
        self.saida = Path(saida)
        self.doc = Document(str(TEMPLATE))
        self.body = self.doc.element.body
        self.filhos = list(self.body)
        assert len(self.filhos) == 349
        self.CAP = {"Figura": [], "Tabela": [], "Quadro": []}
        self.CONT = {"Figura": 0, "Tabela": 0, "Quadro": 0}
        self.TOC = []
        self.REFMAP = {}
        self.largura = W_PORT
        self.landscape = False
        self.titulo_prop, self.assunto = titulo_prop, assunto
        self._capa(titulo_capa)
        for el in self.filhos[59:348]:
            self.body.remove(el)

    # ---------------------------------------------------------- capa
    def _set_text(self, par_el, texto):
        primeiro = True
        for r in par_el.findall(qn("w:r")):
            for t in r.findall(qn("w:t")):
                if primeiro:
                    t.text = texto
                    primeiro = False
                else:
                    t.text = ""

    def _clone_after(self, el, texto):
        novo = copy.deepcopy(el)
        self._set_text(novo, texto)
        el.addnext(novo)
        return novo

    def _capa(self, titulo):
        f = self.filhos

        def tira(inicio, n):
            for k in range(inicio, inicio + n):
                assert not "".join(t.text or "" for t in f[k].iter(qn("w:t"))).strip(), k
                self.body.remove(f[k])

        for idx_nome, idx_tit, vn, vt in ((9, 17, (10, 4), (18, 3)), (29, 37, (30, 4), (38, 3))):
            self._set_text(f[idx_nome], GRUPO[0])
            ant = f[idx_nome]
            for n in GRUPO[1:]:
                ant = self._clone_after(ant, n)
            self._set_text(f[idx_tit], titulo)
            tira(*vn)
            tira(*vt)
        for k in (27, 57):
            for c in list(f[k].iter(qn("w:color"))):
                c.getparent().remove(c)

    # ---------------------------------------------------------- texto
    def par(self, texto="", size=12, align=J, first=1.27, line=1.5, before=0, after=6, bold=False, italic=False, keep_next=False, left=None, hanging=None):
        p = self.doc.add_paragraph()
        D.pfmt(p, align=align, line=line, before=before, after=after, first=first if hanging is None else None, left=left, hanging=hanging, keep_next=keep_next)
        if texto:
            D.add_runs(p, texto, size=size, bold=bold, italic=italic)
        return p

    corpo = par

    def alineas(self, itens):
        for i, t in enumerate(itens):
            letra = "abcdefghijklmnopqrstuvwxyz"[i]
            fim = "." if i == len(itens) - 1 else ";"
            self.par(f"{letra}) {t.rstrip('.;')}{fim}", first=None, left=1.9, hanging=0.63, after=3)

    def h1(self, texto, quebra=True):
        p = self.doc.add_paragraph(style="Heading 1")
        D.pfmt(p, line=1.5, before=0, after=12, page_break_before=quebra, keep_next=True)
        D.set_font(p.add_run(texto), 12, True)
        self.TOC.append((1, texto))
        return p

    def h2(self, texto, quebra=False, toc=True):
        p = self.doc.add_paragraph(style="Heading 2")
        D.pfmt(p, line=1.5, before=12, after=6, keep_next=True, page_break_before=quebra)
        D.set_font(p.add_run(texto), 12, True)
        if toc:
            self.TOC.append((2, texto))
        return p

    def h3(self, texto):
        p = self.doc.add_paragraph(style="Heading 3")
        D.pfmt(p, line=1.5, before=6, after=3, keep_next=True)
        D.set_font(p.add_run(texto), 12, True, True)
        return p

    # ---------------------------------------------------------- legendas, figuras, tabelas
    def legenda(self, tipo, titulo, key=None, keep=True):
        self.CONT[tipo] += 1
        n = self.CONT[tipo]
        self.CAP[tipo].append((n, titulo))
        if key:
            assert key not in self.REFMAP, key
            self.REFMAP[key] = (tipo, n)
        p = self.doc.add_paragraph()
        D.pfmt(p, align=CEN, line=1.0, before=10, after=4, keep_next=keep)
        D.add_runs(p, f"{tipo} ", size=11, bold=True)
        D.fld_runs(p, f"SEQ {tipo} \\* ARABIC", str(n), size=11, bold=True)
        D.add_runs(p, f" – {titulo}", size=11, bold=True)
        return p

    def fonte(self, texto="Elaborado pelos autores (2026)."):
        p = self.doc.add_paragraph()
        D.pfmt(p, align=CEN, line=1.0, before=3, after=12)
        D.add_runs(p, "Fonte: " + texto, size=10)
        return p

    def figura(self, arquivo, titulo, largura_cm=16.0, altura_max_cm=None, fonte_txt="Elaborado pelos autores (2026).", key=None):
        wmax = 24.5 if self.landscape else 15.9
        hmax = altura_max_cm or (12.3 if self.landscape else 19.5)
        im = Image.open(IMG / arquivo)
        asp = im.size[0] / im.size[1]
        w = min(largura_cm, wmax, hmax * asp)
        self.legenda("Figura", titulo, key)
        p = self.doc.add_paragraph()
        D.pfmt(p, align=CEN, line=1.0, before=0, after=0, keep_next=True)
        p.add_run().add_picture(str(IMG / arquivo), width=Cm(w))
        self.fonte(fonte_txt)

    def w_(self, rel):
        tot = sum(rel)
        tw = [round(c / tot * self.largura) for c in rel]
        tw[-1] += self.largura - sum(tw)
        return tw

    def tabela(self, titulo, cab, linhas, rel_widths, kind="Quadro", fonte_txt="Elaborado pelos autores (2026).", key=None, size=9, **kw):
        self.legenda(kind, titulo, key, keep=(len(linhas) <= 12))
        t = D.make_table(self.doc, cab, linhas, self.w_(rel_widths), kind=kind, size=size, total=self.largura, **kw)
        self.fonte(fonte_txt)
        return t

    # ---------------------------------------------------------- secoes
    def secao_retrato(self):
        s = self.doc.add_section(WD_SECTION.NEW_PAGE)
        s.orientation = WD_ORIENT.PORTRAIT
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        self.largura, self.landscape = W_PORT, False

    def secao_paisagem(self):
        s = self.doc.add_section(WD_SECTION.NEW_PAGE)
        s.orientation = WD_ORIENT.LANDSCAPE
        s.page_width, s.page_height = Cm(29.7), Cm(21.0)
        self.largura, self.landscape = W_LAND, True

    # ---------------------------------------------------------- pre-textuais
    def titulo_pre(self, texto, quebra=True):
        p = self.doc.add_paragraph()
        D.pfmt(p, align=CEN, line=2.0, before=0, after=0, page_break_before=quebra)
        D.add_runs(p, texto, size=14, bold=True)
        return p

    def resumo(self, resumo, kw, abstract, kw_en):
        self.titulo_pre("RESUMO", quebra=False)
        self.par("", after=0)
        self.par(resumo, first=1.25, line=1.0, after=12)
        self.par("**Palavras-chave:** " + kw, first=None, line=1.0)
        self.titulo_pre("ABSTRACT")
        self.par("", after=0)
        self.par(abstract, first=1.25, line=1.0, after=12)
        self.par("**Keywords:** " + kw_en, first=None, line=1.0)

    def placeholders_listas(self):
        self.LISTAS = {}
        for chave, tit in (("Figura", "LISTA DE ILUSTRAÇÕES"), ("Tabela", "LISTA DE TABELAS"), ("Quadro", "LISTA DE QUADROS")):
            self.titulo_pre(tit)
            self.LISTAS[chave] = self.doc.add_paragraph()
            D.pfmt(self.LISTAS[chave], line=1.0, after=0)

    def lista_sigla(self, tit, itens):
        self.titulo_pre(tit)
        for a, b in itens:
            p = self.doc.add_paragraph()
            D.pfmt(p, align=LEFT, line=1.15, before=0, after=4, left=4.6, hanging=4.6)
            D.add_runs(p, f"**{a}**\t{b}", size=12)
            pPr = p._p.get_or_add_pPr()
            tabs = OxmlElement("w:tabs")
            tb = OxmlElement("w:tab")
            tb.set(qn("w:val"), "left")
            tb.set(qn("w:pos"), str(round(4.6 * 567)))
            tabs.append(tb)
            pPr.append(tabs)

    def sumario_placeholder(self):
        self.titulo_pre("SUMÁRIO")
        self.SUMARIO = self.doc.add_paragraph()
        D.pfmt(self.SUMARIO, line=1.0, after=0)
        self.doc.add_section(WD_SECTION.NEW_PAGE)

    # ---------------------------------------------------------- fim
    def _lista(self, ph, chave):
        itens = self.CAP[chave]
        ph_el = ph._p
        for k, (n, tit) in enumerate(itens):
            p = self.doc.add_paragraph()
            D.pfmt(p, align=LEFT, line=1.15, before=0, after=4)
            if k == 0:
                self._campo(p, "begin"); self._instr(p, f' TOC \\h \\z \\c "{chave}" '); self._campo(p, "separate")
            D.add_runs(p, f"{chave} {n} – {tit}", size=11)
            if k == len(itens) - 1:
                self._campo(p, "end")
            ph_el.addnext(p._p)
            ph_el = p._p
        ph._p.getparent().remove(ph._p)

    @staticmethod
    def _campo(p, kind):
        r = p.add_run()
        fc = OxmlElement("w:fldChar")
        fc.set(qn("w:fldCharType"), kind)
        r._r.append(fc)

    @staticmethod
    def _instr(p, texto):
        r = p.add_run()
        it = OxmlElement("w:instrText")
        it.set(qn("xml:space"), "preserve")
        it.text = texto
        r._r.append(it)

    def _sumario(self):
        ph_el = self.SUMARIO._p
        for k, (nivel, tit) in enumerate(self.TOC):
            p = self.doc.add_paragraph()
            D.pfmt(p, align=LEFT, line=1.15, before=(6 if nivel == 1 else 0), after=2, left=(0 if nivel == 1 else 0.8))
            if k == 0:
                self._campo(p, "begin"); self._instr(p, ' TOC \\o "1-2" \\h \\z \\u '); self._campo(p, "separate")
            D.add_runs(p, tit, size=11, bold=(nivel == 1))
            if k == len(self.TOC) - 1:
                self._campo(p, "end")
            ph_el.addnext(p._p)
            ph_el = p._p
        self.SUMARIO._p.getparent().remove(self.SUMARIO._p)

    def finalizar(self, keywords=""):
        doc = self.doc
        for chave in ("Figura", "Tabela", "Quadro"):
            self._lista(self.LISTAS[chave], chave)
        self._sumario()
        # cabecalho com numero de pagina na secao textual (2a secao)
        sec_txt = doc.sections[1]
        sec_txt.header.is_linked_to_previous = False
        hp = sec_txt.header.paragraphs[0]
        D.pfmt(hp, align=WD_ALIGN_PARAGRAPH.RIGHT, line=1.0, after=0)
        D.fld_runs(hp, "PAGE", "1", size=10)
        sec_txt.header_distance = Cm(1.25)
        for k, sec in enumerate(doc.sections):
            if k >= 2:
                for e in sec._sectPr.findall(qn("w:pgNumType")):
                    sec._sectPr.remove(e)
        cp = doc.core_properties
        cp.title, cp.author, cp.subject, cp.comments, cp.keywords = self.titulo_prop, ", ".join(GRUPO), self.assunto, "", keywords
        uf = OxmlElement("w:updateFields")
        uf.set(qn("w:val"), "true")
        compat = doc.settings.element.find(qn("w:compat"))
        if compat is not None:
            compat.addprevious(uf)
        else:
            doc.settings.element.append(uf)
        pad = re.compile(r"@([QTF]):(\w+)@")
        nome = {"Q": "Quadro", "T": "Tabela", "F": "Figura"}
        for t in doc.element.body.iter(qn("w:t")):
            if t.text and "@" in t.text:
                def sub(m):
                    tipo, n = self.REFMAP[m.group(2)]
                    return f"{tipo} {n}"
                t.text = pad.sub(sub, t.text)
        D.limpa_rels(doc)
        doc.save(str(self.saida))
        tmp = self.saida.with_suffix(".tmp.docx")
        with zipfile.ZipFile(self.saida) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/footnotes.xml":
                    s = data.decode("utf8")
                    s = re.sub(r"<w:footnote [^>]*w:id=\"0\"[^>]*>.*?</w:footnote>", "", s, flags=re.S)
                    data = s.encode("utf8")
                if item.filename == "word/_rels/footnotes.xml.rels":
                    s = data.decode("utf8")
                    s = re.sub(r"<Relationship [^>]*ipam[^>]*/>", "", s)
                    data = s.encode("utf8")
                zout.writestr(item, data)
        shutil.move(str(tmp), str(self.saida))
        return dict(self.CONT)
