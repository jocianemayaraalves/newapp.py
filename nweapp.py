import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import datetime

# ------------------- BANCO DE DADOS TEMPORÁRIO EM MEMÓRIA -------------------
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {'admin': '1234'}  # login padrão
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_atual' not in st.session_state:
    st.session_state.usuario_atual = ''
if 'dados' not in st.session_state:
    st.session_state.dados = {}

# --------------------- FUNÇÃO PARA ADICIONAR FUNDO VIA URL ---------------------
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://i.imgur.com/1F6oWnM.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url()

# ------------------------ TELA DE LOGIN ------------------------
def login():
    st.markdown("<h2 style='text-align:center;color:#fff;'>Café du Contrôle ☕</h2>", unsafe_allow_html=True)
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in st.session_state.usuarios and st.session_state.usuarios[usuario] == senha:
            st.session_state.logado = True
            st.session_state.usuario_atual = usuario
            if usuario not in st.session_state.dados:
                st.session_state.dados[usuario] = pd.DataFrame(columns=['Data', 'Tipo', 'Valor', 'Categoria'])
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos ❌")

# ------------------------ PÁGINA PRINCIPAL ------------------------
def app():
    # LOGO CENTRALIZADA
    st.markdown(
        """
        <div style='text-align: center; margin-top: -60px; margin-bottom: 10px;'>
            <img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png' width='300'/>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h1 style='text-align: center; color: #f8f8ff; text-shadow: 2px 2px 4px #000000; font-family: Arial;'>
            Bem-vinda ao seu cantinho financeiro 🍂
        </h1>
        """,
        unsafe_allow_html=True
    )

    dados_usuario = st.session_state.dados[st.session_state.usuario_atual]

    # ADICIONAR NOVA ENTRADA
    with st.expander("➕ Adicionar nova entrada financeira"):
        valor = st.number_input("Digite o valor:", min_value=0.0, step=0.01)
        categoria = st.text_input("Categoria:")
        data = st.date_input("Data", value=datetime.date.today())
        if st.button("Salvar entrada"):
            novo = pd.DataFrame([[data, 'Entrada', valor, categoria]], columns=dados_usuario.columns)
            st.session_state.dados[st.session_state.usuario_atual] = pd.concat([dados_usuario, novo], ignore_index=True)
            st.success("Entrada salva com sucesso! 💰")

    # ADICIONAR NOVO GASTO
    with st.expander("➖ Adicionar novo gasto"):
        valor_s = st.number_input("Digite o valor do gasto:", min_value=0.0, step=0.01, key="saida")
        categoria_s = st.text_input("Categoria do gasto:", key="cat_saida")
        data_s = st.date_input("Data do gasto", value=datetime.date.today(), key="data_saida")
        if st.button("Salvar gasto"):
            novo = pd.DataFrame([[data_s, 'Saída', valor_s, categoria_s]], columns=dados_usuario.columns)
            st.session_state.dados[st.session_state.usuario_atual] = pd.concat([dados_usuario, novo], ignore_index=True)
            st.error("Gasto registrado! 💸")

    # DASHBOARD
    st.subheader("📊 Visão geral")
    dados_usuario = st.session_state.dados[st.session_state.usuario_atual]
    if not dados_usuario.empty:
        entradas = dados_usuario[dados_usuario['Tipo'] == 'Entrada']['Valor'].sum()
        saidas = dados_usuario[dados_usuario['Tipo'] == 'Saída']['Valor'].sum()
        saldo = entradas - saidas

        col1, col2, col3 = st.columns(3)
        col1.metric("Entradas", f"R$ {entradas:.2f}")
        col2.metric("Saídas", f"R$ {saidas:.2f}")
        col3.metric("Saldo", f"R$ {saldo:.2f}", delta_color="normal")

        graf = px.bar(dados_usuario, x='Categoria', y='Valor', color='Tipo', title="Gastos x Entradas por categoria")
        st.plotly_chart(graf, use_container_width=True)
    else:
        st.info("Nenhum dado cadastrado ainda 🙃")

    # RODAPÉ
    st.markdown(
        """
        <hr style='border: 1px solid #ccc;'>
        <p style='text-align: center; color: #eeeeee;'>Feito com ❤️ por Mayara - Café du Contrôle ☕</p>
        """,
        unsafe_allow_html=True
    )

# ------------------------ EXECUÇÃO ------------------------
if not st.session_state.logado:
    login()
else:
    app()
