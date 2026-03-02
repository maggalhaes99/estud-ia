import streamlit as st
import json

from app.services.annotation_service import AnnotationService
from app.models.annotation import Annotation

from app.services.template_annotation_service import TemplateAnnotationService
from app.models.template import TemplateAnnotation


def run_app():
    service = AnnotationService()
    template_service = TemplateAnnotationService()

    st.set_page_config(page_title="Anotações de Estudo", layout="wide")

    # =====================
    # Estados da sessão
    # =====================
    if "editando_id" not in st.session_state:
        st.session_state.editando_id = None

    if "salvo_com_sucesso" not in st.session_state:
        st.session_state.salvo_com_sucesso = False

    if "modo_criacao_template" not in st.session_state:
        st.session_state.modo_criacao_template = False

    if "search_text" not in st.session_state:
        st.session_state.search_text = ""

    # =====================
    # Título
    # =====================
    st.title("📚 Estud.IA")
    st.write("Ferramenta de Anotações de estudos e Preparação de Mapeamento Mental para IA")

    # =====================
    # Menu lateral
    # =====================
    st.sidebar.title("Menu")
    opcao = st.sidebar.radio(
        "",
        options=["Criar anotação", "Listar anotações", "Templates", "Exportar"]
    )

    # =====================
    # CRIAR ANOTAÇÃO
    # =====================
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

        if st.button("💾 Salvar Anotação"):
            try:
                note = Annotation(
                    tema=tema,
                    subtema=subtema,
                    nivel=nivel,
                    secoes={
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
                )

                service.create(note)
                st.session_state.salvo_com_sucesso = True
                st.rerun()

            except ValueError as e:
                st.warning(str(e))

    # =====================
    # LISTAR / EDITAR ANOTAÇÕES
    # =====================
    elif opcao == "Listar anotações":
        st.header("📄 Lista de anotações")

        def atualizar_busca():
            st.session_state.editando_id = None

        st.text_input(
            "Busque por uma anotação",
            key="search_text",
            on_change=atualizar_busca
        )

        if st.session_state.search_text.strip():
            data = service.search(st.session_state.search_text.strip())
        else:
            data = service.list_all()

        if not data:
            st.info("Nenhuma anotação cadastrada.")
        else:
            for note in data:
                with st.expander(f"{note.tema} - {note.subtema} ({note.nivel})"):
                    secoes = note.secoes

                    if st.session_state.editando_id != note.id:
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
                        render_lista("Erros comuns", secoes.get("erros_comuns", []))
                        render_lista("Perguntas", secoes.get("perguntas", []))
                        render_lista("Conexões", secoes.get("conexoes", []))

                        if st.button("✏️ Editar", key=f"edit_{note.id}"):
                            st.session_state.editando_id = note.id
                            st.rerun()

                    else:
                        o_que_e = st.text_area("O que é", secoes.get("o_que_e", ""), key=f"oque_{note.id}")
                        para_que = st.text_area("Para que serve", secoes.get("para_que_serve", ""), key=f"para_{note.id}")
                        quando_usar = st.text_area("Quando usar", secoes.get("quando_usar", ""), key=f"quando_{note.id}")
                        quando_nao_usar = st.text_area("Quando NÃO usar", secoes.get("quando_nao_usar", ""), key=f"nao_{note.id}")

                        conceitos_chave = st.text_area(
                            "Conceitos-chave (um por linha)",
                            "\n".join(secoes.get("conceitos_chave", [])),
                            key=f"conceitos_{note.id}"
                        )

                        erros = st.text_area(
                            "Erros comuns (um por linha)",
                            "\n".join(secoes.get("erros_comuns", [])),
                            key=f"erros_{note.id}"
                        )

                        perguntas = st.text_area(
                            "Perguntas (uma por linha)",
                            "\n".join(secoes.get("perguntas", [])),
                            key=f"perguntas_{note.id}"
                        )

                        conexoes = st.text_area(
                            "Conexões (uma por linha)",
                            "\n".join(secoes.get("conexoes", [])),
                            key=f"conexoes_{note.id}"
                        )

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            if st.button("⬅️ Cancelar", key=f"cancel_{note.id}"):
                                st.session_state.editando_id = None
                                st.rerun()

                        with col2:
                            if st.button("❌ Excluir", key=f"delete_{note.id}"):
                                service.delete(note.id)
                                st.session_state.editando_id = None
                                st.rerun()

                        with col3:
                            if st.button("💾 Salvar", key=f"save_{note.id}"):
                                note.secoes = {
                                    "o_que_e": o_que_e,
                                    "para_que_serve": para_que,
                                    "quando_usar": quando_usar,
                                    "quando_nao_usar": quando_nao_usar,
                                    "conceitos_chave": conceitos_chave.splitlines(),
                                    "erros_comuns": erros.splitlines(),
                                    "perguntas": perguntas.splitlines(),
                                    "conexoes": conexoes.splitlines()
                                }

                                service.update(note)
                                st.session_state.editando_id = None
                                st.success("Alterações salvas!")
                                st.rerun()

    # =====================
    # TEMPLATES
    # =====================
    elif opcao == "Templates":
        st.header("📋 Templates")

        if st.button("➕ Novo Template"):
            st.session_state.modo_criacao_template = True

        if st.session_state.modo_criacao_template:
            with st.form("form_criar_template"):
                nome = st.text_input("Nome do template")
                perguntas = st.text_area("Perguntas (uma por linha)")

                submitted = st.form_submit_button("💾 Salvar Template")

                if submitted:
                    try:
                        template = TemplateAnnotation(
                            nome=nome,
                            perguntas=perguntas.splitlines()
                        )

                        template_service.create(template)
                        st.session_state.modo_criacao_template = False
                        st.success("Template criado com sucesso!")
                        st.rerun()

                    except ValueError as e:
                        st.warning(str(e))

    # =====================
    # EXPORTAR
    # =====================
    elif opcao == "Exportar":
        st.header("📤 Exportar anotações")

        data = service.list_all()

        json_data = json.dumps(
            [vars(note) for note in data],
            indent=2,
            ensure_ascii=False
        )

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "📥 Baixar JSON",
                json_data,
                "annotations.json",
                "application/json"
            )

        from app.services.export_service import export_annotations_pdf

        with col2:
            if st.button("📄 Gerar PDF"):
                pdf_path = export_annotations_pdf(data)

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📥 Baixar PDF",
                        f,
                        "annotations.pdf",
                        "application/pdf"
                    )