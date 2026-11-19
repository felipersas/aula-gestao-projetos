#!/usr/bin/env python3
"""
Slide executivo (1 slide, 16:9) da proposta do PMO da MetalTech.

Uma unica especificacao de layout (lista de primitivas em polegadas) gera:
  - slide-executivo.pptx   (nativo e editavel: formas, tabela de formas e textos reais; python-pptx)
  - slide-executivo.html   (referencia, mesma geometria) -> Chrome headless -> .png e .pdf
Os numeros vem de modelo_portfolio.py.
"""
import html
import subprocess
import sys
from pathlib import Path

from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

import modelo_portfolio as M
from conteudo import br, mil

RAIZ = Path(__file__).resolve().parent.parent
FONT = "Arial"
W, H = 13.333, 7.5

# ------------------------------------------------------------------ paleta
PETROL = "0F4C5C"
PETROL2 = "2A7F91"
TEAL_L = "6BA8B5"
GRAFITE = "2B2F33"
CINZA = "5F6B73"
CLARO = "E8EEF1"
CLARO2 = "F3F6F7"
BRANCO = "FFFFFF"
VERDE = "2E8B57"
AMARELO = "E0A800"
VERMELHO = "C0392B"
LARANJA = "D9822B"

EL = []  # elementos


def rect(x, y, w, h, fill=None, line=None, lw=0.75, dash=False, shape="rect", name="", rot=0):
    EL.append(dict(k="shape", x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw, dash=dash, shape=shape, name=name, paras=None))


def text(x, y, w, h, paras, size=10, bold=False, color=GRAFITE, align="l", valign="m", fill=None, line=None, lw=0.75,
         dash=False, shape="rect", mx=0.05, my=0.02, name="", space=0):
    """paras: str | list[str | list[(texto, {bold,color,size})]]"""
    if isinstance(paras, str):
        paras = [paras]
    nb = lambda t: t.replace("R$ ", "R$\u00a0")
    paras = [nb(p) if isinstance(p, str) else [(nb(t), st) for t, st in p] for p in paras]
    EL.append(dict(k="shape", x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw, dash=dash, shape=shape, name=name,
                   paras=paras, size=size, bold=bold, color=color, align=align, valign=valign, mx=mx, my=my, space=space))


def line(x1, y1, x2, y2, color=CINZA, lw=0.75, dash=False):
    EL.append(dict(k="line", x1=x1, y1=y1, x2=x2, y2=y2, color=color, lw=lw, dash=dash))


