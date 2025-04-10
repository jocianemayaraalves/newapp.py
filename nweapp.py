import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from fpdf import FPDF
from PIL import Image

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- FUNÇÕES AUXILIARES --------------------
def gerar_pdf(data, entradas, saidas, saldo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório Financeiro", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Data: {data}", ln=True)
    pdf.cell(200, 10, txt=f"Total de Entradas: R$ {entradas:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total de Gastos: R$ {saidas:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Saldo: R$ {saldo:,.2f}", ln=True)
    return pdf

# -------------------- ESTILO --------------------
st.markdown("""
<style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .sidebar .sidebar-content {
        background-color: #fff;
    }
    .css-1d391kg { color: #333 !important; }
    .css-1cpxqw2 { color: #333 !important; }
    h1, h2, h3, h4, h5 {
        color: #fff !important;
        text-shadow: 1px 1px 4px #000;
    }
    .saldo-box {
        background-color: rgba(255, 255, 0, 0.3);
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .saldo-text {
        font-weight: bold;
        font-size: 18px;
        color: #222;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- LOGO E DATA --------------------
st.markdown('<div style="text-align: center;"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" style="max-width: 280px;"></div>', unsafe_allow_html=True)

# Data customizável
data_input = st.date_input("Selecione a data do lançamento", value=datetime.now())
data_formatada = data_input.strftime("%d/%m/%Y")

# -------------------- MENU LATERAL --------------------
menu = st.sidebar.radio("📋 Menu", ["Lançamentos", "Dashboard", "Gerar Relatório"])

# -------------------- TELA DE LANÇAMENTOS --------------------
if menu == "Lançamentos":
    st.header("💰 Entradas")
    salario = st.number_input("Salário", min_value=0.0, step=100.0)
    renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
    total_entradas = salario + renda_extra

    st.header("💸 Gastos")
    fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
    extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
    total_saidas = fixos + extras

    saldo = total_entradas - total_saidas

    st.header("📊 Resumo do Dia")
    st.markdown(f"**Data:** {data_formatada}")
    st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
    st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")

    with st.container():
        st.markdown('<div class="saldo-box">', unsafe_allow_html=True)
        if saldo > 0:
            st.markdown(f'<div class="saldo-text">Você está positiva hoje! 💚 Saldo: R$ {saldo:,.2f}</div>', unsafe_allow_html=True)
            st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
        elif saldo < 0:
            st.markdown(f'<div class="saldo-text">Você gastou mais do que ganhou hoje! 💸 Saldo: R$ {saldo:,.2f}</div>', unsafe_allow_html=True)
            st.caption("Tá plantando dinheiro, né linda?")
        else:
            st.markdown(f'<div class="saldo-text">Zerada. Saldo: R$ 0,00</div>', unsafe_allow_html=True)
            st.caption("Café preto e foco!")
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------- DASHBOARD --------------------
elif menu == "Dashboard":
    st.header("📈 Dashboard de Períodos")
    data_inicio = st.date_input("Data de Início", value=datetime.now())
    data_fim = st.date_input("Data de Fim", value=datetime.now())

    # Exemplo de dados simulados para os gráficos
    dados = pd.DataFrame({
        'Data': pd.date_range(start=data_inicio, end=data_fim, freq='D'),
        'Entradas': pd.Series([1000 + i*10 for i in range((data_fim - data_inicio).days + 1)]),
        'Saídas': pd.Series([700 + i*8 for i in range((data_fim - data_inicio).days + 1)])
    })
    dados['Saldo'] = dados['Entradas'] - dados['Saídas']

    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots()
        ax1.pie([dados['Entradas'].sum(), dados['Saídas'].sum()], labels=['Entradas', 'Saídas'], autopct='%1.1f%%', colors=['green', 'red'])
        ax1.set_title("Distribuição Financeira")
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots()
        ax2.plot(dados['Data'], dados['Saldo'], color='blue')
        ax2.set_title("Evolução do Saldo")
        ax2.set_xlabel("Data")
        ax2.set_ylabel("Saldo")
        st.pyplot(fig2)

    saldo_medio = dados['Saldo'].mean()
    if saldo_medio > 0:
        st.success(f"💡 Sua média de saldo no período foi positiva: R$ {saldo_medio:,.2f}")
    else:
        st.error(f"⚠️ Sua média de saldo foi negativa: R$ {saldo_medio:,.2f}")

# -------------------- RELATÓRIO --------------------
elif menu == "Gerar Relatório":
    st.header("📄 Relatório em PDF")
    data = st.date_input("Selecione a data para o relatório", value=datetime.now())
    entradas = st.number_input("Total de Entradas", min_value=0.0, step=50.0, key='pdf_entradas')
    saidas = st.number_input("Total de Saídas", min_value=0.0, step=50.0, key='pdf_saidas')
    saldo_pdf = entradas - saidas

    if st.button("Gerar PDF"):
        pdf = gerar_pdf(data.strftime("%d/%m/%Y"), entradas, saidas, saldo_pdf)
        pdf.output("relatorio_financeiro.pdf")
        with open("relatorio_financeiro.pdf", "rb") as f:
            st.download_button("📥 Baixar Relatório", f, file_name="relatorio.pdf")

# -------------------- RODAPÉ --------------------
st.markdown("---")
st.markdown('<div style="text-align: center;"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png" style="width: 120px;"></div>', unsafe_allow_html=True)
st.markdown("<center><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></center>", unsafe_allow_html=True)
