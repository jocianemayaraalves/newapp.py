import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime, date
import matplotlib.pyplot as plt
import sqlite3

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
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

data_lancamento = st.date_input("📅 Selecione a data do lançamento:", value=date.today())

# -------------------- CONFIGURAÇÃO SQLITE --------------------
# Conectando-se ao banco de dados SQLite
conn = sqlite3.connect('cafe_controle.db')
cursor = conn.cursor()

# Criando a tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS relatorios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE,
    entradas FLOAT,
    saidas FLOAT,
    saldo FLOAT
)
""")
conn.commit()

# Função para salvar os relatórios no banco de dados
def salvar_relatorio(data, entradas, saidas, saldo):
    cursor.execute("INSERT INTO relatorios (data, entradas, saidas, saldo) VALUES (?, ?, ?, ?)",
                   (data, entradas, saidas, saldo))
    conn.commit()

# Função para recuperar relatórios do banco de dados
def recuperar_relatorios():
    cursor.execute("SELECT * FROM relatorios ORDER BY data DESC")
    return cursor.fetchall()

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
        salvar_relatorio(data_lancamento, total_entradas, total_saidas, saldo)

# -------------------- RELATÓRIOS --------------------
elif menu == "Relatórios":
    st.header("📂 Relatórios Salvos")
    relatorios = recuperar_relatorios()
    
    if relatorios:
        df = pd.DataFrame(relatorios, columns=["ID", "Data", "Entradas", "Saídas", "Saldo"])
        st.dataframe(df)
    else:
        st.info("Nenhum relatório salvo ainda.")

# -------------------- GERAR PDF --------------------
elif menu == "Gerar PDF":
    st.header("📄 Gerar Relatório em PDF")
    relatorios = recuperar_relatorios()

    if relatorios:
        df = pd.DataFrame(relatorios, columns=["ID", "Data", "Entradas", "Saídas", "Saldo"])

        data_inicial = st.date_input("Data inicial", value=df['Data'].min())
        data_final = st.date_input("Data final", value=df['Data'].max())

        filtro = (df["Data"] >= data_inicial) & (df["Data"] <= data_final)
        df_filtrado = df[filtro]

        st.subheader("Gráficos")
        if not df_filtrado.empty:
            st.pyplot(df_filtrado.plot(x="Data", y=["Entradas", "Saídas", "Saldo"], kind="line").figure)
            st.pyplot(df_filtrado[["Entradas", "Saídas"]].sum().plot.pie(autopct='%1.1f%%').figure)

        st.subheader("Informações Inteligentes")
        st.markdown(f"- **Média de saldo diário:** R$ {df_filtrado['Saldo'].mean():,.2f}")
        st.markdown(f"- **Dia mais lucrativo:** {df_filtrado.loc[df_filtrado['Saldo'].idxmax()]['Data']}")
        st.markdown(f"- **Maior gasto:** R$ {df_filtrado['Saídas'].max():,.2f}")

    else:
        st.warning("Nenhum dado disponível para gerar PDF.")

# -------------------- CARTEIRA --------------------
elif menu == "Carteira":
    st.header("💼 Saldo em Carteira por Mês")
    relatorios = recuperar_relatorios()

    if relatorios:
        df = pd.DataFrame(relatorios, columns=["ID", "Data", "Entradas", "Saídas", "Saldo"])
        df["Data"] = pd.to_datetime(df["Data"])
        df["Mês"] = df["Data"].dt.strftime("%B")
        df_mes = df.groupby("Mês")[["Entradas", "Saídas", "Saldo"]].sum().reset_index()
        st.dataframe(df_mes)
        st.bar_chart(df_mes.set_index("Mês")["Saldo"])
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

# -------------------- RODAPÉ --------------------
st.markdown("""
---
<center><small style='font-size:10px;'>☕ Desenvolvido com carinho pela <strong>ÉdenMachine</strong></small><br>
<img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/refs/heads/main/eden-machine-logo-removebg-preview.png" width="80">
</center>
""", unsafe_allow_html=True)
