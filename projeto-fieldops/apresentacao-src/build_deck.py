#!/usr/bin/env python3
"""
Constroi apresentacao-final.pptx (nativo), a replica HTML e o PDF do FieldOps.
Uso: build_deck.py [--render] [--only N]
"""
import subprocess
import sys
from datetime import date
from pathlib import Path

import deck_lib as L
from deck_lib import *  # noqa
from fatos_apresentacao import carrega
from roteiro_dados import ROT, NOMES

RAIZ = Path(__file__).resolve().parent.parent
F = carrega()
TOTAL = 16


def br(v, dec=2):
    s = f"{v:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def rs(v, dec=2):
    return "R$ " + br(v, dec)


def card(s, x, y, w, h, title, body, accent=TEAL, bsize=14, fill=CLARO2, tcolor=None, tsize=14):
    s.box(x, y, w, h, None, fill=fill)
    s.box(x, y, 0.08, h, None, fill=accent)
    s.text(x + 0.3, y + 0.08, w - 0.42, 0.3, [title], size=tsize, bold=True, color=tcolor or accent)
    s.text(x + 0.3, y + 0.42, w - 0.42, h - 0.5, body, size=bsize)


def kpi(s, x, y, w, h, big, label, fill=PETROL, color=BRANCO, bigsize=26, lsize=14):
    s.box(x, y, w, h, [{"runs": [(big, {"size": bigsize, "bold": True})], "align": "c"},
                       {"runs": [(label, {"size": lsize})], "align": "c"}], fill=fill, color=color, valign="m")


def new(n, title, **kw):
    s = Slide(title, n=n, **kw)
    r = ROT[n]
    mm, ss = divmod(r["seg"], 60)
    quem = " + ".join(dict.fromkeys(q for q, _ in r["fala"]))
    cab = f"[Tempo ≈ {mm}:{ss:02d} · fala sugerida: {quem}]\n"
    corpo = "\n\n".join((f"({q}) " if len(r["fala"]) > 1 else "") + t for q, t in r["fala"])
    s.notes = cab + corpo + f"\n\n[Apontar] {r['apontar']}\n[Transição] {r['transicao']}"
    return s


slides = []

# =====================================================================================================
# 1 CAPA
# =====================================================================================================
s = new(1, "FieldOps: planejamento integrado de um MVP de inspeção em campo")
s.box(0, 0, W, 4.15, None, fill=PETROL, name="faixa")
s.text(0.6, 0.45, 12.1, 0.4, ["Gestão de Projetos  ·  Avaliação 2  ·  Apresentação final"], size=18, color=CLARO)
s.text(0.6, 1.05, 12.1, 1.7, ["FieldOps: planejamento integrado de um MVP de inspeção em campo"], size=42, bold=True, color=BRANCO, name="Titulo")
s.text(0.6, 3.0, 12.1, 0.9, ["App Android com operação offline, painel web administrativo e API REST, de 10/08 a 27/11/2026"],
       size=20, color=CLARO)
kp = [("8", "sprints e marcos (M1 a M8)"), (str(F["pacotes"]), "pacotes de trabalho na EAP"),
      (str(F["itens_cron"]), "itens no cronograma, 967 h"), ("22 + 4", "riscos e oportunidades")]
for i, (b, lab) in enumerate(kp):
    x = 0.6 + i * 3.08
    s.box(x, 4.5, 2.95, 1.3, [{"runs": [(b, {"size": 34, "bold": True, "color": PETROL})], "align": "c"},
                              {"runs": [(lab, {"size": 14, "color": GRAFITE})], "align": "c"}], fill=CLARO, valign="m")
    s.box(x, 4.5, 2.95, 0.07, None, fill=TEAL)
s.text(0.6, 6.15, 12.1, 0.3, [[("Grupo: ", {"bold": True}), ("Felipe Marques (FM), João Victor Souza (JV), Gabriel Ribeiro (GR), Pedro Dias (PD), André Fernandes (AF)", {})]],
       size=14)
s.text(0.6, 6.5, 12.1, 0.3, ["UniSENAI-SP Sorocaba  ·  ADS  ·  Prof. Me. Deivison S. Takatu  ·  Situação monitorada em 18/11/2026"],
       size=14, color=CINZA)
slides.append(s)

# =====================================================================================================
# 2 PROBLEMA E PROPOSTA
# =====================================================================================================
s = new(2, "O FieldOps troca papel e planilha por um fluxo digital único que funciona sem internet")
chrome_later = []
s.box(0.5, 1.4, 7.6, 0.72, [[("Hoje: ", {"bold": True, "color": VERMELHO}),
                              ("formulário em papel, planilha, foto solta e mensagens em vários canais. Resultado: dado perdido, retrabalho e nenhuma rastreabilidade.", {})]],
      fill=VERMELHO_L, size=14, valign="m", mx=0.15)
passos = [("1 Planejar", "Web", "modelo versionado, agenda e atribuição"),
          ("2 Executar", "App Android", "checklist, foto, QR e GPS, sem internet"),
          ("3 Sincronizar", "API REST", "outbox idempotente, sem duplicar"),
          ("4 Revisar", "Web", "aprova, reprova, corrige e audita")]
for i, (t, who, body) in enumerate(passos):
    x = 0.5 + i * 1.97
    s.box(x, 2.4, 1.75, 0.72, [{"runs": [(t, {"bold": True})]}, {"runs": [(who, {"size": 14})]}], fill=PETROL, color=BRANCO, mx=0.1)
    s.box(x, 3.12, 1.75, 1.35, [body], fill=CLARO2, size=16, valign="t", my=0.1, mx=0.1)
    if i < 3:
        s.box(x + 1.77, 2.6, 0.2, 0.32, None, fill=TEAL, shape="rarrow")
card(s, 0.5, 4.7, 7.6, 2.0, "Objetivo e prazo",
     [{"runs": [("Entregar o MVP em 16 semanas (10/08 a 27/11/2026), em 8 sprints e 8 marcos, sem investimento financeiro direto.", {})], "after": 6},
      {"runs": [("Padronizar com modelos versionados, executar offline sem perder dados, dar visibilidade ao supervisor e revisar com auditoria.", {})]}],
     accent=TEAL, bsize=16)
card(s, 8.4, 1.4, 4.43, 2.55, "Dentro do MVP", bsize=16, body=[
    {"runs": [("App Android com SQLite e outbox", {})], "bullet": True, "after": 5},
    {"runs": [("Painel web administrativo", {})], "bullet": True, "after": 5},
    {"runs": [("API REST com OpenAPI e JWT", {})], "bullet": True, "after": 5},
    {"runs": [("Foto, QR Code e localização", {})], "bullet": True, "after": 5},
    {"runs": [("Revisão com trilha de auditoria", {})], "bullet": True, "after": 5}], accent=VERDE)
card(s, 8.4, 4.1, 4.43, 2.6, "Fora do escopo", bsize=16, body=[
    {"runs": [("Portal do cliente e multiempresa", {})], "bullet": True, "after": 5},
    {"runs": [("Pagamento, IA e integração IoT", {})], "bullet": True, "after": 5},
    {"runs": [("Assinatura com validade jurídica", {})], "bullet": True, "after": 5},
    {"runs": [("Mais de um técnico por inspeção", {})], "bullet": True, "after": 5},
    {"runs": [("Validação obrigatória fora do Android", {})], "bullet": True, "after": 5}], accent=VERMELHO)
