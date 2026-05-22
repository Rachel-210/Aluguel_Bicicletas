import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# Configuração da página do Streamlit
st.set_page_config(page_title="Dashboard de Aluguel de Bikes", layout="wide")
st.title("🚴 Dashboard Analítico - Locadora de Bicicletas")

# CONEXÃO COM O BANCO DE DADOS
def abrir_conexao():
    conn = psycopg2.connect(
        dbname="AluguelBicicletas",
        user="postgres",
        password="1230",
        host="localhost",
        port="5432"
    )
    return conn

# BARRA LATERAL
st.sidebar.header("Filtros")

# Filtro de Data
data_inicio = st.sidebar.date_input("Data Inicial", pd.to_datetime("2026-01-01"))
data_fim = st.sidebar.date_input("Data Final", pd.to_datetime("2026-12-31"))

# CONSULTAS SQL 
conn = abrir_conexao()

# Consulta 1: KPIs Gerais (WHERE, COUNT, SUM, AVG)
query_kpis = """
    SELECT 
        COUNT(id_aluguel) as total_alugueis,
        SUM(valor_total) as faturamento_total,
        AVG(valor_total) as ticket_medio,
        COUNT(DISTINCT fk_cliente) as clientes_unicos
    FROM alugueis
    WHERE data_aluguel BETWEEN %s AND %s;
"""
df_kpis = pd.read_sql_query(query_kpis, conn, params=(data_inicio, data_fim))

# Consulta 2: Gráfico de Linhas - Evolução Temporal (GROUP BY e ORDER BY)
query_linhas = """
    SELECT DATE(data_aluguel) as data, COUNT(id_aluguel) as qtd
    FROM alugueis
    WHERE data_aluguel BETWEEN %s AND %s
    GROUP BY DATE(data_aluguel)
    ORDER BY data ASC;
"""
df_linhas = pd.read_sql_query(query_linhas, conn, params=(data_inicio, data_fim))

# Consulta 3: Gráfico de Barras - Modelos Mais Alugados (JOIN, GROUP BY, ORDER BY)
query_barras = """
    SELECT b.modelo, COUNT(a.id_aluguel) as total
    FROM alugueis a
    JOIN bicicletas b ON a.fk_bicicleta = b.id_bicicleta
    WHERE a.data_aluguel BETWEEN %s AND %s
    GROUP BY b.modelo
    ORDER BY total DESC;
"""
df_barras = pd.read_sql_query(query_barras, conn, params=(data_inicio, data_fim))

# Gráfico de Pizza - Status das Bicicletas
query_pizza = "SELECT status, COUNT(*) as qtd FROM bicicletas GROUP BY status;"
df_pizza = pd.read_sql_query(query_pizza, conn)

conn.close()

# EXIBIÇÃO DOS KPIS NO DASHBOARD
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Aluguéis", int(df_kpis['total_alugueis'].iloc[0]))
with col2:
    faturamento = df_kpis['faturamento_total'].iloc[0] or 0
    st.metric("Faturamento Total", f"R$ {faturamento:,.2f}")
with col3:
    ticket = df_kpis['ticket_medio'].iloc[0] or 0
    st.metric("Ticket Médio", f"R$ {ticket:,.2f}")
with col4:
    st.metric("Clientes Atendidos", int(df_kpis['clientes_unicos'].iloc[0]))

st.markdown("---")

# EXIBIÇÃO DOS GRÁFICOS
col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("📈 Evolução dos Aluguéis no Período")
    fig_linha = px.line(df_linhas, x='data', y='qtd', markers=True, labels={'data': 'Data', 'qtd': 'Qtd Aluguéis'})
    st.plotly_chart(fig_linha, use_container_width=True)

with col_dir:
    st.subheader("🚲 Modelos mais Procurados")
    fig_barra = px.bar(df_barras, x='total', y='modelo', orientation='h', labels={'total': 'Total de Aluguéis', 'modelo': 'Modelo'})
    st.plotly_chart(fig_barra, use_container_width=True)

st.markdown("---")
st.subheader("📊 Disponibilidade da Frota (Geral)")
fig_pizza = px.pie(df_pizza, values='qtd', names='status', hole=0.4)
st.plotly_chart(fig_pizza, use_container_width=True)

