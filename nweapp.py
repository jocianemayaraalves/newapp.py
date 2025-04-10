import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64
from io import BytesIO
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Café du Contrôle", layout="wide")

# Estilo personalizado
st.markdown("""
    <style>
        body {
            background-color: #2c1e1e;
        }
        .main {
            background-image: url('https://i.imgur.com/WmJpWkM.jpg');
            background-size: cover;
            background-position: center;
        }
        .block-container {
            padding: 2rem;
        }
        .sidebar .sidebar-content {
            background-color: #f8f8f8;
        }
        .css-1d391kg, .css-1v3fvcr, .css-1dp5vir {
            color: #000000;
        }
        .header, .subheader, .markdown-text-container h1, h2, h3, h4, h5, h6, p, span, div {
            color: #ffffff;
        }
        .saldo-box {
            background-color: rgba(255, 255, 0, 0.2);
            padding: 10px;
            border-radius: 10px;
            text-align: center;
        }
        .saldo-text {
            font-size: 20px;
            font-weight: bold;
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

# Logo do Café
st.image("cafe_logo.png", use_container_width=True)

# Data selecionável
data_hoje = st.date_input("Escolha uma data:", value=datetime.date.today())

# Sessões para armazenar dados
if 'dados' not in st.session_state:
    st.session_state['dados'] = pd.DataFrame(columns=['Data', 'Tipo', 'Descrição', 'Valor'])

# Menu lateral com abas
aba = st.sidebar.radio("Navegar", ["Lançamentos", "Dashboard", "Relatórios"])

# Lançamentos
if aba == "Lançamentos":
    st.subheader("📥 Entradas")
    descricao_entrada = st.text_input("Descrição da entrada")
    valor_entrada = st.number_input("Valor da entrada", min_value=0.0, step=0.01)
    if st.button("Adicionar Entrada"):
        nova_entrada = pd.DataFrame({
            'Data': [data_hoje],
            'Tipo': ['Entrada'],
            'Descrição': [descricao_entrada],
            'Valor': [valor_entrada]
        })
        st.session_state['dados'] = pd.concat([st.session_state['dados'], nova_entrada], ignore_index=True)

    st.subheader("💸 Gastos")
    descricao_saida = st.text_input("Descrição do gasto")
    valor_saida = st.number_input("Valor do gasto", min_value=0.0, step=0.01, key="gasto")
    if st.button("Adicionar Gasto"):
        nova_saida = pd.DataFrame({
            'Data': [data_hoje],
            'Tipo': ['Saída'],
            'Descrição': [descricao_saida],
            'Valor': [-valor_saida]
        })
        st.session_state['dados'] = pd.concat([st.session_state['dados'], nova_saida], ignore_index=True)

    st.subheader("📊 Resumo do Dia")
    df_hoje = st.session_state['dados'][st.session_state['dados']['Data'] == data_hoje]
    total_entrada = df_hoje[df_hoje['Tipo'] == 'Entrada']['Valor'].sum()
    total_saida = -df_hoje[df_hoje['Tipo'] == 'Saída']['Valor'].sum()
    saldo = total_entrada - total_saida

    with st.container():
        st.markdown(f"<div class='saldo-box'><span class='saldo-text'>Saldo do dia: R$ {saldo:.2f}</span></div>", unsafe_allow_html=True)

    # Botão para gerar PDF do dia
    def gerar_pdf(data, df):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Relatório - {data.strftime('%d/%m/%Y')}", ln=True, align="C")
        pdf.ln(10)
        for i, row in df.iterrows():
            pdf.cell(200, 10, txt=f"{row['Tipo']}: {row['Descrição']} - R$ {row['Valor']:.2f}", ln=True)
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        return pdf_output

    if st.button("Salvar Relatório do Dia"):
        pdf_data = gerar_pdf(data_hoje, df_hoje)
        b64 = base64.b64encode(pdf_data.getvalue()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio_{data_hoje}.pdf">📄 Baixar Relatório</a>'
        st.markdown(href, unsafe_allow_html=True)

# Dashboard
elif aba == "Dashboard":
    st.subheader("📈 Dashboard de Período")
    periodo = st.date_input("Selecione o período:", [datetime.date.today(), datetime.date.today()])
    if len(periodo) == 2:
        df_periodo = st.session_state['dados']
        df_periodo = df_periodo[(df_periodo['Data'] >= pd.to_datetime(periodo[0])) & (df_periodo['Data'] <= pd.to_datetime(periodo[1]))]
        if not df_periodo.empty:
            entrada_total = df_periodo[df_periodo['Tipo'] == 'Entrada']['Valor'].sum()
            saida_total = -df_periodo[df_periodo['Tipo'] == 'Saída']['Valor'].sum()

            st.write(f"Total de Entradas: R$ {entrada_total:.2f}")
            st.write(f"Total de Gastos: R$ {saida_total:.2f}")
            st.write(f"Saldo: R$ {entrada_total - saida_total:.2f}")

            fig1, ax1 = plt.subplots()
            ax1.pie([entrada_total, saida_total], labels=['Entradas', 'Gastos'], autopct='%1.1f%%')
            ax1.set_title("Distribuição")
            st.pyplot(fig1)

            fig2, ax2 = plt.subplots()
            df_periodo['Acumulado'] = df_periodo['Valor'].cumsum()
            df_periodo.sort_values('Data', inplace=True)
            ax2.plot(df_periodo['Data'], df_periodo['Acumulado'])
            ax2.set_title("Evolução Financeira")
            st.pyplot(fig2)

            st.write("📌 **Análise**: Se o saldo estiver positivo, parabéns! Continue mantendo o controle. Se estiver negativo, revise seus gastos.")
        else:
            st.warning("Não há dados para o período selecionado.")

# Relatórios
elif aba == "Relatórios":
    st.subheader("📄 Relatórios por Período")
    periodo_relatorio = st.date_input("Período para Relatório:", [datetime.date.today(), datetime.date.today()], key='relatorio')
    if len(periodo_relatorio) == 2:
        df_rel = st.session_state['dados']
        df_rel = df_rel[(df_rel['Data'] >= pd.to_datetime(periodo_relatorio[0])) & (df_rel['Data'] <= pd.to_datetime(periodo_relatorio[1]))]

        if not df_rel.empty:
            pdf_data = gerar_pdf(datetime.date.today(), df_rel)
            b64 = base64.b64encode(pdf_data.getvalue()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio_periodo.pdf">📄 Baixar Relatório do Período</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.warning("Nenhum dado encontrado para gerar o relatório.")

# Rodapé com logo
st.markdown("""
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center;'>
        <img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png' width='100'>
        <p style='color: white;'>Desenvolvido com carinho pela ÉdenMachine</p>
    </div>
""", unsafe_allow_html=True)
