import re
import io
import html
import unicodedata
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Comercial Autobrás", layout="wide")


st.markdown("""
<style>

/* BOTÃO DOWNLOAD PDF - compacto e discreto */
div.stDownloadButton {
    display: inline-block !important;
    width: auto !important;
    margin-top: 0.35rem !important;
    margin-bottom: 0.75rem !important;
}

div.stDownloadButton > button {
    background: linear-gradient(90deg, #ff4b4b, #ff7a00) !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.55rem 1.05rem !important;
    font-size: 0.88rem !important;
    min-height: 38px !important;
    width: auto !important;
    box-shadow: 0px 3px 9px rgba(0,0,0,0.18) !important;
    transition: all 0.20s ease-in-out !important;
}

div.stDownloadButton > button:hover {
    transform: translateY(-1px);
    background: linear-gradient(90deg, #ff2d2d, #ff5e00) !important;
    color: #ffffff !important;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.22) !important;
}

div.stDownloadButton > button:focus {
    outline: none !important;
    border: none !important;
    box-shadow: 0px 3px 9px rgba(0,0,0,0.18) !important;
}

/* Evita que o texto interno force largura total */
div.stDownloadButton > button p {
    color: white !important;
    font-weight: 700 !important;
    margin: 0 !important;
    white-space: nowrap !important;
}



/* ===== VISUAL AUTOBRÁS ===== */
.block-container {
    padding-top: 1.1rem !important;
    padding-bottom: 3rem !important;
    max-width: 1550px !important;
}

[data-testid="stSidebar"] {
    background: #F7FAFC;
}

.autobras-cover {
    min-height: 86vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 28px 12px;
}

.autobras-hero {
    width: 100%;
    border-radius: 34px;
    padding: 54px 52px;
    background:
        radial-gradient(circle at top right, rgba(47,128,237,.26), transparent 28%),
        linear-gradient(135deg, #071827 0%, #0B1F33 38%, #123E68 72%, #2F80ED 100%);
    color: white;
    box-shadow: 0 28px 70px rgba(7,24,39,.28);
    position: relative;
    overflow: hidden;
}

.autobras-hero::after {
    content: "";
    position: absolute;
    right: -80px;
    bottom: -100px;
    width: 320px;
    height: 320px;
    border-radius: 999px;
    background: rgba(255,255,255,.10);
}

.autobras-tag {
    display: inline-flex;
    gap: 8px;
    align-items: center;
    border: 1px solid rgba(255,255,255,.28);
    background: rgba(255,255,255,.10);
    color: #EAF2FF;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .04em;
    text-transform: uppercase;
}

.autobras-title {
    font-size: clamp(42px, 6vw, 76px);
    line-height: .96;
    margin: 22px 0 18px 0;
    font-weight: 900;
    letter-spacing: -0.055em;
    color: #FFFFFF !important;
}

.autobras-subtitle {
    max-width: 860px;
    color: #EAF2FF;
    font-size: 19px;
    line-height: 1.6;
    margin-bottom: 28px;
}

.autobras-cards {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin-top: 30px;
    position: relative;
    z-index: 2;
}

.autobras-card {
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 22px;
    padding: 18px;
    backdrop-filter: blur(8px);
}

.autobras-card strong {
    display: block;
    color: white;
    font-size: 20px;
    margin-bottom: 6px;
}

.autobras-card span {
    color: #D7E8FF;
    font-size: 13px;
    line-height: 1.4;
}

.autobras-topbar {
    padding: 18px 22px;
    border-radius: 22px;
    background: linear-gradient(90deg, #071827, #123E68, #2F80ED);
    color: white;
    margin-bottom: 22px;
    box-shadow: 0 12px 30px rgba(18,62,104,.20);
}

.autobras-topbar h1 {
    color: white !important;
    margin: 0;
    font-size: 30px;
    letter-spacing: -0.03em;
}

.autobras-topbar p {
    margin: 6px 0 0 0;
    color: #EAF2FF;
}

@media (max-width: 900px) {
    .autobras-cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .autobras-hero { padding: 38px 28px; }
}



/* ===== ACABAMENTO EXECUTIVO ===== */
[data-testid="stMetric"] {
    background: #FFFFFF; border: 1px solid #E6ECF2; border-radius: 16px;
    padding: 16px 18px; box-shadow: 0 5px 16px rgba(7,24,39,.06);
}
[data-testid="stMetricLabel"] { color:#617286 !important; font-weight:700; }
[data-testid="stMetricValue"] { color:#0B1F33 !important; font-weight:800; letter-spacing:-.03em; }
[data-testid="stMetricDelta"] { font-weight:700; }
[data-testid="stDataFrame"] { border:1px solid #E6ECF2; border-radius:14px; overflow:hidden; }
[data-testid="stTabs"] button { font-weight:800 !important; }
.section-title {font-size:22px;font-weight:850;color:#0B1F33;margin:12px 0 2px 0;}
.section-subtitle {font-size:13px;color:#718096;margin:0 0 14px 0;}
.period-chip {display:inline-block;background:#EEF5FF;color:#123E68;border:1px solid #D7E8FF;border-radius:999px;padding:6px 11px;font-size:12px;font-weight:700;}

</style>

""", unsafe_allow_html=True)


# =============================
# CONFIG
# =============================
ARQUIVO_EXCEL = "base.xlsx"
MESES_PT = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
MESES_LONG = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5, "junho": 6,
    "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
}

# A partir de agosto/2026, arquivos mensais no repositório passam a complementar/substituir
# apenas o mês correspondente da base histórica. Exemplos: AGOSTO 2026.xlsx, SETEMBRO 2026.xlsx.
INICIO_ARQUIVOS_MENSAIS = pd.Timestamp(2026, 8, 1)
MESES_ARQUIVO = {
    "JANEIRO": 1, "FEVEREIRO": 2, "MARCO": 3, "ABRIL": 4, "MAIO": 5, "JUNHO": 6,
    "JULHO": 7, "AGOSTO": 8, "SETEMBRO": 9, "OUTUBRO": 10, "NOVEMBRO": 11, "DEZEMBRO": 12,
}

# Faturamento 2024 (fornecido por você) — usado quando o ano anterior não existir na base e for 2024
FAT_2024_MES = {
    1: 421_375.43,
    2: 478_839.00,
    3: 514_630.18,
    4: 491_583.50,
    5: 561_725.99,
    6: 440_306.20,
    7: 360_277.10,
    8: 339_108.52,
    9: 480_860.64,
    10: 557_455.19,
    11: 515_291.01,
    12: 629_538.77,
}

# =============================
# HELPERS
# =============================
def normalize_col(s: str) -> str:
    s = str(s).strip()
    s = re.sub(r"\s+", " ", s)
    return s


def normalize_product_key(v) -> str:
    """Normaliza nomes de produtos para cruzamentos mais seguros entre abas."""
    if v is None or pd.isna(v):
        return ""
    s = unicodedata.normalize("NFKD", str(v))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.upper().strip()
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_brl_number(v):
    """Converte número BR (1.234,56) / textos / floats em float."""
    if v is None:
        return 0.0
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)

    s = str(v).strip()
    if s == "" or s.lower() in {"nan", "none", "null"}:
        return 0.0

    s = s.replace("\u00a0", " ")
    s = s.replace("R$", "").replace(" ", "")

    # Padrão BR: 1.234,56
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except Exception:
        return 0.0


def format_brl(v: float) -> str:
    try:
        return f"{float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "—"


def safe_to_datetime(series):
    return pd.to_datetime(series, errors="coerce", dayfirst=True)


def pct_br(x: float) -> str:
    try:
        return f"{x*100:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "—"


def _to_ascii_lower(s: str) -> str:
    s = str(s).strip().lower()
    s = s.replace("ç", "c").replace("ã", "a").replace("á", "a").replace("à", "a").replace("â", "a")
    s = s.replace("é", "e").replace("ê", "e").replace("í", "i").replace("ó", "o").replace("ô", "o")
    s = s.replace("ú", "u")
    return s


def parse_mes_to_num(v):
    """
    Tenta extrair MES_NUM (1..12) de:
    - 1..12
    - 'jan', 'fev', ...
    - 'janeiro', ...
    - '01/2026', '2026-01', etc. (pega o mês)
    Retorna int ou None.
    """
    if v is None:
        return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        n = int(v)
        return n if 1 <= n <= 12 else None

    s = str(v).strip()
    if s == "" or s.lower() in {"nan", "none", "null"}:
        return None

    s_low = _to_ascii_lower(s)

    # abreviado (jan, fev...)
    for i, abv in enumerate(MESES_PT, start=1):
        if s_low == abv:
            return i

    # mês por extenso
    if s_low in MESES_LONG:
        return MESES_LONG[s_low]

    # tenta extrair algo tipo mm/aaaa, aaaa-mm, etc.
    m = re.search(r"(?<!\d)(0?[1-9]|1[0-2])(?!\d)", s_low)
    if m:
        n = int(m.group(1))
        return n if 1 <= n <= 12 else None

    return None


def normalize_text_key(v) -> str:
    """Normaliza textos para cruzamentos robustos (cliente, arquivo, categoria etc.)."""
    if v is None or pd.isna(v):
        return ""
    s = unicodedata.normalize("NFKD", str(v))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.upper().strip()
    s = re.sub(r"\s+", " ", s)
    return s


def classificar_cliente(v) -> str:
    """Converte classificação vazia/tracejada em SEM CLASSIFICAÇÃO."""
    s = "" if v is None or pd.isna(v) else str(v).strip()
    if not s or re.fullmatch(r"[-–—_\s]+", s):
        return "SEM CLASSIFICAÇÃO"
    return s


def normalizar_classificacao_cliente(v) -> str:
    """Consolida grafias equivalentes da classificação de clientes."""
    s_original = classificar_cliente(v)
    if s_original == "SEM CLASSIFICAÇÃO":
        return s_original

    chave = normalize_text_key(s_original)
    chave = re.sub(r"[^A-Z0-9]+", " ", chave)
    chave = re.sub(r"\s+", " ", chave).strip()

    # Consolida variações de Empresa COM máquina: acento, abreviações e pequenas diferenças de escrita.
    if re.search(r"\b(COM|C)\b.*\bMAQUINA\b", chave) or re.search(r"\bEMPRESA\b.*\bC\s*MAQUINA\b", chave):
        return "Empresa com máquina"

    # Consolida variações de Empresa SEM máquina: acento, 's/ máquina' e pequenas diferenças de escrita.
    if re.search(r"\b(SEM|S)\b.*\bMAQUINA\b", chave) or re.search(r"\bEMPRESA\b.*\bS\s*MAQUINA\b", chave):
        return "Empresa sem máquina"

    # Para as demais classificações, remove diferenças apenas de caixa/espaçamento/acentuação
    # usando a primeira grafia padronizada por chave no tratamento posterior.
    return s_original.strip()


def localizar_arquivo_cadastro_clientes(pasta: Path) -> Path | None:
    """Localiza cadastro externo de clientes no repositório, sem depender de caixa/acentos."""
    candidatos = []
    for arq in pasta.glob("*.xlsx"):
        stem = normalize_text_key(arq.stem)
        if (("CADASTRO" in stem and "CLIENT" in stem) or ("RELATORIO" in stem and "CLIENT" in stem)):
            candidatos.append(arq)
    return sorted(candidatos, key=lambda x: x.name)[0] if candidatos else None


