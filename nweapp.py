import streamlit as st
from PIL import Image
from datetime import datetime

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="centered"
)

# Função para aplicar imagem de fundo via URL
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

# Define imagem de fundo (substitua o link se necessário)
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

        .main > div {{
            padding-top: 20px;
            background-color: rgba(0,0,0,0.4); 
            border-radius: 10px;
        }}
    </style>
""", unsafe_allow_html=True)

# -------------------- LOGO --------------------
with st.container():
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" alt="Logo Café du Contrôle"></div>', unsafe_allow_html=True)

# -------------------- SISTEMA FINANCEIRO --------------------
st.title("Controle Financeiro")

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

if saldo > 0:
    st.success(f"Você está positiva hoje! 💚 Saldo: R$ {saldo:,.2f}")
    st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
elif saldo < 0:
    st.error(f"Você gastou mais do que ganhou hoje! 💸 Saldo: R$ {saldo:,.2f}")
    st.caption("Tá plantando dinheiro, né linda?")
else:
    st.warning("Zerada. Saldo: R$ 0,00")
    st.caption("Café preto e foco!")

# Rodapé
st.markdown("---")
st.markdown("<center><small>☕ Desenvolvido com carinho no Café du Contrôle</small></center>", unsafe_allow_html=True)
