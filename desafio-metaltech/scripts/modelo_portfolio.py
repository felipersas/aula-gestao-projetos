#!/usr/bin/env python3
"""
Modelo do Desafio MetalTech S.A. (PMO) - fonte unica dos numeros.

Tudo o que aparece em analise-portfolio.md, no slide, no roteiro e no relatorio
sai daqui. Rodar:  python3 modelo_portfolio.py   (imprime verificacoes e grava saida_modelo.json)

Convencao: valores em R$ mil; meses 1..12; T1 = meses 1-3 ... T4 = meses 10-12.
DADO = veio do enunciado. HIPOTESE (H) = premissa do grupo, rotulada nos documentos.
"""
import itertools
import json
import random
from pathlib import Path

AQUI = Path(__file__).resolve().parent

# ---------------------------------------------------------------- DADOS DO ENUNCIADO
ORCAMENTO_TETO = 2500
PROJ = {
    "P1": dict(nome="Automação da Linha 1", inv=900, prazo=6, risco="Alto", ben="+12% produtividade"),
    "P2": dict(nome="Manutenção Preditiva", inv=450, prazo=4, risco="Médio", ben="-20% paradas"),
    "P3": dict(nome="Novo ERP Industrial", inv=1200, prazo=10, risco="Alto", ben="Integração dos processos"),
    "P4": dict(nome="Redução de Refugo", inv=250, prazo=3, risco="Baixo", ben="-25% desperdício"),
    "P5": dict(nome="Controle de Qualidade", inv=350, prazo=4, risco="Médio", ben="-30% retrabalho"),
    "P6": dict(nome="Treinamento de Operadores", inv=150, prazo=2, risco="Baixo", ben="Aumento de produtividade"),
    "P7": dict(nome="Monitoramento IoT", inv=600, prazo=5, risco="Médio", ben="Dados em tempo real"),
    "P8": dict(nome="Expansão da Capacidade", inv=1500, prazo=12, risco="Alto", ben="+20% capacidade"),
}
METAS = {  # objetivo estrategico -> meta numerica (dado do enunciado)
    "Produtividade": 15,
    "Paradas": 20,
    "Custos": 10,
    "Retrabalho": 30,
}
# benefício quantificado (p.p.) e a que meta se refere (DADO); None = nao quantificado no enunciado
BEN_QUANT = {
    "P1": (12, "Produtividade", "p.p. de produtividade"),
    "P2": (20, "Paradas", "p.p. de redução de paradas"),
    "P4": (25, "Desperdício (alimenta Custos)", "p.p. de redução de desperdício"),
    "P5": (30, "Retrabalho", "p.p. de redução de retrabalho"),
    "P8": (20, "Capacidade (fora das 4 metas)", "p.p. de capacidade"),
}

DECISAO = {
    "P1": "Prioridade", "P2": "Prioridade", "P4": "Prioridade", "P5": "Prioridade", "P6": "Prioridade",
    "P7": "Posterior", "P3": "Adiado", "P8": "Adiado",
}
PRIORIZADOS = [p for p, d in DECISAO.items() if d == "Prioridade"]
PROGRAMAS = {
    "A": dict(nome="Excelência Operacional", projetos=["P1", "P2", "P6"], metas=["Produtividade +15%", "Paradas -20%"]),
    "B": dict(nome="Qualidade 4.0 (fase 1)", projetos=["P4", "P5"], metas=["Retrabalho -30%", "Custos -10%"]),
}

# ---------------------------------------------------------------- CRONOGRAMA (meses, inclusive)
JANELA = {  # projeto -> (inicio, fim)
    "P1": (1, 6), "P2": (1, 4), "P4": (1, 3), "P5": (4, 7), "P6": (5, 6),
    "P7": (7, 11),  # condicional ao gate G2 (H)
}
for p, (i, f) in JANELA.items():
    assert f - i + 1 == PROJ[p]["prazo"], p  # duracao confere com o prazo do enunciado

# ---------------------------------------------------------------- MATRIZ DE PRIORIZACAO
CRIT = [  # (chave, nome, peso)
    ("AE", "Alinhamento estratégico", 0.35),
    ("BC", "Relação benefício/custo", 0.20),
    ("RI", "Risco (nota alta = risco baixo)", 0.15),
    ("PR", "Prazo / rapidez de retorno", 0.10),
    ("SI", "Sinergia / dependências", 0.10),
    ("VR", "Viabilidade de recursos", 0.10),
]
assert abs(sum(c[2] for c in CRIT) - 1) < 1e-9
NOTAS = {
    "P1": dict(AE=5, BC=2, RI=1, PR=2, SI=5, VR=2),
    "P2": dict(AE=5, BC=4, RI=3, PR=4, SI=3, VR=3),
    "P3": dict(AE=2, BC=1, RI=1, PR=1, SI=2, VR=1),
    "P4": dict(AE=4, BC=5, RI=5, PR=5, SI=5, VR=4),
    "P5": dict(AE=5, BC=5, RI=3, PR=4, SI=5, VR=4),
    "P6": dict(AE=3, BC=3, RI=5, PR=5, SI=5, VR=5),
    "P7": dict(AE=3, BC=2, RI=3, PR=3, SI=3, VR=2),
    "P8": dict(AE=2, BC=2, RI=1, PR=1, SI=2, VR=1),
}