def carregar_cadastro_clientes_externo(pasta: Path) -> pd.DataFrame:
    """Lê o cadastro externo. Aceita arquivo CADASTRO DE CLIENTES.xlsx ou equivalente."""
    arq = localizar_arquivo_cadastro_clientes(pasta)
    if arq is None:
        return pd.DataFrame(columns=["CLIENTE_KEY", "UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD", "CLASSIFICACAO_CAD", "ORIGEM_MATCH"])

    # O relatório exportado possui uma linha de título antes do cabeçalho real.
    tentativas = [1, 0]
    d = None
    for header in tentativas:
        try:
            teste = pd.read_excel(arq, header=header)
            teste.columns = [normalize_col(c) for c in teste.columns]
            if "Nome/Razão social" in teste.columns or "Nome/Razao social" in teste.columns:
                d = teste
                break
        except Exception:
            pass
    if d is None:
        return pd.DataFrame(columns=["CLIENTE_KEY", "UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD", "CLASSIFICACAO_CAD", "ORIGEM_MATCH"])

    nome_col = "Nome/Razão social" if "Nome/Razão social" in d.columns else "Nome/Razao social"
    fantasia_col = None
    for candidato in ["Nome/Nome Fantasia", "Nome Fantasia", "Nome fantasia"]:
        if candidato in d.columns:
            fantasia_col = candidato
            break

    # Mantém os dois identificadores do cadastro. A Razão Social é sempre a chave prioritária;
    # o Nome Fantasia funciona somente como fallback quando a venda não encontra a Razão Social.
    for origem in [nome_col, "Estado", "Cidade", "Bairro", "CATEGORIA"]:
        if origem not in d.columns:
            d[origem] = ""
    if fantasia_col is None:
        fantasia_col = "__NOME_FANTASIA__"
        d[fantasia_col] = ""

    cad = pd.DataFrame({
        "RAZAO_SOCIAL": d[nome_col],
        "NOME_FANTASIA": d[fantasia_col],
        "UF_CAD": d["Estado"],
        "LOCALIZACAO_CAD": d["Cidade"],
        "BAIRRO_CAD": d["Bairro"],
        "CLASSIFICACAO_CAD": d["CATEGORIA"],
    })

    for c in ["UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD"]:
        cad[c] = cad[c].fillna("").astype(str).str.strip()
        cad.loc[cad[c].apply(lambda x: bool(re.fullmatch(r"[-–—_\s]+", x)) if x else False), c] = ""
    cad["CLASSIFICACAO_CAD"] = cad["CLASSIFICACAO_CAD"].apply(classificar_cliente)

    # Cria um índice único de aliases. Razão Social recebe prioridade 0 e Nome Fantasia prioridade 1.
    # Assim, se um texto existir simultaneamente como razão social e fantasia de cadastros distintos,
    # prevalece a correspondência exata pela Razão Social.
    razao = cad[["RAZAO_SOCIAL", "UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD", "CLASSIFICACAO_CAD"]].copy()
    razao["CLIENTE_KEY"] = razao["RAZAO_SOCIAL"].apply(normalize_text_key)
    razao["ORIGEM_MATCH"] = "RAZÃO SOCIAL"
    razao["PRIORIDADE_MATCH"] = 0

    fantasia = cad[["NOME_FANTASIA", "UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD", "CLASSIFICACAO_CAD"]].copy()
    fantasia["CLIENTE_KEY"] = fantasia["NOME_FANTASIA"].apply(normalize_text_key)
    fantasia["ORIGEM_MATCH"] = "NOME FANTASIA"
    fantasia["PRIORIDADE_MATCH"] = 1

    aliases = pd.concat([
        razao[["CLIENTE_KEY", "UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD", "CLASSIFICACAO_CAD", "ORIGEM_MATCH", "PRIORIDADE_MATCH"]],
        fantasia[["CLIENTE_KEY", "UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD", "CLASSIFICACAO_CAD", "ORIGEM_MATCH", "PRIORIDADE_MATCH"]],
    ], ignore_index=True)

    aliases = (
        aliases[aliases["CLIENTE_KEY"] != ""]
        .sort_values(["PRIORIDADE_MATCH"], kind="stable")
        .drop_duplicates(subset=["CLIENTE_KEY"], keep="first")
    )
    return aliases[["CLIENTE_KEY", "UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD", "CLASSIFICACAO_CAD", "ORIGEM_MATCH"]]


def identificar_mes_ano_arquivo(nome: str):
    """Retorna (ano, mês) para nomes como AGOSTO 2026.xlsx; caso contrário, None."""
    stem = normalize_text_key(Path(nome).stem)
    m = re.fullmatch(r"(JANEIRO|FEVEREIRO|MARCO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)\s+(20\d{2})", stem)
    if not m:
        return None
    mes = MESES_ARQUIVO[m.group(1)]
    ano = int(m.group(2))
    if pd.Timestamp(ano, mes, 1) < INICIO_ARQUIVOS_MENSAIS:
        return None
    return ano, mes


def carregar_vendas_mensais(pasta: Path, cadastro: pd.DataFrame):
    """Carrega automaticamente todos os arquivos mensais válidos do repositório."""
    frames = []
    meses_importados = set()
    arquivos_lidos = []

    for arq in sorted(pasta.glob("*.xlsx")):
        periodo = identificar_mes_ano_arquivo(arq.name)
        if not periodo:
            continue
        ano_nome, mes_nome = periodo
        try:
            d = pd.read_excel(arq, header=1)
            d.columns = [normalize_col(c) for c in d.columns]
        except Exception:
            continue

        obrig = ["Cliente", "Data", "Valor custo", "Valor"]
        if any(c not in d.columns for c in obrig):
            continue

        # Mantém apenas linhas efetivamente comerciais; rodapés/totais não possuem cliente/data.
        d["DATA2"] = safe_to_datetime(d["Data"])
        d = d[d["Cliente"].notna() & d["DATA2"].notna()].copy()
        # O relatório inclui no total as linhas comerciais com cliente/data, independentemente da Situação.
        # Assim o dashboard reconcilia com o Valor total exibido no rodapé do próprio relatório.

        # Segurança: o conteúdo precisa pertencer ao mesmo mês/ano informado no nome do arquivo.
        d = d[(d["DATA2"].dt.year == ano_nome) & (d["DATA2"].dt.month == mes_nome)].copy()
        if d.empty:
            continue

        d["Valor total"] = d["Valor"].apply(parse_brl_number)
        d["Valor custo"] = d["Valor custo"].apply(parse_brl_number)
        d["Cliente"] = d["Cliente"].fillna("").astype(str).str.strip()
        d["CLIENTE_KEY"] = d["Cliente"].apply(normalize_text_key)

        d = d.merge(cadastro, on="CLIENTE_KEY", how="left")
        d["CADASTRO_ENCONTRADO"] = d["ORIGEM_MATCH"].notna()
        d["UF"] = d["UF_CAD"].fillna("").astype(str).str.strip()
        d["LOCALIZAÇÃO"] = d["LOCALIZACAO_CAD"].fillna("").astype(str).str.strip()
        d["BAIRRO"] = d["BAIRRO_CAD"].fillna("").astype(str).str.strip()
        d["CLASSIFICAÇÃO"] = d["CLASSIFICACAO_CAD"].apply(classificar_cliente)

        manter = ["DATA2", "Valor total", "Valor custo", "Cliente", "UF", "LOCALIZAÇÃO", "BAIRRO", "CLASSIFICAÇÃO", "CADASTRO_ENCONTRADO"]
        frames.append(d[manter].copy())
        meses_importados.add((ano_nome, mes_nome))
        arquivos_lidos.append(arq.name)

    if not frames:
        return pd.DataFrame(), set(), []
    return pd.concat(frames, ignore_index=True), meses_importados, arquivos_lidos


def identificar_mes_ano_arquivo_produtos(nome: str):
    """Retorna (ano, mês) para nomes como PRODUTOS AGOSTO 2026.xlsx ou PRODUTOS SETEMBRO DE 2026.xlsx."""
    stem = normalize_text_key(Path(nome).stem)
    m = re.fullmatch(
        r"(?:PADRAO\s+)?PRODUTOS\s+"
        r"(JANEIRO|FEVEREIRO|MARCO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)"
        r"(?:\s+DE)?\s+(20\d{2})",
        stem,
    )
    if not m:
        return None
    mes = MESES_ARQUIVO[m.group(1)]
    ano = int(m.group(2))
    if pd.Timestamp(ano, mes, 1) < INICIO_ARQUIVOS_MENSAIS:
        return None
    return ano, mes


def carregar_produtos_mensais(pasta: Path):
    """Carrega relatórios mensais de produtos e injeta MÊS/ANO pelo nome do arquivo."""
    frames = []
    meses_importados = set()
    arquivos_lidos = []

    for arq in sorted(pasta.glob("*.xlsx")):
        periodo = identificar_mes_ano_arquivo_produtos(arq.name)
        if not periodo:
            continue
        ano_nome, mes_nome = periodo

        try:
            d = pd.read_excel(arq, header=1)
            d.columns = [normalize_col(c) for c in d.columns]
        except Exception:
            continue

        obrig = ["Produto", "Quantidade", "Custo total", "Valor total"]
        if any(c not in d.columns for c in obrig):
            continue

        # Remove linhas em branco e rodapés/totais: só produto preenchido é linha comercial.
        d = d[d["Produto"].notna()].copy()
        d["Produto"] = d["Produto"].astype(str).str.strip()
        d = d[d["Produto"] != ""].copy()

        d["Quantidade"] = d["Quantidade"].apply(parse_brl_number)
        d["Custo total"] = d["Custo total"].apply(parse_brl_number)
        d["Valor total"] = d["Valor total"].apply(parse_brl_number)
        d["MÊS"] = MESES_PT[mes_nome - 1]
        d["ANO"] = ano_nome

        manter = ["Produto", "Quantidade", "MÊS", "ANO", "Valor total", "Custo total"]
        frames.append(d[manter].copy())
        meses_importados.add((ano_nome, mes_nome))
        arquivos_lidos.append(arq.name)

    if not frames:
        return pd.DataFrame(), set(), []
    return pd.concat(frames, ignore_index=True), meses_importados, arquivos_lidos


def abc_classification(df_in: pd.DataFrame, value_col: str, label_col: str = "Produto") -> pd.DataFrame:
    """
    Gera Curva ABC baseada em value_col (Quantidade ou Faturamento).
    Regras:
      A: até 80% acumulado
      B: 80% a 95%
      C: acima de 95%
    """
    d = df_in[[label_col, value_col]].copy()
    d[value_col] = d[value_col].fillna(0.0)
    d = d.groupby(label_col, as_index=False)[value_col].sum()
    d = d.sort_values(value_col, ascending=False)

    total = float(d[value_col].sum())
    if total <= 0:
        d["%"] = 0.0
        d["% Acum"] = 0.0
        d["Curva"] = "C"
        return d

    d["%"] = d[value_col] / total
    d["% Acum"] = d["%"].cumsum()

    def _curva(p):
        if p <= 0.80:
            return "A"
        if p <= 0.95:
            return "B"
        return "C"

    d["Curva"] = d["% Acum"].apply(_curva)
    return d


def sum_fat_2024_for_months(meses_nums):
    return float(sum(FAT_2024_MES.get(m, 0.0) for m in meses_nums))


