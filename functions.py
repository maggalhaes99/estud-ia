import db
import json

db.check_Table()

def getAnnotation():
    con = db.get_connDB()
    cur = con.cursor()

    cur.execute("SELECT * FROM annotation")
    rows = cur.fetchall()

    export = []

    for row in rows:
        export.append({
            "id": row["id"],
            "tema": row["tema"],
            "subtema": row["subtema"],
            "nivel": row["nivel"],
            "secoes": json.loads(row["secoes"])
        })

    con.close()
    return export