def custo_por_pp(p):
    if p in BEN_QUANT:
        return PROJ[p]["inv"] / BEN_QUANT[p][0]
    return None


def nota_prazo(m):
    return 5 if m <= 3 else 4 if m == 4 else 3 if m == 5 else 2 if m <= 9 else 1


def nota_risco(r):
    return {"Baixo": 5, "Médio": 3, "Alto": 1}[r]


def nota_bc(p):
    c = custo_por_pp(p)
    if c is not None:
        return 5 if c <= 15 else 4 if c <= 30 else 3 if c <= 60 else 2 if c <= 100 else 1
    inv = PROJ[p]["inv"]
    return 3 if inv <= 150 else 2 if inv <= 600 else 1


# as notas de RI, PR e BC seguem regra objetiva: o script confere que bate com a tabela acima
for p in PROJ:
    assert NOTAS[p]["RI"] == nota_risco(PROJ[p]["risco"]), p
    assert NOTAS[p]["PR"] == nota_prazo(PROJ[p]["prazo"]), p
    assert NOTAS[p]["BC"] == nota_bc(p), (p, nota_bc(p))


def score(p, pesos=None):
    pesos = pesos or {k: w for k, _, w in CRIT}
    return sum(NOTAS[p][k] * pesos[k] for k in pesos)


SCORE = {p: round(score(p), 2) for p in PROJ}
RANK = sorted(PROJ, key=lambda p: -SCORE[p])
TOP5 = set(RANK[:5])
assert TOP5 == set(PRIORIZADOS), (RANK, SCORE)


def sensibilidade():
    base = {k: w for k, _, w in CRIT}
    out = []
    # (a) um criterio por vez +-10 p.p., o restante reescalado proporcionalmente
    for k in base:
        for delta in (-0.10, +0.10):
            novo = dict(base)
            novo[k] = max(0.0, base[k] + delta)
            resto = 1 - novo[k]
            soma_outros = sum(v for kk, v in base.items() if kk != k)
            for kk in base:
                if kk != k:
                    novo[kk] = base[kk] * resto / soma_outros
            r = sorted(PROJ, key=lambda p: -score(p, novo))
            out.append(("%s %+d p.p." % (k, int(delta * 100)), r))
    # (b) perfis alternativos
    perfis = {
        "pesos iguais": {k: 1 / 6 for k in base},
        "foco em custo": dict(AE=0.25, BC=0.35, RI=0.15, PR=0.10, SI=0.05, VR=0.10),
        "foco em risco": dict(AE=0.25, BC=0.15, RI=0.30, PR=0.10, SI=0.10, VR=0.10),
        "foco estratégico": dict(AE=0.50, BC=0.15, RI=0.10, PR=0.05, SI=0.10, VR=0.10),
    }
    for nome, pesos in perfis.items():
        assert abs(sum(pesos.values()) - 1) < 1e-9
        r = sorted(PROJ, key=lambda p: -score(p, pesos))
        out.append((nome, r))
    return out


SENS = sensibilidade()


def monte_carlo(n=20000, seed=42):
    rnd = random.Random(seed)
    base = [w for _, _, w in CRIT]
    keys = [k for k, _, _ in CRIT]
    k = 30  # concentracao: quanto maior, mais perto dos pesos-base
    iguais = 0
    p1_acima_p7 = 0
    for _ in range(n):
        g = [rnd.gammavariate(b * k, 1) for b in base]
        s = sum(g)
        pesos = {kk: x / s for kk, x in zip(keys, g)}
        sc = {p: score(p, pesos) for p in PROJ}
        top = set(sorted(PROJ, key=lambda p: -sc[p])[:5])
        iguais += top == TOP5
        p1_acima_p7 += sc["P1"] > sc["P7"]
    return iguais / n, p1_acima_p7 / n


MC_TOP5, MC_P1_P7 = monte_carlo()

# ---------------------------------------------------------------- CENARIOS
CEN = {
    "A": ["P1", "P2", "P4", "P5", "P6"],
    "B": ["P1", "P2", "P5", "P6", "P7"],
    "C": ["P2", "P4", "P5", "P6", "P7"],
    "D": ["P1", "P8"],
}
COBRE = {  # meta -> projetos com benefício quantificado DIRETO no enunciado (P6, P7 e efeitos indiretos não contam como cobertura)
    "Produtividade": ["P1"],
    "Paradas": ["P2"],
    "Custos": ["P4"],          # -25% desperdício é a única alavanca quantificada ligada a custos (efeitos de P5, P2 e P1 são indiretos)
    "Retrabalho": ["P5"],
}


