"""
src/storage/database.py

Responsável por criar e gerenciar a conexão com o banco SQLite.
Todas as outras funções de storage importam get_connection() daqui.
"""

import sqlite3
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Caminho do banco — usa o .env se definido, senão usa o padrão
DB_PATH = os.getenv("DB_PATH", "data/jarvis.db")


def get_connection() -> sqlite3.Connection:
    """
    Retorna uma conexão com o banco SQLite.
    Cria o arquivo e as tabelas automaticamente se não existirem.
    """
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    # Retorna linhas como dicionários (acesso por nome da coluna)
    conn.row_factory = sqlite3.Row

    # Ativa suporte a chaves estrangeiras
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def criar_tabelas():
    """
    Cria todas as tabelas do banco se ainda não existirem.
    Seguro para rodar múltiplas vezes (usa IF NOT EXISTS).
    """
    conn = get_connection()

    with conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS agenda (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo      TEXT    NOT NULL,
                data        TEXT    NOT NULL,  -- formato: YYYY-MM-DD
                hora        TEXT,              -- formato: HH:MM (opcional)
                tipo        TEXT    NOT NULL DEFAULT 'evento',
                                               -- valores: aula, prova, evento
                descricao   TEXT,
                criado_em   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
            );

            CREATE TABLE IF NOT EXISTS tarefas (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao   TEXT    NOT NULL,
                prazo       TEXT,              -- formato: YYYY-MM-DD (opcional)
                prioridade  TEXT    NOT NULL DEFAULT 'media',
                                               -- valores: alta, media, baixa
                concluida   INTEGER NOT NULL DEFAULT 0,  -- 0 = pendente, 1 = concluída
                criado_em   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
                concluido_em TEXT               -- preenchido ao marcar como concluída
            );
        """)

    conn.close()


# Cria as tabelas automaticamente quando o módulo é importado
criar_tabelas()
