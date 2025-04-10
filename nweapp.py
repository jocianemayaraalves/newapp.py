import streamlit as st
import datetime
import pandas as pd
import os
from PIL import Image

# Funções auxiliares para salvar e carregar dados por usuário
def get_user_file(user):
    return f"dados_{user}.csv"

def carregar_dados(usuario):
    arquivo = get_user_file(usuario)
    if os.path.exists(arquivo):
        return pd.read_csv(arquivo)
    else:
        return pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Descrição", "Valor"])

def salvar_dados(usuario, dados):
    arquivo = get_user_file(usuario)
    dados.to_csv(arquivo, index=False)

# Autenticação simples (mock)
usuarios = {"mayara": "1234", "convidado": "teste"}

if "usuario_autenticado" not in st.session_state:
    st.session_state.usuario_autenticado = None

if st.session_state.usuario_autenticado is None:
    st.title("Café du Contrôle ☕")
    st.subheader("Faça login para acessar seu controle financeiro")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in usuarios and usuarios[usuario] == senha:
            st.session_state.usuario_autenticado = usuario
            st.success(f"Bem-vinda, {usuario}!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
else:
    usuario = st.session_state.usuario_autenticado
    st.sidebar.image("logo-cafe.png", use_column_width=True)
    st.sidebar.markdown("""
        <style>
            .sidebar .sidebar-content {
                background-color: #f5f5dc;
                color: #333333;
            }
            .css-1v0mbdj p, .css-1v0mbdj label {
                color: #333333 !important;
            }
        </style>
    """, unsafe_allow_html=True)
    st.sidebar.title("Menu")
    aba = st.sidebar.radio("Ir para:", ["Lançamentos", "Dashboard", "Relatórios"])

    st.markdown("""
        <style>
            .titulo {
                font-size: 28px;
                color: white;
                margin-top: 20px;
            }
            .subtitulo {
                font-size: 22px;
                color: white;
                margin-top: 10px;
            }
            .saldo-container {
                background-color: rgba(255, 255, 0, 0.25);
                border-radius: 10px;
                padding: 15px;
                margin-top: 15px;
            }
            .saldo-text {
                color: #222;
                font-weight: bold;
                font-size: 20px;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    dados = carregar_dados(usuario)

    if aba == "Lançamentos":
        st.markdown("<div class='titulo'>Lançamentos do Dia</div>", unsafe_allow_html=True)

        with st.form("form_lancamento"):
            col1, col2 = st.columns(2)
            with col1:
                data = st.date_input("Data", value=datetime.date.today())
                tipo = st.selectbox("Tipo", ["Entrada", "Gasto"])
                categoria = st.text_input("Categoria")
            with col2:
                descricao = st.text_input("Descrição")
                valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)

            enviado = st.form_submit_button("Adicionar")

            if enviado:
                novo = pd.DataFrame([[data, tipo, categoria, descricao, valor]], columns=dados.columns)
                dados = pd.concat([dados, novo], ignore_index=True)
                salvar_dados(usuario, dados)
                st.success("Lançamento adicionado com sucesso!")

    elif aba == "Dashboard":
        st.markdown("<div class='titulo'>Resumo do Dia</div>", unsafe_allow_html=True)
        hoje = datetime.date.today().strftime('%Y-%m-%d')
        dados_dia = dados[dados["Data"] == hoje]

        total_entradas = dados_dia[dados_dia["Tipo"] == "Entrada"]["Valor"].sum()
        total_gastos = dados_dia[dados_dia["Tipo"] == "Gasto"]["Valor"].sum()
        saldo = total_entradas - total_gastos

        st.markdown(f"<div class='subtitulo'>Entradas: R$ {total_entradas:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitulo'>Gastos: R$ {total_gastos:.2f}</div>", unsafe_allow_html=True)

        st.markdown(f"""
            <div class='saldo-container'>
                <div class='saldo-text'>Saldo do Dia: R$ {saldo:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

        if saldo < 0:
            st.error("Tá plantando dinheiro, né linda?")
        elif saldo > 0:
            st.success("Vou começar a te chamar de Senhora... e com voz aveludada!")
        else:
            st.info("Equilibrou o jogo hoje!")

    elif aba == "Relatórios":
        st.markdown("<div class='titulo'>Relatórios</div>", unsafe_allow_html=True)
        st.dataframe(dados)

    st.markdown("""
        <div style='text-align: center; margin-top: 50px;'>
            <img src='logo-cafe.png' width='120'>
        </div>
    """, unsafe_allow_html=True)
