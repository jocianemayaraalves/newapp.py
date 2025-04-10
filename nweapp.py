import streamlit as st
from PIL import Image
from datetime import datetime
from fpdf import FPDF
import pandas as pd

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- BACKGROUND --------------------
def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_background()

# -------------------- ESTILO PERSONALIZADO --------------------
st.markdown("""
    <style>
        .logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .logo-container img {
            max-width: 300px;
            margin-bottom: 5px;
        }

        .stSidebar {{
            background-color: #f8f5f2 !important;
        }}

        .sidebar .sidebar-content {{
            background-color: #f8f5f2;
            color: #333;
        }}

        h1, h2, h3 {{
            color: #ffffff;
            text-shadow: 1px 1px 4px #000000cc;
        }}

        .main > div {{
            background-color: rgba(255, 255, 0, 0.15);
            border-radius: 10px;
            padding: 20px;
            margin-top: 10px;
        }}

        .saldo-text {{
            font-weight: bold;
            color: #2d2d2d;
        }}
    </style>
""", unsafe_allow_html=True)

# -------------------- LOGO CAFÉ --------------------
st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png"></div>', unsafe_allow_html=True)

# -------------------- DATA EDITÁVEL --------------------
st.markdown("### Informe a data abaixo:")
data_escolhida = st.date_input("Data do Registro", value=datetime.now())

# -------------------- MENU LATERAL --------------------
st.sidebar.markdown("# Menu ☕")
menu = st.sidebar.radio("Navegar para:", ["Adicionar Registros", "Gerar Relatório PDF", "Sobre o App"])

if menu == "Adicionar Registros":
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

    if saldo > 0:
        st.success(f"<span class='saldo-text'>Você está positiva hoje! 💚 Saldo: R$ {saldo:,.2f}</span>", unsafe_allow_html=True)
        st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        st.error(f"<span class='saldo-text'>Você gastou mais do que ganhou hoje! 💸 Saldo: R$ {saldo:,.2f}</span>", unsafe_allow_html=True)
        st.caption("Tá plantando dinheiro, né linda?")
    else:
        st.warning(f"<span class='saldo-text'>Zerada. Saldo: R$ 0,00</span>", unsafe_allow_html=True)
        st.caption("Café preto e foco!")

elif menu == "Gerar Relatório PDF":
    st.subheader("📄 Gerador de Relatório")

    if st.button("📄 Gerar Relatório em PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Relatório Financeiro - Café du Contrôle", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Data: {data_escolhida.strftime('%d/%m/%Y')}", ln=True)
        pdf.cell(200, 10, txt=f"Total de Entradas: R$ {total_entradas:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total de Gastos: R$ {total_saidas:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Saldo do Dia: R$ {saldo:,.2f}", ln=True)

        pdf.output("relatorio_financeiro.pdf")
        with open("relatorio_financeiro.pdf", "rb") as file:
            st.download_button("📥 Baixar Relatório", file, file_name="relatorio_financeiro.pdf")

elif menu == "Sobre o App":
    st.markdown("""
    ### ☕ Sobre o Café du Contrôle
    Este aplicativo foi desenvolvido com carinho para ajudar no controle financeiro pessoal de forma acolhedora e divertida.
    Desenvolvido por **ÉdenMachine**.
    """)

# -------------------- LOGO RODAPÉ --------------------
st.markdown("---")
st.markdown('<div style="text-align:center;"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png" width="200"></div>', unsafe_allow_html=True)
st.markdown("<center><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></center>", unsafe_allow_html=True)
