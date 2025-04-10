import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Café du Contrôle", page_icon="☕", layout="centered")

# --- Estilo ---
st.markdown("""
    <style>
    body {
        background-color: #fdf6f0;
    }
    .title {
        color: #5a3d2b;
        text-align: center;
        font-size: 36px;
        font-family: 'Georgia', serif;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>☕ Café du Contrôle</div>", unsafe_allow_html=True)

# --- Simulação de login simples ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.data = pd.DataFrame(columns=["Tipo", "Descrição", "Valor"])

if not st.session_state.logged_in:
    st.subheader("Login")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email and senha:
            st.session_state.logged_in = True
            st.success("Bem-vinda de volta! Agora toma um café e organiza teu dinheiro, mulher! ☕")
        else:
            st.warning("Preencha os dois campos.")
    st.stop()

# --- Área principal ---
st.subheader("Lançamentos")
tipo = st.selectbox("Tipo", ["Entrada", "Saída"])
descricao = st.text_input("Descrição")
valor = st.number_input("Valor", min_value=0.0, format="%.2f")

if st.button("Salvar"):
    nova_linha = pd.DataFrame([[tipo, descricao, valor]], columns=["Tipo", "Descrição", "Valor"])
    st.session_state.data = pd.concat([st.session_state.data, nova_linha], ignore_index=True)
    st.success(f"{tipo} adicionada com sucesso!")

# --- Mostrar dados ---
if not st.session_state.data.empty:
    st.write("💰 **Resumo de Lançamentos**")
    st.dataframe(st.session_state.data, use_container_width=True)

    entradas = st.session_state.data[st.session_state.data["Tipo"] == "Entrada"]["Valor"].sum()
    saidas = st.session_state.data[st.session_state.data["Tipo"] == "Saída"]["Valor"].sum()
    saldo = entradas - saidas

    st.metric("Total de Entradas", f"R$ {entradas:.2f}")
    st.metric("Total de Saídas", f"R$ {saidas:.2f}")
    st.metric("Saldo Atual", f"R$ {saldo:.2f}")

    # Mensagens divertidas
    if saldo < 0:
        st.error("Tá plantando dinheiro, né linda?")
    elif saldo == 0:
        st.warning("Zero a zero... cuidado com o café fiado ☕")
    else:
        st.success("Vou começar a te chamar de Senhora... e com voz aveludada!")

    # Gráfico
    grafico = px.pie(
        st.session_state.data,
        names="Tipo",
        values="Valor",
        title="Distribuição de Entradas e Saídas",
        color_discrete_map={"Entrada": "#ffad60", "Saída": "#8b5e3c"}
    )
    st.plotly_chart(grafico, use_container_width=True)

else:
    st.info("Ainda não há dados. Comece adicionando uma entrada ou saída.")

# Botão de logout
if st.button("Sair"):
    st.session_state.logged_in = False
    st.experimental_rerun()
