"""src/prompts/planejamento.py — Mensagem de geração de plano de estudos.

Diferente dos demais, este não é um system prompt: é a mensagem de usuário que a
aba Planejamento envia ao chat (via pending_message) para que a LLM acione a
tool planejar_estudos. Centralizado aqui para manter todos os prompts no mesmo lugar.
"""


def gerar_plano_mensagem(
    data_str: str,
    foco: str,
    horas: int,
    estilo: str,
    incluir: list[str],
    tarefas_pendentes: list[str],
    provas_proximas: list[str],
) -> str:
    """Monta a mensagem de usuário que dispara a geração do plano no chat."""
    return (
        f"Monte um plano de estudos para {data_str}. "
        f"Foco: {foco or 'geral'}. "
        f"Horas disponíveis: {horas}h. "
        f"Estilo: {estilo}. "
        f"Incluir: {', '.join(incluir)}. "
        f"Tarefas pendentes: {tarefas_pendentes[:5]}. "
        f"Próximas provas: {provas_proximas[:3]}."
    )
