import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Café du Contrôle", page_icon="☕", layout="centered")

# --- Estilo customizado ---
st.markdown("""
    <style>
    html, body, [data-testid="stApp"] {
        background-color: #f4ebe2;
        color: #3b2e2a;
        font-family: 'Georgia', serif;
    }

    .title {
        text-align: center;
        font-size: 38px;
        color: #7b4b2a;
        margin-bottom: 20px;
    }

    .stButton>button {
        background-color: #dc9c68;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5em 1em;
        font-weight: bold;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }

    .stButton>button:hover {
        background-color: #c78555;
        color: #fff;
    }

    .stTextInput>div>div>input,
    .stSelectbox>div>div>div,
    .stNumberInput>div>div>input,
    .stDateInput>div>input {
        background-color: #fff7ee;
        border: 1px solid #e0c3a0;
        border-radius: 10px;
        padding: 0.25em;
    }

    .stDataFrame {
        background-color: #fffaf3;
        border-radius: 15px;
        padding: 1em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🍁 Café du Contrôle 🍂</div>", unsafe_allow_html=True)

# --- Login simples ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.data = pd.DataFrame(columns=["Data", "Tipo", "Descrição", "Valor"])

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

# --- Área de lançamento ---
st.subheader("📌 Novo Lançamento")
data = st.date_input("Data", datetime.today())
tipo = st.selectbox("Tipo", ["Entrada", "Saída"])
descricao = st.text_input("Descrição")
valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")

if st.button("💾 Adicionar"):
    nova_linha = pd.DataFrame([[data, tipo, descricao, valor]], columns=["Data", "Tipo", "Descrição", "Valor"])
    st.session_state.data = pd.concat([st.session_state.data, nova_linha], ignore_index=True)
    st.success(f"✅ {tipo} registrada com sucesso!")

# --- Tabela e análises ---
if not st.session_state.data.empty:
    st.subheader("📋 Lançamentos")
    df = st.session_state.data.copy()
    df["Data"] = pd.to_datetime(df["Data"])
    df = df.sort_values("Data")

    st.dataframe(df, use_container_width=True)

    entradas = df[df["Tipo"] == "Entrada"]["Valor"].sum()
    saidas = df[df["Tipo"] == "Saída"]["Valor"].sum()
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

    # --- Gráfico de pizza ---
    grafico = px.pie(
        df,
        names="Tipo",
        values="Valor",
        title="📊 Distribuição de Entradas e Saídas",
        color_discrete_map={"Entrada": "#ffad60", "Saída": "#8b5e3c"}
    )

    grafico.update_layout(
        paper_bgcolor='#f4ebe2',
        font=dict(color="#3b2e2a", family="Georgia"),
        title_font=dict(size=20),
        legend_title_text='Tipo de Movimento'
    )

    st.plotly_chart(grafico, use_container_width=True)

    # --- Gráfico de linha por data ---
    df_linha = df.groupby(["Data", "Tipo"])["Valor"].sum().reset_index()
    graf_linha = px.line(
        df_linha,
        x="Data",
        y="Valor",
        color="Tipo",
        title="📈 Evolução Financeira ao Longo do Tempo",
        color_discrete_map={"Entrada": "#ffad60", "Saída": "#8b5e3c"},
        markers=True
    )
    graf_linha.update_layout(paper_bgcolor="#f4ebe2", plot_bgcolor="#f4ebe2")
    st.plotly_chart(graf_linha, use_container_width=True)

else:
    st.info("📋 Ainda não há dados. Comece adicionando uma entrada ou saída.")

if st.button("🚪 Sair"):
    st.session_state.logged_in = False
    st.experimental_rerun()
