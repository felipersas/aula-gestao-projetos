#!/usr/bin/env python3
"""Gera as figuras do relatorio e da analise (matplotlib) em ../img/ a partir de modelo_portfolio."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon

import modelo_portfolio as M

IMG = Path(__file__).resolve().parent.parent / "img"
IMG.mkdir(exist_ok=True)
for f in ("Arial.ttf", "Arial Bold.ttf", "Arial Italic.ttf"):
    fm.fontManager.addfont("/System/Library/Fonts/Supplemental/" + f)
plt.rcParams.update({"font.family": "Arial", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

PETROL = "#0F4C5C"
PETROL2 = "#2A7F91"
GRAFITE = "#2B2F33"
CINZA = "#8A949B"
CLARO = "#E8EEF1"
VERDE = "#2E8B57"
AMARELO = "#E0A800"
VERMELHO = "#C0392B"
COR_DEC = {"Prioridade": VERDE, "Posterior": AMARELO, "Adiado": VERMELHO}
COR_PROJ = {"P1": "#0F4C5C", "P2": "#2A7F91", "P4": "#6BA8B5", "P5": "#8C9A5B", "P6": "#C98B3A", "P7": "#B8B8B8"}
DPI = 200


def salvar(fig, nome):
    fig.savefig(IMG / nome, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def caixa(ax, x, y, w, h, txt, fc, ec=None, tc="white", fs=9, bold=False, lw=1.0, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.06", fc=fc, ec=ec or fc, lw=lw, ls=ls))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", color=tc, fontsize=fs,
            fontweight="bold" if bold else "normal", linespacing=1.25)


# ------------------------------------------------------------------ 1. estrutura
def fig_estrutura():
    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis("off")
    caixa(ax, 2.9, 5.4, 4.2, 0.7, "PORTFÓLIO DA METALTECH\nR$ 2,5 mi · 12 meses", GRAFITE, fs=9.5, bold=True)
    cols = [(0.0, 3.1, "Programa A\nExcelência Operacional\nR$ 1,5 mi", PETROL,
             [("P1 Automação da Linha 1", "R$ 900 mil · Prioridade"), ("P2 Manutenção Preditiva", "R$ 450 mil · Prioridade"), ("P6 Treinamento de Operadores", "R$ 150 mil · Prioridade")], [VERDE] * 3),
            (3.45, 3.1, "Programa B\nQualidade 4.0 (fase 1)\nR$ 0,6 mi", PETROL2,
             [("P4 Redução de Refugo", "R$ 250 mil · Prioridade"), ("P5 Controle de Qualidade", "R$ 350 mil · Prioridade")], [VERDE] * 2),
            (6.9, 3.1, "Programa C (não ativado)\nTransformação Digital\ncandidato a 2027", "#FFFFFF",
             [("P7 Monitoramento IoT", "R$ 600 mil · Posterior (G2, m6)"), ("P3 Novo ERP Industrial", "R$ 1,2 mi · Adiado")], [AMARELO, VERMELHO])]
    for x, w, tit, fc, projs, cores in cols:
        ativo = fc != "#FFFFFF"
        caixa(ax, x, 3.85, w, 1.0, tit, fc, ec=GRAFITE if not ativo else fc, tc="white" if ativo else GRAFITE, fs=9, bold=True,
              ls="-" if ativo else (0, (4, 3)))
        ax.plot([x + w / 2, x + w / 2], [4.85, 5.2], color=CINZA, lw=1)
        ax.plot([x + w / 2, 5.0], [5.2, 5.2], color=CINZA, lw=1)
        ax.plot([5.0, 5.0], [5.2, 5.4], color=CINZA, lw=1)
        for k, (pj, sub, cor) in enumerate(zip([p[0] for p in projs], [p[1] for p in projs], cores)):
            h = 0.68
            y = 3.0 - k * 0.82
            ax.add_patch(Rectangle((x, y), 0.09, h, fc=cor, ec=cor))
            ax.add_patch(Rectangle((x + 0.09, y), w - 0.09, h, fc=CLARO, ec=CLARO))
            ax.text(x + 0.2, y + h * 0.68, pj, va="center", fontsize=7.5, color=GRAFITE, fontweight="bold")
            ax.text(x + 0.2, y + h * 0.28, sub, va="center", fontsize=8, color=GRAFITE)
    caixa(ax, 0.0, 0.25, 6.55, 0.6, "Fora do ciclo: P8 Expansão da Capacidade · R$ 1,5 mi · Adiado", CLARO, ec=VERMELHO, tc=GRAFITE, fs=8.0, lw=1.2)
    caixa(ax, 6.9, 0.25, 3.1, 0.6, "Reserva: R$ 0,4 mi (16%)", "#FFFFFF", ec=PETROL, tc=PETROL, fs=8.2, bold=True, lw=1.2)
    for k, (t, c) in enumerate([("Prioridade", VERDE), ("Posterior", AMARELO), ("Adiado", VERMELHO)]):
        ax.add_patch(Rectangle((4.2 + k * 1.3, 1.7), 0.16, 0.16, fc=c, ec=c))
        ax.text(4.43 + k * 1.3, 1.78, t, va="center", fontsize=7.8, color=GRAFITE)
    salvar(fig, "fig01_estrutura_portfolio.png")


# ------------------------------------------------------------------ 2. priorizacao
def fig_priorizacao():
    ordem = M.RANK
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(6.8, 3.7), gridspec_kw={"width_ratios": [1.9, 1]})
    crit = [k for k, _, _ in M.CRIT]
    nomes = ["Alinham.\nestratégico\n(35%)", "Benefício/\ncusto\n(20%)", "Risco\n(15%)", "Prazo\n(10%)", "Sinergia\n(10%)", "Recursos\n(10%)"]
    import numpy as np
    data = np.array([[M.NOTAS[p][k] for k in crit] for p in ordem])
    ax.imshow(data, cmap=matplotlib.colors.LinearSegmentedColormap.from_list("x", ["#F4D6D2", "#FFF4CC", "#CFE8D8"]), vmin=1, vmax=5, aspect="auto")
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(j, i, str(data[i, j]), ha="center", va="center", fontsize=11, color=GRAFITE, fontweight="bold")
    ax.set_xticks(range(6)); ax.set_xticklabels(nomes, fontsize=8)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(ordem))); ax.set_yticklabels(["%s %s" % (p, M.PROJ[p]["nome"]) for p in ordem], fontsize=8.5)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    for k in range(1, 6):
        ax.axvline(k - 0.5, color="white", lw=2)
    for k in range(1, len(ordem)):
        ax.axhline(k - 0.5, color="white", lw=2)
    ax2.barh(range(len(ordem)), [M.SCORE[p] for p in ordem], color=[COR_DEC[M.DECISAO[p]] for p in ordem], height=0.62)
    for i, p in enumerate(ordem):
        ax2.text(M.SCORE[p] + 0.06, i, "%.2f".replace(".", ",") % M.SCORE[p] if False else ("%.2f" % M.SCORE[p]).replace(".", ","), va="center", fontsize=9, fontweight="bold", color=GRAFITE)
    ax2.set_ylim(len(ordem) - 0.5, -0.5); ax2.set_xlim(0, 5.4)
    ax2.set_yticks([]); ax2.set_xlabel("Pontuação ponderada (1 a 5)", fontsize=8.5)
    ax2.spines["left"].set_visible(False)
    ax2.axhline(4.5, color=GRAFITE, lw=1, ls="--")
    ax2.text(5.35, 4.42, "corte do portfólio", ha="right", va="bottom", fontsize=7.5, color=GRAFITE)
    fig.tight_layout(w_pad=1.0)
    salvar(fig, "fig02_matriz_priorizacao.png")


# ------------------------------------------------------------------ 3. roadmap
def fig_roadmap():
    linhas = [("P1 Automação da Linha 1", "P1"), ("P2 Manutenção Preditiva", "P2"), ("P4 Redução de Refugo", "P4"),
              ("P5 Controle de Qualidade", "P5"), ("P6 Treinamento de Operadores", "P6"), ("P7 Monitoramento IoT (condicional)", "P7"),
              ("Operação assistida e medição de benefícios", "BM")]
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.set_xlim(0, 12.6); ax.set_ylim(len(linhas) + 2.0, -1.7)
    for t in range(4):
        ax.add_patch(Rectangle((3 * t, -1.45), 3, 0.5, fc=PETROL if t % 2 == 0 else PETROL2, ec="white"))
        ax.text(3 * t + 1.5, -1.2, "T%d" % (t + 1), ha="center", va="center", color="white", fontweight="bold", fontsize=9.5)
    for m in range(12):
        ax.text(m + 0.5, -0.65, "m%d" % (m + 1), ha="center", va="center", fontsize=8, color=GRAFITE)
        ax.axvline(m, color="#D5DBDF", lw=0.6, zorder=0)
    ax.axvline(12, color="#D5DBDF", lw=0.6, zorder=0)
    ax.set_xlim(0, 12.6)
    for i, (rot, p) in enumerate(linhas):
        if p == "BM":
            ax.add_patch(Rectangle((6, i - 0.3), 6, 0.6, fc=CLARO, ec=PETROL, lw=1, hatch="///", alpha=0.9))
            ax.text(9, i, "hypercare e medição (m7-m12)", ha="center", va="center", fontsize=8, color=GRAFITE,
                    bbox=dict(fc="white", ec="none", pad=1.2))
            continue
        ini, fim = M.JANELA[p]
        if p == "P7":
            ax.add_patch(Rectangle((ini - 1, i - 0.3), fim - ini + 1, 0.6, fc="white", ec=AMARELO, lw=1.6, ls="--", hatch="//"))
            ax.text((ini - 1 + fim) / 2, i, "se G2 aprovar", ha="center", va="center", fontsize=8, color=GRAFITE, bbox=dict(fc="white", ec="none", pad=1.2))
        else:
            ax.add_patch(Rectangle((ini - 1, i - 0.3), fim - ini + 1, 0.6, fc=COR_PROJ[p], ec="none"))
            ax.text((ini - 1 + fim) / 2, i, "m%d-m%d" % (ini, fim), ha="center", va="center", fontsize=8.5, color="white", fontweight="bold")
    ax.set_yticks(range(len(linhas))); ax.set_yticklabels([l for l, _ in linhas], fontsize=8.5)
    ax.set_xticks([])
    for s in ("left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    yb = len(linhas) - 0.05
    marcos = [(1, "M1", "", PETROL), (3, "G1", "", GRAFITE), (4, "FAT", "", CINZA), (6, "G2", "", AMARELO), (9, "M9", "", PETROL), (12, "M12", "", PETROL)]
    off = {"M1": (0.0, "left"), "G1": (0, "center"), "FAT": (0, "center"), "G2": (0, "center"), "M9": (0, "center"), "M12": (0, "right")}
    for x, cod, txt, cor in marcos:
        ax.add_patch(Polygon([[x, yb - 0.28], [x + 0.2, yb], [x, yb + 0.28], [x - 0.2, yb]], fc=cor, ec=GRAFITE, lw=0.8, zorder=5))
        ax.plot([x, x], [-0.4, yb - 0.28], color=cor, lw=0.9, ls=":", zorder=1)
        ax.text(x, yb + 0.42, cod, ha="center", va="top", fontsize=8, fontweight="bold", color=GRAFITE)
    ax.text(0.0, yb + 1.0, "M1 linha de base · G1 pedido de equipamentos do P1 e P4 encerrado · FAT teste de aceitação do P1\nG2 decide o P7 · M9 e M12 balanços de benefícios", ha="left", va="top", fontsize=7.6, color=GRAFITE, linespacing=1.3)
    ax.add_patch(Polygon([[0, 0]], fc="none"))
    fig.tight_layout()
    salvar(fig, "fig03_roadmap_12_meses.png")


# ------------------------------------------------------------------ 4. desembolso
def fig_desembolso():
    fig, ax = plt.subplots(figsize=(6.8, 3.7))
    import numpy as np
    x = np.arange(1, 13)
    base = np.zeros(12)
    for p in M.PRIORIZADOS:
        v = np.array(M.DESEMB[p])
        ax.bar(x, v, bottom=base, color=COR_PROJ[p], label="%s" % p, width=0.7)
        base += v
    ax.set_xticks(x); ax.set_xticklabels(["m%d" % m for m in x], fontsize=8.5)
    ax.set_ylabel("Desembolso mensal (R$ mil)", fontsize=9); ax.set_ylim(0, 470)
    for xi, v in zip(x, base):
        if v > 0:
            ax.text(xi, v + 8, ("%.0f" % v), ha="center", fontsize=8, color=GRAFITE)
    ax2 = ax.twinx()
    acum = np.array(M.ACUM)
    ax2.plot(x, acum, color=GRAFITE, marker="o", ms=3.5, lw=1.4, label="Acumulado")
    ax2.axhline(M.INV_PRIOR, color=VERDE, ls="--", lw=1)
    ax2.axhline(M.ORCAMENTO_TETO, color=VERMELHO, ls="--", lw=1)
    ax2.text(12.45, M.INV_PRIOR - 90, "priorizados: R\\$ 2.100 mil", ha="right", fontsize=8, color=VERDE)
    ax2.text(12.45, M.ORCAMENTO_TETO + 25, "teto: R\\$ 2.500 mil (inclui a reserva de R\\$ 400 mil)", ha="right", fontsize=8, color=VERMELHO)
    ax2.set_ylim(0, 2850); ax2.set_ylabel("Acumulado (R$ mil)", fontsize=9)
    ax2.spines["right"].set_visible(True)
    for t in range(4):
        ax.text(3 * t + 2, 445, "T%d: R\\$ %s mil" % (t + 1, ("{:,.1f}".format(M.TRI[t]).replace(",", "X").replace(".", ",").replace("X", ".")) if M.TRI[t] % 1 else "{:,.0f}".format(M.TRI[t]).replace(",", ".")),
                ha="center", fontsize=8.5, fontweight="bold", color=PETROL)
        if t:
            ax.axvline(3 * t + 0.5, color="#D5DBDF", lw=0.8)
    h1, l1 = ax.get_legend_handles_labels()
    ax.legend(h1, l1, ncol=5, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.09), frameon=False)
    fig.tight_layout()
    salvar(fig, "fig04_curva_desembolso.png")


# ------------------------------------------------------------------ 5. recursos
def _heat(ax, mat, titulo, conflitos=()):
    import numpy as np
    recs = M.RECS
    data = np.array([mat[r] for r in recs], dtype=float)
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("c", ["#FFFFFF", "#CFE3E8", "#6BA8B5", "#0F4C5C"])
    ax.imshow(np.minimum(data, 100), cmap=cmap, vmin=0, vmax=100, aspect="auto")
    for i, r in enumerate(recs):
        for j in range(12):
            v = data[i, j]
            if v > 0:
                ax.text(j, i, "%d" % v, ha="center", va="center", fontsize=7.8,
                        color="white" if v >= 70 and v <= 100 else GRAFITE, fontweight="bold" if v >= 100 else "normal")
    for (r, m, v) in conflitos:
        i = recs.index(r)
        ax.add_patch(Rectangle((m - 1.5, i - 0.5), 1, 1, fc="#C0392B", ec="white", lw=1))
        ax.text(m - 1, i, "%d" % v, ha="center", va="center", fontsize=7.8, color="white", fontweight="bold")
    ax.set_xticks(range(12)); ax.set_xticklabels(["m%d" % k for k in range(1, 13)], fontsize=8)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(recs))); ax.set_yticklabels(recs, fontsize=9)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    for k in range(1, 12):
        ax.axvline(k - 0.5, color="white", lw=1)
    for k in range(1, len(recs)):
        ax.axhline(k - 0.5, color="white", lw=1)
    ax.set_title(titulo, fontsize=9.5, fontweight="bold", color=GRAFITE, loc="left", pad=22)


def fig_recursos():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 6.0))
    _heat(a1, M.MAT_ING, "A) Sem as decisões: %d células acima de 100%%" % len(M.CONF_ING), M.CONF_ING)
    _heat(a2, M.MAT, "B) Plano adotado: nenhuma célula acima de 100%% (GP no pico: %d%%)" % M.PICO["GP"])
    fig.tight_layout(h_pad=2.2)
    salvar(fig, "fig05_matriz_recursos.png")


# ------------------------------------------------------------------ 6. matriz de riscos
def fig_riscos():
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    probs = [0.9, 0.7, 0.5, 0.3, 0.1]
    imps = [0.05, 0.10, 0.20, 0.40, 0.80]
    for i, p in enumerate(probs):
        for j, im in enumerate(imps):
            sev = p * im
            cor = "#F1B5AE" if sev >= 0.18 else "#FBE3A0" if sev >= 0.06 else "#CFE8D8"
            ax.add_patch(Rectangle((j, i), 1, 1, fc=cor, ec="white", lw=2))
            ax.text(j + 0.96, i + 0.9, ("%.3f" % sev).replace(".", ",").rstrip("0").rstrip(",") if sev * 1000 % 10 else ("%.2f" % sev).replace(".", ","),
                    ha="right", va="top", fontsize=7, color="#6B7479")
            ids = [r["id"] for r in M.RISCOS_DADOS if abs(r["prob"] - p) < 1e-9 and abs(r["imp"] - im) < 1e-9]
            if ids:
                linhas = [" ".join(ids[k:k + 3]) for k in range(0, len(ids), 3)]
                ax.text(j + 0.5, i + 0.52, "\n".join(linhas), ha="center", va="center", fontsize=9, fontweight="bold", color=GRAFITE, linespacing=1.3)
    ax.set_xlim(0, 5); ax.set_ylim(0, 5)
    ax.set_xticks([k + 0.5 for k in range(5)]); ax.set_xticklabels(["%s\n%s" % (("%.2f" % v).replace(".", ","), M.IMP[v]) for v in imps], fontsize=8.5)
    ax.set_yticks([k + 0.5 for k in range(5)]); ax.set_yticklabels(["%s\n%s" % (("%.1f" % v).replace(".", ","), M.PROB[v]) for v in probs], fontsize=8.5)
    ax.set_xlabel("Impacto (escala 0,05 a 0,80)", fontsize=9); ax.set_ylabel("Probabilidade", fontsize=9)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.invert_yaxis(); ax.set_ylim(5, 0)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc="#F1B5AE", label="Severidade alta (≥ 0,18)"), Patch(fc="#FBE3A0", label="Média (0,06 a 0,17)"), Patch(fc="#CFE8D8", label="Baixa (< 0,06)")],
              loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, fontsize=8.5, frameon=False)
    fig.tight_layout()
    salvar(fig, "fig06_matriz_riscos.png")


# ------------------------------------------------------------------ 7. metas x realizacao
def fig_metas():
    import numpy as np
    metas = [("Produtividade\n(meta +15%)\nP1: +12 p.p.", M.BEN_QUANT["P1"][0], M.METAS["Produtividade"]),
             ("Paradas\n(meta -20%)\nP2: -20 p.p.", M.BEN_QUANT["P2"][0], M.METAS["Paradas"]),
             ("Retrabalho\n(meta -30%)\nP5: -30 p.p.", M.BEN_QUANT["P5"][0], M.METAS["Retrabalho"])]
    fig, ax = plt.subplots(figsize=(6.8, 3.7))
    w = 0.19
    cores = [PETROL, PETROL2, "#6BA8B5", "#B7D3DA"]
    for k, r in enumerate(M.REAL):
        vals = [100 * b * r / m for _, b, m in metas]
        pos = np.arange(3) + (k - 1.5) * w
        bars = ax.bar(pos, vals, w * 0.92, color=cores[k], label="benefício realizado em %d%%" % round(r * 100))
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 1.5, "%d%%" % round(v), ha="center", fontsize=8, color=GRAFITE)
    ax.axhline(100, color=VERMELHO, ls="--", lw=1.2)
    ax.text(2.55, 101.5, "meta = 100%", color=VERMELHO, fontsize=8.5, ha="right")
    ax.set_xticks(range(3)); ax.set_xticklabels([m[0] for m in metas], fontsize=8.5)
    ax.set_ylabel("% da meta coberta pelo benefício quantificado", fontsize=8.5); ax.set_ylim(0, 118)
    ax.legend(fontsize=8, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.27), frameon=False)
    fig.tight_layout()
    salvar(fig, "fig07_metas_vs_beneficio.png")


# ------------------------------------------------------------------ 8. partes interessadas
def quadrante(poder, interesse):
    if poder >= 4 and interesse >= 4:
        return "Gerenciar com atenção"
    if poder >= 4:
        return "Manter satisfeito"
    if interesse >= 4:
        return "Manter informado"
    return "Monitorar"


def fig_partes():
    import conteudo as C
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.set_xlim(0.5, 5.5); ax.set_ylim(0.5, 5.5)
    ax.add_patch(Rectangle((3.5, 3.5), 2.0, 2.0, fc="#DCE9ED", ec="none"))
    ax.add_patch(Rectangle((0.5, 3.5), 3.0, 2.0, fc="#F1F4F5", ec="none"))
    ax.add_patch(Rectangle((3.5, 0.5), 2.0, 3.0, fc="#F1F4F5", ec="none"))
    ax.axhline(3.5, color=CINZA, lw=0.8); ax.axvline(3.5, color=CINZA, lw=0.8)
    for x, y, t, ha, va in [(5.45, 5.42, "Gerenciar com atenção", "right", "top"), (0.55, 5.42, "Manter satisfeito", "left", "top"),
                            (5.45, 0.58, "Manter informado", "right", "bottom"), (0.55, 0.58, "Monitorar", "left", "bottom")]:
        ax.text(x, y, t, ha=ha, va=va, fontsize=9, fontweight="bold", color=PETROL)
    grupos = {}
    for pid, nome, poder, interesse, quad, *_ in C.PARTES:
        assert quad == quadrante(poder, interesse), (pid, quad, quadrante(poder, interesse))
        grupos.setdefault((interesse, poder), []).append(pid)
    for (x, y), ids in grupos.items():
        n = len(ids)
        for k, pid in enumerate(ids):
            xx = x + (k - (n - 1) / 2) * 0.3
            ax.scatter([xx], [y], s=330, color=PETROL, edgecolor="white", zorder=3)
            ax.text(xx, y, pid[1:], ha="center", va="center", color="white", fontsize=8, fontweight="bold", zorder=4)
    ax.set_xlabel("Interesse (1 a 5)", fontsize=9); ax.set_ylabel("Poder (1 a 5)", fontsize=9)
    ax.set_xticks(range(1, 6)); ax.set_yticks(range(1, 6))
    for s_ in ax.spines.values():
        s_.set_visible(False)
    ax.tick_params(length=0)
    fig.tight_layout()
    salvar(fig, "fig08_partes_interessadas.png")


if __name__ == "__main__":
    fig_partes()
    fig_estrutura(); fig_priorizacao(); fig_roadmap(); fig_desembolso(); fig_recursos(); fig_riscos(); fig_metas()
    print("ok", sorted(p.name for p in IMG.glob("*.png")))
