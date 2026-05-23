"""
src/storage/tarefas.py

Funções CRUD para a tabela de tarefas.
Usadas diretamente pelas tools do agente.
"""

from datetime import datetime
from .database import get_connection


# ─── CREATE ──────────────────────────────────────────────────────────────────

def adicionar_tarefa(
    descricao: str,
    prazo: str = None,
    prioridade: str = "media",
) -> dict:
    """
    Adiciona uma nova tarefa.

    Parâmetros:
        descricao : texto da tarefa (ex: "Estudar grafos para a prova")
        prazo     : data limite no formato YYYY-MM-DD, opcional
        prioridade: "alta", "media" ou "baixa"

    Retorna a tarefa criada como dicionário.
    """
    conn = get_connection()
    with conn:
        cursor = conn.execute(
            """
            INSERT INTO tarefas (descricao, prazo, prioridade)
            VALUES (?, ?, ?)
            """,
            (descricao, prazo, prioridade),
        )
        tarefa_id = cursor.lastrowid

    tarefa = buscar_tarefa_por_id(tarefa_id)
    conn.close()
    return tarefa


# ─── READ ─────────────────────────────────────────────────────────────────────

def buscar_tarefa_por_id(tarefa_id: int) -> dict | None:
    """Retorna uma tarefa pelo ID ou None se não encontrada."""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def listar_tarefas_pendentes() -> list[dict]:
    """
    Retorna todas as tarefas não concluídas,
    ordenadas por prioridade (alta → media → baixa) e prazo.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT * FROM tarefas
        WHERE concluida = 0
        ORDER BY
            CASE prioridade
                WHEN 'alta'  THEN 1
                WHEN 'media' THEN 2
                WHEN 'baixa' THEN 3
                ELSE 4
            END,
            prazo ASC NULLS LAST
        """
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def listar_tarefas_concluidas() -> list[dict]:
    """Retorna todas as tarefas já concluídas."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM tarefas WHERE concluida = 1 ORDER BY concluido_em DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def listar_todas_tarefas() -> list[dict]:
    """Retorna todas as tarefas (pendentes + concluídas)."""
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT * FROM tarefas
        ORDER BY concluida ASC,
            CASE prioridade
                WHEN 'alta'  THEN 1
                WHEN 'media' THEN 2
                WHEN 'baixa' THEN 3
                ELSE 4
            END,
            prazo ASC NULLS LAST
        """
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── UPDATE ──────────────────────────────────────────────────────────────────

def concluir_tarefa(tarefa_id: int) -> dict | None:
    """
    Marca uma tarefa como concluída e registra o horário.
    Retorna a tarefa atualizada ou None se não encontrada.
    """
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    with conn:
        conn.execute(
            """
            UPDATE tarefas
            SET concluida = 1, concluido_em = ?
            WHERE id = ?
            """,
            (agora, tarefa_id),
        )
    conn.close()
    return buscar_tarefa_por_id(tarefa_id)


def reabrir_tarefa(tarefa_id: int) -> dict | None:
    """Desfaz a conclusão de uma tarefa, voltando ao estado pendente."""
    conn = get_connection()
    with conn:
        conn.execute(
            """
            UPDATE tarefas
            SET concluida = 0, concluido_em = NULL
            WHERE id = ?
            """,
            (tarefa_id,),
        )
    conn.close()
    return buscar_tarefa_por_id(tarefa_id)


def atualizar_tarefa(tarefa_id: int, **campos) -> dict | None:
    """
    Atualiza campos de uma tarefa existente.

    Exemplo:
        atualizar_tarefa(2, prazo="2025-06-15", prioridade="alta")
    """
    if not campos:
        return buscar_tarefa_por_id(tarefa_id)

    colunas = ", ".join(f"{c} = ?" for c in campos)
    valores = list(campos.values()) + [tarefa_id]

    conn = get_connection()
    with conn:
        conn.execute(
            f"UPDATE tarefas SET {colunas} WHERE id = ?", valores
        )
    conn.close()
    return buscar_tarefa_por_id(tarefa_id)


# ─── DELETE ──────────────────────────────────────────────────────────────────

def remover_tarefa(tarefa_id: int) -> bool:
    """
    Remove uma tarefa pelo ID.
    Retorna True se removida, False se não encontrada.
    """
    conn = get_connection()
    with conn:
        cursor = conn.execute(
            "DELETE FROM tarefas WHERE id = ?", (tarefa_id,)
        )
    conn.close()
    return cursor.rowcount > 0
