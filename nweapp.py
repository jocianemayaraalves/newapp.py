# -------------------- RESUMO DIÁRIO --------------------
if menu == "Resumo Diário":
    st.header("💰 Entradas")
    tipo_entrada = st.selectbox("Tipo de Entrada", ["Dinheiro Físico", "Pix", "Cartão", "Outros"])
    valor_entrada = st.number_input("Valor de Entrada", min_value=0.0, step=100.0)
    total_entradas = valor_entrada  # Para simplificação, podemos somar diretamente as entradas.

    st.header("💸 Gastos")
    descricao_gasto = st.text_input("Descrição do Gasto", "")
    valor_gasto = st.number_input("Valor do Gasto", min_value=0.0, step=50.0)
    total_saidas = valor_gasto

    saldo = total_entradas - total_saidas

    st.header("📊 Resumo do Dia")
    st.markdown(f"**Data:** {data_lancamento.strftime('%d/%m/%Y')}")
    st.markdown(f"**Total de Entradas:** R$ {total_entradas:,.2f}")
    st.markdown(f"**Total de Gastos:** R$ {total_saidas:,.2f}")

    if saldo > 0:
        st.success(f"Você está positiva hoje! 💚")
        st.caption("Vou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        st.error("Você gastou mais do que ganhou hoje! 💸")
        st.caption("Tá plantando dinheiro, né linda?")
    else:
        st.warning("Zerada. Saldo: R$ 0,00")
        st.caption("Café preto e foco!")

    st.markdown(f'<div class="saldo-box">Saldo do Dia: R$ {saldo:,.2f}</div>', unsafe_allow_html=True)

    if st.button("💾 Salvar relatório do dia"):
        st.success("Relatório salvo com sucesso!")
        st.session_state.relatorios.append({
            "data": data_lancamento,
            "entradas": total_entradas,
            "saidas": total_saidas,
            "descricao_gasto": descricao_gasto,
            "tipo_entrada": tipo_entrada,
            "saldo": saldo
        })

# -------------------- GERAR PDF --------------------
elif menu == "Gerar PDF":
    st.header("📄 Gerar Relatório em PDF")
    df = pd.DataFrame(st.session_state.relatorios)

    if not df.empty:
        data_inicial = st.date_input("Data inicial", value=df['data'].min().date())
        data_final = st.date_input("Data final", value=df['data'].max().date())

        filtro = (df["data"] >= pd.to_datetime(data_inicial)) & (df["data"] <= pd.to_datetime(data_final))
        df_filtrado = df[filtro]

        st.subheader("Gráficos")
        if not df_filtrado.empty:
            st.pyplot(df_filtrado.plot(x="data", y=["entradas", "saidas", "saldo"], kind="line").figure)
            st.pyplot(df_filtrado[["entradas", "saidas"]].sum().plot.pie(autopct='%1.1f%%').figure)

        st.subheader("Informações Inteligentes")
        st.markdown(f"- **Média de saldo diário:** R$ {df_filtrado['saldo'].mean():,.2f}")
        st.markdown(f"- **Dia mais lucrativo:** {df_filtrado.loc[df_filtrado['saldo'].idxmax()]['data'].strftime('%d/%m/%Y')}")
        st.markdown(f"- **Maior gasto:** R$ {df_filtrado['saidas'].max():,.2f}")

        # PDF Generation Logic
        if st.button("Gerar PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)

            # Cabeçalho com a logo do Café
            pdf.image('logo-cafe.png', 10, 8, 33)  # Ajuste a imagem conforme necessário
            pdf.ln(20)
            pdf.cell(200, 10, "Relatório Café du Contrôle", ln=True, align='C')
            pdf.ln(10)

            # Conteúdo do Relatório
            pdf.set_font('Arial', '', 12)
            for index, row in df_filtrado.iterrows():
                pdf.cell(200, 10, f"{row['data'].strftime('%d/%m/%Y')} - Entrada: R$ {row['entradas']} | Gasto: R$ {row['saidas']} | Saldo: R$ {row['saldo']}", ln=True)

            # Logo da ÉdenMachine no rodapé
            pdf.ln(20)
            pdf.image('logo-eden.png', 10, 250, 33)  # Ajuste a imagem conforme necessário
            pdf.output("relatorio.pdf")

            st.success("PDF gerado com sucesso!")

    else:
        st.warning("Nenhum dado disponível para gerar PDF.")