def avalia_cenario(nome):
    ps = CEN[nome]
    custo = sum(PROJ[p]["inv"] for p in ps)
    cobertas = [m for m, lst in COBRE.items() if any(p in ps for p in lst)]
    diretas = [m for m in ("Produtividade", "Paradas", "Retrabalho") if m in cobertas]
    return dict(
        projetos=ps, custo=custo, pct=round(100 * custo / ORCAMENTO_TETO, 1), reserva=ORCAMENTO_TETO - custo,
        score=round(sum(SCORE[p] for p in ps), 2), metas_cobertas=cobertas,
        n_metas=len(cobertas), n_alto_risco=sum(PROJ[p]["risco"] == "Alto" for p in ps),
        caber=custo <= ORCAMENTO_TETO,
    )


CENARIOS = {k: avalia_cenario(k) for k in CEN}
assert CENARIOS["A"]["custo"] == 2100 and CENARIOS["B"]["custo"] == 2450
assert CENARIOS["C"]["custo"] == 1800 and CENARIOS["D"]["custo"] == 2400
# D' = A + P8 nao cabe
ESTOURO_A_MAIS_P8 = sum(PROJ[p]["inv"] for p in CEN["A"] + ["P8"])  # 3600


def enumera_subconjuntos():
    """todos os 255 subconjuntos viaveis em orcamento e dependencias; ranqueia por soma das notas."""
    res = []
    ids = list(PROJ)
    for r in range(1, len(ids) + 1):
        for ps in itertools.combinations(ids, r):
            custo = sum(PROJ[p]["inv"] for p in ps)
            if custo > ORCAMENTO_TETO:
                continue
            if "P8" in ps and "P1" not in ps:       # recomendação da empresa: P1 antes/junto de P8
                continue
            if "P3" in ps and "P7" not in ps:       # P3 depende de P7 para a etapa de integração (H: tratado como pre-requisito)
                continue
            if "P1" in ps and "P6" not in ps:       # P6 prepara os operadores para o P1 (H: tratado como pre-requisito de adoção)
                continue
            cobre = {m for m, lst in COBRE.items() if any(p in ps for p in lst)}
            res.append(dict(ps=ps, custo=custo, score=round(sum(SCORE[p] for p in ps), 2), metas=len(cobre)))
    return res


SUBS = enumera_subconjuntos()
SUBS_4METAS = [s for s in SUBS if s["metas"] == 4]
MELHOR_COM_RESERVA = max((s for s in SUBS_4METAS if s["custo"] <= ORCAMENTO_TETO * 0.84 + 1e-9), key=lambda s: s["score"])
MELHOR_4METAS_SEM_RESERVA = sorted(SUBS_4METAS, key=lambda s: -s["score"])[:5]
assert set(MELHOR_COM_RESERVA["ps"]) == set(PRIORIZADOS), MELHOR_COM_RESERVA

# ---------------------------------------------------------------- ORCAMENTO
INV_PRIOR = sum(PROJ[p]["inv"] for p in PRIORIZADOS)
RESERVA = ORCAMENTO_TETO - INV_PRIOR
assert INV_PRIOR == 2100 and RESERVA == 400 and INV_PRIOR <= ORCAMENTO_TETO
PROG_CUSTO = {k: sum(PROJ[p]["inv"] for p in v["projetos"]) for k, v in PROGRAMAS.items()}
assert PROG_CUSTO == {"A": 1500, "B": 600}
TOTAL_CARTEIRA = sum(p["inv"] for p in PROJ.values())  # 5400

# desembolso: HIPOTESE - linear ao longo da duração de cada projeto (meses inclusive)


def desembolso_mensal(alt_p1_adiantado=False):
    m = {p: [0.0] * 12 for p in PRIORIZADOS}
    for p in PRIORIZADOS:
        i, f = JANELA[p]
        n = f - i + 1
        for k in range(i, f + 1):
            m[p][k - 1] = PROJ[p]["inv"] / n
    if alt_p1_adiantado:
        # H alternativa: 50% do P1 (pedido de equipamentos) pago nos meses 1-2; 50% linear em 1-6
        m["P1"] = [0.0] * 12
        for k in (1, 2):
            m["P1"][k - 1] += 450 / 2
        for k in range(1, 7):
            m["P1"][k - 1] += 450 / 6
    return m


