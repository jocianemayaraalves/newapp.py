import streamlit as st
from PIL import Image
import base64

# Função para adicionar imagem de fundo (opcional)
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Ativa a imagem de fundo (caso deseje usar)
# add_bg_from_local("caminho_para_sua_imagem_de_fundo.png")

# Centraliza logo sem título adicional
logo = Image.open("logo-cafe.png")
st.markdown(
    """
    <div style='text-align: center; margin-bottom: -20px;'>
        <img src='data:image/png;base64,{}' width='200'>
    </div>
    """.format(base64.b64encode(open("logo-cafe.png", "rb").read()).decode()), 
    unsafe_allow_html=True
)

# Estilização básica outonal + letras clarinhas
st.markdown("""
    <style>
        h1, h2, h3, h4, h5, h6, p, label, span, .stTextInput>div>div>input {
            color: #f0e6da !important;
        }
        .stTextInput>div>div>input {
            background-color: #fdfaf7 !important;
        }
        .stApp {
            font-family: 'Trebuchet MS', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Abaixo segue o restante do seu app (entradas, saídas etc.)

st.header("💰 Entradas")
salario = st.number_input("Salário", step=0.01)
renda_extra = st.number_input("Renda extra", step=0.01)

st.header("💸 Saídas")
gastos_fixos = st.number_input("Gastos fixos", step=0.01)
gastos_extras = st.number_input("Gastos extras", step=0.01)

# Cálculo simples
total_entradas = salario + renda_extra
total_saidas = gastos_fixos + gastos_extras
saldo = total_entradas - total_saidas

st.markdown("---")
st.subheader("📊 Resumo do Dia:")

if saldo > 0:
    st.success(f"Saldo positivo de R${saldo:.2f} — *Vou começar a te chamar de Senhora... e com voz aveludada!*")
elif saldo < 0:
    st.error(f"Saldo negativo de R${saldo:.2f} — *Tá plantando dinheiro, né linda?*")
else:
    st.info("Saldo zerado — *Tá equilibrada, igual café com leite!*")
