import streamlit as st
import pandas as pd
from datetime import datetime, date
from fpdf import FPDF
import matplotlib.pyplot as plt
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide", page_title="Café du Contrôle")

# Inicialização de sessão
if "dados" not in st.session_state:
    st.session_state["dados"] = pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Valor"])

# Estilos personalizados
st.markdown("""
    <style>
        .logo-cafe {
            width: 250px;
            display: block;
            margin: 0 auto 10px auto;
        }
        .logo-eden {
            width: 130px;
            display: block;
            margin: 20px auto 0 auto;
        }
        body {
            background-color: #2c1e1e;
            color: white;
        }
        .saldo-container {
            background-color: rgba(255, 255, 0, 0.2);
            border-radius: 10px;
            padding: 10px;
            color: black;
        }
        .saldo-text {
            color: #222;
            font-weight: bold;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Menu lateral
menu = st.sidebar.radio("Menu", ["Lançamentos", "Dashboard", "Relatórios"])
st.sidebar.image("logo-cafe.png", use_container_width=False, width=250)

# Logo da Eden
st.markdown("""
    <div style='position: fixed; bottom: 10px; left: 50%; transform: translateX(-50%);'>
        <img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png' width='100'>
    </div>
""", unsafe_allow_html=True)

# Função para adicionar dados
def adicionar_dado(data, tipo, categoria, valor):
    novo_dado = pd.DataFrame({'Data': [data], 'Tipo': [tipo], 'Categoria': [categoria], 'Valor': [valor]})
    st.session_state["dados"] = pd.concat([st.session_state["dados"], novo_dado], ignore_index=True)

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

# Lançamentos
if menu == "Lançamentos":
    st.title("Lançamentos - Café du Contrôle")
    data = st.date_input("Data", value=date.today())
    tipo = st.radio("Tipo", ["Entrada", "Gasto"])
    categoria = st.text_input("Categoria")
    valor = st.number_input("Valor", min_value=0.0, step=0.01)

    if st.button("Adicionar"):
        adicionar_dado(data.strftime("%d/%m/%Y"), tipo, categoria, valor)
        st.success("Lançamento adicionado com sucesso!")

    df = st.session_state["dados"]
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
    df_dia = df[df["Data"] == pd.to_datetime(data)]

    entradas = df_dia[df_dia["Tipo"] == "Entrada"]["Valor"].sum()
    gastos = df_dia[df_dia["Tipo"] == "Gasto"]["Valor"].sum()
    saldo = entradas - gastos

    st.markdown("<h3 class='section-title'>Resumo do Dia</h3>", unsafe_allow_html=True)
    st.dataframe(df_dia)

    st.markdown(f"""
        <div class='saldo-container'>
            <div class='saldo-text'>Entradas: R$ {entradas:.2f}</div>
            <div class='saldo-text'>Gastos: R$ {gastos:.2f}</div>
            <div class='saldo-text'>Saldo do dia: R$ {saldo:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Salvar relatório do dia"):
        salvar_pdf(data.strftime("%d/%m/%Y"), entradas, gastos, saldo)
        st.success("Relatório salvo com sucesso!")

# Dashboard
elif menu == "Dashboard":
    st.title("Dashboard - Café du Contrôle")
    periodo = st.date_input("Período", value=(date.today(), date.today()))
    df = st.session_state["dados"].copy()
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
    df_filtrado = df[(df["Data"] >= periodo[0]) & (df["Data"] <= periodo[1])]

    if not df_filtrado.empty:
        entradas = df_filtrado[df_filtrado["Tipo"] == "Entrada"]["Valor"].sum()
        gastos = df_filtrado[df_filtrado["Tipo"] == "Gasto"]["Valor"].sum()
        saldo = entradas - gastos

        st.markdown(f"<div class='saldo-text'>Entradas: R$ {entradas:.2f} | Gastos: R$ {gastos:.2f} | Saldo: R$ {saldo:.2f}</div>", unsafe_allow_html=True)

        fig_pizza = px.pie(df_filtrado, values='Valor', names='Categoria', title='Distribuição por Categoria')
        st.plotly_chart(fig_pizza)

        df_linha = df_filtrado.groupby('Data').sum(numeric_only=True).reset_index()
        fig_linha = px.line(df_linha, x='Data', y='Valor', title='Evolução Financeira')
        st.plotly_chart(fig_linha)
    else:
        st.info("Nenhum dado para o período selecionado.")

# Relatórios
elif menu == "Relatórios":
    st.title("Relatórios - Café du Contrôle")
    periodo = st.date_input("Período para o relatório", value=(date.today(), date.today()), key="relatorio")
    df = st.session_state["dados"].copy()
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
    df_filtrado = df[(df["Data"] >= periodo[0]) & (df["Data"] <= periodo[1])]

    if not df_filtrado.empty:
        entradas = df_filtrado[df_filtrado["Tipo"] == "Entrada"]["Valor"].sum()
        gastos = df_filtrado[df_filtrado["Tipo"] == "Gasto"]["Valor"].sum()
        saldo = entradas - gastos

        if st.button("Gerar Relatório PDF"):
            nome_arquivo = salvar_pdf(f"{periodo[0].strftime('%d-%m-%Y')}_a_{periodo[1].strftime('%d-%m-%Y')}", entradas, gastos, saldo)
            st.success(f"Relatório salvo como {nome_arquivo}")
    else:
        st.warning("Nenhum dado para o período selecionado.")
