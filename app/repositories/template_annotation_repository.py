import json
from app.db import get_connection
from app.models.template import TemplateAnnotation

class TemplateAnnotationRepository:

    def insert(self, template: TemplateAnnotation) -> None:
        with get_connection() as con:
            cur = con.cursor()
            cur.execute(
                """
                INSERT INTO template_annotation (id, nome, perguntas)
                VALUES (?, ?, ?)
                """,
                (
                    template.id,
                    template.nome,
                    json.dumps(template.perguntas),
                )
            )
            con.commit()

    def get_all(self) -> list[TemplateAnnotation]:
        with get_connection() as con:
            cur = con.cursor()
            rows = cur.execute(
                "SELECT id, nome, perguntas FROM template_annotation"
            ).fetchall()

        return [
            TemplateAnnotation(
                id=row["id"],
                nome=row["nome"],
                perguntas=json.loads(row["perguntas"]),
            )
            for row in rows
        ]