import streamlit as st
import pandas as pd
from fpdf import FPDF
from PIL import Image
from datetime import datetime
import matplotlib.pyplot as plt
import io

# -------------------- CONFIG GERAL --------------------
st.set_page_config(
    page_title="Café du Contrôle ☕",
    page_icon=":coffee:",
    layout="wide"
)

# -------------------- FUNÇÃO: FUNDO --------------------
def set_background_from_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        .main > div {{
            background-color: rgba(0, 0, 0, 0.5);
            padding: 2rem;
            border-radius: 12px;
        }}
        h1, h2, h3 {{
            color: #fefefe !important;
            text-shadow: 1px 1px 4px #000000cc;
        }}
        .stMarkdown, .stTextInput > label, .stNumberInput > label {{
            color: #fdfdfd !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_from_url("https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/bg.png")

# -------------------- DADOS --------------------
if 'relatorios' not in st.session_state:
    st.session_state['relatorios'] = []

# -------------------- LOGOS --------------------
with st.container():
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
            <img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" width="280">
        </div>
        """,
        unsafe_allow_html=True
    )
    data_custom = st.date_input("Selecione a data do lançamento:", value=datetime.today())

# -------------------- SIDEBAR / MENU --------------------
menu = st.sidebar.radio("Navegar pelo App", ["Resumo Diário", "Histórico Mensal", "Gerar PDF", "Ajuda ☕"])

# -------------------- RESUMO DIÁRIO --------------------
if menu == "Resumo Diário":
    st.header("💰 Entradas")
    salario = st.number_input("Salário", min_value=0.0, step=100.0)
    renda_extra = st.number_input("Renda Extra", min_value=0.0, step=50.0)
    total_entradas = salario + renda_extra

    st.header("💸 Gastos")
    fixos = st.number_input("Gastos Fixos", min_value=0.0, step=100.0)
    extras = st.number_input("Gastos Variáveis", min_value=0.0, step=50.0)
    total_saidas = fixos + extras

    saldo = total_entradas - total_saidas

    st.header("📊 Resumo do Dia")
    st.markdown(f"**Data:** {data_custom.strftime('%d/%m/%Y')}")
    st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
    st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")

    if saldo > 0:
        st.success(f"Você está positiva hoje! 💚 Saldo: R$ {saldo:,.2f}")
        st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        st.error(f"Você gastou mais do que ganhou hoje! 💸 Saldo: R$ {saldo:,.2f}")
        st.caption("Tá plantando dinheiro, né linda?")
    else:
        st.warning("Zerada. Saldo: R$ 0,00")
        st.caption("Café preto e foco!")

    if st.button("💾 Salvar relatório do dia"):
        st.session_state.relatorios.append({
            "data": data_custom,
            "entradas": total_entradas,
            "saidas": total_saidas,
            "saldo": saldo
        })
        st.success("Relatório salvo com sucesso!")

# -------------------- HISTÓRICO MENSAL --------------------
elif menu == "Histórico Mensal":
    st.header("📅 Histórico Mensal")
    st.info("Em breve: você poderá visualizar um resumo de seus lançamentos por mês, com gráficos lindos no tema outonal. 🍂")

# -------------------- GERAR PDF --------------------
elif menu == "Gerar PDF":
    st.header("📄 Gerar Relatório em PDF")

    data_inicio = st.date_input("Data inicial:", value=datetime.today())
    data_fim = st.date_input("Data final:", value=datetime.today())

    dados_filtrados = [r for r in st.session_state.relatorios if data_inicio <= r['data'] <= data_fim]

    if dados_filtrados:
        df = pd.DataFrame(dados_filtrados)
        st.subheader("📈 Gráficos")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Entradas vs Saídas (Pizza)**")
            total_entradas = df['entradas'].sum()
            total_saidas = df['saidas'].sum()
            fig1, ax1 = plt.subplots()
            ax1.pie([total_entradas, total_saidas], labels=['Entradas', 'Saídas'], autopct='%1.1f%%')
            st.pyplot(fig1)

        with col2:
            st.markdown("**Saldo ao longo do tempo (Linha)**")
            fig2, ax2 = plt.subplots()
            ax2.plot(df['data'], df['saldo'], marker='o', linestyle='-')
            ax2.set_title("Evolução do Saldo")
            ax2.set_ylabel("Saldo")
            plt.xticks(rotation=45)
            st.pyplot(fig2)

        st.subheader("📌 Informações Inteligentes")
        st.markdown(f"**Saldo médio:** R$ {df['saldo'].mean():,.2f}")
        melhor_dia = df.loc[df['saldo'].idxmax()]
        st.markdown(f"**Dia mais lucrativo:** {melhor_dia['data'].strftime('%d/%m/%Y')} (R$ {melhor_dia['saldo']:,.2f})")
        pior_dia = df.loc[df['saldo'].idxmin()]
        st.markdown(f"**Dia mais crítico:** {pior_dia['data'].strftime('%d/%m/%Y')} (R$ {pior_dia['saldo']:,.2f})")

    else:
        st.warning("Nenhum dado encontrado para o período selecionado.")

# -------------------- AJUDA --------------------
elif menu == "Ajuda ☕":
    st.header("❓ Ajuda e Dicas")
    st.markdown("""
    - **Resumo Diário**: preencha suas entradas e gastos para ver seu saldo.
    - **Histórico Mensal**: em breve você poderá visualizar seu progresso mês a mês.
    - **Gerar PDF**: baixe um relatório com seu nome e saldos.
    - Para dúvidas, fale com a equipe da ÉdenMachine. ✨
    """)

# -------------------- RODAPÉ --------------------
st.markdown("""
<hr>
<div style="text-align: center;">
    <small style="font-size: 10px;">☕ Desenvolvido com carinho pela <strong>ÉdenMachine</strong></small><br>
    <img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/refs/heads/main/eden-machine-logo-removebg-preview.png" width="70">
</div>
""", unsafe_allow_html=True)