# ------------------------------------------------------------------ conteudo do slide
def build():
    EL.clear()
    X1, W1 = 0.35, 4.05
    X2, W2 = 4.58, 4.40
    X3, W3 = 9.16, 3.82

    # fundo
    rect(0, 0, W, H, fill=BRANCO, name="fundo")
    # titulo
    rect(0, 0, W, 1.02, fill=PETROL, name="faixa titulo")
    text(0.35, 0.06, 12.63, 0.9,
         "5 projetos priorizados (R$ 2,1 mi) + R$ 0,4 mi de reserva: cada uma das 4 metas tem um projeto responsável, dentro do teto de R$ 2,5 mi",
         size=24, bold=True, color=BRANCO, valign="m", name="titulo")

    def secao(x, y, w, txt, num):
        text(x, y, 0.3, 0.27, str(num), size=11, bold=True, color=BRANCO, fill=PETROL2, align="c", name="num " + txt)
        text(x + 0.34, y, w - 0.34, 0.27, txt, size=11, bold=True, color=PETROL, name="secao " + txt, mx=0.02)
        line(x, y + 0.29, x + w, y + 0.29, color=CLARO, lw=1.0)

    # ================= coluna 1: portfolio + programas
    secao(X1, 1.12, W1, "PORTFÓLIO: 8 projetos, 3 decisões", 1)
    cols = [("ID", 0.36), ("Projeto", 1.66), ("R$ mil", 0.55), ("Nota", 0.45), ("Decisão", 1.03)]
    y0 = 1.46
    xx = X1
    for nome, wd in cols:
        text(xx, y0, wd, 0.24, nome, size=10, bold=True, color=BRANCO, fill=GRAFITE, align="c" if nome != "Projeto" else "l", name="cab " + nome)
        xx += wd
    nomes = {"P1": "Automação Linha 1", "P2": "Manutenção Preditiva", "P4": "Redução de Refugo", "P5": "Controle de Qualidade",
             "P6": "Treinamento Operadores", "P7": "Monitoramento IoT", "P3": "Novo ERP Industrial", "P8": "Expansão Capacidade"}
    ordem = ["P1", "P2", "P4", "P5", "P6", "P7", "P3", "P8"]
    rh = 0.255
    for i, p in enumerate(ordem):
        y = y0 + 0.24 + i * rh
        dec = M.DECISAO[p]
        corf = {"Prioridade": VERDE, "Posterior": AMARELO, "Adiado": VERMELHO}[dec]
        cort = {"Prioridade": BRANCO, "Posterior": GRAFITE, "Adiado": BRANCO}[dec]
        rotulo = dec
        bg = CLARO2 if i % 2 == 0 else BRANCO
        xx = X1
        vals = [p, nomes[p], br(M.PROJ[p]["inv"]), br(M.SCORE[p], 2)]
        for (nome, wd), v in zip(cols[:4], vals):
            text(xx, y, wd, rh, v, size=10, bold=(nome == "ID"), color=GRAFITE, fill=bg, align="l" if nome == "Projeto" else "c", name=f"{p} {nome}")
            xx += wd
        text(xx, y, cols[4][1], rh, rotulo, size=10, bold=True, color=cort, fill=corf, align="c", name=f"{p} decisao", line=BRANCO, lw=1.0)
    yfim = y0 + 0.24 + 8 * rh
    text(X1, yfim + 0.01, W1, 0.2, "Nota: matriz de 1 a 5 · P7 entra só se o G2 aprovar", size=10, color=CINZA, name="nota matriz", mx=0.02)

    secao(X1, 4.02, W1, "PROGRAMAS", 2)
    ycard = 4.37
    ch = 0.48
    progs = [
        ("A", PETROL, "A  Excelência Operacional", "R$ 1,5 mi", "P1 + P2 + P6: produtividade +15%, paradas −20%", False),
        ("B", PETROL2, "B  Qualidade 4.0 (fase 1)", "R$ 0,6 mi", "P4 + P5: retrabalho −30%, custos −10%", False),
        ("C", CINZA, "C  Transformação Digital", "não ativado", "P3 e P7 viram candidatos a 2027", True),
    ]
    for i, (k, cor, tit, val, desc, tracejado) in enumerate(progs):
        y = ycard + i * (ch + 0.04)
        if tracejado:
            text(X1, y, W1, ch, "", fill=BRANCO, line=CINZA, lw=1.0, dash=True, name="prog " + k)
        else:
            rect(X1, y, W1, ch, fill=CLARO2, name="prog " + k)
            rect(X1, y, 0.09, ch, fill=cor, name="prog barra " + k)
        text(X1 + 0.14, y + 0.02, W1 - 1.2, 0.24, tit, size=10, bold=True, color=cor if not tracejado else CINZA, name="prog tit " + k, mx=0.02)
        text(X1 + W1 - 1.1, y + 0.02, 1.05, 0.24, val, size=10, bold=True, color=cor if not tracejado else CINZA, align="r", name="prog val " + k, mx=0.02)
        text(X1 + 0.14, y + 0.24, W1 - 0.2, 0.22, desc, size=10, color=GRAFITE, name="prog desc " + k, mx=0.02)

    # ================= coluna 2: roadmap + investimento
    secao(X2, 1.12, W2, "ROADMAP DE 12 MESES", 3)
    lab = 0.42
    gw = (W2 - lab) / 12
    yr = 1.46
    for t in range(4):
        text(X2 + lab + t * 3 * gw, yr, 3 * gw, 0.23, f"T{t + 1}", size=10, bold=True, color=BRANCO, fill=PETROL if t % 2 == 0 else PETROL2,
             align="c", line=BRANCO, lw=1.0, name=f"T{t + 1}")
    for m in range(12):
        text(X2 + lab + m * gw, yr + 0.23, gw, 0.2, str(m + 1), size=10, color=CINZA, align="c", mx=0, my=0, name=f"m{m + 1}")
    linhas = [("P1", "P1", PETROL), ("P2", "P2", PETROL2), ("P4", "P4", TEAL_L), ("P5", "P5", "8C9A5B"), ("P6", "P6", "C98B3A"), ("P7", "P7", None), ("BM", "", None)]
    ry0 = yr + 0.46
    rhh = 0.25
    for m in range(13):
        line(X2 + lab + m * gw, ry0, X2 + lab + m * gw, ry0 + len(linhas) * rhh, color=CLARO, lw=0.5)
    ym = ry0 + len(linhas) * rhh + 0.03
    marcos = [("G1", 3, GRAFITE), ("FAT", 4, CINZA), ("G2", 6, AMARELO)]
    for cod, m, cor in marcos:  # linhas dos marcos ficam atras das barras
        xc = X2 + lab + m * gw
        line(xc, ry0, xc, ym, color=cor, lw=1.0, dash=True)
    bh_ = 0.2
    for i, (p, lbl, cor) in enumerate(linhas):
        y = ry0 + i * rhh + (rhh - bh_) / 2
        if p == "BM":
            text(X2 + lab + 6 * gw, y, 6 * gw, bh_, "hypercare · balanço m9, m12", size=10, color=PETROL, bold=True, fill=CLARO, line=PETROL, lw=0.75,
                 align="c", mx=0.02, my=0, name="barra BM")
            continue
        text(X2, y, lab, bh_, lbl, size=10, bold=True, color=GRAFITE, align="c", mx=0, my=0, name="rot " + p)
        i0, i1 = M.JANELA[p]
        if p == "P7":
            text(X2 + lab + (i0 - 1) * gw, y, (i1 - i0 + 1) * gw, bh_, "só se o G2 aprovar", size=10, bold=True, color=GRAFITE, fill=BRANCO, line=AMARELO,
                 lw=1.75, dash=True, align="c", mx=0.02, my=0, name="barra P7")
        else:
            txt = f"m{i0}–m{i1}"
            text(X2 + lab + (i0 - 1) * gw, y, (i1 - i0 + 1) * gw, bh_, txt, size=10, bold=True, color=BRANCO, fill=cor, align="c", mx=0.02, my=0, name="barra " + p)
    for cod, m, cor in marcos:
        xc = X2 + lab + m * gw
        rect(xc - 0.09, ym, 0.18, 0.18, fill=cor, line=GRAFITE, lw=0.75, shape="diamond", name="marco " + cod)
    text(X2 + lab + 3 * gw - 0.74, ym - 0.01, 0.6, 0.2, "G1", size=10, bold=True, color=GRAFITE, align="r", mx=0.0, my=0, name="lbl G1")
    text(X2 + lab + 4 * gw + 0.1, ym - 0.01, 0.5, 0.2, "FAT", size=10, bold=True, color=GRAFITE, align="l", mx=0.0, my=0, name="lbl FAT")
    text(X2 + lab + 6 * gw + 0.12, ym - 0.01, 1.7, 0.2, "G2: decide o P7", size=10, bold=True, color=GRAFITE, align="l", mx=0.0, my=0, name="lbl G2")

    yi = 4.02
    secao(X2, yi, W2, "INVESTIMENTO: R$ 2,5 mi", 4)
    seg = [("P1", 900, PETROL), ("P2", 450, PETROL), ("P6", 150, PETROL), ("P4", 250, PETROL2), ("P5", 350, PETROL2), ("Reserva", 400, None)]
    yb = yi + 0.6
    bh = 0.46
    esc = W2 / M.ORCAMENTO_TETO
    xs = X2
    wa = (900 + 450 + 150) * esc
    wbp = (250 + 350) * esc
    text(X2, yb - 0.26, wa, 0.24, "Programa A: R$ 1,5 mi", size=10, bold=True, color=PETROL, mx=0.02, name="lbl prog A")
    text(X2 + wa, yb - 0.26, wbp, 0.24, "B: R$ 0,6 mi", size=10, bold=True, color=PETROL2, mx=0.02, name="lbl prog B")
    for nome, v, cor in seg:
        wd = v * esc
        val = br(v)
        if nome == "Reserva":
            text(xs, yb, wd, bh, [nome, val], size=10, bold=True, color=GRAFITE, fill=BRANCO, line=GRAFITE, lw=1.25, dash=True, align="c", mx=0.0, my=0.0, name="seg " + nome)
        else:
            text(xs, yb, wd, bh, [nome, val], size=10, bold=True, color=BRANCO, fill=cor, line=BRANCO, lw=1.25, align="c", mx=0.0, my=0.0, name="seg " + nome)
        xs += wd
    text(X2, yb + bh + 0.05, W2, 0.78, [
        [("R$ 2,1 mi priorizados (84%) + R$ 0,4 mi de reserva (16%)", {"bold": True})],
        f"Desembolso: T1 R$ {br(M.TRI[0], 1)} mil · T2 R$ {br(M.TRI[1], 0)} mil · T3 R$ {br(M.TRI[2], 1)} mil",
        "Reserva: P1 R$ 180 mil · P2 R$ 90 mil · P4, P5 e P6 R$ 75 mil · analista de planejamento R$ 55 mil",
    ], size=10, color=GRAFITE, valign="t", mx=0.02, name="texto invest")

    # ================= coluna 3: recursos + riscos
    secao(X3, 1.12, W3, "RECURSOS: carga mensal (%)", 5)
    lw_ = 0.46
    cw = (W3 - lw_) / 12
    yh = 1.46
    for m in range(12):
        text(X3 + lw_ + m * cw, yh, cw, 0.18, str(m + 1), size=10, color=CINZA, align="c", mx=0, my=0, name=f"hm {m + 1}")
    rhm = 0.165

    def cor_calor(v):
        if v <= 0:
            return "F0F3F5"
        if v < 50:
            return "CFE3E8"
        if v < 100:
            return TEAL_L
        return PETROL

    for i, r in enumerate(M.RECS):
        y = yh + 0.2 + i * rhm
        text(X3, y, lw_, rhm, r, size=10, bold=True, color=GRAFITE, align="l", mx=0.02, my=0, name="hm rot " + r)
        for m in range(12):
            v = M.MAT[r][m]
            rect(X3 + lw_ + m * cw + 0.01, y + 0.01, cw - 0.02, rhm - 0.02, fill=cor_calor(v), name=f"hm {r} {m + 1}")
    yl = yh + 0.2 + 7 * rhm + 0.02
    lx = X3 + lw_
    for k, (c, t) in enumerate([("CFE3E8", "<50%"), (TEAL_L, "50–99%"), (PETROL, "100%")]):
        rect(lx + k * 1.05, yl + 0.045, 0.16, 0.12, fill=c, name="leg " + t)
        text(lx + k * 1.05 + 0.19, yl, 0.8, 0.2, t, size=10, color=GRAFITE, mx=0.0, my=0, name="leg txt " + t)
    text(X3, yl + 0.21, W3, 0.56, [
        [("Conflitos resolvidos: ", {"bold": True}), (f"{len(M.CONF_ING)} sobrecargas evitadas. QUAL: P4 antes do P5 · EA: P2 sem engenheiro · "
                                                      f"P6 após o FAT · GP: {round(max(M.GP_SEM_COORD))}% → {M.PICO['GP']}% com coordenadores", {})],
    ], size=10, color=GRAFITE, valign="t", mx=0.02, my=0, name="conflitos")

    yr2 = 3.68
    secao(X3, yr2, W3, "RISCOS: 4 maiores (severidade)", 6)
    top = [R for R in M.RISCOS_DADOS if R["id"] in ("R03", "R01", "R02", "R07")]
    txts = {
        "R03": [("Benefício parcial: ", {"bold": True}), ("P2 e P5 sem folga. Linha de base no m1, meta interna +10%", {})],
        "R01": [("P1 atrasa ou estoura: ", {"bold": True}), ("reserva de R$ 180 mil e FAT como gate", {})],
        "R02": [("GP único (115% no m1): ", {"bold": True}), ("coordenadores locais; analista externo", {})],
        "R07": [("Poucos especialistas: ", {"bold": True}), ("backup entre pares e documentação semanal", {})],
    }
    rr = 0.46
    for i, R in enumerate(top):
        y = yr2 + 0.36 + i * rr
        cor = VERMELHO if R["sev"] >= 0.18 else LARANJA
        text(X3, y, 0.52, rr - 0.05, br(R["sev"], 2), size=11, bold=True, color=BRANCO, fill=cor, align="c", name="sev " + R["id"])
        text(X3 + 0.56, y, W3 - 0.56, rr - 0.05, [txts[R["id"]]], size=10, color=GRAFITE, fill=CLARO2, valign="m", mx=0.06, my=0, name="risco " + R["id"])

    # ================= metas
    ym0 = 5.98
    mw = (12.63 - 3 * 0.1) / 4
    metas = [
        ("+15% produtividade", "P1 (+12%) e P6", "faltam 3 p.p.", AMARELO),
        ("−20% paradas", "P2 (−20%)", "folga zero", AMARELO),
        ("−10% custos", "P4 e P5 (indireto)", "a medir", CINZA),
        ("−30% retrabalho", "P5 (−30%)", "folga zero", AMARELO),
    ]
    for i, (meta, proj, folga, cor) in enumerate(metas):
        x = 0.35 + i * (mw + 0.1)
        rect(x, ym0, mw, 0.64, fill=CLARO2, name="meta " + meta)
        rect(x, ym0, 0.09, 0.64, fill=cor, name="meta barra " + meta)
        text(x + 0.14, ym0 + 0.02, mw - 0.18, 0.3, [[(meta, {"bold": True, "color": PETROL, "size": 12})]], size=12, valign="m", name="meta tit " + meta, mx=0.02)
        text(x + 0.14, ym0 + 0.31, mw - 0.18, 0.3, [[("→ " + proj, {"bold": True}), (" · " + folga, {})]], size=10, valign="m", name="meta desc " + meta, mx=0.02)

    # ================= recomendacao
    yb2 = 6.72
    hb = 0.66
    rect(0.35, yb2, 12.63, hb, fill=GRAFITE, name="banner")
    text(0.35, yb2, 1.6, hb, ["RECOMENDAÇÃO", "DO PMO"], size=11, bold=True, color=BRANCO, fill=VERDE, align="c", name="banner rotulo", mx=0.05)
    text(2.0, yb2, 7.15, hb, "Aprovar P1, P2, P4, P5 e P6 (R$ 2,1 mi), manter R$ 0,4 mi de reserva sob o PMO, decidir o P7 no gate G2 (fim do m6) e adiar P3 e P8.",
         size=14, bold=True, color=BRANCO, valign="m", mx=0.08, name="banner decisao")
    line(9.2, yb2 + 0.08, 9.2, yb2 + hb - 0.08, color=CINZA, lw=0.75)
    text(9.25, yb2, 3.73, hb, [[("PEDIDO: ", {"bold": True, "color": "F2C94C"}), ("aprovar hoje R$ 2,1 mi + reserva e nomear a Controladoria para fechar a linha de base até o m1", {})]],
         size=10, color=BRANCO, valign="m", mx=0.08, name="banner pedido")


