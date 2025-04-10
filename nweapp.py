import streamlit as st
from PIL import Image
from datetime import datetime
from fpdf import FPDF
import base64

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide"
)

# -------------------- FUNÇÃO PARA IMAGEM DE FUNDO --------------------
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

# -------------------- MENU LATERAL FIXO --------------------
with st.sidebar:
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] > div:first-child {
                background-color: rgba(0, 0, 0, 0.4);
                border-radius: 10px;
                padding: 20px;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)
    menu = st.radio("Menu", ["Início"], index=0)

# -------------------- ESTILOS GERAIS --------------------
st.markdown("""
    <style>
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }
        .logo-container img {
            max-width: 280px;
        }

        h1, h2, h3 {
            color: #fefefe;
            text-shadow: 1px 1px 4px #000000cc;
        }

        .stMarkdown, .stTextInput > label, .stNumberInput > label {
            color: #fdfdfd !important;
        }

        .transparent-box {
            background-color: rgba(255, 255, 0, 0.15);
            padding: 20px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- LOGO DO CAFÉ --------------------
with st.container():
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" alt="Logo Café du Contrôle"></div>', unsafe_allow_html=True)

# -------------------- CONTEÚDO PRINCIPAL --------------------
if menu == "Início":
    st.markdown("<div class='transparent-box'>", unsafe_allow_html=True)

    st.header("💰 Entradas")
    salario = st.number_input("Salário", min_value=0.0, step=100.0)
    renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
    total_entradas = salario + renda_extra

    st.header("💸 Gastos")
    fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
    extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
    total_saidas = fixos + extras

    hoje = datetime.now().strftime("%d/%m/%Y")

    st.header("📊 Resumo do Dia")
    st.markdown(f"**Data:** {hoje}")
    st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
    st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")
    saldo = total_entradas - total_saidas

    st.header("💼 Saldo do Dia")
    if saldo > 0:
        st.success(f"Você está positiva hoje! 💚 Saldo: R$ {saldo:,.2f}")
        st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        st.error(f"Você gastou mais do que ganhou hoje! 💸 Saldo: R$ {saldo:,.2f}")
        st.caption("Tá plantando dinheiro, né linda?")
    else:
        st.warning("Zerada. Saldo: R$ 0,00")
        st.caption("Café preto e foco!")

    # Botão de gerar relatório em PDF
    if st.button("📄 Gerar Relatório em PDF"):
        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 14)
                self.cell(0, 10, "Café du Contrôle - Relatório do Dia", ln=True, align="C")

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Data: {hoje}", ln=True)
        pdf.cell(0, 10, f"Total de Entradas: R$ {total_entradas:,.2f}", ln=True)
        pdf.cell(0, 10, f"Total de Gastos: R$ {total_saidas:,.2f}", ln=True)
        pdf.cell(0, 10, f"Saldo do Dia: R$ {saldo:,.2f}", ln=True)

        if saldo > 0:
            pdf.multi_cell(0, 10, "Você está positiva hoje!\nVou começar a te chamar de Senhora... e com voz aveludada!")
        elif saldo < 0:
            pdf.multi_cell(0, 10, "Você gastou mais do que ganhou hoje!\nTá plantando dinheiro, né linda?")
        else:
            pdf.multi_cell(0, 10, "Zerada. Saldo: R$ 0,00\nCafé preto e foco!")

        pdf_output = pdf.output(dest="S").encode("latin-1")
        b64_pdf = base64.b64encode(pdf_output).decode('utf-8')
        href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="relatorio-cafe.pdf">📥 Clique aqui para baixar seu PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- RODAPÉ --------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center;'>
        <img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png" width="150">
        <br>
        <small>☕ Desenvolvido com carinho pela <strong>ÉdenMachine</strong></small>
    </div>
""", unsafe_allow_html=True)
