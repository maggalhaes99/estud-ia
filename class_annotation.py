
import db
import json

db.check_Table()

class Annotation:

    def generateId(self):
        import uuid
        id = str(uuid.uuid4())

        return id

    def __init__(self, tema, subtema, nivel):
        self.id = self.generateId()
        self.tema = tema
        self.subtema = subtema
        self.nivel = nivel
        self.secoes = {
            "o_que_e": "",
            "para_que_serve": "",
            "quando_usar": "",
            "quando_nao_usar": "",
            "conceitos_chave": [],
            "exemplo_simples": "",
            "exemplo_pratico": "",
            "erros_comuns": [],
            "perguntas": [],
            "conexoes": []
        }
    
    def updateSecoes(self):
        con = db.get_connDB()
        cur = con.cursor()

        cur.execute("UPDATE annotation SET secoes = ? WHERE id = ?",
                    (json.dumps(self.secoes), self.id)
                    )
        
        con.commit()    
    
    def insertDB(self):
        con = db.get_connDB()
        cur = con.cursor()
        cur.execute("INSERT INTO annotation VALUES (?, ?, ?, ?, ?)", (
            self.id,
            self.tema,
            self.subtema,
            self.nivel,
            json.dumps(self.secoes)
        )
        )
        con.commit()

        res = cur.execute("SELECT * FROM annotation WHERE id = ?", (self.id,))
        query = res.fetchall()
        return query
    
    def deleteAnnotation(self):
        con = db.get_connDB()
        cur = con.cursor()

        id = f"{self.id}"

        cur.execute("DELETE FROM annotation WHERE id = ?", (
            id,
        )
        )
        con.commit()

        return "Apagado"