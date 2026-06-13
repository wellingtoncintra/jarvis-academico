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
        "tarefas pendentes, prioridades E trechos relevantes dos materiais de "
        "estudo) para montar um plano de estudos. "
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

    # ── Materiais (RAG) — 3ª fonte exigida pelo item 3.4 ──────────────────────
    # Consulta: o foco explícito ou, na ausência, os títulos das provas próximas.
    consulta_material = foco or " ".join(e["titulo"] for e in provas_proximas[:2])
    materiais_relevantes = []
    if consulta_material.strip():
        try:
            from src.rag.retriever import buscar_hibrido  # lazy: evita custo no import
            chunks = buscar_hibrido(consulta_material, k=3)
            materiais_relevantes = [
                {"fonte": c["fonte"], "trecho": c["texto"][:200]}
                for c in chunks
            ]
        except Exception:
            # Sem índices ou falha na busca: plano segue com agenda+tarefas.
            materiais_relevantes = []

    partes = []
    if provas_proximas:
        nomes = ", ".join(e["titulo"] for e in provas_proximas[:3])
        partes.append(f"{len(provas_proximas)} prova(s) próxima(s): {nomes}")
    if tarefas_urgentes:
        nomes = ", ".join(t["descricao"][:40] for t in tarefas_urgentes[:3])
        partes.append(f"{len(tarefas_urgentes)} tarefa(s) urgente(s): {nomes}")
    if materiais_relevantes:
        fontes = ", ".join(sorted({m["fonte"] for m in materiais_relevantes}))
        partes.append(f"materiais relevantes encontrados: {fontes}")
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
        "materiais_relevantes":      materiais_relevantes,
        "resumo":                    resumo,
    }
