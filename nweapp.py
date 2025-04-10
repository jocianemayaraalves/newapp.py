import streamlit as st
from PIL import Image
from datetime import datetime
from fpdf import FPDF
import base64

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide"
)

# -------------------- FUNÇÕES --------------------
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

# Função para gerar PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Relatório Financeiro - Café du Contrôle", 0, 1, "C")

    def chapter_body(self, data):
        self.set_font("Arial", "", 12)
        for linha in data:
            self.cell(0, 10, linha, 0, 1)

    def create_pdf(self, data):
        self.add_page()
        self.chapter_body(data)

# Função para download do PDF
def gerar_download_pdf(texto):
    pdf = PDF()
    pdf.create_pdf(texto)
    pdf_output = pdf.output(dest='S').encode('latin1')
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio_financeiro.pdf">📄 Clique aqui para baixar o PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

# -------------------- IMAGEM DE FUNDO --------------------
set_background_from_url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png")

# -------------------- ESTILO --------------------
st.markdown("""
    <style>
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 5px;
        }
        .logo-container img {
            max-width: 280px;
        }
        .eden-logo {
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }
        .eden-logo img {
            max-width: 200px;
        }
        h1, h2, h3, .titulo-sessao {
            color: #fefefe;
            text-shadow: 1px 1px 4px #000000cc;
        }
        .stMarkdown, .stTextInput > label, .stNumberInput > label {
            color: #ffffff !important;
        }
        .main > div {
            padding-top: 20px;
            background-color: rgba(255, 255, 0, 0.2);
            border-radius: 10px;
        }
        .menu-lateral {
            position: fixed;
            top: 0;
            left: 0;
            height: 100%;
            width: 250px;
            background-color: rgba(0, 0, 0, 0.8);
            padding: 20px;
            z-index: 9999;
        }
        .menu-lateral h2, .menu-lateral a {
            color: #fff;
        }
        .saldo {
            color: #1c1c1c;
            font-size: 20px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- MENU LATERAL --------------------
with st.sidebar:
    st.markdown("<div class='menu-lateral'>", unsafe_allow_html=True)
    st.markdown("## ☕ Menu")
    aba = st.radio("Escolha uma opção:", ["Lançamentos", "Relatório em PDF", "Sobre"])
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- LOGO --------------------
st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" alt="Logo Café du Contrôle"></div>', unsafe_allow_html=True)

# -------------------- DATA MODIFICÁVEL --------------------
data_input = st.date_input("Data do lançamento:", value=datetime.now())
data_formatada = data_input.strftime("%d/%m/%Y")

# -------------------- SISTEMA PRINCIPAL --------------------
if aba == "Lançamentos":
    st.markdown("<h2 class='titulo-sessao'>💰 Entradas</h2>", unsafe_allow_html=True)
    salario = st.number_input("Salário", min_value=0.0, step=100.0)
    renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
    total_entradas = salario + renda_extra

    st.markdown("<h2 class='titulo-sessao'>💸 Gastos</h2>", unsafe_allow_html=True)
    fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
    extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
    total_saidas = fixos + extras

    saldo = total_entradas - total_saidas

    st.markdown("<h2 class='titulo-sessao'>📊 Resumo do Dia</h2>", unsafe_allow_html=True)
    st.markdown(f"**Data do Lançamento:** {data_formatada}")
    st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
    st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")

    st.markdown("<h2 class='titulo-sessao'>💼 Saldo do Dia</h2>", unsafe_allow_html=True)
    if saldo > 0:
        st.success(f"💚 <span class='saldo'>Você está positiva! Saldo: R$ {saldo:,.2f}</span>", unsafe_allow_html=True)
        st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        st.error(f"💸 <span class='saldo'>Você gastou mais do que ganhou! Saldo: R$ {saldo:,.2f}</span>", unsafe_allow_html=True)
        st.caption("Tá plantando dinheiro, né linda?")
    else:
        st.warning("<span class='saldo'>Zerada. Saldo: R$ 0,00</span>", unsafe_allow_html=True)
        st.caption("Café preto e foco!")

elif aba == "Relatório em PDF":
    st.markdown("## 📄 Gerar Relatório")
    if st.button("Gerar Relatório em PDF"):
        conteudo = [
            f"Data: {data_formatada}",
            f"Salário: R$ {salario:,.2f}",
            f"Renda Extra: R$ {renda_extra:,.2f}",
            f"Gastos Fixos: R$ {fixos:,.2f}",
            f"Gastos Variáveis: R$ {extras:,.2f}",
            f"Saldo: R$ {saldo:,.2f}"
        ]
        gerar_download_pdf(conteudo)

elif aba == "Sobre":
    st.markdown("## Sobre o Projeto")
    st.write("Café du Contrôle é um app de controle financeiro com uma vibe acolhedora e charmosa. Desenvolvido com carinho para te ajudar a dominar suas finanças com humor e estilo!")

# -------------------- RODAPÉ --------------------
st.markdown("<div class='eden-logo'><img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png' alt='Logo ÉdenMachine'></div>", unsafe_allow_html=True)
st.markdown("<center><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></center>", unsafe_allow_html=True)
