import streamlit as st
import pandas as pd
from datetime import datetime, date
import sqlite3
import matplotlib.pyplot as plt
from fpdf import FPDF

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/cafe-icon.ico",  # URL do ícone
    layout="wide"
)

# -------------------- FUNÇÃO: FUNDO --------------------
def set_background_from_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        .main > div {{
            background-color: rgba(0, 0, 0, 0.5);
            padding: 2rem;
            border-radius: 12px;
        }}
        h1, h2, h3 {{
            color: #fefefe !important;
            text-shadow: 1px 1px 4px #000000cc;
        }}
        .stMarkdown, .stTextInput > label, .stNumberInput > label {{
            color: #fdfdfd !important;
        }}
        .saldo-box {{
            background-color: rgba(255, 255, 0, 0.4);
            padding: 10px;
            border-radius: 10px;
            color: white;
            font-size: 20px;
            font-weight: bold;
            margin-top: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_from_url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png")

# -------------------- LOGO --------------------
with st.container():
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
            <img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" width="280">
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------- FUNÇÕES DO BANCO DE DADOS --------------------

def criar_tabela():
    """Cria a tabela de relatórios se não existir"""
    conn = sqlite3.connect('relatorios.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relatorios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            entradas REAL,
            saidas REAL,
            saldo REAL
        )
    """)
    conn.commit()
    conn.close()

def salvar_dados(data, entradas, saidas, saldo):
    """Salva um novo relatório no banco de dados"""
    conn = sqlite3.connect('relatorios.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO relatorios (data, entradas, saidas, saldo)
        VALUES (?, ?, ?, ?)
    """, (data, entradas, saidas, saldo))
    conn.commit()
    conn.close()

def carregar_dados():
    """Carrega todos os relatórios salvos no banco de dados"""
    conn = sqlite3.connect('relatorios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relatorios ORDER BY data DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

# Criar a tabela no banco de dados
criar_tabela()

# -------------------- DADOS DO USUÁRIO --------------------
data_lancamento = st.date_input("📅 Selecione a data do lançamento:", value=date.today())

# -------------------- SIDEBAR --------------------
menu = st.sidebar.radio("Navegar pelo App", ["Resumo Diário", "Relatórios", "Gerar PDF", "Carteira", "Ajuda ☕"])

# -------------------- RESUMO DIÁRIO --------------------
if menu == "Resumo Diário":
    st.header("💰 Entradas")
    salario = st.number_input("Salário", min_value=0.0, step=100.0)
    renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
    total_entradas = salario + renda_extra

    st.header("💸 Gastos")
    fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
    extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
    total_saidas = fixos + extras

    saldo = total_entradas - total_saidas

    st.header("📊 Resumo do Dia")
    st.markdown(f"**Data:** {data_lancamento.strftime('%d/%m/%Y')}")
    st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
    st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")

    if saldo > 0:
        st.success(f"Você está positiva hoje! 💚")
        st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        st.error("Você gastou mais do que ganhou hoje! 💸")
        st.caption("Tá plantando dinheiro, né linda?")
    else:
        st.warning("Zerada. Saldo: R$ 0,00")
        st.caption("Café preto e foco!")

    st.markdown(f'<div class="saldo-box">Saldo do Dia: R$ {saldo:,.2f}</div>', unsafe_allow_html=True)

    if st.button("💾 Salvar relatório do dia"):
        st.success("Relatório salvo com sucesso!")
        salvar_dados(data_lancamento.strftime('%d/%m/%Y'), total_entradas, total_saidas, saldo)

# -------------------- RELATÓRIOS --------------------
elif menu == "Relatórios":
    st.header("📂 Relatórios Salvos")
    dados_salvos = carregar_dados()

    if dados_salvos:
        st.write("Relatórios Salvos:")
        for dado in dados_salvos:
            st.markdown(f"**Data:** {dado[1]}")
            st.markdown(f"**Entradas:** R$ {dado[2]:,.2f}")
            st.markdown(f"**Saídas:** R$ {dado[3]:,.2f}")
            st.markdown(f"**Saldo:** R$ {dado[4]:,.2f}")
            st.markdown("---")
    else:
        st.info("Nenhum relatório salvo ainda.")

# -------------------- GERAR PDF --------------------
elif menu == "Gerar PDF":
    st.header("📄 Gerar Relatório em PDF")
    df = pd.DataFrame(st.session_state.relatorios)

    if not df.empty:
        data_inicial = st.date_input("Data inicial", value=df['data'].min().date())
        data_final = st.date_input("Data final", value=df['data'].max().date())

        filtro = (df["data"] >= pd.to_datetime(data_inicial)) & (df["data"] <= pd.to_datetime(data_final))
        df_filtrado = df[filtro]

        st.subheader("Gráficos")
        if not df_filtrado.empty:
            st.pyplot(df_filtrado.plot(x="data", y=["entradas", "saidas", "saldo"], kind="line").figure)
            st.pyplot(df_filtrado[["entradas", "saidas"]].sum().plot.pie(autopct='%1.1f%%').figure)

        st.subheader("Informações Inteligentes")
        st.markdown(f"- **Média de saldo diário:** R$ {df_filtrado['saldo'].mean():,.2f}")
        st.markdown(f"- **Dia mais lucrativo:** {df_filtrado.loc[df_filtrado['saldo'].idxmax()]['data'].strftime('%d/%m/%Y')}")
        st.markdown(f"- **Maior gasto:** R$ {df_filtrado['saidas'].max():,.2f}")

    else:
        st.warning("Nenhum dado disponível para gerar PDF.")

# -------------------- CARTEIRA --------------------
elif menu == "Carteira":
    st.header("💼 Saldo em Carteira por Mês")
    df = pd.DataFrame(st.session_state.relatorios)
    if not df.empty:
        df["data"] = pd.to_datetime(df["data"])
        df["mes"] = df["data"].dt.strftime("%B")
        df_mes = df.groupby("mes")[["entradas", "saidas", "saldo"]].sum().reset_index()
        st.dataframe(df_mes)
        st.bar_chart(df_mes.set_index("mes")["saldo"])
    else:
        st.info("Sem dados ainda. Salve relatórios no Resumo Diário.")

# -------------------- AJUDA --------------------
elif menu == "Ajuda ☕":
    st.header("❓ Ajuda e Dicas")
    st.markdown("""
    - **Resumo Diário**: registre entradas e gastos do dia.
    - **Relatórios**: veja seus lançamentos anteriores.
    - **Gerar PDF**: baixe relatórios com gráficos.
    - **Carteira**: veja quanto ainda tem de saldo no mês.
    """)