def dataframe_to_pdf_bytes(df_in: pd.DataFrame, titulo: str = "Relatório") -> bytes:
    """Gera um PDF simples e profissional a partir de um DataFrame exibido no app."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    except Exception as e:
        raise RuntimeError(
            "Para exportar em PDF, instale a biblioteca reportlab: pip install reportlab"
        ) from e

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=0.7 * cm,
        leftMargin=0.7 * cm,
        topMargin=0.7 * cm,
        bottomMargin=0.7 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TituloRelatorio",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=13,
        leading=16,
        spaceAfter=8,
    )
    cell_style = ParagraphStyle(
        "CelulaTabela",
        parent=styles["BodyText"],
        fontSize=6.5,
        leading=8,
        wordWrap="CJK",
    )
    header_style = ParagraphStyle(
        "CabecalhoTabela",
        parent=cell_style,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )

    df_pdf = df_in.copy()
    df_pdf = df_pdf.reset_index() if df_pdf.index.name or not isinstance(df_pdf.index, pd.RangeIndex) else df_pdf.reset_index(drop=True)
    df_pdf = df_pdf.fillna("").astype(str)

    data = [[Paragraph(html.escape(str(c)), header_style) for c in df_pdf.columns]]
    for _, row in df_pdf.iterrows():
        data.append([Paragraph(html.escape(str(v)), cell_style) for v in row.tolist()])

    page_width = landscape(A4)[0] - (1.4 * cm)
    n_cols = max(len(df_pdf.columns), 1)
    col_widths = [page_width / n_cols] * n_cols

    tabela = Table(data, colWidths=col_widths, repeatRows=1, splitByRow=True)
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 6.5),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D9D9D9")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FB")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    story = [Paragraph(html.escape(titulo), title_style), Spacer(1, 0.2 * cm), tabela]
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def botao_download_pdf(df_in: pd.DataFrame, titulo: str, nome_arquivo: str):
    """Cria um botão de download em PDF para o DataFrame informado."""
    try:
        pdf_bytes = dataframe_to_pdf_bytes(df_in, titulo=titulo)
        st.download_button(
            label=f"Baixar PDF - {titulo}",
            data=pdf_bytes,
            file_name=nome_arquivo,
            mime="application/pdf",
            use_container_width=False,
        )
    except Exception as e:
        st.warning(str(e))



# =============================
# LOAD EXCEL + SELEÇÃO DAS ABAS
# =============================
st.markdown("""
<div class="autobras-topbar">
    <h1>Dashboard Comercial Autobrás</h1>
    <p>Inteligência comercial • desempenho • clientes • regiões • produtos</p>