DESEMB = desembolso_mensal()
DESEMB_ALT = desembolso_mensal(True)
MES_TOTAL = [sum(DESEMB[p][k] for p in PRIORIZADOS) for k in range(12)]
MES_TOTAL_ALT = [sum(DESEMB_ALT[p][k] for p in PRIORIZADOS) for k in range(12)]
TRI = [sum(MES_TOTAL[3 * t:3 * t + 3]) for t in range(4)]
TRI_ALT = [sum(MES_TOTAL_ALT[3 * t:3 * t + 3]) for t in range(4)]
assert abs(sum(MES_TOTAL) - 2100) < 1e-6 and abs(sum(MES_TOTAL_ALT) - 2100) < 1e-6
TRI_PROG = {g: [sum(DESEMB[p][3 * t + j] for p in v["projetos"] for j in range(3)) for t in range(4)]
            for g, v in PROGRAMAS.items()}
TRI_PROJ = {p: [sum(DESEMB[p][3 * t:3 * t + 3]) for t in range(4)] for p in PRIORIZADOS}
ACUM = list(itertools.accumulate(MES_TOTAL))

# reserva gerencial: composicao (H)
RESERVA_COMP = [
    ("Contingência P1 (20% de R$ 900 mil; risco alto)", 180),
    ("Contingência P2 (20% de R$ 450 mil; risco médio)", 90),
    ("Contingência P4, P5 e P6 (10% de R$ 750 mil)", 75),
    ("Analista de planejamento externo, 4 meses (gatilho do GP)", 55),
]
assert sum(v for _, v in RESERVA_COMP) == RESERVA

# composicao por categoria de aquisição (H, a validar nas cotações)
CATS = {
    "A": "Equipamentos de automação e inspeção",
    "B": "Sensores e instrumentação",
    "C": "Consultoria de integração e engenharia",
    "D": "Treinamento",
    "E": "Software e licenças",
    "F": "Instalação, infraestrutura e adequações",
}
COMP = {
    "P1": dict(A=500, C=180, F=150, E=70),
    "P2": dict(B=170, E=110, C=100, F=70),
    "P4": dict(C=100, B=80, D=40, F=30),
    "P5": dict(A=200, E=70, C=40, D=40),
    "P6": dict(D=150),
}
for p, d in COMP.items():
    assert sum(d.values()) == PROJ[p]["inv"], p
CAT_TOTAL = {c: sum(COMP[p].get(c, 0) for p in COMP) for c in CATS}
assert sum(CAT_TOTAL.values()) == 2100

# ---------------------------------------------------------------- RECURSOS (matriz carga % por mes)
RECS = ["EA1", "EA2", "TI1", "TI2", "QUAL", "MAN", "GP"]
REC_NOME = {
    "EA1": "Engenheiro de automação 1", "EA2": "Engenheiro de automação 2",
    "TI1": "Analista de TI 1", "TI2": "Analista de TI 2",
    "QUAL": "Especialista em qualidade", "MAN": "Especialista em manutenção", "GP": "Gerente de projetos",
}
# (recurso, atividade, inicio, fim, %)  -- plano ADOTADO
ALOC = [
    ("EA1", "P1", 1, 6, 100), ("EA1", "Operação assistida P1", 7, 9, 30),
    ("EA2", "P1", 1, 4, 90), ("EA2", "P2 (consultivo ≤ 4 h/sem)", 1, 4, 10), ("EA2", "P1", 5, 6, 100),
    ("EA2", "Operação assistida P1", 7, 9, 30),
    ("TI1", "P2", 1, 4, 70), ("TI1", "P1", 3, 6, 30), ("TI1", "Sustentação P1/P2", 7, 12, 30),
    ("TI2", "P4", 1, 3, 20), ("TI2", "P5", 4, 7, 50), ("TI2", "Sustentação P5", 8, 12, 20),
    ("QUAL", "P4", 1, 3, 100), ("QUAL", "P5", 4, 7, 100), ("QUAL", "Medição de benefícios", 8, 12, 40),
    ("MAN", "P2", 1, 4, 100), ("MAN", "P6", 5, 6, 20), ("MAN", "Sustentação P2", 7, 12, 30),
]
# sobreposicao condicional: P7, se o gate G2 aprovar (m7-m11)
ALOC_P7 = [("EA1", "P7", 7, 11, 40), ("TI1", "P7", 7, 11, 50), ("TI2", "P7", 7, 11, 30)]

# GP: modelo de demanda (H). Esforço de gestão por projeto ativo: mês de partida 35%, execução 25%, encerramento 30%;
# governança do portfólio 10%; operação assistida/medição 15% após o m7. Com coordenadores locais: 70% do esforço de projeto.
GP_PART, GP_EXEC, GP_ENC, GP_GOV, GP_POS, GP_COORD = 35, 25, 30, 10, 15, 0.70


