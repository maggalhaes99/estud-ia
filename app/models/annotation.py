import uuid

class Annotation:
    def __init__(self, tema, subtema, nivel, secoes=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.tema = tema
        self.subtema = subtema
        self.nivel = nivel
        self.secoes = secoes or {
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