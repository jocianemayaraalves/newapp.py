import streamlit as st
from datetime import date

# === Estilo personalizado ===
st.markdown("""
    <style>
        .stApp {
            background-image: url('https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png');
            background-size: cover;
            background-attachment: fixed;
        }

        h1, h2, h3 {
            color: #ffffff;
            text-shadow: 2px 2px 4px #8B4513, 0 0 5px #FFD700;
        }

        label, .css-1cpxqw2 {
            color: #f5f5f5 !important;
        }

        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stDateInput>div>div>input {
            background-color: #ffffffdd;
            color: #000000;
        }

        .mensagem-inicial {
            font-size: 20px;
            font-weight: bold;
            color: #ffffff;
            text-shadow: 1px 1px 2px #000000;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# === Logo atualizado ===
st.image("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png", width=250)

# === Título e saudação ===
st.markdown("<h1 style='text-align: center;'>Café du Contrôle</h1>", unsafe_allow_html=True)
st.markdown("<p class='mensagem-inicial'>Toma um café e organiza teu dinheiro, mulher!</p>", unsafe_allow_html=True)

# === Entradas ===
st.subheader("📥 Entradas")
salario = st.number_input("Salário", min_value=0.0, step=0.01, format="%.2f")
renda_extra = st.number_input("Renda extra", min_value=0.0, step=0.01, format="%.2f")

# === Saídas ===
st.subheader("💸 Saídas")
gastos_fixos = st.number_input("Gastos fixos", min_value=0.0, step=0.01, format="%.2f")
gastos_extras = st.number_input("Gastos extras", min_value=0.0, step=0.01, format="%.2f")
data = st.date_input("Data", value=date.today())

# === Cálculo ===
entradas = salario + renda_extra
saidas = gastos_fixos + gastos_extras
saldo = entradas - saidas

# === Resultado ===
st.subheader("🧾 Resumo do Dia:")
st.markdown(f"<p style='color: #f5f5f5;'>Entradas: R${entradas:.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #f5f5f5;'>Saídas: R${saidas:.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #ffffff; font-weight: bold;'>Saldo: R${saldo:.2f}</p>", unsafe_allow_html=True)

# === Mensagens de humor ===
if saldo < 0:
    st.markdown("<p style='color: #ffcccc;'>Tá plantando dinheiro, né linda?</p>", unsafe_allow_html=True)
elif saldo > 0:
    st.markdown("<p style='color: #ccffcc;'>Vou começar a te chamar de Senhora... e com voz aveludada!</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color: #ffffcc;'>Dia neutro, mas com café tudo fica mais leve!</p>", unsafe_allow_html=True)
