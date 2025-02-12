import sqlite3

DATABASE_NAME = "membros.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Retorna os resultados como dicionário
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Criação da tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
