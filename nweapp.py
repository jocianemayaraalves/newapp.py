import streamlit as st
from PIL import Image
from datetime import datetime

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="centered"
)

# -------------------- FUNÇÃO PARA IMAGEM DE FUNDO --------------------
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
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }
        .logo-container img {
            max-width: 250px;
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
    </style>
""", unsafe_allow_html=True)

# -------------------- LOGO --------------------
with st.container():
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" alt="Logo Café du Contrôle"></div>', unsafe_allow_html=True)

# -------------------- SISTEMA FINANCEIRO --------------------
st.header("💰 Entradas")
salario = st.number_input("Salário", min_value=0.0, step=100.0)
renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
total_entradas = salario + renda_extra

st.header("💸 Gastos")
fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
total_saidas = fixos + extras

# -------------------- RESUMO --------------------
hoje = datetime.now().strftime("%d/%m/%Y")

st.header("📊 Resumo do Dia")
st.markdown(f"<span style='color:#fff8e7; font-size:18px'><strong>Data:</strong> {hoje}</span>", unsafe_allow_html=True)
st.markdown(f"<span style='color:#fff8e7; font-size:18px'><strong>Total de Entradas:</strong> R$ {total_entradas:,.2f}</span>", unsafe_allow_html=True)
st.markdown(f"<span style='color:#fff8e7; font-size:18px'><strong>Total de Gastos:</strong> R$ {total_saidas:,.2f}</span>", unsafe_allow_html=True)

saldo = total_entradas - total_saidas

if saldo > 0:
    st.markdown(
        f"<div style='background-color: #264d33; padding: 15px; border-radius: 10px;'>"
        f"<span style='color:#fff8e7; font-size:18px;'><strong>Você está positiva hoje! 💚 Saldo: R$ {saldo:,.2f}</strong></span>"
        f"</div>", unsafe_allow_html=True
    )
    st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")

elif saldo < 0:
    st.markdown(
        f"<div style='background-color: #592c28; padding: 15px; border-radius: 10px;'>"
        f"<span style='color:#fff8e7; font-size:18px;'><strong>Você gastou mais do que ganhou hoje! 💸 Saldo: R$ {saldo:,.2f}</strong></span>"
        f"</div>", unsafe_allow_html=True
    )
    st.caption("Tá plantando dinheiro, né linda?")

else:
    st.markdown(
        f"<div style='background-color: #8c6b30; padding: 15px; border-radius: 10px;'>"
        f"<span style='color:#fff8e7; font-size:18px;'><strong>Zerada. Saldo: R$ 0,00</strong></span>"
        f"</div>", unsafe_allow_html=True
    )
    st.caption("Café preto e foco!")

# -------------------- RODAPÉ COM LOGO ÉDEN --------------------
st.markdown("---")
st.markdown("<center><small>☕ Desenvolvido com carinho pela <strong>ÉdenMachine</strong></small></center>", unsafe_allow_html=True)

# Adicionando logo da ÉdenMachine
eden_logo = Image.open("/mnt/data/eden-machine-logo-removebg-preview.png")
st.image(eden_logo, width=120)