# ------------------------------------------------------------------ verificacao de ajuste de texto (PIL)
_FONTS = {}


def _font(bold, px):
    k = (bold, px)
    if k not in _FONTS:
        f = "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"
        _FONTS[k] = ImageFont.truetype(f, px)
    return _FONTS[k]


def mede(e):
    """retorna (altura_necessaria_pol, largura_max_pol, n_linhas) estimando quebra de linha em Arial."""
    if not e.get("paras"):
        return 0, 0, 0
    wmax = e["w"] - 2 * e["mx"]
    total_h = 0
    nl = 0
    scale = 10  # px por pt na medicao (precisao)
    for p in e["paras"]:
        runs = p if isinstance(p, list) else [(p, {})]
        palavras = []
        for t, st in runs:
            b = st.get("bold", e["bold"])
            sz = st.get("size", e["size"])
            for w_ in t.replace("\n", " ").split(" "):
                palavras.append((w_, b, sz))
        linhas = 1
        cur = 0.0
        psz = max([sz for _, _, sz in palavras] or [e["size"]])
        for w_, b, sz in palavras:
            wpx = _font(b, int(sz * scale)).getlength(w_ + " ") / scale  # em pt
            if cur + wpx - _font(b, int(sz * scale)).getlength(" ") / scale > wmax * 72 and cur > 0:
                linhas += 1
                cur = 0.0
            cur += wpx
        nl += linhas
        total_h += linhas * psz * 1.17 / 72
    return total_h + 2 * e["my"], wmax, nl


