import streamlit as st
from datetime import date

# --- CSS personalizado ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/fundo-cafe-anime.jpg") no-repeat center center fixed;
        background-size: cover;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        background-color: rgba(255, 255, 255, 0.90);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        animation: fadeIn 1.4s ease-in-out;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    h1 {{
        font-size: 3em;
        font-weight: 900;
        color: #fff;
        text-shadow: 2px 2px 3px #000, -1px -1px 2px #f5d7aa;
        font-family: 'Georgia', serif;
    }}

    h2, .stSubheader {{
        color: #502e1c;
        background-color: #f7e6d1;
        padding: 0.3em 0.8em;
        border-radius: 0.5em;
        font-weight: bold;
        font-size: 1.3em;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        display: inline-block;
        margin-top: 1.2em;
    }}

    div, p, label {{
        color: #3a2f28 !important;
        font-family: 'Georgia', serif;
        font-size: 1em;
    }}

    input, textarea, select {{
        background-color: rgba(255,255,255,0.95);
        border-radius: 8px;
        border: 1px solid #dcbfa8;
        padding: 0.5em;
        color: #3a2f28 !important;
    }}

    .stButton>button {{
        background-color: #dc9c68;
        color: white;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.3s ease-in-out;
    }}
    .stButton>button:hover {{
        background-color: #c78555;
        transform: scale(1.05);
    }}

    #logo {{
        position: fixed;
        top: 10px;
        left: 20px;
        width: 120px;
        z-index: 100;
        opacity: 0.95;
    }}

    footer {{
        position: fixed;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-size: 0.85em;
        color: #5f4436;
        font-family: 'Georgia', serif;
        background-color: rgba(255, 255, 255, 0.5);
        padding: 5px 0;
    }}
    </style>

    <img id="logo" src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe-du-controle.png">
    <footer>Seu controle financeiro com cheiro de café quente ☕</footer>
    """,
    unsafe_allow_html=True
)

# --- Título e introdução ---
st.title("☕ Café du Contrôle")
st.write("Toma um café e organiza teu dinheiro, mulher!")

# --- Entradas ---
st.markdown("### 📥 <strong>Entradas</strong>", unsafe_allow_html=True)
salario = st.number_input("Salário", min_value=0.0, format="%.2f")
renda_extra = st.number_input("Renda extra", min_value=0.0, format="%.2f")

# --- Saídas ---
st.markdown("### 💸 <strong>Saídas</strong>", unsafe_allow_html=True)
gastos_fixos = st.number_input("Gastos fixos", min_value=0.0, format="%.2f")
gastos_extras = st.number_input("Gastos extras", min_value=0.0, format="%.2f")

# --- Data ---
st.markdown("### 📅 <strong>Data</strong>", unsafe_allow_html=True)
data = st.date_input("Data", value=date.today())

# --- Resumo ---
st.markdown("### 🧾 <strong>Resumo do Dia:</strong>", unsafe_allow_html=True)
entradas = salario + renda_extra
saidas = gastos_fixos + gastos_extras
saldo = entradas - saidas

st.write(f"**Entradas**: R${entradas:,.2f}")
st.write(f"**Saídas**: R${saidas:,.2f}")

# Mensagem divertida
if saldo > 0:
    st.success("💰 Vou começar a te chamar de Senhora... e com voz aveludada!")
elif saldo < 0:
    st.error("🌱 Tá plantando dinheiro, né linda?")
else:
    st.info("💸 Equilíbrio é tudo, mas um cafezinho a mais não faz mal!")

