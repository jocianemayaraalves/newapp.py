import streamlit as st
import pandas as pd
from datetime import datetime, date
from fpdf import FPDF
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
import base64

st.set_page_config(layout="wide")

if 'dados' not in st.session_state:
    st.session_state['dados'] = pd.DataFrame(columns=['Data', 'Tipo', 'Categoria', 'Valor'])

def adicionar_dado(data, tipo, categoria, valor):
    novo_dado = pd.DataFrame({'Data': [data], 'Tipo': [tipo], 'Categoria': [categoria], 'Valor': [valor]})
    st.session_state['dados'] = pd.concat([st.session_state['dados'], novo_dado], ignore_index=True)

def salvar_relatorio_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Relatório do Dia {data.strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.ln(10)

    df_dia = st.session_state['dados']
    df_dia = df_dia[df_dia['Data'] == data.strftime('%d/%m/%Y')]

    for index, row in df_dia.iterrows():
        linha = f"{row['Data']} - {row['Tipo']} - {row['Categoria']} - R$ {row['Valor']:.2f}"
        pdf.cell(200, 10, txt=linha, ln=True)

    total = df_dia[df_dia['Tipo'] == 'Entrada']['Valor'].sum() - df_dia[df_dia['Tipo'] == 'Gasto']['Valor'].sum()
    pdf.ln(10)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt=f"Saldo do dia: R$ {total:.2f}", ln=True)

    pdf.output("relatorio_dia.pdf")

# Sidebar com abas interativas
menu = st.sidebar.radio("Menu", ["Lançamentos", "Dashboard", "Relatórios"])

# Logo do Café
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
        .saldo-container {
            background-color: rgba(255, 255, 0, 0.3);
            padding: 10px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .saldo-text {
            color: #222;
            font-weight: bold;
            font-size: 18px;
        }
        .titulo-claro {
            color: white;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.image("cafe_logo.png", use_column_width=False, output_format="auto", width=250)
st.markdown(f"<div style='text-align: center;'>{date.today().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

# Lançamentos
if menu == "Lançamentos":
    st.markdown("<h2 class='titulo-claro'>Lançamentos</h2>", unsafe_allow_html=True)

    data = st.date_input("Data", value=date.today())
    tipo = st.radio("Tipo", ["Entrada", "Gasto"])
    categoria = st.text_input("Categoria")
    valor = st.number_input("Valor", min_value=0.0, step=0.01)

    if st.button("Adicionar"):
        adicionar_dado(data.strftime('%d/%m/%Y'), tipo, categoria, valor)
        st.success("Lançamento adicionado com sucesso!")

    if st.session_state['dados'].empty:
        st.info("Nenhum dado lançado ainda.")
    else:
        st.markdown("<h3 class='titulo-claro'>Resumo do Dia</h3>", unsafe_allow_html=True)
        df_dia = st.session_state['dados']
        df_dia['Data'] = pd.to_datetime(df_dia['Data'], dayfirst=True)
        df_dia = df_dia[df_dia['Data'] == pd.to_datetime(data)]

        entradas = df_dia[df_dia['Tipo'] == 'Entrada']['Valor'].sum()
        gastos = df_dia[df_dia['Tipo'] == 'Gasto']['Valor'].sum()
        saldo = entradas - gastos

        st.markdown("<div class='saldo-container'>", unsafe_allow_html=True)
        st.markdown(f"<div class='saldo-text'>Entradas: R$ {entradas:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='saldo-text'>Gastos: R$ {gastos:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='saldo-text'>Saldo do dia: R$ {saldo:.2f}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Salvar relatório do dia"):
            salvar_relatorio_pdf(pd.to_datetime(data))
            st.success("Relatório salvo com sucesso!")

# Dashboard
elif menu == "Dashboard":
    st.markdown("<h2 class='titulo-claro'>Dashboard</h2>", unsafe_allow_html=True)
    periodo = st.date_input("Selecione o período", value=(date.today(), date.today()))

    df_periodo = st.session_state['dados'].copy()
    df_periodo['Data'] = pd.to_datetime(df_periodo['Data'], errors='coerce', dayfirst=True)
    df_filtrado = df_periodo[(df_periodo['Data'] >= periodo[0]) & (df_periodo['Data'] <= periodo[1])]

    if not df_filtrado.empty:
        entradas = df_filtrado[df_filtrado['Tipo'] == 'Entrada']['Valor'].sum()
        gastos = df_filtrado[df_filtrado['Tipo'] == 'Gasto']['Valor'].sum()
        saldo = entradas - gastos

        st.markdown(f"<div class='saldo-text'>Entradas: R$ {entradas:.2f} | Gastos: R$ {gastos:.2f} | Saldo: R$ {saldo:.2f}</div>", unsafe_allow_html=True)

        fig_pizza = px.pie(df_filtrado, values='Valor', names='Categoria', title='Distribuição por Categoria')
        st.plotly_chart(fig_pizza)

        df_linha = df_filtrado.groupby('Data').sum(numeric_only=True).reset_index()
        fig_linha = px.line(df_linha, x='Data', y='Valor', title='Evolução Financeira')
        st.plotly_chart(fig_linha)

# Relatórios
elif menu == "Relatórios":
    st.markdown("<h2 class='titulo-claro'>Relatórios em PDF</h2>", unsafe_allow_html=True)
    periodo = st.date_input("Selecione o período para o relatório", value=(date.today(), date.today()))

    df_periodo = st.session_state['dados'].copy()
    df_periodo['Data'] = pd.to_datetime(df_periodo['Data'], errors='coerce', dayfirst=True)
    df_filtrado = df_periodo[(df_periodo['Data'] >= periodo[0]) & (df_periodo['Data'] <= periodo[1])]

    if not df_filtrado.empty and st.button("Gerar Relatório PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Relatório de {periodo[0].strftime('%d/%m/%Y')} a {periodo[1].strftime('%d/%m/%Y')}", ln=True, align='C')
        pdf.ln(10)

        for index, row in df_filtrado.iterrows():
            linha = f"{row['Data'].strftime('%d/%m/%Y')} - {row['Tipo']} - {row['Categoria']} - R$ {row['Valor']:.2f}"
            pdf.cell(200, 10, txt=linha, ln=True)

        pdf.output("relatorio_periodo.pdf")
        st.success("Relatório PDF gerado com sucesso!")

# Logo da ÉdenMachine
st.markdown("""<br><br><div style='text-align:center;'>
Desenvolvido com carinho pela<br>
<img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png' class='logo-eden'/>
</div>""", unsafe_allow_html=True)
