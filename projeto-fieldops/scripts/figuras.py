#!/usr/bin/env python3
"""Figuras novas do relatorio (matplotlib) e copia das figuras existentes dos artefatos."""
import shutil
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

import dados as D

RAIZ = Path(__file__).resolve().parent.parent
IMG = RAIZ / "img"
ENT = D.ENT
C1, C2, C3, CG = "#0F4C5C", "#007B6E", "#C98B3A", "#6B7780"
plt.rcParams["font.family"] = "DejaVu Sans"

COPIAS = {
    "eap_original.png": "aula-03-escopo/eap-fieldops.png",
    "ishikawa.png": "aula-05-custos-qualidade/01-ishikawa.png",
    "fluxograma_qualidade.png": "aula-05-custos-qualidade/02-fluxograma.png",
    "folha_verificacao.png": "aula-05-custos-qualidade/03-folha-verificacao.png",
    "pareto_defeitos.png": "aula-05-custos-qualidade/04a-pareto-defeitos.png",
    "pareto_nc.png": "aula-05-custos-qualidade/04b-pareto-nao-conformidades.png",
    "histograma.png": "aula-05-custos-qualidade/05-histograma.png",
    "grafico_p.png": "aula-05-custos-qualidade/06a-grafico-p-sprints.png",
    "grafico_imr.png": "aula-05-custos-qualidade/06b-grafico-imr-commits.png",
    "dispersao.png": "aula-05-custos-qualidade/07-dispersao.png",
    "curva_s.png": "aula-05-custos-qualidade/curva-s-orcamento-fieldops.png",
    "custo_por_entrega.png": "aula-05-custos-qualidade/orcamento-por-entrega-fieldops.png",
    "organograma.png": "aula-06-rh-comunicacoes/organograma-fieldops.png",
    "matriz_calor.png": "aula-07-riscos/matriz-calor.png",
    "poder_interesse.png": "aula-08-aquisicoes-partes-interessadas/matriz-poder-interesse-fieldops.png",
    "gantt_original.png": "aula-04-tempo/gantt-fieldops.png",
}


def copia():
    for dst, src in COPIAS.items():
        shutil.copy(ENT / src, IMG / dst)


def caixa(ax, x, y, w, h, txt, fc, tc="white", fs=8, bold=False, ec=None, lw=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.06", fc=fc, ec=ec or fc, lw=lw))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold" if bold else "normal", linespacing=1.25)


def seta(ax, p, q, cor=CG, estilo="-|>", lw=1.2, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=estilo, mutation_scale=9, color=cor, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0))