def confere():
    probs = []
    for e in EL:
        if e["k"] != "shape" or not e.get("paras") or e["paras"] == [""]:
            continue
        h, _, nl = mede(e)
        if h > e["h"] + 0.01:
            probs.append((e["name"], round(h, 2), e["h"], nl))
    return probs


# ------------------------------------------------------------------ PPTX
def rgb(hexa):
    return RGBColor.from_string(hexa)


def emit_pptx(path):
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    for e in EL:
        if e["k"] == "line":
            c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(e["x1"]), Inches(e["y1"]), Inches(e["x2"]), Inches(e["y2"]))
            c.line.color.rgb = rgb(e["color"])
            c.line.width = Pt(e["lw"])
            if e["dash"]:
                c.line.dash_style = MSO_LINE.DASH
            continue
        shp = {"rect": MSO_SHAPE.RECTANGLE, "diamond": MSO_SHAPE.DIAMOND, "round": MSO_SHAPE.ROUNDED_RECTANGLE}[e["shape"]]
        sh = s.shapes.add_shape(shp, Inches(e["x"]), Inches(e["y"]), Inches(e["w"]), Inches(e["h"]))
        sh.name = e["name"] or "forma"
        sh.shadow.inherit = False
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
        if e.get("paras") is None:
            continue
        tf = sh.text_frame
        tf.word_wrap = True
        tf.auto_size = None
        tf.margin_left = tf.margin_right = Inches(e["mx"])
        tf.margin_top = tf.margin_bottom = Inches(e["my"])
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[e["valign"]]
        for i, p in enumerate(e["paras"]):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[e["align"]]
            para.line_spacing = 1.0
            para.space_before = Pt(0)
            para.space_after = Pt(0)
            runs = p if isinstance(p, list) else [(p, {})]
            for t, st in runs:
                r = para.add_run()
                r.text = t
                r.font.name = FONT
                r.font.size = Pt(st.get("size", e["size"]))
                r.font.bold = st.get("bold", e["bold"])
                r.font.color.rgb = rgb(st.get("color", e["color"]))
    prs.core_properties.title = "MetalTech S.A. - Proposta do PMO: portfolio de projetos para os proximos 12 meses"
    prs.core_properties.author = "Grupo PMO MetalTech"
    prs.save(path)


