# -------------------- GERAR RELATÓRIO EM PDF --------------------
if st.button("📄 Gerar Relatório em PDF"):
    from fpdf import FPDF
    import base64

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "Café du Contrôle - Relatório do Dia", ln=True, align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 10, f"Data: {hoje}", ln=True)
    pdf.cell(0, 10, f"Total de Entradas: R$ {total_entradas:,.2f}", ln=True)
    pdf.cell(0, 10, f"Total de Gastos: R$ {total_saidas:,.2f}", ln=True)
    pdf.cell(0, 10, f"Saldo do Dia: R$ {saldo:,.2f}", ln=True)

    if saldo > 0:
        pdf.multi_cell(0, 10, "Você está positiva hoje!\nVou começar a te chamar de Senhora... e com voz aveludada!")
    elif saldo < 0:
        pdf.multi_cell(0, 10, "Você gastou mais do que ganhou hoje!\nTá plantando dinheiro, né linda?")
    else:
        pdf.multi_cell(0, 10, "Zerada. Saldo: R$ 0,00\nCafé preto e foco!")

    # Salvar PDF na memória
    pdf_output = pdf.output(dest="S").encode("latin-1")
    b64_pdf = base64.b64encode(pdf_output).decode('utf-8')

    href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="relatorio-cafe.pdf">📥 Clique aqui para baixar seu PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
