import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
from PIL import Image

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide"
)

# -------------------- BACKGROUND --------------------
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

set_background_from_url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png")

# -------------------- ESTILO --------------------
st.markdown("""
<style>
    /* Textos em geral com cor clara */
    .stMarkdown, .stTextInput > label, .stNumberInput > label, .css-1d391kg, .css-1c7y2kd, .css-qrbaxs, .css-10trblm, .css-1v3fvcr {
        color: #ffffff !important;
    }

    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 1px 1px 4px #000000cc;
    }

    /* Menu lateral com fundo escuro e letras claras */
    section[data-testid="stSidebar"] {
        background-color: #2c2c2c;
    }
    .css-hxt7ib, .css-1v3fvcr {
        color: #ffffff !important;
    }

    /* Card de saldo com fundo amarelo transparente */
    .saldo-card {
        background-color: rgba(255, 255, 0, 0.2);
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
    }
    .saldo-text {
        color: #222222;
        font-weight: bold;
    }

    /* Logos */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 5px;
    }
    .logo-container img {
        max-width: 280px;
    }
    .eden-logo {
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }
    .eden-logo img {
        max-width: 90px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- LOGO CAFÉ --------------------
st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" alt="Logo Café du Contrôle"></div>', unsafe_allow_html=True)

# -------------------- DATA EDITÁVEL --------------------
data = st.date_input("Escolha a data", datetime.today(), label_visibility="collapsed")

# -------------------- SISTEMA FINANCEIRO --------------------
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
st.markdown(f"**Data selecionada:** {data.strftime('%d/%m/%Y')}")
st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")

with st.container():
    st.markdown("<div class='saldo-card'>", unsafe_allow_html=True)
    if saldo > 0:
        st.markdown(f"<span class='saldo-text'>Você está positiva hoje! 💚 Saldo: R$ {saldo:,.2f}</span>", unsafe_allow_html=True)
        st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        st.markdown(f"<span class='saldo-text'>Você gastou mais do que ganhou hoje! 💸 Saldo: R$ {saldo:,.2f}</span>", unsafe_allow_html=True)
        st.caption("Tá plantando dinheiro, né linda?")
    else:
        st.markdown("<span class='saldo-text'>Zerada. Saldo: R$ 0,00</span>", unsafe_allow_html=True)
        st.caption("Café preto e foco!")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- BOTÃO DE RELATÓRIO --------------------
if st.button("📄 Salvar Relatório do Dia"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório Financeiro - Café du Contrôle", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Data: {data.strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(200, 10, txt=f"Total de Entradas: R$ {total_entradas:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total de Gastos: R$ {total_saidas:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Saldo: R$ {saldo:,.2f}", ln=True)

    pdf_path = f"relatorio_{data.strftime('%Y%m%d')}.pdf"
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as file:
        btn = st.download_button(
            label="📥 Baixar Relatório em PDF",
            data=file,
            file_name=pdf_path,
            mime="application/pdf"
        )

# -------------------- RODAPÉ --------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="eden-logo"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png" alt="Logo Éden"></div>', unsafe_allow_html=True)
st.markdown("<center><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></center>", unsafe_allow_html=True)
