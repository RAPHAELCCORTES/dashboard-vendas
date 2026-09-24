"""
Dashboard de Vendas — Atividade Prática de Business Intelligence com Streamlit
Autor: Raphael
Execução local: streamlit run meu_dashboard.py
"""

# =============================================================================
# FASE 1 — ESTRUTURA BÁSICA E OTIMIZAÇÃO DE DESEMPENHO
# =============================================================================
import pandas as pd
import streamlit as st

# Configuração da página (deve ser o primeiro comando Streamlit do script)
st.set_page_config(page_title="Dashboard de Vendas", page_icon="📊", layout="wide")

# Passo 1 — Título principal
st.title("Dashboard de Vendas")
st.caption("Painel de Business Intelligence com filtros interativos, métricas e visualizações.")


# Passo 2 e 3 — Função de carga com cache.
# O Streamlit reexecuta o script inteiro a cada interação; o @st.cache_data guarda
# o DataFrame em memória e só relê o CSV se os argumentos (caminho) mudarem.
@st.cache_data
def carregar_dados(caminho: str = "vendas.csv") -> pd.DataFrame:
    df = pd.read_csv(caminho, parse_dates=["data"])
    df["mes"] = df["data"].dt.to_period("M").dt.to_timestamp()
    return df


@st.cache_data
def converter_para_csv(df: pd.DataFrame) -> bytes:
    # utf-8-sig garante acentuação correta ao abrir o arquivo no Excel
    return df.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")


def formatar_brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


df = carregar_dados()

# =============================================================================
# FASE 2 — LAYOUT E FILTROS LATERAIS (INTERATIVIDADE)
# =============================================================================
# Passo 1 — Painel lateral
st.sidebar.title("Filtros")

# Passo 2 — Seleção múltipla de categorias (todas selecionadas por padrão)
lista_de_categorias = sorted(df["categoria"].unique())
categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as Categorias",
    options=lista_de_categorias,
    default=lista_de_categorias,
)

# Filtros extras: região e período
lista_de_regioes = sorted(df["regiao"].unique())
regioes_selecionadas = st.sidebar.multiselect(
    "Selecione as Regiões", options=lista_de_regioes, default=lista_de_regioes
)

data_min, data_max = df["data"].min().date(), df["data"].max().date()
periodo = st.sidebar.date_input(
    "Período", value=(data_min, data_max), min_value=data_min, max_value=data_max
)

st.sidebar.divider()
st.sidebar.caption(f"Base carregada: {len(df):,} registros".replace(",", "."))

# Passo 3 — Regra de ouro: o valor retornado pelos widgets filtra o DataFrame.
# A cada alteração, o script reexecuta e toda a tela reflete o novo recorte.
if len(periodo) != 2:
    st.info("Selecione a data inicial e a data final do período na barra lateral.")
    st.stop()

inicio, fim = pd.Timestamp(periodo[0]), pd.Timestamp(periodo[1])
df_filtrado = df[
    df["categoria"].isin(categorias_selecionadas)
    & df["regiao"].isin(regioes_selecionadas)
    & df["data"].between(inicio, fim)
]

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# =============================================================================
# FASE 3 — MÉTRICAS EM DESTAQUE E VISUALIZAÇÃO DE DADOS
# =============================================================================
receita_calculada = df_filtrado["receita"].sum()
total_pedidos = df_filtrado["pedido_id"].nunique()
ticket_medio = receita_calculada / total_pedidos
itens_vendidos = int(df_filtrado["quantidade"].sum())

# Variação em relação ao período anterior de mesma duração (usado no delta das métricas)
duracao = fim - inicio
df_anterior = df[
    df["categoria"].isin(categorias_selecionadas)
    & df["regiao"].isin(regioes_selecionadas)
    & df["data"].between(inicio - duracao - pd.Timedelta(days=1), inicio - pd.Timedelta(days=1))
]


def variacao(atual: float, anterior: float):
    if anterior == 0:
        return None
    return f"{(atual - anterior) / anterior:+.1%}".replace(".", ",")


# Passo 1 — Colunas proporcionais
col1, col2 = st.columns([1, 1])

# Passo 2 — Indicadores em destaque
with col1:
    st.metric(
        label="Receita Total",
        value=formatar_brl(receita_calculada),
        delta=variacao(receita_calculada, df_anterior["receita"].sum()),
        border=True,
    )
with col2:
    st.metric(
        label="Total de Pedidos",
        value=f"{total_pedidos:,}".replace(",", "."),
        delta=variacao(total_pedidos, df_anterior["pedido_id"].nunique()),
        border=True,
    )

col3, col4 = st.columns([1, 1])
with col3:
    st.metric(label="Ticket Médio", value=formatar_brl(ticket_medio), border=True)
with col4:
    st.metric(label="Itens Vendidos", value=f"{itens_vendidos:,}".replace(",", "."), border=True)

if len(df_anterior):
    st.caption("Variação calculada em relação ao período anterior de mesma duração.")

# Passo 3 — Navegação por abas
aba1, aba2 = st.tabs(["Evolução Mensal", "Tabela de Dados"])

# Passo 4 — Receita agrupada por mês ANTES de plotar (gráfico legível)
with aba1:
    st.subheader("Receita mensal por categoria")
    dados_agrupados = df_filtrado.pivot_table(
        index="mes", columns="categoria", values="receita", aggfunc="sum", fill_value=0
    )
    st.area_chart(dados_agrupados, x_label="Mês", y_label="Receita (R$)")

    st.subheader("Receita por região")
    receita_regiao = df_filtrado.groupby("regiao")["receita"].sum().sort_values(ascending=False)
    st.bar_chart(receita_regiao, x_label="Região", y_label="Receita (R$)", horizontal=True)

# Passo 5 — Tabela interativa + exportação do recorte em CSV
with aba2:
    st.subheader("Dados filtrados")
    st.dataframe(
        df_filtrado.drop(columns="mes"),
        width="stretch",
        hide_index=True,
        column_config={
            "data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "pedido_id": st.column_config.NumberColumn("Pedido", format="%d"),
            "categoria": "Categoria",
            "produto": "Produto",
            "regiao": "Região",
            "canal": "Canal",
            "quantidade": "Qtd.",
            "preco_unitario": st.column_config.NumberColumn("Preço Unit. (R$)", format="%.2f"),
            "receita": st.column_config.NumberColumn("Receita (R$)", format="%.2f"),
        },
    )
    st.download_button(
        label="📥 Baixar dados filtrados (CSV)",
        data=converter_para_csv(df_filtrado.drop(columns="mes")),
        file_name="vendas_filtradas.csv",
        mime="text/csv",
    )
