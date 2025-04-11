# -------------------- GERAR PDF --------------------
elif menu == "Gerar PDF":
    st.header("📄 Gerar Relatório em PDF")

    # Lendo dados reais das tabelas entradas e saidas
    df_entradas = pd.read_sql_query("SELECT data, valor FROM entradas", conn)
    df_saidas = pd.read_sql_query("SELECT data, valor, descricao FROM saidas", conn)

    if not df_entradas.empty and not df_saidas.empty:
        df_entradas['data'] = pd.to_datetime(df_entradas['data'])
        df_saidas['data'] = pd.to_datetime(df_saidas['data'])

        # Agrupando por data
        entradas_agrupadas = df_entradas.groupby('data').sum().reset_index()
        saidas_agrupadas = df_saidas.groupby('data').sum().reset_index()

        # Juntando as duas em um único dataframe
        df_merged = pd.merge(entradas_agrupadas, saidas_agrupadas, on='data', how='outer', suffixes=('_entrada', '_saida')).fillna(0)
        df_merged['saldo'] = df_merged['valor_entrada'] - df_merged['valor_saida']
        df_merged = df_merged.sort_values(by="data")

        # Filtros de data
        data_inicial = st.date_input("Data inicial", value=df_merged['data'].min().date())
        data_final = st.date_input("Data final", value=df_merged['data'].max().date())

        df_filtrado = df_merged[(df_merged['data'] >= pd.to_datetime(data_inicial)) & (df_merged['data'] <= pd.to_datetime(data_final))]

        if not df_filtrado.empty:
            st.subheader("📈 Gráficos do Período")

            fig, ax = plt.subplots()
            ax.plot(df_filtrado['data'], df_filtrado['valor_entrada'], label="Entradas", marker='o')
            ax.plot(df_filtrado['data'], df_filtrado['valor_saida'], label="Saídas", marker='o')
            ax.plot(df_filtrado['data'], df_filtrado['saldo'], label="Saldo", marker='o')
            ax.set_title("Fluxo de Caixa Diário")
            ax.legend()
            st.pyplot(fig)

            st.subheader("💡 Análises Inteligentes")
            saldo_medio = df_filtrado['saldo'].mean()
            dia_lucrativo = df_filtrado.loc[df_filtrado['saldo'].idxmax()]['data'].strftime('%d/%m/%Y')
            maior_gasto = df_filtrado['valor_saida'].max()

            st.markdown(f"- **Média de saldo diário:** R$ {saldo_medio:,.2f}")
            st.markdown(f"- **Dia mais lucrativo:** {dia_lucrativo}")
            st.markdown(f"- **Maior gasto do período:** R$ {maior_gasto:,.2f}")

            if st.button("📄 Gerar PDF"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)

                # Logo
                pdf.image("logo-cafe.png", x=10, y=8, w=40)
                pdf.cell(200, 10, txt="Relatório Financeiro - Café du Contrôle", ln=True, align="C")
                pdf.ln(10)

                # Informações do desenvolvedor
                pdf.set_font("Arial", "", 12)
                pdf.cell(200, 10, txt=f"Desenvolvido por ÉdenMachine - {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="L")
                pdf.ln(10)

                # Dados
                for index, row in df_filtrado.iterrows():
                    data_formatada = row['data'].strftime('%d/%m/%Y')
                    pdf.cell(0, 10, f"{data_formatada} - Entrada: R$ {row['valor_entrada']:,.2f} | Saída: R$ {row['valor_saida']:,.2f} | Saldo: R$ {row['saldo']:,.2f}", ln=True)

                pdf.ln(5)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"Média de saldo diário: R$ {saldo_medio:,.2f}", ln=True)
                pdf.cell(0, 10, f"Dia mais lucrativo: {dia_lucrativo}", ln=True)
                pdf.cell(0, 10, f"Maior gasto do período: R$ {maior_gasto:,.2f}", ln=True)

                # Rodapé
                pdf.image("eden-machine-logo-removebg-preview.png", x=85, y=pdf.get_y()+10, w=40)

                nome_arquivo = f"relatorio_cafe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                pdf.output(nome_arquivo)
                st.success(f"Relatório gerado com sucesso: {nome_arquivo}")
                with open(nome_arquivo, "rb") as f:
                    st.download_button("⬇️ Baixar PDF", f, file_name=nome_arquivo, mime="application/pdf")

        else:
            st.warning("Nenhum dado disponível no intervalo selecionado.")
    else:
        st.warning("Nenhum dado encontrado para gerar o PDF.")