slides.append(s)

# =====================================================================================================
# 3 ABORDAGEM DE GESTAO
# =====================================================================================================
s = new(3, "Gerimos em 8 sprints e 8 marcos, com backlog de 72 PBIs e o GitHub como fonte da verdade")
cor_sit = lambda t: (VERDE if "Atingido" == t.replace("🔵", "").strip().split(" (")[0].replace("Atingido", "Atingido") and "pendências" not in t and "Não" not in t else
                     AMARELO if "pendências" in t else VERMELHO if "Não atingido" in t else CINZA)
for i, m in enumerate(F["marcos"]):
    x = 0.5 + i * 1.545
    sit = m["sit"]
    if "Não atingido" in sit:
        fc, tc = VERMELHO, BRANCO
    elif "pendências" in sit:
        fc, tc = AMARELO, GRAFITE
    elif "Atingido" in sit:
        fc, tc = VERDE, BRANCO
    else:
        fc, tc = CINZA, BRANCO
    nome = m["nome"].replace("Recursos nativos", "Recursos nativos").replace("Execução online", "Execução online")
    s.box(x, 1.4, 1.43, 1.25, [{"runs": [(f"S{i + 1} · {m['id']}", {"bold": True})], "align": "c"},
                               {"runs": [(nome, {})], "align": "c"},
                               {"runs": [(m["data"][:5], {"bold": True})], "align": "c"}], fill=fc, color=tc, size=14, mx=0.04)
s.text(0.5, 2.7, 12.3, 0.3, ["Cor do marco em 18/11: verde = atingido; amarelo = atingido com pendências; vermelho = não atingido; cinza = futuro"],
       size=14, color=CINZA)
s.box(0.5, 3.15, 5.1, 3.0, None, fill=CLARO2)
s.box(0.5, 3.15, 0.08, 3.0, None, fill=TEAL)
s.text(0.72, 3.23, 4.8, 0.3, ["Backlog: 10 épicos, 72 PBIs P0"], size=14, bold=True, color=TEAL)
eps = ["EP-01 Fundação", "EP-02 Acesso", "EP-03 Cadastros", "EP-04 Modelos", "EP-05 Planejamento", "EP-06 Execução",
       "EP-07 Nativos", "EP-08 Offline e sync", "EP-09 Revisão", "EP-10 Qualidade"]
