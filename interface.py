import streamlit as st
import json
from class_annotation import Annotation
from functions import getAnnotation

st.set_page_config(page_title="Anotações de Estudo", layout="wide")

# Inicialização de estados
if "editando_id" not in st.session_state:
    st.session_state.editando_id = None

if "salvo_com_sucesso" not in st.session_state:
    st.session_state.salvo_com_sucesso = False

st.title("📚 Estud.IA")
st.write("Ferramenta de Anotações de estudos e Preparação de Mapeamento Mental para IA")

# Menu Lateral
st.sidebar.title("Menu")
opcao = st.sidebar.radio(
    "",
    options=["Criar anotação", "Listar anotações", "Exportar"]
)

# Cria anotações
if opcao == "Criar anotação":
    st.header("✍️ Nova Anotação")

    if st.session_state.salvo_com_sucesso:
            st.success("✅ Anotação salva com sucesso!")
            st.session_state.salvo_com_sucesso = False

    tema = st.text_input("Tema")
    subtema = st.text_input("Subtema")
    nivel = st.selectbox("Nível", ["Iniciante", "Intermediário", "Avançado"])

    st.subheader("Conteúdo")

    o_que_e = st.text_area("O que é")
    para_que = st.text_area("Para que serve")
    quando_usar = st.text_area("Quando usar")
    quando_nao_usar = st.text_area("Quando NÃO usar")

    conceitos_chave = st.text_area("Conceitos-chave (um por linha)")
    exemplo_simples = st.text_area("Exemplo simples")
    exemplo_pratico = st.text_area("Exemplo prático")

    erros = st.text_area("Erros comuns (um por linha)")
    perguntas = st.text_area("Perguntas (uma por linha)")
    conexoes = st.text_area("Conexões com outros temas (uma por linha)")

    if st.button("Salvar Anotação"):
        if not tema or not subtema:
            st.warning("Tema e Subtema são obrigatórios.")
        else:
            note = Annotation(tema, subtema, nivel)

            note.secoes = {
                "o_que_e": o_que_e,
                "para_que_serve": para_que,
                "quando_usar": quando_usar,
                "quando_nao_usar": quando_nao_usar,
                "conceitos_chave": conceitos_chave.splitlines(),
                "exemplo_simples": exemplo_simples,
                "exemplo_pratico": exemplo_pratico,
                "erros_comuns": erros.splitlines(),
                "perguntas": perguntas.splitlines(),
                "conexoes": conexoes.splitlines()
            }

            note.insertDB()
            note.updateSecoes()

            st.session_state.salvo_com_sucesso = True
            st.rerun()

