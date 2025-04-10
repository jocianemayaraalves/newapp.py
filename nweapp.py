import streamlit as st
import datetime

# === ESTILO COMPLETO COM FUNDO, LOGO, ANIMAÇÃO E RODAPÉ ===
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/fundo-cafe-anime.jpg") no-repeat center center fixed;
        background-size: cover;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        background-color: rgba(255, 255, 255, 0.88);
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
        background: linear-gradient(145deg, #b88c66, #5c4033, #8e7c6a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        font-family: 'Georgia', serif;
    }}

    h2, .stSubheader {{
        color: #4e3b2c;
        font-size: 1.3em;
        font-weight: 600;
        text-shadow: 1px 1px 1px #fff4ec;
    }}

    div, p, label {{
        color: #3a2f28;
        font-family: 'Georgia', serif;
    }}

    input, textarea, select {{
        background-color: rgba(255,255,255,0.95);
        border-radius: 8px;
        border: 1px solid #dcbfa8;
        padding: 0.5em;
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

    <!-- LOGO personalizada -->
    <img id="logo" src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe-du-controle.png">

    <!-- RODAPÉ -->
    <footer>
        Seu controle financeiro com cheiro de café quente ☕
    </footer>
    """,
    unsafe_allow_html=True
)

# === CONTEÚDO DO APP ===
st.title("☕ Café du Contrôle")
st.subheader("Toma um café e organiza teu dinheiro, mulher!")

st.markdown("### 📥 Entradas")
salario = st.number_input("Salário", min_value=0.0, format="%.2f")
renda_extra = st.number_input("Renda extra", min_value=0.0, format="%.2f")

st.markdown("### 💸 Saídas")
gastos_fixos = st.number_input("Gastos fixos", min_value=0.0, format="%.2f")
gastos_extras = st.number_input("Gastos extras", min_value=0.0, format="%.2f")

data = st.date_input("Data", value=datetime.date.today())

entradas = salario + renda_extra
saidas = gastos_fixos + gastos_extras
saldo = entradas - saidas

st.markdown("### 🧾 Resumo do Dia:")
st.write(f"**Entradas**: R$ {entradas:.2f}")
st.write(f"**Saídas**: R$ {saidas:.2f}")
st.write(f"**Saldo**: R$ {saldo:.2f}")

if saldo < 0:
    st.error("Tá plantando dinheiro, né linda?")
elif saldo > 0:
    st.success("Vou começar a te chamar de Senhora... e com voz aveludada!")
else:
    st.info("Equilibrou tudo hoje. Igual coração de mãe!")
