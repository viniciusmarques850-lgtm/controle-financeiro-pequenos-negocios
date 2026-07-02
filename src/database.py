import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'financeiro.db')

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lancamentos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao   TEXT    NOT NULL,
            valor       REAL    NOT NULL,
            tipo        TEXT    NOT NULL CHECK(tipo IN ('entrada', 'saida')),
            categoria   TEXT    NOT NULL,
            data        TEXT    NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados pronto.")

if __name__ == '__main__':
    criar_tabelas()