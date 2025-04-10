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

# -------------------- FUNÇÃO PARA FUNDO --------------------
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

set_background_from_url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png")

# -------------------- ESTILOS --------------------
st.markdown("""
    <style>
        .sidebar .sidebar-content {{
            background-color: #f4f4f4;
        }}

        .sidebar .sidebar-content * {{
            color: #2c2c2c !important;
        }}

        .logo-container {{
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }}

        .logo-container img {{
            max-width: 280px;
        }}

        h1, h2, h3 {{
            color: #fefefe;
            text-shadow: 1px 1px 4px #000000cc;
        }}

        .custom-header {{
            color: #fefefe;
            font-size: 28px;
            text-shadow: 1px 1px 4px #000000cc;
        }}

        .resumo-container {{
            background-color: rgba(255, 255, 0, 0.2);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }}

        .saldo-label {{
            font-weight: bold;
            color: #333333;
            font-size: 20px;
        }}

        .footer-logo {{
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }}

        .footer-logo img {{
            max-height: 80px;
        }}
    </style>
""", unsafe_allow_html=True)

# -------------------- MENU LATERAL --------------------
st.sidebar.title("☕ Café du Contrôle")
menu = st.sidebar.radio("Navegação", ["Dashboard", "Relatório PDF"])

# -------------------- LOGO E DATA --------------------
with st.container():
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" alt="Logo Café du Contrôle"></div>', unsafe_allow_html=True)

    data_lancamento = st.date_input("Data de Lançamento", datetime.now())
    data_formatada = data_lancamento.strftime("%d/%m/%Y")

# -------------------- DASHBOARD --------------------
if menu == "Dashboard":
    st.markdown("<h2 class='custom-header'>💰 Entradas</h2>", unsafe_allow_html=True)
    salario = st.number_input("Salário", min_value=0.0, step=100.0)
    renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
    total_entradas = salario + renda_extra

    st.markdown("<h2 class='custom-header'>💸 Gastos</h2>", unsafe_allow_html=True)
    fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
    extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
    total_saidas = fixos + extras

    saldo = total_entradas - total_saidas

    st.markdown("""
        <div class='resumo-container'>
            <h2 class='custom-header'>📊 Resumo do Dia</h2>
            <p class='saldo-label'>Data: {}</p>
            <p class='saldo-label'>Total de Entradas: R$ {:,.2f}</p>
            <p class='saldo-label'>Total de Gastos: R$ {:,.2f}</p>
    """.format(data_formatada, total_entradas, total_saidas), unsafe_allow_html=True)

    if saldo > 0:
        st.markdown(f"<p class='saldo-label'>Saldo: R$ {saldo:,.2f}</p>", unsafe_allow_html=True)
        st.success("Você está positiva hoje! 💚")
        st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        st.markdown(f"<p class='saldo-label'>Saldo: R$ {saldo:,.2f}</p>", unsafe_allow_html=True)
        st.error("Você gastou mais do que ganhou hoje! 💸")
        st.caption("Tá plantando dinheiro, né linda?")
    else:
        st.markdown(f"<p class='saldo-label'>Saldo: R$ {saldo:,.2f}</p>", unsafe_allow_html=True)
        st.warning("Zerada. Saldo: R$ 0,00")
        st.caption("Café preto e foco!")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- RELATÓRIO PDF --------------------
elif menu == "Relatório PDF":
    st.header("📄 Gerar Relatório")

    if st.button("📄 Gerar Relatório em PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Relatório Diário - Café du Contrôle", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Data: {data_formatada}", ln=True)
        pdf.cell(200, 10, txt=f"Salário: R$ {salario:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Renda Extra: R$ {renda_extra:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Gastos Fixos: R$ {fixos:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Gastos Variáveis: R$ {extras:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Saldo do Dia: R$ {saldo:,.2f}", ln=True)

        pdf_output = f"relatorio_{data_formatada}.pdf"
        pdf.output(pdf_output)

        with open(pdf_output, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="{pdf_output}">📥 Clique aqui para baixar o relatório</a>'
            st.markdown(href, unsafe_allow_html=True)

# -------------------- RODAPÉ --------------------
st.markdown("""
    <div class="footer-logo">
        <img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png" alt="ÉdenMachine Logo">
    </div>
    <center><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></center>
""", unsafe_allow_html=True)
