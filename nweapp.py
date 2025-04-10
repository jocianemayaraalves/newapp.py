import streamlit as st
from PIL import Image
import base64

# Função para adicionar imagem de fundo
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Adiciona a imagem de fundo
add_bg_from_local("bg.png")

# Centraliza a logo
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{}' width='250'>
    </div>
    """.format(base64.b64encode(open("logo-cafe.png", "rb").read()).decode()), 
    unsafe_allow_html=True
)

# Estilização dos textos
st.markdown("""
    <style>
        h1, h2, h3, h4, h5, h6, p, label, span {
            color: #f0e6da !important;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input {
            background-color: #ffffffcc;
            color: #000000;
        }
        .stApp {
            font-family: 'Trebuchet MS', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Conteúdo do aplicativo
st.header("💰 Entradas")
salario = st.number_input("Salário", step=0.01)
renda_extra = st.number_input("Renda extra", step=0.01)

st.header("💸 Saídas")
gastos_fixos = st.number_input("Gastos fixos", step=0.01)
gastos_extras = st.number_input("Gastos extras", step=0.01)

# Cálculo do saldo
total_entradas = salario + renda_extra
total_saidas = gastos_fixos + gastos_extras
saldo = total_entradas - total_saidas

st.markdown("---")
st.subheader("📊 Resumo do Dia:")

if saldo > 0:
    st.success(f"Saldo positivo de R${saldo:.2f} — *Parabéns! Continue assim!*")
elif saldo < 0:
    st.error(f"Saldo negativo de R${saldo:.2f} — *Atenção! Hora de economizar!*")
else:
    st.info("Saldo zerado — *Equilíbrio é a chave!*")