def gp_carga(janelas, coord=True, pos=True):
    cargas = [0.0] * 12
    for m in range(1, 13):
        esf = 0.0
        for p, (i, f) in janelas.items():
            if i <= m <= f:
                esf += GP_PART if m == i else GP_ENC if m == f else GP_EXEC
        cargas[m - 1] = esf * (GP_COORD if coord else 1) + GP_GOV + (GP_POS if (pos and m >= 7) else 0)
    return cargas


JAN_A = {p: JANELA[p] for p in PRIORIZADOS}
JAN_A7 = dict(JAN_A, P7=JANELA["P7"])
GP_SEM_COORD = gp_carga(JAN_A, coord=False)
GP_COM_COORD = gp_carga(JAN_A, coord=True)
GP_COM_COORD_P7 = gp_carga(JAN_A7, coord=True)
# cenario ingenuo: todos os 5 projetos priorizados partem no mês 1, cada um com sua duração
JAN_ING = {p: (1, PROJ[p]["prazo"]) for p in PRIORIZADOS}
GP_ING = gp_carga(JAN_ING, coord=False, pos=False)


def matriz(aloc, extra=None):
    m = {r: [0] * 12 for r in RECS if r != "GP"}
    for r, _, i, f, pct in aloc + (extra or []):
        for k in range(i, f + 1):
            m[r][k - 1] += pct
    return m


MAT = matriz(ALOC)
MAT["GP"] = [round(x) for x in GP_COM_COORD]
MAT_P7 = matriz(ALOC, ALOC_P7)
MAT_P7["GP"] = [round(x) for x in GP_COM_COORD_P7]

# cenario ingênuo (sem as decisões): todos partem no m1; P2 usa EA 50% (instrumentação), P6 começa no m1, P5 no m1
ALOC_ING = [
    ("EA1", "P1", 1, 6, 100), ("EA2", "P1", 1, 6, 100), ("EA1", "P2 instrumentação", 1, 4, 50),
    ("TI1", "P2", 1, 4, 70), ("TI1", "P1", 1, 6, 30), ("TI2", "P4", 1, 3, 20), ("TI2", "P5", 1, 4, 50),
    ("QUAL", "P4", 1, 3, 100), ("QUAL", "P5", 1, 4, 100),
    ("MAN", "P2", 1, 4, 100), ("MAN", "P6", 1, 2, 20),
]
MAT_ING = matriz(ALOC_ING)
MAT_ING["GP"] = [round(x) for x in GP_ING]

# checagem literal do plano adotado SEM absorver o consultivo do EA2 (P1=100 + P2=10) -> 110%
EA2_LITERAL = [100 + 10 if 1 <= m <= 4 else 100 if m <= 6 else 0 for m in range(1, 13)]


def conflitos(mat, limite=100):
    out = []
    for r, v in mat.items():
        for k, x in enumerate(v, 1):
            if x > limite:
                out.append((r, k, x))
    return out


CONF_ING = conflitos(MAT_ING)
CONF_ADOT = conflitos(MAT)
CONF_ADOT_P7 = conflitos(MAT_P7)
assert not CONF_ADOT and not CONF_ADOT_P7, (CONF_ADOT, CONF_ADOT_P7)
assert max(GP_SEM_COORD) > 100  # o pico existe sem a mitigacao
PICO = {r: max(v) for r, v in MAT.items()}
PICO_MES = {r: [k + 1 for k, x in enumerate(v) if x == max(v)] for r, v in MAT.items()}

