import sqlite3
from pathlib import Path

DB_PATH = Path("encantaria.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    # Usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        senha TEXT,
        descricao TEXT,
        tipo_usuario TEXT,
        cidade TEXT,
        estado TEXT,
        categorias TEXT,
        portfolio TEXT,
        foto_url TEXT,
        data_criacao TEXT
    )
    """)

    # Anúncios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS anuncios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        titulo TEXT,
        descricao TEXT,
        categoria TEXT,
        tipo TEXT,
        cidade TEXT,
        estado TEXT,
        data_publicacao TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """)

    # Mensagens
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        remetente_id INTEGER,
        destinatario_id INTEGER,
        conteudo TEXT,
        data_envio TEXT,
        lida INTEGER DEFAULT 0,
        FOREIGN KEY(remetente_id) REFERENCES usuarios(id),
        FOREIGN KEY(destinatario_id) REFERENCES usuarios(id)
    )
    """)

    conn.commit()
    conn.close()

# Inicializa DB ao importar
init_db()
