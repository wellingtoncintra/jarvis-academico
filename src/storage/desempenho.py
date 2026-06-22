"""
src/storage/desempenho.py

Persistência do desempenho do Active Recall.

Cada tentativa de recordação ativa é registrada com o tópico praticado e a
classificação atribuída pela avaliação (correta / parcial / incorreta). A
agregação por tópico alimenta a seção "dificuldades identificadas" da aba de
aprendizado, transformando feedback efêmero em histórico acionável.

Usa o context manager get_cursor() (database.py), com commit/rollback e
fechamento de conexão garantidos.
"""

from .database import get_cursor

# Classificações aceitas (normalizadas em minúsculas).
CLASSIFICACOES_VALIDAS = {"correta", "parcial", "incorreta"}


def registrar_tentativa(topico: str, classificacao: str) -> dict:
    """
    Registra uma tentativa de Active Recall.

    Parâmetros:
        topico        : tema praticado (se vazio, registrado como 'geral')
        classificacao : 'correta', 'parcial' ou 'incorreta'

    Retorna a tentativa registrada como dicionário. Classificações fora do
    conjunto válido são registradas como 'incorreta' por segurança, para não
    perder o sinal de que houve uma tentativa malsucedida de avaliação.
    """
    topico = (topico or "").strip() or "geral"
    classificacao = (classificacao or "").strip().lower()
    if classificacao not in CLASSIFICACOES_VALIDAS:
        classificacao = "incorreta"

    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO desempenho_recall (topico, classificacao) VALUES (?, ?)",
            (topico, classificacao),
        )
        tentativa_id = cur.lastrowid
        cur.execute("SELECT * FROM desempenho_recall WHERE id = ?", (tentativa_id,))
        row = cur.fetchone()

    return dict(row) if row else None


def resumo_por_topico() -> list[dict]:
    """
    Agrega o desempenho por tópico.

    Retorna uma lista de dicionários, um por tópico, ordenada do tópico com
    pior aproveitamento para o melhor (os "mais difíceis" primeiro). Cada item:

        {
            "topico":       str,
            "total":        int,   # tentativas no tópico
            "corretas":     int,
            "parciais":     int,
            "incorretas":   int,
            "aproveitamento": float  # (corretas + 0.5*parciais) / total, em %
        }
    """
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                topico,
                COUNT(*)                                                   AS total,
                SUM(CASE WHEN classificacao = 'correta'   THEN 1 ELSE 0 END) AS corretas,
                SUM(CASE WHEN classificacao = 'parcial'   THEN 1 ELSE 0 END) AS parciais,
                SUM(CASE WHEN classificacao = 'incorreta' THEN 1 ELSE 0 END) AS incorretas
            FROM desempenho_recall
            GROUP BY topico
            """
        )
        rows = [dict(r) for r in cur.fetchall()]

    for r in rows:
        total = r["total"] or 1
        # Acerto parcial conta como meio acerto.
        r["aproveitamento"] = round(100.0 * (r["corretas"] + 0.5 * r["parciais"]) / total, 1)

    # Mais difíceis primeiro: menor aproveitamento no topo; desempata por volume.
    rows.sort(key=lambda r: (r["aproveitamento"], -r["total"]))
    return rows


def total_tentativas() -> int:
    """Retorna o número total de tentativas registradas."""
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS n FROM desempenho_recall")
        row = cur.fetchone()
    return int(row["n"]) if row else 0


def limpar_desempenho() -> None:
    """Apaga todo o histórico de desempenho (usado pela ação de reset na UI)."""
    with get_cursor() as cur:
        cur.execute("DELETE FROM desempenho_recall")
