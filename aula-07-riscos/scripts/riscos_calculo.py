"""Calculo do registro de riscos: niveis de impacto, severidade, ranking, EMV e simulacao de Monte Carlo."""
import numpy as np

from riscos_dados import AMEACAS, OPORTUNIDADES, TAXA_DEV, TAXA_GP

# ---- orcamento oficial (aula-05-custos-qualidade/orcamento-fieldops.md)
# Referencia unica: CUSTO BASE (valor esperado PERT, sem reservas). Faixas de impacto de custo e porcentagens usam este valor.
CUSTO_BASE = 47714.83
RESERVA_10 = 4771.48          # contingencia 10% do custo base (entra na linha de base, liberada pelo gerente)
RESERVA_5 = 2385.74           # reserva gerencial 5% do custo base (liberada so pelo patrocinador, PI-01)
LINHA_BASE = 52486.31         # BAC = custo base + contingencia
ORCAMENTO_TOTAL = 54872.05    # BAC + reserva gerencial
HORAS_ORCAMENTO = 967         # horas (cM) do orcamento
DIAS_UTEIS = 80               # 16 semanas x 5 dias

ESCALA_P = [(0.1, "Muito baixa", "menos de 10% de chance"), (0.3, "Baixa", "cerca de 30%"), (0.5, "Média", "cerca de 50%"),
            (0.7, "Alta", "cerca de 70%"), (0.9, "Muito alta", "90% ou já ocorreu")]
NIVEIS = [0.05, 0.10, 0.20, 0.40, 0.80]
LIM_ALTA, LIM_MEDIA = 0.15, 0.05   # severidade media: alta >= 0,15; media >= 0,05; baixa < 0,05
LIM_OBS_MAX = 0.24                  # lista de observacao: severidade maxima >= 0,24


def nivel_custo(reais):
    pct = reais / CUSTO_BASE
    for lim, n in [(0.02, 0.05), (0.10, 0.10), (0.20, 0.20), (0.40, 0.40)]:
        if pct < lim:
            return n
    return 0.80


def nivel_tempo(dias):
    for lim, n in [(1, 0.05), (4, 0.10), (8, 0.20), (16, 0.40)]:
        if dias < lim:
            return n
    return 0.80


def nivel_posicao(v):
    """Nivel da escala mais proximo (empate vai para o nivel maior), para posicionar na matriz."""
    return min(NIVEIS, key=lambda n: (abs(n - v), -n))


def classe(sev):
    return "Alta" if sev >= LIM_ALTA else ("Média" if sev >= LIM_MEDIA else "Baixa")


# riscos ja materializados em 18/11/2026 (R11: materializou em S3 e foi tratado; o p atual e de regressao)
MATERIALIZADOS = {"R01", "R02", "R03", "R04", "R10", "R13", "R15", "R16", "R22"}


def calcula(lista, ameaca=True):
    out = []
    for r in lista:
        d = dict(r)
        taxa = r.get("taxa", TAXA_DEV)
        d["custo_rs"] = r["horas"] * taxa + r["caixa"]
        d["c"] = nivel_custo(d["custo_rs"])
        d["t"] = nivel_tempo(r["dias"])
        imp = [d["c"], d["t"], r["esc"], r["qual"]]
        d["media"] = sum(imp) / 4
        d["max"] = max(imp)
        d["sev"] = r["p"] * d["media"]
        d["sev_max"] = r["p"] * d["max"]
        d["classe"] = classe(d["sev"])
        d["obs"] = d["sev"] >= LIM_ALTA or d["sev_max"] >= LIM_OBS_MAX
        d["emv_rs"] = r["p"] * d["custo_rs"]
        d["emv_dias"] = r["p"] * r["dias"]
        d["resp_rs"] = r["r_horas"] * r["r_taxa"] + r["r_caixa"]
        d["mat"] = r["id"] in MATERIALIZADOS
        d["sev_res"] = r["p_res"] * d["media"]
        d["classe_res"] = classe(d["sev_res"])
        out.append(d)
    if ameaca:
        ordem = sorted(out, key=lambda x: (-round(x["sev"], 6), -round(x["sev_max"], 6), -x["p"], x["id"]))
        for i, d in enumerate(ordem, 1):
            d["rank"] = i
    else:
        ordem = sorted(out, key=lambda x: (-round(x["sev"], 6), x["id"]))
        for i, d in enumerate(ordem, 1):
            d["rank"] = i
    return out


def monte_carlo(ameacas, n=20000, seed=42):
    """Custo extra total (R$): cada risco ocorre com probabilidade p; custo ~ triangular(0,5c; c; 2c)."""
    rng = np.random.default_rng(seed)
    custo = np.zeros(n)
    for r in ameacas:
        ocorre = rng.random(n) < r["p"]
        c = r["custo_rs"]
        custo += ocorre * (rng.triangular(0.5 * c, c, 2.0 * c, n) if c > 0 else np.zeros(n))
    q = lambda p: float(np.percentile(custo, p))
    return dict(n=n, seed=seed, media=float(custo.mean()), p50=q(50), p80=q(80), p90=q(90),
                prob_gt_reserva10=float((custo > RESERVA_10).mean()),
                prob_gt_reservas=float((custo > RESERVA_10 + RESERVA_5).mean()))


AM = calcula(AMEACAS, True)
OP = calcula(OPORTUNIDADES, False)

if __name__ == "__main__":
    print("custo base", CUSTO_BASE, "reserva10", RESERVA_10, "reserva5", RESERVA_5)
    for d in sorted(AM, key=lambda x: x["rank"]):
        print(d["rank"], d["id"], d["nome"][:30], d["p"], d["c"], d["t"], d["esc"], d["qual"], round(d["media"], 4), round(d["sev"], 4), d["classe"], round(d["sev_max"], 3), d["obs"], round(d["custo_rs"]), round(d["emv_rs"]), d["resp_rs"], d["sev_res"].__round__(3))
    print("soma EMV", sum(d["emv_rs"] for d in AM), "soma resp", sum(d["resp_rs"] for d in AM))
    print(monte_carlo([d for d in AM if not d["mat"]]))
    for d in OP:
        print(d["id"], d["rank"], round(d["sev"], 4), d["custo_rs"], d["emv_rs"])
