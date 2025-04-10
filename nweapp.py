import streamlit as st
import pandas as pd
from fpdf import FPDF
from PIL import Image
from datetime import datetime

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

# -------------------- LOGO + DATA PERSONALIZADA --------------------
with st.container():
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
            <img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/logo-cafe.png" width="280">
        </div>
        """,
        unsafe_allow_html=True
    )
    data_selecionada = st.date_input("Escolha a data do lançamento", value=datetime.now(), format="DD/MM/YYYY")

# -------------------- SIDEBAR / MENU --------------------
menu = st.sidebar.radio("Navegar pelo App", ["Resumo Diário", "Histórico Mensal", "Relatórios", "Gerar PDF", "Ajuda ☕"])

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
    hoje = data_selecionada.strftime("%d/%m/%Y")

    st.header("📊 Resumo do Dia")
    st.markdown(f"**Data:** {hoje}")
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

    # -------------------- SALVAR RELATÓRIO DO DIA --------------------
    if 'relatorios_salvos' not in st.session_state:
        st.session_state['relatorios_salvos'] = []

    if st.button("💾 Salvar relatório do dia"):
        relatorio = {
            "data": hoje,
            "entradas": total_entradas,
            "saidas": total_saidas,
            "saldo": saldo
        }
        st.session_state['relatorios_salvos'].append(relatorio)
        st.success("Relatório salvo com sucesso!")

# -------------------- HISTÓRICO MENSAL --------------------
elif menu == "Histórico Mensal":
    st.header("📅 Histórico Mensal")
    st.info("Em breve: você poderá visualizar um resumo de seus lançamentos por mês, com gráficos lindos no tema outonal. 🍂")

# -------------------- RELATÓRIOS --------------------
elif menu == "Relatórios":
    st.header("📚 Relatórios Salvos")

    if 'relatorios_salvos' in st.session_state and st.session_state['relatorios_salvos']:
        df_relatorios = pd.DataFrame(st.session_state['relatorios_salvos'])
        st.dataframe(df_relatorios)
    else:
        st.info("Nenhum relatório salvo ainda. Salve pelo Resumo Diário.")

# -------------------- GERAR PDF --------------------
elif menu == "Gerar PDF":
    st.header("📄 Gerar Relatório em PDF")

    nome = st.text_input("Seu nome:")
    entradas_pdf = st.number_input("Entradas (R$)", key="pdf_entrada")
    saidas_pdf = st.number_input("Saídas (R$)", key="pdf_saida")
    saldo_pdf = entradas_pdf - saidas_pdf

    if st.button("📥 Baixar PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Relatório Financeiro - Café du Contrôle ☕", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Nome: {nome}", ln=True)
        pdf.cell(200, 10, txt=f"Entradas: R$ {entradas_pdf:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Saídas: R$ {saidas_pdf:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Saldo: R$ {saldo_pdf:,.2f}", ln=True)

        pdf_output = "relatorio.pdf"
        pdf.output(pdf_output)

        with open(pdf_output, "rb") as file:
            st.download_button("📄 Clique para baixar seu PDF", file, file_name="relatorio_financeiro.pdf")

# -------------------- AJUDA --------------------
elif menu == "Ajuda ☕":
    st.header("❓ Ajuda e Dicas")
    st.markdown("""
    - **Resumo Diário**: preencha suas entradas e gastos para ver seu saldo.
    - **Histórico Mensal**: em breve você poderá visualizar seu progresso mês a mês.
    - **Relatórios**: veja todos os lançamentos salvos por você.
    - **Gerar PDF**: baixe um relatório com seu nome e saldos.
    - Para dúvidas, fale com a equipe da ÉdenMachine. ✨
    """)

# -------------------- RODAPÉ --------------------
st.markdown("---")
st.markdown("""
    <div style="text-align: center;">
        <small>☕ Desenvolvido com carinho pela <strong>ÉdenMachine</strong></small><br>
        <img src="https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png" width="100">
    </div>
    """, unsafe_allow_html=True)
