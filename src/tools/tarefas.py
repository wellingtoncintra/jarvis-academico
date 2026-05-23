"""
src/tools/tarefas.py — Responses API format.
"""

from src.storage import tarefas as db


GERENCIAR_TAREFAS_DEF = {
    "type": "function",
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
                    "'listar_pendentes' = tarefas não concluídas, "
                    "'listar_todas' = todas incluindo concluídas, "
                    "'adicionar' = cria nova tarefa (requer 'descricao'), "
                    "'concluir' = marca como feita (requer 'tarefa_id' ou 'descricao_busca')."
                ),
            },
            "descricao": {
                "type": "string",
                "description": "Texto da nova tarefa. Obrigatório para acao='adicionar'.",
            },
            "prazo": {
                "type": "string",
                "description": "Data limite no formato YYYY-MM-DD (opcional).",
            },
            "prioridade": {
                "type": "string",
                "enum": ["alta", "media", "baixa"],
                "description": "Prioridade da tarefa (padrão: 'media').",
            },
            "tarefa_id": {
                "type": "integer",
                "description": "ID numérico da tarefa para acao='concluir'.",
            },
            "descricao_busca": {
                "type": "string",
                "description": (
                    "Trecho do nome da tarefa para localizar quando o ID não for conhecido. "
                    "Usado com acao='concluir'."
                ),
            },
        },
        "required": ["acao"],
    },
}


# ── Implementação (sem alteração) ─────────────────────────────────────────────

def gerenciar_tarefas(
    acao: str,
    descricao: str = None,
    prazo: str = None,
    prioridade: str = "media",
    tarefa_id: int = None,
    descricao_busca: str = None,
) -> dict:
    if acao == "listar_pendentes":
        tarefas = db.listar_tarefas_pendentes()
        return {"acao": acao, "total": len(tarefas), "tarefas": tarefas}

    if acao == "listar_todas":
        tarefas = db.listar_todas_tarefas()
        return {"acao": acao, "total": len(tarefas), "tarefas": tarefas}

    if acao == "adicionar":
        if not descricao:
            return {"acao": acao, "ok": False, "erro": "Campo 'descricao' é obrigatório."}
        tarefa = db.adicionar_tarefa(descricao=descricao, prazo=prazo, prioridade=prioridade)
        return {"acao": acao, "ok": True, "tarefa": tarefa}

    if acao == "concluir":
        if tarefa_id is not None:
            tarefa = db.concluir_tarefa(tarefa_id)
            if tarefa:
                return {"acao": acao, "ok": True, "tarefa": tarefa}
            return {"acao": acao, "ok": False, "erro": f"Tarefa id={tarefa_id} não encontrada."}

        if descricao_busca:
            pendentes = db.listar_tarefas_pendentes()
            matches   = [t for t in pendentes if descricao_busca.lower() in t["descricao"].lower()]
            if not matches:
                return {
                    "acao": acao, "ok": False,
                    "erro": f"Nenhuma tarefa pendente com '{descricao_busca}'. Use 'listar_pendentes' para ver os IDs.",
                }
            tarefa = db.concluir_tarefa(matches[0]["id"])
            return {"acao": acao, "ok": True, "tarefa": tarefa}

        return {"acao": acao, "ok": False, "erro": "Forneça 'tarefa_id' ou 'descricao_busca'."}

    return {"acao": acao, "ok": False, "erro": f"Ação desconhecida: '{acao}'."}
