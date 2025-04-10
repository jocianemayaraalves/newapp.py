import streamlit as st
from PIL import Image
from datetime import datetime
from fpdf import FPDF
import pandas as pd

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

set_background_from_url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png")

# -------------------- ESTILO --------------------
st.markdown("""
    <style>
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }
        .logo-container img {
            max-width: 300px;
        }

        h1, h2, h3 {
            color: #fefefe;
            text-shadow: 1px 1px 4px #000000cc;
        }

        .stMarkdown, .stTextInput > label, .stNumberInput > label {
            color: #fdfdfd !important;
        }

        .main > div {
            padding-top: 20px;
            background-color: rgba(0,0,0,0.4); 
            border-radius: 10px;
        }

        .saldo-box {
            background-color: rgba(255, 255, 0, 0.2);
            padding: 20px;
            border-radius: 10px;
        }

        .saldo-box .saldo-text {
            color: #222222;
            font-weight: bold;
        }

        .sidebar .sidebar-content {
            background-color: rgba(0, 0, 0, 0.5);
        }

        .menu-item {
            color: #222222;
            font-weight: bold;
            margin-bottom: 10px;
        }

    </style>
""", unsafe_allow_html=True)

# -------------------- MENU LATERAL --------------------
st.sidebar.markdown("## ☕ Menu")
st.sidebar.markdown("<div class='menu-item'>Página Inicial</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='menu-item'>Relatórios</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='menu-item'>Configurações</div>", unsafe_allow_html=True)

# -------------------- LOGO CAFÉ --------------------
st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" alt="Logo Café du Contrôle"></div>', unsafe_allow_html=True)

# -------------------- SISTEMA FINANCEIRO --------------------
st.markdown("<h2>💰 Entradas</h2>", unsafe_allow_html=True)
salario = st.number_input("Salário", min_value=0.0, step=100.0)
renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
total_entradas = salario + renda_extra

st.markdown("<h2>💸 Gastos</h2>", unsafe_allow_html=True)
fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
total_saidas = fixos + extras

hoje = datetime.now().strftime("%d/%m/%Y")

st.markdown("<h2>📊 Resumo do Dia</h2>", unsafe_allow_html=True)
st.markdown(f"**Data:** {hoje}")
st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")
saldo = total_entradas - total_saidas

# -------------------- SALDO --------------------
st.markdown("<h2>💼 Saldo do Dia</h2>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='saldo-box'>", unsafe_allow_html=True)
    if saldo > 0:
        st.markdown(f"<div class='saldo-text'>Você está positiva hoje! 💚 Saldo: R$ {saldo:,.2f}</div>", unsafe_allow_html=True)
        st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        st.markdown(f"<div class='saldo-text'>Você gastou mais do que ganhou hoje! 💸 Saldo: R$ {saldo:,.2f}</div>", unsafe_allow_html=True)
        st.caption("Tá plantando dinheiro, né linda?")
    else:
        st.markdown("<div class='saldo-text'>Zerada. Saldo: R$ 0,00</div>", unsafe_allow_html=True)
        st.caption("Café preto e foco!")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- RODAPÉ --------------------
st.markdown("---")
st.markdown("<center><img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png' style='max-width: 150px;'></center>", unsafe_allow_html=True)
st.markdown("<center><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></center>", unsafe_allow_html=True)
