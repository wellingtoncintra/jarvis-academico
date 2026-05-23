"""
src/tools/planejamento.py

Tool de planejamento de estudos — agrega agenda + tarefas + RAG
e devolve o contexto consolidado para a LLM gerar o plano.

Não gera o plano em texto aqui: isso é responsabilidade da LLM.
A tool monta o insumo; a LLM escreve o plano com base nele.
"""

from datetime import date, timedelta

from src.storage import agenda as db_agenda
from src.storage import tarefas as db_tarefas


# ── Definição (schema para a LLM) ────────────────────────────────────────────

PLANEJAR_ESTUDOS = {
    "type": "function",
    "function": {
        "name": "planejar_estudos",
        "description": (
            "Coleta o contexto acadêmico completo do estudante (eventos próximos, "
            "tarefas pendentes e sugestão de prioridades) para montar um plano de estudos. "
            "Use quando o usuário pedir um plano de estudos, quiser saber o que priorizar hoje "
            "ou pedir ajuda para organizar o tempo antes de uma prova."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "foco": {
                    "type": "string",
                    "description": (
                        "Tema ou evento específico para focar no plano "
                        "(ex: 'prova de IA na sexta', 'trabalho de BD'). "
                        "Opcional — se omitido, o plano cobre tudo que está pendente."
                    ),
                },
                "dias": {
                    "type": "integer",
                    "description": (
                        "Quantos dias à frente considerar na agenda (padrão: 7). "
                        "Use um valor menor para planos de curto prazo (ex: 1 para 'hoje')."
                    ),
                },
                "horas_disponiveis": {
                    "type": "number",
                    "description": "Horas disponíveis para estudar hoje (opcional).",
                },
            },
            "required": [],
        },
    },
}


# ── Implementação ─────────────────────────────────────────────────────────────

def planejar_estudos(
    foco: str = None,
    dias: int = 7,
    horas_disponiveis: float = None,
) -> dict:
    """
    Agrega agenda + tarefas pendentes e calcula prioridades básicas.

    Retorna um dicionário de contexto para a LLM usar ao gerar o plano:
        {
            "hoje": str,
            "foco": str | None,
            "horas_disponiveis": float | None,
            "eventos_proximos": [...],       ← próximos `dias` dias
            "tarefas_pendentes": [...],      ← ordenadas por prioridade e prazo
            "provas_proximas": [...],        ← subset de eventos do tipo 'prova'
            "tarefas_com_prazo_urgente": [...],  ← prazo nos próximos 3 dias
            "resumo": str,                   ← texto curto para a LLM saber o que usar
        }
    """
    hoje     = date.today()
    data_fim = (hoje + timedelta(days=dias)).isoformat()

    # ── Coleta de dados ───────────────────────────────────────────────────────
    eventos_proximos   = db_agenda.listar_eventos_por_periodo(hoje.isoformat(), data_fim)
    tarefas_pendentes  = db_tarefas.listar_tarefas_pendentes()

    # Filtra provas nos próximos `dias` dias
    provas_proximas = [
        e for e in eventos_proximos
        if e.get("tipo") == "prova"
    ]

    # Tarefas com prazo urgente (próximos 3 dias)
    limite_urgente = (hoje + timedelta(days=3)).isoformat()
    tarefas_urgentes = [
        t for t in tarefas_pendentes
        if t.get("prazo") and t["prazo"] <= limite_urgente
    ]

    # ── Resumo textual para orientar a LLM ───────────────────────────────────
    partes = []
    if provas_proximas:
        nomes = ", ".join(e["titulo"] for e in provas_proximas[:3])
        partes.append(f"{len(provas_proximas)} prova(s) próxima(s): {nomes}")
    if tarefas_urgentes:
        nomes = ", ".join(t["descricao"][:40] for t in tarefas_urgentes[:3])
        partes.append(f"{len(tarefas_urgentes)} tarefa(s) com prazo urgente: {nomes}")
    if not partes:
        partes.append("Nenhum evento ou prazo urgente nos próximos dias.")

    resumo = " | ".join(partes)
    if foco:
        resumo = f"Foco: {foco}. " + resumo

    return {
        "hoje":                     hoje.isoformat(),
        "foco":                     foco,
        "horas_disponiveis":        horas_disponiveis,
        "eventos_proximos":         eventos_proximos,
        "tarefas_pendentes":        tarefas_pendentes,
        "provas_proximas":          provas_proximas,
        "tarefas_com_prazo_urgente": tarefas_urgentes,
        "resumo":                   resumo,
    }
