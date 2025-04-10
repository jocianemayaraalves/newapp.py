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

# -------------------- FUNÇÃO DE FUNDO --------------------
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

# -------------------- ESTILOS --------------------
st.markdown("""
    <style>
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
            background-color: rgba(0,0,0,0.4); 
            border-radius: 10px;
            padding: 20px;
        }

        .sidebar .sidebar-content {
            background-color: rgba(255, 255, 255, 0.15);
        }

        .css-1d391kg { /* Sidebar width fix */
            width: 250px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- MENU LATERAL --------------------
with st.sidebar:
    st.header("☕ Menu")
    menu = st.radio("Navegar para:", ["Início", "Relatórios futuros", "Sobre"])

# -------------------- CONTEÚDO PRINCIPAL --------------------
if menu == "Início":
    # Logo principal
    st.markdown('<div class="logo-container" style="text-align: center;"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" alt="Logo Café du Contrôle"></div>', unsafe_allow_html=True)

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

    # -------------------- SALDO EM DESTAQUE --------------------
    saldo_box = f"""
    <div style="background-color: #fff9e6; padding: 20px; border-radius: 10px; margin-top: 20px; box-shadow: 0 0 10px #00000055;">
        <h3 style="color: #4b2e00; text-align: center;">
            Saldo do Dia: R$ {saldo:,.2f}
        </h3>
        <p style="text-align: center; font-style: italic; color: #4b2e00;">
    """

    if saldo > 0:
        mensagem = "💚 Você está positiva hoje! <br>Vou começar a te chamar de Senhora... e com voz aveludada!"
    elif saldo < 0:
        mensagem = "💸 Você gastou mais do que ganhou hoje! <br>Tá plantando dinheiro, né linda?"
    else:
        mensagem = "⚠️ Zerada. Saldo: R$ 0,00 <br>Café preto e foco!"

    saldo_box += mensagem + "</p></div>"
    st.markdown(saldo_box, unsafe_allow_html=True)

# -------------------- SOBRE --------------------
elif menu == "Sobre":
    st.subheader("☕ Café du Contrôle")
    st.markdown("Organize suas finanças de forma acolhedora e divertida. Uma criação com amor da **ÉdenMachine**.")
    st.markdown("---")

# -------------------- LOGO DA ÉDEN --------------------
st.markdown("""
    <div style="position: relative; bottom: 0; width: 100%; text-align: center; margin-top: 50px;">
        <img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png" style="max-height: 100px;" />
        <p style="color: white; font-size: 12px;">Desenvolvido com carinho pela ÉdenMachine</p>
    </div>
""", unsafe_allow_html=True)
