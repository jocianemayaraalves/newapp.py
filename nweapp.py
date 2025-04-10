import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
from fpdf import FPDF

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide",
    initial_sidebar_state="expanded"
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

# -------------------- BACKGROUND --------------------
set_background_from_url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png")

# -------------------- ESTILO PERSONALIZADO --------------------
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

    .eden-logo {
        display: flex;
        justify-content: center;
        margin-top: 40px;
    }
    .eden-logo img {
        max-width: 150px;
        opacity: 0.7;
    }

    h1, h2, h3 {
        color: #fefefe;
        text-shadow: 1px 1px 4px #000000cc;
    }

    .stMarkdown, .stTextInput > label, .stNumberInput > label, .stDateInput > label {
        color: #fdfdfd !important;
    }

    .saldo-box {
        background-color: rgba(255, 255, 153, 0.5);
        padding: 15px;
        border-radius: 10px;
    }

    .saldo-text {
        color: #333333;
        font-weight: bold;
        font-size: 18px;
    }

    section[data-testid="stSidebar"] > div:first-child {
        background-color: rgba(0, 0, 0, 0.7);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- LOGO DO CAFÉ --------------------
st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" alt="Logo Café du Contrôle"></div>', unsafe_allow_html=True)

# -------------------- MENU LATERAL --------------------
menu = st.sidebar.radio("☕ Menu", ["Lançamentos", "Relatório em PDF", "Sobre o App"])

# -------------------- DATA SELECIONÁVEL --------------------
data_selecionada = st.date_input("📅 Selecione a data do lançamento:", datetime.now())

# -------------------- CONTEÚDO PRINCIPAL --------------------
if menu == "Lançamentos":
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
    st.markdown(f"**Data:** {data_selecionada.strftime('%d/%m/%Y')}")
    st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
    st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")

    with st.container():
        st.markdown("<div class='saldo-box'>", unsafe_allow_html=True)
        if saldo > 0:
            st.markdown(f"<p class='saldo-text'>Você está positiva hoje! 💚 Saldo: R$ {saldo:,.2f}</p>", unsafe_allow_html=True)
            st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
        elif saldo < 0:
            st.markdown(f"<p class='saldo-text'>Você gastou mais do que ganhou hoje! 💸 Saldo: R$ {saldo:,.2f}</p>", unsafe_allow_html=True)
            st.caption("Tá plantando dinheiro, né linda?")
        else:
            st.markdown("<p class='saldo-text'>Zerada. Saldo: R$ 0,00</p>", unsafe_allow_html=True)
            st.caption("Café preto e foco!")
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Relatório em PDF":
    st.header("📄 Gerar Relatório")
    st.write("Função para exportar relatórios será implementada aqui.")

elif menu == "Sobre o App":
    st.header("🌟 Sobre o Café du Contrôle")
    st.write("Organize suas finanças com charme e bom humor. Idealizado para trazer aconchego e controle para o seu bolso!")

# -------------------- RODAPÉ --------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='eden-logo'><img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png'></div>", unsafe_allow_html=True)
st.markdown("<center><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></center>", unsafe_allow_html=True)
