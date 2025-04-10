import streamlit as st
import datetime

# === ESTILO E FUNDO COM IMAGEM ===
st.markdown(
    f"""
    <style>
    /* Imagem de fundo fixa no app */
    .stApp {{
        background: url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/fundo-cafe-anime.jpg") no-repeat center center fixed;
        background-size: cover;
    }}

    /* Container do conteúdo com fundo branco translúcido */
    [data-testid="stAppViewContainer"] > .main {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 1rem;
    }}

    /* Texto com tom mais escuro */
    div, p, label, h1, h2, h3, h4 {{
        color: #3b2e2a;
        font-family: 'Georgia', serif;
    }}

    /* Inputs estilizados */
    input, textarea, select {{
        background-color: rgba(255,255,255,0.95);
        border-radius: 8px;
        border: 1px solid #dcbfa8;
        padding: 0.5em;
    }}

    /* Botões */
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
    </style>
    """,
    unsafe_allow_html=True
)

# === CONTEÚDO DO APP ===
st.title("☕ Café du Contrôle")
st.subheader("Toma um café e organiza teu dinheiro, mulher!")

# ENTRADAS
st.markdown("### 📥 Entradas")
salario = st.number_input("Salário", min_value=0.0, format="%.2f")
renda_extra = st.number_input("Renda extra", min_value=0.0, format="%.2f")

# SAÍDAS
st.markdown("### 💸 Saídas")
gastos_fixos = st.number_input("Gastos fixos", min_value=0.0, format="%.2f")
gastos_extras = st.number_input("Gastos extras", min_value=0.0, format="%.2f")

# DATA
data = st.date_input("Data", value=datetime.date.today())

# CÁLCULO
entradas = salario + renda_extra
saidas = gastos_fixos + gastos_extras
saldo = entradas - saidas

# RESULTADO
st.markdown("### 🧾 Resumo do Dia:")
st.write(f"**Entradas**: R$ {entradas:.2f}")
st.write(f"**Saídas**: R$ {saidas:.2f}")
st.write(f"**Saldo**: R$ {saldo:.2f}")

# MENSAGEM DIVERTIDA
if saldo < 0:
    st.error("Tá plantando dinheiro, né linda?")
elif saldo > 0:
    st.success("Vou começar a te chamar de Senhora... e com voz aveludada!")
else:
    st.info("Equilibrou tudo hoje. Igual coração de mãe!")

