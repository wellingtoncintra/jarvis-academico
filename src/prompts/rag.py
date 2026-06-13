"""src/prompts/rag.py — Prompt de geração de resposta do RAG.

Usado pela tool buscar_material_rag (via retriever.responder) para gerar a
resposta final com base nos trechos recuperados dos materiais.
"""


def rag_resposta(pergunta: str, contexto: str) -> str:
    """Monta o prompt de geração de resposta a partir dos chunks recuperados."""
    return (
        "Responda em português usando apenas o contexto abaixo. "
        "Se não houver informação suficiente, diga: 'Não encontrado no contexto.'\n\n"
        f"Contexto:\n{contexto}\n\n"
        f"Pergunta: {pergunta}"
    )
