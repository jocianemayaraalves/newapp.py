import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import io
from PIL import Image
import base64

# Configuração da página
st.set_page_config(layout="wide", page_title="Café du Contrôle")

# Funções auxiliares
def carregar_dados():
    if "dados" not in st.session_state:
        st.session_state["dados"] = []
    return st.session_state["dados"]

def salvar_dados(data, tipo, descricao, valor):
    st.session_state["dados"].append({"Data": data, "Tipo": tipo, "Descrição": descricao, "Valor": valor})

def gerar_pdf(dados, periodo=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório Financeiro", ln=True, align="C")
    if periodo:
        pdf.cell(200, 10, txt=f"Período: {periodo[0]} a {periodo[1]}", ln=True, align="C")
    pdf.ln(10)
    for item in dados:
        pdf.cell(200, 10, txt=f"{item['Data']} - {item['Tipo']} - {item['Descrição']}: R$ {item['Valor']:.2f}", ln=True)
    return pdf.output(dest='S').encode('latin1')

def salvar_pdf_download(data_bytes, filename):
    b64 = base64.b64encode(data_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📄 Baixar PDF</a>'
    return href

# Estilo CSS
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .main {
            background: url('https://images.unsplash.com/photo-1504384308090-c894fdcc538d') no-repeat center center fixed;
            background-size: cover;
        }
        .sidebar .sidebar-content {
            background-color: #f8f4ed;
            color: #333;
        }
        .sidebar .sidebar-content span, .sidebar .sidebar-content label {
            color: #333 !important;
        }
        .saldo-box {
            background-color: rgba(255, 230, 0, 0.2);
            padding: 15px;
            border-radius: 10px;
            color: #333;
            font-size: 20px;
            margin-top: 10px;
        }
        .saldo-text {
            color: #000;
            font-weight: bold;
        }
        .section-title {
            color: white;
            font-size: 22px;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Logo do café e da empresa
st.image("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/cafe_logo.png", use_container_width=True)
st.markdown("##")
st.image("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png", width=100)

# Data retroativa
data_atual = st.date_input("Selecione a data:", value=datetime.today())

# Menu lateral
aba = st.sidebar.radio("Menu", ["☕ Lançamentos", "📊 Dashboard", "📁 Relatórios"])

dados = carregar_dados()

# Aba: Lançamentos
if aba == "☕ Lançamentos":
    with st.form("form_lancamento"):
        tipo = st.selectbox("Tipo", ["Entrada", "Gasto"])
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.01, format="%.2f")
        enviar = st.form_submit_button("Adicionar")
        if enviar:
            salvar_dados(data_atual.strftime("%Y-%m-%d"), tipo, descricao, valor)
            st.success("Lançamento adicionado com sucesso!")

    # Mostrar lançamentos do dia
    df = pd.DataFrame(dados)
    df_dia = df[df["Data"] == data_atual.strftime("%Y-%m-%d")]
    entradas = df_dia[df_dia["Tipo"] == "Entrada"]["Valor"].sum()
    gastos = df_dia[df_dia["Tipo"] == "Gasto"]["Valor"].sum()
    saldo = entradas - gastos

    st.markdown("<div class='section-title'>Entradas</div>", unsafe_allow_html=True)
    st.write(f"R$ {entradas:.2f}")

    st.markdown("<div class='section-title'>Gastos</div>", unsafe_allow_html=True)
    st.write(f"R$ {gastos:.2f}")

    st.markdown("<div class='section-title'>Resumo do Dia</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='saldo-box'><span class='saldo-text'>Saldo do Dia: R$ {saldo:.2f}</span></div>", unsafe_allow_html=True)

    # Botão de salvar relatório do dia
    if st.button("📄 Salvar Relatório do Dia"):
        pdf_bytes = gerar_pdf(df_dia.to_dict('records'))
        st.markdown(salvar_pdf_download(pdf_bytes, f"relatorio_{data_atual}.pdf"), unsafe_allow_html=True)

# Aba: Dashboard
elif aba == "📊 Dashboard":
    st.title("📈 Visão Geral Financeira")
    if not dados:
        st.warning("Nenhum dado cadastrado ainda.")
    else:
        df = pd.DataFrame(dados)
        df["Valor"] = pd.to_numeric(df["Valor"])
        df["Data"] = pd.to_datetime(df["Data"])

        periodo = st.date_input("Selecione o período", [df["Data"].min(), df["Data"].max()])
        df_periodo = df[(df["Data"] >= pd.to_datetime(periodo[0])) & (df["Data"] <= pd.to_datetime(periodo[1]))]

        if df_periodo.empty:
            st.info("Sem dados nesse período.")
        else:
            entradas = df_periodo[df_periodo["Tipo"] == "Entrada"]["Valor"].sum()
            gastos = df_periodo[df_periodo["Tipo"] == "Gasto"]["Valor"].sum()
            saldo = entradas - gastos

            st.markdown(f"### 💰 Entradas: R$ {entradas:.2f}")
            st.markdown(f"### 🧾 Gastos: R$ {gastos:.2f}")
            st.markdown(f"### 💎 Saldo: R$ {saldo:.2f}")

            # Gráfico de pizza
            fig1, ax1 = plt.subplots()
            ax1.pie([entradas, gastos], labels=["Entradas", "Gastos"], autopct='%1.1f%%', startangle=90, colors=["#90ee90", "#ff9999"])
            ax1.axis("equal")
            st.pyplot(fig1)

            # Gráfico de linha
            df_linha = df_periodo.groupby(["Data", "Tipo"])["Valor"].sum().unstack().fillna(0)
            fig2, ax2 = plt.subplots()
            df_linha.plot(ax=ax2, marker='o')
            ax2.set_title("Fluxo Diário")
            ax2.set_ylabel("R$ Valor")
            st.pyplot(fig2)

            # Texto explicativo
            if saldo > 0:
                st.success("Parabéns! Sua saúde financeira neste período está positiva. Continue assim!")
            elif saldo < 0:
                st.error("Atenção! Você gastou mais do que ganhou neste período.")
            else:
                st.info("Equilíbrio total! Nem lucro, nem prejuízo.")

# Aba: Relatórios
elif aba == "📁 Relatórios":
    st.title("📄 Gerar Relatório por Período")
    if not dados:
        st.warning("Você ainda não cadastrou nenhum dado.")
    else:
        df = pd.DataFrame(dados)
        df["Data"] = pd.to_datetime(df["Data"])

        periodo = st.date_input("Escolha o intervalo:", [df["Data"].min(), df["Data"].max()])
        df_periodo = df[(df["Data"] >= pd.to_datetime(periodo[0])) & (df["Data"] <= pd.to_datetime(periodo[1]))]

        if df_periodo.empty:
            st.warning("Sem dados para este intervalo.")
        else:
            st.dataframe(df_periodo)
            if st.button("📤 Baixar Relatório em PDF"):
                pdf_bytes = gerar_pdf(df_periodo.to_dict('records'), periodo=[periodo[0].strftime("%d/%m/%Y"), periodo[1].strftime("%d/%m/%Y")])
                st.markdown(salvar_pdf_download(pdf_bytes, "relatorio_periodo.pdf"), unsafe_allow_html=True)