# ------------------------------------------------------------------ arquitetura
def fig_arquitetura():
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.3); ax.axis("off")
    caixa(ax, 0.0, 3.5, 3.1, 1.5, "Aplicativo mobile (Android)\nExpo + React Native + TS\ncâmera · QR Code · GPS", C2, fs=6.9, bold=True)
    caixa(ax, 0.0, 1.4, 3.1, 1.5, "Persistência local\nSQLite (operacional)\nOutbox de pendências", "#E3F1EF", tc=C1, fs=6.9, ec=C2)
    caixa(ax, 3.75, 2.0, 2.5, 2.6, "API REST central\nJava + Spring Boot\nJWT · perfis · OpenAPI\nFlyway · auditoria\nsincronização\nidempotente", C1, fs=6.9, bold=True)
    caixa(ax, 6.9, 3.5, 3.1, 1.5, "Interface administrativa\nNext.js 16 (App Router)\nReact 19 + TypeScript", C2, fs=6.9, bold=True)
    caixa(ax, 6.9, 1.4, 3.1, 1.5, "Dados centrais\nPostgreSQL\nArmazenamento S3 (evidências)", "#E3F1EF", tc=C1, fs=6.9, ec=C2)
    seta(ax, (1.55, 3.5), (1.55, 2.9), cor=C2, estilo="<|-|>")
    seta(ax, (3.1, 4.25), (3.75, 3.9), estilo="<|-|>")
    seta(ax, (3.1, 2.15), (3.75, 2.7), estilo="<|-|>", ls="--")
    seta(ax, (6.25, 3.9), (6.9, 4.25), estilo="<|-|>")
    seta(ax, (6.25, 2.7), (6.9, 2.15), estilo="<|-|>")
    ax.text(3.45, 4.75, "HTTPS/JSON", fontsize=6.2, color=CG, ha="center", va="bottom")
    ax.text(3.45, 1.9, "push / pull\n(lote, cursor)", fontsize=6.2, color=CG, ha="center", va="top")
    ax.text(0.0, 0.55, "Contrato OpenAPI compartilhado (RJ01): web e app consomem o mesmo contrato, publicado em M1.", fontsize=6.8, color=C1, ha="left", va="center")
    ax.text(0.0, 0.15, "Repositórios (org FieldOps-Project): docs, backend, frontend e app; CI por repositório; PR com revisão.", fontsize=6.8, color=CG, ha="left", va="center")
    fig.savefig(IMG / "arquitetura.png", dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ EAP resumida (paisagem)
def fig_eap():
    import textwrap
    nomes = D.eap_nomes()
    fig, ax = plt.subplots(figsize=(9.7, 6.0))
    ax.set_xlim(0, 7.0); ax.set_ylim(0, 9.2); ax.axis("off")
    caixa(ax, 1.9, 8.5, 3.2, 0.62, "FieldOps — Plataforma de Inspeção em Campo (MVP)\n7 entregas · 36 pacotes de trabalho", C1, fs=7.2, bold=True)
    ax.plot([3.5, 3.5], [8.5, 8.28], color=C1, lw=1.2)
    ax.plot([0.5, 6.5], [8.28, 8.28], color=C1, lw=1.2)
    for i, (k, nome) in enumerate(D.ENTREGAS.items()):
        x = i + 0.04
        ax.plot([i + 0.5, i + 0.5], [8.28, 8.08], color=C1, lw=1.2)
        caixa(ax, x, 7.2, 0.92, 0.86, k + "\n" + "\n".join(textwrap.wrap(nome, 17)), C2, fs=6.2, bold=True)
        pk = [c for c in nomes if c.startswith(k + ".")]
        for j, cod in enumerate(pk):
            y = 6.95 - j * 0.9 - 0.78
            caixa(ax, x + 0.03, y, 0.86, 0.78, cod + "\n" + "\n".join(textwrap.wrap(D.SHORT[cod], 18)), "white", tc=C1, fs=5.9, ec=C2, lw=1.0)
    ax.text(0, 0.0, "Nível 0: projeto; nível 1: entrega (verde); nível 2: pacote de trabalho (contorno). Nomes completos no dicionário da EAP (Apêndice D).",
            fontsize=6.3, color=CG, ha="left", va="bottom")
    fig.savefig(IMG / "eap_resumo.png", dpi=250, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ Gantt por pacote
def d2(s):
    dd, mm = s.split("/")
    return date(2026, int(mm), int(dd))


def fig_gantt(real_on=True, arquivo='gantt_pacotes.png'):
    ativ = [a for a in D.cronograma() if not a["marco"]]
    real = D.realizado_atividades()
    pk = {}
    for a in ativ:
        pk.setdefault(a["wbs"], []).append(a)
    cods = sorted(pk, key=lambda c: tuple(int(x) for x in c.split(".")))
    hoje = date(2026, 11, 18)
    t0 = date(2026, 8, 10)
    fig, ax = plt.subplots(figsize=(6.6, 8.6))
    n = len(cods)
    y = 0
    rot, ys = [], []
    cores = {"1": "#6B7790", "2": "#8E6BBF", "3": "#2D6DB5", "4": "#1E9C8C", "5": "#E08E1F", "6": "#C24B57", "7": "#5C9C3E"}
    pos = {}
    for cod in cods:
        g = cod.split(".")[0]
        ini = min(d2(a["ini"]) for a in pk[cod]); fim = max(d2(a["fim"]) for a in pk[cod])
        esf = sum(a["esf"] for a in pk[cod])
        pr = sum(a["esf"] * real[a["id"]] for a in pk[cod]) / esf / 100
        x0, x1 = (ini - t0).days, (fim - t0).days + 1
        yy = n - len(rot)
        if real_on:
            ax.barh(yy, x1 - x0, left=x0, height=0.62, color=cores[g], alpha=0.28, edgecolor=cores[g], lw=0.6)
            ax.barh(yy, (x1 - x0) * pr, left=x0, height=0.62, color=cores[g], edgecolor=cores[g], lw=0.6)
            ax.text(x1 + 1.2, yy, f"{pr * 100:.0f}%", va="center", fontsize=6.2, color="#333")
        else:
            ax.barh(yy, x1 - x0, left=x0, height=0.62, color=cores[g], edgecolor=cores[g], lw=0.6)
        rot.append(f"{cod} {D.SHORT[cod]}"); ys.append(yy)
    ax.set_yticks(ys); ax.set_yticklabels(rot, fontsize=6.8)
    for l, g in zip(ax.get_yticklabels(), cods):
        l.set_color(cores[g.split(".")[0]])
    marcos = [("M1", "21/08"), ("M2", "04/09"), ("M3", "18/09"), ("M4", "02/10"), ("M5", "16/10"), ("M6", "30/10"), ("M7", "13/11"), ("M8", "27/11")]
    for nome, dt in marcos:
        x = (d2(dt) - t0).days + 0.5
        ax.axvline(x, color="#9AA5AB", lw=0.6, ls=":")
        ax.plot([x], [n + 1.1], marker="D", color="#0B1530", ms=4.5, clip_on=False)
        ax.text(x, n + 1.7, nome, ha="center", fontsize=6.6, fontweight="bold", color="#0B1530")
    if real_on:
        xh = (hoje - t0).days + 0.5
        ax.axvline(xh, color="#D32F2F", lw=1.4)
        ax.text(xh - 1, 0.1, "hoje 18/11", color="#D32F2F", fontsize=6.6, ha="right", va="bottom", fontweight="bold")
    ax.set_xlim(0, (date(2026, 11, 28) - t0).days)
    ticks = [date(2026, m, 1) for m in (9, 10, 11)] + [date(2026, 8, 10)]
    ax.set_xticks([(t - t0).days for t in sorted(ticks)])
    ax.set_xticklabels([t.strftime("%d/%m") for t in sorted(ticks)], fontsize=6.8)
    ax.set_ylim(0.3, n + 2.2)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.savefig(IMG / arquivo, dpi=230, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ burnup de issues
def fig_burnup():
    sp = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
    tot = [17, 17, 10, 14, 8, 13, 14, 10]
    ok = [15, 17, 7, 10, 4, 2, 2, 0]
    ct = [sum(tot[:i + 1]) for i in range(8)]
    co = [sum(ok[:i + 1]) for i in range(8)]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.2), gridspec_kw=dict(width_ratios=[1.25, 1]))
    x = range(8)
    a.plot(x, ct, "-o", color=C1, lw=1.8, ms=4, label="Planejado: issues acumuladas dos milestones (total 103)")
    a.plot(x, co, "-o", color="#C24B57", lw=1.8, ms=4, label="Concluídas acumuladas (57 em 18/11)")
    a.fill_between(x, co, ct, color="#C24B57", alpha=0.10)
    a.annotate("46 issues\nabertas", (7, 80), fontsize=7, color="#C24B57", ha="center")
    a.set_xticks(list(x)); a.set_xticklabels(sp, fontsize=7.5)
    a.set_ylabel("issues acumuladas", fontsize=7.5); a.tick_params(axis="y", labelsize=7.5)
    a.set_title("Burnup por sprint (milestones do GitHub)", fontsize=8.5, loc="left", fontweight="bold")
    a.legend(fontsize=6.4, loc="upper left", frameon=False)
    a.spines[["top", "right"]].set_visible(False)
    pct = [100 * o / t for o, t in zip(ok, tot)]
    cor = ["#2E8B57" if p >= 90 else "#E0A800" if p >= 70 else "#C24B57" for p in pct]
    b.bar(list(x), pct, color=cor, width=0.62)
    for i, p in enumerate(pct):
        b.text(i, p + 2, f"{ok[i]}/{tot[i]}", ha="center", fontsize=6.6)
    b.axhline(70, color=CG, lw=0.8, ls="--"); b.axhline(90, color=CG, lw=0.8, ls=":")
    b.text(7.45, 71, "70%", fontsize=6.4, color=CG, ha="right", va="bottom"); b.text(7.45, 91, "90%", fontsize=6.4, color=CG, ha="right", va="bottom")
    b.set_ylim(0, 118); b.set_xticks(list(x)); b.set_xticklabels(sp, fontsize=7.5); b.tick_params(axis="y", labelsize=7.5)
    b.set_title("Conclusão por sprint (%)", fontsize=8.5, loc="left", fontweight="bold")
    b.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(IMG / "burnup_sprints.png", dpi=230, facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ fluxo de mudanca
def fig_fluxo():
    fig, ax = plt.subplots(figsize=(7.4, 4.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis("off")
    passos = [
        ("1. Solicitação", "qualquer integrante abre a issue\n\"mudanca-de-escopo\" com o\nformulário de solicitação"),
        ("2. Triagem", "o gerente (FM) registra no log e\nclassifica em até 2 dias úteis\n(classe 1, 2 ou 3)"),
        ("3. Análise de impacto", "R do pacote (e JV, se houver\ncontrato): escopo/EAP, prazo,\ncusto, riscos e qualidade"),
        ("4. Decisão", "conforme a classe:\nFM; FM + PI-02;\nPI-02 com PI-01 e PI-03"),
        ("5. Comunicação", "COM-10 (e COM-09 se houver\nmudança de contrato)\nem até 24 h"),
        ("6. Atualização", "linhas de base (EAP, cronograma,\norçamento, riscos) em nova\nversão e registro no log"),
    ]
    xs = [0.1, 3.5, 6.9]
    ys = [3.55, 0.85]
    pos = [(xs[0], ys[0]), (xs[1], ys[0]), (xs[2], ys[0]), (xs[2], ys[1]), (xs[1], ys[1]), (xs[0], ys[1])]
    for (t, d), (x, y) in zip(passos, pos):
        caixa(ax, x, y + 1.15, 3.0, 0.5, t, C1, fs=8, bold=True)
        caixa(ax, x, y, 3.0, 1.15, d, "#EAF2F3", tc="#1B2B33", fs=7.2, ec=C1)
    seta(ax, (3.1, ys[0] + 1.0), (3.5, ys[0] + 1.0), cor=C1)
    seta(ax, (6.5, ys[0] + 1.0), (6.9, ys[0] + 1.0), cor=C1)
    seta(ax, (8.4, ys[0]), (8.4, ys[1] + 1.65), cor=C1)
    seta(ax, (6.9, ys[1] + 1.0), (6.5, ys[1] + 1.0), cor=C1)
    seta(ax, (3.5, ys[1] + 1.0), (3.1, ys[1] + 1.0), cor=C1)
    caixa(ax, 0.1, 5.5, 9.8, 0.55, "Rejeitada ou adiada: o motivo fica registrado na issue e volta ao solicitante; nada é implementado antes da decisão.", "#FBEFE0", tc="#6B4A12", fs=7, ec=C3)
    ax.text(0.1, 0.25, "Verificação: na retrospectiva da sprint, o gerente confere se a mudança foi aplicada e se os indicadores de escopo refletem a nova linha de base.", fontsize=6.6, color=CG)
    fig.savefig(IMG / "fluxo_mudanca.png", dpi=230, bbox_inches="tight", facecolor="white")
    plt.close(fig)



# ------------------------------------------------------------------ Pareto de defeitos (versao vertical, legivel em retrato)
def fig_pareto():
    cab, rows = D.md_tabelas("qual", "*Figura 4a. Pareto dos defeitos")
    cat = [D.sem_md(r[0]) for r in rows]; q = [int(r[2]) for r in rows]; ac = [float(r[4].replace("%", "").replace(",", ".")) for r in rows]
    pw = [int(r[5]) for r in rows]
    ordem = sorted(range(len(rows)), key=lambda i: -pw[i])
    acw, tot = [], sum(pw)
    run = 0
    for i in ordem:
        run += pw[i]; acw.append(100 * run / tot)
    import textwrap
    curto = lambda t: "\n".join(textwrap.wrap(t.replace("Persistência, offline e sincronização", "Offline e sincronização").replace("Regras de negócio e fluxo de inspeção", "Regras de negócio e fluxo").replace("Sessão, autenticação e segurança", "Sessão e segurança").replace("Build, tipos, dependências e testes", "Build, tipos e testes").replace("Contrato, erros e migrações da API", "Contrato e migrações da API").replace("Acessibilidade e estados de interface", "Acessibilidade e estados").replace("Layout e acabamento visual", "Layout e acabamento"), 14))
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 6.0))
    for ax, idx, vals, cum, tit, yl in ((axs[0], list(range(len(rows))), q, ac, "(a) Defeitos corrigidos por categoria: frequência (n = 50 commits fix)", "commits fix"),
                                         (axs[1], ordem, [pw[i] for i in ordem], acw, "(b) Os mesmos defeitos ponderados por severidade presumida (pesos 1, 3, 5 e 10)", "peso × quantidade")):
        xs = range(len(idx))
        ax.bar(xs, vals, color="#1F4E79", width=0.65)
        for x, v in zip(xs, vals):
            ax.text(x, v + max(vals) * 0.02, str(v), ha="center", fontsize=7.5, fontweight="bold")
        ax.set_xticks(list(xs)); ax.set_xticklabels([curto(cat[i]) for i in idx], fontsize=7)
        ax.set_ylabel(yl, fontsize=7.5); ax.tick_params(axis="y", labelsize=7)
        ax.set_title(tit, fontsize=8, loc="left", fontweight="bold")
        ax2 = ax.twinx(); ax2.plot(list(xs), cum, "-o", color="#C0392B", ms=3.5, lw=1.5)
        for x, v in zip(xs, cum):
            ax2.text(x, v + 4, f"{v:.0f}%", ha="center", fontsize=6.8, color="#C0392B")
        ax2.axhline(80, color="#8A94A0", lw=0.8, ls="--"); ax2.set_ylim(0, 118); ax2.tick_params(axis="y", labelsize=7)
        ax2.set_ylabel("% acumulado", fontsize=7.5); ax.set_ylim(0, max(vals) * 1.22)
        ax.spines[["top"]].set_visible(False); ax2.spines[["top"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(IMG / "pareto_defeitos_ret.png", dpi=230, facecolor="white")
    plt.close(fig)


def fig_curva_s():
    rows = [r for r in D.curva_s() if r[0].startswith("S")]
    lb = [D.num(r[7]) for r in rows]; ac = [D.num(r[8]) for r in rows]
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.6, 3.1), gridspec_kw=dict(width_ratios=[1.5, 1]))
    x = range(8)
    a.bar(x, lb, color="#9DB7D5", width=0.6, label="linha de base da sprint")
    a.plot(x, ac, "-o", color=C1, lw=1.8, ms=4, label="linha de base acumulada")
    a.axhline(D.num("R$ 52.486,31"), color="#2D6DB5", lw=0.9, ls=":"); a.text(-0.4, 49200, "BAC R$ 52.486,31", fontsize=6.6, color="#2D6DB5")
    a.axhline(D.num("R$ 54.872,05"), color="#C0392B", lw=0.9, ls="-."); a.text(-0.4, 56000, "Orçamento total R$ 54.872,05", fontsize=6.6, color="#C0392B")
    for i, v in enumerate(ac):
        a.text(i, v + 1500, f"{v / 1000:.1f} mil".replace(".", ","), ha="center", fontsize=6.2, color=C1)
    a.set_xticks(list(x)); a.set_xticklabels([f"S{i + 1}" for i in x], fontsize=7.5)
    a.set_ylim(0, 63000); a.tick_params(axis="y", labelsize=7); a.set_ylabel("R$", fontsize=7.5)
    a.set_title("Curva S por sprint (valor esperado PERT)", fontsize=8, loc="left", fontweight="bold")
    a.legend(fontsize=6.4, loc="center left", frameon=False, bbox_to_anchor=(0.0, 0.62))
    a.spines[["top", "right"]].set_visible(False)
    evm = [("PV", 42779.78, "#9AA3B5"), ("EV", 22514.18, "#2D6DB5"), ("AC (hip.)", 38598.42, "#C24B57")]
    b.bar([e[0] for e in evm], [e[1] for e in evm], color=[e[2] for e in evm], width=0.6)
    for i, e in enumerate(evm):
        b.text(i, e[1] + 800, "R$ " + f"{e[1]:,.0f}".replace(",", "."), ha="center", fontsize=6.8, fontweight="bold")
    b.set_ylim(0, 50000); b.tick_params(labelsize=7)
    b.set_title("EVM da mão de obra em 18/11\nSPI 0,53 · CPI 0,58", fontsize=8, loc="left", fontweight="bold")
    b.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(IMG / "curva_s_ret.png", dpi=230, facecolor="white")
    plt.close(fig)


def fig_pi():
    ps = D.partes()
    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 10.8)
    cores = {"Gerenciar com atenção": "#F9D9D6", "Manter satisfeito": "#FBEFC9", "Manter informado": "#D8E8F5", "Monitorar": "#E6E8EA"}
    ax.add_patch(Rectangle((0, 5.5), 5.5, 5.3, fc=cores["Manter satisfeito"], ec="none"))
    ax.add_patch(Rectangle((5.5, 5.5), 5.0, 5.3, fc=cores["Gerenciar com atenção"], ec="none"))
    ax.add_patch(Rectangle((0, 0), 5.5, 5.5, fc=cores["Monitorar"], ec="none"))
    ax.add_patch(Rectangle((5.5, 0), 5.0, 5.5, fc=cores["Manter informado"], ec="none"))
    ax.axhline(5.5, color="#555", lw=0.8); ax.axvline(5.5, color="#555", lw=0.8)
    for txt, x, y in (("MANTER SATISFEITO", 0.15, 10.35), ("GERENCIAR COM ATENÇÃO", 10.4, 5.75), ("MONITORAR", 0.15, 0.2), ("MANTER INFORMADO", 10.4, 0.2)):
        ax.text(x, y, txt, fontsize=7.2, fontweight="bold", color="#444", ha="left" if x < 5 else "right", va="center")
    off = {"PI-02": (-0.2, 0.0, "right"), "PI-05": (-0.1, 0.38, "right"), "PI-06": (0.15, 0.3, "left"), "PI-03": (0.15, 0.3, "left"), "PI-04": (-0.15, 0.3, "right"),
           "PI-01": (-0.15, 0.3, "right"), "PI-13": (0.15, -0.4, "left"), "PI-12": (0.15, 0.3, "left"), "PI-11": (0.15, 0.3, "left"), "PI-07": (0.15, 0.3, "left"),
           "PI-08": (0.15, 0.3, "left"), "PI-09": (0.15, -0.4, "left"), "PI-10": (0.15, 0.3, "left")}
    curto = {"PI-01": "Coordenação", "PI-02": "Prof. Glauco", "PI-03": "Comitê docente", "PI-04": "Prof. Deivison", "PI-05": "Gerente (FM)", "PI-06": "Equipe", "PI-07": "Técnicos", "PI-08": "Supervisores",
             "PI-09": "Administradores", "PI-10": "Cliente", "PI-11": "Operadora", "PI-12": "Provedores", "PI-13": "UniSENAI infra"}
    for p in ps:
        x, y = p["inter"], p["poder"]
        ax.plot([x], [y], "o", color="#0F4C5C", ms=5)
        dx, dy, ha = off[p["id"]]
        ax.text(x + dx, y + dy, f"{p['id']} {curto[p['id']]}", fontsize=6.8, ha=ha, va="center", color="#111")
    ax.set_xlabel("Interesse no projeto (nota de 1 a 10)", fontsize=7.5); ax.set_ylabel("Poder sobre o projeto (nota de 1 a 10)", fontsize=7.5)
    ax.set_xticks(range(0, 11)); ax.set_yticks(range(0, 11)); ax.tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(IMG / "poder_interesse_ret.png", dpi=230, facecolor="white")
    plt.close(fig)


def fig_org():
    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    ax.set_xlim(0, 10); ax.set_ylim(-0.8, 8.2); ax.axis("off")
    def bx(x, y, w, h, t, fc, tc="#111", ec=C1, ls="-", fs=6.6, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08", fc=fc, ec=ec, lw=1.0, ls=ls))
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold" if bold else "normal", linespacing=1.25)
    bx(0.2, 7.0, 5.0, 1.0, "Comitê executivo e patrocinador\nPI-01 Coordenação do curso\nPI-03 Professores de Expo, Spring Boot e Web", "#E8EEF4", bold=False)
    bx(6.0, 7.0, 3.8, 1.0, "Avaliador de Gestão de Projetos\nPI-04 Prof. Deivison Takatu", "white", ls="--", ec=CG)
    bx(0.2, 5.6, 5.0, 1.0, "Orientador e product owner acadêmico\nPI-02 Prof. Glauco Todesco\nregras de negócio e critérios de aceitação", "#E8EEF4")
    bx(6.0, 5.6, 3.8, 1.0, "Cliente e usuários finais\nPI-10, PI-11 (via PO) e PI-07 a PI-09\n(personas representadas pelo PO)", "white", ls="--", ec=CG)
    bx(0.2, 4.2, 5.0, 1.0, "Gerente do projeto: FM Felipe Marques\n(também desenvolvedor mobile)", "#FBEFD2", ec=C3, bold=True)
    bx(6.0, 4.2, 3.8, 1.0, "Provedores e infraestrutura\nPI-12 Expo/EAS, GitHub, hospedagem, S3\nPI-13 UniSENAI (calendário, laboratório)", "white", ls="--", ec=CG)
    ax.plot([2.7, 2.7], [7.0, 6.6], color=C1, lw=1.2); ax.plot([2.7, 2.7], [5.6, 5.2], color=C1, lw=1.2)
    for yy in (7.5, 6.1, 4.7):
        ax.plot([5.2, 6.0], [yy, yy], color=CG, lw=1.0, ls=":")
    ax.plot([2.7, 2.7], [4.2, 3.7], color=C1, lw=1.2); ax.plot([1.25, 8.75], [3.7, 3.7], color=C1, lw=1.2)
    cols = [("Frente Backend", "API e banco de dados", ["JV  líder técnico da API", "GR  cadastros e testes", "PD  planejamento e revisão"]),
            ("Frente Web", "painel em Next.js", ["AF  dev web"]),
            ("Frente Mobile", "app Expo e offline", ["FM  dev mobile", "PD  offline e sincronização"]),
            ("Qualidade e docs", "testes, CI e demo", ["GR  testes", "PD  integração, CI, docs", "AF  acessibilidade", "JV  dados de demonstração"])]
    for i, (t, sub, pess) in enumerate(cols):
        x = 0.05 + i * 2.5
        ax.plot([x + 1.2, x + 1.2], [3.7, 3.4], color=C1, lw=1.2)
        bx(x, 2.45, 2.4, 0.95, t + "\n" + sub, C2, tc="white", ec=C2, fs=6.2, bold=True)
        for j, p in enumerate(pess):
            bx(x, 1.9 - j * 0.5, 2.4, 0.42, p, "white", fs=6.0)
    ax.text(0.05, -0.75, "Linha contínua: relação hierárquica e de prestação de contas. Linha pontilhada: partes sem comando sobre a equipe.\nPapéis dos integrantes inferidos dos repositórios (proposta a confirmar com o grupo).", fontsize=6.0, color=CG, va="bottom")
    fig.savefig(IMG / "organograma_ret.png", dpi=230, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    copia()
    fig_arquitetura(); fig_eap(); fig_gantt(); fig_gantt(False, 'gantt_baseline.png'); fig_burnup(); fig_fluxo(); fig_pareto(); fig_curva_s(); fig_pi(); fig_org()
    print("ok", sorted(p.name for p in IMG.iterdir()))
