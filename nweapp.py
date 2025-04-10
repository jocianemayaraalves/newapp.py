import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide"
)

# -------------------- FUNÇÕES AUXILIARES --------------------
def set_background_from_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('{image_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def gerar_pdf(dataframe, periodo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Relatório Financeiro - {periodo}", ln=True, align="C")
    pdf.ln(10)

    for i, row in dataframe.iterrows():
        pdf.cell(200, 10, txt=f"Data: {row['Data']} | Entradas: R$ {row['Entradas']} | Gastos: R$ {row['Gastos']} | Saldo: R$ {row['Saldo']}", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio_financeiro.pdf">📄 Baixar Relatório em PDF</a>'
    return href

# -------------------- ESTILO --------------------
set_background_from_url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png")

st.markdown("""
    <style>
        .stApp, .css-18e3th9, .css-1d391kg, .css-1dp5vir, .css-1v0mbdj {
            color: #ffffff !important;
        }

        h1, h2, h3, h4 {
            color: #ffffff;
            text-shadow: 1px 1px 3px #000000;
        }

        .menu-container {
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            width: 220px;
            background-color: #2f2f2f;
            padding: 20px;
            z-index: 999;
            box-shadow: 2px 0 5px rgba(0,0,0,0.3);
        }

        .menu-container h3, .menu-container label, .menu-container span {
            color: #ffffff;
        }

        .main-content {
            margin-left: 240px;
            padding: 20px;
        }

        .saldo-box {
            background-color: rgba(255, 255, 0, 0.3);
            border-radius: 10px;
            padding: 10px;
            color: #111;
        }

        .logo-container img {
            max-width: 300px;
        }

        .eden-logo img {
            max-width: 120px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- MENU LATERAL --------------------
st.sidebar.title("☕ Café du Contrôle")
ab = st.sidebar.radio("Ir para:", ["Lançamentos", "Dashboard", "Relatórios"])

# -------------------- BANCO DE DADOS TEMPORÁRIO --------------------
if 'dados' not in st.session_state:
    st.session_state['dados'] = pd.DataFrame(columns=['Data', 'Entradas', 'Gastos', 'Saldo'])

# -------------------- CONTEÚDO PRINCIPAL --------------------
with st.container():
    st.markdown('<div class="logo-container" style="text-align:center;"><img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png"></div>', unsafe_allow_html=True)
    data_input = st.date_input("Selecione a data", datetime.now())

if ab == "Lançamentos":
    st.header("💰 Entradas")
    salario = st.number_input("Salário", min_value=0.0, step=100.0)
    renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
    total_entradas = salario + renda_extra

    st.header("💸 Gastos")
    fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
    extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
    total_saidas = fixos + extras

    saldo = total_entradas - total_saidas
    nova_linha = {"Data": data_input.strftime("%d/%m/%Y"), "Entradas": total_entradas, "Gastos": total_saidas, "Saldo": saldo}

    if st.button("Salvar Lançamento do Dia"):
        st.session_state['dados'] = pd.concat([st.session_state['dados'], pd.DataFrame([nova_linha])], ignore_index=True)
        st.success("Lançamento salvo!")

    st.header("📊 Resumo do Dia")
    with st.container():
        st.markdown(f"<div class='saldo-box'><h3>Saldo do Dia: R$ {saldo:,.2f}</h3></div>", unsafe_allow_html=True)
        if saldo > 0:
            st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
        elif saldo < 0:
            st.caption("Tá plantando dinheiro, né linda?")
        else:
            st.caption("Café preto e foco!")

elif ab == "Dashboard":
    st.header("📈 Dashboard de Período")
    periodo = st.date_input("Selecione o período", [datetime.now(), datetime.now()])
    if len(periodo) == 2:
        df_periodo = st.session_state['dados']
        df_periodo['Data'] = pd.to_datetime(df_periodo['Data'], format='%d/%m/%Y')
        df_filtrado = df_periodo[(df_periodo['Data'] >= periodo[0]) & (df_periodo['Data'] <= periodo[1])]

        if not df_filtrado.empty:
            st.subheader("Gráfico de Pizza - Entradas vs Gastos")
            fig1, ax1 = plt.subplots()
            ax1.pie([df_filtrado['Entradas'].sum(), df_filtrado['Gastos'].sum()], labels=['Entradas', 'Gastos'], autopct='%1.1f%%')
            st.pyplot(fig1)

            st.subheader("Gráfico de Linha - Saldo")
            fig2, ax2 = plt.subplots()
            ax2.plot(df_filtrado['Data'], df_filtrado['Saldo'], marker='o')
            ax2.set_title('Evolução do Saldo')
            ax2.set_ylabel('R$')
            st.pyplot(fig2)

            media = df_filtrado['Saldo'].mean()
            st.info(f"A média do saldo nesse período foi de R$ {media:,.2f}. Sua saúde financeira está {'positiva' if media >= 0 else 'negativa'} neste intervalo.")
        else:
            st.warning("Nenhum dado encontrado para o período selecionado.")

elif ab == "Relatórios":
    st.header("📄 Relatórios em PDF")
    periodo = st.date_input("Selecione o período do relatório", [datetime.now(), datetime.now()])
    if len(periodo) == 2:
        df = st.session_state['dados']
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
        df_filtro = df[(df['Data'] >= periodo[0]) & (df['Data'] <= periodo[1])]
        if not df_filtro.empty:
            pdf_link = gerar_pdf(df_filtro, f"{periodo[0].strftime('%d/%m/%Y')} - {periodo[1].strftime('%d/%m/%Y')}")
            st.markdown(pdf_link, unsafe_allow_html=True)
        else:
            st.warning("Nenhum dado encontrado para gerar relatório.")

# -------------------- RODAPÉ --------------------
st.markdown("---")
st.markdown("<div class='eden-logo' style='text-align:center;'><img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png'></div>", unsafe_allow_html=True)
st.markdown("<center><small>☕ Desenvolvido com carinho pela ÉdenMachine</small></center>", unsafe_allow_html=True)
