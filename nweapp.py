import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Café du Contrôle", page_icon="☕", layout="centered")

# --- Estilo customizado ---
st.markdown("""
    <style>
    html, body {
        font-family: 'Georgia', serif;
        background-color: #fdf6f0;
        color: #3b2e2a;
    }

    .title {
        text-align: center;
        font-size: 38px;
        color: #8b5e3c;
        margin-bottom: 20px;
    }

    .stButton>button {
        background-color: #ffad60;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5em 1em;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #e29450;
        color: #fff;
    }

    .stTextInput>div>div>input,
    .stSelectbox>div>div>div {
        background-color: #fff7ee;
        border-radius: 10px;
        padding: 0.25em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🍁 Café du Contrôle 🍂</div>", unsafe_allow_html=True)

# --- Login simples ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.data = pd.DataFrame(columns=["Tipo", "Descrição", "Valor"])

if not st.session_state.logged_in:
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email and senha:
            st.session_state.logged_in = True
            st.success("☕ Bem-vinda de volta! Agora toma um café e organiza teu dinheiro, mulher!")
        else:
            st.warning("Preencha os dois campos.")
    st.stop()

# --- Área principal ---
st.subheader("📌 Lançamentos")
tipo = st.selectbox("Tipo", ["Entrada", "Saída"])
descricao = st.text_input("Descrição")
valor = st.number_input("Valor", min_value=0.0, format="%.2f")

if st.button("💾 Salvar"):
    nova_linha = pd.DataFrame([[tipo, descricao, valor]], columns=["Tipo", "Descrição", "Valor"])
    st.session_state.data = pd.concat([st.session_state.data, nova_linha], ignore_index=True)
    st.success(f"✅ {tipo} adicionada com sucesso!")

# --- Mostrar dados ---
if not st.session_state.data.empty:
    st.write("💰 **Resumo de Lançamentos**")
    st.dataframe(st.session_state.data, use_container_width=True)

    entradas = st.session_state.data[st.session_state.data["Tipo"] == "Entrada"]["Valor"].sum()
    saidas = st.session_state.data[st.session_state.data["Tipo"] == "Saída"]["Valor"].sum()
    saldo = entradas - saidas

    st.metric("💵 Total de Entradas", f"R$ {entradas:.2f}")
    st.metric("📤 Total de Saídas", f"R$ {saidas:.2f}")
    st.metric("🧮 Saldo Atual", f"R$ {saldo:.2f}")

    if saldo < 0:
        st.error("🚨 Tá plantando dinheiro, né linda?")
    elif saldo == 0:
        st.warning("😬 Zero a zero... cuidado com o café fiado ☕")
    else:
        st.success("💸 Vou começar a te chamar de Senhora... e com voz aveludada!")

    grafico = px.pie(
        st.session_state.data,
        names="Tipo",
        values="Valor",
        title="📊 Distribuição de Entradas e Saídas",
        color_discrete_map={"Entrada": "#ffad60", "Saída": "#8b5e3c"}
    )

    grafico.update_layout(
        paper_bgcolor='#fdf6f0',
        font=dict(color="#3b2e2a", family="Georgia"),
        title_font=dict(size=20),
        legend_title_text='Tipo de Movimento'
    )

    st.plotly_chart(grafico, use_container_width=True)

else:
    st.info("📋 Ainda não há dados. Comece adicionando uma entrada ou saída.")

if st.button("🚪 Sair"):
    st.session_state.logged_in = False
    st.experimental_rerun()
