"""
src/tools/planejamento.py — Responses API format.
"""

from datetime import date, timedelta
from src.storage import agenda as db_agenda
from src.storage import tarefas as db_tarefas


PLANEJAR_ESTUDOS_DEF = {
    "type": "function",
    "name": "planejar_estudos",
    "description": (
        "Coleta o contexto acadêmico completo do estudante (eventos próximos, "
        "tarefas pendentes e prioridades) para montar um plano de estudos. "
        "Use quando o usuário pedir um plano de estudos, quiser saber o que "
        "priorizar hoje ou precisar organizar o tempo antes de uma prova."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "foco": {
                "type": "string",
                "description": "Tema ou evento específico para focar (opcional).",
            },
            "dias": {
                "type": "integer",
                "description": "Quantos dias à frente considerar (padrão: 7).",
            },
            "horas_disponiveis": {
                "type": "number",
                "description": "Horas disponíveis para estudar hoje (opcional).",
            },
        },
        "required": [],
    },
}


def planejar_estudos(foco: str = None, dias: int = 7, horas_disponiveis: float = None) -> dict:
    hoje     = date.today()
    data_fim = (hoje + timedelta(days=dias)).isoformat()

    eventos_proximos  = db_agenda.listar_eventos_por_periodo(hoje.isoformat(), data_fim)
    tarefas_pendentes = db_tarefas.listar_tarefas_pendentes()

    provas_proximas  = [e for e in eventos_proximos if e.get("tipo") == "prova"]
    limite_urgente   = (hoje + timedelta(days=3)).isoformat()
    tarefas_urgentes = [t for t in tarefas_pendentes if t.get("prazo") and t["prazo"] <= limite_urgente]

    partes = []
    if provas_proximas:
        nomes = ", ".join(e["titulo"] for e in provas_proximas[:3])
        partes.append(f"{len(provas_proximas)} prova(s) próxima(s): {nomes}")
    if tarefas_urgentes:
        nomes = ", ".join(t["descricao"][:40] for t in tarefas_urgentes[:3])
        partes.append(f"{len(tarefas_urgentes)} tarefa(s) urgente(s): {nomes}")
    if not partes:
        partes.append("Nenhum evento ou prazo urgente nos próximos dias.")

    resumo = " | ".join(partes)
    if foco:
        resumo = f"Foco: {foco}. " + resumo

    return {
        "hoje":                      hoje.isoformat(),
        "foco":                      foco,
        "horas_disponiveis":         horas_disponiveis,
        "eventos_proximos":          eventos_proximos,
        "tarefas_pendentes":         tarefas_pendentes,
        "provas_proximas":           provas_proximas,
        "tarefas_com_prazo_urgente": tarefas_urgentes,
        "resumo":                    resumo,
    }
