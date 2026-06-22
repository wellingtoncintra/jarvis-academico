"""
src/storage/agenda.py

Funções CRUD para a tabela de agenda.
Usadas diretamente pelas tools do agente.

Todas as operações usam o context manager get_cursor() (em database.py),
que garante commit/rollback e fechamento da conexão mesmo em caso de erro.
"""

from datetime import date, timedelta
from .database import get_cursor


# ─── CREATE ──────────────────────────────────────────────────────────────────

def adicionar_evento(
    titulo: str,
    data: str,
    hora: str = None,
    tipo: str = "evento",
    descricao: str = None,
) -> dict:
    """
    Adiciona um evento na agenda.

    Parâmetros:
        titulo    : nome do evento (ex: "Prova de Cálculo")
        data      : no formato YYYY-MM-DD (ex: "2025-06-10")
        hora      : no formato HH:MM, opcional (ex: "14:00")
        tipo      : "aula", "prova" ou "evento"
        descricao : texto livre opcional

    Retorna o evento criado como dicionário.
    """
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO agenda (titulo, data, hora, tipo, descricao)
            VALUES (?, ?, ?, ?, ?)
            """,
            (titulo, data, hora, tipo, descricao),
        )
        evento_id = cur.lastrowid

    return buscar_evento_por_id(evento_id)


# ─── READ ─────────────────────────────────────────────────────────────────────

def buscar_evento_por_id(evento_id: int) -> dict | None:
    """Retorna um evento pelo ID ou None se não encontrado."""
    with get_cursor() as cur:
        cur.execute("SELECT * FROM agenda WHERE id = ?", (evento_id,))
        row = cur.fetchone()
    return dict(row) if row else None


def listar_eventos_por_data(data: str) -> list[dict]:
    """
    Lista todos os eventos de uma data específica.
    data: formato YYYY-MM-DD
    """
    with get_cursor() as cur:
        cur.execute(
            "SELECT * FROM agenda WHERE data = ? ORDER BY hora ASC NULLS LAST",
            (data,),
        )
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def listar_eventos_por_periodo(data_inicio: str, data_fim: str) -> list[dict]:
    """
    Lista eventos entre duas datas (inclusive).
    Datas no formato YYYY-MM-DD.
    """
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT * FROM agenda
            WHERE data BETWEEN ? AND ?
            ORDER BY data ASC, hora ASC NULLS LAST
            """,
            (data_inicio, data_fim),
        )
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def listar_eventos_hoje() -> list[dict]:
    """Atalho: retorna os eventos de hoje."""
    hoje = date.today().isoformat()  # ex: "2025-06-01"
    return listar_eventos_por_data(hoje)


def listar_eventos_semana() -> list[dict]:
    """Atalho: retorna os eventos dos próximos 7 dias (incluindo hoje)."""
    hoje = date.today()
    fim = hoje + timedelta(days=6)
    return listar_eventos_por_periodo(hoje.isoformat(), fim.isoformat())


def listar_todos_eventos() -> list[dict]:
    """Retorna todos os eventos ordenados por data."""
    with get_cursor() as cur:
        cur.execute(
            "SELECT * FROM agenda ORDER BY data ASC, hora ASC NULLS LAST"
        )
        rows = cur.fetchall()
    return [dict(r) for r in rows]


# ─── UPDATE ──────────────────────────────────────────────────────────────────

def atualizar_evento(evento_id: int, **campos) -> dict | None:
    """
    Atualiza campos de um evento existente.
    Passa apenas os campos que deseja alterar.

    Exemplo:
        atualizar_evento(3, hora="15:00", descricao="Sala 204")
    """
    if not campos:
        return buscar_evento_por_id(evento_id)

    colunas = ", ".join(f"{c} = ?" for c in campos)
    valores = list(campos.values()) + [evento_id]

    with get_cursor() as cur:
        cur.execute(f"UPDATE agenda SET {colunas} WHERE id = ?", valores)
    return buscar_evento_por_id(evento_id)


# ─── DELETE ──────────────────────────────────────────────────────────────────

def remover_evento(evento_id: int) -> bool:
    """
    Remove um evento pelo ID.
    Retorna True se removido, False se não encontrado.
    """
    with get_cursor() as cur:
        cur.execute("DELETE FROM agenda WHERE id = ?", (evento_id,))
        removido = cur.rowcount > 0
    return removido