# ------------------------------------------------------------------ HTML (referencia) -> png/pdf
PX = 144.0  # px por polegada: 13.333in -> 1920px


def emit_html(path):
    out = ["<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>Slide executivo MetalTech</title><style>",
           "@page{size:%.3fin %.3fin;margin:0}" % (W, H),
           "html,body{margin:0;padding:0;background:#fff}",
           "#s{position:relative;width:%dpx;height:%dpx;overflow:hidden;font-family:Arial,Helvetica,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}" % (round(W * PX), round(H * PX)),
           ".e{position:absolute;box-sizing:border-box;display:flex;flex-direction:column;margin:0}",
           ".p{margin:0;line-height:1.17;white-space:normal}",
           "</style></head><body><div id='s'>"]
    for e in EL:
        if e["k"] == "line":
            x1, y1, x2, y2 = e["x1"] * PX, e["y1"] * PX, e["x2"] * PX, e["y2"] * PX
            lw = max(1.0, e["lw"] * PX / 72)
            if abs(x1 - x2) < 1e-6:
                st = f"left:{x1 - lw / 2:.1f}px;top:{min(y1, y2):.1f}px;width:0;height:{abs(y2 - y1):.1f}px;border-left:{lw:.1f}px {'dashed' if e['dash'] else 'solid'} #{e['color']}"
            else:
                st = f"left:{min(x1, x2):.1f}px;top:{y1 - lw / 2:.1f}px;width:{abs(x2 - x1):.1f}px;height:0;border-top:{lw:.1f}px {'dashed' if e['dash'] else 'solid'} #{e['color']}"
            out.append(f"<div class='e' style='{st}'></div>")
            continue
        st = [f"left:{e['x'] * PX:.1f}px", f"top:{e['y'] * PX:.1f}px", f"width:{e['w'] * PX:.1f}px", f"height:{e['h'] * PX:.1f}px"]
        if e["fill"]:
            st.append(f"background:#{e['fill']}")
        if e["line"]:
            st.append(f"border:{max(1.0, e['lw'] * PX / 72):.1f}px {'dashed' if e['dash'] else 'solid'} #{e['line']}")
        if e["shape"] == "diamond":
            st.append("clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%)")
            if e["line"]:
                st = [x for x in st if not x.startswith("border")]
                st.append(f"background:#{e['fill']}")
        if e.get("paras") is not None:
            st.append({"t": "justify-content:flex-start", "m": "justify-content:center", "b": "justify-content:flex-end"}[e["valign"]])
            st.append(f"padding:{e['my'] * PX:.1f}px {e['mx'] * PX:.1f}px")
            st.append({"l": "text-align:left", "c": "text-align:center", "r": "text-align:right"}[e["align"]])
        out.append(f"<div class='e' style='{';'.join(st)}'>")
        if e.get("paras") is not None:
            for p in e["paras"]:
                runs = p if isinstance(p, list) else [(p, {})]
                spans = []
                for t, sty in runs:
                    b = sty.get("bold", e["bold"])
                    c = sty.get("color", e["color"])
                    sz = sty.get("size", e["size"])
                    spans.append(f"<span style='font-size:{sz * PX / 72:.1f}px;font-weight:{700 if b else 400};color:#{c}'>{html.escape(t)}</span>")
                out.append(f"<div class='p'>{''.join(spans) or '&nbsp;'}</div>")
        out.append("</div>")
    out.append("</div></body></html>")
    Path(path).write_text("\n".join(out), encoding="utf-8")


CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def render(html_path, png_path, pdf_path):
    base = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-pdf-header-footer"]
    url = Path(html_path).resolve().as_uri()
    subprocess.run(base + ["--screenshot=" + str(png_path), "--window-size=1920,1080", "--force-device-scale-factor=1", url],
                   check=True, capture_output=True, timeout=120)
    subprocess.run(base + ["--print-to-pdf=" + str(pdf_path), url], check=True, capture_output=True, timeout=120)


if __name__ == "__main__":
    build()
    probs = confere()
    for p in probs:
        print("AJUSTE", p)
    print("elementos:", len(EL), "problemas de texto:", len(probs))
    emit_pptx(RAIZ / "slide-executivo.pptx")
    tmp = RAIZ / "scripts" / "slide-referencia.html"
    emit_html(tmp)
    if "--render" in sys.argv:
        render(tmp, RAIZ / "slide-executivo.png", RAIZ / "slide-executivo.pdf")
        print("render ok")
