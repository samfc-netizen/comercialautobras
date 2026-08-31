import re
import io
import html
import unicodedata
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

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
    padding-top: 1.6rem !important;
    padding-bottom: 3rem !important;
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

.chat-shell {
    border-radius: 26px;
    padding: 22px;
    background: linear-gradient(180deg, #F8FBFF 0%, #EFF6FF 100%);
    border: 1px solid #DCEBFF;
    box-shadow: 0 14px 36px rgba(17, 47, 89, .10);
    margin-bottom: 16px;
}

.chat-title {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.chat-avatar {
    width: 44px;
    height: 44px;
    border-radius: 15px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #0B1F33, #2F80ED);
    color: white;
    font-weight: 900;
}

.chat-title h2 {
    margin: 0 !important;
    font-size: 26px;
    letter-spacing: -0.03em;
    color: #0B1F33 !important;
}

.chat-title p {
    margin: 2px 0 0 0;
    color: #51657D;
}

.chat-examples {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
}

.chat-chip {
    border: 1px solid #CDE0F7;
    background: white;
    color: #123E68;
    border-radius: 999px;
    padding: 8px 12px;
    font-size: 13px;
    font-weight: 700;
}

@media (max-width: 900px) {
    .autobras-cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .autobras-hero { padding: 38px 28px; }
}

</style>

""", unsafe_allow_html=True)


# =============================
# CAPA INICIAL
# =============================
if "autobras_dashboard_started" not in st.session_state:
    st.session_state["autobras_dashboard_started"] = False

if not st.session_state["autobras_dashboard_started"]:
    st.markdown("""
    <div class="autobras-cover">
        <div class="autobras-hero">
            <div class="autobras-tag">Inteligência Comercial • BI • Gestão</div>
            <h1 class="autobras-title">DASHBOARD COMERCIAL AUTOBRÁS</h1>
            <p class="autobras-subtitle">
                Painel executivo para acompanhar faturamento, margem, crescimento, clientes, regiões, produtos e oportunidades comerciais.
                A proposta é transformar a base de vendas em leitura gerencial simples, rápida e orientada à decisão.
            </p>
            <div class="autobras-cards">
                <div class="autobras-card"><strong>Vendas</strong><span>Faturamento, evolução mensal e comparativos por período.</span></div>
                <div class="autobras-card"><strong>Margem</strong><span>Margem bruta em R$, percentual e análise por cliente, UF e produto.</span></div>
                <div class="autobras-card"><strong>Clientes</strong><span>Ranking, crescimento, queda, concentração, novos e inativos.</span></div>
                <div class="autobras-card"><strong>Agente BI</strong><span>Pergunte como em um chat e receba respostas calculadas pela base.</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_inicio_1, col_inicio_2, col_inicio_3 = st.columns([1, 1.4, 1])
    with col_inicio_2:
        if st.button("Entrar no Dashboard", type="primary", use_container_width=True):
            st.session_state["autobras_dashboard_started"] = True
            st.rerun()
    st.stop()


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
        return pd.DataFrame(columns=["CLIENTE_KEY", "UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD", "CLASSIFICACAO_CAD"])

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
        return pd.DataFrame(columns=["CLIENTE_KEY", "UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD", "CLASSIFICACAO_CAD"])

    nome_col = "Nome/Razão social" if "Nome/Razão social" in d.columns else "Nome/Razao social"
    rename = {
        nome_col: "Cliente",
        "Estado": "UF_CAD",
        "Cidade": "LOCALIZACAO_CAD",
        "Bairro": "BAIRRO_CAD",
        "CATEGORIA": "CLASSIFICACAO_CAD",
    }
    for origem in list(rename):
        if origem not in d.columns:
            d[origem] = ""
    d = d.rename(columns=rename)
    d["CLIENTE_KEY"] = d["Cliente"].apply(normalize_text_key)
    for c in ["UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD"]:
        d[c] = d[c].fillna("").astype(str).str.strip()
        d.loc[d[c].apply(lambda x: bool(re.fullmatch(r"[-–—_\s]+", x)) if x else False), c] = ""
    d["CLASSIFICACAO_CAD"] = d["CLASSIFICACAO_CAD"].apply(classificar_cliente)
    return (
        d[d["CLIENTE_KEY"] != ""]
        .drop_duplicates(subset=["CLIENTE_KEY"], keep="first")
        [["CLIENTE_KEY", "UF_CAD", "LOCALIZACAO_CAD", "BAIRRO_CAD", "CLASSIFICACAO_CAD"]]
    )


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
        d["UF"] = d["UF_CAD"].fillna("").astype(str).str.strip()
        d["LOCALIZAÇÃO"] = d["LOCALIZACAO_CAD"].fillna("").astype(str).str.strip()
        d["BAIRRO"] = d["BAIRRO_CAD"].fillna("").astype(str).str.strip()
        d["CLASSIFICAÇÃO"] = d["CLASSIFICACAO_CAD"].apply(classificar_cliente)

        manter = ["DATA2", "Valor total", "Valor custo", "Cliente", "UF", "LOCALIZAÇÃO", "BAIRRO", "CLASSIFICAÇÃO"]
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
    <p>Indicadores comerciais, leitura executiva e agente de perguntas e respostas.</p>
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

df["ANO"] = df["DATA2"].dt.year
df["MES_NUM"] = df["DATA2"].dt.month
df["MES"] = df["MES_NUM"].apply(lambda m: MESES_PT[m - 1])

# Margem sempre calculada pelo código, inclusive nos arquivos mensais.
df["MARGEM_BRUTA_R$"] = df["Valor total"] - df["Valor custo"]
df["MARGEM_BRUTA_%"] = df.apply(
    lambda r: (r["MARGEM_BRUTA_R$"] / r["Valor total"]) if r["Valor total"] else 0.0,
    axis=1
)

if arquivos_mensais:
    st.caption("Arquivos mensais de vendas incorporados: " + ", ".join(arquivos_mensais))
    if df_cadastro_ext.empty:
        st.warning("Arquivos mensais encontrados, mas o arquivo CADASTRO DE CLIENTES.xlsx não foi localizado. Cidade, bairro, UF e classificação podem ficar sem preenchimento nas vendas novas.")

if arquivos_prod_mensais:
    st.caption("Arquivos mensais de produtos incorporados: " + ", ".join(arquivos_prod_mensais))

# Validação cadastral: sinaliza qualquer cliente sem UF e/ou cidade/localização.
df["UF"] = df["UF"].fillna("").astype(str).str.strip()
df["LOCALIZAÇÃO"] = df["LOCALIZAÇÃO"].fillna("").astype(str).str.strip()
mask_geo_incompleta = (df["UF"] == "") | (df["LOCALIZAÇÃO"] == "")
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

df_f = df_ano[(df_ano["DATA2"].dt.date >= d_ini) & (df_ano["DATA2"].dt.date <= d_fim)].copy()

# meses selecionados no período (para filtrar BASE DE PRODUTOS por MÊS)
meses_sel = sorted(df_f["MES_NUM"].dropna().unique().tolist())

# =============================
# KPIs
# =============================
fat_total = df_f["Valor total"].sum()
custo_total = df_f["Valor custo"].sum()
margem_rs = fat_total - custo_total
margem_pct = (margem_rs / fat_total) if fat_total else 0.0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Faturamento (R$)", f"R$ {format_brl(fat_total)}")
k2.metric("Valor Custo (R$)", f"R$ {format_brl(custo_total)}")
k3.metric("Margem Bruta (R$)", f"R$ {format_brl(margem_rs)}")
k4.metric("Margem Bruta (%)", pct_br(margem_pct))

# =============================
# INDICADOR: CRESCIMENTO ANO-1 (mesmo período)
# =============================
st.subheader("Crescimento Ano-1 (mesmo período)")

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

st.dataframe(tbl_yoy_show, use_container_width=True, hide_index=True)
botao_download_pdf(tbl_yoy_show, "Crescimento Ano-1", "crescimento_ano_1.pdf")

st.divider()

# =============================
# 1) FATURAMENTO POR MÊS (BARRAS)
# =============================
fat_mes = (
    df_f.groupby("MES_NUM", as_index=False)["Valor total"].sum()
    .sort_values("MES_NUM")
)
fat_mes["MES"] = fat_mes["MES_NUM"].apply(lambda m: MESES_PT[m - 1])

fig_fat_mes = px.bar(
    fat_mes,
    x="MES",
    y="Valor total",
    title="Faturamento Total por Mês (R$)",
    hover_data={"Valor total": ":,.2f"},
)
st.plotly_chart(fig_fat_mes, use_container_width=True)

# =============================
# 2) RELAÇÃO FINANCEIRA POR MÊS (TABELA)
# =============================
st.subheader("Relação Financeira por Mês (Tabela)")

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

st.dataframe(rel_mes_show, use_container_width=True, hide_index=True)
botao_download_pdf(rel_mes_show, "Relação Financeira por Mês", "relacao_financeira_mes.pdf")

st.divider()

# =============================
# 3) MAPA (TREEMAP) CONDICIONAL EM 1 GRÁFICO
# =============================
st.subheader("Mapa de Vendas (UF → Localização → Bairro no DF | demais: UF → Localização)")

base_map = df_f.copy()
for c in ["UF", "LOCALIZAÇÃO", "BAIRRO"]:
    base_map[c] = base_map[c].fillna("").astype(str).str.strip()
    base_map.loc[base_map[c] == "", c] = "(vazio)"

base_map["UF_UP"] = base_map["UF"].str.upper()
base_map["BAIRRO_MAPA"] = base_map.apply(
    lambda r: r["BAIRRO"] if r["UF_UP"] == "DF" else "— (sem detalhamento)",
    axis=1
)

map_agg = (
    base_map.groupby(["UF", "LOCALIZAÇÃO", "BAIRRO_MAPA"], as_index=False)
    .agg(FATURAMENTO=("Valor total", "sum"))
)

fig_map = px.treemap(
    map_agg,
    path=["UF", "LOCALIZAÇÃO", "BAIRRO_MAPA"],
    values="FATURAMENTO",
    title="Interaja no hover: caminho (UF/Localização/Bairro), Faturamento e % do Total (todas as UFs)"
)

fig_map.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "Caminho: %{currentPath}<br>"
        "Faturamento: R$ %{value:,.2f}<br>"
        "Representatividade (Total): %{percentRoot:.2%}"
        "<extra></extra>"
    )
)

st.plotly_chart(fig_map, use_container_width=True)

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

# =============================
# 6) PIZZA: FATURAMENTO POR CLASSIFICAÇÃO (TIPO DE CLIENTE)
# =============================
st.subheader("Faturamento por Tipo de Cliente (Classificação)")