# ---------------------------------------------------------------- RISCOS
PROB = {0.1: "Muito baixa", 0.3: "Baixa", 0.5: "Média", 0.7: "Alta", 0.9: "Muito alta"}
IMP = {0.05: "Muito baixo", 0.10: "Baixo", 0.20: "Moderado", 0.40: "Alto", 0.80: "Muito alto"}
# (id, titulo, causa, risco, consequencia, prob, impacto, tipo_impacto, resposta, estrategia, dono, gatilho)
RISCOS = [
    ("R01", "Atraso ou estouro no P1",
     "Projeto de risco alto, equipamentos importados e integração com a linha existente",
     "o P1 atrasar ou custar mais que os R$ 900 mil",
     "perda do +12% de produtividade, atraso do P6 e consumo da reserva",
     0.5, 0.40, "Tempo/Custo",
     "Reserva de R$ 180 mil dedicada ao P1; FAT como gate do P6; contrato com marcos de pagamento e multa por atraso; G1 (fim do m3) valida pedido de equipamentos",
     "Mitigar", "GP + EA1", "SPI < 0,90 ou pedido de equipamentos não emitido até o m2"),
    ("R02", "GP como ponto único de falha",
     "Um único gerente de projetos para 3 projetos simultâneos nos m1-m4 (demanda de 115% no m1 sem mitigação)",
     "sobrecarga ou ausência do GP",
     "decisões e riscos sem acompanhamento nos três projetos, atrasos em cascata",
     0.5, 0.40, "Tempo",
     "Coordenadores locais por projeto; rito semanal de 30 min; analista de planejamento externo (R$ 55 mil da reserva) se carga > 90% em 2 meses seguidos",
     "Mitigar", "Diretoria (patrocinador)", "carga do GP > 90% por 2 meses"),
    ("R03", "Benefício parcial e metas sem folga",
     "P2 e P5 entregam exatamente -20% e -30%; P1 entrega 12 dos 15 p.p. de produtividade",
     "os benefícios se realizarem em menos de 100% do prometido",
     "metas de paradas, retrabalho e produtividade ficam abaixo do alvo no balanço do m12",
     0.7, 0.40, "Escopo",
     "Linha de base no m1; meta interna 10% acima do alvo; aceite condicionado a indicador; medição mensal e balanço no m9 e m12",
     "Mitigar", "PMO + Controladoria", "indicador < 90% da trajetória no m9"),
    ("R04", "Baixa adoção pelos operadores",
     "Mudança de rotina na Linha 1 e receio de perda de função",
     "os operadores resistirem ou não dominarem o novo equipamento",
     "ganho de produtividade abaixo do previsto e paradas por erro de operação",
     0.5, 0.20, "Qualidade",
     "P6 como pré-requisito de operação; operadores-chave no FAT; comunicação do porquê da mudança; turmas por turno",
     "Mitigar", "Gerente de produção", "avaliação de competência < 80%"),
    ("R05", "P2 sem dados de IoT",
     "P7 adiado: sem monitoramento em tempo real, os dados para os modelos preditivos são escassos",
     "os modelos preditivos terem baixa precisão",
     "alertas falsos ou tardios e meta de -20% de paradas em risco",
     0.5, 0.20, "Qualidade",
     "Escopo mínimo de aquisição de dados dentro do P2 (sensores nos ativos críticos); piloto em 3 ativos antes de expandir",
     "Mitigar", "MAN + TI1", "recall do modelo < 70% no piloto"),
    ("R06", "Prazo de entrega de equipamentos",
     "Fornecedores com prazo de fabricação e importação longos",
     "os equipamentos do P1 não chegarem a tempo para o FAT no m4",
     "deslocamento do FAT, do P6 e do G2",
     0.5, 0.20, "Tempo",
     "Cotação com prazo como critério (25%); pedido até o m2; prazo contratual com multa; fornecedor alternativo qualificado",
     "Mitigar", "EA1 + Compras", "pedido não emitido até o m2"),
    ("R07", "Dependência de poucos especialistas",
     "Cada especialista (EA, QUAL, MAN) é único ou está em 100% de dedicação",
     "afastamento ou saída de um especialista",
     "paralisação do projeto que depende dele",
     0.3, 0.40, "Tempo",
     "Documentação semanal; par técnico (EA1/EA2 e TI1/TI2 como backups); cláusula de suporte do fornecedor",
     "Mitigar", "GP", "afastamento > 5 dias úteis"),
    ("R08", "Atraso do P6 por efeito cascata",
     "P6 só começa após o FAT do P1",
     "o P6 atrasar quando o FAT atrasar",
     "operadores sem treinamento no go-live do P1",
     0.5, 0.10, "Tempo",
     "Conteúdo pré-montado pelo fornecedor do P1; treinamento em duas ondas; trilha alternativa em simulador",
     "Mitigar", "GP + RH", "FAT atrasa mais de 2 semanas"),
    ("R09", "TI1 sem folga no m3-m4",
     "TI1 em 70% (P2) + 30% (P1) = 100% no pico",
     "qualquer demanda extra deslocar o P1 ou o P2",
     "atraso na integração de dados do P2 ou do P1",
     0.3, 0.20, "Tempo",
     "Proibir demandas fora do portfólio no m3-m4; TI2 como backup (carga de 20%); aceitar o uso da reserva para apoio externo pontual",
     "Mitigar", "GP", "carga do TI1 > 100% em qualquer semana"),
    ("R10", "Linha de base inexistente ou contestada",
     "Os indicadores atuais de paradas, retrabalho e produtividade não são medidos de forma padronizada",
     "o balanço de benefícios ser contestado",
     "disputa sobre o resultado e dificuldade de liberar o P7 no G2",
     0.3, 0.40, "Escopo",
     "Linha de base aprovada pela Controladoria até o fim do m1; definições de indicador no relatório; auditoria no m9",
     "Evitar", "PMO + Controladoria", "linha de base não aprovada no m1"),
    ("R11", "Integração do P1 com sistemas existentes",
     "Linha 1 com CLPs e sistemas legados sem documentação",
     "a integração entre o novo equipamento e a base instalada falhar",
     "retrabalho de engenharia e atraso no comissionamento",
     0.5, 0.20, "Tempo",
     "Levantamento do legado no m1; consultoria de integração contratada com escopo e aceite; testes de integração no FAT",
     "Mitigar", "EA2 + TI1", "falha no teste de integração do FAT"),
    ("R12", "Parada não planejada na instalação do P1",
     "Instalação e comissionamento exigem intervenção na Linha 1 em operação",
     "a instalação provocar paradas de produção",
     "piora temporária da meta de paradas e perda de produção",
     0.3, 0.40, "Escopo",
     "Instalação em paradas programadas; plano de retorno (rollback); ensaio a seco no FAT",
     "Mitigar", "Gerente de produção + EA1", "parada não programada > 4 h"),
    ("R13", "Reserva insuficiente para o P7 no G2",
     "O P7 custa R$ 600 mil e a reserva é de R$ 400 mil (já comprometida em parte)",
     "não haver recurso para iniciar o P7 no G2",
     "fase 2 do Programa B fica para o ciclo seguinte",
     0.9, 0.05, "Escopo",
     "Aceitar: critério do G2 prevê escopo faseado (fase 1 ≤ saldo da reserva) ou complemento aprovado pela diretoria",
     "Aceitar", "Diretoria", "no G2"),
    ("R14", "Pressão para antecipar P3, P7 ou P8",
     "Áreas usuárias querem o ERP ou a expansão já neste ciclo",
     "a diretoria incluir projetos fora do portfólio sem rever o orçamento",
     "recursos escassos pulverizados e perda de foco nas metas",
     0.3, 0.20, "Escopo",
     "Critérios objetivos do G2; ata do portfólio com projetos adiados e condições de retorno; mudança só pelo comitê",
     "Evitar", "PMO", "pedido formal de inclusão"),
]
RISCOS_DADOS = []
for r in RISCOS:
    (rid, tit, causa, risco, cons, p, i, tipo, resp, est, dono, gat) = r
    assert p in PROB and i in IMP, rid
    RISCOS_DADOS.append(dict(id=rid, titulo=tit, causa=causa, risco=risco, consequencia=cons, prob=p, imp=i,
                             tipo=tipo, sev=round(p * i, 3), resposta=resp, estrategia=est, dono=dono, gatilho=gat))
