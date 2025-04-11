import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime, date
import matplotlib.pyplot as plt
import sqlite3
from PIL import Image

# -------------------- CONFIG GERAL --------------------
favicon = Image.open("favicon.png")

st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/favicon.png",
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
conn = sqlite3.connect('cafe_controle.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS relatorios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE,
    entradas FLOAT,
    tipo_entrada TEXT,
    descricao_saida TEXT,
    saidas FLOAT,
    saldo FLOAT,
    contas_futuras FLOAT
)
""")
conn.commit()

def salvar_relatorio(data, entradas, tipo_entrada, descricao_saida, saidas, saldo, contas_futuras):
    cursor.execute("INSERT INTO relatorios (data, entradas, tipo_entrada, descricao_saida, saidas, saldo, contas_futuras) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (data, entradas, tipo_entrada, descricao_saida, saidas, saldo, contas_futuras))
    conn.commit()

def recuperar_relatorios():
    cursor.execute("SELECT * FROM relatorios ORDER BY data DESC")
    return cursor.fetchall()

# -------------------- SIDEBAR --------------------
menu = st.sidebar.radio("Navegar pelo App", ["Resumo Diário", "Relatórios", "Gerar PDF", "Carteira", "Ajuda ☕"])

# -------------------- RESUMO DIÁRIO --------------------
if menu == "Resumo Diário":
    st.header("💰 Entradas")
    entradas = []
    with st.form("form_entradas"):
        num_entradas = st.number_input("Quantas entradas deseja adicionar?", min_value=1, max_value=10, value=1)
        for i in range(int(num_entradas)):
            tipo = st.selectbox(f"Tipo de Entrada #{i+1}", ["PIX", "Dinheiro Físico", "Transferência", "Outros"], key=f"tipo_{i}")
            valor = st.number_input(f"Valor da Entrada #{i+1}", min_value=0.0, step=50.0, key=f"valor_entrada_{i}")
            entradas.append((tipo, valor))
        submitted_entradas = st.form_submit_button("Registrar Entradas")

    total_entradas = sum([v for t, v in entradas])

    st.header("💸 Gastos")
    saidas = []
    with st.form("form_saidas"):
        num_saidas = st.number_input("Quantos gastos deseja adicionar?", min_value=1, max_value=10, value=1)
        for i in range(int(num_saidas)):
            desc = st.text_input(f"Descrição do Gasto #{i+1}", key=f"desc_saida_{i}")
            valor = st.number_input(f"Valor do Gasto #{i+1}", min_value=0.0, step=50.0, key=f"valor_saida_{i}")
            saidas.append((desc, valor))
        submitted_saidas = st.form_submit_button("Registrar Gastos")

    total_saidas = sum([v for d, v in saidas])

    contas_futuras = st.number_input("Total de Contas Futuras (Cartão/Empréstimo)", min_value=0.0, step=50.0)

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
        for tipo, valor in entradas:
            for desc, val in saidas:
                salvar_relatorio(data_lancamento, valor, tipo, desc, val, valor - val, contas_futuras)

# -------------------- RELATÓRIOS --------------------
elif menu == "Relatórios":
    st.header("📂 Relatórios Salvos")
    relatorios = recuperar_relatorios()

    if relatorios:
        df = pd.DataFrame(relatorios, columns=["ID", "Data", "Entradas", "Tipo Entrada", "Descrição Saída", "Saídas", "Saldo", "Contas Futuras"])
        st.dataframe(df)
    else:
        st.info("Nenhum relatório salvo ainda.")

# -------------------- GERAR PDF --------------------
elif menu == "Gerar PDF":
    st.header("📄 Gerar Relatório em PDF")
    relatorios = recuperar_relatorios()

    if relatorios:
        df = pd.DataFrame(relatorios, columns=["ID", "Data", "Entradas", "Tipo Entrada", "Descrição Saída", "Saídas", "Saldo", "Contas Futuras"])
        df["Data"] = pd.to_datetime(df["Data"])

        data_inicial = st.date_input("Data inicial", value=df['Data'].min())
        data_final = st.date_input("Data final", value=df['Data'].max())

        filtro = (df["Data"] >= pd.to_datetime(data_inicial)) & (df["Data"] <= pd.to_datetime(data_final))
        df_filtrado = df[filtro]

        st.subheader("Gráficos")
        if not df_filtrado.empty:
            st.pyplot(df_filtrado.plot(x="Data", y=["Entradas", "Saídas", "Saldo"], kind="line").figure)
            st.pyplot(df_filtrado[["Entradas", "Saídas"]].sum().plot.pie(autopct='%1.1f%%').figure)

        st.subheader("Informações Inteligentes")
        st.markdown(f"- **Média de saldo diário:** R$ {df_filtrado['Saldo'].mean():,.2f}")
        st.markdown(f"- **Dia mais lucrativo:** {df_filtrado.loc[df_filtrado['Saldo'].idxmax()]['Data'].strftime('%d/%m/%Y')}")
        st.markdown(f"- **Maior gasto:** R$ {df_filtrado['Saídas'].max():,.2f}")

    else:
        st.warning("Nenhum dado disponível para gerar PDF.")

# -------------------- CARTEIRA --------------------
elif menu == "Carteira":
    st.header("💼 Saldo em Carteira por Mês")
    relatorios = recuperar_relatorios()

    if relatorios:
        df = pd.DataFrame(relatorios, columns=["ID", "Data", "Entradas", "Tipo Entrada", "Descrição Saída", "Saídas", "Saldo", "Contas Futuras"])
        df["Data"] = pd.to_datetime(df["Data"])
        df["Mês"] = df["Data"].dt.strftime("%B")
        df_mes = df.groupby("Mês")[["Entradas", "Saídas", "Saldo", "Contas Futuras"]].sum().reset_index()
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
<center><small style='font-size:12px;'>☕ Desenvolvido com carinho pela <strong>ÉdenMachine</strong></small><br>
<img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/refs/heads/main/eden-machine-logo-removebg-preview.png" width="100">
</center>
""", unsafe_allow_html=True)