cls_tbl = df_f.copy()
cls_tbl["CLASSIFICAÇÃO"] = cls_tbl["CLASSIFICAÇÃO"].fillna("").astype(str).str.strip()
cls_tbl.loc[cls_tbl["CLASSIFICAÇÃO"] == "", "CLASSIFICAÇÃO"] = "(vazio)"

cls = cls_tbl.groupby("CLASSIFICAÇÃO", as_index=False)["Valor total"].sum()
cls = cls.sort_values("Valor total", ascending=False)

fig_pizza = px.pie(
    cls,
    names="CLASSIFICAÇÃO",
    values="Valor total",
    title="Faturamento por Classificação",
)
fig_pizza.update_traces(texttemplate="%{percent:.1%}<br>R$ %{value:,.2f}")
st.plotly_chart(fig_pizza, use_container_width=True)

st.divider()

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
# 10) AGENTE DE BI - PERGUNTAS E RESPOSTAS
# =============================
st.divider()
st.markdown("""
<div class="chat-shell">
    <div class="chat-title">
        <div class="chat-avatar">BI</div>
        <div>
            <h2>Chat Comercial Inteligente</h2>
            <p>Faça perguntas sobre faturamento, margem, clientes, produtos, UF, cidades, crescimento, metas, alertas e oportunidades.</p>
        </div>
    </div>
    <div class="chat-examples">
        <span class="chat-chip">Qual foi o faturamento de maio?</span>
        <span class="chat-chip">Quais clientes caíram de março para abril?</span>
        <span class="chat-chip">Compare 2026 com 2025</span>
        <span class="chat-chip">Quais alertas comerciais existem?</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Observação técnica:
# Este agente é gratuito e não depende de API paga. Ele usa interpretação por intenção + Pandas.
# Opcionalmente, se rapidfuzz estiver instalado, ele melhora a busca aproximada por nomes de produtos/clientes.
try:
    from rapidfuzz import process as rf_process, fuzz as rf_fuzz
    RAPIDFUZZ_OK = True
except Exception:
    import difflib
    RAPIDFUZZ_OK = False


def qa_norm(txt: str) -> str:
    """Normaliza texto para interpretação de pergunta."""
    txt = _to_ascii_lower(str(txt))
    txt = re.sub(r"[^a-z0-9\s/%.,-]", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def qa_currency(v) -> str:
    return f"R$ {format_brl(float(v or 0))}"


def qa_int(v) -> str:
    try:
        return f"{float(v):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "0"


def qa_extract_top(pergunta: str, default: int = 10) -> int:
    p = qa_norm(pergunta)
    patterns = [
        r"top\s*(\d+)",
        r"(\d+)\s*(maiores|melhores|principais|clientes|produtos|cidades|ufs|estados)",
        r"listar\s*(\d+)",
        r"mostrar\s*(\d+)",
    ]
    for pat in patterns:
        m = re.search(pat, p)
        if m:
            try:
                return max(1, min(int(m.group(1)), 500))
            except Exception:
                pass
    return default


def qa_extract_months(pergunta: str) -> list:
    p = qa_norm(pergunta)
    meses = []
    # Extenso
    nomes = dict(MESES_LONG)
    nomes.update({"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6, "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12})
    for nome, num in nomes.items():
        if re.search(rf"\b{re.escape(qa_norm(nome))}\b", p) and num not in meses:
            meses.append(num)
    # Formatos 01/2026, mês 3 etc.
    for n in re.findall(r"\b(0?[1-9]|1[0-2])(?:/\d{2,4})?\b", p):
        ni = int(n)
        if ni not in meses:
            # Evita capturar top 10 como mês quando existe top antes
            if re.search(rf"top\s*{ni}\b", p):
                continue
            meses.append(ni)
    return meses


def qa_month_label(m: int) -> str:
    try:
        return MESES_PT[int(m) - 1].upper()
    except Exception:
        return "PERÍODO"


def qa_filter_month(df_base: pd.DataFrame, pergunta: str) -> tuple[pd.DataFrame, str, int | None]:
    meses = qa_extract_months(pergunta)
    if meses:
        m = meses[0]
        if "MES_NUM" in df_base.columns:
            return df_base[df_base["MES_NUM"] == m].copy(), qa_month_label(m), m
    return df_base.copy(), "período filtrado", None


def qa_extract_uf(pergunta: str) -> str | None:
    p_up = str(pergunta).upper()
    ufs_validas = sorted({str(u).upper().strip() for u in df["UF"].dropna().unique().tolist() if str(u).strip()})
    for uf in ufs_validas:
        if re.search(rf"\b{re.escape(uf)}\b", p_up):
            return uf
    return None


def qa_best_match(termo: str, opcoes: list[str], score_min: int = 55) -> str | None:
    termo = str(termo or "").strip()
    opcoes = [str(o) for o in opcoes if str(o).strip()]
    if not termo or not opcoes:
        return None
    # match direto por contém
    termo_n = qa_norm(termo)
    candidatos = [o for o in opcoes if termo_n in qa_norm(o)]
    if candidatos:
        return sorted(candidatos, key=len)[0]
    if RAPIDFUZZ_OK:
        match = rf_process.extractOne(termo, opcoes, scorer=rf_fuzz.WRatio)
        if match and match[1] >= score_min:
            return match[0]
    else:
        import difflib
        matches = difflib.get_close_matches(termo, opcoes, n=1, cutoff=score_min / 100)
        if matches:
            return matches[0]
    return None


def qa_prepare_products(df_p_original: pd.DataFrame, ano_base: int, meses_base: list[int]) -> pd.DataFrame:
    required = ["Produto", "Quantidade", "MÊS", "ANO", "Valor total", "Custo total"]
    if df_p_original is None or df_p_original.empty or any(c not in df_p_original.columns for c in required):
        return pd.DataFrame()
    d = df_p_original.copy()
    d["Produto"] = d["Produto"].astype(str).fillna("").str.strip()
    d["Quantidade"] = d["Quantidade"].apply(parse_brl_number)
    d["Valor total"] = d["Valor total"].apply(parse_brl_number)
    d["Custo total"] = d["Custo total"].apply(parse_brl_number)
    d["MES_NUM"] = d["MÊS"].apply(parse_mes_to_num)
    d["ANO"] = pd.to_numeric(d["ANO"], errors="coerce")
    d = d[d["ANO"].notna()].copy()
    d = d[d["ANO"].astype(int) == int(ano_base)].copy()
    if meses_base:
        d = d[d["MES_NUM"].isin(meses_base)].copy()
    d["MARGEM_BRUTA_R$"] = d["Valor total"] - d["Custo total"]
    d["MARGEM_BRUTA_%"] = d.apply(lambda r: (r["MARGEM_BRUTA_R$"] / r["Valor total"]) if r["Valor total"] else 0.0, axis=1)
    return d


df_prod_agent = qa_prepare_products(df_p, ano_sel, meses_sel)


def qa_format_financial_table(d: pd.DataFrame, money_cols=None, pct_cols=None, int_cols=None) -> pd.DataFrame:
    show = d.copy()
    for c in money_cols or []:
        if c in show.columns:
            show[c] = show[c].apply(qa_currency)
    for c in pct_cols or []:
        if c in show.columns:
            show[c] = show[c].apply(pct_br)
    for c in int_cols or []:
        if c in show.columns:
            show[c] = show[c].apply(qa_int)
    return show


def qa_show_table(d: pd.DataFrame, title: str, file_name: str, max_rows: int = 100):
    if d is None or d.empty:
        st.warning("Não encontrei dados para essa análise dentro dos filtros atuais.")
        return
    d2 = d.head(max_rows).copy()
    st.dataframe(d2, use_container_width=True, hide_index=True)
    botao_download_pdf(d2, title, file_name)


def qa_intent(pergunta: str) -> str:
    p = qa_norm(pergunta)

    # Intenções executivas / diretoria
    if any(x in p for x in ["alerta", "alertas", "pontos de atencao", "atenção", "risco", "riscos"]):
        return "alertas_comerciais"
    if any(x in p for x in ["oportunidade", "oportunidades", "onde focar", "foco comercial", "prioridade comercial"]):
        return "oportunidades_comerciais"
    if any(x in p for x in ["meta", "falta para bater", "falta pra bater", "quanto falta"]):
        return "meta_comercial"
    if any(x in p for x in ["previsao", "previsão", "projecao", "projeção", "fechamento do mes", "fechamento do mês"]):
        return "previsao_fechamento"
    if any(x in p for x in ["ritmo", "acima do ano anterior", "abaixo do ano anterior", "ano anterior"]):
        return "ritmo_vendas"

    # Participação, concentração e ticket médio
    if any(x in p for x in ["participacao", "participação", "representatividade", "share", "% do faturamento", "percentual do faturamento"]):
        if any(x in p for x in ["produto", "produtos"]):
            return "participacao_produtos"
        if any(x in p for x in ["cidade", "localizacao", "localização", "municipio", "município"]):
            return "participacao_cidades"
        if any(x in p for x in ["uf", "estado", "estados", "regiao", "região"]):
            return "participacao_uf"
        return "participacao_clientes"
    if any(x in p for x in ["concentracao", "concentração", "dependemos", "dependencia", "dependência", "top 10 representam", "maiores clientes representam"]):
        return "concentracao_clientes"
    if any(x in p for x in ["ticket medio", "ticket médio", "valor medio", "valor médio"]):
        if any(x in p for x in ["cliente", "clientes"]):
            return "ticket_medio_clientes"
        if any(x in p for x in ["uf", "estado", "estados"]):
            return "ticket_medio_uf"
        if any(x in p for x in ["cidade", "localizacao", "localização"]):
            return "ticket_medio_cidades"
        return "ticket_medio_geral"

    # Clientes: base, abandono e frequência
    if any(x in p for x in ["cliente medio", "cliente médio", "media por cliente", "média por cliente"]):
        return "cliente_medio"
    if any(x in p for x in ["clientes perdidos", "deixaram de comprar", "nao compraram", "não compraram", "compravam", "perdidos"]):
        return "clientes_perdidos"
    if any(x in p for x in ["clientes novos", "novos clientes", "comecaram a comprar", "começaram a comprar", "primeira compra"]):
        return "clientes_novos"
    if any(x in p for x in ["inativos", "sem comprar", "sem compra", "abandono", "risco de abandono"]):
        return "clientes_inativos"
    if any(x in p for x in ["frequencia", "frequência", "compram todo mes", "compram todo mês", "recorrentes", "recorrencia", "recorrência"]):
        return "frequencia_clientes"
    if "curva abc" in p and any(x in p for x in ["cliente", "clientes"]):
        return "abc_clientes"

    # Produtos: mix, sem venda, cross selling e margem
    if any(x in p for x in ["cross selling", "cross-selling", "venda cruzada", "compram", "mas nao compram", "mas não compram"]):
        return "cross_selling"
    if any(x in p for x in ["mix", "produtos diferentes", "quantos produtos"]):
        if any(x in p for x in ["cliente", "clientes"]):
            return "mix_por_cliente"
        if any(x in p for x in ["uf", "estado", "cidade", "localizacao", "localização"]):
            return "mix_por_regiao"
        return "mix_produtos"
    if any(x in p for x in ["sem venda", "nao venderam", "não venderam", "zerados", "produto parado", "produtos parados"]):
        return "produtos_sem_venda"
    if any(x in p for x in ["menor margem", "menores margens", "margem baixa", "margem negativa"]):
        if any(x in p for x in ["produto", "produtos"]):
            return "produtos_menor_margem"
        if any(x in p for x in ["cliente", "clientes"]):
            return "clientes_menor_margem"
        if any(x in p for x in ["uf", "estado", "cidade"]):
            return "regioes_menor_margem"
    if any(x in p for x in ["maior margem", "maiores margens", "mais rentaveis", "mais rentáveis"]):
        if any(x in p for x in ["produto", "produtos"]):
            return "top_produtos_margem"
        if any(x in p for x in ["cliente", "clientes"]):
            return "top_clientes_margem"

    # Intenções já existentes
    if any(x in p for x in ["cairam", "caiu", "queda", "perderam", "reduziram", "diminuiu", "diminuiram"]):
        if "cliente" in p:
            return "clientes_queda"
        if "produto" in p or "produtos" in p:
            return "produtos_queda"
    if any(x in p for x in ["aumentaram", "cresceram", "subiram", "evoluiram"]):
        if "cliente" in p:
            return "clientes_crescimento"
        if "produto" in p or "produtos" in p:
            return "produtos_crescimento"
    if "giro" in p and ("produto" in p or "produtos" in p):
        return "giro_produto"
    if ("produto" in p or "produtos" in p) and "margem" in p:
        return "top_produtos_margem"
    if ("produto" in p or "produtos" in p) and any(x in p for x in ["quantidade", "qtd", "vendidos", "mais vendem"]):
        return "top_produtos_quantidade"
    if "produto" in p or "produtos" in p:
        return "top_produtos_faturamento"
    if ("cliente" in p or "clientes" in p) and "margem" in p:
        return "top_clientes_margem"
    if "cliente" in p or "clientes" in p:
        return "top_clientes_faturamento"
    if any(x in p for x in ["comparativo", "ranking", "ranking de vendas", "vendas na uf", "por uf", "por estado"]):
        if any(x in p for x in ["uf", "estado", "regiao", "região"]):
            return "comparativo_uf"
    if any(x in p for x in ["uf", "estado", "regiao", "região"]):
        if "margem" in p:
            return "comparativo_uf_margem"
        if "faturamento" in p or "venda" in p or "receita" in p:
            return "faturamento_uf"
        return "comparativo_uf"
    if any(x in p for x in ["cidade", "localizacao", "localização", "municipio", "município"]):
        return "ranking_cidades"
    if any(x in p for x in ["crescimento", "cresceu", "quanto cresceu", "evolucao", "evolução"]):
        return "crescimento_mes"
    if any(x in p for x in ["faturamento", "receita", "venda", "vendas"]):
        return "faturamento_mes"
    if any(x in p for x in ["margem", "lucro bruto"]):
        return "margem_geral"
    return "desconhecido"

def qa_aggregate_sales(d: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    out = d.groupby(group_cols, as_index=False).agg(
        FATURAMENTO=("Valor total", "sum"),
        CUSTO=("Valor custo", "sum"),
        QTD_REGISTROS=("Valor total", "count"),
    )
    out["MARGEM_BRUTA_R$"] = out["FATURAMENTO"] - out["CUSTO"]
    out["MARGEM_BRUTA_%"] = out.apply(lambda r: (r["MARGEM_BRUTA_R$"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0, axis=1)
    return out



def qa_extract_years(pergunta: str) -> list[int]:
    """Extrai anos explícitos da pergunta, como 2026 e 2025."""
    anos_encontrados = []
    for y in re.findall(r"\b(20\d{2}|19\d{2})\b", str(pergunta)):
        yi = int(y)
        if yi not in anos_encontrados:
            anos_encontrados.append(yi)
    return anos_encontrados


def qa_is_year_comparison(pergunta: str) -> bool:
    p = qa_norm(pergunta)
    anos_q = qa_extract_years(pergunta)
    gatilhos = [
        "comparar", "comparativo", "comparacao", "comparação", "versus", " vs ", " contra ",
        "ano", "anos", "ano anterior", "desempenho", "evolucao", "evolução", "crescimento"
    ]
    return len(anos_q) >= 2 and any(g in f" {p} " for g in gatilhos)


def qa_prepare_products_all_years(df_p_original: pd.DataFrame) -> pd.DataFrame:
    """Prepara BASE DE PRODUTOS sem travar no ano selecionado, para comparativos ano x ano."""
    required = ["Produto", "Quantidade", "MÊS", "ANO", "Valor total", "Custo total"]
    if df_p_original is None or df_p_original.empty or any(c not in df_p_original.columns for c in required):
        return pd.DataFrame()
    d = df_p_original.copy()
    d["Produto"] = d["Produto"].astype(str).fillna("").str.strip()
    d["Quantidade"] = d["Quantidade"].apply(parse_brl_number)
    d["Valor total"] = d["Valor total"].apply(parse_brl_number)
    d["Custo total"] = d["Custo total"].apply(parse_brl_number)
    d["MES_NUM"] = d["MÊS"].apply(parse_mes_to_num)
    d["ANO"] = pd.to_numeric(d["ANO"], errors="coerce")
    d = d[d["ANO"].notna()].copy()
    d["ANO"] = d["ANO"].astype(int)
    d["MARGEM_BRUTA_R$"] = d["Valor total"] - d["Custo total"]
    d["MARGEM_BRUTA_%"] = d.apply(lambda r: (r["MARGEM_BRUTA_R$"] / r["Valor total"]) if r["Valor total"] else 0.0, axis=1)
    return d


def qa_year_dimension(pergunta: str) -> tuple[str | None, str]:
    """Define a dimensão do comparativo anual a partir da pergunta."""
    p = qa_norm(pergunta)
    if "produto" in p or "produtos" in p or "giro" in p:
        return "Produto", "produto"
    if "cliente" in p or "clientes" in p:
        return "Cliente", "cliente"
    if any(x in p for x in ["cidade", "localizacao", "localização", "municipio", "município"]):
        return "LOCALIZAÇÃO", "cidade/localização"
    if any(x in p for x in ["bairro", "bairros"]):
        return "BAIRRO", "bairro"
    if any(x in p for x in ["uf", "estado", "estados", "regiao", "região"]):
        return "UF", "UF/estado"
    if any(x in p for x in ["classificacao", "classificação", "tipo de cliente"]):
        return "CLASSIFICAÇÃO", "classificação"
    return None, "geral"


def qa_compare_years_sales(pergunta: str):
    """Compara anos na base de vendas, para geral, UF, cidade, cliente, bairro ou classificação."""
    anos_q = qa_extract_years(pergunta)
    if len(anos_q) < 2:
        st.warning("Informe dois anos na pergunta. Exemplo: comparar faturamento de 2026 com 2025.")
        return

    ano_a, ano_b = int(anos_q[0]), int(anos_q[1])
    dim_col, dim_label = qa_year_dimension(pergunta)
    top_n = qa_extract_top(pergunta, default=50)
    meses_q = qa_extract_months(pergunta)
    p = qa_norm(pergunta)

    base = df[df["ANO"].isin([ano_a, ano_b])].copy()
    if meses_q:
        base = base[base["MES_NUM"].isin(meses_q)].copy()
        periodo_txt = ", ".join(qa_month_label(m) for m in meses_q)
    else:
        periodo_txt = "ano completo"

    if base.empty:
        st.warning(f"Não encontrei dados de vendas para comparar {ano_a} com {ano_b} no período solicitado.")
        return

    metrica_base = "MARGEM_BRUTA_R$" if "margem" in p else "Valor total"
    metrica_nome = "Margem Bruta" if metrica_base == "MARGEM_BRUTA_R$" else "Faturamento"

    if dim_col is None:
        agg = base.groupby("ANO", as_index=False).agg(
            FATURAMENTO=("Valor total", "sum"),
            CUSTO=("Valor custo", "sum"),
            MARGEM_BRUTA_VALOR=("MARGEM_BRUTA_R$", "sum"),
            QTD_REGISTROS=("Valor total", "count"),
        ).rename(columns={"MARGEM_BRUTA_VALOR": "MARGEM_BRUTA_R$"})
        dados = {int(r["ANO"]): r for _, r in agg.iterrows()}
        va = float(dados.get(ano_a, {}).get("FATURAMENTO", 0.0))
        vb = float(dados.get(ano_b, {}).get("FATURAMENTO", 0.0))
        ca = float(dados.get(ano_a, {}).get("CUSTO", 0.0))
        cb = float(dados.get(ano_b, {}).get("CUSTO", 0.0))
        ma = float(dados.get(ano_a, {}).get("MARGEM_BRUTA_R$", 0.0))
        mb = float(dados.get(ano_b, {}).get("MARGEM_BRUTA_R$", 0.0))
        dif = (ma - mb) if metrica_base == "MARGEM_BRUTA_R$" else (va - vb)
        base_ref = mb if metrica_base == "MARGEM_BRUTA_R$" else vb
        var_pct = (dif / base_ref) if base_ref else 0.0
        st.success(f"Comparativo anual geral: {ano_a} x {ano_b} ({periodo_txt}). {metrica_nome} variou {qa_currency(dif)} ({pct_br(var_pct)}).")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"Faturamento {ano_a}", qa_currency(va))
        c2.metric(f"Faturamento {ano_b}", qa_currency(vb))
        c3.metric("Diferença", qa_currency(dif), pct_br(var_pct))
        c4.metric(f"Margem {ano_a}", qa_currency(ma))

        detalhe = pd.DataFrame([
            {"ANO": ano_b, "FATURAMENTO": vb, "CUSTO": cb, "MARGEM_BRUTA_R$": mb, "MARGEM_BRUTA_%": (mb / vb) if vb else 0.0},
            {"ANO": ano_a, "FATURAMENTO": va, "CUSTO": ca, "MARGEM_BRUTA_R$": ma, "MARGEM_BRUTA_%": (ma / va) if va else 0.0},
        ])
        show = qa_format_financial_table(detalhe, ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], ["MARGEM_BRUTA_%"])
        qa_show_table(show, "Comparativo Anual Geral - Agente BI", "comparativo_anual_geral_agente_bi.pdf", 10)
        return

    if dim_col not in base.columns:
        st.warning(f"A coluna {dim_col} não existe na base de vendas para fazer esse comparativo.")
        return

    agg = base.groupby([dim_col, "ANO"], as_index=False).agg(
        FATURAMENTO=("Valor total", "sum"),
        CUSTO=("Valor custo", "sum"),
        MARGEM_BRUTA_VALOR=("MARGEM_BRUTA_R$", "sum"),
        QTD_REGISTROS=("Valor total", "count"),
    ).rename(columns={"MARGEM_BRUTA_VALOR": "MARGEM_BRUTA_R$"})
    valor_col = "MARGEM_BRUTA_R$" if metrica_base == "MARGEM_BRUTA_R$" else "FATURAMENTO"
    pv = agg.pivot_table(index=dim_col, columns="ANO", values=valor_col, aggfunc="sum", fill_value=0.0).reset_index()
    for y in [ano_a, ano_b]:
        if y not in pv.columns:
            pv[y] = 0.0
    pv = pv[[dim_col, ano_b, ano_a]].copy()
    pv.columns = [dim_col, f"{metrica_nome} {ano_b}", f"{metrica_nome} {ano_a}"]
    pv["DIFERENÇA_R$"] = pv[f"{metrica_nome} {ano_a}"] - pv[f"{metrica_nome} {ano_b}"]
    pv["VARIAÇÃO_%"] = pv.apply(lambda r: (r["DIFERENÇA_R$"] / r[f"{metrica_nome} {ano_b}"]) if r[f"{metrica_nome} {ano_b}"] else (1.0 if r[f"{metrica_nome} {ano_a}"] > 0 else 0.0), axis=1)

    # Complementa com margem percentual do ano A quando a base permite.
    fat_a = agg[agg["ANO"] == ano_a][[dim_col, "FATURAMENTO", "MARGEM_BRUTA_R$"]].copy()
    fat_a["MARGEM_%_" + str(ano_a)] = fat_a.apply(lambda r: (r["MARGEM_BRUTA_R$"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0, axis=1)
    fat_a = fat_a[[dim_col, "MARGEM_%_" + str(ano_a)]]
    pv = pv.merge(fat_a, on=dim_col, how="left")

    if any(x in p for x in ["cairam", "caiu", "queda", "perderam", "reduziram", "diminuiu", "diminuiram"]):
        pv = pv[pv["DIFERENÇA_R$"] < 0].sort_values("DIFERENÇA_R$", ascending=True)
        direcao = "queda"
    elif any(x in p for x in ["aumentaram", "cresceram", "subiram", "evoluiram", "crescimento"]):
        pv = pv[pv["DIFERENÇA_R$"] > 0].sort_values("DIFERENÇA_R$", ascending=False)
        direcao = "crescimento"
    else:
        pv = pv.sort_values(f"{metrica_nome} {ano_a}", ascending=False)
        direcao = "desempenho"

    st.success(f"Comparativo anual por {dim_label}: {ano_a} x {ano_b} ({periodo_txt}), analisando {metrica_nome.lower()} e ordenado por {direcao}.")
    show = pv.head(top_n).copy()
    money_cols = [f"{metrica_nome} {ano_b}", f"{metrica_nome} {ano_a}", "DIFERENÇA_R$"]
    pct_cols = ["VARIAÇÃO_%", "MARGEM_%_" + str(ano_a)]
    show = qa_format_financial_table(show, money_cols, pct_cols)
    qa_show_table(show, f"Comparativo Anual por {dim_label} - Agente BI", f"comparativo_anual_{dim_label.replace('/', '_')}_agente_bi.pdf", top_n)


def qa_compare_years_products(pergunta: str):
    """Compara anos na BASE DE PRODUTOS."""
    anos_q = qa_extract_years(pergunta)
    if len(anos_q) < 2:
        st.warning("Informe dois anos na pergunta. Exemplo: comparar produtos de 2026 com 2025.")
        return
    ano_a, ano_b = int(anos_q[0]), int(anos_q[1])
    top_n = qa_extract_top(pergunta, default=50)
    meses_q = qa_extract_months(pergunta)
    p = qa_norm(pergunta)

    dprod_all = qa_prepare_products_all_years(df_p)
    if dprod_all.empty:
        st.warning("Não foi possível comparar produtos por ano. Confira a aba BASE DE PRODUTOS.")
        return
    base = dprod_all[dprod_all["ANO"].isin([ano_a, ano_b])].copy()
    if meses_q:
        base = base[base["MES_NUM"].isin(meses_q)].copy()
        periodo_txt = ", ".join(qa_month_label(m) for m in meses_q)
    else:
        periodo_txt = "ano completo"
    if base.empty:
        st.warning(f"Não encontrei dados de produtos para comparar {ano_a} com {ano_b} no período solicitado.")
        return

    if "margem" in p:
        valor_col = "MARGEM_BRUTA_R$"
        metrica_nome = "Margem Bruta"
    elif any(x in p for x in ["quantidade", "qtd", "giro", "vendidos"]):
        valor_col = "Quantidade"
        metrica_nome = "Quantidade/Giro"
    else:
        valor_col = "Valor total"
        metrica_nome = "Faturamento"

    agg = base.groupby(["Produto", "ANO"], as_index=False).agg(
        QTD=("Quantidade", "sum"),
        FATURAMENTO=("Valor total", "sum"),
        CUSTO=("Custo total", "sum"),
        MARGEM_BRUTA_VALOR=("MARGEM_BRUTA_R$", "sum"),
    ).rename(columns={"MARGEM_BRUTA_VALOR": "MARGEM_BRUTA_R$"})
    source_col = {"Quantidade": "QTD", "Valor total": "FATURAMENTO", "MARGEM_BRUTA_R$": "MARGEM_BRUTA_R$"}[valor_col]
    pv = agg.pivot_table(index="Produto", columns="ANO", values=source_col, aggfunc="sum", fill_value=0.0).reset_index()
    for y in [ano_a, ano_b]:
        if y not in pv.columns:
            pv[y] = 0.0
    pv = pv[["Produto", ano_b, ano_a]].copy()
    pv.columns = ["Produto", f"{metrica_nome} {ano_b}", f"{metrica_nome} {ano_a}"]
    pv["DIFERENÇA"] = pv[f"{metrica_nome} {ano_a}"] - pv[f"{metrica_nome} {ano_b}"]
    pv["VARIAÇÃO_%"] = pv.apply(lambda r: (r["DIFERENÇA"] / r[f"{metrica_nome} {ano_b}"]) if r[f"{metrica_nome} {ano_b}"] else (1.0 if r[f"{metrica_nome} {ano_a}"] > 0 else 0.0), axis=1)

    if any(x in p for x in ["cairam", "caiu", "queda", "perderam", "reduziram"]):
        pv = pv[pv["DIFERENÇA"] < 0].sort_values("DIFERENÇA", ascending=True)
        direcao = "queda"
    elif any(x in p for x in ["aumentaram", "cresceram", "subiram", "crescimento"]):
        pv = pv[pv["DIFERENÇA"] > 0].sort_values("DIFERENÇA", ascending=False)
        direcao = "crescimento"
    else:
        pv = pv.sort_values(f"{metrica_nome} {ano_a}", ascending=False)
        direcao = "desempenho"

    st.success(f"Comparativo anual de produtos: {ano_a} x {ano_b} ({periodo_txt}), analisando {metrica_nome.lower()} e ordenado por {direcao}.")
    show = pv.head(top_n).copy()
    if valor_col == "Quantidade":
        show = qa_format_financial_table(show, [], ["VARIAÇÃO_%"], [f"{metrica_nome} {ano_b}", f"{metrica_nome} {ano_a}", "DIFERENÇA"])
    else:
        show = qa_format_financial_table(show, [f"{metrica_nome} {ano_b}", f"{metrica_nome} {ano_a}", "DIFERENÇA"], ["VARIAÇÃO_%"])
    qa_show_table(show, "Comparativo Anual de Produtos - Agente BI", "comparativo_anual_produtos_agente_bi.pdf", top_n)


# =============================
# INTENÇÕES ESTRATÉGICAS ADICIONAIS DO AGENTE
# =============================
def qa_extract_number_value(pergunta: str) -> float | None:
    """Extrai valor monetário/numérico da pergunta para uso em metas."""
    txt = str(pergunta).lower().replace("r$", " ")
    mult = 1.0
    if "milhao" in qa_norm(txt) or "milhão" in txt or "milhoes" in qa_norm(txt) or "milhões" in txt:
        mult = 1_000_000.0
    elif " mil" in f" {txt} ":
        mult = 1_000.0
    nums = re.findall(r"\d+(?:[\.\,]\d+)*", txt)
    if not nums:
        return None
    raw = nums[-1]
    val = parse_brl_number(raw)
    return val * mult if val else None


def qa_extract_days(pergunta: str, default: int = 90) -> int:
    p = qa_norm(pergunta)
    m = re.search(r"(\d+)\s*dias", p)
    if m:
        return max(1, int(m.group(1)))
    m = re.search(r"(\d+)\s*mes", p)
    if m:
        return max(1, int(m.group(1)) * 30)
    return default


def qa_table_participacao(d: pd.DataFrame, group_col: str, titulo: str, nome_pdf: str, top_n: int = 50):
    if group_col not in d.columns or d.empty:
        st.warning("Não encontrei dados suficientes para calcular participação.")
        return
    out = qa_aggregate_sales(d, [group_col]).sort_values("FATURAMENTO", ascending=False)
    total = float(out["FATURAMENTO"].sum())
    out["PARTICIPAÇÃO_%"] = out["FATURAMENTO"].apply(lambda x: (x / total) if total else 0.0)
    st.success(f"Participação por {group_col}: total analisado de {qa_currency(total)}.")
    show = qa_format_financial_table(out.head(top_n), ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], ["MARGEM_BRUTA_%", "PARTICIPAÇÃO_%"], ["QTD_REGISTROS"])
    qa_show_table(show, titulo, nome_pdf, top_n)


def qa_ticket_medio(d: pd.DataFrame, group_col: str | None, titulo: str, nome_pdf: str, top_n: int = 50):
    if d.empty:
        st.warning("Não encontrei dados para calcular ticket médio.")
        return
    if group_col is None:
        pedidos = int(len(d))
        fat = float(d["Valor total"].sum())
        ticket = fat / pedidos if pedidos else 0.0
        clientes = int(d["Cliente"].nunique()) if "Cliente" in d.columns else 0
        cliente_medio = fat / clientes if clientes else 0.0
        st.success(f"Ticket médio geral: {qa_currency(ticket)} por registro/pedido.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento", qa_currency(fat))
        c2.metric("Qtd. registros/pedidos", qa_int(pedidos))
        c3.metric("Ticket médio", qa_currency(ticket))
        st.info(f"Valor médio por cliente ativo no período: {qa_currency(cliente_medio)}.")
        return
    if group_col not in d.columns:
        st.warning(f"A coluna {group_col} não existe na base.")
        return
    out = d.groupby(group_col, as_index=False).agg(
        FATURAMENTO=("Valor total", "sum"),
        QTD_REGISTROS=("Valor total", "count"),
        CLIENTES=("Cliente", "nunique"),
    )
    out["TICKET_MEDIO"] = out.apply(lambda r: (r["FATURAMENTO"] / r["QTD_REGISTROS"]) if r["QTD_REGISTROS"] else 0.0, axis=1)
    out["CLIENTE_MEDIO"] = out.apply(lambda r: (r["FATURAMENTO"] / r["CLIENTES"]) if r["CLIENTES"] else 0.0, axis=1)
    out = out.sort_values("FATURAMENTO", ascending=False).head(top_n)
    show = qa_format_financial_table(out, ["FATURAMENTO", "TICKET_MEDIO", "CLIENTE_MEDIO"], [], ["QTD_REGISTROS", "CLIENTES"])
    qa_show_table(show, titulo, nome_pdf, top_n)


def qa_clientes_perdidos_novos(pergunta: str, tipo: str, top_n: int = 100):
    anos_q = qa_extract_years(pergunta)
    if len(anos_q) >= 2:
        ano_atual, ano_base = int(anos_q[0]), int(anos_q[1])
    else:
        ano_atual, ano_base = int(ano_sel), int(ano_sel) - 1
    meses_q = qa_extract_months(pergunta)
    base_ant = df[df["ANO"] == ano_base].copy()
    base_atual = df[df["ANO"] == ano_atual].copy()
    if meses_q:
        base_ant = base_ant[base_ant["MES_NUM"].isin(meses_q)].copy()
        base_atual = base_atual[base_atual["MES_NUM"].isin(meses_q)].copy()
    cli_ant = set(base_ant["Cliente"].dropna().astype(str))
    cli_atual = set(base_atual["Cliente"].dropna().astype(str))
    alvo = (cli_ant - cli_atual) if tipo == "perdidos" else (cli_atual - cli_ant)
    base_ref = base_ant if tipo == "perdidos" else base_atual
    out = qa_aggregate_sales(base_ref[base_ref["Cliente"].astype(str).isin(alvo)], ["Cliente"]).sort_values("FATURAMENTO", ascending=False)
    st.success(f"Clientes {tipo}: {len(alvo)} cliente(s) comparando {ano_atual} com {ano_base}.")
    show = qa_format_financial_table(out.head(top_n), ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], ["MARGEM_BRUTA_%"], ["QTD_REGISTROS"])
    qa_show_table(show, f"Clientes {tipo.title()} - Agente BI", f"clientes_{tipo}_agente_bi.pdf", top_n)


def qa_clientes_inativos(pergunta: str, top_n: int = 100):
    dias = qa_extract_days(pergunta, default=90)
    hoje = pd.Timestamp.today().normalize()
    if int(ano_sel) < hoje.year:
        hoje = df_ano["DATA2"].max().normalize()
    limite = hoje - pd.Timedelta(days=dias)
    ult = df_ano.groupby("Cliente", as_index=False).agg(
        ULTIMA_COMPRA=("DATA2", "max"),
        FATURAMENTO=("Valor total", "sum"),
        QTD_REGISTROS=("Valor total", "count"),
    )
    out = ult[ult["ULTIMA_COMPRA"] < limite].copy()
    out["DIAS_SEM_COMPRA"] = (hoje - out["ULTIMA_COMPRA"]).dt.days
    out = out.sort_values("DIAS_SEM_COMPRA", ascending=False).head(top_n)
    out["ULTIMA_COMPRA"] = out["ULTIMA_COMPRA"].dt.strftime("%d/%m/%Y")
    show = qa_format_financial_table(out, ["FATURAMENTO"], [], ["QTD_REGISTROS", "DIAS_SEM_COMPRA"])
    st.success(f"Clientes sem compra há mais de {dias} dias: {len(out)} exibidos.")
    qa_show_table(show, "Clientes Inativos - Agente BI", "clientes_inativos_agente_bi.pdf", top_n)


def qa_frequencia_clientes(top_n: int = 100):
    meses_ano = max(1, int(df_ano["MES_NUM"].nunique()))
    out = df_ano.groupby("Cliente", as_index=False).agg(
        MESES_COM_COMPRA=("MES_NUM", "nunique"),
        FATURAMENTO=("Valor total", "sum"),
        QTD_REGISTROS=("Valor total", "count"),
    )
    out["FREQUÊNCIA_%"] = out["MESES_COM_COMPRA"] / meses_ano
    out = out.sort_values(["MESES_COM_COMPRA", "FATURAMENTO"], ascending=[False, False]).head(top_n)
    show = qa_format_financial_table(out, ["FATURAMENTO"], ["FREQUÊNCIA_%"], ["MESES_COM_COMPRA", "QTD_REGISTROS"])
    st.success(f"Frequência de compra por cliente considerando {meses_ano} mês(es) disponíveis no ano selecionado.")
    qa_show_table(show, "Frequência de Clientes - Agente BI", "frequencia_clientes_agente_bi.pdf", top_n)


def qa_abc_clientes(top_n: int = 500):
    abc = abc_classification(df_ano, value_col="Valor total", label_col="Cliente")
    abc = abc.rename(columns={"Valor total": "FATURAMENTO", "%": "PARTICIPAÇÃO_%", "% Acum": "PARTICIPAÇÃO_ACUM_%", "Curva": "CURVA"})
    resumo = abc.groupby("CURVA", as_index=False).agg(CLIENTES=("Cliente", "count"), FATURAMENTO=("FATURAMENTO", "sum"))
    total = float(abc["FATURAMENTO"].sum())
    resumo["PARTICIPAÇÃO_%"] = resumo["FATURAMENTO"].apply(lambda x: (x / total) if total else 0.0)
    st.success("Curva ABC de clientes gerada por faturamento.")
    st.dataframe(qa_format_financial_table(resumo, ["FATURAMENTO"], ["PARTICIPAÇÃO_%"], ["CLIENTES"]), use_container_width=True, hide_index=True)
    show = qa_format_financial_table(abc.head(top_n), ["FATURAMENTO"], ["PARTICIPAÇÃO_%", "PARTICIPAÇÃO_ACUM_%"])
    qa_show_table(show, "Curva ABC Clientes - Agente BI", "curva_abc_clientes_agente_bi.pdf", top_n)


def qa_concentracao_clientes(top_n: int = 10):
    out = qa_aggregate_sales(df_ano, ["Cliente"]).sort_values("FATURAMENTO", ascending=False)
    total = float(out["FATURAMENTO"].sum())
    top = float(out.head(top_n)["FATURAMENTO"].sum())
    part = top / total if total else 0.0
    st.success(f"Os top {top_n} clientes representam {pct_br(part)} do faturamento do ano selecionado.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Faturamento Total", qa_currency(total))
    c2.metric(f"Top {top_n}", qa_currency(top))
    c3.metric("Concentração", pct_br(part))
    show = qa_format_financial_table(out.head(top_n), ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], ["MARGEM_BRUTA_%"], ["QTD_REGISTROS"])
    qa_show_table(show, "Concentração de Clientes - Agente BI", "concentracao_clientes_agente_bi.pdf", top_n)


def qa_produtos_sem_venda(top_n: int = 500):
    if df_prod_agent.empty:
        st.warning("Não foi possível analisar produtos sem venda. Confira a aba BASE DE PRODUTOS.")
        return
    todos = set(df_prod_agent["Produto"].dropna().astype(str))
    vendidos = set(df_prod_agent[df_prod_agent["Quantidade"] > 0]["Produto"].dropna().astype(str))
    sem = sorted(todos - vendidos)
    out = pd.DataFrame({"Produto": sem})
    st.success(f"Produtos sem venda no período filtrado: {len(sem)}.")
    qa_show_table(out.head(top_n), "Produtos Sem Venda - Agente BI", "produtos_sem_venda_agente_bi.pdf", top_n)


def qa_mix_produtos(pergunta: str, top_n: int = 100):
    p = qa_norm(pergunta)
    if df_prod_agent.empty:
        st.warning("Não foi possível analisar mix. Confira a aba BASE DE PRODUTOS.")
        return
    if "Cliente" in df.columns and any(x in p for x in ["cliente", "clientes"]):
        # A BASE DE PRODUTOS pode não ter cliente. Usa a base de vendas se Produto existir nela; caso contrário, informa limitação.
        if "Produto" not in df_ano.columns:
            st.warning("Para mix por cliente, a aba de vendas precisa ter a coluna Produto. Na base atual, o mix detalhado está na BASE DE PRODUTOS sem vínculo por cliente.")
            return
    total_produtos = int(df_prod_agent[df_prod_agent["Quantidade"] > 0]["Produto"].nunique())
    fat = float(df_prod_agent["Valor total"].sum())
    st.success(f"Mix vendido no período: {total_produtos} produto(s) diferentes, com faturamento de {qa_currency(fat)}.")
    out = df_prod_agent.groupby("Produto", as_index=False).agg(QTD=("Quantidade", "sum"), FATURAMENTO=("Valor total", "sum"))
    out = out[out["QTD"] > 0].sort_values("FATURAMENTO", ascending=False).head(top_n)
    show = qa_format_financial_table(out, ["FATURAMENTO"], [], ["QTD"])
    qa_show_table(show, "Mix de Produtos - Agente BI", "mix_produtos_agente_bi.pdf", top_n)


def qa_menor_margem(d: pd.DataFrame, group_col: str, titulo: str, nome_pdf: str, top_n: int = 50):
    out = qa_aggregate_sales(d, [group_col])
    out = out.sort_values("MARGEM_BRUTA_%", ascending=True).head(top_n)
    st.success(f"Menores margens por {group_col}.")
    show = qa_format_financial_table(out, ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], ["MARGEM_BRUTA_%"], ["QTD_REGISTROS"])
    qa_show_table(show, titulo, nome_pdf, top_n)


def qa_produtos_menor_margem(top_n: int = 50):
    if df_prod_agent.empty:
        st.warning("Não foi possível analisar margem de produtos. Confira a aba BASE DE PRODUTOS.")
        return
    out = df_prod_agent.groupby("Produto", as_index=False).agg(
        FATURAMENTO=("Valor total", "sum"), CUSTO=("Custo total", "sum"), QTD=("Quantidade", "sum")
    )
    out["MARGEM_BRUTA_R$"] = out["FATURAMENTO"] - out["CUSTO"]
    out["MARGEM_BRUTA_%"] = out.apply(lambda r: (r["MARGEM_BRUTA_R$"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0, axis=1)
    out = out[out["FATURAMENTO"] > 0].sort_values("MARGEM_BRUTA_%", ascending=True).head(top_n)
    show = qa_format_financial_table(out, ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], ["MARGEM_BRUTA_%"], ["QTD"])
    qa_show_table(show, "Produtos com Menor Margem - Agente BI", "produtos_menor_margem_agente_bi.pdf", top_n)


def qa_cross_selling(pergunta: str, top_n: int = 100):
    if "Produto" not in df_ano.columns:
        st.warning("Para cross selling, a aba RELATÓRIO DE VENDAS precisa ter uma coluna Produto vinculada ao cliente. Na base atual, produtos e clientes parecem estar em abas separadas.")
        return
    p = qa_norm(pergunta)
    produtos = sorted(df_ano["Produto"].dropna().astype(str).unique().tolist())
    # tenta capturar termos depois de 'compram' e 'nao compram'
    partes = re.split(r"mas nao compram|mas não compram", p)
    if len(partes) < 2:
        st.warning("Escreva assim: clientes que compram produto A mas não compram produto B.")
        return
    termo_a = partes[0].replace("clientes que compram", "").replace("compram", "").strip()
    termo_b = partes[1].strip()
    prod_a = qa_best_match(termo_a, produtos, 40)
    prod_b = qa_best_match(termo_b, produtos, 40)
    if not prod_a or not prod_b:
        st.warning("Não consegui identificar os dois produtos para venda cruzada.")
        return
    cli_a = set(df_ano[df_ano["Produto"] == prod_a]["Cliente"].astype(str))
    cli_b = set(df_ano[df_ano["Produto"] == prod_b]["Cliente"].astype(str))
    alvo = cli_a - cli_b
    base = df_ano[df_ano["Cliente"].astype(str).isin(alvo)]
    out = qa_aggregate_sales(base, ["Cliente"]).sort_values("FATURAMENTO", ascending=False).head(top_n)
    st.success(f"Clientes que compram '{prod_a}' mas não compram '{prod_b}': {len(alvo)}.")
    show = qa_format_financial_table(out, ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], ["MARGEM_BRUTA_%"], ["QTD_REGISTROS"])
    qa_show_table(show, "Cross Selling - Agente BI", "cross_selling_agente_bi.pdf", top_n)


def qa_alertas_comerciais():
    alertas = []
    fat = float(df_ano["Valor total"].sum())
    margem = float(df_ano["MARGEM_BRUTA_R$"].sum())
    margem_pct = margem / fat if fat else 0.0
    if margem_pct < 0.25:
        alertas.append({"Alerta": "Margem bruta abaixo de 25%", "Impacto": pct_br(margem_pct), "Ação sugerida": "Revisar preços, descontos e produtos de baixa margem."})
    conc = qa_aggregate_sales(df_ano, ["Cliente"]).sort_values("FATURAMENTO", ascending=False)
    if not conc.empty:
        part_top10 = float(conc.head(10)["FATURAMENTO"].sum()) / fat if fat else 0.0
        if part_top10 > 0.5:
            alertas.append({"Alerta": "Alta concentração nos top 10 clientes", "Impacto": pct_br(part_top10), "Ação sugerida": "Ampliar carteira ativa e reduzir dependência."})
    # clientes que compraram em meses anteriores e não compraram no último mês disponível
    ult_mes = int(df_ano["MES_NUM"].max()) if not df_ano.empty else None
    if ult_mes:
        cli_antes = set(df_ano[df_ano["MES_NUM"] < ult_mes]["Cliente"].astype(str))
        cli_ult = set(df_ano[df_ano["MES_NUM"] == ult_mes]["Cliente"].astype(str))
        perdidos_mes = len(cli_antes - cli_ult)
        if perdidos_mes > 0:
            alertas.append({"Alerta": f"Clientes sem compra em {qa_month_label(ult_mes)}", "Impacto": qa_int(perdidos_mes), "Ação sugerida": "Gerar lista de reativação para o time comercial."})
    if not alertas:
        alertas.append({"Alerta": "Nenhum alerta crítico automático encontrado", "Impacto": "—", "Ação sugerida": "Manter acompanhamento de margem, clientes e regiões."})
    st.success("Alertas comerciais automáticos gerados.")
    st.dataframe(pd.DataFrame(alertas), use_container_width=True, hide_index=True)


def qa_oportunidades_comerciais(top_n: int = 20):
    oportunidades = []
    uf = qa_aggregate_sales(df_ano, ["UF"]).sort_values("MARGEM_BRUTA_%", ascending=False)
    if not uf.empty:
        for _, r in uf.head(5).iterrows():
            oportunidades.append({"Oportunidade": f"Expandir foco na UF {r['UF']}", "Base": qa_currency(r["FATURAMENTO"]), "Motivo": f"Margem de {pct_br(r['MARGEM_BRUTA_%'])}."})
    clientes = qa_aggregate_sales(df_ano, ["Cliente"]).sort_values("FATURAMENTO", ascending=False)
    if not clientes.empty:
        for _, r in clientes.head(5).iterrows():
            oportunidades.append({"Oportunidade": f"Proteger/expandir cliente {r['Cliente']}", "Base": qa_currency(r["FATURAMENTO"]), "Motivo": "Cliente relevante na curva de faturamento."})
    if df_prod_agent is not None and not df_prod_agent.empty:
        prod = df_prod_agent.groupby("Produto", as_index=False).agg(FATURAMENTO=("Valor total", "sum"), MARGEM=("MARGEM_BRUTA_R$", "sum"))
        prod["MARGEM_%"] = prod.apply(lambda r: (r["MARGEM"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0, axis=1)
        prod = prod.sort_values("MARGEM_%", ascending=False).head(5)
        for _, r in prod.iterrows():
            oportunidades.append({"Oportunidade": f"Priorizar produto {r['Produto']}", "Base": qa_currency(r["FATURAMENTO"]), "Motivo": f"Produto com margem de {pct_br(r['MARGEM_%'])}."})
    st.success("Oportunidades comerciais automáticas geradas.")
    qa_show_table(pd.DataFrame(oportunidades).head(top_n), "Oportunidades Comerciais - Agente BI", "oportunidades_comerciais_agente_bi.pdf", top_n)


def qa_meta_comercial(pergunta: str):
    meta = qa_extract_number_value(pergunta)
    if not meta:
        st.warning("Informe a meta na pergunta. Exemplo: quanto falta para bater a meta de R$ 1.000.000?")
        return
    realizado = float(df_f["Valor total"].sum())
    falta = max(meta - realizado, 0.0)
    pct_meta = realizado / meta if meta else 0.0
    st.success(f"Realizado de {qa_currency(realizado)} contra meta de {qa_currency(meta)}. Falta {qa_currency(falta)}.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Meta", qa_currency(meta))
    c2.metric("Realizado", qa_currency(realizado), pct_br(pct_meta))
    c3.metric("Falta", qa_currency(falta))


def qa_previsao_fechamento():
    if df_f.empty:
        st.warning("Não há dados no período filtrado para previsão.")
        return
    ini = pd.Timestamp(d_ini)
    fim = pd.Timestamp(d_fim)
    datas_venda = sorted(df_f["DATA2"].dt.normalize().unique())
    dias_com_venda = len(datas_venda)
    realizado = float(df_f["Valor total"].sum())
    media_dia = realizado / dias_com_venda if dias_com_venda else 0.0
    dias_uteis_periodo = len(pd.bdate_range(ini, fim))
    previsao = media_dia * dias_uteis_periodo
    st.success(f"Previsão de fechamento pelo ritmo atual: {qa_currency(previsao)}.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Realizado", qa_currency(realizado))
    c2.metric("Dias com venda", qa_int(dias_com_venda))
    c3.metric("Média/dia", qa_currency(media_dia))
    c4.metric("Previsão", qa_currency(previsao))


def qa_ritmo_vendas():
    ano_ant = int(ano_sel) - 1
    atual = float(df_f["Valor total"].sum())
    ini_ant = (pd.Timestamp(d_ini) - pd.DateOffset(years=1)).date()
    fim_ant = (pd.Timestamp(d_fim) - pd.DateOffset(years=1)).date()
    base_ant = df[(df["ANO"] == ano_ant) & (df["DATA2"].dt.date >= ini_ant) & (df["DATA2"].dt.date <= fim_ant)]
    ant = float(base_ant["Valor total"].sum())
    dif = atual - ant
    pct = dif / ant if ant else 0.0
    status = "acima" if dif >= 0 else "abaixo"
    st.success(f"O ritmo atual está {status} do ano anterior em {qa_currency(abs(dif))} ({pct_br(pct)}).")
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{ano_sel}", qa_currency(atual))
    c2.metric(f"{ano_ant}", qa_currency(ant))
    c3.metric("Diferença", qa_currency(dif), pct_br(pct))

def qa_answer(pergunta: str):
    pergunta = str(pergunta or "").strip()
    if not pergunta:
        st.info("Digite uma pergunta para o agente responder.")
        return

    intent = qa_intent(pergunta)
    top_n = qa_extract_top(pergunta)
    d_mes, label_periodo, mes_num = qa_filter_month(df_ano, pergunta)
    pnorm = qa_norm(pergunta)

    # Comparativo ano x ano: 2026 x 2025, 2025 x 2024 etc.
    # Esta camada vem antes das intenções de mês, porque usa a base completa e não apenas o ano do filtro lateral.
    if qa_is_year_comparison(pergunta):
        if "produto" in pnorm or "produtos" in pnorm or "giro" in pnorm:
            qa_compare_years_products(pergunta)
        else:
            qa_compare_years_sales(pergunta)
        return

    with st.caption(f"Intenção identificada: {intent} | Base: {label_periodo} | Ano: {ano_sel}"):
        pass

    # =============================
    # Intenções estratégicas adicionadas
    # =============================
    if intent == "participacao_clientes":
        qa_table_participacao(d_mes, "Cliente", "Participação por Cliente - Agente BI", "participacao_clientes_agente_bi.pdf", top_n)
        return
    if intent == "participacao_uf":
        qa_table_participacao(d_mes, "UF", "Participação por UF - Agente BI", "participacao_uf_agente_bi.pdf", top_n)
        return
    if intent == "participacao_cidades":
        qa_table_participacao(d_mes, "LOCALIZAÇÃO", "Participação por Cidade - Agente BI", "participacao_cidades_agente_bi.pdf", top_n)
        return
    if intent == "participacao_produtos":
        if df_prod_agent.empty:
            st.warning("Não foi possível calcular participação de produtos. Confira a aba BASE DE PRODUTOS.")
        else:
            out = df_prod_agent.groupby("Produto", as_index=False).agg(FATURAMENTO=("Valor total", "sum"), QTD=("Quantidade", "sum"))
            total = float(out["FATURAMENTO"].sum())
            out["PARTICIPAÇÃO_%"] = out["FATURAMENTO"].apply(lambda x: (x / total) if total else 0.0)
            out = out.sort_values("FATURAMENTO", ascending=False).head(top_n)
            show = qa_format_financial_table(out, ["FATURAMENTO"], ["PARTICIPAÇÃO_%"], ["QTD"])
            qa_show_table(show, "Participação por Produto - Agente BI", "participacao_produtos_agente_bi.pdf", top_n)
        return
    if intent == "concentracao_clientes":
        qa_concentracao_clientes(top_n=max(10, top_n))
        return
    if intent == "ticket_medio_geral":
        qa_ticket_medio(d_mes, None, "Ticket Médio Geral - Agente BI", "ticket_medio_geral_agente_bi.pdf", top_n)
        return
    if intent == "ticket_medio_clientes":
        qa_ticket_medio(d_mes, "Cliente", "Ticket Médio por Cliente - Agente BI", "ticket_medio_clientes_agente_bi.pdf", top_n)
        return
    if intent == "ticket_medio_uf":
        qa_ticket_medio(d_mes, "UF", "Ticket Médio por UF - Agente BI", "ticket_medio_uf_agente_bi.pdf", top_n)
        return
    if intent == "ticket_medio_cidades":
        qa_ticket_medio(d_mes, "LOCALIZAÇÃO", "Ticket Médio por Cidade - Agente BI", "ticket_medio_cidades_agente_bi.pdf", top_n)
        return
    if intent == "cliente_medio":
        fat = float(d_mes["Valor total"].sum())
        qtd_cli = int(d_mes["Cliente"].nunique()) if "Cliente" in d_mes.columns else 0
        media = fat / qtd_cli if qtd_cli else 0.0
        st.success(f"Cliente médio no período: {qa_currency(media)}.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento", qa_currency(fat))
        c2.metric("Clientes ativos", qa_int(qtd_cli))
        c3.metric("Cliente médio", qa_currency(media))
        return
    if intent == "clientes_perdidos":
        qa_clientes_perdidos_novos(pergunta, "perdidos", top_n)
        return
    if intent == "clientes_novos":
        qa_clientes_perdidos_novos(pergunta, "novos", top_n)
        return
    if intent == "clientes_inativos":
        qa_clientes_inativos(pergunta, top_n)
        return
    if intent == "frequencia_clientes":
        qa_frequencia_clientes(top_n)
        return
    if intent == "abc_clientes":
        qa_abc_clientes(top_n=max(top_n, 100))
        return
    if intent == "produtos_sem_venda":
        qa_produtos_sem_venda(top_n=max(top_n, 100))
        return
    if intent in ["mix_produtos", "mix_por_cliente", "mix_por_regiao"]:
        qa_mix_produtos(pergunta, top_n)
        return
    if intent == "cross_selling":
        qa_cross_selling(pergunta, top_n)
        return
    if intent == "produtos_menor_margem":
        qa_produtos_menor_margem(top_n)
        return
    if intent == "clientes_menor_margem":
        qa_menor_margem(d_mes, "Cliente", "Clientes com Menor Margem - Agente BI", "clientes_menor_margem_agente_bi.pdf", top_n)
        return
    if intent == "regioes_menor_margem":
        grupo = "UF" if any(x in pnorm for x in ["uf", "estado"]) else "LOCALIZAÇÃO"
        qa_menor_margem(d_mes, grupo, "Regiões com Menor Margem - Agente BI", "regioes_menor_margem_agente_bi.pdf", top_n)
        return
    if intent == "alertas_comerciais":
        qa_alertas_comerciais()
        return
    if intent == "oportunidades_comerciais":
        qa_oportunidades_comerciais(top_n)
        return
    if intent == "meta_comercial":
        qa_meta_comercial(pergunta)
        return
    if intent == "previsao_fechamento":
        qa_previsao_fechamento()
        return
    if intent == "ritmo_vendas":
        qa_ritmo_vendas()
        return

    if intent == "faturamento_mes":
        fat = float(d_mes["Valor total"].sum())
        custo = float(d_mes["Valor custo"].sum())
        margem = fat - custo
        margem_pct = (margem / fat) if fat else 0.0
        st.success(f"O faturamento de {label_periodo} foi de {qa_currency(fat)}.")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Faturamento", qa_currency(fat))
        c2.metric("Custo", qa_currency(custo))
        c3.metric("Margem Bruta", qa_currency(margem))
        c4.metric("Margem %", pct_br(margem_pct))
        return

    if intent == "margem_geral":
        fat = float(d_mes["Valor total"].sum())
        custo = float(d_mes["Valor custo"].sum())
        margem = fat - custo
        margem_pct = (margem / fat) if fat else 0.0
        st.success(f"A margem bruta de {label_periodo} foi de {qa_currency(margem)}, equivalente a {pct_br(margem_pct)} do faturamento.")
        return

    if intent == "crescimento_mes":
        meses = qa_extract_months(pergunta)
        if len(meses) >= 2:
            m1, m2 = meses[0], meses[1]
            fat1 = float(df_ano[df_ano["MES_NUM"] == m1]["Valor total"].sum())
            fat2 = float(df_ano[df_ano["MES_NUM"] == m2]["Valor total"].sum())
            dif = fat2 - fat1
            pct = (dif / fat1) if fat1 else 0.0
            st.success(f"De {qa_month_label(m1)} para {qa_month_label(m2)}, o faturamento variou {qa_currency(dif)} ({pct_br(pct)}).")
            c1, c2, c3 = st.columns(3)
            c1.metric(qa_month_label(m1), qa_currency(fat1))
            c2.metric(qa_month_label(m2), qa_currency(fat2))
            c3.metric("Variação", qa_currency(dif), pct_br(pct))
            return
        if mes_num is None:
            st.warning("Informe o mês. Exemplo: qual foi o crescimento de abril?")
            return
        atual = float(df_ano[df_ano["MES_NUM"] == mes_num]["Valor total"].sum())
        mes_ant = mes_num - 1
        if mes_ant >= 1:
            base = float(df_ano[df_ano["MES_NUM"] == mes_ant]["Valor total"].sum())
            label_base = qa_month_label(mes_ant)
        else:
            ano_ant_q = int(ano_sel) - 1
            base = float(df[(df["ANO"] == ano_ant_q) & (df["MES_NUM"] == 12)]["Valor total"].sum())
            label_base = f"DEZ/{ano_ant_q}"
        dif = atual - base
        pct = (dif / base) if base else 0.0
        st.success(f"Em {qa_month_label(mes_num)}, o crescimento foi de {qa_currency(dif)} ({pct_br(pct)}) contra {label_base}.")
        c1, c2, c3 = st.columns(3)
        c1.metric(qa_month_label(mes_num), qa_currency(atual))
        c2.metric(label_base, qa_currency(base))
        c3.metric("Crescimento", qa_currency(dif), pct_br(pct))
        return

    if intent in ["top_clientes_faturamento", "top_clientes_margem"]:
        out = qa_aggregate_sales(d_mes, ["Cliente"])
        ordem = "MARGEM_BRUTA_R$" if intent == "top_clientes_margem" else "FATURAMENTO"
        out = out.sort_values(ordem, ascending=False).head(top_n)
        st.success(f"Top {top_n} clientes por {'margem bruta' if ordem == 'MARGEM_BRUTA_R$' else 'faturamento'} em {label_periodo}.")
        show = qa_format_financial_table(out, ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], ["MARGEM_BRUTA_%"], ["QTD_REGISTROS"])
        qa_show_table(show, "Top Clientes - Agente BI", "top_clientes_agente_bi.pdf", top_n)
        return

    if intent in ["faturamento_uf", "comparativo_uf", "comparativo_uf_margem"]:
        uf = qa_extract_uf(pergunta)
        out = qa_aggregate_sales(d_mes, ["UF"])
        if uf and intent == "faturamento_uf":
            row = out[out["UF"].astype(str).str.upper() == uf]
            if row.empty:
                st.warning(f"Não encontrei faturamento para a UF {uf} em {label_periodo}.")
                return
            r = row.iloc[0]
            st.success(f"O faturamento da UF {uf} em {label_periodo} foi de {qa_currency(r['FATURAMENTO'])}.")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Faturamento", qa_currency(r["FATURAMENTO"]))
            c2.metric("Custo", qa_currency(r["CUSTO"]))
            c3.metric("Margem", qa_currency(r["MARGEM_BRUTA_R$"]))
            c4.metric("Margem %", pct_br(r["MARGEM_BRUTA_%"]))
            return
        ordem = "MARGEM_BRUTA_R$" if ("margem" in pnorm or intent == "comparativo_uf_margem") else "FATURAMENTO"
        out = out.sort_values(ordem, ascending=False)
        melhor = out.iloc[0] if not out.empty else None
        if melhor is not None:
            st.success(f"A UF líder em {label_periodo} é {melhor['UF']} com {qa_currency(melhor[ordem])} em {'margem' if ordem == 'MARGEM_BRUTA_R$' else 'faturamento'}.")
        show = qa_format_financial_table(out, ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], ["MARGEM_BRUTA_%"], ["QTD_REGISTROS"])
        qa_show_table(show, "Comparativo por UF - Agente BI", "comparativo_uf_agente_bi.pdf", 100)
        return

    if intent == "ranking_cidades":
        out = qa_aggregate_sales(d_mes, ["LOCALIZAÇÃO"])
        ordem = "MARGEM_BRUTA_R$" if "margem" in pnorm else "FATURAMENTO"
        out = out.sort_values(ordem, ascending=False).head(top_n)
        st.success(f"Top {top_n} cidades/localizações por {'margem' if ordem == 'MARGEM_BRUTA_R$' else 'faturamento'} em {label_periodo}.")
        show = qa_format_financial_table(out, ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], ["MARGEM_BRUTA_%"], ["QTD_REGISTROS"])
        qa_show_table(show, "Ranking de Cidades - Agente BI", "ranking_cidades_agente_bi.pdf", top_n)
        return

    if intent in ["top_produtos_faturamento", "top_produtos_margem", "top_produtos_quantidade"]:
        if df_prod_agent.empty:
            st.warning("Não foi possível analisar produtos. Confira se a aba BASE DE PRODUTOS contém Produto, Quantidade, MÊS, ANO, Valor total e Custo total.")
            return
        dprod, label_prod, _ = qa_filter_month(df_prod_agent, pergunta)
        out = dprod.groupby("Produto", as_index=False).agg(
            QTD=("Quantidade", "sum"),
            FATURAMENTO=("Valor total", "sum"),
            CUSTO=("Custo total", "sum"),
        )
        out["MARGEM_BRUTA_R$"] = out["FATURAMENTO"] - out["CUSTO"]
        out["MARGEM_BRUTA_%"] = out.apply(lambda r: (r["MARGEM_BRUTA_R$"] / r["FATURAMENTO"]) if r["FATURAMENTO"] else 0.0, axis=1)
        if intent == "top_produtos_margem":
            ordem = "MARGEM_BRUTA_R$"
        elif intent == "top_produtos_quantidade":
            ordem = "QTD"
        else:
            ordem = "FATURAMENTO"
        out = out.sort_values(ordem, ascending=False).head(top_n)
        st.success(f"Top {top_n} produtos por {ordem.lower().replace('_', ' ')} em {label_prod}.")
        show = qa_format_financial_table(out, ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], ["MARGEM_BRUTA_%"], ["QTD"])
        qa_show_table(show, "Top Produtos - Agente BI", "top_produtos_agente_bi.pdf", top_n)
        return

    if intent == "giro_produto":
        if df_prod_agent.empty:
            st.warning("Não foi possível analisar giro. Confira a aba BASE DE PRODUTOS.")
            return
        # Remove palavras comuns para tentar achar o produto
        termo = re.sub(r"\b(qual|foi|o|a|os|as|giro|do|da|de|produto|produtos|mes|mês|em|no|na|por|favor)\b", " ", qa_norm(pergunta))
        for nome_mes in list(MESES_LONG.keys()) + MESES_PT:
            termo = re.sub(rf"\b{qa_norm(nome_mes)}\b", " ", termo)
        termo = re.sub(r"\b(0?[1-9]|1[0-2])\b", " ", termo)
        termo = re.sub(r"\s+", " ", termo).strip()
        opcoes = sorted(df_prod_agent["Produto"].dropna().astype(str).unique().tolist())
        produto_match = qa_best_match(termo, opcoes, score_min=45) if termo else None
        dprod, label_prod, _ = qa_filter_month(df_prod_agent, pergunta)
        if produto_match:
            dprod = dprod[dprod["Produto"] == produto_match].copy()
        elif termo:
            dprod = dprod[dprod["Produto"].apply(lambda x: termo in qa_norm(x))].copy()
        if dprod.empty:
            st.warning("Não encontrei produto compatível. Tente escrever uma parte da descrição exatamente como aparece na base.")
            return
        giro = dprod.groupby(["Produto", "MES_NUM"], as_index=False).agg(
            GIRO_QTD=("Quantidade", "sum"),
            FATURAMENTO=("Valor total", "sum"),
            CUSTO=("Custo total", "sum"),
        )
        giro["MARGEM_BRUTA_R$"] = giro["FATURAMENTO"] - giro["CUSTO"]
        giro["MÊS"] = giro["MES_NUM"].apply(lambda m: qa_month_label(int(m)) if pd.notna(m) else "-")
        giro = giro.sort_values(["Produto", "MES_NUM"])
        produto_txt = f" para {produto_match}" if produto_match else ""
        st.success(f"Giro encontrado{produto_txt} em {label_prod}.")
        show = giro[["Produto", "MÊS", "GIRO_QTD", "FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"]].copy()
        show = qa_format_financial_table(show, ["FATURAMENTO", "CUSTO", "MARGEM_BRUTA_R$"], [], ["GIRO_QTD"])
        qa_show_table(show, "Giro de Produto - Agente BI", "giro_produto_agente_bi.pdf", 200)
        return

    if intent in ["clientes_queda", "clientes_crescimento"]:
        meses = qa_extract_months(pergunta)
        if len(meses) < 2:
            st.warning("Informe dois meses para comparação. Exemplo: quais clientes caíram de março para abril?")
            return
        m1, m2 = meses[0], meses[1]
        base = df_ano[df_ano["MES_NUM"].isin([m1, m2])].copy()
        pv = base.pivot_table(index="Cliente", columns="MES_NUM", values="Valor total", aggfunc="sum", fill_value=0.0)
        for m in [m1, m2]:
            if m not in pv.columns:
                pv[m] = 0.0
        pv = pv[[m1, m2]].reset_index()
        col1 = f"FAT_{qa_month_label(m1)}"
        col2 = f"FAT_{qa_month_label(m2)}"
        pv.columns = ["Cliente", col1, col2]
        pv["DIFERENÇA_R$"] = pv[col2] - pv[col1]
        pv["VARIAÇÃO_%"] = pv.apply(lambda r: (r["DIFERENÇA_R$"] / r[col1]) if r[col1] else (1.0 if r[col2] > 0 else 0.0), axis=1)
        if intent == "clientes_queda":
            out = pv[pv["DIFERENÇA_R$"] < 0].sort_values("DIFERENÇA_R$", ascending=True).head(top_n)
            st.success(f"Top {top_n} clientes que caíram de {qa_month_label(m1)} para {qa_month_label(m2)}.")
        else:
            out = pv[pv["DIFERENÇA_R$"] > 0].sort_values("DIFERENÇA_R$", ascending=False).head(top_n)
            st.success(f"Top {top_n} clientes que cresceram de {qa_month_label(m1)} para {qa_month_label(m2)}.")
        show = qa_format_financial_table(out, [col1, col2, "DIFERENÇA_R$"], ["VARIAÇÃO_%"])
        qa_show_table(show, "Comparativo de Clientes - Agente BI", "comparativo_clientes_agente_bi.pdf", top_n)
        return

    st.warning("Não consegui identificar essa pergunta ainda. Use um dos exemplos abaixo ou escreva usando termos como faturamento, cliente, produto, UF, cidade, margem, crescimento ou giro.")


# Interface do agente em formato de chat
if "historico_agente_bi" not in st.session_state:
    st.session_state["historico_agente_bi"] = []

with st.chat_message("assistant"):
    st.write("Olá. Sou o assistente comercial do dashboard. Digite sua pergunta abaixo e eu calculo a resposta usando a base carregada.")

pergunta_agent = st.chat_input(
    "Pergunte sobre vendas, margem, clientes, produtos, UF, cidades, crescimento ou metas..."
)

if pergunta_agent:
    st.session_state["historico_agente_bi"].append(pergunta_agent)
    with st.chat_message("user"):
        st.write(pergunta_agent)
    with st.chat_message("assistant"):
        qa_answer(pergunta_agent)

with st.expander("Histórico desta sessão", expanded=False):
    if st.session_state["historico_agente_bi"]:
        for i, q in enumerate(reversed(st.session_state["historico_agente_bi"][-20:]), start=1):
            st.write(f"{i}. {q}")
    else:
        st.caption("Nenhuma pergunta feita ainda.")

# Biblioteca de perguntas: mais de 100 parâmetros prontos
perguntas_exemplos = []
meses_exemplos = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
ufs_exemplos = sorted({str(u).upper().strip() for u in df["UF"].dropna().unique().tolist() if str(u).strip()}) or ["DF", "GO", "MG"]

for mes in meses_exemplos:
    perguntas_exemplos.extend([
        f"Qual foi o faturamento de {mes}?",
        f"Qual foi a margem de {mes}?",
        f"Qual foi o crescimento de {mes}?",
        f"Quais são os top 10 clientes de {mes}?",
        f"Quais são os top 20 clientes de {mes}?",
        f"Quais clientes deixam mais margem em {mes}?",
        f"Quais são os top 10 produtos em faturamento de {mes}?",
        f"Quais são os top 10 produtos em margem de {mes}?",
        f"Quais produtos mais venderam em quantidade em {mes}?",
        f"Qual cidade teve maior faturamento em {mes}?",
        f"Qual UF deixou mais margem em {mes}?",
        f"Qual o comparativo de vendas por UF em {mes}?",
    ])

for uf in ufs_exemplos:
    perguntas_exemplos.extend([
        f"Qual meu faturamento na UF {uf}?",
        f"Qual meu faturamento na UF {uf} em março?",
        f"Qual meu faturamento na UF {uf} em abril?",
        f"Qual a margem da UF {uf}?",
    ])

pares_meses = [("janeiro", "fevereiro"), ("fevereiro", "março"), ("março", "abril"), ("abril", "maio"), ("maio", "junho"), ("junho", "julho"), ("julho", "agosto"), ("agosto", "setembro"), ("setembro", "outubro"), ("outubro", "novembro"), ("novembro", "dezembro")]
for a, b in pares_meses:
    perguntas_exemplos.extend([
        f"Quais clientes caíram de {a} para {b}?",
        f"Quais clientes aumentaram de {a} para {b}?",
        f"Quais clientes cresceram de {a} para {b}?",
        f"Qual foi o crescimento de {a} para {b}?",
    ])

perguntas_exemplos.extend([
    "Comparar faturamento de 2026 com 2025",
    "Comparar margem de 2026 com 2025",
    "Comparar desempenho por UF de 2026 com 2025",
    "Comparar estados de 2026 com 2025",
    "Comparar cidades de 2026 com 2025",
    "Comparar clientes de 2026 com 2025",
    "Quais clientes cresceram de 2025 para 2026?",
    "Quais clientes caíram de 2025 para 2026?",
    "Comparar produtos de 2026 com 2025",
    "Quais produtos cresceram de 2025 para 2026?",
    "Quais produtos caíram de 2025 para 2026?",
    "Comparar giro dos produtos de 2026 com 2025",
    "Comparar faturamento por UF em março de 2026 com 2025",
    "Comparar clientes em abril de 2026 com 2025",
])

perguntas_exemplos.extend([
    "Quais são meus top 10 clientes?",
    "Quais são meus top 20 clientes?",
    "Quais são meus top 50 clientes?",
    "Quais clientes deixam mais margem?",
    "Qual o ranking de clientes por margem?",
    "Qual o ranking de clientes por faturamento?",
    "Qual o comparativo de vendas por UF?",
    "Qual região ou estado deixa mais margem?",
    "Qual UF tem maior faturamento?",
    "Qual UF tem maior margem?",
    "Qual cidade onde eu tenho maior faturamento?",
    "Quais são as top 10 cidades por faturamento?",
    "Quais são as top 20 cidades por margem?",
    "Quais são meus top 10 produtos em faturamento?",
    "Quais são meus top 20 produtos em faturamento?",
    "Quais são meus top 10 produtos em margem?",
    "Quais são meus top 20 produtos em margem?",
    "Quais produtos mais vendem em quantidade?",
    "Qual foi o giro do produto thinner?",
    "Qual foi o giro do produto esmalte?",
    "Qual foi o giro do produto verniz?",
    "Qual foi o giro do produto catalisador?",
    "Qual foi o giro do produto massa?",
    "Qual foi o giro do produto primer?",
    "Qual foi o giro do produto lixa?",
    "Qual foi o giro do produto disco?",
    "Qual foi o giro do produto tinta?",
    "Qual foi o giro do produto fundo?",
    "Qual foi o giro do produto cola?",
    "Qual foi o giro do produto silicone?",
    "Qual foi o giro do produto fita?",
])

perguntas_exemplos = list(dict.fromkeys(perguntas_exemplos))

with st.expander(f"Biblioteca de perguntas possíveis ({len(perguntas_exemplos)} exemplos)", expanded=False):
    st.caption("Estes são exemplos. O agente também entende variações parecidas, desde que tenham termos como faturamento, crescimento, cliente, produto, UF, cidade, margem ou giro.")
    st.dataframe(pd.DataFrame({"Perguntas possíveis": perguntas_exemplos}), use_container_width=True, hide_index=True)