# Listar anotações
elif opcao == "Listar anotações":
    st.header("📄 Lista de anotações")

    data = getAnnotation()

    if not data:
        st.info("Nenhuma anotação cadastrada.")
    else:
        for note in data:
            with st.expander(f"{note['tema']} - {note['subtema']} ({note['nivel']})"):

                secoes = note["secoes"]

                # Apresenta Seção
                if st.session_state.editando_id != note["id"]:
                    st.markdown("### 📘 Conteúdo")

                    def render_lista(titulo, lista):
                        if lista:
                            st.markdown(f"**{titulo}**")
                            for item in lista:
                                st.write(f"- {item}")

                    st.markdown("**O que é**")
                    st.write(secoes.get("o_que_e", ""))

                    st.markdown("**Para que serve**")
                    st.write(secoes.get("para_que_serve", ""))

                    st.markdown("**Quando usar**")
                    st.write(secoes.get("quando_usar", ""))

                    st.markdown("**Quando NÃO usar**")
                    st.write(secoes.get("quando_nao_usar", ""))

                    render_lista("Conceitos-chave", secoes.get("conceitos_chave", []))

                    st.markdown("**Exemplo simples**")
                    st.write(secoes.get("exemplo_simples", ""))

                    st.markdown("**Exemplo prático**")
                    st.write(secoes.get("exemplo_pratico", ""))

                    render_lista("Erros comuns", secoes.get("erros_comuns", []))
                    render_lista("Perguntas", secoes.get("perguntas", []))
                    render_lista("Conexões", secoes.get("conexoes", []))

                    if st.button("✏️ Editar", key=f"edit_{note['id']}"):
                        st.session_state.editando_id = note["id"]
                        st.rerun()

                # Abre edição
                else:
                    o_que_e = st.text_area(
                        "O que é", secoes.get("o_que_e", ""), key=f"oque_{note['id']}"
                    )
                    para_que = st.text_area(
                        "Para que serve", secoes.get("para_que_serve", ""), key=f"para_{note['id']}"
                    )
                    quando_usar = st.text_area(
                        "Quando usar", secoes.get("quando_usar", ""), key=f"quando_{note['id']}"
                    )
                    quando_nao_usar = st.text_area(
                        "Quando NÃO usar", secoes.get("quando_nao_usar", ""), key=f"naousar_{note['id']}"
                    )

                    conceitos_chave = st.text_area(
                        "Conceitos-chave (um por linha)",
                        "\n".join(secoes.get("conceitos_chave", [])),
                        key=f"conceitos_{note['id']}"
                    )

                    exemplo_simples = st.text_area(
                        "Exemplo simples", secoes.get("exemplo_simples", ""), key=f"exsimples_{note['id']}"
                    )
                    exemplo_pratico = st.text_area(
                        "Exemplo prático", secoes.get("exemplo_pratico", ""), key=f"expratico_{note['id']}"
                    )

                    erros = st.text_area(
                        "Erros comuns (um por linha)",
                        "\n".join(secoes.get("erros_comuns", [])),
                        key=f"erros_{note['id']}"
                    )

                    perguntas = st.text_area(
                        "Perguntas (uma por linha)",
                        "\n".join(secoes.get("perguntas", [])),
                        key=f"perguntas_{note['id']}"
                    )

                    conexoes = st.text_area(
                        "Conexões com outros temas (uma por linha)",
                        "\n".join(secoes.get("conexoes", [])),
                        key=f"conexoes_{note['id']}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("💾 Salvar", key=f"save_{note['id']}"):
                            note_obj = Annotation(
                                note["tema"], note["subtema"], note["nivel"]
                            )
                            note_obj.id = note["id"]

                            note_obj.secoes = {
                                "o_que_e": o_que_e,
                                "para_que_serve": para_que,
                                "quando_usar": quando_usar,
                                "quando_nao_usar": quando_nao_usar,
                                "conceitos_chave": conceitos_chave.splitlines(),
                                "exemplo_simples": exemplo_simples,
                                "exemplo_pratico": exemplo_pratico,
                                "erros_comuns": erros.splitlines(),
                                "perguntas": perguntas.splitlines(),
                                "conexoes": conexoes.splitlines()
                            }

                            note_obj.updateSecoes()
                            st.session_state.editando_id = None
                            st.success("Alterações salvas!")
                            st.rerun()

                    with col2:
                        if st.button("❌ Cancelar", key=f"cancel_{note['id']}"):
                            st.session_state.editando_id = None
                            st.rerun()

# Exportar
elif opcao == "Exportar":
    st.header("📤 Exportar anotações")

    data = getAnnotation()

    # JSON
    json_data = json.dumps(data, indent=2, ensure_ascii=False)

    st.download_button(
        "📥 Baixar JSON",
        json_data,
        "annotations.json",
        "application/json"
    )

    # PDF
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import A4
    import io

    if st.button("📄 Gerar PDF"):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        for note in data:
            elements.append(Paragraph(f"<b>{note['tema']} - {note['subtema']}</b>", styles["Title"]))
            elements.append(Paragraph(f"Nível: {note['nivel']}", styles["Normal"]))
            elements.append(Spacer(1, 12))

            for secao, valor in note["secoes"].items():
                elements.append(Paragraph(f"<b>{secao}</b>", styles["Heading3"]))

                if isinstance(valor, list):
                    for item in valor:
                        elements.append(Paragraph(f"- {item}", styles["Normal"]))
                else:
                    elements.append(Paragraph(str(valor), styles["Normal"]))

                elements.append(Spacer(1, 10))

            elements.append(Spacer(1, 24))

        doc.build(elements)

        st.download_button(
            "⬇️ Baixar PDF",
            buffer.getvalue(),
            "annotations.pdf",
            "application/pdf"
        )