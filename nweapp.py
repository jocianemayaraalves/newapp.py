import streamlit as st
from PIL import Image
from datetime import datetime

# ---------------- CONFIG GERAL ----------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide"
)

# ---------------- FUNÇÃO: Fundo ----------------
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

# Fundo do app
set_background_from_url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png")

# ---------------- ESTILO CUSTOMIZADO ----------------
st.markdown("""
    <style>
        /* Menu lateral fixo */
        section[data-testid="stSidebar"] {
            background-color: #f4f1ec;
            color: #222222;
        }
        section[data-testid="stSidebar"] .css-10trblm {
            color: #222222;
        }

        /* Títulos claros */
        .titulo {
            color: #fefefe;
            font-size: 28px;
            text-shadow: 1px 1px 4px #000000cc;
            margin-top: 30px;
        }

        /* Data abaixo da logo */
        .data {
            color: #fefefe;
            text-shadow: 1px 1px 2px #000000aa;
            font-size: 16px;
        }

        /* Bloco do saldo com transparência */
        .saldo-container {
            margin-top: 15px;
            padding: 12px;
            border-radius: 10px;
            background-color: rgba(255, 255, 0, 0.2);
            color: #222;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 0 8px rgba(0,0,0,0.1);
        }

        .saldo-text {
            font-size: 20px;
            color: #222;
        }

        .saldo-container.positivo { border-left: 5px solid #00cc66; }
        .saldo-container.negativo { border-left: 5px solid #cc0033; }
        .saldo-container.zerado { border-left: 5px solid #ffaa00; }

        /* Logo Café */
        .logo-cafe-container {
            display: flex;
            justify-content: center;
            margin-bottom: 5px;
        }
        .logo-cafe-container img {
            max-width: 320px;
        }

        /* Rodapé logo Eden */
        .rodape-logo {
            width: 100%;
            text-align: center;
            margin-top: 40px;
        }
        .rodape-logo img {
            max-width: 180px;
        }

    </style>
""", unsafe_allow_html=True)

# ---------------- LOGO DO CAFÉ ----------------
with st.container():
    st.markdown('<div class="logo-cafe-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" alt="Logo Café du Contrôle"></div>', unsafe_allow_html=True)

# ---------------- DATA ----------------
data_hoje = st.date_input("Escolha a data", value=datetime.today())
st.markdown(f"<span class='data'>Data selecionada: {data_hoje.strftime('%d/%m/%Y')}</span>", unsafe_allow_html=True)

# ---------------- SISTEMA FINANCEIRO ----------------
st.markdown("<h2 class='titulo'>💰 Entradas</h2>", unsafe_allow_html=True)
salario = st.number_input("Salário", min_value=0.0, step=100.0)
renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
total_entradas = salario + renda_extra

st.markdown("<h2 class='titulo'>💸 Gastos</h2>", unsafe_allow_html=True)
fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
total_saidas = fixos + extras

# ---------------- SALDO ----------------
st.markdown("<h2 class='titulo'>📊 Resumo do Dia</h2>", unsafe_allow_html=True)
st.markdown(f"<strong>Total de Entradas:</strong> R$ {total_entradas:,.2f}", unsafe_allow_html=True)
st.markdown(f"<strong>Total de Gastos:</strong> R$ {total_saidas:,.2f}", unsafe_allow_html=True)

saldo = total_entradas - total_saidas

if saldo > 0:
    st.markdown(
        f"""
        <div class='saldo-container positivo'>
            <span class='saldo-text'>Você está positiva hoje! 💚 Saldo: R$ {saldo:,.2f}</span><br>
            <small>Vou começar a te chamar de Senhora... e com voz aveludada!</small>
        </div>
        """, unsafe_allow_html=True
    )
elif saldo < 0:
    st.markdown(
        f"""
        <div class='saldo-container negativo'>
            <span class='saldo-text'>Você gastou mais do que ganhou hoje! 💸 Saldo: R$ {saldo:,.2f}</span><br>
            <small>Tá plantando dinheiro, né linda?</small>
        </div>
        """, unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
        <div class='saldo-container zerado'>
            <span class='saldo-text'>Zerada. Saldo: R$ 0,00</span><br>
            <small>Café preto e foco!</small>
        </div>
        """, unsafe_allow_html=True
    )

# ---------------- RODAPÉ ----------------
st.markdown("---")
st.markdown('<div class="rodape-logo"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png" alt="Logo ÉdenMachine"></div>', unsafe_allow_html=True)
st.markdown("<center><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></center>", unsafe_allow_html=True)
