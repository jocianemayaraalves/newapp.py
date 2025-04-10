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
 from fpdf import FPDF
 from datetime import datetime
 
 # Sidebar com abas interativas
 menu = st.sidebar.radio("Menu", ["Lançamentos", "Dashboard", "Relatórios"])
 # Configuração da página
 st.set_page_config(layout="wide", page_title="Café du Contrôle")
 
 # Logo do Café
 # Estilos personalizados
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
         body {
             background-color: #2c1e1e;
             color: white;
         }
         .saldo-container {
             background-color: rgba(255, 255, 0, 0.3);
             padding: 10px;
         .menu {
             background-color: #fff;
             padding: 20px;
             border-radius: 10px;
             margin-top: 20px;
             height: 100vh;
             color: #000;
         }
         .saldo-text {
             color: #222;
             font-weight: bold;
             font-size: 18px;
         .menu h2 {
             color: #000;
         }
         .titulo-claro {
             color: white;
         .section-title {
             font-size: 24px;
             font-weight: bold;
             color: white;
         }
         .saldo-container {
             background-color: rgba(255, 255, 0, 0.2);
             border-radius: 10px;
             padding: 10px;
             color: black;
         }
     </style>
 """, unsafe_allow_html=True)
 
 st.image("cafe_logo.png", use_column_width=False, output_format="auto", width=250)
 st.markdown(f"<div style='text-align: center;'>{date.today().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)
 # Função para salvar PDF
 def salvar_pdf(data_str, entradas, gastos, saldo):
     pdf = FPDF()
     pdf.add_page()
     pdf.set_font("Arial", size=12)
     pdf.cell(200, 10, txt=f"Relatório do Dia - {data_str}", ln=True)
     pdf.cell(200, 10, txt=f"Entradas: R$ {entradas:.2f}", ln=True)
     pdf.cell(200, 10, txt=f"Gastos: R$ {gastos:.2f}", ln=True)
     pdf.cell(200, 10, txt=f"Saldo: R$ {saldo:.2f}", ln=True)
     filename = f"relatorio_{data_str.replace('/', '-')}.pdf"
     pdf.output(filename)
     return filename
 
 # Sidebar/Menu Lateral
 with st.sidebar:
     st.markdown("<div class='menu'>", unsafe_allow_html=True)
     st.image("logo-cafe.png", use_container_width=False, width=250)
     st.title("Menu")
     aba = st.radio("Ir para:", ["Lançamentos", "Dashboard", "Relatórios"])
     st.markdown("</div>", unsafe_allow_html=True)
 
 # Logo da Eden
 st.markdown("""
     <div style='position: fixed; bottom: 10px; left: 50%; transform: translateX(-50%);'>
         <img src='https://raw.githubusercontent.com/jocianemayaraalves/newapp.py/main/eden-machine-logo-removebg-preview.png' width='100'>
     </div>
 """, unsafe_allow_html=True)
 
 # Lançamentos
 if menu == "Lançamentos":
     st.markdown("<h2 class='titulo-claro'>Lançamentos</h2>", unsafe_allow_html=True)
 # Data e Tabelas
 st.title("Café du Contrôle")
 data = st.date_input("Selecione a data:", value=datetime.today())
 data_str = data.strftime("%d/%m/%Y")
 
     data = st.date_input("Data", value=date.today())
     tipo = st.radio("Tipo", ["Entrada", "Gasto"])
     categoria = st.text_input("Categoria")
     valor = st.number_input("Valor", min_value=0.0, step=0.01)
 if "registros" not in st.session_state:
     st.session_state.registros = []
 
 if aba == "Lançamentos":
     st.subheader("Entradas")
     entrada = st.number_input("Valor da Entrada", min_value=0.0, step=0.01)
     st.subheader("Gastos")
     gasto = st.number_input("Valor do Gasto", min_value=0.0, step=0.01)
     categoria = st.text_input("Categoria do Gasto")
     if st.button("Adicionar"):
         adicionar_dado(data.strftime('%d/%m/%Y'), tipo, categoria, valor)
         st.success("Lançamento adicionado com sucesso!")
 
     if st.session_state['dados'].empty:
         st.info("Nenhum dado lançado ainda.")
         st.session_state.registros.append({"Data": data, "Entrada": entrada, "Gasto": gasto, "Categoria": categoria})
 
     # Resumo do dia
     df = pd.DataFrame(st.session_state.registros)
     df_dia = df[df["Data"] == data]
     entradas = df_dia["Entrada"].sum()
     gastos = df_dia["Gasto"].sum()
     saldo = entradas - gastos
 
     st.subheader("Resumo do Dia")
     st.dataframe(df_dia, use_container_width=True)
     
     st.markdown(f"""
         <div class='saldo-container'>
             <h4 style='color: white;'>Saldo do dia ({data_str}): R$ {saldo:.2f}</h4>
         </div>
     """, unsafe_allow_html=True)
 
     if st.button("Salvar relatório do dia"):
         salvar_pdf(data_str, entradas, gastos, saldo)
         st.success("Relatório salvo com sucesso!")
 
 elif aba == "Dashboard":
     st.subheader("Análise de Período")
     periodo = st.date_input("Selecione o período", [datetime.today(), datetime.today()])
     df = pd.DataFrame(st.session_state.registros)
 
     if not df.empty:
         df["Data"] = pd.to_datetime(df["Data"])
         df_periodo = df[(df["Data"] >= pd.to_datetime(periodo[0])) & (df["Data"] <= pd.to_datetime(periodo[1]))]
 
         if not df_periodo.empty:
             entradas_totais = df_periodo["Entrada"].sum()
             gastos_totais = df_periodo["Gasto"].sum()
             saldo_total = entradas_totais - gastos_totais
 
             col1, col2 = st.columns(2)
 
             with col1:
                 st.write("Distribuição de Gastos")
                 fig, ax = plt.subplots()
                 df_gastos = df_periodo.groupby("Categoria")["Gasto"].sum()
                 ax.pie(df_gastos, labels=df_gastos.index, autopct="%1.1f%%")
                 st.pyplot(fig)
 
             with col2:
                 st.write("Evolução do Saldo")
                 df_periodo_grouped = df_periodo.groupby("Data").agg({"Entrada": "sum", "Gasto": "sum"})
                 df_periodo_grouped["Saldo"] = df_periodo_grouped["Entrada"] - df_periodo_grouped["Gasto"]
                 st.line_chart(df_periodo_grouped["Saldo"])
 
             st.write("Resumo:")
             if saldo_total > 0:
                 st.success(f"Você está com saldo positivo! R$ {saldo_total:.2f}")
             elif saldo_total < 0:
                 st.error(f"Cuidado! Você está no vermelho. Saldo: R$ {saldo_total:.2f}")
             else:
                 st.warning("Saldo zerado.")
         else:
             st.warning("Nenhum dado encontrado para o período selecionado.")
     else:
         st.warning("Nenhum dado registrado ainda.")
 
 elif aba == "Relatórios":
     st.subheader("Gerar Relatório em PDF por Período")
     periodo_pdf = st.date_input("Período do relatório", [datetime.today(), datetime.today()], key="relatorio")
     df = pd.DataFrame(st.session_state.registros)
 
     if not df.empty:
         df["Data"] = pd.to_datetime(df["Data"])
         df_pdf = df[(df["Data"] >= pd.to_datetime(periodo_pdf[0])) & (df["Data"] <= pd.to_datetime(periodo_pdf[1]))]
         if not df_pdf.empty:
             entradas = df_pdf["Entrada"].sum()
             gastos = df_pdf["Gasto"].sum()
             saldo = entradas - gastos
             if st.button("Gerar PDF"):
                 nome_arquivo = salvar_pdf(f"{periodo_pdf[0].strftime('%d-%m-%Y')}_a_{periodo_pdf[1].strftime('%d-%m-%Y')}", entradas, gastos, saldo)
                 st.success(f"Relatório salvo como {nome_arquivo}")
         else:
             st.warning("Nenhum dado encontrado para o período.")
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
