from fpdf import FPDF

def export_annotations_pdf(annotations, file_path="annotations.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    for note in annotations:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Tema: {note.tema}", ln=True)

        pdf.set_font("Arial", size=11)
        pdf.cell(0, 8, f"Subtema: {note.subtema}", ln=True)
        pdf.cell(0, 8, f"Nível: {note.nivel}", ln=True)

        pdf.ln(2)
        pdf.multi_cell(0, 8, "Seções:")

        for secao in note.secoes:
            pdf.multi_cell(0, 8, f"- {secao}")

        pdf.ln(5)

    pdf.output(file_path)
    return file_path