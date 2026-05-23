"""
src/tools/tarefas.py

Tool de tarefas exposta ao agente:
  - gerenciar_tarefas → lista, adiciona ou conclui tarefas no SQLite

Uma única tool com o campo 'acao' para não sobrecarregar a LLM
com tools separadas para cada operação.
"""

from src.storage import tarefas as db


# ── Definição (schema para a LLM) ────────────────────────────────────────────

GERENCIAR_TAREFAS = {
    "type": "function",
    "function": {
        "name": "gerenciar_tarefas",
        "description": (
            "Gerencia a lista de tarefas acadêmicas do estudante. "
            "Use para listar tarefas pendentes ou todas, adicionar uma nova tarefa "
            "ou marcar uma tarefa como concluída."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "acao": {
                    "type": "string",
                    "enum": ["listar_pendentes", "listar_todas", "adicionar", "concluir"],
                    "description": (
                        "'listar_pendentes' = mostra tarefas não concluídas, "
                        "'listar_todas' = mostra todas incluindo concluídas, "
                        "'adicionar' = cria nova tarefa (requer 'descricao'), "
                        "'concluir' = marca tarefa como feita (requer 'tarefa_id' ou 'descricao_busca')."
                    ),
                },
                "descricao": {
                    "type": "string",
                    "description": (
                        "Texto da nova tarefa. "
                        "Obrigatório quando acao='adicionar'."
                    ),
                },
                "prazo": {
                    "type": "string",
                    "description": (
                        "Data limite no formato YYYY-MM-DD (opcional). "
                        "Usado quando acao='adicionar'."
                    ),
                },
                "prioridade": {
                    "type": "string",
                    "enum": ["alta", "media", "baixa"],
                    "description": (
                        "Prioridade da tarefa (padrão: 'media'). "
                        "Usado quando acao='adicionar'."
                    ),
                },
                "tarefa_id": {
                    "type": "integer",
                    "description": (
                        "ID numérico da tarefa a concluir. "
                        "Use quando o ID for conhecido. "
                        "Usado quando acao='concluir'."
                    ),
                },
                "descricao_busca": {
                    "type": "string",
                    "description": (
                        "Trecho do texto da tarefa para localizar pelo nome. "
                        "Usado quando acao='concluir' e o ID não for conhecido. "
                        "A tool busca a primeira tarefa pendente que contenha esse trecho."
                    ),
                },
            },
            "required": ["acao"],
        },
    },
}


# ── Implementação ─────────────────────────────────────────────────────────────

def gerenciar_tarefas(
    acao: str,
    descricao: str = None,
    prazo: str = None,
    prioridade: str = "media",
    tarefa_id: int = None,
    descricao_busca: str = None,
) -> dict:
    """
    Executa a ação solicitada sobre as tarefas.

    Retornos por ação:
        listar_pendentes / listar_todas →
            { "acao": str, "total": int, "tarefas": [...] }

        adicionar →
            { "acao": "adicionar", "ok": True, "tarefa": {...} }

        concluir →
            { "acao": "concluir", "ok": True/False, "tarefa": {...} | "erro": str }
    """

    # ── Listar ────────────────────────────────────────────────────────────────
    if acao == "listar_pendentes":
        tarefas = db.listar_tarefas_pendentes()
        return {"acao": acao, "total": len(tarefas), "tarefas": tarefas}

    if acao == "listar_todas":
        tarefas = db.listar_todas_tarefas()
        return {"acao": acao, "total": len(tarefas), "tarefas": tarefas}

    # ── Adicionar ─────────────────────────────────────────────────────────────
    if acao == "adicionar":
        if not descricao:
            return {
                "acao": acao,
                "ok":   False,
                "erro": "Campo 'descricao' é obrigatório para adicionar uma tarefa.",
            }
        tarefa = db.adicionar_tarefa(
            descricao=descricao,
            prazo=prazo,
            prioridade=prioridade,
        )
        return {"acao": acao, "ok": True, "tarefa": tarefa}

    # ── Concluir ──────────────────────────────────────────────────────────────
    if acao == "concluir":
        # Caso 1: ID fornecido diretamente
        if tarefa_id is not None:
            tarefa = db.concluir_tarefa(tarefa_id)
            if tarefa:
                return {"acao": acao, "ok": True, "tarefa": tarefa}
            return {
                "acao": acao,
                "ok":   False,
                "erro": f"Tarefa com id={tarefa_id} não encontrada.",
            }

        # Caso 2: busca por trecho do texto
        if descricao_busca:
            pendentes = db.listar_tarefas_pendentes()
            termo     = descricao_busca.lower()
            matches   = [t for t in pendentes if termo in t["descricao"].lower()]

            if not matches:
                return {
                    "acao": acao,
                    "ok":   False,
                    "erro": (
                        f"Nenhuma tarefa pendente encontrada com '{descricao_busca}'. "
                        "Use 'listar_pendentes' para ver os IDs disponíveis."
                    ),
                }

            # Conclui a primeira correspondência
            tarefa = db.concluir_tarefa(matches[0]["id"])
            return {"acao": acao, "ok": True, "tarefa": tarefa}

        return {
            "acao": acao,
            "ok":   False,
            "erro": "Forneça 'tarefa_id' ou 'descricao_busca' para concluir uma tarefa.",
        }

    return {"acao": acao, "ok": False, "erro": f"Ação desconhecida: '{acao}'."}
