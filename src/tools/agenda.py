"""
src/tools/agenda.py

Formato das definições: Responses API (flat, sem wrapper "function").
As implementações Python não mudam.
"""

from datetime import date, timedelta
from src.storage import agenda as db


# ── Definições (formato Responses API) ───────────────────────────────────────

CONSULTAR_AGENDA_DEF = {
    "type": "function",
    "name": "consultar_agenda",
    "description": (
        "Consulta eventos da agenda acadêmica do estudante. "
        "Use quando o usuário perguntar o que tem hoje, amanhã, "
        "na semana, ou em uma data/período específico."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "periodo": {
                "type": "string",
                "enum": ["hoje", "amanha", "semana", "todos"],
                "description": (
                    "'hoje' = eventos de hoje, "
                    "'amanha' = eventos de amanhã, "
                    "'semana' = próximos 7 dias, "
                    "'todos' = todos os eventos cadastrados."
                ),
            },
            "data_especifica": {
                "type": "string",
                "description": (
                    "Data exata no formato YYYY-MM-DD. "
                    "Use quando o usuário mencionar uma data específica. "
                    "Se fornecido, ignora o campo 'periodo'."
                ),
            },
        },
        "required": [],
    },
}

ADICIONAR_AGENDA_DEF = {
    "type": "function",
    "name": "adicionar_agenda",
    "description": (
        "Adiciona um novo evento na agenda acadêmica do estudante. "
        "Use quando o usuário pedir para cadastrar aula, prova, trabalho ou qualquer evento."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "titulo": {
                "type": "string",
                "description": "Nome do evento (ex: 'Prova de Banco de Dados').",
            },
            "data": {
                "type": "string",
                "description": "Data do evento no formato YYYY-MM-DD.",
            },
            "hora": {
                "type": "string",
                "description": "Horário no formato HH:MM (opcional, ex: '14:00').",
            },
            "tipo": {
                "type": "string",
                "enum": ["aula", "prova", "evento"],
                "description": "Tipo do evento.",
            },
            "descricao": {
                "type": "string",
                "description": "Detalhes adicionais sobre o evento (opcional).",
            },
        },
        "required": ["titulo", "data"],
    },
}


# ── Implementações (sem alteração) ────────────────────────────────────────────

def consultar_agenda(periodo: str = "hoje", data_especifica: str = None) -> dict:
    hoje = date.today()

    if data_especifica:
        eventos = db.listar_eventos_por_data(data_especifica)
        label   = data_especifica
    elif periodo == "hoje":
        eventos = db.listar_eventos_hoje()
        label   = hoje.isoformat()
    elif periodo == "amanha":
        amanha  = (hoje + timedelta(days=1)).isoformat()
        eventos = db.listar_eventos_por_data(amanha)
        label   = amanha
    elif periodo == "semana":
        eventos = db.listar_eventos_semana()
        label   = f"{hoje.isoformat()} até {(hoje + timedelta(days=6)).isoformat()}"
    else:
        eventos = db.listar_todos_eventos()
        label   = "todos"

    return {"periodo": label, "total": len(eventos), "eventos": eventos}


def adicionar_agenda(
    titulo: str,
    data: str,
    hora: str = None,
    tipo: str = "evento",
    descricao: str = None,
) -> dict:
    evento = db.adicionar_evento(titulo=titulo, data=data, hora=hora, tipo=tipo, descricao=descricao)
    return {"ok": True, "evento": evento}
