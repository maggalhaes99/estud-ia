import json
from app.db import get_connection
from app.models.annotation import Annotation

class AnnotationRepository:

    def insert(self, annotation: Annotation):
        with get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO annotation VALUES (?, ?, ?, ?, ?)
            """, (
                annotation.id,
                annotation.tema,
                annotation.subtema,
                annotation.nivel,
                json.dumps(annotation.secoes)
            ))

    def update_secoes(self, annotation: Annotation):
        with get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                UPDATE annotation SET secoes = ? WHERE id = ?
            """, (
                json.dumps(annotation.secoes),
                annotation.id
            ))

    def delete(self, annotation_id: str):
        with get_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM annotation WHERE id = ?", (annotation_id,))

    def get_all(self):
        with get_connection() as con:
            cur = con.cursor()
            rows = cur.execute("SELECT * FROM annotation").fetchall()

        return [
            Annotation(
                id=row["id"],
                tema=row["tema"],
                subtema=row["subtema"],
                nivel=row["nivel"],
                secoes=json.loads(row["secoes"])
            )
            for row in rows
        ]

    def search(self, text: str):
        query = f"%{text.lower()}%"
        with get_connection() as con:
            cur = con.cursor()
            rows = cur.execute("""
                SELECT * FROM annotation
                WHERE LOWER(tema) LIKE ?
                   OR LOWER(subtema) LIKE ?
                   OR LOWER(nivel) LIKE ?
                   OR LOWER(secoes) LIKE ?
            """, (query, query, query, query)).fetchall()

        return [
            Annotation(
                id=row["id"],
                tema=row["tema"],
                subtema=row["subtema"],
                nivel=row["nivel"],
                secoes=json.loads(row["secoes"])
            )
            for row in rows
        ]