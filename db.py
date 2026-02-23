
##Importar, criar Banco de Dados e abrir Cursor para comandos SQL

import sqlite3
DB_NAME = "anotacoes.db"

def get_connDB():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    return con

def check_Table():
    con = get_connDB()
    cur = con.cursor()

    #Cria a tabela caso não exista
    cur.execute("CREATE TABLE IF NOT EXISTS annotation(" \
    "id TEXT PRIMARY KEY NOT NULL, " \
    "tema VARCHAR(20) NOT NULL, " \
    "subtema VARCHAR(40) NOT NULL, " \
    "nivel VARCHAR(20) NOT NULL, " \
    "secoes TEXT);")

    con.commit()
    con.close()