RISCOS_DADOS.sort(key=lambda x: (-x["sev"], x["id"]))
for k, r in enumerate(RISCOS_DADOS, 1):
    r["rank"] = k


def zona(sev):
    return "Alta" if sev >= 0.18 else "Média" if sev >= 0.06 else "Baixa"


for r in RISCOS_DADOS:
    r["zona"] = zona(r["sev"])
assert len(RISCOS_DADOS) >= 10

# EMV (H) do impacto de custo para checar a reserva: P(estouro) x estouro esperado
EMV = [
    ("P1: P = 0,5 x 30% de R$ 900 mil (faixa 20-40%)", 0.5 * 0.30 * 900),
    ("P2: P = 0,3 x 20% de R$ 450 mil", 0.3 * 0.20 * 450),
    ("P4, P5, P6: P = 0,3 x 10% de R$ 750 mil", 0.3 * 0.10 * 750),
    ("Analista de planejamento: P = 0,5 x R$ 55 mil", 0.5 * 55),
]
EMV_TOTAL = sum(v for _, v in EMV)

# ---------------------------------------------------------------- METAS x BENEFICIO
PRODUT_FALTA = METAS["Produtividade"] - BEN_QUANT["P1"][0]  # 3 p.p.
REAL = [1.0, 0.9, 0.8, 0.7]
SENS_BEN = []
for r in REAL:
    SENS_BEN.append(dict(r=r, prod=BEN_QUANT["P1"][0] * r, par=BEN_QUANT["P2"][0] * r, ret=BEN_QUANT["P5"][0] * r,
                         prod_falta=METAS["Produtividade"] - BEN_QUANT["P1"][0] * r))
# sensibilidade ilustrativa (H) do meta de custos: pesos no custo operacional e efeitos
CUSTO_H = dict(refugo=8.0, retrabalho=6.0, paradas=10.0)  # % do custo operacional (H)
CUSTO_CONTR = dict(
    refugo=CUSTO_H["refugo"] * 0.25, retrabalho=CUSTO_H["retrabalho"] * 0.30, paradas=CUSTO_H["paradas"] * 0.20)
CUSTO_SOMA = sum(CUSTO_CONTR.values())  # 5.8 p.p.
CUSTO_RESTO = METAS["Custos"] - CUSTO_SOMA
GANHO_UNIT_12 = 100 * (1 - 1 / 1.12)
CUSTO_FRACAO_NEC_12 = 100 * CUSTO_RESTO / GANHO_UNIT_12  # parcela do custo sensivel a produtividade