</div>
""", unsafe_allow_html=True)

try:
    xls = pd.ExcelFile(ARQUIVO_EXCEL)
except Exception as e:
    st.error(f"Erro ao abrir o arquivo '{ARQUIVO_EXCEL}': {e}")
    st.stop()

abas = xls.sheet_names

# =============================
# LOAD EXCEL (abas fixas)
# =============================

ABA_VENDAS = "RELATÓRIO DE VENDAS"
ABA_PRODUTOS = "BASE DE PRODUTOS"
ABA_CLIENTES = "BASE DE CLIENTES"
ABA_LINHA = "LINHA"

abas = xls.sheet_names

faltando = [
    aba for aba in [ABA_VENDAS, ABA_PRODUTOS, ABA_CLIENTES, ABA_LINHA]
    if aba not in abas
]

if faltando:
    st.error(
        "As seguintes abas não foram encontradas no Excel:\n\n"
        + "\n".join(f"- {a}" for a in faltando)
        + "\n\nVerifique os nomes das abas no arquivo."
    )
    st.stop()

try:
    df_v = pd.read_excel(xls, sheet_name=ABA_VENDAS)
    df_p = pd.read_excel(xls, sheet_name=ABA_PRODUTOS)
    df_c = pd.read_excel(xls, sheet_name=ABA_CLIENTES)
    df_l = pd.read_excel(xls, sheet_name=ABA_LINHA)

except Exception as e:
    st.error(f"Erro ao ler as abas selecionadas: {e}")
    st.stop()

df_v.columns = [normalize_col(c) for c in df_v.columns]
df_p.columns = [normalize_col(c) for c in df_p.columns]
df_c.columns = [normalize_col(c) for c in df_c.columns]
df_l.columns = [normalize_col(c) for c in df_l.columns]

# Produtos mensais a partir de agosto/2026. Cada arquivo mensal substitui somente
# o respectivo mês existente na BASE DE PRODUTOS, evitando duplicidade.
PASTA_DADOS = Path(".")
df_prod_mensal, meses_prod_mensais, arquivos_prod_mensais = carregar_produtos_mensais(PASTA_DADOS)
if meses_prod_mensais and {"ANO", "MÊS"}.issubset(df_p.columns):
    df_p_hist = df_p.copy()
    ano_hist = pd.to_numeric(df_p_hist["ANO"], errors="coerce")
    mes_hist = df_p_hist["MÊS"].apply(parse_mes_to_num)
    chaves_hist = list(zip(ano_hist, mes_hist))
    manter_hist_prod = [
        not (pd.notna(a) and pd.notna(m) and (int(a), int(m)) in meses_prod_mensais)
        for a, m in chaves_hist
    ]
    df_p_hist = df_p_hist.loc[manter_hist_prod].copy()
    df_p = pd.concat([df_p_hist, df_prod_mensal], ignore_index=True, sort=False)
elif meses_prod_mensais:
    # Se a base histórica não tiver MÊS/ANO válidos, preserva o que existe e anexa os mensais.
    df_p = pd.concat([df_p, df_prod_mensal], ignore_index=True, sort=False)

# =============================
# PREP VENDAS
# =============================
required_cols = ["DATA2", "Valor total", "Valor custo", "Cliente", "UF", "LOCALIZAÇÃO", "BAIRRO", "CLASSIFICAÇÃO"]
missing = [c for c in required_cols if c not in df_v.columns]
if missing:
    st.error(
        "A aba de vendas não contém as colunas esperadas. Faltando: "
        + ", ".join(missing)
        + "\n\nConfira nomes, espaços e acentos (ex.: DATA2, Valor total, Valor custo, LOCALIZAÇÃO...)."
    )
    st.stop()

# Base histórica existente permanece como fonte principal.
df_base = df_v.copy()
df_base["DATA2"] = safe_to_datetime(df_base["DATA2"])
df_base = df_base[df_base["DATA2"].notna()].copy()
df_base["Valor total"] = df_base["Valor total"].apply(parse_brl_number)
df_base["Valor custo"] = df_base["Valor custo"].apply(parse_brl_number)
for col in ["Cliente", "UF", "LOCALIZAÇÃO", "BAIRRO", "CLASSIFICAÇÃO"]:
    df_base[col] = df_base[col].fillna("").astype(str).str.strip()

# Cadastro externo usado para enriquecer as vendas mensais a partir de agosto/2026.
PASTA_DADOS = Path(".")
df_cadastro_ext = carregar_cadastro_clientes_externo(PASTA_DADOS)
df_mensal, meses_mensais, arquivos_mensais = carregar_vendas_mensais(PASTA_DADOS, df_cadastro_ext)

if meses_mensais:
    # O arquivo mensal é autoritativo somente para seu mês, evitando duplicidade com base.xlsx.
    chave_base = list(zip(df_base["DATA2"].dt.year, df_base["DATA2"].dt.month))
    manter_hist = [chave not in meses_mensais for chave in chave_base]
    df_base = df_base.loc[manter_hist].copy()
    df = pd.concat([df_base[required_cols], df_mensal[required_cols]], ignore_index=True)
else:
    df = df_base[required_cols].copy()

# Remove duplicidades exatas depois da consolidação.
df = df.drop_duplicates()

# Padroniza classificações equivalentes antes de qualquer indicador do dashboard.
df["CLASSIFICAÇÃO"] = df["CLASSIFICAÇÃO"].apply(normalizar_classificacao_cliente)

# Consolida também diferenças residuais apenas de acento/caixa/espaçamento nas demais categorias.
_class_key = df["CLASSIFICAÇÃO"].apply(normalize_text_key)
_class_canon = (
    pd.DataFrame({"KEY": _class_key, "VAL": df["CLASSIFICAÇÃO"]})
    .query("KEY != ''")
    .drop_duplicates("KEY", keep="first")
    .set_index("KEY")["VAL"]
    .to_dict()
)
df["CLASSIFICAÇÃO"] = _class_key.map(_class_canon).fillna("SEM CLASSIFICAÇÃO")

df["ANO"] = df["DATA2"].dt.year
df["MES_NUM"] = df["DATA2"].dt.month
df["MES"] = df["MES_NUM"].apply(lambda m: MESES_PT[m - 1])

# Margem sempre calculada pelo código, inclusive nos arquivos mensais.
df["MARGEM_BRUTA_R$"] = df["Valor total"] - df["Valor custo"]
df["MARGEM_BRUTA_%"] = df.apply(
    lambda r: (r["MARGEM_BRUTA_R$"] / r["Valor total"]) if r["Valor total"] else 0.0,
    axis=1
)

# Clientes das vendas mensais que não foram localizados nem por Razão Social nem por Nome Fantasia.
clientes_sem_cadastro = pd.DataFrame()
if not df_mensal.empty and "CADASTRO_ENCONTRADO" in df_mensal.columns:
    mask_sem_cad = ~df_mensal["CADASTRO_ENCONTRADO"].fillna(False)
    if mask_sem_cad.any():
        clientes_sem_cadastro = (
            df_mensal.loc[mask_sem_cad]
            .groupby("Cliente", as_index=False)
            .agg(FATURAMENTO=("Valor total", "sum"))
            .sort_values("FATURAMENTO", ascending=False)
        )

if arquivos_mensais:
    st.caption("Arquivos mensais de vendas incorporados: " + ", ".join(arquivos_mensais))
    if df_cadastro_ext.empty:
        st.warning("Arquivos mensais encontrados, mas o arquivo CADASTRO DE CLIENTES.xlsx não foi localizado. Cidade, bairro, UF e classificação podem ficar sem preenchimento nas vendas novas.")

if arquivos_prod_mensais:
    st.caption("Arquivos mensais de produtos incorporados: " + ", ".join(arquivos_prod_mensais))

if not clientes_sem_cadastro.empty:
    mask_ml_pend = clientes_sem_cadastro["Cliente"].apply(normalize_text_key).str.contains(r"\bMERCADO\s+LIVRE\b", regex=True, na=False)
    cad_nao_localizado = clientes_sem_cadastro.loc[~mask_ml_pend].copy()
    if not cad_nao_localizado.empty:
        st.warning(
            f"Atenção cadastral: {cad_nao_localizado['Cliente'].nunique()} cliente(s) das vendas mensais "
            "não foram encontrados no CADASTRO DE CLIENTES nem por Razão Social nem por Nome Fantasia."
        )
        with st.expander("Ver clientes não encontrados no cadastro"):
            cad_show = cad_nao_localizado.copy()
            cad_show["FATURAMENTO"] = cad_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
            st.dataframe(cad_show, use_container_width=True, hide_index=True)

# Regra especial: vendas do cliente Mercado Livre são pulverizadas em todo o Brasil.
# Para fins gerenciais, a UF é tratada como "MERCADO LIVRE" e o cliente não entra
# na pendência cadastral de UF/cidade.
df["UF"] = df["UF"].fillna("").astype(str).str.strip()
df["LOCALIZAÇÃO"] = df["LOCALIZAÇÃO"].fillna("").astype(str).str.strip()
mask_mercado_livre = df["Cliente"].apply(normalize_text_key).str.contains(r"\bMERCADO\s+LIVRE\b", regex=True, na=False)
df.loc[mask_mercado_livre, "UF"] = "MERCADO LIVRE"

# Validação cadastral: sinaliza qualquer cliente sem UF e/ou cidade/localização,
# exceto Mercado Livre, cuja operação não representa uma praça geográfica única.
mask_geo_incompleta = ((df["UF"] == "") | (df["LOCALIZAÇÃO"] == "")) & (~mask_mercado_livre)
if mask_geo_incompleta.any():
    geo_pend = (
        df.loc[mask_geo_incompleta]
        .groupby(["Cliente", "UF", "LOCALIZAÇÃO"], dropna=False, as_index=False)
        .agg(FATURAMENTO=("Valor total", "sum"))
        .sort_values("FATURAMENTO", ascending=False)
    )
    qtd_geo = int(geo_pend["Cliente"].nunique())
    st.warning(
        f"Atenção cadastral: {qtd_geo} cliente(s) estão sem UF e/ou cidade/localização. "
        "Revise o arquivo de cadastro de clientes para completar esses dados."
    )
    with st.expander("Ver clientes com UF/cidade não encontrada"):
        geo_show = geo_pend.copy()
        geo_show["UF"] = geo_show["UF"].replace("", "NÃO INFORMADO")
        geo_show["LOCALIZAÇÃO"] = geo_show["LOCALIZAÇÃO"].replace("", "NÃO INFORMADO")
        geo_show["FATURAMENTO"] = geo_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
        st.dataframe(geo_show, use_container_width=True, hide_index=True)

# =============================
# FILTROS (ANO + PERÍODO)
# =============================
with st.sidebar:
    st.header("Filtros")

    anos = sorted(df["ANO"].dropna().unique().tolist())
    if not anos:
        st.error("Não há dados com DATA2 válida para filtrar por ano.")
        st.stop()

    ano_sel = st.selectbox("Ano", anos, index=len(anos) - 1)

    df_ano = df[df["ANO"] == ano_sel].copy()
    if df_ano.empty:
        st.warning("Não há dados para o ano selecionado.")
        st.stop()

    min_d = df_ano["DATA2"].min().date()
    max_d = df_ano["DATA2"].max().date()

    periodo = st.date_input(
        "Período (calendário BR)",
        value=(min_d, max_d),
        min_value=min_d,
        max_value=max_d,
    )
    if isinstance(periodo, tuple) and len(periodo) == 2:
        d_ini, d_fim = periodo
    else:
        d_ini, d_fim = min_d, max_d

    st.markdown(f'<div class="period-chip">{d_ini.strftime("%d/%m/%Y")} → {d_fim.strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)

df_f = df_ano[(df_ano["DATA2"].dt.date >= d_ini) & (df_ano["DATA2"].dt.date <= d_fim)].copy()

# meses selecionados no período (para filtrar BASE DE PRODUTOS por MÊS)
meses_sel = sorted(df_f["MES_NUM"].dropna().unique().tolist())

tab_visao, tab_geo, tab_clientes, tab_class, tab_prod = st.tabs(["Visão Geral", "Geografia", "Clientes", "Classificações", "Produtos"])

with tab_visao:
    # =============================
    # KPIs
    # =============================
    fat_total = df_f["Valor total"].sum()
    custo_total = df_f["Valor custo"].sum()
    margem_rs = fat_total - custo_total
    margem_pct = (margem_rs / fat_total) if fat_total else 0.0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Faturamento", f"R$ {format_brl(fat_total)}")
    k2.metric("Custo", f"R$ {format_brl(custo_total)}", f"{pct_br(custo_total/fat_total) if fat_total else '—'} da venda")
    k3.metric("Margem Bruta", f"R$ {format_brl(margem_rs)}")
    k4.metric("Margem %", pct_br(margem_pct))

    # =============================
    # INDICADOR: CRESCIMENTO ANO-1 (mesmo período)
    # =============================
    st.markdown('<div class="section-title">Desempenho Comercial</div><div class="section-subtitle">Comparativo com o mesmo período do ano anterior.</div>', unsafe_allow_html=True)

    ano_ant = int(ano_sel) - 1

    # Receita atual (já está filtrada por período)
    fat_atual_periodo = float(df_f["Valor total"].sum())

    # Define período do ano anterior (mesmo range de datas)
    d_ini_ts = pd.Timestamp(d_ini)
    d_fim_ts = pd.Timestamp(d_fim)
    d_ini_ant = (d_ini_ts - pd.DateOffset(years=1)).date()
    d_fim_ant = (d_fim_ts - pd.DateOffset(years=1)).date()

    df_ant_ano = df[df["ANO"] == ano_ant].copy()
    tem_ano_ant_na_base = not df_ant_ano.empty

    if tem_ano_ant_na_base:
        df_ant_periodo = df_ant_ano[
            (df_ant_ano["DATA2"].dt.date >= d_ini_ant) &
            (df_ant_ano["DATA2"].dt.date <= d_fim_ant)
        ].copy()
        fat_ant_periodo = float(df_ant_periodo["Valor total"].sum())
        origem_ant = f"Base XLSX (ano {ano_ant})"
    else:
        # fallback apenas para 2024
        if ano_ant == 2024:
            fat_ant_periodo = sum_fat_2024_for_months(meses_sel)
            origem_ant = "Tabela fixa 2024 (por mês)"
        else:
            fat_ant_periodo = 0.0
            origem_ant = f"Sem dados do ano {ano_ant} (base vazia)"

    crescimento_rs = fat_atual_periodo - fat_ant_periodo
    crescimento_pct = (crescimento_rs / fat_ant_periodo) if fat_ant_periodo else 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"Faturamento {ano_sel} (período)", f"R$ {format_brl(fat_atual_periodo)}")
    c2.metric(f"Faturamento {ano_ant} (período)", f"R$ {format_brl(fat_ant_periodo)}")
    c3.metric("Crescimento (R$)", f"R$ {format_brl(crescimento_rs)}")
    c4.metric("Crescimento (%)", pct_br(crescimento_pct))

    st.caption(f"Fonte do Ano-1: **{origem_ant}**. Período comparado: {d_ini}–{d_fim} vs {d_ini_ant}–{d_fim_ant}.")

    # Tabela mês-a-mês: atual vs ano-1
    fat_mes_atual = (
        df_f.groupby("MES_NUM", as_index=False)["Valor total"].sum()
        .rename(columns={"Valor total": "FAT_ATUAL"})
    )
    fat_mes_atual["MÊS"] = fat_mes_atual["MES_NUM"].apply(lambda m: MESES_PT[m - 1])

    if tem_ano_ant_na_base:
        df_ant_periodo["MES_NUM"] = df_ant_periodo["DATA2"].dt.month
        fat_mes_ant = (
            df_ant_periodo.groupby("MES_NUM", as_index=False)["Valor total"].sum()
            .rename(columns={"Valor total": "FAT_ANO_1"})
        )
    else:
        # 2024 fixo por meses (sem recorte de dia) — usa apenas meses selecionados
        fat_mes_ant = pd.DataFrame({
            "MES_NUM": meses_sel if meses_sel else list(range(1, 13)),
        })
        fat_mes_ant["FAT_ANO_1"] = fat_mes_ant["MES_NUM"].apply(lambda m: float(FAT_2024_MES.get(m, 0.0)) if ano_ant == 2024 else 0.0)

    tbl_yoy = pd.merge(fat_mes_atual, fat_mes_ant, on="MES_NUM", how="left")
    tbl_yoy["FAT_ANO_1"] = tbl_yoy["FAT_ANO_1"].fillna(0.0)
    tbl_yoy["DIF_R$"] = tbl_yoy["FAT_ATUAL"] - tbl_yoy["FAT_ANO_1"]
    tbl_yoy["DIF_%"] = tbl_yoy.apply(lambda r: (r["DIF_R$"] / r["FAT_ANO_1"]) if r["FAT_ANO_1"] else 0.0, axis=1)

    tbl_yoy_show = tbl_yoy[["MÊS", "FAT_ATUAL", "FAT_ANO_1", "DIF_R$", "DIF_%"]].copy()
    tbl_yoy_show["FAT_ATUAL"] = tbl_yoy_show["FAT_ATUAL"].apply(lambda x: f"R$ {format_brl(x)}")
    tbl_yoy_show["FAT_ANO_1"] = tbl_yoy_show["FAT_ANO_1"].apply(lambda x: f"R$ {format_brl(x)}")
    tbl_yoy_show["DIF_R$"] = tbl_yoy_show["DIF_R$"].apply(lambda x: f"R$ {format_brl(x)}")
    tbl_yoy_show["DIF_%"] = tbl_yoy_show["DIF_%"].apply(pct_br)

    fig_yoy = go.Figure()
    fig_yoy.add_trace(go.Bar(
        x=tbl_yoy["MÊS"], y=tbl_yoy["FAT_ATUAL"], name=str(ano_sel),
        text=tbl_yoy["FAT_ATUAL"].apply(lambda v: f"R$ {v/1_000_000:.2f} mi" if v >= 1_000_000 else f"R$ {v/1_000:.0f} mil"),
        textposition="outside"
    ))
    fig_yoy.add_trace(go.Scatter(
        x=tbl_yoy["MÊS"], y=tbl_yoy["FAT_ANO_1"], name=str(ano_ant),
        mode="lines+markers", line=dict(width=3), marker=dict(size=8)
    ))
    fig_yoy.update_layout(
        height=410, margin=dict(l=10, r=10, t=45, b=10),
        legend=dict(orientation="h", y=1.10), xaxis_title=None,
        yaxis_title="Faturamento (R$)", hovermode="x unified"
    )
    st.plotly_chart(fig_yoy, use_container_width=True)

    with st.expander("Ver comparativo mensal detalhado"):
        st.dataframe(tbl_yoy_show, use_container_width=True, hide_index=True)
        botao_download_pdf(tbl_yoy_show, "Crescimento Ano-1", "crescimento_ano_1.pdf")

    st.divider()

    # =============================
    # 2) RELAÇÃO FINANCEIRA POR MÊS (TABELA)
    # =============================
    st.markdown('<div class="section-title">Resultado mensal</div><div class="section-subtitle">Faturamento, custo e margem por competência.</div>', unsafe_allow_html=True)

    rel_mes = df_f.groupby("MES_NUM", as_index=False).agg(
        FATURAMENTO=("Valor total", "sum"),
        VALOR_CUSTO=("Valor custo", "sum"),
    ).sort_values("MES_NUM")

    rel_mes["MARGEM_BRUTA_R$"] = rel_mes["FATURAMENTO"] - rel_mes["VALOR_CUSTO"]
    rel_mes["MARGEM_BRUTA_%"] = rel_mes.apply(
        lambda r: (rel_mes.loc[r.name, "MARGEM_BRUTA_R$"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0,
        axis=1
    )
    rel_mes["MÊS"] = rel_mes["MES_NUM"].apply(lambda m: MESES_PT[m - 1])

    rel_mes_show = rel_mes[["MÊS", "FATURAMENTO", "VALOR_CUSTO", "MARGEM_BRUTA_R$", "MARGEM_BRUTA_%"]].copy()
    rel_mes_show["FATURAMENTO"] = rel_mes_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
    rel_mes_show["VALOR_CUSTO"] = rel_mes_show["VALOR_CUSTO"].apply(lambda x: f"R$ {format_brl(x)}")
    rel_mes_show["MARGEM_BRUTA_R$"] = rel_mes_show["MARGEM_BRUTA_R$"].apply(lambda x: f"R$ {format_brl(x)}")
    rel_mes_show["MARGEM_BRUTA_%"] = rel_mes_show["MARGEM_BRUTA_%"].apply(pct_br)

    with st.expander("Ver tabela financeira mensal"):
        st.dataframe(rel_mes_show, use_container_width=True, hide_index=True)
        botao_download_pdf(rel_mes_show, "Relação Financeira por Mês", "relacao_financeira_mes.pdf")

    st.divider()


with tab_geo:
    # =============================
    # 3) MAPA DO BRASIL POR UF + DRILL GEOGRÁFICO
    # =============================
    st.subheader("Mapa do Brasil — Faturamento por UF")

    # Coordenadas aproximadas dos centroides das UFs. Os pontos permanecem na posição
    # geográfica real; os rótulos usam deslocamentos próprios para evitar sobreposição.
    UF_COORDS = {
        "AC": (-8.77, -70.55), "AL": (-9.62, -36.82), "AP": (1.41, -51.77),
        "AM": (-3.47, -65.10), "BA": (-12.96, -41.70), "CE": (-5.20, -39.53),
        "DF": (-15.78, -47.93), "ES": (-19.19, -40.34), "GO": (-15.98, -49.86),
        "MA": (-5.42, -45.44), "MT": (-12.64, -55.42), "MS": (-20.51, -54.54),
        "MG": (-18.10, -44.38), "PA": (-3.79, -52.48), "PB": (-7.28, -36.72),
        "PR": (-24.89, -51.55), "PE": (-8.38, -37.86), "PI": (-6.60, -42.28),
        "RJ": (-22.25, -42.66), "RN": (-5.81, -36.59), "RS": (-30.17, -53.50),
        "RO": (-10.83, -63.34), "RR": (1.99, -61.33), "SC": (-27.45, -50.95),
        "SP": (-22.19, -48.79), "SE": (-10.57, -37.45), "TO": (-9.46, -48.26),
    }

    # Deslocamento do TEXTO (não do ponto) em graus. Ajuda principalmente no Centro-Oeste
    # e Nordeste, onde centroides ficam próximos. A linha liga o rótulo à posição real.
    UF_LABEL_OFFSET = {
        "DF": (1.45, 2.15),
        "GO": (-1.20, -1.85),
        "AL": (-0.70, 1.25),
        "SE": (0.65, 1.35),
        "PB": (0.80, 1.25),
        "PE": (-0.55, 1.55),
        "RN": (0.95, 1.05),
        "ES": (-0.40, 1.35),
        "RJ": (-0.90, 1.25),
        "SC": (-0.35, 1.05),
    }

    uf_mapa_all = (
        df_f.assign(UF=df_f["UF"].fillna("").astype(str).str.upper().str.strip())
        .groupby("UF", as_index=False)["Valor total"].sum()
        .rename(columns={"Valor total": "FATURAMENTO"})
    )
    uf_mapa = uf_mapa_all[uf_mapa_all["UF"].isin(UF_COORDS)].copy()
    uf_mapa["LAT"] = uf_mapa["UF"].map(lambda x: UF_COORDS[x][0])
    uf_mapa["LON"] = uf_mapa["UF"].map(lambda x: UF_COORDS[x][1])
    uf_mapa["LABEL_LAT"] = uf_mapa.apply(lambda r: r["LAT"] + UF_LABEL_OFFSET.get(r["UF"], (0.85, 0))[0], axis=1)
    uf_mapa["LABEL_LON"] = uf_mapa.apply(lambda r: r["LON"] + UF_LABEL_OFFSET.get(r["UF"], (0.85, 0))[1], axis=1)
    uf_mapa["LABEL"] = uf_mapa.apply(lambda r: f"<b>{r['UF']}</b><br>R$ {format_brl(r['FATURAMENTO'])}", axis=1)

    fig_brasil = go.Figure()

    # Linhas-guia para rótulos deslocados.
    for _, r in uf_mapa.iterrows():
        if r["UF"] in UF_LABEL_OFFSET:
            fig_brasil.add_trace(go.Scattergeo(
                lon=[r["LON"], r["LABEL_LON"]], lat=[r["LAT"], r["LABEL_LAT"]],
                mode="lines", line=dict(width=1.2, color="#6B7C93"),
                hoverinfo="skip", showlegend=False
            ))

    # Pontos nas posições reais das UFs.
    max_fat_uf = float(uf_mapa["FATURAMENTO"].max()) if not uf_mapa.empty else 0.0
    fig_brasil.add_trace(go.Scattergeo(
        lon=uf_mapa["LON"], lat=uf_mapa["LAT"],
        mode="markers",
        customdata=uf_mapa[["UF", "FATURAMENTO"]],
        marker=dict(
            size=uf_mapa["FATURAMENTO"].apply(lambda v: 10 + 22 * (v / max_fat_uf) if max_fat_uf else 10),
            opacity=0.78, line=dict(width=1.3, color="white")
        ),
        hovertemplate="<b>%{customdata[0]}</b><br>Faturamento: R$ %{customdata[1]:,.2f}<extra></extra>",
        showlegend=False
    ))

    # Rótulos em camada separada: fonte maior, caixa branca e posição independente.
    fig_brasil.add_trace(go.Scattergeo(
        lon=uf_mapa["LABEL_LON"], lat=uf_mapa["LABEL_LAT"],
        text=uf_mapa["LABEL"], mode="text",
        textfont=dict(size=13, color="#102A43", family="Arial Black"),
        customdata=uf_mapa[["UF", "FATURAMENTO"]],
        hovertemplate="<b>%{customdata[0]}</b><br>Faturamento: R$ %{customdata[1]:,.2f}<extra></extra>",
        showlegend=False
    ))

    fig_brasil.update_geos(
        scope="south america", projection_type="mercator",
        lataxis_range=[-35, 6], lonaxis_range=[-75, -32],
        showland=True, landcolor="#EEF3F8", showcountries=True, countrycolor="#AAB7C4",
        showcoastlines=True, coastlinecolor="#AAB7C4", bgcolor="rgba(0,0,0,0)"
    )
    fig_brasil.update_layout(
        height=690, margin=dict(l=0, r=0, t=20, b=0),
        title="Faturamento por UF"
    )
    st.plotly_chart(fig_brasil, use_container_width=True)

    ufs_fora_mapa = sorted(set(uf_mapa_all["UF"]) - set(UF_COORDS) - {"", "MERCADO LIVRE"})
    if ufs_fora_mapa:
        st.caption("UFs não posicionadas no mapa: " + ", ".join(ufs_fora_mapa))

    # -----------------------------
    # DRILL GEOGRÁFICO: DF > REGIÃO/BAIRRO | DEMAIS UFs > CIDADE > BAIRRO
    # -----------------------------
    st.markdown("#### Drill geográfico — UF → Cidade/Região → Bairro")
    st.caption("No Distrito Federal, o primeiro detalhamento usa bairros/regiões e consolida variações como Ceilândia Norte/Sul em Ceilândia. Nas demais UFs, o primeiro nível é Cidade.")

    UFS_BR = {
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
        "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
        "SP", "SE", "TO"
    }

    NOMES_UF_BR = {
        "ACRE", "ALAGOAS", "AMAPA", "AMAZONAS", "BAHIA", "CEARA", "DISTRITO FEDERAL",
        "ESPIRITO SANTO", "GOIAS", "MARANHAO", "MATO GROSSO", "MATO GROSSO DO SUL",
        "MINAS GERAIS", "PARA", "PARAIBA", "PARANA", "PERNAMBUCO", "PIAUI",
        "RIO DE JANEIRO", "RIO GRANDE DO NORTE", "RIO GRANDE DO SUL", "RONDONIA", "RORAIMA",
        "SANTA CATARINA", "SAO PAULO", "SERGIPE", "TOCANTINS"
    }

    def normalizar_local_geo(v, consolidar_df=False):
        """
        Cria uma chave geográfica única para TODO o Brasil.
        Consolida acentos/caixa/espaços e remove UF/estado anexado ao final do nome.
        Exemplos: GOIANIA, GOIANIA-GO, GOIANIA/GO e GOIANIA, GO -> Goiania.
        No DF, também consolida subdivisões direcionais, como Ceilandia Norte/Sul -> Ceilandia.
        """
        if v is None or pd.isna(v):
            return "NÃO INFORMADO"
        original = re.sub(r"\s+", " ", str(v).strip())
        if not original or re.fullmatch(r"[-–—_\s]+", original):
            return "NÃO INFORMADO"

        chave = normalize_text_key(original)
        chave = re.sub(r"\s+", " ", chave).strip()

        # Remove sufixos de UF em qualquer formato comum: Cidade,GO | Cidade-GO | Cidade/GO | Cidade GO.
        siglas = "|".join(sorted(UFS_BR))
        chave = re.sub(rf"\s*[,;/\-]\s*(?:{siglas})\s*$", "", chave).strip()
        chave = re.sub(rf"\s+(?:{siglas})\s*$", "", chave).strip()

        # Remove também o nome completo do estado quando anexado ao fim: Cidade, Goiás etc.
        for nome_estado in sorted(NOMES_UF_BR, key=len, reverse=True):
            chave = re.sub(rf"\s*[,;/\-]\s*{re.escape(nome_estado)}\s*$", "", chave).strip()

        if consolidar_df:
            # Ex.: CEILANDIA NORTE / CEILANDIA SUL -> CEILANDIA.
            chave = re.sub(r"\s+(NORTE|SUL|LESTE|OESTE)$", "", chave).strip()

        return chave.title() if chave else "NÃO INFORMADO"

    geo_base = df_f.copy()
    for c in ["UF", "LOCALIZAÇÃO", "BAIRRO"]:
        geo_base[c] = geo_base[c].fillna("").astype(str).str.strip()
    geo_base["UF"] = geo_base["UF"].str.upper()

    ufs_geo = sorted([u for u in geo_base["UF"].unique().tolist() if u and u != "MERCADO LIVRE"])
    geo_col1, geo_col2 = st.columns(2)
    with geo_col1:
        geo_uf_sel = st.selectbox("UF para detalhar", ["(Selecione)"] + ufs_geo, key="geo_uf_drill")

    if geo_uf_sel != "(Selecione)":
        geo_uf = geo_base[geo_base["UF"] == geo_uf_sel].copy()
        fat_geo_uf = float(geo_uf["Valor total"].sum())
        fat_geo_geral = float(geo_base["Valor total"].sum())
        eh_df = geo_uf_sel == "DF"

        if eh_df:
            # No DF, BAIRRO é o nível gerencial principal. Norte/Sul etc. são consolidados.
            geo_uf["NIVEL_GEO"] = geo_uf["BAIRRO"].apply(lambda x: normalizar_local_geo(x, consolidar_df=True))
            rotulo_nivel = "Região/Bairro"
            rotulo_plural = "Regiões/Bairros"
        else:
            # Demais UFs: Cidade, consolidando diferenças de acento, caixa e espaços.
            geo_uf["NIVEL_GEO"] = geo_uf["LOCALIZAÇÃO"].apply(normalizar_local_geo)
            rotulo_nivel = "Cidade"
            rotulo_plural = "Cidades"

        locais = (
            geo_uf.groupby("NIVEL_GEO", as_index=False)["Valor total"].sum()
            .rename(columns={"NIVEL_GEO": rotulo_nivel.upper(), "Valor total": "FATURAMENTO"})
            .sort_values("FATURAMENTO", ascending=False)
        )
        locais["% DA UF"] = locais["FATURAMENTO"].apply(lambda x: x / fat_geo_uf if fat_geo_uf else 0.0)
        locais["% DO GERAL"] = locais["FATURAMENTO"].apply(lambda x: x / fat_geo_geral if fat_geo_geral else 0.0)

        with geo_col2:
            local_sel = st.selectbox(
                f"{rotulo_nivel} para detalhar",
                ["(Todas)"] + locais[rotulo_nivel.upper()].tolist(),
                key="geo_cidade_drill"
            )

        gm1, gm2, gm3 = st.columns(3)
        gm1.metric(f"Faturamento {geo_uf_sel}", f"R$ {format_brl(fat_geo_uf)}")
        gm2.metric("Participação no Geral", pct_br(fat_geo_uf / fat_geo_geral if fat_geo_geral else 0.0))
        gm3.metric(f"{rotulo_plural} com faturamento", f"{len(locais):,}".replace(",", "."))

        locais_plot = locais.head(15).sort_values("FATURAMENTO", ascending=True)
        fig_locais = px.bar(
            locais_plot, x="FATURAMENTO", y=rotulo_nivel.upper(), orientation="h",
            title=f"Top {rotulo_plural.lower()} de {geo_uf_sel} por faturamento",
            text="FATURAMENTO"
        )
        fig_locais.update_traces(
            texttemplate="R$ %{text:,.0f}", textposition="outside",
            hovertemplate="<b>%{y}</b><br>Faturamento: R$ %{x:,.2f}<extra></extra>"
        )
        fig_locais.update_layout(height=max(380, 30 * len(locais_plot) + 100), xaxis_title="Faturamento", yaxis_title="")
        st.plotly_chart(fig_locais, use_container_width=True)

        locais_show = locais.copy()
        locais_show["FATURAMENTO"] = locais_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
        locais_show["% DA UF"] = locais_show["% DA UF"].apply(pct_br)
        locais_show["% DO GERAL"] = locais_show["% DO GERAL"].apply(pct_br)
        st.dataframe(locais_show, use_container_width=True, hide_index=True)

        # Nas demais UFs, mantém o segundo nível por Bairro. No DF, o bairro/região já é o nível principal.
        if (not eh_df) and local_sel != "(Todas)":
            st.markdown(f"##### Bairros — {local_sel} / {geo_uf_sel}")
            geo_cidade = geo_uf[geo_uf["NIVEL_GEO"] == local_sel].copy()
            fat_geo_cidade = float(geo_cidade["Valor total"].sum())
            geo_cidade["BAIRRO_NORM"] = geo_cidade["BAIRRO"].apply(normalizar_local_geo)
            bairros = (
                geo_cidade.groupby("BAIRRO_NORM", as_index=False)["Valor total"].sum()
                .rename(columns={"BAIRRO_NORM": "BAIRRO", "Valor total": "FATURAMENTO"})
                .sort_values("FATURAMENTO", ascending=False)
            )
            bairros["% DA CIDADE"] = bairros["FATURAMENTO"].apply(lambda x: x / fat_geo_cidade if fat_geo_cidade else 0.0)
            bairros["% DA UF"] = bairros["FATURAMENTO"].apply(lambda x: x / fat_geo_uf if fat_geo_uf else 0.0)
            bairros["% DO GERAL"] = bairros["FATURAMENTO"].apply(lambda x: x / fat_geo_geral if fat_geo_geral else 0.0)

            bm1, bm2, bm3 = st.columns(3)
            bm1.metric(f"Faturamento {local_sel}", f"R$ {format_brl(fat_geo_cidade)}")
            bm2.metric(f"Participação em {geo_uf_sel}", pct_br(fat_geo_cidade / fat_geo_uf if fat_geo_uf else 0.0))
            bm3.metric("Bairros com faturamento", f"{len(bairros):,}".replace(",", "."))

            bairros_plot = bairros.head(15).sort_values("FATURAMENTO", ascending=True)
            fig_bairros = px.bar(
                bairros_plot, x="FATURAMENTO", y="BAIRRO", orientation="h",
                title=f"Top bairros de {local_sel} por faturamento", text="FATURAMENTO"
            )
            fig_bairros.update_traces(
                texttemplate="R$ %{text:,.0f}", textposition="outside",
                hovertemplate="<b>%{y}</b><br>Faturamento: R$ %{x:,.2f}<extra></extra>"
            )
            fig_bairros.update_layout(height=max(380, 30 * len(bairros_plot) + 100), xaxis_title="Faturamento", yaxis_title="")
            st.plotly_chart(fig_bairros, use_container_width=True)

            bairros_show = bairros.copy()
            bairros_show["FATURAMENTO"] = bairros_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
            bairros_show["% DA CIDADE"] = bairros_show["% DA CIDADE"].apply(pct_br)
            bairros_show["% DA UF"] = bairros_show["% DA UF"].apply(pct_br)
            bairros_show["% DO GERAL"] = bairros_show["% DO GERAL"].apply(pct_br)
            st.dataframe(bairros_show, use_container_width=True, hide_index=True)
        elif eh_df and local_sel != "(Todas)":
            geo_local = geo_uf[geo_uf["NIVEL_GEO"] == local_sel].copy()
            fat_local = float(geo_local["Valor total"].sum())
            lm1, lm2 = st.columns(2)
            lm1.metric(f"Faturamento {local_sel}", f"R$ {format_brl(fat_local)}")
            lm2.metric("Participação no DF", pct_br(fat_local / fat_geo_uf if fat_geo_uf else 0.0))

        # Clientes da cidade/região selecionada. No DF, NIVEL_GEO representa Região/Bairro;
        # nas demais UFs, representa Cidade. O faturamento é consolidado por cliente.
        if local_sel != "(Todas)":
            geo_clientes = geo_uf[geo_uf["NIVEL_GEO"] == local_sel].copy()
            fat_regiao_sel = float(geo_clientes["Valor total"].sum())

            clientes_regiao = (
                geo_clientes.groupby("Cliente", as_index=False)
                .agg(
                    FATURAMENTO=("Valor total", "sum"),
                    VALOR_CUSTO=("Valor custo", "sum"),
                )
                .sort_values("FATURAMENTO", ascending=False)
            )
            clientes_regiao["MARGEM_BRUTA_R$"] = clientes_regiao["FATURAMENTO"] - clientes_regiao["VALOR_CUSTO"]
            clientes_regiao["MARGEM_BRUTA_%"] = clientes_regiao.apply(
                lambda r: (r["MARGEM_BRUTA_R$"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0, axis=1
            )
            clientes_regiao["% DA REGIÃO"] = clientes_regiao["FATURAMENTO"].apply(
                lambda x: x / fat_regiao_sel if fat_regiao_sel else 0.0
            )
            clientes_regiao["% DA UF"] = clientes_regiao["FATURAMENTO"].apply(
                lambda x: x / fat_geo_uf if fat_geo_uf else 0.0
            )
            clientes_regiao["% DO GERAL"] = clientes_regiao["FATURAMENTO"].apply(
                lambda x: x / fat_geo_geral if fat_geo_geral else 0.0
            )

            st.markdown(f"##### Clientes — {local_sel} / {geo_uf_sel}")
            cm1, cm2, cm3 = st.columns(3)
            cm1.metric("Clientes com faturamento", f"{clientes_regiao['Cliente'].nunique():,}".replace(",", "."))
            cm2.metric("Faturamento da região", f"R$ {format_brl(fat_regiao_sel)}")
            cm3.metric("Participação no Geral", pct_br(fat_regiao_sel / fat_geo_geral if fat_geo_geral else 0.0))

            clientes_show = clientes_regiao[[
                "Cliente", "FATURAMENTO", "MARGEM_BRUTA_R$", "MARGEM_BRUTA_%",
                "% DA REGIÃO", "% DA UF", "% DO GERAL"
            ]].copy()
            clientes_show["FATURAMENTO"] = clientes_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
            clientes_show["MARGEM_BRUTA_R$"] = clientes_show["MARGEM_BRUTA_R$"].apply(lambda x: f"R$ {format_brl(x)}")
            for col_pct in ["MARGEM_BRUTA_%", "% DA REGIÃO", "% DA UF", "% DO GERAL"]:
                clientes_show[col_pct] = clientes_show[col_pct].apply(pct_br)
            st.dataframe(clientes_show, use_container_width=True, hide_index=True)
            botao_download_pdf(
                clientes_show,
                f"Clientes - {local_sel} - {geo_uf_sel}",
                f"clientes_{normalize_text_key(local_sel).lower().replace(' ', '_')}_{geo_uf_sel.lower()}.pdf"
            )
    else:
        st.info("Selecione uma UF. No DF o detalhamento será por bairro/região; nas demais UFs, por cidade.")

    st.divider()

    # =============================
    # 4) TABELA POR UF: FATURAMENTO, CUSTO, MARGEM R$, MARGEM %
    # =============================
    st.subheader("Tabela por UF: Faturamento × Custo × Margem")

    uf_tbl = df_f.groupby("UF", as_index=False).agg(
        FATURAMENTO=("Valor total", "sum"),
        VALOR_CUSTO=("Valor custo", "sum"),
    )

    uf_tbl["MARGEM_BRUTA_R$"] = uf_tbl["FATURAMENTO"] - uf_tbl["VALOR_CUSTO"]
    uf_tbl["MARGEM_BRUTA_%"] = uf_tbl.apply(
        lambda r: (r["MARGEM_BRUTA_R$"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0,
        axis=1
    )

    uf_tbl = uf_tbl.sort_values("FATURAMENTO", ascending=False)

    uf_tbl_show = uf_tbl.copy()
    uf_tbl_show["FATURAMENTO"] = uf_tbl_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
    uf_tbl_show["VALOR_CUSTO"] = uf_tbl_show["VALOR_CUSTO"].apply(lambda x: f"R$ {format_brl(x)}")
    uf_tbl_show["MARGEM_BRUTA_R$"] = uf_tbl_show["MARGEM_BRUTA_R$"].apply(lambda x: f"R$ {format_brl(x)}")
    uf_tbl_show["MARGEM_BRUTA_%"] = uf_tbl_show["MARGEM_BRUTA_%"].apply(pct_br)

    st.dataframe(uf_tbl_show, use_container_width=True, hide_index=True)
    botao_download_pdf(uf_tbl_show, "Tabela por UF", "tabela_por_uf.pdf")

    st.divider()

    # =============================
    # 5) CLIENTES POR UF (com linha de totais dinâmica)
    # =============================
    st.subheader("Clientes por UF (Faturamento × Custo × Margem)")

    ufs_disp = sorted([u for u in df_f["UF"].dropna().unique().tolist() if str(u).strip() != ""])
    uf_sel = st.selectbox("Selecione a UF", ["(Selecione)"] + ufs_disp, index=0)

    if uf_sel == "(Selecione)":
        st.info("Selecione uma UF para listar os clientes e seus indicadores no período filtrado.")
    else:
        df_uf = df_f[df_f["UF"] == uf_sel].copy()

        tab_cli = df_uf.groupby("Cliente", as_index=False).agg(
            FATURAMENTO=("Valor total", "sum"),
            VALOR_CUSTO=("Valor custo", "sum"),
        )
        tab_cli["MARGEM_BRUTA_R$"] = tab_cli["FATURAMENTO"] - tab_cli["VALOR_CUSTO"]
        tab_cli["MARGEM_BRUTA_%"] = tab_cli.apply(
            lambda r: (r["MARGEM_BRUTA_R$"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0,
            axis=1
        )

        total_uf = tab_cli["FATURAMENTO"].sum()
        tab_cli["% UF (Fat)"] = tab_cli["FATURAMENTO"].apply(lambda x: (x / total_uf) if total_uf else 0.0)

        tab_cli = tab_cli.sort_values("FATURAMENTO", ascending=False)

        tot_fat = tab_cli["FATURAMENTO"].sum()
        tot_custo = tab_cli["VALOR_CUSTO"].sum()
        tot_margem = tot_fat - tot_custo
        tot_margem_pct = (tot_margem / tot_fat) if tot_fat else 0.0

        total_row = pd.DataFrame([{
            "Cliente": "TOTAL",
            "FATURAMENTO": tot_fat,
            "VALOR_CUSTO": tot_custo,
            "MARGEM_BRUTA_R$": tot_margem,
            "MARGEM_BRUTA_%": tot_margem_pct,
            "% UF (Fat)": 1.0 if total_uf else 0.0
        }])

        tab_cli2 = pd.concat([tab_cli, total_row], ignore_index=True)

        tab_show = tab_cli2.copy()
        tab_show["FATURAMENTO"] = tab_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
        tab_show["VALOR_CUSTO"] = tab_show["VALOR_CUSTO"].apply(lambda x: f"R$ {format_brl(x)}")
        tab_show["MARGEM_BRUTA_R$"] = tab_show["MARGEM_BRUTA_R$"].apply(lambda x: f"R$ {format_brl(x)}")
        tab_show["MARGEM_BRUTA_%"] = tab_show["MARGEM_BRUTA_%"].apply(pct_br)
        tab_show["% UF (Fat)"] = tab_show["% UF (Fat)"].apply(pct_br)

        clientes_uf_pdf = tab_show[["Cliente", "FATURAMENTO", "VALOR_CUSTO", "MARGEM_BRUTA_R$", "MARGEM_BRUTA_%", "% UF (Fat)"]]
        st.dataframe(
            clientes_uf_pdf,
            use_container_width=True,
            hide_index=True
        )
        botao_download_pdf(clientes_uf_pdf, f"Clientes por UF - {uf_sel}", f"clientes_uf_{uf_sel}.pdf")

    st.divider()


with tab_clientes:
    # =============================
    # 7) RANKING DE CLIENTES (faturamento + % geral)
    # =============================
    st.subheader("Ranking de Clientes (Faturamento e % do Total)")

    rank = df_f.groupby("Cliente", as_index=False)["Valor total"].sum().sort_values("Valor total", ascending=False)
    tot_geral = rank["Valor total"].sum()
    rank["% Geral"] = rank["Valor total"].apply(lambda x: (x / tot_geral) if tot_geral else 0.0)

    rank_show = rank.copy()
    rank_show["Valor total"] = rank_show["Valor total"].apply(lambda x: f"R$ {format_brl(x)}")
    rank_show["% Geral"] = rank_show["% Geral"].apply(pct_br)

    st.dataframe(rank_show, use_container_width=True, hide_index=True)
    botao_download_pdf(rank_show, "Ranking de Clientes", "ranking_clientes.pdf")

    st.divider()

    # =============================
    # 8) EVOLUÇÃO DE VENDAS | CLIENTES (jan..dez + Total Geral) com zeros em vermelho
    # =============================
    st.subheader("Evolução de Vendas | Clientes (jan..dez)")

    top_n = st.slider("Quantos clientes mostrar (por faturamento no período)?", 10, 300, 50, step=10)

    top_clientes = rank.head(top_n)["Cliente"].tolist()
    df_ev = df_f[df_f["Cliente"].isin(top_clientes)].copy()

    pivot = df_ev.pivot_table(
        index="Cliente",
        columns="MES_NUM",
        values="Valor total",
        aggfunc="sum",
        fill_value=0.0
    )

    for m in range(1, 13):
        if m not in pivot.columns:
            pivot[m] = 0.0
    pivot = pivot[list(range(1, 13))]

    pivot.columns = [MESES_PT[m - 1] for m in pivot.columns]
    pivot["Total Geral"] = pivot.sum(axis=1)
    pivot = pivot.sort_values("Total Geral", ascending=False)

    def style_zeros_red(v):
        try:
            val = float(v)
        except Exception:
            return ""
        if val == 0.0:
            return "background-color: #ffdddd"
        return ""

    pivot_fmt = pivot.copy()
    for c in MESES_PT + ["Total Geral"]:
        pivot_fmt[c] = pivot_fmt[c].apply(lambda x: f"R$ {format_brl(x)}")

    # Compatibilidade com versões mais novas do pandas/Styler,
    # onde .applymap() pode não estar disponível no Styler.
    styler = pivot_fmt.style
    if hasattr(styler, "map"):
        styler = styler.map(style_zeros_red, subset=MESES_PT)
    elif hasattr(styler, "applymap"):
        styler = styler.applymap(style_zeros_red, subset=MESES_PT)

    st.dataframe(
        styler,
        use_container_width=True
    )
    botao_download_pdf(pivot_fmt.reset_index(), "Evolução de Vendas por Cliente", "evolucao_vendas_clientes.pdf")

    st.caption("Meses sem faturamento ficam zerados e destacados em vermelho.")

    st.divider()



with tab_class:
    # =============================
    # 6) FATURAMENTO POR CLASSIFICAÇÃO + DRILL-DOWN
    # =============================
    st.subheader("Faturamento por Tipo de Cliente (Classificação)")

    cls_tbl = df_f.copy()
    cls_tbl["CLASSIFICAÇÃO"] = cls_tbl["CLASSIFICAÇÃO"].apply(normalizar_classificacao_cliente)
    cls = (
        cls_tbl.groupby("CLASSIFICAÇÃO", as_index=False)["Valor total"].sum()
        .sort_values("Valor total", ascending=False)
    )

    fig_pizza = px.pie(
        cls, names="CLASSIFICAÇÃO", values="Valor total",
        title="Faturamento por Classificação", hole=0.35
    )
    fig_pizza.update_traces(texttemplate="%{percent:.1%}<br>R$ %{value:,.2f}")
    st.plotly_chart(fig_pizza, use_container_width=True)

    st.markdown("#### Drill-down por Classificação")
    classificacoes_disp = cls["CLASSIFICAÇÃO"].tolist()
    classificacao_sel = st.selectbox(
        "Selecione a classificação para detalhar os clientes",
        ["(Selecione)"] + classificacoes_disp,
        index=0, key="drill_classificacao_cliente"
    )

    if classificacao_sel == "(Selecione)":
        st.info("Selecione uma classificação para visualizar os clientes que a compõem.")
    else:
        df_cls = cls_tbl[cls_tbl["CLASSIFICAÇÃO"] == classificacao_sel].copy()
        total_classificacao = float(df_cls["Valor total"].sum())
        total_geral_classificacao = float(cls_tbl["Valor total"].sum())

        drill_cls = (
            df_cls.groupby("Cliente", as_index=False)["Valor total"].sum()
            .rename(columns={"Valor total": "FATURAMENTO"})
            .sort_values("FATURAMENTO", ascending=False)
        )
        drill_cls["% NA CLASSIFICAÇÃO"] = drill_cls["FATURAMENTO"].apply(
            lambda x: x / total_classificacao if total_classificacao else 0.0
        )
        drill_cls["% NO GERAL"] = drill_cls["FATURAMENTO"].apply(
            lambda x: x / total_geral_classificacao if total_geral_classificacao else 0.0
        )

        d1, d2, d3 = st.columns(3)
        d1.metric("Faturamento da classificação", f"R$ {format_brl(total_classificacao)}")
        d2.metric("Clientes", f"{drill_cls['Cliente'].nunique():,}".replace(",", "."))
        d3.metric("Participação no geral", pct_br(total_classificacao / total_geral_classificacao if total_geral_classificacao else 0.0))

        drill_show = drill_cls.copy()
        drill_show["FATURAMENTO"] = drill_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
        drill_show["% NA CLASSIFICAÇÃO"] = drill_show["% NA CLASSIFICAÇÃO"].apply(pct_br)
        drill_show["% NO GERAL"] = drill_show["% NO GERAL"].apply(pct_br)
        st.dataframe(drill_show, use_container_width=True, hide_index=True)
        botao_download_pdf(
            drill_show,
            f"Clientes - {classificacao_sel}",
            "drill_clientes_classificacao.pdf"
        )

    st.divider()


with tab_prod:
    # =============================
    # 9) PRODUTOS (BASE DE PRODUTOS)
    # =============================
    st.header("Produtos")

    required_prod = ["Produto", "Quantidade", "MÊS", "ANO", "Valor total", "Custo total"]
    missing_prod = [c for c in required_prod if c not in df_p.columns]
    if missing_prod:
        st.warning(
            "Não foi possível montar os indicadores de produtos porque faltam colunas na base consolidada de produtos: "
            + ", ".join(missing_prod)
            + "\n\nConfira se os nomes estão exatamente assim (incluindo acentos) e tente novamente."
        )
    else:
        df_prod = df_p.copy()

        # Relacionamento da nova aba LINHA: PRODUTO -> CATEGORIA -> GRUPO
        required_linha = ["PRODUTO", "CATEGORIA", "GRUPO"]
        missing_linha = [c for c in required_linha if c not in df_l.columns]
        if missing_linha:
            st.warning(
                "A aba LINHA não possui as colunas obrigatórias: " + ", ".join(missing_linha)
            )
            df_l_map = pd.DataFrame(columns=["PRODUTO_KEY", "CATEGORIA", "GRUPO"])
        else:
            df_l_map = df_l[required_linha].copy()
            df_l_map["PRODUTO_KEY"] = df_l_map["PRODUTO"].apply(normalize_product_key)
            for c in ["CATEGORIA", "GRUPO"]:
                df_l_map[c] = df_l_map[c].fillna("").astype(str).str.strip()
            df_l_map = (
                df_l_map[df_l_map["PRODUTO_KEY"] != ""]
                .drop_duplicates(subset=["PRODUTO_KEY"], keep="first")
                [["PRODUTO_KEY", "CATEGORIA", "GRUPO"]]
            )

        df_prod["Produto"] = df_prod["Produto"].astype(str).fillna("").str.strip()
        df_prod["PRODUTO_KEY"] = df_prod["Produto"].apply(normalize_product_key)
        df_prod = df_prod.merge(df_l_map, on="PRODUTO_KEY", how="left")
        df_prod["CATEGORIA"] = df_prod["CATEGORIA"].fillna("NÃO CLASSIFICADO").replace("", "NÃO CLASSIFICADO")
        df_prod["GRUPO"] = df_prod["GRUPO"].fillna("NÃO CLASSIFICADO").replace("", "NÃO CLASSIFICADO")
        df_prod["Quantidade"] = df_prod["Quantidade"].apply(parse_brl_number)
        df_prod["Valor total"] = df_prod["Valor total"].apply(parse_brl_number)
        df_prod["Custo total"] = df_prod["Custo total"].apply(parse_brl_number)

        df_prod["MES_NUM"] = df_prod["MÊS"].apply(parse_mes_to_num)

        # Usa coluna ANO para diferenciar meses repetidos (Jan..Dez e depois Jan..)
        df_prod["ANO"] = pd.to_numeric(df_prod["ANO"], errors="coerce")
        df_prod = df_prod[df_prod["ANO"].notna()].copy()

        # Filtra produtos pelo mesmo ano selecionado (Ano do filtro)
        df_prod = df_prod[df_prod["ANO"].astype(int) == int(ano_sel)].copy()

        # Filtro por meses do período selecionado (vendas)
        if meses_sel:
            df_prod_f = df_prod[df_prod["MES_NUM"].isin(meses_sel)].copy()
        else:
            df_prod_f = df_prod.copy()

        if df_prod_f.empty:
            st.info("Sem dados de produtos para os meses do período filtrado.")
        else:
            st.subheader("Tabela Mensal de Produtos (Quantidade)")

            tab_qtd = df_prod_f.pivot_table(
                index="Produto",
                columns="MES_NUM",
                values="Quantidade",
                aggfunc="sum",
                fill_value=0.0
            )

            for m in range(1, 13):
                if m not in tab_qtd.columns:
                    tab_qtd[m] = 0.0
            tab_qtd = tab_qtd[list(range(1, 13))]

            tab_qtd.columns = [MESES_PT[m - 1] for m in tab_qtd.columns]
            tab_qtd["Total (Qtd)"] = tab_qtd.sum(axis=1)
            tab_qtd = tab_qtd.sort_values("Total (Qtd)", ascending=False)

            st.dataframe(tab_qtd, use_container_width=True)
            botao_download_pdf(tab_qtd.reset_index(), "Tabela Mensal de Produtos", "tabela_mensal_produtos.pdf")

            st.subheader("Curva ABC por Quantidade (Produtos)")
            abc_qtd = abc_classification(df_prod_f, value_col="Quantidade", label_col="Produto")
            abc_qtd_show = abc_qtd.copy()
            abc_qtd_show["Quantidade"] = abc_qtd_show["Quantidade"].apply(
                lambda x: f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )
            abc_qtd_show["%"] = abc_qtd_show["%"].apply(pct_br)
            abc_qtd_show["% Acum"] = abc_qtd_show["% Acum"].apply(pct_br)
            abc_qtd_pdf = abc_qtd_show[["Produto", "Quantidade", "%", "% Acum", "Curva"]]
            st.dataframe(abc_qtd_pdf, use_container_width=True, hide_index=True)
            botao_download_pdf(abc_qtd_pdf, "Curva ABC por Quantidade", "curva_abc_quantidade.pdf")

            st.subheader("Curva ABC por Faturamento (Produtos)")
            abc_fat = abc_classification(df_prod_f, value_col="Valor total", label_col="Produto")
            abc_fat_show = abc_fat.copy()
            abc_fat_show["Valor total"] = abc_fat_show["Valor total"].apply(lambda x: f"R$ {format_brl(x)}")
            abc_fat_show["%"] = abc_fat_show["%"].apply(pct_br)
            abc_fat_show["% Acum"] = abc_fat_show["% Acum"].apply(pct_br)
            abc_fat_pdf = abc_fat_show[["Produto", "Valor total", "%", "% Acum", "Curva"]]
            st.dataframe(abc_fat_pdf, use_container_width=True, hide_index=True)
            botao_download_pdf(abc_fat_pdf, "Curva ABC por Faturamento", "curva_abc_faturamento.pdf")

            st.subheader("Ranking de Produtos (Faturamento, Custo e Margem)")

            prod_rank = df_prod_f.groupby("Produto", as_index=False).agg(
                FATURAMENTO=("Valor total", "sum"),
                CUSTO=("Custo total", "sum"),
                QTD=("Quantidade", "sum"),
            )

            prod_rank["MARGEM_BRUTA_R$"] = prod_rank["FATURAMENTO"] - prod_rank["CUSTO"]
            prod_rank["MARGEM_BRUTA_%"] = prod_rank.apply(
                lambda r: (r["MARGEM_BRUTA_R$"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0,
                axis=1
            )

            prod_rank = prod_rank.sort_values("FATURAMENTO", ascending=False)

            prod_rank_show = prod_rank.copy()
            prod_rank_show["QTD"] = prod_rank_show["QTD"].apply(
                lambda x: f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )
            prod_rank_show["FATURAMENTO"] = prod_rank_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
            prod_rank_show["CUSTO"] = prod_rank_show["CUSTO"].apply(lambda x: f"R$ {format_brl(x)}")
            prod_rank_show["MARGEM_BRUTA_R$"] = prod_rank_show["MARGEM_BRUTA_R$"].apply(lambda x: f"R$ {format_brl(x)}")
            prod_rank_show["MARGEM_BRUTA_%"] = prod_rank_show["MARGEM_BRUTA_%"].apply(pct_br)

            ranking_produtos_pdf = prod_rank_show[["Produto", "QTD", "FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$", "MARGEM_BRUTA_%"]]
            st.dataframe(
                ranking_produtos_pdf,
                use_container_width=True,
                hide_index=True
            )
            botao_download_pdf(ranking_produtos_pdf, "Ranking de Produtos", "ranking_produtos.pdf")

            st.divider()
            st.header("Mix Comercial: Grupo → Categoria → Produto")
            st.caption("O indicador utiliza a aba LINHA e respeita o ano e os meses selecionados no painel.")

            # Visão geral da representatividade por grupo
            grupo_mix = (
                df_prod_f.groupby("GRUPO", as_index=False)
                .agg(
                    FATURAMENTO=("Valor total", "sum"),
                    QUANTIDADE=("Quantidade", "sum"),
                    CATEGORIAS=("CATEGORIA", "nunique"),
                    PRODUTOS=("Produto", "nunique"),
                )
                .sort_values("FATURAMENTO", ascending=False)
            )
            total_mix = float(grupo_mix["FATURAMENTO"].sum())
            grupo_mix["REPRESENTATIVIDADE"] = grupo_mix["FATURAMENTO"].apply(
                lambda x: (x / total_mix) if total_mix else 0.0
            )

            fig_grupos = px.pie(
                grupo_mix,
                names="GRUPO",
                values="FATURAMENTO",
                title="Representatividade do Faturamento por Grupo",
                hole=0.32,
                custom_data=["REPRESENTATIVIDADE", "QUANTIDADE", "CATEGORIAS", "PRODUTOS"],
            )
            fig_grupos.update_traces(
                texttemplate="%{label}<br>%{percent:.1%}<br>R$ %{value:,.2f}",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Faturamento: R$ %{value:,.2f}<br>"
                    "Representatividade: %{percent:.2%}<br>"
                    "Quantidade: %{customdata[1]:,.0f}<br>"
                    "Categorias: %{customdata[2]}<br>"
                    "Produtos: %{customdata[3]}<extra></extra>"
                ),
            )
            st.plotly_chart(fig_grupos, use_container_width=True)

            grupos_disp = grupo_mix["GRUPO"].tolist()
            grupo_sel_mix = st.selectbox(
                "Selecione o Grupo para detalhar",
                grupos_disp,
                key="mix_grupo_sel",
            )

            df_grupo_mix = df_prod_f[df_prod_f["GRUPO"] == grupo_sel_mix].copy()
            fat_grupo_mix = float(df_grupo_mix["Valor total"].sum())
            qtd_grupo_mix = int(round(df_grupo_mix["Quantidade"].sum()))

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Faturamento do Grupo", f"R$ {format_brl(fat_grupo_mix)}")
            m2.metric("Quantidade Vendida", qa_int(qtd_grupo_mix) if "qa_int" in globals() else f"{qtd_grupo_mix:,}".replace(",", "."))
            m3.metric("Categorias", int(df_grupo_mix["CATEGORIA"].nunique()))
            m4.metric("Produtos", int(df_grupo_mix["Produto"].nunique()))

            categoria_mix = (
                df_grupo_mix.groupby("CATEGORIA", as_index=False)
                .agg(
                    FATURAMENTO=("Valor total", "sum"),
                    CUSTO=("Custo total", "sum"),
                    QUANTIDADE=("Quantidade", "sum"),
                    PRODUTOS=("Produto", "nunique"),
                )
                .sort_values("FATURAMENTO", ascending=False)
            )
            categoria_mix["MARGEM_BRUTA_R$"] = categoria_mix["FATURAMENTO"] - categoria_mix["CUSTO"]
            categoria_mix["MARGEM_BRUTA_%"] = categoria_mix.apply(
                lambda r: (r["MARGEM_BRUTA_R$"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0, axis=1
            )
            categoria_mix["REPRESENTATIVIDADE"] = categoria_mix["FATURAMENTO"].apply(
                lambda x: (x / fat_grupo_mix) if fat_grupo_mix else 0.0
            )

            fig_categorias = px.pie(
                categoria_mix,
                names="CATEGORIA",
                values="FATURAMENTO",
                title=f"Categorias dentro do Grupo: {grupo_sel_mix}",
                hole=0.32,
                custom_data=["REPRESENTATIVIDADE", "QUANTIDADE", "PRODUTOS", "MARGEM_BRUTA_%"],
            )
            fig_categorias.update_traces(
                texttemplate="%{label}<br>%{percent:.1%}<br>R$ %{value:,.2f}",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Faturamento: R$ %{value:,.2f}<br>"
                    "Representatividade no Grupo: %{percent:.2%}<br>"
                    "Quantidade: %{customdata[1]:,.0f}<br>"
                    "Produtos: %{customdata[2]}<br>"
                    "Margem Bruta: %{customdata[3]:.2%}<extra></extra>"
                ),
            )
            st.plotly_chart(fig_categorias, use_container_width=True)

            categoria_show = categoria_mix.copy()
            categoria_show["FATURAMENTO"] = categoria_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
            categoria_show["CUSTO"] = categoria_show["CUSTO"].apply(lambda x: f"R$ {format_brl(x)}")
            categoria_show["MARGEM_BRUTA_R$"] = categoria_show["MARGEM_BRUTA_R$"].apply(lambda x: f"R$ {format_brl(x)}")
            categoria_show["MARGEM_BRUTA_%"] = categoria_show["MARGEM_BRUTA_%"].apply(pct_br)
            categoria_show["REPRESENTATIVIDADE"] = categoria_show["REPRESENTATIVIDADE"].apply(pct_br)
            categoria_show["QUANTIDADE"] = categoria_show["QUANTIDADE"].apply(
                lambda x: f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )
            categoria_pdf = categoria_show[[
                "CATEGORIA", "FATURAMENTO", "REPRESENTATIVIDADE", "QUANTIDADE",
                "PRODUTOS", "CUSTO", "MARGEM_BRUTA_R$", "MARGEM_BRUTA_%"
            ]]
            st.dataframe(categoria_pdf, use_container_width=True, hide_index=True)
            botao_download_pdf(categoria_pdf, f"Mix por Categoria - {grupo_sel_mix}", "mix_categorias.pdf")

            categorias_disp = categoria_mix["CATEGORIA"].tolist()
            categoria_sel_mix = st.selectbox(
                "Selecione a Categoria para visualizar os Produtos",
                categorias_disp,
                key="mix_categoria_sel",
            )
            df_categoria_mix = df_grupo_mix[df_grupo_mix["CATEGORIA"] == categoria_sel_mix].copy()
            fat_categoria_mix = float(df_categoria_mix["Valor total"].sum())

            produto_mix = (
                df_categoria_mix.groupby("Produto", as_index=False)
                .agg(
                    FATURAMENTO=("Valor total", "sum"),
                    CUSTO=("Custo total", "sum"),
                    QUANTIDADE=("Quantidade", "sum"),
                )
                .sort_values("FATURAMENTO", ascending=False)
            )
            produto_mix["MARGEM_BRUTA_R$"] = produto_mix["FATURAMENTO"] - produto_mix["CUSTO"]
            produto_mix["MARGEM_BRUTA_%"] = produto_mix.apply(
                lambda r: (r["MARGEM_BRUTA_R$"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0, axis=1
            )
            produto_mix["REPRESENTATIVIDADE"] = produto_mix["FATURAMENTO"].apply(
                lambda x: (x / fat_categoria_mix) if fat_categoria_mix else 0.0
            )

            fig_produtos_mix = px.bar(
                produto_mix.head(30),
                x="FATURAMENTO",
                y="Produto",
                orientation="h",
                title=f"Produtos da Categoria {categoria_sel_mix} — Top 30 por Faturamento",
                custom_data=["REPRESENTATIVIDADE", "QUANTIDADE", "MARGEM_BRUTA_%"],
            )
            fig_produtos_mix.update_layout(yaxis={"categoryorder": "total ascending"})
            fig_produtos_mix.update_traces(
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Faturamento: R$ %{x:,.2f}<br>"
                    "Representatividade na Categoria: %{customdata[0]:.2%}<br>"
                    "Quantidade: %{customdata[1]:,.0f}<br>"
                    "Margem Bruta: %{customdata[2]:.2%}<extra></extra>"
                )
            )
            st.plotly_chart(fig_produtos_mix, use_container_width=True)

            produto_show = produto_mix.copy()
            produto_show["FATURAMENTO"] = produto_show["FATURAMENTO"].apply(lambda x: f"R$ {format_brl(x)}")
            produto_show["CUSTO"] = produto_show["CUSTO"].apply(lambda x: f"R$ {format_brl(x)}")
            produto_show["MARGEM_BRUTA_R$"] = produto_show["MARGEM_BRUTA_R$"].apply(lambda x: f"R$ {format_brl(x)}")
            produto_show["MARGEM_BRUTA_%"] = produto_show["MARGEM_BRUTA_%"].apply(pct_br)
            produto_show["REPRESENTATIVIDADE"] = produto_show["REPRESENTATIVIDADE"].apply(pct_br)
            produto_show["QUANTIDADE"] = produto_show["QUANTIDADE"].apply(
                lambda x: f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )
            produto_pdf = produto_show[[
                "Produto", "FATURAMENTO", "REPRESENTATIVIDADE", "QUANTIDADE",
                "CUSTO", "MARGEM_BRUTA_R$", "MARGEM_BRUTA_%"
            ]]
            st.dataframe(produto_pdf, use_container_width=True, hide_index=True)
            botao_download_pdf(produto_pdf, f"Produtos - {categoria_sel_mix}", "mix_produtos_categoria.pdf")

            nao_classificados = int(df_prod_f.loc[df_prod_f["GRUPO"] == "NÃO CLASSIFICADO", "Produto"].nunique())
            if nao_classificados:
                st.warning(
                    f"Existem {nao_classificados} produtos vendidos sem correspondência na aba LINHA. "
                    "Eles aparecem no grupo NÃO CLASSIFICADO para não serem excluídos dos totais."
                )

            st.caption("Em Produtos, o filtro é por MÊS (meses contidos no período selecionado em Vendas).")


    # =============================
