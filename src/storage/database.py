"""
src/storage/database.py

Responsável por criar e gerenciar a conexão com o banco SQLite.
As funções de storage usam o context manager get_cursor() daqui, que
garante commit no sucesso, rollback em caso de erro e fechamento da
conexão mesmo quando uma exceção é levantada.
"""

import sqlite3
from contextlib import contextmanager
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


@contextmanager
def get_cursor():
    """
    Context manager para operações no banco.

    Garante, de forma única para leitura e escrita:
      - commit automático quando o bloco termina sem erro;
      - rollback automático se uma exceção for levantada;
      - fechamento da conexão em qualquer caso (bloco finally).

    Substitui o padrão anterior (conn = get_connection(); with conn: ...;
    conn.close()), no qual o close() ficava fora do with e podia não
    executar em caso de exceção, vazando a conexão.

    Uso:
        with get_cursor() as cur:
            cur.execute("INSERT INTO ...", (...))
            novo_id = cur.lastrowid
    """
    conn = get_connection()
    try:
        yield conn.cursor()
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def criar_tabelas():
    """
    Cria todas as tabelas do banco se ainda não existirem.
    Seguro para rodar múltiplas vezes (usa IF NOT EXISTS).
    """
    with get_cursor() as cur:
        cur.executescript("""
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

            CREATE TABLE IF NOT EXISTS desempenho_recall (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                topico         TEXT    NOT NULL DEFAULT 'geral',
                classificacao  TEXT    NOT NULL,  -- correta, parcial, incorreta
                criado_em      TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
            );
        """)


# Cria as tabelas automaticamente quando o módulo é importado
criar_tabelas()