# ---------------------------------------------------------------- ROADMAP / MARCOS
MARCOS = [
    ("M1", "Linha de base de indicadores aprovada", 1),
    ("G1", "Gate 1: pedido de equipamentos do P1 emitido e P4 encerrado", 3),
    ("FAT", "FAT do P1 aprovado (gatilho do P6)", 4),
    ("G2", "Gate 2: decide o P7", 6),
    ("GL", "Go-live do P1 e aceite do P6", 6),
    ("M9", "Balanço parcial de benefícios", 9),
    ("M12", "Balanço final de benefícios e proposta do ciclo 2027", 12),
]

# ---------------------------------------------------------------- VERIFICACOES / SAIDA
def main():
    print("== Matriz de priorizacao")
    for p in RANK:
        print(p, SCORE[p], DECISAO[p], NOTAS[p])
    print("TOP5 == priorizados:", TOP5 == set(PRIORIZADOS))
    print("Margem P1 x P7:", round(SCORE["P1"] - SCORE["P7"], 2))
    print("== Sensibilidade (top-5 igual?)")
    for nome, r in SENS:
        print("%-18s top5=%s  rank=%s" % (nome, set(r[:5]) == TOP5, ",".join(r)))
    print("Monte Carlo: P(top5 igual) = %.3f ; P(P1>P7) = %.3f" % (MC_TOP5, MC_P1_P7))
    print("== Cenarios")
    for k, v in CENARIOS.items():
        print(k, v)
    print("A + P8 =", ESTOURO_A_MAIS_P8)
    print("Melhor subconjunto 4 metas c/ reserva>=16%:", MELHOR_COM_RESERVA)
    print("Top-5 subconjuntos 4 metas (qualquer reserva):")
    for s in MELHOR_4METAS_SEM_RESERVA:
        print("  ", s)
    print("== Orcamento: priorizados", INV_PRIOR, "reserva", RESERVA, "total", INV_PRIOR + RESERVA, "teto", ORCAMENTO_TETO)
    print("Programas:", PROG_CUSTO, "carteira total:", TOTAL_CARTEIRA)
    print("Trimestres:", [round(x, 1) for x in TRI], "alt:", [round(x, 1) for x in TRI_ALT])
    print("Mensal:", [round(x, 1) for x in MES_TOTAL])
    print("Acumulado:", [round(x, 1) for x in ACUM])
    print("Trimestre por programa:", {k: [round(x, 1) for x in v] for k, v in TRI_PROG.items()})
    print("Categorias:", CAT_TOTAL)
    print("== Recursos (adotado)")
    for r in RECS:
        print("%-5s" % r, MAT[r], "pico", PICO[r], "meses", PICO_MES[r])
    print("GP sem coordenadores:", [round(x) for x in GP_SEM_COORD])
    print("GP com coordenadores:", [round(x, 1) for x in GP_COM_COORD], "| com P7:", [round(x, 1) for x in GP_COM_COORD_P7])
    print("EA2 literal (sem absorver consultivo):", EA2_LITERAL)
    print("Conflitos cenario ingenuo:", CONF_ING)
    print("Conflitos adotado:", CONF_ADOT, "| com P7:", CONF_ADOT_P7)
    print("MAT_P7:", {r: MAT_P7[r] for r in RECS})
    print("== Riscos")
    for r in RISCOS_DADOS:
        print(r["rank"], r["id"], r["prob"], r["imp"], r["sev"], r["zona"], r["titulo"])
    print("EMV total:", EMV_TOTAL, [(a, round(b, 1)) for a, b in EMV])
    print("== Metas")
    for s in SENS_BEN:
        print(s)
    print("Custos (H):", CUSTO_CONTR, "soma", CUSTO_SOMA, "resto", CUSTO_RESTO, "fracao necessaria (12%)", round(CUSTO_FRACAO_NEC_12, 1))
    print("Custo por p.p.:", {p: round(custo_por_pp(p), 1) for p in BEN_QUANT})
    # saida JSON para os demais geradores
    out = dict(
        score=SCORE, rank=RANK, notas=NOTAS, tri=TRI, tri_alt=TRI_ALT, mes=MES_TOTAL, acum=ACUM,
        mat=MAT, mat_p7=MAT_P7, mat_ing=MAT_ING, gp_sem=GP_SEM_COORD, gp_com=GP_COM_COORD,
        pico=PICO, cenarios=CENARIOS, mc=[MC_TOP5, MC_P1_P7], emv=EMV_TOTAL,
        riscos=RISCOS_DADOS, tri_prog=TRI_PROG, tri_proj=TRI_PROJ, cat_total=CAT_TOTAL,
    )
    (AQUI / "saida_modelo.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