for i, t in enumerate(eps):
    s.box(0.72 + (i % 2) * 2.42, 3.62 + (i // 2) * 0.42, 2.34, 0.36, [t], fill=TEAL_XL, size=14, mx=0.1)
s.text(0.72, 5.75, 4.8, 0.3, [{"runs": [("10 PBIs P1 ficam fora da linha de base.", {"bold": True})]}], size=14)
card(s, 5.8, 3.15, 3.3, 3.0, "GitHub, fonte da verdade", [
    {"runs": [("4 repositórios: docs, backend, frontend, app", {})], "bullet": True, "after": 6},
    {"runs": [("1 milestone por sprint", {})], "bullet": True, "after": 6},
    {"runs": [("PR com revisão e CI", {})], "bullet": True, "after": 6},
    {"runs": [("Conventional Commits", {})], "bullet": True}], accent=PETROL, bsize=16)
card(s, 9.3, 3.15, 3.53, 3.0, "Ordem de corte (RJ07)", [
    {"runs": [("1 sem dashboard avançado", {})], "after": 4},
    {"runs": [("2 limitar tipos de resposta", {})], "after": 4},
    {"runs": [("3 só foto da câmera", {})], "after": 4},
    {"runs": [("4 construtor sem arrastar", {})], "after": 4},
    {"runs": [("5 conflito: detectar e bloquear", {})], "after": 4},
    {"runs": [("6 adiar notificações e PDF", {})]}], accent=VERMELHO, bsize=16)
s.box(0.5, 6.3, 12.33, 0.6, [[("Ritos: ", {"bold": True}), ("planning, daily, review, demo do marco, retrospectiva e relatório quinzenal. ", {}),
                               ("Núcleo intocável: ", {"bold": True}), ("login, planejamento, checklist, foto, offline, sync, revisão.", {})]],
      fill=CLARO, size=14, mx=0.15)
slides.append(s)

# =====================================================================================================
# 4 BENCHMARKING
# =====================================================================================================
s = new(4, "Há soluções maduras no mercado; o FieldOps se justifica pelo controle acadêmico, não por superá-las")
OK, MK, PA, NC = VERDE_L, "D9E6F2", AMARELO_L, CLARO
hdr = lambda t: dict(t=t, fill=GRAFITE, color=BRANCO, bold=True, align="c")
FO = lambda t: dict(t=t, fill=PETROL, color=BRANCO, bold=True)
cell = lambda t, f: dict(t=t, fill=f)
crit = lambda t: dict(t=t, fill=CLARO, bold=True)
rows = [
    [dict(t="Critério", fill=GRAFITE, color=BRANCO, bold=True), dict(t="FieldOps (MVP)", fill=PETROL, color=BRANCO, bold=True, align="c"),
     hdr("SafetyCulture (Mitti)"), hdr("Fulcrum"), hdr("GoAudits"), hdr("KoboToolbox")],
    [crit("Funciona offline"), FO("Projetado; sync em atraso"), cell("Sim, no app móvel", OK), cell("Sim (marketing)", MK), cell("Sim (marketing)", MK), cell("Sim, no KoboCollect", OK)],
    [crit("Checklists versionados"), FO("Sim: versão imutável e snapshot"), cell("Parcial: sem ver versões antigas", PA), cell("n/c", NC), cell("n/c", NC), cell("Sim: histórico de versões", OK)],
    [crit("QR do equipamento"), FO("Sim: QR único por equipamento"), cell("Sim: QR e código de barras", OK), cell("Sim: leitor de QR (marketing)", MK), cell("n/c", NC), cell("Parcial: campo de código", PA)],
    [crit("Foto e GPS"), FO("Foto e GPS pontual no app"), cell("n/c na doc. oficial", NC), cell("Sim, automático (marketing)", MK), cell("Sim (marketing)", MK), cell("Sim, GPS também offline", OK)],
    [crit("Revisão e aprovação"), FO("Sim; API em construção"), cell("Sim: 1 aprovador por modelo", OK), cell("n/c", NC), cell("n/c", NC), cell("Sim: aprovado, não aprovado", OK)],
    [crit("Trilha de auditoria"), FO("Sim (RP10); em construção"), cell("Parcial: log por plano", PA), cell("Histórico e trilha (marketing)", MK), cell("n/c", NC), cell("Parcial: metadado de auditoria", PA)],
    [crit("Custo e licença"), FO("Sem licença; horas: R$ 47.714,83"), cell("Grátis (10); US$ 24 Premium", OK), cell("Pago por usuário; valor n/c", NC), cell("Por usuário, ~US$ 10 (marketing)", MK), cell("Grátis, com limites; aberto", OK)],
    [crit("Customização acadêmica"), FO("Total: código e regras próprios"), cell("Só configuração, sem código-fonte", PA), cell("Só configuração, sem código-fonte", PA), cell("Só configuração, sem código-fonte", PA), cell("Alta: código aberto", OK)],
]
s.table(0.5, 1.32, [2.4, 2.15, 1.95, 1.95, 1.95, 1.93], [0.54] * 9, rows, border=BRANCO, bw=1.5, size=14, my=0.02)
lg = [(OK, "Confirmado (doc. oficial)"), (MK, "Alegação do fornecedor"), (PA, "Parcial ou limitado"), (NC, "n/c: não conferido")]
xs = [0.5, 3.75, 7.2, 10.1]
ws = [3.15, 3.35, 2.8, 2.73]
for (f, t), x, w in zip(lg, xs, ws):
    s.box(x, 6.27, 0.28, 0.28, None, fill=f, line=CINZA_L, lw=1)
    s.text(x + 0.36, 6.24, w - 0.4, 0.34, [t], size=14, valign="m")
s.text(0.5, 6.62, 12.33, 0.45, ["Fontes (18/11/2026): help.safetyculture.com (help.mitti.com), mitti.com/pricing e support.kobotoolbox.org (oficiais); fulcrumapp.com e goaudits.com "
                                "(marketing; preços indisponíveis). Customização: avaliação do grupo. FieldOps é MVP acadêmico, sem a maturidade dos concorrentes."], size=12, color=CINZA)
slides.append(s)

# =====================================================================================================
# 5 EAP + RASTREABILIDADE
# =====================================================================================================
s = new(5, "A EAP tem 7 entregas e 36 pacotes, e cada requisito RP e RJ cai em pelo menos uma entrega")
reqs = [f"RP{i:02d}" for i in range(1, 11)] + [f"RJ{i:02d}" for i in range(1, 9)]
X0 = 5.65
CW = 0.395
s.text(X0, 1.32, 10 * CW, 0.28, ["Produto (RP)"], size=14, bold=True, color=PETROL, align="c")
s.text(X0 + 10 * CW, 1.32, 8 * CW, 0.28, ["Projeto (RJ)"], size=14, bold=True, color=TEAL, align="c")
for j, r in enumerate(reqs):
    s.box(X0 + j * CW, 1.62, CW - 0.03, 0.55, [{"runs": [(r[:2], {})], "align": "c"}, {"runs": [(r[2:], {"bold": True})], "align": "c"}],
          fill=PETROL if r.startswith("RP") else TEAL, color=BRANCO, size=14, mx=0, my=0)
RH = 0.6
Y0 = 2.25
s.box(0.5, Y0, 1.55, 7 * RH - 0.08, [{"runs": [("FieldOps", {"bold": True})], "align": "c"}, {"runs": [("MVP", {})], "align": "c"},
                                      {"runs": [("36 pacotes", {"size": 14})], "align": "c"}], fill=GRAFITE, color=BRANCO, size=16)
nomes_curtos = {1: "1 Gerenciamento do Projeto", 2: "2 Fundação Técnica", 3: "3 API REST Central", 4: "4 Interface Web",
                5: "5 Aplicativo Mobile Android", 6: "6 Qualidade e Testes", 7: "7 Entrega e Release (M8)"}
s.line(2.05, Y0 + 7 * RH / 2 - 0.04, 2.17, Y0 + 7 * RH / 2 - 0.04, color=CINZA, lw=2)
s.line(2.17, Y0 + 0.26, 2.17, Y0 + 6 * RH + 0.26, color=CINZA, lw=2)
for g in range(1, 8):
    y = Y0 + (g - 1) * RH
    s.line(2.17, y + 0.26, 2.3, y + 0.26, color=CINZA, lw=2)
    s.box(2.3, y, 3.3, RH - 0.08, [[(nomes_curtos[g], {"bold": True}), (f" ({F['pacotes_por_entrega'][g]})", {"color": CINZA})]],
          fill=TEAL_XL, size=14, mx=0.1)
    cov = F["eap_req"][g][1]
    for j, r in enumerate(reqs):
        on = r in cov
        s.box(X0 + j * CW, y, CW - 0.03, RH - 0.08, None, fill=(PETROL if r.startswith("RP") else TEAL) if on else CLARO)
s.text(0.5, 6.58, 12.33, 0.5, ["Verificado por script: os 18 requisitos têm entrega, os 72 PBIs P0 estão em algum pacote e os 10 PBIs P1 ficam fora da linha de base. "
                               "(n) = pacotes de trabalho, onde se penduram cronograma, orçamento e RACI."], size=14, color=GRAFITE)
slides.append(s)

# =====================================================================================================
# 6 CRONOGRAMA (Gantt nativo)
# =====================================================================================================
s = new(6, "O caminho crítico passa pelo backend e não tem folga: qualquer atraso na API desloca o M8")
D0 = date(2026, 8, 10)
GX0, GX1 = 3.05, 11.15
K = (GX1 - GX0) / 110.0
gx = lambda d: GX0 + (d - D0).days * K
# sprints
for i in range(8):
    a = D0.toordinal() + 14 * i
    xa = GX0 + 14 * i * K
    s.box(xa, 1.3, 14 * K - 0.02, 0.32, [f"S{i + 1}"], fill=CLARO if i % 2 == 0 else CINZA_L, size=14, bold=True, align="c", color=PETROL, mx=0, my=0)
# marcos
fim_sprint = [date(2026, 8, 21), date(2026, 9, 4), date(2026, 9, 18), date(2026, 10, 2), date(2026, 10, 16), date(2026, 10, 30), date(2026, 11, 13), date(2026, 11, 27)]
for i, (m, dt) in enumerate(zip(F["marcos"], fim_sprint)):
    sit = m["sit"]
    fc = CINZA if "Futuro" in sit else VERMELHO if "Não atingido" in sit else AMARELO if "pendências" in sit else VERDE
    xc = gx(dt) + K * 0.5
    s.box(xc - 0.12, 1.68, 0.24, 0.24, None, fill=fc, shape="diamond")
    s.text(xc - 0.3, 1.93, 0.6, 0.27, [m["id"]], size=14, bold=True, align="c", color=GRAFITE, valign="m")
# grupos
GC = {1: "6B7A99", 2: "8E6BBF", 3: "2F6DB5", 4: "1F9E8C", 5: "E08E1F", 6: "C4505A", 7: "5A9E3A"}
GT = {1: "1 Gerenciamento", 2: "2 Fundação", 3: "3 API REST (backend)", 4: "4 Web", 5: "5 App Android", 6: "6 Qualidade e testes", 7: "7 Entrega e release"}
LANE, PAD = 0.098, 0.065


def lanes(items):
    ends = []
    out = []
    for a in sorted(items, key=lambda a: (a["ini"], a["fim"])):
        for li, e in enumerate(ends):
            if e < a["ini"]:
                ends[li] = a["fim"]
                out.append((a, li))
                break
        else:
            ends.append(a["fim"])
            out.append((a, len(ends) - 1))
    return out, len(ends)


y = 2.2
s.text(0.5, y - 0.02, 2.4, 0.3, ["Entrega da EAP"], size=14, bold=True, color=PETROL)
s.text(11.3, y - 0.02, 1.55, 0.3, ["% real."], size=14, bold=True, color=PETROL, align="r")
y += 0.28
for g in range(1, 8):
    its = [a for a in F["ativ"] if a["wbs"].startswith(f"{g}.")]
    ln, nl = lanes(its)
    h = nl * (LANE + 0.015) + PAD
    s.box(GX0 - 0.0, y, GX1 - GX0, h, None, fill=CLARO2)
    s.text(0.5, y, 2.5, h, [GT[g]], size=14, valign="m", color=GRAFITE)
    for a, li in ln:
        xa, xb = gx(a["ini"]), gx(a["fim"]) + K
        yy = y + PAD / 2 + li * (LANE + 0.015)
        s.box(xa, yy, xb - xa, LANE, None, fill=CLARO if False else {1: "D3D8E4", 2: "DDD2EC", 3: "C9DAEF", 4: "BFE6E0", 5: "F6DDB8", 6: "F0CFD2", 7: "D2E7C9"}[g],
              line=VERMELHO if a["critica"] else None, lw=1.25)
        if a["real"] > 0:
            s.box(xa, yy, (xb - xa) * a["real"], LANE, None, fill=GC[g], line=VERMELHO if a["critica"] else None, lw=1.25)
    tot = sum(a["esforco"] for a in its)
    pr = sum(a["esforco"] * a["real"] for a in its) / tot
    s.text(11.3, y, 1.55, h, [f"{pr * 100:.0f}%"], size=14, bold=True, align="r", valign="m", color=GRAFITE)
    y += h + 0.035
# caminho critico
crit = [a for a in F["ativ"] if a["critica"]]
ln, nl = lanes(crit)
h = nl * (LANE + 0.015) + PAD
s.box(GX0, y, GX1 - GX0, h, None, fill=VERMELHO_L)
s.text(0.5, y, 2.5, h, [[("Caminho crítico", {"bold": True, "color": VERMELHO}), (" (20)", {})]], size=14, valign="m")
for a, li in ln:
    xa, xb = gx(a["ini"]), gx(a["fim"]) + K
    s.box(xa, y + PAD / 2 + li * (LANE + 0.015), xb - xa, LANE, None, fill=VERMELHO)
y += h + 0.05
yg_end = y
# hoje
xh = gx(date(2026, 11, 18)) + K * 0.5
s.line(xh, 1.3, xh, yg_end, color=VERMELHO, lw=2.5)
s.text(xh - 1.25, yg_end + 0.02, 1.5, 0.28, ["hoje 18/11"], size=14, bold=True, color=VERMELHO, align="r", valign="m")
s.text(0.5, yg_end + 0.02, 8.0, 0.28, ["Claro = planejado  ·  escuro = realizado  ·  contorno vermelho = crítica"], size=14, color=CINZA, valign="m")
s.box(0.5, yg_end + 0.38, 12.33, 0.66, [{"runs": [("20 atividades e 8 marcos sem folga, quase todas de backend.", {"bold": True})]},
                                          {"runs": [("Restam 32,5 dias úteis de trabalho crítico para 6 de calendário; sem corte, o M8 iria para 06/01/2027.", {})]}],
      fill=GRAFITE, color=BRANCO, size=14, mx=0.15)
GANTT_END = yg_end + 1.0
slides.append(s)

# =====================================================================================================
# 7 RECURSOS E RESPONSABILIDADES
# =====================================================================================================
s = new(7, "O gerente aparece em 36 de 36 pacotes: a carga do gerente é o principal desequilíbrio de pessoas")
s.box(1.085, 1.4, 4.6, 0.78, [{"runs": [("Comitê (PI-01, PI-03)", {"bold": True})], "align": "c"}, {"runs": [("PO acadêmico: Prof. Glauco (PI-02)", {})], "align": "c"}],
      fill=GRAFITE, color=BRANCO)
s.box(1.535, 2.45, 3.7, 0.78, [{"runs": [("Gerente: FM Felipe Marques", {"bold": True})], "align": "c"}, {"runs": [("também dev mobile", {})], "align": "c"}],
      fill=PETROL, color=BRANCO)
s.line(3.385, 2.18, 3.385, 2.45, color=CINZA, lw=2)
frentes = [("Backend", "JV, GR, PD"), ("Web", "AF"), ("Mobile", "FM, PD"), ("Qualidade e docs", "GR, PD, AF")]
s.line(3.385, 3.23, 3.385, 3.55, color=CINZA, lw=2)
s.line(1.18, 3.55, 5.59, 3.55, color=CINZA, lw=2)
for i, (t, m) in enumerate(frentes):
    x = 0.5 + i * 1.47
    s.line(x + 0.68, 3.55, x + 0.68, 3.75, color=CINZA, lw=2)
    s.box(x, 3.75, 1.37, 1.15, [{"runs": [(t, {"bold": True})], "align": "c"}, {"runs": [(m, {})], "align": "c"}], fill=TEAL_XL, size=14, mx=0.04)
card(s, 0.5, 5.15, 5.8, 1.55, "Capacidade: 960 h",
     ["5 pessoas × 16 semanas × 12 h. Cronograma: 967 h (FM 202, JV 190, GR 192, PD 191, AF 192)."], accent=TEAL, bsize=16)
# barras RACI
s.text(6.7, 1.38, 6.1, 0.3, ["Papéis na matriz RACI (36 pacotes)"], size=14, bold=True, color=PETROL)
RX, SC = 7.35, 0.098
for i, p in enumerate(["FM", "JV", "GR", "PD", "AF"]):
    r, a, c, _ = F["raci"][p]
    y = 1.8 + i * 0.5
    s.text(6.7, y, 0.6, 0.4, [p], size=14, bold=True, valign="m")
    x = RX
    for v, col, tc in [(r, PETROL, BRANCO), (a, TEAL, BRANCO), (c, TEAL_L, GRAFITE)]:
        if v:
            s.box(x, y, v * SC, 0.4, [str(v)], fill=col, color=tc, size=14, bold=True, align="c", mx=0, my=0)
            x += v * SC
lx = 7.35
for t, col in [("R responsável", PETROL), ("A aprova", TEAL), ("C consultado", TEAL_L)]:
    s.box(lx, 4.4, 0.24, 0.24, None, fill=col)
    s.text(lx + 0.3, 4.37, 1.6, 0.3, [t], size=14, valign="m")
    lx += 1.85
card(s, 6.7, 4.85, 3.0, 1.85, "Desequilíbrios", [
    {"runs": [("FM: 11 R e 21 A; A/R sem 2ª leitura em 5.1, 5.3 e 5.5", {})], "bullet": True, "after": 2},
    {"runs": [("AF: único R do web (7 R)", {})], "bullet": True}], accent=VERMELHO, bsize=14)
card(s, 9.85, 4.85, 2.98, 1.85, "Respostas", [
    {"runs": [("Cenário B: A de 6 pacotes a JV e GR", {})], "bullet": True, "after": 2},
    {"runs": [("Revisão cruzada e pareamento", {})], "bullet": True}], accent=VERDE, bsize=14)
slides.append(s)

# =====================================================================================================
# 8 CUSTOS
# =====================================================================================================
s = new(8, "O orçamento é R$ 54.872,05, quase tudo mão de obra valorada; o caixa esperado é de R$ 669,08")
o = F["orc"]
s.text(0.5, 1.35, 5.9, 0.3, ["Da estimativa PERT ao orçamento total (R$)"], size=14, bold=True, color=PETROL)
base_y, hmax = 4.55, 2.65
sc = hmax / o["total"]
cols = [("Base PERT", 0, o["base"], PETROL), ("+10% cont.", o["base"], o["cont"], TEAL), ("BAC", 0, o["bac"], PETROL),
        ("+5% reserva", o["bac"], o["ger"], TEAL_L), ("Total", 0, o["total"], GRAFITE)]
vals = [o["base"], o["cont"], o["bac"], o["ger"], o["total"]]
for i, ((nm, b0, v, c), vv) in enumerate(zip(cols, vals)):
    x = 0.6 + i * 1.18
    top = base_y - (b0 + v) * sc
    s.box(x, top, 0.96, v * sc, None, fill=c)
    s.text(x - 0.12, top - 0.3, 1.2, 0.28, [br(vv)], size=14, bold=True, align="c", valign="m")
    s.text(x - 0.1, base_y + 0.05, 1.16, 0.3, [nm], size=14, align="c")
s.line(0.5, base_y, 6.45, base_y, color=CINZA, lw=1.5)
# curva S
s.text(6.9, 1.35, 5.9, 0.3, ["Curva S: linha de base acumulada por sprint (R$ mil)"], size=14, bold=True, color=PETROL)
px0, px1, py0, py1 = 7.75, 12.55, 4.55, 1.95
dx = lambda d: px0 + (d - D0).days / 109.0 * (px1 - px0)
dy = lambda v: py0 - v / 60000.0 * (py0 - py1)
for v in (0, 20000, 40000, 60000):
    s.line(px0, dy(v), px1, dy(v), color=CINZA_L, lw=1)
    s.text(6.9, dy(v) - 0.14, 0.78, 0.28, [f"{v // 1000}"], size=14, align="r", valign="m", color=CINZA)
pts = [(dx(D0), dy(0))] + [(dx(d), dy(v)) for d, v in zip(fim_sprint, F["curvaS"])]
s.line(px0, dy(o["bac"]), px1, dy(o["bac"]), color=VERMELHO, lw=1.5, dash=True)
s.text(px0 + 0.05, dy(o["bac"]) - 0.32, 3.2, 0.28, ["BAC 52,5 mil"], size=14, color=VERMELHO, bold=True, valign="m")
s.poly(pts, color=PETROL, lw=3)
for (x, yv) in pts[1:]:
    s.box(x - 0.06, yv - 0.06, 0.12, 0.12, None, fill=PETROL, shape="oval")
xh = dx(date(2026, 11, 18))
s.line(xh, py1 - 0.15, xh, py0, color=VERMELHO, lw=2)
s.text(xh - 1.2, py0 - 0.4 - 0.0, 1.12, 0.28, ["hoje"], size=14, bold=True, color=VERMELHO, align="r", valign="m")
for i, d in enumerate(fim_sprint):
    s.text(dx(d) - 0.3, base_y + 0.05, 0.6, 0.3, [f"S{i + 1}"], size=14, align="c", color=CINZA)
s.line(px0, py0, px1, py0, color=CINZA, lw=1.5)
kp = [("R$ 669,08", "caixa esperado"), ("R$ 374,00", "caixa mais provável"), ("R$ 2.478,50", "caixa no pior caso"), ("52 itens", "36 M.O., 14 diretos, 2 reservas")]
for i, (b, lab) in enumerate(kp):
    x = 0.5 + i * 3.1
    kpi(s, x, 5.1, 3.0, 0.95, b, lab, fill=CLARO, color=PETROL if i < 3 else GRAFITE, bigsize=22, lsize=14)
s.box(0.5, 6.15, 12.33, 0.62, [[("Controle: ", {"bold": True}),
                                 ("EVM por marco. Desvio até 10% do item: gerente. Contingência acima de 5% do BAC: PI-02. Caixa novo acima de R$ 150: exceção ao PI-01 e PI-02.", {})]],
      fill=GRAFITE, color=BRANCO, size=14, mx=0.15)
slides.append(s)

# =====================================================================================================
# 9 QUALIDADE
# =====================================================================================================
s = new(9, "A qualidade do processo é o ponto fraco: só 11% dos PRs têm revisão registrada de outra pessoa")
s.text(0.5, 1.35, 7.0, 0.3, ["Folha de verificação do DoD em 55 PRs mergeados (% conformes)"], size=14, bold=True, color=PETROL)
dados = [("Critérios de aceitação marcados (0 de 518 issues)", 0, "meta 100%"),
         ("PRs com revisão registrada de outra pessoa (6 de 55)", 11, "meta 100%"),
         ("PRs com evidência de funcionamento", 40, "meta ≥ 90%"),
         ("PRs com issue vinculada (Closes #N)", 75, "meta 100%"),
         ("Taxa de sucesso das execuções de CI", 89, "meta ≥ 90%"),
         ("CI verde no momento do merge", 97, "meta 100%")]
BX, BW = 3.65, 2.3
for i, (lab, v, meta) in enumerate(dados):
    y = 1.8 + i * 0.78
    s.text(0.5, y, 3.1, 0.7, [lab], size=14, valign="m")
    s.box(BX, y + 0.16, BW, 0.38, None, fill=CLARO)
    col = VERMELHO if v < 50 else AMARELO if v < 90 else VERDE
    if v > 0:
        s.box(BX, y + 0.16, BW * v / 100, 0.38, None, fill=col)
    s.text(BX + BW + 0.08, y + 0.08, 0.62, 0.54, [f"{v}%"], size=16, bold=True, valign="m")
    s.text(BX + BW + 0.72, y, 1.15, 0.7, [meta], size=14, color=CINZA, valign="m")
s.text(0.5, 6.5, 7.4, 0.3, ["Só a revisão registrada no GitHub é visível."], size=14, color=CINZA)
card(s, 8.1, 1.4, 4.73, 1.5, "Padrão e aceite", [
    "DoD por história e por camada; critérios dado/quando/então por marco (AC-SYNC, AC-REVIEW, AC-RELEASE de 19 passos)."], accent=TEAL)
card(s, 8.1, 3.0, 4.73, 1.5, "Garantia × controle", [
    "Garantia audita o processo (revisão cruzada, retro). Controle mede o produto (CI, testes, gráficos p e I-MR)."], accent=PETROL)
card(s, 8.1, 4.6, 4.73, 1.2, "Não conformidade", [
    "Vira issue com severidade; a crítica bloqueia a entrega."], accent=VERMELHO)
s.box(8.1, 5.9, 4.73, 0.9, [[("Ação 1: ", {"bold": True}), ("proteger a develop, com 1 aprovação de outra pessoa e CI verde.", {})]],
      fill=GRAFITE, color=BRANCO, size=14, mx=0.15)
slides.append(s)

# =====================================================================================================
# 10 RISCOS
# =====================================================================================================
s = new(10, "Cinco dos 22 riscos têm severidade alta, e a sincronização offline lidera o ranking")
s.text(0.5, 1.33, 6.0, 0.5, ["22 riscos: 5 altos, 13 médios e 4 baixos; 9 já ocorreram. A cor do chip é a severidade exata."], size=14, bold=True, color=PETROL)
niv = [0.05, 0.10, 0.20, 0.40, 0.80]
probs = [0.9, 0.7, 0.5, 0.3, 0.1]
MX0, MY0, CWm, CHm = 1.25, 2.25, 1.0, 0.7
s.text(0.5, 1.9, 0.75, 0.3, ["P ↓ I →"], size=14, color=CINZA, valign="m")
for j, nv in enumerate(niv):
    s.box(MX0 + j * CWm, 1.9, CWm - 0.03, 0.3, [br(nv)], fill=GRAFITE, color=BRANCO, size=14, bold=True, align="c", mx=0, my=0)
cls = {r["id"]: r["classe"] for r in F["riscos"]}
for i, p in enumerate(probs):
    y = MY0 + i * CHm
    s.box(0.5, y, 0.72, CHm - 0.03, [br(p, 1)], fill=GRAFITE, color=BRANCO, size=14, bold=True, align="c", mx=0, my=0)
    for j, nv in enumerate(niv):
        v = p * nv
        bg = VERMELHO_L if v >= 0.15 else AMARELO_L if v >= 0.05 else VERDE_L
        s.box(MX0 + j * CWm, y, CWm - 0.03, CHm - 0.03, None, fill=bg)
        ids = F["matriz"].get((p, j), [])
        for k, rid in enumerate(ids):
            c = cls[rid]
            fc, tc = (VERMELHO, BRANCO) if c == "Alta" else (AMARELO, GRAFITE) if c == "Média" else (VERDE, BRANCO)
            s.box(MX0 + j * CWm + 0.02 + (k % 2) * 0.48, y + 0.05 + (k // 2) * 0.31, 0.46, 0.28, [rid], fill=fc, color=tc, size=14, bold=True, align="c", mx=0, my=0)
top = [
    ("1", "R06", "Falha de sincronização offline", "0,26", "Mitigar: chave idempotente e 3 testes AC-SYNC (JV)"),
    ("2", "R03", "Backend sem responsável", "0,25", "Mitigar: dono e data para as 21 issues (FM)"),
    ("3", "R02", "Backlog acima da capacidade", "0,23", "Mitigar: nova linha de base e ordem de corte (FM)"),
    ("4", "R14", "Integração tardia app, web e API", "0,19", "Mitigar: fluxo ponta a ponta em dias alternados (PD)"),
    ("5", "R04", "Sobrecarga do gerente", "0,16", "Mitigar: delegar revisão do app ao PD; 1 h diária de gestão (FM)"),
]
tr = [[dict(t="#", fill=GRAFITE, color=BRANCO, bold=True, align="c"), dict(t="Risco", fill=GRAFITE, color=BRANCO, bold=True),
       dict(t="Sev.", fill=GRAFITE, color=BRANCO, bold=True, align="c"), dict(t="Resposta e dono", fill=GRAFITE, color=BRANCO, bold=True)]]
for rk, rid, nm, sv, rp in top:
    tr.append([dict(t=rk, fill=VERMELHO, color=BRANCO, bold=True, align="c"), dict(t=[[(rid + " ", {"bold": True}), (nm, {})]], fill=CLARO2),
               dict(t=sv, fill=CLARO2, bold=True, align="c"), dict(t=rp, fill=CLARO2)])
s.table(6.55, 1.9, [0.4, 2.2, 0.6, 3.08], [0.3] + [0.7] * 5, tr, border=BRANCO, bw=2, size=14)
for i, (b, lab) in enumerate([("R$ 6.635", "EMV dos riscos ainda possíveis"), ("R$ 4.771,48", "contingência de 10%"),
                              ("R$ 7.157,22", "contingência 10% + 5%"), ("R$ 9.812", "P80 da simulação Monte Carlo")]):
    kpi(s, 0.5 + i * 3.1, 5.85, 3.0, 0.98, b, lab, fill=PETROL if i != 0 else VERMELHO, bigsize=22)
slides.append(s)

# =====================================================================================================
# 11 COMUNICACAO E PARTES INTERESSADAS
# =====================================================================================================
s = new(11, "Sete das 13 partes interessadas têm poder alto, e 19 rotinas de comunicação cuidam de cada uma")
QX0, QX1, QY0, QY1 = 1.45, 6.5, 1.4, 6.2
qx = lambda v: QX0 + v / 10.6 * (QX1 - QX0)
qy = lambda v: QY1 - v / 10.6 * (QY1 - QY0)
thx, thy = qx(5.5), qy(5.5)
s.box(QX0, QY0, thx - QX0, thy - QY0, None, fill=AMARELO_L)
s.box(thx, QY0, QX1 - thx, thy - QY0, None, fill=VERMELHO_L)
s.box(QX0, thy, thx - QX0, QY1 - thy, None, fill=CLARO)
s.box(thx, thy, QX1 - thx, QY1 - thy, None, fill=TEAL_XL)
s.line(thx, QY0, thx, QY1, color=GRAFITE, lw=2)
s.line(QX0, thy, QX1, thy, color=GRAFITE, lw=2)
s.text(QX0 + 0.06, thy - 0.32, 2.4, 0.3, ["Manter satisfeito"], size=14, bold=True, color=CINZA)
s.text(thx + 0.06, thy - 0.32, 2.5, 0.3, ["Gerenciar com atenção"], size=14, bold=True, color=CINZA)
s.text(QX0 + 0.06, QY1 - 0.32, 2.4, 0.3, ["Monitorar"], size=14, bold=True, color=CINZA)
s.text(thx + 0.06, QY1 - 0.32, 2.4, 0.3, ["Manter informado"], size=14, bold=True, color=CINZA)
s.text(0.5, 3.1, 0.9, 0.8, [{"runs": [("Poder", {"bold": True})], "align": "c"}, {"runs": [("↑", {"bold": True, "size": 20})], "align": "c"}], size=14, color=PETROL)
s.text(QX0, QY1 + 0.08, QX1 - QX0, 0.3, ["Interesse →  (número = PI-xx)"], size=14, bold=True, color=PETROL, align="c")
chipc = {"Gerenciar com atenção": (VERMELHO, BRANCO), "Manter satisfeito": (AMARELO, GRAFITE), "Manter informado": (TEAL, BRANCO), "Monitorar": (CINZA, BRANCO)}
for p in F["partes"]:
    fc, tc = chipc[p["quad"]]
    cx, cy = qx(p["interesse"]), qy(p["poder"])
    s.box(cx - 0.23, cy - 0.17, 0.46, 0.34, [p["id"][3:]], fill=fc, color=tc, size=14, bold=True, align="c", mx=0, my=0, shape="round")
RX0 = 6.8
RW = 6.03
card(s, RX0, 1.4, RW, 1.3, "Gerenciar com atenção (5)", ["PI-02 Glauco, PI-03 Comitê, PI-04 Deivison, PI-05 FM, PI-06 Equipe. Alinhamento semanal, demo de marco e relatório quinzenal."], accent=VERMELHO)
card(s, RX0, 2.78, RW, 1.05, "Manter satisfeito (2)", ["PI-01 Coordenação, PI-13 UniSENAI. Aviso em 24 h se um marco estiver em risco."], accent=AMARELO, tcolor=GRAFITE)
card(s, RX0, 3.91, RW, 1.2, "Manter informado (4)", ["PI-07 Técnicos, PI-08 Supervisores, PI-09 Admin., PI-11 Operadora. Teste com usuário-proxy em M3, M5 e M7."], accent=TEAL)
card(s, RX0, 5.19, RW, 1.05, "Monitorar (2)", ["PI-10 Cliente, PI-12 Provedores. Limites dos planos toda semana; portal como trabalho futuro."], accent=CINZA, tcolor=GRAFITE)
s.box(RX0, 6.34, RW, 0.45, [[("19 comunicações; maior lacuna: técnicos e supervisores", {"bold": True})]], fill=GRAFITE, color=BRANCO, size=14, mx=0.12)
slides.append(s)

# =====================================================================================================
# 12 MONITORAMENTO E CONTROLE (situacao real)
# =====================================================================================================
s = new(12, "Em 18/11 temos 57 de 103 issues e M6 e M7 sem entrega: o desvio é real e tem resposta definida")
s.text(0.5, 1.33, 6.5, 0.3, ["Issues concluídas por sprint em 18/11/2026"], size=14, bold=True, color=PETROL)
bb, bh = 4.15, 2.05
for i, (nm, a, b) in enumerate(F["sprints"]):
    x = 0.55 + i * 0.79
    pct = a / b
    s.box(x, bb - bh, 0.66, bh, None, fill=CLARO)
    col = VERDE if pct >= 0.95 else AMARELO if pct >= 0.70 else VERMELHO
    if a:
        s.box(x, bb - bh * pct, 0.66, bh * pct, None, fill=col)
    s.text(x - 0.06, bb - bh - 0.3, 0.78, 0.28, [f"{a}/{b}"], size=14, bold=True, align="c", valign="m")
    s.text(x - 0.06, bb + 0.03, 0.78, 0.28, [f"S{i + 1}"], size=14, bold=True, align="c", valign="m")
    s.text(x - 0.06, bb + 0.3, 0.78, 0.28, [f"M{i + 1}"], size=14, align="c", valign="m", color=CINZA)
s.line(0.5, bb, 6.85, bb, color=CINZA, lw=1.5)
for i, (b, lab, fc) in enumerate([("57/103", "55%", PETROL), ("0,53", "SPI", VERMELHO), ("0,58*", "CPI", VERMELHO), ("M8", "em risco", VERMELHO)]):
    kpi(s, 0.5 + i * 1.6, 4.85, 1.5, 0.78, b, lab, fill=fc, bigsize=20)
s.text(0.5, 5.68, 6.4, 0.25, ["* custo real hipotético (12 h/pessoa/semana)."], size=14, color=CINZA)
card(s, 7.15, 1.4, 5.68, 1.38, "Web: 22 de 31 issues", ["Login, cadastros com QR, construtor e publicação de modelos, agenda, acompanhamento, evidências e fila de revisão."], accent=VERDE)
card(s, 7.15, 2.88, 5.68, 1.38, "App: 21 de 39 issues", ["Login seguro, checklist dinâmico, foto, QR, localização, SQLite e outbox. Faltam sincronização e correção."], accent=AMARELO, tcolor=GRAFITE)
card(s, 7.15, 4.36, 5.68, 1.38, "API: 14 de 41 issues", ["Autenticação, cadastros e modelos versionados. Faltam sincronização, evidências e revisão; 21 issues sem dono."], accent=VERMELHO)
s.box(0.5, 6.0, 1.45, 0.88, ["DECISÃO"], fill=VERDE, color=BRANCO, size=16, bold=True, align="c")
s.box(1.95, 6.0, 10.88, 0.88, [{"runs": [("Refazer a linha de base, aplicar já os itens 1 e 2 da ordem de corte e dar dono às 21 issues.", {"bold": True})]},
                                {"runs": [("Gatilhos: sprint abaixo de 40% no meio, issue P0 sem dono por 2 dias, SPI abaixo de 0,70. Mudança: issue e decisão do PI-02.", {})]}],
      fill=GRAFITE, color=BRANCO, size=14, mx=0.15)
slides.append(s)

# =====================================================================================================
# 13 LICOES
# =====================================================================================================
s = new(13, "As lições apontam três causas: integração tardia, backend sem dono e DoD autodeclarado")
H_ = lambda t: dict(t=t, fill=GRAFITE, color=BRANCO, bold=True)
lic = [
    ("Integrar cedo, a cada marco", "Login do app integrado à API só em 18/09; sincronização, revisão e evidências ainda sem integração (R14).",
     "Ambiente integrado com Docker Compose e seed; fluxo ponta a ponta em dias alternados."),
    ("Todo pacote precisa de dono", "21 issues do backend sem responsável; 88% dos commits do backend e 98% do app vêm de uma pessoa.",
     "Dono e data em toda issue; pareamento de 2 h por camada; revisão cruzada."),
    ("O DoD tem de ser verificado", "Só 11% dos PRs com revisão registrada de outra pessoa; 0 de 518 critérios marcados nas issues.",
     "Proteger a develop (1 aprovação e CI verde); marcar critérios ao fechar a issue."),
    ("Respeitar a prioridade do núcleo", "Dashboard P1 concluído em 09/11 enquanto a sincronização, P0, não começou (R10).",
     "Congelar as issues P1; aplicar a ordem de corte ao primeiro sinal de atraso."),
    ("Risco técnico pede protótipo e folga", "Offline e sincronização tinham a cauda mais pesada no PERT (classe D) e foram as sprints que mais atrasaram.",
     "Protótipo do motor de sync antes do marco; reserva de tempo no caminho crítico."),
]
tr = [[H_("Lição"), H_("Evidência medida"), H_("Recomendação")]]
for a, b, c in lic:
    tr.append([dict(t=a, fill=PETROL, color=BRANCO, bold=True), dict(t=b, fill=CLARO2), dict(t=c, fill=TEAL_XL)])
s.table(0.5, 1.4, [3.0, 4.75, 4.58], [0.4] + [0.92] * 5, tr, border=BRANCO, bw=2, size=14)
s.text(0.5, 6.5, 12.33, 0.3, ["Lições registradas a cada retrospectiva e consolidadas no encerramento (docs/lessons-learned.md)."], size=14, color=CINZA)
slides.append(s)

# =====================================================================================================
# 14 DECISOES-CHAVE
# =====================================================================================================
s = new(14, "Quatro decisões sustentam o projeto, cada uma com justificativa e custo assumido")
dec = [
    ("1  Next.js 16 em vez de Angular",
     "A especificação aceita Angular ou React. A sessão fica em cookie httpOnly e a API é acessada pelo servidor: o token não chega ao navegador (RJ06).",
     "Diverge do TAP de 30/09 e da rubrica de arquitetura Angular; o ADR-0008 ainda está aberto (docs#3, risco R18)."),
    ("2  Ordem de corte (RJ07)",
     "Prazo e 960 h são fixos, então o que cede é o escopo. Núcleo intocável: login, planejamento, checklist, foto, offline, sincronização e revisão.",
     "Saem dashboard avançado, tipos de resposta extras, notificações, PDF e assinatura."),
    ("3  Outbox com idempotência",
     "O SQLite é persistência operacional. Cada alteração vira operação com ID próprio; reenviar não duplica nem perde dados (AC-SYNC).",
     "É a parte mais complexa e a mais atrasada (R06; classe D no PERT)."),
    ("4  Contingência de 10% + 5%",
     "10% cobrem riscos identificados (gerente libera); 5% cobrem desconhecidos (só a coordenação libera). Com horas fixas, reserva não compra prazo.",
     "EMV de R$ 6.635 e P80 de R$ 9.812 superam os R$ 4.771,48; o excedente vira corte."),
]
for i, (t, why, cost) in enumerate(dec):
    x = 0.5 + (i % 2) * 6.265
    y = 1.4 + (i // 2) * 2.8
    s.box(x, y, 6.07, 0.45, [t], fill=PETROL, color=BRANCO, size=16, bold=True, mx=0.15)
    s.box(x, y + 0.45, 6.07, 2.2, None, fill=CLARO2)
    s.text(x + 0.15, y + 0.55, 5.8, 2.05, [{"runs": [("Por quê: ", {"bold": True, "color": TEAL}), (why, {})], "after": 6},
                                           {"runs": [("Custo assumido: ", {"bold": True, "color": VERMELHO}), (cost, {})]}], size=16)
slides.append(s)

# =====================================================================================================
# 15 CONCLUSAO
# =====================================================================================================
s = new(15, "Conclusão: o planejamento está integrado, o atraso foi medido e o núcleo do MVP está protegido")
cad = [("EAP", ["36 pacotes"]), ("Cronograma", ["71 itens", "967 h"]), ("Orçamento", ["52 linhas", "R$ 54.872,05"]),
       ("Riscos", ["22 riscos", "+ 4 oportunidades"]), ("Controle", ["SPI 0,53", "CPI 0,58"])]
for i, (a, b) in enumerate(cad):
    x = 0.5 + i * 2.52
    s.box(x, 1.4, 2.2, 1.2, [{"runs": [(a, {"bold": True, "size": 16})], "align": "c"}] + [{"runs": [(t, {})], "align": "c"} for t in b],
          fill=PETROL if i < 4 else VERMELHO, color=BRANCO, size=14)
    if i < 4:
        s.box(x + 2.24, 1.84, 0.24, 0.32, None, fill=TEAL, shape="rarrow")
s.text(0.5, 2.8, 12.3, 0.3, ["Próximos passos até o M8 (27/11/2026)"], size=14, bold=True, color=PETROL)
passos = [("19/11", "Proteger a develop; dono nas 21 issues; itens 1 e 2 da ordem de corte"), ("21/11", "Contrato de sincronização fechado (docs#2)"),
          ("24/11", "Ensaio do AC-SYNC e do AC-RELEASE"), ("26/11", "Demonstração ponta a ponta antecipada"), ("27/11", "M8: aceite, lições aprendidas e relatório final")]
s.line(0.9, 3.58, 12.4, 3.58, color=TEAL, lw=3)
for i, (d_, t) in enumerate(passos):
    x = 0.5 + i * 2.52
    s.box(x + 0.95, 3.43, 0.3, 0.3, None, fill=VERMELHO if i == 4 else TEAL, shape="oval")
    s.text(x, 3.1, 2.2, 0.3, [{"runs": [(d_, {"bold": True, "color": PETROL})], "align": "c"}], size=14)
    s.text(x, 3.85, 2.3, 1.5, [{"runs": [(t, {})], "align": "c"}], size=16)
card(s, 0.5, 5.4, 12.33, 1.35, "Encerramento (EAP 1.4)", [
    "Aceite do comitê (PI-03) e da coordenação (PI-01) após a demonstração do AC-RELEASE, sem editar o banco; lições aprendidas e relatório final. "
    "Se o M8 não fechar tudo, entregamos o núcleo e registramos o restante como trabalho futuro."], accent=VERDE, bsize=16)
slides.append(s)

# =====================================================================================================
# 16 BACKUP
# =====================================================================================================
s = new(16, "Backup: oito perguntas difíceis com respostas curtas", backup=True)
qa = [
    ("Por que atrasou e o que muda?", "Backend sem dono (21 issues) e integração tardia quebraram o caminho crítico em S6. Muda: dono nas issues, nova linha de base e ordem de corte já."),
    ("Por que Next.js e não Angular?", "A especificação aceita Angular ou React; Next.js mantém a sessão no servidor (RJ06). Custo: diverge do TAP; ADR-0008 a publicar."),
    ("Por que estimar custos num projeto acadêmico?", "O enunciado pede hipóteses explícitas: horas a R$ 45 e R$ 60 (custo de oportunidade). O caixa real fica entre R$ 374 e R$ 2.478,50."),
    ("Como sabem o % realizado?", "Issues fechadas por sprint (57/103) são medidas. O % por atividade é estimativa calibrada a essa razão; o custo real do EVM é hipótese."),
    ("Como tratam o risco de sincronização?", "R06 (0,26): contrato push/pull fechado, chave idempotente e 3 cenários do AC-SYNC testados no backend real até 25/11."),
    ("Garantia ou controle da qualidade?", "Garantia audita o processo (revisão, DoD, retro). Controle mede o produto (CI, testes, gráficos de controle) e propõe mudanças."),
    ("O que é caminho crítico aqui?", "Corrente sem folga de 10/08 a 27/11: 20 atividades e 8 marcos, quase todas de backend. Restam 32,5 dias úteis para 6 de calendário."),
    ("Como será o encerramento?", "Demonstração do AC-RELEASE no M8 (19 passos, sem editar o banco), aceite do PI-03 e PI-01, lições e relatório; resto vira trabalho futuro."),
]
for i, (q, a) in enumerate(qa):
    x = 0.5 + (i % 2) * 6.265
    y = 1.38 + (i // 2) * 1.37
    s.box(x, y, 6.07, 1.29, None, fill=CLARO2)
    s.box(x, y, 0.08, 1.29, None, fill=AMARELO)
    s.text(x + 0.2, y + 0.06, 5.75, 1.2, [{"runs": [(q, {"bold": True, "color": PETROL})], "after": 2}, {"runs": [(a, {})]}], size=14)
slides.append(s)

assert len(slides) == TOTAL, len(slides)
# chrome (titulo, rodape) em todos menos a capa
for s in slides:
    if s.n == 1:
        s.text(11.8, 7.14, 1.03, 0.26, [f"1 / {TOTAL}"], size=12, color=CINZA, align="r", valign="m")
        continue
    chrome(s, TOTAL)


def problemas():
    out = []
    for s in slides:
        for p in s.issues:
            out.append((s.n, p))
    return out


CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    pb = problemas()
    for n, p in pb:
        print("AJUSTE slide", n, p)
    print("slides:", len(slides), "problemas de texto:", len(pb), "gantt termina em", round(GANTT_END, 2))
    only = None
    if "--only" in sys.argv:
        only = int(sys.argv[sys.argv.index("--only") + 1])
    sel = [s for s in slides if only is None or s.n == only]
    if "--nonotes" in sys.argv:  # QuickLook trava com notas do python-pptx; so para a pre-visualizacao
        import copy
        sel = [copy.copy(s) for s in sel]
        for s in sel:
            s.notes = ""
    out = RAIZ / ("apresentacao-final.pptx" if only is None else f"/private/tmp/claude-501/-Users-felipersas-Documents-Facul-gestao-proj/62d3b502-aedc-4c7d-92d1-65523f456f30/scratchpad/prev/only{only}.pptx")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    build_pptx(sel, out, "FieldOps: planejamento integrado de um MVP de inspeção em campo (apresentação final)", "Grupo FieldOps (FM, JV, GR, PD, AF)")
    html_path = RAIZ / "apresentacao-src" / "apresentacao.html"
    build_html(slides, html_path, "FieldOps - apresentação final")
    if "--render" in sys.argv:
        base = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-pdf-header-footer"]
        url = html_path.resolve().as_uri()
        subprocess.run(base + ["--print-to-pdf=" + str(RAIZ / "apresentacao-final.pdf"), url], check=True, capture_output=True, timeout=180)
        prev = Path("/private/tmp/claude-501/-Users-felipersas-Documents-Facul-gestao-proj/62d3b502-aedc-4c7d-92d1-65523f456f30/scratchpad/prev")
        prev.mkdir(parents=True, exist_ok=True)
        for s in slides:
            subprocess.run(base + [f"--screenshot={prev}/s{s.n:02d}.png", "--window-size=1920,1080", "--force-device-scale-factor=1", url + f"#s{s.n}"],
                           check=True, capture_output=True, timeout=120)
        print("render ok")


if __name__ == "__main__":
    main()
