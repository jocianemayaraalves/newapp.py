import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide"
)

# -------------------- FUNÇÕES --------------------
def set_background_from_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('{image_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Define imagem de fundo
set_background_from_url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png")

# Carrega ou inicializa o histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# -------------------- ESTILOS --------------------
st.markdown("""
    <style>
        .sidebar .sidebar-content {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        .sidebar .css-1d391kg, .sidebar .css-1l02zno, .sidebar .css-1kyxreq {{
            color: #000000 !important;
        }}

        .logo-container {{
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }}
        .logo-container img {{
            max-width: 280px;
        }}

        h1, h2, h3, .stMarkdown, .stTextInput > label, .stNumberInput > label {{
            color: #fdfdfd !important;
            text-shadow: 1px 1px 4px #000000aa;
        }}

        .saldo-box {{
            background-color: rgba(255, 255, 0, 0.3);
            padding: 10px;
            border-radius: 10px;
            font-weight: bold;
            color: #222;
        }}

        .menu-item {{
            font-weight: bold;
            font-size: 16px;
        }}
    </style>
""", unsafe_allow_html=True)

# -------------------- LOGO E DATA --------------------
with st.container():
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png"></div>', unsafe_allow_html=True)

hoje = st.date_input("Selecione a data", value=datetime.today(), format="DD/MM/YYYY")

# -------------------- MENU LATERAL --------------------
menu = st.sidebar.radio("Navegação", ["📥 Lançamentos", "📊 Dashboard", "📁 Relatórios"], key="menu")

# -------------------- ENTRADAS E SAÍDAS --------------------
if menu == "📥 Lançamentos":
    st.header("💰 Entradas")
    salario = st.number_input("Salário", min_value=0.0, step=100.0)
    renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
    total_entradas = salario + renda_extra

    st.header("💸 Gastos")
    fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
    extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
    total_saidas = fixos + extras

    saldo = total_entradas - total_saidas

    if st.button("Salvar Lançamento"):
        st.session_state.historico.append({
            "data": hoje.strftime("%d/%m/%Y"),
            "entradas": total_entradas,
            "saidas": total_saidas,
            "saldo": saldo
        })
        st.success("Lançamento salvo!")

    st.header("📊 Resumo do Dia")
    st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
    st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")
    st.markdown(f"<div class='saldo-box'>Saldo: R$ {saldo:,.2f}</div>", unsafe_allow_html=True)

    if saldo > 0:
        st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        st.caption("Tá plantando dinheiro, né linda?")
    else:
        st.caption("Café preto e foco!")

# -------------------- DASHBOARD --------------------
elif menu == "📊 Dashboard":
    st.header("📈 Visão Geral por Período")
    if len(st.session_state.historico) == 0:
        st.warning("Nenhum dado cadastrado ainda.")
    else:
        df = pd.DataFrame(st.session_state.historico)
        datas = st.multiselect("Selecione as datas para analisar", df["data"].unique())

        if datas:
            filtro = df[df["data"].isin(datas)]
            total_entradas = filtro["entradas"].sum()
            total_saidas = filtro["saidas"].sum()
            saldo_periodo = filtro["saldo"].sum()

            st.markdown(f"**Entradas no período:** R$ {total_entradas:,.2f}")
            st.markdown(f"**Gastos no período:** R$ {total_saidas:,.2f}")
            st.markdown(f"**Saldo total:** R$ {saldo_periodo:,.2f}")

            # Gráfico de pizza
            fig1, ax1 = plt.subplots()
            ax1.pie([total_entradas, total_saidas], labels=["Entradas", "Saídas"], autopct='%1.1f%%')
            ax1.axis('equal')
            st.pyplot(fig1)

            # Gráfico de linha
            fig2, ax2 = plt.subplots()
            filtro_plot = filtro.copy()
            filtro_plot["data"] = pd.to_datetime(filtro_plot["data"], format="%d/%m/%Y")
            filtro_plot = filtro_plot.sort_values("data")
            ax2.plot(filtro_plot["data"], filtro_plot["saldo"], marker='o')
            ax2.set_title("Evolução do Saldo")
            ax2.set_ylabel("Saldo (R$)")
            st.pyplot(fig2)

# -------------------- RELATÓRIOS --------------------
elif menu == "📁 Relatórios":
    st.header("📄 Gerar Relatório em PDF")
    if len(st.session_state.historico) == 0:
        st.warning("Nenhum dado disponível para gerar relatório.")
    else:
        df = pd.DataFrame(st.session_state.historico)
        datas = st.multiselect("Selecione as datas para o relatório", df["data"].unique(), key="relatorio")

        if st.button("Gerar PDF") and datas:
            filtro = df[df["data"].isin(datas)]
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="Relatório Financeiro - Café du Contrôle", ln=True, align='C')
            pdf.ln(10)

            for _, row in filtro.iterrows():
                pdf.cell(200, 10, txt=f"Data: {row['data']} - Entradas: R$ {row['entradas']:.2f} - Saídas: R$ {row['saidas']:.2f} - Saldo: R$ {row['saldo']:.2f}", ln=True)

            pdf.output("relatorio_cafe_du_controle.pdf")
            with open("relatorio_cafe_du_controle.pdf", "rb") as file:
                st.download_button(
                    label="📥 Baixar Relatório",
                    data=file,
                    file_name="relatorio_cafe_du_controle.pdf",
                    mime="application/pdf"
                )

# -------------------- RODAPÉ --------------------
st.markdown("""
    <br><hr>
    <div style='text-align:center;'>
        <img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png' width='150'>
        <p><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></p>
    </div>
""", unsafe_allow_html=True)
