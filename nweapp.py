import streamlit as st
from PIL import Image
from datetime import date

# === Estilos personalizados ===
st.markdown("""
    <style>
        /* Plano de fundo */
        .stApp {
            background-image: url('https://raw.githubusercontent.com/seu-usuario/cafe-du-controle/main/bg.png');
            background-size: cover;
            background-attachment: fixed;
        }

        /* Títulos com brilho */
        h1, h2, h3 {
            color: #ffffff;
            text-shadow: 2px 2px 5px #000000, 0 0 10px #d9a441;
        }

        /* Textos gerais */
        .css-10trblm, .css-1v3fvcr {
            color: #f2f2f2 !important;
        }

        label {
            color: #f0f0f0 !important;
            font-weight: bold;
        }

        /* Caixa de entrada */
        .stTextInput>div>div>input {
            background-color: #ffffffcc;
            color: #000000;
        }

        /* Caixa de data */
        .stDateInput>div>div>input {
            background-color: #ffffffcc;
            color: #000000;
        }

        /* Mensagem inicial */
        .mensagem-inicial {
            font-size: 20px;
            font-weight: bold;
            color: #ffffff;
            text-shadow: 1px 1px 3px #000000;
        }
    </style>
""", unsafe_allow_html=True)

# === Logo ===
logo = Image.open("logo.png")
st.image(logo, width=250)

# === Título e Mensagem ===
st.markdown("<h1 style='text-align: center;'>Café du Contrôle</h1>", unsafe_allow_html=True)
st.markdown("<p class='mensagem-inicial' style='text-align: center;'>Toma um café e organiza teu dinheiro, mulher!</p>", unsafe_allow_html=True)

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
st.markdown(f"<p style='color: #f0f0f0;'>Entradas: R${entradas:.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #f0f0f0;'>Saídas: R${saidas:.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #f0f0f0; font-weight: bold;'>Saldo: R${saldo:.2f}</p>", unsafe_allow_html=True)

# === Mensagens engraçadas ===
if saldo < 0:
    st.markdown("<p style='color: #ffcccc;'>Tá plantando dinheiro, né linda?</p>", unsafe_allow_html=True)
elif saldo > 0:
    st.markdown("<p style='color: #ccffcc;'>Vou começar a te chamar de Senhora... e com voz aveludada!</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color: #ffffcc;'>Dia neutro, mas com café fica melhor!</p>", unsafe_allow_html=True)
