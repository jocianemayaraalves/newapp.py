import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime

# Configuração da página
st.set_page_config(layout="wide", page_title="Café du Contrôle")

# Estilos personalizados
st.markdown("""
    <style>
        body {
            background-color: #2c1e1e;
            color: white;
        }
        .menu {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            height: 100vh;
            color: #000;
        }
        .menu h2 {
            color: #000;
        }
        .section-title {
            font-size: 24px;
            color: white;
        }
        .saldo-container {
            background-color: rgba(255, 255, 0, 0.2);
            border-radius: 10px;
            padding: 10px;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# Função para salvar PDF
def salvar_pdf(data_str, entradas, gastos, saldo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Relatório do Dia - {data_str}", ln=True)
    pdf.cell(200, 10, txt=f"Entradas: R$ {entradas:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Gastos: R$ {gastos:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Saldo: R$ {saldo:.2f}", ln=True)
    filename = f"relatorio_{data_str.replace('/', '-')}.pdf"
    pdf.output(filename)
    return filename

# Sidebar/Menu Lateral
with st.sidebar:
    st.markdown("<div class='menu'>", unsafe_allow_html=True)
    st.image("logo-cafe.png", use_container_width=False, width=250)
    st.title("Menu")
    aba = st.radio("Ir para:", ["Lançamentos", "Dashboard", "Relatórios"])
    st.markdown("</div>", unsafe_allow_html=True)

# Logo da Eden
st.markdown("""
    <div style='position: fixed; bottom: 10px; left: 50%; transform: translateX(-50%);'>
        <img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png' width='100'>
    </div>
""", unsafe_allow_html=True)

# Data e Tabelas
st.title("Café du Contrôle")
data = st.date_input("Selecione a data:", value=datetime.today())
data_str = data.strftime("%d/%m/%Y")

if "registros" not in st.session_state:
    st.session_state.registros = []

if aba == "Lançamentos":
    st.subheader("Entradas")
    entrada = st.number_input("Valor da Entrada", min_value=0.0, step=0.01)
    st.subheader("Gastos")
    gasto = st.number_input("Valor do Gasto", min_value=0.0, step=0.01)
    categoria = st.text_input("Categoria do Gasto")
    if st.button("Adicionar"):
        st.session_state.registros.append({"Data": data, "Entrada": entrada, "Gasto": gasto, "Categoria": categoria})

    # Resumo do dia
    df = pd.DataFrame(st.session_state.registros)
    df_dia = df[df["Data"] == data]
    entradas = df_dia["Entrada"].sum()
    gastos = df_dia["Gasto"].sum()
    saldo = entradas - gastos

    st.subheader("Resumo do Dia")
    st.dataframe(df_dia, use_container_width=True)
    
    st.markdown(f"""
        <div class='saldo-container'>
            <h4 style='color: white;'>Saldo do dia ({data_str}): R$ {saldo:.2f}</h4>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Salvar relatório do dia"):
        salvar_pdf(data_str, entradas, gastos, saldo)
        st.success("Relatório salvo com sucesso!")

elif aba == "Dashboard":
    st.subheader("Análise de Período")
    periodo = st.date_input("Selecione o período", [datetime.today(), datetime.today()])
    df = pd.DataFrame(st.session_state.registros)

    if not df.empty:
        df["Data"] = pd.to_datetime(df["Data"])
        df_periodo = df[(df["Data"] >= pd.to_datetime(periodo[0])) & (df["Data"] <= pd.to_datetime(periodo[1]))]

        if not df_periodo.empty:
            entradas_totais = df_periodo["Entrada"].sum()
            gastos_totais = df_periodo["Gasto"].sum()
            saldo_total = entradas_totais - gastos_totais

            col1, col2 = st.columns(2)

            with col1:
                st.write("Distribuição de Gastos")
                fig, ax = plt.subplots()
                df_gastos = df_periodo.groupby("Categoria")["Gasto"].sum()
                ax.pie(df_gastos, labels=df_gastos.index, autopct="%1.1f%%")
                st.pyplot(fig)

            with col2:
                st.write("Evolução do Saldo")
                df_periodo_grouped = df_periodo.groupby("Data").agg({"Entrada": "sum", "Gasto": "sum"})
                df_periodo_grouped["Saldo"] = df_periodo_grouped["Entrada"] - df_periodo_grouped["Gasto"]
                st.line_chart(df_periodo_grouped["Saldo"])

            st.write("Resumo:")
            if saldo_total > 0:
                st.success(f"Você está com saldo positivo! R$ {saldo_total:.2f}")
            elif saldo_total < 0:
                st.error(f"Cuidado! Você está no vermelho. Saldo: R$ {saldo_total:.2f}")
            else:
                st.warning("Saldo zerado.")
        else:
            st.warning("Nenhum dado encontrado para o período selecionado.")
    else:
        st.warning("Nenhum dado registrado ainda.")

elif aba == "Relatórios":
    st.subheader("Gerar Relatório em PDF por Período")
    periodo_pdf = st.date_input("Período do relatório", [datetime.today(), datetime.today()], key="relatorio")
    df = pd.DataFrame(st.session_state.registros)

    if not df.empty:
        df["Data"] = pd.to_datetime(df["Data"])
        df_pdf = df[(df["Data"] >= pd.to_datetime(periodo_pdf[0])) & (df["Data"] <= pd.to_datetime(periodo_pdf[1]))]
        if not df_pdf.empty:
            entradas = df_pdf["Entrada"].sum()
            gastos = df_pdf["Gasto"].sum()
            saldo = entradas - gastos
            if st.button("Gerar PDF"):
                nome_arquivo = salvar_pdf(f"{periodo_pdf[0].strftime('%d-%m-%Y')}_a_{periodo_pdf[1].strftime('%d-%m-%Y')}", entradas, gastos, saldo)
                st.success(f"Relatório salvo como {nome_arquivo}")
        else:
            st.warning("Nenhum dado encontrado para o período.")
    else:
        st.warning("Nenhum dado registrado ainda.")
