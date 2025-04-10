import streamlit as st
from PIL import Image
from datetime import datetime
from fpdf import FPDF

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide"
)

# -------------------- FUNÇÃO: Plano de fundo --------------------
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

# -------------------- CSS ESTILO --------------------
st.markdown("""
    <style>
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 0px;
        }
        .logo-container img {
            max-width: 300px;
        }
        .header-container {
            text-align: center;
            margin-top: -20px;
            margin-bottom: 20px;
        }
        h1, h2, h3 {
            color: #fefefe;
            text-shadow: 1px 1px 4px #000000cc;
        }
        .stMarkdown, .stTextInput > label, .stNumberInput > label {
            color: #fdfdfd !important;
        }
        .stSidebar {
            background-color: #1e1e1e;
        }
        .saldo {
            font-size: 20px;
            font-weight: bold;
            background-color: rgba(255, 255, 0, 0.2);
            padding: 10px;
            border-radius: 10px;
            color: #333;
            margin-bottom: 10px;
        }
        .saldo.aviso {
            color: #664d00;
        }
        .rodape-eden img {
            max-width: 100px;
            display: block;
            margin: 0 auto;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- MENU LATERAL --------------------
menu = st.sidebar.radio("📋 Menu", ["Lançamentos", "Relatório em PDF", "Sobre"])

# -------------------- LOGO CAFÉ --------------------
with st.container():
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" alt="Logo Café du Contrôle"></div>', unsafe_allow_html=True)

# -------------------- DATA --------------------
data = st.date_input("📅 Escolha a data do lançamento:", value=datetime.now(), format="DD/MM/YYYY")
data_str = data.strftime("%d/%m/%Y")

# -------------------- TELA PRINCIPAL --------------------
if menu == "Lançamentos":
    st.header("💰 Entradas")
    salario = st.number_input("Salário", min_value=0.0, step=100.0)
    renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
    total_entradas = salario + renda_extra

    st.header("💸 Gastos")
    fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
    extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
    total_saidas = fixos + extras

    st.header("📊 Resumo do Dia")
    st.markdown(f"**Data:** {data_str}")
    st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
    st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")
    saldo = total_entradas - total_saidas

    if saldo > 0:
        st.markdown(f"<div class='saldo'>💚 Você está positiva hoje! Saldo: R$ {saldo:,.2f}</div>", unsafe_allow_html=True)
        st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        st.markdown(f"<div class='saldo'>💸 Você gastou mais do que ganhou hoje! Saldo: R$ {saldo:,.2f}</div>", unsafe_allow_html=True)
        st.caption("Tá plantando dinheiro, né linda?")
    else:
        st.markdown("<div class='saldo aviso'>⚠️ Zerada. Saldo: R$ 0,00</div>", unsafe_allow_html=True)
        st.caption("Café preto e foco!")

elif menu == "Relatório em PDF":
    st.header("📄 Gerar Relatório em PDF")

    if st.button("📤 Gerar Relatório"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Relatório Financeiro - Café du Contrôle ☕", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Data: {data_str}", ln=True)
        pdf.cell(200, 10, txt=f"Entradas: R$ {total_entradas:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Gastos: R$ {total_saidas:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Saldo do Dia: R$ {saldo:,.2f}", ln=True)

        with open("relatorio.pdf", "wb") as f:
            pdf.output(f)

        with open("relatorio.pdf", "rb") as f:
            st.download_button("📥 Baixar PDF", f, file_name="relatorio.pdf")

elif menu == "Sobre":
    st.header("💡 Sobre o App")
    st.markdown("""
    O **Café du Contrôle** é uma ferramenta gratuita e charmosa para te ajudar a controlar sua vida financeira com leveza e bom humor.
    
    Desenvolvido com carinho por **Mayara**, com apoio da **ÉdenMachine** ☕💻
    """)

# -------------------- RODAPÉ ÉDEN --------------------
st.markdown("---")
st.markdown('<div class="rodape-eden"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png" alt="Logo ÉdenMachine"></div>', unsafe_allow_html=True)
st.markdown("<center><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></center>", unsafe_allow_html=True)
