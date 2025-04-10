import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from fpdf import FPDF
from PIL import Image

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide"
)

# -------------------- FUNÇÃO BACKGROUND --------------------
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
        </style>
        """,
        unsafe_allow_html=True
    )

# Plano de fundo
set_background_from_url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png")

# -------------------- ESTILO --------------------
st.markdown("""
    <style>
        .sidebar .sidebar-content {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}

        .css-1d391kg {{
            color: #000000 !important;
        }}

        h1, h2, h3, .stMarkdown, .stTextInput > label, .stNumberInput > label, .stDateInput > label {{
            color: #fefefe !important;
            text-shadow: 1px 1px 4px #000000cc;
        }}

        .saldo-container {{
            background-color: rgba(255, 255, 0, 0.3);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }}

        .logo-container img.cafe-logo {{
            max-width: 320px;
        }}

        .logo-container img.eden-logo {{
            max-width: 120px;
        }}

        .relatorio-btn {{
            text-align: center;
            margin-top: 20px;
        }}
    </style>
""", unsafe_allow_html=True)

# -------------------- LOGOS --------------------
with st.container():
    st.markdown('<div class="logo-container" style="text-align: center;"><img class="cafe-logo" src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png"></div>', unsafe_allow_html=True)
    st.markdown("### 📅 Escolha a data")
    data_escolhida = st.date_input("Data do registro", value=datetime.today(), format="DD/MM/YYYY")

# -------------------- MENU LATERAL --------------------
with st.sidebar:
    st.markdown("## 📊 Menu de Navegação")
    menu = st.radio("Ir para:", ["Registro Diário", "Dashboard", "Histórico", "Relatórios PDF"])

# -------------------- REGISTRO DIÁRIO --------------------
if menu == "Registro Diário":
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
    st.markdown(f"**Data:** {data_escolhida.strftime('%d/%m/%Y')}")
    st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
    st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")

    with st.container():
        st.markdown("<div class='saldo-container'>", unsafe_allow_html=True)
        if saldo > 0:
            st.success(f"Saldo do dia: R$ {saldo:,.2f} — Você está positiva hoje! 💚")
            st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
        elif saldo < 0:
            st.error(f"Saldo do dia: R$ {saldo:,.2f} — Você gastou mais do que ganhou hoje! 💸")
            st.caption("Tá plantando dinheiro, né linda?")
        else:
            st.warning("Saldo do dia: R$ 0,00 — Zerada.")
            st.caption("Café preto e foco!")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='relatorio-btn'>", unsafe_allow_html=True)
    if st.button("📄 Salvar relatório do dia"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Relatório Financeiro — Café du Contrôle", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Data: {data_escolhida.strftime('%d/%m/%Y')}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Entradas: R$ {total_entradas:,.2f}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Saídas: R$ {total_saidas:,.2f}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Saldo: R$ {saldo:,.2f}", ln=True, align='L')
        pdf.output("relatorio_diario.pdf")
        st.success("Relatório PDF gerado com sucesso! Salve pelo menu do navegador.")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- RODAPÉ --------------------
st.markdown("---")
st.markdown("<div style='text-align:center;'><img class='eden-logo' src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png'></div>", unsafe_allow_html=True)
st.markdown("<center><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></center>", unsafe_allow_html=True)
