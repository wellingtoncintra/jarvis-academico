"""src/prompts/aprendizado.py — Prompts das melhorias de aprendizado.

Cobre as três interações com a LLM da página de Melhoria de Aprendizagem:
geração de pergunta (Active Recall), avaliação da resposta do aluno e geração
de exercícios de múltipla escolha.
"""


# ── Active Recall: geração de pergunta ────────────────────────────────────────

RECALL_SYSTEM = (
    "Você é um tutor acadêmico. Gere perguntas de revisão (active recall) "
    "baseadas ESTRITAMENTE no contexto fornecido pelo material do aluno. "
    "Nunca use conhecimento externo ao contexto."
)


def recall_user(dificuldade: str, topico: str, contexto: str) -> str:
    """Monta a mensagem de usuário para gerar uma pergunta de active recall."""
    return (
        f"Com base apenas no contexto abaixo, gere UMA pergunta de nível "
        f"'{dificuldade.lower()}' sobre o tópico '{topico}'.\n\n"
        f"Responda APENAS com um JSON válido, sem texto antes ou depois, no formato:\n"
        f'{{"pergunta": "...", "gabarito": "..."}}\n\n'
        f"O gabarito deve ser a resposta correta e concisa, extraída do contexto.\n\n"
        f"Contexto:\n{contexto}"
    )


# ── Active Recall: avaliação da resposta ──────────────────────────────────────

AVALIACAO_SYSTEM = (
    "Você é um tutor que avalia respostas de estudantes de forma justa e "
    "construtiva, sempre em português brasileiro."
)


def avaliacao_user(pergunta: str, gabarito: str, resposta_aluno: str) -> str:
    """Monta a mensagem de usuário para avaliar a resposta do aluno."""
    return (
        f"Pergunta: {pergunta}\n"
        f"Gabarito (resposta correta): {gabarito}\n"
        f"Resposta do aluno: {resposta_aluno}\n\n"
        "Classifique a resposta do aluno como CORRETA, PARCIALMENTE CORRETA ou "
        "INCORRETA (escreva a classificação em maiúsculas no início) e, em "
        "seguida, dê um feedback curto e construtivo explicando o que faltou ou "
        "o que acertou. Seja direto."
    )


# ── Exercícios: geração de múltipla escolha ───────────────────────────────────

EXERCICIOS_SYSTEM = (
    "Você é um tutor acadêmico que cria exercícios de múltipla escolha "
    "baseados ESTRITAMENTE no material fornecido. Nunca use conhecimento "
    "externo ao contexto. Responda sempre em português brasileiro."
)


def exercicios_user(qtd: int, nivel: str, topico: str, contexto: str) -> str:
    """Monta a mensagem de usuário para gerar exercícios de múltipla escolha."""
    return (
        f"Com base apenas no contexto abaixo, crie {qtd} exercício(s) de "
        f"múltipla escolha de nível '{nivel.lower()}' sobre '{topico}'.\n\n"
        "Responda APENAS com um JSON válido, sem texto antes ou depois, no formato:\n"
        '{"questoes": [{"enunciado": "...", '
        '"alternativas": {"A": "...", "B": "...", "C": "...", "D": "..."}, '
        '"correta": "A", "explicacao": "..."}]}\n\n'
        "Cada questão deve ter exatamente 4 alternativas (A, B, C, D), uma única "
        "correta, e uma breve explicação da resposta certa extraída do contexto.\n\n"
        f"Contexto:\n{contexto}"
    )
