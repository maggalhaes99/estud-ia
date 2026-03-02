import sqlite3

DB_NAME = "anotacoes.db"

def get_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS annotation (
                id TEXT PRIMARY KEY,
                tema TEXT NOT NULL,
                subtema TEXT NOT NULL,
                nivel TEXT NOT NULL,
                secoes TEXT
            );
        """)

        cur.execute("""        
            CREATE TABLE IF NOT EXISTS template_annotation (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                perguntas TEXT
            );""")