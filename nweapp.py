import streamlit as st
import pandas as pd
import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Configurações iniciais do app
st.set_page_config(page_title="Café du Contrôle", layout="wide")

# CSS customizado
st.markdown("""
    <style>
        body {
            background-image: url('https://i.imgur.com/2FcqN5M.jpg');
            background-size: cover;
        }
        .main {
            background: rgba(255, 255, 255, 0.1);
        }
        .titulo {
            font-size: 30px;
            color: white;
        }
        .secao {
            color: white;
            font-weight: bold;
            font-size: 22px;
            margin-top: 20px;
        }
        .saldo-barra {
            background-color: rgba(255, 255, 0, 0.4);
            padding: 10px;
            border-radius: 10px;
        }
        .saldo-text {
            font-size: 18px;
            color: black;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# Logos
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://i.imgur.com/x86YbtU.png", use_column_width=True)

# Logo da Éden centralizada na parte inferior
st.markdown("""
    <div style='position: fixed; bottom: 10px; width: 100%; text-align: center;'>
        <img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png' width='80'>
    </div>
""", unsafe_allow_html=True)

# Data retroativa
data_hoje = st.date_input("Data das movimentações:", value=datetime.date.today())

# Inicialização do DataFrame na sessão
if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Valor"])

# Menu lateral
menu = st.sidebar.radio("Menu", ["Lançamentos", "Dashboard", "Relatórios"])

if menu == "Lançamentos":
    st.markdown("<div class='secao'>Entradas</div>", unsafe_allow_html=True)
    entrada_valor = st.number_input("Valor da entrada:", min_value=0.0, format="%.2f")
    categoria_entrada = st.text_input("Categoria da entrada:")
    if st.button("Adicionar Entrada"):
        novo = {"Data": data_hoje, "Tipo": "Entrada", "Categoria": categoria_entrada, "Valor": entrada_valor}
        st.session_state.dados = pd.concat([st.session_state.dados, pd.DataFrame([novo])], ignore_index=True)

    st.markdown("<div class='secao'>Gastos</div>", unsafe_allow_html=True)
    gasto_valor = st.number_input("Valor do gasto:", min_value=0.0, format="%.2f")
    categoria_gasto = st.text_input("Categoria do gasto:")
    if st.button("Adicionar Gasto"):
        novo = {"Data": data_hoje, "Tipo": "Gasto", "Categoria": categoria_gasto, "Valor": gasto_valor}
        st.session_state.dados = pd.concat([st.session_state.dados, pd.DataFrame([novo])], ignore_index=True)

    st.markdown("<div class='secao'>Resumo do Dia</div>", unsafe_allow_html=True)
    df_dia = st.session_state.dados[st.session_state.dados['Data'] == data_hoje]
    total_entradas = df_dia[df_dia['Tipo'] == 'Entrada']['Valor'].sum()
    total_gastos = df_dia[df_dia['Tipo'] == 'Gasto']['Valor'].sum()
    saldo = total_entradas - total_gastos

    st.markdown(f"""
        <div class='saldo-barra'>
            <span class='saldo-text'><b>Saldo do dia {data_hoje.strftime('%d/%m/%Y')}:</b> R$ {saldo:.2f}</span>
        </div>
    """, unsafe_allow_html=True)

elif menu == "Dashboard":
    st.markdown("<div class='secao'>Dashboard Financeiro</div>", unsafe_allow_html=True)
    periodo = st.date_input("Selecione o período:", [datetime.date.today(), datetime.date.today()])
    df_periodo = st.session_state.dados.copy()
    df_periodo = df_periodo[(df_periodo['Data'] >= pd.to_datetime(periodo[0])) & (df_periodo['Data'] <= pd.to_datetime(periodo[1]))]

    if not df_periodo.empty:
        entradas = df_periodo[df_periodo['Tipo'] == 'Entrada']
        gastos = df_periodo[df_periodo['Tipo'] == 'Gasto']

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Gráfico de Pizza - Categorias de Gastos")
            fig1, ax1 = plt.subplots()
            gastos.groupby("Categoria")["Valor"].sum().plot.pie(autopct='%1.1f%%', ax=ax1)
            st.pyplot(fig1)

        with col2:
            st.subheader("Gráfico de Linha - Evolução do Saldo")
            df_periodo['Saldo_Acumulado'] = df_periodo.apply(lambda row: row['Valor'] if row['Tipo'] == 'Entrada' else -row['Valor'], axis=1).cumsum()
            fig2, ax2 = plt.subplots()
            ax2.plot(df_periodo['Data'], df_periodo['Saldo_Acumulado'])
            st.pyplot(fig2)

        st.write("Resumo do período:")
        total_ent = entradas['Valor'].sum()
        total_gas = gastos['Valor'].sum()
        saldo_final = total_ent - total_gas
        st.success(f"Entradas: R$ {total_ent:.2f} | Gastos: R$ {total_gas:.2f} | Saldo: R$ {saldo_final:.2f}")

elif menu == "Relatórios":
    st.markdown("<div class='secao'>Gerar Relatório em PDF</div>", unsafe_allow_html=True)
    periodo = st.date_input("Selecione o período do relatório:", [datetime.date.today(), datetime.date.today()])
    df_periodo = st.session_state.dados.copy()
    df_periodo = df_periodo[(df_periodo['Data'] >= pd.to_datetime(periodo[0])) & (df_periodo['Data'] <= pd.to_datetime(periodo[1]))]

    if st.button("Gerar Relatório em PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Relatório Financeiro: {periodo[0]} a {periodo[1]}", ln=True, align='C')

        for index, row in df_periodo.iterrows():
            pdf.cell(200, 10, txt=f"{row['Data']} - {row['Tipo']} - {row['Categoria']}: R$ {row['Valor']:.2f}", ln=True)

        buffer = BytesIO()
        pdf.output(buffer)
        b64 = base64.b64encode(buffer.getvalue()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio.pdf">Baixar PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
